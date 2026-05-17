#!/usr/bin/env python3
"""Verify a local Proof Pack 001 ZIP payload without publishing it."""
from __future__ import annotations

import argparse
import fnmatch
import hashlib
import json
import re
import sys
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "RELEASE_MANIFEST.json"
EXPECTED_PACK_ID = "HAWKINSOPERATIONS_PROOF_PACK_001"
EXPECTED_DETECTION_ID = "HO-DET-001"
EXPECTED_CEILING = "CONTROLLED_TEST_VALIDATED"
EXPECTED_PUBLIC_SAFE = "NOT_PUBLIC_SAFE"
ZIP_NAME = "HAWKINSOPERATIONS_PROOF_PACK_001.zip"

FORBIDDEN_PAYLOAD_PATTERNS = [
    "proof/records/HO-NDR-001.md",
    "docs/debugging/*",
    "docs/case-studies/*",
    ".github/workflows/*",
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
    "AI-decided disposition",
    "analyst-approved disposition",
    "fleet-wide",
    "enterprise deployed",
    "enterprise deployment",
    "production AutoSOC",
]

BOUNDARY_MARKERS = [
    "blocked",
    "not prove",
    "does not prove",
    "does not claim",
    "not claimed",
    "not_public_safe",
    "not public-safe",
    "must_not_promote",
    "must not promote",
    "unsupported",
    "excluded",
    "boundary",
    "no ",
    "no tag",
    "no release",
    "pending",
    "requires",
]

PRIVATE_LEAK_PATTERNS = [
    ("Windows local path", re.compile(r"(?i)\b(?:C:\\Raylee|C:\\Users|C:\\Work|C:\\Repo|C:\\Data)\b")),
    ("LAN IP", re.compile(r"\b(?:(?:10|127)\.\d{1,3}|172\.(?:1[6-9]|2[0-9]|3[0-1])|192\.168)\.\d{1,3}\.\d{1,3}\b")),
    ("raw screenshot name", re.compile(r"(?i)\b(?:screenshot|screen-shot)[-_ ][\w.-]*\.(?:png|jpg|jpeg)\b")),
    ("raw Security Onion reference", re.compile(r"(?i)\braw\s+Security Onion\b")),
    ("raw Splunk export reference", re.compile(r"(?i)\braw\s+Splunk\s+export\b")),
    ("private career screenshot", re.compile(r"(?i)\b(?:LinkedIn|recruiter|opportunity|private contact)[-_ ][\w.-]*\.(?:png|jpg|jpeg)\b")),
    ("credential-like assignment", re.compile(r"(?i)\b(?:api[_-]?key|password|authorization|cookie|token|secret)\s*[:=]\s*\S+")),
    ("private GPU host", re.compile(r"\bHO-GPU-\d+\b")),
]


def fail(message: str) -> None:
    print(f"Proof Pack 001 ZIP verification failed: {message}", file=sys.stderr)
    raise SystemExit(1)


def load_manifest() -> dict:
    try:
        return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    except FileNotFoundError:
        fail("missing RELEASE_MANIFEST.json")
    except json.JSONDecodeError as exc:
        fail(f"invalid RELEASE_MANIFEST.json: {exc}")


def normalize_name(name: str) -> str:
    normalized = name.replace("\\", "/").strip("/")
    if not normalized or normalized.startswith("../") or "/../" in normalized:
        fail(f"unsafe payload path: {name}")
    return normalized


def matches_any(name: str, patterns: list[str]) -> bool:
    return any(fnmatch.fnmatchcase(name, pattern) for pattern in patterns)


def expected_payload(manifest: dict) -> list[str]:
    if manifest.get("pack_id") != EXPECTED_PACK_ID:
        fail(f"pack_id must be {EXPECTED_PACK_ID}")
    if manifest.get("detection_id") != EXPECTED_DETECTION_ID:
        fail(f"detection_id must be {EXPECTED_DETECTION_ID}")
    if manifest.get("ceiling") != EXPECTED_CEILING:
        fail(f"ceiling must be {EXPECTED_CEILING}")
    if manifest.get("public_safe") != EXPECTED_PUBLIC_SAFE:
        fail(f"public_safe must be {EXPECTED_PUBLIC_SAFE}")
    included = [normalize_name(name) for name in manifest.get("included_files", [])]
    excluded = [normalize_name(name) for name in manifest.get("excluded_files", [])]
    if not included:
        fail("manifest included_files is empty")
    for name in included:
        if name in excluded or matches_any(name, excluded):
            fail(f"included file is excluded: {name}")
        if matches_any(name, FORBIDDEN_PAYLOAD_PATTERNS):
            fail(f"forbidden path would be included: {name}")
    return included


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def parse_checksums(text: str) -> dict[str, str]:
    checksums: dict[str, str] = {}
    for line in text.splitlines():
        if not line or line.startswith("#"):
            continue
        match = re.fullmatch(r"([0-9a-f]{64})  (.+)", line)
        if not match:
            fail(f"invalid checksum line: {line}")
        digest, name = match.groups()
        checksums[normalize_name(name)] = digest
    return checksums


def scan_private_leaks(name: str, data: bytes) -> None:
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError:
        return
    for label, pattern in PRIVATE_LEAK_PATTERNS:
        match = pattern.search(text)
        if match:
            fail(f"private/local leakage in {name} matched {label}: {match.group(0)}")


def validate_claim_boundary(name: str, data: bytes) -> None:
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError:
        return
    current_section = ""
    for line in text.splitlines():
        heading = re.match(r"^#+\s+(.+?)\s*$", line)
        if heading:
            current_section = heading.group(1).lower()
        lower = line.lower()
        boundary_context = any(marker in current_section for marker in ["blocked", "boundary", "excluded", "not claimed"])
        for term in BLOCKED_TERMS:
            if term.lower() not in lower:
                continue
            if "not_public_safe" in lower or "not public-safe" in lower:
                continue
            if boundary_context or any(marker in lower for marker in BOUNDARY_MARKERS):
                continue
            fail(f"blocked claim appears outside boundary context in {name}: {line}")


def verify_zip(zip_path: Path, manifest: dict) -> None:
    if not zip_path.is_file():
        fail(f"ZIP path does not exist: {zip_path}")
    expected = expected_payload(manifest)
    with zipfile.ZipFile(zip_path, "r") as archive:
        names = [normalize_name(name) for name in archive.namelist()]
        if names != expected:
            fail("ZIP included file list does not match RELEASE_MANIFEST.json included_files")
        for name in names:
            if matches_any(name, FORBIDDEN_PAYLOAD_PATTERNS):
                fail(f"forbidden path present in ZIP: {name}")
        manifest_inside = json.loads(archive.read("RELEASE_MANIFEST.json").decode("utf-8"))
        if manifest_inside.get("ceiling") != EXPECTED_CEILING:
            fail(f"ZIP manifest ceiling must be {EXPECTED_CEILING}")
        if manifest_inside.get("public_safe") != EXPECTED_PUBLIC_SAFE:
            fail(f"ZIP manifest public_safe must be {EXPECTED_PUBLIC_SAFE}")
        checksums = parse_checksums(archive.read("SHA256SUMS.txt").decode("utf-8"))
        expected_checksum_targets = [name for name in expected if name != "SHA256SUMS.txt"]
        if list(checksums) != expected_checksum_targets:
            fail("SHA256SUMS.txt target list does not match ZIP payload")
        for name in names:
            data = archive.read(name)
            scan_private_leaks(name, data)
            validate_claim_boundary(name, data)
            if name == "SHA256SUMS.txt":
                continue
            normalized_digest = sha256_bytes(data.replace(b"\r\n", b"\n"))
            if checksums.get(name) != normalized_digest:
                fail(f"checksum mismatch for {name}")


def verify_sidecar(zip_path: Path) -> None:
    sidecar = zip_path.with_name("HAWKINSOPERATIONS_PROOF_PACK_001.payload-sha256sums.txt")
    if not sidecar.exists():
        return
    checksums = parse_checksums(sidecar.read_text(encoding="utf-8"))
    if checksums.get(zip_path.name) != sha256_bytes(zip_path.read_bytes()):
        fail("sidecar ZIP checksum does not match")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("zip_path", nargs="?", help="ZIP to verify")
    parser.add_argument("--check", action="store_true", help="validate verifier inputs without requiring a ZIP")
    args = parser.parse_args()

    manifest = load_manifest()
    expected_payload(manifest)
    if args.check and not args.zip_path:
        print("Proof Pack 001 ZIP verifier check passed.")
        print(f"Expected ZIP name: {ZIP_NAME}")
        return 0
    if not args.zip_path:
        fail("ZIP path argument is required unless --check is used")
    zip_path = Path(args.zip_path)
    verify_zip(zip_path, manifest)
    verify_sidecar(zip_path)
    print("Proof Pack 001 ZIP verification passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
