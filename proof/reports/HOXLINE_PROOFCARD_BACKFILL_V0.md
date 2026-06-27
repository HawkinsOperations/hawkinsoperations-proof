# Hoxline ProofCard Backfill v0

generated_at: 2026-06-27T07:28:23-05:00
input_proof_index_path: proof/indexes/DETECTION_PROOF_STATUS_INDEX.yml
input_proof_record_backfill_report_path: proof/reports/hoxline-proof-record-backfill-v0.json
input_case_growth_index_path: C:\Raylee\Repo\HawkinsOperations\hoxline\examples\case-growth\current-case-growth-index.json
proof_ceiling: PROOFCARD_BACKFILL_CONTROLLED_REPO_EVIDENCE_ONLY

## Objective

Backfill ProofCards for eligible existing proof records without promoting runtime, signal, customer, production, public_safe, approval, closure, product-market-fit, or customer-adoption claims.

## Counts

| Metric | Count |
|---|---:|
| proof_records_total_indexed | 11 |
| proofcards_before | 3 |
| proofcards_missing_before | 8 |
| proofcards_created | 8 |
| proofcards_after_estimated | 11 |
| proofcards_missing_after_estimated | 0 |
| public_safe_cases_created | 0 |
| closed_cases_created | 0 |
| runtime_proof_created | 0 |
| signal_proof_created | 0 |
| production_claims_created | 0 |
| customer_claims_created | 0 |
| approval_claims_created | 0 |

## Created ProofCards

| Case | Proof Record | ProofCard | Proof Ceiling | Public Safe | Case Status |
|---|---|---|---|---|---|
| HO-DET-009 | proof/records/HO-DET-009.md | proof/cards/HO-DET-009.md | CONTROLLED_TEST_VALIDATED | NOT_PUBLIC_SAFE | NOT_CLOSED |
| HO-DET-010 | proof/records/HO-DET-010.md | proof/cards/HO-DET-010.md | CONTROLLED_TEST_VALIDATED | NOT_PUBLIC_SAFE | NOT_CLOSED |
| HO-DET-011 | proof/records/HO-DET-011.md | proof/cards/HO-DET-011.md | PRIVATE_RUNTIME_EVIDENCE_CAPTURED | NOT_PUBLIC_SAFE | NOT_CLOSED |
| HO-DET-013 | proof/records/HO-DET-013.md | proof/cards/HO-DET-013.md | CONTROLLED_TEST_VALIDATED | NOT_PUBLIC_SAFE | NOT_CLOSED |
| ID-DET-001 | proof/records/ID-DET-001.md | proof/cards/ID-DET-001.md | CONTROLLED_TEST_VALIDATED | NOT_PUBLIC_SAFE | NOT_CLOSED |
| ID-DET-002 | proof/records/ID-DET-002.md | proof/cards/ID-DET-002.md | CONTROLLED_TEST_VALIDATED | NOT_PUBLIC_SAFE | NOT_CLOSED |
| ID-DET-003 | proof/records/ID-DET-003.md | proof/cards/ID-DET-003.md | CONTROLLED_TEST_VALIDATED | NOT_PUBLIC_SAFE | NOT_CLOSED |
| ID-DET-004 | proof/records/ID-DET-004.md | proof/cards/ID-DET-004.md | CONTROLLED_TEST_VALIDATED | NOT_PUBLIC_SAFE | NOT_CLOSED |

## Deferred Cases

None. Every indexed proof record with a missing ProofCard was eligible for an internal review card.

## Blocked Cases

None.

## Proof Index Update

Updated: proof/indexes/DETECTION_PROOF_STATUS_INDEX.yml

The index now references the eight created ProofCards while preserving:

- proof_record_path for every case
- proof_ceiling for every case
- public_safe_status: NOT_PUBLIC_SAFE
- runtime_status and signal_status from the proof index
- blocked claims and next gates

## What This Backfill Proves

- ProofCards exist for the eight listed existing proof records.
- The created cards summarize proof-record and proof-index authority.
- The created cards keep public_safe blocked.
- The created cards keep human review required for any promotion.

## What This Backfill Does Not Prove

This backfill does not prove runtime-active public operation, signal-observed public evidence, public_safe runtime status, customer deployment, production readiness, autonomous SOC, SOCaaS deployment, AI approval, analyst approval, final authorization, case closure, product-market fit, customer adoption, website rendering as proof, GitHub rendering as proof, or green CI as approval.

## Next Gate

Reviewer should inspect the ProofCards and proof index updates before any public-safe candidate review packet. The next likely build is a public-safe candidate review packet only after human approval and proof-boundary review.
