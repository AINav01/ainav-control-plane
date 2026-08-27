"""Plane hasher — SchemaVer 1.

One module. Packs do not hash Action bytes themselves.
Store tagged digests only: ``sha256:<64 hex>`` or ``sha3-256:<64 hex>``.
The prefix is metadata. It is never part of the hashed bytes.
"""
from __future__ import annotations

import hashlib
import hmac
import json
import re
from typing import Any, Iterable

SUPPORTED_ALGS = ("sha256", "sha3-256")
DEFAULT_ALG = "sha256"
DEFAULT_CANONICAL = "v1"
SCHEMA_VER = 1
TAGGED_RE = re.compile(r"^(sha256|sha3-256):[0-9a-f]{64}$")


class HasherError(ValueError):
    """Fail-closed hasher / cutover error. reason is a stable code."""

    def __init__(self, reason: str, detail: str = ""):
        self.reason = reason
        super().__init__(detail or reason)


def canonical_blob(action: dict[str, Any], canonical_ver: str = DEFAULT_CANONICAL) -> bytes:
    if canonical_ver != "v1":
        raise HasherError("unknown_canonical_ver", canonical_ver)
    core = {
        "actor_class": action.get("actor", {}).get("actor_class"),
        "resource_type": action.get("resource", {}).get("type"),
        "resource_id": action.get("resource", {}).get("id"),
        "resource_env": action.get("resource", {}).get("env"),
        "verb": action.get("verb"),
        "context": action.get("context") or {},
        "params": action.get("params") or {},
        "evidence": action.get("evidence") or {},
    }
    return json.dumps(core, sort_keys=True, separators=(",", ":"), default=str).encode("utf-8")


def _digest_hex(alg: str, blob: bytes) -> str:
    if alg == "sha256":
        return hashlib.sha256(blob).hexdigest()
    if alg == "sha3-256":
        return hashlib.sha3_256(blob).hexdigest()
    raise HasherError("unsupported_hash_alg", alg)


def tag(alg: str, hexdigest: str) -> str:
    if alg not in SUPPORTED_ALGS:
        raise HasherError("unsupported_hash_alg", alg)
    if not re.fullmatch(r"[0-9a-f]{64}", hexdigest or ""):
        raise HasherError("malformed_digest", hexdigest or "")
    return f"{alg}:{hexdigest}"


def parse_tagged(tagged: str) -> tuple[str, str]:
    if not tagged or ":" not in str(tagged):
        raise HasherError("untagged_digest", "bare hex is forbidden")
    if not TAGGED_RE.fullmatch(tagged):
        raise HasherError("malformed_tagged_digest", tagged)
    alg, hexdigest = tagged.split(":", 1)
    return alg, hexdigest


def coerce_tagged(value: str, *, default_alg: str = DEFAULT_ALG) -> str:
    if TAGGED_RE.fullmatch(value or ""):
        return value
    if re.fullmatch(r"[0-9a-f]{64}", value or ""):
        return tag(default_alg, value)
    raise HasherError("malformed_tagged_digest", value or "")


def hash_action(
    action: dict[str, Any],
    *,
    alg: str = DEFAULT_ALG,
    canonical_ver: str = DEFAULT_CANONICAL,
) -> str:
    return tag(alg, _digest_hex(alg, canonical_blob(action, canonical_ver)))


def verify_action(
    action: dict[str, Any],
    tagged: str,
    *,
    canonical_ver: str = DEFAULT_CANONICAL,
) -> bool:
    expected = hash_action(action, alg=parse_tagged(tagged)[0], canonical_ver=canonical_ver)
    return hmac.compare_digest(expected, tagged)


def hash_many(
    action: dict[str, Any],
    algs: Iterable[str],
    *,
    canonical_ver: str = DEFAULT_CANONICAL,
) -> dict[str, str]:
    out: dict[str, str] = {}
    for alg in algs:
        if alg not in SUPPORTED_ALGS:
            raise HasherError("unsupported_hash_alg", alg)
        out[alg] = hash_action(action, alg=alg, canonical_ver=canonical_ver)
    if not out:
        raise HasherError("empty_write_algs", "dual-write produced no digests")
    return out


LOCKFILE_DIGEST_FIELDS = (
    "hash_alg",
    "canonical_ver",
    "schema_ver",
    "plane_version",
    "pack_id",
    "pack_version",
    "flags",
    "allowlist",
    "sig_alg",
)


def policy_digest(lockfile: dict[str, Any], *, alg: str = DEFAULT_ALG) -> str:
    core = {k: lockfile.get(k) for k in LOCKFILE_DIGEST_FIELDS}
    core.setdefault("hash_alg", DEFAULT_ALG)
    core.setdefault("canonical_ver", DEFAULT_CANONICAL)
    core.setdefault("schema_ver", SCHEMA_VER)
    core.setdefault("flags", {})
    core.setdefault("allowlist", [])
    core.setdefault("sig_alg", "none")
    blob = b"ainav:v1:lockfile\n" + json.dumps(
        core, sort_keys=True, separators=(",", ":"), default=str
    ).encode("utf-8")
    return tag(alg, _digest_hex(alg, blob))


def consume_alg(ticket_hash_alg: str, ticket_tagged: str) -> str:
    tagged_alg, _ = parse_tagged(ticket_tagged)
    if ticket_hash_alg != tagged_alg:
        raise HasherError("ticket_alg_mismatch", f"{ticket_hash_alg} != {tagged_alg}")
    return ticket_hash_alg
