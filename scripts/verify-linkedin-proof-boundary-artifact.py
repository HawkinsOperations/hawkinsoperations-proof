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

VISUAL_TABLE_ARTIFACTS = [
    "Detection Source",
    "Validation",
    "Website",
    "Proof Pack 001",
    "AI Support",
]

README_REQUIRED_SECTIONS = [
    "Executive Summary",
    "June 1 Scale Snapshot",
    "The Problem",
    "What Was Actually Proved",
    "What Stayed Blocked",
    "The Control Pattern",
    "Public-Safe Boundary Matrix",
    "Deeper Evidence Threads",
    "Why This Matters for SOC Automation and AI Security Operations",
    "What This Packet Proves",
    "What This Packet Does Not Prove",
    "LinkedIn Usage",
    "Reviewer Links",
    "Verification",
]

README_SCALE_ROWS = [
    "Reviewer Metrics Pipeline v1",
    "Runtime Route Proof v1 Private Candidate",
    "Runtime Route Proof v1 Guardrails",
    "Wazuh CI / Static Rule Validation",
    "Runner Trust Split",
    "Runtime Wrapper / Access Bridge Preflight",
    "GitHub Front Door / Reviewer Routing",
    "HawkinsOps V1 Legacy Routing",
    "Public Wording / Proof-Boundary Packet",
    "Governance Saves / System Saves",
    "Career / SOC Automation Translation",
]

README_SCALE_HEADERS = [
    "Workstream",
    "What was added or advanced",
    "What it proves",
    "What it still does not prove",
]

WHAT_REQUIRED_SECTIONS = [
    "Today's Achievement in Plain English",
    "Final Table",
    "Scale Snapshot for the Post",
    "Why the Visual Is Backed by Real Work",
    "Control Pattern Behind the Post",
    "Deeper Evidence Threads",
    "What Not to Overclaim",
    "Final LinkedIn Caption",
    "First Comment Text",
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

MAP_TOP_LEVEL_KEYS = [
    "packet_name",
    "created_date",
    "scale_snapshot",
    "artifact_boundaries",
    "june_1_workstreams",
    "blocked_claims",
    "linkedin_usage",
    "public_routes",
    "claim_ceiling",
    "public_safe_status",
]

REQUIRED_WORKSTREAMS = [
    "reviewer_metrics_pipeline_v1",
    "runtime_route_proof_v1_private_candidate",
    "runtime_route_proof_v1_guardrails",
    "wazuh_ci_static_validation",
    "runner_trust_split",
    "runtime_wrapper_access_bridge",
    "github_front_door_reviewer_routing",
    "hawkinsops_v1_legacy_routing",
    "governance_saves_system_saves",
    "linkedin_proof_boundary_packet",
]

WORKSTREAM_KEYS = [
    "workstream",
    "status",
    "what_changed",
    "public_safe_summary",
    "proof_ceiling",
    "public_safe_status",
    "blocked_claims",
    "source_routes",
    "notes",
]

REQUIRED_CLAIM_CEILING = "PUBLIC_SUMMARY_SAFE_CANDIDATE_WITH_CONTROLLED_TEST_VALIDATED_REFERENCES"
REQUIRED_PACKET_STATUS = "NOT_PUBLIC_SAFE_PUBLICATION_REQUIRES_REVIEW"
REQUIRED_RUNTIME_STATUS = "NOT_PUBLIC_SAFE"

ALWAYS_PRIVATE_TERMS = [
    "MU" + "FG",
    "Dou" + "glas",
    "Fort" + "inet",
    "Zach" + "ari",
    "Michael" + " Lee",
    "Char" + "lotte",
    "Det" + "roit",
    "LinkedIn " + "screen" + "shot",
    "raw " + "evidence",
    "raw " + "runtime",
    "private " + "message",
    "Tailscale",
    "Wazuh " + "manager",
    "Cribl " + "host",
    "Splunk " + "host",
    "local " + "path",
    "host " + "IP",
]

CONTEXTUAL_PRIVATE_TERMS = [
    "re" + "cruiter",
    "screen" + "shot",
]

PRIVATE_PATTERNS = [
    ("Windows local path", re.compile(r"(?i)(?:[A-Z]:\\|\\\\)")),
    (
        "private IPv4 address",
        re.compile(r"\b(?:10|100|192\.168|172\.(?:1[6-9]|2[0-9]|3[0-1]))\.\d{1,3}\.\d{1,3}\b"),
    ),
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
    "live signal proven",
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
    "Wazuh-routed proof",
    "Cribl-routed public proof",
    "Splunk-indexed public proof",
    "website proves",
    "green CI authorizes merge",
    "Project board proves",
    "wrapper proves runtime",
    "private evidence is public proof",
]

BOUNDARY_MARKERS = [
    "blocked",
    "not prove",
    "does not prove",
    "does not claim",
    "does not promote",
    "not claimed",
    "not public-safe",
    "not_public_safe",
    "refused",
    "forbidden",
    "without",
    "cannot",
    "must not",
    "remains blocked",
    "no ",
    "not ",
]


class VerificationError(Exception):
    """Raised when packet verification fails."""


def fail(message: str) -> None:
    raise VerificationError(message)


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def normalize(text: str) -> str:
    return text.replace("’", "'").replace("–", "-").replace("—", "-")


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


def heading_regex(level: int, title: str) -> re.Pattern[str]:
    escaped = re.escape(title)
    return re.compile(rf"(?im)^{'#' * level}\s+(?:\d+\.\s+)?{escaped}\s*$")


def require_headings(text: str, path: Path, headings: list[str], level: int = 2) -> None:
    normalized = normalize(text)
    for heading in headings:
        if not heading_regex(level, heading).search(normalized):
            fail(f"missing required heading in {rel(path)}: {'#' * level} {heading}")


def has_boundary_context(line: str) -> bool:
    lowered = line.lower()
    return any(marker in lowered for marker in BOUNDARY_MARKERS)


def scan_private_text(path: Path, text: str) -> None:
    lowered = text.lower()
    for term in ALWAYS_PRIVATE_TERMS:
        if term.lower() in lowered:
            fail(f"private term appears in {rel(path)}: {term}")
    for term in CONTEXTUAL_PRIVATE_TERMS:
        if term.lower() in lowered:
            fail(f"contextual private term appears in {rel(path)}: {term}")
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
    for header in ["Artifact", "What it proves", "What it does not prove"]:
        if header not in text:
            fail(f"missing table header in {rel(path)}: {header}")


def verify_readme(readme: str) -> None:
    path = PACKET_DIR / "README.md"
    require_headings(readme, path, README_REQUIRED_SECTIONS, level=2)
    for header in README_SCALE_HEADERS:
        if header not in readme:
            fail(f"README scale snapshot missing table header: {header}")
    for row in README_SCALE_ROWS:
        if row not in readme:
            fail(f"README scale snapshot missing row: {row}")
    for token in REVIEWER_METRIC_TOKENS:
        if token not in readme:
            fail(f"README missing reviewer metric token: {token}")
    if "Website rendering is not proof" not in readme:
        fail("README must explicitly say website rendering is not proof")
    if "Checks are evidence, not authority" not in readme:
        fail("README must explicitly say checks are evidence, not authority")
    if "AI is labor" not in readme or "governance" not in readme.lower():
        fail("README must preserve AI labor / governance authority boundary")
    verify_markdown_tables(readme, path)


def verify_what_file(what_file: str) -> None:
    path = PACKET_DIR / "WHAT_THE_SYSTEM_REFUSED_TO_CLAIM.md"
    require_headings(what_file, path, WHAT_REQUIRED_SECTIONS, level=2)
    for heading in DEEP_THREAD_HEADINGS:
        if not heading_regex(3, heading).search(normalize(what_file)):
            fail(f"WHAT file missing deeper evidence thread: {heading}")
    verify_markdown_tables(what_file, path)


def require_non_empty_string(entry: dict[str, Any], key: str, label: str) -> None:
    if not isinstance(entry.get(key), str) or not entry[key].strip():
        fail(f"{label} {key} must be a non-empty string")


def require_non_empty_list(entry: dict[str, Any], key: str, label: str) -> None:
    if not isinstance(entry.get(key), list) or not entry[key]:
        fail(f"{label} {key} must be a non-empty list")


def joined_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True).lower()


def require_contains(label: str, text: str, *needles: str) -> None:
    lowered = text.lower()
    for needle in needles:
        if needle.lower() not in lowered:
            fail(f"{label} missing required token: {needle}")


def verify_workstream_semantics(workstream: dict[str, Any]) -> None:
    name = workstream["workstream"]
    joined = joined_json(workstream)
    if name == "reviewer_metrics_pipeline_v1":
        for token in ["4", "49", "106", "8", "31", "0", "public-safe count 0"]:
            require_contains(name, joined, token)
    elif name == "runtime_route_proof_v1_private_candidate":
        require_contains(name, joined, "NOT_PUBLIC_SAFE", "private candidate", "AI_DECIDED_DISPOSITION=false")
        if "public-safe runtime proof" in joined and "blocked" not in joined:
            fail("runtime_route_proof_v1_private_candidate promotes public-safe runtime proof")
    elif name == "runtime_route_proof_v1_guardrails":
        require_contains(name, joined, "wording gate", "what-to-say", "what-not-to-say", "not public-safe runtime proof")
    elif name == "wazuh_ci_static_validation":
        require_contains(name, joined, "source/static", "validation", "runtime proof", "deployment")
    elif name == "runner_trust_split":
        require_contains(name, joined, "public PR", "trusted", "manual/private")
    elif name == "runtime_wrapper_access_bridge":
        require_contains(name, joined, "read-only", "preflight", "wrapper proves runtime")
    elif name == "github_front_door_reviewer_routing":
        require_contains(name, joined, "reviewer", "not proof")
    elif name == "hawkinsops_v1_legacy_routing":
        require_contains(name, joined, "legacy", "historical", "not current")
    elif name == "governance_saves_system_saves":
        require_contains(name, joined, "private governance-save", "summary")
    elif name == "linkedin_proof_boundary_packet":
        require_contains(name, joined, "public-summary-safe candidate", "not proof promotion")


def verify_map(data: dict[str, Any]) -> None:
    for key in MAP_TOP_LEVEL_KEYS:
        if key not in data:
            fail(f"proof-boundary-map.json missing top-level key: {key}")
    if "entries" in data and "june_1_workstreams" not in data:
        fail("proof-boundary-map.json still uses old entries-only schema")
    if data.get("claim_ceiling") != REQUIRED_CLAIM_CEILING:
        fail("proof-boundary-map.json claim ceiling must remain public-summary-safe candidate")
    if data.get("public_safe_status") != REQUIRED_PACKET_STATUS:
        fail("proof-boundary-map.json public_safe_status must require review")
    boundaries = data.get("artifact_boundaries")
    if not isinstance(boundaries, list) or not boundaries:
        fail("proof-boundary-map.json artifact_boundaries must be a non-empty list")
    seen_artifacts = {entry.get("artifact") for entry in boundaries if isinstance(entry, dict)}
    for artifact in VISUAL_TABLE_ARTIFACTS:
        if artifact not in seen_artifacts:
            fail(f"proof-boundary-map.json artifact_boundaries missing artifact: {artifact}")
    for entry in boundaries:
        if not isinstance(entry, dict):
            fail("artifact_boundaries entries must be objects")
        for key in ["artifact", "proves", "does_not_prove", "public_safe_status"]:
            if key not in entry:
                fail(f"artifact boundary missing key: {key}")
    workstreams = data.get("june_1_workstreams")
    if not isinstance(workstreams, list):
        fail("proof-boundary-map.json june_1_workstreams must be a list")
    seen = {entry.get("workstream") for entry in workstreams if isinstance(entry, dict)}
    if seen != set(REQUIRED_WORKSTREAMS) or len(workstreams) != len(REQUIRED_WORKSTREAMS):
        fail("proof-boundary-map.json must contain exactly the required June 1 workstreams")
    for entry in workstreams:
        if not isinstance(entry, dict):
            fail("june_1_workstreams entries must be objects")
        label = f"workstream {entry.get('workstream', '<missing>')}"
        for key in WORKSTREAM_KEYS:
            if key not in entry:
                fail(f"{label} missing key: {key}")
        for key in ["workstream", "status", "public_safe_summary", "proof_ceiling", "public_safe_status", "notes"]:
            require_non_empty_string(entry, key, label)
        for key in ["what_changed", "blocked_claims", "source_routes"]:
            require_non_empty_list(entry, key, label)
        verify_workstream_semantics(entry)


def verify_manifest(data: dict[str, Any]) -> None:
    required = [
        "packet_name",
        "packet_purpose",
        "linkedin_post_hook",
        "created_date",
        "repo",
        "claim_ceiling",
        "public_safe_status",
        "june_1_scale_categories",
        "source_repos_checked",
        "source_log_classes_checked",
        "public_routes_checked",
        "files",
        "verifier_command",
        "verification_commands",
        "blocked_claims",
        "supported_workstreams",
        "supported_artifact_categories",
        "excluded_private_only_workstreams",
        "excluded_private_categories",
        "no_zip_reason",
    ]
    for key in required:
        if key not in data:
            fail(f"ARTIFACT_MANIFEST.json missing key: {key}")
    if data["claim_ceiling"] != REQUIRED_CLAIM_CEILING:
        fail("manifest claim ceiling must remain a public-summary candidate")
    if data["public_safe_status"] != REQUIRED_PACKET_STATUS:
        fail("manifest public_safe_status must require review")
    if data.get("files") != PACKET_FILES:
        fail("manifest files must match packet files in order")
    for key in [
        "june_1_scale_categories",
        "source_repos_checked",
        "source_log_classes_checked",
        "public_routes_checked",
        "blocked_claims",
        "supported_workstreams",
        "excluded_private_only_workstreams",
    ]:
        if not isinstance(data.get(key), list) or not data[key]:
            fail(f"manifest {key} must be a non-empty list")
    if set(data.get("supported_workstreams", [])) != set(REQUIRED_WORKSTREAMS):
        fail("manifest supported_workstreams must match required workstreams")
    if data.get("no_zip_reason") != "ZIP_COMMIT_BLOCKED_BY_REPO_PATTERN":
        fail("manifest must preserve no-zip reason")


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
    expected_names = {name for name in PACKET_FILES if name != "CHECKSUMS.sha256"}
    if set(parsed) != expected_names:
        missing = sorted(expected_names - set(parsed))
        extra = sorted(set(parsed) - expected_names)
        fail(f"CHECKSUMS.sha256 entries mismatch; missing={missing}; extra={extra}")
    for name in sorted(expected_names):
        path = PACKET_DIR / name
        actual = sha256(path)
        if actual != parsed[name]:
            fail(f"checksum mismatch for {name}: expected {parsed[name]}, got {actual}")


def main() -> int:
    try:
        for name in PACKET_FILES:
            path = PACKET_DIR / name
            text = read(path)
            scan_private_text(path, text)
            scan_forbidden_positive_claims(path, text)

        readme = read(PACKET_DIR / "README.md")
        what_file = read(PACKET_DIR / "WHAT_THE_SYSTEM_REFUSED_TO_CLAIM.md")
        verify_readme(readme)
        verify_what_file(what_file)
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
