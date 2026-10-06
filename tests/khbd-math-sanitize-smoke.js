/**
 * Smoke: chuẩn hoá chia hết và đối chiếu 8 KHBD mẫu.
 */
const fs = require("fs");
const path = require("path");
const assert = require("assert");
const { sanitizeKhbdMathSource } = require("../TROLYTHIEN/engine/export_khbd_engine.js");

const samples = [
  ["$36 \\vdots x$", "\\vdots"],
  ["$48 \\dots x$", "\\vdots"],
  ["100 - x \\dots 4", "\\vdots"],
  ["a \\not\\vdots b", "\\nmid"],
  ["\\frac{24}{108}", "\\frac"],
  ["$rac{24}{108}$", "\\frac"],
  ["frac{80}{140}", "\\frac"],
  ["36 \u000bdots x", "\\vdots"],
  ["\u000crac{24}{108}", "\\frac"],
  ["\\ \\vdots \\ ", "\\vdots"]
];

for (const [input, expect] of samples) {
  const out = sanitizeKhbdMathSource(input);
  assert.ok(out.includes(expect), `${JSON.stringify(input)} -> ${JSON.stringify(out)} missing ${expect}`);
  assert.ok(!/[\u0000-\u0008\u000b\u000c\u000e-\u001f]/.test(out), "control char left in " + JSON.stringify(out));
  assert.ok(!/\bdots\b/.test(out), "dots left in " + JSON.stringify(out));
  assert.ok(!/\\v\s*\\vdots|\\v\b/.test(out), "rogue \\v left in " + JSON.stringify(out));
}

const dir = fs.existsSync(path.resolve("tools/TROLYTHIEN/1_SOAN_KHBD/Ket_qua"))
  ? path.resolve("tools/TROLYTHIEN/1_SOAN_KHBD/Ket_qua")
  : path.resolve("TROLYTHIEN/1_SOAN_KHBD/Ket_qua");
const files = fs.readdirSync(dir).filter(name => /^KHBD_0[1-8]_.*\.md$/.test(name)).sort();
const withIntegration = new Set(["03", "04", "08"]);
const withMindmap = new Set(["01", "02", "06"]);
for (const name of files) {
  const id = name.slice(5, 7);
  const text = fs.readFileSync(path.join(dir, name), "utf8");
  const hasNls = text.includes("***(Tích hợp NLS");
  const hasAi = text.includes("***(Tích hợp AI");
  assert.strictEqual(hasNls, withIntegration.has(id), name + " NLS");
  assert.strictEqual(hasAi, withIntegration.has(id), name + " AI");
  const images = text.match(/!\[[^\]]*\]\([^)]+\)/g) || [];
  if (withMindmap.has(id)) {
    assert.ok(images.length === 1 && /mindmap-0[126]/.test(images[0]), name + " mindmap");
    assert.ok(/Hoạt động 2\.1/.test(text), name + " activity 2.1");
  } else if (id === "05") {
    assert.ok(images.length === 1 && /hinh-05-so-do-phan-tich/.test(images[0]), name + " prime diagram");
  } else {
    assert.strictEqual(images.length, 0, name + " extra image");
  }
}

console.log("khbd-math-sanitize-smoke: PASS");
