# Runtime Route Proof v1 Private Candidate Map

## Status

| Field | Value |
|---|---|
| Map ID | runtime-route-proof-v1-private-candidate-map |
| Reviewer map | `proof/maps/RUNTIME-ROUTE-PROOF-V1-REVIEWER-MAP.md` |
| Record | `proof/records/RUNTIME-ROUTE-PROOF-V1-PRIVATE-CANDIDATE.md` |
| JSON map | `proof/indexes/runtime-route-proof-v1-private-candidate-map.json` |
| Prerelease | https://github.com/HawkinsOperations/hawkinsoperations-proof/releases/tag/runtime-route-proof-v1-private-candidate-2026-06-01 |
| Release tag | runtime-route-proof-v1-private-candidate-2026-06-01 |
| Marker ID | HO-RUNTIME-V1-20260601T120922Z-BATCH764 |
| Private route | Wazuh -> Cribl -> Splunk |
| Deterministic verifier | PASS_ROUTE_RECEIPTS |
| Manifest verified | true |
| Proof ceiling | PRIVATE_RUNTIME_ROUTE_PROOF_V1_CANDIDATE |
| Preservation ceiling | PRIVATE_RUNTIME_ROUTE_PROOF_V1_CANDIDATE_PRESERVED |
| Public-safe status | NOT_PUBLIC_SAFE |
| Lifetime Governed Cases | 4 |
| Public-safe count | 0 |

## Route

| Hop | Private receipt status | What PASS means | Repo boundary |
|---|---|---|---|
| Wazuh | PASS | The marker had a private Wazuh receipt in the controlled route proof packet. | Summary only; raw receipt excluded. |
| Cribl | PASS | The same marker had source-attributed Cribl route evidence in the controlled route proof packet. | Summary only; raw receipt excluded. |
| Splunk | PASS | The same marker had a private Splunk Cribl-source receipt in the controlled route proof packet. | Summary only; raw receipt excluded. |

## Reviewer-Safe Packet Reference

| Field | Value |
|---|---|
| Packet filename | HO-RUNTIME-ROUTE-PROOF-V1-PRIVATE-REVIEWER-SAFE-2026-06-01.zip |
| Packet SHA256 | 3a1d4472bffcce68cff6e101c54e06b5a67528338bda174e6fef209fa9b1b278 |
| Raw private evidence in repo | false |

## Claim Boundary

| Boundary | Value |
|---|---|
| public_safe_runtime_proof | false |
| production_soc_operation | false |
| autonomous_soc_operation | false |
| ai_decided_disposition | false |
| lifetime_governed_case_mutation | false |
| public_publication_approved | false |
| human_review_required | true |

## Boundary

This map routes reviewers to the proof candidate record and the platform packet verifier contract. It does not include raw runtime evidence and does not prove public-safe runtime proof, production SOC operation, autonomous SOC behavior, AI-decided disposition, or any Lifetime Governed Case mutation. It does not mutate Lifetime Governed Cases.

For a two-minute reviewer path through the release, proof record, machine map, packet hash, platform verifier, and blocked claims, start with [Runtime Route Proof v1 Reviewer Map](../maps/RUNTIME-ROUTE-PROOF-V1-REVIEWER-MAP.md).
