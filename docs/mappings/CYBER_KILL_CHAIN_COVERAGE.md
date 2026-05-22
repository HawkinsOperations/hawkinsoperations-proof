# HawkinsOperations Cyber Kill Chain Coverage

## Purpose

This maps HawkinsOperations artifacts to the Cyber Kill Chain for reviewer understanding.

- This is a coverage and reviewer map.
- This is not runtime proof.
- This does not promote signal-observed, production, public-safe runtime, or autonomous claims.
- Proof authority remains in validation records, proof records, verifier outputs, and human review.

## Coverage Summary

| Cyber Kill Chain Stage | HawkinsOperations Coverage | Current State | Strongest Artifact | Blocked Claims |
|---|---|---|---|---|
| Reconnaissance | Identity context, visibility boundary, pipeline route planning, and gap tracking. | Controlled identity validation plus boundary/source contracts. | ID-DET-001..004 validation reports; HO-NDR-001 boundary card; HO-PIPE-001 source contract. | live IdP, live SIEM/NDR, complete identity coverage, public-safe runtime proof. |
| Weaponization | Defensive modeling of attacker behaviors into source, fixtures, validators, scanners, and proof routes. | Source and validation truth separated from proof truth. | Detection source packages, validation registry, claim-boundary scanners, proof records where present. | AI-approved detection, analyst-approved disposition, production-ready, runtime-active, signal-observed. |
| Delivery | Cloud/access-attempt-adjacent visibility through controlled CloudTrail-style denial fixtures. | FIXTURE_ONLY / CONTROLLED_TEST_VALIDATED. | AWS-DET-001 proof record and proof card. | live AWS, live CloudTrail, AWS account coverage, cloud runtime-active proof. |
| Exploitation | Suspicious execution and post-exploitation process behavior. | CONTROLLED_TEST_VALIDATED. | HO-DET-001 proof record, proof card, Proof Pack 001, validation report. | live Splunk, runtime-active, signal-observed, Cribl-routed proof, Wazuh-routed proof, production-ready. |
| Installation | Persistence, service creation, scheduled task creation, and foothold maintenance behavior. | Mixed: PRIVATE_RUNTIME_EVIDENCE_CAPTURED for HO-DET-011; CONTROLLED_TEST_VALIDATED governed proof record for HO-DET-012. | HO-DET-011 proof record; HO-DET-012 proof record, proof card, validation report, and proof index boundary. | public-safe proof, signal-observed, production deployment, complete service-creation coverage, scheduled-task coverage completeness. |
| Command & Control | NDR visibility, cross-source corroboration shape, and pipeline route integrity support. | BOUNDARY_CONTRACT_ONLY / SOURCE_EXISTS / VALIDATION_CONTRACT_ENFORCED. | HO-NDR-001 boundary contract and card; HO-PIPE-001 source contract and validation contract result. | Security Onion observed proof, Cribl-routed proof, Wazuh-routed proof, live Splunk, signal-observed. |
| Actions on Objectives | Analyst workflow, case structure, triage support, metrics, and bounded automation support. | AI_SUPPORT_ONLY / HUMAN_REVIEW_REQUIRED. | SOAR Case Packet v0, AutoSOC case packet, Detection Factory Controller v0, Local GPU Triage Gate, Offline LLM Triage Support Contract. | autonomous SOC, autonomous resolution, AI-approved disposition, analyst-approved disposition, response automation, containment execution, closure execution, suppression execution, SOCaaS availability. |

## Stage-by-Stage Mapping

### Reconnaissance

- Meaning: Where visibility, identity context, exposed surfaces, and coverage gaps are understood before or around attacker activity.
- HawkinsOperations artifacts: ID-DET-001 suspicious identity session context; ID-DET-002 suspicious MFA fatigue or repeated MFA failure; ID-DET-003 privileged role assignment or admin group change; ID-DET-004 impossible travel or anomalous session context; HO-NDR-001 Security Onion visibility boundary; HO-PIPE-001 pipeline route integrity source contract.
- ATT&CK / behavior family: identity session context; MFA fatigue / repeated MFA failure; privileged role / admin group change; impossible travel / anomalous session; NDR visibility and pipeline route support.
- Current proof state: ID-DET-001..004 are NO_PROOF_RECORD in the proof index; HO-NDR-001 is BOUNDARY_CONTRACT_ONLY; HO-PIPE-001 is SOURCE_EXISTS with validation contract enforcement.
- Validation state: ID-DET-001..004 are CONTROLLED_TEST_VALIDATED in validation reports with 10 controlled identity fixtures each, 5 positive, 5 negative, 0 missed positives, and 0 false-positive negatives. HO-NDR-001 has validation contract enforcement for contract shape. HO-PIPE-001 has validation contract enforcement for route-integrity shape and field-preservation requirements.
- What exists: Source packages for ID-DET-001..004 and HO-PIPE-001, validation reports for ID-DET-001..004, the HO-NDR-001 boundary contract and proof card, the Telemetry Coverage Contract v0, the HO-PIPE-001 validation result, and proof-index no-proof-record boundaries for the identity family.
- What it proves: Controlled identity-event fixture validation exists for the identity family; NDR and pipeline visibility boundaries are documented without claiming observed telemetry.
- What it does not prove: live IdP proof, live SIEM/NDR proof, production identity coverage, complete identity coverage, impossible-travel completeness, session hijacking completeness, runtime-active status, signal-observed status, or public-safe runtime proof.
- Automation support: reviewer route selection, validation registry display, proof status indexing, claim-boundary scanners, and visibility/route contract checks.
- AI-support boundary: AI may summarize sanitized identity context and identify missing review fields. AI cannot promote proof, decide disposition, approve cases, or claim coverage completeness.
- Blocked claims: live IdP, live Splunk, Wazuh-routed proof, Cribl-routed proof, Security Onion observed proof, production identity coverage, complete identity coverage, impossible-travel completeness, session hijacking completeness, autonomous SOC, AI-approved disposition, analyst-approved disposition.
- Next promotion gate: proof record creation under separate proof scope; live identity telemetry evidence; signal-preserved case packet; public-safe review; human review.
- Role-fit signal: Shows coverage thinking, gap analysis, identity monitoring alignment, and controlled validation discipline for AI Security Operations and SOC automation review.

### Weaponization

- Meaning: Where attacker behaviors are modeled defensively into detection logic, fixtures, validators, scanners, and reviewable proof packages.
- HawkinsOperations artifacts: detection source packages, Splunk/Sigma/Wazuh source where present, validation packages, validation registry, parity verifiers, claim-boundary scanners, proof status index, proof records for HO-DET-001, HO-DET-011, HO-DET-012, and AWS-DET-001.
- ATT&CK / behavior family: ATT&CK-mapped detection families represented in source and validation records, including PowerShell execution, service creation, scheduled task creation, identity suspicious behavior, cloud IAM denial behavior, telemetry tamper source planning, and NDR visibility contracts.
- Current proof state: proof records exist only where the proof repo records them. HO-DET-012 has a governed CONTROLLED_TEST_VALIDATED proof record; ID-DET-001..004 remain NO_PROOF_RECORD. HO-DET-013 remains SOURCE_EXISTS / VALIDATION_PLANNED. HO-NDR-001 remains a boundary scaffold route.
- Validation state: controlled validation exists for HO-DET-001, HO-DET-011, HO-DET-012, AWS-DET-001, and ID-DET-001..004. Validation is planned for HO-DET-013. HO-PIPE-001 has validation contract enforcement for route-integrity shape and field-preservation requirements.
- What exists: Defensive detection models, controlled fixtures, deterministic validators, parity verifiers, claim-boundary scanners, and proof records where approved records exist.
- What it proves: HawkinsOperations can convert behaviors into testable detection engineering artifacts and keep source, validation, and proof truth separated.
- What it does not prove: offensive weaponization, production readiness, runtime-active deployment, signal-observed telemetry, public-safe runtime proof, autonomous SOC operation, AI-approved disposition, or analyst-approved disposition.
- Automation support: deterministic validators, result parity verifiers, proof-index verifier, claim-boundary scanners, proof-pack verifier, and reviewer packets.
- AI-support boundary: AI may draft summaries, identify missing context, and help organize reviewer questions. Deterministic validation and human review authorize claims.
- Blocked claims: AI-approved detection, analyst-approved disposition, production-ready, runtime-active, signal-observed, public-safe runtime proof, customer-deployed.
- Next promotion gate: reviewer packet, validation report, proof record where absent, deterministic verifier pass, and human review.
- Role-fit signal: Shows detection engineering workflow, test design, quality gates, and proof-boundary maturity without promoting unsupported claims.

### Delivery

- Meaning: Where suspicious access attempts or inbound paths begin to enter monitored environments.
- HawkinsOperations artifacts: AWS-DET-001 CloudTrail-style IAM denial source, validation report, proof record, proof card, and future cloud/access delivery lane.
- ATT&CK / behavior family: cloud/IAM denial behavior and access-attempt visibility.
- Current proof state: CONTROLLED_TEST_VALIDATED for AWS-DET-001 in the proof record; FIXTURE_ONLY for the CloudTrail-style validation scope; NOT_PUBLIC_SAFE.
- Validation state: AWS-DET-001 passed 6 controlled CloudTrail-style IAM denial fixtures: 3 positive, 3 negative, 0 missed positives, and 0 false-positive negatives.
- What exists: Source rule, CloudTrail-style fixture selector, controlled validation report, proof record, proof card, validator, parity verifier, and claim-boundary scanner.
- What it proves: AWS-DET-001 passed controlled fixture validation for IAM denied or unauthorized behavior.
- What it does not prove: live AWS proof, live CloudTrail proof, AWS account coverage, deployed cloud detection, cloud runtime-active proof, signal-observed public proof, or public-safe runtime proof.
- Automation support: validation report, proof card, result parity verifier, claim-boundary scanner, and blocked live-AWS claim handling.
- AI-support boundary: AI may summarize case context and missing fields. AI cannot claim live AWS proof or approve cloud runtime claims.
- Blocked claims: live AWS, live CloudTrail, AWS account coverage, cloud runtime-active proof, signal-observed, production-ready, AI-approved disposition, analyst-approved disposition.
- Next promotion gate: sanitized live CloudTrail evidence, enabled cloud detection route, evidence linkage, stale review, wording review, public-safe review, and human approval.
- Role-fit signal: Shows cloud/security monitoring relevance while maintaining clear fixture-only and no-live-cloud boundaries.

### Exploitation

- Meaning: Where suspicious execution and post-exploitation behavior is detected.
- HawkinsOperations artifacts: HO-DET-001 Suspicious PowerShell EncodedCommand Execution; HO-DET-001 proof record; HO-DET-001 proof card; Proof Pack 001; controlled validation report; proof-loop workflow; case packet; AutoSOC triage packet; claim-boundary scanner.
- ATT&CK / behavior family: T1059.001 Command and Scripting Interpreter: PowerShell.
- Current proof state: CONTROLLED_TEST_VALIDATED. Private/internal runtime context exists in the proof record only as non-public boundary context and does not promote public runtime proof.
- Validation state: HO-DET-001 passed 14 controlled process-creation fixtures: 7 positive, 7 negative, 0 missed positives, and 0 false-positive negatives.
- What exists: Detection source, Splunk source, validation cases, validation result, proof record, proof card, Proof Pack 001 release route, case packet, AutoSOC triage packet, proof integrity verifier, proof pack verifier, parity verifier, and claim-boundary scanner.
- What it proves: HO-DET-001 is controlled-test validated for the stated PowerShell encoded-command fixture scope.
- What it does not prove: runtime-active deployment, signal-observed public proof, live Splunk proof, Cribl-routed proof, Wazuh-routed proof, public-safe runtime proof, production-ready status, autonomous SOC operation, AI-approved disposition, or analyst-approved disposition.
- Automation support: validation script, parity verifier, claim-boundary scanner, proof integrity verifier, proof-pack verifier, deterministic case packet, and reviewer packet.
- AI-support boundary: AI may support triage summaries and questions over sanitized facts. AI cannot approve proof, promote claims, close cases, or decide disposition.
- Blocked claims: runtime-active, signal-observed, live Splunk, Cribl-routed proof, Wazuh-routed proof, production-ready, public-safe runtime proof, autonomous SOC, AI-approved disposition, analyst-approved disposition.
- Next promotion gate: runtime evidence promotion, signal evidence, public-safe evidence linkage, stale review, wording review, and human review.
- Role-fit signal: Direct match to detection engineering, alert quality, false-positive control, SOC workflow modeling, and governed AI-assisted triage.

### Installation

- Meaning: Where persistence, service creation, scheduled tasks, and foothold maintenance behaviors are detected.
- HawkinsOperations artifacts: HO-DET-011 Windows Service Creation / Binary Change; HO-DET-012 Suspicious Scheduled Task Creation.
- ATT&CK / behavior family: service creation / persistence behavior; scheduled task or job behavior.
- Current proof state: HO-DET-011 is PRIVATE_RUNTIME_EVIDENCE_CAPTURED and NOT_PUBLIC_SAFE in the proof record. HO-DET-012 has a governed CONTROLLED_TEST_VALIDATED proof record and remains NOT_PUBLIC_SAFE, with runtime, signal, and public-safe runtime proof blocked / not proven.
- Validation state: HO-DET-011 passed 17 controlled Windows service creation fixtures: 7 positive, 10 negative, 0 missed positives, and 0 false-positive negatives. HO-DET-012 passed 8 controlled scheduled-task fixtures: 4 positive, 4 negative, 0 missed positives, and 0 false-positive negatives.
- What exists: Source packages for both detections, validation reports, claim-boundary scanners, HO-DET-011 proof record, HO-DET-012 proof record, HO-DET-012 proof card, proof index boundaries, and platform case-packet visibility for HO-DET-011 with drift review noted in platform contract docs.
- What it proves: Controlled validation exists for both persistence-related detections. HO-DET-011 also has sanitized private runtime evidence captured, but that status is not public-safe proof.
- What it does not prove: runtime-active public proof, signal-observed proof, public-safe proof, production deployment, Wazuh observation, Splunk observation, Cribl routing, complete service-creation coverage, scheduled-task coverage completeness, autonomous SOC, AI-approved disposition, or analyst-approved disposition.
- Automation support: validator scripts, result parity checks, claim-boundary scanners, proof status index, proof record routes for HO-DET-011 and HO-DET-012, and case-packet guardrails.
- AI-support boundary: AI may summarize validation outcomes and flag drift for review. AI cannot normalize drift, promote private runtime evidence, create proof records, or decide disposition.
- Blocked claims: public-safe proof, signal-observed, runtime-active, production deployment, complete service-creation coverage, scheduled-task coverage completeness, live Splunk, Wazuh-routed proof, Cribl-routed proof, autonomous SOC, AI-approved disposition, analyst-approved disposition.
- Next promotion gate: public-safe evidence review for HO-DET-011; runtime and signal evidence review under separate scope for HO-DET-012; route correlation review; stale review; wording review; human approval.
- Role-fit signal: Strong persistence-stage fit showing validated output, proof-boundary discipline, private/public separation, and unresolved proof gaps.

### Command & Control

- Meaning: Where outbound control paths, cross-source visibility, and telemetry routing would support investigation of attacker control channels.
- HawkinsOperations artifacts: HO-NDR-001 Security Onion / NDR visibility boundary; HO-PIPE-001 Cribl / pipeline route integrity source contract; cross-source corroboration contract surfaces.
- ATT&CK / behavior family: C2 visibility support surface, NDR corroboration boundary, and pipeline route contract.
- Current proof state: HO-NDR-001 is BOUNDARY_CONTRACT_ONLY with proof card and boundary contract routes. HO-PIPE-001 is SOURCE_EXISTS / VALIDATION_CONTRACT_ENFORCED and not a runtime route proof.
- Validation state: HO-NDR-001 contract/verifier shape is enforced in validation. HO-PIPE-001 validation contract enforcement exists for route-integrity shape and field-preservation requirements.
- What exists: Security Onion visibility contract, cross-source corroboration sample, verifier routes, proof card, boundary doc, source-controlled pipeline route integrity contract, HO-PIPE-001 validation result, and platform Telemetry Coverage Contract v0 for HO-NDR-001 and HO-PIPE-001.
- What it proves: Boundary and contract shapes exist for future NDR/cross-source review. Pipeline source artifacts and validation contract enforcement exist for route integrity and field preservation without claiming delivered telemetry.
- What it does not prove: Security Onion observed proof, Cribl-routed proof, Wazuh-routed proof, live Splunk proof, Zeek completeness, Suricata detection quality, runtime-active status, signal-observed status, production NDR, or public-safe runtime proof.
- Automation support: pipeline route contract, cross-source corroboration contract, visibility boundary, proof status index, and verifier routes.
- AI-support boundary: AI may explain missing telemetry and summarize route requirements. AI cannot claim observed Security Onion, Splunk, Wazuh, or Cribl signal.
- Blocked claims: Security Onion observed proof, Cribl-routed proof, Wazuh-routed proof, live Splunk, signal-observed, runtime-active, production-ready, public-safe proof, autonomous SOC, AI-approved disposition, analyst-approved disposition.
- Next promotion gate: preserved NDR evidence, cross-source signal packet, route verifier, evidence-link review, public-safe review, and human review.
- Role-fit signal: Shows telemetry architecture thinking, route integrity, and automation workflow boundaries without claiming observed C2 telemetry.

### Actions on Objectives

- Meaning: Where alerts become analyst workflow, triage, case packets, metrics, and bounded response support.
- HawkinsOperations artifacts: SOAR Case Packet v0, AutoSOC Case Ledger v0 tracked artifact route, Detection Factory Controller v0, Local GPU Triage Gate, Offline LLM Triage Support Contract, HO-DET-001 case packet, AutoSOC triage packet, proof records, and reviewer packets.
- ATT&CK / behavior family: investigation and response workflow layer; not a direct detection claim.
- Current proof state: AI_SUPPORT_ONLY, HUMAN_REVIEW_REQUIRED, and reviewer-route-only where represented. Rendering and schemas are not proof authority.
- Validation state: SOAR Case Packet v0 and platform support contracts are deterministic contract/sample surfaces. HO-DET-001 controlled case packet and AutoSOC triage packet are controlled-test support artifacts.
- What exists: Sanitized case packet structures, blocked action gates, deterministic case packet and triage artifacts, offline LLM support contract, local GPU triage contract/gate, detection factory controller status/plan packet contract, AutoSOC case ledger tracked artifact route, proof records, and proof cards.
- What it proves: HawkinsOperations has bounded analyst-support workflow structures and deterministic guardrails for case packet review, triage support, and proof-boundary visibility.
- What it does not prove: autonomous SOC operation, autonomous resolution, AI-approved disposition, analyst-approved disposition, response automation, containment execution, closure execution, suppression execution, SOCaaS availability, production SOC, or public-safe runtime proof.
- Automation support: deterministic case packet structure, append-only ledger concept or tracked ledger route, factory controller status/plan packets, verifier/check cards, blocked action gates, and claim-boundary scanning.
- AI-support boundary: AI may summarize sanitized facts, identify missing context, draft human-review questions, and map checklist fields. AI cannot decide disposition, close cases, approve proof, suppress alerts, contain systems, execute response, or promote public claims.
- Blocked claims: autonomous SOC, autonomous resolution, AI-approved disposition, analyst-approved disposition, response automation, containment execution, closure execution, suppression execution, SOCaaS availability, production-ready, public-safe runtime proof.
- Next promotion gate: case packet evidence, deterministic verifier pass, human review, public-safe review, and separate promotion approval before any response or closure wording.
- Role-fit signal: Direct fit for AI-assisted SOC workflow, SOAR automation, case summarization, metrics, validation, false-positive control, and governed analyst support.

## Role-Fit Summary

This map translates HawkinsOperations into a role-fit surface for AI Security Operations, Detection Engineering, and SOC Automation review.

- AI Security Operations: shows AI as support labor with deterministic boundaries, missing-context review, and human approval requirements.
- Detection Engineering: shows source packages, ATT&CK or behavior mapping, controlled validation, false-positive boundaries, and proof-state separation.
- SOC Automation: shows case packets, ledger routes, factory controller packets, blocked response gates, and verifier-backed workflow controls.
- AI-assisted triage: shows sanitized summaries and question drafting while blocking disposition authority.
- SOAR workflow support: shows structured case packets and response gates without claiming containment, closure, suppression, or production automation.
- Validation and false-positive control: shows positive and negative fixture counts, result parity, and claim-boundary scanners.
- Coverage and gap reporting: shows which stages have proof records, which have validation only, and which remain contract-only, source-only, planned, or blocked.

## Claim Boundary

AI is labor.

Evidence and human review authorize claims.

Cyber Kill Chain mapping is reviewer navigation, not proof authority.

This artifact does not create proof records, does not publish private evidence, does not update the website, does not claim runtime-active status, does not claim signal-observed proof, does not claim production readiness, does not claim public-safe runtime proof, and does not approve AI or analyst disposition.
