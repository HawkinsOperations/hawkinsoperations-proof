# HO-DET-001 - Suspicious PowerShell EncodedCommand Execution via Sysmon Event ID 1

## Header

- Detection ID: HO-DET-001
- Detection title: HO-DET-001 - Suspicious PowerShell EncodedCommand Execution via Sysmon Event ID 1
- Proof packet status: CONTROLLED_TEST_VALIDATED recorded in the proof repo
- Current proof level: TEST_VALIDATED_SYNTHETIC_SCOPE
- Current trust class: TEST_VALIDATED_SYNTHETIC_SCOPE
- Current public label: CONTROLLED_TEST_VALIDATED
- Public display label: CONTROLLED_TEST_VALIDATED
- Public trust label: CONTROLLED_TEST_VALIDATED
- Private controlled runtime status: CONTROLLED_LAB_RUNTIME_MATCH_VERIFIED
- Public-safe status: NOT_PUBLIC_SAFE
- Approval status: NOT_APPROVED

Compatibility note: `TEST_VALIDATED_SYNTHETIC_SCOPE` is the internal verifier token preserved for proof-integrity compatibility. `CONTROLLED_TEST_VALIDATED` is the public-facing label used to describe the same controlled-test validation boundary without using legacy public wording.

This packet records merged controlled-test validation evidence for HO-DET-001 and a verifier-backed private controlled lab runtime match. It does not assert runtime activity, production deployment, public-safe status, or live SOC operation.

## Status Clarification

- Proof packet status: CONTROLLED_TEST_VALIDATED.
- Internal proof compatibility value - TEST_VALIDATED_SYNTHETIC_SCOPE.
- Detection public label: CONTROLLED_TEST_VALIDATED.
- Detection public trust label: CONTROLLED_TEST_VALIDATED.
- Private controlled runtime status: CONTROLLED_LAB_RUNTIME_MATCH_VERIFIED.
- Canonical detection source: `hawkinsoperations-detections/detections/successor/ho-det-001/rule.yml`.
- Canonical Splunk source: `hawkinsoperations-detections/detections/successor/ho-det-001/splunk.spl`.
- Canonical validation path: `hawkinsoperations-validation/reports/ho-det-001/validation-result.json`.
- Public pipeline proof pack: `hawkinsoperations-validation/reports/ho-det-001/pipeline-proof.md`.
- Public pipeline proof pack JSON: `hawkinsoperations-validation/reports/ho-det-001/pipeline-proof.json`.
- Public pipeline proof pack merge: `HawkinsOperations/hawkinsoperations-validation#27` at merge commit `6d4e3ac7b284e380048e8e4f20edf50b6fa9bccb`.
- Historical validation proof record: `proof/records/HO-DET-001-SYNTHETIC-VALIDATION-001.json`.
- Runtime-active status: BLOCKED.
- Public signal-observed status: BLOCKED.
- Signal-observed status: BLOCKED.
- Private controlled lab runtime match status: VERIFIED by validation PR `HawkinsOperations/hawkinsoperations-validation#22`.
- Public evidence-linked status: BLOCKED for public runtime or signal evidence; private/internal packet evidence is verifier-backed but not public-safe raw evidence.
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
- `hawkinsoperations-validation/scripts/verify-ho-det-001-reproducible-proof-pack.py`
- `hawkinsoperations-validation/scripts/verify-ho-det-001-runtime-packet.py`
- `hawkinsoperations-validation/validation/successor/ho-det-001/reproducible-proof/`
- `HawkinsOperations/hawkinsoperations-validation#22`
- `docs/case-studies/PURPLE-TEAM-CLOSED-LOOP-001.md`

## Source Refs

- Detections merge commit: `13a74f812fd17027b4a1968b615a4aae78c99f51`
- Validation merge commit: `e3bcf6c087b8e22ea62c08438fae6a60e800b094`
- Validation enforcement PR: `HawkinsOperations/hawkinsoperations-validation#10`
- Validation enforcement merge commit: `8b48500d2ebbaacd93ac88e77a31dccf1d3b4e25`
- Platform runtime contract enforcement PR: `HawkinsOperations/hawkinsoperations-platform#5`
- Platform runtime contract enforcement merge commit: `b3d0ffbd66c1bd5f60f7e9ff99712cdc3e0595bd`
- Clone-runnable proof-pack PR: `HawkinsOperations/hawkinsoperations-validation#18`
- Controlled runtime packet verifier PR: `HawkinsOperations/hawkinsoperations-validation#22`
- Controlled runtime packet verifier merge commit: `b47dd02d08565baec76018f5ef909d1b7895737d`
- Controlled runtime packet verifier source commit: `4015c6acce044321fd6c3000f9be64e4b99c3550`
- Controlled runtime packet verifier path: `hawkinsoperations-validation/scripts/verify-ho-det-001-runtime-packet.py`
- Controlled runtime packet verifier verdict: `VERIFIED_CONTROLLED_LAB_RUNTIME_MATCH_CAPTURED`

## Clone-Runnable Public Proof Pack

- Public clone-run verifier: `hawkinsoperations-validation/scripts/verify-ho-det-001-reproducible-proof-pack.py`.
- Public fixture path: `hawkinsoperations-validation/validation/successor/ho-det-001/reproducible-proof/`.
- Scope: STRUCTURE_AND_BOUNDARY_ONLY / CONTROLLED_TEST_VALIDATED.
- Validation PR: `HawkinsOperations/hawkinsoperations-validation#18`.
- This does not prove runtime-active, signal-observed, public-safe runtime proof, live Splunk fired, Cribl-routed telemetry, Wazuh live collection, production-ready, fleet-wide, AWS-live, autonomous SOC, AI-approved disposition, or analyst-approved disposition.

## Validation Enforcement Status

- Validation enforcement status: CI_ENFORCED_FOR_CONTROLLED_TEST_SCOPE.
- Validation enforcement PR: `HawkinsOperations/hawkinsoperations-validation#10`.
- Validation enforcement merge commit: `8b48500d2ebbaacd93ac88e77a31dccf1d3b4e25`.
- Proof-loop workflow: `hawkinsoperations-validation/.github/workflows/ho-det-001-proof-loop.yml`.
- Enforcement scope: HO-DET-001 controlled-test validation, case-packet contract, deterministic triage boundary, claim-boundary scan, result parity, and proof-loop CI.
- Control boundary: This is a real control only for the exact checked controlled-test validation scope. It does not prove runtime-active, signal-observed, evidence-linked public proof, public-safe, production, fleet, Cribl, Wazuh, AWS-live, HO-GPU-01 runtime-active, autonomous SOC, or AI-approved disposition.

## Platform Runtime Contract Enforcement

- Platform runtime contract enforcement status: SATISFIED as a non-promotional guardrail.
- Platform enforcement PR: `HawkinsOperations/hawkinsoperations-platform#5`.
- Platform enforcement merge commit: `b3d0ffbd66c1bd5f60f7e9ff99712cdc3e0595bd`.
- Verifier output: `PLATFORM_RUNTIME_CONTRACT=pass`; `PROOF_CEILING=CONTROLLED_TEST_VALIDATED`; `PUBLIC_SAFE_STATUS=NOT_PUBLIC_SAFE`; `PROMOTION_STATUS=BLOCKED`; `RUNTIME_ACTIVE=false`; `SIGNAL_OBSERVED=false`; `AI_DECIDED_DISPOSITION=false`.
- Control boundary: This contract preserves the public ceiling at CONTROLLED_TEST_VALIDATED. It does not prove runtime-active status, signal-observed public proof, public-safe runtime proof, live Splunk fired, Splunk-proven Runtime Signal 001, Cribl-routed status, Wazuh-routed public proof, production-ready status, fleet-wide coverage, AWS-live status, autonomous SOC operation, AI-approved disposition, or analyst-approved disposition.

## Controlled Runtime Signal Packet 001

- Packet ID: `HO-DET-001_CONTROLLED_RUNTIME_SIGNAL_PACKET_001`.
- Private/internal status: CONTROLLED_LAB_RUNTIME_MATCH_VERIFIED.
- Public-safe status: NOT_PUBLIC_SAFE.
- Validation PR: `HawkinsOperations/hawkinsoperations-validation#22`.
- Validation merge commit: `b47dd02d08565baec76018f5ef909d1b7895737d`.
- Verifier path: `hawkinsoperations-validation/scripts/verify-ho-det-001-runtime-packet.py`.
- Verifier verdict: `VERIFIED_CONTROLLED_LAB_RUNTIME_MATCH_CAPTURED`.
- Private verifier output SHA256: `A405AE1DF92D639396A8D48C3F6DDE31DFCCBEA3F92E7DE0AFE0CDE87D8F56DC`.
- Packet hash manifest: present and verifier-confirmed for 28 of 28 referenced files.
- Marker correlation: manifest, local Sysmon telemetry, Splunk marker export, and HO-DET-001 result evidence.
- Match count: 2 controlled child Windows PowerShell EncodedCommand events tied to marker and search time window.
- Sanitization status: pass.
- Blocked-claim boundary scan: pass.
- Raw packet evidence status: private/internal only; private packet files were not committed publicly.
- Supported private/internal claim: "HO-DET-001 produced a controlled lab runtime match in Splunk."
- Boundary: This section records verifier-backed controlled lab runtime match evidence. It does not promote public-safe runtime proof, runtime-active deployment, production-ready status, fleet-wide status, Cribl-routed status, Wazuh-routed status, AWS-live status, autonomous SOC operation, AI-approved disposition, or analyst-approved disposition.

## Controlled Cribl-to-Splunk Marker Delivery Packet 001

- Internal status: CONTROLLED_LAB_CRIBL_TO_SPLUNK_MARKER_DELIVERY_VERIFIED.
- Public-safe status: NOT_PUBLIC_SAFE.
- Public proof ceiling: CONTROLLED_TEST_VALIDATED.
- Evidence custody: retained outside this repository in the Phase 4H/4I private packet. Local paths and raw capture names are intentionally omitted from this proof record.
- Marker digest: `sha256:8f061426e75134286ce958b74a7488d70d49960597b6f0c15b265f5fdd47649f`.
- Supported private/internal claim: "A controlled clean remote marker was delivered through the Cribl-to-Splunk lab lane and observed in expected Splunk rawdata with marker fields preserved."
- Boundary: This does not prove HO-DET-001/Sysmon telemetry is Cribl-routed, does not prove Cribl-routed telemetry for production or fleet scope, does not prove Wazuh live collection as public proof, does not prove live Splunk fired as public proof, does not prove public-safe runtime proof, and does not change the public proof ceiling.

## Supported Claim

"HO-DET-001 is CONTROLLED_TEST_VALIDATED through a public proof-loop workflow with controlled positive and negative test cases, deterministic pass/fail output, and blocked-claim enforcement."

"HO-DET-001 produced a controlled lab runtime match in Splunk."

"A controlled clean remote marker was delivered through the Cribl-to-Splunk lab lane and observed in expected Splunk rawdata with marker fields preserved."

## Unsupported Claims

- runtime-active
- signal-observed
- public-safe
- production-ready
- live Splunk fired
- Cribl-routed telemetry
- Cribl-routed
- Wazuh live collection
- Wazuh-routed
- AWS-live
- autonomous SOC
- production AutoSOC triage
- analyst-approved disposition
- HO-GPU-01 runtime-active
- AI-decided disposition
- AI-approved disposition

## Current Truth Table

| Claim | Truth label | Evidence/reference | Allowed wording | Blocked wording | Next promotion gate |
|---|---|---|---|---|---|
| HO-DET-001 proof packet exists in the proof repo. | PROVEN | `proof/records/HO-DET-001.md` | "A proof packet exists for HO-DET-001." | "The detection is production proven." | Keep proof current as gates change. |
| HO-DET-001 detection source exists. | PROVEN | `hawkinsoperations-detections/detections/successor/ho-det-001/rule.yml` | "Detection source exists for HO-DET-001." | "The detection is active." | Runtime deployment evidence. |
| HO-DET-001 Splunk source exists. | PROVEN | `hawkinsoperations-detections/detections/successor/ho-det-001/splunk.spl` at merge commit `13a74f812fd17027b4a1968b615a4aae78c99f51` | "A Splunk SPL source artifact exists for HO-DET-001." | "Live Splunk fired." | Deploy and preserve runtime/search evidence. |
| HO-DET-001 controlled-test validation passed. | PROVEN | `hawkinsoperations-validation/reports/ho-det-001/validation-result.json` at merge commit `e3bcf6c087b8e22ea62c08438fae6a60e800b094` | "HO-DET-001 is CONTROLLED_TEST_VALIDATED through controlled positive and negative process-creation test cases." | "This catches attacks." | Runtime and signal evidence. |
| HO-DET-001 public pipeline proof pack exists. | PROVEN | `hawkinsoperations-validation/reports/ho-det-001/pipeline-proof.md`; `hawkinsoperations-validation/reports/ho-det-001/pipeline-proof.json`; `HawkinsOperations/hawkinsoperations-validation#27`; merge commit `6d4e3ac7b284e380048e8e4f20edf50b6fa9bccb` | "HO-DET-001 is CONTROLLED_TEST_VALIDATED through a public proof-loop workflow with controlled positive and negative test cases, deterministic pass/fail output, and blocked-claim enforcement." | "This proves runtime-active, production-ready, fleet-wide, or public-safe runtime evidence status." | Runtime/signal/public-safe evidence review. |
| HO-DET-001 validation enforcement exists. | PROVEN | `hawkinsoperations-validation#10`; `.github/workflows/ho-det-001-proof-loop.yml`; merge commit `8b48500d2ebbaacd93ac88e77a31dccf1d3b4e25` | "HO-DET-001 validation enforcement exists for controlled-test scope." | "Validation enforcement proves runtime, signal, production, or public-safe status." | Runtime/signal/public-safe evidence review. |
| HO-DET-001 platform runtime contract enforcement exists. | PROVEN | `hawkinsoperations-platform#5`; `contracts/examples/ho-det-001-runtime-contract.sample.json`; merge commit `b3d0ffbd66c1bd5f60f7e9ff99712cdc3e0595bd` | "HO-DET-001 platform runtime contract enforcement exists as a non-promotional guardrail." | "Platform contract enforcement proves runtime-active, signal-observed, public-safe runtime proof, production-ready, fleet-wide, Cribl-routed, Wazuh-routed public proof, AWS-live, autonomous SOC, AI-approved disposition, or analyst-approved disposition." | Runtime/signal/public-safe evidence review. |
| HO-DET-001 controlled lab runtime match is verifier-backed. | PROVEN_PRIVATE_INTERNAL | `HawkinsOperations/hawkinsoperations-validation#22`; merge commit `b47dd02d08565baec76018f5ef909d1b7895737d`; verifier verdict `VERIFIED_CONTROLLED_LAB_RUNTIME_MATCH_CAPTURED` | "HO-DET-001 produced a controlled lab runtime match in Splunk." | "HO-DET-001 is runtime-active."; "HO-DET-001 has public-safe runtime proof."; "HO-DET-001 is production-ready."; "HO-DET-001 is fleet-wide."; "HO-DET-001 is Cribl-routed."; "HO-DET-001 is Wazuh-routed."; "HO-DET-001 is AWS-live."; "HO-DET-001 runs an autonomous SOC."; "AI approved the disposition."; "An analyst approved the disposition." | Public evidence linkage, privacy review, stale review, wording review, and Raylee approval. |
| Controlled clean Cribl-to-Splunk lab marker delivery is privately verified. | PROVEN_PRIVATE_INTERNAL | Phase 4H/4I private packet; marker digest `sha256:8f061426e75134286ce958b74a7488d70d49960597b6f0c15b265f5fdd47649f`; status `CONTROLLED_LAB_CRIBL_TO_SPLUNK_MARKER_DELIVERY_VERIFIED` | "A controlled clean remote marker was delivered through the Cribl-to-Splunk lab lane and observed in expected Splunk rawdata with marker fields preserved." | "HO-DET-001 is Cribl-routed."; "Cribl routed live telemetry."; "Live Splunk fired."; "HO-DET-001 is runtime-active."; "HO-DET-001 is production-ready."; "HO-DET-001 is fleet-wide."; "HO-DET-001 is public-safe." | Public evidence linkage, privacy review, stale review, wording review, and Raylee approval. |
| AutoSOC triage packet exists. | PROVEN | `hawkinsoperations-validation/validation/successor/ho-det-001/autosoc-triage-packet.json` | "A deterministic controlled-test triage packet was generated from the validation result." | "Production AutoSOC triage occurred." | Production AutoSOC run evidence. |
| Offline LLM support stub exists. | PROVEN | `hawkinsoperations-validation/validation/successor/ho-det-001/llm-summary.json` | "A deterministic blocked-runtime LLM support stub exists." | "HO-GPU-01 was runtime-active." | Approved local model runtime evidence. |
| HO-DET-001 runtime-active status is proven. | BLOCKED | No deployment, enablement, schedule, or backend state evidence linked. | "Runtime-active status requires deployment evidence." | "This detection is active." | Preserve runtime deployment evidence. |
| HO-DET-001 signal-observed status is proven. | BLOCKED | No preserved telemetry, alert, log, or search output linked. | "Signal-observed status requires preserved telemetry, alert, log, or search output." | "This catches attacks." | Preserve signal observation evidence. |
| HO-DET-001 public-safe status is approved. | BLOCKED | No reviewed public wording, privacy review, stale review, evidence linkage, or Raylee approval. | "Public-safe status requires reviewed wording, privacy review, stale review, evidence linkage, and Raylee approval." | "HO-DET-001 is PUBLIC_SAFE." | Raylee approval after evidence and claim review. |

## Validation Summary

- Validation status: pass
- Total controlled cases: 14
- Matched positive count: 7
- Negative cases not matched: 7
- Missed positive cases: none
- False-positive negative cases: none
- Validation scope: synthetic process-creation fixtures only
- Validation scope: controlled process-creation test cases only
- Validation result path: `hawkinsoperations-validation/reports/ho-det-001/validation-result.json`

## AutoSOC Summary

- Packet ID: HO-DET-001-SYNTHETIC-TRIAGE-001
- Scope: deterministic controlled-test output only
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

- Status: SATISFIED for controlled-test scope
- Evidence: `hawkinsoperations-validation/validation/successor/ho-det-001/validation-cases.json`.

### CONTROLLED_TEST_VALIDATED

- Status: SATISFIED
- Evidence: `hawkinsoperations-validation/reports/ho-det-001/validation-result.json`.
- Supported claim: "HO-DET-001 is CONTROLLED_TEST_VALIDATED through a public proof-loop workflow with controlled positive and negative test cases, deterministic pass/fail output, and blocked-claim enforcement."

### CONTROLLED_LAB_RUNTIME_MATCH_VERIFIED

- Status: SATISFIED_PRIVATE_INTERNAL.
- Evidence: `HawkinsOperations/hawkinsoperations-validation#22`, merge commit `b47dd02d08565baec76018f5ef909d1b7895737d`, and verifier `hawkinsoperations-validation/scripts/verify-ho-det-001-runtime-packet.py`.
- Verifier verdict: `VERIFIED_CONTROLLED_LAB_RUNTIME_MATCH_CAPTURED`.
- Private verifier output SHA256: `A405AE1DF92D639396A8D48C3F6DDE31DFCCBEA3F92E7DE0AFE0CDE87D8F56DC`.
- Match count: 2 controlled child Windows PowerShell EncodedCommand events tied to marker and search time window.
- Supported claim: "HO-DET-001 produced a controlled lab runtime match in Splunk."
- Public ceiling boundary: Current public label and trust class remain CONTROLLED_TEST_VALIDATED until public-safe evidence linkage, privacy review, stale review, wording review, and Raylee approval are complete.

### CONTROLLED_LAB_CRIBL_TO_SPLUNK_MARKER_DELIVERY_VERIFIED

- Status: SATISFIED_PRIVATE_INTERNAL.
- Evidence: Phase 4H/4I private packet retained outside this repository, marker digest `sha256:8f061426e75134286ce958b74a7488d70d49960597b6f0c15b265f5fdd47649f`, and status `CONTROLLED_LAB_CRIBL_TO_SPLUNK_MARKER_DELIVERY_VERIFIED`.
- Supported claim: "A controlled clean remote marker was delivered through the Cribl-to-Splunk lab lane and observed in expected Splunk rawdata with marker fields preserved."
- Boundary: This does not prove HO-DET-001/Sysmon telemetry is Cribl-routed, does not prove Cribl-routed telemetry for production or fleet scope, does not prove Wazuh live collection as public proof, does not prove live Splunk fired as public proof, does not prove runtime-active deployment, does not prove production-ready status, does not prove fleet-wide status, does not prove public-safe runtime proof, and does not change the public proof ceiling.

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
- "HO-DET-001 has merged controlled-test validation artifacts in the validation repository."
- "HO-DET-001 is CONTROLLED_TEST_VALIDATED through a public proof-loop workflow with controlled positive and negative test cases, deterministic pass/fail output, and blocked-claim enforcement."
- "HO-DET-001 produced a controlled lab runtime match in Splunk."
- "A controlled clean remote marker was delivered through the Cribl-to-Splunk lab lane and observed in expected Splunk rawdata with marker fields preserved."
- "HO-DET-001 platform runtime contract enforcement exists as a non-promotional guardrail."
- "A deterministic controlled-test AutoSOC triage packet was generated from the HO-DET-001 validation result."
- "The offline LLM support artifact is a deterministic blocked-runtime stub and does not prove HO-GPU-01 runtime."

## Blocked Claims

- "This detection is active."
- "This catches attacks."
- "This proves coverage."
- "This is production-ready."
- "This is public-safe."
- "Live Splunk fired."
- "Cribl routed live telemetry."
- "HO-DET-001 is Cribl-routed."
- "Wazuh collected live telemetry."
- "HO-DET-001 is Wazuh-routed."
- "HO-DET-001 is AWS-live."
- "HO-DET-001 runs an autonomous SOC."
- "Production AutoSOC triage occurred."
- "An analyst approved the disposition."
- "AI approved the disposition."
- "HO-GPU-01 ran the model."
- "AI decided the disposition."
- "The website proves detection status."
- "Original detections are now successor detections."

## Next Promotion Gate

The next promotion gate is proof-record review of the controlled lab runtime match and controlled Cribl-to-Splunk marker-delivery updates, followed by public evidence linkage, privacy review, stale review, wording review, and Raylee approval. Public proof and website updates remain blocked until those reviews are complete. Runtime-active deployment remains a separate blocked claim requiring deployment or enablement proof.
