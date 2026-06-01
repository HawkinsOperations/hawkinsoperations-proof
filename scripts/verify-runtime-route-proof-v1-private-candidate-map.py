#!/usr/bin/env python3
"""Verify the Runtime Route Proof v1 private-candidate proof map boundary."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MAP_JSON = ROOT / "proof" / "indexes" / "runtime-route-proof-v1-private-candidate-map.json"
MAP_MD = ROOT / "proof" / "indexes" / "runtime-route-proof-v1-private-candidate-map.md"
RECORD_MD = ROOT / "proof" / "records" / "RUNTIME-ROUTE-PROOF-V1-PRIVATE-CANDIDATE.md"

EXPECTED = {
    "schema_version": "runtime-route-proof-v1-private-candidate-map-v1",
    "map_id": "runtime-route-proof-v1-private-candidate-map",
    "record_path": "proof/records/RUNTIME-ROUTE-PROOF-V1-PRIVATE-CANDIDATE.md",
    "marker_id": "HO-RUNTIME-V1-20260601T120922Z-BATCH764",
    "private_route": ["Wazuh", "Cribl", "Splunk"],
    "deterministic_verifier_status": "PASS_ROUTE_RECEIPTS",
    "manifest_verified": True,
    "lifetime_governed_cases": 4,
    "public_safe_count": 0,
    "public_safe_status": "NOT_PUBLIC_SAFE",
    "proof_ceiling": "PRIVATE_RUNTIME_ROUTE_PROOF_V1_CANDIDATE",
    "preservation_ceiling": "PRIVATE_RUNTIME_ROUTE_PROOF_V1_CANDIDATE_PRESERVED",
}

EXPECTED_RECEIPTS = {
    "wazuh": "PASS",
    "cribl": "PASS",
    "splunk": "PASS",
}

EXPECTED_PACKET = {
    "filename": "HO-RUNTIME-ROUTE-PROOF-V1-PRIVATE-REVIEWER-SAFE-2026-06-01.zip",
    "sha256": "3a1d4472bffcce68cff6e101c54e06b5a67528338bda174e6fef209fa9b1b278",
    "raw_private_evidence_in_repo": False,
}

EXPECTED_BOUNDARY = {
    "public_safe_runtime_proof": False,
    "production_soc_operation": False,
    "autonomous_soc_operation": False,
    "ai_decided_disposition": False,
    "lifetime_governed_case_mutation": False,
    "public_publication_approved": False,
    "human_review_required": True,
}

REQUIRED_MARKDOWN = (
    "HO-RUNTIME-V1-20260601T120922Z-BATCH764",
    "Wazuh -> Cribl -> Splunk",
    "PASS_ROUTE_RECEIPTS",
    "Manifest verified",
    "Lifetime Governed Cases",
    "Public-safe count",
    "NOT_PUBLIC_SAFE",
    "PRIVATE_RUNTIME_ROUTE_PROOF_V1_CANDIDATE_PRESERVED",
    "AI-decided disposition",
    "does not prove public-safe runtime proof",
    "does not mutate Lifetime Governed Cases",
)

LEAK_PATTERNS = {
    "windows_absolute_path": re.compile(r"\b[A-Z]:[\\/]"),
    "unc_path": re.compile(r"\\\\[^\\\s]+\\[^\\\s]+"),
    "lan_ip": re.compile(r"\b(?:10|172\.(?:1[6-9]|2\d|3[01])|192\.168)\.\d{1,3}\.\d{1,3}\b"),
    "secret_assignment": re.compile(r"(?i)\b(secret|token|api[_-]?key|password|authorization|cookie)\s*[:=]\s*\S+"),
    "raw_payload_label": re.compile(r"(?i)\b(raw_payload|command_line_raw|event_body_raw|full_log_raw)\b"),
}

PROMOTED_CLAIM_PATTERNS = {
    "public_safe_approval": re.compile(r"(?i)\bPUBLIC_SAFE_APPROVED\b|\bpublic-safe approved\b"),
    "production_soc": re.compile(r"(?i)\bPRODUCTION_SOC_PROVEN\b|\bproduction SOC operation proven\b"),
    "autonomous_soc": re.compile(r"(?i)\bAUTONOMOUS_SOC_PROVEN\b|\bautonomous SOC operation proven\b"),
    "ai_decided": re.compile(r"(?i)\bAI_DECIDED_DISPOSITION\s*[:=]\s*true\b"),
    "lifetime_mutation": re.compile(r"(?i)\bLIFETIME_GOVERNED_CASE_CREATED\b|\blifetime_governed_case_mutation\s*[:=]\s*true\b"),
}


def fail(message: str) -> None:
    print(f"runtime route proof v1 proof-map verification failed: {message}", file=sys.stderr)
    raise SystemExit(1)


def load_json(path: Path) -> dict:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        fail(f"invalid JSON in {path.relative_to(ROOT)}: {exc}")
    if not isinstance(data, dict):
        fail(f"{path.relative_to(ROOT)} root must be an object")
    return data


def scan_text(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    for label, pattern in LEAK_PATTERNS.items():
        if pattern.search(text):
            fail(f"{label} pattern found in {path.relative_to(ROOT)}")
    for label, pattern in PROMOTED_CLAIM_PATTERNS.items():
        if pattern.search(text):
            fail(f"{label} pattern found in {path.relative_to(ROOT)}")


def assert_equal(actual, expected, label: str) -> None:
    if actual != expected:
        fail(f"{label} expected {expected!r} but got {actual!r}")


def verify_markdown(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    normalized = text.lower()
    for required in REQUIRED_MARKDOWN:
        if required.lower() not in normalized:
            fail(f"{path.relative_to(ROOT)} missing required boundary text: {required}")


def verify() -> dict:
    for path in (MAP_JSON, MAP_MD, RECORD_MD):
        if not path.exists():
            fail(f"missing required file: {path.relative_to(ROOT)}")
        scan_text(path)

    data = load_json(MAP_JSON)
    for key, expected in EXPECTED.items():
        assert_equal(data.get(key), expected, key)

    assert_equal(data.get("receipts"), EXPECTED_RECEIPTS, "receipts")
    assert_equal(data.get("reviewer_safe_packet"), EXPECTED_PACKET, "reviewer_safe_packet")
    assert_equal(data.get("claim_boundary"), EXPECTED_BOUNDARY, "claim_boundary")

    record_path = ROOT / data["record_path"]
    if record_path != RECORD_MD:
        fail("record_path must point to the private candidate record")

    verify_markdown(MAP_MD)
    verify_markdown(RECORD_MD)

    blocked_claims = data.get("blocked_claims")
    if not isinstance(blocked_claims, list) or "public-safe runtime proof" not in blocked_claims:
        fail("blocked_claims must preserve public-safe runtime proof denial")

    return {
        "status": "PASS",
        "map": str(MAP_JSON.relative_to(ROOT)),
        "record": str(RECORD_MD.relative_to(ROOT)),
        "marker_id": data["marker_id"],
        "deterministic_verifier_status": data["deterministic_verifier_status"],
        "manifest_verified": data["manifest_verified"],
        "lifetime_governed_cases": data["lifetime_governed_cases"],
        "public_safe_count": data["public_safe_count"],
        "public_safe_status": data["public_safe_status"],
        "raw_private_evidence_in_repo": data["reviewer_safe_packet"]["raw_private_evidence_in_repo"],
        "ai_decided_disposition": data["claim_boundary"]["ai_decided_disposition"],
    }


def main() -> int:
    print(json.dumps(verify(), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
