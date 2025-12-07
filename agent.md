## Session notes (Dec 5, 2025)

Repos:
- Storyteller (`iso20022-Storyteller-ui`): validated CBPR+ SR2025 samples are on `main` (commit `a9031dc`). Feature branch `feature/validation-samples` still exists.
- Scrubber (`iso20022-scrubber-ui`): validated sample set is on `main` (commit `3bedaa6` after reverting feature UI). New UI features (schema validation, mapping export, diff/coverage) are staged on `experiment` at `43b13a8`.

Scrubber UI features on `experiment`:
- CBPR+ SR2025 schema validation (xmllint-wasm) with status badge.
- Mapping export buttons (JSON/CSV).
- Diff tab (already existed) and PII coverage cards.

What to do next:
- Decide whether to merge `experiment` → `main` for scrubber after testing the new UI.
- If merging, optionally delete `feature/validation-samples` (Storyteller) and keep `experiment` only as a sandbox.

Local serve commands:
- Scrubber UI: `cd scrubber-ui && python3 -m http.server 4175 --bind 127.0.0.1` then open `http://127.0.0.1:4175/index.html`.
- Storyteller UI: `cd storyteller/ui && python3 -m http.server 8877 --bind 127.0.0.1`.

Branch tips:
- Storyteller main: `a9031dc`
- Scrubber main: `3bedaa6` (revert of features)
- Scrubber experiment: `43b13a8` (features)
