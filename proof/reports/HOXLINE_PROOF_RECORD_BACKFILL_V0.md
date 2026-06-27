# Hoxline Proof Record Backfill v0

generated_at: 2026-06-27T06:01:49-05:00
input_case_growth_index_path: C:\Raylee\Repo\HawkinsOperations\hoxline\examples\case-growth\current-case-growth-index.json
proof_ceiling: PROOF_RECORD_BACKFILL_CONTROLLED_REPO_EVIDENCE_ONLY

## Objective

Backfill proof records for eligible repo-supported cases identified by Hoxline Case Growth Index v0 without promoting runtime, signal, customer, production, public_safe, approval, or closed-case status.

## Counts

| Metric | Count |
|---|---:|
| cases_total | 27 |
| proof_records_before | 4 |
| missing_proof_records_before | 23 |
| proof_records_created | 7 |
| proof_records_after_estimated | 11 |
| missing_proof_records_after_estimated | 16 |
| public_safe_cases_created | 0 |
| closed_cases_created | 0 |
| runtime_proof_created | 0 |
| signal_proof_created | 0 |
| production_claims_created | 0 |
| customer_claims_created | 0 |
| approval_claims_created | 0 |

## Created Records

| Case | Proof Record | Proof Ceiling | Public Safe | Case Status |
|---|---|---|---|---|
| HO-DET-009 | proof/records/HO-DET-009.md | CONTROLLED_TEST_VALIDATED | NOT_PUBLIC_SAFE | NOT_CLOSED |
| HO-DET-010 | proof/records/HO-DET-010.md | CONTROLLED_TEST_VALIDATED | NOT_PUBLIC_SAFE | NOT_CLOSED |
| HO-DET-013 | proof/records/HO-DET-013.md | CONTROLLED_TEST_VALIDATED | NOT_PUBLIC_SAFE | NOT_CLOSED |
| ID-DET-001 | proof/records/ID-DET-001.md | CONTROLLED_TEST_VALIDATED | NOT_PUBLIC_SAFE | NOT_CLOSED |
| ID-DET-002 | proof/records/ID-DET-002.md | CONTROLLED_TEST_VALIDATED | NOT_PUBLIC_SAFE | NOT_CLOSED |
| ID-DET-003 | proof/records/ID-DET-003.md | CONTROLLED_TEST_VALIDATED | NOT_PUBLIC_SAFE | NOT_CLOSED |
| ID-DET-004 | proof/records/ID-DET-004.md | CONTROLLED_TEST_VALIDATED | NOT_PUBLIC_SAFE | NOT_CLOSED |

## Deferred Cases

| Case | Reason |
|---|---|
| HO-DET-002 | Source-only or planned successor case without controlled validation evidence in the Case Growth Index. |
| HO-DET-003 | Source-only or planned successor case without controlled validation evidence in the Case Growth Index. |
| HO-DET-004 | Source-only or planned successor case without controlled validation evidence in the Case Growth Index. |
| HO-DET-005 | Source-only or planned successor case without controlled validation evidence in the Case Growth Index. |
| HO-DET-006 | Source-only or planned successor case without controlled validation evidence in the Case Growth Index. |
| HO-DET-007 | Source-only or planned successor case without controlled validation evidence in the Case Growth Index. |
| HO-DET-008 | Source-only or planned successor case without controlled validation evidence in the Case Growth Index. |
| HO-DET-014 | Source-only or planned successor case without controlled validation evidence in the Case Growth Index. |
| HO-DET-015 | Source-only or planned successor case without controlled validation evidence in the Case Growth Index. |
| HO-DET-016 | Source-only or planned successor case without controlled validation evidence in the Case Growth Index. |
| HO-NDR-001 | External boundary and cross-source contract scope with existing ProofCard; proof-record backfill requires separate proof scope. |
| HO-NDR-002 | External boundary or source-only NDR scope requires separate proof ownership review. |
| HO-PIPE-001 | Pipeline telemetry contract case requires separate contract proof scope. |
| HOD-001 | Legacy or archival case requires separate archival review. |
| HOX-GAUNTLET-001 | Product-demo case belongs in Hoxline product proof rather than detection proof-record backfill. |

## Blocked Cases

| Case | Reason |
|---|---|
| HO-DET-999 | No source truth or controlled validation evidence supports a proof record; creating one would imply unsupported proof. |

## Proof Index Update

Updated: proof/indexes/DETECTION_PROOF_STATUS_INDEX.yml

The index now references the seven created proof records and preserves:

- public_safe_status: NOT_PUBLIC_SAFE
- case_status: NOT_CLOSED in the records
- runtime_status: NOT_PROVEN
- signal_status: NOT_PROVEN
- website_status: WEBSITE_UNTOUCHED_NOT_PROOF
- green CI as non-approval boundary in the records

## What This Backfill Proves

- The seven listed proof records exist.
- The created records are bounded to repo-visible source and controlled validation evidence.
- The proof ceiling for created records is CONTROLLED_TEST_VALIDATED.
- Deferred and blocked cases are explicitly listed instead of promoted.

## What This Backfill Does Not Prove

This backfill does not prove runtime-active public operation, signal-observed public evidence, public_safe runtime status, customer deployment, production readiness, autonomous SOC, SOCaaS deployment, AI approval, analyst approval, final authorization, case closure, product-market fit, customer adoption, website rendering as proof, GitHub rendering as proof, or green CI as approval.

## Next Gate

Reviewer should inspect the created proof records, the proof status index update, and the deferred/blocked case list before any proofcard backfill, public-safe candidate review, or private runtime gate.
