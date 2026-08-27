"""In-process dual seats. Not Redis. Not U-DUAL production."""
from __future__ import annotations

from agent_gov.hasher import HasherError


def require_dual(seat_a: str | None, seat_b: str | None) -> tuple[str, str]:
    a = (seat_a or "").strip()
    b = (seat_b or "").strip()
    if not a or not b:
        raise HasherError("ticket_incomplete", "seat_a and seat_b required")
    if a == b:
        raise HasherError("sod_denied", a)
    return a, b
