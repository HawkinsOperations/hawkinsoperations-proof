# Governance Saves Evidence Matrix

## Public-Safe Candidate Evidence

| Candidate ID | Short Name | Stress-Test Classification | Why It Is Public-Safe To Discuss | Evidence Strength |
|---|---|---|---|---|
| GS-001 | Platform PR #34 unresolved-thread merge block | `COUNTABLE_SAVE` | Public PR metadata plus local log show passing checks did not override unresolved runtime-verifier review findings. | `HIGH_CONFIDENCE_PUBLIC` |
| GS-004 | HO-DET-001 proof ceiling boundary | `STANDING_CONTROL` | Public/source-controlled proof files state `CONTROLLED_TEST_VALIDATED`, `NOT_PUBLIC_SAFE`, blocked runtime/signal/public-safe claims, and rendering-is-not-proof boundaries. Includes useful GS-008 website boundary evidence. | `HIGH_CONFIDENCE_PUBLIC` |
| GS-005 | Proof Pack release gate | `STANDING_CONTROL` | Source-controlled release files and verifiers keep release status at candidate/no-tag/no-release before approval. | `HIGH_CONFIDENCE_PUBLIC` |
| GS-006 | AI disposition/status verifier | `STANDING_CONTROL` | Source-controlled index and verifier require human review and reject AI-decided disposition/public-safe promotion. | `HIGH_CONFIDENCE_PUBLIC` |
| GS-008 | Website rendering boundary | `SUPPORTING_EVIDENCE_ONLY` | Not independently countable. Website rendering boundary evidence has been folded into GS-004 and GS-009. | `HIGH_CONFIDENCE_PUBLIC` |
| GS-009 | Website blocked-claim scanner | `STANDING_CONTROL` | Site contract scanner tracks blocked wording such as runtime-active, signal-observed, and public-safe runtime proof; GS-008 website source evidence supports this boundary. | `HIGH_CONFIDENCE_PUBLIC` |
| GS-010 | HO-DET-012 runtime evidence gate | `STANDING_CONTROL` | Boundary document requires approved runtime capture, telemetry evidence, verification, and human approval before promotion. | `HIGH_CONFIDENCE_PUBLIC` |
| GS-012 | Human PR review authority | `SUPPORTING_EVIDENCE_ONLY` | Org-level and repo-level review docs require merge-readiness and `MERGE_APPROVED`; use as governance context unless enforcement is separately proven. | `HIGH_CONFIDENCE_PUBLIC` |
| GS-014 | April dirty-tree visibility stop | `INTERNAL_COUNTABLE_LOCAL_ONLY` | Public discussion is safe only as a generalized dirty-tree gate example; omit local file details and do not use as a public metric. | `HIGH_CONFIDENCE_LOCAL` |
| GS-015 | April website promotion dirty-tree stop | `INTERNAL_COUNTABLE_LOCAL_ONLY` | Public discussion is safe only as a process example with generated/unexpected file details redacted; no production-impact claim. | `HIGH_CONFIDENCE_LOCAL` |
| GS-021 | May website branch-hygiene stop | `INTERNAL_COUNTABLE_LOCAL_ONLY` | Public discussion is safe only as a generalized branch-hygiene example; omit branch lineage details and do not use as a public metric. | `HIGH_CONFIDENCE_LOCAL` |
| GS-022 | May multi-repo package dirty-state stop | `INTERNAL_COUNTABLE_LOCAL_ONLY` | Public discussion is safe as a generalized package-scope example; omit local path details and do not use as a public metric. | `HIGH_CONFIDENCE_LOCAL` |
| GS-029 | May staged-index scope stop | `INTERNAL_COUNTABLE_LOCAL_ONLY` | Public discussion is safe as a process-control story if proof and website hunk details are generalized. | `HIGH_CONFIDENCE_LOCAL` |
| GS-037 | Website PR #20 scope and mergeability gate | `NEEDS_PUBLIC_LINK` | Public discussion is safe as a generalized website PR scope/mergeability example after PR links are attached; do not use as a public metric. | `HIGH_CONFIDENCE_LOCAL` |
| GS-042 | HO-NDR proof route correction | `NEEDS_PUBLIC_LINK` | Public discussion is safe as a proof-route correction after public PR/diff links are attached; correction did not publish the local proof record. | `HIGH_CONFIDENCE_LOCAL` |
| GS-044 | Search Console verification claim boundary | `NEEDS_PUBLIC_LINK` | Public discussion is safe as a visibility-claim boundary after PR/live-route links are attached; it is not indexing, ranking, crawler-adoption, or proof evidence. | `HIGH_CONFIDENCE_LOCAL` |

## Confirmed Local / Log-Backed Candidates

| Candidate ID | Short Name | Local Evidence | Public Link Needed |
|---|---|---|---|
| GS-002 | Validation PR #41 unresolved-thread correction | Log shows merge blocked by unresolved review thread and follow-up correction enforcing dry-run, non-mutating, non-authorizing, support-only AI fields. | Yes; classification `NEEDS_PUBLIC_LINK`. |
| GS-003 | Validation PR #50 proof-status blocker | Log shows checks passed but merge state blocked by unresolved review thread, then scoped fix to enforce `NO_PROOF_RECORD`. | Yes; classification `NEEDS_PUBLIC_LINK`. |
| GS-007 | Website "approved ZIP" wording downgrade | Log shows public wording changed from "approved reviewer ZIP" to "bounded reviewer ZIP" to avoid authority overclaim. | Yes; classification `NEEDS_PUBLIC_LINK`. |
| GS-011 | AI/GPU support-only output gate | Log and case-study docs show support-only fields preserved and final disposition/public-proof claims blocked. | Yes, after redaction/generalization; classification `PRIVATE_ONLY`. |
| GS-013 | April PR review-thread merge gate | April log shows validation merge order delayed until unresolved, non-outdated review threads were resolved or outdated. | Yes; classification `NEEDS_PUBLIC_LINK`. |
| GS-014 | April dirty-tree visibility stop | April log shows unrelated dirty/untracked state stopped a clean visibility commit. | Redaction needed before public use; internally countable only. |
| GS-015 | April website dirty-tree promotion stop | April log shows website source edits, branch creation, commit, and PR stopped while untracked or unexpected local state existed. | Redaction needed before public use; internally countable only. |
| GS-016 | April proof-boundary packet | April log documents proof/public-safe/runtime/signal/evidence boundaries for a draft detection proof packet. | Use as standing/supporting evidence unless linked to a correction event. |
| GS-017 | April Sigma/Wazuh claim downgrade | April log shows public wording narrowed away from runtime signal, universal SIEM, fleet-wide, and current runtime implications. | Yes; classification `NEEDS_PUBLIC_LINK`. |
| GS-018 | April legacy workflow runtime gate | April log shows scheduled runtime workflow path disabled while validation/proof checks stayed preserved. | Yes; classification `NEEDS_PUBLIC_LINK`. |
| GS-020 | April enforcement-reality boundary | April log distinguishes soft ownership/branch-protection notes from confirmed blocking enforcement. | Public ruleset/check evidence needed before using as public proof. |
| GS-021 | May website branch-hygiene stop | May Week 1 log shows website implementation blocked before edits on unsafe branch state. | Redaction needed before public use; internally countable only. |
| GS-022 | May multi-repo package dirty-state stop | May Week 1 log shows package work blocked despite validations passing because unrelated dirty state remained. | Redaction needed before public use; internally countable only. |
| GS-023 | May detection status-sidecar correction | May Week 1 log shows stale local detection metadata preserved and corrected before sync. | Redaction needed before public use; internally countable only. |
| GS-025 | May validation PR #18 merge gate | May Week 1 log shows unsafe pre-sanitization state held back and clean PR merge gates applied. | Yes; classification `NEEDS_PUBLIC_LINK`. |
| GS-026 | May protected-branch rejection | May Week 1 log shows direct `.github` main push rejected by branch protection and no unsafe workaround used. | Yes; classification `NEEDS_PUBLIC_LINK`. |
| GS-027 | May validation PR #23 CI parity catch | May Week 1 log shows remote-clean checks failed on proof parity while PR stayed draft. | Yes; classification `NEEDS_PUBLIC_LINK`. |
| GS-028 | May proof PR #17 green-check gate | May Week 1 log shows green checks did not override branch divergence and changed-file-scope review. | Yes; classification `NEEDS_PUBLIC_LINK`. |
| GS-029 | May staged-index scope stop | May Week 1 log shows commit blocked when proof record and website hunks exceeded cleanup scope. | Redaction needed before public use; internally countable only. |
| GS-030 | May public route wording correction | May Week 1 log shows stale public wording and private proof routes corrected. | Yes; classification `NEEDS_PUBLIC_LINK`. |
| GS-031 | May GitHub org profile correction | May Week 1 log shows reviewer-first profile wording and rendering boundary preserved. | Yes; classification `NEEDS_PUBLIC_LINK`. |
| GS-032 | May homepage proof hierarchy correction | May Week 1 log shows homepage proof hierarchy kept fixture/private receipt status bounded. | Yes; classification `NEEDS_PUBLIC_LINK`. |
| GS-034 | Branch mismatch blocked governance-saves edits | Governed logbook shows PR #51 governance-saves edits stopped when the proof repo was on the HO-DET-011 runtime-readiness branch instead of the assigned PR #51 branch. | Yes; classification `NEEDS_PUBLIC_LINK`. |
| GS-035 | Validation direct-main push rejection | May Week 2 log shows a direct validation-main push rejected by repository rules requiring PR checks. | Yes; classification `NEEDS_PUBLIC_LINK`. |
| GS-036 | Platform required-check ruleset verification | May Week 2 log shows required-check behavior verified through a platform test PR. | Use as `STANDING_CONTROL`; public ruleset/check readback needed before external use. |
| GS-037 | Website PR #20 scope and mergeability gate | May Week 2 log shows website PR work blocked on branch-carried files, conflict state, and missing visible review before final approval readiness. | Yes; classification `NEEDS_PUBLIC_LINK`. |
| GS-038 | Validation PR #28 fail-closed workflow and proof parity blockers | May Week 2 log shows workflow drift and proof-record parity blockers held PR #28 before merge. | Yes; classification `NEEDS_PUBLIC_LINK`. |
| GS-039 | PR #15 private-path and reduction-boundary correction | May Week 2 log shows host-local/private-path and reduction-boundary wording corrected before merge. | Yes; classification `NEEDS_PUBLIC_LINK`; redaction required. |
| GS-040 | Proof PR #28 visible human-review gate | May Week 2 log shows proof PR #28 delayed until visible current-head human review existed despite chat approval. | Yes; classification `NEEDS_PUBLIC_LINK`. |
| GS-041 | `.github` PR #27 ruleset review-thread block | May Week 2 log shows GitHub ruleset blocked merge until a required review thread was resolved. | Yes; classification `NEEDS_PUBLIC_LINK`. |
| GS-042 | Proof PR #30 unpublished HO-NDR route correction | May Week 2 log shows public proof-route text corrected so it no longer implied an unpublished proof record existed. | Yes; classification `NEEDS_PUBLIC_LINK`. |
| GS-043 | HO-DET-011 status metadata and dependency gate | May Week 2 log shows private runtime evidence, public status, routed telemetry, and PR dependency ordering kept separate. | Yes; classification `NEEDS_PUBLIC_LINK`; private runtime wording must stay bounded. |
| GS-044 | Website Search Console verification claim boundary | May Week 2 log shows verification work stayed below indexing, ranking, crawler-adoption, or proof claims. | Yes; classification `NEEDS_PUBLIC_LINK`. |
| GS-045 | Public-safe abstract packet held private | May Week 2 log shows a private abstract packet held as review-only because it contained local paths/private planning context. | No; classification `PRIVATE_ONLY`. |
| GS-046 | Security Onion visibility contract sanitized evidence boundary | May Week 2 log shows a sanitized validation contract created without importing private packet files or raw evidence. | Yes; classification `NEEDS_PUBLIC_LINK`. |

## Candidates Needing Public Links

| Candidate ID | Needed Link | Why |
|---|---|---|
| GS-002 | Validation PR #41 URL, review-thread URL, final fix commit | Needed before public website use or counting as public-backed save. |
| GS-003 | Validation PR #50 URL, review-thread URL, final fix/merge outcome | Needed before public website use or counting as public-backed save. |
| GS-007 | Website PR/commit URL for wording downgrade | Needed to make the correction externally inspectable. |
| GS-013 | Detections/validation PR URLs and review-thread URLs | Needed before public website use or public-backed counting. |
| GS-017 | Public diff or PR URL for Sigma/Wazuh wording downgrade | Needed to make the public-claim correction externally inspectable. |
| GS-018 | Public workflow PR or commit URL for runtime workflow retirement | Needed before public-backed counting or website use. |
| GS-011 | Public-safe case-study route or redacted summary | Raw/local runtime details are not public-safe by default. |
| GS-012 | Branch-protection/ruleset readback | Needed before saying the human-review authority is technically blocking across repos. |
| GS-020 | Branch-protection/ruleset/check readback | Needed before claiming active blocking enforcement across repos. |
| GS-025 | Validation PR #18 URL, check evidence, final clean-branch outcome | Needed before public-backed counting. |
| GS-026 | Public ruleset/readback or PR evidence for the branch-protection rejection | Needed before external enforcement story use. |
| GS-027 | Validation PR #23 URL, failed workflow links, rerun links, proof parity PR link | Needed before public-backed counting. |
| GS-028 | Proof PR #17 URL, compare/check evidence, final outcome | Needed before public-backed counting. |
| GS-030 | Public PR/commit URL for front-door wording and route correction | Needed before website use or public-backed counting. |
| GS-031 | Public profile commit/PR URL | Needed before website use or public-backed counting. |
| GS-032 | Website PR #11 URL and final wording evidence | Needed before website use or public-backed counting. |
| GS-034 | Public-safe PR/log reference or summarized branch-preflight closeout | Needed before public-backed counting or website use. |
| GS-035 | Validation PR #25 URL, rejection/ruleset evidence, and required-check evidence | Needed before public-backed counting. |
| GS-037 | Website PR #20 URL, conflict/scope evidence, visible-review evidence, and final outcome | Needed before website use or public-backed counting. |
| GS-038 | Validation PR #28 URL, failed/passing workflow links, and proof parity PR evidence | Needed before public-backed counting. |
| GS-039 | Detections PR #15 URL, review-thread evidence, and corrected reduction wording | Needed before external use. |
| GS-040 | Proof PR #28 URL, visible current-head review evidence, and final outcome | Needed before external use. |
| GS-041 | `.github` PR #27 URL, ruleset evidence, and thread-resolution evidence | Needed before public-backed counting. |
| GS-042 | Proof PR #30 URL, final diff, and merge evidence | Needed before public-backed counting. |
| GS-043 | Detections PR #17 URL, validation PR #30 URL, check-log evidence, and final dependency outcome | Needed before external use. |
| GS-044 | Website PR #21 URL and live verification file evidence | Needed before website use; indexing/ranking claims remain blocked. |
| GS-046 | Validation PR/check evidence for the sanitized Security Onion contract | Needed before external use. |

## Entries Not Countable Yet

| Candidate ID | Classification | Reason Not Countable Yet |
|---|---|---|
| GS-002 | `NEEDS_PUBLIC_LINK` | Local evidence is strong, but public PR/review/fix evidence is not attached. |
| GS-003 | `NEEDS_PUBLIC_LINK` | Local evidence is strong, but public PR/review/final outcome evidence is not attached. |
| GS-004 | `STANDING_CONTROL` | Boundary evidence, not a specific blocked/corrected event. |
| GS-005 | `STANDING_CONTROL` | Release gate exists, but a specific blocked release/tag/ZIP event is not attached. |
| GS-006 | `STANDING_CONTROL` | Verifier guardrail exists, but a specific failed/corrected AI-overreach event is not attached. |
| GS-007 | `NEEDS_PUBLIC_LINK` | Wording downgrade is local/log-backed; public PR/commit evidence is needed. |
| GS-008 | `SUPPORTING_EVIDENCE_ONLY` | Demoted before commit. It overlaps GS-004 and GS-009 and is not independently countable. |
| GS-009 | `STANDING_CONTROL` | Scanner exists, but a specific scanner catch is not attached. |
| GS-010 | `STANDING_CONTROL` | Runtime gate exists, but a specific blocked promotion attempt is not attached. |
| GS-011 | `PRIVATE_ONLY` | Local runtime/GPU context must not be public-counted. |
| GS-012 | `SUPPORTING_EVIDENCE_ONLY` | Authority context for other saves, not independently countable without enforcement readback or a specific PR event. |
| GS-013 | `NEEDS_PUBLIC_LINK` | Local April log evidence is specific, but public PR/review-thread links are not attached. |
| GS-016 | `STANDING_CONTROL` | Proof boundary is documented, but no specific public correction or blocked merge/release event is attached. |
| GS-017 | `NEEDS_PUBLIC_LINK` | Public wording downgrade is local/log-backed; public diff or PR evidence is needed. |
| GS-018 | `NEEDS_PUBLIC_LINK` | Runtime workflow hardening is local/log-backed; public workflow evidence is needed. |
| GS-019 | `PRIVATE_ONLY` | Local runtime/evidence details must not be public-counted. |
| GS-020 | `STANDING_CONTROL` | Enforcement-reality boundary is supporting hardening evidence, not a specific save by itself. |
| GS-024 | `PRIVATE_ONLY` | Private evidence sanitizer/history and hash-only evidence index details must not be public-counted. |
| GS-025 | `NEEDS_PUBLIC_LINK` | Local PR #18 evidence is strong, but public PR/check/final outcome links are not attached. |
| GS-026 | `NEEDS_PUBLIC_LINK` | Concrete branch-protection rejection is local/log-backed; public ruleset/PR evidence is needed. |
| GS-027 | `NEEDS_PUBLIC_LINK` | CI parity catch is local/log-backed; public PR/workflow links are needed. |
| GS-028 | `NEEDS_PUBLIC_LINK` | Proof PR branch-divergence event is local/log-backed; public PR/check links are needed. |
| GS-030 | `NEEDS_PUBLIC_LINK` | Public-route wording correction is local/log-backed; public PR/commit evidence is needed. |
| GS-031 | `NEEDS_PUBLIC_LINK` | Public profile correction is local/log-backed; public commit/PR evidence is needed. |
| GS-032 | `NEEDS_PUBLIC_LINK` | Homepage proof hierarchy correction is local/log-backed; public PR/final wording evidence is needed. |
| GS-033 | `PRIVATE_ONLY` | Private HO-SECONION/Zeek boundary evidence must not be public-counted. |
| GS-034 | `NEEDS_PUBLIC_LINK` | Local branch-preflight evidence is specific, but public-safe evidence or public PR/log reference is needed before public-backed counting. |
| GS-035 | `NEEDS_PUBLIC_LINK` | Local May Week 2 evidence is specific, but public ruleset/check/PR evidence is not attached. |
| GS-036 | `STANDING_CONTROL` | Required-check ruleset behavior is control architecture, not a standalone save count. |
| GS-037 | `NEEDS_PUBLIC_LINK` | Local website PR gate evidence is strong, but public PR/review/final outcome links are not attached. |
| GS-038 | `NEEDS_PUBLIC_LINK` | Local CI/parity blocker evidence is strong, but public workflow/check/PR links are not attached. |
| GS-039 | `NEEDS_PUBLIC_LINK` | Local reduction-boundary/private-path correction evidence is strong, but public PR/thread evidence and redaction are needed. |
| GS-040 | `NEEDS_PUBLIC_LINK` | Local visible-review gate evidence is strong, but public PR/review evidence is not attached. |
| GS-041 | `NEEDS_PUBLIC_LINK` | Local ruleset/review-thread evidence is strong, but public PR/ruleset/thread evidence is not attached. |
| GS-042 | `NEEDS_PUBLIC_LINK` | Local proof-route correction evidence is strong, but public PR/diff/merge evidence is not attached. |
| GS-043 | `NEEDS_PUBLIC_LINK` | Local status/dependency evidence is strong, but public PR/check/final dependency evidence is not attached. |
| GS-044 | `NEEDS_PUBLIC_LINK` | Local website visibility claim-boundary evidence is strong, but public PR/live-route evidence is not attached. |
| GS-045 | `PRIVATE_ONLY` | Private abstract packet details must not be public-counted or treated as publish-ready. |
| GS-046 | `NEEDS_PUBLIC_LINK` | Local sanitized-contract evidence is strong, but public PR/check evidence is not attached. |

## Countability Summary

| Classification | Entries | Commit Decision |
|---|---|---|
| `COUNTABLE_SAVE` | GS-001 | Public-backed review bucket only. This is not a public metric until separately approved for a specific public surface. |
| `INTERNAL_COUNTABLE_LOCAL_ONLY` | GS-014, GS-015, GS-021, GS-022, GS-023, GS-029 | Local-log-backed review bucket only. These require review/redaction before external use and must not be represented as public metrics. |
| `NEEDS_PUBLIC_LINK` | GS-002, GS-003, GS-007, GS-013, GS-017, GS-018, GS-025, GS-026, GS-027, GS-028, GS-030, GS-031, GS-032, GS-034, GS-035, GS-037, GS-038, GS-039, GS-040, GS-041, GS-042, GS-043, GS-044, GS-046 | Keep marked; do not block this cleanup on adding links. |
| `STANDING_CONTROL` | GS-004, GS-005, GS-006, GS-009, GS-010, GS-016, GS-020, GS-036 | Do not represent as public save counts. |
| `SUPPORTING_EVIDENCE_ONLY` | GS-008, GS-012 | Use only to support other entries. |
| `PRIVATE_ONLY` | GS-011, GS-019, GS-024, GS-033, GS-045 | Keep local/private unless redacted and approved later. |

## Current Counting Boundary

- Public website metrics are not authorized from this matrix.
- `COUNTABLE_SAVE` requires a concrete blocked, corrected, downgraded, delayed, or rejected event.
- `INTERNAL_COUNTABLE_LOCAL_ONLY` means a concrete local/log-backed event exists, but it is not public-backed and is not a public save count.
- Standing controls may be summarized as controls, but they are not save counts.
- Supporting and duplicate evidence rows are not independently countable.
- Local/log-backed saves require public-safe review and redaction before external use.
- `NEEDS_PUBLIC_LINK` entries are not public-backed until the relevant PR, review, check, commit, or public source link is attached.
- `PRIVATE_ONLY` entries stay private unless a separately approved sanitized summary exists.

## Private-Only Candidates

| Candidate ID | Reason |
|---|---|
| GS-011 | Contains local runtime/GPU support context in the log evidence. Public use must generalize to support-only AI boundaries and omit private runtime specifics. |
| GS-019 | Contains private Cribl/Splunk/Wazuh runtime-evidence review context. Public use is blocked unless a separate sanitized summary is approved. |
| GS-024 | Contains private evidence sanitizer/history and hash-only evidence index details. Public use is blocked unless a separate sanitized pattern summary is approved. |
| GS-033 | Contains private HO-SECONION/Zeek proof-boundary evidence. Public use is blocked unless a separate sanitized summary is approved. |
| GS-045 | Contains private/public-safe abstraction work with local path and planning context. Public use is blocked unless a sanitized summary is separately approved. |

## Rejected Candidates

| Rejected ID | Reason |
|---|---|
| RJ-001 | Production impact is not proven. |
| RJ-002 | Standing governance statements are not automatically countable saves. |
| RJ-003 | Website rendering is not proof. |
| RJ-004 | Platform PR #34 final resolution is not yet verified in this pass. |
| RJ-005 | April branch protection and CODEOWNERS notes do not prove active blocking enforcement across every repo. |
| RJ-006 | May Week 1 operations-only inventory, folder, and VM controls are supporting/private operations evidence, not public governance-save counts. |
| RJ-007 | May Week 1 live rendering checks and route views are presentation evidence only; they do not prove proof status. |
| RJ-008 | May Week 2 operations-only Inventory, Work artifact routing, cleanup, and runtime-private findings are supporting/private evidence for this backlog unless tied to a repo/public/proof governance-save row. |

## Best 5 Website-Safe Examples

| Rank | Candidate ID | Website-Safe Summary |
|---|---|---|
| 1 | GS-001 | Passing checks did not override unresolved review findings on a runtime-truth verifier. |
| 2 | GS-042 | Public proof-route text was corrected so it no longer implied an unpublished HO-NDR proof record existed. |
| 3 | GS-044 | Search Console verification stayed below indexing, ranking, crawler-adoption, or proof claims. |
| 4 | GS-032 | Homepage proof hierarchy kept fixture and private/internal receipt status from becoming public proof. |
| 5 | GS-037 | Website PR scope and mergeability gates blocked hidden branch-carried files before merge readiness. |

## Best 5 Interview / Story Examples

| Rank | Candidate ID | Interview Angle |
|---|---|---|
| 1 | GS-001 | "I refused to merge a verifier even though checks passed because review found fail-open contract drift." |
| 2 | GS-040 | "Even after chat approval, I held a proof PR until visible current-head human review existed." |
| 3 | GS-038 | "A workflow failed closed on report drift and proof parity blockers before public-report routing could merge." |
| 4 | GS-039 | "A pipeline artifact was corrected before merge so private paths and reduction math did not overclaim." |
| 5 | GS-041 | "A GitHub ruleset blocked an org-facing PR until a review thread was resolved." |

## Wording To Tighten Before Commit

| Location | Current Risk | Required Tightening |
|---|---|---|
| `GOVERNANCE-SAVES-CANDIDATES.md` GS-005 | Could be read as a historical blocked release event. | Keep as `STANDING_CONTROL` unless a specific blocked release/tag/ZIP event is linked. |
| `GOVERNANCE-SAVES-CANDIDATES.md` GS-008 | Duplicates website boundary evidence already covered by GS-004 and GS-009. | Resolved: GS-008 is demoted to `SUPPORTING_EVIDENCE_ONLY` and is not independently countable. |
| `GOVERNANCE-SAVES-CANDIDATES.md` GS-011 | Local runtime/GPU details are not public-safe by default. | Keep `PRIVATE_ONLY`; use only a redacted support-only AI summary outside local review. |
| `GOVERNANCE-SAVES-CANDIDATES.md` GS-014 and GS-015 | Local dirty-tree details could expose paths or read like final public metrics. | Use generalized dirty-tree wording externally and keep counts blocked until reviewed. |
| `GOVERNANCE-SAVES-CANDIDATES.md` GS-017 and GS-018 | Public stories could imply runtime-active or production-prevention impact. | Keep wording to claim downgrade and workflow hardening; do not claim production prevention or runtime-active status. |
| `GOVERNANCE-SAVES-CANDIDATES.md` GS-019 | Private runtime evidence could be exposed as public-safe. | Keep `PRIVATE_ONLY`; do not summarize externally without separate sanitized approval. |
| `GOVERNANCE-SAVES-CANDIDATES.md` GS-021 through GS-023 and GS-029 | Local dirty/branch/staged-index details could expose paths or read like final metrics. | Use generalized branch/dirty/scope wording externally; keep count language `INTERNAL_COUNTABLE_LOCAL_ONLY` only. |
| `GOVERNANCE-SAVES-CANDIDATES.md` GS-034 | Branch-preflight evidence could expose local branch/session details or read like public proof. | Keep `NEEDS_PUBLIC_LINK`; summarize only as a wrong-branch preflight stop until public-safe evidence is attached. |
| `GOVERNANCE-SAVES-CANDIDATES.md` GS-024 and GS-033 | Private evidence/runtime boundary details could be exposed as public-safe. | Keep `PRIVATE_ONLY`; do not summarize externally without separately approved sanitized wording. |
| `GOVERNANCE-SAVES-CANDIDATES.md` GS-027 and GS-032 | Public examples could imply signal-observed or runtime-active status. | Keep wording to parity/blocking and proof-hierarchy correction only. |
| `GOVERNANCE-SAVES-CANDIDATES.md` GS-035 through GS-046 | May Week 2 rows could look like a new public count. | Keep all new rows local/log-backed, non-metric, and link-gated or private as classified. |
| `GOVERNANCE-SAVES-CANDIDATES.md` website readiness notes | Could imply final public examples. | Keep "candidate/example" wording and no totals until public-safe review. |
| Any future summary | Production, runtime-active, public-safe runtime, autonomous SOC, AI-approved, analyst-approved, and final public metric wording remain blocked. | Use lower claim wording and route through review before publication. |

## Best 5 Repo / Proof Hardening Follow-Ups

| Rank | Candidate ID | Follow-Up |
|---|---|---|
| 1 | GS-001 | After PR #34 is fixed, record final commit, resolved thread URLs, and whether the verifier gained fail-closed tests. |
| 2 | GS-038 | Attach PR #28 workflow failure/pass links and proof parity PR evidence. |
| 3 | GS-042 | Attach PR #30 URL, final diff, and merge evidence. |
| 4 | GS-043 | Attach PR #17 / PR #30 dependency evidence and final outcome. |
| 5 | GS-020 / GS-026 / GS-035 / GS-041 | Capture current branch-protection/ruleset readback to separate soft governance from blocking enforcement. |

## April 2026 Expansion Summary

Pass 2A used `C:\Raylee\Operations\Logbook\2026\04-2026\04-24_to_04-30.md` as the full April weekly source. It added GS-013 through GS-020. GS-014 and GS-015 are `INTERNAL_COUNTABLE_LOCAL_ONLY` dirty-tree saves, GS-013/GS-017/GS-018 need public links, GS-016/GS-020 are standing or supporting controls, and GS-019 is private-only.

No April entry is a final public metric, production-prevention claim, runtime-active claim, signal-observed claim, public-safe runtime claim, autonomous SOC claim, AI-approved disposition, or analyst-approved disposition.

## May 1-7 2026 Expansion Summary

Pass 2B used `C:\Raylee\Operations\Logbook\2026\05-2026\05-01_to_05-07.md` as the May Week 1 source. Eight read-only scanner roles returned findings. The consolidated backlog added GS-021 through GS-033.

Strongest May Week 1 rows:

- GS-022: multi-repo package blocked while unrelated dirty state remained.
- GS-027: remote-clean CI/proof parity failure kept validation PR #23 from being treated as ready.
- GS-028: proof PR #17 was restacked because green checks did not override branch divergence and changed-file-scope drift.
- GS-029: staged-index gate stopped a governance cleanup commit with proof and website hunks outside scope.
- GS-032: homepage proof hierarchy kept fixture and private/internal receipt status bounded.

Not countable or not public-backed yet:

- GS-025, GS-026, GS-027, GS-028, GS-030, GS-031, and GS-032 need public links.
- GS-034 needs a public-safe evidence reference or summarized branch-preflight closeout reference.
- GS-024 and GS-033 remain private-only.
- May operations-only inventory, folder, GitHub board, and VM control findings were held as supporting/rejected for this backlog rather than promoted to public governance-save counts.

No May Week 1 entry is a final public metric, production-prevention claim, runtime-active claim, signal-observed claim, public-safe runtime claim, autonomous SOC claim, AI-approved disposition, or analyst-approved disposition.

## May 8-14 2026 Expansion Summary

Pass 2C used `C:\Raylee\Operations\Logbook\2026\05-2026\05-08_to_05-14.md` as the May Week 2 source. Eight read-only scanner roles returned findings. The consolidated backlog added GS-035 through GS-046.

Strongest May Week 2 rows:

- GS-035: direct-main validation push rejected by repository rules requiring PR checks.
- GS-037: website PR #20 blocked on scope, conflict, and visible-review gates.
- GS-038: validation PR #28 failed closed on workflow drift and proof-record parity blockers.
- GS-039: detections PR #15 corrected private-path and reduction-boundary wording before merge.
- GS-040: proof PR #28 stayed blocked until visible current-head human review existed.
- GS-041: `.github` PR #27 was blocked by a ruleset-required review thread.
- GS-042: proof PR #30 corrected a public route that implied an unpublished HO-NDR proof record existed.
- GS-043: HO-DET-011 status and validation dependency gates kept private runtime evidence and PR sequencing bounded.
- GS-044: Search Console verification stayed below indexing, ranking, crawler-adoption, or proof claims.

Not countable or not public-backed yet:

- GS-035, GS-037, GS-038, GS-039, GS-040, GS-041, GS-042, GS-043, GS-044, and GS-046 need public links.
- GS-036 is a standing control.
- GS-045 is private-only.
- Operations-only Inventory, Work artifact routing, cleanup, and runtime-private scanner findings were held as supporting/private evidence rather than promoted to public governance-save counts.

No May Week 2 entry is a final public metric, production-prevention claim, runtime-active claim, signal-observed claim, public-safe runtime claim, autonomous SOC claim, AI-approved disposition, or analyst-approved disposition.

## Matrix Warning

This matrix is for internal prioritization. Do not publish candidate counts, save totals, or percentage claims from this file until each entry is confirmed, deduplicated, public-safe, and approved for the exact external surface.
