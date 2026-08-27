"""Lockfile gates evaluated at admit. Not dual consume."""
from __future__ import annotations

from typing import Any

from agent_gov.action import normalize_action
from agent_gov.hasher import HasherError


def enforce_gates(action: dict[str, Any], lockfile: dict[str, Any]) -> None:
    flags = lockfile.get("flags") or {}
    if flags.get("halt_api"):
        raise HasherError("halt_engaged", "halt_api flag is on")
    allow = list(lockfile.get("allowlist") or [])
    if not allow:
        return
    norm = normalize_action(action)
    params = norm.get("params") or {}
    resource = norm.get("resource") or {}
    candidates = {
        str(resource.get("id") or ""),
        str(params.get("token") or ""),
        str(params.get("token_id") or ""),
        str(params.get("asset") or ""),
    }
    candidates.discard("")
    if candidates.isdisjoint(set(allow)):
        raise HasherError("allowlist_denied", ",".join(sorted(candidates)) or "empty")
