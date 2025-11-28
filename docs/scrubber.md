# Smart XML Anonymizer (“The Scrubber”)

## Problem Statement
Sharing production ISO 20022 logs with vendors or the community is risky because files contain PII (names, addresses, IBANs, tax IDs, transaction amounts). Manual redaction is slow and breaks XML schemas, while naive find/replace produces invalid IBANs (fails mod‑97) and exposes institutions to GDPR/CCPA violations (`ISO20022_MicroTools_PRD_numbered.txt:95-105`).

## Target Users
- Implementation managers collaborating with external vendors during go-live.
- QA engineers deriving reproducible test cases from prod incidents.
- Developers debugging integrations in lower environments (`ISO20022_MicroTools_PRD_numbered.txt:100-103`).

## Value Proposition
Produces vendor-safe XML by masking sensitive data while preserving schema validity and contextual integrity, cutting debug cycles from hours to minutes and ensuring regulatory compliance (`ISO20022_MicroTools_PRD_numbered.txt:104-105`).

## Functional Requirements
### Smart Masking Engine
Detects and replaces:
- Personal & company names (via `<Nm>` and org tags) with placeholder “Person A/B” or “Company A/B”.
- Addresses (`<PstlAdr>`) mapped to synthetic but realistic formats (e.g., “123 Test Street…”).
- IBANs via regex + mod‑97 check, replacing with checksum-valid dummy IBANs.
- Account IDs (under `<AcctId>`) with same-length randomized digits.
- Transaction references preserving format/length (`ISO20022_MicroTools_PRD_numbered.txt:107-129`).

### Consistency & Preservation Rules
- Consistency mode ensures repeated entities receive identical pseudonyms to maintain referential integrity.
- Must NOT anonymize BIC/SWIFT codes, error/status codes, currency/country codes, XML structure/namespaces, and (optionally shifted) timestamps (`ISO20022_MicroTools_PRD_numbered.txt:130-138`).

### Output Options
- Download anonymized XML with `_anonymized` suffix.
- Copy-to-clipboard, side-by-side diff, and CSV mapping export describing replacements (`ISO20022_MicroTools_PRD_numbered.txt:139-143`).

## Success Metrics
- Schema validation pass rate: 100% target (>99% critical threshold).
- PII detection recall: >99% target (>95% threshold).
- Processing time: <2 s target (<5 s threshold) (`ISO20022_MicroTools_PRD_numbered.txt:144-155`).

## User Stories
- US-2.1: Implementation manager shares anonymized failure with vendor.
- US-2.2: QA engineer generates test data from production incident.
- US-2.3: Developer replays anonymized file through parsers without schema edits (`ISO20022_MicroTools_PRD_numbered.txt:157-160`).

## Technical Notes
- Shared dependencies: iban.js for validation/generation, faker.js for dummy data per Appendix A (`ISO20022_MicroTools_PRD_numbered.txt:327-329`).
- Consider a deterministic pseudonymization key so identical inputs produce the same placeholder when required for debugging.
