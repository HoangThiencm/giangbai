'use strict';

const assert = require('assert');
const fs = require('fs');
const vm = require('vm');

const source = fs.readFileSync('js/khbd-app.js', 'utf8');
const match = source.match(/function ppctRowCodes\(row, kind\) \{[\s\S]*?\n\}/);
assert(match, 'Không tìm thấy hàm ppctRowCodes.');

const sandbox = {};
vm.createContext(sandbox);
vm.runInContext(`${match[0]}; this.ppctRowCodes = ppctRowCodes;`, sandbox);

const row = {
  nls: { codes: ['1.2.TC1a'] },
  digital_competency: ['1.2.TC1a'],
  ai: { codes: ['6.A1.1'] },
  ai_competency: ['6.A1.1']
};

assert.deepStrictEqual(Array.from(sandbox.ppctRowCodes(row, 'nls')), ['1.2.TC1a']);
assert.deepStrictEqual(Array.from(sandbox.ppctRowCodes(row, 'ai')), ['6.A1.1']);
console.log('PASS PPCT dedupe smoke');
