# HO-DET-012 Public-Safe Decision Gate

## Purpose

This decision packet prepares the final human public-safe decision for HO-DET-012 after the merged runtime corroboration review packet and merged runtime receipt verifier. It does not promote proof status, index status, website status, or public-safe status.

## Current Decision State

- Private runtime evidence state: PRIVATE_RUNTIME_EVIDENCE_CAPTURED.
- Public proof index ceiling: CONTROLLED_TEST_VALIDATED.
- Public proof index runtime status: NOT_PROVEN.
- Public proof index signal status: NOT_PROVEN.
- Public-safe status: NOT_PUBLIC_SAFE.
- Current decision gate status: HUMAN_DECISION_REQUIRED.
- Website update status: BLOCKED_PENDING_PUBLIC_SAFE_APPROVAL.
- Splunk status: NOT_VERIFIED.
- Raw private evidence public: false.
- AI decided disposition: false.
- Human review required: true.

HO-DET-012 must remain blocked from public-safe promotion until a human reviewer approves the exact public wording, evidence boundary, stale review, redaction boundary, and target surfaces.

## 1. What Is Already Proven Privately

The existing private evidence supports this private-only claim:

> HO-DET-012 has a private lab runtime receipt for one controlled Windows scheduled-task creation test, with local Windows telemetry, private Wazuh observation, cleanup confirmation, a private hash manifest, and a deterministic receipt verifier.

This is private runtime evidence. It does not prove public runtime proof or public signal-observed proof.

## 2. What Is Publicly Safe To Say Right Now

The following wording is safe right now only as a bounded review statement:

> HO-DET-012 produced a private lab runtime receipt from a controlled Windows scheduled-task creation test. The run produced local Windows telemetry and private Wazuh observation, with raw evidence retained outside public repos. Public-safe runtime publication remains under review.

Safe supporting statements:

- The validation repository contains a deterministic verifier, schema, and redacted sample for the private receipt shape.
- The proof repository contains a sanitized runtime corroboration review packet.
- Raw private evidence is retained outside public repositories.
- Splunk remains NOT_VERIFIED.
- Public-safe runtime publication remains under review.
- Human approval is required before any public-safe runtime or signal wording can advance.

## 3. What Remains Blocked

These remain blocked:

- Blocked: public runtime proof.
- Blocked: public signal-observed proof.
- Blocked: public-safe proof.
- Blocked: Splunk observation.
- Blocked: production readiness.
- Blocked: fleet-wide coverage.
- Blocked: autonomous SOC operation.
- Blocked: AI-approved disposition.
- Blocked: AI-decided disposition.
- Blocked: analyst-approved disposition.
- Blocked: exact scheduled-task marker publication.
- Blocked: exact correlation marker publication.
- Blocked: raw telemetry counts as public proof.
- Blocked: private evidence hashes as public proof anchors without separate review.

## 4. Exact Public Wording Allowed

Allowed now:

> HO-DET-012 produced a private lab runtime receipt from a controlled Windows scheduled-task creation test. The run produced local Windows telemetry and private Wazuh observation, with raw evidence retained outside public repos. Public-safe runtime publication remains under review.

Allowed after explicit approval to mark the packet as a public-safe candidate:

> HO-DET-012 has a public-safe candidate summary for a private lab runtime receipt from one controlled Windows scheduled-task creation test. The summary confirms that local Windows telemetry and private Wazuh observation were reviewed in sanitized form, while raw evidence remains private. Splunk remains NOT_VERIFIED, and the claim does not extend to production, fleet-wide, autonomous SOC, AI-approved, or analyst-approved status.

## 5. Exact Wording Forbidden

Do not use this wording:

- Forbidden wording: "HO-DET-012 public runtime proof is closed."
- Forbidden wording: "HO-DET-012 has public signal-observed proof."
- Forbidden wording: "HO-DET-012 was observed in Splunk."
- Forbidden wording: "HO-DET-012 is production-ready."
- Forbidden wording: "HO-DET-012 is fleet-wide."
- Forbidden wording: "HO-DET-012 provides autonomous SOC operation."
- Forbidden wording: "HO-DET-012 has AI-approved disposition."
- Forbidden wording: "HO-DET-012 has analyst-approved disposition."
- Forbidden wording: "HO-DET-012 proves full scheduled-task coverage."
- Forbidden wording: "Raw Wazuh evidence is public proof."
- Forbidden wording: "Private hashes are public proof anchors."

## 6. Files That Would Change After Public-Safe Candidate Approval

If a human reviewer later approves `PUBLIC_SAFE_CANDIDATE`, the expected follow-on repo changes would be limited to these proof files:

- `docs/runtime/HO-DET-012-PUBLIC-SAFE-DECISION-GATE.md`
- `docs/runtime/HO-DET-012-RUNTIME-CORROBORATION-REVIEW.md`
- `proof/records/HO-DET-012.md`
- `proof/indexes/DETECTION_PROOF_STATUS_INDEX.yml`

Possible proof changes after approval:

- mark the decision gate as approved for candidate wording;
- add the approved public-safe candidate wording to the proof record;
- update the proof index only if the validator vocabulary supports the approved status;
- preserve `Splunk NOT_VERIFIED`;
- preserve blocked claims for production, fleet-wide, autonomous SOC, AI-approved disposition, and analyst-approved disposition;
- keep raw private evidence out of the repo.

Website changes would be allowed only after proof approval is merged and would likely be limited to existing website data surfaces:

- `src/data/proofRecords.ts`
- `src/data/validationRegistry.ts`
- `src/data/proofPackManifest.ts`
- `src/data/platformContracts.ts`

Do not change website global public-safe configuration unless a separate explicit website/publication approval covers that broader status.

## 7. Files That Would Change If It Stays Blocked

If the decision remains blocked, no proof index, proof record, or website status change is required.

The only safe follow-on change would be maintaining this decision packet or the existing runtime corroboration review packet as private-evidence-boundary documentation. Current public proof state should remain:

- `proof_ceiling: CONTROLLED_TEST_VALIDATED`
- `runtime_status: NOT_PROVEN`
- `signal_status: NOT_PROVEN`
- `public_safe_status: NOT_PUBLIC_SAFE`
- `website_status: WEBSITE_UNTOUCHED_NOT_PROOF`

The private runtime receipt remains captured outside public repositories.

## 8. Website Decision

Website update should remain blocked now.

Website update becomes eligible only after:

- exact public-safe candidate wording is approved;
- proof record and proof index changes are reviewed and merged;
- website wording is checked against blocked claims;
- website validators pass;
- the update stays limited to bounded routing/status summary.

Even after approval, website wording must not claim public runtime proof, public signal-observed proof, Splunk observation, production readiness, fleet-wide proof, autonomous SOC, AI-approved disposition, or analyst-approved disposition.

## Final Decision Prompt

Human reviewer decision required:

- Decision required: approve `PUBLIC_SAFE_CANDIDATE` candidate wording for HO-DET-012; or
- Keep HO-DET-012 at private runtime evidence captured with public proof/index state `CONTROLLED_TEST_VALIDATED` / `NOT_PROVEN` / `NOT_PUBLIC_SAFE`.

Default without approval:

`CONTROLLED_TEST_VALIDATED / NOT_PROVEN / NOT_PUBLIC_SAFE`
