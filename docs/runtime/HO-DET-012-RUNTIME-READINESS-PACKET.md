# HO-DET-012 Runtime Readiness Packet

## Objective

Prepare HO-DET-012 for a future private runtime proof run using the HO-DET-011 runtime proof pattern, without generating a scheduled-task event in this run.

This packet is readiness material only. It does not create runtime evidence, query Wazuh, update proof status, update the proof index, update the website, or approve public-safe wording.

Future runtime event approval phrase:

`HO_DET_012_PRIVATE_RUNTIME_EVENT_APPROVED`

## Current Truth State

| Field | Current state |
| --- | --- |
| Detection ID | HO-DET-012 |
| Detection title | Suspicious Scheduled Task Creation |
| Source status | SOURCE_EXISTS |
| Source surfaces | Sigma-style YAML, Splunk SPL, Wazuh XML, event mapping, README, status metadata |
| Validation status | CONTROLLED_TEST_VALIDATED |
| Validation cases | 8 total: 4 positive, 4 negative |
| Validation misses | 0 missed positives |
| Validation false-positive negatives | 0 |
| ATT&CK mapping | T1053.005 Scheduled Task; Persistence and Privilege Escalation |
| Proof record | `proof/records/HO-DET-012.md` |
| Proof card | `proof/cards/HO-DET-012.md` |
| Runtime evidence | NOT_CAPTURED / NOT_PROVEN |
| Signal evidence | NOT_PROVEN |
| Public-safe status | NOT_PUBLIC_SAFE |
| Website status | Website references are validation/public-boundary display only and are not proof |
| Data runtime evidence | No HO-DET-012 runtime evidence directory observed during readiness discovery |

Platform readiness is conditional. The platform factory includes HO-DET-012 controlled-test status and private runtime receipt review support, but a read-only factory status command currently reports proof-index drift for the HO-DET-012 proof record path. That drift should be resolved before treating the platform lane as clean runtime-ready.

## Source Files Inspected

- `hawkinsoperations-detections/detections/successor/ho-det-012/README.md`
- `hawkinsoperations-detections/detections/successor/ho-det-012/rule.yml`
- `hawkinsoperations-detections/detections/successor/ho-det-012/splunk.spl`
- `hawkinsoperations-detections/detections/successor/ho-det-012/wazuh.xml`
- `hawkinsoperations-detections/detections/successor/ho-det-012/event-mapping.yml`
- `hawkinsoperations-detections/detections/successor/ho-det-012/status.yml`
- `hawkinsoperations-validation/validation/successor/ho-det-012/validation-cases.json`
- `hawkinsoperations-validation/reports/ho-det-012/validation-result.json`
- `hawkinsoperations-validation/validation/successor/ho-det-012/README.md`
- `hawkinsoperations-proof/proof/records/HO-DET-012.md`
- `hawkinsoperations-proof/proof/cards/HO-DET-012.md`
- `hawkinsoperations-proof/docs/boundaries/HO-DET-012-RUNTIME-EVIDENCE-GATE.md`
- `hawkinsoperations-proof/proof/indexes/DETECTION_PROOF_STATUS_INDEX.yml`

## Expected Telemetry

Expected Windows event IDs:

- Windows Security Event ID 4698 for scheduled task creation where audit policy and collection support it.
- Windows Security Event ID 4702 for scheduled task update where audit policy and collection support it.
- Microsoft-Windows-TaskScheduler/Operational Event ID 106 for task registration where enabled and collected.
- Microsoft-Windows-TaskScheduler/Operational Event ID 140 for task update where enabled and collected.

Expected Sysmon ID:

- Sysmon Event ID 1 for process context when the task is created through scheduled-task tooling and Sysmon is present.

Telemetry availability is not proof by itself. The future runtime packet must record exactly which local and Wazuh-backed events were observed for the approved run.

## Safe Event Design

The proposed future runtime event is one controlled scheduled-task creation followed by deterministic cleanup.

Design constraints:

- Use a unique run ID and correlation ID.
- Use a task name containing the correlation ID in the private run only.
- Use one benign Windows-native action.
- Do not run the task intentionally.
- Do not use malware, credential access, stealth, evasion, persistence beyond the controlled temporary task, production-like names, or private operational names.
- Do not leave the task installed.
- Store the exact command and raw telemetry only in private evidence storage outside public repos.

Proposed benign task action:

`C:\Windows\System32\cmd.exe /c exit 0`

Rationale:

- It is Windows-native.
- It has no external network dependency.
- It does not create a payload file.
- It is harmless if accidentally executed.
- It provides scheduled-task action context that can exercise the detection safely.

The future run should create the task for a future one-time schedule and should not intentionally start it. The runtime proof objective is task creation telemetry, not task execution.

## Wazuh Query Plan

The Wazuh path can reuse the same private Windows lab agent route used by the HO-DET-011 runtime pattern only after a future preflight confirms the route is still reachable and read-only archive/alert queries work.

Public or repo text must not expose raw Wazuh lines, internal hostnames, internal addresses, usernames, private paths, exact task names, exact correlation markers, or raw event payloads.

Future private query requirements:

- Query Wazuh archives and alerts read-only.
- Match the private agent name recorded in the private receipt.
- Match the private correlation ID.
- Match one or more of Event IDs 4698, 4702, 106, 140, or Sysmon 1.
- Save raw results only under the private runtime evidence directory.
- Hash every raw and sanitized evidence file.
- Record count-only public-safe summaries separately from raw telemetry.

Splunk remains NOT_VERIFIED unless separately approved and tested. This readiness packet does not claim Splunk observation.

## Expected Evidence

A successful future private runtime run should preserve:

- Private run metadata: run ID, correlation ID, start time, end time, operator approval phrase, host class, and non-production/lab scope.
- Source version metadata for detection, validation, proof, and platform references.
- Exact private scheduled-task creation command.
- Local telemetry summary with counts for relevant Windows and Sysmon event IDs.
- Raw local event evidence stored privately.
- Private Wazuh archive/alert query result files.
- Wazuh count summary for matching agent, correlation ID, and expected event IDs.
- Cleanup command and cleanup verification evidence.
- Hash manifest for all private evidence files.
- Deterministic verifier output.
- Explicit flags: `raw_private_evidence_public=false`, `ai_decided_disposition=false`, and `human_review_required=true`.

Minimum future runtime success criteria:

- The task creation command succeeds, or local event logs prove the controlled creation attempt was recorded.
- Local telemetry includes at least one expected scheduled-task or process event carrying the private correlation marker.
- Wazuh archives or alerts include the private agent, correlation marker, and at least one expected event ID.
- Cleanup confirms the scheduled task is absent.
- Raw evidence remains private.
- Verifier passes.

## Cleanup Plan

The future run must delete the controlled scheduled task immediately after telemetry capture.

Cleanup requirements:

- Delete only the uniquely named task created for the approved run.
- Confirm the task no longer exists after deletion.
- Record cleanup command privately.
- Record cleanup verification privately.
- Stop hard if deletion fails or if task absence cannot be confirmed.

No scheduled task may be left installed.

## Private Receipt Fields

The future private runtime receipt should include:

- `schema_version`
- `detection_id`
- `run_id`
- `correlation_id`
- `approval_phrase`
- `event_design`
- `benign_task_action`
- `task_name_private`
- `event_generation_result`
- `local_event_counts`
- `expected_event_ids`
- `sysmon_event_ids`
- `wazuh_agent_name_private`
- `wazuh_archive_match_count`
- `wazuh_alert_match_count`
- `splunk_status`
- `cleanup_result`
- `cleanup_absent_confirmed`
- `evidence_files`
- `hash_manifest`
- `runtime_verifier_result`
- `raw_private_evidence_public`
- `ai_decided_disposition`
- `human_review_required`
- `public_safe_status`
- `blocked_claims`

The receipt itself is private evidence and must not be committed to a repo.

## Verifier Design

Needed verifier files:

- `hawkinsoperations-validation/scripts/verify-ho-det-012-runtime-receipt.py`
- `hawkinsoperations-validation/validation/successor/ho-det-012/runtime-receipt.schema.json`
- `hawkinsoperations-validation/validation/successor/ho-det-012/runtime-receipt.sample.redacted.json`
- `hawkinsoperations-validation/validation/successor/ho-det-012/README.md`

Verifier requirements:

- Validate receipt schema.
- Require `detection_id=HO-DET-012`.
- Require run ID and correlation ID.
- Require expected event IDs to be drawn only from 4698, 4702, 106, 140, and Sysmon 1.
- Require cleanup confirmation.
- Require Wazuh observation fields for private runtime success.
- Require Splunk to remain NOT_VERIFIED unless separately evidenced.
- Require raw-private-evidence-public to be false.
- Require AI disposition to be false.
- Require human review to be true.
- Reject production, fleet-wide, autonomous SOC, public-safe, AI-approved, and analyst-approved claims.
- Verify hashes for referenced private evidence files when the verifier is run in the private evidence environment.

## Proof Review Packet Plan

Needed proof review files after private runtime evidence exists:

- `hawkinsoperations-proof/docs/runtime/HO-DET-012-RUNTIME-CORROBORATION-REVIEW.md`
- `hawkinsoperations-proof/docs/runtime/HO-DET-012-PUBLIC-SAFE-DECISION-GATE.md`

Potential future proof files only after explicit approval:

- `hawkinsoperations-proof/proof/runtime/HO-DET-012-RUNTIME-CORROBORATION.md`
- `hawkinsoperations-proof/proof/records/HO-DET-012.md`
- `hawkinsoperations-proof/proof/indexes/DETECTION_PROOF_STATUS_INDEX.yml`

The first public-safe review packet should answer:

- What private evidence exists.
- What can be summarized publicly.
- What must stay private.
- Which exact wording is allowed.
- Which exact wording is forbidden.
- Whether public-safe status remains NOT_PUBLIC_SAFE or can be considered for a later human approval gate.
- Whether the website remains blocked.

## Public-Safe Blocker Forecast

Default forecast after private runtime capture:

`PRIVATE_RUNTIME_PROOF_CAPTURED_PUBLIC_BLOCKED`

Expected blockers:

- Raw Wazuh lines must remain private.
- Raw Windows event payloads must remain private.
- Private host, user, path, task name, correlation marker, and internal route details must remain private.
- The exact scheduled task name should remain private unless a later review explicitly classifies it as safe.
- Splunk observation remains blocked unless separately verified.
- Website publication remains blocked unless a later public-safe decision gate approves exact wording.
- Public wording must not claim runtime-active deployment, public signal-observed proof, production readiness, fleet-wide coverage, autonomous SOC, AI-approved disposition, or analyst-approved disposition.

Candidate public wording before approval should remain no stronger than:

`HO-DET-012 is controlled-test validated for scheduled-task creation and update fixtures. A private runtime proof run is designed but not yet executed. Public-safe runtime publication remains blocked pending private evidence capture, verifier review, and human approval.`

## Stop Conditions

Stop before runtime work if:

- Future approval phrase is missing.
- The shell is not in the expected admin/elevated context for the approved runtime action.
- The scheduled-task action would execute unsafe behavior.
- The task name is production-like or misleading.
- Cleanup is not deterministic.
- Wazuh route preflight fails.
- Local event telemetry is unavailable.
- Raw evidence would enter a repo or public output.
- Splunk wording would be needed without Splunk evidence.
- Platform factory drift remains unresolved and the run depends on platform readiness.
- Public wording would overclaim runtime, signal, public-safe, production, fleet-wide, autonomous SOC, AI-approved, or analyst-approved status.

## Readiness Decision

HO-DET-012 is a strong next private runtime candidate after HO-DET-011, but it is not yet runtime-ready for execution.

Readiness state:

`READY_FOR_PRIVATE_RUNTIME_DESIGN_REVIEW`

Current blockers before event generation:

- Future runtime action requires explicit approval with `HO_DET_012_PRIVATE_RUNTIME_EVENT_APPROVED`.
- Wazuh route must be preflighted read-only in the future run.
- Platform factory proof-index drift should be resolved or explicitly waived before treating the platform lane as clean.
- Runtime receipt verifier files do not exist yet.
- Public-safe review packet does not exist yet.
- Website remains blocked.

