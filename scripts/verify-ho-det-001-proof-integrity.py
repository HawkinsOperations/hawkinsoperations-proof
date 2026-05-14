#!/usr/bin/env python3
"""Enforce HO-DET-001 proof-record integrity boundaries."""
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROOF_RECORD = ROOT / "proof" / "records" / "HO-DET-001.md"


REQUIRED_STATUS_FIELDS = [
    "Detection ID: HO-DET-001",
    "Current proof level: CONTROLLED_TEST_VALIDATED",
    "Current trust class: CONTROLLED_TEST_VALIDATED",
    "Public-safe status: NOT_PUBLIC_SAFE",
    "Approval status: NOT_APPROVED",
]

REQUIRED_SECTIONS = [
    "Status Clarification",
    "Linked Artifacts",
    "Source Refs",
    "Validation Enforcement Status",
    "Platform Runtime Contract Enforcement",
    "Supported Claim",
    "Unsupported Claims",
    "Current Truth Table",
    "Validation Summary",
    "Proof Level Assessment",
    "Allowed Claims",
    "Blocked Claims",
    "Next Promotion Gate",
]

REQUIRED_LINKED_ARTIFACTS = [
    "hawkinsoperations-detections/detections/successor/ho-det-001/rule.yml",
    "hawkinsoperations-detections/detections/successor/ho-det-001/splunk.spl",
    "hawkinsoperations-validation/reports/ho-det-001/validation-result.json",
    "hawkinsoperations-validation/.github/workflows/ho-det-001-proof-loop.yml",
    "hawkinsoperations-validation/validation/successor/ho-det-001/case-packet.json",
    "hawkinsoperations-validation/scripts/verify-ho-det-001-triage-boundary.py",
    "hawkinsoperations-validation/scripts/scan-ho-det-001-claim-boundaries.py",
    "HawkinsOperations/hawkinsoperations-platform#5",
    "HawkinsOperations/hawkinsoperations-validation#18",
    "hawkinsoperations-validation/scripts/verify-ho-det-001-reproducible-proof-pack.py",
    "hawkinsoperations-validation/validation/successor/ho-det-001/reproducible-proof/",
]

REQUIRED_VALIDATION_FACTS = [
    "Validation status: pass",
    "Total controlled cases: 14",
    "Matched positive count: 7",
    "Missed positive cases: none",
    "False-positive negative cases: none",
    "Validation scope: controlled-test process-creation fixtures only",
]

REQUIRED_BLOCKED_CLAIMS = [
    "runtime-active",
    "signal-observed",
    "public-safe",
    "production-ready",
    "live Splunk fired",
    "Cribl-routed telemetry",
    "Wazuh live collection",
    "production AutoSOC triage",
    "analyst-approved disposition",
    "HO-GPU-01 runtime-active",
    "AI-decided disposition",
    "website proves detection status",
]

PATH_SEPARATOR_CLASS = "[" + chr(92) + "/]"

LEAK_PATTERNS = [
    ("Windows absolute local path", re.compile(r"(?i)\b[A-Z]:[\\/]")),
    ("UNC path", re.compile(r"\\\\[^\\\s]+\\[^\\\s]+")),
    ("LAN IP", re.compile(r"\b(?:10|172\.(?:1[6-9]|2\d|3[01])|192\.168)\.\d{1,3}\.\d{1,3}\b")),
    ("secret assignment", re.compile(r"(?i)\b(secret|token|api[_-]?key|password|authorization|cookie)\s*[:=]\s*\S+")),
    ("raw runtime evidence filename", re.compile(r"(?i)\b(runtime-signal|runtime-evidence|event-capture|splunk-search-path-fix)[-_][\w.-]+")),
    (
        "raw screenshot path",
        re.compile(
            r"(?i)((?:screen" r"shots?)"
            + PATH_SEPARATOR_CLASS
            + r".*\.(png|jpg|jpeg)|(?:screen" r"shot)\s+\d{4}-\d{2}-\d{2})"
        ),
    ),
    ("private evidence folder", re.compile(r"(?i)\bevidence-staging\b")),
    ("private host marker", re.compile(r"(?i)\b(private host|host label|host/ip|internal ip|lan ip)\b")),
]

BLOCKED_CONTEXT_MARKERS = [
    "blocked",
    "unsupported",
    "not_satisfied",
    "not satisfied",
    "not_public_safe",
    "not public-safe",
    "not_approved",
    "not approved",
    "does not prove",
    "evidence required",
    "promotion gate",
    "promotion-gate",
    "boundary",
    "blocked wording",
    "not assert",
    "does not assert",
    "not prove",
    "requires",
    "required",
    "no ",
    "without",
]

BLOCKED_CONTEXT_SECTIONS = {
    "Status Clarification",
    "Clone-Runnable Public Proof Pack",
    "Validation Enforcement Status",
    "Platform Runtime Contract Enforcement",
    "Unsupported Claims",
    "Current Truth Table",
    "Proof Level Assessment",
    "AutoSOC Summary",
    "LLM Summary",
    "Blocked Claims",
    "Next Promotion Gate",
}

POSITIVE_CLAIM_SECTIONS = {
    "Supported Claim",
    "Allowed Claims",
}


def fail(message: str) -> None:
    print(f"HO-DET-001 proof integrity failed: {message}", file=sys.stderr)
    raise SystemExit(1)


def require_contains(text: str, needle: str, label: str) -> None:
    if needle not in text:
        fail(f"missing {label}: {needle}")


def section_body(text: str, section: str) -> str:
    match = re.search(rf"^## {re.escape(section)}\s*$", text, re.MULTILINE)
    if not match:
        fail(f"missing required section: {section}")
    next_match = re.search(r"^##\s+", text[match.end() :], re.MULTILINE)
    if not next_match:
        return text[match.end() :]
    return text[match.end() : match.end() + next_match.start()]


def section_at(text: str, offset: int) -> str:
    current = ""
    for match in re.finditer(r"^## (.+?)\s*$", text, re.MULTILINE):
        if match.start() > offset:
            break
        current = match.group(1)
    return current


def validate_status_fields(text: str) -> None:
    for field in REQUIRED_STATUS_FIELDS:
        require_contains(text, field, "status field")


def validate_sections(text: str) -> None:
    for section in REQUIRED_SECTIONS:
        section_body(text, section)


def validate_links_and_facts(text: str) -> None:
    for artifact in REQUIRED_LINKED_ARTIFACTS:
        require_contains(text, artifact, "linked artifact")
    for fact in REQUIRED_VALIDATION_FACTS:
        require_contains(text, fact, "validation fact")


def validate_blocked_claims(text: str) -> None:
    blocked_body = section_body(text, "Blocked Claims")
    unsupported_body = section_body(text, "Unsupported Claims")
    combined = f"{unsupported_body}\n{blocked_body}".lower()
    for claim in REQUIRED_BLOCKED_CLAIMS:
        if claim.lower() not in combined:
            fail(f"missing blocked claim in blocked/unsupported sections: {claim}")

    for claim in REQUIRED_BLOCKED_CLAIMS:
        claim_re = re.compile(re.escape(claim), re.IGNORECASE)
        for match in claim_re.finditer(text):
            section = section_at(text, match.start())
            line_start = text.rfind("\n", 0, match.start()) + 1
            line_end = text.find("\n", match.end())
            if line_end == -1:
                line_end = len(text)
            line = text[line_start:line_end].lower()
            has_context = (
                section in BLOCKED_CONTEXT_SECTIONS
                or any(marker in line for marker in BLOCKED_CONTEXT_MARKERS)
            )
            if section in POSITIVE_CLAIM_SECTIONS and not any(
                marker in line for marker in BLOCKED_CONTEXT_MARKERS
            ):
                fail(f"blocked claim appears in positive claim section: {claim}")
            if not has_context:
                fail(f"blocked claim appears outside blocked/boundary context: {claim}")


def validate_private_leak_boundaries(text: str) -> None:
    for label, pattern in LEAK_PATTERNS:
        match = pattern.search(text)
        if match:
            fail(f"private/public-safety rejection matched {label}: {match.group(0)}")


def main() -> int:
    if not PROOF_RECORD.exists():
        fail("missing proof/records/HO-DET-001.md")
    text = PROOF_RECORD.read_text(encoding="utf-8")
    validate_status_fields(text)
    validate_sections(text)
    validate_links_and_facts(text)
    validate_blocked_claims(text)
    validate_private_leak_boundaries(text)
    print("HO-DET-001 proof integrity check passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
