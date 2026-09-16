'use strict';

const assert = require('assert');
const fs = require('fs');
const path = require('path');

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

assert.deepStrictEqual(table.options.columnWidths, [6426, 3213]);
const styles = fs.readFileSync(path.join(__dirname, '..', 'css', 'khbd-styles.css'), 'utf8');
assert.match(styles, /th:first-child:nth-last-child\(2\)[\s\S]*?width:\s*66\.67%/, 'Preview left column must be 66.67%');
assert.match(styles, /th:last-child:nth-child\(2\)[\s\S]*?width:\s*33\.33%/, 'Preview right column must be 33.33%');
assert.strictEqual(table.options.rows[0].options.children.length, 2, 'Header phải có đúng 2 cột');
assert.strictEqual(table.options.rows[1].options.children.length, 2, 'Dữ liệu phải có đúng 2 cột');
const rightCell = table.options.rows[1].options.children[1];
const rightText = rightCell.options.children.map(p => p.options.children.map(run => run.options.text || '').join('')).join('');
assert.match(rightText, /\|-5\| = 5.*\| Ghi nhớ/, 'Cell thừa phải được gộp vào cột Nội dung');
console.log('khbd-table-columns-smoke: passed');
