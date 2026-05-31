#!/usr/bin/env python3
"""Verify Lifetime Case Ledger verifier badge references and boundaries."""
import argparse
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
README_PATH = ROOT / "README.md"
WORKFLOW_PATH = ROOT / ".github" / "workflows" / "governance-gate.yml"

WORKFLOW_NAME = "Governance Gate"
WORKFLOW_FILE = "governance-gate.yml"
SUMMARY_JOB = "lifetime-ledger-public-summary"
BUNDLE_JOB = "lifetime-ledger-proof-bundle"
PROOF_CEILING = "SCHEMA_CONTRACT_VERIFIER_EXISTS_ONLY"
LEDGER_STATUS = "NOT_PUBLIC_SAFE"

REQUIRED_README_SNIPPETS = [
    "## Lifetime Case Ledger Verification Badges",
    "Ledger summary verifier",
    "Ledger proof bundle verifier",
    f"actions/workflows/{WORKFLOW_FILE}/badge.svg?branch=main&event=push",
    f"actions/workflows/{WORKFLOW_FILE}?query=branch%3Amain",
    SUMMARY_JOB,
    BUNDLE_JOB,
    PROOF_CEILING,
    LEDGER_STATUS,
    "Badges report GitHub Actions workflow check status only.",
    "They do not prove runtime activity, signal observation, public proof, public-safe runtime proof, SOCaaS deployment, production deployment, autonomous SOC authority, AI-approved disposition, analyst-approved disposition, or case closure.",
]

REQUIRED_WORKFLOW_SNIPPETS = [
    f"name: {WORKFLOW_NAME}",
    f"{SUMMARY_JOB}:",
    f"{BUNDLE_JOB}:",
    "python scripts/verify-lifetime-ledger-public-summary.py --platform-manifest hawkinsoperations-platform/contracts/lifetime-case-ledger-v1-state-manifest.json --format json >/dev/null",
    "python scripts/verify-lifetime-ledger-proof-bundle.py --platform-manifest hawkinsoperations-platform/contracts/lifetime-case-ledger-v1-state-manifest.json --format json >/dev/null",
    "ref: e0580fc8d0b141cbdd71c1b95e3d7885a1d708e0",
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


def fail(message: str) -> None:
    print(f"Lifetime ledger badge verification failed: {message}", file=sys.stderr)
    raise SystemExit(1)


def read_text(path: Path, label: str) -> str:
    if not path.exists():
        fail(f"missing {label}: {path}")
    return path.read_text(encoding="utf-8")


def require_snippets(text: str, snippets: list[str], label: str) -> None:
    missing = [snippet for snippet in snippets if snippet not in text]
    if missing:
        fail(f"{label} missing required text: {missing[0]}")


def scan_private_markers(text: str, label: str) -> None:
    for name, pattern in DENIED_PATTERNS:
        if pattern.search(text):
            fail(f"{label} contains blocked private marker: {name}")


def verify(readme_path: Path, workflow_path: Path) -> dict[str, str]:
    readme = read_text(readme_path, "README")
    workflow = read_text(workflow_path, "governance workflow")
    require_snippets(workflow, REQUIRED_WORKFLOW_SNIPPETS, "governance workflow")
    require_snippets(readme, REQUIRED_README_SNIPPETS, "README")
    scan_private_markers(readme, "README badge section")

    badge_count = readme.count(f"actions/workflows/{WORKFLOW_FILE}/badge.svg?branch=main&event=push")
    if badge_count != 2:
        fail("README must contain exactly two Lifetime Case Ledger workflow badge image references")

    if "PUBLIC_SAFE_APPROVED" in readme or "RUNTIME_ACTIVE" in readme or "SIGNAL_OBSERVED" in readme:
        fail("README badge wording contains promoted trust-state language")

    return {
        "mode": "verify-lifetime-ledger-badges",
        "readme_path": readme_path.relative_to(ROOT).as_posix(),
        "workflow_path": workflow_path.relative_to(ROOT).as_posix(),
        "workflow": WORKFLOW_NAME,
        "summary_job": SUMMARY_JOB,
        "bundle_job": BUNDLE_JOB,
        "proof_ceiling": PROOF_CEILING,
        "ledger_status": LEDGER_STATUS,
    }


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--readme", default=str(README_PATH))
    parser.add_argument("--workflow", default=str(WORKFLOW_PATH))
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    result = verify(Path(args.readme).resolve(), Path(args.workflow).resolve())
    print("Lifetime ledger badge verification passed.")
    for key in ("workflow", "summary_job", "bundle_job", "proof_ceiling", "ledger_status"):
        print(f"{key}={result[key]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
