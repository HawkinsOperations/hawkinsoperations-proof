# What the System Refused to Claim

This packet supports a public LinkedIn visual about HawkinsOperations proof boundaries. It shows what current public artifacts can support and what remains explicitly blocked.

It is a reviewer-routing and proof-boundary packet. It is not runtime proof, signal proof, production proof, external-use authorization, or public-safe runtime proof.

## 1. Visual Summary Table

| Artifact | What it proves | What it does not prove |
|---|---|---|
| Detection Source | Source exists and can be reviewed. | Does not prove runtime behavior, live signal, production deployment, or public-safe runtime proof. |
| Validation | Controlled validation boundary under scoped test conditions. | Does not prove live signal, runtime route, production deployment, or public-safe runtime proof. |
| Website | Reviewer navigation and public route rendering. | Does not prove proof authority, runtime truth, signal truth, evidence truth, or external-use authorization. |
| Proof Pack 001 | Bounded reviewer release route for HO-DET-001 under CONTROLLED_TEST_VALIDATED. | Does not prove public-safe runtime proof, production deployment, SOCaaS availability, autonomous SOC, or AI-approved disposition. |
| AI Support | Drafting, reviewer prep, triage scaffolding, and summarization support. | Does not prove final security disposition authority, analyst-approved disposition, autonomous SOC operation, or human approval replacement. |

## 2. Public-Safe Artifact Map

| Artifact | Public source | Supported claim | Blocked claim | Proof ceiling |
|---|---|---|---|---|
| Detection Source | `hawkinsoperations-detections` source routes and `proof/records/HO-DET-001.md` | HO-DET-001 source exists and can route reviewers toward validation and proof records. | Do not claim runtime behavior, live signal, production deployment, public-safe runtime proof, or live tool proof. | Source truth plus CONTROLLED_TEST_VALIDATED references; NOT_PUBLIC_SAFE for runtime/public-safe proof. |
| Validation | `hawkinsoperations-validation` reports and proof-loop routes referenced by `proof/records/HO-DET-001.md` | HO-DET-001 has controlled-test validation under scoped positive and negative fixture conditions. | Do not claim runtime route, live signal, production deployment, autonomous SOC, AI-approved disposition, analyst-approved disposition, or public-safe runtime proof. | CONTROLLED_TEST_VALIDATED; NOT_PUBLIC_SAFE for runtime/public-safe proof. |
| Website | `hawkinsoperations-website` proof routes and `https://hawkinsoperations.com/proof/ho-det-001/` | Website rendering can guide reviewers to the current boundary and proof routes. | Do not claim website rendering creates proof authority, runtime truth, signal truth, or public-safe status. | Reviewer navigation only; rendering is not proof. |
| Proof Pack 001 | `hawkinsoperations-proof` release route and proof pack checks | Proof Pack 001 is a bounded reviewer package route for HO-DET-001. | Do not claim the pack proves runtime-active public proof, public signal proof, production readiness, SOCaaS availability, autonomous SOC, AI-approved disposition, analyst-approved disposition, or public-safe runtime proof. | CONTROLLED_TEST_VALIDATED; bounded reviewer release route only. |
| AI Support | AI authority boundary case study, proof record boundaries, and platform support contracts | AI may support drafting, reviewer prep, triage scaffolding, and summarization. | Do not claim AI approves disposition, containment, case closure, proof promotion, release authority, runtime-active status, or signal-observed public proof. | AI labor/support only; governance remains authority. |

## 3. What This Packet Proves

- HawkinsOperations uses separate public surfaces for source, validation, website routing, proof packages, and AI support.
- The public HO-DET-001 ceiling remains CONTROLLED_TEST_VALIDATED.
- Runtime-active public proof remains blocked.
- Public signal-observed proof remains blocked.
- Public-safe runtime proof remains blocked.
- Website rendering routes reviewers but does not create proof.
- AI support remains labor and does not replace evidence or human governance.

## 4. What This Packet Does Not Prove

- It does not prove runtime behavior.
- It does not prove live signal.
- It does not prove production deployment.
- It does not prove customer deployment.
- It does not prove SOCaaS availability.
- It does not prove autonomous SOC operation.
- It does not prove AI-approved disposition.
- It does not prove analyst-approved disposition.
- It does not approve public-safe runtime proof.

## 5. Claim Boundary Rules

- Source truth can prove source exists. It does not prove runtime behavior.
- Validation truth can prove controlled validation under scoped conditions. It does not prove live signal.
- Website rendering can route reviewers. It does not create proof authority.
- Proof Pack 001 can support a bounded reviewer release route. It does not raise the public ceiling.
- AI support can help draft and summarize. It does not approve final security decisions or claim promotion.

## 6. Reviewer Links

- Public first-comment route: https://hawkinsoperations.com/proof/ho-det-001/
- Proof record: https://github.com/HawkinsOperations/hawkinsoperations-proof/blob/main/proof/records/HO-DET-001.md
- Proof Pack 001 release route: https://github.com/HawkinsOperations/hawkinsoperations-proof/releases/tag/hawkinsoperations-proof-pack-001
- Proof repository: https://github.com/HawkinsOperations/hawkinsoperations-proof

Recommended first-comment wording:

> Proof-boundary route for the HO-DET-001 receipt: https://hawkinsoperations.com/proof/ho-det-001/
>
> Boundary: controlled-test validation only. Website rendering is not proof; proof authority remains in the GitHub proof record and validation artifacts. No runtime-active, signal-observed, production, autonomous SOC, or public-safe runtime proof claim is made.

## 7. Verification

Run from the `hawkinsoperations-proof` repository root:

```powershell
python scripts/verify-linkedin-proof-boundary-artifact.py
python scripts/verify_proof_integrity.py
python scripts/verify-ho-det-001-proof-integrity.py
python scripts/verify-proof-pack-001-release.py
git diff --check
```

ZIP status: `ZIP_COMMIT_BLOCKED_BY_REPO_PATTERN`. This packet intentionally commits Markdown, JSON, checksums, and a verifier script only. It does not add a new committed distribution ZIP family.
