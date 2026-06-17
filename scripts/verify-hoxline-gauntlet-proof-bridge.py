#!/usr/bin/env python3
"""Verify the HO-DET-001 Hoxline Gauntlet proof bridge."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
BRIDGE_JSON = ROOT / "proof" / "records" / "ho-det-001-hoxline-gauntlet-bridge-v1.json"
BRIDGE_MD = ROOT / "proof" / "records" / "HO-DET-001_HOXLINE_GAUNTLET_BRIDGE_V1.md"
MAP_JSON = ROOT / "proof" / "indexes" / "hoxline-gauntlet-proof-map-v1.json"
MAP_MD = ROOT / "proof" / "indexes" / "hoxline-gauntlet-proof-map-v1.md"

EXPECTED_ALLOWED_CLAIM = (
    "HO-DET-001 has Hoxline Gauntlet reviewer evidence and validation-bridge references "
    "under stated controlled scope."
)
REQUIRED_BLOCKED_CLAIMS = {
    "production ready",
    "runtime proven",
    "signal observed",
    "customer deployed",
    "SOCaaS deployed",
    "public-safe runtime proof",
    "AI approved",
    "analyst approved",
    "final authorization",
    "case closure",
}
REQUIRED_MISSING_EVIDENCE = {
    "runtime_evidence",
    "signal_observation_evidence",
    "public_safe_authorization",
    "human_review_gate_complete",
}
REQUIRED_FIELDS = {
    "artifact_id",
    "detection_id",
    "proof_bridge_kind",
    "bridge_owner",
    "supported_bounded_claim",
    "allowed_claim_wording",
    "blocked_claim_wording",
    "source_paths",
    "validation_bridge_reference",
    "hoxline_gauntlet_reference",
    "proof_ceiling",
    "proof_ceiling_statement",
    "public_safe",
    "public_safe_status",
    "human_review_required",
    "missing_evidence",
    "reviewer_commands",
    "website_rendering_boundary",
    "next_gate",
}
PROMOTION_TERMS = (
    "runtime proven",
    "signal observed",
    "production ready",
    "customer deployed",
    "socaas deployed",
    "public-safe runtime proof",
)
NEGATIVE_CONTEXT_MARKERS = (
    "blocked",
    "missing",
    "not ",
    "does not",
    "no ",
    "requires",
    "required",
    "without",
    "before",
)
STALE_WORK_BACKSLASH = "C:" + "\\Raylee\\Work"
STALE_WORK_SLASH = "C:" + "/Raylee/Work"


class VerificationError(Exception):
    """Proof bridge verification failure."""


def fail(message: str) -> None:
    raise VerificationError(message)


def _load_json(path: Path, label: str) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        fail(f"missing {label}: {path}")
    except json.JSONDecodeError as exc:
        fail(f"malformed {label}: {exc}")
    if not isinstance(data, dict):
        fail(f"{label} must be an object")
    return data


def load_bridge() -> dict[str, Any]:
    return _load_json(BRIDGE_JSON, "proof bridge JSON")


def load_map() -> dict[str, Any]:
    return _load_json(MAP_JSON, "proof map JSON")


def _require_repo_relative(value: str, label: str) -> None:
    path = Path(value)
    if path.is_absolute() or ".." in path.parts:
        fail(f"{label} must be repo-relative")


def _require_source_paths(paths: dict[str, Any]) -> None:
    required = {
        "hoxline_repo",
        "hoxline_gauntlet_output",
        "hoxline_gauntlet_schema",
        "hoxline_proofcard_example",
        "validation_bridge_json",
        "validation_bridge_markdown",
        "proof_record",
        "proof_map_json",
        "proof_map_markdown",
    }
    missing = sorted(required - paths.keys())
    if missing:
        fail(f"source_paths missing: {', '.join(missing)}")
    for field, value in paths.items():
        if not isinstance(value, str) or not value:
            fail(f"source_paths.{field} must be a non-empty string")
        if field != "hoxline_repo":
            _require_repo_relative(value, f"source_paths.{field}")


def validate_bridge(data: dict[str, Any], proof_map: dict[str, Any], texts: list[str] | None = None) -> dict[str, Any]:
    missing = sorted(REQUIRED_FIELDS - data.keys())
    if missing:
        fail(f"missing required fields: {', '.join(missing)}")
    if data["artifact_id"] != "HO-DET-001":
        fail("artifact_id mismatch")
    if data.get("bridge_record_id") != "HO-DET-001_HOXLINE_GAUNTLET_PROOF_BRIDGE_V1":
        fail("bridge_record_id mismatch")
    if data["detection_id"] != "HO-DET-001":
        fail("detection_id must be HO-DET-001")
    if data["public_safe"] is not False:
        fail("public_safe must be false")
    if data["public_safe_status"] not in {"BLOCKED", "NOT_PUBLIC_SAFE"}:
        fail("public_safe_status must remain blocked")
    if data["human_review_required"] is not True:
        fail("human_review_required must be true")
    if data["proof_ceiling"] != "CONTROLLED_TEST_VALIDATED":
        fail("proof_ceiling must be CONTROLLED_TEST_VALIDATED")
    if data["supported_bounded_claim"] != EXPECTED_ALLOWED_CLAIM:
        fail("supported bounded claim changed or broadened")
    if data["allowed_claim_wording"] != EXPECTED_ALLOWED_CLAIM:
        fail("allowed claim wording changed or broadened")

    blocked = set(data.get("blocked_claim_wording", []))
    missing_blocked = sorted(REQUIRED_BLOCKED_CLAIMS - blocked)
    if missing_blocked:
        fail(f"blocked claims incomplete: {', '.join(missing_blocked)}")

    missing_evidence = set(data.get("missing_evidence", []))
    missing_required_evidence = sorted(REQUIRED_MISSING_EVIDENCE - missing_evidence)
    if missing_required_evidence:
        fail(f"missing evidence list incomplete: {', '.join(missing_required_evidence)}")

    source_paths = data["source_paths"]
    if not isinstance(source_paths, dict):
        fail("source_paths must be an object")
    _require_source_paths(source_paths)
    validation_ref = data["validation_bridge_reference"]
    if not isinstance(validation_ref, dict) or not validation_ref.get("path"):
        fail("validation bridge reference absent")
    if validation_ref.get("artifact_id") != "HO-DET-001_HOXLINE_GAUNTLET_VALIDATION_BRIDGE_V1":
        fail("validation bridge artifact_id mismatch")

    website_boundary = data["website_rendering_boundary"]
    if not isinstance(website_boundary, dict):
        fail("website_rendering_boundary must be an object")
    if website_boundary.get("website_is_proof_authority") is not False:
        fail("website is treated as proof authority")
    if website_boundary.get("website_edits_required") is not False:
        fail("website edits must not be required")

    _validate_map(proof_map, data)
    _validate_positive_context(data)

    combined = json.dumps({"bridge": data, "map": proof_map}, sort_keys=True)
    if re.search(r"(?i)C:[\\/]+Raylee[\\/]+Work\b", combined):
        fail("stale C:\\Raylee\\Work path found")
    if texts:
        for text in texts:
            _validate_text_boundaries(text)

    return {
        "artifact_id": data["artifact_id"],
        "detection_id": data["detection_id"],
        "proof_ceiling": data["proof_ceiling"],
        "public_safe": data["public_safe"],
        "human_review_required": data["human_review_required"],
        "blocked_claims_verified": sorted(blocked),
    }


def _validate_map(proof_map: dict[str, Any], bridge: dict[str, Any]) -> None:
    if proof_map.get("artifact_id") != bridge["artifact_id"]:
        fail("proof map artifact_id must match bridge")
    if proof_map.get("detection_id") != bridge["detection_id"]:
        fail("proof map detection_id must match bridge")
    if proof_map.get("allowed_claim") != EXPECTED_ALLOWED_CLAIM:
        fail("proof map allowed claim changed or broadened")
    if proof_map.get("public_safe") is not False:
        fail("proof map public_safe must be false")
    if proof_map.get("human_review_required") is not True:
        fail("proof map human_review_required must be true")
    if proof_map.get("website_is_proof_authority") is not False:
        fail("proof map treats website as proof authority")
    missing_blocked = sorted(REQUIRED_BLOCKED_CLAIMS - set(proof_map.get("blocked_claims", [])))
    if missing_blocked:
        fail(f"proof map blocked claims incomplete: {', '.join(missing_blocked)}")


def _validate_positive_context(data: dict[str, Any]) -> None:
    positive_text = "\n".join(
        [
            str(data.get("supported_bounded_claim", "")),
            str(data.get("allowed_claim_wording", "")),
        ]
    ).lower()
    for term in PROMOTION_TERMS:
        if term in positive_text:
            fail(f"runtime/signal/prod/customer claim is supported: {term}")


def _validate_text_boundaries(text: str) -> None:
    if STALE_WORK_BACKSLASH in text or STALE_WORK_SLASH in text:
        fail("stale forbidden Raylee Work path found")
    current_section = ""
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if line.startswith("## "):
            current_section = line[3:].strip().lower()
            continue
        lower = line.lower()
        if "website" in lower and "proof authority" in lower and "not proof authority" not in lower:
            if not any(marker in lower for marker in NEGATIVE_CONTEXT_MARKERS):
                fail("website is treated as proof authority")
        for term in PROMOTION_TERMS:
            if term in lower and current_section not in {"blocked claims", "missing evidence", "proof ceiling"}:
                if not any(marker in lower for marker in NEGATIVE_CONTEXT_MARKERS):
                    fail(f"promotion term outside negative boundary context: {term}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify HO-DET-001 Hoxline Gauntlet proof bridge.")
    parser.add_argument("--format", choices=("text", "json"), default="text")
    args = parser.parse_args()

    try:
        texts = [
            BRIDGE_MD.read_text(encoding="utf-8"),
            MAP_MD.read_text(encoding="utf-8"),
        ]
        result = validate_bridge(load_bridge(), load_map(), texts)
    except VerificationError as exc:
        if args.format == "json":
            print(json.dumps({"status": "fail", "error": str(exc)}, indent=2))
        else:
            print(f"HOXLINE_GAUNTLET_PROOF_BRIDGE=fail: {exc}", file=sys.stderr)
        return 1

    if args.format == "json":
        print(json.dumps({"status": "pass", **result}, indent=2))
    else:
        print("HOXLINE_GAUNTLET_PROOF_BRIDGE=pass")
        print(f"ARTIFACT_ID={result['artifact_id']}")
        print(f"PROOF_CEILING={result['proof_ceiling']}")
        print("PUBLIC_SAFE=false")
        print("HUMAN_REVIEW_REQUIRED=true")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
