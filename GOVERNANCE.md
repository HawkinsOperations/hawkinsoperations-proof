# Governance

Repository: `hawkinsoperations-proof`

## Rules

1. Evidence entries must be attributable and reproducible.
2. Claims without evidence links are not promotable.
3. No host-local paths, credentials, or secret material in tracked files.
4. Public-safe redaction standards apply only after public-safe approval; externally shareable proof remains blocked unless approval exists.

## Evidence Contract

- Evidence ledger files:
  - `evidence/EVIDENCE_LEDGER_SCHEMA.json`
  - `evidence/evidence-ledger.json`
- Entries include artifact paths and checksums.

## Promotion Gate

- Required governance files must exist.
- CI gate must pass before merge.
- Public-safe output remains blocked unless explicitly approved; internal control-plane data stays out.
