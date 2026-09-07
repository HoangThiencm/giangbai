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

const systemWithVietnamese = String.raw`Giải $\begin{cases}x+y=5 & \text{ (quả)} \\ x-y=1\end{cases}$`;
const preservedSystem = unwrapVietnameseMathForKatex(systemWithVietnamese);
assert.strictEqual(preservedSystem, systemWithVietnamese, 'Hệ phương trình có tiếng Việt phải giữ nguyên khối: ' + preservedSystem);

const leftBraceSystem = String.raw`Giải $\left\{x+y=5 \\ x-y=1\right.$`;
assert.strictEqual(unwrapVietnameseMathForKatex(leftBraceSystem), leftBraceSystem, 'Hệ \\left\\{ phải giữ nguyên khối');

console.log('khbd-katex-vn-smoke: passed');
console.log('texted=', JSON.stringify(texted));
console.log('wrapped=', JSON.stringify(wrapped));
console.log('mixed=', JSON.stringify(mixed));
