# HawkinsOperations Proof Records Index

## Purpose

This index routes reviewers to proof records, boundary records, and reviewer-facing proof cards. It does not create proof, replace source records, or promote claims beyond the records it links.

AI generates work. Evidence and human review authorize claims.

This index covers the current reviewer route set for HO-DET-001, HO-DET-011, AWS-DET-001, and HO-NDR-001. Older baseline artifacts may exist in this repository, but they do not promote the current HawkinsOperations proof ceiling.

## Current Claim Boundary

- Default public ceiling: CONTROLLED_TEST_VALIDATED
- Default public-safe status: NOT_PUBLIC_SAFE
- GitHub/website rendering is not proof.
- Proof cards are route/display artifacts only.

## Records Index Table

| ID | Record type | Source record / boundary route | Proof card | Current ceiling | Public-safe status | Supported scope | Blocked claims | Next gate |
|---|---|---|---|---|---|---|---|---|
| HO-DET-001 | proof record | [proof/records/HO-DET-001.md](HO-DET-001.md) | [proof/cards/HO-DET-001.md](../cards/HO-DET-001.md) | CONTROLLED_TEST_VALIDATED | NOT_PUBLIC_SAFE | Controlled-test validation against controlled positive and negative process-creation fixtures. | Runtime-active, signal-observed, evidence-linked public proof, public-safe, production, fleet-wide, live Splunk public proof, Cribl-routed, Wazuh-routed, AWS-live, autonomous SOC, AI-approved disposition, AI-decided disposition, analyst-approved disposition, production AutoSOC. | Public evidence linkage, privacy review, stale review, wording review, and Raylee approval before public-safe/runtime/signal wording. |
| HO-DET-011 | proof record | [proof/records/HO-DET-011.md](HO-DET-011.md) | none | PRIVATE_RUNTIME_EVIDENCE_CAPTURED | NOT_PUBLIC_SAFE | Controlled-test validation against 17 controlled Windows service creation fixtures, platform case-packet guardrail, and sanitized private local Windows runtime evidence for one controlled service-creation test. | Runtime-active, signal-observed public proof, evidence-linked public proof, public-safe, live Splunk fired, Splunk observed, Wazuh observed, Wazuh-routed, Cribl routed, Cribl-routed, AWS-live, production-ready, fleet-wide, service-creation coverage completeness, autonomous SOC, AI-approved disposition, AI-decided disposition, analyst-approved disposition. | Event-specific Wazuh/Splunk/Cribl correlation review before routed-telemetry wording; public evidence linkage, redaction review, stale review, wording review, and Raylee approval before public-safe wording. |
| AWS-DET-001 | controlled-test validation record | [proof/records/AWS-DET-001.md](AWS-DET-001.md) | [proof/cards/AWS-DET-001.md](../cards/AWS-DET-001.md) | CONTROLLED_TEST_VALIDATED | NOT_PUBLIC_SAFE | Fixture-only validation against controlled CloudTrail-style IAM denial fixtures. | AWS-live, live CloudTrail, cloud runtime-active, deployed cloud detection, AWS account coverage, signal-observed, evidence-linked public proof, public-safe, production, AI-approved disposition, AI-decided disposition, analyst-approved disposition. | Live AWS/CloudTrail evidence, privacy review, stale review, wording review, and Raylee approval before AWS-live/cloud runtime wording. |
| HO-NDR-001 | private proof record scaffold | [proof/records/HO-NDR-001.md](HO-NDR-001.md); [docs/boundaries/HO-NDR-001-SECURITY-ONION-VISIBILITY-CONTRACT.md](../../docs/boundaries/HO-NDR-001-SECURITY-ONION-VISIBILITY-CONTRACT.md) | [proof/cards/HO-NDR-001.md](../cards/HO-NDR-001.md) | CROSS_SOURCE_CORROBORATION_CONTRACT_DEFINED; planned post-runtime ceiling PRIVATE_CROSS_SOURCE_CORROBORATION_CAPTURED only after approved capture | NOT_PUBLIC_SAFE | Sanitized Security Onion visibility validation contract and cross-source corroboration scaffold exist in the validation repo. | Public-safe proof, production NDR, permanent SPAN, fleet-wide visibility, durable monitoring, PCAP availability, long-term retention, cross-source corroboration captured, Security Onion telemetry forwarded to Splunk, Splunk search executed, Cribl route proven, JA4+ support, Strelka/YARA workflow, dynamic Zeek plugin claims, Zeek completeness, Suricata detection quality, runtime-active, signal-observed, autonomous SOC. | Runtime approval, event-specific private evidence capture, verifier output, evidence-link review, public-safe redaction review, stale review, wording review, and Raylee approval before public NDR claims. |

## Control Reality

- HO-DET-001: verifier-backed proof record with CI-enforced controlled-test scope where supported by the existing proof record and linked validation routes. This does not prove runtime-active, signal-observed, production, routed telemetry, or public-safe status.
- HO-DET-011: proof-boundary record with merged source, 17-case controlled-test validation, platform guardrail references, and sanitized private local Windows runtime evidence. This does not prove runtime-active, public or routed signal-observed proof, public-safe, production, routed telemetry, Wazuh observation, Splunk observation, Cribl routing, fleet-wide, service-creation coverage completeness, autonomous SOC, AI-approved disposition, AI-decided disposition, or analyst-approved disposition.
- AWS-DET-001: fixture-only controlled-test validation record. It has controlled CloudTrail-style fixture validation, not AWS-live proof, live CloudTrail proof, cloud runtime-active proof, deployed cloud detection proof, or AWS account coverage.
- HO-NDR-001: private proof scaffold route. The validation repo owns the Security Onion visibility contract and cross-source corroboration scaffold. This does not approve runtime execution, public-safe proof, production NDR claims, Security Onion telemetry forwarding, Splunk searches, Cribl route changes, or achieved cross-source corroboration.

Docs are not real controls unless backed by CI, a verifier, branch protection, a ruleset, or a blocking check.

## Blocked Claims Register

The current index does not approve or imply:

- runtime-active
- signal-observed
- evidence-linked public proof
- public-safe
- production-ready
- fleet-wide
- enterprise-deployed
- Cribl-routed
- Wazuh-routed
- AWS-live
- live CloudTrail
- live Splunk public proof
- Security Onion production NDR
- permanent SPAN
- PCAP availability
- durable monitoring
- long-term retention
- cross-source corroboration
- autonomous SOC
- AI-approved disposition
- AI-decided disposition
- analyst-approved disposition
- production AutoSOC

## Reviewer Route

Start with the proof card for scan speed. Use the source record or boundary route for detail. Follow linked validation, workflow, verifier, and ledger routes where the source record or card identifies them. Treat next gates as promotion blockers, not roadmap promises.

## Next Promotion Gates

| ID | Next promotion gate |
|---|---|
| HO-DET-001 | Public evidence linkage, privacy review, stale review, wording review, and Raylee approval before public-safe, runtime, or signal wording. |
| HO-DET-011 | Event-specific Wazuh/Splunk/Cribl correlation review before routed-telemetry wording; public evidence linkage, redaction review, stale review, wording review, and Raylee approval before public-safe wording. |
| AWS-DET-001 | Live AWS/CloudTrail evidence, privacy review, stale review, wording review, and Raylee approval before AWS-live or cloud runtime wording. |
| HO-NDR-001 | Runtime approval, event-specific private evidence capture, verifier output, evidence-link review, public-safe redaction review, stale review, wording review, and Raylee approval before public NDR claims. |
