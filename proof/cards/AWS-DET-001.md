# AWS-DET-001 Proof Card

## Header

| Field | Value |
|---|---|
| ID | AWS-DET-001 |
| Title | Denied IAM API Activity From CloudTrail-Style Fixtures |
| Record type | proof record |
| Current ceiling | TEST_VALIDATED_SYNTHETIC_SCOPE |
| Public-safe status | NOT_PUBLIC_SAFE |
| Last reviewed | UNKNOWN |

## Supported Claim

AWS-DET-001 passed fixture-only validation against controlled CloudTrail-style IAM denial fixtures.

## What This Proves

- The proof record exists at `proof/records/AWS-DET-001.md`.
- The detection source route is linked at `hawkinsoperations-detections/detections/cloud/aws/aws-det-001/rule.yml`.
- The fixture selector route is linked at `hawkinsoperations-detections/detections/cloud/aws/aws-det-001/cloudtrail.jsonpath`.
- The validation result route is linked at `hawkinsoperations-validation/reports/aws-det-001/validation-result.json`.
- The fixture workflow route is linked at `hawkinsoperations-validation/.github/workflows/aws-det-001-fixture-loop.yml`.

## What This Does NOT Prove

- AWS-live status is not proven.
- Live CloudTrail evidence is not proven.
- Cloud runtime-active, deployed cloud detection, AWS account coverage, and production status are not proven.
- Signal-observed public proof, evidence-linked public proof, public-safe status, AI-approved disposition, AI-decided disposition, and analyst-approved disposition are blocked.

## Evidence / Artifact Route

| Route | Path |
|---|---|
| Source record | `proof/records/AWS-DET-001.md` |
| Validation | `hawkinsoperations-validation/reports/aws-det-001/validation-result.json` |
| Workflow | `hawkinsoperations-validation/.github/workflows/aws-det-001-fixture-loop.yml` |
| Verifier | `hawkinsoperations-validation/scripts/validate-aws-det-001.py`; `hawkinsoperations-validation/scripts/verify-aws-det-001-result-parity.py`; `hawkinsoperations-validation/scripts/scan-aws-det-001-claim-boundaries.py` |
| Ledger | UNKNOWN |
| Related PR/commit | UNKNOWN |

## Control Reality

CI-enforced synthetic fixture scope is referenced through validation routes, but no AWS-specific proof repo card verifier was found. This card is a route/display artifact and must not be read as a cloud-live, deployed, or public-safe proof record.

## Current Status

| Plane | Truth |
|---|---|
| Repo truth | PROVEN: proof record and artifact routes exist. |
| Validation truth | PROVEN: fixture-only validation passed within controlled CloudTrail-style IAM denial fixtures. |
| Runtime truth | BLOCKED for cloud runtime-active status. |
| Signal truth | BLOCKED for public signal-observed proof. |
| Evidence truth | Linked validation artifacts exist; evidence ledger entry is UNKNOWN. |
| Public proof | TEST_VALIDATED_SYNTHETIC_SCOPE only; NOT_PUBLIC_SAFE for public promotion. |

## Next Promotion Gate

AWS-DET-001 needs separate evidence linkage, privacy review, stale review, wording review, and Raylee approval before any AWS-live, live CloudTrail, cloud runtime-active, deployed cloud detection, AWS account coverage, signal-observed, evidence-linked, public-safe, production, or disposition-authority wording is allowed.

## Reviewer Takeaway

AWS-DET-001 is currently a fixture-only AWS detection proof route. It is useful for reviewing controlled CloudTrail-style IAM denial validation, not for claiming live AWS operation, account coverage, production deployment, or public-safe cloud signal proof.
