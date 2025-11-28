# Reject Reason Decoder (“The Fixer”)

## Problem Statement
Payments rejected via pacs.002 embed four-character codes (e.g., AC03, AM05, BE04) within `<TxSts><Rsn><Cd>` and often include cryptic `<AddtlInf>`. Analysts must dig through lengthy SWIFT/CBPR+ references, interpret context (which agent rejected), and experiment with fixes—burning 30–60 minutes per incident with multiple retry loops (`ISO20022_MicroTools_PRD_numbered.txt:257-262`).

## Target Users
- Exception-handling teams processing failed payments.
- Client service reps translating failures for corporate clients.
- Technical support teams diagnosing integration issues (`ISO20022_MicroTools_PRD_numbered.txt:262-265`).

## Value Proposition
Instantly diagnoses rejection causes, explains context, and prescribes remediation so analysts can resolve issues in <5 minutes with higher first-time-fix rates (`ISO20022_MicroTools_PRD_numbered.txt:266-267`, `ISO20022_MicroTools_PRD_numbered.txt:302-307`).

## Functional Requirements
### Input Processing
- Accept pacs.002 XML via paste/upload.
- Auto-extract TxSts, Rsn/Cd, AddtlInf, rejecting agent context.
- Support multiple rejection reasons within a single message (`ISO20022_MicroTools_PRD_numbered.txt:269-272`).

### Knowledge Base
- Maintain structured catalogue of reason codes with plain-English meaning and remediation guidance (e.g., AC01 incorrect account, AC03 invalid account, AC04 closed account, AM05 duplication, BE04 missing address, RC01 invalid BIC, NARR refer to additional info) (`ISO20022_MicroTools_PRD_numbered.txt:273-290`).

### Output
For each rejection:
- What happened (summary).
- Where it happened (institution + BIC if available).
- Why (root cause).
- Actionable fix (specific steps).
- Confidence level (High/Medium/Low) reflecting data specificity (`ISO20022_MicroTools_PRD_numbered.txt:291-297`).

## Success Metrics
- Resolution time <5 min vs 30–60 min baseline.
- First-time fix rate >80% (~50% baseline).
- Viral coefficient >1.2 (new product) (`ISO20022_MicroTools_PRD_numbered.txt:298-310`).

## User Stories
- US-5.1: Exception handler pastes pacs.002 and receives immediate diagnosis.
- US-5.2: CSR gets plain-English explanation suitable for clients.
- US-5.3: New analyst learns rejection codes over time while working cases (`ISO20022_MicroTools_PRD_numbered.txt:311-314`).

## Technical Notes
- Knowledge base can leverage `ExternalStatusReason1Code`, `ExternalReturnReason1Code`, and other code lists now stored in `reference/external_codes/`.
- Consider optional LLM assist to interpret free-text `NARR` segments for bank-specific guidance (`ISO20022_MicroTools_PRD_numbered.txt:333-334`).
