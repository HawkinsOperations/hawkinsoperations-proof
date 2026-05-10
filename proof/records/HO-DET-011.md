# HO-DET-011 - Windows Service Creation or Service Binary Change

## Header

- Detection ID: HO-DET-011
- Detection title: Windows service creation / service binary change
- Proof packet status: PRIVATE_RUNTIME_EVIDENCE_CAPTURED recorded in the proof repo
- Current proof level: PRIVATE_RUNTIME_EVIDENCE_CAPTURED
- Current trust class: PRIVATE_RUNTIME_EVIDENCE_CAPTURED
- Public-safe status: NOT_PUBLIC_SAFE
- Approval status: NOT_APPROVED

This packet records merged source, synthetic validation, platform case-packet guardrail evidence, and a sanitized private local Windows runtime evidence summary for HO-DET-011. It does not assert runtime-active status, public or routed signal-observed status, public-safe proof, Wazuh observation, Splunk observation, Cribl routing, production deployment, fleet-wide coverage, complete service-creation coverage, autonomous SOC operation, AI-approved disposition, AI-decided disposition, or analyst-approved disposition.

## Status Clarification

- Proof packet status: PRIVATE_RUNTIME_EVIDENCE_CAPTURED.
- Detection proof level: PRIVATE_RUNTIME_EVIDENCE_CAPTURED.
- Detection trust class: PRIVATE_RUNTIME_EVIDENCE_CAPTURED.
- Canonical detection source: `hawkinsoperations-detections/detections/successor/ho-det-011/rule.yml`.
- Canonical Splunk source: `hawkinsoperations-detections/detections/successor/ho-det-011/splunk.spl`.
- Canonical Wazuh source: `hawkinsoperations-detections/detections/successor/ho-det-011/wazuh.xml`.
- Canonical event mapping: `hawkinsoperations-detections/detections/successor/ho-det-011/event-mapping.yml`.
- Canonical validation path: `hawkinsoperations-validation/reports/ho-det-011/validation-result.json`.
- Platform case-packet sample: `hawkinsoperations-platform/contracts/examples/ho-det-011-case-packet.sample.json`.
- Platform case-packet schema: `hawkinsoperations-platform/contracts/schemas/ho-det-011-case-packet.schema.json`.
- Platform case-packet verifier: `hawkinsoperations-platform/scripts/verify-ho-det-011-case-packet.py`.
- Runtime evidence status: PRIVATE_RUNTIME_EVIDENCE_CAPTURED for local Windows event capture only.
- Runtime-active status: BLOCKED / NOT_PROVEN.
- Public or routed signal status: BLOCKED / NOT_PROVEN.
- Wazuh status: NOT_PROVEN.
- Splunk status: NOT_PROVEN.
- Cribl status: NOT_PROVEN.
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
- Current proof ceiling: PRIVATE_RUNTIME_EVIDENCE_CAPTURED.
- Synthetic validation scope: TEST_VALIDATED_SYNTHETIC_SCOPE.
- Runtime evidence status: PRIVATE_RUNTIME_EVIDENCE_CAPTURED for local Windows event capture only.
- Runtime-active status: BLOCKED / NOT_PROVEN.
- Public or routed signal status: BLOCKED / NOT_PROVEN.
- Public-safe status: NOT_PUBLIC_SAFE.

## Private Runtime Evidence Summary

- Evidence run ID: `20260510-143232`.
- Evidence location: raw evidence retained under the approved private Data evidence route; raw event logs are not copied into this proof repo.
- Sanitized evidence basis: manifest, claim boundary, and hash receipt were verified from the approved private route.
- Local Windows System Event ID 7045 observed: yes.
- Local Windows Security Event ID 4697 observed: yes.
- Local Sysmon Event ID 1 observed: yes.
- Cleanup result: CLEANED_UP.
- Final disposable service state: SERVICE_ABSENT.
- Wazuh observed: NOT_PROVEN.
- Splunk observed: NOT_PROVEN.
- Cribl routed: NOT_PROVEN.
- Public-safe proof: NOT_PROVEN / NOT_PUBLIC_SAFE.
- Coverage boundary: this proves one controlled private local Windows service-creation capture only; it does not prove service-creation coverage completeness, production readiness, fleet-wide coverage, Wazuh correlation, Splunk correlation, Cribl routing, or public-safe proof.

## Platform Case-Packet Guardrail

- Platform guardrail status: SATISFIED as a non-promotional boundary.
- Platform guardrail PR: `HawkinsOperations/hawkinsoperations-platform#9`.
- Platform guardrail merge/squash commit: `e3374181148f044b75782689db252e3f12d5c6fc`.
- Guardrail artifacts:
  - `hawkinsoperations-platform/contracts/schemas/ho-det-011-case-packet.schema.json`
  - `hawkinsoperations-platform/contracts/examples/ho-det-011-case-packet.sample.json`
  - `hawkinsoperations-platform/scripts/verify-ho-det-011-case-packet.py`
  - `hawkinsoperations-platform/contracts/contract-version.json`
- Guardrail boundary: This platform packet and the later private local Windows runtime evidence preserve public-safe status at NOT_PUBLIC_SAFE and keep runtime-active, signal-observed public proof, live Splunk fired, Wazuh-routed, Cribl-routed, AWS-live, production-ready, fleet-wide, service-creation coverage completeness, autonomous SOC, AI-approved disposition, AI-decided disposition, and analyst-approved disposition claims blocked.

## Supported Claim

"HO-DET-011 passed synthetic validation against controlled Windows service creation fixtures."

## Allowed Claims

- "HO-DET-011 source artifacts exist in the detections repository."
- "HO-DET-011 passed synthetic validation against controlled Windows service creation fixtures."
- "HO-DET-011 has a platform case-packet guardrail that preserves synthetic-scope claim boundaries."
- "HO-DET-011 has sanitized private local Windows runtime evidence captured for one controlled service-creation test."
- "HO-DET-011 is capped at PRIVATE_RUNTIME_EVIDENCE_CAPTURED for private evidence and NOT_PUBLIC_SAFE for public use."

## Blocked Claims

- runtime-active
- signal-observed
- public-safe
- evidence-linked public proof
- live Splunk fired
- Splunk observed
- Wazuh observed
- Wazuh-routed
- Cribl routed
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

PRIVATE_RUNTIME_EVIDENCE_CAPTURED

## Next Promotion Gate

HO-DET-011 requires separate event-specific Wazuh, Splunk, or Cribl correlation review before any routed-telemetry wording can advance. Public-safe wording remains blocked until public evidence linkage, redaction review, stale review, wording review, and Raylee approval are complete.
