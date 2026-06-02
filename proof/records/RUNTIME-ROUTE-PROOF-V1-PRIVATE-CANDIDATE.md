# Runtime Route Proof v1 Private Candidate

## Status

| Field | Value |
|---|---|
| Record ID | RUNTIME-ROUTE-PROOF-V1-PRIVATE-CANDIDATE |
| Published prerelease URL | https://github.com/HawkinsOperations/hawkinsoperations-proof/releases/tag/runtime-route-proof-v1-private-candidate-2026-06-01 |
| Release tag | runtime-route-proof-v1-private-candidate-2026-06-01 |
| Marker ID | HO-RUNTIME-V1-20260601T120922Z-BATCH764 |
| Private route | Wazuh -> Cribl -> Splunk |
| Wazuh receipt | PASS |
| Cribl receipt | PASS |
| Splunk receipt | PASS |
| Deterministic verifier | PASS_ROUTE_RECEIPTS |
| Manifest verified | true |
| Lifetime Governed Cases | 4 |
| Public-safe count | 0 |
| Public-safe status | NOT_PUBLIC_SAFE |
| Proof ceiling | PRIVATE_RUNTIME_ROUTE_PROOF_V1_CANDIDATE |
| Preservation ceiling | PRIVATE_RUNTIME_ROUTE_PROOF_V1_CANDIDATE_PRESERVED |
| AI-decided disposition | false |

## Evidence Summary

This record preserves a private controlled runtime route receipt correlation for Runtime Route Proof v1. The successful marker `HO-RUNTIME-V1-20260601T120922Z-BATCH764` produced correlated Wazuh, Cribl, and Splunk receipt status after delayed read-only source-attribution verification.

The same marker is correlated across all three private route receipts. `PASS_ROUTE_RECEIPTS` is the private runtime verifier result preserved by this record; the repository verifier checks that the map, record, reviewer navigation, and claim boundaries remain preserved, but it does not re-run Wazuh, Cribl, or Splunk.

The proof ceiling names the private candidate claim. The preservation ceiling names the source-controlled retention of the reviewer-safe private candidate summary, not public-safe approval.

The private route proof is represented in this repository only through reviewer-safe summary facts and hashes. Raw private runtime receipts, raw payloads, local evidence paths, private host details, tokens, secrets, and internal network details are intentionally excluded from this repository.

## Reviewer Navigation

- Start here: [Runtime Route Proof v1 Reviewer Map](../maps/RUNTIME-ROUTE-PROOF-V1-REVIEWER-MAP.md).
- Published private-candidate prerelease: [Runtime Route Proof v1 Private Candidate](https://github.com/HawkinsOperations/hawkinsoperations-proof/releases/tag/runtime-route-proof-v1-private-candidate-2026-06-01).
- Machine-readable proof map: [runtime-route-proof-v1-private-candidate-map.json](../indexes/runtime-route-proof-v1-private-candidate-map.json).
- Platform packet verifier: [verify-runtime-route-proof-v1-private-candidate.py](https://github.com/HawkinsOperations/hawkinsoperations-platform/blob/main/scripts/verify-runtime-route-proof-v1-private-candidate.py).
- Platform packet schema: [runtime-route-proof-v1-private-candidate.schema.json](https://github.com/HawkinsOperations/hawkinsoperations-platform/blob/main/contracts/schemas/runtime-route-proof-v1-private-candidate.schema.json).
- Platform packet sample: [runtime-route-proof-v1-private-candidate.sample.json](https://github.com/HawkinsOperations/hawkinsoperations-platform/blob/main/contracts/examples/runtime-route-proof-v1-private-candidate.sample.json).

Use the reviewer map for the 90-second route through the prerelease, proof record, map JSON, packet hash, platform schema/sample/verifier, and blocked claims.

## Reviewer-Safe Packet

| Field | Value |
|---|---|
| Packet filename | HO-RUNTIME-ROUTE-PROOF-V1-PRIVATE-REVIEWER-SAFE-2026-06-01.zip |
| Packet SHA256 | 3a1d4472bffcce68cff6e101c54e06b5a67528338bda174e6fef209fa9b1b278 |
| Packet custody | GitHub prerelease asset contains reviewer-safe package material; private operator evidence store contains raw private evidence; repo contains summary facts and hashes only. |
| Packet status | PRIVATE_REVIEWER_SAFE_SUMMARY |

## What This Proves

- A successful private Runtime Route Proof v1 marker exists.
- Wazuh, Cribl, and Splunk private route receipts correlate for the marker.
- The deterministic route verifier passed with `PASS_ROUTE_RECEIPTS`.
- The private receipt manifest verified successfully.
- Lifetime Governed Cases remained 4.
- Public-safe count remained 0.
- Reviewer-safe packet material exists outside this repository and has a pinned SHA256.

## What This Does Not Prove

- It does not prove public-safe runtime proof.
- It does not prove production SOC operation.
- It does not prove autonomous SOC operation.
- It does not prove broad Wazuh forwarding, broad Cribl routing, or broad Splunk ingestion.
- It does not prove fleet-wide deployment or customer deployment.
- It does not authorize AI-decided disposition, analyst-approved disposition, containment, closure, or suppression.
- It does not mutate Lifetime Governed Cases.
- It does not approve public publication.

## Blocked Claims

- public-safe runtime proof
- production SOC operation
- autonomous SOC operation
- AI-decided disposition
- analyst-approved disposition
- Lifetime Governed Case mutation
- broad ingestion
- broad deployment
- public publication approval

## Human Review Boundary

This record is source-controlled proof-boundary preservation only. Human governance review is still required before any public-safe candidate review, public wording change, release wording, website wording, LinkedIn wording, recruiter-facing wording, or stronger claim ceiling.

Visible GitHub review activity may support governance traceability, but repository presence and CI checks do not promote this private candidate to public-safe proof.
