"""Bind Action to ticket. Packs must not assemble action_hash by hand."""
from __future__ import annotations

import hmac
from datetime import datetime, timedelta, timezone
from types import MappingProxyType
from typing import Any, Mapping

from agent_gov.action import normalize_action
from agent_gov.cutover import primary_hash, record_hashes, ticket_survives_flip
from agent_gov.hasher import HasherError, consume_alg, verify_action
from agent_gov.lockfile import default_lockfile


def _aware(now: datetime | None) -> datetime:
    t = now or datetime.now(timezone.utc)
    if t.tzinfo is None:
        t = t.replace(tzinfo=timezone.utc)
    return t


def propose(action: dict[str, Any], lockfile: dict[str, Any] | None = None, *, now: datetime | None = None) -> Mapping[str, Any]:
    lock = lockfile or default_lockfile()
    normalized = normalize_action(action)
    hashes = record_hashes(normalized, lock, now=now)
    tagged = primary_hash(hashes, lock)
    issued = _aware(now)
    ttl = int(lock.get("ticket_ttl_seconds") or 3600)
    expires = issued + timedelta(seconds=ttl)
    return MappingProxyType({
        "action_hash": tagged,
        "hash_alg": lock["hash_alg"],
        "canonical_ver": lock.get("canonical_ver") or "v1",
        "hashes": dict(hashes),
        "policy_digest": lock.get("policy_digest"),
        "plane_version": lock.get("plane_version"),
        "pack_id": lock.get("pack_id"),
        "pack_version": lock.get("pack_version"),
        "issued_at": issued.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "expires_at": expires.strftime("%Y-%m-%dT%H:%M:%SZ"),
    })


def admit_ticket(
    ticket: Mapping[str, Any],
    lockfile: dict[str, Any],
    *,
    action: dict[str, Any] | None = None,
    now: datetime | None = None,
) -> str:
    alg = ticket.get("hash_alg")
    tagged = ticket.get("action_hash")
    if not alg or not tagged:
        raise HasherError("ticket_incomplete", "hash_alg and action_hash required")
    exp = ticket.get("expires_at")
    if exp:
        try:
            deadline = datetime.fromisoformat(str(exp).replace("Z", "+00:00"))
        except ValueError as exc:
            raise HasherError("ticket_expired", "bad expires_at") from exc
        if deadline.tzinfo is None:
            deadline = deadline.replace(tzinfo=timezone.utc)
        if _aware(now) >= deadline:
            raise HasherError("ticket_expired", str(exp))
    if not ticket_survives_flip(str(alg), lockfile):
        raise HasherError("cutover_ticket_voided", str(alg))
    ticket_digest = ticket.get("policy_digest")
    lock_digest = lockfile.get("policy_digest")
    if ticket_digest and lock_digest and not hmac.compare_digest(str(ticket_digest), str(lock_digest)):
        raise HasherError("policy_digest_mismatch", "lockfile moved")
    if action is not None:
        if not verify_action(normalize_action(action), str(tagged), canonical_ver=str(ticket.get("canonical_ver") or "v1")):
            raise HasherError("mutation_denied", "action does not match ticket")
    return consume_alg(str(alg), str(tagged))
