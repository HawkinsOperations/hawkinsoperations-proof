# HawkinsOperations Proof Pack 001

## Packet Identity

| Field | Value |
|---|---|
| Pack ID | HAWKINSOPERATIONS_PROOF_PACK_001 |
| Detection ID | HO-DET-001 |
| Detection title | Suspicious PowerShell EncodedCommand Execution via Sysmon Event ID 1 |
| Ceiling | CONTROLLED_TEST_VALIDATED |
| Reviewer package status | PUBLIC_SAFE_REVIEWER_RELEASE_CANDIDATE |
| Raw/private runtime evidence public-safe | NOT_PUBLIC_SAFE |
| Public-safe runtime proof | BLOCKED |
| Release status | PUBLIC_SAFE_REVIEWER_RELEASE_CANDIDATE_NO_TAG_NO_RELEASE |

## Boundary

This reviewer packet is a public-safe reviewer package for HO-DET-001. It is designed to let a reviewer inspect the controlled-test proof loop, proof record, release manifest, and checksum plan before any official tag or GitHub Release exists.

The package is a sanitized release artifact candidate. Raw/private runtime evidence is excluded and remains NOT_PUBLIC_SAFE. Public-safe runtime proof remains blocked unless separately approved.

Website rendering is not proof. Public pages can route to this packet after review, but the proof authority remains the proof record and the deterministic verifier outputs.

This packet does not prove runtime-active deployment, signal-observed public proof, evidence-linked public runtime proof, public-safe status, production-ready status, SOCaaS, live Splunk, Cribl-routed telemetry, Wazuh-routed collection, AWS-live status, autonomous SOC operation, AI-approved disposition, analyst-approved disposition, fleet-wide deployment, or enterprise deployment.

## Included Files

- `REVIEWER_PACKET.md`
- `RELEASE_MANIFEST.json`
- `SHA256SUMS.txt`
- `RELEASE_NOTES_TEMPLATE.md`
- `SCOPE.md`
- `GOVERNANCE.md`
- `STATUS.md`
- `proof/cards/HO-DET-001.md`
- `proof/records/HO-DET-001.md`
- `proof/records/HO-DET-001-CONTROLLED-TEST-VALIDATION-001.json`
- `evidence/evidence-ledger.json`
- `evidence/EVIDENCE_LEDGER_SCHEMA.json`
- `scripts/verify-ho-det-001-proof-integrity.py`
- `.github/contracts/proof-record.schema.json`

## Excluded Files

- `README.md`
- `proof/records/HO-NDR-001.md`
- `proof/records/HO-DET-011.md`
- `proof/cards/HO-NDR-001.md`
- `docs/boundaries/HO-NDR-001-SECURITY-ONION-VISIBILITY-CONTRACT.md`
- `docs/debugging/*`
- `proof/records/PROOF-HOD-001-2026-04-21-001.json`
- `proof/records/AWS-DET-001.md`
- `proof/cards/AWS-DET-001.md`
- `.github/workflows/*`
- `docs/case-studies/*`

## Validation Summary

HO-DET-001 is CONTROLLED_TEST_VALIDATED through controlled positive and negative process-creation fixtures.

- Validation status: pass
- Total controlled cases: 14
- Positive controlled cases: 7
- Negative controlled cases: 7
- Matched positives: 7
- Missed positives: 0
- False-positive negative matches: 0
- Validation scope: controlled-test process-creation fixtures only

## Proof Loop Summary

The proof loop routes through source artifacts, validation artifacts, case-packet checks, deterministic verifier checks, and a proof record. The release path prepares a public-safe reviewer package only. It does not publish the packet.

Key routes:

- Proof record: `proof/records/HO-DET-001.md`
- Proof card: `proof/cards/HO-DET-001.md`
- Validation report: `hawkinsoperations-validation/reports/ho-det-001/validation-result.json`
- Public pipeline proof report: `hawkinsoperations-validation/reports/ho-det-001/pipeline-proof.md`
- Source detection: `hawkinsoperations-detections/detections/successor/ho-det-001/rule.yml`
- Splunk source: `hawkinsoperations-detections/detections/successor/ho-det-001/splunk.spl`
- Proof integrity verifier: `scripts/verify-ho-det-001-proof-integrity.py`
- Proof Pack release verifier: `scripts/verify-proof-pack-001-release.py`

## Blocked Claims

The following claims remain blocked for this packet:

- runtime-active public proof
- signal-observed public proof
- evidence-linked public runtime proof
- public-safe status
- production-ready status
- SOCaaS
- live Splunk
- Cribl-routed telemetry
- Wazuh-routed collection
- AWS-live status
- autonomous SOC
- AI-approved disposition
- analyst-approved disposition
- fleet-wide deployment
- enterprise deployment

## Reviewer Instructions

1. Read `RELEASE_MANIFEST.json` first to confirm the pack identity, included files, exclusions, release status, tag plan, and claim boundary.
2. Run `python scripts/verify-proof-pack-001-release.py` from the repository root.
3. Run `python scripts/verify-ho-det-001-proof-integrity.py` from the repository root.
4. Run `python scripts/verify_proof_integrity.py` from the repository root.
5. Confirm `SHA256SUMS.txt` matches the included packet files named by the manifest.
6. Treat every runtime, signal, public-safe runtime proof, production, SOCaaS, autonomous, AI-approved, analyst-approved, fleet-wide, and enterprise wording path as blocked unless a later approved release changes the trust state.

## Release Status

This packet is ready for review as a public-safe reviewer release candidate package. It is not an official release, does not create a tag, does not upload a zip, does not create a GitHub Release, and does not sign an artifact. Release publication still requires separate approval.
