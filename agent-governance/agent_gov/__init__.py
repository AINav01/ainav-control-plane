"""Agent Governance — AINav-shaped admission control (fixtures + multi-host ready)."""

from agent_gov.action import canonical_action_hash, normalize_action
from agent_gov.action_map import ActionMapper, default_bank_mapper
from agent_gov.client import (
    AdmitClient,
    AdmitError,
    DualSession,
    build_action,
    require_effect_ok,
)
from agent_gov.effect import EffectReceipt, apply_effect
from agent_gov.orchestrator import Orchestrator
from agent_gov.policy_engine import evaluate_policy, load_policy
from agent_gov.records import decision_record, validate_decision_record
from agent_gov.redis_consume import (
    RedisDualConsume,
    build_consume_keys,
    load_dual_consume_source,
    request_key,
    token_key,
)
from agent_gov.redis_errors import interpret_redis_reply, map_redis_err
from agent_gov.store import FileStore
from agent_gov.openfga_stub import OpenFGAStub, default_pilot_store, load_tuples_yaml

__version__ = "2.0.0"
__all__ = [
    "AdmitClient",
    "AdmitError",
    "DualSession",
    "build_action",
    "require_effect_ok",
    "ActionMapper",
    "default_bank_mapper",
    "EffectReceipt",
    "apply_effect",
    "RedisDualConsume",
    "build_consume_keys",
    "load_dual_consume_source",
    "request_key",
    "token_key",
    "map_redis_err",
    "interpret_redis_reply",
    "Orchestrator",
    "FileStore",
    "OpenFGAStub",
    "default_pilot_store",
    "load_tuples_yaml",
    "canonical_action_hash",
    "normalize_action",
    "evaluate_policy",
    "load_policy",
    "decision_record",
    "validate_decision_record",
]
