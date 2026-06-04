# HawkinsOperations Proof

Claim-control authority for HawkinsOperations proof.

This repository turns detection, validation, platform, evidence, and reviewer work into bounded proof records, reviewer packages, claim ceilings, verifier routes, and promotion gates. It is the place a reviewer should use to see what HawkinsOperations can prove, how to verify it, and which security claims remain blocked.

AI can generate work. Evidence, deterministic checks, and human review authorize claims.

## 10-Second Proof Route

| Start here | What it shows | Verify with | Claim ceiling |
|---|---|---|---|
| [Proof Pack 001 release](https://github.com/HawkinsOperations/hawkinsoperations-proof/releases/tag/hawkinsoperations-proof-pack-001) | A real bounded reviewer release artifact for `HO-DET-001`. | ZIP SHA256 plus `scripts/verify-proof-pack-001-zip.py`. | `CONTROLLED_TEST_VALIDATED` |
| [HO-DET-001 proof record](proof/records/HO-DET-001.md) | The flagship detection proof route: source, Splunk source, controlled validation, proof-loop CI, private runtime context, blocked claims, and human review gates. | `scripts/verify-ho-det-001-proof-integrity.py` and `scripts/verify_proof_integrity.py`. | `CONTROLLED_TEST_VALIDATED`; private runtime context remains `NOT_PUBLIC_SAFE` |
| [Runtime Route Proof v1 reviewer map](proof/maps/RUNTIME-ROUTE-PROOF-V1-REVIEWER-MAP.md) | A private-candidate Wazuh -> Cribl -> Splunk route receipt for one controlled marker. | `scripts/verify-runtime-route-proof-v1-private-candidate-map.py`. | `PRIVATE_RUNTIME_ROUTE_PROOF_V1_CANDIDATE_PRESERVED`; `NOT_PUBLIC_SAFE` |
| [Reviewer Proof Map](proof/indexes/reviewer-proof-map.md) | Lifetime Case Ledger proof chain, 4 events / 4 cases, status-only badges, and render-only boundaries. | `scripts/verify-reviewer-proof-map.py`. | `SCHEMA_CONTRACT_VERIFIER_EXISTS_ONLY`; `NOT_PUBLIC_SAFE` |
| [Reviewer Metrics Pipeline v1 map](proof/indexes/reviewer-metrics-pipeline-v1-map.md) | Strict governed cases, validation activity, proof record count, and blocked promotions separated instead of inflated. | `scripts/verify-reviewer-metrics-summary.py`. | `REVIEWER_METRICS_PIPELINE_V1_CLOSED_REVIEWER_VISIBLE`; `NOT_PUBLIC_SAFE` |

## Strongest Current Receipts

| Receipt | Why it matters | What it proves | What it does not prove |
|---|---|---|---|
| Proof Pack 001 | A reviewer can verify a release artifact, SHA, manifest, and package boundary instead of reading claims on trust. | `HAWKINSOPERATIONS_PROOF_PACK_001.zip` exists as a bounded reviewer release route for `HO-DET-001`. | Runtime-active public proof, public signal proof, production readiness, public-safe runtime proof, autonomous SOC, AI-approved disposition, or analyst-approved disposition. |
| `HO-DET-001` proof record | The flagship proof route ties detection source, Splunk source, controlled validation, proof-loop enforcement, AI support boundary, and blocked claims together. | `HO-DET-001` is `CONTROLLED_TEST_VALIDATED` within controlled positive and negative process-creation fixture scope. | Live Splunk firing, Cribl-routed or Wazuh-routed public proof, AWS-live proof, production operation, fleet-wide coverage, or public-safe runtime proof. |
| Runtime Route Proof v1 | Shows route-proof discipline without promoting private runtime material into public proof. | One private controlled marker has reviewer-safe Wazuh, Cribl, and Splunk receipt summaries with verifier result `PASS_ROUTE_RECEIPTS`. | Public-safe proof, broad ingestion, production SOC operation, autonomous SOC behavior, AI-decided disposition, or public publication approval. |
| Lifetime Case Ledger / Reviewer Proof Map | Keeps count claims reviewable and bounded instead of turning metrics into proof. | The proof repo owns a reviewable 4 events / 4 cases summary and proof bundle route against a pinned platform manifest. | Runtime, signal, public-safe, deployment, disposition, case closure, badge-as-proof, website-as-proof, or Project-as-proof authority. |
| Reviewer Metrics Pipeline v1 | Gives reviewers the big numbers without collapsing strict case count, validation activity, and blocked claims into one unsafe claim. | 4 strict governed cases, 49 validation-backed activity/fire count, 106 validation cases, 8 proof records, 31 blocked/prevented promotions, and 0 public-safe runtime proofs are separated by authority surface. | Production volume, live telemetry, public runtime proof, public-safe status, GitHub Project proof authority, or AI/analyst disposition authority. |
| HO-DET-001 SOCaaS Pilot Receipt Pack | Shows the operating model for a security-operations reviewer: source -> validation -> case packet -> proof record -> reviewer route. | A bounded controlled-test receipt chain exists for reviewer inspection. | SOCaaS deployment, customer deployment, production readiness, FortiSIEM proof, autonomous response, or public-safe runtime proof. |
| AI Authority Boundary / Purple Team Closed Loop | Shows the rule that makes AI-assisted SOC work safe enough to inspect: AI supports, verifiers and humans govern. | AI support stayed support-only; deterministic checks preserved `AI_DECIDED_DISPOSITION=false`, `HUMAN_REVIEW_REQUIRED=true`, and `PUBLIC_SAFE_STATUS=NOT_PUBLIC_SAFE`. | AI authority, case closure, autonomous SOC, analyst-approved disposition, production AutoSOC, or public model-runtime proof. |

## Proof Pack 001 Quick Verification

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

Passing the checksum and ZIP verifier supports only this bounded claim: Proof Pack 001 is a real reviewer release artifact for `HO-DET-001` under `CONTROLLED_TEST_VALIDATED`. It does not prove runtime-active public proof, public signal-observed proof, production readiness, SOCaaS readiness, autonomous SOC operation, AI-approved disposition, analyst-approved disposition, or public-safe runtime proof.

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

Website and GitHub rendering route reviewers; rendering is not proof. The release package does not prove runtime-active deployment, signal-observed proof, production readiness, Cribl/Wazuh/Splunk/AWS live proof, autonomous SOC operation, public-safe runtime proof, AI-approved disposition, analyst-approved disposition, or case closure.

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

## Reviewer Metrics Pipeline v1

Use [proof/indexes/reviewer-metrics-pipeline-v1-map.md](proof/indexes/reviewer-metrics-pipeline-v1-map.md) for the proof-owned metrics route. It keeps strict governed cases separate from validation volume and proof-surface counts.

| Metric | Current value | Boundary |
|---|---:|---|
| Lifetime Governed Cases | 4 | Strict governed accepted case records only. |
| Detection Activity / Fire Count | 49 | Controlled validation-backed activity; not production telemetry. |
| Validation Case Count | 106 | Controlled validation case volume only. |
| Proof Record Count | 8 | Reviewer-safe proof surface count. |
| Blocked Claims / Prevented Promotions | 31 | Claim firewall count, not a failure or incident count. |
| Public-safe Count | 0 | No public-safe runtime proof has been approved. |

The metrics route is checked by:

```powershell
python scripts/verify-reviewer-metrics-summary.py
```

The metrics route does not prove live Wazuh telemetry, Cribl routing, Splunk indexing, production SOC operation, public-safe runtime proof, signal observation, AI authority, analyst disposition authority, or GitHub Project board proof authority.

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

- [HO-DET-001](proof/records/HO-DET-001.md)
- [RUNTIME-ROUTE-PROOF-V1-PRIVATE-CANDIDATE](proof/records/RUNTIME-ROUTE-PROOF-V1-PRIVATE-CANDIDATE.md)
- [HO-DET-011](proof/records/HO-DET-011.md)
- [HO-DET-012](proof/records/HO-DET-012.md)
- [AWS-DET-001](proof/records/AWS-DET-001.md)

Use [proof/records/README.md](proof/records/README.md) for the current proof-record route table and per-record blocked promotion gates. `HO-DET-011`, `HO-DET-012`, `AWS-DET-001`, identity detections, Cyber Kill Chain maps, and ATT&CK maps should be treated according to their own stated proof records or index rows; do not let their presence imply runtime, signal, public-safe, production, cloud-live, or fleet-wide proof.

## Case Studies

- [HO-DET-001 SOCaaS Pilot Receipt Pack](docs/case-studies/HO-DET-001-SOCAAS-PILOT-RECEIPT.md)
- [HO-DET-001: AI Authority Boundary Case Study](docs/case-studies/HO-DET-001-AI-AUTHORITY-BOUNDARY.md)
- [Purple Team Closed Loop 001](docs/case-studies/PURPLE-TEAM-CLOSED-LOOP-001.md)
- [Operations Accomplishment Ledger](docs/case-studies/OPERATIONS-ACCOMPLISHMENT-LEDGER.md)

Case studies explain the operating model and proof boundary. They do not create production deployment, public-safe runtime proof, customer deployment, autonomous SOC, AI-approved disposition, or analyst-approved disposition.

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
