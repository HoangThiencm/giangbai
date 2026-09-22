"use strict";

const assert = require("assert");
const fs = require("fs");
const path = require("path");

const root = path.join(__dirname, "..");
const appFile = path.join(root, "js", "khbd-app.js");
const mainApi = fs.readFileSync(path.join(root, "api", "khbd_ppct_catalog.php"), "utf8");
const canvasApi = fs.readFileSync(path.join(root, "api", "canvas_ppct_catalog.php"), "utf8");
for (const source of [mainApi, canvasApi]) {
  assert(source.includes("school_name VARCHAR(150) NOT NULL DEFAULT ''"), "Migration phải thêm school_name tương thích PPCT cũ.");
  assert(source.includes("owner_user_id,subject,grade,academic_year,school_name"), "Unique key/lưu PPCT phải bao gồm school_name.");
  assert(source.includes("$method==='DELETE'") || source.includes("$method === 'DELETE'"), "API phải hỗ trợ xóa profile.");
  assert(source.includes("'profiles'"), "GET thiếu school_name phải trả danh sách profiles.");
}

global.window = { addEventListener() {}, removeEventListener() {}, document: {}, lucide: { createIcons() {} } };
const elements = {};
function element(id) { return elements[id] || (elements[id] = { id, value: "", innerHTML: "", textContent: "", checked: false, style: {}, dataset: {}, classList: { add() {}, remove() {}, contains() { return false; }, toggle() {} }, addEventListener() {}, querySelectorAll() { return []; }, querySelector() { return null; }, appendChild() {}, append() {} }); }
global.document = { addEventListener() {}, getElementById: element, querySelectorAll() { return []; }, createElement() { return { textContent: "", innerHTML: "", value: "", appendChild() {}, append() {}, style: {}, classList: { add() {}, remove() {} } }; } };
const storage = {};
global.localStorage = { getItem(key) { return storage[key] || null; }, setItem(key, value) { storage[key] = String(value); }, removeItem(key) { delete storage[key]; } };
global.showToast = () => {}; global.userConfirm = () => true; global.updateProgress = () => {}; global.hideProgress = () => {};

const server = {
  "THCS Trường A": [{ id: "a-1", title: "Bài thuộc Trường A" }],
  "THCS Trường B": [{ id: "b-1", title: "Bài thuộc Trường B" }]
};
global.fetch = async url => {
  const params = new URL(String(url), "https://example.test").searchParams;
  if (!params.has("school_name")) return { ok: true, async json() { return { ok: true, profiles: [{ school_name: "THCS Trường A", academic_year: "2026-2027" }, { school_name: "THCS Trường B", academic_year: "2026-2027" }] }; } };
  const school = params.get("school_name") || "";
  return { ok: true, async json() { return { ok: true, catalog: { id: school === "THCS Trường A" ? 1 : 2, academic_year: "2026-2027", rows: server[school] || [], source: {} } }; } };
};

const app = require(appFile);
app.appState.selectedSubject = "toan";
app.appState.selectedGrade = "6";
app.appState.ppctCatalogAcademicYear = "2026-2027";
app.appState.ppctSchool = "THCS Trường A";
app.appState.ppctCatalogsBySchool = {};
app.appState.ppctCatalog = { rows: server["THCS Trường A"], source: {}, selectedRowId: "", serverId: 1 };
app.ppctStoreActiveCatalog();

(async () => {
  app.appState.ppctSchool = "";
  app.appState.ppctCatalog = { rows: [], source: {}, selectedRowId: "", serverId: null };
  app.appState.ppctCatalogsBySchool = {};
  await app.refreshPpctSchoolControls();
  assert.strictEqual(app.appState.ppctSchool, "THCS Trường A", "Khi chưa chọn trường và không có cache cũ, phải chọn profile đầu tiên.");
  app.appState.ppctSchool = "";
  app.appState.ppctCatalog = { rows: [{ id: "legacy", title: "PPCT chưa đặt tên" }], source: {}, selectedRowId: "", serverId: null };
  app.appState.ppctCatalogsBySchool = { "": app.appState.ppctCatalog };
  await app.refreshPpctSchoolControls();
  assert.strictEqual(app.appState.ppctSchool, "", "Cache PPCT chưa đặt tên có dữ liệu không được ghi đè bởi profile đầu tiên.");
  await app.switchPpctSchool("THCS Trường A");
  await app.switchPpctSchool("THCS Trường B");
  assert.strictEqual(app.appState.ppctCatalog.rows[0].title, "Bài thuộc Trường B", "Chuyển Trường B phải nạp đúng PPCT B.");
  assert.strictEqual(app.appState.ppctCatalogsBySchool["THCS Trường A"].rows[0].title, "Bài thuộc Trường A", "PPCT A không được bị ghi đè.");
  await app.switchPpctSchool("THCS Trường A");
  assert.strictEqual(app.appState.ppctCatalog.rows[0].title, "Bài thuộc Trường A", "Chuyển lại Trường A phải phục hồi PPCT A.");
  assert.strictEqual(app.ppctCatalogMeta().school_name, "THCS Trường A", "Fetch/lưu phải mang school_name đang chọn.");
  console.log("✓ PPCT nhiều trường giữ riêng dữ liệu và chuyển hồ sơ đúng.");
})().catch(error => { console.error(error); process.exitCode = 1; });
