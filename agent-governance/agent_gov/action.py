"""Canonical Action + action_hash.

``canonical_action_hash`` returns untagged hex for historical callers.
New code should use ``agent_gov.hasher.hash_action`` (tagged).
Both share one blob.
"""
from __future__ import annotations

from typing import Any

from agent_gov.hasher import DEFAULT_ALG, DEFAULT_CANONICAL, hash_action, parse_tagged


def canonical_action_hash(action: dict[str, Any]) -> str:
    tagged = hash_action(action, alg=DEFAULT_ALG, canonical_ver=DEFAULT_CANONICAL)
    _, hexdigest = parse_tagged(tagged)
    return hexdigest


def normalize_action(raw: dict[str, Any]) -> dict[str, Any]:
    actor = raw.get("actor") or {}
    resource = raw.get("resource") or {}
    out = {
        "action_id": raw.get("action_id") or "unknown",
        "actor": {
            "actor_class": actor.get("actor_class") or "any_agent",
            "agent_instance": actor.get("agent_instance"),
            "on_behalf_of": actor.get("on_behalf_of"),
            "channel": actor.get("channel") or "api",
        },
        "resource": {
            "type": resource.get("type") or resource.get("resource_type"),
            "id": resource.get("id"),
            "env": resource.get("env"),
        },
        "verb": raw.get("verb"),
        "context": dict(raw.get("context") or {}),
        "evidence": dict(raw.get("evidence") or {}),
        "params": dict(raw.get("params") or {}),
    }
    if raw.get("rekor_uuid"):
        out["rekor_uuid"] = raw["rekor_uuid"]
    if raw.get("fulcio_identity"):
        out["fulcio_identity"] = raw["fulcio_identity"]
    return out
