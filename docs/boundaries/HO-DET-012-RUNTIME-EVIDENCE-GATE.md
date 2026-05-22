# HO-DET-012 Runtime Evidence Gate

## Purpose

This document defines the control gate for any future HO-DET-012 runtime evidence work.

It is design guidance only. It does not execute runtime capture, create evidence, update proof records, update proof indexes, or approve public-safe wording.

## Current Proven State

| Field | Current state |
| --- | --- |
| Detection | HO-DET-012 Suspicious Scheduled Task Creation |
| Proof record | `proof/records/HO-DET-012.md` exists |
| Proof card | `proof/cards/HO-DET-012.md` exists |
| Proof index | `proof/indexes/DETECTION_PROOF_STATUS_INDEX.yml` records HO-DET-012 |
| Proof ceiling | `CONTROLLED_TEST_VALIDATED` |
| Controlled validation | 8 total cases, 4 positive, 4 negative |
| Missed positives | 0 |
| False-positive negatives | 0 |
| Runtime state | `NOT_PROVEN`; runtime-active remains blocked until a separately approved capture proves a scoped runtime fact |
| Signal state | `NOT_PROVEN`; signal-observed remains blocked until a separately approved telemetry or alert route proves a scoped signal fact |
| Public-safe state | `NOT_PUBLIC_SAFE`; public-safe runtime remains blocked until separate public-safe review and approval |

The current proof ceiling remains `CONTROLLED_TEST_VALIDATED` unless a later approved proof update changes it.

## Evidence Required Before Any Runtime Claim

A future runtime gate may proceed only after a separate approval explicitly authorizes the capture. Before any proof update is eligible, the evidence packet must include:

- Approved lab target scope, including the host class, non-production status, and operator approval for the test window.
- Approved benign scheduled-task creation or update scenario, including cleanup expectations and a statement that the scenario is reversible.
- Timestamped private raw evidence stored outside the proof repo under an approved evidence route.
- Sanitized evidence summary that removes private hostnames, internal addresses, usernames, secrets, tokens, and nonessential local paths.
- Command transcript or operator receipt showing what was intentionally executed and when, without exposing private material in public or repo text.
- Hash manifest for raw and sanitized materials.
- Source provenance for the detection files, validation result, proof record, and this gate document.
- Stale-state review confirming the detection source, validation truth, and proof index state were current at capture time.
- Privacy and redaction review before any summary is considered for repo or public use.
- Wording review confirming that any proposed claim stays inside the evidence scope.
- Human approval before any proof record, proof card, proof index, release note, website, or public surface is changed.

Expected candidate event sources for this detection are:

- Windows Security event ID 4698 or 4702 where audit policy and collection support those events.
- Microsoft-Windows-TaskScheduler/Operational event ID 106 or 140 where that channel is enabled.
- Sysmon event ID 1 for process context where Sysmon is present and configured.

The packet must document which source was used. Availability of a source is not evidence by itself.

## Eligible Claim After Approved Capture

If a future approved capture produces verified, reviewable, private evidence, the maximum candidate claim eligible for later review is:

`HO-DET-012 has private, controlled lab runtime evidence for one benign scheduled-task test within the approved evidence packet scope.`

That sentence is not claimed by this document. It is only the narrow claim that could become eligible after capture, verification, redaction, stale review, wording review, and human approval.

Signal wording requires separate evidence. A runtime event on a host does not prove that a SIEM, pipeline, or alert route observed the signal.

## Claims That Remain Blocked

Even after a private runtime packet exists, the following claims remain blocked unless separately proven, reviewed, and approved:

- runtime-active as a broad deployment or public proof claim.
- signal-observed unless a separate telemetry or alert route is captured and reviewed.
- public-safe runtime until a separate public-safe review approves exact wording and redaction.
- production-ready.
- autonomous SOC.
- AI-approved disposition.
- analyst-approved disposition.
- live Splunk.
- live Wazuh.
- live Cribl.
- Security Onion observed proof.
- Fleet-wide coverage or scheduled-task coverage completeness.
- Containment, closure, response automation, or suppression execution.

Private runtime evidence does not by itself authorize public proof, website wording, release wording, production language, signal wording, or public-safe runtime wording.

## Review Gates Before Proof Update

Before any future proof record, proof card, or proof index update, the reviewer must confirm:

1. The capture was explicitly approved before execution.
2. The packet route was approved before any files were created.
3. Raw evidence remains private and outside the proof repo.
4. Sanitized summaries contain no private hostnames, internal addresses, usernames, secrets, tokens, private opportunity material, or unnecessary local paths.
5. Hashes and timestamps are present for the evidence packet.
6. The detection source version and validation truth were current when the packet was captured.
7. The proposed wording is narrower than or equal to the evidence.
8. The proposed wording does not imply production readiness, sustained monitoring, public-safe status, autonomous disposition, AI disposition, analyst disposition, containment, closure, response automation, or suppression execution.
9. Any signal wording is backed by separate signal evidence.
10. Human approval exists for the exact proof update.

## Required Verifier Or Checklist

A future proof update must include at least one deterministic verifier or a manually reviewable checklist that confirms:

- Required evidence packet fields are present.
- Raw evidence is not committed to the proof repo.
- Sanitized summary path and hash are recorded.
- Runtime claim wording is scoped to the approved lab event.
- Signal wording is absent unless separately evidenced.
- Blocked claims remain blocked.
- Public-safe runtime remains blocked unless a separate public-safe approval exists.
- Proof validators pass after the update.

Until that verifier or checklist exists and passes, the proof index must not be promoted beyond `CONTROLLED_TEST_VALIDATED`.

## Stop Conditions

Stop before proceeding if:

- The requested action would execute runtime capture inside this design PR.
- The requested action would touch VMs, SSH, Splunk, Wazuh, Cribl, Security Onion, Sysmon, Windows event logs, or other runtime systems without a separate runtime approval.
- The requested action would create evidence files, screenshots, exports, transcripts, or hash manifests without approved evidence routing.
- The requested action would update proof records, proof cards, or proof indexes to promote runtime or signal state without separate approval.
- The requested action would modify detections, validation, platform, workflows, website, or public rendering.
- The event source, host scope, or route is unclear.
- Private identifiers cannot be redacted from the proposed summary.
- Stale-state review fails.
- Wording review would require a claim broader than the evidence.
- Human approval is missing.

This gate preserves the current HO-DET-012 proof ceiling and keeps runtime, signal, public-safe, production, autonomous SOC, AI, and analyst disposition claims blocked until later evidence and approval justify a scoped change.
