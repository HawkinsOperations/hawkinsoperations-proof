# HawkinsOperations Proof
## Evidence and Claim Ceiling Plane

This repository stores reviewed evidence records and defines what HawkinsOperations can safely claim.

Proof is the claim boundary: evidence can support a claim only within its recorded scope, public-safe status, and review state.

## Current Public Claim Ceiling

| Boundary | Current state |
|---|---|
| Flagship proof path | HO-DET-001 |
| Public proof ceiling | CONTROLLED_TEST_VALIDATED |
| Public-safe status | NOT_PUBLIC_SAFE |
| Private/internal runtime status | CONTROLLED_LAB_RUNTIME_MATCH_VERIFIED |
| Runtime-active public proof | BLOCKED |
| Public signal-observed proof | BLOCKED |
| Public-safe runtime proof | BLOCKED |

Private/internal runtime match evidence is not public-safe proof. Public claims require reviewed wording, evidence linkage, privacy review, stale review, and Raylee approval.

## Proof Pack 001 Official Release Route

Proof Pack 001 has an official direct GitHub Release route in `hawkinsoperations-proof`:

[HawkinsOperations Proof Pack 001](https://github.com/HawkinsOperations/hawkinsoperations-proof/releases/tag/hawkinsoperations-proof-pack-001)

The release package is a bounded reviewer packet for `HO-DET-001` and does not raise the public proof ceiling.

| Item | Current state |
|---|---|
| Release tag | `hawkinsoperations-proof-pack-001` |
| Pack ID | `HAWKINSOPERATIONS_PROOF_PACK_001` |
| Release asset | `HAWKINSOPERATIONS_PROOF_PACK_001.zip` |
| ZIP SHA256 | `44d8a643aa2b113c9e99be0462e699d39af707a67190823cc05bb381907dc452` |
| Public ceiling | `CONTROLLED_TEST_VALIDATED` |
| Reviewer package status | `PUBLIC_SAFE_REVIEWER_RELEASE_CANDIDATE` |
| Raw/private runtime evidence | `NOT_PUBLIC_SAFE` |
| Public-safe runtime proof | `BLOCKED` |

Use the exact tag release URL above for public routing. Do not rely on GitHub's generic `/releases` index if it renders inconsistently.

Website and GitHub rendering route reviewers; rendering is not proof. The release package does not prove runtime-active deployment, signal-observed proof, production readiness, Cribl/Wazuh/Splunk/AWS live proof, autonomous SOC operation, or public-safe runtime proof.

## Runtime Route Proof v1 Private Candidate Reviewer Route

Runtime Route Proof v1 has a private-candidate prerelease for the Wazuh -> Cribl -> Splunk route:

[Runtime Route Proof v1 Private Candidate](https://github.com/HawkinsOperations/hawkinsoperations-proof/releases/tag/runtime-route-proof-v1-private-candidate-2026-06-01)

Start with [proof/maps/RUNTIME-ROUTE-PROOF-V1-REVIEWER-MAP.md](proof/maps/RUNTIME-ROUTE-PROOF-V1-REVIEWER-MAP.md) for the two-minute reviewer path. It connects the prerelease, proof record, machine-readable map, reviewer-safe ZIP SHA, and platform verifier/schema/sample.

| Item | Current state |
|---|---|
| Marker | `HO-RUNTIME-V1-20260601T120922Z-BATCH764` |
| Route | Wazuh -> Cribl -> Splunk |
| Verifier | `PASS_ROUTE_RECEIPTS` |
| Release type | Private-candidate prerelease |
| Proof ceiling | `PRIVATE_RUNTIME_ROUTE_PROOF_V1_CANDIDATE_PRESERVED` |
| Public-safe status | `NOT_PUBLIC_SAFE` |
| ZIP SHA256 | `3a1d4472bffcce68cff6e101c54e06b5a67528338bda174e6fef209fa9b1b278` |

This private-candidate release does not prove public-safe runtime proof, production SOC operation, autonomous SOC behavior, broad ingestion, AI-decided disposition, public publication approval, or Lifetime Governed Case mutation.

## Proof Pack 001 90-Second Reviewer Check

Use this quick path to verify the released artifact without raising the claim ceiling:

1. Open the direct release route: [HawkinsOperations Proof Pack 001](https://github.com/HawkinsOperations/hawkinsoperations-proof/releases/tag/hawkinsoperations-proof-pack-001).
2. Confirm the release tag is `hawkinsoperations-proof-pack-001` and the asset is `HAWKINSOPERATIONS_PROOF_PACK_001.zip`.
3. Download the ZIP and compare its SHA256 to `44d8a643aa2b113c9e99be0462e699d39af707a67190823cc05bb381907dc452`.
4. If using PowerShell, verify the downloaded ZIP with:

```powershell
Get-FileHash .\HAWKINSOPERATIONS_PROOF_PACK_001.zip -Algorithm SHA256
```

5. If using a local checkout of this repo, verify the ZIP payload with:

```powershell
python -B scripts/verify-proof-pack-001-zip.py .\HAWKINSOPERATIONS_PROOF_PACK_001.zip
```

Passing the checksum and ZIP verifier supports only this bounded reviewer claim: Proof Pack 001 is a real release artifact for `HO-DET-001` under `CONTROLLED_TEST_VALIDATED`. It does not prove runtime-active public proof, public signal proof, production readiness, SOCaaS readiness, autonomous SOC operation, AI-approved disposition, analyst-approved disposition, or public-safe runtime proof.

## Lifetime Case Ledger Verification Badges

[![Ledger summary verifier](https://github.com/HawkinsOperations/hawkinsoperations-proof/actions/workflows/governance-gate.yml/badge.svg?branch=main&event=push)](https://github.com/HawkinsOperations/hawkinsoperations-proof/actions/workflows/governance-gate.yml?query=branch%3Amain)
[![Ledger proof bundle verifier](https://github.com/HawkinsOperations/hawkinsoperations-proof/actions/workflows/governance-gate.yml/badge.svg?branch=main&event=push)](https://github.com/HawkinsOperations/hawkinsoperations-proof/actions/workflows/governance-gate.yml?query=branch%3Amain)

These badges route to the `Governance Gate` workflow. The workflow contains the `lifetime-ledger-public-summary` and `lifetime-ledger-proof-bundle` jobs, which verify the source-controlled Lifetime Case Ledger summary and proof bundle against the pinned platform manifest.

Badges report GitHub Actions workflow check status only. They do not prove runtime activity, signal observation, public proof, public-safe runtime proof, SOCaaS deployment, production deployment, autonomous SOC authority, AI-approved disposition, analyst-approved disposition, or case closure.

| Badge | Verifier job | What it verifies | Boundary |
|---|---|---|---|
| Ledger summary verifier | `lifetime-ledger-public-summary` | `proof/records/lifetime-case-ledger-v1-public-summary.json` matches the pinned platform manifest counts, proof ceiling, six-repo anchors, and blocked-claim boundaries. | Ledger status remains `NOT_PUBLIC_SAFE`; proof ceiling remains `SCHEMA_CONTRACT_VERIFIER_EXISTS_ONLY`. |
| Ledger proof bundle verifier | `lifetime-ledger-proof-bundle` | `proof/records/lifetime-case-ledger-v1-proof-bundle.json` packages the summary, pinned platform manifest reference, six-repo anchors, verifier commands, and reviewer steps without importing private evidence. | Ledger status remains `NOT_PUBLIC_SAFE`; proof ceiling remains `SCHEMA_CONTRACT_VERIFIER_EXISTS_ONLY`. |

## Reviewer Proof Map

Use [proof/indexes/reviewer-proof-map.md](proof/indexes/reviewer-proof-map.md) as the proof-owned reviewer map for the Lifetime Case Ledger chain.

The map ties together the ledger public summary, proof bundle, badge/status checks, evidence preservation map, branch cleanup map, blocked claims, and proof authority boundaries. It keeps the ledger at 4 events / 4 cases, `NOT_PUBLIC_SAFE`, and `SCHEMA_CONTRACT_VERIFIER_EXISTS_ONLY`.

The companion machine-readable map lives at [proof/indexes/reviewer-proof-map.json](proof/indexes/reviewer-proof-map.json) and is checked by:

```powershell
python scripts/verify-reviewer-proof-map.py --platform-root ../hawkinsoperations-platform --github-root ../.github
```

The reviewer proof map does not prove runtime-active public proof, signal-observed public proof, public-safe runtime proof, production deployment, SOCaaS deployment, autonomous SOC, AI-approved disposition, analyst-approved disposition, case closure, Cribl-routed telemetry, Wazuh-routed telemetry, AWS-live evidence, fleet-wide coverage, live Splunk firing, website as proof authority, badge as proof authority, or Project #1 as proof authority.

## What This Repository Proves

| Proof surface | What it can support |
|---|---|
| Proof records | Claim ceilings and evidence links |
| Evidence bundles | Reviewed support for bounded claims |
| Validation summaries | What was tested and under what scope |
| Case studies | Public-safe explanation of bounded evidence |
| Claim mapping | Which claims are supported, blocked, or not yet reviewed |

## What This Repository Does Not Prove

| Not proven by this repo alone | Why |
|---|---|
| Source correctness | Source truth belongs in detections |
| Test behavior | Validation truth belongs in validation |
| Live runtime state | Runtime evidence needs separate review |
| Public signal proof | Signal-observed public proof is blocked until approved |
| Website truth | Website is rendering only |
| Production readiness | Requires separate scoped evidence and approval |

## HO-DET-001 Current Boundary

| Item | Current state |
|---|---|
| Proof record | [proof/records/HO-DET-001.md](proof/records/HO-DET-001.md) |
| Public ceiling | CONTROLLED_TEST_VALIDATED |
| Public-safe status | NOT_PUBLIC_SAFE |
| Private/internal runtime status | CONTROLLED_LAB_RUNTIME_MATCH_VERIFIED |
| Platform contract guardrail | Non-promotional guardrail |
| Runtime-active public proof | BLOCKED |
| Public signal-observed proof | BLOCKED |
| Public-safe runtime proof | BLOCKED |

## Proof Record Routes

- [AWS-DET-001](proof/records/AWS-DET-001.md)
- [HO-DET-001](proof/records/HO-DET-001.md)

## Case Studies

- [HO-DET-001 SOCaaS Pilot Receipt Pack](docs/case-studies/HO-DET-001-SOCAAS-PILOT-RECEIPT.md)
- [Operations Accomplishment Ledger](docs/case-studies/OPERATIONS-ACCOMPLISHMENT-LEDGER.md)
- [HO-DET-001: AI Authority Boundary Case Study](docs/case-studies/HO-DET-001-AI-AUTHORITY-BOUNDARY.md)
- [Purple Team Closed Loop 001](docs/case-studies/PURPLE-TEAM-CLOSED-LOOP-001.md)

## Evidence Contract

- Every evidence artifact must map to a source, run, commit, or reviewed record.
- Evidence must state its scope.
- Evidence must preserve public/private boundaries.
- Public-facing claims must map to proof records.
- Raw private evidence is not automatically public-safe evidence.
- A proof record does not promote claims beyond its stated ceiling.

## Promotion Rule

A claim can move toward public use only when:

- evidence linkage exists
- the claim ceiling supports it
- private leakage risk is reviewed
- stale review is complete
- wording is reviewed
- Raylee approves promotion

## Current Claim Boundary

The left column lists what the current proof record can support. The right column lists claims this README explicitly does not make.

| Supported within current public ceiling | Explicitly not claimed |
|---|---|
| HO-DET-001 has merged source artifacts | Not claimed: runtime-active public proof |
| HO-DET-001 has merged controlled-test validation artifacts | Not claimed: public signal-observed proof |
| HO-DET-001 passed controlled-test validation | Not claimed: evidence-linked public proof |
| Internal platform contract guardrail exists as a non-promotional guardrail | Not claimed: public-safe runtime proof |
| Private/internal runtime match status is scoped private/internal | Not claimed: production-ready claim, fleet-wide claim, enterprise deployed claim |
| AI can support work, but cannot approve claims | Not claimed: live Splunk fired as public proof, Cribl-routed claim, Wazuh-routed claim, AWS-live claim |
| Human review is required before public promotion | Not claimed: autonomous SOC claim, AI-approved disposition, AI-decided disposition, analyst-approved disposition, production AutoSOC claim |

## Real Controls Rule

Docs, READMEs, proof records, diagrams, and websites are not real controls by themselves.

A control becomes real only when it blocks, fails, or forces correction through required review, branch protection, rulesets, blocking CI, deterministic verifiers, typed claim gates, or another enforceable mechanism.

Green CI/status checks are not merge authority.
Codex review is AI labor, not human governance.

## Related Repositories

| Repo | Boundary |
|---|---|
| `hawkinsoperations-detections` | Source truth |
| `hawkinsoperations-validation` | Behavior truth |
| Internal platform route | Runtime contracts / integration guardrails; not a public proof surface |
| `hawkinsoperations-website` | Public rendering only |
| `.github` | Org governance / reviewer routing |

## Doctrine

AI generates work. Evidence and human review authorize claims.

Build loud. Verify hard. Claim tight. Ship receipts.
