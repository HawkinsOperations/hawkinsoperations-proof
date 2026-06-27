#!/usr/bin/env python3
"""Verify Hoxline ProofCard Backfill v0 artifacts."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:  # pragma: no cover - environment failure path
    yaml = None


ROOT = Path(__file__).resolve().parents[1]
ORG_ROOT = ROOT.parent

REQUIRED_SECTIONS = [
    "# {case_id} ProofCard",
    "## 1. Card Summary",
    "## 2. Current Authority",
    "## 3. Proof Ceiling",
    "## 4. Truth State",
    "## 5. Evidence References",
    "## 6. Allowed Claims",
    "## 7. Blocked Claims",
    "## 8. Non-Proof Surfaces",
    "## 9. Human Review Requirement",
    "## 10. Next Gate",
]

REQUIRED_CARD_MARKERS = [
    "proofcard_version: proofcard-backfill-v0",
    "proof_record_path:",
    "proof_ceiling:",
    "source_status:",
    "validation_status:",
    "runtime_status:",
    "signal_status:",
    "public_safe_status: NOT_PUBLIC_SAFE",
    "case_status: NOT_CLOSED",
    "human_review_required: true",
    "website_status: WEBSITE_RENDERING_NOT_PROOF",
    "github_status: GITHUB_RENDERING_NOT_PROOF",
    "green_ci_status: GREEN_CI_NOT_APPROVAL",
    "card_status: INTERNAL_REVIEW_CARD_NOT_PUBLIC_SAFE",
]

REQUIRED_BLOCKED_CLAIMS = [
    "runtime-active public proof",
    "signal-observed public proof",
    "public_safe proof",
    "public_safe runtime proof",
    "production-ready",
    "customer deployment",
    "SOCaaS deployment",
    "autonomous SOC",
    "AI-approved disposition",
    "analyst-approved disposition",
    "final authorization",
    "case closure",
    "website rendering as proof",
    "GitHub rendering as proof",
    "green CI as approval",
    "product-market fit",
    "customer adoption",
]

ZERO_COUNT_FIELDS = [
    "public_safe_cases_created",
    "closed_cases_created",
    "runtime_proof_created",
    "signal_proof_created",
    "production_claims_created",
    "customer_claims_created",
    "approval_claims_created",
]

FALSE_BOUNDARY_FIELDS = [
    "runtime_public_proof_created",
    "signal_public_proof_created",
    "customer_deployment_claimed",
    "production_readiness_claimed",
    "public_safe_runtime_proof_claimed",
    "ai_approval_claimed",
    "analyst_approval_claimed",
    "final_authorization_claimed",
    "case_closure_claimed",
    "product_market_fit_claimed",
    "customer_adoption_claimed",
    "website_rendering_treated_as_proof",
    "github_rendering_treated_as_proof",
    "green_ci_treated_as_approval",
]

ALLOWED_RUNTIME_STATUSES = {"NOT_PROVEN", "PRIVATE_RUNTIME_BOUNDARY_CONTEXT_ONLY", "PRIVATE_RUNTIME_EVIDENCE_CAPTURED"}
ALLOWED_SIGNAL_STATUSES = {"NOT_PROVEN"}


class VerificationError(Exception):
    """Raised when ProofCard backfill artifacts fail verification."""


def load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise VerificationError(f"missing JSON report: {path}")
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise VerificationError(f"malformed JSON report: {exc}") from exc
    if not isinstance(data, dict):
        raise VerificationError("JSON report must be an object")
    return data


def load_yaml(path: Path) -> dict[str, Any]:
    if yaml is None:
        raise VerificationError("PyYAML is required to parse the proof index")
    if not path.exists():
        raise VerificationError(f"missing proof index: {path}")
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        raise VerificationError(f"malformed proof index: {exc}") from exc
    if not isinstance(data, dict):
        raise VerificationError("proof index must be an object")
    return data


def require_mapping(value: Any, label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise VerificationError(f"{label} must be an object")
    return value


def require_list(value: Any, label: str) -> list[Any]:
    if not isinstance(value, list):
        raise VerificationError(f"{label} must be a list")
    return value


def repo_path(path: str, repo_root: Path) -> Path:
    candidate = repo_root / path
    try:
        candidate.resolve().relative_to(repo_root.resolve())
    except ValueError as exc:
        raise VerificationError(f"path escapes proof repo root: {path}") from exc
    return candidate


def evidence_ref_exists(ref: str, repo_root: Path) -> bool:
    if ref.startswith("proof/"):
        return (repo_root / ref).exists()
    if ref.startswith("hawkinsoperations-"):
        return (ORG_ROOT / ref).exists()
    return True


def index_entries_by_id(index: dict[str, Any]) -> dict[str, dict[str, Any]]:
    entries = require_list(index.get("entries"), "proof index entries")
    by_id: dict[str, dict[str, Any]] = {}
    for raw in entries:
        entry = require_mapping(raw, "proof index entry")
        detection_id = entry.get("detection_id")
        if not isinstance(detection_id, str) or not detection_id:
            raise VerificationError("proof index entry missing detection_id")
        by_id[detection_id] = entry
    return by_id


def verify_card(case_id: str, card_path: Path, repo_root: Path, expected_record_path: str) -> None:
    if not card_path.exists():
        raise VerificationError(f"{case_id} ProofCard path missing: {card_path}")
    text = card_path.read_text(encoding="utf-8")
    for section in REQUIRED_SECTIONS:
        marker = section.format(case_id=case_id)
        if marker not in text:
            raise VerificationError(f"{case_id} ProofCard missing section: {marker}")
    for marker in REQUIRED_CARD_MARKERS:
        if marker not in text:
            raise VerificationError(f"{case_id} ProofCard missing marker: {marker}")
    if f"case_id: {case_id}" not in text:
        raise VerificationError(f"{case_id} ProofCard missing case_id marker")
    if f"proof_record_path: {expected_record_path}" not in text:
        raise VerificationError(f"{case_id} ProofCard does not reference expected proof record")
    for claim in REQUIRED_BLOCKED_CLAIMS:
        if claim not in text:
            raise VerificationError(f"{case_id} ProofCard missing blocked claim: {claim}")
    for line in text.splitlines():
        if line.startswith("- proof/") or line.startswith("- hawkinsoperations-"):
            ref = line[2:]
            if not evidence_ref_exists(ref, repo_root):
                raise VerificationError(f"{case_id} evidence reference does not resolve: {ref}")
    if "runtime-active public proof" not in text or "signal-observed public proof" not in text:
        raise VerificationError(f"{case_id} ProofCard must block public runtime and signal proof")
    if "website rendering as proof" not in text or "GitHub rendering as proof" not in text or "green CI as approval" not in text:
        raise VerificationError(f"{case_id} ProofCard must block non-proof surfaces")


def verify_backfill(repo_root: Path = ROOT) -> dict[str, Any]:
    report = load_json(repo_root / "proof" / "reports" / "hoxline-proofcard-backfill-v0.json")
    index = load_yaml(repo_root / "proof" / "indexes" / "DETECTION_PROOF_STATUS_INDEX.yml")
    counts = require_mapping(report.get("counts_before_after"), "counts_before_after")
    created = require_list(report.get("created_proofcards"), "created_proofcards")
    entries = index_entries_by_id(index)

    if counts.get("proofcards_created") != len(created):
        raise VerificationError("proofcards_created must equal created_proofcards length")
    if len(report.get("eligible_cases", [])) != len(created):
        raise VerificationError("eligible_cases must equal created_proofcards length")
    if counts.get("proofcards_after_estimated") != counts.get("proofcards_before", 0) + len(created):
        raise VerificationError("proofcards_after_estimated must derive from before count plus created count")
    if counts.get("proofcards_missing_after_estimated") != counts.get("proofcards_missing_before", 0) - len(created):
        raise VerificationError("proofcards_missing_after_estimated must derive from before missing count minus created count")
    if counts.get("proof_records_total_indexed") != counts.get("proofcards_after_estimated"):
        raise VerificationError("proofcard backfill should cover all indexed proof records after this backfill")

    for field in ZERO_COUNT_FIELDS:
        if counts.get(field) != 0:
            raise VerificationError(f"{field} must be 0")
    boundary = require_mapping(report.get("boundary"), "boundary")
    for field in FALSE_BOUNDARY_FIELDS:
        if boundary.get(field) is not False:
            raise VerificationError(f"boundary.{field} must be false")

    verified: list[str] = []
    for raw in created:
        record = require_mapping(raw, "created_proofcards entry")
        case_id = record.get("case_id")
        proof_record_path = record.get("proof_record_path")
        proof_card_path = record.get("proof_card_path")
        if not isinstance(case_id, str) or not case_id:
            raise VerificationError("created ProofCard missing case_id")
        if not isinstance(proof_record_path, str) or not proof_record_path:
            raise VerificationError(f"{case_id} missing proof_record_path")
        if not isinstance(proof_card_path, str) or not proof_card_path:
            raise VerificationError(f"{case_id} missing proof_card_path")
        if not repo_path(proof_record_path, repo_root).exists():
            raise VerificationError(f"{case_id} proof record does not exist: {proof_record_path}")
        if record.get("public_safe_status") != "NOT_PUBLIC_SAFE":
            raise VerificationError(f"{case_id} public_safe_status must be NOT_PUBLIC_SAFE")
        if record.get("case_status") != "NOT_CLOSED":
            raise VerificationError(f"{case_id} case_status must be NOT_CLOSED")

        entry = entries.get(case_id)
        if entry is None:
            raise VerificationError(f"{case_id} missing from proof index")
        if entry.get("proof_record_path") != proof_record_path:
            raise VerificationError(f"{case_id} index proof_record_path does not match report")
        if entry.get("proof_card_path") != proof_card_path:
            raise VerificationError(f"{case_id} index proof_card_path does not match report")
        if entry.get("proof_ceiling") != record.get("proof_ceiling"):
            raise VerificationError(f"{case_id} index proof_ceiling does not match report")
        if entry.get("public_safe_status") != "NOT_PUBLIC_SAFE":
            raise VerificationError(f"{case_id} index public_safe_status must be NOT_PUBLIC_SAFE")
        if entry.get("runtime_status") not in ALLOWED_RUNTIME_STATUSES:
            raise VerificationError(f"{case_id} unsupported runtime_status")
        if entry.get("signal_status") not in ALLOWED_SIGNAL_STATUSES:
            raise VerificationError(f"{case_id} unsupported signal_status")

        verify_card(case_id, repo_path(proof_card_path, repo_root), repo_root, proof_record_path)
        verified.append(case_id)

    return {
        "status": "PASS",
        "created_proofcards_count": len(created),
        "verified_proofcards": verified,
        "deferred_cases_count": len(report.get("deferred_cases", [])),
        "blocked_cases_count": len(report.get("blocked_cases", [])),
        "proof_ceiling": report.get("proof_ceiling"),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=ROOT)
    parser.add_argument("--format", choices=["text", "json"], default="text")
    args = parser.parse_args(argv)

    try:
        result = verify_backfill(args.repo_root)
    except VerificationError as exc:
        if args.format == "json":
            print(json.dumps({"status": "FAIL", "error": str(exc)}, indent=2))
        else:
            print(f"ProofCard backfill verification failed: {exc}", file=sys.stderr)
        return 1

    if args.format == "json":
        print(json.dumps(result, indent=2))
    else:
        print(f"ProofCard backfill verification passed: {result['created_proofcards_count']} cards")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
