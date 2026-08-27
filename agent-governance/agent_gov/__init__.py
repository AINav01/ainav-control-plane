"""AINav plane MAJOR surface. Dual-admit Job C — hash / lockfile / tickets."""

from agent_gov.action import canonical_action_hash, normalize_action
from agent_gov.hasher import HasherError, hash_action, verify_action
from agent_gov.lockfile import default_lockfile, load_lockfile
from agent_gov.propose import admit_ticket, propose
from agent_gov.records import decision_record, validate_decision_record

__version__ = "2.1.0-plane-major"
__all__ = [
    "HasherError",
    "admit_ticket",
    "canonical_action_hash",
    "decision_record",
    "default_lockfile",
    "hash_action",
    "load_lockfile",
    "normalize_action",
    "propose",
    "validate_decision_record",
    "verify_action",
]
