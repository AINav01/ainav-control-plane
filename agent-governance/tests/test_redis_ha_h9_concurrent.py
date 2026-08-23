"""
H9 concurrent dual-consume fixture.

Live Redis (REDIS_URL): parallel EVALSHA → exactly one ok.
Offline: parallel workers against a lock-serialized simulator
(mirrors Redis single-threaded script execution) → exactly one ok.

See docs/REDIS_HA_FIXTURES.md
"""
from __future__ import annotations

import os
import threading
import time
import uuid
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Any

import pytest

from agent_gov.lua_simulator import simulate_dual_consume
from agent_gov.redis_consume import (
    RedisDualConsume,
    build_consume_keys,
    request_key,
    seed_request_hash_fields,
    seed_token_hash_fields,
    token_key,
)
from agent_gov.redis_errors import interpret_redis_reply


WORKERS = int(os.environ.get("H9_WORKERS", "16"))
H9_HASH = "sha256:h9_concurrent_fixture"


def _seed_maps(rid: str, now: int) -> tuple[dict[str, str], list[dict[str, str]]]:
    req = seed_request_hash_fields(
        rid, H9_HASH, expires_at=now + 3600, required_n=2
    )
    tokens = [
        seed_token_hash_fields(
            rid, H9_HASH, "payments_ops", "ops@example.com", expires_at=now + 3600
        ),
        seed_token_hash_fields(
            rid, H9_HASH, "payments_risk", "risk@example.com", expires_at=now + 3600
        ),
    ]
    return req, tokens


class _SerializedSimulatorStore:
    """
    Thread-safe store: one lock around simulate_dual_consume.
    Models Redis: scripts do not interleave on one key's slot owner.
    """

    def __init__(self, request: dict[str, str], tokens: list[dict[str, str]], now: int):
        self._lock = threading.Lock()
        self.request = request
        self.tokens = tokens
        self.now = now

    def consume(self) -> dict[str, Any]:
        with self._lock:
            raw = simulate_dual_consume(self.request, self.tokens, H9_HASH, self.now)
            return interpret_redis_reply(raw)


def test_h9_concurrent_exactly_one_ok_serialized_simulator():
    """
    Offline H9 harness: N parallel consumes, serialized like Redis Lua.
    Expect exactly one ok; final state fully burned.
    """
    now = int(time.time())
    rid = f"h9_sim_{uuid.uuid4().hex[:12]}"
    req, tokens = _seed_maps(rid, now)
    store = _SerializedSimulatorStore(req, tokens, now)
    barrier = threading.Barrier(WORKERS)

    def worker() -> dict[str, Any]:
        barrier.wait(timeout=10)
        return store.consume()

    results: list[dict[str, Any]] = []
    with ThreadPoolExecutor(max_workers=WORKERS) as pool:
        futs = [pool.submit(worker) for _ in range(WORKERS)]
        for f in as_completed(futs):
            results.append(f.result())

    oks = [r for r in results if r.get("ok") is True]
    errs = [r for r in results if not r.get("ok")]
    assert len(results) == WORKERS
    assert len(oks) == 1, f"expected exactly one ok, got {len(oks)}: {results!r}"
    assert len(errs) == WORKERS - 1
    for e in errs:
        assert e.get("reason_code") in (
            "replay_denied",
            "token_consume_failed",
            "already_consumed",
        ) or e.get("error") in ("already_consumed", "token_used")
    assert req.get("consumed") == "1"
    assert all(t.get("used") == "1" for t in tokens)


def test_h9_keys_same_hash_tag():
    rid = "h9_slot_check"
    keys = build_consume_keys(rid, ["t1", "t2"])
    assert all(f"{{{rid}}}" in k for k in keys)
    assert keys[0] == request_key(rid)


@pytest.mark.redis_ha
def test_h9_concurrent_exactly_one_ok_live_redis():
    """
    Live H9: parallel RedisDualConsume.consume → exactly one ok.
    Requires REDIS_URL and redis-py. Skips otherwise.
    """
    url = os.environ.get("REDIS_URL", "").strip()
    if not url:
        pytest.skip("REDIS_URL not set — live H9 skipped")

    redis_mod = pytest.importorskip("redis")
    client = redis_mod.Redis.from_url(url, decode_responses=True)
    try:
        assert client.ping() is True
    except Exception as exc:
        pytest.skip(f"Redis unreachable: {exc}")

    now = int(time.time())
    rid = f"h9_live_{uuid.uuid4().hex[:12]}"
    tok_ids = ["t1", "t2"]
    rkey = request_key(rid)
    tkeys = [token_key(rid, tid) for tid in tok_ids]

    client.delete(rkey, *tkeys)

    req_fields = seed_request_hash_fields(
        rid, H9_HASH, expires_at=now + 3600, required_n=2
    )
    client.hset(rkey, mapping=req_fields)
    client.hset(
        tkeys[0],
        mapping=seed_token_hash_fields(
            rid, H9_HASH, "payments_ops", "ops@example.com", expires_at=now + 3600
        ),
    )
    client.hset(
        tkeys[1],
        mapping=seed_token_hash_fields(
            rid, H9_HASH, "payments_risk", "risk@example.com", expires_at=now + 3600
        ),
    )

    barrier = threading.Barrier(WORKERS)
    try:
        from agent_gov.redis_consume import load_dual_consume_source

        source = load_dual_consume_source()
    except FileNotFoundError:
        pytest.skip("dual_consume.lua not found")

    def worker() -> dict[str, Any]:
        c = redis_mod.Redis.from_url(url, decode_responses=True)
        rdc = RedisDualConsume(c, source=source)
        rdc.ensure_loaded()
        barrier.wait(timeout=15)
        return rdc.consume(rid, tok_ids, H9_HASH, now=now)

    results: list[dict[str, Any]] = []
    with ThreadPoolExecutor(max_workers=WORKERS) as pool:
        futs = [pool.submit(worker) for _ in range(WORKERS)]
        for f in as_completed(futs):
            results.append(f.result())

    oks = [r for r in results if r.get("ok") is True]
    assert len(oks) == 1, f"H9 live: expected 1 ok, got {len(oks)} results={results!r}"
    assert len(results) == WORKERS

    assert client.hget(rkey, "consumed") == "1"
    assert client.hget(tkeys[0], "used") == "1"
    assert client.hget(tkeys[1], "used") == "1"

    client.delete(rkey, *tkeys)
