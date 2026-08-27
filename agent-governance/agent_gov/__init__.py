"""AINav plane 2.4 — hash tickets, gates, in-process dual seats."""

from agent_gov.action import canonical_action_hash, normalize_action
from agent_gov.effector import EffectLedger, idempotency_key
from agent_gov.hasher import HasherError, hash_action, verify_action
from agent_gov.ledger import ConsumeLedger
from agent_gov.lockfile import default_lockfile, load_lockfile
from agent_gov.plane import admit
from agent_gov.propose import admit_ticket, propose
from agent_gov.records import decision_record, validate_decision_record
from agent_gov.seats import require_dual

__version__ = "2.4.0"
__all__ = [
    "ConsumeLedger",
    "EffectLedger",
    "HasherError",
    "admit",
    "admit_ticket",
    "canonical_action_hash",
    "decision_record",
    "default_lockfile",
    "hash_action",
    "idempotency_key",
    "load_lockfile",
    "normalize_action",
    "propose",
    "require_dual",
    "validate_decision_record",
    "verify_action",
]
