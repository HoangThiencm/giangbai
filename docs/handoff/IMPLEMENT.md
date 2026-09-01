# IMPLEMENT: PPCT recognition and preview synchronization

## Latest implementation: PPCT ordering and Appendix 1 header

- Removed the `UBND XÃ/PHƯỜNG ...` line from the Appendix 1 HTML preview and DOCX export. The left heading now consistently uses normalized `TRƯỜNG ...` and `TỔ ...` values only.
- Added PPCT row movement (`▲` / `▼`), HTML5 drag-and-drop, and inline editing for lesson, week, curriculum period, equipment, and location in Section 3.
- Added synchronized PPCT helpers so reordering and edits update `sourcePpctTable`, `sourcePpctRows`, and already-generated Appendix 1/3 data immediately while remapping selected AI period IDs to their moved lesson.
- Updated smoke coverage for the no-UBND heading and PPCT move/reorder/edit synchronization.

## Latest verification

- `node tests/xaydungphuluc-smoke.js` — PASS
- `node tests/xaydungphuluc-integration-smoke.js` — PASS

## Latest implementation: standards-grounded SGK enrichment and math-branch matching

- Updated `compactSgkText` to preserve the table of contents, chapters, lesson names, learning activities, and technology-practice cues (including software, GeoGebra, calculators, and digital transformation), while retaining the 30,000-character safety cap. SGK remains supplementary context only.
- Clarified the Appendix Builder interface: the school PPCT plus the Ministry-standard catalog is sufficient; the SGK upload is explicitly optional. The AI picker also explains that AI codes are limited to the periods selected from PPCT.
- Refined official digital-competency ranking for Toán: algebra prioritizes `5.3` then `1.1`; geometry prioritizes `3.1` then `5.2`; statistics/probability prioritizes `1.1`/`1.2` and uses `3.1` for digital charts. AI recommendations remain grade-specific and are returned only when the relevant PPCT period is selected.
- Added smoke assertions covering structured SGK extraction and the three mathematics-branch priorities.

## Latest verification

- `node tests/xaydungphuluc-smoke.js` — PASS
- `node tests/xaydungphuluc-integration-smoke.js` — PASS
- `git diff --check` — PASS

## Latest implementation: clean YCCĐ matching and landscape DOCX

- Added clean Toán YCCĐ helpers in `js/khbd-yccd.js`: lesson matching now prioritizes the explicit `Bài <số>`, then normalized lesson name, and only then uses keyword scoring. The new clean export joins trimmed, deduplicated outcome bullets without source, legal, lesson, or topic metadata; `getOfficialYccd()` remains compatible.
- Routed Appendix 1 fallback outcomes, standards context, and the prompt's lesson catalog through the clean YCCĐ wrapper. Appendix 1 now replaces an AI outcome containing boilerplate metadata with the clean official YCCĐ and prompts the model to return behavioral outcomes only.
- Made NLS selection honor the lower bound of its configured density range (1–2 → 1, 2–3 → 2, 3–4 → 3), while preserving the existing AI selection behavior.
- Changed DOCX output to A4 landscape (`16838 × 11906`), with landscape orientation and 1134-twip margins on all four sides.
- Extended smoke coverage for Bài 14 clean matching, metadata removal in Appendix 1, all density lower bounds, and the landscape export configuration. Extended integration smoke with static coverage of the clean helper and landscape export.

## Latest verification

- `node tests/xaydungphuluc-smoke.js` — PASS
- `node tests/xaydungphuluc-integration-smoke.js` — PASS
- `git diff --check` — PASS

## Latest implementation: full-width AI picker and explicit full-suite generation

- Made the AI lesson picker card and its picker container full-width, with horizontal overflow for the source PPCT table instead of a two-column grid.
- Changed the full-suite button to explicitly call `generateSelected('all')`.
- Hardened `generateSelected(force)`: it safely falls back to `all` when no radio is checked, expands full-suite selection to appendices 1–3, and synchronizes the `all` radio when that path is used.
- Updated smoke and integration coverage to check the picker layout, button argument, and mocked full-suite generation without calling an AI provider.

## Latest implementation: standards, staged document workflow, and single integration column

- Added `js/khbd-standards.js` and a shared `normalizeIntegrationTable` adapter so imported, generated, previewed, and DOCX PPCT tables retain exactly one integration column.
- Made the PPCT layout fluid, horizontally scrollable on small screens, and restored the planned column proportions without forced word breaks.
- Split document actions: selecting PPCT/SGK files now only stages them; **Nhận diện PPCT** performs PPCT parsing/recognition, while **Đọc SGK** sends compact SGK context to AI and records the visible “Đã hiểu thông tin SGK” status.
- Added selected, lesson-specific official NLS/AI recommendations and Toán YCCĐ context to the generation prompt. AI codes remain constrained to selected periods.
- Updated smoke and integration coverage for standards loading, the staged actions, SGK status, official code shapes, and idempotent integration-column normalization.

## Latest verification

- `node tests/xaydungphuluc-smoke.js` — PASS
- `node tests/xaydungphuluc-integration-smoke.js` — PASS
- `git diff --check` — PASS

## Changes made

- Updated the PPCT recognition prompt to explicitly accept tab-separated table input and return the required PPCT fields.
- Made `normalizeRecognizedPpct` accept direct arrays and common wrappers (`ppct`, `schedule`, `plan`, `data`, `lessons`, `items`, `rows`, `table`), including Vietnamese and snake_case fields. Header rows are inferred when the provider does not mark them.
- Updated the upload flow to convert DOCX/XLSX tables to TSV before recognition, retaining plain text as fallback. Parsed/AI PPCT rows now become the canonical `sourcePpctRows` and are synchronized into `sourcePpctTable`.
- After recognition, the app initializes fallback Appendix 1 and 3 data, renders Appendix 1 immediately, refreshes the AI picker, and leaves a durable success message plus log entry.
- Added smoke coverage for JSON response variants, PPCT-table synchronization, structured-table recognition input, and preview initialization.
- Removed the superseded duplicate definitions of the upload, normalization, table-rendering, preview, configuration, and DOCX-export functions; each now has one source declaration, retaining the final current implementation and its helpers.

## Verification

- `node tests/xaydungphuluc-smoke.js` — PASS
- `node tests/xaydungphuluc-integration-smoke.js` — PASS
- `git diff --check` — PASS
