# HO-DET-001 - Suspicious PowerShell EncodedCommand Execution via Sysmon Event ID 1

## Header

- Detection ID: HO-DET-001
- Detection title: HO-DET-001 - Suspicious PowerShell EncodedCommand Execution via Sysmon Event ID 1
- Proof packet status: TEST_VALIDATED_SYNTHETIC_SCOPE recorded in the proof repo
- Current proof level: TEST_VALIDATED_SYNTHETIC_SCOPE
- Current trust class: TEST_VALIDATED_SYNTHETIC_SCOPE
- Public-safe status: NOT_PUBLIC_SAFE
- Approval status: NOT_APPROVED

This packet records merged synthetic validation evidence for HO-DET-001. It does not assert runtime activity, observed signal, production deployment, public-safe status, or live SOC operation.

## Status Clarification

- Proof packet status: TEST_VALIDATED_SYNTHETIC_SCOPE.
- Detection proof level: TEST_VALIDATED_SYNTHETIC_SCOPE.
- Detection trust class: TEST_VALIDATED_SYNTHETIC_SCOPE.
- Canonical detection source: `hawkinsoperations-detections/detections/successor/ho-det-001/rule.yml`.
- Canonical Splunk source: `hawkinsoperations-detections/detections/successor/ho-det-001/splunk.spl`.
- Canonical validation path: `hawkinsoperations-validation/reports/ho-det-001/validation-result.json`.
- Synthetic proof record: `proof/records/HO-DET-001-SYNTHETIC-VALIDATION-001.json`.
- Runtime-active status: BLOCKED.
- Signal-observed status: BLOCKED.
- Evidence-linked status: BLOCKED for runtime or signal evidence; this packet links synthetic validation artifacts only.
- Public-safe status: NOT_PUBLIC_SAFE.
- Approval status: NOT_APPROVED.

Related HOD-001 encoded-command artifacts may inform review, but they are not HO-DET-001 truth. Legacy artifacts do not promote current HawkinsOperations status.

## Linked Artifacts

- `hawkinsoperations-detections/detections/successor/ho-det-001/rule.yml`
- `hawkinsoperations-detections/detections/successor/ho-det-001/splunk.spl`
- `hawkinsoperations-validation/validation/successor/ho-det-001/validation-cases.json`
- `hawkinsoperations-validation/reports/ho-det-001/validation-result.json`
- `hawkinsoperations-validation/reports/ho-det-001/validation-result.md`
- `hawkinsoperations-validation/validation/successor/ho-det-001/autosoc-triage-packet.json`
- `hawkinsoperations-validation/validation/successor/ho-det-001/llm-summary.json`
- `hawkinsoperations-validation/.github/workflows/ho-det-001-proof-loop.yml`
- `hawkinsoperations-validation/.github/contracts/case-packet.schema.json`
- `hawkinsoperations-validation/validation/successor/ho-det-001/case-packet.json`
- `hawkinsoperations-validation/scripts/verify-ho-det-001-triage-boundary.py`
- `hawkinsoperations-validation/scripts/scan-ho-det-001-claim-boundaries.py`
- `hawkinsoperations-validation/scripts/verify-ho-det-001-result-parity.py`
- `hawkinsoperations-validation/scripts/verify_case_packet_contract.py`
- `hawkinsoperations-validation/scripts/build-ho-det-001-case-packet.py`
- `docs/case-studies/PURPLE-TEAM-CLOSED-LOOP-001.md`
- `docs/proving-ground/PROVING-GROUND-THESIS-PACKET-001.md`

## Source Refs

- Detections merge commit: `13a74f812fd17027b4a1968b615a4aae78c99f51`
- Validation merge commit: `e3bcf6c087b8e22ea62c08438fae6a60e800b094`
- Validation enforcement PR: `HawkinsOperations/hawkinsoperations-validation#10`
- Validation enforcement merge commit: `8b48500d2ebbaacd93ac88e77a31dccf1d3b4e25`

## Validation Enforcement Status

- Validation enforcement status: CI_ENFORCED_FOR_SYNTHETIC_SCOPE.
- Validation enforcement PR: `HawkinsOperations/hawkinsoperations-validation#10`.
- Validation enforcement merge commit: `8b48500d2ebbaacd93ac88e77a31dccf1d3b4e25`.
- Proof-loop workflow: `hawkinsoperations-validation/.github/workflows/ho-det-001-proof-loop.yml`.
- Enforcement scope: HO-DET-001 synthetic validation, case-packet contract, deterministic triage boundary, claim-boundary scan, result parity, and proof-loop CI.
- Control boundary: This is a real control only for the exact checked synthetic validation scope. It does not prove runtime-active, signal-observed, evidence-linked public proof, public-safe, production, fleet, Cribl, Wazuh, AWS-live, HO-GPU-01 runtime-active, autonomous SOC, or AI-approved disposition.

## Supported Claim

"HO-DET-001 passed synthetic validation against controlled positive and negative process-creation fixtures."

## Unsupported Claims

- runtime-active
- signal-observed
- public-safe
- production-ready
- live Splunk fired
- Cribl-routed telemetry
- Wazuh live collection
- production AutoSOC triage
- analyst-approved disposition
- HO-GPU-01 runtime-active
- AI-decided disposition

## Current Truth Table

| Claim | Truth label | Evidence/reference | Allowed wording | Blocked wording | Next promotion gate |
|---|---|---|---|---|---|
| HO-DET-001 proof packet exists in the proof repo. | PROVEN | `proof/records/HO-DET-001.md` | "A proof packet exists for HO-DET-001." | "The detection is production proven." | Keep proof current as gates change. |
| HO-DET-001 detection source exists. | PROVEN | `hawkinsoperations-detections/detections/successor/ho-det-001/rule.yml` | "Detection source exists for HO-DET-001." | "The detection is active." | Runtime deployment evidence. |
| HO-DET-001 Splunk source exists. | PROVEN | `hawkinsoperations-detections/detections/successor/ho-det-001/splunk.spl` at merge commit `13a74f812fd17027b4a1968b615a4aae78c99f51` | "A Splunk SPL source artifact exists for HO-DET-001." | "Live Splunk fired." | Deploy and preserve runtime/search evidence. |
| HO-DET-001 synthetic validation passed. | PROVEN | `hawkinsoperations-validation/reports/ho-det-001/validation-result.json` at merge commit `e3bcf6c087b8e22ea62c08438fae6a60e800b094` | "HO-DET-001 passed synthetic validation against controlled positive and negative process-creation fixtures." | "This catches attacks." | Runtime and signal evidence. |
| HO-DET-001 validation enforcement exists. | PROVEN | `hawkinsoperations-validation#10`; `.github/workflows/ho-det-001-proof-loop.yml`; merge commit `8b48500d2ebbaacd93ac88e77a31dccf1d3b4e25` | "HO-DET-001 validation enforcement exists for synthetic scope." | "Validation enforcement proves runtime, signal, production, or public-safe status." | Runtime/signal/public-safe evidence review. |
| AutoSOC synthetic triage packet exists. | PROVEN | `hawkinsoperations-validation/validation/successor/ho-det-001/autosoc-triage-packet.json` | "A deterministic synthetic triage packet was generated from the validation result." | "Production AutoSOC triage occurred." | Production AutoSOC run evidence. |
| Offline LLM support stub exists. | PROVEN | `hawkinsoperations-validation/validation/successor/ho-det-001/llm-summary.json` | "A deterministic blocked-runtime LLM support stub exists." | "HO-GPU-01 was runtime-active." | Approved local model runtime evidence. |
| HO-DET-001 runtime-active status is proven. | BLOCKED | No deployment, enablement, schedule, or backend state evidence linked. | "Runtime-active status requires deployment evidence." | "This detection is active." | Preserve runtime deployment evidence. |
| HO-DET-001 signal-observed status is proven. | BLOCKED | No preserved telemetry, alert, log, or search output linked. | "Signal-observed status requires preserved telemetry, alert, log, or search output." | "This catches attacks." | Preserve signal observation evidence. |
| HO-DET-001 public-safe status is approved. | BLOCKED | No reviewed public wording, privacy review, stale review, evidence linkage, or Raylee approval. | "Public-safe status requires reviewed wording, privacy review, stale review, evidence linkage, and Raylee approval." | "HO-DET-001 is PUBLIC_SAFE." | Raylee approval after evidence and claim review. |

## Validation Summary

- Validation status: pass
- Total controlled cases: 14
- Matched positive count: 7
- Missed positive cases: none
- False-positive negative cases: none
- Validation scope: synthetic process-creation fixtures only
- Validation result path: `hawkinsoperations-validation/reports/ho-det-001/validation-result.json`

## AutoSOC Summary

- Packet ID: HO-DET-001-SYNTHETIC-TRIAGE-001
- Scope: deterministic synthetic output only
- Production AutoSOC status: BLOCKED
- Analyst-approved disposition: BLOCKED

## LLM Summary

- Model runtime status: BLOCKED
- Execution mode: deterministic_stub_no_model_call
- Summary type: hypothesis_triage_support_only
- AI-decided disposition: BLOCKED

## Proof Level Assessment

### SOURCE_EXISTS

- Status: SATISFIED
- Evidence: `hawkinsoperations-detections/detections/successor/ho-det-001/rule.yml` and `hawkinsoperations-detections/detections/successor/ho-det-001/splunk.spl`.

### TEST_DEFINED

- Status: SATISFIED for synthetic scope
- Evidence: `hawkinsoperations-validation/validation/successor/ho-det-001/validation-cases.json`.

### TEST_VALIDATED_SYNTHETIC_SCOPE

- Status: SATISFIED
- Evidence: `hawkinsoperations-validation/reports/ho-det-001/validation-result.json`.
- Supported claim: "HO-DET-001 passed synthetic validation against controlled positive and negative process-creation fixtures."

### RUNTIME_ACTIVE

- Status: NOT_SATISFIED
- Evidence required: deployment or enablement proof, backend/platform identifier sanitized for public use, timestamp, owner, currentness review, and stale review date.

### SIGNAL_OBSERVED

- Status: NOT_SATISFIED
- Evidence required: preserved telemetry, alert, log, or search output showing the signal, with context, time window, query or rule reference, and redaction review.

### PUBLIC_SAFE

- Status: BLOCKED
- Evidence required: approved claim text, evidence path, trust class, allowed wording, blocked wording, stale review date, privacy review, public claim review, and Raylee approval.

## Allowed Claims

- "HO-DET-001 has merged source artifacts in the detections repository."
- "HO-DET-001 has merged synthetic validation artifacts in the validation repository."
- "HO-DET-001 passed synthetic validation against controlled positive and negative process-creation fixtures."
- "A deterministic synthetic AutoSOC triage packet was generated from the HO-DET-001 synthetic validation result."
- "The offline LLM support artifact is a deterministic blocked-runtime stub and does not prove HO-GPU-01 runtime."

## Blocked Claims

- "This detection is active."
- "This catches attacks."
- "This proves coverage."
- "This is production-ready."
- "This is public-safe."
- "Live Splunk fired."
- "Cribl routed live telemetry."
- "Wazuh collected live telemetry."
- "Production AutoSOC triage occurred."
- "An analyst approved the disposition."
- "HO-GPU-01 ran the model."
- "AI decided the disposition."
- "The website proves detection status."
- "Original detections are now successor detections."

## Next Promotion Gate

The next promotion gate is runtime deployment evidence or preserved signal evidence, depending on operator priority. Public proof and website updates remain blocked until evidence linkage, privacy review, stale review, wording review, and Raylee approval are complete.
