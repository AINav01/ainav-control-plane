"""Bind Action to ticket. Packs must not assemble action_hash by hand."""
from __future__ import annotations

import hmac
import uuid
from datetime import datetime, timedelta, timezone
from types import MappingProxyType
from typing import Any, Mapping

from agent_gov.action import normalize_action
from agent_gov.cutover import primary_hash, record_hashes, ticket_survives_flip
from agent_gov.gates import enforce_gates
from agent_gov.hasher import HasherError, consume_alg, verify_action
from agent_gov.lockfile import default_lockfile


def _aware(now: datetime | None) -> datetime:
    t = now or datetime.now(timezone.utc)
    if t.tzinfo is None:
        t = t.replace(tzinfo=timezone.utc)
    return t


def propose(action: dict[str, Any], lockfile: dict[str, Any] | None = None, *, now: datetime | None = None) -> Mapping[str, Any]:
    lock = lockfile or default_lockfile()
    if not lock.get("policy_digest"):
        raise HasherError("ticket_incomplete", "lockfile policy_digest required")
    enforce_gates(action, lock)
    normalized = normalize_action(action)
    hashes = record_hashes(normalized, lock, now=now)
    tagged = primary_hash(hashes, lock)
    issued = _aware(now)
    ttl = int(lock.get("ticket_ttl_seconds") or 3600)
    expires = issued + timedelta(seconds=ttl)
    return MappingProxyType({
        "request_id": str(uuid.uuid4()),
        "action_hash": tagged,
        "hash_alg": lock["hash_alg"],
        "canonical_ver": lock.get("canonical_ver") or "v1",
        "hashes": dict(hashes),
        "policy_digest": lock["policy_digest"],
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
    action: dict[str, Any],
    now: datetime | None = None,
) -> str:
    alg = ticket.get("hash_alg")
    tagged = ticket.get("action_hash")
    exp = ticket.get("expires_at")
    ticket_digest = ticket.get("policy_digest")
    lock_digest = lockfile.get("policy_digest")
    request_id = ticket.get("request_id")
    if not alg or not tagged:
        raise HasherError("ticket_incomplete", "hash_alg and action_hash required")
    if not exp:
        raise HasherError("ticket_incomplete", "expires_at required")
    if not request_id:
        raise HasherError("ticket_incomplete", "request_id required")
    if not ticket_digest or not lock_digest:
        raise HasherError("ticket_incomplete", "policy_digest required on ticket and lockfile")
    if action is None:
        raise HasherError("ticket_incomplete", "action required")
    try:
        deadline = datetime.fromisoformat(str(exp).replace("Z", "+00:00"))
    except ValueError as exc:
        raise HasherError("ticket_incomplete", "bad expires_at") from exc
    if deadline.tzinfo is None:
        deadline = deadline.replace(tzinfo=timezone.utc)
    if _aware(now) >= deadline:
        raise HasherError("ticket_expired", str(exp))
    if not ticket_survives_flip(str(alg), lockfile):
        raise HasherError("cutover_ticket_voided", str(alg))
    if not hmac.compare_digest(str(ticket_digest), str(lock_digest)):
        raise HasherError("policy_digest_mismatch", "lockfile moved")
    if not verify_action(normalize_action(action), str(tagged), canonical_ver=str(ticket.get("canonical_ver") or "v1")):
        raise HasherError("mutation_denied", "action does not match ticket")
    enforce_gates(action, lockfile)
    return consume_alg(str(alg), str(tagged))
