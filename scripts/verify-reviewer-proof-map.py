#!/usr/bin/env python3
"""Verify the proof-owned reviewer proof map and claim boundaries."""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
MAP_PATH = ROOT / "proof" / "indexes" / "reviewer-proof-map.json"
README_PATH = ROOT / "proof" / "indexes" / "reviewer-proof-map.md"

PROOF_CEILING = "SCHEMA_CONTRACT_VERIFIER_EXISTS_ONLY"
LEDGER_STATUS = "NOT_PUBLIC_SAFE"
EXPECTED_EVENTS = 4
EXPECTED_CASES = 4
CORRECT_PLATFORM_MANIFEST_PATH = "../hawkinsoperations-platform/contracts/lifetime-case-ledger-v1-state-manifest.json"
STALE_PLATFORM_MANIFEST_TOKENS = (
    "lifetime-ledger-platform-state-" + "manifest",
    "evidence/" + "lifetime-ledger-platform-state-" + "manifest.json",
)

REQUIRED_PROOF_ARTIFACTS = {
    "proof/records/lifetime-case-ledger-v1-public-summary.json",
    "proof/records/lifetime-case-ledger-v1-proof-bundle.json",
    "proof/indexes/lifetime-case-ledger-v1-evidence-map.json",
    "proof/indexes/hawkinsoperations-branch-cleanup-map.json",
    "scripts/verify-lifetime-ledger-public-summary.py",
    "scripts/verify-lifetime-ledger-proof-bundle.py",
    "scripts/verify-lifetime-ledger-badges.py",
    "scripts/verify-lifetime-ledger-evidence-map.py",
    "scripts/verify-hawkinsoperations-branch-cleanup-map.py",
    "scripts/verify-reviewer-proof-map.py",
}

REQUIRED_PLATFORM_ARTIFACTS = {
    "contracts/lifetime-case-ledger-v1-state-manifest.json",
}

REQUIRED_GITHUB_ARTIFACTS = {
    "profile/README.md",
}

REQUIRED_CHAIN_IDS = [
    "platform_ledger",
    "platform_state_manifest",
    "proof_public_summary",
    "proof_bundle",
    "badge_status_checks",
    "render_only_downstream_surfaces",
]

REQUIRED_BLOCKED_CLAIMS = [
    "runtime-active public proof",
    "signal-observed public proof",
    "public-safe runtime proof",
    "production deployment",
    "SOCaaS deployment",
    "autonomous SOC",
    "AI-approved disposition",
    "analyst-approved disposition",
    "case closure",
    "Cribl-routed",
    "Wazuh-routed",
    "AWS-live",
    "fleet-wide",
    "live Splunk firing",
    "website as proof authority",
    "badge as proof authority",
    "Project #1 as proof authority",
]

REQUIRED_CHECKLIST = [
    "summary_verifiable",
    "bundle_verifiable",
    "badges_status_only",
    "evidence_maps_present",
    "cleanup_candidates_classification_only",
    "blocked_claims_explicit",
    "website_render_authority_blocked",
    "project_one_proof_authority_blocked",
]

REQUIRED_REVIEWER_CLICK_IDS = [
    "start_reviewer_map",
    "check_public_summary",
    "check_proof_bundle",
    "check_verifier",
    "check_blocked_claims",
]

DENIED_TEXT_PATTERNS = [
    ("local absolute path", re.compile(r"(?i)(?:[A-Z]:\\|\\\\)")),
    ("private IPv4 address", re.compile(r"\b(?:10|192\.168|172\.(?:1[6-9]|2[0-9]|3[0-1]))\.\d{1,3}\.\d{1,3}\b")),
    ("secret marker", re.compile(r"(?i)\b(secret|password|credential|api[_-]?key|token)\b")),
    ("raw private evidence", re.compile(r"(?i)\braw private evidence\b(?!.*(?:excluded|not included|not public-safe|blocked))")),
]

PROMOTED_CLAIM_PATTERNS = [
    ("runtime-active public proof", re.compile(r"(?i)\bruntime-active public proof\b(?!.*(?:blocked|not prove|does not prove|not claimed))")),
    ("signal-observed public proof", re.compile(r"(?i)\bsignal-observed public proof\b(?!.*(?:blocked|not prove|does not prove|not claimed))")),
    ("public-safe runtime proof", re.compile(r"(?i)\bpublic-safe runtime proof\b(?!.*(?:blocked|not prove|does not prove|not claimed))")),
    ("production deployment", re.compile(r"(?i)\bproduction deployment\b(?!.*(?:blocked|not prove|does not prove|not claimed))")),
    ("SOCaaS deployment", re.compile(r"(?i)\bSOCaaS deployment\b(?!.*(?:blocked|not prove|does not prove|not claimed))")),
    ("autonomous SOC", re.compile(r"(?i)\bautonomous SOC\b(?!.*(?:blocked|not prove|does not prove|not claimed))")),
    ("AI-approved disposition", re.compile(r"(?i)\bAI-approved disposition\b(?!.*(?:blocked|not prove|does not prove|not claimed))")),
    ("analyst-approved disposition", re.compile(r"(?i)\banalyst-approved disposition\b(?!.*(?:blocked|not prove|does not prove|not claimed))")),
    ("case closure", re.compile(r"(?i)\bcase closure\b(?!.*(?:blocked|not prove|does not prove|not claimed|without))")),
    ("Cribl-routed", re.compile(r"(?i)\bCribl-routed\b(?!.*(?:blocked|not prove|does not prove|not claimed))")),
    ("Wazuh-routed", re.compile(r"(?i)\bWazuh-routed\b(?!.*(?:blocked|not prove|does not prove|not claimed))")),
    ("AWS-live", re.compile(r"(?i)\bAWS-live\b(?!.*(?:blocked|not prove|does not prove|not claimed))")),
    ("fleet-wide", re.compile(r"(?i)\bfleet-wide\b(?!.*(?:blocked|not prove|does not prove|not claimed))")),
    ("live Splunk firing", re.compile(r"(?i)\blive Splunk firing\b(?!.*(?:blocked|not prove|does not prove|not claimed))")),
    ("website proof authority", re.compile(r"(?i)\bwebsite as proof authority\b(?!.*(?:blocked|not prove|does not prove|not claimed))")),
    ("badge proof authority", re.compile(r"(?i)\bbadge as proof authority\b(?!.*(?:blocked|not prove|does not prove|not claimed))")),
    ("Project proof authority", re.compile(r"(?i)\bProject #1 as proof authority\b(?!.*(?:blocked|not prove|does not prove|not claimed))")),
    ("public safe approved", re.compile(r"(?i)\bPUBLIC_SAFE_APPROVED\b")),
    ("public proof safe", re.compile(r"(?i)\bPUBLIC_PROOF_SAFE\b")),
]


class VerificationError(Exception):
    """Raised when reviewer proof map verification fails."""


def fail(message: str) -> None:
    raise VerificationError(message)


def load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        fail(f"missing reviewer proof map: {path.relative_to(ROOT).as_posix()}")
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        fail(f"invalid reviewer proof map JSON: {exc}")
    if not isinstance(data, dict):
        fail("reviewer proof map root must be an object")
    return data


def scan_text(text: str, label: str) -> None:
    for token in STALE_PLATFORM_MANIFEST_TOKENS:
        if token in text:
            fail(f"{label} contains stale platform manifest reference: {token}")
    for name, pattern in DENIED_TEXT_PATTERNS:
        if pattern.search(text):
            fail(f"{label} contains blocked private marker: {name}")
    for name, pattern in PROMOTED_CLAIM_PATTERNS:
        for line in text.splitlines() or [text]:
            if not pattern.search(line):
                continue
            lowered = line.lower()
            if any(
                boundary in lowered
                for boundary in (
                    "blocked",
                    "does not prove",
                    "not proof authority",
                    "not claimed",
                    "status-only",
                    "render-only",
                    "operating control only",
                )
            ):
                continue
            fail(f"{label} contains promoted claim wording: {name}")


def require_bool_false(value: Any, label: str) -> None:
    if value is not False:
        fail(f"{label} must be false")


def verify_artifact_paths(paths: list[Any], root: Path, required: set[str], label: str) -> None:
    found: set[str] = set()
    for value in paths:
        if not isinstance(value, str) or not value:
            fail(f"{label} artifact paths must be non-empty strings")
        if value.startswith("/") or "\\" in value or re.search(r"(?i)^[A-Z]:", value):
            fail(f"{label} artifact path must be repo-relative POSIX path: {value}")
        found.add(value)
    missing = sorted(required - found)
    if missing:
        fail(f"{label} missing required artifact reference: {missing[0]}")
    for value in required:
        if not (root / value).exists():
            fail(f"{label} required artifact does not exist: {value}")


def verify_chain(stages: list[Any]) -> None:
    if not isinstance(stages, list):
        fail("proof_chain.stages must be a list")
    ids = [stage.get("id") for stage in stages if isinstance(stage, dict)]
    if ids != REQUIRED_CHAIN_IDS:
        fail("proof_chain.stages must preserve the required stage order")
    for index, stage in enumerate(stages):
        if not isinstance(stage, dict):
            fail(f"proof_chain stage {index} must be an object")
        for field in ("owner", "artifact_path", "what_it_proves", "what_it_does_not_prove", "current_status", "proof_ceiling"):
            value = stage.get(field)
            if not isinstance(value, str) or not value.strip():
                fail(f"proof_chain stage {stage.get('id', index)} missing {field}")
            scan_text(value, f"proof_chain stage {stage.get('id', index)} {field}")
        if stage["proof_ceiling"] != PROOF_CEILING:
            fail(f"proof_chain stage {stage['id']} must keep {PROOF_CEILING}")


def verify_checklist(items: list[Any]) -> None:
    if not isinstance(items, list):
        fail("trust_backup_checklist must be a list")
    by_id: dict[str, dict[str, Any]] = {}
    for item in items:
        if not isinstance(item, dict):
            fail("trust_backup_checklist items must be objects")
        item_id = item.get("id")
        if not isinstance(item_id, str):
            fail("trust_backup_checklist item id must be string")
        by_id[item_id] = item
        if item.get("status") != "PASS_REVIEWABLE":
            fail(f"trust_backup_checklist {item_id} must be PASS_REVIEWABLE")
        evidence = item.get("evidence")
        if not isinstance(evidence, str) or not evidence.strip():
            fail(f"trust_backup_checklist {item_id} missing evidence")
        scan_text(evidence, f"trust_backup_checklist {item_id} evidence")
    missing = sorted(set(REQUIRED_CHECKLIST) - set(by_id))
    if missing:
        fail(f"trust_backup_checklist missing required item: {missing[0]}")


def verify_reviewer_click_path(items: list[Any]) -> None:
    if not isinstance(items, list):
        fail("reviewer_click_path must be a list")
    ids = [item.get("id") for item in items if isinstance(item, dict)]
    if ids != REQUIRED_REVIEWER_CLICK_IDS:
        fail("reviewer_click_path must preserve the required reviewer order")
    for item in items:
        if not isinstance(item, dict):
            fail("reviewer_click_path items must be objects")
        for field in ("id", "label", "artifact_path", "reviewer_value"):
            value = item.get(field)
            if not isinstance(value, str) or not value.strip():
                fail(f"reviewer_click_path {item.get('id', '<unknown>')} missing {field}")
            scan_text(value, f"reviewer_click_path {item.get('id', '<unknown>')} {field}")


def verify_blocked_claims(claims: list[Any]) -> None:
    if not isinstance(claims, list):
        fail("blocked_claims must be a list")
    by_claim: dict[str, dict[str, Any]] = {}
    for entry in claims:
        if not isinstance(entry, dict):
            fail("blocked_claims entries must be objects")
        claim = entry.get("claim")
        if not isinstance(claim, str):
            fail("blocked claim must be string")
        by_claim[claim] = entry
        if entry.get("status") != "BLOCKED":
            fail(f"blocked claim must remain BLOCKED: {claim}")
        if "not prove" not in str(entry.get("reason", "")).lower() and "not proof authority" not in str(entry.get("reason", "")).lower():
            fail(f"blocked claim needs negative-boundary reason: {claim}")
    missing = sorted(set(REQUIRED_BLOCKED_CLAIMS) - set(by_claim))
    if missing:
        fail(f"blocked_claims missing required claim: {missing[0]}")


def verify(data: dict[str, Any], *, platform_root: Path | None, github_root: Path | None) -> dict[str, Any]:
    if data.get("map_id") != "REVIEWER_PROOF_MAP_V1":
        fail("unexpected or missing map_id")
    if data.get("owner_repo") != "hawkinsoperations-proof":
        fail("owner_repo must be hawkinsoperations-proof")
    if data.get("proof_ceiling") != PROOF_CEILING:
        fail(f"proof_ceiling must remain {PROOF_CEILING}")
    if data.get("ledger_status") != LEDGER_STATUS:
        fail(f"ledger_status must remain {LEDGER_STATUS}")
    if data.get("artifact_class") != "proof_owned_reviewer_map":
        fail("artifact_class must be proof_owned_reviewer_map")
    if data.get("corrected_platform_manifest_path") != CORRECT_PLATFORM_MANIFEST_PATH:
        fail("corrected_platform_manifest_path must point to the repo-conventional platform manifest")

    counts = data.get("ledger_summary", {})
    if not isinstance(counts, dict):
        fail("ledger_summary must be object")
    if counts.get("total_ledger_events") != EXPECTED_EVENTS:
        fail("ledger_summary.total_ledger_events must remain 4")
    if counts.get("total_cases") != EXPECTED_CASES:
        fail("ledger_summary.total_cases must remain 4")
    if counts.get("ledger_public_safe_status") != LEDGER_STATUS:
        fail(f"ledger_summary.ledger_public_safe_status must remain {LEDGER_STATUS}")
    require_bool_false(counts.get("case_closure_authority"), "ledger_summary.case_closure_authority")

    boundaries = data.get("authority_boundaries", {})
    if not isinstance(boundaries, dict):
        fail("authority_boundaries must be object")
    for key in (
        "website_render_surfaces_are_proof_authority",
        "badges_are_proof_authority",
        "project_one_is_proof_authority",
        "github_project_mutation_performed",
        "proof_promotion_performed",
    ):
        require_bool_false(boundaries.get(key), f"authority_boundaries.{key}")

    proof_paths = data.get("required_proof_artifacts")
    if not isinstance(proof_paths, list):
        fail("required_proof_artifacts must be list")
    verify_artifact_paths(proof_paths, ROOT, REQUIRED_PROOF_ARTIFACTS, "proof")

    if platform_root is not None:
        platform_paths = data.get("read_only_platform_artifacts", [])
        if not isinstance(platform_paths, list):
            fail("read_only_platform_artifacts must be list")
        verify_artifact_paths(platform_paths, platform_root, REQUIRED_PLATFORM_ARTIFACTS, "platform")

    if github_root is not None:
        github_paths = data.get("read_only_github_artifacts", [])
        if not isinstance(github_paths, list):
            fail("read_only_github_artifacts must be list")
        verify_artifact_paths(github_paths, github_root, REQUIRED_GITHUB_ARTIFACTS, ".github")

    proof_chain = data.get("proof_chain", {})
    if not isinstance(proof_chain, dict):
        fail("proof_chain must be object")
    verify_chain(proof_chain.get("stages", []))

    verify_checklist(data.get("trust_backup_checklist", []))
    verify_reviewer_click_path(data.get("reviewer_click_path", []))
    verify_blocked_claims(data.get("blocked_claims", []))

    does_not_prove = data.get("does_not_prove")
    if not isinstance(does_not_prove, list) or len(does_not_prove) < len(REQUIRED_BLOCKED_CLAIMS):
        fail("does_not_prove must list the blocked proof boundaries")
    joined_does_not_prove = "\n".join(str(item) for item in does_not_prove)
    for claim in REQUIRED_BLOCKED_CLAIMS:
        if claim not in joined_does_not_prove:
            fail(f"does_not_prove missing required boundary: {claim}")

    map_text = json.dumps(data, sort_keys=True)
    scan_text(map_text, "reviewer proof map")

    if not README_PATH.exists():
        fail(f"missing reviewer proof map markdown: {README_PATH.relative_to(ROOT).as_posix()}")
    markdown = README_PATH.read_text(encoding="utf-8")
    scan_text(markdown, README_PATH.relative_to(ROOT).as_posix())
    for required in (
        "4 events",
        "4 cases",
        LEDGER_STATUS,
        PROOF_CEILING,
        "status-only",
        "render-only",
        "Project #1 is operating control only",
        "badge as proof authority",
        "website as proof authority",
        CORRECT_PLATFORM_MANIFEST_PATH,
        "Reviewer Click Path",
        "Start with this map",
    ):
        if required not in markdown:
            fail(f"reviewer proof map markdown missing required text: {required}")

    return {
        "map_id": data["map_id"],
        "proof_ceiling": data["proof_ceiling"],
        "ledger_status": data["ledger_status"],
        "blocked_claim_count": len(data["blocked_claims"]),
        "proof_chain_stage_count": len(proof_chain["stages"]),
    }


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--map", default=str(MAP_PATH))
    parser.add_argument("--platform-root")
    parser.add_argument("--github-root")
    parser.add_argument("--format", choices=("text", "json"), default="text")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    try:
        data = load_json(Path(args.map).resolve())
        result = verify(
            data,
            platform_root=Path(args.platform_root).resolve() if args.platform_root else None,
            github_root=Path(args.github_root).resolve() if args.github_root else None,
        )
    except VerificationError as exc:
        print(f"Reviewer proof map verification failed: {exc}", file=sys.stderr)
        return 1
    if args.format == "json":
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print("Reviewer proof map verification passed.")
        print(f"blocked_claim_count={result['blocked_claim_count']}")
        print(f"ledger_status={result['ledger_status']}")
        print(f"proof_ceiling={result['proof_ceiling']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
