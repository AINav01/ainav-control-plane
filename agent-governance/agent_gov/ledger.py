"""In-process consume ledger. Replay of the same action_hash dies.

Not U-DUAL. Not multi-host. Production consume is Redis both-or-neither.
"""
from __future__ import annotations

from agent_gov.hasher import HasherError


class ConsumeLedger:
    def __init__(self) -> None:
        self._seen: set[str] = set()

    def consume(self, action_hash: str) -> None:
        if not action_hash:
            raise HasherError("ticket_incomplete", "action_hash required")
        if action_hash in self._seen:
            raise HasherError("replay_denied", action_hash)
        self._seen.add(action_hash)

    def seen(self, action_hash: str) -> bool:
        return action_hash in self._seen
