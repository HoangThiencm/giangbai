"use strict";

const assert = require("assert");
const fs = require("fs");
const path = require("path");
const vm = require("vm");

const root = path.resolve(__dirname, "..");
const pages = ["canvas_soankhbd.html", path.join("backupcode viettailieu", "canvas_soankhbd.html")];

function bootstrapSource(html) {
  const markers = ["function bootstrapCanvasCoreModules()", "function installCurriculumFallback()", "function fallbackCurriculum()"];
  const functionStart = markers.map((marker) => html.indexOf(marker)).find((index) => index >= 0);
  const scriptStart = functionStart >= 0 ? html.lastIndexOf("<script", functionStart) : -1;
  const codeStart = scriptStart >= 0 ? html.indexOf("\n", scriptStart) + 1 : -1;
  const end = codeStart >= 0 ? html.indexOf("\n  </script>", codeStart) : -1;
  assert.ok(codeStart >= 0 && end > codeStart, "must contain Canvas core bootstrap");
  return html.slice(codeStart, end);
}

async function runBootstrap(source, normal) {
  const window = { __KHBD_CANVAS__: { host: "https://example.test" } };
  const document = {
    createElement() { return {}; },
    head: { appendChild(node) {
      if (normal) {
        if (node.src.includes("curriculum")) {
          window.CURRICULUM_DATA = { subjects: [{ id: "toan", name: "Toán", grades: [6] }] };
          window.getGradeLevel = (grade) => Number(grade) <= 5 ? "tieu-hoc" : Number(grade) <= 9 ? "thcs" : "thpt";
          window.getGradeLevelName = (grade) => Number(grade) <= 5 ? "Tiểu học" : Number(grade) <= 9 ? "THCS" : "THPT";
        } else if (node.src.includes("standards")) window.KHBD_STANDARDS = {};
        else if (node.src.includes("yccd")) window.KHBD_YCCD = {};
        else if (node.src.includes("ai-design-config")) window.AiDesignConfig = {};
      }
      node.onload(); // HTTP 200 with no script body still leaves globals absent.
    } }
  };
  const context = { window, document, Promise, setTimeout() { return 1; }, clearTimeout() {}, console };
  vm.createContext(context);
  vm.runInContext(source, context, { timeout: 1000 });
  await window.__KHBD_CANVAS_CORE_READY__;
  return window;
}

(async () => {
  for (const rel of pages) {
    const html = fs.readFileSync(path.join(root, rel), "utf8");
    assert.match(html, /20260916-canvas-module-v9/, `${rel} uses v9 cache busting`);
    assert.match(html, /Không tải được danh mục chương trình từ host; đang dùng danh mục dự phòng/, `${rel} distinguishes fallback banner`);
    assert.match(html, /khbd-curriculum\.js/, `${rel} loads curriculum through the v9 loader`);
    assert.match(html, /[?]v[=]"?\s*[+]\s*(?:version|v)/, `${rel} appends a uniform version to module URLs`);
    assert.match(html, /khbd-standards\.js/, `${rel} loads standards defensively`);
    assert.match(html, /khbd-yccd\.js/, `${rel} loads yccd defensively`);
    assert.match(html, /ai-design-config\.js/, `${rel} loads config defensively`);

    const absent = await runBootstrap(bootstrapSource(html), false);
    assert.strictEqual(absent.__KHBD_CANVAS__.moduleFallback.curriculum, true, `${rel} detects empty curriculum response`);
    assert.ok(absent.getSubjectsForGrade(6).length >= 17, `${rel} fallback supplies supported Grade 6 subjects`);
    assert.ok(absent.getLessonsForBook("toan", "standard", 6).some((chapter) => chapter.items.some((x) => /Bài 5/.test(x))), `${rel} fallback makes Grade 6 lesson selectable`);
    assert.strictEqual(absent.getGradeLevel(6), "thcs", `${rel} fallback supplies the lower-secondary grade code`);
    assert.strictEqual(absent.getGradeLevelName(10), "THPT", `${rel} fallback supplies the upper-secondary grade label`);

    const normal = await runBootstrap(bootstrapSource(html), true);
    assert.ok(!normal.__KHBD_CANVAS__.moduleFallback.curriculum, `${rel} preserves normal curriculum module`);
    assert.strictEqual(normal.getGradeLevel(6), "thcs", `${rel} preserves normal curriculum grade helper`);
    assert.strictEqual(normal.getGradeLevelName(10), "THPT", `${rel} preserves normal curriculum grade label helper`);
  }
  console.log("canvas-module-fallback-smoke: OK");
})().catch((error) => { console.error(error); process.exitCode = 1; });
