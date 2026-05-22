#!/usr/bin/env python3
"""Fail-closed verification for the Cyber Kill Chain coverage artifact."""
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
MARKDOWN_PATH = ROOT / "docs" / "mappings" / "CYBER_KILL_CHAIN_COVERAGE.md"
INDEX_PATH = ROOT / "proof" / "indexes" / "CYBER_KILL_CHAIN_COVERAGE.yml"

EXPECTED_STAGES = [
    "Reconnaissance",
    "Weaponization",
    "Delivery",
    "Exploitation",
    "Installation",
    "Command & Control",
    "Actions on Objectives",
]

REQUIRED_TOP_LEVEL = {
    "version",
    "artifact",
    "system",
    "public_safe",
    "proof_authority",
    "claim_boundary",
    "stages",
}

REQUIRED_STAGE_FIELDS = {
    "stage",
    "status",
    "artifacts",
    "behavior_family",
    "proof_state",
    "validation_state",
    "automation_support",
    "ai_support_boundary",
    "blocked_claims",
    "next_promotion_gate",
    "role_fit_signal",
}

REQUIRED_BOUNDARY_VALUES = {
    "rendering_is_not_proof": True,
    "runtime_active_claimed": False,
    "signal_observed_claimed": False,
    "production_ready_claimed": False,
    "ai_approved_claimed": False,
    "analyst_approved_claimed": False,
}

REQUIRED_MAPPINGS = {
    "Reconnaissance": ["ID-DET-001", "ID-DET-002", "ID-DET-003", "ID-DET-004"],
    "Delivery": ["AWS-DET-001"],
    "Exploitation": ["HO-DET-001"],
    "Installation": ["HO-DET-011", "HO-DET-012"],
    "Command & Control": ["HO-NDR-001", "HO-PIPE-001"],
    "Actions on Objectives": ["SOAR", "AutoSOC", "Local GPU", "Offline LLM"],
}

RISKY_TERMS = [
    "runtime-active",
    "signal-observed",
    "production-ready",
    "public-safe runtime",
    "autonomous SOC",
    "AI-approved",
    "analyst-approved",
    "live AWS",
    "live IdP",
    "live Splunk",
    "Cribl-routed proof",
    "Wazuh-routed proof",
    "Security Onion observed proof",
]

NEGATIVE_CONTEXT_MARKERS = [
    "blocked",
    "blocked_claims",
    "claim boundary",
    "claim_boundary",
    "does not",
    "cannot",
    "forbidden",
    "denied",
    "no ",
    "no-claim",
    "not ",
    "not_",
    "not claimed",
    "not proven",
    "without ",
    "false",
    "proof_authority: false",
]

NEGATIVE_TABLE_HEADERS = [
    "blocked claims",
    "blocked",
    "not claimed",
    "not proven",
    "no-claim",
    "claim boundary",
    "does not prove",
    "does not claim",
    "forbidden",
    "denied",
]


class VerificationError(Exception):
    """Raised when the Cyber Kill Chain coverage artifact fails verification."""


def fail(message: str) -> None:
    print(f"Cyber Kill Chain coverage verification failed: {message}", file=sys.stderr)
    raise SystemExit(1)


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def load_yaml(path: Path) -> dict[str, Any]:
    if yaml is None:
        raise VerificationError("PyYAML is required to parse YAML files")
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        raise VerificationError(f"malformed YAML in {rel(path)}: {exc}") from exc
    if not isinstance(data, dict):
        raise VerificationError(f"{rel(path)} must contain a top-level mapping")
    return data


def require_files_exist() -> None:
    for path in [MARKDOWN_PATH, INDEX_PATH]:
        if not path.is_file():
            raise VerificationError(f"missing required artifact file: {rel(path)}")


def require_nonempty_sequence(value: Any, label: str) -> list[Any]:
    if not isinstance(value, list) or not value:
        raise VerificationError(f"{label} must be a non-empty list")
    return value


def require_nonempty_text(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise VerificationError(f"{label} must be a non-empty string")
    return value


def normalize_text(value: Any) -> str:
    if isinstance(value, list):
        return "\n".join(str(item) for item in value)
    return str(value)


def validate_top_level(index: dict[str, Any]) -> None:
    missing = REQUIRED_TOP_LEVEL - set(index)
    if missing:
        raise VerificationError(f"index missing top-level fields: {sorted(missing)}")
    if index.get("version") != 1:
        raise VerificationError("version must be 1")
    if index.get("artifact") != "CYBER_KILL_CHAIN_COVERAGE":
        raise VerificationError("artifact must be CYBER_KILL_CHAIN_COVERAGE")
    if index.get("system") != "HawkinsOperations":
        raise VerificationError("system must be HawkinsOperations")
    if index.get("public_safe") is not True:
        raise VerificationError("public_safe must be true")
    if index.get("proof_authority") is not False:
        raise VerificationError("proof_authority must be false")

    boundary = index.get("claim_boundary")
    if not isinstance(boundary, dict):
        raise VerificationError("claim_boundary must be a mapping")
    for field, expected in REQUIRED_BOUNDARY_VALUES.items():
        if boundary.get(field) is not expected:
            raise VerificationError(f"claim_boundary.{field} must be {str(expected).lower()}")


def validate_stages(index: dict[str, Any]) -> dict[str, dict[str, Any]]:
    stages = require_nonempty_sequence(index.get("stages"), "stages")
    names: list[str] = []
    by_name: dict[str, dict[str, Any]] = {}
    for raw_stage in stages:
        if not isinstance(raw_stage, dict):
            raise VerificationError("each stage must be a mapping")
        missing = REQUIRED_STAGE_FIELDS - set(raw_stage)
        stage_name = raw_stage.get("stage", "<unknown>")
        if missing:
            raise VerificationError(f"{stage_name} missing fields: {sorted(missing)}")
        stage = require_nonempty_text(raw_stage.get("stage"), "stage")
        if stage in by_name:
            raise VerificationError(f"duplicate stage: {stage}")
        for field in REQUIRED_STAGE_FIELDS - {"stage"}:
            value = raw_stage.get(field)
            if field in {"status", "role_fit_signal"}:
                require_nonempty_text(value, f"{stage}.{field}")
            else:
                require_nonempty_sequence(value, f"{stage}.{field}")
        names.append(stage)
        by_name[stage] = raw_stage
    if names != EXPECTED_STAGES:
        raise VerificationError(f"stages must exactly match expected order: {EXPECTED_STAGES}")
    return by_name


def validate_required_mappings(stages: dict[str, dict[str, Any]]) -> None:
    for stage_name, required_terms in REQUIRED_MAPPINGS.items():
        stage_text = normalize_text(stages[stage_name])
        for term in required_terms:
            if term not in stage_text:
                raise VerificationError(f"{stage_name} missing required mapping term: {term}")


def has_negative_marker(value: str) -> bool:
    return any(marker in value.lower() for marker in NEGATIVE_CONTEXT_MARKERS)


def is_markdown_table_row(line: str) -> bool:
    stripped = line.strip()
    return stripped.startswith("|") and stripped.endswith("|") and stripped.count("|") >= 2


def split_markdown_table_row(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def is_markdown_table_separator(cells: list[str]) -> bool:
    return bool(cells) and all(re.fullmatch(r":?-{3,}:?", cell.strip()) for cell in cells)


def table_header_for_row(lines: list[str], index: int) -> list[str]:
    start = index
    while start > 0 and is_markdown_table_row(lines[start - 1]):
        start -= 1
    for offset in range(start, index):
        cells = split_markdown_table_row(lines[offset])
        if not is_markdown_table_separator(cells):
            return cells
    return []


def table_cell_has_negative_context(lines: list[str], index: int, term: str) -> bool:
    cells = split_markdown_table_row(lines[index])
    headers = table_header_for_row(lines, index)
    term_pattern = re.compile(re.escape(term), flags=re.IGNORECASE)
    for cell_index, cell in enumerate(cells):
        if not term_pattern.search(cell):
            continue
        header = headers[cell_index] if cell_index < len(headers) else ""
        if has_negative_marker(cell):
            return True
        if any(marker in header.lower() for marker in NEGATIVE_TABLE_HEADERS):
            return True
        if len(cells) == 2 and any(has_negative_marker(other) for other in cells if other != cell):
            return True
    return False


def line_has_negative_context(lines: list[str], index: int, term: str) -> bool:
    line = lines[index]
    if is_markdown_table_row(line):
        return table_cell_has_negative_context(lines, index, term)

    start = max(index - 20, 0)
    end = min(index + 2, len(lines))
    context = "\n".join(lines[start:end]).lower()
    if any(marker in context for marker in NEGATIVE_CONTEXT_MARKERS):
        return True
    for offset in range(start, index + 1):
        if "blocked_claims:" in lines[offset].lower():
            return True
    return False


def validate_risky_term_context(path: Path) -> None:
    lines = path.read_text(encoding="utf-8").splitlines()
    for index, line in enumerate(lines):
        for term in RISKY_TERMS:
            if re.search(re.escape(term), line, flags=re.IGNORECASE):
                if not line_has_negative_context(lines, index, term):
                    raise VerificationError(
                        f"{rel(path)}:{index + 1} uses '{term}' outside blocked/negative context"
                    )


def validate_no_stale_work_path(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    if "C:\\Raylee\\Work" in text:
        raise VerificationError(f"{rel(path)} contains stale Work path reference")


def run_internal_context_self_checks() -> None:
    positive_table = [
        "| Stage | Current State | Blocked Claims |",
        "|---|---|---|",
        "| Exploitation | runtime-active | signal-observed blocked |",
    ]
    if line_has_negative_context(positive_table, 2, "runtime-active"):
        raise VerificationError("internal self-check failed: positive table runtime-active row passed")

    blocked_table = [
        "| Stage | Current State | Blocked Claims |",
        "|---|---|---|",
        "| Exploitation | CONTROLLED_TEST_VALIDATED | runtime-active is blocked / not proven |",
    ]
    if not line_has_negative_context(blocked_table, 2, "runtime-active"):
        raise VerificationError("internal self-check failed: blocked table runtime-active row failed")

    positive_text = ["Current state: runtime-active"]
    if line_has_negative_context(positive_text, 0, "runtime-active"):
        raise VerificationError("internal self-check failed: positive text runtime-active passed")

    blocked_text = ["Blocked claims:", "- runtime-active"]
    if not line_has_negative_context(blocked_text, 1, "runtime-active"):
        raise VerificationError("internal self-check failed: blocked text runtime-active failed")


def main() -> int:
    try:
        run_internal_context_self_checks()
        require_files_exist()
        index = load_yaml(INDEX_PATH)
        validate_top_level(index)
        stages = validate_stages(index)
        validate_required_mappings(stages)
        for path in [MARKDOWN_PATH, INDEX_PATH]:
            validate_risky_term_context(path)
            validate_no_stale_work_path(path)
    except VerificationError as exc:
        fail(str(exc))

    print("Cyber Kill Chain coverage verification passed.")
    print("STAGES=7")
    print("PROOF_AUTHORITY=false")
    print("CLAIM_BOUNDARIES=pass")
    print("REQUIRED_MAPPINGS=pass")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
