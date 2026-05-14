# HO-DET-001: AI Authority Boundary Case Study

Letting AI participate in a SOC workflow without granting it authority.

## 60-second summary

HO-DET-001 is a HawkinsOperations detection proof packet for suspicious PowerShell EncodedCommand execution. This case study covers a short AI authority-boundary sprint around that packet.

What was tested:

- A sanitized HO-DET-001 case packet was passed through local LLM triage support.
- The model was allowed to summarize, not decide.
- A deterministic verifier checked that AI could not approve, promote, close, decide disposition, or mark anything public-safe.
- Controlled-test validation remained the public proof ceiling.

What worked:

- The controlled-test validation result passed.
- Private/internal local model support was recorded in a controlled lab setting.
- Private/internal GPU activity was observed during a bounded model call.
- The authority-boundary verifier preserved AI support-only status.

What stayed blocked:

- Production claims.
- Runtime-active public proof.
- Signal-observed public proof.
- Public-safe runtime proof.
- AI-approved or analyst-approved disposition.

Current public claim ceiling: `CONTROLLED_TEST_VALIDATED`.

## The problem

A model can summarize a case, but the risk is treating model output as authority.

The useful question was not whether an LLM could produce a readable summary. The useful question was whether the surrounding workflow would refuse to let the model approve, promote, close, decide disposition, or mark the result public-safe.

## What was built

- A sanitized HO-DET-001 case packet for triage-support input.
- A local Qwen 2.5 14B model support pass.
- Private controlled lab GPU activity observation during the bounded model call.
- A deterministic authority-boundary verifier.
- A controlled-test validation result for controlled positive and negative fixtures.
- A proof-loop workflow for the checked controlled-test scope, including triage boundary, AI triage schema, claim-boundary, parity, case-packet, evidence-manifest, controlled-test validation, and closed-loop verifier checks.

The private lab GPU observation does not promote HO-DET-001 to runtime-active public proof, signal-observed public proof, evidence-linked public proof, or public-safe status.

## What the verifier enforced

```text
AI_DECIDED_DISPOSITION=false
HUMAN_REVIEW_REQUIRED=true
AI_MAY_APPROVE=false
AI_MAY_PROMOTE=false
AI_MAY_CLOSE=false
PUBLIC_SAFE_STATUS=NOT_PUBLIC_SAFE
PROOF_CEILING=CONTROLLED_TEST_VALIDATED
```

## Validation result

```text
TOTAL_CASES=14
MATCHED_POSITIVE_COUNT=7
MISSED_POSITIVE_CASES=none
FALSE_POSITIVE_NEGATIVE_CASES=none
```

The supported public claim remains:

> HO-DET-001 passed controlled-test validation against controlled positive and negative process-creation fixtures.

## What this proves

- Controlled-test validation passed for the checked fixture scope.
- The AI authority boundary was deterministically checked.
- Private/internal lab LLM triage support was recorded outside the public proof basis.
- Private/internal controlled lab GPU activity was observed during the bounded model call outside the public proof basis.
- AI remained support-only.

## What this does not prove

- Production.
- Fleet-wide deployment.
- Autonomous SOC.
- Runtime-active public proof.
- Signal-observed public proof.
- Public-safe runtime proof.
- Cribl-routed proof.
- Wazuh-routed proof.
- AI-approved disposition.
- Analyst-approved disposition.

## Public claim ceiling

Current ceiling: `CONTROLLED_TEST_VALIDATED`.

This artifact does not promote the proof record beyond that ceiling.

## Reviewer links

- [HO-DET-001 proof record](../../proof/records/HO-DET-001.md)
- [Controlled-test validation result](https://github.com/HawkinsOperations/hawkinsoperations-validation/blob/main/reports/ho-det-001/validation-result.json)
- [Controlled-test validation report](https://github.com/HawkinsOperations/hawkinsoperations-validation/blob/main/reports/ho-det-001/validation-result.md)
- [Proof-loop workflow](https://github.com/HawkinsOperations/hawkinsoperations-validation/blob/main/.github/workflows/ho-det-001-proof-loop.yml)
- [Closed AutoSOC Loop 001 verifier](https://github.com/HawkinsOperations/hawkinsoperations-validation/blob/main/scripts/verify-closed-autosoc-loop-001.py)

## LinkedIn note

This case study supports the LinkedIn post by giving reviewers a bounded proof route, not by promoting private runtime evidence into public proof.
