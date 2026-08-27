"""SchemaVer 1 / plane 2.3."""
from __future__ import annotations

import json
import sys
import tempfile
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from agent_gov.action import normalize_action
from agent_gov.hasher import HasherError, hash_action, parse_tagged, policy_digest
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


def test_golden_file():
    path = ROOT / "data" / "golden" / "v1.json"
    assert path.is_file()
    data = json.loads(path.read_text(encoding="utf-8"))
    vec = data["vectors"][0]
    assert vec["expect"] == LOCKED
    assert hash_action(normalize_action(vec["action"])) == LOCKED


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
    assert ticket["request_id"] and ticket["expires_at"] and ticket["policy_digest"]
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


def test_missing_expires_is_incomplete():
    lock = default_lockfile()
    ticket = dict(propose(V1, lock))
    ticket.pop("expires_at")
    try:
        admit_ticket(ticket, lock, action=V1)
    except HasherError as exc:
        assert exc.reason == "ticket_incomplete"
        return
    raise AssertionError("missing expires_at must be incomplete")


def test_missing_digest_is_incomplete():
    lock = default_lockfile()
    ticket = dict(propose(V1, lock))
    ticket.pop("policy_digest")
    try:
        admit_ticket(ticket, lock, action=V1)
    except HasherError as exc:
        assert exc.reason == "ticket_incomplete"
        return
    raise AssertionError("missing digest must be incomplete")


def test_missing_request_id_is_incomplete():
    lock = default_lockfile()
    ticket = dict(propose(V1, lock))
    ticket.pop("request_id")
    try:
        admit_ticket(ticket, lock, action=V1)
    except HasherError as exc:
        assert exc.reason == "ticket_incomplete"
        return
    raise AssertionError("missing request_id must be incomplete")


def test_halt_engaged():
    lock = validate_lockfile({
        "schema_ver": 1, "plane_version": "2.3.0",
        "hash_alg": "sha256", "canonical_ver": "v1",
        "flags": {"halt_api": True},
    })
    rec = admit(V1, lock, ledger=ConsumeLedger())
    assert rec["decision"] == "deny"
    assert rec["reason_code"] == "halt_engaged"
    assert validate_decision_record(rec) == []


def test_flag_not_implemented():
    lock = validate_lockfile({
        "schema_ver": 1, "plane_version": "2.3.0",
        "hash_alg": "sha256", "canonical_ver": "v1",
        "flags": {"acrs_enforced": True},
    })
    rec = admit(V1, lock, ledger=ConsumeLedger())
    assert rec["decision"] == "deny"
    assert rec["reason_code"] == "flag_not_implemented"


def test_allowlist_denied():
    lock = validate_lockfile({
        "schema_ver": 1, "plane_version": "2.3.0",
        "hash_alg": "sha256", "canonical_ver": "v1",
        "flags": {}, "allowlist": ["USDC"],
    })
    rec = admit(V1, lock, ledger=ConsumeLedger())
    assert rec["reason_code"] == "allowlist_denied"


def test_allowlist_token_param():
    lock = validate_lockfile({
        "schema_ver": 1, "plane_version": "2.3.0",
        "hash_alg": "sha256", "canonical_ver": "v1",
        "flags": {}, "allowlist": ["USDC"],
    })
    action = dict(V1)
    action["params"] = dict(V1["params"], token="USDC")
    rec = admit(action, lock, ledger=ConsumeLedger())
    assert rec["decision"] == "hold"


def test_allowlist_ok():
    lock = validate_lockfile({
        "schema_ver": 1, "plane_version": "2.3.0",
        "hash_alg": "sha256", "canonical_ver": "v1",
        "flags": {}, "allowlist": ["pay_1001"],
    })
    rec = admit(V1, lock, ledger=ConsumeLedger())
    assert rec["decision"] == "hold"


def test_admit_without_ledger_denies():
    rec = admit(V1, default_lockfile(), ledger=None)
    assert rec["reason_code"] == "ticket_incomplete"
    assert rec["action_hash"] == LOCKED
    assert validate_decision_record(rec) == []


def test_ttl_moves_digest():
    a = validate_lockfile({
        "schema_ver": 1, "plane_version": "2.3.0",
        "hash_alg": "sha256", "canonical_ver": "v1",
        "flags": {}, "ticket_ttl_seconds": 3600,
    })
    b = validate_lockfile({
        "schema_ver": 1, "plane_version": "2.3.0",
        "hash_alg": "sha256", "canonical_ver": "v1",
        "flags": {}, "ticket_ttl_seconds": 60,
    })
    assert a["policy_digest"] != b["policy_digest"]
    assert policy_digest(a) == a["policy_digest"]


def test_sha3_window_writes_both():
    now = datetime(2027, 1, 15, tzinfo=timezone.utc)
    lock = validate_lockfile({
        "schema_ver": 1,
        "plane_version": "2.3.0",
        "hash_alg": "sha3-256",
        "canonical_ver": "v1",
        "flags": {},
        "cutover": {
            "window_start": "2027-01-01T00:00:00Z",
            "window_stop": "2027-02-01T00:00:00Z",
            "write_algs": ["sha256", "sha3-256"],
        },
    })
    ticket = propose(V1, lock, now=now)
    assert ticket["hashes"]["sha256"] == LOCKED
    assert admit_ticket(ticket, lock, action=V1, now=now) == "sha3-256"


def test_replay_ledger():
    lock = default_lockfile()
    book = ConsumeLedger()
    first = admit(V1, lock, ledger=book)
    assert first["decision"] == "hold" and first.get("request_id")
    second = admit(V1, lock, ledger=book)
    assert second["reason_code"] == "replay_denied"


def test_persist_ledger():
    lock = default_lockfile()
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "seen.json"
        first = admit(V1, lock, ledger=ConsumeLedger(path))
        assert first["decision"] == "hold"
        again = admit(V1, lock, ledger=ConsumeLedger(path))
        assert again["reason_code"] == "replay_denied"


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
        request_id="rid-1",
        extra={"action_hash": "sha256:" + "0" * 64, "request_id": "tamper"},
    )
    assert rec["action_hash"] == LOCKED
    assert rec["request_id"] == "rid-1"
    assert validate_decision_record(rec) == []


def test_example_json():
    path = ROOT / "data" / "lockfile.example.json"
    assert path.is_file()
    lf = load_lockfile(path)
    assert lf["hash_alg"] == "sha256"
    assert lf["plane_version"] == "2.3.0"
    assert lf["ticket_ttl_seconds"] == 3600


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_") and callable(fn):
            fn()
            print("ok", name)
    print("plane MAJOR tests passed")
