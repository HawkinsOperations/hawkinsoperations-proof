#!/usr/bin/env python3
"""Fail-closed verification for the detection proof status index."""
from __future__ import annotations

import re
import sys
import unicodedata
from pathlib import Path, PurePosixPath
from typing import Any
from urllib.parse import unquote

try:
    import yaml
except ImportError:  # pragma: no cover - environment failure path
    yaml = None


ROOT = Path(__file__).resolve().parents[1]
ORG_ROOT = ROOT.parent
INDEX_PATH = ROOT / "proof" / "indexes" / "DETECTION_PROOF_STATUS_INDEX.yml"
DETECTIONS_MATRIX_PATH = ORG_ROOT / "hawkinsoperations-detections" / "detections" / "DETECTION_PROMOTION_MATRIX.yml"
VALIDATION_REGISTRY_PATH = ORG_ROOT / "hawkinsoperations-validation" / "validation" / "VALIDATION_REGISTRY.yml"

REQUIRED_TOP_LEVEL = {
    "schema_version",
    "owner_repo",
    "truth_surface",
    "human_review_required",
    "current_authority",
    "claim_boundary",
    "entries",
}
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
REQUIRED_HO_DET_001_TRUTH_PLANES = {
    "source_truth",
    "validation_truth",
    "runtime_truth",
    "signal_truth",
    "evidence_truth",
    "ai_triage_truth",
    "public_proof_truth",
    "human_review_truth",
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
AFFIRMATIVE_AUTHORITY_CLAIM_RE = re.compile(
    r"\b(?:"
    r"(?:customer|socaas)\b.{0,48}\bdeploy(?:ed|ment|ing)?\b"
    r"|deployed\s+to\s+(?:a\s+)?customer"
    r"|analyst\s+(?:approval\s+(?:is\s+)?(?:granted|approved)|approved)"
    r"|final\s+authorization\s+(?:is\s+)?(?:granted|approved|received)"
    r"|case\s+(?:closure\s+(?:is\s+)?(?:approved|complete)|is\s+closed|closed)"
    r"|public[\s_-]*safe(?:\s+runtime\s+proof)?\s+(?:is\s+)?(?:established|confirmed|approved|for\s+release)"
    r"|production\s+(?:deployment\s+)?(?:is\s+)?(?:active|live|ready|confirmed)"
    r"|runtime\s+(?:is\s+)?active"
    r"|signal\s+(?:(?:is|was)\s+)?observed"
    r"|ai\s+(?:disposition\s+)?authority\s+(?:is\s+)?enabled"
    r")\b",
    re.IGNORECASE,
)
LOCAL_NEGATION_RE = re.compile(
    r"\b(?:blocked|denied|false|not|never|no|prohibited|reject(?:ed|s)?|unsupported|without)\b",
    re.IGNORECASE,
)
NEGATIVE_LIST_INTRO_RE = re.compile(
    r"\b(?:does|do|did|must|is|are|was|were|can|cannot|could|should|will|would)\s+not\s+"
    r"(?:prove|establish|claim|promote|authorize|assert)\b|\bwithout\s+claiming\b",
    re.IGNORECASE,
)
NEGATIVE_LIST_SUFFIX_RE = re.compile(
    r"\bclaims?\s+(?:remain|remains|are|is)\s+(?:blocked|unsupported|not\s+approved)\.?$",
    re.IGNORECASE,
)
AFFIRMATIVE_STATE_AFTER_NEGATIVE_LIST_RE = re.compile(
    r"(?:"
    r"\b(?:customer|socaas)\b.{0,32}\b(?:deployment\s+)?(?:is|was)\s+"
    r"(?:active|confirmed|deployed|live|ready)\b"
    r"|\b(?:customer|socaas)\b.{0,32}\b(?:is|was)\s+deployed\b"
    r"|\bproduction\b.{0,24}\b(?:is|was)\s+(?:active|live|ready)\b"
    r"|\bruntime\b.{0,16}\b(?:is|was)\s+active\b"
    r"|\bsignal\b.{0,16}\b(?:is|was)\s+observed\b"
    r"|\bpublic[\s_-]*safe\b.{0,24}\b(?:is|was)\s+"
    r"(?:approved|confirmed|established|ready|released)\b"
    r"|\b(?:ai|analyst)\b.{0,32}\b(?:(?:is|was)\s+approved|approval\s+(?:is\s+)?granted|authority\s+(?:is\s+)?enabled)\b"
    r"|\bfinal\s+authori[sz]ation\b.{0,16}\b(?:is|was)?\s*(?:approved|granted|received)\b"
    r"|\bcase\s+closure\b.{0,16}\b(?:is|was)?\s*(?:approved|complete|granted|received)\b"
    r"|\bcase\b.{0,16}\b(?:is|was)\s+closed\b"
    r")",
    re.IGNORECASE,
)


def normalize_authority_security_text(value: str) -> str:
    normalized = unicodedata.normalize("NFKD", value).translate(
        {ord("\t"): " ", ord("\n"): " ", ord("\r"): " "}
    )
    return "".join(
        character
        for character in normalized
        if not unicodedata.category(character).startswith(("C", "M"))
    )


def contains_unnegated_affirmative_state(value: str) -> bool:
    # The affirmative pattern already requires a positive predicate such as
    # "is active" or "is confirmed". A negative word elsewhere in the same
    # scalar must not launder that later assertion.
    return AFFIRMATIVE_STATE_AFTER_NEGATIVE_LIST_RE.search(value) is not None


EXACT_BLOCKED_CLAIM_VALUES = {
    value.casefold()
    for value in {
        *BLOCKED_CLAIMS,
        "GitHub rendering as proof",
        "green CI as approval",
        "customer deployment",
        "SOCaaS deployment",
        "final authorization",
        "case closure",
        "public-safe proof unless an explicit proof record supports it",
    }
}


class VerificationError(Exception):
    """Raised when the proof status index fails verification."""


class UniqueKeySafeLoader(yaml.SafeLoader if yaml is not None else object):
    """Safe YAML loader that rejects duplicate keys at every mapping depth."""


if yaml is not None:
    def _construct_unique_mapping(loader: UniqueKeySafeLoader, node: Any, deep: bool = False) -> dict[Any, Any]:
        mapping: dict[Any, Any] = {}
        for key_node, value_node in node.value:
            key = loader.construct_object(key_node, deep=deep)
            try:
                duplicate = key in mapping
            except TypeError as exc:
                raise yaml.constructor.ConstructorError(
                    "while constructing a mapping",
                    node.start_mark,
                    "found an unhashable mapping key",
                    key_node.start_mark,
                ) from exc
            if duplicate:
                raise yaml.constructor.ConstructorError(
                    "while constructing a mapping",
                    node.start_mark,
                    f"found duplicate key {key!r}",
                    key_node.start_mark,
                )
            mapping[key] = loader.construct_object(value_node, deep=deep)
        return mapping


    UniqueKeySafeLoader.add_constructor(
        yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
        _construct_unique_mapping,
    )


def fail(message: str) -> None:
    print(f"Detection proof status index verification failed: {message}", file=sys.stderr)
    raise SystemExit(1)


def load_yaml(path: Path, label: str) -> Any:
    if yaml is None:
        raise VerificationError("PyYAML is required to parse YAML files")
    if not path.exists():
        raise VerificationError(f"missing {label}: {path}")
    try:
        return yaml.load(path.read_text(encoding="utf-8"), Loader=UniqueKeySafeLoader)
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
    require_exact_keys(index, REQUIRED_TOP_LEVEL, ALLOWED_TOP_LEVEL_FIELDS, "index")
    if index.get("owner_repo") != "hawkinsoperations-proof":
        raise VerificationError("owner_repo must be hawkinsoperations-proof")
    if index.get("truth_surface") != "proof_boundary_index":
        raise VerificationError("truth_surface must be proof_boundary_index")
    if index.get("human_review_required") is not True:
        raise VerificationError("human_review_required must be true")
    current = require_mapping(index.get("current_authority"), "current_authority")
    require_exact_keys(
        current,
        REQUIRED_CURRENT_AUTHORITY_FIELDS,
        ALLOWED_CURRENT_AUTHORITY_FIELDS,
        "current_authority",
    )
    if current.get("historical_snapshot") is not False:
        raise VerificationError("current_authority.historical_snapshot must be false")
    if current.get("current_authority") is not True:
        raise VerificationError("current_authority.current_authority must be true")
    if current.get("source_path") != "proof/indexes/DETECTION_PROOF_STATUS_INDEX.yml":
        raise VerificationError("current_authority.source_path must identify the proof-owned index")
    if current.get("derivation_method") != "derive_non_null_unique_paths_from_entries":
        raise VerificationError("current_authority.derivation_method must be derive_non_null_unique_paths_from_entries")
    declared_counts = require_mapping(current.get("derived_counts"), "current_authority.derived_counts")
    require_exact_keys(
        declared_counts,
        ALLOWED_DERIVED_COUNT_FIELDS,
        ALLOWED_DERIVED_COUNT_FIELDS,
        "current_authority.derived_counts",
    )
    if any(type(value) is not int or value < 0 for value in declared_counts.values()):
        raise VerificationError("current_authority.derived_counts values must be non-negative integers")
    boundary = require_mapping(index.get("claim_boundary"), "claim_boundary")
    require_exact_keys(
        boundary,
        ALLOWED_CLAIM_BOUNDARY_FIELDS,
        ALLOWED_CLAIM_BOUNDARY_FIELDS,
        "claim_boundary",
    )
    allowed_status_values = boundary.get("allowed_status_values")
    if not isinstance(allowed_status_values, list) or not allowed_status_values:
        raise VerificationError("claim_boundary.allowed_status_values must be a non-empty list")
    if any(not isinstance(item, str) or not item.strip() for item in allowed_status_values):
        raise VerificationError("claim_boundary.allowed_status_values entries must be non-empty strings")
    blocked = boundary.get("blocked_claims")
    if not isinstance(blocked, list):
        raise VerificationError("claim_boundary.blocked_claims must be a list")
    lower_blocked = "\n".join(str(item).lower() for item in blocked)
    for claim in BLOCKED_CLAIMS:
        if claim.lower() not in lower_blocked:
            raise VerificationError(f"claim_boundary missing blocked claim: {claim}")


def canonical_owned_path(value: str, field: str, detection_id: str) -> tuple[str, Path]:
    if any(ord(character) < 32 for character in value):
        raise VerificationError(f"{detection_id}.{field} contains a control character")
    decoded = value
    for _ in range(3):
        candidate = unquote(decoded)
        if candidate == decoded:
            break
        decoded = candidate
    if decoded != value:
        raise VerificationError(f"{detection_id}.{field} must not contain encoded path syntax")
    if "\\" in value:
        raise VerificationError(f"{detection_id}.{field} must use canonical POSIX separators")
    if re.match(r"^[A-Za-z]:", value) or value.startswith(("/", "//")):
        raise VerificationError(f"{detection_id}.{field} must be a repository-relative path")
    raw_parts = value.split("/")
    if any(part in {"", ".", ".."} for part in raw_parts):
        raise VerificationError(f"{detection_id}.{field} contains non-canonical path segments")
    pure = PurePosixPath(value)
    expected_parent = PurePosixPath("proof", "records" if field == "proof_record_path" else "cards")
    if pure.parent != expected_parent:
        raise VerificationError(
            f"{detection_id}.{field} must remain under {expected_parent.as_posix()}"
        )
    canonical = pure.as_posix()
    path = ROOT.joinpath(*pure.parts)
    resolved_root = ROOT.resolve()
    resolved_owned_root = ROOT.joinpath(*expected_parent.parts).resolve()
    resolved_path = path.resolve()
    try:
        resolved_path.relative_to(resolved_owned_root)
    except ValueError as exc:
        raise VerificationError(
            f"{detection_id}.{field} escapes {expected_parent.as_posix()}"
        ) from exc
    try:
        resolved_path.relative_to(resolved_root)
    except ValueError as exc:
        raise VerificationError(f"{detection_id}.{field} escapes the proof repository") from exc
    return canonical, resolved_path


def validate_path_field(entry: dict[str, Any], field: str, detection_id: str) -> str | None:
    value = entry.get(field)
    if value is None:
        return None
    if not isinstance(value, str) or not value.strip():
        raise VerificationError(f"{detection_id}.{field} must be null or a non-empty relative path")
    canonical, path = canonical_owned_path(value, field, detection_id)
    if canonical != value:
        raise VerificationError(f"{detection_id}.{field} must use its canonical repository-relative path")
    if not path.is_file():
        raise VerificationError(f"{detection_id}.{field} points to missing file: {value}")
    if path.name.casefold() != f"{detection_id}.md".casefold():
        raise VerificationError(f"{detection_id}.{field} filename must exactly identify its owning case")
    return value


def require_exact_keys(value: dict[str, Any], required: set[str], allowed: set[str], label: str) -> None:
    missing = required - set(value)
    unknown = set(value) - allowed
    if missing:
        raise VerificationError(f"{label} missing fields: {sorted(missing)}")
    if unknown:
        raise VerificationError(f"{label} contains unknown fields: {sorted(unknown)}")


PROMOTION_KEY_POLICIES: dict[str, set[Any]] = {
    "runtimeactive": {False},
    "runtimestatus": ALLOWED_RUNTIME_STATUSES,
    "signalobserved": {False},
    "signalstatus": ALLOWED_SIGNAL_STATUSES,
    "publicsafe": {False, "NOT_PUBLIC_SAFE"},
    "publicsafestatus": {"NOT_PUBLIC_SAFE"},
    "proofstatus": ALLOWED_PROOF_CEILINGS,
    "aidecideddisposition": {False, "BLOCKED"},
    "aidispositionauthority": {False, "BLOCKED", "AI_NOT_AUTHORITY"},
    "analystapproved": {False, "BLOCKED", "NOT_APPROVED"},
    "approvalstatus": {"NOT_APPROVED", "BLOCKED", "PENDING"},
    "finalauthorization": {False, "BLOCKED", "NOT_AUTHORIZED"},
    "caseclosed": {False},
    "casestatus": {"NOT_CLOSED"},
    "closurestatus": {"NOT_CLOSED", "BLOCKED"},
    "productionready": {False},
    "customerdeployed": {False},
    "socaasdeployed": {False},
}
PROMOTIONAL_VALUE_TOKENS = {
    "PUBLIC_SAFE",
    "RUNTIME_ACTIVE",
    "SIGNAL_OBSERVED",
    "PRODUCTION_READY",
    "CUSTOMER_DEPLOYED",
    "SOCAAS_DEPLOYED",
    "AI_APPROVED",
    "ANALYST_APPROVED",
    "FINAL_AUTHORIZED",
    "CASE_CLOSED",
}
ALLOWED_TOP_LEVEL_FIELDS = REQUIRED_TOP_LEVEL | {"purpose"}
ALLOWED_CURRENT_AUTHORITY_FIELDS = {
    "historical_snapshot",
    "current_authority",
    "source_path",
    "derivation_method",
    "derived_counts",
}
REQUIRED_CURRENT_AUTHORITY_FIELDS = ALLOWED_CURRENT_AUTHORITY_FIELDS
ALLOWED_DERIVED_COUNT_FIELDS = {
    "indexed_case_count",
    "proof_record_count",
    "proof_card_count",
    "missing_proof_record_count",
    "missing_proof_card_count",
    "public_safe_count",
}
ALLOWED_CLAIM_BOUNDARY_FIELDS = {"allowed_status_values", "blocked_claims"}
ALLOWED_ENTRY_FIELDS = REQUIRED_ENTRY_FIELDS | {
    "candidate_review_packet_path",
    "review_lane",
    "review_type",
    "candidate_review_state",
    "runtime_truth_spine",
}
ALLOWED_CANDIDATE_REVIEW_FIELDS = {
    "public_safe_status",
    "runtime_active",
    "signal_observed",
    "human_review_required",
    "privacy_review",
    "stale_review",
    "evidence_linkage_review",
    "wording_approval",
    "proof_ceiling",
    "case_status",
    "claim_authority",
}


def normalized_field_name(value: Any) -> str:
    decoded = str(value)
    for _ in range(4):
        next_value = unquote(decoded)
        if next_value == decoded:
            break
        decoded = next_value
    normalized = unicodedata.normalize("NFKC", decoded).casefold()
    return re.sub(r"[^a-z0-9]", "", normalized)


def compositional_promotion_key(key: str) -> bool:
    return (
        ("production" in key and any(part in key for part in ("active", "live", "ready", "deploy", "state", "status")))
        or (any(part in key for part in ("customer", "socaas")) and any(part in key for part in ("active", "deploy", "state", "status")))
        or ("runtime" in key and any(part in key for part in ("active", "state", "status")))
        or ("signal" in key and any(part in key for part in ("observed", "state", "status")))
        or ("publicsafe" in key and "count" not in key)
        or ("final" in key and any(part in key for part in ("authoriz", "authority")))
        or ("case" in key and "count" not in key and any(part in key for part in ("closed", "closure", "state", "status")))
        or any(part in key for part in ("approvalstate", "approvalstatus", "closurestatus", "casestate", "casestatus"))
        or (
            key.startswith(("ai", "analyst"))
            and any(part in key for part in ("approved", "approval", "authority", "disposition"))
        )
        or ("review" in key and "disposition" in key)
    )


def explicitly_bounded_authority_value(value: Any) -> bool:
    if isinstance(value, list) and len(value) == 1:
        return explicitly_bounded_authority_value(value[0])
    if value is False or value is None or value == 0:
        return True
    if not isinstance(value, str):
        return False
    return normalized_field_name(value) in {
        "blocked",
        "false",
        "humanreviewrequired",
        "missing",
        "none",
        "notapproved",
        "notauthorized",
        "notclosed",
        "notproven",
        "notpublicsafe",
        "notruntimeactive",
        "open",
        "partial",
        "pending",
        "existingflowcandidate",
        "privateruntimeboundarycontextonly",
        "privateruntimeevidencecaptured",
        "privateruntimeevidencecapturedlocalwindowsonly",
        "publicruntimeblocked",
        "runtimeactiveprivate",
        "runtimeblocked",
        "runtimeevidenceverifiedprivate",
        "signalblocked",
        "signalobservedprivate",
        "sourceexists",
        "unsupported",
    }


EXACT_BOUNDED_AUTHORITY_PROSE = {
    (
        "This bridge does not prove runtime, signal, production, customer deployment, "
        "SOCaaS deployment, public-safe runtime proof, AI approval, analyst approval, "
        "final authorization, or case closure. It keeps Hoxline and website material as "
        "reviewer routing only; proof authority remains in source-owned proof records and "
        "verifier-backed validation artifacts."
    ).casefold(),
}


def validate_authority_prose(value: str, label: str) -> None:
    normalized = normalize_authority_security_text(value).replace("\r", "\n")
    normalized_label = unicodedata.normalize("NFKC", label).casefold()
    if (
        re.search(r"(?:^|\.)blocked_claims\[\d+\]$", normalized_label)
        and normalized.strip().casefold() in EXACT_BLOCKED_CLAIM_VALUES
    ):
        return
    if normalized.strip().casefold() in EXACT_BOUNDED_AUTHORITY_PROSE:
        return
    for segment in re.split(
        r"[;:/\n—–]+|\b(?:but|however|although|yet|while|whereas)\b|(?<=[.!?])\s+",
        normalized,
        flags=re.IGNORECASE,
    ):
        if not segment.strip():
            continue
        intro = NEGATIVE_LIST_INTRO_RE.search(segment)
        suffix = NEGATIVE_LIST_SUFFIX_RE.search(segment)
        if suffix:
            if AFFIRMATIVE_STATE_AFTER_NEGATIVE_LIST_RE.search(
                segment[:suffix.start()]
            ):
                raise VerificationError(
                    f"{label} contains an unauthorized affirmative authority claim"
                )
            continue
        if intro:
            if (
                AFFIRMATIVE_STATE_AFTER_NEGATIVE_LIST_RE.search(
                    segment[intro.end():]
                )
            ):
                raise VerificationError(
                    f"{label} contains an unauthorized affirmative authority claim"
                )
            continue
        clauses = segment.split(",")
        if any(
            contains_unnegated_affirmative_state(clause)
            or (
                AFFIRMATIVE_AUTHORITY_CLAIM_RE.search(clause)
                and not LOCAL_NEGATION_RE.search(clause)
            )
            for clause in clauses
            if clause.strip()
        ):
            raise VerificationError(f"{label} contains an unauthorized affirmative authority claim")


def validate_recursive_authority_boundaries(
    value: Any,
    label: str = "proof status index",
    normalized_path: tuple[str, ...] = (),
    promotion_context: bool = False,
) -> None:
    """Reject authority promotion even when hidden in nested extension objects or arrays."""
    if isinstance(value, dict):
        normalized_keys: dict[str, Any] = {}
        for key, child in value.items():
            child_label = f"{label}.{key}"
            normalized = normalized_field_name(key)
            child_normalized_path = (*normalized_path, normalized)
            cumulative_keys = {normalized}
            cumulative_keys.update(
                f"{segment}{normalized}"
                for segment in normalized_path
                if segment
                in {
                    "runtime",
                    "signal",
                    "public",
                    "approval",
                    "production",
                    "customer",
                    "socaas",
                    "ai",
                    "analyst",
                    "review",
                    "final",
                    "case",
                }
            )
            if normalized in normalized_keys:
                raise VerificationError(
                    f"{label} contains normalized key collision: "
                    f"{normalized_keys[normalized]!r} and {key!r}"
                )
            normalized_keys[normalized] = key
            child_promotion_context = promotion_context or any(
                compositional_promotion_key(candidate)
                for candidate in cumulative_keys
            )
            policy = PROMOTION_KEY_POLICIES.get(normalized)
            if policy is not None and not isinstance(child, (dict, list)):
                try:
                    allowed = child in policy
                except TypeError:
                    allowed = False
                if not allowed:
                    raise VerificationError(
                        f"{child_label} contains unauthorized authority value: {child!r}"
                    )
            elif (
                not isinstance(child, (dict, list))
                and child_promotion_context
                and not explicitly_bounded_authority_value(child)
            ):
                raise VerificationError(
                    f"{child_label} contains compositional authority promotion: {child!r}"
                )
            validate_recursive_authority_boundaries(
                child,
                child_label,
                child_normalized_path,
                child_promotion_context,
            )
    elif isinstance(value, list):
        for index, child in enumerate(value):
            validate_recursive_authority_boundaries(
                child,
                f"{label}[{index}]",
                normalized_path,
                promotion_context,
            )
    elif promotion_context and not explicitly_bounded_authority_value(value):
        raise VerificationError(
            f"{label} contains compositional authority promotion: {value!r}"
        )
    elif isinstance(value, str):
        normalized_value = unicodedata.normalize("NFKC", value)
        if normalized_value.strip().upper() in PROMOTIONAL_VALUE_TOKENS:
            raise VerificationError(f"{label} contains unauthorized promotion token: {value!r}")
        validate_authority_prose(normalized_value, label)


def owned_path_key(value: str) -> str:
    """Normalize aliases with the case-insensitive semantics of the governed Windows workspace."""
    return "/".join(part.casefold() for part in PurePosixPath(value).parts)


def _clean_markdown_key(value: str) -> str:
    cleaned = value.strip()
    while (
        (cleaned.startswith("**") and cleaned.endswith("**"))
        or (cleaned.startswith("__") and cleaned.endswith("__"))
        or (cleaned.startswith("`") and cleaned.endswith("`"))
    ):
        cleaned = cleaned[2:-2] if cleaned[:2] in {"**", "__"} else cleaned[1:-1]
        cleaned = cleaned.strip()
    return cleaned.rstrip(":").strip()


def markdown_metadata_pairs(text: str) -> list[tuple[int, str, str]]:
    pairs: list[tuple[int, str, str]] = []
    for line_number, original in enumerate(text.splitlines(), 1):
        line = unicodedata.normalize("NFKC", original).strip()
        while line.startswith(">"):
            line = line[1:].lstrip()
        if line.startswith("|"):
            cells = [cell.strip() for cell in line.strip("|").split("|")]
            if len(cells) >= 2 and cells[0] and cells[1] and not set(cells[0]) <= {"-", ":"}:
                pairs.append((line_number, _clean_markdown_key(cells[0]), cells[1]))
            continue
        line = re.sub(r"^[-*+]\s+", "", line)
        formatted = re.match(r"^(?P<mark>\*\*|__|`)(?P<key>.+?)(?P=mark)\s*:?\s*(?P<value>.+?)\s*$", line)
        if formatted is not None:
            pairs.append(
                (
                    line_number,
                    _clean_markdown_key(formatted.group("key")),
                    formatted.group("value").strip(),
                )
            )
            continue
        plain = re.match(r"^([A-Za-z][A-Za-z0-9 _.-]*)\s*:\s*(.+?)\s*$", line)
        if plain is not None:
            pairs.append((line_number, _clean_markdown_key(plain.group(1)), plain.group(2).strip()))
    return pairs


def metadata_values(text: str, scalar_names: tuple[str, ...], table_names: tuple[str, ...] = ()) -> list[str]:
    expected = {normalized_field_name(name) for name in (*scalar_names, *table_names)}
    return [
        raw.strip().rstrip(".")
        for _, key, raw in markdown_metadata_pairs(text)
        if normalized_field_name(key) in expected
    ]


def unique_metadata_value(
    text: str,
    scalar_names: tuple[str, ...],
    table_names: tuple[str, ...],
    *,
    label: str,
    required: bool,
) -> str | None:
    values = metadata_values(text, scalar_names, table_names)
    normalized = {value.strip("` ").rstrip(".") for value in values}
    if not normalized:
        if required:
            raise VerificationError(f"{label} is missing")
        return None
    if len(normalized) != 1:
        raise VerificationError(f"{label} contains conflicting repeated metadata: {sorted(normalized)}")
    return next(iter(normalized))


def enum_metadata_value(
    text: str,
    scalar_names: tuple[str, ...],
    table_names: tuple[str, ...],
    *,
    label: str,
    allowed: set[str],
    required: bool,
) -> str | None:
    raw_values = metadata_values(text, scalar_names, table_names)
    parsed: list[str] = []
    for raw in raw_values:
        tokens = {
            token
            for token in allowed
            if re.search(rf"(?<![A-Z0-9_]){re.escape(token)}(?![A-Z0-9_])", raw.upper())
        }
        if len(tokens) != 1:
            raise VerificationError(f"{label} contains malformed or ambiguous metadata: {raw!r}")
        parsed.append(next(iter(tokens)))
    unique = set(parsed)
    if not unique:
        if required:
            raise VerificationError(f"{label} is missing")
        return None
    if len(unique) != 1:
        raise VerificationError(f"{label} contains conflicting repeated metadata: {sorted(unique)}")
    return next(iter(unique))


def _coerce_metadata_scalar(raw: str) -> Any:
    value = unicodedata.normalize("NFKC", raw).strip().strip("`").rstrip(".")
    if value.casefold() == "true":
        return True
    if value.casefold() == "false":
        return False
    return value


def validate_markdown_authority_metadata(text: str, label: str) -> None:
    """Apply recursive authority policies to scalar and inline structured Markdown metadata."""
    current_heading = ""
    table_headers: list[str] | None = None
    lines = text.splitlines()
    for line_number, line in enumerate(lines, 1):
        normalized_line = unicodedata.normalize("NFKC", line).strip()
        heading = re.match(r"^#{1,6}\s+(.+?)\s*$", normalized_line)
        if heading is not None:
            current_heading = normalized_field_name(heading.group(1))
            table_headers = None
        if normalized_line.startswith("|"):
            cells = [cell.strip() for cell in normalized_line.strip("|").split("|")]
            if all(cell and set(cell) <= {"-", ":"} for cell in cells):
                continue
            next_line = (
                unicodedata.normalize("NFKC", lines[line_number]).strip()
                if line_number < len(lines)
                else ""
            )
            next_cells = (
                [cell.strip() for cell in next_line.strip("|").split("|")]
                if next_line.startswith("|")
                else []
            )
            next_is_separator = bool(next_cells) and all(
                cell and set(cell) <= {"-", ":"} for cell in next_cells
            )
            if table_headers is None and next_is_separator:
                table_headers = [normalized_field_name(cell) for cell in cells]
                continue
            active_headers = table_headers or [
                f"column{cell_index + 1}" for cell_index in range(len(cells))
            ]
            truth_label = ""
            if "truthlabel" in active_headers:
                truth_index = active_headers.index("truthlabel")
                if truth_index < len(cells):
                    truth_label = normalized_field_name(cells[truth_index])
            for cell_index, cell in enumerate(cells):
                column = active_headers[cell_index] if cell_index < len(active_headers) else ""
                if column == "blockedwording":
                    continue
                if column == "claim" and truth_label == "blocked":
                    continue
                validate_authority_prose(
                    cell,
                    f"{label}:{line_number}.{column or f'column{cell_index + 1}'}",
                )
            continue
        if normalized_line:
            table_headers = None
        blocked_item = re.match(r"^[-*+]\s+(.+?)\s*$", normalized_line)
        if (
            blocked_item is not None
            and ("blockedclaims" in current_heading or "blockedwording" in current_heading)
            and (
                blocked_item.group(1).strip().casefold() in EXACT_BLOCKED_CLAIM_VALUES
                or re.fullmatch(r'["“].+["”]\.?', blocked_item.group(1).strip()) is not None
                or blocked_item.group(1).strip().casefold().startswith("blocked:")
            )
        ):
            continue
        validate_authority_prose(line, f"{label}:{line_number}")
    for line_number, key, raw in markdown_metadata_pairs(text):
        value = _coerce_metadata_scalar(raw)
        policy = PROMOTION_KEY_POLICIES.get(normalized_field_name(key))
        if policy is not None and value not in policy:
            raise VerificationError(
                f"{label}:{line_number} contains unauthorized {key} value: {raw!r}"
            )
        if (
            isinstance(value, str)
            and unicodedata.normalize("NFKC", value).strip().upper()
            in PROMOTIONAL_VALUE_TOKENS
        ):
            raise VerificationError(
                f"{label}:{line_number} contains unauthorized promotion token: {raw!r}"
            )
        stripped = raw.strip()
        if stripped.startswith(("{", "[")):
            try:
                nested = yaml.load(stripped, Loader=UniqueKeySafeLoader) if yaml is not None else None
            except yaml.YAMLError as exc:
                raise VerificationError(
                    f"{label}:{line_number} contains malformed structured metadata: {exc}"
                ) from exc
            validate_recursive_authority_boundaries(nested, f"{label}:{line_number}.{key}")


def validate_owned_artifact(
    entry: dict[str, Any], field: str, path_value: str, detection_id: str, *, is_card: bool
) -> None:
    text = (ROOT / path_value).read_text(encoding="utf-8")
    artifact_kind = "ProofCard" if is_card else "proof record"
    validate_markdown_authority_metadata(text, f"{detection_id} {artifact_kind}")
    heading = next((line.strip() for line in text.splitlines() if line.strip()), "")
    if re.fullmatch(rf"#\s+{re.escape(detection_id)}(?:\s+|\s*[-:—]\s*).+", heading, re.IGNORECASE) is None:
        raise VerificationError(f"{detection_id}.{field} heading does not exactly identify its owning case")
    declared_case_id = unique_metadata_value(
        text,
        ("case_id", "detection_id", "Detection ID", "Case ID"),
        ("Case ID", "Detection ID"),
        label=f"{detection_id} {artifact_kind} structured identity",
        required=True,
    )
    if declared_case_id != detection_id:
        raise VerificationError(
            f"{detection_id} {artifact_kind} structured identity mismatch: {declared_case_id}"
        )
    ceiling = enum_metadata_value(
        text,
        ("proof_ceiling", "Current proof level", "Proof packet status"),
        ("Current ceiling",),
        label=f"{detection_id} {artifact_kind} proof ceiling",
        allowed=ALLOWED_PROOF_CEILINGS,
        required=True,
    )
    expected_ceiling = entry["proof_ceiling"]
    if ceiling != expected_ceiling:
        raise VerificationError(
            f"{detection_id} {artifact_kind} ceiling mismatch: expected {expected_ceiling}, actual {ceiling}"
        )
    public_safe = enum_metadata_value(
        text,
        ("public_safe_status", "Public-safe status"),
        ("Public-safe status", "Public safe"),
        label=f"{detection_id} {artifact_kind} public-safe status",
        allowed={"NOT_PUBLIC_SAFE", "PUBLIC_SAFE"},
        required=True,
    )
    if public_safe != PUBLIC_SAFE_REQUIRED:
        raise VerificationError(
            f"{detection_id} {artifact_kind} public-safe status must remain {PUBLIC_SAFE_REQUIRED}"
        )
    if is_card and entry.get("proof_record_path") is not None:
        declared_record = unique_metadata_value(
            text,
            ("proof_record_path",),
            (),
            label=f"{detection_id} ProofCard proof_record_path",
            required=True,
        )
        if declared_record != entry["proof_record_path"]:
            raise VerificationError(
                f"{detection_id} ProofCard proof_record_path mismatch: expected {entry['proof_record_path']}, actual {declared_record}"
            )
    runtime_status = enum_metadata_value(
        text,
        ("runtime_status",),
        ("Runtime",),
        label=f"{detection_id} {artifact_kind} runtime status",
        allowed=ALLOWED_RUNTIME_STATUSES | {"RUNTIME_EVIDENCE_VERIFIED_PRIVATE", "CONTROLLED_LAB_RUNTIME_MATCH_VERIFIED"},
        required=True,
    )
    expected_runtime = entry["runtime_status"]
    if runtime_status != expected_runtime:
        raise VerificationError(
            f"{detection_id} {artifact_kind} runtime status mismatch: expected {expected_runtime}, actual {runtime_status}"
        )
    signal_status = enum_metadata_value(
        text,
        ("signal_status",),
        ("Signal",),
        label=f"{detection_id} {artifact_kind} signal status",
        allowed=ALLOWED_SIGNAL_STATUSES | {"BLOCKED"},
        required=True,
    )
    if signal_status != entry["signal_status"]:
        raise VerificationError(
            f"{detection_id} {artifact_kind} signal status mismatch: expected {entry['signal_status']}, actual {signal_status}"
        )


def derive_current_counts(entries: dict[str, dict[str, Any]]) -> dict[str, int]:
    records = [entry["proof_record_path"] for entry in entries.values() if entry.get("proof_record_path") is not None]
    cards = [entry["proof_card_path"] for entry in entries.values() if entry.get("proof_card_path") is not None]
    if len(records) != len({owned_path_key(value) for value in records}):
        raise VerificationError("proof_record_path must map to exactly one case")
    if len(cards) != len({owned_path_key(value) for value in cards}):
        raise VerificationError("proof_card_path must map to exactly one case")
    return {
        "indexed_case_count": len(entries),
        "proof_record_count": len(records),
        "proof_card_count": len(cards),
        "missing_proof_record_count": len(entries) - len(records),
        "missing_proof_card_count": len(entries) - len(cards),
        "public_safe_count": sum(
            1 for entry in entries.values() if entry.get("public_safe_status") != PUBLIC_SAFE_REQUIRED
        ),
    }


def validate_current_counts(index: dict[str, Any], entries: dict[str, dict[str, Any]]) -> dict[str, int]:
    derived = derive_current_counts(entries)
    current = require_mapping(index["current_authority"], "current_authority")
    declared = require_mapping(current.get("derived_counts"), "current_authority.derived_counts")
    if declared != derived:
        raise VerificationError(f"current proof counts drift: declared={declared}, derived={derived}")
    if derived["public_safe_count"] != 0:
        raise VerificationError("current proof index must derive public_safe_count=0")
    return derived


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


def require_ref_list(value: Any, label: str, minimum: int = 2) -> None:
    if not isinstance(value, list) or len(value) < minimum:
        raise VerificationError(f"{label} must include at least {minimum} references")
    for item in value:
        if not isinstance(item, str) or not item.strip():
            raise VerificationError(f"{label} entries must be non-empty strings")


def validate_ho_det_001_runtime_truth_spine(entry: dict[str, Any]) -> None:
    spine = entry.get("runtime_truth_spine")
    if not isinstance(spine, dict):
        raise VerificationError("HO-DET-001.runtime_truth_spine must be present")
    require_exact_keys(
        spine,
        REQUIRED_HO_DET_001_TRUTH_PLANES,
        REQUIRED_HO_DET_001_TRUTH_PLANES,
        "HO-DET-001.runtime_truth_spine",
    )

    source_truth = require_mapping(spine["source_truth"], "HO-DET-001.source_truth")
    require_exact_keys(source_truth, {"state", "owner", "refs"}, {"state", "owner", "refs"}, "HO-DET-001.source_truth")
    if source_truth.get("state") != "SOURCE_EXISTS":
        raise VerificationError("HO-DET-001.source_truth.state must be SOURCE_EXISTS")
    validation_truth = require_mapping(spine["validation_truth"], "HO-DET-001.validation_truth")
    require_exact_keys(validation_truth, {"state", "owner", "refs"}, {"state", "owner", "refs"}, "HO-DET-001.validation_truth")
    if validation_truth.get("state") != "CONTROLLED_TEST_VALIDATED":
        raise VerificationError("HO-DET-001.validation_truth.state must be CONTROLLED_TEST_VALIDATED")
    require_ref_list(source_truth.get("refs"), "HO-DET-001.source_truth.refs")
    require_ref_list(validation_truth.get("refs"), "HO-DET-001.validation_truth.refs")

    runtime_truth = require_mapping(spine["runtime_truth"], "HO-DET-001.runtime_truth")
    require_exact_keys(
        runtime_truth,
        {"state", "public_runtime_claim_status", "verified_runtime_evidence_refs"},
        {"state", "public_runtime_claim_status", "verified_runtime_evidence_refs"},
        "HO-DET-001.runtime_truth",
    )
    if runtime_truth.get("state") != "RUNTIME_EVIDENCE_VERIFIED_PRIVATE":
        raise VerificationError("HO-DET-001.runtime_truth.state must remain RUNTIME_EVIDENCE_VERIFIED_PRIVATE")
    if runtime_truth.get("public_runtime_claim_status") != "PUBLIC_RUNTIME_BLOCKED":
        raise VerificationError("HO-DET-001.runtime_truth.public_runtime_claim_status must remain PUBLIC_RUNTIME_BLOCKED")
    require_ref_list(runtime_truth.get("verified_runtime_evidence_refs"), "HO-DET-001.runtime_truth.verified_runtime_evidence_refs")

    signal_truth = require_mapping(spine["signal_truth"], "HO-DET-001.signal_truth")
    require_exact_keys(
        signal_truth,
        {"state", "public_signal_claim_status", "verified_signal_record_refs"},
        {"state", "public_signal_claim_status", "verified_signal_record_refs"},
        "HO-DET-001.signal_truth",
    )
    if signal_truth.get("state") != "SIGNAL_OBSERVED_PRIVATE":
        raise VerificationError("HO-DET-001.signal_truth.state must remain SIGNAL_OBSERVED_PRIVATE")
    if signal_truth.get("public_signal_claim_status") != "PUBLIC_RUNTIME_BLOCKED":
        raise VerificationError("HO-DET-001.signal_truth.public_signal_claim_status must remain PUBLIC_RUNTIME_BLOCKED")
    require_ref_list(signal_truth.get("verified_signal_record_refs"), "HO-DET-001.signal_truth.verified_signal_record_refs")

    evidence_truth = require_mapping(spine["evidence_truth"], "HO-DET-001.evidence_truth")
    require_exact_keys(
        evidence_truth,
        {"state", "raw_private_evidence_public_safe", "repo_contains_raw_private_evidence", "hash_only_private_refs"},
        {"state", "raw_private_evidence_public_safe", "repo_contains_raw_private_evidence", "hash_only_private_refs"},
        "HO-DET-001.evidence_truth",
    )
    if evidence_truth.get("state") != "RUNTIME_EVIDENCE_VERIFIED_PRIVATE":
        raise VerificationError("HO-DET-001.evidence_truth.state must remain RUNTIME_EVIDENCE_VERIFIED_PRIVATE")
    if evidence_truth.get("raw_private_evidence_public_safe") is not False:
        raise VerificationError("HO-DET-001.evidence_truth.raw_private_evidence_public_safe must remain false")
    if evidence_truth.get("repo_contains_raw_private_evidence") is not False:
        raise VerificationError("HO-DET-001.evidence_truth.repo_contains_raw_private_evidence must remain false")

    ai_truth = require_mapping(spine["ai_triage_truth"], "HO-DET-001.ai_triage_truth")
    require_exact_keys(
        ai_truth,
        {"support_state", "triage_output_state", "authority_state", "ai_decided_disposition", "human_review_required"},
        {"support_state", "triage_output_state", "authority_state", "ai_decided_disposition", "human_review_required"},
        "HO-DET-001.ai_triage_truth",
    )
    if ai_truth.get("support_state") != "AI_SUPPORT_ONLY":
        raise VerificationError("HO-DET-001.ai_triage_truth.support_state must remain AI_SUPPORT_ONLY")
    if ai_truth.get("triage_output_state") != "AI_TRIAGE_OUTPUT_PRIVATE":
        raise VerificationError("HO-DET-001.ai_triage_truth.triage_output_state must remain AI_TRIAGE_OUTPUT_PRIVATE")
    if ai_truth.get("authority_state") != "AI_NOT_AUTHORITY":
        raise VerificationError("HO-DET-001.ai_triage_truth.authority_state must remain AI_NOT_AUTHORITY")
    if ai_truth.get("ai_decided_disposition") is not False:
        raise VerificationError("HO-DET-001.ai_triage_truth.ai_decided_disposition must remain false")

    public_truth = require_mapping(spine["public_proof_truth"], "HO-DET-001.public_proof_truth")
    require_exact_keys(
        public_truth,
        {"state", "proof_ceiling", "public_safe_status"},
        {"state", "proof_ceiling", "public_safe_status"},
        "HO-DET-001.public_proof_truth",
    )
    if public_truth.get("state") != "PUBLIC_RUNTIME_BLOCKED":
        raise VerificationError("HO-DET-001.public_proof_truth.state must remain PUBLIC_RUNTIME_BLOCKED")
    if public_truth.get("proof_ceiling") != "CONTROLLED_TEST_VALIDATED":
        raise VerificationError("HO-DET-001.public_proof_truth.proof_ceiling must remain CONTROLLED_TEST_VALIDATED")
    if public_truth.get("public_safe_status") != PUBLIC_SAFE_REQUIRED:
        raise VerificationError("HO-DET-001.public_proof_truth.public_safe_status must remain NOT_PUBLIC_SAFE")

    human_truth = require_mapping(spine["human_review_truth"], "HO-DET-001.human_review_truth")
    require_exact_keys(
        human_truth,
        {"state", "public_runtime_summary_state", "approval_required_for_public_summary"},
        {"state", "public_runtime_summary_state", "approval_required_for_public_summary"},
        "HO-DET-001.human_review_truth",
    )
    if human_truth.get("public_runtime_summary_state") != "PUBLIC_RUNTIME_BLOCKED":
        raise VerificationError("HO-DET-001.human_review_truth.public_runtime_summary_state must remain PUBLIC_RUNTIME_BLOCKED")
    if human_truth.get("approval_required_for_public_summary") is not True:
        raise VerificationError("HO-DET-001.human_review_truth.approval_required_for_public_summary must remain true")


def validate_entry(
    entry: dict[str, Any],
    detections: dict[str, dict[str, Any]],
    validation: dict[str, dict[str, Any]],
) -> None:
    detection_hint = entry.get("detection_id", "<unknown>")
    require_exact_keys(
        entry,
        REQUIRED_ENTRY_FIELDS,
        ALLOWED_ENTRY_FIELDS,
        f"entry {detection_hint}",
    )

    detection_id = require_nonempty_string(entry["detection_id"], "detection_id")
    if entry.get("candidate_review_state") is not None:
        candidate = require_mapping(
            entry["candidate_review_state"],
            f"{detection_id}.candidate_review_state",
        )
        require_exact_keys(
            candidate,
            ALLOWED_CANDIDATE_REVIEW_FIELDS,
            ALLOWED_CANDIDATE_REVIEW_FIELDS,
            f"{detection_id}.candidate_review_state",
        )
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
    if record_path is not None:
        validate_owned_artifact(entry, "proof_record_path", record_path, detection_id, is_card=False)
    if card_path is not None:
        validate_owned_artifact(entry, "proof_card_path", card_path, detection_id, is_card=True)
    validate_proof_ceiling(entry, record_path, card_path, detection_id)
    validate_private_runtime_status(entry, record_path, detection_id)
    validate_claim_boundary_text(entry, detection_id)
    if detection_id == "HO-DET-001":
        validate_ho_det_001_runtime_truth_spine(entry)

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

    # This field is a bounded rendering observation, not proof authority.
    # Proof validates only its non-promotional vocabulary and deliberately
    # does not consume downstream platform code to establish proof truth.


CASE_ARTIFACT_NAME_RE = re.compile(r"^(?:HO-(?:DET|NDR)|AWS-DET|ID-DET)-\d{3}\.md$", re.IGNORECASE)
CASE_ID_RE = re.compile(r"(?:HO-(?:DET|NDR)|AWS-DET|ID-DET)-\d{3}", re.IGNORECASE)


def discover_case_artifacts(directory: Path, label: str) -> dict[str, str]:
    """Discover canonical and aliased case artifacts from content, not filenames alone."""
    discovered: dict[str, str] = {}
    identities: dict[str, str] = {}
    if not directory.is_dir():
        raise VerificationError(f"missing proof {label} directory: {rel(directory)}")
    expected_heading_kind = "proofcard" if label == "card" else "proof record"
    for path in sorted(directory.rglob("*")):
        if not path.is_file():
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError as exc:
            raise VerificationError(f"proof {label} file is not valid UTF-8: {rel(path)}") from exc
        heading = next((line.strip() for line in text.splitlines() if line.strip()), "")
        normalized_heading = unicodedata.normalize("NFKC", heading)
        heading_id_match = CASE_ID_RE.search(normalized_heading)
        heading_declares_kind = expected_heading_kind in normalized_heading.casefold()
        canonical_filename = CASE_ARTIFACT_NAME_RE.fullmatch(path.name) is not None
        raw_declared_ids = metadata_values(
            text,
            ("case_id", "detection_id", "Detection ID", "Case ID"),
            ("Case ID", "Detection ID"),
        )
        metadata_keys = {
            normalized_field_name(key) for _, key, _ in markdown_metadata_pairs(text)
        }
        structured_artifact = bool(raw_declared_ids) and {
            "proofceiling",
            "publicsafestatus",
        }.issubset(metadata_keys)
        if not canonical_filename and not (
            (heading_id_match is not None and heading_declares_kind)
            or structured_artifact
        ):
            continue

        # An aliased artifact is still authority-bearing content and must be
        # scanned before the reverse-inventory mismatch is reported.
        validate_markdown_authority_metadata(text, f"unindexed proof {label} {rel(path)}")
        declared_ids = {
            value.strip("` ").upper()
            for value in raw_declared_ids
            if CASE_ID_RE.fullmatch(value.strip("` "))
        }
        if heading_id_match is not None:
            declared_ids.add(heading_id_match.group(0).upper())
        filename_id = CASE_ID_RE.fullmatch(path.stem)
        if filename_id is not None:
            declared_ids.add(filename_id.group(0).upper())
        if len(declared_ids) != 1:
            raise VerificationError(
                f"proof {label} artifact identity is missing or contradictory: "
                f"{rel(path)} declares {sorted(declared_ids)}"
            )
        case_id = next(iter(declared_ids)).casefold()
        if case_id in identities:
            raise VerificationError(
                f"proof {label} artifact identity is owned by multiple files: "
                f"{identities[case_id]} and {rel(path)}"
            )
        identities[case_id] = rel(path)

        relative = rel(path)
        key = owned_path_key(relative)
        if key in discovered:
            raise VerificationError(
                f"duplicate normalized {label} path: {discovered[key]} and {relative}"
            )
        discovered[key] = relative
    return discovered


def verify_reverse_inventory(entries: dict[str, dict[str, Any]]) -> None:
    discovered_records = discover_case_artifacts(ROOT / "proof" / "records", "record")
    discovered_cards = discover_case_artifacts(ROOT / "proof" / "cards", "card")
    indexed_records = {
        owned_path_key(entry["proof_record_path"]): entry["proof_record_path"]
        for entry in entries.values()
        if entry.get("proof_record_path") is not None
    }
    indexed_cards = {
        owned_path_key(entry["proof_card_path"]): entry["proof_card_path"]
        for entry in entries.values()
        if entry.get("proof_card_path") is not None
    }
    orphan_records = sorted(set(discovered_records) - set(indexed_records))
    missing_records = sorted(set(indexed_records) - set(discovered_records))
    orphan_cards = sorted(set(discovered_cards) - set(indexed_cards))
    missing_cards = sorted(set(indexed_cards) - set(discovered_cards))
    if orphan_records:
        raise VerificationError(
            f"proof record reverse inventory contains unindexed case artifacts: "
            f"{[discovered_records[key] for key in orphan_records]}"
        )
    if missing_records:
        raise VerificationError(
            f"proof record reverse inventory is missing indexed artifacts: "
            f"{[indexed_records[key] for key in missing_records]}"
        )
    if orphan_cards:
        raise VerificationError(
            f"ProofCard reverse inventory contains unindexed case artifacts: "
            f"{[discovered_cards[key] for key in orphan_cards]}"
        )
    if missing_cards:
        raise VerificationError(
            f"ProofCard reverse inventory is missing indexed artifacts: "
            f"{[indexed_cards[key] for key in missing_cards]}"
        )

    ndr = entries.get("HO-NDR-001")
    if ndr is None:
        raise VerificationError("HO-NDR-001 must remain explicitly indexed")
    if ndr.get("proof_record_path") is not None:
        raise VerificationError("HO-NDR-001 must remain card-only unless separately approved proof authority exists")
    if ndr.get("proof_card_path") != "proof/cards/HO-NDR-001.md":
        raise VerificationError("HO-NDR-001 must retain its owned boundary card")


def verify_index(index_path: Path = INDEX_PATH) -> list[dict[str, Any]]:
    index = require_mapping(load_yaml(index_path, "proof status index"), "proof status index")
    validate_recursive_authority_boundaries(index)
    validate_top_level(index)
    entries = normalize_entries_by_id(index, "proof status index")
    detections = load_detection_matrix()
    validation = load_validation_registry()
    derive_current_counts(entries)
    for entry in entries.values():
        validate_entry(entry, detections, validation)
    verify_reverse_inventory(entries)
    validate_current_counts(index, entries)
    return list(entries.values())


def main() -> int:
    try:
        entries = verify_index()
    except VerificationError as exc:
        fail(str(exc))
    print("Detection proof status index verification passed.")
    counts = derive_current_counts({entry["detection_id"]: entry for entry in entries})
    print(
        "CURRENT_PROOF_COUNTS | "
        + " | ".join(f"{field}={value}" for field, value in counts.items())
    )
    print("DETECTION_ID | PROOF_CEILING | RUNTIME_STATUS | SIGNAL_STATUS | PUBLIC_SAFE_STATUS")
    for entry in entries:
        print(
            f"{entry['detection_id']} | {entry['proof_ceiling']} | {entry['runtime_status']} | "
            f"{entry['signal_status']} | {entry['public_safe_status']}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
