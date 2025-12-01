## Storyteller – ISO 20022 Narrative Generator

Client-side tool that ingests pacs.008 / pacs.009 / camt.053 XML and produces readable narratives (paragraph + concise modes) for ops and compliance analysts. No backend required; everything runs locally.

### Features
- Auto-detects message type from the ISO 20022 payload.
- Extracts actors, financials, references, remittance, routing, and charges.
- Two outputs: narrative paragraph and concise summary (plus JSON view and key fields in the UI).
- Ships with a broad sample set to exercise parsing edge cases.

### Quick start – browser UI
```
cd storyteller/ui
python3 -m http.server 4185
# then open http://localhost:4185/index.html
```
- Samples are bundled under `ui/samples/` for easy local hosting.
- Paste your own XML or load a sample; everything stays in-browser.

### Quick start – CLI
```
cd storyteller
python cli.py samples/pacs008-sample.xml --mode narrative
python cli.py samples/pacs009-sample.xml --mode concise
python cli.py samples/camt053-sample.xml
python generate_samples.py   # regenerate synthetic samples
```

### Extending
- Add new message parsers in `parser.py` and update `generate_narrative` in `narrative.py`.
- Swap the deterministic templates for an LLM call once prompts and guardrails are ready.

### Layout
```
storyteller/
  cli.py, parser.py, narrative.py    # core extraction + template generation
  samples/                           # canonical sample inputs
  ui/                                # static HTML/CSS/JS front-end
    index.html
    samples/                         # copy of samples for static hosting
```

### Notes
- No network/storage; intended for offline experimentation and UX validation.
- Uses deterministic templates to prove extraction quality before wiring in an LLM.
