"""SoR idempotency key = request_id + action_hash. Not a Dynamics client."""
from __future__ import annotations

from agent_gov.hasher import HasherError


def idempotency_key(request_id: str, action_hash: str) -> str:
    if not request_id or not action_hash:
        raise HasherError("ticket_incomplete", "request_id and action_hash required")
    return f"{request_id}:{action_hash}"


class EffectLedger:
    def __init__(self) -> None:
        self._seen: set[str] = set()

    def effect(self, request_id: str, action_hash: str) -> str:
        key = idempotency_key(request_id, action_hash)
        if key in self._seen:
            raise HasherError("effect_replay", key)
        self._seen.add(key)
        return key
