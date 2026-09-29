const fs = require('node:fs');
const path = require('node:path');
const assert = require('node:assert/strict');
const vm = require('node:vm');

const root = path.join(__dirname, '..');
const read = name => fs.readFileSync(path.join(root, name), 'utf8');
const hub = read('vanban-hub.js');
const app = read('vanban-app.js');
const php = read('api/vanban.php');
const access = read('access-control.js');
const hubPage = read('quanlyvanban.html');
const adminPage = read('quanlyvanban-hanhchinh.html');
const majorPage = read('quanlyvanban-chuyenmon.html');

assert.match(access, /'quanlyvanban-chuyenmon\.html': 'quanlyvanban'/);
assert.match(hub, /chuyenmon:\s*\{\s*label:\s*'Chuyên môn',\s*icon:\s*'fa-graduation-cap',\s*accent:\s*'indigo',\s*page:\s*'quanlyvanban-chuyenmon\.html'\s*\}/);
assert.match(hub, /doc\.sector === 'dang' \|\| doc\.sector === 'chuyenmon'/);
assert.match(hubPage, /lg:grid-cols-3/);
assert.match(hubPage, /Chuyên môn/);

assert.match(php, /return in_array\(\$value, \['hanhchinh', 'dang', 'chuyenmon'\], true\)/);
assert.match(php, /if \(\$sector === 'chuyenmon'\) return 'Chuyên môn';/);
assert.match(php, /if \(\$sector === 'chuyenmon'\) return 'CHUYEN_MON';/);
assert.match(php, /if \(\$action === 'transfer_sector' \|\| \$action === 'copy_sector'\)/);
assert.match(php, /owner_id = \? AND id IN/);
assert.match(php, /vbd_copy_document_files/);
assert.match(php, /function vbd_latest_signature_date/);
assert.match(php, /function vbd_find_document_number/);
assert.match(php, /QĐ\|QD\|KH/);

const skipBlock = php.match(/\$skipKeywords = \[([\s\S]*?)\];/);
assert.ok(skipBlock, 'phải còn danh sách dòng bỏ qua');
assert.doesNotMatch(skipBlock[1], /ngày ký|ký số|thời gian ký/);
assert.match(php, /empty\(\$result\['document_date'\]\) && \$signatureDate/);

assert.match(majorPage, /window\.VANBAN_SECTOR = 'chuyenmon'/);
assert.match(majorPage, /vanban-app\.js/);
assert.match(majorPage, /id="documentList"/);
assert.match(majorPage, /id="documentDetailModal"/);
assert.match(majorPage, /id="sourceText"/);
assert.match(majorPage, /id="documentNumber"/);
assert.match(majorPage, /id="documentDate"/);
assert.match(majorPage, /id="pasteClipboardBtn"/);
assert.match(majorPage, /Dán nhanh từ Clipboard/);
assert.match(majorPage, /Chuyên môn/);
assert.match(majorPage, /indigo/);

assert.match(adminPage, /id="sectorBulkBar"/);
assert.match(adminPage, /Chuyển đã chọn sang Chuyên môn/);
assert.match(adminPage, /Sao chép đã chọn sang Chuyên môn/);
assert.match(adminPage, /id="pasteClipboardBtn"/);
assert.match(app, /data-select-id/);
assert.match(app, /Chuyển sang Chuyên môn/);
assert.match(app, /Sao chép sang Chuyên môn/);
assert.match(app, /transfer_sector/);
assert.match(app, /copy_sector/);
assert.match(app, /getAnnotations\(/);
assert.match(app, /\/Type\s*\/Sig/);
assert.match(app, /pdf\.numPages > headCount/);
assert.match(app, /target_sector: 'chuyenmon'/);

const start = app.indexOf('/* vbd-parse-export:start */');
const end = app.indexOf('/* vbd-parse-export:end */');
assert.ok(start >= 0 && end > start, 'khối nhận diện phải tách được để kiểm thử');
const context = vm.createContext({ window: {}, globalThis: {}, TextDecoder, Uint8Array, TextEncoder });
context.globalThis = context;
vm.runInContext(app.slice(start, end), context);
const api = context.window.VanbanParse;
assert.equal(typeof api.extractDocumentFields, 'function');

assert.equal(api.parsePdfSignatureDate('D:20260925103015+07\'00\''), '2026-09-25');
assert.equal(api.parsePdfSignatureDate('/M (D:20260926093015+07\'00\')'), '2026-09-26');
assert.equal(api.parsePdfSignatureDate('không có ngày'), '');

const signedPdf = `%PDF-1.7
<< /Type /Sig /Filter /Adobe.PPKLite /Name (Chuyen vien) /M (D:20260920120000+07'00') >>
<< /Type /Sig /Filter /Adobe.PPKLite /Name (Hieu truong) /M (D:20260925103015+07'00') >>
`;
const signatures = api.extractPdfSignaturesFromBytes(Buffer.from(signedPdf, 'latin1'));
assert.equal(signatures.length, 2);
const block = api.formatSignatureBlock(signatures);
assert.match(block, /Ngày ký: 25\/09\/2026/);
assert.match(block, /Ký số: Hieu truong/);
assert.doesNotMatch(block, /20\/09\/2026/);

const withHeader = `
ỦY BAN NHÂN DÂN PHƯỜNG
Số: 123/QĐ-UBND
V/v Ban hành kế hoạch chuyên môn năm học
Hồ Nai, ngày 01 tháng 09 năm 2026
Ngày ký: 26/09/2026 09:30:15
`;
const headerFields = api.extractDocumentFields(withHeader);
assert.equal(headerFields.document_number, '123/QĐ-UBND');
assert.equal(headerFields.document_date, '2026-09-01');
assert.match(headerFields.title, /Ban hành kế hoạch chuyên môn/);
assert.match(headerFields.summary_text, /Ban hành kế hoạch chuyên môn/);

const signedOnly = `
Số: 45 / QĐ - SGDĐT
V/v Triển khai chuyên môn tháng chín
Ngày ký: 26/09/2026 09:30:15
Ký số: Hiệu trưởng
`;
const signedFields = api.extractDocumentFields(signedOnly);
assert.equal(signedFields.document_number, '45/QĐ-SGDĐT');
assert.equal(signedFields.document_date, '2026-09-26');
assert.match(signedFields.title, /Triển khai chuyên môn/);

const planNumber = api.extractDocumentFields('Số: 12/KH-THCS\nVề việc Sinh hoạt chuyên môn tổ khoa học\n');
assert.equal(planNumber.document_number, '12/KH-THCS');
assert.match(planNumber.title, /Sinh hoạt chuyên môn/);

const newest = api.extractDocumentFields('Ngày ký: 20/09/2026 08:00:00\nThời gian ký: 26/09/2026 09:30:15\n');
assert.equal(newest.document_date, '2026-09-26');

console.log('PASS: lĩnh vực Chuyên môn, chuyển/sao chép văn bản, số quyết định và ngày ký số.');
