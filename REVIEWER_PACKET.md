# Boundary: HO-DET-001 SOCaaS-Fit Pilot Receipt Loop

## Packet Identity

| Field | Value |
|---|---|
| Packet title | HO-DET-001 SOCaaS-Fit Pilot Receipt Loop boundary packet |
| Pack ID | HAWKINSOPERATIONS_PROOF_PACK_001 |
| Detection ID | HO-DET-001 |
| Detection title | Suspicious PowerShell EncodedCommand Execution via Sysmon Event ID 1 |
| Ceiling | CONTROLLED_TEST_VALIDATED |
| Reviewer package status | PUBLIC_SAFE_REVIEWER_RELEASE_CANDIDATE |
| Raw/private runtime evidence public-safe | NOT_PUBLIC_SAFE |
| Public-safe runtime proof | BLOCKED |
| Release status | PUBLIC_SAFE_REVIEWER_RELEASE_CANDIDATE_NO_TAG_NO_RELEASE |

## Boundary: Executive Summary

HawkinsOperations now has one merged controlled-test reviewer receipt loop for HO-DET-001. The SOCaaS-fit wording in this packet is reviewer context only: it explains how the merged artifacts can be inspected end to end while preserving the existing CONTROLLED_TEST_VALIDATED ceiling.

This reviewer packet is a public-safe reviewer package for HO-DET-001. It lets a reviewer inspect the controlled-test proof loop, proof record, release manifest, checksum plan, detection intent, validation evidence, support-only triage boundary, and customer-safe wording route before any official tag or GitHub Release exists.

The package is a sanitized release artifact candidate. Raw/private runtime evidence is excluded and remains NOT_PUBLIC_SAFE. Public-safe runtime proof remains blocked unless separately approved.

Website rendering is not proof. Public pages can route to this packet after review, but the proof authority remains the proof record and deterministic verifier outputs.

## What This Proves

- Detection intent is documented in the detections repository.
- Robustness and decomposition metadata exists for the observable, ATT&CK mapping, required data source, false-positive context, exclusions, and blind spots.
- Validation evidence exists in the validation repository.
- Deterministic validation passed for the controlled positive and negative process-creation fixture scope.
- Triage-support boundaries exist and keep human authority required.
- Proof receipt language exists in the proof card and proof record.
- Customer-safe claim wording exists as bounded reviewer/customer-safe explanation language.
- The website and reviewer surface reflect the bounded status and route back to proof authority.

## Boundary: What This Does NOT Prove

- Does not prove runtime-active detection.
- Does not prove a signal-observed result.
- Does not prove production deployment or production-ready status.
- Does not prove customer deployment or customer-deployed availability.
- Does not prove public-safe runtime evidence.
- Does not prove production SOCaaS deployment or SOCaaS availability.
- Does not prove autonomous SOC operation.
- Does not prove autonomous resolution.
- Does not prove AI-approved disposition.
- Does not prove analyst-approved disposition.

## Evidence Chain

| Evidence layer | Repository | Reviewer route | Meaning |
|---|---|---|---|
| Detection source | hawkinsoperations-detections | `detections/successor/ho-det-001/rule.yml`; `detections/successor/ho-det-001/status.yml`; `detections/successor/ho-det-001/splunk.spl` | Source logic, status metadata, ATT&CK mapping, endpoint process-field expectations, and blocked claims. |
| Validation | hawkinsoperations-validation | `docs/HO-DET-001_CLOSED_LOOP.md`; `reports/ho-det-001/validation-result.json`; `validation/successor/ho-det-001/case-packet.json`; `validation/successor/ho-det-001/autosoc-triage-packet.json` | Controlled-test result, deterministic pass/fail output, case-packet receipt chain, and support-only triage artifacts. |
| Platform case-packet shape | hawkinsoperations-platform | `contracts/examples/soar-case-packet-v0.sample.json` | SOAR-style analyst-support contract with deterministic validation and human-gated response boundaries. |
| Proof card and record | hawkinsoperations-proof | `proof/cards/HO-DET-001.md`; `proof/records/HO-DET-001.md` | Proof receipt, blocked-claim boundary, reviewer route, and final ceiling. |
| Reviewer/customer-safe rendering | hawkinsoperations-website | `src/data/proofRecords.ts` | Website route that reflects bounded status without becoming proof authority. |

## Commit / PR Table

| Repository | PR | Merged commit | Purpose | Claim boundary |
|---|---:|---|---|---|
| hawkinsoperations-detections | #30 | `8bbf95f93f5673f6a451e2165af4afe14c93bcee` | Adds receipt-fit metadata, robustness/decomposition fields, and bounded source-status language for HO-DET-001. | CONTROLLED_TEST_VALIDATED only. |
| hawkinsoperations-validation | #48 | `bc5a17520188bae1d7ddd25a8937358828ed9f6b` | Adds closed-loop documentation tying controlled fixtures, deterministic validation, case packet, proof route, and support-only triage. | CONTROLLED_TEST_VALIDATED only. |
| hawkinsoperations-platform | #31 | `13cf6c62abaf0a57e558f61e80ff41627fdcf024` | Adds SOAR-style case-packet sample showing analyst-support fields, blocked actions, and human authority gates. | CONTROLLED_TEST_VALIDATED only. |
| hawkinsoperations-proof | #43 | `761f20be97ce3254f18dfa3a7766945e13a4d1c4` | Adds proof-card and proof-record receipt wording plus checksum-aligned proof-pack metadata. | CONTROLLED_TEST_VALIDATED only. |
| hawkinsoperations-website | #36 | `e8b6cd1899631f231f30e96688bd74ad9238f237` | Adds reviewer/customer-safe rendering language for the bounded HO-DET-001 pilot receipt chain. | CONTROLLED_TEST_VALIDATED only. |

## Boundary: SOCaaS Relevance

Customers need receipts, not unsupported assurance. This SOCaaS-fit receipt loop matters because it shows what one detection can safely prove, what evidence supports that state, and what remains outside the claim boundary.

- SOCaaS-style detection delivery needs reviewer-visible receipts for detection intent, validation state, proof ceiling, and blocked claims.
- Detections need evidence boundaries so controlled-test status is not confused with runtime-active or signal-observed proof.
- Triage support needs human authority because the case packet can summarize sanitized facts and missing context, but it cannot decide disposition or execute response.
- Proof language must separate tested status from deployment claims, customer deployment claims, public-safe runtime evidence, autonomous SOC claims, AI-approved disposition, and analyst-approved disposition.

## Validation Summary

HO-DET-001 is CONTROLLED_TEST_VALIDATED through controlled positive and negative process-creation fixtures.

- Validation status: pass
- Total controlled cases: 14
- Positive controlled cases: 7
- Negative controlled cases: 7
- Matched positives: 7
- Missed positives: 0
- False-positive negative matches: 0
- Validation scope: controlled-test process-creation fixtures only

## Proof Loop Summary

The proof loop routes through source artifacts, validation artifacts, case-packet checks, deterministic verifier checks, proof receipt language, and reviewer/customer-safe rendering. The release path prepares a public-safe reviewer package only. It does not publish the packet.

Key routes:

- Proof record: `proof/records/HO-DET-001.md`
- Proof card: `proof/cards/HO-DET-001.md`
- Validation walkthrough: `hawkinsoperations-validation/docs/HO-DET-001_CLOSED_LOOP.md`
- Validation report: `hawkinsoperations-validation/reports/ho-det-001/validation-result.json`
- Public pipeline proof report: `hawkinsoperations-validation/reports/ho-det-001/pipeline-proof.md`
- Source detection: `hawkinsoperations-detections/detections/successor/ho-det-001/rule.yml`
- Splunk source: `hawkinsoperations-detections/detections/successor/ho-det-001/splunk.spl`
- Platform case-packet sample: `hawkinsoperations-platform/contracts/examples/soar-case-packet-v0.sample.json`
- Website reviewer route data: `hawkinsoperations-website/src/data/proofRecords.ts`
- Proof integrity verifier: `scripts/verify-ho-det-001-proof-integrity.py`
- Proof Pack release verifier: `scripts/verify-proof-pack-001-release.py`

## Repeatable Pattern

This packet defines the first merged reviewer receipt loop pattern. The next candidates should reuse the same shape only after their evidence boundaries are clean:

- HO-DET-012 scheduled task persistence.
- HO-DET-011 service creation or binary change after private-runtime and platform drift boundaries are clean.
- HO-DET-002 PowerShell suspicious flags after validation is complete.

## Included Files

- `REVIEWER_PACKET.md`
- `RELEASE_MANIFEST.json`
- `SHA256SUMS.txt`
- `RELEASE_NOTES_TEMPLATE.md`
- `SCOPE.md`
- `GOVERNANCE.md`
- `STATUS.md`
- `proof/cards/HO-DET-001.md`
- `proof/records/HO-DET-001.md`
- `proof/records/HO-DET-001-CONTROLLED-TEST-VALIDATION-001.json`
- `evidence/evidence-ledger.json`
- `evidence/EVIDENCE_LEDGER_SCHEMA.json`
- `scripts/verify-ho-det-001-proof-integrity.py`
- `.github/contracts/proof-record.schema.json`

## Excluded Files

- `README.md`
- `proof/records/HO-NDR-001.md`
- `proof/records/HO-DET-011.md`
- `proof/cards/HO-NDR-001.md`
- `docs/boundaries/HO-NDR-001-SECURITY-ONION-VISIBILITY-CONTRACT.md`
- `docs/debugging/*`
- `proof/records/PROOF-HOD-001-2026-04-21-001.json`
- `proof/records/AWS-DET-001.md`
- `proof/cards/AWS-DET-001.md`
- `.github/workflows/*`
- `docs/case-studies/*`

## Blocked Claims

The following claims remain blocked for this packet:

- runtime-active public proof
- signal-observed public proof
- evidence-linked public runtime proof
- public-safe runtime proof
- production-ready status
- production deployment
- customer-deployed status
- SOCaaS deployment
- SOCaaS availability
- live Splunk
- Cribl-routed telemetry
- Wazuh-routed collection
- AWS-live status
- autonomous SOC
- autonomous resolution
- AI-approved disposition
- analyst-approved disposition
- fleet-wide deployment
- enterprise deployment

## Reviewer Instructions

1. Read `RELEASE_MANIFEST.json` first to confirm the pack identity, included files, exclusions, release status, tag plan, and claim boundary.
2. Run `python scripts/verify-proof-pack-001-release.py` from the repository root.
3. Run `python scripts/verify-ho-det-001-proof-integrity.py` from the repository root.
4. Run `python scripts/verify_proof_integrity.py` from the repository root.
5. Confirm `SHA256SUMS.txt` matches the included packet files named by the manifest.
6. Treat every runtime, signal, public-safe runtime proof, production, customer-deployed, SOCaaS, autonomous, AI-approved, analyst-approved, fleet-wide, and enterprise wording path as blocked unless a later approved release changes the trust state.

## Boundary: Final Claim Boundary

Final ceiling:

CONTROLLED_TEST_VALIDATED

This packet does not change proof level, public-safe status, runtime status, signal status, deployment status, customer status, or disposition authority.

## Release Status

This packet is ready for review as a public-safe reviewer release candidate package. It is not an official release, does not create a tag, does not upload a zip, does not create a GitHub Release, and does not sign an artifact. Release publication still requires separate approval.
