# HawkinsOperations Proof

Evidence repository for HawkinsOperations, focused on verifiable and shareable proof artifacts.

## Purpose

This repository stores curated evidence that supports technical claims across detection engineering, validation, and platform operation.

## Scope

- Evidence index and proof bundles
- Validation summaries and release evidence
- Public-safe artifacts linked to specific versions/commits

## Out of Scope

- Raw private telemetry dumps
- Host-specific operational diaries
- Secret-bearing logs or internal-only identifiers

## Repository Contract

- Every evidence artifact must be attributable to a source commit/run.
- Evidence must be structured for independent review.
- Public-facing claims should map to concrete proof records here.
- Platform runtime contract enforcement for HO-DET-001 is a non-promotional guardrail. It preserves the current public ceiling but does not prove runtime-active status, signal-observed public proof, public-safe runtime proof, live Splunk fired, Cribl-routed status, Wazuh-routed public proof, AWS-live status, production-ready status, fleet-wide coverage, autonomous SOC operation, AI-approved disposition, or analyst-approved disposition.

## Public-Safe Proof

- Redacted evidence packets
- Versioned claims-to-proof mapping
- Release-level verification snapshots

## Proof Records

- [AWS-DET-001](proof/records/AWS-DET-001.md)
- [HO-DET-001](proof/records/HO-DET-001.md)

## Case Studies

- [HO-DET-001: AI Authority Boundary Case Study](docs/case-studies/HO-DET-001-AI-AUTHORITY-BOUNDARY.md)
- [Purple Team Closed Loop 001](docs/case-studies/PURPLE-TEAM-CLOSED-LOOP-001.md)

## Related Repositories

- Detections: `hawkinsoperations-detections`
- Validation: `hawkinsoperations-validation`
- Platform: `hawkinsoperations-platform`
- Website: `hawkinsoperations-website`

