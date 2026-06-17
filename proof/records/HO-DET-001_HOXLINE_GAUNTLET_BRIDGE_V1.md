# HO-DET-001 Hoxline Gauntlet Proof Bridge v1

## Header

| Field | Value |
|---|---|
| Artifact ID | `HO-DET-001` |
| Bridge record ID | `HO-DET-001_HOXLINE_GAUNTLET_PROOF_BRIDGE_V1` |
| Detection ID | `HO-DET-001` |
| Owner | `hawkinsoperations-proof` |
| Record type | Hoxline Gauntlet proof bridge |
| Proof ceiling | `CONTROLLED_TEST_VALIDATED` |
| Public-safe | `false` / `BLOCKED` |
| Human review required | `true` |

## Supported Bounded Claim

"HO-DET-001 has Hoxline Gauntlet v1 reviewer evidence and validation-bridge references under stated controlled scope."

## Hoxline Source Manifest

- Hoxline source repo: `HawkinsOperations/hoxline`
- Remote: `https://github.com/HawkinsOperations/hoxline.git`
- Branch: `feature/hoxline-gauntlet-v1-engine`
- Primary source manifest: `HawkinsOperations/hoxline/examples/gauntlet/ho-det-001-gauntlet-v1-source-manifest.json`
- Local checkout compatibility name: `aevumguard`
- Repo-relative manifest path: `examples/gauntlet/ho-det-001-gauntlet-v1-source-manifest.json`
- Manifest status: present and primary for this bridge.

## Primary Hoxline v1 Source Paths

- Gauntlet v1 run: `examples/gauntlet/ho-det-001-gauntlet-run-v1.json`
- Gauntlet v1 schema: `schemas/gauntlet-run-v1.schema.json`
- Overclaim fail-closed fixture: `examples/gauntlet/ho-det-001-gauntlet-run-v1-overclaim.json`
- Evidence Graph v1: `examples/gauntlet/ho-det-001-evidence-graph-v1.json`
- Evidence Graph v1 schema: `schemas/evidence-graph-v1.schema.json`
- ProofCard v1: `examples/gauntlet/ho-det-001-proofcard-v1.json`
- ProofCard v1 schema: `schemas/proofcard-v1.schema.json`
- Claim Authority decision v1: `examples/gauntlet/ho-det-001-claim-decision-v1.json`
- Claim Authority decision v1 schema: `schemas/claim-authority-decision-v1.schema.json`
- Gauntlet v1 doc: `docs/gauntlet/HOXLINE_GAUNTLET_V1.md`
- ProofCard v1 doc: `docs/proofcards/PROOFCARD_V1.md`
- Claim Authority v1 doc: `docs/claim-authority/CLAIM_AUTHORITY_V1.md`

## Compatibility v0 Paths

These paths are compatibility-only and are not primary proof authority:

- Gauntlet v0 run: `examples/gauntlet/ho-det-001-full-loop-run-v0.json`
- Gauntlet v0 schema: `schemas/gauntlet-full-loop-run-v0.schema.json`
- ProofCard v0 example: `examples/gauntlet/ho-det-001-proofcard-v0.json`
- Evidence Graph v0 example: `examples/gauntlet/ho-det-001-evidence-graph-v0.json`

## Validation Bridge Reference

The validation repo owns the validation bridge:

- Artifact ID: `HO-DET-001_HOXLINE_GAUNTLET_VALIDATION_BRIDGE_V1`
- Path: `validation/hoxline/ho-det-001-hoxline-gauntlet-validation-bridge-v1.json`
- Status: `VALIDATION_BRIDGE_REVIEWER_PATH_RECORDED`
- Allowed validation claim: "HO-DET-001 has Hoxline Gauntlet v1 reviewer-path validation under controlled scope."

## Hoxline Gauntlet Reference

- Repo: `HawkinsOperations/hoxline`
- Primary source manifest: `HawkinsOperations/hoxline/examples/gauntlet/ho-det-001-gauntlet-v1-source-manifest.json`
- Repo-relative manifest path: `examples/gauntlet/ho-det-001-gauntlet-v1-source-manifest.json`
- Output: `examples/gauntlet/ho-det-001-gauntlet-run-v1.json`
- Schema: `schemas/gauntlet-run-v1.schema.json`
- Overclaim fixture: `examples/gauntlet/ho-det-001-gauntlet-run-v1-overclaim.json`
- ProofCard v1: `examples/gauntlet/ho-det-001-proofcard-v1.json`
- Claim Authority decision v1: `examples/gauntlet/ho-det-001-claim-decision-v1.json`
- Verifier: `python -B -m hoxline gauntlet verify --input examples/gauntlet/ho-det-001-gauntlet-run-v1.json --schema schemas/gauntlet-run-v1.schema.json`

## Blocked Claims

- production ready
- runtime proven
- signal observed
- customer deployed
- SOCaaS deployed
- public-safe runtime proof
- AI approved
- analyst approved
- final authorization
- case closure

## Missing Evidence

- analyst_review_record
- case_closure_record
- customer_deployment_evidence
- deployment_evidence
- final_authorization_record
- human_review_gate_complete
- public_safe_authorization
- runtime_evidence
- service_deployment_evidence
- signal_observation_evidence

## Reviewer Commands

From `hawkinsoperations-proof`:

```powershell
python -B scripts/verify-hoxline-gauntlet-proof-bridge.py --format json
python -B scripts/verify-hoxline-gauntlet-proof-bridge.py --format json --hoxline-root ..\aevumguard
python -B scripts/verify_proof_integrity.py
python -B scripts/verify-reviewer-metrics-summary.py --format json
python -B scripts/verify-reviewer-metrics-pipeline-closeout.py --format json
python -B -m unittest discover -s tests
```

From sibling checkout `aevumguard`:

```powershell
python -B -m hoxline gauntlet verify --input examples/gauntlet/ho-det-001-gauntlet-run-v1.json --schema schemas/gauntlet-run-v1.schema.json
python -B -m hoxline gauntlet summarize --input examples/gauntlet/ho-det-001-gauntlet-run-v1.json
python -B -m hoxline claim-authority decide --input examples/gauntlet/ho-det-001-gauntlet-run-v1.json
python -B -m hoxline proofcard render --input examples/gauntlet/ho-det-001-gauntlet-run-v1.json
python -B -m hoxline gauntlet verify --input examples/gauntlet/ho-det-001-gauntlet-run-v1-overclaim.json --schema schemas/gauntlet-run-v1.schema.json
python -B -m hoxline gauntlet verify --input examples/gauntlet/ho-det-001-full-loop-run-v0.json --schema schemas/gauntlet-full-loop-run-v0.schema.json
```

The overclaim fixture is expected to fail closed with a nonzero verifier result.

## Website Rendering Boundary

Website rendering is not proof authority. No website edit is required for this bridge, and no website route may promote this bridge beyond source-owned validation/proof records.

## Proof Ceiling

This follow-up reconciles validation/proof bridge records to Hoxline Gauntlet v1 only. It does not create runtime truth, signal truth, public-safe status, customer deployment, SOCaaS deployment, production readiness, AI-approved disposition, analyst-approved disposition, final authorization, or case closure.

## Next Gate

`human_review_gate`
