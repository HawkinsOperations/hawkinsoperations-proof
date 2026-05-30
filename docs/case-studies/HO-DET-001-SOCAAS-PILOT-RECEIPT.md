# HO-DET-001 SOCaaS Pilot Receipt Pack

## Executive Summary

HO-DET-001 has a bounded SOCaaS pilot receipt route for reviewer inspection. The route connects detection source artifacts, controlled validation receipts, a platform case-packet contract, proof card and proof record surfaces, and website reviewer routing while preserving the current proof ceiling.

Current proof ceiling: `CONTROLLED_TEST_VALIDATED`.

This case study does not create a new proof level. It explains the existing receipt chain and the claims that remain blocked until stronger evidence and approval exist.

## What This Proves

- HO-DET-001 detection source artifacts exist in the detections repository.
- HO-DET-001 controlled-test validation artifacts exist in the validation repository.
- Controlled positive and negative process-creation fixture validation passed within the stated scope.
- The platform route includes a case-packet contract shape for analyst-support workflows.
- The proof repo has a proof card, proof record, evidence ledger entries, and verifier routes that preserve the `CONTROLLED_TEST_VALIDATED` ceiling.
- Website/reviewer routing can point to bounded proof surfaces without becoming proof authority.
- AI support remains support-only and cannot decide disposition, approve proof, close cases, or promote public wording.

## What This Does Not Prove

- Runtime-active public proof.
- Signal-observed public proof.
- Public-safe runtime proof.
- Production deployment.
- Customer deployment.
- SOCaaS deployment or SOCaaS availability.
- FortiSIEM integration, FortiSIEM deployment, or FortiSIEM signal observation.
- Live Splunk, Wazuh, Cribl, AWS, or other live SIEM route proof.
- Autonomous SOC operation or autonomous response.
- AI-approved, AI-decided, analyst-approved, or analyst-decided disposition.

## Evidence Chain

| Evidence layer | Route | Current meaning | Boundary |
|---|---|---|---|
| Detection source route | `hawkinsoperations-detections/detections/successor/ho-det-001/rule.yml`; `hawkinsoperations-detections/detections/successor/ho-det-001/status.yml`; `hawkinsoperations-detections/detections/successor/ho-det-001/splunk.spl` | Source artifacts exist for the detection intent, metadata, and Splunk expression. | Source truth only; not runtime, signal, production, or public-safe proof. |
| Validation receipt route | `hawkinsoperations-validation/reports/ho-det-001/validation-result.json`; `hawkinsoperations-validation/reports/ho-det-001/pipeline-proof.md`; `hawkinsoperations-validation/reports/ho-det-001/pipeline-proof.json`; `hawkinsoperations-validation/docs/HO-DET-001_CLOSED_LOOP.md` | Controlled-test validation passed and the proof-loop workflow preserves deterministic validation boundaries. | Controlled-test validation only; not live runtime or signal proof. |
| Platform contract route | `hawkinsoperations-platform/contracts/examples/soar-case-packet-v0.sample.json`; `hawkinsoperations-platform/contracts/examples/autosoc-closed-loop-case-ledger-v1.sample.json` | Analyst-support packet shape and case-ledger route exist as non-promotional contracts. | Contract shape only; not production SOAR/SOCaaS operation or case closure. |
| Proof card / record route | `proof/cards/HO-DET-001.md`; `proof/records/HO-DET-001.md`; `proof/records/HO-DET-001-CONTROLLED-TEST-VALIDATION-001.json`; `evidence/evidence-ledger.json` | Proof surfaces record the allowed claim, blocked claims, evidence links, and current ceiling. | Proof ceiling remains `CONTROLLED_TEST_VALIDATED`; public-safe status remains `NOT_PUBLIC_SAFE`. |
| Verifier route | `scripts/verify-ho-det-001-proof-integrity.py`; `scripts/verify_detection_proof_status_index.py`; `scripts/verify_proof_integrity.py`; `scripts/verify-proof-pack-001-release.py` | Deterministic checks preserve proof-record integrity, proof status index boundaries, ledger integrity, and Pack 001 release boundaries. | Passing checks are validation evidence, not merge authority or public promotion authority. |
| AI authority boundary route | `docs/case-studies/HO-DET-001-AI-AUTHORITY-BOUNDARY.md`; `proof/indexes/DETECTION_PROOF_STATUS_INDEX.yml` | AI can support triage and summarization but remains `AI_SUPPORT_ONLY` / `AI_NOT_AUTHORITY`. | AI cannot approve, close, promote, decide disposition, or mark material public-safe. |
| Governance saves route | `docs/governance-saves/GOVERNANCE-SAVES-CANDIDATES.md`; `docs/governance-saves/GOVERNANCE-SAVES-EVIDENCE-MATRIX.md` | Governance-saves material documents controls that blocked or corrected unsafe claim, merge, publication, or authority drift. | Candidate/save evidence does not raise the HO-DET-001 proof ceiling. |
| Website route | `hawkinsoperations-website/src/data/proofRecords.ts` | Website data may route reviewers to bounded proof status. | Website rendering is not proof and cannot promote runtime, signal, public-safe, production, or SOCaaS claims. |

## Allowed Claims

- "HO-DET-001 has merged source artifacts in the detections repository."
- "HO-DET-001 has merged controlled-test validation artifacts in the validation repository."
- "HO-DET-001 is `CONTROLLED_TEST_VALIDATED` through controlled positive and negative process-creation fixture validation."
- "HO-DET-001 can be reviewed as a controlled-test SOCaaS pilot receipt candidate with endpoint process facts, deterministic validation, support-only triage, and explicit human claim boundaries."
- "The platform case-packet contract is a non-promotional analyst-support route."
- "AI support remains support-only and does not decide disposition or approve proof."
- "Website routing can help reviewers find proof surfaces, but website rendering is not proof."

## Blocked Claims

- "HO-DET-001 is runtime-active."
- "HO-DET-001 has public signal-observed proof."
- "HO-DET-001 has public-safe runtime proof."
- "HO-DET-001 is production-ready."
- "HO-DET-001 is customer-deployed."
- "HO-DET-001 is SOCaaS-ready."
- "HO-DET-001 is deployed as SOCaaS."
- "HO-DET-001 is FortiSIEM-proven."
- "FortiSIEM observed HO-DET-001 signals."
- "Live Splunk fired as public proof."
- "Cribl routed HO-DET-001 telemetry as public proof."
- "Wazuh collected HO-DET-001 telemetry as public proof."
- "HO-DET-001 runs an autonomous SOC."
- "HO-DET-001 performed autonomous response."
- "AI approved the disposition."
- "AI decided the disposition."
- "An analyst approved the disposition."
- "The website proves HO-DET-001 status."

## Reviewer Acceptance Rule

Reviewer acceptance is limited to the bounded receipt chain. Accept the packet only if the proof card, proof record, proof status index, evidence ledger, and relevant verifier outputs agree that the ceiling remains `CONTROLLED_TEST_VALIDATED` and that public-safe runtime, signal-observed, production, SOCaaS deployment, FortiSIEM, autonomous SOC, AI disposition authority, and analyst disposition authority claims remain blocked.

If route documents disagree, use `proof/records/HO-DET-001.md`, `proof/cards/HO-DET-001.md`, `proof/indexes/DETECTION_PROOF_STATUS_INDEX.yml`, and deterministic verifier output as the current proof authority until the route document is corrected.

## Next Gate For Live SIEM / FortiSIEM Integration

The next gate is a separate approved live SIEM integration scope. For FortiSIEM or any other SIEM, the claim cannot move past `CONTROLLED_TEST_VALIDATED` until there is approved deployment or enablement evidence, preserved telemetry or alert/search output, evidence linkage, privacy review, stale review, public wording review, and Raylee approval for the exact stronger claim.

Until that gate is satisfied, FortiSIEM remains an integration target or future route only, not proven runtime, signal, production, SOCaaS, or public-safe proof.
