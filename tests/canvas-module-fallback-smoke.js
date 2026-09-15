"use strict";

const assert = require("assert");
const fs = require("fs");
const path = require("path");
const vm = require("vm");

const root = path.resolve(__dirname, "..");
const pages = ["canvas_soankhbd.html", path.join("backupcode viettailieu", "canvas_soankhbd.html")];

function bootstrapSource(html) {
  const marker = "<script>\n  (function bootstrapCanvasCoreModules()";
  const start = html.indexOf(marker);
  const fallbackStart = html.indexOf("<script>\n  (function () {", html.indexOf("Core data modules"));
  const actualStart = start >= 0 ? start : fallbackStart;
  const end = html.indexOf("\n  </script>", actualStart);
  assert.ok(actualStart >= 0 && end > actualStart, "must contain Canvas core bootstrap");
  return html.slice(html.indexOf("\n", actualStart) + 1, end);
}

async function runBootstrap(source, normal) {
  const window = { __KHBD_CANVAS__: { host: "https://example.test" } };
  const document = {
    createElement() { return {}; },
    head: { appendChild(node) {
      if (normal) {
        if (node.src.includes("curriculum")) {
          window.CURRICULUM_DATA = { subjects: [{ id: "toan", name: "Toán", grades: [6] }] };
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
    assert.match(html, /20260916-canvas-module-v8/, `${rel} uses v8 cache busting`);
    assert.match(html, /Không tải được danh mục chương trình từ host; đang dùng danh mục dự phòng/, `${rel} distinguishes fallback banner`);
    assert.match(html, /khbd-curriculum\.js/, `${rel} loads curriculum through the v8 loader`);
    assert.match(html, /[?]v[=]"?\s*[+]\s*(?:version|v)/, `${rel} appends a uniform version to module URLs`);
    assert.match(html, /khbd-standards\.js/, `${rel} loads standards defensively`);
    assert.match(html, /khbd-yccd\.js/, `${rel} loads yccd defensively`);
    assert.match(html, /ai-design-config\.js/, `${rel} loads config defensively`);

    const absent = await runBootstrap(bootstrapSource(html), false);
    assert.strictEqual(absent.__KHBD_CANVAS__.moduleFallback.curriculum, true, `${rel} detects empty curriculum response`);
    assert.ok(absent.getSubjectsForGrade(6).length >= 17, `${rel} fallback supplies supported Grade 6 subjects`);
    assert.ok(absent.getLessonsForBook("toan", "standard", 6).some((chapter) => chapter.items.some((x) => /Bài 5/.test(x))), `${rel} fallback makes Grade 6 lesson selectable`);

    const normal = await runBootstrap(bootstrapSource(html), true);
    assert.ok(!normal.__KHBD_CANVAS__.moduleFallback.curriculum, `${rel} preserves normal curriculum module`);
  }
  console.log("canvas-module-fallback-smoke: OK");
})().catch((error) => { console.error(error); process.exitCode = 1; });
