# AWS-DET-001 - Denied IAM API Activity From CloudTrail-Style Fixtures

## Header

- Detection ID: AWS-DET-001
- Detection title: Denied IAM API Activity From CloudTrail-Style Fixtures
- Proof packet status: TEST_VALIDATED_SYNTHETIC_SCOPE recorded in the proof repo
- Current proof level: TEST_VALIDATED_SYNTHETIC_SCOPE
- Current trust class: TEST_VALIDATED_SYNTHETIC_SCOPE
- Public-safe status: NOT_PUBLIC_SAFE
- Approval status: NOT_APPROVED

This packet records fixture-only validation evidence for AWS-DET-001. It does not assert AWS-live proof, CloudTrail live proof, cloud runtime-active proof, production deployment, public-safe status, or live cloud signal observation.

## Status Clarification

- Proof packet status: TEST_VALIDATED_SYNTHETIC_SCOPE.
- Detection proof level: TEST_VALIDATED_SYNTHETIC_SCOPE.
- Detection trust class: TEST_VALIDATED_SYNTHETIC_SCOPE.
- Canonical detection source: `hawkinsoperations-detections/detections/cloud/aws/aws-det-001/rule.yml`.
- Canonical fixture selector: `hawkinsoperations-detections/detections/cloud/aws/aws-det-001/cloudtrail.jsonpath`.
- Canonical validation path: `hawkinsoperations-validation/reports/aws-det-001/validation-result.json`.
- AWS-live status: BLOCKED.
- AWS CloudTrail live status: BLOCKED.
- Cloud runtime-active status: BLOCKED.
- Signal-observed status: BLOCKED.
- Public-safe status: NOT_PUBLIC_SAFE.
- Approval status: NOT_APPROVED.

## Linked Artifacts

- `docs/proving-ground/PROVING-GROUND-THESIS-PACKET-001.md`
- `hawkinsoperations-detections/detections/cloud/aws/aws-det-001/rule.yml`
- `hawkinsoperations-detections/detections/cloud/aws/aws-det-001/cloudtrail.jsonpath`
- `hawkinsoperations-detections/detections/cloud/aws/aws-det-001/README.md`
- `hawkinsoperations-validation/validation/cloud/aws/aws-det-001/validation-cases.json`
- `hawkinsoperations-validation/reports/aws-det-001/validation-result.json`
- `hawkinsoperations-validation/reports/aws-det-001/validation-result.md`
- `hawkinsoperations-validation/scripts/validate-aws-det-001.py`
- `hawkinsoperations-validation/scripts/verify-aws-det-001-result-parity.py`
- `hawkinsoperations-validation/scripts/scan-aws-det-001-claim-boundaries.py`
- `hawkinsoperations-validation/.github/workflows/aws-det-001-fixture-loop.yml`

## Supported Claim

"AWS-DET-001 passed fixture-only validation against controlled CloudTrail-style IAM denial fixtures."

## Validation Summary

- Validation status: pass
- Total controlled cases: 6
- Matched positive count: 3
- Missed positive cases: none
- False-positive negative cases: none
- Validation scope: synthetic CloudTrail-style IAM denied/unauthorized API fixtures only
- AWS live status: BLOCKED
- Public-safe status: NOT_PUBLIC_SAFE

## Allowed Claims

- "AWS-DET-001 source exists as a fixture-only CloudTrail-style detection candidate."
- "AWS-DET-001 passed fixture-only validation against controlled CloudTrail-style IAM denial fixtures."
- "AWS-DET-001 does not use AWS credentials, live AWS APIs, or live CloudTrail evidence."

## Blocked Claims

- AWS-live proof
- AWS CloudTrail live proof
- cloud runtime-active proof
- production proof
- public-safe runtime proof
- signal-observed public proof
- deployed cloud detection
- AWS account coverage
- analyst-approved disposition
- AI-approved disposition

## Current Claim Ceiling

TEST_VALIDATED_SYNTHETIC_SCOPE

## Next Promotion Gate

AWS-DET-001 requires separate evidence, review, and Raylee approval before any AWS-live, CloudTrail live, cloud runtime-active, signal-observed, evidence-linked, public-safe, production, or deployed-cloud wording is allowed.
