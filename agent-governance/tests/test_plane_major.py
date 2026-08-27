"""SchemaVer 1 / plane 2.2 smoke."""
from __future__ import annotations

import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from agent_gov.action import normalize_action
from agent_gov.hasher import HasherError, hash_action, parse_tagged
from agent_gov.ledger import ConsumeLedger
from agent_gov.lockfile import default_lockfile, load_lockfile, validate_lockfile
from agent_gov.plane import admit
from agent_gov.propose import admit_ticket, propose
from agent_gov.records import decision_record, validate_decision_record

V1 = normalize_action({
    "action_id": "act_demo_001",
    "actor": {"actor_class": "payments_agent", "channel": "api", "agent_instance": "inst-9"},
    "resource": {"type": "bank.payment", "id": "pay_1001", "env": "lab"},
    "verb": "post",
    "params": {"amount": 1000, "currency": "USD", "beneficiary": "acct_9"},
    "context": {"channel": "agent"},
    "evidence": {"pack_id": "ev_1"},
    "rekor_uuid": "should-not-affect-hash",
})
LOCKED = "sha256:8d4a295b1dfb76f4169193012fdb7666fb199df66f45fe94c0bfe247648f4e10"


def test_v1():
    tagged = hash_action(V1)
    assert tagged == LOCKED
    alg, hx = parse_tagged(tagged)
    assert alg == "sha256" and len(hx) == 64


def test_untagged_rejected():
    try:
        parse_tagged(LOCKED.split(":", 1)[1])
    except HasherError as exc:
        assert exc.reason == "untagged_digest"
        return
    raise AssertionError("untagged must fail")


def test_propose_admit():
    lock = default_lockfile()
    ticket = propose(V1, lock)
    assert ticket["action_hash"] == LOCKED
    assert "expires_at" in ticket
    assert admit_ticket(ticket, lock, action=V1) == "sha256"
    mutated = dict(V1)
    mutated["params"] = dict(V1["params"], amount=1001)
    try:
        admit_ticket(ticket, lock, action=mutated)
    except HasherError as exc:
        assert exc.reason == "mutation_denied"
        return
    raise AssertionError("mutate must deny")


def test_ticket_expired():
    lock = default_lockfile()
    past = datetime.now(timezone.utc) - timedelta(hours=2)
    ticket = propose(V1, lock, now=past)
    try:
        admit_ticket(ticket, lock, action=V1)
    except HasherError as exc:
        assert exc.reason == "ticket_expired"
        return
    raise AssertionError("expired ticket must deny")


def test_replay_ledger():
    lock = default_lockfile()
    book = ConsumeLedger()
    first = admit(V1, lock, ledger=book)
    assert first["decision"] == "hold"
    second = admit(V1, lock, ledger=book)
    assert second["decision"] == "deny"
    assert second["reason_code"] == "replay_denied"


def test_lockfile_unknown_flag():
    try:
        validate_lockfile({
            "schema_ver": 1, "plane_version": "1.0.0",
            "hash_alg": "sha256", "canonical_ver": "v1",
            "flags": {"soft_dual": True},
        })
    except HasherError as exc:
        assert exc.reason == "unknown_lockfile_flag"
        return
    raise AssertionError("soft_dual must not load")


def test_record_integrity():
    rec = decision_record(
        decision="deny", action_hash=LOCKED, reason_code="mutation_denied",
        extra={"action_hash": "sha256:" + "0" * 64},
    )
    assert rec["action_hash"] == LOCKED
    assert validate_decision_record(rec) == []


def test_example_json():
    path = ROOT / "data" / "lockfile.example.json"
    if path.exists():
        lf = load_lockfile(path)
        assert lf["hash_alg"] == "sha256"


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_") and callable(fn):
            fn()
            print("ok", name)
    print("plane MAJOR tests passed")
