#!/usr/bin/env python3
"""Verify the HawkinsOperations branch cleanup governance map."""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
MAP_PATH = ROOT / "proof" / "indexes" / "hawkinsoperations-branch-cleanup-map.json"
PHASE13_MAP_PATH = ROOT / "proof" / "indexes" / "lifetime-case-ledger-v1-evidence-map.json"

REQUIRED_CATEGORIES = {
    "active_do_not_touch",
    "merged_preserve_until_cleanup_approved",
    "merged_cleanup_candidate",
    "stale_review_required",
    "evidence_preserve",
    "branch_drift_review_required",
    "unknown_do_not_touch",
    "local_only_review_required",
    "remote_only_review_required",
    "delete_candidate_requires_explicit_approval",
}

REQUIRED_BRANCH_FIELDS = {
    "category",
    "repo",
    "branch_name",
    "local_present",
    "remote_present",
    "base_branch",
    "merged_to_main",
    "related_pr",
    "related_phase",
    "latest_commit_sha",
    "evidence_value",
    "cleanup_risk",
    "delete_allowed",
    "deletion_requires_explicit_approval",
    "recommended_action",
    "reason",
}

DENIED_TEXT_PATTERNS = [
    ("local absolute path", re.compile(r"(?i)(?:[A-Z]:\\|\\\\)")),
    ("private IPv4 address", re.compile(r"\b(?:10|192\.168|172\.(?:1[6-9]|2[0-9]|3[0-1]))\.\d{1,3}\.\d{1,3}\b")),
    ("raw command line", re.compile(r"(?i)\braw[_ -]?command[_ -]?line\b")),
    ("screenshot", re.compile(r"(?i)\bscreenshot\b")),
    ("secret marker", re.compile(r"(?i)\b(secret|password|credential|api[_-]?key|token)\b")),
    ("private filename", re.compile(r"(?i)\bprivate[_ -]?filename\b")),
    ("raw model output", re.compile(r"(?i)\braw[_ -]?model[_ -]?output\b")),
    ("internal service name", re.compile(r"(?i)\binternal[_ -]?service[_ -]?name\b")),
]

PROMOTED_CLAIM_PATTERNS = [
    ("runtime active", re.compile(r"(?i)\bRUNTIME_ACTIVE\b|\bruntime-active public status\b(?!.*(?:blocked|not claimed|not prove|not promoted))")),
    ("signal observed", re.compile(r"(?i)\bSIGNAL_OBSERVED\b|\bsignal-observed public status\b(?!.*(?:blocked|not claimed|not prove|not promoted))")),
    ("public safe approved", re.compile(r"(?i)\bPUBLIC_SAFE_APPROVED\b")),
    ("public proof safe", re.compile(r"(?i)\bPUBLIC_PROOF_SAFE\b")),
    ("SOCaaS deployment", re.compile(r"(?i)\bSOCaaS deployment\b(?!.*(?:blocked|not claimed|not prove|not promoted))")),
    ("production deployment", re.compile(r"(?i)\bproduction deployment\b(?!.*(?:blocked|not claimed|not prove|not promoted))")),
    ("autonomous SOC", re.compile(r"(?i)\bautonomous SOC\b(?!.*(?:blocked|not claimed|not prove|not promoted))")),
    ("AI approved disposition", re.compile(r"(?i)\bAI-approved\b(?!.*(?:blocked|not claimed|not prove|not promoted))")),
    ("analyst approved disposition", re.compile(r"(?i)\banalyst-approved\b(?!.*(?:blocked|not claimed|not prove|not promoted))")),
    ("case closure authority", re.compile(r"(?i)\bcase closure authority\b(?!.*(?:blocked|not claimed|not prove|not promoted))")),
]


def fail(message: str) -> None:
    print(f"HawkinsOperations branch cleanup map verification failed: {message}", file=sys.stderr)
    raise SystemExit(1)


def scan_text(text: str, label: str) -> None:
    for name, pattern in DENIED_TEXT_PATTERNS:
        if pattern.search(text):
            fail(f"{label} contains blocked private marker: {name}")
    for name, pattern in PROMOTED_CLAIM_PATTERNS:
        if pattern.search(text):
            fail(f"{label} contains promoted claim wording: {name}")


def as_bool(value: Any, label: str) -> bool:
    if not isinstance(value, bool):
        fail(f"{label} must be boolean")
    return value


def load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        fail(f"missing map: {path.relative_to(ROOT).as_posix()}")
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        fail(f"invalid JSON: {exc}")
    if not isinstance(data, dict):
        fail("map root must be an object")
    return data


def verify_related_pr(value: Any, index: int) -> None:
    if value is None:
        return
    if not isinstance(value, dict):
        fail(f"branch {index} related_pr must be object or null")
    required = {"number", "state", "url"}
    missing = sorted(required - set(value))
    if missing:
        fail(f"branch {index} related_pr missing {missing[0]}")
    if value["state"] not in {"OPEN", "MERGED", "CLOSED"}:
        fail(f"branch {index} related_pr has unsupported state")


def verify_branch(entry: dict[str, Any], index: int, seen: set[tuple[str, str]], categories: set[str]) -> None:
    missing = sorted(REQUIRED_BRANCH_FIELDS - set(entry))
    if missing:
        fail(f"branch {index} missing required field: {missing[0]}")

    category = entry["category"]
    if category not in REQUIRED_CATEGORIES:
        fail(f"branch {index} has unknown category: {category}")
    categories.add(category)

    repo = entry["repo"]
    branch_name = entry["branch_name"]
    if not isinstance(repo, str) or not repo:
        fail(f"branch {index} repo must be non-empty string")
    if not isinstance(branch_name, str) or not branch_name:
        fail(f"branch {index} branch_name must be non-empty string")
    if branch_name == "main":
        fail(f"branch {index} must not classify main")
    if "\\" in branch_name or re.search(r"(?i)^[A-Z]:", branch_name):
        fail(f"branch {index} branch_name must not contain a path")

    key = (repo, branch_name)
    if key in seen:
        fail(f"duplicate branch entry: {repo}:{branch_name}")
    seen.add(key)

    local_present = as_bool(entry["local_present"], f"branch {index} local_present")
    remote_present = as_bool(entry["remote_present"], f"branch {index} remote_present")
    delete_allowed = as_bool(entry["delete_allowed"], f"branch {index} delete_allowed")
    deletion_requires = as_bool(
        entry["deletion_requires_explicit_approval"],
        f"branch {index} deletion_requires_explicit_approval",
    )

    if not local_present and not remote_present:
        fail(f"branch {index} must be present locally, remotely, or both")
    if delete_allowed:
        fail(f"branch {index} allows deletion: {repo}:{branch_name}")
    if not deletion_requires:
        fail(f"branch {index} lacks explicit deletion approval gate: {repo}:{branch_name}")

    merged_to_main = entry["merged_to_main"]
    if not (isinstance(merged_to_main, bool) or merged_to_main is None):
        fail(f"branch {index} merged_to_main must be boolean or null")

    verify_related_pr(entry["related_pr"], index)

    action_text = f"{entry['recommended_action']} {entry['reason']}".lower()
    if category == "unknown_do_not_touch" and ("delete" in action_text or "cleanup candidate" in action_text):
        fail(f"branch {index} unknown branch is marked cleanup-safe")
    if category == "evidence_preserve" and "delete candidate" in action_text:
        fail(f"branch {index} evidence-preserve branch is marked as delete candidate")
    if category == "delete_candidate_requires_explicit_approval" and "explicit" not in action_text:
        fail(f"branch {index} delete candidate lacks explicit-approval language")

    for field in ("repo", "branch_name", "base_branch", "related_phase", "latest_commit_sha", "evidence_value", "cleanup_risk", "recommended_action", "reason"):
        value = entry[field]
        if value is not None and not isinstance(value, str):
            fail(f"branch {index} field {field} must be string or null")
        if isinstance(value, str):
            scan_text(value, f"branch {index} {field}")


def verify(data: dict[str, Any]) -> dict[str, Any]:
    if data.get("map_id") != "HAWKINSOPERATIONS_PHASE_14_BRANCH_CLEANUP_GOVERNANCE_MAP":
        fail("unexpected or missing map_id")
    if data.get("classification_only") is not True:
        fail("classification_only must be true")
    if data.get("branch_deletion_performed") is not False:
        fail("branch_deletion_performed must be false")
    if data.get("ledger_status") != "NOT_PUBLIC_SAFE":
        fail("ledger_status must remain NOT_PUBLIC_SAFE")
    if data.get("proof_ceiling") != "SCHEMA_CONTRACT_VERIFIER_EXISTS_ONLY":
        fail("proof_ceiling must remain SCHEMA_CONTRACT_VERIFIER_EXISTS_ONLY")
    if data.get("source_phase13_evidence_map") != "proof/indexes/lifetime-case-ledger-v1-evidence-map.json":
        fail("source_phase13_evidence_map must point to the Phase 13 evidence map")
    if not PHASE13_MAP_PATH.exists():
        fail("Phase 13 evidence map is missing")

    branches = data.get("branches")
    if not isinstance(branches, list) or not branches:
        fail("branches must be a non-empty list")

    seen: set[tuple[str, str]] = set()
    categories: set[str] = set()
    for index, entry in enumerate(branches):
        if not isinstance(entry, dict):
            fail(f"branch {index} must be an object")
        verify_branch(entry, index, seen, categories)

    missing_categories = sorted(REQUIRED_CATEGORIES - categories)
    if missing_categories:
        fail(f"missing required category: {missing_categories[0]}")

    return {
        "branch_count": len(branches),
        "categories": sorted(categories),
        "ledger_status": data["ledger_status"],
        "proof_ceiling": data["proof_ceiling"],
    }


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--map", default=str(MAP_PATH))
    parser.add_argument("--format", choices=("text", "json"), default="text")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    map_path = Path(args.map).resolve()
    data = load_json(map_path)
    scan_text(map_path.read_text(encoding="utf-8"), map_path.relative_to(ROOT).as_posix())
    result = verify(data)
    if args.format == "json":
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print("HawkinsOperations branch cleanup map verification passed.")
        print(f"branch_count={result['branch_count']}")
        print(f"ledger_status={result['ledger_status']}")
        print(f"proof_ceiling={result['proof_ceiling']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
