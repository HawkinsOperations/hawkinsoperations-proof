# HO-DET-001 Proof Card

## Header

| Field | Value |
|---|---|
| ID | HO-DET-001 |
| Title | Suspicious PowerShell EncodedCommand Execution via Sysmon Event ID 1 |
| Record type | proof record |
| Internal verifier token | CONTROLLED_TEST_VALIDATED |
| Current ceiling | CONTROLLED_TEST_VALIDATED |
| Public display label | CONTROLLED_TEST_VALIDATED |
| Public-safe status | NOT_PUBLIC_SAFE |
| Last reviewed | UNKNOWN |

Compatibility note: `CONTROLLED_TEST_VALIDATED` is the internal verifier token preserved for proof-integrity compatibility. `CONTROLLED_TEST_VALIDATED` is the public-facing label used to describe the same controlled-test validation boundary without using legacy public wording.

## Supported Claim

HO-DET-001 is CONTROLLED_TEST_VALIDATED through a public proof-loop workflow with controlled positive and negative test cases, deterministic pass/fail output, and blocked-claim enforcement.

## What This Proves

- The proof record exists at `proof/records/HO-DET-001.md`.
- The controlled-test validation result is linked at `hawkinsoperations-validation/reports/ho-det-001/validation-result.json`.
- The public pipeline proof pack is linked at `hawkinsoperations-validation/reports/ho-det-001/pipeline-proof.md`.
- The machine-readable public pipeline proof pack is linked at `hawkinsoperations-validation/reports/ho-det-001/pipeline-proof.json`.
- The proof record reports 14 controlled cases: 7 matched positives and 7 negative cases without false-positive negative matches.
- The proof loop route is linked at `hawkinsoperations-validation/.github/workflows/ho-det-001-proof-loop.yml`.
- The proof repo verifier exists at `scripts/verify-ho-det-001-proof-integrity.py`.

## What This Does NOT Prove

- Runtime-active deployment is not proven.
- Signal-observed public proof is blocked.
- Evidence-linked public proof is blocked.
- Public-safe, production-ready, fleet-wide, or enterprise-deployed status is not proven.
- Live Splunk public proof, Cribl-routed HO-DET telemetry, Wazuh-routed telemetry, AWS-live status, autonomous SOC operation, production AutoSOC, AI-approved disposition, AI-decided disposition, and analyst-approved disposition are not proven.

## Evidence / Artifact Route

| Route | Path |
|---|---|
| Source record | `proof/records/HO-DET-001.md` |
| Validation | `hawkinsoperations-validation/reports/ho-det-001/validation-result.json` |
| Workflow | `hawkinsoperations-validation/.github/workflows/ho-det-001-proof-loop.yml`; `.github/workflows/ho-det-001-proof-integrity.yml` |
| Verifier | `scripts/verify-ho-det-001-proof-integrity.py`; `hawkinsoperations-validation/scripts/verify-ho-det-001-reproducible-proof-pack.py`; `hawkinsoperations-validation/scripts/verify-ho-det-001-runtime-packet.py` |
| Ledger | `evidence/evidence-ledger.json` entries `HO-DET-001-CONTROLLED-TEST-VALIDATION-001` and `HO-DET-001-PLATFORM-RUNTIME-CONTRACT-GUARDRAIL-001` |
| Related PR/commit | `HawkinsOperations/hawkinsoperations-validation#10`; `HawkinsOperations/hawkinsoperations-validation#18`; `HawkinsOperations/hawkinsoperations-validation#22`; `HawkinsOperations/hawkinsoperations-platform#5` |

## Control Reality

CI-enforced controlled-test scope and verifier-backed proof record. The proof card is route/display only. It does not raise the public ceiling, and it does not turn private/internal controlled lab runtime match evidence into public proof.

## Current Status

| Plane | Truth |
|---|---|
| Repo truth | PROVEN: proof record and linked source artifact routes exist. |
| Validation truth | PROVEN: controlled-test validation passed within controlled test-case scope. |
| Runtime truth | PRIVATE_INTERNAL only where recorded; public runtime-active status remains BLOCKED. |
| Signal truth | BLOCKED for public signal-observed proof. |
| Evidence truth | Ledger-backed for controlled-test validation and platform guardrail records; private/internal runtime evidence is not public-safe proof. |
| Public proof | CONTROLLED_TEST_VALIDATED only; NOT_PUBLIC_SAFE for public promotion. |

## Next Promotion Gate

To raise the claim, HO-DET-001 needs approved evidence linkage for the specific stronger claim, privacy review, stale review, wording review, and Raylee approval. Runtime-active status needs deployment or enablement proof. Signal-observed status needs preserved telemetry, alert, log, or search output with reviewable context. Public-safe status requires approved public wording and evidence-link review.

## Reviewer Takeaway

HO-DET-001 has a strong controlled-test validation record and verifier-backed proof routing for that scope. Treat this card as a fast map to the proof record, not as proof of live operation, public signal observation, routed telemetry, production coverage, or public-safe status.

## Planned Signed Release Packet

Current state:

- No signed GitHub Release artifact exists yet for this proof card.
- The current release effort ceiling is PLANNED_RELEASE_PATH.
- Repo-side source status: REVIEWER_PACKET_PATH_DEFINED_SOURCE_ONLY.
- This section defines the future reviewer packet path and exclusion contract only.
- It does not create `REVIEWER_PACKET.md`, `RELEASE_MANIFEST.json`, `SHA256SUMS.txt`, a zip, a tag, a GitHub Release, a Sigstore bundle, or a signed artifact.

Planned artifact:

- Planned release name: HawkinsOperations Proof Pack 001.
- Planned tag: `hawkinsoperations-proof-pack-001`.
- Planned zip: `HAWKINSOPERATIONS_PROOF_PACK_001.zip`.
- Planned Sigstore bundle: `HAWKINSOPERATIONS_PROOF_PACK_001.sigstore.json`.
- Planned checksum file: `SHA256SUMS.txt`.
- Planned generated reviewer packet inside zip: `REVIEWER_PACKET.md`.
- Planned generated manifest inside zip: `RELEASE_MANIFEST.json`.

Candidate Pack 001 contents:

- `REVIEWER_PACKET.md`
- `RELEASE_MANIFEST.json`
- `SHA256SUMS.txt`
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

Excluded from Pack 001:

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

Claim boundary:

- The future signed release, once implemented and verified, may support CONTROLLED_TEST_VALIDATED only.
- It must not promote PUBLIC_SAFE.
- It must not promote RUNTIME_ACTIVE.
- It must not promote SIGNAL_OBSERVED.
- It must not promote EVIDENCE_LINKED public proof.
- It must not promote production-ready, fleet-wide, live Splunk fired, Cribl-routed, Wazuh-routed, AWS-live, autonomous SOC, AI-approved disposition, AI-decided disposition, analyst-approved disposition, or production AutoSOC claims.

Verification language:

- Future verification wording must remain planned until the release workflow, tag, artifact, Sigstore bundle, and clean reviewer-side verification are actually created and tested.
- The final Cosign certificate identity must not be frozen until it is confirmed from the actual signed bundle.
- The expected future OIDC issuer is `https://token.actions.githubusercontent.com`.
- The expected future release workflow path is `.github/workflows/publish-proof-release.yml`, but that workflow does not exist yet and must not be created in this edit.

Source-side implementation checks:

- The proof integrity verifier must fail if this card no longer names `PLANNED_RELEASE_PATH`.
- The verifier must fail if Pack 001 no longer names `CONTROLLED_TEST_VALIDATED` as the only allowed future support level.
- The verifier must fail if Pack 001 no longer keeps `NOT_PUBLIC_SAFE` public-safe status.
- The verifier must fail if Pack 001 no longer excludes `proof/records/HO-NDR-001.md`.
- The verifier must fail if Pack 001 wording implies a release, tag, zip, signature, checksum publication, downloaded-artifact verification, or public-safe promotion already exists.

Reviewer meaning:

- A successful future verification would prove artifact integrity and signing provenance for the release artifact.
- It would not prove runtime activity, signal observation, public-safe status, production coverage, or analyst/AI disposition authority.
