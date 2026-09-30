"use strict";

const assert = require("assert");
const fs = require("fs");
const path = require("path");

const templatePath = path.resolve(__dirname, "../TROLYTHIEN/10_BAI_GIANG_HTML/templates/master_lecture_template.html");
assert.ok(fs.existsSync(templatePath), "File master_lecture_template.html phai ton tai");

const html = fs.readFileSync(templatePath, "utf8");
console.log("Total chars:", html.length);
console.log("Total lines:", html.split("\n").length);

assert.ok(html.includes("MathJax"), "Phai co MathJax");
assert.ok(html.includes("--primary") && html.includes(".slide-deck"), "Phai co bo style CSS day du");
assert.ok(html.includes('id="controlBar"'), "Phai co thanh control bar");
assert.ok(html.includes('id="editModal"'), "Phai co edit modal");
assert.ok(html.includes("image-lightbox-dialog") && html.includes("zoomLightbox"), "Phai co tinh nang Lightbox Zoom Va 22");
assert.ok(html.includes("speechSynthesis") && html.includes("toggleReadSlideEn"), "Phai co tinh nang doc TTS");

const slideCount = (html.match(/class=["'][^"']*slide-item/g) || []).length;
console.log("Found sample slides:", slideCount);
assert.strictEqual(slideCount, 9, "Template phai co dung 9 slide mau mau muc");

console.log("master_lecture_template validation: PASS");
