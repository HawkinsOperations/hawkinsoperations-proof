# Purple Team Closed Loop 001

A synthetic HO-DET-001 loop showing how AI can support triage without gaining authority.

## 60-second summary

This card explains a reviewer-facing, synthetic purple-team-style loop for HO-DET-001: controlled PowerShell EncodedCommand-style process creation, HO-DET-001 detection and Splunk source review, positive and negative synthetic validation, case-packet triage, support-only AI, and deterministic authority checks.

AI was allowed to provide support-only triage over a sanitized case packet. AI was blocked from approving, promoting, closing, deciding disposition, or marking anything public-safe. The current public claim ceiling remains `TEST_VALIDATED_SYNTHETIC_SCOPE`.

## Loop map

| Step | Status | Evidence basis | Public-safe wording | Blocked wording |
|---|---|---|---|---|
| 1. Controlled synthetic behavior | PROVEN | Synthetic fixture scope. | Controlled EncodedCommand-style behavior. | Production or live attack. |
| 2. Sysmon process-creation style telemetry target | PROVEN | Sysmon Event ID 1/process-creation scope. | Process-creation style telemetry target. | Live telemetry proof. |
| 3. HO-DET-001 detection source and Splunk source | PROVEN | Proof-record source references. | HO-DET-001 source and Splunk source exist. | Live Splunk fired. |
| 4. Synthetic validation with positive and negative fixtures | PROVEN | 14 fixtures: 7 positive, 7 negative. | Synthetic validation passed. | Runtime or signal proof. |
| 5. Case packet | PROVEN | Sanitized case-packet references. | Case packet existed for support-only triage. | Production AutoSOC triage. |
| 6. Local LLM support-only triage | PRIVATE_ONLY | AI-boundary case study and private classification. | Private support-only observations sit outside public proof. | AI-approved disposition or public model-runtime proof. |
| 7. Deterministic authority verifier | PROVEN | Verifier boundary results. | AI remained support-only. | AI could approve, promote, close, or decide. |
| 8. Public proof boundary | PROVEN | `TEST_VALIDATED_SYNTHETIC_SCOPE`. | Public proof remains synthetic-only. | Production, autonomous SOC, Cribl-routed, or Wazuh-routed proof. |

## What was proven

- HO-DET-001 source exists.
- HO-DET-001 Splunk source exists.
- HO-DET-001 passed synthetic validation against controlled fixtures.
- 14 synthetic fixtures were checked.
- 7 positive cases matched.
- 7 negative cases did not false-positive.
- A sanitized case packet existed for support-only triage.
- AI authority boundary was checked.
- AI did not approve, promote, close, decide disposition, or mark public-safe.
- Private/internal lab model support and GPU activity were recorded in private evidence, remain outside the public proof basis, and do not promote model-runtime, runtime, signal, or public-safe status.

## What was not proven

- Production.
- Fleet-wide deployment.
- Autonomous SOC.
- Runtime-active public proof.
- Signal-observed public proof.
- Public-safe runtime proof.
- Live Splunk fired as public proof.
- Cribl-routed proof.
- Wazuh-routed proof.
- Microsoft Defender-integrated proof.
- AWS-live proof.
- AWS CloudTrail live proof.
- Cloud runtime-active proof.
- AI-approved disposition.
- Analyst-approved disposition.

## Verifier boundary

```text
AI_DECIDED_DISPOSITION=false
HUMAN_REVIEW_REQUIRED=true
RECOMMENDED_DISPOSITION=null
AI_MAY_APPROVE=false
AI_MAY_PROMOTE=false
AI_MAY_CLOSE=false
PUBLIC_SAFE_STATUS=NOT_PUBLIC_SAFE
PROOF_CEILING=TEST_VALIDATED_SYNTHETIC_SCOPE
```

## Validation result

```text
TOTAL_CASES=14
MATCHED_POSITIVE_COUNT=7
MISSED_POSITIVE_CASES=none
FALSE_POSITIVE_NEGATIVE_CASES=none
```

## Why this is purple-team-style, not production

This closes a synthetic adversary-behavior-to-proof loop, not a live production detection loop. It is useful because the workflow preserves detection validation, AI support boundaries, and public claim discipline without treating private runtime evidence as public proof.

## Next expansion lanes

This proof card closes a synthetic HO-DET-001 loop only. The next expansion lanes are Microsoft Defender endpoint comparison, AWS cloud telemetry fixtures, Cribl routed-telemetry comparison, and Wazuh parallel signal comparison.

These are next-gate lanes, not current closed-loop proof. Do not say Microsoft Defender, AWS, Cribl, or Wazuh are integrated, routed, production, runtime-active, signal-observed, or public-safe for Purple Team Closed Loop 001 unless separate evidence proves it.

## Reviewer links

- [HO-DET-001 AI authority-boundary case study](HO-DET-001-AI-AUTHORITY-BOUNDARY.md)
- [HO-DET-001 proof record](../../proof/records/HO-DET-001.md)
- [Synthetic validation result](https://github.com/HawkinsOperations/hawkinsoperations-validation/blob/main/reports/ho-det-001/validation-result.json)
- [Synthetic validation report](https://github.com/HawkinsOperations/hawkinsoperations-validation/blob/main/reports/ho-det-001/validation-result.md)
- [Proof-loop workflow](https://github.com/HawkinsOperations/hawkinsoperations-validation/blob/main/.github/workflows/ho-det-001-proof-loop.yml)

## Current public claim ceiling

`TEST_VALIDATED_SYNTHETIC_SCOPE`

## Final boundary statement

The loop supports a synthetic public proof story. Private runtime and GPU evidence remain private, and public runtime, signal, production, routing, and public-safe proof remain blocked.
