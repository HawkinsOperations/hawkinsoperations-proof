# HO-DET-001 Runtime Signal 002 Route-Provenance Debug

## Date / Scope

Date: 2026-05-06

Scope: Static debugging artifact for HO-DET-001 Runtime Signal 002 route provenance, built from governed session log entries and active control rules. This artifact records what the existing private/internal evidence supports and what remains blocked.

Mode: CREATE_ONLY

Out of scope:

- Proof-record edits.
- README edits.
- Validation, detections, platform, website, or GitHub control changes.
- Raw private Splunk event content inspection or reproduction.
- Staging, committing, pushing, merging, or GitHub mutation.

## Debugging Question

Did the existing Runtime Signal 002 Splunk marker-bearing Sysmon rows prove HO-DET-001 Sysmon traffic traversed Cribl, or did they only prove Splunk indexed marker-bearing Sysmon rows through a non-Cribl or unknown route?

## Intended Claim Under Test

Intended private/internal claim under test:

`Runtime Signal 002 produced marker-bearing Sysmon Event ID 1 rows visible in Splunk, and those rows can be attributed to the intended Cribl-routed HO-DET-001 path.`

The first half was supported privately. The route-attribution half was not.

## Evidence Chain

Evidence source class: governed local session log and active control files.

Observed chain:

1. A preflight confirmed the operator could perform controlled private/internal checks without changing services, routes, indexes, HEC, or proof surfaces.
2. A controlled event-generation step produced local Sysmon Event ID 1 anchors, but did not prove Cribl-specific traversal.
3. A first Splunk UI export existed and was preserved, but its projected fields omitted the marker and key event fields.
4. A later raw-field Splunk export proved marker-bearing Sysmon Event ID 1 rows in private/internal scope.
5. Route-provenance audit compared the Splunk export shape against existing Splunk forwarder and Cribl route evidence.
6. The audit classified the rows as Splunk-indexed through a non-Cribl or unknown route, with evidence favoring direct Splunk Sysmon ingestion over Cribl traversal.

Control boundaries applied:

- Repo truth is not runtime truth.
- Runtime truth is not public proof.
- Data output is not automatically public-safe evidence.
- Website or GitHub rendering is not proof.
- Private/internal evidence does not self-promote to public-safe status.

## First Failed Export: Projected CSV Lacked Marker/Key Event Fields

The first exported CSV proved only that a Splunk UI export existed and contained a bounded row set.

Supported:

- Export existed.
- Row count was known.
- Basic index-facing fields were present.

Blocked:

- Marker proof from the projected export.
- Event-specific Sysmon field proof from the projected export.
- Any claim that the projected export alone proved HO-DET-001 signal observation.

Reason: the projected export lacked the marker-bearing content and key event fields needed to connect the rows to the controlled marker event. It was retained as a private/internal evidence candidate, but it was not self-contained marker proof.

## Improved Raw Export: Marker-Bearing Sysmon Rows Proven Private/Internal

The improved raw-field export changed the private/internal evidence state.

Supported:

- Marker-bearing rows were present in the raw-field export.
- The rows were Sysmon Event ID 1 XML rows.
- Raw content was nonblank in the exported rows.
- A subset showed EncodedCommand evidence.
- One row matched the original local anchor identifier from the controlled event-generation sequence.

Classification:

`SPLUNK_MARKER_BEARING_SYSMON_ROWS=PROVEN_PRIVATE_INTERNAL`

Limits:

- The raw event content remains private/internal and is intentionally not reproduced here.
- The export includes verification-noise rows as well as the original anchor row.
- This proves private/internal Splunk-indexed marker-bearing Sysmon rows, not Cribl route traversal.
- This does not create public-safe runtime proof.

## Route Provenance Audit

The route-provenance audit asked whether the marker-bearing Sysmon rows could be attributed to Cribl traversal.

Evidence supporting Splunk indexing:

- The raw export showed marker-bearing Sysmon Event ID 1 rows.
- The export context matched a Sysmon-oriented Splunk search/index path.
- Existing forwarder evidence showed Sysmon Operational collection through a Splunk Universal Forwarder path.

Evidence against claiming Cribl-routed Sysmon:

- Prior Runtime Signal 002 Cribl log/state marker observation was zero at check time.
- The raw export did not include event-specific Cribl or HEC route metadata.
- Existing Cribl artifacts described a separate Wazuh/syslog lane, not the exported Sysmon path.
- Later Cribl marker-delivery evidence proved a separate lab marker lane, but not Runtime Signal 002 Sysmon traversal.
- Aggregate Cribl route health evidence was not marker-specific delivery proof.

Route conclusion:

`ROUTE_PROVENANCE=SPLUNK_INDEXED_NON_CRIBL_OR_UNKNOWN_ROUTE`

## Final Classification

`SPLUNK_MARKER_BEARING_SYSMON_ROWS=PROVEN_PRIVATE_INTERNAL`

`ROUTE_PROVENANCE=SPLUNK_INDEXED_NON_CRIBL_OR_UNKNOWN_ROUTE`

`HO_DET_001_CRIBL_ROUTED_SYSMON=BLOCKED`

`PUBLIC_SAFE_STATUS=NOT_PUBLIC_SAFE`

`PUBLIC_PROOF_CEILING=CONTROLLED_TEST_VALIDATED`

## Blocked Claims

The following claims are blocked for this artifact:

- Cribl-routed HO-DET-001 Sysmon proof.
- Wazuh-routed HO-DET-001 Sysmon proof.
- Runtime-active public proof.
- Signal-observed public proof.
- Public-safe runtime proof.
- Production-ready status.
- Fleet-wide coverage.
- Autonomous SOC operation.
- AI-approved disposition.
- Analyst-approved disposition.

Allowed bounded wording:

- Private/internal Splunk export proved marker-bearing Sysmon Event ID 1 rows.
- Route provenance remains Splunk-indexed through a non-Cribl or unknown route.
- HO-DET-001 Cribl-routed Sysmon proof remains blocked.
- Public ceiling remains test-validated controlled-test scope.

## Why This Matters To HawkinsOperations

This artifact preserves the central HawkinsOperations boundary: AI is labor, governance is authority.

The evidence became stronger in one specific way: private/internal Splunk marker-bearing Sysmon rows were proven. That improvement does not authorize a stronger route claim. A true proof lane must distinguish event observation from route provenance, and must keep public language below the supported ceiling.

The debugging result prevents a common claim leak: treating Splunk visibility as proof that the event traversed the intended Cribl route.

## What Control Should Be Built Next

Next control needed: a Cribl-specific route-correlation capture contract for HO-DET-001.

Minimum requirements:

- Capture event-specific route metadata before, during, and after Cribl processing.
- Preserve a marker-specific correlation key without exposing raw private event data.
- Prove source lane, Cribl input, pipeline, destination, Splunk ingestion, and final indexed row linkage.
- Separate direct Splunk forwarder ingestion from Cribl-forwarded ingestion.
- Produce a sanitized summary and blocked-claims table.
- Keep public ceiling unchanged until explicit operator approval promotes a public claim record.

This should be a plan-only control first. No new event, service change, route change, or proof promotion should occur without separate approval.

## Public-Safe Summary Draft

Draft for private review only; not approved for publication:

HO-DET-001 remains publicly bounded to test-validated controlled-test scope. A private/internal debugging pass proved marker-bearing Sysmon rows in Splunk, but route provenance did not support a Cribl-routed Sysmon claim. Public-safe runtime proof remains blocked pending a separate approved claim record.

Required boundary sentence if this is later reviewed for public use:

Website/GitHub rendering is not proof. Public surfaces route to proof records.

## Private/Internal Notes Intentionally Excluded

Excluded from this repo artifact:

- Raw Splunk event content.
- Raw marker strings.
- Private hostnames.
- LAN IP addresses.
- Usernames.
- Local private evidence paths.
- Private export filenames.
- Event record identifiers.
- Process GUIDs or UUID-like values.
- Hashes for private exports.
- Raw model output.
- Tokens, secrets, credentials, or credential-handling details.

These exclusions are intentional. The artifact records the route-provenance debugging result without publishing private operational evidence.
