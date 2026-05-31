#!/usr/bin/env python3
"""Fail-closed verification for the proof-owned Lifetime Case Ledger public summary."""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SUMMARY_PATH = ROOT / "proof" / "records" / "lifetime-case-ledger-v1-public-summary.json"
DEFAULT_PLATFORM_MANIFEST = ROOT.parent / "hawkinsoperations-platform" / "contracts" / "lifetime-case-ledger-v1-state-manifest.json"

SUMMARY_ID = "LIFETIME_CASE_LEDGER_V1_PHASE_9_PUBLIC_SUMMARY"
SUMMARY_VERSION = "phase_9_proof_owned_public_summary_v1"
STATE_BASIS = "post_phase_7_merged_main"
PLATFORM_MANIFEST_ID = "LIFETIME_CASE_LEDGER_V1_PHASE_8_STATE_MANIFEST"
PLATFORM_MANIFEST_VERSION = "phase_8_ledger_state_manifest_v1"
PLATFORM_MANIFEST_COMMIT_SHA = "e0580fc8d0b141cbdd71c1b95e3d7885a1d708e0"
PROOF_CEILING = "SCHEMA_CONTRACT_VERIFIER_EXISTS_ONLY"
LEDGER_BOUNDARY = "tracked platform seed bridge, not runtime truth, not signal truth, not public proof"
PUBLIC_SAFE_STATUS = "NOT_PUBLIC_SAFE"
REQUIRED_COUNTS = {
    "total_ledger_events": 4,
    "total_cases": 4,
    "public_safe_count": 0,
    "closed_case_count": 0,
    "correction_event_count": 0,
    "superseding_event_count": 0,
}
APPENDED_DETECTIONS = ["HO-DET-001", "HO-DET-011", "HO-DET-012"]
REQUIRED_REPOS = {
    ".github",
    "hawkinsoperations-detections",
    "hawkinsoperations-validation",
    "hawkinsoperations-platform",
    "hawkinsoperations-proof",
    "hawkinsoperations-website",
}
GOVERNANCE_DEFAULTS = {
    "human_review_required": True,
    "ai_support_mode": "AI_SUPPORT_ONLY",
    "ai_decided_disposition": False,
    "recommended_disposition": None,
    "proof_blocked": True,
    "public_safe": False,
    "case_closed": False,
    "github_issue_mutation_allowed": False,
}
DOES_NOT_PROVE = {
    "live runtime activity",
    "signal observation",
    "production deployment",
    "SOCaaS availability",
    "public-safe runtime proof",
    "public proof",
    "autonomous SOC authority",
    "AI-approved final disposition",
    "analyst-approved final disposition",
    "case closure authority",
}
BLOCKED_CLAIMS = {
    "production deployment",
    "public raw runtime evidence",
    "runtime-active public status",
    "signal-observed public status",
    "public-safe runtime proof",
    "SOCaaS deployment",
    "autonomous SOC",
    "AI-approved final disposition",
    "analyst-approved final disposition",
    "case closure without explicit human-approved closure artifact",
    "evidence-linked public proof",
    "live Splunk firing",
    "production triage",
    "local GPU support node runtime-active",
    "Cribl-routed proof",
    "Wazuh-routed proof",
    "AWS-live",
    "fleet-wide deployment",
    "production-ready SOC",
    "public-safe status",
}
PRIVATE_PATTERNS = (
    re.compile(r"\b[A-Za-z]:\\"),
    re.compile(r"\b(?:10|127|169\.254|172\.(?:1[6-9]|2\d|3[0-1])|192\.168)\.\d{1,3}\.\d{1,3}\b"),
    re.compile(r"(?i)\b(hostname|username|raw command line|raw_command_line|private filename|private_filename)\b"),
    re.compile(r"(?i)\b(secret|password|token|api[_-]?key|credential)\b"),
    re.compile(r"(?i)\b(raw model output|internal service)\b"),
)
SHA40_RE = re.compile(r"^[0-9a-f]{40}$")


class VerificationError(Exception):
    """Raised when the proof-owned ledger summary fails verification."""


def fail(message: str) -> None:
    print(f"Lifetime ledger public summary verification failed: {message}", file=sys.stderr)
    raise SystemExit(1)


def load_json(path: Path, label: str) -> dict[str, Any]:
    if not path.is_file():
        raise VerificationError(f"missing {label}: {path}")
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise VerificationError(f"invalid JSON in {label}: {exc}") from exc
    if not isinstance(value, dict):
        raise VerificationError(f"{label} must be a JSON object")
    return value


def scan_private_markers(label: str, value: Any) -> None:
    text = json.dumps(value, sort_keys=True)
    for pattern in PRIVATE_PATTERNS:
        if pattern.search(text):
            raise VerificationError(f"{label} contains blocked private/raw marker: {pattern.pattern}")


def require_sha(value: Any, label: str) -> str:
    if not isinstance(value, str) or not SHA40_RE.fullmatch(value):
        raise VerificationError(f"{label} must be a 40-character lowercase commit SHA")
    return value


def require_repo_relative_path(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise VerificationError(f"{label} must be a non-empty repo-relative path")
    if "\\" in value or value.startswith(("/", ".")) or re.search(r"\b[A-Za-z]:\\", value):
        raise VerificationError(f"{label} must be repo-relative and use forward slashes")
    return value


def require_set(actual: Any, required: set[str], label: str) -> list[str]:
    if not isinstance(actual, list):
        raise VerificationError(f"{label} must be a list")
    actual_set = {str(item) for item in actual}
    missing = sorted(required - actual_set)
    if missing:
        raise VerificationError(f"{label} missing required values: {missing}")
    return sorted(actual_set)


def require_exact_counts(summary: dict[str, Any], manifest: dict[str, Any]) -> dict[str, int]:
    summary_counts = summary.get("ledger_counts")
    manifest_counts = manifest.get("current_ledger_counts")
    if not isinstance(summary_counts, dict) or not isinstance(manifest_counts, dict):
        raise VerificationError("summary and platform manifest must both expose ledger count mappings")
    failures = {
        key: {"summary": summary_counts.get(key), "manifest": manifest_counts.get(key), "required": required}
        for key, required in REQUIRED_COUNTS.items()
        if summary_counts.get(key) != required or manifest_counts.get(key) != required
    }
    if failures:
        raise VerificationError(f"ledger count drift detected: {failures}")
    return {key: int(summary_counts[key]) for key in REQUIRED_COUNTS}


def entries_by_repo(entries: Any, label: str) -> dict[str, dict[str, Any]]:
    if not isinstance(entries, list):
        raise VerificationError(f"{label} must be a list")
    by_repo: dict[str, dict[str, Any]] = {}
    for entry in entries:
        if not isinstance(entry, dict):
            raise VerificationError(f"{label} entries must be objects")
        repo_name = entry.get("repo_name")
        if not isinstance(repo_name, str) or not repo_name:
            raise VerificationError(f"{label} repo_name is required")
        if repo_name in by_repo:
            raise VerificationError(f"{label} duplicate repo entry: {repo_name}")
        require_sha(entry.get("commit_sha"), f"{label}.{repo_name}.commit_sha")
        for field in ("role", "branch", "authority_boundary"):
            if not isinstance(entry.get(field), str) or not entry[field].strip():
                raise VerificationError(f"{label}.{repo_name}.{field} is required")
        by_repo[repo_name] = entry
    missing = sorted(REQUIRED_REPOS - set(by_repo))
    if missing:
        raise VerificationError(f"{label} missing repos: {missing}")
    extra = sorted(set(by_repo) - REQUIRED_REPOS)
    if extra:
        raise VerificationError(f"{label} has unknown repos: {extra}")
    return by_repo


def verify_summary(summary_path: Path, platform_manifest_path: Path) -> dict[str, Any]:
    summary = load_json(summary_path, "proof-owned ledger summary")
    manifest = load_json(platform_manifest_path, "platform Phase 8 manifest")
    scan_private_markers("proof-owned ledger summary", summary)

    if summary.get("summary_id") != SUMMARY_ID:
        raise VerificationError("summary_id is invalid")
    if summary.get("summary_version") != SUMMARY_VERSION:
        raise VerificationError("summary_version is invalid")
    if summary.get("owner_repo") != "hawkinsoperations-proof":
        raise VerificationError("owner_repo must be hawkinsoperations-proof")
    if summary.get("source_controlled_summary") is not True:
        raise VerificationError("source_controlled_summary must be true")
    if summary.get("state_basis") != STATE_BASIS:
        raise VerificationError("summary state_basis is invalid")
    if manifest.get("state_basis") != STATE_BASIS:
        raise VerificationError("platform manifest state_basis is invalid")
    if manifest.get("manifest_id") != PLATFORM_MANIFEST_ID:
        raise VerificationError("platform manifest_id is invalid")
    if manifest.get("manifest_version") != PLATFORM_MANIFEST_VERSION:
        raise VerificationError("platform manifest_version is invalid")
    if manifest.get("source_controlled_manifest") is not True:
        raise VerificationError("platform manifest must be source-controlled")

    source = summary.get("source_platform_manifest")
    if not isinstance(source, dict):
        raise VerificationError("source_platform_manifest must be an object")
    if source.get("repo_name") != "hawkinsoperations-platform":
        raise VerificationError("source platform repo_name is invalid")
    if require_repo_relative_path(source.get("repo_relative_path"), "source_platform_manifest.repo_relative_path") != (
        "contracts/lifetime-case-ledger-v1-state-manifest.json"
    ):
        raise VerificationError("source platform manifest path is invalid")
    if require_sha(source.get("manifest_commit_sha"), "source_platform_manifest.manifest_commit_sha") != PLATFORM_MANIFEST_COMMIT_SHA:
        raise VerificationError("source platform manifest commit SHA is not the approved Phase 8 merge commit")
    if source.get("manifest_id") != manifest.get("manifest_id"):
        raise VerificationError("source manifest_id does not match platform manifest")
    if source.get("manifest_version") != manifest.get("manifest_version"):
        raise VerificationError("source manifest_version does not match platform manifest")
    if source.get("platform_commit_sha_from_manifest") != manifest.get("platform_commit_sha"):
        raise VerificationError("source platform_commit_sha_from_manifest does not match platform manifest")

    if summary.get("ledger_boundary") != LEDGER_BOUNDARY or manifest.get("ledger_boundary") != LEDGER_BOUNDARY:
        raise VerificationError("ledger boundary drifted or was promoted")
    counts = require_exact_counts(summary, manifest)

    if sorted(summary.get("appended_detection_ids") or []) != APPENDED_DETECTIONS:
        raise VerificationError("summary appended_detection_ids mismatch")
    if sorted(manifest.get("appended_detection_ids") or []) != APPENDED_DETECTIONS:
        raise VerificationError("platform manifest appended_detection_ids mismatch")
    if summary.get("proof_ceiling") != PROOF_CEILING or manifest.get("proof_ceiling") != PROOF_CEILING:
        raise VerificationError("proof ceiling drifted or was promoted")

    boundary = summary.get("public_safe_boundary")
    if not isinstance(boundary, dict):
        raise VerificationError("public_safe_boundary must be an object")
    if boundary.get("summary_surface") != "PUBLIC_SUMMARY_SAFE_FOR_BOUNDED_LEDGER_COUNTS":
        raise VerificationError("summary surface must remain bounded public summary only")
    if boundary.get("ledger_public_safe_status") != PUBLIC_SAFE_STATUS:
        raise VerificationError("ledger public-safe status must remain NOT_PUBLIC_SAFE")
    for field in (
        "public_runtime_proof",
        "public_signal_proof",
        "public_proof_promotion",
        "case_closure_authority",
        "ai_or_analyst_disposition_authority",
    ):
        if boundary.get(field) is not False:
            raise VerificationError(f"public_safe_boundary.{field} must be false")
    if summary.get("governance_defaults") != GOVERNANCE_DEFAULTS:
        raise VerificationError("governance defaults weakened")
    require_set(summary.get("does_not_prove"), DOES_NOT_PROVE, "does_not_prove")
    require_set(summary.get("blocked_claims"), BLOCKED_CLAIMS, "blocked_claims")

    summary_repos = entries_by_repo(summary.get("six_repo_sha_reference"), "summary six_repo_sha_reference")
    manifest_repos = entries_by_repo(manifest.get("six_repo_state"), "platform manifest six_repo_state")
    for repo_name, entry in summary_repos.items():
        if entry != manifest_repos[repo_name]:
            raise VerificationError(f"six-repo SHA reference drift for {repo_name}")

    commands = summary.get("verification_commands")
    if not isinstance(commands, list) or not commands:
        raise VerificationError("verification_commands must be a non-empty list")
    expected_command = (
        "python scripts/verify-lifetime-ledger-public-summary.py "
        "--platform-manifest ../hawkinsoperations-platform/contracts/lifetime-case-ledger-v1-state-manifest.json"
    )
    if expected_command not in commands:
        raise VerificationError("verification_commands missing Phase 9 verifier command")
    for command in commands:
        require_repo_relative_path(str(command), "verification command")

    downstream = summary.get("downstream_preparation")
    if not isinstance(downstream, dict):
        raise VerificationError("downstream_preparation must be an object")
    for field in (
        "proof_bundle_input",
        "badge_pipeline_input",
        "website_summary_input",
        "requires_separate_publication_approval_for_display",
        "requires_separate_proof_pack_or_badge_implementation",
    ):
        if downstream.get(field) is not True:
            raise VerificationError(f"downstream_preparation.{field} must be true")

    return {
        "mode": "verify-lifetime-ledger-public-summary",
        "summary_path": summary_path.relative_to(ROOT).as_posix(),
        "platform_manifest_path": platform_manifest_path.relative_to(ROOT.parent).as_posix()
        if platform_manifest_path.is_relative_to(ROOT.parent)
        else str(platform_manifest_path),
        "platform_manifest_commit_sha": PLATFORM_MANIFEST_COMMIT_SHA,
        "platform_commit_sha_from_manifest": source["platform_commit_sha_from_manifest"],
        "ledger_counts": counts,
        "appended_detection_ids": APPENDED_DETECTIONS,
        "proof_ceiling": PROOF_CEILING,
        "ledger_public_safe_status": PUBLIC_SAFE_STATUS,
        "summary_surface": boundary["summary_surface"],
        "six_repo_sha_reference": list(summary_repos.values()),
        "does_not_prove_verified": sorted(DOES_NOT_PROVE),
        "blocked_claims_verified": sorted(BLOCKED_CLAIMS),
        "boundary": (
            "Proof-owned Phase 9 summary is limited to bounded ledger counts and boundary state from the "
            "platform Phase 8 manifest. It does not import raw evidence, append ledger rows, prove runtime "
            "activity, prove signal observation, publish public proof, mark the ledger public-safe, claim "
            "SOCaaS or production deployment, grant disposition authority, or close cases."
        ),
    }


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--summary", default=str(SUMMARY_PATH))
    parser.add_argument("--platform-manifest", default=str(DEFAULT_PLATFORM_MANIFEST))
    parser.add_argument("--format", default="text", choices=("text", "json"))
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    try:
        result = verify_summary(Path(args.summary).resolve(), Path(args.platform_manifest).resolve())
    except VerificationError as exc:
        fail(str(exc))
    if args.format == "json":
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print("Lifetime ledger public summary verification passed.")
        print(f"summary_path={result['summary_path']}")
        print(f"platform_manifest_commit_sha={result['platform_manifest_commit_sha']}")
        print(f"total_ledger_events={result['ledger_counts']['total_ledger_events']}")
        print(f"total_cases={result['ledger_counts']['total_cases']}")
        print(f"proof_ceiling={result['proof_ceiling']}")
        print(f"ledger_public_safe_status={result['ledger_public_safe_status']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
