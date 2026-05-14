# HO-NDR-001 Security Onion Visibility Contract Boundary

## Summary

The validation repo contains a sanitized clone-runnable Security Onion visibility contract and a cross-source corroboration scaffold. This proof-repo boundary stub records that the routes exist without importing private evidence or promoting a runtime proof claim.

## Authority Boundary

- Validation repo owns the schema, sample, verifier, and workflow.
- Proof repo records the existence of the boundary route only.
- The proof record scaffold may reference `PRIVATE_CROSS_SOURCE_CORROBORATION_CAPTURED` only as a planned post-runtime ceiling, not an achieved state.
- Private runtime evidence remains local/private.
- Website rendering is not proof.
- No public-safe proof is approved.

## Merged Validation Reference

- Validation PR: HawkinsOperations/hawkinsoperations-validation#24
- Merge commit: e37adfed3eade12022efd1f7cceef6175598623f
- Claim ceiling: PRIVATE_NDR_MODULE_VISIBILITY_ROLLUP_DEFINED

## Cross-Source Corroboration Scaffold

- Current claim ceiling: CROSS_SOURCE_CORROBORATION_CONTRACT_DEFINED
- Planned post-runtime ceiling: PRIVATE_CROSS_SOURCE_CORROBORATION_CAPTURED
- Achieved status: NOT_CAPTURED_SAMPLE_ONLY
- Validation sample: `hawkinsoperations-validation/validation/security-onion/ho-ndr-001/cross-source-corroboration.sample.json`
- Verifier: `hawkinsoperations-validation/scripts/verify-security-onion-cross-source-corroboration.py`
- Workflow: `hawkinsoperations-validation/.github/workflows/security-onion-visibility-contract.yml`

The scaffold defines required future evidence for one controlled event across Security Onion / Suricata, endpoint telemetry, Splunk correlation, and optional Cribl route receipts. It does not approve runtime execution, Splunk searches, Cribl route changes, Security Onion telemetry forwarding, screenshot capture, or public proof promotion.

## Supported Wording

- A sanitized Security Onion visibility validation contract exists in the validation repo.
- The contract defines required shape and guardrails for private NDR module visibility evidence.
- The contract does not import private evidence and does not promote public proof.

## Blocked Wording

The following claims are not approved by this boundary stub:

- public-safe proof
- production NDR
- permanent SPAN
- fleet-wide visibility
- durable monitoring
- PCAP availability
- long-term retention
- cross-source corroboration
- cross-source corroboration captured
- Security Onion telemetry forwarded to Splunk
- Splunk search executed
- Cribl route proven
- JA4+ support
- Strelka/YARA workflow
- dynamic Zeek plugin claims
- Zeek coverage completeness
- Suricata detection quality

## Next Gates

- separate runtime approval before event generation
- event-specific private evidence capture
- verifier output for the cross-source corroboration contract
- public-safe redaction review
- proof record approval if ever promoted
- website update only after proof record approval
- separate evidence-link review
- stale review date requirement
