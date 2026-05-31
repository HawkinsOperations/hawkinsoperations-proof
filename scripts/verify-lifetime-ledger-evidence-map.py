#!/usr/bin/env python3
"""Verify the Lifetime Case Ledger evidence preservation map."""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
MAP_PATH = ROOT / "proof" / "indexes" / "lifetime-case-ledger-v1-evidence-map.json"

REQUIRED_CATEGORIES = {
    "canonical_current",
    "evidence_preserve",
    "render_only",
    "verifier",
    "badge_or_status_indicator",
    "legacy_reference",
    "stale_reference",
    "duplicate_candidate",
    "cleanup_candidate_requires_approval",
    "do_not_touch",
}

REQUIRED_CANONICAL = {
    ("hawkinsoperations-platform", "evidence/autosoc-case-ledger-v0.sqlite"),
    ("hawkinsoperations-platform", "contracts/lifetime-case-ledger-v1-state-manifest.json"),
    ("hawkinsoperations-proof", "proof/records/lifetime-case-ledger-v1-public-summary.json"),
    ("hawkinsoperations-proof", "proof/records/lifetime-case-ledger-v1-proof-bundle.json"),
    ("hawkinsoperations-proof", "scripts/verify-lifetime-ledger-badges.py"),
    ("hawkinsoperations-proof", "README.md"),
    ("hawkinsoperations-website", "app/proof/page.tsx"),
    ("hawkinsoperations-website", "src/data/proofRecords.ts"),
}

REQUIRED_VERIFIERS = {
    ("hawkinsoperations-proof", "scripts/verify-lifetime-ledger-public-summary.py"),
    ("hawkinsoperations-proof", "scripts/verify-lifetime-ledger-proof-bundle.py"),
    ("hawkinsoperations-proof", "scripts/verify-lifetime-ledger-badges.py"),
    ("hawkinsoperations-proof", "scripts/verify-lifetime-ledger-evidence-map.py"),
}

REQUIRED_RELATIONSHIP_ARTIFACTS = {
    ("hawkinsoperations-detections", "detections/DETECTION_FACTORY_INDEX.md"),
    ("hawkinsoperations-detections", "detections/DETECTION_PROMOTION_MATRIX.yml"),
    ("hawkinsoperations-validation", "validation/VALIDATION_REGISTRY.yml"),
    ("hawkinsoperations-validation", "reports/ho-det-001/validation-result.json"),
    ("hawkinsoperations-validation", "reports/ho-det-011/validation-result.json"),
    ("hawkinsoperations-validation", "reports/ho-det-012/validation-result.json"),
    ("hawkinsoperations-website", "src/data/navigation.ts"),
    ("hawkinsoperations-website", "scripts/verify-site-contract.mjs"),
}

REQUIRED_FIELDS = {
    "category",
    "owning_repo",
    "artifact_path",
    "role",
    "authority_boundary",
    "status",
    "preserve",
    "evidence_preservation_requirement",
    "delete_allowed",
    "move_allowed",
    "archive_allowed",
    "cleanup_requires_explicit_approval",
    "reason",
    "related_verifier",
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
    ("runtime active", re.compile(r"(?i)\bRUNTIME_ACTIVE\b|\bruntime-active public status\b(?!.*(?:blocked|not claimed|not prove))")),
    ("signal observed", re.compile(r"(?i)\bSIGNAL_OBSERVED\b|\bsignal-observed public status\b(?!.*(?:blocked|not claimed|not prove))")),
    ("public safe approved", re.compile(r"(?i)\bPUBLIC_SAFE_APPROVED\b")),
    ("public proof safe", re.compile(r"(?i)\bPUBLIC_PROOF_SAFE\b")),
    ("SOCaaS deployment", re.compile(r"(?i)\bSOCaaS deployment\b(?!.*(?:blocked|not claimed|not prove))")),
    ("production deployment", re.compile(r"(?i)\bproduction deployment\b(?!.*(?:blocked|not claimed|not prove))")),
    ("autonomous SOC", re.compile(r"(?i)\bautonomous SOC\b(?!.*(?:blocked|not claimed|not prove))")),
    ("AI approved disposition", re.compile(r"(?i)\bAI-approved\b(?!.*(?:blocked|not claimed|not prove))")),
    ("analyst approved disposition", re.compile(r"(?i)\banalyst-approved\b(?!.*(?:blocked|not claimed|not prove))")),
    ("case closure authority", re.compile(r"(?i)\bcase closure authority\b(?!.*(?:blocked|not claimed|not prove))")),
]

REPO_ROOTS = {
    "hawkinsoperations-proof": ROOT,
}


def fail(message: str) -> None:
    print(f"Lifetime ledger evidence map verification failed: {message}", file=sys.stderr)
    raise SystemExit(1)


def as_bool(value: Any, label: str) -> bool:
    if not isinstance(value, bool):
        fail(f"{label} must be boolean")
    return value


def load_map(path: Path) -> dict[str, Any]:
    if not path.exists():
        fail(f"missing evidence map: {path.relative_to(ROOT).as_posix()}")
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        fail(f"invalid JSON: {exc}")
    if not isinstance(data, dict):
        fail("map root must be an object")
    return data


def scan_text(text: str, label: str) -> None:
    for name, pattern in DENIED_TEXT_PATTERNS:
        if pattern.search(text):
            fail(f"{label} contains blocked private marker: {name}")
    for name, pattern in PROMOTED_CLAIM_PATTERNS:
        if pattern.search(text):
            fail(f"{label} contains promoted claim wording: {name}")


def verify_entry(entry: dict[str, Any], index: int, seen: set[tuple[str, str]], categories: set[str]) -> None:
    missing = sorted(REQUIRED_FIELDS - set(entry))
    if missing:
        fail(f"entry {index} missing required field: {missing[0]}")

    category = entry["category"]
    if category not in REQUIRED_CATEGORIES:
        fail(f"entry {index} has unknown category: {category}")
    categories.add(category)

    owning_repo = entry["owning_repo"]
    artifact_path = entry["artifact_path"]
    if not isinstance(owning_repo, str) or not isinstance(artifact_path, str):
        fail(f"entry {index} owning_repo and artifact_path must be strings")
    if artifact_path.startswith("/") or "\\" in artifact_path or re.search(r"(?i)^[A-Z]:", artifact_path):
        fail(f"entry {index} artifact_path must be repo-relative POSIX path")

    key = (owning_repo, artifact_path)
    if key in seen:
        fail(f"duplicate map key: {owning_repo}:{artifact_path}")
    seen.add(key)

    preserve = as_bool(entry["preserve"], f"entry {index} preserve")
    delete_allowed = as_bool(entry["delete_allowed"], f"entry {index} delete_allowed")
    move_allowed = as_bool(entry["move_allowed"], f"entry {index} move_allowed")
    archive_allowed = as_bool(entry["archive_allowed"], f"entry {index} archive_allowed")
    cleanup_requires = as_bool(
        entry["cleanup_requires_explicit_approval"],
        f"entry {index} cleanup_requires_explicit_approval",
    )

    if delete_allowed or move_allowed or archive_allowed:
        fail(f"entry {index} allows cleanup action without approval: {owning_repo}:{artifact_path}")

    if category in {"canonical_current", "evidence_preserve", "do_not_touch"} and not preserve:
        fail(f"entry {index} preservation artifact must have preserve=true: {owning_repo}:{artifact_path}")

    if category == "cleanup_candidate_requires_approval" and not cleanup_requires:
        fail(f"entry {index} cleanup candidate must require explicit approval")

    if category in {"render_only", "badge_or_status_indicator"}:
        boundary = f"{entry['role']} {entry['authority_boundary']}".lower()
        if "proof authority" in boundary and "not proof authority" not in boundary:
            fail(f"entry {index} render/badge artifact is marked as proof authority")

    for field in ("role", "authority_boundary", "status", "evidence_preservation_requirement", "reason"):
        value = entry[field]
        if not isinstance(value, str) or not value.strip():
            fail(f"entry {index} field {field} must be non-empty string")
        scan_text(value, f"entry {index} {field}")


def verify_external_existence(entries: list[dict[str, Any]], roots: dict[str, Path]) -> None:
    for entry in entries:
        repo = entry["owning_repo"]
        path = entry["artifact_path"]
        category = entry["category"]
        if category not in {
            "canonical_current",
            "evidence_preserve",
            "verifier",
            "badge_or_status_indicator",
            "render_only",
            "legacy_reference",
            "stale_reference",
            "duplicate_candidate",
            "cleanup_candidate_requires_approval",
            "do_not_touch",
        }:
            continue
        root = roots.get(repo)
        if root is None:
            continue
        if not (root / path).exists():
            fail(f"mapped artifact missing from {repo}: {path}")


def verify(data: dict[str, Any], roots: dict[str, Path]) -> dict[str, Any]:
    if data.get("map_id") != "LIFETIME_CASE_LEDGER_V1_PHASE_13_EVIDENCE_PRESERVATION_MAP":
        fail("unexpected or missing map_id")
    if data.get("ledger_status") != "NOT_PUBLIC_SAFE":
        fail("ledger_status must remain NOT_PUBLIC_SAFE")
    if data.get("proof_ceiling") != "SCHEMA_CONTRACT_VERIFIER_EXISTS_ONLY":
        fail("proof_ceiling must remain SCHEMA_CONTRACT_VERIFIER_EXISTS_ONLY")
    if data.get("classification_only") is not True:
        fail("classification_only must be true")

    entries = data.get("artifacts")
    if not isinstance(entries, list) or not entries:
        fail("artifacts must be a non-empty list")

    seen: set[tuple[str, str]] = set()
    categories: set[str] = set()
    for index, entry in enumerate(entries):
        if not isinstance(entry, dict):
            fail(f"entry {index} must be an object")
        verify_entry(entry, index, seen, categories)

    missing_categories = sorted(REQUIRED_CATEGORIES - categories)
    if missing_categories:
        fail(f"missing required category: {missing_categories[0]}")

    missing_canonical = sorted(REQUIRED_CANONICAL - seen)
    if missing_canonical:
        repo, path = missing_canonical[0]
        fail(f"missing required canonical artifact: {repo}:{path}")

    missing_verifier = sorted(REQUIRED_VERIFIERS - seen)
    if missing_verifier:
        repo, path = missing_verifier[0]
        fail(f"missing required verifier artifact: {repo}:{path}")

    missing_relationship = sorted(REQUIRED_RELATIONSHIP_ARTIFACTS - seen)
    if missing_relationship:
        repo, path = missing_relationship[0]
        fail(f"missing required source relationship artifact: {repo}:{path}")

    verify_external_existence(entries, roots)

    return {
        "artifact_count": len(entries),
        "categories": sorted(categories),
        "ledger_status": data["ledger_status"],
        "proof_ceiling": data["proof_ceiling"],
    }


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--map", default=str(MAP_PATH))
    parser.add_argument("--platform-root")
    parser.add_argument("--website-root")
    parser.add_argument("--detections-root")
    parser.add_argument("--validation-root")
    parser.add_argument("--github-root")
    parser.add_argument("--format", choices=("text", "json"), default="text")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    roots = dict(REPO_ROOTS)
    for key, value in {
        "hawkinsoperations-platform": args.platform_root,
        "hawkinsoperations-website": args.website_root,
        "hawkinsoperations-detections": args.detections_root,
        "hawkinsoperations-validation": args.validation_root,
        ".github": args.github_root,
    }.items():
        if value:
            roots[key] = Path(value).resolve()

    map_path = Path(args.map).resolve()
    data = load_map(map_path)
    scan_text(map_path.read_text(encoding="utf-8"), map_path.relative_to(ROOT).as_posix())
    result = verify(data, roots)

    if args.format == "json":
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print("Lifetime ledger evidence map verification passed.")
        print(f"artifact_count={result['artifact_count']}")
        print(f"ledger_status={result['ledger_status']}")
        print(f"proof_ceiling={result['proof_ceiling']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
