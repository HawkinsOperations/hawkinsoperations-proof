#!/usr/bin/env python3
"""Fail-closed verification for the detection proof status index."""
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
ORG_ROOT = ROOT.parent
INDEX_PATH = ROOT / "proof" / "indexes" / "DETECTION_PROOF_STATUS_INDEX.yml"
DETECTIONS_MATRIX_PATH = ORG_ROOT / "hawkinsoperations-detections" / "detections" / "DETECTION_PROMOTION_MATRIX.yml"
VALIDATION_REGISTRY_PATH = ORG_ROOT / "hawkinsoperations-validation" / "validation" / "VALIDATION_REGISTRY.yml"
PLATFORM_FACTORY_PATH = ORG_ROOT / "hawkinsoperations-platform" / "scripts" / "ho_factory.py"

REQUIRED_TOP_LEVEL = {"schema_version", "owner_repo", "truth_surface", "human_review_required", "claim_boundary", "entries"}
REQUIRED_ENTRY_FIELDS = {
    "detection_id",
    "source_truth_owner",
    "source_status",
    "validation_truth_owner",
    "validation_status",
    "platform_visibility_owner",
    "platform_visibility_status",
    "proof_record_path",
    "proof_card_path",
    "proof_ceiling",
    "runtime_status",
    "signal_status",
    "public_safe_status",
    "website_status",
    "blocked_claims",
    "next_gate",
    "notes",
}

ALLOWED_PROOF_CEILINGS = {
    "NO_PROOF_RECORD",
    "CONTROLLED_TEST_VALIDATED",
    "PRIVATE_RUNTIME_EVIDENCE_CAPTURED",
    "CROSS_SOURCE_CORROBORATION_CONTRACT_DEFINED",
}
ALLOWED_SOURCE_STATUSES = {"SOURCE_EXISTS", "EXTERNAL_BOUNDARY_CONTRACT"}
ALLOWED_VALIDATION_STATUSES = {
    "VALIDATION_PLANNED",
    "CONTROLLED_TEST_VALIDATED",
    "VALIDATION_CONTRACT_ENFORCED",
}
ALLOWED_PLATFORM_STATUSES = {"STATUS_VISIBILITY_PRESENT_NON_PROMOTIONAL", "NOT_PLATFORM_INDEXED"}
ALLOWED_RUNTIME_STATUSES = {"NOT_PROVEN", "PRIVATE_RUNTIME_BOUNDARY_CONTEXT_ONLY", "PRIVATE_RUNTIME_EVIDENCE_CAPTURED"}
ALLOWED_SIGNAL_STATUSES = {"NOT_PROVEN"}
ALLOWED_WEBSITE_STATUSES = {"WEBSITE_UNTOUCHED_NOT_PROOF"}
PUBLIC_SAFE_REQUIRED = "NOT_PUBLIC_SAFE"

PRIVATE_RUNTIME_RECORD_MARKERS = {
    "PRIVATE_RUNTIME_EVIDENCE_CAPTURED": "PRIVATE_RUNTIME_EVIDENCE_CAPTURED",
    "PRIVATE_RUNTIME_BOUNDARY_CONTEXT_ONLY": "Private/internal runtime",
}

PLATFORM_VISIBLE_IDS = {
    "HO-DET-001",
    "HO-DET-011",
    "HO-DET-012",
    "ID-DET-001",
    "ID-DET-002",
    "ID-DET-003",
    "ID-DET-004",
}

BLOCKED_CLAIMS = [
    "runtime-active public proof",
    "signal-observed public proof",
    "public-safe proof",
    "live IdP proof",
    "live SIEM proof",
    "live Splunk proof",
    "live Wazuh proof",
    "live Cribl proof",
    "live Security Onion proof",
    "production-ready",
    "fleet-wide",
    "autonomous SOC",
    "AI-approved disposition",
    "analyst-approved disposition",
    "website rendering as proof",
]

BOUNDARY_CONTEXT_MARKERS = [
    "blocked",
    "not_proven",
    "not proven",
    "not_public_safe",
    "not public-safe",
    "not proof",
    "not promote",
    "does not prove",
    "does not create",
    "does not claim",
    "without promoting",
    "boundary",
    "unless an explicit proof record supports it",
    "separate proof scope",
    "no ",
    "blocked_claims",
    "claim_boundary",
]


class VerificationError(Exception):
    """Raised when the proof status index fails verification."""


def fail(message: str) -> None:
    print(f"Detection proof status index verification failed: {message}", file=sys.stderr)
    raise SystemExit(1)


def load_yaml(path: Path, label: str) -> Any:
    if yaml is None:
        raise VerificationError("PyYAML is required to parse YAML files")
    if not path.exists():
        raise VerificationError(f"missing {label}: {path}")
    try:
        return yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        raise VerificationError(f"malformed {label}: {exc}") from exc


def rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return str(path)


def require_mapping(value: Any, label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise VerificationError(f"{label} must be a mapping")
    return value


def require_nonempty_string(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise VerificationError(f"{label} must be a non-empty string")
    return value


def normalize_entries_by_id(data: dict[str, Any], label: str) -> dict[str, dict[str, Any]]:
    entries = data.get("entries")
    if not isinstance(entries, list) or not entries:
        raise VerificationError(f"{label}.entries must be a non-empty list")
    by_id: dict[str, dict[str, Any]] = {}
    for raw in entries:
        entry = require_mapping(raw, f"{label}.entry")
        detection_id = require_nonempty_string(entry.get("detection_id"), f"{label}.entry.detection_id")
        if detection_id in by_id:
            raise VerificationError(f"duplicate detection_id in {label}: {detection_id}")
        by_id[detection_id] = entry
    return by_id


def load_detection_matrix() -> dict[str, dict[str, Any]]:
    matrix = require_mapping(load_yaml(DETECTIONS_MATRIX_PATH, "detections matrix"), "detections matrix")
    return normalize_entries_by_id(matrix, "detections matrix")


def load_validation_registry() -> dict[str, dict[str, Any]]:
    registry = require_mapping(load_yaml(VALIDATION_REGISTRY_PATH, "validation registry"), "validation registry")
    packages = registry.get("packages")
    if not isinstance(packages, list) or not packages:
        raise VerificationError("validation registry.packages must be a non-empty list")
    by_id: dict[str, dict[str, Any]] = {}
    for raw in packages:
        entry = require_mapping(raw, "validation registry.package")
        detection_id = require_nonempty_string(entry.get("detection_id"), "validation registry.package.detection_id")
        if detection_id in by_id:
            raise VerificationError(f"duplicate detection_id in validation registry: {detection_id}")
        by_id[detection_id] = entry
    return by_id


def validation_status_from_registry(entry: dict[str, Any]) -> str:
    ceiling = entry.get("proof_ceiling")
    if ceiling == "CONTROLLED_TEST_VALIDATED":
        return "CONTROLLED_TEST_VALIDATED"
    if ceiling == "VALIDATION_CONTRACT_ENFORCED":
        return "VALIDATION_CONTRACT_ENFORCED"
    raise VerificationError(f"unknown validation registry proof_ceiling for {entry.get('detection_id')}: {ceiling}")


def validate_top_level(index: dict[str, Any]) -> None:
    missing = REQUIRED_TOP_LEVEL - set(index)
    if missing:
        raise VerificationError(f"index missing top-level fields: {sorted(missing)}")
    if index.get("owner_repo") != "hawkinsoperations-proof":
        raise VerificationError("owner_repo must be hawkinsoperations-proof")
    if index.get("truth_surface") != "proof_boundary_index":
        raise VerificationError("truth_surface must be proof_boundary_index")
    if index.get("human_review_required") is not True:
        raise VerificationError("human_review_required must be true")
    boundary = require_mapping(index.get("claim_boundary"), "claim_boundary")
    blocked = boundary.get("blocked_claims")
    if not isinstance(blocked, list):
        raise VerificationError("claim_boundary.blocked_claims must be a list")
    lower_blocked = "\n".join(str(item).lower() for item in blocked)
    for claim in BLOCKED_CLAIMS:
        if claim.lower() not in lower_blocked:
            raise VerificationError(f"claim_boundary missing blocked claim: {claim}")


def validate_path_field(entry: dict[str, Any], field: str, detection_id: str) -> str | None:
    value = entry.get(field)
    if value is None:
        return None
    if not isinstance(value, str) or not value.strip():
        raise VerificationError(f"{detection_id}.{field} must be null or a non-empty relative path")
    if Path(value).is_absolute() or ".." in Path(value).parts:
        raise VerificationError(f"{detection_id}.{field} must be a safe relative path")
    path = ROOT / value
    if not path.is_file():
        raise VerificationError(f"{detection_id}.{field} points to missing file: {value}")
    return value


def validate_private_runtime_status(entry: dict[str, Any], record_path: str | None, detection_id: str) -> None:
    runtime_status = entry["runtime_status"]
    if runtime_status == "NOT_PROVEN":
        return
    if record_path is None:
        raise VerificationError(f"{detection_id} promotes private runtime status without a proof record")
    marker = PRIVATE_RUNTIME_RECORD_MARKERS.get(runtime_status)
    if marker is None:
        raise VerificationError(f"{detection_id} uses unknown private runtime status: {runtime_status}")
    record_text = (ROOT / record_path).read_text(encoding="utf-8")
    if marker not in record_text:
        raise VerificationError(f"{detection_id} proof record does not support runtime_status {runtime_status}")


def validate_proof_ceiling(entry: dict[str, Any], record_path: str | None, card_path: str | None, detection_id: str) -> None:
    ceiling = entry["proof_ceiling"]
    if ceiling not in ALLOWED_PROOF_CEILINGS:
        raise VerificationError(f"{detection_id} has unknown proof_ceiling: {ceiling}")
    if ceiling in {"CONTROLLED_TEST_VALIDATED", "PRIVATE_RUNTIME_EVIDENCE_CAPTURED"} and record_path is None:
        raise VerificationError(f"{detection_id} claims {ceiling} without a proof record")
    if ceiling == "CROSS_SOURCE_CORROBORATION_CONTRACT_DEFINED" and card_path is None:
        raise VerificationError(f"{detection_id} claims boundary contract ceiling without a proof card")
    if ceiling == "NO_PROOF_RECORD" and record_path is not None:
        raise VerificationError(f"{detection_id} has proof record path but proof_ceiling is NO_PROOF_RECORD")
    if record_path is not None:
        text = (ROOT / record_path).read_text(encoding="utf-8")
        if ceiling == "CONTROLLED_TEST_VALIDATED" and "CONTROLLED_TEST_VALIDATED" not in text:
            raise VerificationError(f"{detection_id} proof record does not support CONTROLLED_TEST_VALIDATED")
        if ceiling == "PRIVATE_RUNTIME_EVIDENCE_CAPTURED" and "PRIVATE_RUNTIME_EVIDENCE_CAPTURED" not in text:
            raise VerificationError(f"{detection_id} proof record does not support PRIVATE_RUNTIME_EVIDENCE_CAPTURED")


def validate_claim_boundary_text(entry: dict[str, Any], detection_id: str) -> None:
    blocked = entry["blocked_claims"]
    if not isinstance(blocked, list) or not blocked:
        raise VerificationError(f"{detection_id}.blocked_claims must be a non-empty list")
    lower_blocked = "\n".join(str(item).lower() for item in blocked)
    for claim in ["runtime-active public proof", "signal-observed public proof", "public-safe proof"]:
        if claim not in lower_blocked:
            raise VerificationError(f"{detection_id}.blocked_claims missing required blocked claim: {claim}")
    serialized = "\n".join(f"{key}: {value}" for key, value in entry.items()).lower()
    for term in BLOCKED_CLAIMS:
        term_lower = term.lower()
        for match in re.finditer(re.escape(term_lower), serialized):
            line_start = serialized.rfind("\n", 0, match.start()) + 1
            line_end = serialized.find("\n", match.end())
            if line_end == -1:
                line_end = len(serialized)
            line = serialized[line_start:line_end]
            if not any(marker in line for marker in BOUNDARY_CONTEXT_MARKERS):
                raise VerificationError(f"{detection_id} blocked term outside boundary context: {line}")


def validate_entry(
    entry: dict[str, Any],
    detections: dict[str, dict[str, Any]],
    validation: dict[str, dict[str, Any]],
    platform_text: str,
) -> None:
    missing = REQUIRED_ENTRY_FIELDS - set(entry)
    if missing:
        raise VerificationError(f"entry missing fields: {sorted(missing)}")

    detection_id = require_nonempty_string(entry["detection_id"], "detection_id")
    for field in [
        "source_truth_owner",
        "source_status",
        "validation_truth_owner",
        "validation_status",
        "platform_visibility_owner",
        "platform_visibility_status",
        "proof_ceiling",
        "runtime_status",
        "signal_status",
        "public_safe_status",
        "website_status",
        "next_gate",
        "notes",
    ]:
        require_nonempty_string(entry[field], f"{detection_id}.{field}")

    if entry["source_truth_owner"] != "hawkinsoperations-detections":
        raise VerificationError(f"{detection_id}.source_truth_owner must be hawkinsoperations-detections")
    if entry["validation_truth_owner"] != "hawkinsoperations-validation":
        raise VerificationError(f"{detection_id}.validation_truth_owner must be hawkinsoperations-validation")
    if entry["platform_visibility_owner"] != "hawkinsoperations-platform":
        raise VerificationError(f"{detection_id}.platform_visibility_owner must be hawkinsoperations-platform")
    if entry["source_status"] not in ALLOWED_SOURCE_STATUSES:
        raise VerificationError(f"{detection_id} has unsupported source_status: {entry['source_status']}")
    if entry["validation_status"] not in ALLOWED_VALIDATION_STATUSES:
        raise VerificationError(f"{detection_id} has unsupported validation_status: {entry['validation_status']}")
    if entry["platform_visibility_status"] not in ALLOWED_PLATFORM_STATUSES:
        raise VerificationError(f"{detection_id} has unsupported platform_visibility_status: {entry['platform_visibility_status']}")
    if entry["runtime_status"] not in ALLOWED_RUNTIME_STATUSES:
        raise VerificationError(f"{detection_id} has unsupported runtime_status: {entry['runtime_status']}")
    if entry["signal_status"] not in ALLOWED_SIGNAL_STATUSES:
        raise VerificationError(f"{detection_id} has unsupported signal_status: {entry['signal_status']}")
    if entry["public_safe_status"] != PUBLIC_SAFE_REQUIRED:
        raise VerificationError(f"{detection_id}.public_safe_status must be {PUBLIC_SAFE_REQUIRED}")
    if entry["website_status"] not in ALLOWED_WEBSITE_STATUSES:
        raise VerificationError(f"{detection_id}.website_status must be WEBSITE_UNTOUCHED_NOT_PROOF")

    record_path = validate_path_field(entry, "proof_record_path", detection_id)
    card_path = validate_path_field(entry, "proof_card_path", detection_id)
    validate_proof_ceiling(entry, record_path, card_path, detection_id)
    validate_private_runtime_status(entry, record_path, detection_id)
    validate_claim_boundary_text(entry, detection_id)

    detection_entry = detections.get(detection_id)
    if detection_entry is None:
        raise VerificationError(f"{detection_id} missing from detections source-truth matrix")
    if detection_entry.get("source_status") != entry["source_status"]:
        raise VerificationError(
            f"{detection_id} source_status drift: proof index={entry['source_status']} "
            f"detections matrix={detection_entry.get('source_status')}"
        )
    if detection_entry.get("runtime_active") is not False:
        raise VerificationError(f"{detection_id} detections matrix runtime_active must be false")
    if detection_entry.get("signal_observed") is not False:
        raise VerificationError(f"{detection_id} detections matrix signal_observed must be false")
    if detection_entry.get("public_safe_status") != PUBLIC_SAFE_REQUIRED:
        raise VerificationError(f"{detection_id} detections matrix public_safe_status must be {PUBLIC_SAFE_REQUIRED}")

    validation_entry = validation.get(detection_id)
    if validation_entry is None:
        if entry["validation_status"] != "VALIDATION_PLANNED":
            raise VerificationError(f"{detection_id} missing from validation registry but validation_status is not VALIDATION_PLANNED")
    else:
        expected_validation_status = validation_status_from_registry(validation_entry)
        if entry["validation_status"] != expected_validation_status:
            raise VerificationError(
                f"{detection_id} validation drift: proof index={entry['validation_status']} "
                f"validation registry={expected_validation_status}"
            )
        if validation_entry.get("public_safe_status") != PUBLIC_SAFE_REQUIRED:
            raise VerificationError(f"{detection_id} validation registry public_safe_status must be {PUBLIC_SAFE_REQUIRED}")
        if validation_entry.get("runtime_status") is not False:
            raise VerificationError(f"{detection_id} validation registry runtime_status must be false")
        if validation_entry.get("signal_status") is not False:
            raise VerificationError(f"{detection_id} validation registry signal_status must be false")

    if detection_id in PLATFORM_VISIBLE_IDS:
        if entry["platform_visibility_status"] != "STATUS_VISIBILITY_PRESENT_NON_PROMOTIONAL":
            raise VerificationError(f"{detection_id} should be marked platform-visible but non-promotional")
        if detection_id not in platform_text:
            raise VerificationError(f"{detection_id} missing from platform factory visibility surface")
    elif entry["platform_visibility_status"] != "NOT_PLATFORM_INDEXED":
        raise VerificationError(f"{detection_id} should be marked NOT_PLATFORM_INDEXED")


def verify_index(index_path: Path = INDEX_PATH) -> list[dict[str, Any]]:
    index = require_mapping(load_yaml(index_path, "proof status index"), "proof status index")
    validate_top_level(index)
    entries = normalize_entries_by_id(index, "proof status index")
    detections = load_detection_matrix()
    validation = load_validation_registry()
    platform_text = PLATFORM_FACTORY_PATH.read_text(encoding="utf-8") if PLATFORM_FACTORY_PATH.exists() else ""
    for entry in entries.values():
        validate_entry(entry, detections, validation, platform_text)
    return list(entries.values())


def main() -> int:
    try:
        entries = verify_index()
    except VerificationError as exc:
        fail(str(exc))
    print("Detection proof status index verification passed.")
    print("DETECTION_ID | PROOF_CEILING | RUNTIME_STATUS | SIGNAL_STATUS | PUBLIC_SAFE_STATUS")
    for entry in entries:
        print(
            f"{entry['detection_id']} | {entry['proof_ceiling']} | {entry['runtime_status']} | "
            f"{entry['signal_status']} | {entry['public_safe_status']}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
