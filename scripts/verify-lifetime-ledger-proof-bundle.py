#!/usr/bin/env python3
"""Verify the Lifetime Case Ledger v1 Phase 10 proof bundle."""
import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
BUNDLE_PATH = ROOT / "proof" / "records" / "lifetime-case-ledger-v1-proof-bundle.json"
SUMMARY_PATH = ROOT / "proof" / "records" / "lifetime-case-ledger-v1-public-summary.json"
DEFAULT_PLATFORM_MANIFEST = ROOT.parent / "hawkinsoperations-platform" / "contracts" / "lifetime-case-ledger-v1-state-manifest.json"

BUNDLE_ID = "LIFETIME_CASE_LEDGER_V1_PHASE_10_PROOF_BUNDLE"
BUNDLE_VERSION = "phase_10_six_repo_ledger_proof_bundle_v1"
SUMMARY_ID = "LIFETIME_CASE_LEDGER_V1_PHASE_9_PUBLIC_SUMMARY"
SUMMARY_VERSION = "phase_9_proof_owned_public_summary_v1"
PLATFORM_MANIFEST_ID = "LIFETIME_CASE_LEDGER_V1_PHASE_8_STATE_MANIFEST"
PLATFORM_MANIFEST_VERSION = "phase_8_ledger_state_manifest_v1"
PLATFORM_MANIFEST_COMMIT_SHA = "e0580fc8d0b141cbdd71c1b95e3d7885a1d708e0"
PROOF_CEILING = "SCHEMA_CONTRACT_VERIFIER_EXISTS_ONLY"
LEDGER_BOUNDARY = "tracked platform seed bridge, not runtime truth, not signal truth, not public proof"

REQUIRED_COUNTS = {
    "total_ledger_events": 4,
    "total_cases": 4,
    "public_safe_count": 0,
    "closed_case_count": 0,
    "correction_event_count": 0,
    "superseding_event_count": 0,
}
APPENDED_DETECTIONS = ["HO-DET-001", "HO-DET-011", "HO-DET-012"]

REQUIRED_COMMANDS = [
    "python scripts/verify-lifetime-ledger-proof-bundle.py --platform-manifest ../hawkinsoperations-platform/contracts/lifetime-case-ledger-v1-state-manifest.json",
    "python scripts/verify-lifetime-ledger-public-summary.py --platform-manifest ../hawkinsoperations-platform/contracts/lifetime-case-ledger-v1-state-manifest.json",
    "python scripts/verify_detection_proof_status_index.py",
    "python scripts/verify_proof_integrity.py",
]

REQUIRED_REVIEWER_STEPS = [
    "Read proof/records/lifetime-case-ledger-v1-proof-bundle.json.",
    "Confirm the bundle source_proof_summary path is proof/records/lifetime-case-ledger-v1-public-summary.json.",
    "Confirm the bundle source_platform_manifest pinned commit is e0580fc8d0b141cbdd71c1b95e3d7885a1d708e0.",
    "Run python scripts/verify-lifetime-ledger-proof-bundle.py --platform-manifest ../hawkinsoperations-platform/contracts/lifetime-case-ledger-v1-state-manifest.json.",
    "Run python scripts/verify-lifetime-ledger-public-summary.py --platform-manifest ../hawkinsoperations-platform/contracts/lifetime-case-ledger-v1-state-manifest.json.",
    "Treat blocked claims and does_not_prove entries as reviewer boundaries, not proof of runtime, signal, public-proof, SOCaaS, production, disposition, or closure status.",
]

DENIED_PATTERNS = [
    ("local absolute path", re.compile(r"(?i)(?:[A-Z]:\\|\\\\)")),
    ("private IPv4 address", re.compile(r"\b(?:10|192\.168|172\.(?:1[6-9]|2[0-9]|3[0-1]))\.\d{1,3}\.\d{1,3}\b")),
    ("raw command line", re.compile(r"(?i)\braw[_ -]?command[_ -]?line\b")),
    ("screenshot", re.compile(r"(?i)\bscreenshot\b")),
    ("secret marker", re.compile(r"(?i)\b(secret|password|credential|api[_-]?key|token)\b")),
    ("private filename", re.compile(r"(?i)\bprivate[_ -]?filename\b")),
    ("raw model output", re.compile(r"(?i)\braw[_ -]?model[_ -]?output\b")),
    ("internal node token", re.compile(r"\bLOCAL_GPU_SUPPORT_NODE\b")),
]


class VerificationError(Exception):
    pass


def fail(message: str) -> None:
    print(f"Lifetime ledger proof bundle verification failed: {message}", file=sys.stderr)
    raise SystemExit(1)


def load_json(path: Path, label: str) -> dict[str, Any]:
    if not path.exists():
        raise VerificationError(f"missing {label}: {path}")
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise VerificationError(f"invalid {label}: {exc}") from exc
    if not isinstance(value, dict):
        raise VerificationError(f"{label} must be a JSON object")
    return value


def scan_private_markers(label: str, value: Any) -> None:
    text = json.dumps(value, sort_keys=True)
    for name, pattern in DENIED_PATTERNS:
        if pattern.search(text):
            raise VerificationError(f"{label} contains blocked private marker: {name}")


def require_sha(value: Any, field: str) -> str:
    if not isinstance(value, str) or not re.fullmatch(r"[0-9a-f]{40}", value):
        raise VerificationError(f"{field} must be a 40-character lowercase git SHA")
    return value


def require_repo_relative_path(value: Any, field: str) -> str:
    if not isinstance(value, str) or not value:
        raise VerificationError(f"{field} must be a repo-relative path")
    if re.match(r"(?i)^[A-Z]:\\", value) or value.startswith("\\\\") or value.startswith("/") or ".." in Path(value).parts:
        raise VerificationError(f"{field} must not be local, absolute, or parent-relative")
    return value.replace("\\", "/")


def require_list_exact(value: Any, expected: list[str], field: str) -> None:
    if value != expected:
        raise VerificationError(f"{field} mismatch")


def require_counts(bundle: dict[str, Any], summary: dict[str, Any], manifest: dict[str, Any]) -> dict[str, int]:
    bundle_counts = bundle.get("ledger_counts")
    summary_counts = summary.get("ledger_counts")
    manifest_counts = manifest.get("current_ledger_counts")
    if not isinstance(bundle_counts, dict) or not isinstance(summary_counts, dict) or not isinstance(manifest_counts, dict):
        raise VerificationError("bundle, summary, and platform manifest must expose ledger count mappings")
    failures = {
        key: {
            "bundle": bundle_counts.get(key),
            "summary": summary_counts.get(key),
            "manifest": manifest_counts.get(key),
            "required": required,
        }
        for key, required in REQUIRED_COUNTS.items()
        if bundle_counts.get(key) != required or summary_counts.get(key) != required or manifest_counts.get(key) != required
    }
    if failures:
        raise VerificationError(f"ledger count drift: {failures}")
    return {key: int(bundle_counts[key]) for key in REQUIRED_COUNTS}


def entries_by_repo(value: Any, field: str) -> dict[str, dict[str, Any]]:
    if not isinstance(value, list):
        raise VerificationError(f"{field} must be a list")
    repos: dict[str, dict[str, Any]] = {}
    for entry in value:
        if not isinstance(entry, dict):
            raise VerificationError(f"{field} entries must be objects")
        repo_name = entry.get("repo_name")
        if not isinstance(repo_name, str) or not repo_name:
            raise VerificationError(f"{field} entries require repo_name")
        require_sha(entry.get("commit_sha"), f"{field}.{repo_name}.commit_sha")
        if repo_name in repos:
            raise VerificationError(f"duplicate repo in {field}: {repo_name}")
        repos[repo_name] = entry
    expected = {".github", "hawkinsoperations-detections", "hawkinsoperations-validation", "hawkinsoperations-platform", "hawkinsoperations-proof", "hawkinsoperations-website"}
    if set(repos) != expected:
        raise VerificationError(f"{field} repo set mismatch")
    return repos


def verify_bundle(bundle_path: Path, summary_path: Path, platform_manifest_path: Path) -> dict[str, Any]:
    bundle = load_json(bundle_path, "Phase 10 proof bundle")
    summary = load_json(summary_path, "Phase 9 proof summary")
    manifest = load_json(platform_manifest_path, "Phase 8 platform manifest")
    scan_private_markers("Phase 10 proof bundle", bundle)

    if bundle.get("bundle_id") != BUNDLE_ID:
        raise VerificationError("bundle_id mismatch")
    if bundle.get("bundle_version") != BUNDLE_VERSION:
        raise VerificationError("bundle_version mismatch")
    if bundle.get("owner_repo") != "hawkinsoperations-proof":
        raise VerificationError("owner_repo mismatch")
    if bundle.get("bundle_status") != "REVIEWER_PACKET_SOURCE_ONLY_NO_TAG_NO_RELEASE":
        raise VerificationError("bundle_status must remain source-only with no tag or release")
    if bundle.get("ledger_boundary") != LEDGER_BOUNDARY:
        raise VerificationError("ledger boundary drifted or was promoted")

    if summary.get("summary_id") != SUMMARY_ID or summary.get("summary_version") != SUMMARY_VERSION:
        raise VerificationError("source proof summary identity mismatch")
    if manifest.get("manifest_id") != PLATFORM_MANIFEST_ID or manifest.get("manifest_version") != PLATFORM_MANIFEST_VERSION:
        raise VerificationError("source platform manifest identity mismatch")
    if manifest.get("source_controlled_manifest") is not True:
        raise VerificationError("platform manifest must be source-controlled")

    source_summary = bundle.get("source_proof_summary")
    if not isinstance(source_summary, dict):
        raise VerificationError("source_proof_summary must be an object")
    if require_repo_relative_path(source_summary.get("repo_relative_path"), "source_proof_summary.repo_relative_path") != "proof/records/lifetime-case-ledger-v1-public-summary.json":
        raise VerificationError("source proof summary path mismatch")
    if source_summary.get("summary_id") != summary.get("summary_id") or source_summary.get("summary_version") != summary.get("summary_version"):
        raise VerificationError("source proof summary metadata mismatch")

    source_manifest = bundle.get("source_platform_manifest")
    if not isinstance(source_manifest, dict):
        raise VerificationError("source_platform_manifest must be an object")
    if require_repo_relative_path(source_manifest.get("repo_relative_path"), "source_platform_manifest.repo_relative_path") != "contracts/lifetime-case-ledger-v1-state-manifest.json":
        raise VerificationError("source platform manifest path mismatch")
    if require_sha(source_manifest.get("pinned_commit_sha"), "source_platform_manifest.pinned_commit_sha") != PLATFORM_MANIFEST_COMMIT_SHA:
        raise VerificationError("source platform manifest is not pinned to the approved Phase 8 commit")
    if source_manifest.get("manifest_id") != manifest.get("manifest_id") or source_manifest.get("manifest_version") != manifest.get("manifest_version"):
        raise VerificationError("source platform manifest metadata mismatch")

    counts = require_counts(bundle, summary, manifest)
    require_list_exact(sorted(bundle.get("appended_detection_ids") or []), APPENDED_DETECTIONS, "appended_detection_ids")
    require_list_exact(sorted(summary.get("appended_detection_ids") or []), APPENDED_DETECTIONS, "source summary appended_detection_ids")
    require_list_exact(sorted(manifest.get("appended_detection_ids") or []), APPENDED_DETECTIONS, "source manifest appended_detection_ids")

    if bundle.get("proof_ceiling") != PROOF_CEILING or summary.get("proof_ceiling") != PROOF_CEILING or manifest.get("proof_ceiling") != PROOF_CEILING:
        raise VerificationError("proof ceiling drifted or was promoted")
    if bundle.get("public_safe_boundary") != summary.get("public_safe_boundary"):
        raise VerificationError("public_safe_boundary must match source proof summary")
    if bundle["public_safe_boundary"].get("ledger_public_safe_status") != "NOT_PUBLIC_SAFE":
        raise VerificationError("ledger public-safe status was promoted")
    for field in ("public_runtime_proof", "public_signal_proof", "public_proof_promotion", "case_closure_authority", "ai_or_analyst_disposition_authority"):
        if bundle["public_safe_boundary"].get(field) is not False:
            raise VerificationError(f"public-safe boundary field must remain false: {field}")

    if bundle.get("does_not_prove") != summary.get("does_not_prove"):
        raise VerificationError("does_not_prove must match source proof summary")
    if bundle.get("blocked_claims") != summary.get("blocked_claims"):
        raise VerificationError("blocked_claims must match source proof summary")
    for required in ("runtime-active public status", "signal-observed public status", "public-safe runtime proof", "SOCaaS deployment", "production deployment", "autonomous SOC", "AI-approved final disposition", "analyst-approved final disposition", "case closure without explicit human-approved closure artifact"):
        if required not in bundle["blocked_claims"]:
            raise VerificationError(f"missing blocked claim: {required}")

    bundle_repos = entries_by_repo(bundle.get("six_repo_sha_reference"), "bundle six_repo_sha_reference")
    summary_repos = entries_by_repo(summary.get("six_repo_sha_reference"), "summary six_repo_sha_reference")
    manifest_repos = entries_by_repo(manifest.get("six_repo_state"), "platform manifest six_repo_state")
    for repo_name, entry in bundle_repos.items():
        if entry != summary_repos[repo_name] or entry != manifest_repos[repo_name]:
            raise VerificationError(f"six-repo SHA reference drift for {repo_name}")

    commands = bundle.get("verifier_commands")
    require_list_exact(commands, REQUIRED_COMMANDS, "verifier_commands")
    steps = bundle.get("reviewer_verification_steps")
    require_list_exact(steps, REQUIRED_REVIEWER_STEPS, "reviewer_verification_steps")

    included = bundle.get("included_source_files")
    require_list_exact(
        included,
        [
            "proof/records/lifetime-case-ledger-v1-proof-bundle.json",
            "proof/records/lifetime-case-ledger-v1-public-summary.json",
            "scripts/verify-lifetime-ledger-proof-bundle.py",
            "scripts/verify-lifetime-ledger-public-summary.py",
            ".github/workflows/governance-gate.yml",
        ],
        "included_source_files",
    )
    for path in included:
        if not (ROOT / path).exists():
            raise VerificationError(f"included source file is missing: {path}")

    return {
        "mode": "verify-lifetime-ledger-proof-bundle",
        "bundle_path": bundle_path.relative_to(ROOT).as_posix(),
        "summary_path": summary_path.relative_to(ROOT).as_posix(),
        "platform_manifest_path": platform_manifest_path.relative_to(ROOT.parent).as_posix()
        if platform_manifest_path.is_relative_to(ROOT.parent)
        else str(platform_manifest_path),
        "platform_manifest_commit_sha": PLATFORM_MANIFEST_COMMIT_SHA,
        "ledger_counts": counts,
        "proof_ceiling": PROOF_CEILING,
        "ledger_public_safe_status": bundle["public_safe_boundary"]["ledger_public_safe_status"],
        "appended_detection_ids": APPENDED_DETECTIONS,
        "six_repo_sha_reference": list(bundle_repos.values()),
        "blocked_claims_verified": sorted(bundle["blocked_claims"]),
        "does_not_prove_verified": sorted(bundle["does_not_prove"]),
    }


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bundle", default=str(BUNDLE_PATH))
    parser.add_argument("--summary", default=str(SUMMARY_PATH))
    parser.add_argument("--platform-manifest", default=str(DEFAULT_PLATFORM_MANIFEST))
    parser.add_argument("--format", default="text", choices=("text", "json"))
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    try:
        result = verify_bundle(Path(args.bundle).resolve(), Path(args.summary).resolve(), Path(args.platform_manifest).resolve())
    except VerificationError as exc:
        fail(str(exc))
    if args.format == "json":
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print("Lifetime ledger proof bundle verification passed.")
        print(f"bundle_path={result['bundle_path']}")
        print(f"summary_path={result['summary_path']}")
        print(f"platform_manifest_commit_sha={result['platform_manifest_commit_sha']}")
        print(f"total_ledger_events={result['ledger_counts']['total_ledger_events']}")
        print(f"total_cases={result['ledger_counts']['total_cases']}")
        print(f"proof_ceiling={result['proof_ceiling']}")
        print(f"ledger_public_safe_status={result['ledger_public_safe_status']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
