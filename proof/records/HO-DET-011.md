# HO-DET-011 - Windows Service Creation or Service Binary Change

## Header

- Detection ID: HO-DET-011
- Detection title: Windows service creation / service binary change
- Proof packet status: TEST_VALIDATED_SYNTHETIC_SCOPE recorded in the proof repo
- Current proof level: TEST_VALIDATED_SYNTHETIC_SCOPE
- Current trust class: TEST_VALIDATED_SYNTHETIC_SCOPE
- Public-safe status: NOT_PUBLIC_SAFE
- Approval status: NOT_APPROVED

This packet records merged source, synthetic validation, and platform case-packet guardrail evidence for HO-DET-011. It does not assert runtime-active status, signal-observed status, public-safe proof, live Splunk firing, routed telemetry, production deployment, fleet-wide coverage, complete service-creation coverage, autonomous SOC operation, AI-approved disposition, AI-decided disposition, or analyst-approved disposition.

## Status Clarification

- Proof packet status: TEST_VALIDATED_SYNTHETIC_SCOPE.
- Detection proof level: TEST_VALIDATED_SYNTHETIC_SCOPE.
- Detection trust class: TEST_VALIDATED_SYNTHETIC_SCOPE.
- Canonical detection source: `hawkinsoperations-detections/detections/successor/ho-det-011/rule.yml`.
- Canonical Splunk source: `hawkinsoperations-detections/detections/successor/ho-det-011/splunk.spl`.
- Canonical Wazuh source: `hawkinsoperations-detections/detections/successor/ho-det-011/wazuh.xml`.
- Canonical event mapping: `hawkinsoperations-detections/detections/successor/ho-det-011/event-mapping.yml`.
- Canonical validation path: `hawkinsoperations-validation/reports/ho-det-011/validation-result.json`.
- Platform case-packet sample: `hawkinsoperations-platform/contracts/examples/ho-det-011-case-packet.sample.json`.
- Platform case-packet schema: `hawkinsoperations-platform/contracts/schemas/ho-det-011-case-packet.schema.json`.
- Platform case-packet verifier: `hawkinsoperations-platform/scripts/verify-ho-det-011-case-packet.py`.
- Runtime status: BLOCKED / NOT_PROVEN.
- Signal status: BLOCKED / NOT_OBSERVED.
- Public-safe status: NOT_PUBLIC_SAFE.
- Approval status: NOT_APPROVED.

## Linked Artifacts

- `hawkinsoperations-detections/detections/successor/ho-det-011/rule.yml`
- `hawkinsoperations-detections/detections/successor/ho-det-011/splunk.spl`
- `hawkinsoperations-detections/detections/successor/ho-det-011/wazuh.xml`
- `hawkinsoperations-detections/detections/successor/ho-det-011/event-mapping.yml`
- `hawkinsoperations-detections/detections/successor/ho-det-011/status.yml`
- `hawkinsoperations-detections/detections/successor/ho-det-011/README.md`
- `hawkinsoperations-validation/validation/successor/ho-det-011/validation-cases.json`
- `hawkinsoperations-validation/reports/ho-det-011/validation-result.json`
- `hawkinsoperations-validation/reports/ho-det-011/validation-result.md`
- `hawkinsoperations-validation/scripts/validate-ho-det-011.py`
- `hawkinsoperations-platform/contracts/schemas/ho-det-011-case-packet.schema.json`
- `hawkinsoperations-platform/contracts/examples/ho-det-011-case-packet.sample.json`
- `hawkinsoperations-platform/scripts/verify-ho-det-011-case-packet.py`
- `hawkinsoperations-platform/contracts/contract-version.json`

## Source Refs

- Detections source PR: `HawkinsOperations/hawkinsoperations-detections#11`.
- Detections merge commit: `3bf93b820eee300630f5784979deec049f1845fa`.
- Validation PR: `HawkinsOperations/hawkinsoperations-validation#25`.
- Validation merge commit: `4c4bf5a64b90692ea363bc68ab9f606ed1e84698`.
- Platform guardrail PR: `HawkinsOperations/hawkinsoperations-platform#9`.
- Platform merge/squash commit: `e3374181148f044b75782689db252e3f12d5c6fc`.

## Validation Summary

- Validation status: pass.
- Total controlled cases: 6.
- Matched positive count: 3.
- Negative cases not matched: 3.
- Missed positive cases: none.
- False-positive negative cases: none.
- Validation scope: controlled synthetic Windows service creation fixtures only.
- Supported validation claim: "HO-DET-011 passed synthetic validation against controlled Windows service creation fixtures."
- Current proof ceiling: TEST_VALIDATED_SYNTHETIC_SCOPE.
- Runtime status: BLOCKED / NOT_PROVEN.
- Signal status: BLOCKED / NOT_OBSERVED.
- Public-safe status: NOT_PUBLIC_SAFE.

## Platform Case-Packet Guardrail

- Platform guardrail status: SATISFIED as a non-promotional boundary.
- Platform guardrail PR: `HawkinsOperations/hawkinsoperations-platform#9`.
- Platform guardrail merge/squash commit: `e3374181148f044b75782689db252e3f12d5c6fc`.
- Guardrail artifacts:
  - `hawkinsoperations-platform/contracts/schemas/ho-det-011-case-packet.schema.json`
  - `hawkinsoperations-platform/contracts/examples/ho-det-011-case-packet.sample.json`
  - `hawkinsoperations-platform/scripts/verify-ho-det-011-case-packet.py`
  - `hawkinsoperations-platform/contracts/contract-version.json`
- Guardrail boundary: This platform packet preserves the proof ceiling at TEST_VALIDATED_SYNTHETIC_SCOPE and keeps runtime-active, signal-observed, public-safe, live Splunk fired, Wazuh-routed, Cribl-routed, AWS-live, production-ready, fleet-wide, service-creation coverage completeness, autonomous SOC, AI-approved disposition, AI-decided disposition, and analyst-approved disposition claims blocked.

## Supported Claim

"HO-DET-011 passed synthetic validation against controlled Windows service creation fixtures."

## Allowed Claims

- "HO-DET-011 source artifacts exist in the detections repository."
- "HO-DET-011 passed synthetic validation against controlled Windows service creation fixtures."
- "HO-DET-011 has a platform case-packet guardrail that preserves synthetic-scope claim boundaries."
- "HO-DET-011 is capped at TEST_VALIDATED_SYNTHETIC_SCOPE."

## Blocked Claims

- runtime-active
- signal-observed
- public-safe
- evidence-linked public proof
- live Splunk fired
- Wazuh-routed
- Cribl-routed
- AWS-live
- production-ready
- fleet-wide
- service-creation coverage completeness
- autonomous SOC
- AI-approved disposition
- AI-decided disposition
- analyst-approved disposition

## Current Claim Ceiling

TEST_VALIDATED_SYNTHETIC_SCOPE

## Next Promotion Gate

HO-DET-011 requires controlled runtime capture with `RUNTIME_APPROVED` before any runtime, signal, routed-telemetry, public-safe, production, fleet, service-completeness, autonomous SOC, AI disposition, or analyst disposition claim can advance.
