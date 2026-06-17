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
    "HO-DET-001 has Hoxline Gauntlet v1 reviewer evidence and validation-bridge references "
    "under stated controlled scope."
)
EXPECTED_VALIDATION_ALLOWED_CLAIM = "HO-DET-001 has Hoxline Gauntlet v1 reviewer-path validation under controlled scope."
EXPECTED_MANIFEST = "examples/gauntlet/ho-det-001-gauntlet-v1-source-manifest.json"
EXPECTED_PRIMARY_MANIFEST = "HawkinsOperations/hoxline/" + EXPECTED_MANIFEST
EXPECTED_V1_RUN = "examples/gauntlet/ho-det-001-gauntlet-run-v1.json"
EXPECTED_V1_SCHEMA = "schemas/gauntlet-run-v1.schema.json"
EXPECTED_V0_RUN = "examples/gauntlet/ho-det-001-full-loop-run-v0.json"
EXPECTED_V0_SCHEMA = "schemas/gauntlet-full-loop-run-v0.schema.json"
REQUIRED_V1_SOURCE_PATHS = {
    "hoxline_gauntlet_run_v1": EXPECTED_V1_RUN,
    "hoxline_gauntlet_schema_v1": EXPECTED_V1_SCHEMA,
    "hoxline_overclaim_fixture_v1": "examples/gauntlet/ho-det-001-gauntlet-run-v1-overclaim.json",
    "hoxline_evidence_graph_v1": "examples/gauntlet/ho-det-001-evidence-graph-v1.json",
    "hoxline_proofcard_v1": "examples/gauntlet/ho-det-001-proofcard-v1.json",
    "hoxline_claim_decision_v1": "examples/gauntlet/ho-det-001-claim-decision-v1.json",
    "hoxline_gauntlet_doc_v1": "docs/gauntlet/HOXLINE_GAUNTLET_V1.md",
    "hoxline_proofcard_doc_v1": "docs/proofcards/PROOFCARD_V1.md",
    "hoxline_claim_authority_doc_v1": "docs/claim-authority/CLAIM_AUTHORITY_V1.md",
    "hoxline_evidence_graph_schema_v1": "schemas/evidence-graph-v1.schema.json",
    "hoxline_proofcard_schema_v1": "schemas/proofcard-v1.schema.json",
    "hoxline_claim_decision_schema_v1": "schemas/claim-authority-decision-v1.schema.json",
}
REQUIRED_HOXLINE_FILES = set(REQUIRED_V1_SOURCE_PATHS.values()) | {
    EXPECTED_MANIFEST,
    EXPECTED_V0_RUN,
    EXPECTED_V0_SCHEMA,
}
REQUIRED_REVIEWER_COMMANDS = {
    "python -B -m hoxline gauntlet verify --input examples/gauntlet/ho-det-001-gauntlet-run-v1.json --schema schemas/gauntlet-run-v1.schema.json",
    "python -B -m hoxline gauntlet summarize --input examples/gauntlet/ho-det-001-gauntlet-run-v1.json",
    "python -B -m hoxline claim-authority decide --input examples/gauntlet/ho-det-001-gauntlet-run-v1.json",
    "python -B -m hoxline proofcard render --input examples/gauntlet/ho-det-001-gauntlet-run-v1.json",
    "python -B -m hoxline gauntlet verify --input examples/gauntlet/ho-det-001-gauntlet-run-v1-overclaim.json --schema schemas/gauntlet-run-v1.schema.json",
    "python -B -m hoxline gauntlet verify --input examples/gauntlet/ho-det-001-full-loop-run-v0.json --schema schemas/gauntlet-full-loop-run-v0.schema.json",
}
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
    "analyst_review_record",
    "case_closure_record",
    "customer_deployment_evidence",
    "deployment_evidence",
    "final_authorization_record",
    "human_review_gate_complete",
    "public_safe_authorization",
    "runtime_evidence",
    "service_deployment_evidence",
    "signal_observation_evidence",
}
REQUIRED_FIELDS = {
    "artifact_id",
    "bridge_record_id",
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
    "cross_repo_consistency",
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
    "compatibility",
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


def validate_bridge(
    data: dict[str, Any],
    proof_map: dict[str, Any],
    texts: list[str] | None = None,
    hoxline_root: Path | None = None,
) -> dict[str, Any]:
    missing = sorted(REQUIRED_FIELDS - data.keys())
    if missing:
        fail(f"missing required fields: {', '.join(missing)}")
    if data["artifact_id"] != "HO-DET-001":
        fail("artifact_id mismatch")
    if data["bridge_record_id"] != "HO-DET-001_HOXLINE_GAUNTLET_PROOF_BRIDGE_V1":
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
    if data["next_gate"] != "human_review_gate":
        fail("next_gate must be human_review_gate")

    blocked = set(data.get("blocked_claim_wording", []))
    missing_blocked = sorted(REQUIRED_BLOCKED_CLAIMS - blocked)
    if missing_blocked:
        fail(f"blocked claims incomplete: {', '.join(missing_blocked)}")

    missing_evidence = set(data.get("missing_evidence", []))
    missing_required_evidence = sorted(REQUIRED_MISSING_EVIDENCE - missing_evidence)
    if missing_required_evidence:
        fail(f"missing evidence list incomplete: {', '.join(missing_required_evidence)}")

    _validate_source_paths(data["source_paths"])
    _validate_validation_reference(data["validation_bridge_reference"])
    _validate_hoxline_reference(data["hoxline_gauntlet_reference"])
    _validate_map(proof_map, data)
    _validate_cross_repo(data["cross_repo_consistency"])
    _validate_website_boundary(data["website_rendering_boundary"])
    _validate_reviewer_commands(data)
    _validate_positive_context(data)
    _validate_no_forbidden_paths({"bridge": data, "map": proof_map})

    if hoxline_root is not None:
        _validate_hoxline_files_exist(hoxline_root)

    if texts:
        combined_text = "\n".join(texts)
        for text in texts:
            _validate_text_boundaries(text)
        for required in set(REQUIRED_V1_SOURCE_PATHS.values()) | {EXPECTED_MANIFEST, EXPECTED_V0_RUN, EXPECTED_V0_SCHEMA}:
            if required not in combined_text:
                fail(f"text missing Hoxline source route: {required}")

    return {
        "artifact_id": data["artifact_id"],
        "detection_id": data["detection_id"],
        "proof_ceiling": data["proof_ceiling"],
        "public_safe": data["public_safe"],
        "human_review_required": data["human_review_required"],
        "source_manifest_path": data["source_paths"]["source_manifest_path"],
        "primary_v1_run_path": data["source_paths"]["hoxline_gauntlet_run_v1"],
        "primary_v1_schema_path": data["source_paths"]["hoxline_gauntlet_schema_v1"],
        "blocked_claims_verified": sorted(blocked),
    }


def _validate_source_paths(paths: Any) -> None:
    if not isinstance(paths, dict):
        fail("source_paths must be an object")
    if paths.get("hoxline_repo") != "HawkinsOperations/hoxline":
        fail("source_paths.hoxline_repo must be HawkinsOperations/hoxline")
    if paths.get("hoxline_primary_source_manifest") != EXPECTED_PRIMARY_MANIFEST:
        fail("primary Hoxline source manifest must use HawkinsOperations/hoxline")
    if paths.get("source_manifest_path") != EXPECTED_MANIFEST:
        fail("source manifest path absent")
    if paths.get("hoxline_primary_v1_run_path") != "HawkinsOperations/hoxline/" + EXPECTED_V1_RUN:
        fail("primary Hoxline v1 run path absent")
    for field, expected in REQUIRED_V1_SOURCE_PATHS.items():
        if paths.get(field) != expected:
            fail(f"source_paths.{field} must be {expected}")
        _require_repo_relative(expected, f"source_paths.{field}")
    for required in ("validation_bridge_json", "validation_bridge_markdown", "proof_record", "proof_map_json", "proof_map_markdown"):
        value = paths.get(required)
        if not isinstance(value, str) or not value:
            fail(f"source_paths.{required} must be present")
        _require_repo_relative(value, f"source_paths.{required}")
    compatibility = paths.get("compatibility_v0_paths")
    if not isinstance(compatibility, dict):
        fail("compatibility_v0_paths must be an object")
    if compatibility.get("compatibility_role") != "compatibility-only; not primary proof authority":
        fail("v0 paths must be compatibility-only")
    if compatibility.get("gauntlet_run") != EXPECTED_V0_RUN or compatibility.get("gauntlet_schema") != EXPECTED_V0_SCHEMA:
        fail("v0 compatibility paths are incomplete")


def _validate_validation_reference(validation_ref: Any) -> None:
    if not isinstance(validation_ref, dict) or not validation_ref.get("path"):
        fail("validation bridge reference absent")
    if validation_ref.get("artifact_id") != "HO-DET-001_HOXLINE_GAUNTLET_VALIDATION_BRIDGE_V1":
        fail("validation bridge artifact_id mismatch")
    if validation_ref.get("allowed_claim") != EXPECTED_VALIDATION_ALLOWED_CLAIM:
        fail("validation bridge allowed claim mismatch")


def _validate_hoxline_reference(reference: Any) -> None:
    if not isinstance(reference, dict):
        fail("hoxline_gauntlet_reference must be an object")
    expected = {
        "source_manifest_path": EXPECTED_MANIFEST,
        "path": EXPECTED_V1_RUN,
        "schema": EXPECTED_V1_SCHEMA,
        "overclaim_fixture": "examples/gauntlet/ho-det-001-gauntlet-run-v1-overclaim.json",
        "proofcard": "examples/gauntlet/ho-det-001-proofcard-v1.json",
        "claim_authority_decision": "examples/gauntlet/ho-det-001-claim-decision-v1.json",
    }
    for field, value in expected.items():
        if reference.get(field) != value:
            fail(f"hoxline_gauntlet_reference.{field} must be {value}")
    if reference.get("repo") != "HawkinsOperations/hoxline":
        fail("hoxline_gauntlet_reference.repo must be HawkinsOperations/hoxline")
    if reference.get("primary_source_manifest") != EXPECTED_PRIMARY_MANIFEST:
        fail("hoxline_gauntlet_reference primary source manifest mismatch")
    if "ho-det-001-gauntlet-run-v1.json" not in reference.get("cli_verifier_command", ""):
        fail("v1 CLI verifier command missing")


def _validate_map(proof_map: dict[str, Any], bridge: dict[str, Any]) -> None:
    if proof_map.get("artifact_id") != bridge["artifact_id"]:
        fail("proof map artifact_id must match bridge")
    if proof_map.get("detection_id") != bridge["detection_id"]:
        fail("proof map detection_id must match bridge")
    if proof_map.get("allowed_claim") != EXPECTED_ALLOWED_CLAIM:
        fail("proof map allowed claim changed or broadened")
    if proof_map.get("hoxline_source_manifest") != EXPECTED_PRIMARY_MANIFEST:
        fail("proof map source manifest mismatch")
    if proof_map.get("hoxline_primary_v1_run_path") != "HawkinsOperations/hoxline/" + EXPECTED_V1_RUN:
        fail("proof map primary v1 run path mismatch")
    if proof_map.get("hoxline_primary_v1_schema_path") != EXPECTED_V1_SCHEMA:
        fail("proof map primary v1 schema path mismatch")
    if proof_map.get("public_safe") is not False:
        fail("proof map public_safe must be false")
    if proof_map.get("human_review_required") is not True:
        fail("proof map human_review_required must be true")
    if proof_map.get("website_is_proof_authority") is not False:
        fail("proof map treats website as proof authority")
    if proof_map.get("next_gate") != "human_review_gate":
        fail("proof map next_gate mismatch")
    compatibility = proof_map.get("v0_compatibility_reference")
    if not isinstance(compatibility, dict) or compatibility.get("compatibility_only") is not True:
        fail("proof map v0 route must be compatibility-only")
    missing_blocked = sorted(REQUIRED_BLOCKED_CLAIMS - set(proof_map.get("blocked_claims", [])))
    if missing_blocked:
        fail(f"proof map blocked claims incomplete: {', '.join(missing_blocked)}")
    if set(proof_map.get("missing_evidence", [])) != REQUIRED_MISSING_EVIDENCE:
        fail("proof map missing evidence mismatch")


def _validate_cross_repo(cross: Any) -> None:
    if not isinstance(cross, dict):
        fail("cross_repo_consistency must be an object")
    expected = {
        "artifact_id": "HO-DET-001",
        "detection_id": "HO-DET-001",
        "hoxline_primary_source_manifest": EXPECTED_PRIMARY_MANIFEST,
        "hoxline_primary_v1_run_path": "HawkinsOperations/hoxline/" + EXPECTED_V1_RUN,
        "hoxline_primary_v1_schema_path": EXPECTED_V1_SCHEMA,
        "source_manifest_path": EXPECTED_MANIFEST,
        "proof_ceiling": "CONTROLLED_TEST_VALIDATED",
        "validation_allowed_claim": EXPECTED_VALIDATION_ALLOWED_CLAIM,
        "proof_allowed_claim": EXPECTED_ALLOWED_CLAIM,
        "public_safe_status": "BLOCKED",
        "next_gate": "human_review_gate",
        "website_boundary": "rendering-only",
    }
    for field, value in expected.items():
        if cross.get(field) != value:
            fail(f"cross_repo_consistency.{field} must be {value}")
    if cross.get("public_safe") is not False or cross.get("human_review_required") is not True:
        fail("cross repo public_safe/human_review boundary changed")
    if set(cross.get("blocked_claims", [])) != REQUIRED_BLOCKED_CLAIMS:
        fail("cross repo blocked claims mismatch")
    if set(cross.get("missing_evidence", [])) != REQUIRED_MISSING_EVIDENCE:
        fail("cross repo missing evidence mismatch")


def _validate_website_boundary(boundary: Any) -> None:
    if not isinstance(boundary, dict):
        fail("website_rendering_boundary must be an object")
    if boundary.get("website_is_proof_authority") is not False:
        fail("website is treated as proof authority")
    if boundary.get("website_edits_required") is not False:
        fail("website edits must not be required")


def _validate_reviewer_commands(data: dict[str, Any]) -> None:
    commands = set(data.get("reviewer_commands", []))
    missing = sorted(REQUIRED_REVIEWER_COMMANDS - commands)
    if missing:
        fail(f"reviewer commands missing required entries: {', '.join(missing)}")


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


def _validate_no_forbidden_paths(data: dict[str, Any]) -> None:
    combined = json.dumps(data, sort_keys=True)
    if re.search(r"(?i)C:[\\/]+Raylee[\\/]+Work\b", combined):
        fail("stale forbidden Raylee Work path found")
    if re.search(r"(?i)\b[A-Z]:[\\/]", combined):
        fail("absolute local path found")
    if re.search(r"(?i)\b(secret|token|api[_-]?key|password|authorization|cookie)\s*[:=]\s*\S+", combined):
        fail("secret-like material found")


def _validate_hoxline_files_exist(hoxline_root: Path) -> None:
    root = hoxline_root.resolve()
    for rel_path in sorted(REQUIRED_HOXLINE_FILES):
        full_path = (root / rel_path).resolve()
        try:
            full_path.relative_to(root)
        except ValueError:
            fail(f"Hoxline path escapes root: {rel_path}")
        if not full_path.exists():
            fail(f"Hoxline referenced file missing: {rel_path}")


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
    parser.add_argument("--hoxline-root", type=Path, help="optional local Hoxline checkout root for source route existence checks")
    args = parser.parse_args()

    try:
        texts = [
            BRIDGE_MD.read_text(encoding="utf-8"),
            MAP_MD.read_text(encoding="utf-8"),
        ]
        result = validate_bridge(load_bridge(), load_map(), texts, args.hoxline_root)
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
