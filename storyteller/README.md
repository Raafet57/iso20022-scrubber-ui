## Storyteller Prototype

This folder contains an offline prototype of the “Storyteller” ISO 20022 narrative generator covering pacs.008, pacs.009, and camt.053 messages. It parses XML files client-side (no services) and produces descriptive summaries using deterministic templates. The goal is to validate extraction logic before wiring in an LLM and UI.

### Features
- Detects the message type (pacs.008, pacs.009, camt.053) by inspecting the `Document` payload.
- Extracts key actors, financial data, references, remittance information, and routing metadata.
- Generates two narrative styles:
  - `narrative`: paragraph-style summary suitable for quick reading.
  - `concise`: bullet-style output for scanning.
- Includes sample files sourced from SWIFTRef-inspired test data.

### Usage
```
cd storyteller
python cli.py samples/pacs008-sample.xml --mode narrative
python cli.py samples/pacs009-sample.xml --mode concise
python cli.py samples/camt053-sample.xml
python generate_samples.py  # regenerate the extended synthetic dataset

# Launch browser UI (static)
cd ui
python3 -m http.server 4185
# open http://localhost:4185/index.html
```

### Extending
- New message types can be supported by adding an extraction function in `parser.py` and updating `generate_narrative` in `narrative.py`.
- Narrative templates are intentionally simple; replace them with LLM calls once the canonical schema stabilises.

### Notes
- No network calls or storage; everything runs locally for experimentation.
- Sample files are lightweight and use SWIFTRef-style identifiers to exercise the parser.
- The `/ui` subfolder reuses the same parsing logic in browser JavaScript and reads samples from `../samples`.
