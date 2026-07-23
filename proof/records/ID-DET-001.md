# ID-DET-001 Proof Record
detection_id: ID-DET-001

## 1. Summary

proof_ceiling: CONTROLLED_TEST_VALIDATED
source_status: SOURCE_EXISTS
validation_status: CONTROLLED_TEST_VALIDATED
runtime_status: NOT_PROVEN
signal_status: NOT_PROVEN
public_safe_status: NOT_PUBLIC_SAFE
case_status: NOT_CLOSED
human_review_required: true
website_status: WEBSITE_RENDERING_NOT_PROOF
green_ci_status: GREEN_CI_NOT_APPROVAL

This record backfills proof authority for ID-DET-001 from repo-visible source and controlled validation evidence only.

## 2. Truth Surface

The authoritative surfaces for this record are the identity detection package in hawkinsoperations-detections, controlled validation artifacts in hawkinsoperations-validation, and this proof record plus the proof status index in hawkinsoperations-proof.

Platform identity-lane references are runtime-candidate context only. They are not public runtime proof.

## 3. Source Truth

ID-DET-001 has source truth in the detections repo. The identity detection package identifies the case as repo-visible source evidence.

## 4. Validation Truth

ID-DET-001 has controlled validation evidence in the validation repo. This record treats that evidence as controlled-test validation only.

## 5. Runtime Truth

runtime_status: NOT_PROVEN

Platform identity-lane context does not prove live IdP or public runtime status.

## 6. Signal Truth

signal_status: NOT_PROVEN

This record does not prove signal-observed public status.

## 7. Evidence Truth

Evidence is limited to source-controlled files. No private evidence, raw runtime logs, raw endpoint telemetry, or raw alert material is used.

## 8. Public Proof Truth

public_safe_status: NOT_PUBLIC_SAFE

This record is not a public-safe approval and does not authorize public proof wording.

## 9. Claim Authority

The proof repo may record the existence of this proof record and its controlled-test proof ceiling. It may not promote runtime, signal, customer, production, approval, or closure status.

## 10. Blocked Claims

- runtime-active public proof
- signal-observed public proof
- public-safe proof
- production-ready
- customer deployment
- SOCaaS deployment
- autonomous SOC
- live IdP proof
- live SIEM proof
- AI-approved disposition
- analyst-approved disposition
- final authorization
- case closure
- website rendering as proof
- GitHub rendering as proof
- green CI as approval

## 11. Evidence References

- hawkinsoperations-detections/detections/identity/id-det-001/rule.yml
- hawkinsoperations-detections/detections/identity/id-det-001/event-mapping.yml
- hawkinsoperations-detections/detections/identity/id-det-001/status.yml
- hawkinsoperations-validation/reports/id-det-001/validation-result.json
- hawkinsoperations-validation/reports/id-det-001/validation-result.md
- hawkinsoperations-validation/scripts/validate-id-det-001.py
- hawkinsoperations-validation/scripts/verify-id-det-001-result-parity.py
- hawkinsoperations-platform/scripts/ho_factory.py

## 12. What This Record Proves

- A proof record exists for ID-DET-001.
- Repo-visible source truth exists.
- Controlled validation evidence exists.
- The proof ceiling is CONTROLLED_TEST_VALIDATED.
- Public-safe and closed-case status remain blocked.

## 13. What This Record Does Not Prove

This record does not prove runtime-active public operation, signal-observed public evidence, public-safe runtime status, customer deployment, production readiness, autonomous SOC, SOCaaS deployment, AI approval, analyst approval, final authorization, case closure, product-market fit, or customer adoption.

## 14. Next Gate

Reviewer validates source and controlled-test validation before any separately approved identity runtime gate.

## 15. Human Review Requirement

Human review is required before this case can move beyond the controlled-test proof ceiling.
