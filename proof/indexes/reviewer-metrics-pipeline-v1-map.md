# Reviewer Metrics Pipeline v1 Map

This map is the proof-owned reviewer route for the "big number without lying" pipeline. It keeps strict governed cases separate from broader controlled validation activity.

Proof ceiling: `REVIEWER_METRICS_PIPELINE_V1_CLOSED_REVIEWER_VISIBLE`

Public-safe status: `NOT_PUBLIC_SAFE`

## Metrics

| Metric | Value | Authority repo | Source surface | Verifier command | Reviewer explanation | Does not prove |
| --- | ---: | --- | --- | --- | --- | --- |
| Lifetime Governed Cases | 4 | `hawkinsoperations-platform` | `contracts/lifetime-case-ledger-v1-state-manifest.json` | `python -B scripts/ho_factory.py lifetime-ledger-state-manifest-verify --repo-root .. --format json` | Strict governed accepted case records only. | Every detection fire, validation volume, runtime operation, or public-safe approval. |
| Detection Activity / Fire Count | 49 | `hawkinsoperations-validation` | `activity/detection-activity-ledger-v1.json` | `python -B scripts/verify-detection-activity-ledger.py --format json` | Controlled validation-backed activity/fire count. | Does not prove governed case count, public runtime proof, signal observation, or production operation. |
| Validation Case Count | 106 | `hawkinsoperations-validation` | `activity/detection-activity-ledger-v1.json` | `python -B scripts/verify-detection-activity-ledger.py --format json` | Controlled validation case volume. | Production telemetry, runtime deployment, or public-safe proof. |
| Proof Record Count | 8 | `hawkinsoperations-proof` | `proof/records/reviewer-metrics-pipeline-v1-summary.json` | `python -B scripts/verify-reviewer-metrics-summary.py --format json` | Reviewer-safe proof surface count. | Public-safe runtime approval, new runtime evidence, or production readiness. |
| Blocked Claims / Prevented Promotions | 31 | `hawkinsoperations-proof` | `proof/records/reviewer-metrics-pipeline-v1-summary.json` | `python -B scripts/verify-reviewer-metrics-summary.py --format json` | Claim firewall count for unsupported claims intentionally blocked. | Failure count, operational incident count, or runtime status. |
| Public-safe Count | 0 | `hawkinsoperations-proof` | `proof/records/reviewer-metrics-pipeline-v1-summary.json` | `python -B scripts/verify-reviewer-metrics-summary.py --format json` | No public-safe runtime proof has been approved. | Absence of engineering work, public-safe approval, or runtime proof. |
| Reviewer Demo Path / Project Board Reconciliation | `REPO_BACKED_RECONCILIATION_PLAN_NO_PROJECT_MUTATION` | `.github` | `profile/START_HERE.md` | `python -B scripts/verify-command-center-invariants.py` | Repo-backed reviewer routing with Project metadata kept coordination-only. | GitHub Project mutation, Project Board proof authority, merge authority, or runtime proof. |

## Reviewer Demo Path

1. Start here: `.github/profile/START_HERE.md`.
2. Strict number: Lifetime Governed Cases remains 4 and belongs to `hawkinsoperations-platform`.
3. Big activity number: Detection Activity / controlled validation fire count remains 49 and belongs to `hawkinsoperations-validation`.
4. Validation volume: Validation Case Count remains 106 and belongs to `hawkinsoperations-validation`.
5. Proof surfaces: Proof Record Count remains 8 and belongs to `hawkinsoperations-proof`.
6. Blocked claims: Blocked Claims / Prevented Promotions remains 31 and belongs to `hawkinsoperations-proof`.
7. Board status: Project Board reconciliation remains `REPO_BACKED_RECONCILIATION_PLAN_NO_PROJECT_MUTATION`.
8. What remains blocked: runtime, signal, public-safe, production, autonomous SOC, AI authority, analyst disposition authority, and GitHub Project proof authority.

## Authority Boundaries

- `hawkinsoperations-validation` owns Detection Activity / Fire Count and Validation Case Count.
- `hawkinsoperations-platform` owns strict Lifetime Governed Cases and the state contract.
- `hawkinsoperations-proof` owns reviewer-safe rollup, proof records, and blocked claims.
- `.github` owns command-center routing and reviewer navigation.
- `hawkinsoperations-website` is render-only and not proof authority.
- GitHub Project metadata is coordination-only and not proof authority.

## What This Does Not Prove

- does not prove live Wazuh telemetry
- does not prove Cribl routing
- does not prove Splunk indexing
- does not prove HO-GPU-01 triage
- does not prove production SOC operation
- does not prove public-safe runtime proof
- does not prove signal observation
- does not prove AI authority
- does not prove analyst disposition authority
- does not prove GitHub Project board proof authority
