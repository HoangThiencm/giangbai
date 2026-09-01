# IMPLEMENT: PPCT recognition and preview synchronization

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
