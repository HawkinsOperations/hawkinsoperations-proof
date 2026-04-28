# HO-DET-001 — Suspicious PowerShell EncodedCommand Execution via Sysmon Event ID 1

## Header

- Detection ID: HO-DET-001
- Detection title: HO-DET-001 — Suspicious PowerShell EncodedCommand Execution via Sysmon Event ID 1
- Proof packet status: SOURCE_EXISTS as a draft record in the proof repo
- Current proof level: 1 SOURCE_EXISTS
- Current trust class: SOURCE_EXISTS
- Public-safe status: NOT_PUBLIC_SAFE
- Approval status: NOT_APPROVED

This packet is a governed proof-lifecycle demonstration showing how HawkinsOperations separates source, validation, runtime, signal, evidence, and public claims before promoting a detection. It is not a novelty claim and does not assert end-to-end detection proof.

## Status Clarification

- Proof packet status: SOURCE_EXISTS as a draft record in the proof repo.
- Detection proof level: 1 SOURCE_EXISTS.
- Detection trust class: SOURCE_EXISTS.
- Canonical detection source: `hawkinsoperations-detections/detections/successor/ho-det-001/rule.yml`.
- Canonical validation path: UNKNOWN.
- Runtime-active status: UNKNOWN.
- Signal-observed status: UNKNOWN.
- Evidence-linked status: UNKNOWN.
- Public-safe status: NOT_PUBLIC_SAFE.
- Approval status: NOT_APPROVED.

The proof packet itself exists as a draft proof packet. The canonical HO-DET-001 source artifact exists in the detection source repository. Related HOD-001 encoded-command artifacts may inform future review, but they are not HO-DET-001 truth. Current detection proof level is limited to SOURCE_EXISTS until static review, validation, runtime, signal, evidence-linkage, and public-safe gates are satisfied.

## Detection identity

- Detection ID: HO-DET-001
- Detection title: HO-DET-001 — Suspicious PowerShell EncodedCommand Execution via Sysmon Event ID 1
- Threat behavior: PowerShell or pwsh process execution using encoded command flags or encoded payload patterns.
- Data source: Windows process creation telemetry, expected Sysmon Event ID 1 when available.
- Backend target: UNKNOWN; expected targets may include SIEM/search or detection backend after source owner defines implementation.
- MITRE mapping if known: INFERRED candidate mapping to Command and Scripting Interpreter: PowerShell (T1059.001). This is not promoted for HO-DET-001 until source and review exist under successor proof rules.
- Source owner repo: hawkinsoperations-detections
- Validation owner repo: hawkinsoperations-validation
- Proof owner repo: hawkinsoperations-proof
- Public rendering owner: hawkinsoperations-website

## Current truth table

| Claim | Truth label | Evidence/reference | Allowed wording | Blocked wording | Next promotion gate |
|---|---|---|---|---|---|
| HO-DET-001 proof packet exists in the proof repo. | PROVEN | proof/records/HO-DET-001.md | "A draft proof packet exists for HO-DET-001." | "The detection is proven." | Identify source path and owner review. |
| HO-DET-001 detection source exists. | PROVEN | hawkinsoperations-detections/detections/successor/ho-det-001/rule.yml | "Detection source exists for HO-DET-001." | "The detection is active." | Static review against source and rule contract. |
| A related encoded-command baseline exists under HOD-001. | INFERRED | Read-only search found HOD-001 encoded-command artifacts in related repos. | "Related HOD-001 artifacts may inform review but do not automatically become HO-DET-001 truth." | "HOD-001 is HO-DET-001." | Reclassify or map through successor governance. |
| HO-DET-001 static review has passed. | UNKNOWN | No static review record for HO-DET-001 found. | "Static review is required." | "This passed static validation." | Static review against source and rule contract. |
| HO-DET-001 test definition exists. | UNKNOWN | No HO-DET-001 validation plan found in related validation repo. | "Validation plan is not yet proven for HO-DET-001." | "A validation plan is defined." | Create or identify positive and negative tests. |
| HO-DET-001 validation result exists. | UNKNOWN | No HO-DET-001 validation result found. | "Validation result is not yet proven for HO-DET-001." | "The detection passed validation." | Run validation and preserve output. |
| HO-DET-001 runtime-active status is proven. | UNKNOWN | No deployment, enablement, schedule, or backend state evidence linked. | "Runtime-active status requires deployment evidence." | "This detection is active." | Preserve runtime deployment evidence. |
| HO-DET-001 signal-observed status is proven. | UNKNOWN | No preserved telemetry, alert, log, or search output linked. | "Signal-observed status requires preserved telemetry, alert, log, or search output." | "This catches attacks." | Preserve signal observation evidence. |
| HO-DET-001 evidence-linked status is proven. | UNKNOWN | This packet contains no promoted evidence item linking source, validation, runtime, or signal. | "Evidence linkage is pending." | "HO-DET-001 is evidence-linked." | Add reviewed evidence item IDs and claim linkage. |
| HO-DET-001 public-safe status is approved. | BLOCKED | No reviewed public wording, privacy review, stale review, evidence linkage, or Raylee approval. | "Public-safe status requires reviewed wording, privacy review, stale review, evidence linkage, and Raylee approval." | "HO-DET-001 is PUBLIC_SAFE." | Raylee approval after evidence and claim review. |

## Proof level assessment

### 0 IDEA

- Status: SATISFIED
- Evidence required: Detection identity and intended proof-lifecycle scope.
- Current evidence: This proof packet defines HO-DET-001 as a governed proof-lifecycle demonstration.
- Promotion gate: Identify canonical source in hawkinsoperations-detections.
- Blocked claim if not satisfied: "This detection has source."

### 1 SOURCE_EXISTS

- Status: SATISFIED
- Evidence required: Canonical source file path, source owner repo, commit or stable reference, and source review context.
- Current evidence: `hawkinsoperations-detections/detections/successor/ho-det-001/rule.yml`.
- Promotion gate: Complete static review against the source artifact and rule contract.
- Blocked claim if not satisfied: "Detection source exists."

### 2 STATIC_VALIDATED

- Status: NOT_SATISFIED
- Evidence required: Static review record showing structural coherence, expected fields, ATT&CK mapping review if used, data source assumptions, and backend compatibility.
- Current evidence: UNKNOWN; no HO-DET-001 static review record linked.
- Promotion gate: Complete static review after source exists.
- Blocked claim if not satisfied: "This passed static review."

### 3 TEST_DEFINED

- Status: NOT_SATISFIED
- Evidence required: Positive and negative test cases, expected match behavior, expected non-match behavior, and validation owner path.
- Current evidence: UNKNOWN; no HO-DET-001 validation plan linked.
- Promotion gate: Define validation cases in hawkinsoperations-validation.
- Blocked claim if not satisfied: "A validation check is defined."

### 4 TEST_VALIDATED

- Status: NOT_SATISFIED
- Evidence required: Recorded validation execution result, timestamp, owner, environment, pass/fail output, and preserved result path.
- Current evidence: UNKNOWN; no HO-DET-001 validation result linked.
- Promotion gate: Run validation and preserve output.
- Blocked claim if not satisfied: "This passed validation."

### 5 RUNTIME_ACTIVE

- Status: NOT_SATISFIED
- Evidence required: Deployment or enablement proof, backend/platform identifier sanitized for public use, timestamp, owner, currentness review, and stale review date.
- Current evidence: UNKNOWN; no runtime evidence linked.
- Promotion gate: Preserve deployment evidence from platform owner.
- Blocked claim if not satisfied: "This detection is active."

### 6 SIGNAL_OBSERVED

- Status: NOT_SATISFIED
- Evidence required: Preserved telemetry, alert, log, or search output showing the signal, with context, time window, query or rule reference, and redaction review.
- Current evidence: UNKNOWN; no signal evidence linked.
- Promotion gate: Preserve signal observation and context.
- Blocked claim if not satisfied: "This catches attacks" or "A signal was observed."

### 7 EVIDENCE_LINKED

- Status: NOT_SATISFIED
- Evidence required: Evidence item IDs, evidence owner, artifact path or redacted reference, supported claim, unsupported claim, privacy status, stale review status, and promotion status.
- Current evidence: UNKNOWN; no evidence item is promoted for HO-DET-001.
- Promotion gate: Link reviewed source, validation, runtime, and signal evidence as available.
- Blocked claim if not satisfied: "HO-DET-001 is evidence-linked."

### 8 PUBLIC_SAFE

- Status: BLOCKED
- Evidence required: Approved claim text, evidence path, trust class, allowed wording, blocked wording, stale review date, privacy review, public claim review, and Raylee approval.
- Current evidence: No approval evidence exists in this packet.
- Promotion gate: Raylee approval after evidence linkage and public-safe review.
- Blocked claim if not satisfied: "HO-DET-001 is PUBLIC_SAFE."

## Trust class assessment

- Current trust class: SOURCE_EXISTS
- Reason: The proof packet exists and the canonical source path is identified, but static validation, test definition, test result, runtime evidence, signal observation, evidence linkage, and public approval are not proven for HO-DET-001.
- What would promote it: A logged static review against the canonical source and rule contract could promote the detection claim to STATIC_VALIDATED.
- What would block promotion: Missing source path, missing owner, private or unsafe details, stale or unreviewed evidence, unlogged changes, or any attempt to self-promote through AI output.

## Source truth

- Known source path: `hawkinsoperations-detections/detections/successor/ho-det-001/rule.yml`.
- Source path status: SOURCE_EXISTS.
- Source owner repo: hawkinsoperations-detections.
- What source existence supports: Only that a source artifact exists at a known path under the source owner repo.
- What source existence does not support: Runtime activity, validation success, signal observation, evidence linkage, public-safe status, or production readiness.

Related HOD-001 encoded-command files may inform review, but those files are not promoted as HO-DET-001 source truth by copy, similarity, or AI interpretation.

## Validation truth

- Known validation path if proven: UNKNOWN.
- Expected validation path if not proven: hawkinsoperations-validation should own HO-DET-001 validation cases and result outputs after definition.
- Positive test expectation: A process creation event for PowerShell or pwsh using an encoded command flag should match when the canonical source rule defines that behavior.
- Negative test expectation: Benign process creation events without encoded command behavior, or allowed administrative patterns if defined by tuning, should not match.
- Validation output requirement: Preserved pass/fail output with timestamp, validation owner, command or harness reference, result path, and hash or integrity reference if available.
- What validation supports: Test definition or test result only within the recorded scope.
- What validation does not support: Runtime deployment, ongoing signal observation, public-safe approval, or broad coverage claims.

Read-only inspection found related HOD-001 validation artifacts in hawkinsoperations-validation, but no HO-DET-001 validation path or result was found.

## Runtime truth

- Required deployment evidence: Deployment, enablement, schedule, or backend configuration evidence from the platform owner, sanitized before public use.
- Required platform/backend proof: Backend target, rule identifier, deployment state, owner, timestamp, and stale review date.
- Required timestamp/currentness: Runtime evidence must include collection date/time and must be reviewed for currentness before promotion.
- Current runtime status: UNKNOWN.
- Blocked runtime claims: "This detection is active", "This is production-ready", "This proves coverage", and "The repo proves runtime behavior."

## Signal truth

- Required event/log/search/alert evidence: Preserved telemetry, alert, log, or search output showing HO-DET-001 behavior under the governed source and runtime context.
- Required preserved context: Query or rule reference, event fields needed for review, time window, test or live context label, owner, and redaction/privacy status.
- Required evidence format: Redacted artifact, evidence ledger entry, or proof record with stable evidence item ID and claim linkage.
- Current signal status: UNKNOWN.
- Blocked signal claims: "This catches attacks", "Signal was observed", "The detection validated runtime behavior", and "The successor system has validated detections."

## Evidence truth

| Evidence item ID | Evidence type | Evidence owner | Supports which claim | Does not support which claim | Privacy status | Stale review status | Promotion status |
|---|---|---|---|---|---|---|---|
| HO-DET-001-PACKET-001 | Draft proof packet | hawkinsoperations-proof | A governed proof packet exists and defines required boundaries. | Test passed, runtime active, signal observed, evidence-linked, public-safe. | Public-safe candidate wording only; no private terms intentionally included. | Review required before any public use. | DRAFT |
| HO-DET-001-SOURCE-001 | Source artifact | hawkinsoperations-detections | Source exists at `detections/successor/ho-det-001/rule.yml`. | Runtime activity, validation success, signal observation, public-safe status. | No private terms intentionally included. | Review required before further promotion. | SOURCE_EXISTS |
| HO-DET-001-VALIDATION-001 | Validation plan/result | hawkinsoperations-validation | UNKNOWN; no HO-DET-001 validation linked. | Runtime activity, signal observation, public-safe status. | UNKNOWN | UNKNOWN | NOT_PROMOTED |
| HO-DET-001-RUNTIME-001 | Runtime deployment evidence | platform owner | UNKNOWN; no runtime evidence linked. | Signal observation, public-safe status. | UNKNOWN | UNKNOWN | NOT_PROMOTED |
| HO-DET-001-SIGNAL-001 | Telemetry/search/alert evidence | evidence owner to be assigned | UNKNOWN; no signal evidence linked. | Public-safe status without review and approval. | UNKNOWN | UNKNOWN | NOT_PROMOTED |

## Public proof / public-safe review

- Candidate public wording: "HO-DET-001 demonstrates the HawkinsOperations successor promotion path for a single detection. Current status is limited to source existence and the evidence linked in this proof packet. Runtime-active, signal-observed, evidence-linked, and public-safe claims require separate preserved evidence and review."
- Sanitization status: No private opportunity terms, hostnames, IP addresses, raw logs, secrets, screenshots, or local machine paths are intentionally included in candidate public wording.
- Stale review status: NOT_REVIEWED.
- Claim review status: NOT_REVIEWED.
- Approval status: NOT_APPROVED.

## Allowed claims

- "A draft proof packet exists for HO-DET-001."
- "Detection source exists for HO-DET-001."
- "HO-DET-001 demonstrates the HawkinsOperations successor promotion path for a single detection. Current status is limited to source existence and the evidence linked in this proof packet. Runtime-active, signal-observed, evidence-linked, and public-safe claims require separate preserved evidence and review."
- "Runtime-active status requires deployment evidence."
- "Signal-observed status requires preserved telemetry, alert, log, or search output."
- "Public-safe status requires reviewed wording, privacy review, stale review, evidence linkage, and Raylee approval."

## Blocked claims

- "This detection is active."
- "This catches attacks."
- "This proves coverage."
- "This is production-ready."
- "This is public-safe."
- "The successor system has validated detections."
- "AI validated this."
- "The repo proves runtime behavior."
- "The website proves detection status."
- "Original detections are now successor detections."
- "HO-DET-001 is evidence-linked."
- "HO-DET-001 is PUBLIC_SAFE."

## Next promotion gate

The next promotion gate is STATIC_VALIDATED: complete a source review against `hawkinsoperations-detections/detections/successor/ho-det-001/rule.yml` and the rule contract without claiming runtime, signal, evidence-linked, or public-safe status.
