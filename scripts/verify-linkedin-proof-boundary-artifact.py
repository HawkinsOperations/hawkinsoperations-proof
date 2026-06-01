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
    "Wazuh CI",
    "Reviewer Metrics",
    "Website",
    "Proof Pack 001",
    "Runtime Route Proof v1",
    "Runner Trust Split",
    "Green CI / Merge Authority",
    "AI Support",
]

VISUAL_TABLE_ARTIFACTS = [
    "Detection Source",
    "Validation",
    "Website",
    "Proof Pack 001",
    "AI Support",
]

README_REQUIRED_SECTIONS = [
    "## Executive Summary",
    "## The Problem",
    "## The Control Pattern",
    "## The Public-Safe Boundary Matrix",
    "## Deeper Evidence Threads",
    "### 1. Detection Source Is Source Truth",
    "### 2. Validation Is Controlled Validation Truth",
    "### 3. Wazuh CI Refused Runtime Overclaim",
    "### 4. Reviewer Metrics Refused Metric Inflation",
    "### 5. Website Rendering Refused Proof Authority",
    "### 6. Proof Pack 001 Preserved Claim Ceiling",
    "### 7. Runtime Route Proof v1 Stayed Private / Blocked",
    "### 8. Runner Trust Split Refused Public PR Self-Hosted Exposure",
    "### 9. Green CI Refused Merge Authority",
    "### 10. AI Support Refused Final Authority",
    "## What This Packet Proves",
    "## What This Packet Does Not Prove",
    "## LinkedIn Usage",
    "## Reviewer Links",
    "## Verification",
]

WHAT_REQUIRED_SECTIONS = [
    "## Final Table",
    "## Why This Is Deeper Than a Table",
    "## Control Pattern Behind the Post",
    "## Deeper Evidence Threads",
    "## Final LinkedIn Caption",
    "## First Comment Text",
    "## Do Not Claim",
]

DEEP_THREAD_HEADINGS = [
    "Detection Source Is Source Truth",
    "Validation Is Controlled Validation Truth",
    "Wazuh CI Refused Runtime Overclaim",
    "Reviewer Metrics Refused Metric Inflation",
    "Website Rendering Refused Proof Authority",
    "Proof Pack 001 Preserved Claim Ceiling",
    "Runtime Route Proof v1 Stayed Private / Blocked",
    "Runner Trust Split Refused Public PR Self-Hosted Exposure",
    "Green CI Refused Merge Authority",
    "AI Support Refused Final Authority",
]

REVIEWER_METRIC_TOKENS = [
    "4 governed cases",
    "49 controlled validation fires",
    "106 validation cases",
    "8 proof records",
    "31 blocked claims",
    "public-safe count 0",
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
    "recommended disposition",
    "containment approved",
    "case closure approved",
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
    for artifact in VISUAL_TABLE_ARTIFACTS:
        if artifact not in text:
            fail(f"missing required artifact row in {rel(path)}: {artifact}")
    required_headers = ["Artifact", "What it proves", "What it does not prove"]
    for header in required_headers:
        if header not in text:
            fail(f"missing table header in {rel(path)}: {header}")


def require_sections(text: str, path: Path, sections: list[str]) -> None:
    for section in sections:
        if section not in text:
            fail(f"missing required section in {rel(path)}: {section}")


def verify_deep_content(readme: str, what_file: str) -> None:
    for heading in DEEP_THREAD_HEADINGS:
        if heading not in readme:
            fail(f"README missing deeper evidence thread: {heading}")
        if heading not in what_file:
            fail(f"WHAT_THE_SYSTEM_REFUSED_TO_CLAIM missing deeper evidence thread: {heading}")
    for token in REVIEWER_METRIC_TOKENS:
        if token not in readme:
            fail(f"README missing reviewer metric token: {token}")
    if "Website rendering is not proof" not in readme:
        fail("README must explicitly say website rendering is not proof")
    if "Checks are evidence, not authority" not in readme:
        fail("README must explicitly say checks are evidence, not authority")
    if "AI is labor" not in readme or "governance" not in readme.lower():
        fail("README must preserve AI labor / governance authority boundary")


def verify_map(data: dict[str, Any]) -> None:
    entries = data.get("entries")
    if not isinstance(entries, list):
        fail("proof-boundary-map.json entries must be a list")
    seen = {entry.get("artifact") for entry in entries if isinstance(entry, dict)}
    if seen != set(REQUIRED_ARTIFACTS) or len(entries) != len(REQUIRED_ARTIFACTS):
        fail("proof-boundary-map.json must contain exactly the expanded required entries")
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
            "why_it_matters",
            "source_repo",
            "source_route",
            "supporting_public_routes",
            "proof_ceiling",
            "public_safe_status",
            "blocked_claims",
            "linkedin_visual_row",
            "notes",
        ]:
            if key not in entry:
                fail(f"proof-boundary-map.json entry missing key: {key}")
        for array_key in ["proves", "does_not_prove", "supporting_public_routes", "blocked_claims"]:
            value = entry.get(array_key)
            if not isinstance(value, list) or not value:
                fail(f"proof-boundary-map.json {entry['artifact']} {array_key} must be a non-empty list")
        if not isinstance(entry.get("linkedin_visual_row"), bool):
            fail(f"proof-boundary-map.json {entry['artifact']} linkedin_visual_row must be boolean")
        if entry["artifact"] in {"Detection Source", "Validation", "Proof Pack 001"}:
            if entry["proof_ceiling"] != REQUIRED_CEILING:
                fail(f"{entry['artifact']} proof ceiling must remain {REQUIRED_CEILING}")
        if "runtime" in " ".join(entry.get("does_not_prove", [])).lower():
            if REQUIRED_RUNTIME_STATUS not in entry["public_safe_status"]:
                fail(f"{entry['artifact']} public_safe_status must preserve {REQUIRED_RUNTIME_STATUS}")
        if entry["artifact"] == "Reviewer Metrics":
            joined = json.dumps(entry, sort_keys=True)
            for token in REVIEWER_METRIC_TOKENS:
                if token not in joined:
                    fail(f"Reviewer Metrics map entry missing token: {token}")
            if "public-safe runtime proof" not in " ".join(entry.get("blocked_claims", [])).lower():
                fail("Reviewer Metrics must block public-safe runtime proof")
        if entry["artifact"] == "Website":
            joined = json.dumps(entry, sort_keys=True).lower()
            if "navigation" not in joined or "not proof" not in joined:
                fail("Website map entry must remain navigation/rendering only, not proof authority")
        if entry["artifact"] == "AI Support":
            joined = json.dumps(entry, sort_keys=True).lower()
            if "support" not in joined or "authority" not in joined:
                fail("AI Support map entry must preserve support/labor only, not final authority")


def verify_manifest(data: dict[str, Any]) -> None:
    required = [
        "packet_name",
        "packet_purpose",
        "linkedin_post_hook",
        "created_date",
        "repo",
        "claim_ceiling",
        "public_safe_status",
        "files",
        "source_repos_checked",
        "public_routes_checked",
        "forbidden_claims",
        "supported_artifact_categories",
        "excluded_private_categories",
        "no_zip_reason",
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
    categories = data.get("supported_artifact_categories")
    if not isinstance(categories, list):
        fail("manifest supported_artifact_categories must be a list")
    for artifact in REQUIRED_ARTIFACTS:
        if artifact not in categories:
            fail(f"manifest missing supported artifact category: {artifact}")
    if data.get("no_zip_reason") != "ZIP_COMMIT_BLOCKED_BY_REPO_PATTERN":
        fail("manifest must preserve no-zip reason")
    public_routes = data.get("public_routes_checked")
    if not isinstance(public_routes, list) or len(public_routes) < 5:
        fail("manifest public_routes_checked must list public routes")
    excluded = data.get("excluded_private_categories")
    if not isinstance(excluded, list) or not excluded:
        fail("manifest excluded_private_categories must be a non-empty list")


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
    extras = sorted(set(parsed) - {name for name in PACKET_FILES if name != "CHECKSUMS.sha256"})
    if extras:
        fail(f"CHECKSUMS.sha256 contains extra entries: {', '.join(extras)}")


def main() -> int:
    try:
        for name in PACKET_FILES:
            path = PACKET_DIR / name
            text = read(path)
            scan_private_text(path, text)
            scan_forbidden_positive_claims(path, text)

        readme = read(PACKET_DIR / "README.md")
        what_file = read(PACKET_DIR / "WHAT_THE_SYSTEM_REFUSED_TO_CLAIM.md")
        require_sections(readme, PACKET_DIR / "README.md", README_REQUIRED_SECTIONS)
        require_sections(what_file, PACKET_DIR / "WHAT_THE_SYSTEM_REFUSED_TO_CLAIM.md", WHAT_REQUIRED_SECTIONS)
        verify_markdown_tables(readme, PACKET_DIR / "README.md")
        verify_markdown_tables(what_file, PACKET_DIR / "WHAT_THE_SYSTEM_REFUSED_TO_CLAIM.md")
        verify_deep_content(readme, what_file)
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
