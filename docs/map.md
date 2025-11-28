# Payment Chain Visualizer (“The Map”)

## Problem Statement
Cross-border payments route through multiple agents (Instructing, Intermediary 1–3, Debtor/Creditor Agents, etc.). These hops are buried in nested pacs.008/pacs.009 XML, making it hard for investigators to answer “Where is my payment now?” or “Why did it route via another corridor?” Manual tracing across BIC directories is slow and error prone (`ISO20022_MicroTools_PRD_numbered.txt:161-166`).

## Target Users
- Primary: Payment investigation teams tracing stalled/delayed wires.
- Secondary: Liquidity managers analyzing nostro/vostro relationships.
- Tertiary: Correspondent banking teams reviewing routing efficiency (`ISO20022_MicroTools_PRD_numbered.txt:166-169`).

## Value Proposition
Transforms XML agent chains into intuitive, left-to-right routing diagrams, reducing time-to-insight from 15+ minutes to <30 seconds and driving faster escalations or client updates (`ISO20022_MicroTools_PRD_numbered.txt:170-171`).

## Functional Requirements
### XML Parser
- Extract BICs for DbtrAgt, InstgAgt, IntrmyAgt1-3, CdtrAgt, and InstdAgt from pacs.008/pacs.009 payloads (`ISO20022_MicroTools_PRD_numbered.txt:172-179`).

### BIC Enrichment
- Resolve each BIC via SWIFTRef/open directory to display institution name, country (flag/icon), city, and institution type (`ISO20022_MicroTools_PRD_numbered.txt:180-185`).

### Visualization Engine
- Render left-to-right flow using D3.js or React Flow:
  - Nodes show bank name, BIC, country indicator.
  - Directed edges labelled with settlement method (COVE, INGA, INDA).
  - Optional color coding per clearing system (TARGET2, CHIPS, Fedwire) (`ISO20022_MicroTools_PRD_numbered.txt:186-190`).

### Time Analysis (Phase 2)
- When timestamps (CreDtTm, SttlmDt) exist, surface estimated “time in flight” per hop (`ISO20022_MicroTools_PRD_numbered.txt:191-192`).

## Success Metrics
- Time to insight <30 s vs ≥15 m baseline.
- Diagram export (PNG/PDF) used in >25% of sessions.
- BIC enrichment accuracy >99% (`ISO20022_MicroTools_PRD_numbered.txt:193-196`).

## User Stories
- US-3.1: Investigator sees full bank chain to pinpoint delay.
- US-3.2: Liquidity manager visualizes correspondent relationships for optimization.
- US-3.3: Client service rep exports diagram for customer communications (`ISO20022_MicroTools_PRD_numbered.txt:198-200`).

## Technical Notes
- Depend on React Flow or D3 plus BIC lookup service per Appendix A (`ISO20022_MicroTools_PRD_numbered.txt:329-331`).
- Consider caching enrichment results to minimize API calls when agents repeat across payments.
