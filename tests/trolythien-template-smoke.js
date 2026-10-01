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
assert.ok(html.includes("PageDown") && html.includes("PageUp") && html.includes("ArrowDown") && html.includes("ArrowUp") && html.includes("Backspace"), "Phai ho tro phim but trinh chieu");
assert.ok(html.includes("blank-screen") && html.includes("toggleBlankScreen"), "Phai co man hinh den");
assert.ok(html.includes(".blur()") && html.includes("zoomableFigure"), "Phai blur thanh dieu khien va delegation zoom");
assert.ok(html.includes(".image-lightbox-backdrop, svg, img, .figure-box, [data-zoomable]"), "Click anh/SVG khong duoc goi nextStep");
assert.ok(html.includes('data-step="1"') && html.includes('data-step="2"') && html.includes('data-step="3"') && html.includes('data-step="4"'), "Template phai co dan dat 4 buoc");
assert.ok(html.includes("Gợi ý / Dẫn dắt") && html.includes("Đáp số"), "Slide mau phai tach goi y va dap so");

function columnStepSets(slideHtml) {
  const parts = slideHtml.split(/<div class="col-board"/);
  return parts.slice(1).map(part => {
    const chunk = part.split(/<div class="col-board\b/)[0];
    const steps = new Set();
    const re = /<div class="content-block\b[^>]*>/g;
    let m;
    while ((m = re.exec(chunk))) {
      const step = (m[0].match(/data-step="(\d+)"/) || [])[1];
      if (step && step !== "0") steps.add(step);
    }
    return steps;
  });
}

const templateSlides = html.split(/<section class="slide-item\b/).slice(1);
templateSlides.forEach((slide, i) => {
  const sets = columnStepSets(slide);
  for (let a = 0; a < sets.length; a++) {
    for (let b = a + 1; b < sets.length; b++) {
      for (const step of sets[a]) {
        assert.ok(!sets[b].has(step), "Slide mau " + (i + 1) + " trung data-step=" + step + " o hai cot");
      }
    }
  }
});
assert.ok(html.includes('data-step="1"') && html.includes("<svg"), "Buoc 1 template co hinh SVG");
assert.ok(html.includes('id="laserPointer"') && html.includes('id="drawCanvas"'), "Phai co laser va canvas ve");
assert.ok(html.includes("toggleLaserMode") && html.includes("togglePenMode") && html.includes("clearDrawCanvas"), "Phai co ham laser va but ve");
assert.ok(html.includes("e.key === 'l' || e.key === 'L'") && html.includes("e.key === 'p' || e.key === 'P'"), "Phai co phim tat L va P");
assert.ok(html.includes("document.body.classList.contains('laser-mode')) return;"), "Laser mode khong duoc click nextStep");
assert.ok(html.includes("getSweetVietnameseVoice") && html.includes("speakBlockVi") && html.includes("HoaiMy"), "Chi doc tieng Viet bang giong Natural");
assert.ok(html.includes("function playAudioOrSpeech") && html.includes("audio/slide-"), "Phai phat mp3 Hoai My truoc khi doc speech");
assert.ok(html.includes('data-step="0"'), "Cot ghi bang co khoi cot loi luon hien");
assert.ok(html.includes("speechSynthesis") && html.includes("toggleReadSlideEn"), "Phai co tinh nang doc TTS");
assert.ok(html.includes('id="blackboardOverlay"') && html.includes("function toggleBlackboard") && html.includes("function jumpToPeriod"), "Phai co bang viet va nhay tiet");
assert.ok(html.includes("speakBlockAuto") && html.includes("e.key === 'w' || e.key === 'W'"), "Phai co loa song ngu va phim W");
assert.ok(html.includes("body.pen-mode, body.pen-mode .slide-deck") && html.includes("overflow: hidden"), "But ve khoa cuon");
assert.ok(!html.includes('id="btnHelpCaption"'), "Khong con nut tat phu de");
assert.ok(html.includes("jumpToPeriod(1)") && html.includes("jumpToPeriod(2)") && html.includes("jumpToPeriod(3)"), "Co nut Tiet 1, 2, 3");
assert.ok(html.includes("e.shiftKey") && html.includes("16"), "Shift ve thang va tiet 3 toi slide 16");

const slideCount = (html.match(/class=["'][^"']*slide-item/g) || []).length;
console.log("Found sample slides:", slideCount);
assert.strictEqual(slideCount, 9, "Template phai co dung 9 slide mau mau muc");

console.log("master_lecture_template validation: PASS");
