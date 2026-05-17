#!/usr/bin/env python3
"""Build a deterministic local Proof Pack 001 ZIP payload."""
from __future__ import annotations

import argparse
import fnmatch
import hashlib
import json
import os
import re
import subprocess
import sys
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "RELEASE_MANIFEST.json"
DEFAULT_OUTPUT_DIR = ROOT / "dist" / "proof-pack-001"
ZIP_NAME = "HAWKINSOPERATIONS_PROOF_PACK_001.zip"
PAYLOAD_MANIFEST_NAME = "HAWKINSOPERATIONS_PROOF_PACK_001.payload-manifest.json"
PAYLOAD_SHA256_NAME = "HAWKINSOPERATIONS_PROOF_PACK_001.payload-sha256sums.txt"
EXPECTED_PACK_ID = "HAWKINSOPERATIONS_PROOF_PACK_001"
EXPECTED_DETECTION_ID = "HO-DET-001"
EXPECTED_CEILING = "CONTROLLED_TEST_VALIDATED"
EXPECTED_PUBLIC_SAFE = "PUBLIC_SAFE_REVIEWER_RELEASE_CANDIDATE"
EXPECTED_RUNTIME_PUBLIC_SAFE = "NOT_PUBLIC_SAFE"
EXPECTED_PUBLIC_SAFE_RUNTIME_PROOF = "BLOCKED"
RELEASE_APPROVAL = "RELEASE_APPROVED_PROOF_PACK_001"
ZIP_TIMESTAMP = (2026, 1, 1, 0, 0, 0)

FORBIDDEN_PAYLOAD_PATTERNS = [
    "proof/records/HO-NDR-001.md",
    "docs/debugging/*",
    "docs/case-studies/*",
    ".github/workflows/*",
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
    print(f"Proof Pack 001 ZIP build failed: {message}", file=sys.stderr)
    raise SystemExit(1)


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def load_manifest() -> dict:
    try:
        manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    except FileNotFoundError:
        fail("missing RELEASE_MANIFEST.json")
    except json.JSONDecodeError as exc:
        fail(f"invalid RELEASE_MANIFEST.json: {exc}")
    return manifest


def require_manifest_boundary(manifest: dict) -> None:
    expected = {
        "pack_id": EXPECTED_PACK_ID,
        "detection_id": EXPECTED_DETECTION_ID,
        "ceiling": EXPECTED_CEILING,
        "public_safe": EXPECTED_PUBLIC_SAFE,
        "raw_private_runtime_evidence_public_safe": EXPECTED_RUNTIME_PUBLIC_SAFE,
        "public_safe_runtime_proof": EXPECTED_PUBLIC_SAFE_RUNTIME_PROOF,
    }
    for key, value in expected.items():
        if manifest.get(key) != value:
            fail(f"{key} must be {value}")
    if not isinstance(manifest.get("included_files"), list):
        fail("included_files must be a list")
    if not isinstance(manifest.get("excluded_files"), list):
        fail("excluded_files must be a list")


def normalize_name(name: str) -> str:
    normalized = name.replace("\\", "/").strip("/")
    if not normalized or normalized.startswith("../") or "/../" in normalized:
        fail(f"unsafe payload path: {name}")
    return normalized


def matches_any(name: str, patterns: list[str]) -> bool:
    return any(fnmatch.fnmatchcase(name, pattern) for pattern in patterns)


def assert_allowed_payload(manifest: dict) -> list[str]:
    included = [normalize_name(name) for name in manifest["included_files"]]
    excluded = [normalize_name(name) for name in manifest["excluded_files"]]
    if len(included) != len(set(included)):
        fail("included_files contains duplicates")
    for name in included:
        path = ROOT / name
        if not path.is_file():
            fail(f"included file missing: {name}")
        if name in excluded or matches_any(name, excluded):
            fail(f"included file is excluded: {name}")
        if matches_any(name, FORBIDDEN_PAYLOAD_PATTERNS):
            fail(f"forbidden payload path would be included: {name}")
    if (ROOT / "proof" / "records" / "HO-NDR-001.md").exists():
        fail("proof/records/HO-NDR-001.md exists and must not be packaged")
    return included


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def scan_private_leaks(names: list[str]) -> None:
    for name in names:
        path = ROOT / name
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for label, pattern in PRIVATE_LEAK_PATTERNS:
            match = pattern.search(text)
            if match:
                fail(f"private/local leakage in {name} matched {label}: {match.group(0)}")


def is_ignored(path: Path) -> bool:
    result = subprocess.run(
        ["git", "check-ignore", "-q", str(path.relative_to(ROOT).as_posix())],
        cwd=ROOT,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False,
    )
    return result.returncode == 0


def output_label(args: argparse.Namespace) -> str:
    if args.official:
        approval = args.release_approved or os.environ.get("RELEASE_APPROVAL", "")
        if approval != RELEASE_APPROVAL:
            fail(
                "official mode requires --release-approved RELEASE_APPROVED_PROOF_PACK_001 "
                "or RELEASE_APPROVAL=RELEASE_APPROVED_PROOF_PACK_001"
            )
        return "OFFICIAL_RELEASE_CANDIDATE_PENDING_GITHUB_RELEASE_PUBLICATION"
    return "PUBLIC_SAFE_REVIEWER_RELEASE_CANDIDATE"


def build_payload_manifest(names: list[str], label: str) -> dict:
    return {
        "pack_id": EXPECTED_PACK_ID,
        "detection_id": EXPECTED_DETECTION_ID,
        "ceiling": EXPECTED_CEILING,
        "public_safe": EXPECTED_PUBLIC_SAFE,
        "raw_private_runtime_evidence_public_safe": EXPECTED_RUNTIME_PUBLIC_SAFE,
        "public_safe_runtime_proof": EXPECTED_PUBLIC_SAFE_RUNTIME_PROOF,
        "artifact_status": label,
        "zip_name": ZIP_NAME,
        "included_files": [
            {
                "path": name,
                "sha256": sha256_file(ROOT / name),
                "size": (ROOT / name).stat().st_size,
            }
            for name in names
        ],
    }


def render_payload_sha256sums(payload: dict, zip_path: Path | None = None) -> str:
    lines = [
        "# SHA256 checksums for Proof Pack 001 ZIP payload files.",
        "# This is local release-candidate checksum data until an approved GitHub Release publishes it.",
    ]
    for item in payload["included_files"]:
        lines.append(f"{item['sha256']}  {item['path']}")
    if zip_path is not None:
        lines.append(f"{sha256_file(zip_path)}  {zip_path.name}")
    return "\n".join(lines) + "\n"


def write_zip(names: list[str], zip_path: Path) -> None:
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for name in names:
            data = (ROOT / name).read_bytes()
            info = zipfile.ZipInfo(filename=name, date_time=ZIP_TIMESTAMP)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            archive.writestr(info, data)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="validate build inputs without writing artifacts")
    parser.add_argument("--output-dir", default=str(DEFAULT_OUTPUT_DIR), help="generated ignored output directory")
    parser.add_argument("--official", action="store_true", help="label output as official release candidate")
    parser.add_argument("--release-approved", default="", help="required approval token for explicit official mode")
    args = parser.parse_args()

    manifest = load_manifest()
    require_manifest_boundary(manifest)
    names = assert_allowed_payload(manifest)
    scan_private_leaks(names)
    label = output_label(args)
    payload = build_payload_manifest(names, label)

    if args.check:
        print("Proof Pack 001 ZIP build check passed.")
        print(f"Payload files: {len(names)}")
        print(f"Output label: {label}")
        return 0

    output_dir = Path(args.output_dir)
    if not output_dir.is_absolute():
        output_dir = ROOT / output_dir
    output_dir = output_dir.resolve()
    try:
        output_dir.relative_to(ROOT)
    except ValueError:
        fail(f"output directory must stay inside repo root: {output_dir}")
    if not is_ignored(output_dir):
        fail(f"output directory is not git-ignored: {rel(output_dir)}")
    output_dir.mkdir(parents=True, exist_ok=True)

    zip_path = output_dir / ZIP_NAME
    manifest_path = output_dir / PAYLOAD_MANIFEST_NAME
    sha_path = output_dir / PAYLOAD_SHA256_NAME
    write_zip(names, zip_path)
    manifest_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8", newline="\n")
    sha_path.write_text(render_payload_sha256sums(payload, zip_path), encoding="utf-8", newline="\n")
    print(f"Built {rel(zip_path)}")
    print(f"Wrote {rel(manifest_path)}")
    print(f"Wrote {rel(sha_path)}")
    print(f"Output label: {label}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
