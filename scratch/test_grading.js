// Test server-side grading logic in node
const assert = require('assert');

function normalize_short_answer_val(val) {
    let str = String(val || '').toLowerCase().trim();
    str = str.replace(/,/g, '.');
    str = str.replace(/\s+/g, '');
    return str;
}

function compare_short_answers(userVal, trueVal) {
    const u = normalize_short_answer_val(userVal);
    const t = normalize_short_answer_val(trueVal);
    if (!u || !t) return false;
    if (u === t) return true;

    if (!isNaN(Number(u)) && !isNaN(Number(t))) {
        return Math.abs(Number(u) - Number(t)) < 0.0001;
    }

    const eval_frac = (s) => {
        const m = s.match(/^(-?\d+)\/(\d+)$/);
        if (m) {
            const denom = Number(m[2]);
            if (denom !== 0) return Number(m[1]) / denom;
        }
        return null;
    };

    const u_frac = eval_frac(u);
    const t_frac = eval_frac(t);
    const u_num = u_frac !== null ? u_frac : (!isNaN(Number(u)) ? Number(u) : null);
    const t_num = t_frac !== null ? t_frac : (!isNaN(Number(t)) ? Number(t) : null);

    if (u_num !== null && t_num !== null) {
        return Math.abs(u_num - t_num) < 0.0001;
    }

    return false;
}

function score_tf_question(userAnswers, trueAnswers) {
    // trueAnswers: [bool, bool, bool, bool]
    // userAnswers: array of bool or object { 0: bool, 1: bool, ... }
    let correctItems = 0;
    for (let i = 0; i < 4; i++) {
        let uVal = null;
        if (Array.isArray(userAnswers)) {
            uVal = userAnswers[i];
        } else if (userAnswers && typeof userAnswers === 'object') {
            uVal = userAnswers[i] !== undefined ? userAnswers[i] : userAnswers[String(i)];
            if (uVal === undefined) {
                const letters = ['a', 'b', 'c', 'd'];
                uVal = userAnswers[letters[i]];
            }
        }
        if (uVal !== null && uVal !== undefined) {
            const uBool = (uVal === true || uVal === 'true' || uVal === 1 || uVal === '1' || String(uVal).toLowerCase() === 'đ' || String(uVal).toLowerCase() === 't');
            const tBool = !!trueAnswers[i];
            if (uBool === tBool) {
                correctItems++;
            }
        }
    }

    // Quy định chuẩn Bộ GD&ĐT (CV 7991):
    // Đúng 1 ý: 0.1 điểm; Đúng 2 ý: 0.25 điểm; Đúng 3 ý: 0.50 điểm; Đúng 4 ý: 1.00 điểm
    let qScore = 0;
    if (correctItems === 1) qScore = 0.1;
    else if (correctItems === 2) qScore = 0.25;
    else if (correctItems === 3) qScore = 0.50;
    else if (correctItems === 4) qScore = 1.00;

    return { correctItems, qScore };
}

// Test assertions
assert.strictEqual(compare_short_answers('25', '25'), true);
assert.strictEqual(compare_short_answers(' 25 ', '25'), true);
assert.strictEqual(compare_short_answers('0,5', '0.5'), true);
assert.strictEqual(compare_short_answers('1/2', '0.5'), true);
assert.strictEqual(compare_short_answers('3/4', '0.75'), true);
assert.strictEqual(compare_short_answers('-2', '-2.0'), true);
assert.strictEqual(compare_short_answers('25', '26'), false);

assert.deepStrictEqual(score_tf_question([true, false, true, true], [true, false, true, true]), { correctItems: 4, qScore: 1.0 });
assert.deepStrictEqual(score_tf_question([true, true, true, true], [true, false, true, true]), { correctItems: 3, qScore: 0.5 });
assert.deepStrictEqual(score_tf_question([true, true, false, true], [true, false, true, true]), { correctItems: 2, qScore: 0.25 });
assert.deepStrictEqual(score_tf_question([true, true, false, false], [true, false, true, true]), { correctItems: 1, qScore: 0.1 });
assert.deepStrictEqual(score_tf_question([false, true, false, false], [true, false, true, true]), { correctItems: 0, qScore: 0.0 });

console.log('ALL GRADING LOGIC TESTS PASSED!');
