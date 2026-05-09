# HO-DET-001 Proof Card

## Header

| Field | Value |
|---|---|
| ID | HO-DET-001 |
| Title | Suspicious PowerShell EncodedCommand Execution via Sysmon Event ID 1 |
| Record type | proof record |
| Current ceiling | TEST_VALIDATED_SYNTHETIC_SCOPE |
| Public-safe status | NOT_PUBLIC_SAFE |
| Last reviewed | UNKNOWN |

## Supported Claim

HO-DET-001 passed synthetic validation against controlled positive and negative process-creation fixtures.

## What This Proves

- The proof record exists at `proof/records/HO-DET-001.md`.
- The synthetic validation result is linked at `hawkinsoperations-validation/reports/ho-det-001/validation-result.json`.
- The proof record reports 14 controlled cases: 7 matched positives and 7 negative cases without false-positive negative matches.
- The proof loop route is linked at `hawkinsoperations-validation/.github/workflows/ho-det-001-proof-loop.yml`.
- The proof repo verifier exists at `scripts/verify-ho-det-001-proof-integrity.py`.

## What This Does NOT Prove

- Runtime-active deployment is not proven.
- Signal-observed public proof is blocked.
- Evidence-linked public proof is blocked.
- Public-safe, production-ready, fleet-wide, or enterprise-deployed status is not proven.
- Live Splunk public proof, Cribl-routed HO-DET telemetry, Wazuh-routed telemetry, AWS-live status, autonomous SOC operation, production AutoSOC, AI-approved disposition, AI-decided disposition, and analyst-approved disposition are not proven.

## Evidence / Artifact Route

| Route | Path |
|---|---|
| Source record | `proof/records/HO-DET-001.md` |
| Validation | `hawkinsoperations-validation/reports/ho-det-001/validation-result.json` |
| Workflow | `hawkinsoperations-validation/.github/workflows/ho-det-001-proof-loop.yml`; `.github/workflows/ho-det-001-proof-integrity.yml` |
| Verifier | `scripts/verify-ho-det-001-proof-integrity.py`; `hawkinsoperations-validation/scripts/verify-ho-det-001-reproducible-proof-pack.py`; `hawkinsoperations-validation/scripts/verify-ho-det-001-runtime-packet.py` |
| Ledger | `evidence/evidence-ledger.json` entries `HO-DET-001-SYNTHETIC-VALIDATION-001` and `HO-DET-001-PLATFORM-RUNTIME-CONTRACT-GUARDRAIL-001` |
| Related PR/commit | `HawkinsOperations/hawkinsoperations-validation#10`; `HawkinsOperations/hawkinsoperations-validation#18`; `HawkinsOperations/hawkinsoperations-validation#22`; `HawkinsOperations/hawkinsoperations-platform#5` |

## Control Reality

CI-enforced synthetic scope and verifier-backed proof record. The proof card is route/display only. It does not raise the public ceiling, and it does not turn private/internal controlled lab runtime match evidence into public proof.

## Current Status

| Plane | Truth |
|---|---|
| Repo truth | PROVEN: proof record and linked source artifact routes exist. |
| Validation truth | PROVEN: synthetic validation passed within controlled fixture scope. |
| Runtime truth | PRIVATE_INTERNAL only where recorded; public runtime-active status remains BLOCKED. |
| Signal truth | BLOCKED for public signal-observed proof. |
| Evidence truth | Ledger-backed for synthetic validation and platform guardrail records; private/internal runtime evidence is not public-safe proof. |
| Public proof | TEST_VALIDATED_SYNTHETIC_SCOPE only; NOT_PUBLIC_SAFE for public promotion. |

## Next Promotion Gate

To raise the claim, HO-DET-001 needs approved evidence linkage for the specific stronger claim, privacy review, stale review, wording review, and Raylee approval. Runtime-active status needs deployment or enablement proof. Signal-observed status needs preserved telemetry, alert, log, or search output with reviewable context. Public-safe status requires approved public wording and evidence-link review.

## Reviewer Takeaway

HO-DET-001 has a strong synthetic validation record and verifier-backed proof routing for that scope. Treat this card as a fast map to the proof record, not as proof of live operation, public signal observation, routed telemetry, production coverage, or public-safe status.
