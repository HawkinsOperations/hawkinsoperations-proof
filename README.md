# HawkinsOperations Proof

Proof authority for HawkinsOperations.

`.github` routes the reviewer. `hawkinsoperations-platform` provides the executable contract, ledger, runtime-candidate, and control mechanics. `hawkinsoperations-proof` decides what can be claimed.

This repo owns the proof-facing layer: proof records, proof cards, proof maps, reviewer release packages, verifier-backed summaries, case studies, claim ceilings, and blocked-claim boundaries. It is where reviewer-visible security work turns into bounded proof instead of unsupported assertion.

AI can generate work. Evidence, deterministic checks, proof records, and human review authorize claims.

## 10-Second Proof Signal

| Proof signal | Route | What exists | Boundary |
|---|---|---|---|
| Proof Pack 001 | [GitHub release](https://github.com/HawkinsOperations/hawkinsoperations-proof/releases/tag/hawkinsoperations-proof-pack-001) | Bounded `HO-DET-001` reviewer ZIP, SHA256, release route, and verifier path. | `CONTROLLED_TEST_VALIDATED`; not public-safe runtime proof. |
| `HO-DET-001` proof route | [record](proof/records/HO-DET-001.md) / [card](proof/cards/HO-DET-001.md) | Flagship detection proof route for source, Splunk source, controlled validation, proof-loop checks, and blocked claims. | Runtime, signal, production, and public-safe claims remain blocked. |
| Reviewer Metrics Pipeline v1 | [map](proof/indexes/reviewer-metrics-pipeline-v1-map.md) / [summary](proof/records/reviewer-metrics-pipeline-v1-summary.json) | Reviewer-scale activity snapshot: validation activity, validation cases, proof records, blocked claims, and public-safe count. | The older `4/4` value in this snapshot is historical, not current governed ledger truth. |
| Runtime Route Proof v1 | [reviewer map](proof/maps/RUNTIME-ROUTE-PROOF-V1-REVIEWER-MAP.md) | Private-candidate Wazuh -> Cribl -> Splunk route summary for one controlled marker, plus prerelease route. | `NOT_PUBLIC_SAFE`; not broad ingestion, production, or public runtime proof. |
| Lifetime Case Ledger / Reviewer Proof Map | [reviewer map](proof/indexes/reviewer-proof-map.md) | Proof-owned ledger summary and proof-bundle route. | Current governed ledger truth comes from platform `6/6`; proof map `4/4` material is point-in-time proof-route context. |
| `HO-DET-001` SOCaaS Pilot Receipt Pack | [case study](docs/case-studies/HO-DET-001-SOCAAS-PILOT-RECEIPT.md) | Source -> validation -> platform case-packet shape -> proof record -> reviewer route narrative. | Case study only; not deployment, customer, production, or runtime proof. |
| AI Authority Boundary | [case study](docs/case-studies/HO-DET-001-AI-AUTHORITY-BOUNDARY.md) | AI support-only triage boundary with deterministic verifier expectations. | AI does not decide disposition, approve proof, close cases, or promote public wording. |
| Purple Team Closed Loop 001 | [case study](docs/case-studies/PURPLE-TEAM-CLOSED-LOOP-001.md) | Controlled-test loop showing detection behavior, validation, case packet, support-only AI, and authority checks. | Controlled-test story only; not live production operation. |

## Current Proof Numbers

Use these numbers as separate truth surfaces. Do not add candidates, validation activity, proof records, or blocked-claim counts into governed cases.

| Number | Current value | Source boundary |
|---|---:|---|
| Lifetime Governed Cases | 6 | Current platform ledger truth from `hawkinsoperations-platform/contracts/lifetime-case-ledger-v1-state-manifest.json`. |
| Lifetime Ledger events | 6 | Current platform ledger truth from the same state manifest. |
| Windows Runtime Collector candidates | 1 | Platform runtime-candidate lane; private candidate only. |
| Linux Runtime Collector candidates | 1 | Platform runtime-candidate lane; private candidate only. |
| Normalized append-ready candidates | 2 | Platform normalizer output; append required explicit approval and verifier gates. |
| Duplicate normalized candidates | 0 | Platform dedupe check result. |
| Public-safe cases | 0 | No public-safe case promotion. |
| Closed cases | 0 | No case closure authority. |
| Controlled validation activity fires / detection activity records | 49 | Reviewer activity metric, not governed cases or runtime signals. |
| Validation cases | 106 | Controlled validation volume, not production coverage. |
| Proof records | 8 | Proof-record routing count, not public-safe approval. |
| Blocked claims | 31 | Claim-control count, not missing functionality. |

`contracts/reviewer-metrics-pipeline-v1-state.json` in `hawkinsoperations-platform` and this repo's Reviewer Metrics Pipeline v1 proof summary still include a `4/4` closeout snapshot. Treat that as historical point-in-time reviewer metrics context only. Current governed ledger truth is `6/6` from the platform ledger state manifest and canonical ledger route.

Proof does not own ledger mechanics. Proof owns the claim boundary around proof-facing summaries and reviewer routes.

## Lifetime Case Ledger Verification Badges

[![Ledger summary verifier](https://github.com/HawkinsOperations/hawkinsoperations-proof/actions/workflows/governance-gate.yml/badge.svg?branch=main&event=push)](https://github.com/HawkinsOperations/hawkinsoperations-proof/actions/workflows/governance-gate.yml?query=branch%3Amain)
[![Ledger proof bundle verifier](https://github.com/HawkinsOperations/hawkinsoperations-proof/actions/workflows/governance-gate.yml/badge.svg?branch=main&event=push)](https://github.com/HawkinsOperations/hawkinsoperations-proof/actions/workflows/governance-gate.yml?query=branch%3Amain)

These badges route to the `Governance Gate` workflow. The workflow contains the `lifetime-ledger-public-summary` and `lifetime-ledger-proof-bundle` jobs, which verify source-controlled Lifetime Case Ledger records against the pinned platform manifest.

| Badge | Verifier job | What it verifies | Boundary |
|---|---|---|---|
| Ledger summary verifier | `lifetime-ledger-public-summary` | Proof-owned summary route and platform-manifest reference. | Ledger status remains `NOT_PUBLIC_SAFE`; proof ceiling remains `SCHEMA_CONTRACT_VERIFIER_EXISTS_ONLY`. |
| Ledger proof bundle verifier | `lifetime-ledger-proof-bundle` | Proof-owned reviewer bundle route and verifier command references. | Ledger status remains `NOT_PUBLIC_SAFE`; proof ceiling remains `SCHEMA_CONTRACT_VERIFIER_EXISTS_ONLY`. |

Badges report GitHub Actions workflow check status only. They do not prove runtime activity, signal observation, public proof, public-safe runtime proof, SOCaaS deployment, production deployment, autonomous SOC authority, AI-approved disposition, analyst-approved disposition, or case closure.

## What Proof Owns

- Proof records and proof cards.
- Proof packs, release routes, checksums, manifests, and reviewer packages.
- Proof maps, proof indexes, and reviewer handoffs.
- Verifier-backed proof summaries.
- Case studies that explain the operating model and proof boundary.
- Claim ceilings, blocked-claim boundaries, and promotion gates.
- Public/reviewer wording discipline for proof-facing surfaces.

## What Proof Does Not Own

| Surface | Owner | Proof boundary |
|---|---|---|
| Detection source truth | `hawkinsoperations-detections` | Proof may cite source routes, but source existence is not runtime truth. |
| Validation behavior truth | `hawkinsoperations-validation` | Proof may cite validation results, but validation truth is limited to the checked scope. |
| Platform mechanics, ledger, contracts, runtime candidates | `hawkinsoperations-platform` | Proof may route current platform numbers, but platform owns the executable mechanics. |
| Runtime system truth | runtime/lab systems | Runtime truth requires separate approved runtime evidence and review. |
| Signal-observed truth | SIEM/log/telemetry systems | Signal truth requires preserved signal evidence and review. |
| Website rendering truth | `hawkinsoperations-website` | Website pages route reviewers; rendering is not proof. |
| Command-center routing | `.github` | `.github` routes reviewers and authority boundaries; it does not create proof. |
| GitHub Project metadata | private project board | Project metadata is coordination only, not proof or approval. |

## Artifact Ladder

| Artifact | Route | What exists | Why it matters | Boundary |
|---|---|---|---|---|
| Proof Pack 001 | [release](https://github.com/HawkinsOperations/hawkinsoperations-proof/releases/tag/hawkinsoperations-proof-pack-001), `RELEASE_MANIFEST.json`, `SHA256SUMS.txt` | A bounded reviewer ZIP route for `HO-DET-001`. | Gives reviewers a concrete package, checksum, and verifier path. | Does not publish raw runtime evidence or raise the public ceiling. |
| `HO-DET-001` proof record/card | [record](proof/records/HO-DET-001.md), [card](proof/cards/HO-DET-001.md) | Detection source, Splunk source, controlled validation, private runtime context, proof-loop references, and blocked claims. | Shows the strongest proof path for one concrete security detection. | Public ceiling remains `CONTROLLED_TEST_VALIDATED`; public-safe remains `NOT_PUBLIC_SAFE`. |
| `HO-DET-001` SOCaaS Pilot Receipt Pack | [case study](docs/case-studies/HO-DET-001-SOCAAS-PILOT-RECEIPT.md) | Reviewer narrative for source, validation, case-packet, proof, and rendering handoff. | Explains the operating model for SOC automation review without requiring private evidence. | Does not claim SOCaaS deployment, customer deployment, production, or runtime proof. |
| Reviewer Metrics Pipeline v1 | [map](proof/indexes/reviewer-metrics-pipeline-v1-map.md), [summary JSON](proof/records/reviewer-metrics-pipeline-v1-summary.json), [summary MD](proof/records/reviewer-metrics-pipeline-v1-summary.md) | Proof-bounded metrics snapshot with 49 activity fires, 106 validation cases, 8 proof records, 31 blocked claims, and 0 public-safe runtime proofs. | Shows scale without lying about governed cases or runtime truth. | Its `4/4` ledger fields are historical snapshot values; current governed truth is platform `6/6`. |
| Runtime Route Proof v1 | [reviewer map](proof/maps/RUNTIME-ROUTE-PROOF-V1-REVIEWER-MAP.md), [proof record](proof/records/RUNTIME-ROUTE-PROOF-V1-PRIVATE-CANDIDATE.md), [map JSON](proof/indexes/runtime-route-proof-v1-private-candidate-map.json) | Private-candidate route summary for one Wazuh -> Cribl -> Splunk marker, verifier result `PASS_ROUTE_RECEIPTS`, and prerelease route. | Shows runtime-route proof discipline while keeping private evidence private. | `NOT_PUBLIC_SAFE`; does not prove broad ingestion, production operation, or public runtime proof. |
| Lifetime Case Ledger / Reviewer Proof Map | [reviewer map](proof/indexes/reviewer-proof-map.md), [public summary](proof/records/lifetime-case-ledger-v1-public-summary.json), [proof bundle](proof/records/lifetime-case-ledger-v1-proof-bundle.json) | Proof-owned point-in-time ledger proof chain and reviewer route. | Shows how ledger summaries are bounded, verified, and separated from presentation. | Current ledger truth is platform `6/6`; older proof map `4/4` material is not current governed truth. |
| AI Authority Boundary | [case study](docs/case-studies/HO-DET-001-AI-AUTHORITY-BOUNDARY.md) | Support-only AI triage boundary and deterministic authority expectations. | Shows the safety rule for AI-assisted SOC work: model output is labor, not authority. | AI cannot approve, promote, decide disposition, close cases, or mark public-safe. |
| Purple Team Closed Loop 001 | [case study](docs/case-studies/PURPLE-TEAM-CLOSED-LOOP-001.md) | Controlled-test loop across detection behavior, validation, case-packet support, AI boundary, and proof ceiling. | Gives a reviewer an end-to-end controlled security-operations story. | Does not prove production, live signal, public-safe runtime proof, or autonomous operation. |
| Operations Accomplishment Ledger | [case study](docs/case-studies/OPERATIONS-ACCOMPLISHMENT-LEDGER.md) | GitHub-backed accomplishment inventory with proof boundaries and website-use recommendations. | Helps reviewers see what was produced without importing private evidence. | Summary artifact only; does not approve publication or stronger claims. |
| Proof verifier stack | `scripts/` | Integrity, release, metrics, runtime-route, reviewer-map, ledger-bundle, badge, and proof-index verifiers. | Makes proof claims checkable instead of rhetorical. | Verifier success proves only the checked verifier scope; CI is not approval. |

## 60-Second Reviewer Path

1. Open [Proof Pack 001](https://github.com/HawkinsOperations/hawkinsoperations-proof/releases/tag/hawkinsoperations-proof-pack-001) and verify the release route, ZIP name, and SHA256.
2. Open the [`HO-DET-001` proof record](proof/records/HO-DET-001.md) and [proof card](proof/cards/HO-DET-001.md).
3. Open the [Reviewer Metrics Pipeline v1 map](proof/indexes/reviewer-metrics-pipeline-v1-map.md), then treat its `4/4` ledger fields as historical and use platform for current `6/6`.
4. Open the [Runtime Route Proof v1 reviewer map](proof/maps/RUNTIME-ROUTE-PROOF-V1-REVIEWER-MAP.md).
5. Open the [`HO-DET-001` SOCaaS Pilot Receipt Pack](docs/case-studies/HO-DET-001-SOCAAS-PILOT-RECEIPT.md).
6. Run the proof verifier commands below from this repository root.

## Verifier Commands

These commands exist in this repository. They are PowerShell-friendly and should be run from the repository root.

```powershell
python -B scripts\verify-ho-det-001-proof-integrity.py
python -B scripts\verify_proof_integrity.py
python -B scripts\verify-proof-pack-001-release.py
python -B scripts\verify-reviewer-proof-map.py --platform-root ..\hawkinsoperations-platform --github-root ..\.github
python -B scripts\verify-reviewer-metrics-summary.py
python -B scripts\verify-runtime-route-proof-v1-private-candidate-map.py
```

Proof Pack 001 ZIP payload verification requires the release ZIP to be present locally:

```powershell
python -B scripts\verify-proof-pack-001-zip.py .\HAWKINSOPERATIONS_PROOF_PACK_001.zip
```

## Claim Discipline

Blocked claims are a proof firewall, not an apology. They show that proof records are enforcing the difference between work produced, behavior validated, runtime evidence preserved, public-safe material approved, and claims authorized.

Public-safe, runtime-active, signal-observed, production, SOCaaS deployment, customer deployment, FortiSIEM integration-proven, autonomous SOC, AI-approved disposition, AI-decided disposition, analyst-approved disposition, live Splunk, Cribl-routed public proof, Wazuh-routed public proof, AWS-live, fleet-wide, case closure, website-as-proof, GitHub-rendering-as-proof, GitHub-Project-as-proof, and green-CI-as-approval claims remain blocked unless a proof record, evidence, review, and explicit approval support the exact stronger claim.

## Related Repositories

| Repo | Role |
|---|---|
| `.github` | Command center, reviewer routing, and authority explanation. |
| `hawkinsoperations-platform` | Executable control mechanics, contracts, ledgers, runtime-candidate gates, and metrics state. |
| `hawkinsoperations-detections` | Detection source truth. |
| `hawkinsoperations-validation` | Controlled behavior truth and validation evidence. |
| `hawkinsoperations-website` | Public rendering and reviewer navigation only. |

## Bottom Line

This repo is the claim-authority layer for HawkinsOperations proof. It turns artifacts into bounded receipts, verifier routes, proof ceilings, reviewer packages, and blocked-claim gates.

Build loud. Verify hard. Claim tight. Ship receipts.
