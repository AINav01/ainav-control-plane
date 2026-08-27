"""Dual-write window. New rows only. Never rewrite history."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from agent_gov.hasher import DEFAULT_ALG, HasherError, hash_many, parse_tagged


def _now(now: datetime | None) -> datetime:
    t = now or datetime.now(timezone.utc)
    if t.tzinfo is None:
        t = t.replace(tzinfo=timezone.utc)
    return t


def _parse(ts: str | None) -> datetime | None:
    if not ts:
        return None
    t = datetime.fromisoformat(str(ts).replace("Z", "+00:00"))
    if t.tzinfo is None:
        t = t.replace(tzinfo=timezone.utc)
    return t


def in_window(lockfile: dict[str, Any], *, now: datetime | None = None) -> bool:
    cut = lockfile.get("cutover") or {}
    start, stop = _parse(cut.get("window_start")), _parse(cut.get("window_stop"))
    if not start or not stop:
        return False
    return start <= _now(now) < stop


def write_algs(lockfile: dict[str, Any], *, now: datetime | None = None) -> list[str]:
    primary = lockfile.get("hash_alg") or DEFAULT_ALG
    cut = lockfile.get("cutover") or {}
    configured = list(cut.get("write_algs") or [primary])
    if in_window(lockfile, now=now):
        if primary not in configured:
            configured = [primary, *configured]
        return configured
    return [primary]


def record_hashes(action: Any, lockfile: dict[str, Any], *, now: datetime | None = None, canonical_ver: str | None = None) -> dict[str, str]:
    ver = canonical_ver or lockfile.get("canonical_ver") or "v1"
    hashes = hash_many(action, write_algs(lockfile, now=now), canonical_ver=ver)
    primary = lockfile.get("hash_alg") or DEFAULT_ALG
    if primary not in hashes:
        raise HasherError("primary_hash_missing", primary)
    return hashes


def primary_hash(hashes: dict[str, str], lockfile: dict[str, Any]) -> str:
    alg = lockfile.get("hash_alg") or DEFAULT_ALG
    tagged = hashes.get(alg)
    if not tagged:
        raise HasherError("primary_hash_missing", alg)
    parsed, _ = parse_tagged(tagged)
    if parsed != alg:
        raise HasherError("hashes_map_mismatch", parsed)
    return tagged


def ticket_survives_flip(ticket_hash_alg: str, lockfile: dict[str, Any]) -> bool:
    return ticket_hash_alg == (lockfile.get("hash_alg") or DEFAULT_ALG)
