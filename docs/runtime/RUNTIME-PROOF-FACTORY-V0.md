# Runtime Proof Factory v0

## Purpose

Runtime Proof Factory v0 publishes a bounded public-safe summary for the first two HawkinsOperations private runtime proof lanes approved for sanitized public wording: HO-DET-011 and HO-DET-012.

This document is a public-safe summary surface. It is not raw evidence, not a public runtime proof closure, not a public signal-observed proof claim, and not a production-readiness claim.

## Publication Basis

- Later operator approval: `PUBLIC_SAFE_APPROVED` for this bounded summary wording only.
- Decision-gate state: the merged HO-DET-011 and HO-DET-012 decision-gate documents remain historical gate records and are not rewritten by this summary.
- Source authority: merged HO-DET-011 and HO-DET-012 review and decision artifacts constrain the allowed wording.
- Publication lane: bounded public-safe summary only.
- Raw evidence location: retained outside public repositories.
- Splunk status: `NOT_VERIFIED`.
- AI disposition authority: not claimed.
- Human review requirement: preserved.

`PUBLIC_SAFE_APPROVED` is the later human/operator approval for this bounded summary surface. It does not retroactively change the decision-gate documents, mutate proof index status, expose raw evidence, or authorize public runtime proof, public signal-observed proof, Splunk observation, production, fleet-wide, autonomous SOC, AI-approved, or analyst-approved claims.

## Published Summary

HO-DET-011 and HO-DET-012 have private lab runtime receipts with Wazuh-backed private observation and merged deterministic verifier, review, and decision artifacts. Raw evidence remains private. Splunk remains `NOT_VERIFIED`. Production, fleet-wide, autonomous, AI-approved, and analyst-approved claims are not made.

## Detection Summaries

### HO-DET-011

- Runtime lane: controlled Windows service-creation test.
- Private runtime receipt: captured.
- Private observation: Wazuh-backed private observation captured.
- Deterministic verifier: merged.
- Public-safe review packet: merged.
- Public-safe decision gate: merged.
- Public wording ceiling: bounded private-runtime receipt summary.
- Raw evidence: retained outside public repositories.
- Splunk: `NOT_VERIFIED`.

Allowed public wording:

> HO-DET-011 has a public-safe candidate summary for a private lab runtime receipt from one controlled Windows service-creation test. The summary confirms that local Windows telemetry and private Wazuh observation were reviewed in sanitized form, while raw evidence remains private. Splunk remains NOT_VERIFIED, and the claim does not extend to production, fleet-wide, autonomous SOC, AI-approved, or analyst-approved status.

### HO-DET-012

- Runtime lane: controlled Windows scheduled-task creation test.
- Private runtime receipt: captured.
- Private observation: Wazuh-backed private observation captured.
- Deterministic verifier: merged.
- Public-safe review packet: merged.
- Public-safe decision gate: merged.
- Public wording ceiling: bounded private-runtime receipt summary.
- Raw evidence: retained outside public repositories.
- Splunk: `NOT_VERIFIED`.

Allowed public wording:

> HO-DET-012 has a public-safe candidate summary for a private lab runtime receipt from one controlled Windows scheduled-task creation test. The summary confirms that local Windows telemetry and private Wazuh observation were reviewed in sanitized form, while raw evidence remains private. Splunk remains NOT_VERIFIED, and the claim does not extend to production, fleet-wide, autonomous SOC, AI-approved, or analyst-approved status.

## What This Publishes

- A bounded public-safe summary that private runtime receipts exist for HO-DET-011 and HO-DET-012.
- A bounded public-safe summary that private Wazuh observation was captured for both lanes.
- A bounded public-safe summary that deterministic verifier, review, and decision-gate artifacts are merged.
- A bounded public-safe statement that raw evidence remains private and outside public repositories.

## What This Does Not Publish

- Raw Wazuh lines.
- Raw Windows event payloads.
- Exact command output.
- Host identifiers.
- User identifiers.
- Private storage paths.
- Internal IP addresses or URLs.
- Exact service, task, or correlation markers.
- Private evidence hashes as public proof anchors.

## Blocked Claims

This document does not claim:

- public runtime proof closure;
- public signal-observed proof;
- Splunk observation;
- production readiness;
- fleet-wide coverage;
- autonomous SOC operation;
- AI-approved disposition;
- AI-decided disposition;
- analyst-approved disposition;
- complete service-creation coverage;
- complete scheduled-task coverage.

## Status Vocabulary Note

The current proof status index validator does not contain a public-safe summary status for individual detection rows. For that reason, this publication does not mutate `DETECTION_PROOF_STATUS_INDEX.yml`.

The strongest valid proof-index state remains:

- HO-DET-011: `PRIVATE_RUNTIME_EVIDENCE_CAPTURED` / `PRIVATE_RUNTIME_EVIDENCE_CAPTURED` / `NOT_PROVEN` / `NOT_PUBLIC_SAFE`.
- HO-DET-012: `CONTROLLED_TEST_VALIDATED` / `NOT_PROVEN` / `NOT_PROVEN` / `NOT_PUBLIC_SAFE`.

The public-safe approval applies to this bounded summary wording only. It does not convert private runtime evidence into public runtime proof or public signal-observed proof.
