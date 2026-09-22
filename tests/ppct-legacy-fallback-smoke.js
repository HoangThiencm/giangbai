"use strict";

const assert = require("assert");
const fs = require("fs");
const path = require("path");

const root = path.join(__dirname, "..");
const mainApi = fs.readFileSync(path.join(root, "api", "khbd_ppct_catalog.php"), "utf8");
const canvasApi = fs.readFileSync(path.join(root, "api", "canvas_ppct_catalog.php"), "utf8");
for (const api of [mainApi, canvasApi]) {
  assert(api.includes("WHERE owner_user_id=? AND subject=? AND grade=? ORDER BY updated_at DESC,id DESC"), "Profiles phải bỏ lọc academic_year.");
  assert(api.includes("AND academic_year=? ORDER BY updated_at DESC,id DESC LIMIT 1"), "Catalog phải ưu tiên bản đúng năm học.");
  assert(api.includes("AND academic_year='' ORDER BY updated_at DESC,id DESC LIMIT 1"), "Catalog phải fallback PPCT cũ chưa đặt năm.");
}

global.window = { addEventListener() {}, removeEventListener() {}, document: {}, lucide: { createIcons() {} } };
const elements = {};
function element(id) { return elements[id] || (elements[id] = { id, value: "", innerHTML: "", textContent: "", checked: false, style: {}, dataset: {}, classList: { add() {}, remove() {}, contains() { return false; }, toggle() {} }, addEventListener() {}, querySelectorAll() { return []; }, querySelector() { return null; }, appendChild() {}, append() {} }); }
global.document = { addEventListener() {}, getElementById: element, querySelectorAll() { return []; }, createElement() { return { textContent: "", innerHTML: "", value: "", appendChild() {}, append() {}, style: {}, classList: { add() {}, remove() {} } }; } };
const storage = {};
global.localStorage = { getItem(key) { return storage[key] || null; }, setItem(key, value) { storage[key] = String(value); }, removeItem(key) { delete storage[key]; } };
global.showToast = () => {}; global.userConfirm = () => true; global.updateProgress = () => {}; global.hideProgress = () => {};

const profilesByGrade = {
  "8": [{ school_name: "Trường A", academic_year: "2026-2027" }],
  "6": [{ school_name: "Trường B", academic_year: "2026-2027" }],
  "9": [{ school_name: "Trường Cũ", academic_year: "" }]
};
const catalogBySchool = {
  "Trường A": { id: 8, academic_year: "2026-2027", title: "PPCT lớp 8" },
  "Trường B": { id: 6, academic_year: "2026-2027", title: "PPCT lớp 6" },
  "Trường Cũ": { id: 2, academic_year: "", title: "PPCT cũ chưa đặt năm" }
};
global.fetch = async url => {
  const params = new URL(String(url), "https://example.test").searchParams;
  const grade = params.get("grade");
  if (!params.has("school_name")) return { ok: true, async json() { return { ok: true, profiles: profilesByGrade[grade] || [] }; } };
  const catalog = catalogBySchool[params.get("school_name") || ""];
  return { ok: true, async json() { return { ok: true, catalog: catalog ? { id: catalog.id, academic_year: catalog.academic_year, rows: [{ id: String(catalog.id), title: catalog.title }], source: {} } : null }; } };
};

const app = require(path.join(root, "js", "khbd-app.js"));
(async () => {
  Object.assign(app.appState, {
    selectedSubject: "toan", selectedGrade: "8", ppctCatalogAcademicYear: "2026-2027",
    ppctSchool: "Trường A", ppctCatalogsBySchool: {},
    ppctCatalog: { rows: [{ id: "8", title: "PPCT lớp 8" }], source: {}, selectedRowId: "", serverId: 8 }
  });
  await app.refreshPpctForChangedGrade();
  assert.strictEqual(app.appState.ppctSchool, "Trường A", "Lớp 8 giữ trường A.");

  app.appState.selectedGrade = "6";
  await app.refreshPpctForChangedGrade();
  assert.strictEqual(app.appState.ppctSchool, "Trường B", "Đổi sang lớp 6 phải tự chọn trường B.");
  assert.strictEqual(app.appState.ppctCatalog.rows[0].title, "PPCT lớp 6", "Lớp 6 phải tải PPCT trường B.");

  app.appState.selectedGrade = "9";
  const legacyProfiles = await app.loadPpctSchoolProfiles();
  assert.deepStrictEqual(legacyProfiles, profilesByGrade["9"], "Hồ sơ PPCT năm rỗng vẫn phải được tìm thấy khi năm hiện hành đã đặt.");
  await app.switchPpctSchool("Trường Cũ");
  assert.strictEqual(app.appState.ppctCatalog.rows[0].title, "PPCT cũ chưa đặt năm", "Catalog phải fallback về bản PPCT năm rỗng cùng trường/môn/khối.");
  console.log("✓ PPCT cũ vẫn tìm thấy và đổi khối tự chọn đúng trường.");
})().catch(error => { console.error(error); process.exitCode = 1; });
