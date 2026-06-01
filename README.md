# HawkinsOperations Proof

Canonical claim-ceiling and proof-pack verification README.

This repository owns HawkinsOperations proof records, reviewer proof routes, and claim ceilings. It does not raise claims automatically. A proof record, release, verifier, badge, README, website page, or GitHub rendering can support only the claim ceiling stated here and in the linked proof records.

## 10-Second Reviewer Path

1. Open the official release: [HawkinsOperations Proof Pack 001](https://github.com/HawkinsOperations/hawkinsoperations-proof/releases/tag/hawkinsoperations-proof-pack-001).
2. Confirm the tag is `hawkinsoperations-proof-pack-001` and the asset is `HAWKINSOPERATIONS_PROOF_PACK_001.zip`.
3. Verify the ZIP SHA256:

```powershell
Get-FileHash .\HAWKINSOPERATIONS_PROOF_PACK_001.zip -Algorithm SHA256
```

Expected SHA256:

```text
44d8a643aa2b113c9e99be0462e699d39af707a67190823cc05bb381907dc452
```

4. From a local checkout, verify the ZIP payload:

```powershell
python -B scripts/verify-proof-pack-001-zip.py .\HAWKINSOPERATIONS_PROOF_PACK_001.zip
```

Passing the checksum and ZIP verifier supports only this bounded claim: Proof Pack 001 is a real reviewer release artifact for `HO-DET-001` under `CONTROLLED_TEST_VALIDATED`.

It does not prove runtime-active public proof, public signal-observed proof, production readiness, SOCaaS readiness, autonomous SOC operation, AI-approved disposition, analyst-approved disposition, or public-safe runtime proof.

## Current Claim Ceiling

| Boundary | Current state |
|---|---|
| Canonical proof path | `HO-DET-001` |
| Public proof ceiling | `CONTROLLED_TEST_VALIDATED` |
| Proof Pack 001 reviewer package status | `PUBLIC_SAFE_REVIEWER_RELEASE_CANDIDATE` |
| Raw/private runtime evidence | `NOT_PUBLIC_SAFE` |
| Private/internal runtime status | `CONTROLLED_LAB_RUNTIME_MATCH_VERIFIED` |
| Runtime-active public proof | `BLOCKED` |
| Public signal-observed proof | `BLOCKED` |
| Public-safe runtime proof | `BLOCKED` |

Reviewer package candidate status means the bounded release packet can be reviewed through the public release route. It does not make raw runtime evidence public-safe, and it does not promote private/internal runtime evidence into public proof.

`NOT_PUBLIC_SAFE` runtime evidence may support internal review only. Public claims require evidence linkage, claim ceiling support, privacy review, stale review, wording review, and Raylee approval.

## Proof Pack 001 Release Contract

Proof Pack 001 has an official direct GitHub Release route in `hawkinsoperations-proof`:

[HawkinsOperations Proof Pack 001](https://github.com/HawkinsOperations/hawkinsoperations-proof/releases/tag/hawkinsoperations-proof-pack-001)

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

The release package does not prove runtime-active deployment, signal-observed proof, production readiness, Cribl/Wazuh/Splunk/AWS live proof, autonomous SOC operation, public-safe runtime proof, AI-approved disposition, analyst-approved disposition, or case closure.

## Lifetime Case Ledger Verification Badges

[![Ledger summary verifier](https://github.com/HawkinsOperations/hawkinsoperations-proof/actions/workflows/governance-gate.yml/badge.svg?branch=main&event=push)](https://github.com/HawkinsOperations/hawkinsoperations-proof/actions/workflows/governance-gate.yml?query=branch%3Amain)
[![Ledger proof bundle verifier](https://github.com/HawkinsOperations/hawkinsoperations-proof/actions/workflows/governance-gate.yml/badge.svg?branch=main&event=push)](https://github.com/HawkinsOperations/hawkinsoperations-proof/actions/workflows/governance-gate.yml?query=branch%3Amain)

These badges route to the `Governance Gate` workflow. The workflow contains the `lifetime-ledger-public-summary` and `lifetime-ledger-proof-bundle` jobs, which verify source-controlled Lifetime Case Ledger records against the pinned platform manifest.

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

## What This Repository Can Prove

| Proof surface | What it can support |
|---|---|
| Proof records | Claim ceilings, evidence links, blocked claims, and review state |
| Evidence bundles | Reviewed support for bounded claims within their recorded scope |
| Validation summaries | What was tested and under what validation scope |
| Case studies | Public-safe or reviewer-safe explanation only when their own text says so |
| Claim mapping | Which claims are supported, blocked, or not yet reviewed |

## What This Repository Does Not Prove

| Not proven by this repo alone | Why |
|---|---|
| Source correctness | Source truth belongs in detections and code review. |
| Test behavior beyond recorded validation | Validation truth belongs in validation records and verifier scope. |
| Live runtime state | Runtime evidence needs separate private review and promotion. |
| Public signal proof | Signal-observed public proof is blocked until approved. |
| Website truth | Website and GitHub pages are rendering and routing only. |
| Badge-as-proof authority | Badges show workflow status only. |
| Production readiness | Requires separately scoped evidence, review, and approval. |

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
- A reviewer candidate packet does not make private/runtime evidence public-safe.

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
| `HO-DET-001` has merged source artifacts. | Not claimed: runtime-active public proof. |
| `HO-DET-001` has merged controlled-test validation artifacts. | Not claimed: public signal-observed proof. |
| `HO-DET-001` passed controlled-test validation within recorded scope. | Not claimed: evidence-linked public proof beyond the stated ceiling. |
| Internal platform contract guardrail exists as a non-promotional guardrail. | Not claimed: public-safe runtime proof. |
| Private/internal runtime match status is scoped private/internal. | Not claimed: production-ready, fleet-wide, or enterprise-deployed status. |
| AI can support work but cannot approve claims. | Not claimed: live Splunk fired as public proof, Cribl-routed claim, Wazuh-routed claim, or AWS-live claim. |
| Human review is required before public promotion. | Not claimed: autonomous SOC, AI-approved disposition, AI-decided disposition, analyst-approved disposition, production AutoSOC, or case closure. |

## Real Controls Rule

Docs, READMEs, proof records, diagrams, websites, and badges are not real controls by themselves.

A control becomes real only when it blocks, fails, or forces correction through required review, branch protection, rulesets, blocking CI, deterministic verifiers, typed claim gates, or another enforceable mechanism.

Green CI/status checks are not merge authority. Codex review is AI labor, not human governance.

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
