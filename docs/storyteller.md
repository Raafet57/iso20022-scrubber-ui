# ISO 20022 Narrative Generator (“The Storyteller”)

## Problem Statement
Payment-operations analysts, compliance reviewers, and client service reps struggle to read ISO 20022 XML directly because business context is buried inside technical tags such as `<UltmtDbtr>`, `<Cdtr>`, `<Purp>`, and `<RmtInf>`. Typical pacs.008 files contain 150–300 elements, forcing analysts to mentally translate debtor/creditor details, intermediaries, charges, references, and remittance strings before they can answer a customer inquiry. This cognitive load slows response times, increases training costs for new hires, and elevates the error rate during high-volume periods (`ISO20022_MicroTools_PRD_numbered.txt:40-49`).

## Target Users
- Primary: L1/L2 payment operations support responding to customer investigations.
- Secondary: Compliance officers reviewing AML/KYC escalations.
- Tertiary: Client service representatives supporting corporate treasurers (`ISO20022_MicroTools_PRD_numbered.txt:45-48`).

## Value Proposition
Automatically converts pacs.008/pacs.009/camt.053 XML into readable narratives, reducing investigation time by ~40%, giving junior analysts actionable context without deep ISO training, and improving customer-response speed/accuracy (`ISO20022_MicroTools_PRD_numbered.txt:49-50`).

## Functional Requirements
### Input Interface
- Text area for paste (≥50k characters).
- XML file upload up to 5 MB.
- Supports pacs.008, pacs.009, camt.053 and auto-detects message type from namespace (`ISO20022_MicroTools_PRD_numbered.txt:52-56`).

### Processing Logic
- Extract actors (Dbtr, UltmtDbtr, Cdtr, UltmtCdtr, instructing/intermediary/creditor agents).
- Capture financials (InstdAmt, IntrBkSttlmAmt, currency, FX rate), temporal data (creation, request, settlement timestamps), references (End-to-End ID, UETR, Tx references), remittance info (structured/unstructured), and charge info (SHA/OUR/BEN, breakdown).
- Use the structured data to feed the narrative generator (`ISO20022_MicroTools_PRD_numbered.txt:57-64`).

### Output Generation
- Invoke a lightweight LLM (Claude 3 Haiku or equivalent) to produce:
  - **Narrative mode**: Rich paragraph summarizing who is paying whom, why, how much, routing, and charge bearer.
  - **Concise mode**: Bullet summary for rapid scanning (`ISO20022_MicroTools_PRD_numbered.txt:65-68`).

## Non-Functional Requirements
- Performance: sub-3s response for typical files.
- Security: client-side parsing; no server-side XML storage.
- Availability: 99.5% uptime in US/EU/APAC business hours (`ISO20022_MicroTools_PRD_numbered.txt:69-72`).

## Success Metrics
- Accuracy rating ≥4.5/5 via in-app feedback.
- Time on page <30 s on average.
- ≥500 weekly active users by Month 3 (`ISO20022_MicroTools_PRD_numbered.txt:73-85`).

## Technical Architecture
- React/Next.js SPA hosted on Vercel/Netlify.
- XML parsing via fast-xml-parser or xml2js (client-side).
- LLM integration via Anthropic Claude API (`ISO20022_MicroTools_PRD_numbered.txt:86-90`, `ISO20022_MicroTools_PRD_numbered.txt:323-326`).

## User Stories
- US-1.1: L1 agent pastes pacs.008 to instantly identify payer/beneficiary and status.
- US-1.2: Compliance analyst reads narrative to understand flagged payment purpose.
- US-1.3: New hire toggles between narrative and bullet view to learn structure while working (`ISO20022_MicroTools_PRD_numbered.txt:92-94`).

## Implementation Notes
- Reuse shared code for XML ingestion and validation with other micro-tools.
- Caching frequently used tag mappings (e.g., actor role to friendly label) accelerates LLM prompting.
- Align output tone with documented UX/prompt guidelines when available.
