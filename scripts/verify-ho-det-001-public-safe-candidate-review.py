#!/usr/bin/env python3
"""Verify the HO-DET-001 public-safe candidate review packet."""
from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:  # pragma: no cover - environment failure path
    yaml = None


ROOT = Path(__file__).resolve().parents[1]
PACKET_PATH = ROOT / "proof" / "records" / "HO-DET-001-PUBLIC-SAFE-CANDIDATE-REVIEW-V1.md"
INDEX_PATH = ROOT / "proof" / "indexes" / "DETECTION_PROOF_STATUS_INDEX.yml"

REQUIRED_SECTIONS = [
    "Purpose",
    "Artifact Identity",
    "Current Evidence State",
    "Current Review State",
    "Current Claim Ceiling",
    "Allowed Wording",
    "Blocked Wording",
    "Promotion Requirements",
    "Authority Boundary",
    "Reviewer Summary",
]

REQUIRED_FIELD_LINES = [
    "artifact_id: HO-DET-001",
    "review_lane: PUBLIC_SAFE_CANDIDATE_REVIEW_V1",
    "review_type: public-safe candidate review",
    "public_safe_status: NOT_PUBLIC_SAFE",
    "runtime_active: false",
    "signal_observed: false",
    "human_review_required: true",
    "privacy_review: PENDING",
    "stale_review: PENDING",
    "evidence_linkage_review: PENDING",
    "wording_approval: PENDING",
    "proof_ceiling: CONTROLLED_TEST_VALIDATED",
    "proof_ceiling_meaning: CONTROLLED_VALIDATION_ONLY",
    "case_status: NOT_CLOSED",
    "claim_authority: BLOCK_STRONGER_RUNTIME_SIGNAL_PUBLIC_SAFE_CLAIMS",
]

REQUIRED_ALLOWED_WORDING = [
    "HO-DET-001 has controlled validation evidence and remains under governed public-safe candidate review.",
    "HO-DET-001 is a controlled-validation-backed artifact with public-safe review gates still pending.",
]

REQUIRED_BLOCKED_WORDING = [
    "runtime proven",
    "runtime active",
    "signal observed",
    "public-safe approved",
    "public-safe proof",
    "production ready",
    "production SOC",
    "SOC deployed",
    "SOCaaS deployed",
    "customer deployed",
    "customer validated",
    "analyst approved",
    "AI approved",
    "autonomous approval",
    "final human authorization",
    "case closed",
    "green CI as approval",
    "website rendering as proof",
    "GitHub rendering as proof",
]

REQUIRED_PROMOTION_REQUIREMENTS = [
    "privacy review",
    "stale review",
    "evidence-linkage review",
    "exact wording approval",
    "platform state alignment",
    "proof authority update",
    "explicit human approval",
    "no stronger claim until the above pass",
]

FORBIDDEN_PACKET_MARKERS = [
    "public_safe_status: APPROVED",
    "public_safe_status: PUBLIC_SAFE",
    "runtime_active: true",
    "signal_observed: true",
    "case_status: CLOSED",
]

BLOCKED_CONTEXT_SECTIONS = {"Blocked Wording"}
WINDOWS_ABSOLUTE_PATH = re.compile(r"\b[A-Z]:[\\/]", re.IGNORECASE)


class VerificationError(Exception):
    """Raised when candidate review verification fails."""


def fail(message: str) -> None:
    print(f"HO-DET-001 public-safe candidate review verification failed: {message}", file=sys.stderr)
    raise SystemExit(1)


def load_yaml(path: Path, label: str) -> Any:
    if yaml is None:
        raise VerificationError("PyYAML is required to parse YAML files")
    if not path.exists():
        raise VerificationError(f"missing {label}: {path}")
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def section_body(text: str, section: str) -> str:
    match = re.search(rf"^## {re.escape(section)}\s*$", text, re.MULTILINE)
    if not match:
        raise VerificationError(f"missing required section: {section}")
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


def require_contains(text: str, needle: str, label: str) -> None:
    if needle not in text:
        raise VerificationError(f"missing {label}: {needle}")


def verify_packet_text(text: str) -> None:
    for section in REQUIRED_SECTIONS:
        section_body(text, section)
    for field in REQUIRED_FIELD_LINES:
        require_contains(text, field, "candidate review invariant")
    for marker in FORBIDDEN_PACKET_MARKERS:
        if marker.lower() in text.lower():
            raise VerificationError(f"forbidden packet marker present: {marker}")
    if WINDOWS_ABSOLUTE_PATH.search(text):
        raise VerificationError("Windows absolute local path present")

    allowed_body = section_body(text, "Allowed Wording")
    for wording in REQUIRED_ALLOWED_WORDING:
        require_contains(allowed_body, wording, "allowed wording")

    blocked_body = section_body(text, "Blocked Wording")
    blocked_lower = blocked_body.lower()
    for wording in REQUIRED_BLOCKED_WORDING:
        if wording.lower() not in blocked_lower:
            raise VerificationError(f"missing blocked wording: {wording}")

    for wording in REQUIRED_BLOCKED_WORDING:
        pattern = re.compile(re.escape(wording), re.IGNORECASE)
        for match in pattern.finditer(text):
            section = section_at(text, match.start())
            if section not in BLOCKED_CONTEXT_SECTIONS:
                raise VerificationError(f"blocked wording outside Blocked Wording section: {wording}")

    promotion_body = section_body(text, "Promotion Requirements").lower()
    for requirement in REQUIRED_PROMOTION_REQUIREMENTS:
        if requirement.lower() not in promotion_body:
            raise VerificationError(f"missing promotion requirement: {requirement}")

    authority_body = section_body(text, "Authority Boundary").lower()
    for required_text in [
        "proof records",
        "claim ceilings",
        "proofcards",
        "proof packs",
        "evidence boundary records",
        "blocked and allowed claim authority",
        "reviewer proof maps",
        "does not own raw runtime evidence publication",
        "does not own raw runtime evidence publication, runtime truth, signal truth, source truth, validation truth, website rendering truth, or final public-safe approval by implication",
    ]:
        if required_text not in authority_body:
            raise VerificationError(f"missing authority boundary text: {required_text}")


def verify_index() -> None:
    index = load_yaml(INDEX_PATH, "detection proof status index")
    entries = index.get("entries")
    if not isinstance(entries, list):
        raise VerificationError("index entries must be a list")
    entry = next((item for item in entries if item.get("detection_id") == "HO-DET-001"), None)
    if not isinstance(entry, dict):
        raise VerificationError("HO-DET-001 entry missing from detection proof status index")
    if entry.get("candidate_review_packet_path") != "proof/records/HO-DET-001-PUBLIC-SAFE-CANDIDATE-REVIEW-V1.md":
        raise VerificationError("HO-DET-001 index entry does not point to the candidate review packet")
    state = entry.get("candidate_review_state")
    if not isinstance(state, dict):
        raise VerificationError("HO-DET-001 candidate_review_state missing from index")
    expected = {
        "public_safe_status": "NOT_PUBLIC_SAFE",
        "runtime_active": False,
        "signal_observed": False,
        "human_review_required": True,
        "privacy_review": "PENDING",
        "stale_review": "PENDING",
        "evidence_linkage_review": "PENDING",
        "wording_approval": "PENDING",
        "proof_ceiling": "CONTROLLED_TEST_VALIDATED",
        "case_status": "NOT_CLOSED",
        "claim_authority": "BLOCK_STRONGER_RUNTIME_SIGNAL_PUBLIC_SAFE_CLAIMS",
    }
    for key, value in expected.items():
        if state.get(key) != value:
            raise VerificationError(f"index candidate_review_state.{key} must be {value!r}")


def main() -> int:
    try:
        if not PACKET_PATH.exists():
            raise VerificationError(f"missing packet: {PACKET_PATH}")
        verify_packet_text(PACKET_PATH.read_text(encoding="utf-8"))
        verify_index()
    except VerificationError as exc:
        fail(str(exc))
    print("HO-DET-001 public-safe candidate review verification passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
