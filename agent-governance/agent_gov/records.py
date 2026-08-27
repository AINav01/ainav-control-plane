"""Minimal DecisionRecord builder for plane MAJOR."""
from __future__ import annotations

import re
from datetime import datetime, timezone
from typing import Any

REASON_CODES = frozenset({
    "mutation_denied", "replay_denied", "policy_digest_mismatch",
    "cutover_ticket_voided", "hash_alg_mismatch", "untagged_digest",
    "ticket_expired", "ticket_incomplete",
    "halt_engaged", "allowlist_denied", "flag_not_implemented",
    "executed_after_dual_admit", "hold_pending_approval",
    "policy_escalate_dual", "fail_closed_exception",
})
_HASH_RE = re.compile(r"^(sha256|sha3-256):[0-9a-f]{64}$")
_PROTECTED = ("schema_version", "action_hash", "hash_alg", "canonical_ver", "hashes", "request_id")


def decision_record(
    *,
    decision: str,
    action_hash: str,
    reason_code: str,
    request_id: str | None = None,
    extra: dict[str, Any] | None = None,
    **_kwargs: Any,
) -> dict[str, Any]:
    raw = str(action_hash)
    h = raw if raw.startswith(("sha256:", "sha3-256:")) else f"sha256:{raw}"
    hash_alg = "sha3-256" if h.startswith("sha3-256:") else "sha256"
    rec: dict[str, Any] = {
        "schema_version": "1",
        "decision": decision,
        "reason_code": reason_code,
        "action_hash": h,
        "hash_alg": hash_alg,
        "canonical_ver": "v1",
        "hashes": {hash_alg: h},
        "sig_alg": "none",
        "signature": None,
        "request_id": request_id,
        "ts": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    }
    if extra:
        protected = {k: rec[k] for k in _PROTECTED}
        rec.update(extra)
        rec.update(protected)
    return rec


def validate_decision_record(rec: dict[str, Any]) -> list[str]:
    errs: list[str] = []
    for k in ("schema_version", "decision", "reason_code", "action_hash", "ts"):
        if k not in rec or rec[k] in (None, ""):
            errs.append(f"missing:{k}")
    if rec.get("schema_version") != "1":
        errs.append("schema_version")
    if rec.get("reason_code") not in REASON_CODES:
        errs.append(f"reason_code:{rec.get('reason_code')}")
    if not _HASH_RE.match(str(rec.get("action_hash") or "")):
        errs.append("action_hash_format")
    if rec.get("decision") not in ("allow", "deny", "escalate", "escalate_dual", "allow_with_obligations", "hold"):
        errs.append(f"decision:{rec.get('decision')}")
    hashes = rec.get("hashes") or {}
    if isinstance(hashes, dict) and rec.get("action_hash") and rec.get("hash_alg"):
        mapped = hashes.get(rec.get("hash_alg"))
        if mapped and mapped != rec.get("action_hash"):
            errs.append("hashes_action_hash_mismatch")
    return errs
