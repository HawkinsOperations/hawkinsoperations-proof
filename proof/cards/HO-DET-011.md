# HO-DET-011 ProofCard

## 1. Card Summary

proofcard_version: proofcard-backfill-v0
case_id: HO-DET-011
proof_record_path: proof/records/HO-DET-011.md
proof_ceiling: PRIVATE_RUNTIME_EVIDENCE_CAPTURED
source_status: SOURCE_EXISTS
validation_status: CONTROLLED_TEST_VALIDATED
runtime_status: PRIVATE_RUNTIME_EVIDENCE_CAPTURED
signal_status: NOT_PROVEN
public_safe_status: NOT_PUBLIC_SAFE
case_status: NOT_CLOSED
human_review_required: true
website_status: WEBSITE_RENDERING_NOT_PROOF
github_status: GITHUB_RENDERING_NOT_PROOF
green_ci_status: GREEN_CI_NOT_APPROVAL
card_status: INTERNAL_REVIEW_CARD_NOT_PUBLIC_SAFE

This card summarizes the existing HO-DET-011 proof record. Private runtime evidence capture remains non-public and does not create public runtime proof.

## 2. Current Authority

The proof record and proof status index are the authority for this card. The private runtime status is bounded to the proof record; this card does not expose or rely on raw private evidence.

## 3. Proof Ceiling

PRIVATE_RUNTIME_EVIDENCE_CAPTURED

## 4. Truth State

| Plane | Status |
|---|---|
| Source | SOURCE_EXISTS |
| Validation | CONTROLLED_TEST_VALIDATED |
| Runtime | PRIVATE_RUNTIME_EVIDENCE_CAPTURED |
| Signal | NOT_PROVEN |
| Public safe | NOT_PUBLIC_SAFE |
| Case | NOT_CLOSED |

## 5. Evidence References

- proof/records/HO-DET-011.md
- hawkinsoperations-detections/detections/successor/ho-det-011/rule.yml
- hawkinsoperations-detections/detections/successor/ho-det-011/event-mapping.yml
- hawkinsoperations-detections/detections/successor/ho-det-011/status.yml
- hawkinsoperations-validation/reports/ho-det-011/validation-result.json
- hawkinsoperations-validation/reports/ho-det-011/validation-result.md
- hawkinsoperations-validation/scripts/validate-ho-det-011.py
- hawkinsoperations-validation/scripts/verify-ho-det-011-result-parity.py
- hawkinsoperations-platform/contracts/examples/ho-det-011-case-packet.sample.json
- hawkinsoperations-platform/scripts/verify-ho-det-011-case-packet.py

## 6. Allowed Claims

- ProofCard exists for HO-DET-011.
- Proof record exists for HO-DET-011.
- Source evidence is repo-visible.
- Controlled validation evidence exists.
- Current proof ceiling is PRIVATE_RUNTIME_EVIDENCE_CAPTURED.
- Private runtime evidence capture is recorded in the proof record as non-public proof context.
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
- live SIEM proof
- live Splunk proof
- live Wazuh proof
- live Cribl proof
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

Website rendering, GitHub rendering, and green CI are non-proof surfaces for this card. This card does not publish raw private evidence.

## 9. Human Review Requirement

Human review is required before any public runtime, signal, public_safe, customer, production, approval, or closure wording changes.

## 10. Next Gate

Separate event-specific Wazuh, Splunk, or Cribl correlation review before any routed-telemetry wording can advance.
