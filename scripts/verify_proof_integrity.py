#!/usr/bin/env python3
"""
Baseline proof integrity check.

Current scope:
- Validates baseline HOD-001 proof record schema shape
- Validates required baseline HOD-001 proof artifact paths in this repository
- Validates integrity field presence and basic format checks (IDs, refs, hash formats)

Not covered yet:
- Non-baseline proof families
- Detection correctness
- Validation semantic truth
- Generalized cross-family proof maturity
"""
import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / ".github" / "contracts" / "proof-record.schema.json"
LEDGER_PATH = ROOT / "evidence" / "evidence-ledger.json"
PROOF_RECORD_PATH = ROOT / "proof" / "records" / "PROOF-HOD-001-2026-04-21-001.json"
HEX64_RE = re.compile(r"^[0-9a-fA-F]{64}$")
COMMIT_RE = re.compile(r"^[0-9a-f]{7,40}$")


def fail(msg: str) -> None:
    print(f"Baseline proof integrity check failed: {msg}", file=sys.stderr)
    raise SystemExit(1)


def load_json(path: Path, label: str) -> dict:
    if not path.exists():
        fail(f"missing {label}: {path.relative_to(ROOT).as_posix()}")
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        fail(f"invalid JSON in {label} ({path.relative_to(ROOT).as_posix()}): {exc}")


def validate_required_artifacts_exist() -> None:
    for path in [SCHEMA_PATH, LEDGER_PATH, PROOF_RECORD_PATH]:
        if not path.exists():
            fail(f"required baseline artifact missing: {path.relative_to(ROOT).as_posix()}")


def validate_schema_shape(record: dict, schema: dict) -> None:
    for key in schema.get("required", []):
        if key not in record:
            fail(f"proof record missing required key: {key}")

    detection = record.get("detection", {})
    validation = record.get("validation", {})

    if not isinstance(record.get("proof_id"), str):
        fail("proof_id must be a string")
    if not isinstance(record.get("created_at"), str):
        fail("created_at must be a string")

    if not isinstance(detection.get("id"), str):
        fail("detection.id must be a string")
    if not COMMIT_RE.match(detection.get("commit", "")):
        fail("detection.commit must be 7-40 lowercase hex chars")
    if not isinstance(detection.get("artifact_paths"), list) or not detection["artifact_paths"]:
        fail("detection.artifact_paths must be a non-empty array")

    if not COMMIT_RE.match(validation.get("commit", "")):
        fail("validation.commit must be 7-40 lowercase hex chars")
    if not HEX64_RE.match(validation.get("report_hash_sha256", "")):
        fail("validation.report_hash_sha256 must be a 64-char hex string")
    if not isinstance(validation.get("artifact_paths"), list) or not validation["artifact_paths"]:
        fail("validation.artifact_paths must be a non-empty array")

    if not isinstance(record.get("outcome_summary"), str):
        fail("outcome_summary must be a string")
    if not isinstance(record.get("claim_boundary"), str):
        fail("claim_boundary must be a string")


def validate_integrity_fields(record: dict, ledger: dict) -> None:
    if record.get("proof_id") != "PROOF-HOD-001-2026-04-21-001":
        fail("baseline scope expects proof_id PROOF-HOD-001-2026-04-21-001")
    if record.get("detection", {}).get("id") != "HOD-001":
        fail("baseline scope expects detection.id HOD-001")

    entries = ledger.get("entries", [])
    if not isinstance(entries, list) or not entries:
        fail("evidence ledger must contain at least one entry")

    target = None
    for entry in entries:
        if entry.get("id") == "PROOF-HOD-001-2026-04-21-001":
            target = entry
            break
    if target is None:
        fail("missing baseline proof ledger entry PROOF-HOD-001-2026-04-21-001")

    if not isinstance(target.get("source_ref"), str) or "HOD-001" not in target["source_ref"]:
        fail("ledger source_ref must include HOD-001 baseline reference")
    if not HEX64_RE.match(target.get("sha256", "")):
        fail("ledger sha256 must be a 64-char hex string")
    artifact_paths = target.get("artifact_paths", [])
    if not isinstance(artifact_paths, list) or not artifact_paths:
        fail("ledger artifact_paths must be a non-empty array")
    if "proof/records/PROOF-HOD-001-2026-04-21-001.json" not in artifact_paths:
        fail("ledger artifact_paths must include baseline proof record path")


def main() -> int:
    print("Scope: baseline proof integrity for HOD-001 artifacts only.")
    validate_required_artifacts_exist()
    schema = load_json(SCHEMA_PATH, "proof schema")
    ledger = load_json(LEDGER_PATH, "proof evidence ledger")
    record = load_json(PROOF_RECORD_PATH, "baseline proof record")
    validate_schema_shape(record, schema)
    validate_integrity_fields(record, ledger)
    print("Baseline proof integrity check passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
