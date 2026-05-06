# HO-DET-001 Runtime Signal 003 Cribl Route Public Review

Classification: PRIVATE_TO_PUBLIC_REVIEW_ONLY

This document is a reviewer-facing boundary draft for Runtime Signal 003. It records what the private evidence can support, what it excludes, and what must remain blocked unless a later approval explicitly promotes wording into a proof record or public surface.

It is not a proof-record update, website update, GitHub profile update, release note, or public claim.

## Claim Ceiling

```text
RS003_CRIBL_ROUTE_MARKER_ROW=PROVEN_PRIVATE_INTERNAL
CONTAMINATION_ROWS=EXCLUDED
PUBLIC_SAFE_STATUS=BLOCKED_PENDING_REVIEW
PROOF_RECORD_UPDATE=NOT_APPROVED
WEBSITE_UPDATE=NOT_APPROVED
GITHUB_UPDATE=NOT_APPROVED
```

## Private Evidence Summary

Runtime Signal 003 has private evidence of one controlled marker row landing in Splunk with Cribl route attribution. The valid row was associated with the Cribl relay host and the dedicated Runtime Signal 003 Cribl proof lane.

The same private review set also contained three marker-bearing endpoint Sysmon/OpenSSH rows from the Windows endpoint. Those rows are excluded from Cribl route proof because they do not carry Cribl pipeline attribution.

Supported internal claim:

```text
One Runtime Signal 003 marker row is privately proven as Cribl-routed through the dedicated proof lane.
```

This does not approve public wording, proof-record mutation, website mutation, GitHub mutation, or broader operational status claims.

## Why Runtime Signal 002 Stayed Blocked

Runtime Signal 002 proved that marker-bearing Sysmon rows were visible in Splunk private evidence. It did not prove that those rows traversed the intended Cribl route.

The blocker was provenance. Splunk visibility alone did not establish Cribl traversal, and the available rows lacked event-specific Cribl route attribution.

Allowed review wording:

```text
Runtime Signal 002 showed why marker visibility is not enough: route attribution must be proven separately.
```

## Why Runtime Signal 003 Is Stronger

Runtime Signal 003 is stronger because one marker-bearing row contains Cribl route attribution tied to the dedicated proof lane. That separates the valid Cribl-attributed row from endpoint command-line contamination.

The stronger claim is narrow:

```text
A dedicated Runtime Signal 003 Cribl proof lane produced one marker-bearing Splunk row with Cribl route attribution.
```

This remains private review material. It does not approve broader status or public proof wording.

## Contamination Exclusion

Excluded evidence:

- Three marker-bearing endpoint Sysmon/OpenSSH rows.
- These rows came from the Windows endpoint path.
- These rows lacked Cribl pipeline attribution.
- These rows must not be counted as Cribl route proof.

Allowed contamination wording:

```text
Three marker-bearing endpoint Sysmon rows were excluded because they did not prove Cribl traversal.
```

Blocked contamination interpretation:

```text
Every marker-bearing row proved Cribl routing.
```

Reason blocked: only one marker-bearing row carried Cribl route attribution.

## What Can Be Said

Candidate statements for reviewer consideration:

- Private validation produced one Runtime Signal 003 marker row with Cribl route attribution.
- The Cribl relay path was validated at private scope for one controlled marker row.
- The review preserved a strict distinction between route proof and endpoint command-line contamination.
- Runtime Signal 002 remained blocked because marker visibility did not establish Cribl traversal.
- Runtime Signal 003 improved the proof boundary by separating Cribl-attributed output from endpoint contamination.

Reviewer-facing candidate:

```text
A controlled private validation produced one Cribl-attributed Runtime Signal 003 marker row in Splunk while excluding endpoint contamination from the proof claim.
```

## What Cannot Be Said

Do not claim:

- HO-DET-001 is approved for public proof.
- HO-DET-001 has an approved active deployment claim.
- HO-DET-001 has approved public signal observation.
- HO-DET-001 has broad Cribl-routed telemetry proof.
- HO-DET-001 has Wazuh-routed proof.
- HO-DET-001 has Splunk-live public proof.
- HO-DET-001 has production or fleet coverage proof.
- HO-DET-001 operates as an autonomous SOC.
- AI or an analyst approved the disposition.
- Runtime Signal 002 proved Cribl traversal.
- Endpoint Sysmon/OpenSSH contamination rows are Cribl route evidence.
- Every marker-bearing Runtime Signal 003 row was Cribl-routed.

## Proof-Record Candidate Wording

NOT APPROVED FOR PROOF RECORD UPDATE.

Candidate only:

```text
Runtime Signal 003: private validation found one marker-bearing Splunk row with Cribl route attribution. Three marker-bearing endpoint Sysmon rows were excluded as contamination. Status remains private pending promotion review.
```

Required status if later approved:

```text
PUBLIC_SAFE_STATUS=BLOCKED_PENDING_REVIEW
PROOF_RECORD_UPDATE=NOT_APPROVED
WEBSITE_UPDATE=NOT_APPROVED
GITHUB_UPDATE=NOT_APPROVED
```

## LinkedIn Candidate Wording

NOT APPROVED FOR POSTING.

Candidate only:

```text
A private lab validation pass confirmed the difference between visibility and route proof. One controlled marker row carried Cribl route attribution, while separate endpoint Sysmon rows were excluded as contamination. The useful result was not a bigger claim; it was a tighter one.
```

This wording avoids private host details, raw evidence identifiers, private paths, private command lines, and exact marker values.

## Reviewer Checklist

Before any later public or repo use, confirm:

- No local paths are present.
- No internal network addresses are present.
- No raw hostnames are present beyond generic host labels.
- No raw event bodies are present.
- No private command lines are present.
- No exact marker identifier is present.
- No credentials, secrets, or secret-bearing values are present.
- Runtime Signal 002 remains blocked for Cribl route proof.
- The three endpoint contamination rows remain excluded.
- Runtime Signal 003 is described as one Cribl-attributed marker row, not broad coverage.
- Proof-record update remains not approved unless separately authorized.
- Website update remains not approved unless separately authorized.
- GitHub update remains not approved unless separately authorized.

## Final Boundary

This document is a public-review candidate only. It is not public approval, proof-record approval, website approval, or GitHub approval.
