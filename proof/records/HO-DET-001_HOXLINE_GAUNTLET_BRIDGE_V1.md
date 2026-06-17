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

"HO-DET-001 has Hoxline Gauntlet reviewer evidence and validation-bridge references under stated controlled scope."

## Source Paths

- Hoxline repo: `HawkinsOperations/aevumguard`
- Hoxline Gauntlet JSON: `examples/gauntlet/ho-det-001-full-loop-run-v0.json`
- Hoxline Gauntlet Markdown: `examples/gauntlet/ho-det-001-full-loop-run-v0.md`
- Hoxline Gauntlet schema: `schemas/gauntlet-full-loop-run-v0.schema.json`
- Hoxline ProofCard example: `examples/gauntlet/ho-det-001-proofcard-v0.json`
- Validation bridge JSON: `hawkinsoperations-validation/validation/hoxline/ho-det-001-hoxline-gauntlet-validation-bridge-v1.json`
- Validation bridge Markdown: `hawkinsoperations-validation/validation/hoxline/HO-DET-001_HOXLINE_GAUNTLET_VALIDATION_BRIDGE_V1.md`
- Proof map JSON: `proof/indexes/hoxline-gauntlet-proof-map-v1.json`
- Proof map Markdown: `proof/indexes/hoxline-gauntlet-proof-map-v1.md`

## Validation Bridge Reference

The validation repo owns the validation bridge:

- Artifact ID: `HO-DET-001_HOXLINE_GAUNTLET_VALIDATION_BRIDGE_V1`
- Path: `validation/hoxline/ho-det-001-hoxline-gauntlet-validation-bridge-v1.json`
- Status: `VALIDATION_BRIDGE_REVIEWER_PATH_RECORDED`
- Allowed validation claim: "HO-DET-001 has Hoxline Gauntlet reviewer-path validation under controlled scope."

## Hoxline Gauntlet Reference

- Repo: `HawkinsOperations/aevumguard`
- Output: `examples/gauntlet/ho-det-001-full-loop-run-v0.json`
- Schema: `schemas/gauntlet-full-loop-run-v0.schema.json`
- Verifier: `python -B -m hoxline gauntlet verify --input examples/gauntlet/ho-det-001-full-loop-run-v0.json --schema schemas/gauntlet-full-loop-run-v0.schema.json`

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

- runtime_evidence
- signal_observation_evidence
- public_safe_authorization
- human_review_gate_complete
- analyst_review_record
- customer_deployment_evidence
- service_deployment_evidence
- final_authorization_record
- case_closure_record

## Reviewer Commands

From `hawkinsoperations-proof`:

```powershell
python -B scripts/verify-hoxline-gauntlet-proof-bridge.py --format json
python -B scripts/verify_proof_integrity.py
python -B scripts/verify-reviewer-metrics-summary.py --format json
python -B scripts/verify-reviewer-metrics-pipeline-closeout.py --format json
```

From sibling checkout `aevumguard`:

```powershell
python -B -m hoxline gauntlet verify --input examples/gauntlet/ho-det-001-full-loop-run-v0.json --schema schemas/gauntlet-full-loop-run-v0.schema.json
```

## Website Rendering Boundary

Website rendering is not proof authority. No website edit is required for this bridge, and no website route may promote this bridge beyond source-owned validation/proof records.

## Proof Ceiling

This sprint adds source-owned validation/proof bridge records only. It does not create runtime truth, signal truth, public-safe status, customer deployment, SOCaaS deployment, production readiness, AI-approved disposition, analyst-approved disposition, final authorization, or case closure.

## Next Gate

Cross-repo reviewer review, privacy/stale/wording review, and explicit human approval are required before any stronger runtime, signal, public-safe, production, customer, SOCaaS, AI, analyst, authorization, or closure wording.
