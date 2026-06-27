#!/usr/bin/env python3
"""Verify Hoxline Proof Record Backfill v0 artifacts."""
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
REPORT_PATH = ROOT / "proof" / "reports" / "hoxline-proof-record-backfill-v0.json"
INDEX_PATH = ROOT / "proof" / "indexes" / "DETECTION_PROOF_STATUS_INDEX.yml"

REQUIRED_SECTIONS = [
    "# {case_id} Proof Record",
    "## 1. Summary",
    "## 2. Truth Surface",
    "## 3. Source Truth",
    "## 4. Validation Truth",
    "## 5. Runtime Truth",
    "## 6. Signal Truth",
    "## 7. Evidence Truth",
    "## 8. Public Proof Truth",
    "## 9. Claim Authority",
    "## 10. Blocked Claims",
    "## 11. Evidence References",
    "## 12. What This Record Proves",
    "## 13. What This Record Does Not Prove",
    "## 14. Next Gate",
    "## 15. Human Review Requirement",
]

REQUIRED_RECORD_MARKERS = [
    "proof_ceiling: CONTROLLED_TEST_VALIDATED",
    "source_status: SOURCE_EXISTS",
    "validation_status: CONTROLLED_TEST_VALIDATED",
    "runtime_status: NOT_PROVEN",
    "signal_status: NOT_PROVEN",
    "public_safe_status: NOT_PUBLIC_SAFE",
    "case_status: NOT_CLOSED",
    "human_review_required: true",
    "website_status: WEBSITE_RENDERING_NOT_PROOF",
    "green_ci_status: GREEN_CI_NOT_APPROVAL",
]

REQUIRED_BLOCKED_CLAIMS = [
    "runtime-active public proof",
    "signal-observed public proof",
    "public-safe proof",
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
    "website_rendering_treated_as_proof",
    "github_rendering_treated_as_proof",
    "green_ci_treated_as_approval",
]


class VerificationError(Exception):
    """Raised when the backfill artifacts fail verification."""


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


def rel_from_repo(path: str, repo_root: Path) -> Path:
    candidate = repo_root / path
    try:
        candidate.resolve().relative_to(repo_root.resolve())
    except ValueError as exc:
        raise VerificationError(f"path escapes repo root: {path}") from exc
    return candidate


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


def verify_record(case_id: str, record_path: Path) -> None:
    if not record_path.exists():
        raise VerificationError(f"{case_id} proof record path missing: {record_path}")
    text = record_path.read_text(encoding="utf-8")
    for section in REQUIRED_SECTIONS:
        marker = section.format(case_id=case_id)
        if marker not in text:
            raise VerificationError(f"{case_id} proof record missing section: {marker}")
    for marker in REQUIRED_RECORD_MARKERS:
        if marker not in text:
            raise VerificationError(f"{case_id} proof record missing marker: {marker}")
    for claim in REQUIRED_BLOCKED_CLAIMS:
        if claim not in text:
            raise VerificationError(f"{case_id} proof record missing blocked claim: {claim}")
    if "runtime_status: NOT_PROVEN" not in text or "signal_status: NOT_PROVEN" not in text:
        raise VerificationError(f"{case_id} proof record must keep runtime and signal NOT_PROVEN")
    if "website rendering as proof" not in text or "green CI as approval" not in text:
        raise VerificationError(f"{case_id} proof record must block website proof and green CI approval")


def verify_backfill(repo_root: Path = ROOT) -> dict[str, Any]:
    report = load_json(repo_root / "proof" / "reports" / "hoxline-proof-record-backfill-v0.json")
    index = load_yaml(repo_root / "proof" / "indexes" / "DETECTION_PROOF_STATUS_INDEX.yml")
    counts = require_mapping(report.get("counts_before_after"), "counts_before_after")
    created_records = require_list(report.get("created_records"), "created_records")
    entries = index_entries_by_id(index)

    if counts.get("proof_records_created") != len(created_records):
        raise VerificationError("proof_records_created must equal created_records length")
    if len(report.get("eligible_cases", [])) != len(created_records):
        raise VerificationError("eligible_cases must equal created_records length")
    if counts.get("proof_records_after_estimated") != counts.get("proof_records_before", 0) + len(created_records):
        raise VerificationError("proof_records_after_estimated must derive from before count plus created count")
    if counts.get("missing_proof_records_after_estimated") != counts.get("missing_proof_records_before", 0) - len(created_records):
        raise VerificationError("missing_proof_records_after_estimated must derive from before missing count minus created count")

    for field in ZERO_COUNT_FIELDS:
        if counts.get(field) != 0:
            raise VerificationError(f"{field} must be 0")
    for field in FALSE_BOUNDARY_FIELDS:
        if require_mapping(report.get("boundary"), "boundary").get(field) is not False:
            raise VerificationError(f"boundary.{field} must be false")

    verified_records: list[str] = []
    for raw in created_records:
        record = require_mapping(raw, "created_records entry")
        case_id = record.get("case_id")
        proof_record_path = record.get("proof_record_path")
        if not isinstance(case_id, str) or not case_id:
            raise VerificationError("created record missing case_id")
        if not isinstance(proof_record_path, str) or not proof_record_path:
            raise VerificationError(f"{case_id} missing proof_record_path")
        if record.get("proof_ceiling") != "CONTROLLED_TEST_VALIDATED":
            raise VerificationError(f"{case_id} proof_ceiling must be CONTROLLED_TEST_VALIDATED")
        if record.get("public_safe_status") != "NOT_PUBLIC_SAFE":
            raise VerificationError(f"{case_id} public_safe_status must be NOT_PUBLIC_SAFE")
        if record.get("case_status") != "NOT_CLOSED":
            raise VerificationError(f"{case_id} case_status must be NOT_CLOSED")

        index_entry = entries.get(case_id)
        if index_entry is None:
            raise VerificationError(f"{case_id} missing from proof index")
        if index_entry.get("proof_record_path") != proof_record_path:
            raise VerificationError(f"{case_id} proof index path does not match report")
        if index_entry.get("proof_ceiling") != "CONTROLLED_TEST_VALIDATED":
            raise VerificationError(f"{case_id} proof index ceiling must be CONTROLLED_TEST_VALIDATED")
        if index_entry.get("public_safe_status") != "NOT_PUBLIC_SAFE":
            raise VerificationError(f"{case_id} proof index public_safe_status must be NOT_PUBLIC_SAFE")
        if index_entry.get("runtime_status") != "NOT_PROVEN" or index_entry.get("signal_status") != "NOT_PROVEN":
            raise VerificationError(f"{case_id} proof index must keep runtime and signal NOT_PROVEN")

        verify_record(case_id, rel_from_repo(proof_record_path, repo_root))
        verified_records.append(case_id)

    return {
        "status": "PASS",
        "created_records_count": len(created_records),
        "verified_records": verified_records,
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
            print(f"Proof record backfill verification failed: {exc}", file=sys.stderr)
        return 1

    if args.format == "json":
        print(json.dumps(result, indent=2))
    else:
        print(f"Proof record backfill verification passed: {result['created_records_count']} records")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
