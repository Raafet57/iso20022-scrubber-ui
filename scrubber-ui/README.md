# ISO 20022 Smart XML Anonymizer

This repository packages the standalone Scrubber UI plus the minimal documentation and reference code sets needed to work locally. Everything runs client-side in the browser; no build tooling is required.

## Features
- Paste/upload ISO 20022 messages (pacs.008/.009, camt.053, etc.)
- Toggle anonymization settings (consistency mode, remittance preservation, timestamp shifting)
- Inspect anonymized XML, a line-by-line diff, and a mapping log of replacements
- Copy/download clean XML for vendor sharing
- Bundled SWIFTRef-derived samples containing realistic BICs, names, addresses, IBANs, and remittance data

## Running Locally
1. Serve the `scrubber-ui` folder (any static server works). Example:
   ```bash
   python3 -m http.server 4175 --directory scrubber-ui
   ```
2. Open <http://localhost:4175/index.html> in Chrome/Edge.
3. Use the sample dropdown to load ready-made files or drop your own ISO 20022 XML.

## Repository Layout
```
README.md                # this file
scrubber-ui/             # vanilla HTML/CSS/JS UI plus samples
  index.html
  samples/
reference/
  external_codes/        # ISO 20022 external code sets (JSON, XLSX, CSV)
docs/
  scrubber.md            # detailed functional specification extracted from the master PRD
```

## Reference Assets
- `docs/scrubber.md`: canonical specification for "The Scrubber" micro-tool (copied from the ISO Micro-Tools PRD).
- `reference/external_codes/`: contains ISO 20022 code lists used by the Reject Decoder/ Scrubber knowledge bases.

## Notes
- If you need a packaged version for GitHub Pages or other hosting, copy the `scrubber-ui` folder contents directly to your web root.
- Large bank-directory datasets from the original `iso_micro` repo are intentionally omitted to keep this repo lightweight.
