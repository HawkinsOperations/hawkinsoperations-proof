# ID-DET-002 ProofCard

## 1. Card Summary

proofcard_version: proofcard-backfill-v0
case_id: ID-DET-002
proof_record_path: proof/records/ID-DET-002.md
proof_ceiling: CONTROLLED_TEST_VALIDATED
source_status: SOURCE_EXISTS
validation_status: CONTROLLED_TEST_VALIDATED
runtime_status: NOT_PROVEN
signal_status: NOT_PROVEN
public_safe_status: NOT_PUBLIC_SAFE
case_status: NOT_CLOSED
human_review_required: true
website_status: WEBSITE_RENDERING_NOT_PROOF
github_status: GITHUB_RENDERING_NOT_PROOF
green_ci_status: GREEN_CI_NOT_APPROVAL
card_status: INTERNAL_REVIEW_CARD_NOT_PUBLIC_SAFE

This card summarizes the existing ID-DET-002 proof record. It does not raise the proof ceiling.

## 2. Current Authority

The proof record and proof status index are the authority for this card. Identity-lane platform context remains non-promotional.

## 3. Proof Ceiling

CONTROLLED_TEST_VALIDATED

## 4. Truth State

| Plane | Status |
|---|---|
| Source | SOURCE_EXISTS |
| Validation | CONTROLLED_TEST_VALIDATED |
| Runtime | NOT_PROVEN |
| Signal | NOT_PROVEN |
| Public safe | NOT_PUBLIC_SAFE |
| Case | NOT_CLOSED |

## 5. Evidence References

- proof/records/ID-DET-002.md
- hawkinsoperations-detections/detections/identity/id-det-002/rule.yml
- hawkinsoperations-detections/detections/identity/id-det-002/event-mapping.yml
- hawkinsoperations-detections/detections/identity/id-det-002/status.yml
- hawkinsoperations-validation/reports/id-det-002/validation-result.json
- hawkinsoperations-validation/reports/id-det-002/validation-result.md
- hawkinsoperations-validation/scripts/validate-id-det-002.py
- hawkinsoperations-validation/scripts/verify-id-det-002-result-parity.py
- hawkinsoperations-platform/scripts/ho_factory.py

## 6. Allowed Claims

- ProofCard exists for ID-DET-002.
- Proof record exists for ID-DET-002.
- Source evidence is repo-visible.
- Controlled validation evidence exists.
- Current proof ceiling is CONTROLLED_TEST_VALIDATED.
- Human review is required for any promotion.

## 7. Blocked Claims

- runtime-active public proof
- signal-observed public proof
- public_safe proof
- public_safe runtime proof
- production-ready
- customer deployment
- SOCaaS deployment
- autonomous SOC
- live IdP proof
- AI-approved disposition
- analyst-approved disposition
- final authorization
- case closure
- website rendering as proof
- GitHub rendering as proof
- green CI as approval
- product-market fit
- customer adoption

## 8. Non-Proof Surfaces

Website rendering, GitHub rendering, and green CI are non-proof surfaces for this card.

## 9. Human Review Requirement

Human review is required before any runtime, signal, public_safe, customer, production, approval, or closure wording changes.

## 10. Next Gate

Reviewer validates source and controlled-test validation before any separately approved identity runtime gate.
