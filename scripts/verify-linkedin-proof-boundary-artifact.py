#!/usr/bin/env python3
"""Verify the LinkedIn proof-boundary artifact packet."""
from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PACKET_DIR = ROOT / "docs" / "linkedin" / "proof-boundary-what-system-refused-2026-06-01"

PACKET_FILES = [
    "README.md",
    "WHAT_THE_SYSTEM_REFUSED_TO_CLAIM.md",
    "proof-boundary-map.json",
    "ARTIFACT_MANIFEST.json",
    "CHECKSUMS.sha256",
]

REQUIRED_ARTIFACTS = [
    "Detection Source",
    "Validation",
    "Website",
    "Proof Pack 001",
    "AI Support",
]

REQUIRED_CEILING = "CONTROLLED_TEST_VALIDATED"
REQUIRED_RUNTIME_STATUS = "NOT_PUBLIC_SAFE"

PRIVATE_TERMS = [
    "MU" + "FG",
    "Dou" + "glas",
    "Fort" + "inet",
    "Zach" + "ari",
    "Michael" + " Lee",
    "LinkedIn " + "screen" + "shot",
    "raw " + "evidence",
    "Tailscale " + "hostname",
    "Wazuh " + "manager IP",
    "Cribl " + "host",
    "Splunk " + "host",
]

PRIVATE_PATTERNS = [
    ("Windows local path", re.compile(r"(?i)(?:[A-Z]:\\|\\\\)")),
    ("private IPv4 address", re.compile(r"\b(?:10|100|192\.168|172\.(?:1[6-9]|2[0-9]|3[0-1]))\.\d{1,3}\.\d{1,3}\b")),
    (
        "credential-like marker",
        re.compile(
            r"(?i)\b(?:"
            + "pass"
            + "word|sec"
            + "ret|tok"
            + "en|api"
            + "key|api"
            + "_key|private"
            + " key)\b"
        ),
    ),
]

FORBIDDEN_POSITIVE_CLAIMS = [
    "production deployment",
    "production-ready",
    "customer deployment",
    "live customer",
    "SOCaaS available",
    "SOCaaS availability",
    "runtime proven",
    "runtime-active public proof",
    "signal-observed public proof",
    "public-safe runtime proof",
    "autonomous SOC",
    "AI-approved disposition",
    "AI-decided disposition",
    "analyst-approved disposition",
    "fleet-wide",
    "live Wazuh",
    "live Splunk",
    "Cribl-routed",
    "AWS-live",
]

BOUNDARY_MARKERS = [
    "blocked",
    "not prove",
    "does not prove",
    "does not claim",
    "not claimed",
    "not ",
    "not public-safe",
    "not_public_safe",
    "no ",
    "refused",
    "forbidden",
    "without",
    "cannot",
    "must not",
    "remains blocked",
]


class VerificationError(Exception):
    """Raised when packet verification fails."""


def fail(message: str) -> None:
    raise VerificationError(message)


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def read(path: Path) -> str:
    if not path.exists():
        fail(f"missing file: {rel(path)}")
    return path.read_text(encoding="utf-8")


def load_json(path: Path) -> dict[str, Any]:
    text = read(path)
    try:
        data = json.loads(text)
    except json.JSONDecodeError as exc:
        fail(f"invalid JSON in {rel(path)}: {exc}")
    if not isinstance(data, dict):
        fail(f"{rel(path)} must contain a JSON object")
    return data


def has_boundary_context(line: str) -> bool:
    lowered = line.lower()
    return any(marker in lowered for marker in BOUNDARY_MARKERS)


def scan_private_text(path: Path, text: str) -> None:
    for term in PRIVATE_TERMS:
        if term.lower() in text.lower():
            fail(f"private term appears in {rel(path)}: {term}")
    for label, pattern in PRIVATE_PATTERNS:
        if pattern.search(text):
            fail(f"{label} appears in {rel(path)}")


def scan_forbidden_positive_claims(path: Path, text: str) -> None:
    for line_number, line in enumerate(text.splitlines(), start=1):
        lowered = line.lower()
        for claim in FORBIDDEN_POSITIVE_CLAIMS:
            if claim.lower() in lowered and not has_boundary_context(lowered):
                fail(f"forbidden positive claim in {rel(path)}:{line_number}: {claim}")


def verify_markdown_tables(text: str, path: Path) -> None:
    for artifact in REQUIRED_ARTIFACTS:
        if artifact not in text:
            fail(f"missing required artifact row in {rel(path)}: {artifact}")
    required_headers = ["Artifact", "What it proves", "What it does not prove"]
    for header in required_headers:
        if header not in text:
            fail(f"missing table header in {rel(path)}: {header}")


def verify_map(data: dict[str, Any]) -> None:
    entries = data.get("entries")
    if not isinstance(entries, list):
        fail("proof-boundary-map.json entries must be a list")
    seen = {entry.get("artifact") for entry in entries if isinstance(entry, dict)}
    for artifact in REQUIRED_ARTIFACTS:
        if artifact not in seen:
            fail(f"proof-boundary-map.json missing artifact: {artifact}")
    for entry in entries:
        if not isinstance(entry, dict):
            fail("proof-boundary-map.json entries must be objects")
        for key in [
            "artifact",
            "proves",
            "does_not_prove",
            "source_repo",
            "source_route",
            "proof_ceiling",
            "public_safe_status",
            "notes",
        ]:
            if key not in entry:
                fail(f"proof-boundary-map.json entry missing key: {key}")
        if entry["artifact"] in {"Detection Source", "Validation", "Proof Pack 001"}:
            if entry["proof_ceiling"] != REQUIRED_CEILING:
                fail(f"{entry['artifact']} proof ceiling must remain {REQUIRED_CEILING}")
        if "runtime" in " ".join(entry.get("does_not_prove", [])).lower():
            if REQUIRED_RUNTIME_STATUS not in entry["public_safe_status"]:
                fail(f"{entry['artifact']} public_safe_status must preserve {REQUIRED_RUNTIME_STATUS}")


def verify_manifest(data: dict[str, Any]) -> None:
    required = [
        "packet_name",
        "created_date",
        "repo",
        "claim_ceiling",
        "public_safe_status",
        "files",
        "source_repos_checked",
        "forbidden_claims",
        "verification_commands",
    ]
    for key in required:
        if key not in data:
            fail(f"ARTIFACT_MANIFEST.json missing key: {key}")
    if data["claim_ceiling"] != "PUBLIC_SUMMARY_SAFE_CANDIDATE_WITH_CONTROLLED_TEST_VALIDATED_REFERENCES":
        fail("manifest claim ceiling must remain a public-summary candidate")
    if data["public_safe_status"] != "NOT_PUBLIC_SAFE_PUBLICATION_REQUIRES_REVIEW":
        fail("manifest public_safe_status must require review")
    manifest_files = data.get("files")
    if manifest_files != PACKET_FILES:
        fail("manifest files must match packet files in order")
    source_repos = data.get("source_repos_checked")
    if not isinstance(source_repos, list) or len(source_repos) < 6:
        fail("manifest must list the six source repos checked")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    digest.update(path.read_bytes().replace(b"\r\n", b"\n"))
    return digest.hexdigest()


def verify_checksums() -> None:
    checksum_path = PACKET_DIR / "CHECKSUMS.sha256"
    text = read(checksum_path)
    parsed: dict[str, str] = {}
    for line in text.splitlines():
        if not line or line.startswith("#"):
            continue
        match = re.fullmatch(r"([0-9a-f]{64})  (.+)", line)
        if not match:
            fail(f"invalid checksum line: {line}")
        parsed[match.group(2)] = match.group(1)
    for name in PACKET_FILES:
        if name == "CHECKSUMS.sha256":
            continue
        path = PACKET_DIR / name
        expected = parsed.get(name)
        if not expected:
            fail(f"CHECKSUMS.sha256 missing entry for {name}")
        actual = sha256(path)
        if actual != expected:
            fail(f"checksum mismatch for {name}: expected {expected}, got {actual}")


def main() -> int:
    try:
        for name in PACKET_FILES:
            path = PACKET_DIR / name
            text = read(path)
            scan_private_text(path, text)
            scan_forbidden_positive_claims(path, text)

        verify_markdown_tables(read(PACKET_DIR / "README.md"), PACKET_DIR / "README.md")
        verify_markdown_tables(
            read(PACKET_DIR / "WHAT_THE_SYSTEM_REFUSED_TO_CLAIM.md"),
            PACKET_DIR / "WHAT_THE_SYSTEM_REFUSED_TO_CLAIM.md",
        )
        verify_map(load_json(PACKET_DIR / "proof-boundary-map.json"))
        verify_manifest(load_json(PACKET_DIR / "ARTIFACT_MANIFEST.json"))
        verify_checksums()
    except VerificationError as exc:
        print(f"LINKEDIN_PROOF_BOUNDARY_ARTIFACT=fail: {exc}", file=sys.stderr)
        return 1

    print("LINKEDIN_PROOF_BOUNDARY_ARTIFACT=pass")
    return 0


if __name__ == "__main__":
    sys.exit(main())
