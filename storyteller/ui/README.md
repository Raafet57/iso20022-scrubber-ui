## Storyteller UI

Lightweight browser interface for the Storyteller prototype. Everything runs client-side (no build tools). It parses ISO 20022 XML (pacs.008, pacs.009, camt.053), generates both narrative and concise summaries, and displays the extracted data.

### Running locally

```
cd /Users/Raafet/Projects/iso_micro/storyteller-ui
python3 -m http.server 4185
```

Navigate to <http://localhost:4185/index.html> in Chrome/Edge.

### Features

- Paste XML or upload a file (≤5 MB).
- Load built-in samples (pacs.008 cover payment, pacs.009 CPPC route, camt.053 statement).
- Auto-detect message type and parse actors, financials, timelines, references, remittance, and routing data.
- Generates two modes:
  - **Narrative** – paragraph-style summary.
  - **Concise** – bullet list.
- Shows a structured table + raw JSON of the parsed payload.
- Copy buttons for both narrative modes.

### Notes

- Parsing logic mirrors the Python prototype (`storyteller/parser.py`).
- Extend support for more messages by updating the JavaScript extraction functions.
- No secrets or LLM calls; narratives use deterministic templates.
