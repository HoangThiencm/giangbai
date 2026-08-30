'use strict';

const assert = require('assert');

class DocxValue { constructor(options) { this.options = options; } }
global.window = {
  docx: {
    Table: DocxValue, TableRow: DocxValue, TableCell: DocxValue, Paragraph: DocxValue, TextRun: DocxValue,
    WidthType: { DXA: 'dxa' }, BorderStyle: { SINGLE: 'single' }, VerticalAlign: { TOP: 'top' }, TableLayoutType: { FIXED: 'fixed' }
  }
};

const { DocxGenerator } = require('../js/khbd-docx.js');
const generator = new DocxGenerator();
const table = generator.createDocxTableFromMarkdown([
  '| Hoạt động của GV và HS | Nội dung |',
  '| :--- | :--- |',
  '| **GV:** Nêu nhiệm vụ | $|-5| = 5$ | Ghi nhớ |'
]);

assert.deepStrictEqual(table.options.columnWidths, [4819, 4820]);
assert.strictEqual(table.options.rows[0].options.children.length, 2, 'Header phải có đúng 2 cột');
assert.strictEqual(table.options.rows[1].options.children.length, 2, 'Dữ liệu phải có đúng 2 cột');
const rightCell = table.options.rows[1].options.children[1];
const rightText = rightCell.options.children.map(p => p.options.children.map(run => run.options.text || '').join('')).join('');
assert.match(rightText, /\|-5\| = 5.*\| Ghi nhớ/, 'Cell thừa phải được gộp vào cột Nội dung');
console.log('khbd-table-columns-smoke: passed');
