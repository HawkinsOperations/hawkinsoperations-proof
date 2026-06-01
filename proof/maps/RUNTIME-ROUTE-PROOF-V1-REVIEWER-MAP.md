# Runtime Route Proof v1 Reviewer Map

This is the fastest reviewer route for the Runtime Route Proof v1 Private Candidate. Read it as private candidate proof navigation, not as public-safe proof or production proof.

## Open This First

| Reviewer question | Open |
|---|---|
| What release packages the reviewer-safe material? | [Runtime Route Proof v1 Private Candidate prerelease](https://github.com/HawkinsOperations/hawkinsoperations-proof/releases/tag/runtime-route-proof-v1-private-candidate-2026-06-01) |
| What proof record states the claim boundary? | [Runtime Route Proof v1 proof record](../records/RUNTIME-ROUTE-PROOF-V1-PRIVATE-CANDIDATE.md) |
| What machine-readable map pins the proof facts? | [Private candidate map JSON](../indexes/runtime-route-proof-v1-private-candidate-map.json) |
| What human-readable map pins the proof facts? | [Private candidate map Markdown](../indexes/runtime-route-proof-v1-private-candidate-map.md) |
| What platform contract checks packet shape? | [Platform verifier](https://github.com/HawkinsOperations/hawkinsoperations-platform/blob/main/scripts/verify-runtime-route-proof-v1-private-candidate.py) |
| What platform schema defines the packet? | [Platform schema](https://github.com/HawkinsOperations/hawkinsoperations-platform/blob/main/contracts/schemas/runtime-route-proof-v1-private-candidate.schema.json) |
| What platform sample mirrors the packet facts? | [Platform sample](https://github.com/HawkinsOperations/hawkinsoperations-platform/blob/main/contracts/examples/runtime-route-proof-v1-private-candidate.sample.json) |

Private-review summary ZIP, raw evidence excluded, no public-safe release approval: `HO-RUNTIME-ROUTE-PROOF-V1-PRIVATE-REVIEWER-SAFE-2026-06-01.zip`

ZIP SHA256: `3a1d4472bffcce68cff6e101c54e06b5a67528338bda174e6fef209fa9b1b278`

## Executive Meaning

A single controlled private marker is summarized as having correlated Wazuh, Cribl, and Splunk private receipt statuses. This supports private-candidate route proof only; it does not claim public signal proof, production SOC operation, autonomous SOC proof, or broad-ingestion proof.

Route shorthand: Wazuh -> Cribl -> Splunk.

What happened tonight: the route evidence was preserved as reviewer-safe summaries, checked by deterministic proof/platform verifiers, and published as a private candidate prerelease while keeping `NOT_PUBLIC_SAFE`, `public_safe_count=0`, `Lifetime Governed Cases=4`, and `AI_DECIDED_DISPOSITION=false`.

## Route Map

| Step | What the reviewer should understand | Boundary |
|---|---|---|
| Detection marker | `HO-RUNTIME-V1-20260601T120922Z-BATCH764` is the controlled private marker. | Marker scope only. |
| Wazuh receipt | Wazuh receipt status is `PASS`. | Summary only; raw receipt excluded. |
| Cribl routed receipt | Cribl route status is `PASS` by source-attributed delivery evidence. | Not retained Cribl raw log-body proof. |
| Splunk Cribl-source receipt | Splunk receipt status is `PASS` for the marker under the Cribl HEC source path. | Private runtime evidence, not public signal proof. |
| Deterministic verifier | Runtime Route Proof v1 verifier returned `PASS_ROUTE_RECEIPTS` and `manifest_verified=true`. | Validation truth for this packet only. |
| Reviewer-safe packet | The packet pins summary files and SHA256. | Raw private evidence excluded. |
| Prerelease | GitHub prerelease preserves the reviewer-safe packet and boundaries. | Prerelease/private candidate only. |

## Proof State Ladder

| Proof state | Current value |
|---|---|
| Single controlled marker privately summarized | yes; not runtime-active public proof |
| Reviewer-safe packet | yes |
| Repo preserved | yes |
| Private-candidate GitHub prerelease route exists | yes; not public publication approval |
| Public-safe | no |
| Production | no |
| Autonomous SOC | no |
| AI-decided disposition | no |

## What This Proves

- Private controlled runtime route receipt correlation exists for the single marker `HO-RUNTIME-V1-20260601T120922Z-BATCH764`.
- For the single controlled marker only, Wazuh, Cribl, and Splunk private receipt statuses are `PASS`.
- The deterministic verifier passed with `PASS_ROUTE_RECEIPTS`.
- The private manifest verified successfully with `manifest_verified=true`.
- The reviewer-safe package hash is pinned.
- The proof boundary held: `NOT_PUBLIC_SAFE`, `public_safe_count=0`, `Lifetime Governed Cases=4`, and `AI_DECIDED_DISPOSITION=false`.

## What This Does Not Prove

- Public-safe runtime proof.
- Production SOC operation.
- Autonomous SOC behavior.
- AI-decided disposition.
- Lifetime Governed Case mutation.
- Broad Wazuh forwarding, broad Cribl routing, or broad Splunk ingestion.
- Customer deployment or fleet-wide deployment.
- Security Onion/NDR witness correlation.
- Public publication approval.

## Why It Matters

- It catches telemetry route and field-preservation failures instead of assuming the pipeline works.
- It prevents false proof promotion by separating private runtime evidence from public-safe proof.
- It shows source-controlled proof preservation, platform contract validation, and release packaging as separate truth surfaces.
- It keeps AI-assisted execution under human governance: AI can help package and explain, but cannot approve claims.
- It protects Splunk and Cribl evidence from being widened into broad-ingestion or production claims.

## Reviewer Walkthrough In 90 Seconds

1. Open the [prerelease](https://github.com/HawkinsOperations/hawkinsoperations-proof/releases/tag/runtime-route-proof-v1-private-candidate-2026-06-01).
2. Confirm the ZIP filename is `HO-RUNTIME-ROUTE-PROOF-V1-PRIVATE-REVIEWER-SAFE-2026-06-01.zip`.
3. Compare the ZIP SHA256 with `3a1d4472bffcce68cff6e101c54e06b5a67528338bda174e6fef209fa9b1b278`.
4. Open the [proof record](../records/RUNTIME-ROUTE-PROOF-V1-PRIVATE-CANDIDATE.md) and confirm the marker, route, verifier result, counts, and blocked claims.
5. Open the [map JSON](../indexes/runtime-route-proof-v1-private-candidate-map.json) and confirm the same facts are machine-readable.
6. Open the platform [schema](https://github.com/HawkinsOperations/hawkinsoperations-platform/blob/main/contracts/schemas/runtime-route-proof-v1-private-candidate.schema.json), [sample](https://github.com/HawkinsOperations/hawkinsoperations-platform/blob/main/contracts/examples/runtime-route-proof-v1-private-candidate.sample.json), and [verifier](https://github.com/HawkinsOperations/hawkinsoperations-platform/blob/main/scripts/verify-runtime-route-proof-v1-private-candidate.py) to see the packet contract.
7. Confirm blocked claims remain blocked: public-safe, production, autonomous SOC, AI disposition, broad ingestion, and governed-case mutation.

## Next Promotion Gate

Public-safe review requires a separate promotion lane. This reviewer map must not be used to imply public-safe proof, production operation, autonomous SOC behavior, broad ingestion, AI-decided disposition, public publication approval, or Lifetime Governed Case mutation.
