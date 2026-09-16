"use strict";

const assert = require("assert");
const fs = require("fs");
const path = require("path");
const { clipKhbdActivityMarkdown } = require("../js/khbd-app.js");

const source = [
  "## B. HOẠT ĐỘNG 2: HÌNH THÀNH KIẾN THỨC MỚI (45 phút)",
  "",
  "### Hoạt động 2.1: 1. PHÉP NHÂN SỐ TỰ NHIÊN (23 phút)",
  "#### a) Mục tiêu",
  "- Học sinh thực hiện phép nhân số tự nhiên.",
  "#### d) Tổ chức thực hiện",
  "- GV hướng dẫn, HS thực hành phép nhân.",
  "",
  "### Hoạt động 2.2: 2. PHÉP CHIA HẾT VÀ PHÉP CHIA CÓ DƯ (22 phút)",
  "#### a) Mục tiêu",
  "- Học sinh thực hiện phép chia có dư.",
  "#### d) Tổ chức thực hiện",
  "- GV hướng dẫn, HS thực hành phép chia.",
  "",
  "## C. HOẠT ĐỘNG 3: LUYỆN TẬP (15 phút)",
  "- Luyện tập củng cố."
].join("\n");

const clipped = clipKhbdActivityMarkdown("B", source, { subsectionCount: 2 });
assert.match(clipped, /Hoạt động 2\.1/i, "must preserve Activity 2.1");
assert.match(clipped, /Hoạt động 2\.2/i, "must preserve Activity 2.2");
assert.match(clipped, /PHÉP NHÂN SỐ TỰ NHIÊN/i, "must preserve first branch content");
assert.match(clipped, /PHÉP CHIA HẾT VÀ PHÉP CHIA CÓ DƯ/i, "must preserve second branch content");
assert.doesNotMatch(clipped, /HOẠT ĐỘNG 3: LUYỆN TẬP/i, "must stop before the next activity");
assert.ok(clipped.length > 350, "must not truncate the multi-branch activity");

const root = path.resolve(__dirname, "..");
for (const rel of ["canvas_soankhbd.html", path.join("backupcode viettailieu", "canvas_soankhbd.html")]) {
  const html = fs.readFileSync(path.join(root, rel), "utf8");
  assert.match(html, /20260916-textbook-exact-v18/, rel + " uses v18 cache busting");
}

console.log("canvas-activity-b-multi-branches-smoke: OK");
