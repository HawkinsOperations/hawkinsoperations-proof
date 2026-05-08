# HO-NDR-001 Security Onion Visibility Contract Boundary

## Summary

The validation repo contains a sanitized clone-runnable Security Onion visibility contract. This proof-repo boundary stub records that the route exists without importing private evidence or promoting a proof claim.

## Authority Boundary

- Validation repo owns the schema, sample, verifier, and workflow.
- Proof repo records the existence of the boundary route only.
- Private runtime evidence remains local/private.
- Website rendering is not proof.
- No public-safe proof is approved.

## Merged Validation Reference

- Validation PR: HawkinsOperations/hawkinsoperations-validation#24
- Merge commit: e37adfed3eade12022efd1f7cceef6175598623f
- Claim ceiling: PRIVATE_NDR_MODULE_VISIBILITY_ROLLUP_DEFINED

## Supported Wording

- A sanitized Security Onion visibility validation contract exists in the validation repo.
- The contract defines required shape and guardrails for private NDR module visibility evidence.
- The contract does not import private evidence and does not promote public proof.

## Blocked Wording

The following claims are not approved by this boundary stub:

- public-safe proof
- production NDR
- permanent SPAN
- fleet-wide visibility
- durable monitoring
- PCAP availability
- long-term retention
- cross-source corroboration
- Zeek coverage completeness
- Suricata detection quality

## Next Gates

- public-safe redaction review
- proof record approval if ever promoted
- website update only after proof record approval
- separate evidence-link review
- stale review date requirement
