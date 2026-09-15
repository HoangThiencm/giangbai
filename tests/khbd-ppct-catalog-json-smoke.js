const assert = require('assert');
const app = require('../js/khbd-app.js');
assert.deepStrictEqual(app.parseAiJsonSafely('```json\n{"a":"ok"}\n```'), { a: 'ok' });
assert.strictEqual(app.parseAiJsonSafely('{"x":"\\\\cdot"}').x, '\\cdot');
assert.strictEqual(app.parseAiJsonSafely('{"x":"line\\nnext"}').x, 'line\nnext');
assert.strictEqual(app.parseAiJsonSafely('{"x":"a\\q b"}').x, 'a\\q b');
assert.throws(() => app.parseAiJsonSafely('{"x":'), /JSON AI chưa đầy đủ/);
const rows = app.parsePpctCatalog(`| Nội dung | Số tiết | Tuần | NLS | AI |
|---|---|---|---|---|
| Bài 1: Tập hợp | 2 tiết | Tuần 1 | NLS1.1 | AI1.2 |
| Bài 1: Tập hợp | 1 tiết | Tuần 2 | | |`, { subject: 'TOAN', grade: '6' });
assert.strictEqual(rows.length, 2); assert.notStrictEqual(rows[0].id, rows[1].id); assert(rows[0].nls.enabled && rows[0].ai.enabled);
console.log('PASS khbd ppct catalog/json smoke');
