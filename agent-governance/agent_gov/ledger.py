"""Consume ledger keyed by action_hash (not request_id).

Same write cannot admit twice. New request_id does not reset replay.
Optional path persists across process restart. Still not U-DUAL / Redis.
"""
from __future__ import annotations

import json
from pathlib import Path

from agent_gov.hasher import HasherError


class ConsumeLedger:
    def __init__(self, path: str | Path | None = None) -> None:
        self._path = Path(path) if path else None
        self._seen: set[str] = set()
        if self._path and self._path.is_file():
            raw = json.loads(self._path.read_text(encoding="utf-8"))
            if not isinstance(raw, list):
                raise HasherError("ledger_corrupt", str(self._path))
            self._seen = {str(x) for x in raw}

    def consume(self, action_hash: str) -> None:
        if not action_hash:
            raise HasherError("ticket_incomplete", "action_hash required")
        if action_hash in self._seen:
            raise HasherError("replay_denied", action_hash)
        self._seen.add(action_hash)
        if self._path:
            self._path.parent.mkdir(parents=True, exist_ok=True)
            self._path.write_text(json.dumps(sorted(self._seen)), encoding="utf-8")

    def seen(self, action_hash: str) -> bool:
        return action_hash in self._seen
