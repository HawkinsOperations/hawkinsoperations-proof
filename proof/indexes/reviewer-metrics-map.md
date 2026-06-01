# Reviewer Metrics Map

This map routes reviewers from each metric to its owning truth surface.

| Metric | Owner | Source artifact | Proof boundary |
| --- | --- | --- | --- |
| Lifetime Governed Cases | `hawkinsoperations-platform` | `contracts/lifetime-case-ledger-v1-state-manifest.json` | Strict governed case count only. |
| Detection Activity Count | `hawkinsoperations-validation` | `activity/detection-activity-ledger-v1.json` | Controlled validation positive fixture matches only. |
| Validation Case Count | `hawkinsoperations-validation` | `validation/VALIDATION_REGISTRY.yml` | Controlled fixture count only. |
| Proof Record Count | `hawkinsoperations-proof` | `proof/records/` | Source-controlled proof records only; no claim promotion. |
| Blocked Claims Count | `hawkinsoperations-proof` and `.github` | `proof/indexes/reviewer-proof-map.json`; `.github#10` | Blocked/prevented promotion visibility only. |
| Project Board Reconciliation Status | `.github` | `governance/ISSUE_FACTORY_CONTROL_RECEIPTS.md` | Board coordination status only, not proof authority. |

Website rendering is intentionally excluded from v1 implementation while website PR #47 remains open.
