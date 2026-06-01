# Runtime Route Proof v1 Private Candidate Map

## Status

| Field | Value |
|---|---|
| Map ID | runtime-route-proof-v1-private-candidate-map |
| Record | `proof/records/RUNTIME-ROUTE-PROOF-V1-PRIVATE-CANDIDATE.md` |
| JSON map | `proof/indexes/runtime-route-proof-v1-private-candidate-map.json` |
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

| Hop | Private receipt status | Repo boundary |
|---|---|---|
| Wazuh | PASS | Summary only; raw receipt excluded. |
| Cribl | PASS | Summary only; raw receipt excluded. |
| Splunk | PASS | Summary only; raw receipt excluded. |

## Reviewer-Safe Packet Reference

| Field | Value |
|---|---|
| Packet filename | HO-RUNTIME-ROUTE-PROOF-V1-PRIVATE-REVIEWER-SAFE-2026-06-01.zip |
| Packet SHA256 | 3a1d4472bffcce68cff6e101c54e06b5a67528338bda174e6fef209fa9b1b278 |
| Raw private evidence in repo | false |

## Boundary

This map routes reviewers to the proof candidate record and the platform packet verifier contract. It does not include raw runtime evidence and does not prove public-safe runtime proof, production operation, autonomous SOC behavior, AI-decided disposition, or any Lifetime Governed Case mutation. It does not mutate Lifetime Governed Cases.
