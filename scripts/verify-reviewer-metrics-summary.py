#!/usr/bin/env python3
"""Verify the proof-owned reviewer metrics summary."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SUMMARY_PATH = ROOT / "proof" / "records" / "reviewer-metrics-pipeline-v1-summary.json"

REQUIRED_METRICS = {
    "lifetime_governed_cases",
    "lifetime_ledger_events",
    "detection_activity_count",
    "controlled_validation_fire_count",
    "controlled_negative_test_count",
    "validation_case_count",
    "proof_record_count",
    "blocked_claim_count",
    "runtime_public_safe_count",
    "public_safe_count",
    "detection_family_count",
}
DENIED_TEXT = [
    ("C:\\Raylee\\Work", re.compile(r"C:\\Raylee\\Work", re.IGNORECASE)),
    ("private IPv4 address", re.compile(r"\b(?:10|192\.168|172\.(?:1[6-9]|2[0-9]|3[0-1]))\.\d{1,3}\.\d{1,3}\b")),
    ("secret marker", re.compile(r"\b(secret|password|credential|api[_-]?key|token)\b", re.IGNORECASE)),
]


class VerificationError(Exception):
    """Raised when reviewer metrics summary violates the proof boundary."""


def fail(message: str) -> None:
    raise VerificationError(message)


def load_json(path: Path, label: str = "reviewer metrics summary") -> dict[str, Any]:
    if not path.exists():
        fail(f"missing {label}: {path}")
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        fail(f"malformed {label}: {exc}")
    if not isinstance(data, dict):
        fail(f"{label} root must be an object")
    return data


def scan_value(value: Any, label: str) -> None:
    if isinstance(value, dict):
        for key, nested in value.items():
            scan_value(key, label)
            scan_value(nested, label)
    elif isinstance(value, list):
        for nested in value:
            scan_value(nested, label)
    elif isinstance(value, str):
        for name, pattern in DENIED_TEXT:
            if pattern.search(value):
                fail(f"{label} contains blocked text: {name}")


def _source_artifact_path(summary: dict[str, Any], key: str, repo_root: Path) -> Path:
    source_artifacts = summary.get("source_artifacts")
    if not isinstance(source_artifacts, dict) or not source_artifacts:
        fail("source_artifacts must be a non-empty object")
    value = source_artifacts.get(key)
    if not isinstance(value, str) or not value:
        fail(f"source artifact {key} must be a string")
    path = Path(value)
    if path.is_absolute():
        fail(f"source artifact {key} must be repo-relative or sibling-relative")
    return (repo_root / path).resolve()


def platform_metrics_from_summary(summary_path: Path = SUMMARY_PATH, repo_root: Path = ROOT) -> dict[str, int]:
    summary = load_json(summary_path)
    platform_state_path = _source_artifact_path(summary, "platform_metrics_state", repo_root)
    platform_state = load_json(platform_state_path, "platform reviewer metrics state")
    platform_metrics = platform_state.get("metrics")
    summary_metrics = summary.get("metrics")
    if not isinstance(platform_metrics, dict):
        fail("platform reviewer metrics state metrics must be present")
    if not isinstance(summary_metrics, dict):
        fail("summary metrics must be present")

    missing_platform_keys = sorted(set(summary_metrics) - set(platform_metrics))
    if missing_platform_keys:
        fail(f"platform metrics missing summarized keys: {missing_platform_keys}")
    comparable_keys = sorted(summary_metrics)
    expected: dict[str, int] = {}
    for key in comparable_keys:
        value = platform_metrics[key]
        if not isinstance(value, int) or value < 0:
            fail(f"platform metric {key} must be a non-negative integer")
        expected[key] = value
    return expected


def project_reconciliation_from_summary(summary_path: Path = SUMMARY_PATH, repo_root: Path = ROOT) -> dict[str, bool]:
    summary = load_json(summary_path)
    receipt_path = _source_artifact_path(summary, "github_control_receipts", repo_root)
    text = receipt_path.read_text(encoding="utf-8")
    lowered = text.lower()
    reconciliation = summary.get("project_board_reconciliation_status")
    if not isinstance(reconciliation, dict):
        fail("project_board_reconciliation_status must be present")

    return {
        "standing_issue_8_present": "#8" in text and "standing control" in lowered,
        "standing_issue_10_present": "#10" in text and "blocked claims" in lowered,
        "project_2_route_present": "project #2" in lowered,
        "report_only_boundary_present": "report_only" in lowered or "not proof" in lowered,
        "project_metadata_is_proof_authority": reconciliation.get("project_metadata_is_proof_authority") is True,
        "github_project_mutation_performed": reconciliation.get("github_project_mutation_performed") is True,
    }


def verify_summary(summary_path: Path = SUMMARY_PATH, repo_root: Path = ROOT) -> dict[str, Any]:
    summary = load_json(summary_path)
    scan_value(summary, "reviewer metrics summary")

    if summary.get("owner_repo") != "hawkinsoperations-proof":
        fail("owner_repo must be hawkinsoperations-proof")
    if summary.get("public_safe_status") != "NOT_PUBLIC_SAFE":
        fail("public_safe_status must be NOT_PUBLIC_SAFE")
    if summary.get("proof_ceiling") != "SCHEMA_CONTRACT_VERIFIER_EXISTS_ONLY":
        fail("proof_ceiling must remain SCHEMA_CONTRACT_VERIFIER_EXISTS_ONLY")

    metrics = summary.get("metrics")
    if not isinstance(metrics, dict):
        fail("metrics must be present")
    missing = REQUIRED_METRICS - set(metrics)
    if missing:
        fail(f"metrics missing fields: {sorted(missing)}")
    for key in REQUIRED_METRICS:
        if not isinstance(metrics[key], int) or metrics[key] < 0:
            fail(f"{key} must be a non-negative integer")
    if metrics["detection_activity_count"] <= metrics["lifetime_governed_cases"]:
        fail("detection activity count must remain visibly broader than governed cases")
    if metrics["detection_activity_count"] != metrics["controlled_validation_fire_count"]:
        fail("v1 detection activity count must equal controlled validation fire count")
    if metrics["runtime_public_safe_count"] != 0 or metrics["public_safe_count"] != 0:
        fail("summary must not claim public-safe counts")

    authority = summary.get("authority_boundaries")
    if not isinstance(authority, dict):
        fail("authority_boundaries must be present")
    if authority.get("website_is_proof_authority") is not False:
        fail("website must remain render-only and not proof authority")
    if authority.get("github_project_metadata_is_proof_authority") is not False:
        fail("GitHub Project metadata must not be proof authority")
    if authority.get("detection_activity_is_governed_case_count") is not False:
        fail("detection activity must not be governed case count")

    reconciliation = summary.get("project_board_reconciliation_status")
    if not isinstance(reconciliation, dict):
        fail("project_board_reconciliation_status must be present")
    if reconciliation.get("github_project_mutation_performed") is not False:
        fail("summary must not mutate GitHub Projects")
    if reconciliation.get("project_metadata_is_proof_authority") is not False:
        fail("Project metadata must remain non-authoritative")
    if not summary.get("does_not_prove") or not summary.get("blocked_claims"):
        fail("does_not_prove and blocked_claims must be populated")
    for key, expected in platform_metrics_from_summary(summary_path, repo_root).items():
        if metrics.get(key) != expected:
            fail(f"{key} platform metric mismatch: expected {expected}, found {metrics.get(key)}")
    project_reconciliation = project_reconciliation_from_summary(summary_path, repo_root)
    for key in ("standing_issue_8_present", "standing_issue_10_present", "project_2_route_present", "report_only_boundary_present"):
        if project_reconciliation[key] is not True:
            fail(f"project reconciliation source missing boundary: {key}")
    if project_reconciliation["project_metadata_is_proof_authority"] is not False:
        fail("Project metadata must remain non-authoritative")
    if project_reconciliation["github_project_mutation_performed"] is not False:
        fail("summary must not mutate GitHub Projects")

    return {
        "status": "pass",
        "summary_path": str(summary_path.relative_to(repo_root)) if summary_path.is_relative_to(repo_root) else str(summary_path),
        "metrics": metrics,
        "proof_ceiling": summary["proof_ceiling"],
        "public_safe_status": summary["public_safe_status"],
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--summary", type=Path, default=SUMMARY_PATH)
    parser.add_argument("--format", choices={"text", "json"}, default="text")
    args = parser.parse_args(argv)
    try:
        result = verify_summary(args.summary, ROOT)
    except VerificationError as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1
    if args.format == "json":
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print("PASS: reviewer metrics summary is proof-bounded")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
