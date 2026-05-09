# HawkinsOperations Proof Cards

Proof cards are reviewer-facing route and display artifacts. They do not create proof, promote claims, or replace proof records.

GitHub and website rendering remain non-proof. Public surfaces route reviewers to proof records, validation artifacts, boundary contracts, and the evidence ledger where available.

AI generates work. Evidence and human review authorize claims.

## Current Public Boundary

| Field | Current default |
|---|---|
| Public proof ceiling | TEST_VALIDATED_SYNTHETIC_SCOPE |
| Public-safe status | NOT_PUBLIC_SAFE |
| Rendering status | NON_PROOF_ROUTE_ONLY |

## Cards

| ID | Card | Record type | Supported claim ceiling | Public-safe status |
|---|---|---|---|---|
| HO-DET-001 | [HO-DET-001](HO-DET-001.md) | proof record | TEST_VALIDATED_SYNTHETIC_SCOPE | NOT_PUBLIC_SAFE |
| AWS-DET-001 | [AWS-DET-001](AWS-DET-001.md) | proof record | TEST_VALIDATED_SYNTHETIC_SCOPE | NOT_PUBLIC_SAFE |
| HO-NDR-001 | [HO-NDR-001](HO-NDR-001.md) | boundary contract | PRIVATE_NDR_MODULE_VISIBILITY_ROLLUP_DEFINED | NOT_PUBLIC_SAFE |

## Reviewer Use

Use these cards for fast orientation, then follow the artifact routes into the source records. If a card and a source record ever disagree, the source record and approved validation artifacts are the authority until the card is corrected.

## Blocked by Default

These cards do not support runtime-active, signal-observed, evidence-linked public proof, public-safe, production-ready, fleet-wide, enterprise-deployed, routed telemetry, cloud-live, autonomous SOC, AI-approved disposition, AI-decided disposition, analyst-approved disposition, or production AutoSOC claims unless a source record explicitly supports that claim and Raylee approves promotion.
