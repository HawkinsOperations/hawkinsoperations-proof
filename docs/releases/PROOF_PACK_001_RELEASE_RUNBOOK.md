# Proof Pack 001 Release Runbook

## Boundary

This runbook records the Proof Pack 001 release-packaging boundary and post-release public route. It does not authorize another tag, another GitHub Release, another ZIP upload, a signature, a signed artifact, a website update, public-safe approval, runtime-active claim, signal-observed claim, production claim, autonomous SOC claim, AI-approved disposition claim, or analyst-approved disposition claim.

Proof Pack 001 has an official direct GitHub Release route:

https://github.com/HawkinsOperations/hawkinsoperations-proof/releases/tag/hawkinsoperations-proof-pack-001

The generic GitHub `/releases` index is not the source of truth if it renders inconsistently. Public surfaces should route reviewers to the exact tag release URL above.

The official release state is bounded by:

- release tag: `hawkinsoperations-proof-pack-001`
- GitHub Release: `HawkinsOperations Proof Pack 001`
- uploaded release ZIP asset: `HAWKINSOPERATIONS_PROOF_PACK_001.zip`
- release ZIP SHA256: `44d8a643aa2b113c9e99be0462e699d39af707a67190823cc05bb381907dc452`
- checksum verification for the release ZIP and payload

Current ceiling remains `CONTROLLED_TEST_VALIDATED`.

Reviewer package status remains `PUBLIC_SAFE_REVIEWER_RELEASE_CANDIDATE`.

Raw/private runtime evidence remains `NOT_PUBLIC_SAFE` and excluded.

Public-safe runtime proof remains `BLOCKED`.

## Pre-Release Checklist

- Confirm the checkout is clean and based on `main`.
- Confirm `RELEASE_MANIFEST.json` still names `HAWKINSOPERATIONS_PROOF_PACK_001`.
- Confirm public routing uses the exact direct release URL:
  `https://github.com/HawkinsOperations/hawkinsoperations-proof/releases/tag/hawkinsoperations-proof-pack-001`.
- Confirm route-only reconciliation does not edit released packet payload files or change their checksum-bound contents.
- Confirm no generated ZIP, Sigstore bundle, signature, or signed artifact is staged or committed.
- Confirm human GitHub review exists before merge.
- Confirm Raylee provides `MERGE_APPROVED` before merge.
- Confirm Raylee provides a separate explicit approval before any future release publication step.

## Validation Commands

Run from the repository root:

```powershell
python -B scripts/verify-ho-det-001-proof-integrity.py
python -B scripts/verify_proof_integrity.py
python -B scripts/verify-proof-pack-001-release.py
python -B scripts/build-proof-pack-001-zip.py --check
python -B scripts/verify-proof-pack-001-zip.py --check
python -B scripts/verify-proof-pack-001-zip.py dist/proof-pack-001/HAWKINSOPERATIONS_PROOF_PACK_001.zip
git diff --check
```

## Build Command

The build check is safe and does not write artifacts:

```powershell
python -B scripts/build-proof-pack-001-zip.py --check
```

The local build command is:

```powershell
python -B scripts/build-proof-pack-001-zip.py
```

The script writes only under `dist/proof-pack-001/`, which is ignored by Git. Generated ZIPs, checksum sidecars, release artifacts, signatures, signing bundles, and payload manifests must stay untracked and must not be committed.

Official mode requires the literal release approval token. GitHub Actions context is never approval by itself.

```powershell
python -B scripts/build-proof-pack-001-zip.py --official --release-approved RELEASE_APPROVED_PROOF_PACK_001
```

Equivalent environment-variable form:

```powershell
$env:RELEASE_APPROVAL = 'RELEASE_APPROVED_PROOF_PACK_001'
python -B scripts/build-proof-pack-001-zip.py --official
```

## Verify Command

Verifier input is optional only for check mode:

```powershell
python -B scripts/verify-proof-pack-001-zip.py --check
```

After a local ZIP build, verify the ZIP:

```powershell
python -B scripts/verify-proof-pack-001-zip.py dist/proof-pack-001/HAWKINSOPERATIONS_PROOF_PACK_001.zip
```

## Human Review Gate

Before merge, review the PR in GitHub Files changed and confirm:

- changed files match approved release-packaging scope
- no generated ZIP, checksum sidecar, signature, bundle, or screenshot is committed
- scripts are checkable without publication
- blocked claims remain blocked
- private leak scan passes
- no stronger public claim is introduced

## Merge Gate

Do not merge until Raylee provides:

```text
MERGE_APPROVED
```

Green CI/status checks are not merge authority. Codex review is AI labor, not human governance.

## Future Release Action Gate

Proof Pack 001 already has an official direct GitHub Release route. Do not create another tag, GitHub Release, ZIP upload, checksum publication, signature, or signed artifact without a separate explicit Raylee approval.

The historical Proof Pack 001 release approval token was:

```text
RELEASE_APPROVED_PROOF_PACK_001
```

## Tag Naming

The official Proof Pack 001 tag is:

```text
hawkinsoperations-proof-pack-001
```

## GitHub Release Title

The official Proof Pack 001 release title is:

```text
HawkinsOperations Proof Pack 001
```

## GitHub Release Body Draft

```markdown
# HawkinsOperations Proof Pack 001

This release packages the bounded HO-DET-001 controlled-test proof packet.

Ceiling: CONTROLLED_TEST_VALIDATED
Reviewer package status: PUBLIC_SAFE_REVIEWER_RELEASE_CANDIDATE
Raw/private runtime evidence public-safe: NOT_PUBLIC_SAFE
Public-safe runtime proof: BLOCKED

Included payload:

- reviewer packet
- release manifest
- source checksum file
- release notes template
- scope, governance, and status documents
- HO-DET-001 proof card and proof record
- controlled-test validation record
- evidence ledger and schema
- proof integrity verifier source
- proof record schema

This release does not prove runtime-active public proof, signal-observed public proof, evidence-linked public runtime proof, public-safe status, production-ready status, SOCaaS, live Splunk proof, Cribl-routed public proof, Wazuh-routed public proof, AWS-live status, autonomous SOC operation, AI-approved disposition, AI-decided disposition, analyst-approved disposition, fleet-wide deployment, or enterprise deployment.

Website/GitHub rendering is not proof. Evidence and human review authorize claims.
```

## Rollback Or Cancel Procedure

If any validation fails before release:

- stop the release process
- do not create or push a tag
- do not create a GitHub Release
- do not upload ZIPs or checksums
- keep generated files unstaged
- fix the source packet through a normal PR
- rerun all validation commands

If a tag or GitHub Release is created incorrectly, stop and ask Raylee for an explicit rollback approval before deleting or changing anything.

## Blocked Claims

The release packet must not promote:

- public-safe proof
- runtime-active proof
- signal-observed public proof
- evidence-linked public runtime proof
- production-ready status
- SOCaaS-ready status
- fleet-wide deployment
- enterprise deployed status
- live Splunk proof
- Cribl-routed public proof
- Wazuh-routed public proof
- AWS-live status
- autonomous SOC operation
- AI-approved disposition
- AI-decided disposition
- analyst-approved disposition
- production AutoSOC status

## Post-Release Website Update Gate

Do not update website or public pointers until:

- the tag exists
- the GitHub Release exists
- the release ZIP exists
- ZIP and payload checksum verification pass
- Raylee approves the website/public pointer update separately

Website rendering is not proof.

## Optional Signing Future Gate

Signing and Sigstore are future work. Do not add or publish signatures, Sigstore bundles, signed artifacts, or signing workflow behavior without separate explicit approval.
