"""Plane 2.2 facade. Hash layer only — not Redis dual consume."""
from __future__ import annotations

from datetime import datetime
from typing import Any, Mapping

from agent_gov.hasher import HasherError
from agent_gov.ledger import ConsumeLedger
from agent_gov.lockfile import default_lockfile
from agent_gov.propose import admit_ticket, propose
from agent_gov.records import decision_record


def admit(
    action: dict[str, Any],
    lockfile: dict[str, Any] | None = None,
    *,
    ticket: Mapping[str, Any] | None = None,
    ledger: ConsumeLedger,
    now: datetime | None = None,
) -> dict[str, Any]:
    lock = lockfile or default_lockfile()
    tkt = ticket or propose(action, lock, now=now)
    tagged = str(tkt.get("action_hash") or "")
    try:
        if ledger is None:
            raise HasherError("ticket_incomplete", "ledger required")
        admit_ticket(tkt, lock, action=action, now=now)
        ledger.consume(tagged)
        return decision_record(
            decision="hold",
            action_hash=tagged,
            reason_code="hold_pending_approval",
            extra={
                "policy_digest": tkt.get("policy_digest"),
                "hash_alg": tkt.get("hash_alg"),
                "canonical_ver": tkt.get("canonical_ver"),
            },
        )
    except HasherError as exc:
        reason = exc.reason if exc.reason in {
            "mutation_denied", "replay_denied", "policy_digest_mismatch",
            "cutover_ticket_voided", "hash_alg_mismatch", "untagged_digest",
            "ticket_expired", "ticket_incomplete",
        } else "fail_closed_exception"
        return decision_record(
            decision="deny",
            action_hash=tagged if tagged.startswith(("sha256:", "sha3-256:")) else "",
            reason_code=reason,
            extra={"error": exc.reason},
        )
