#!/usr/bin/env python3
"""Verify Reviewer Metrics Pipeline v1 closeout map and boundary record."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
MAP_JSON = ROOT / "proof" / "indexes" / "reviewer-metrics-pipeline-v1-map.json"
MAP_MD = ROOT / "proof" / "indexes" / "reviewer-metrics-pipeline-v1-map.md"
CLOSEOUT_MD = ROOT / "proof" / "records" / "REVIEWER-METRICS-PIPELINE-V1-CLOSEOUT.md"

EXPECTED_METRICS: dict[str, int | str] = {
    "Lifetime Governed Cases": 4,
    "Detection Activity / Fire Count": 49,
    "Validation Case Count": 106,
    "Proof Record Count": 8,
    "Blocked Claims / Prevented Promotions": 31,
    "Public-safe Count": 0,
    "Reviewer Demo Path / Project Board Reconciliation": "REPO_BACKED_RECONCILIATION_PLAN_NO_PROJECT_MUTATION",
}

EXPECTED_AUTHORITIES = {
    "Lifetime Governed Cases": "hawkinsoperations-platform",
    "Detection Activity / Fire Count": "hawkinsoperations-validation",
    "Validation Case Count": "hawkinsoperations-validation",
    "Proof Record Count": "hawkinsoperations-proof",
    "Blocked Claims / Prevented Promotions": "hawkinsoperations-proof",
    "Public-safe Count": "hawkinsoperations-proof",
    "Reviewer Demo Path / Project Board Reconciliation": ".github",
}

REQUIRED_BOUNDARIES = [
    "live Wazuh telemetry",
    "Cribl routing",
    "Splunk indexing",
    "HO-GPU-01 triage",
    "production SOC operation",
    "public-safe runtime proof",
    "signal observation",
    "AI authority",
    "analyst disposition authority",
    "GitHub Project board proof authority",
]

REQUIRED_REVIEWER_PATH = [
    "Start here",
    "Strict number",
    "Big activity number",
    "Validation volume",
    "Proof surfaces",
    "Blocked claims",
    "Board status",
    "What remains blocked",
]

DENIED_PRIVATE = [
    ("local Windows path", re.compile(r"(?i)(?:[A-Z]:\\|\\\\)")),
    ("private IPv4 address", re.compile(r"\b(?:10|192\.168|172\.(?:1[6-9]|2[0-9]|3[0-1]))\.\d{1,3}\.\d{1,3}\b")),
    ("secret marker", re.compile(r"(?i)\b(secret|password|credential|api[_-]?key|token)\b")),
]

PROMOTED_CLAIMS = [
    "runtime-active public proof",
    "signal-observed public proof",
    "public-safe runtime proof",
    "production SOC operation",
    "production operation",
    "signal observation",
    "autonomous SOC",
    "AI authority",
    "AI-approved disposition",
    "AI-decided disposition",
    "analyst-approved disposition",
    "GitHub Project board proof authority",
]


class VerificationError(Exception):
    """Raised when closeout verification fails."""


def fail(message: str) -> None:
    raise VerificationError(message)


def load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        fail(f"missing JSON file: {path.relative_to(ROOT).as_posix()}")
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        fail(f"invalid JSON in {path.relative_to(ROOT).as_posix()}: {exc}")
    if not isinstance(data, dict):
        fail(f"{path.relative_to(ROOT).as_posix()} root must be an object")
    return data


def scan_private_text(text: str, label: str) -> None:
    for name, pattern in DENIED_PRIVATE:
        if pattern.search(text):
            fail(f"{label} contains blocked private marker: {name}")


def boundary_context(line: str) -> bool:
    lowered = line.lower()
    return any(
        marker in lowered
        for marker in (
            "remains blocked",
            "remains not approved",
            "does not prove",
            "does not claim",
            "not claimed",
            "not proof authority",
            "not public-safe",
            "not approved",
            "blocked",
            "no public-safe",
            "no runtime",
            "no production",
            "not production",
            "coordination-only",
            "not public",
            "not_public_safe",
        )
    )


def scan_claim_text(text: str, label: str) -> None:
    for claim in PROMOTED_CLAIMS:
        pattern = re.compile(rf"(?i)\b{re.escape(claim)}\b")
        for line in text.splitlines():
            if pattern.search(line) and not boundary_context(line):
                fail(f"{label} contains promoted claim without boundary: {claim}")


def boundary_path(path: str) -> bool:
    return any(
        marker in path
        for marker in (
            ".does_not_prove",
            ".proof_boundary",
            "$.does_not_prove",
        )
    )


def run_boundary_context_self_tests() -> dict[str, str]:
    rejected = [
        "public-safe runtime " + "proof remains approved",
        "production SOC " + "operation remains active",
        "signal " + "observation remains proven",
        "AI " + "authority remains enabled",
    ]
    allowed = [
        "public-safe runtime proof remains blocked",
        "production SOC operation is not approved",
        "this does not prove signal observation",
        "AI authority is not claimed",
    ]

    for line in rejected:
        try:
            scan_claim_text(line, "boundary self-test rejected case")
        except VerificationError:
            continue
        fail(f"boundary self-test accepted promoted wording: {line}")

    for line in allowed:
        try:
            scan_claim_text(line, "boundary self-test allowed case")
        except VerificationError as exc:
            fail(f"boundary self-test rejected explicit boundary wording: {line}: {exc}")

    return {
        "status": "pass",
        "positive_promoted_phrases_rejected": str(len(rejected)),
        "explicit_boundary_phrases_allowed": str(len(allowed)),
    }


def scan_json_strings(value: Any, path: str = "$") -> None:
    if isinstance(value, dict):
        for key, nested in value.items():
            scan_private_text(str(key), path)
            scan_json_strings(nested, f"{path}.{key}")
    elif isinstance(value, list):
        for index, nested in enumerate(value):
            scan_json_strings(nested, f"{path}[{index}]")
    elif isinstance(value, str):
        scan_private_text(value, path)
        if not boundary_path(path):
            scan_claim_text(value, path)


def verify_map_json(data: dict[str, Any]) -> dict[str, int | str]:
    if data.get("map_id") != "REVIEWER_METRICS_PIPELINE_V1_MAP":
        fail("map_id mismatch")
    if data.get("owner_repo") != "hawkinsoperations-proof":
        fail("owner_repo must be hawkinsoperations-proof")
    if data.get("proof_ceiling") != "REVIEWER_METRICS_PIPELINE_V1_CLOSED_REVIEWER_VISIBLE":
        fail("proof ceiling mismatch")
    if data.get("public_safe_status") != "NOT_PUBLIC_SAFE":
        fail("public_safe_status must be NOT_PUBLIC_SAFE")

    metrics = data.get("metrics")
    if not isinstance(metrics, list):
        fail("metrics must be a list")
    by_name: dict[str, dict[str, Any]] = {}
    for item in metrics:
        if not isinstance(item, dict):
            fail("metric entries must be objects")
        name = item.get("name")
        if not isinstance(name, str):
            fail("metric name must be a string")
        by_name[name] = item
        if not item.get("authority_repo"):
            fail(f"{name} missing authority_repo")
        if not item.get("source_surface"):
            fail(f"{name} missing source_surface")
        if not item.get("verifier_command"):
            fail(f"{name} missing verifier_command")
        if not item.get("proof_boundary"):
            fail(f"{name} missing proof_boundary")
        if not item.get("reviewer_explanation"):
            fail(f"{name} missing reviewer_explanation")
        if not item.get("does_not_prove"):
            fail(f"{name} missing does_not_prove")

    missing = sorted(set(EXPECTED_METRICS) - set(by_name))
    if missing:
        fail(f"missing metric: {missing[0]}")
    for name, expected in EXPECTED_METRICS.items():
        actual = by_name[name].get("value")
        if actual != expected:
            fail(f"{name} value mismatch: expected {expected!r}, found {actual!r}")
        authority = by_name[name].get("authority_repo")
        if authority != EXPECTED_AUTHORITIES[name]:
            fail(f"{name} authority mismatch: expected {EXPECTED_AUTHORITIES[name]}, found {authority}")

    if by_name["Lifetime Governed Cases"]["proof_boundary"].lower().find("strict") < 0:
        fail("Lifetime Governed Cases must be explicitly strict")
    if by_name["Detection Activity / Fire Count"]["proof_boundary"].lower().find("controlled validation") < 0:
        fail("Detection Activity must stay controlled-validation scoped")
    if by_name["Public-safe Count"]["value"] != 0:
        fail("Public-safe Count must remain 0")

    boundaries = data.get("authority_boundaries")
    if not isinstance(boundaries, dict):
        fail("authority_boundaries must be an object")
    required_false = [
        "detection_activity_is_governed_case_count",
        "github_project_mutation_performed",
        "proof_promotion_performed",
        "public_safe_approval_performed",
    ]
    for key in required_false:
        if boundaries.get(key) is not False:
            fail(f"authority_boundaries.{key} must be false")
    if boundaries.get("project_board_is_coordination_only") is not True:
        fail("Project Board must remain coordination-only")
    if boundaries.get("website_is_render_only") is not True:
        fail("website must remain render-only")

    reviewer_path = data.get("required_reviewer_path")
    if reviewer_path != REQUIRED_REVIEWER_PATH:
        fail("required reviewer path changed or incomplete")

    does_not_prove = data.get("does_not_prove")
    if not isinstance(does_not_prove, list):
        fail("does_not_prove must be a list")
    for boundary in REQUIRED_BOUNDARIES:
        if boundary not in does_not_prove:
            fail(f"does_not_prove missing boundary: {boundary}")

    scan_json_strings(data)
    return {name: by_name[name]["value"] for name in EXPECTED_METRICS}


def normalize_markdown_cell(value: str) -> str:
    value = value.strip()
    if value.startswith("`") and value.endswith("`") and len(value) >= 2:
        value = value[1:-1]
    return value.strip()


def markdown_section(text: str, heading: str) -> str:
    marker = f"## {heading}"
    start = text.find(marker)
    if start == -1:
        fail(f"missing Markdown section: {marker}")
    body_start = start + len(marker)
    next_heading = text.find("\n## ", body_start)
    if next_heading == -1:
        return text[body_start:]
    return text[body_start:next_heading]


def parse_markdown_table(section: str, label: str) -> list[dict[str, str]]:
    lines = [line.strip() for line in section.splitlines() if line.strip().startswith("|")]
    if len(lines) < 3:
        fail(f"{label} table must include header, separator, and rows")
    headers = [normalize_markdown_cell(cell) for cell in lines[0].strip("|").split("|")]
    if headers != ["Metric", "Value", "Authority repo"]:
        fail(f"{label} table header mismatch: {headers}")

    separator_cells = [cell.strip() for cell in lines[1].strip("|").split("|")]
    if len(separator_cells) != len(headers) or not all(set(cell) <= {"-", ":"} and "-" in cell for cell in separator_cells):
        fail(f"{label} table separator is invalid")

    rows: list[dict[str, str]] = []
    for line in lines[2:]:
        cells = [normalize_markdown_cell(cell) for cell in line.strip("|").split("|")]
        if len(cells) != len(headers):
            fail(f"{label} table row has wrong column count: {line}")
        rows.append(dict(zip(headers, cells)))
    return rows


def verify_closeout_metrics_table(text: str) -> dict[str, str]:
    rows = parse_markdown_table(markdown_section(text, "Final Metrics"), "Final Metrics")
    actual: dict[str, str] = {}
    for row in rows:
        metric = row["Metric"]
        if metric in actual:
            fail(f"Final Metrics table repeats metric: {metric}")
        actual[metric] = row["Value"]

    expected_names = set(EXPECTED_METRICS)
    actual_names = set(actual)
    missing = sorted(expected_names - actual_names)
    extra = sorted(actual_names - expected_names)
    if missing:
        fail(f"Final Metrics table missing metric: {missing[0]}")
    if extra:
        fail(f"Final Metrics table contains unexpected metric: {extra[0]}")

    for metric, expected in EXPECTED_METRICS.items():
        expected_value = str(expected)
        if actual[metric] != expected_value:
            fail(f"Final Metrics table value mismatch for {metric}: expected {expected_value!r}, found {actual[metric]!r}")
    return actual


def verify_markdown(path: Path, required: list[str]) -> None:
    if not path.exists():
        fail(f"missing Markdown file: {path.relative_to(ROOT).as_posix()}")
    text = path.read_text(encoding="utf-8")
    scan_private_text(text, path.relative_to(ROOT).as_posix())
    scan_claim_text(text, path.relative_to(ROOT).as_posix())
    for needle in required:
        if needle not in text:
            fail(f"{path.relative_to(ROOT).as_posix()} missing required text: {needle}")


def verify() -> dict[str, Any]:
    boundary_self_test = run_boundary_context_self_tests()
    data = load_json(MAP_JSON)
    metrics = verify_map_json(data)
    markdown_needles = [
        "## Metrics",
        "## Reviewer Demo Path",
        "## Authority Boundaries",
        "## What This Does Not Prove",
        "Lifetime Governed Cases",
        "Detection Activity / Fire Count",
        "Project Board reconciliation remains `REPO_BACKED_RECONCILIATION_PLAN_NO_PROJECT_MUTATION`",
    ]
    verify_markdown(MAP_MD, markdown_needles)
    verify_markdown(
        CLOSEOUT_MD,
        [
            "## Result",
            "## Final Metrics",
            "## Source Map",
            "## Verifiers",
            "## Claim Boundary",
            "## What This Does Not Prove",
            "## Project Board Boundary",
        ],
    )
    closeout_metrics = verify_closeout_metrics_table(CLOSEOUT_MD.read_text(encoding="utf-8"))
    return {
        "status": "pass",
        "map_json": MAP_JSON.relative_to(ROOT).as_posix(),
        "map_markdown": MAP_MD.relative_to(ROOT).as_posix(),
        "closeout_record": CLOSEOUT_MD.relative_to(ROOT).as_posix(),
        "metrics": metrics,
        "closeout_markdown_metrics": closeout_metrics,
        "boundary_context_self_test": boundary_self_test,
        "proof_ceiling": "REVIEWER_METRICS_PIPELINE_V1_CLOSED_REVIEWER_VISIBLE",
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--format", choices=("text", "json"), default="text")
    args = parser.parse_args(argv)
    try:
        result = verify()
    except VerificationError as exc:
        print(f"REVIEWER_METRICS_PIPELINE_V1_CLOSEOUT=FAIL: {exc}", file=sys.stderr)
        return 1
    if args.format == "json":
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print("REVIEWER_METRICS_PIPELINE_V1_CLOSEOUT=PASS")
        print(f"map_json={result['map_json']}")
        print(f"closeout_record={result['closeout_record']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
