# HO-NDR-001 Boundary Card

## Header

| Field | Value |
|---|---|
| ID | HO-NDR-001 |
| Title | Security Onion Cross-Source Corroboration Scaffold |
| Record type | private proof record scaffold |
| Current ceiling | CROSS_SOURCE_CORROBORATION_CONTRACT_DEFINED |
| Planned post-runtime ceiling | PRIVATE_CROSS_SOURCE_CORROBORATION_CAPTURED |
| Public-safe status | NOT_PUBLIC_SAFE |
| Last reviewed | UNKNOWN |

## Supported Claim

A sanitized Security Onion visibility validation contract and cross-source corroboration scaffold exist in the validation repo.

## What This Proves

- The boundary record exists at `docs/boundaries/HO-NDR-001-SECURITY-ONION-VISIBILITY-CONTRACT.md`.
- The proof record scaffold exists at `proof/records/HO-NDR-001.md`.
- The boundary record states that validation owns the schema, sample, verifier, and workflow.
- The cross-source scaffold defines required future evidence for Security Onion / Suricata, endpoint telemetry, Splunk correlation, and optional Cribl route receipts.
- The boundary record links merged validation reference `HawkinsOperations/hawkinsoperations-validation#24`.
- The boundary record keeps private runtime evidence out of this proof repo route.

## What This Does NOT Prove

- Public-safe proof is not approved.
- Security Onion production NDR is not proven.
- Permanent SPAN, fleet-wide visibility, durable monitoring, PCAP availability, and long-term retention are not proven.
- Cross-source corroboration capture, Zeek completeness, and Suricata detection quality are not proven.
- Splunk search execution, Security Onion telemetry forwarding, Cribl route proof, JA4+ support, Strelka/YARA workflow, and dynamic Zeek plugin claims are not proven.
- Runtime-active, signal-observed, evidence-linked public proof, production-ready, enterprise-deployed, autonomous SOC, AI-approved disposition, AI-decided disposition, analyst-approved disposition, and production AutoSOC claims are blocked.

## Evidence / Artifact Route

| Route | Path |
|---|---|
| Source record | `proof/records/HO-NDR-001.md` |
| Boundary record | `docs/boundaries/HO-NDR-001-SECURITY-ONION-VISIBILITY-CONTRACT.md` |
| Validation | `HawkinsOperations/hawkinsoperations-validation#24` |
| Workflow | `hawkinsoperations-validation/.github/workflows/security-onion-visibility-contract.yml` |
| Verifier | `hawkinsoperations-validation/scripts/verify-security-onion-visibility-rollup.py`; `hawkinsoperations-validation/scripts/verify-security-onion-cross-source-corroboration.py` |
| Ledger | UNKNOWN |
| Related PR/commit | `HawkinsOperations/hawkinsoperations-validation#24`; merge commit `e37adfed3eade12022efd1f7cceef6175598623f` |

## Control Reality

Private proof record scaffold. This is not public-safe proof, not evidence of production NDR, and not evidence that cross-source corroboration has been captured. It records that sanitized validation contract routes exist and that promotion requires later runtime evidence and review.

## Current Status

| Plane | Truth |
|---|---|
| Repo truth | PROVEN: boundary record, proof scaffold, and validation contract routes exist. |
| Validation truth | PROVEN for contract/verifier shape only; not runtime packet content. |
| Runtime truth | BLOCKED for public or production NDR claims. |
| Signal truth | BLOCKED for signal-observed public proof. |
| Evidence truth | Contract routes exist; event-specific cross-source evidence is not captured by this scaffold. |
| Public proof | NOT_PUBLIC_SAFE; no public-proof promotion. |

## Next Promotion Gate

HO-NDR-001 needs separate runtime approval, event-specific evidence capture, verifier output, evidence linkage, privacy review, stale review, wording review, and Raylee approval before public-safe wording, production NDR, visibility coverage, retention, PCAP, Zeek, Suricata, or cross-source corroboration capture claims can be promoted.

## Reviewer Takeaway

HO-NDR-001 is a private scaffold. It gives reviewers a clean route to the Security Onion visibility and cross-source corroboration contracts without treating those contracts as production NDR proof, public-safe evidence, or achieved cross-source corroboration.
