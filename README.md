# HawkinsOperations Proof
## Evidence and Claim Ceiling Plane

This repository stores reviewed evidence records and defines what HawkinsOperations can safely claim.

Proof is the claim boundary: evidence can support a claim only within its recorded scope, public-safe status, and review state.

## Current Public Claim Ceiling

| Boundary | Current state |
|---|---|
| Flagship proof path | HO-DET-001 |
| Public proof ceiling | TEST_VALIDATED_SYNTHETIC_SCOPE |
| Public-safe status | NOT_PUBLIC_SAFE |
| Private/internal runtime status | CONTROLLED_LAB_RUNTIME_MATCH_VERIFIED |
| Runtime-active public proof | BLOCKED |
| Public signal-observed proof | BLOCKED |
| Public-safe runtime proof | BLOCKED |

Private/internal runtime match evidence is not public-safe proof. Public claims require reviewed wording, evidence linkage, privacy review, stale review, and Raylee approval.

## What This Repository Proves

| Proof surface | What it can support |
|---|---|
| Proof records | Claim ceilings and evidence links |
| Evidence bundles | Reviewed support for bounded claims |
| Validation summaries | What was tested and under what scope |
| Case studies | Public-safe explanation of bounded evidence |
| Claim mapping | Which claims are supported, blocked, or not yet reviewed |

## What This Repository Does Not Prove

| Not proven by this repo alone | Why |
|---|---|
| Source correctness | Source truth belongs in detections |
| Test behavior | Validation truth belongs in validation |
| Live runtime state | Runtime evidence needs separate review |
| Public signal proof | Signal-observed public proof is blocked until approved |
| Website truth | Website is rendering only |
| Production readiness | Requires separate scoped evidence and approval |

## HO-DET-001 Current Boundary

| Item | Current state |
|---|---|
| Proof record | [proof/records/HO-DET-001.md](proof/records/HO-DET-001.md) |
| Public ceiling | TEST_VALIDATED_SYNTHETIC_SCOPE |
| Public-safe status | NOT_PUBLIC_SAFE |
| Private/internal runtime status | CONTROLLED_LAB_RUNTIME_MATCH_VERIFIED |
| Platform contract guardrail | Non-promotional guardrail |
| Runtime-active public proof | BLOCKED |
| Public signal-observed proof | BLOCKED |
| Public-safe runtime proof | BLOCKED |

## Proof Record Routes

- [AWS-DET-001](proof/records/AWS-DET-001.md)
- [HO-DET-001](proof/records/HO-DET-001.md)

## Case Studies

- [HO-DET-001: AI Authority Boundary Case Study](docs/case-studies/HO-DET-001-AI-AUTHORITY-BOUNDARY.md)
- [Purple Team Closed Loop 001](docs/case-studies/PURPLE-TEAM-CLOSED-LOOP-001.md)

## Evidence Contract

- Every evidence artifact must map to a source, run, commit, or reviewed record.
- Evidence must state its scope.
- Evidence must preserve public/private boundaries.
- Public-facing claims must map to proof records.
- Raw private evidence is not automatically public-safe evidence.
- A proof record does not promote claims beyond its stated ceiling.

## Promotion Rule

A claim can move toward public use only when:

- evidence linkage exists
- the claim ceiling supports it
- private leakage risk is reviewed
- stale review is complete
- wording is reviewed
- Raylee approves promotion

## Current Claim Boundary

| Supported within current public ceiling | Explicitly not claimed |
|---|---|
| HO-DET-001 has merged source artifacts | runtime-active public proof |
| HO-DET-001 has merged synthetic validation artifacts | public signal-observed proof |
| HO-DET-001 passed controlled synthetic validation | evidence-linked public proof |
| Platform contract guardrail exists as a non-promotional guardrail | public-safe runtime proof |
| Private/internal runtime match status is scoped private/internal | production-ready claim, fleet-wide claim, enterprise deployed claim |
| AI can support work, but cannot approve claims | live Splunk fired as public proof, Cribl-routed claim, Wazuh-routed claim, AWS-live claim |
| Human review is required before public promotion | autonomous SOC claim, AI-approved disposition, AI-decided disposition, analyst-approved disposition, production AutoSOC claim |

## Real Controls Rule

Docs, READMEs, proof records, diagrams, and websites are not real controls by themselves.

A control becomes real only when it blocks, fails, or forces correction through required review, branch protection, rulesets, blocking CI, deterministic verifiers, typed claim gates, or another enforceable mechanism.

Green CI/status checks are not merge authority.
Codex review is AI labor, not human governance.

## Related Repositories

| Repo | Boundary |
|---|---|
| `hawkinsoperations-detections` | Source truth |
| `hawkinsoperations-validation` | Behavior truth |
| `hawkinsoperations-platform` | Runtime contracts / integration guardrails |
| `hawkinsoperations-website` | Public rendering only |
| `.github` | Org governance / reviewer routing |

## Doctrine

AI is labor. Governance is authority.

Build loud. Verify hard. Claim tight. Ship receipts.
