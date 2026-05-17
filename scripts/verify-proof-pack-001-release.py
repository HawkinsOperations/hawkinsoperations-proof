#!/usr/bin/env python3
"""Verify Proof Pack 001 release-source boundaries."""
import argparse
import hashlib
import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "RELEASE_MANIFEST.json"
CHECKSUM_PATH = ROOT / "SHA256SUMS.txt"
REVIEWER_PACKET = ROOT / "REVIEWER_PACKET.md"
RELEASE_NOTES_TEMPLATE = ROOT / "RELEASE_NOTES_TEMPLATE.md"
WORKFLOW_PATH = ROOT / ".github" / "workflows" / "publish-proof-release.yml"

EXPECTED_PACK_ID = "HAWKINSOPERATIONS_PROOF_PACK_001"
EXPECTED_DETECTION_ID = "HO-DET-001"
EXPECTED_CEILING = "CONTROLLED_TEST_VALIDATED"
EXPECTED_PUBLIC_SAFE = "NOT_PUBLIC_SAFE"
EXPECTED_TAG = "hawkinsoperations-proof-pack-001"
EXPECTED_RELEASE_STATUS = "CHECK_MODE_SOURCE_ONLY_NO_TAG_NO_RELEASE"

REQUIRED_INCLUDED_FILES = [
    "REVIEWER_PACKET.md",
    "RELEASE_MANIFEST.json",
    "SHA256SUMS.txt",
    "RELEASE_NOTES_TEMPLATE.md",
    "SCOPE.md",
    "GOVERNANCE.md",
    "STATUS.md",
    "proof/cards/HO-DET-001.md",
    "proof/records/HO-DET-001.md",
    "proof/records/HO-DET-001-CONTROLLED-TEST-VALIDATION-001.json",
    "evidence/evidence-ledger.json",
    "evidence/EVIDENCE_LEDGER_SCHEMA.json",
    "scripts/verify-ho-det-001-proof-integrity.py",
    ".github/contracts/proof-record.schema.json",
]

REQUIRED_EXCLUDED_FILES = [
    "README.md",
    "proof/records/HO-NDR-001.md",
    "proof/records/HO-DET-011.md",
    "proof/cards/HO-NDR-001.md",
    "docs/boundaries/HO-NDR-001-SECURITY-ONION-VISIBILITY-CONTRACT.md",
    "docs/debugging/*",
    "proof/records/PROOF-HOD-001-2026-04-21-001.json",
    "proof/records/AWS-DET-001.md",
    "proof/cards/AWS-DET-001.md",
    ".github/workflows/*",
    "docs/case-studies/*",
]

REQUIRED_GENERATED_FILES = [
    "REVIEWER_PACKET.md",
    "RELEASE_MANIFEST.json",
    "SHA256SUMS.txt",
    "RELEASE_NOTES_TEMPLATE.md",
    "scripts/verify-proof-pack-001-release.py",
    ".github/workflows/publish-proof-release.yml",
]

REQUIRED_COMMANDS = [
    "python scripts/verify-ho-det-001-proof-integrity.py",
    "python scripts/verify_proof_integrity.py",
    "python scripts/verify-proof-pack-001-release.py",
    "git diff --check",
]

BLOCKED_TERMS = [
    "runtime-active",
    "signal-observed",
    "evidence-linked public runtime proof",
    "public-safe",
    "production-ready",
    "SOCaaS",
    "live Splunk",
    "Cribl-routed",
    "Wazuh-routed",
    "AWS-live",
    "autonomous SOC",
    "AI-approved disposition",
    "analyst-approved disposition",
    "fleet-wide",
    "enterprise deployment",
]

BLOCKED_CONTEXT_MARKERS = [
    "blocked",
    "not prove",
    "not as proof",
    "does not prove",
    "does not create",
    "does not claim",
    "not claimed",
    "not_public_safe",
    "not public-safe",
    "not approved",
    "must_not_promote",
    "must not promote",
    "must fail",
    "explicitly not claimed",
    "unsupported",
    "excluded",
    "boundary",
    "without",
    "before any",
    "only after",
    "no ",
    "no tag",
    "no release",
    "no_tag_no_release",
]

PRIVATE_LEAK_PATTERNS = [
    ("Windows local path", re.compile(r"(?i)\b(?:C:\\Raylee|C:\\Users|C:\\Work|C:\\Repo|C:\\Data)\b")),
    ("LAN IP", re.compile(r"\b192\.168\.\d{1,3}\.\d{1,3}\b")),
    ("raw screenshot name", re.compile(r"(?i)\b(?:screenshot|screen-shot)[-_ ][\w.-]*\.(?:png|jpg|jpeg)\b")),
    ("raw CSV name", re.compile(r"(?i)\braw[-_ ][\w.-]*\.csv\b")),
    ("credential-like assignment", re.compile(r"(?i)\b(?:api[_-]?key|password|authorization|cookie)\s*[:=]\s*\S+")),
]

FORBIDDEN_CURRENT_RELEASE_CLAIMS = [
    "official release exists",
    "signed GitHub Release artifact exists",
    "GitHub Release exists",
    "release artifact exists",
    "zip published",
    "tag created",
    "signature published",
    "signed artifact exists",
    "public-safe approved",
    "PUBLIC_SAFE approved",
    "RUNTIME_ACTIVE approved",
    "SIGNAL_OBSERVED approved",
]


def fail(message: str) -> None:
    print(f"Proof Pack 001 release verification failed: {message}", file=sys.stderr)
    raise SystemExit(1)


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def load_manifest() -> dict:
    if not MANIFEST_PATH.exists():
        fail("missing RELEASE_MANIFEST.json")
    try:
        return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        fail(f"invalid RELEASE_MANIFEST.json: {exc}")


def require_equal(manifest: dict, key: str, expected: str) -> None:
    if manifest.get(key) != expected:
        fail(f"{key} must be {expected}")


def require_list(manifest: dict, key: str, expected: list[str]) -> None:
    value = manifest.get(key)
    if not isinstance(value, list):
        fail(f"{key} must be a list")
    if value != expected:
        fail(f"{key} does not match expected order/content")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    data = path.read_bytes().replace(b"\r\n", b"\n")
    digest.update(data)
    return digest.hexdigest()


def checksum_targets(manifest: dict) -> list[str]:
    checksum_file = manifest["checksum_file"]
    return [name for name in manifest["included_files"] if name != checksum_file]


def render_checksums(manifest: dict) -> str:
    lines = [
        "# SHA256 checksums for Proof Pack 001 source packet files.",
        "# Generated by: python scripts/verify-proof-pack-001-release.py --write-checksums",
        "# This file is source-controlled packet verification data only.",
        "# It is not a published release checksum file until a later approved release workflow publishes an official artifact.",
    ]
    for name in checksum_targets(manifest):
        path = ROOT / name
        if not path.exists():
            fail(f"cannot checksum missing included file: {name}")
        lines.append(f"{sha256(path)}  {name}")
    return "\n".join(lines) + "\n"


def parse_checksums(text: str) -> dict[str, str]:
    checksums: dict[str, str] = {}
    for line in text.splitlines():
        if not line or line.startswith("#"):
            continue
        match = re.fullmatch(r"([0-9a-f]{64})  (.+)", line)
        if not match:
            fail(f"invalid checksum line: {line}")
        digest, name = match.groups()
        checksums[name] = digest
    return checksums


def validate_manifest(manifest: dict) -> None:
    required_keys = [
        "pack_id",
        "detection_id",
        "ceiling",
        "public_safe",
        "included_files",
        "excluded_files",
        "generated_files",
        "checksum_file",
        "release_tag_planned",
        "release_status",
        "claim_boundary",
        "validation_commands",
        "verifier_command",
    ]
    for key in required_keys:
        if key not in manifest:
            fail(f"manifest missing required key: {key}")

    require_equal(manifest, "pack_id", EXPECTED_PACK_ID)
    require_equal(manifest, "detection_id", EXPECTED_DETECTION_ID)
    require_equal(manifest, "ceiling", EXPECTED_CEILING)
    require_equal(manifest, "public_safe", EXPECTED_PUBLIC_SAFE)
    require_equal(manifest, "checksum_file", "SHA256SUMS.txt")
    require_equal(manifest, "release_tag_planned", EXPECTED_TAG)
    require_equal(manifest, "release_status", EXPECTED_RELEASE_STATUS)
    require_equal(manifest, "verifier_command", "python scripts/verify-proof-pack-001-release.py")
    require_list(manifest, "included_files", REQUIRED_INCLUDED_FILES)
    require_list(manifest, "excluded_files", REQUIRED_EXCLUDED_FILES)
    require_list(manifest, "generated_files", REQUIRED_GENERATED_FILES)
    require_list(manifest, "validation_commands", REQUIRED_COMMANDS)

    boundary = manifest["claim_boundary"]
    if not isinstance(boundary, dict):
        fail("claim_boundary must be an object")
    blocked = boundary.get("must_not_promote")
    if not isinstance(blocked, list):
        fail("claim_boundary.must_not_promote must be a list")
    for term in BLOCKED_TERMS:
        if not any(term.lower() in item.lower() for item in blocked):
            fail(f"claim boundary missing blocked term: {term}")


def validate_files(manifest: dict) -> None:
    for name in manifest["included_files"]:
        path = ROOT / name
        if not path.exists() or not path.is_file():
            fail(f"included file missing: {name}")

    for name in manifest["generated_files"]:
        path = ROOT / name
        if not path.exists() or not path.is_file():
            fail(f"generated file missing: {name}")

    included = set(manifest["included_files"])
    generated = set(manifest["generated_files"])
    for excluded in manifest["excluded_files"]:
        if excluded in included or excluded in generated:
            fail(f"excluded file is listed as included/generated: {excluded}")
    if "proof/records/HO-NDR-001.md" not in manifest["excluded_files"]:
        fail("HO-NDR-001 record must be explicitly excluded")
    if (ROOT / "proof" / "records" / "HO-NDR-001.md").exists():
        fail("proof/records/HO-NDR-001.md must not be present in the Proof Pack 001 source tree")


def validate_checksums(manifest: dict, write_checksums: bool) -> None:
    expected_text = render_checksums(manifest)
    if write_checksums:
        CHECKSUM_PATH.write_text(expected_text, encoding="utf-8", newline="\n")
    if not CHECKSUM_PATH.exists():
        fail("missing SHA256SUMS.txt")
    actual_text = CHECKSUM_PATH.read_text(encoding="utf-8")
    if "PLACEHOLDER" in actual_text:
        fail("SHA256SUMS.txt still contains placeholder checksum state")
    if actual_text != expected_text:
        fail("SHA256SUMS.txt does not match deterministic checksum output")
    parsed = parse_checksums(actual_text)
    expected_targets = checksum_targets(manifest)
    if list(parsed) != expected_targets:
        fail("SHA256SUMS.txt target list does not match manifest included files")


def validate_private_leaks(paths: list[Path]) -> None:
    for path in paths:
        text = path.read_text(encoding="utf-8")
        for label, pattern in PRIVATE_LEAK_PATTERNS:
            match = pattern.search(text)
            if match:
                fail(f"private/local leakage in {rel(path)} matched {label}: {match.group(0)}")


def validate_claim_boundaries(paths: list[Path]) -> None:
    for path in paths:
        text = path.read_text(encoding="utf-8")
        current_section = ""
        for line in text.splitlines():
            heading = re.match(r"^#+\s+(.+?)\s*$", line)
            if heading:
                current_section = heading.group(1).lower()
            lower = line.lower()
            section_boundary_context = any(
                marker in current_section
                for marker in ["blocked", "explicitly not claimed", "excluded", "boundary", "promotion gate", "implementation checks"]
            )
            for forbidden in FORBIDDEN_CURRENT_RELEASE_CLAIMS:
                if forbidden.lower() not in lower:
                    continue
                if section_boundary_context or any(marker in lower for marker in BLOCKED_CONTEXT_MARKERS):
                    continue
                fail(f"release wording implies current publication in {rel(path)}: {line}")
            for term in BLOCKED_TERMS:
                if term.lower() not in lower:
                    continue
                if "not_public_safe" in lower or "not public-safe" in lower:
                    continue
                if section_boundary_context or any(marker in lower for marker in BLOCKED_CONTEXT_MARKERS):
                    continue
                fail(f"blocked claim appears outside boundary context in {rel(path)}: {line}")


def validate_workflow() -> None:
    if not WORKFLOW_PATH.exists():
        fail("missing .github/workflows/publish-proof-release.yml")
    text = WORKFLOW_PATH.read_text(encoding="utf-8")
    required = [
        "workflow_dispatch:",
        "pull_request:",
        "contents: read",
        "python scripts/verify-proof-pack-001-release.py",
        "python scripts/verify-ho-det-001-proof-integrity.py",
        "python scripts/verify_proof_integrity.py",
        "git diff --check",
    ]
    for item in required:
        if item not in text:
            fail(f"release workflow missing required check-mode marker: {item}")
    forbidden = [
        "gh release create",
        "git tag",
        "git push",
        "cosign sign",
        "upload-artifact",
        "Compress-Archive",
        "zip ",
    ]
    for item in forbidden:
        if item.lower() in text.lower():
            fail(f"release workflow contains forbidden publication behavior: {item}")
    if re.search(r"(?m)^\s+push:\s*$", text):
        fail("release workflow must not run on push")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-checksums", action="store_true")
    args = parser.parse_args()

    manifest = load_manifest()
    validate_manifest(manifest)
    validate_files(manifest)
    validate_checksums(manifest, args.write_checksums)
    text_paths = [
        REVIEWER_PACKET,
        MANIFEST_PATH,
        RELEASE_NOTES_TEMPLATE,
        ROOT / "proof" / "cards" / "HO-DET-001.md",
        WORKFLOW_PATH,
    ]
    claim_text_paths = [
        REVIEWER_PACKET,
        RELEASE_NOTES_TEMPLATE,
        ROOT / "proof" / "cards" / "HO-DET-001.md",
        WORKFLOW_PATH,
    ]
    validate_private_leaks(text_paths)
    validate_claim_boundaries(claim_text_paths)
    validate_workflow()
    print("Proof Pack 001 release source verification passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
