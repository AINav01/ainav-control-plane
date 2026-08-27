"""Load and validate a tenant lockfile. Fail closed on unknown alg."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from agent_gov.hasher import (
    DEFAULT_ALG,
    DEFAULT_CANONICAL,
    HasherError,
    SCHEMA_VER,
    SUPPORTED_ALGS,
    policy_digest,
)

REQUIRED = ("schema_ver", "plane_version", "hash_alg", "canonical_ver", "flags")
FLAG_DEFAULTS = {
    "acrs_enforced": False,
    "sentinel_export": False,
    "halt_api": False,
    "genius_watch": False,
    "mica_emt_only": False,
    "travel_rule": False,
}
DEFAULT_TTL = 3600


def _read(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    if path.suffix in {".yaml", ".yml"}:
        try:
            import yaml  # type: ignore
        except ImportError as exc:
            raise HasherError("yaml_unavailable", str(exc)) from exc
        data = yaml.safe_load(text)
    else:
        data = json.loads(text)
    if not isinstance(data, dict):
        raise HasherError("lockfile_not_object", path.name)
    return data


def validate_lockfile(raw: dict[str, Any]) -> dict[str, Any]:
    missing = [k for k in REQUIRED if k not in raw]
    if missing:
        raise HasherError("lockfile_missing", ",".join(missing))
    if raw.get("schema_ver") != SCHEMA_VER:
        raise HasherError("lockfile_schema", str(raw.get("schema_ver")))
    if raw.get("hash_alg") not in SUPPORTED_ALGS:
        raise HasherError("unsupported_hash_alg", str(raw.get("hash_alg")))
    if raw.get("canonical_ver") != DEFAULT_CANONICAL:
        raise HasherError("unknown_canonical_ver", str(raw.get("canonical_ver")))
    flags = dict(FLAG_DEFAULTS)
    incoming = raw.get("flags") or {}
    unknown_flags = sorted(set(incoming) - set(FLAG_DEFAULTS))
    if unknown_flags:
        raise HasherError("unknown_lockfile_flag", ",".join(unknown_flags))
    flags.update(incoming)
    cut = dict(raw.get("cutover") or {})
    start, stop = cut.get("window_start"), cut.get("window_stop")
    if bool(start) != bool(stop):
        raise HasherError("cutover_window_incomplete", "both window bounds required")
    write_algs = cut.get("write_algs") or [raw["hash_alg"]]
    for alg in write_algs:
        if alg not in SUPPORTED_ALGS:
            raise HasherError("unsupported_hash_alg", str(alg))
    ttl = int(raw.get("ticket_ttl_seconds") or DEFAULT_TTL)
    if ttl <= 0:
        raise HasherError("lockfile_ttl", str(ttl))
    out = {
        "schema_ver": SCHEMA_VER,
        "plane_version": raw["plane_version"],
        "pack_id": raw.get("pack_id"),
        "pack_version": raw.get("pack_version"),
        "hash_alg": raw["hash_alg"],
        "canonical_ver": raw.get("canonical_ver") or DEFAULT_CANONICAL,
        "sig_alg": raw.get("sig_alg") or "none",
        "ticket_ttl_seconds": ttl,
        "allowlist": sorted(str(x) for x in (raw.get("allowlist") or [])),
        "flags": flags,
        "cutover": {
            "window_start": cut.get("window_start"),
            "window_stop": cut.get("window_stop"),
            "write_algs": list(write_algs),
        },
    }
    out["policy_digest"] = policy_digest(out, alg=DEFAULT_ALG)
    return out


def load_lockfile(path: str | Path) -> dict[str, Any]:
    return validate_lockfile(_read(Path(path)))


def default_lockfile() -> dict[str, Any]:
    return validate_lockfile(
        {
            "schema_ver": 1,
            "plane_version": "2.3.0",
            "hash_alg": DEFAULT_ALG,
            "canonical_ver": DEFAULT_CANONICAL,
            "sig_alg": "none",
            "ticket_ttl_seconds": DEFAULT_TTL,
            "allowlist": [],
            "flags": dict(FLAG_DEFAULTS),
            "cutover": {"window_start": None, "window_stop": None, "write_algs": [DEFAULT_ALG]},
        }
    )
