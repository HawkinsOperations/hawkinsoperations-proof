# Governance

Repository: `hawkinsoperations-proof`

## Rules

1. Evidence entries must be attributable and reproducible.
2. Claims without evidence links are not promotable.
3. No host-local paths, credentials, or secret material in tracked files.
4. Public-safe reviewer package output is allowed only for sanitized package files after package review; raw/private runtime evidence and externally shareable runtime proof remain blocked unless public-safe runtime proof approval exists.

## Evidence Contract

- Evidence ledger files:
  - `evidence/EVIDENCE_LEDGER_SCHEMA.json`
  - `evidence/evidence-ledger.json`
- Entries include artifact paths and checksums.

## Promotion Gate

- Required governance files must exist.
- CI gate must pass before merge.
- Public-safe runtime proof output remains blocked unless explicitly approved; internal control-plane data stays out.
