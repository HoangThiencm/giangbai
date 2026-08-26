'use strict';
const assert = require('assert');
const { unwrapVietnameseMathForKatex } = require('../js/khbd-app.js');

const texted = unwrapVietnameseMathForKatex('Cho $\\text{từ}$ thuộc $A$.');
assert.ok(texted.includes('từ'), 'Kéo chữ Việt ra khỏi \\text{}: ' + texted);
assert.ok(!/\\text\{từ\}/.test(texted), 'Không giữ \\text{từ}: ' + texted);
assert.ok(texted.includes('$A$'), 'Giữ $A$: ' + texted);

const wrapped = unwrapVietnameseMathForKatex('Tập $từ$ và $x \\in A$.');
assert.ok(wrapped.includes('từ'), 'Bỏ $...$ quanh chữ Việt thuần: ' + wrapped);
assert.ok(wrapped.includes('$x \\in A$'), 'Giữ công thức toán: ' + wrapped);

const mixed = unwrapVietnameseMathForKatex('$$\\text{với } x \\in A$$');
assert.ok(mixed.includes('với'), 'Kéo "với" ra khỏi display math: ' + mixed);
assert.ok(/\$\$?x \\in A\$\$?/.test(mixed), 'Giữ x \\in A trong math: ' + mixed);

const plain = unwrapVietnameseMathForKatex('Cho $x^2+1=0$ và tập hợp.');
assert.strictEqual(plain, 'Cho $x^2+1=0$ và tập hợp.');

console.log('khbd-katex-vn-smoke: passed');
console.log('texted=', JSON.stringify(texted));
console.log('wrapped=', JSON.stringify(wrapped));
console.log('mixed=', JSON.stringify(mixed));
