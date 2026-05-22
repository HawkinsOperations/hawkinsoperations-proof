# HO-DET-012 Proof Card

## Header

| Field | Value |
|---|---|
| ID | HO-DET-012 |
| Title | Suspicious Scheduled Task Creation |
| Record type | proof record |
| Current ceiling | CONTROLLED_TEST_VALIDATED |
| Public-safe status | NOT_PUBLIC_SAFE |
| Last reviewed | UNKNOWN |

## Supported Claim

HO-DET-012 passed controlled-test validation against scheduled-task creation and update fixtures.

## What This Proves

- The proof record exists at `proof/records/HO-DET-012.md`.
- The detection source route is linked at `hawkinsoperations-detections/detections/successor/ho-det-012/rule.yml`.
- The validation result route is linked at `hawkinsoperations-validation/reports/ho-det-012/validation-result.json`.
- The validation case route is linked at `hawkinsoperations-validation/validation/successor/ho-det-012/validation-cases.json`.
- The validation result reports 8 controlled cases: 4 positive and 4 negative.
- The validation result reports 0 missed positives and 0 false-positive negatives.

## What This Does NOT Prove

- Runtime-active status is not proven.
- Signal-observed public proof is blocked.
- Public-safe runtime proof is blocked.
- Production-ready, fleet-wide, or deployed status is not proven.
- Live Splunk proof, live Wazuh proof, live Cribl proof, live Security Onion proof, autonomous SOC operation, AI-approved disposition, and analyst-approved disposition are not proven.

## Evidence / Artifact Route

| Route | Path |
|---|---|
| Source record | `proof/records/HO-DET-012.md` |
| Detection source | `hawkinsoperations-detections/detections/successor/ho-det-012/rule.yml` |
| Validation | `hawkinsoperations-validation/reports/ho-det-012/validation-result.json` |
| Validation cases | `hawkinsoperations-validation/validation/successor/ho-det-012/validation-cases.json` |
| Verifier | `hawkinsoperations-validation/scripts/validate-ho-det-012.py`; `hawkinsoperations-validation/scripts/verify-ho-det-012-result-parity.py`; `hawkinsoperations-validation/scripts/scan-ho-det-012-claim-boundaries.py` |
| Ledger | UNKNOWN |
| Related PR/commit | UNKNOWN |

## Control Reality

Controlled validation scope is referenced through validation routes, but this card is route/display only. It does not raise the proof ceiling beyond CONTROLLED_TEST_VALIDATED and does not create runtime, signal, public-safe runtime, production, autonomous SOC, AI-approved, or analyst-approved proof.

## Current Status

| Plane | Truth |
|---|---|
| Repo truth | PROVEN: proof record and artifact routes exist. |
| Validation truth | PROVEN: controlled scheduled-task validation passed within controlled fixture scope. |
| Runtime truth | BLOCKED for runtime-active status. |
| Signal truth | BLOCKED for public signal-observed proof. |
| Evidence truth | Linked validation artifacts exist; evidence ledger entry is UNKNOWN. |
| Public proof | CONTROLLED_TEST_VALIDATED only; NOT_PUBLIC_SAFE for public promotion. |

## Next Promotion Gate

HO-DET-012 needs separate runtime evidence, signal evidence, public-safe review, stale review, wording review, and Raylee approval before any runtime-active, signal-observed, routed-telemetry, public-safe runtime, production, autonomous SOC, AI-approved, or analyst-approved wording is allowed.

## Reviewer Takeaway

HO-DET-012 is currently a controlled scheduled-task validation proof route. It is useful for reviewing controlled fixture validation, not for claiming live operation, routed telemetry, production deployment, autonomous disposition, or public-safe runtime proof.
