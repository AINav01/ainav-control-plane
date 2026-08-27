"""Lockfile gates evaluated at admit. Not dual consume."""
from __future__ import annotations

from typing import Any

from agent_gov.action import normalize_action
from agent_gov.hasher import HasherError

IMPLEMENTED_FLAGS = frozenset({"halt_api"})
ALLOWLIST_PARAM_KEYS = ("token", "token_id", "asset", "instrument", "coin", "stablecoin")


def enforce_gates(action: dict[str, Any], lockfile: dict[str, Any]) -> None:
    flags = lockfile.get("flags") or {}
    pending = sorted(k for k, on in flags.items() if on and k not in IMPLEMENTED_FLAGS)
    if pending:
        raise HasherError("flag_not_implemented", ",".join(pending))
    if flags.get("halt_api"):
        raise HasherError("halt_engaged", "halt_api flag is on")
    allow = list(lockfile.get("allowlist") or [])
    if not allow:
        return
    norm = normalize_action(action)
    params = norm.get("params") or {}
    resource = norm.get("resource") or {}
    candidates = {str(resource.get("id") or "")}
    for key in ALLOWLIST_PARAM_KEYS:
        candidates.add(str(params.get(key) or ""))
    candidates.discard("")
    if candidates.isdisjoint(set(allow)):
        raise HasherError("allowlist_denied", ",".join(sorted(candidates)) or "empty")
