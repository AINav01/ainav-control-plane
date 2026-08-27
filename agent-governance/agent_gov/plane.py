"""Plane 2.4 facade. Hash layer + optional in-process dual seats. Not Redis."""
from __future__ import annotations

from datetime import datetime
from typing import Any, Mapping

from agent_gov.hasher import HasherError, hash_action
from agent_gov.ledger import ConsumeLedger
from agent_gov.lockfile import default_lockfile
from agent_gov.propose import admit_ticket, propose
from agent_gov.records import decision_record
from agent_gov.seats import require_dual

_DENY = {
    "mutation_denied", "replay_denied", "policy_digest_mismatch",
    "cutover_ticket_voided", "hash_alg_mismatch", "untagged_digest",
    "ticket_expired", "ticket_incomplete", "halt_engaged",
    "allowlist_denied", "flag_not_implemented", "sod_denied", "effect_replay",
}


def _tagged_or_hash(action: dict[str, Any], tagged: str) -> str:
    if tagged.startswith(("sha256:", "sha3-256:")):
        return tagged
    return hash_action(action)


def admit(
    action: dict[str, Any],
    lockfile: dict[str, Any] | None = None,
    *,
    ticket: Mapping[str, Any] | None = None,
    ledger: ConsumeLedger | None = None,
    now: datetime | None = None,
    seat_a: str | None = None,
    seat_b: str | None = None,
) -> dict[str, Any]:
    lock = lockfile or default_lockfile()
    tagged = ""
    request_id = None
    try:
        if ledger is None:
            raise HasherError("ticket_incomplete", "ledger required")
        tkt = ticket or propose(action, lock, now=now)
        tagged = str(tkt.get("action_hash") or "")
        request_id = tkt.get("request_id")
        admit_ticket(tkt, lock, action=action, now=now)
        ledger.consume(tagged)
        extra = {
            "policy_digest": tkt.get("policy_digest"),
            "hash_alg": tkt.get("hash_alg"),
            "canonical_ver": tkt.get("canonical_ver"),
        }
        if seat_a is None and seat_b is None:
            reason = "hold_pending_approval"
        else:
            a, b = require_dual(seat_a, seat_b)
            extra["seats"] = [a, b]
            reason = "dual_consumed_pending_effector"
        return decision_record(
            decision="hold",
            action_hash=_tagged_or_hash(action, tagged),
            reason_code=reason,
            request_id=str(request_id) if request_id else None,
            extra=extra,
        )
    except HasherError as exc:
        reason = exc.reason if exc.reason in _DENY else "fail_closed_exception"
        return decision_record(
            decision="deny",
            action_hash=_tagged_or_hash(action, tagged),
            reason_code=reason,
            request_id=str(request_id) if request_id else None,
            extra={"error": exc.reason},
        )
