# Legacy-to-Rich Translator (“The Rosetta Stone”)

## Problem Statement
As SWIFT retires MT categories in favour of ISO 20022, seasoned MT103/202/940 operators struggle to locate equivalent data inside verbose MX structures like `<DbtrAcct><Id><IBAN>`. This knowledge gap drives $10k+ per-employee training costs, slows migration adoption, and increases friction between legacy experts and ISO-native teams (`ISO20022_MicroTools_PRD_numbered.txt:201-206`).

## Target Users
- Banks migrating via CBPR+ (primary).
- Corporate treasurers consuming ISO 20022 statements.
- Training/documentation teams building migration materials (`ISO20022_MicroTools_PRD_numbered.txt:206-209`).

## Value Proposition
Provides a side-by-side “virtual MT” generated from ISO XML, preserving institutional knowledge while showcasing richer data. Acts as both educational aid and day-to-day reference, accelerating migration understanding (`ISO20022_MicroTools_PRD_numbered.txt:210-211`).

## Functional Requirements
### Split-View Interface
- Left pane accepts ISO XML (pacs.008, pacs.009, camt.053).
- Right pane renders MT103/202/940-equivalent view to mimic legacy tooling (`ISO20022_MicroTools_PRD_numbered.txt:213-215`).

### Field Mapping Engine
- Implement mappings from SWIFT MT↔MX guidelines, e.g.:
  - :20: ← `CdtTrfTxInf/PmtId/InstrId`
  - :32A: ← `IntrBkSttlmDt` + `IntrBkSttlmAmt`
  - :50K: ← `Dbtr/Nm + Dbtr/PstlAdr`
  - :59: ← `Cdtr/Nm + Cdtr/PstlAdr`
  - :70: ← `RmtInf/Ustrd`
  - :71A: ← `ChrgBr`
  - Field 121 (UETR) ← `CdtTrfTxInf/PmtId/UETR`
(`ISO20022_MicroTools_PRD_numbered.txt:216-241`)

### Interactive Highlighting
- Hover/click on XML highlights MT field (and vice versa) to reinforce learning; tooltips explain the relationship (`ISO20022_MicroTools_PRD_numbered.txt:242-244`).

### Truncation Warnings
- Flag data that cannot survive MT conversion (addresses >4×35 chars, structured remittance, ultimate parties) so users understand potential data loss (`ISO20022_MicroTools_PRD_numbered.txt:244-248`).

## Success Metrics
- Interaction rate with highlighting >60%.
- Post-session “Did this help you understand ISO 20022?” ≥4/5.
- 30-day return users >40% (`ISO20022_MicroTools_PRD_numbered.txt:249-252`).

## User Stories
- US-4.1: Banker finds MT Field 50K equivalent quickly.
- US-4.2: Trainer demonstrates ISO data richness vs MT.
- US-4.3: Corporate treasurer interprets new statements for reconciliation (`ISO20022_MicroTools_PRD_numbered.txt:254-256`).

## Technical Notes
- Reuse Monaco Editor for side-by-side highlighting plus custom mapping JSON as per Appendix A (`ISO20022_MicroTools_PRD_numbered.txt:331-333`).
- Maintain authoritative mapping source files so updates track SWIFT releases.
