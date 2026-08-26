/**
 * js/khbd-app.js
 * Quản lý logic giao diện, luồng dữ liệu, tương tác người dùng,
 * Dán/Kéo thả ảnh SGK, Render KaTeX trực quan, Tự động hóa 1-Click
 * và Tích hợp xuất Word .docx hoàn chỉnh.
 * Soạn KHBD môn Toán THCS theo SGK do giáo viên cung cấp.
 */

// STATE TOÀN CỤC CỦA ỨNG DỤNG
const appState = {
  selectedGrade: "6",
  selectedSubject: "TOAN",
  selectedLesson: "",
  customTopic: "",
  school: "TRƯỜNG THCS NGUYỄN DU",
  group: "TỔ TOÁN - TIN HỌC",
  teacher: "Giáo viên Môn Toán",
  subject: "TOÁN",
  duration: "02 tiết (90 phút)",
  teachingContext: {
    classProfile: "",
    supportNeeds: "",
    integrations: { digital: false, ai: false, foreignLanguage: false, inclusive: false },
    methods: [],
    techniques: [],
    specialRequirements: ""
  },
  
  // Danh sách ảnh SGK (Mảng phẳng trực quan)
  images: [],

  // Nội dung đã biên soạn
  content: {
    vision: "",
    objectives: "",
    materials: "",
    activities: {
      A: "",
      B: "",
      C: "",
      D: "",
      E: "",
      F: "",
      G: ""
    }
  },

  activeTab: "tabVision",
  activeActSubtab: "A",
  isGenerating: false,
  cancelRequested: false,
  generationController: null
};

const MAX_IMAGES = 10;
const MAX_IMAGE_BYTES = 5 * 1024 * 1024;
const MAX_TOTAL_IMAGE_BYTES = 25 * 1024 * 1024;
const ALLOWED_IMAGE_TYPES = new Set(["image/jpeg", "image/png", "image/webp", "image/gif"]);

// Biến lưu trữ tài liệu PDF tạm thời
let currentPdfFile = null;
let currentPdfDoc = null;

// CÁC TÊN TIÊU ĐỀ HOẠT ĐỘNG
const ACTIVITY_TITLES = {
  A: { short: "A. Mở đầu", full: "A. HOẠT ĐỘNG MỞ ĐẦU (TIẾP CẬN VẤN ĐỀ)" },
  B: { short: "B. Hình thành KT", full: "B. HOẠT ĐỘNG HÌNH THÀNH KIẾN THỨC MỚI" },
  C: { short: "C. Luyện tập", full: "C. HOẠT ĐỘNG LUYỆN TẬP" },
  D: { short: "D. Vận dụng", full: "D. HOẠT ĐỘNG VẬN DỤNG" }
};

// =============================================================================
// KHỞI CHẠY KHI TRANG SẴN SÀNG
// =============================================================================
document.addEventListener("DOMContentLoaded", async () => {
  initLucideIcons();
  loadStateFromLocalStorage();
  setupEventListeners();
  populateLessonDropdown();
  syncDraftDom();
  updateKeyCountDisplay();
  syncGeminiConfigToUI();
  updateImageCounts();
  renderImageGallery();
  renderStandardsCatalog();
  renderPhasePedagogy();
  renderAllTabsPreview();

  try {
    await geminiAPI.syncKeysFromServer();
    updateKeyCountDisplay();
  } catch (e) {
    console.warn("Lỗi sync keys khi khởi tạo:", e);
  }
});

function initLucideIcons() {
  if (window.lucide) {
    window.lucide.createIcons();
  }
}

function syncDraftDom() {
  const values = { selectGrade: appState.selectedGrade, inputSchool: appState.school, inputGroup: appState.group, inputTeacher: appState.teacher, inputSubject: appState.subject, inputTopicCustom: appState.customTopic, inputDuration: appState.duration, inputClassProfileNote: appState.teachingContext.classProfileNote, inputSupportNote: appState.teachingContext.supportNote, inputSpecialRequirements: appState.teachingContext.specialRequirements, editorVision: appState.content.vision, editorObjectives: appState.content.objectives, editorMaterials: appState.content.materials, editorActivity: appState.content.activities.A };
  Object.entries(values).forEach(([id, value]) => { const el = document.getElementById(id); if (el) el.value = value || ""; });
  const lessonSelect = document.getElementById("selectLesson");
  if (lessonSelect) lessonSelect.value = appState.selectedLesson || "";
  setCheckboxGroupValues(".class-profile-choice", appState.teachingContext.classProfileChoices);
  setCheckboxGroupValues(".support-choice", appState.teachingContext.supportChoices);
  const context = appState.teachingContext;
  if (document.getElementById("inputClassSize")) document.getElementById("inputClassSize").value = context.classSize;
  if (document.getElementById("selectReadiness")) document.getElementById("selectReadiness").value = context.readiness;
  if (document.getElementById("selectGrouping")) document.getElementById("selectGrouping").value = context.grouping;
  [["hasProjector","projector"],["hasInternet","internet"],["hasDevices","devices"]].forEach(([id,key]) => { const input = document.getElementById(id); if (input) input.checked = Boolean(context.facilities?.[key]); });
  renderDraftControls();
  renderPedagogyCatalogs();
}

// =============================================================================
// LƯU TRỮ VÀ KHÔI PHỤC TRẠNG THÁI (LOCALSTORAGE)
// =============================================================================
function getDraftScope() {
  const candidates = ["currentUser", "user", "authUser", "userInfo"];
  for (const key of candidates) try {
    const user = JSON.parse(localStorage.getItem(key) || "null");
    if (user?.id != null) return `user-${String(user.id).replace(/[^a-zA-Z0-9_-]/g, "_")}`;
  } catch (_) { /* ignore malformed session cache */ }
  const token = localStorage.getItem("authToken");
  return token ? `user-${String(localStorage.getItem("userId") || localStorage.getItem("userEmail") || "authenticated").replace(/[^a-zA-Z0-9_-]/g, "_")}` : "anonymous";
}
function normalizeDraftPart(value) { return String(value || "").trim().toLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g, "").replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, ""); }
function buildDraftId(grade, lesson, topic) { return ["kntt", appState.selectedSubject || "TOAN", "none", grade, normalizeDraftPart(lesson), normalizeDraftPart(topic)].join(":"); }
function getDraftId() { return buildDraftId(appState.selectedGrade, appState.selectedLesson, appState.customTopic); }
function getDraftIndexKey() { return `khbd_drafts_v2:${getDraftScope()}:index`; }
function getDraftKey(id = getDraftId()) { return `khbd_drafts_v2:${getDraftScope()}:${id}`; }
function currentDraftData() {
  return { selectedGrade: appState.selectedGrade, selectedSubject: appState.selectedSubject, selectedLesson: appState.selectedLesson, customTopic: appState.customTopic, school: appState.school, group: appState.group, teacher: appState.teacher, subject: appState.subject, duration: appState.duration, teachingContext: appState.teachingContext, content: appState.content };
}
function saveStateToLocalStorage() {
  try {
    const id = getDraftId(), dataToSave = currentDraftData();
    localStorage.setItem(getDraftKey(id), JSON.stringify(dataToSave));
    localStorage.setItem(`khbd_drafts_v2:${getDraftScope()}:active`, id);
    const index = JSON.parse(localStorage.getItem(getDraftIndexKey()) || "[]").filter(item => item.id !== id);
    index.unshift({ id, label: appState.customTopic || appState.selectedLesson || `Toán ${appState.selectedGrade}`, updatedAt: Date.now() });
    localStorage.setItem(getDraftIndexKey(), JSON.stringify(index.slice(0, 50)));
    renderDraftControls();
  } catch (e) {
    console.warn("Lỗi lưu state vào localStorage:", e);
  }
}

function applyDraftData(data) {
  if (!data) return;
  Object.assign(appState, { selectedGrade: data.selectedGrade || "6", selectedSubject: data.selectedSubject || "TOAN", selectedLesson: data.selectedLesson || "", customTopic: data.customTopic || "", school: data.school || appState.school, group: data.group || appState.group, teacher: data.teacher || appState.teacher, subject: data.subject || appState.subject, duration: data.duration || appState.duration });
  appState.teachingContext = normalizeTeachingContext(data.teachingContext);
  if (data.content) { const a = data.content.activities || {}; appState.content = { vision: data.content.vision || "", objectives: data.content.objectives || "", materials: data.content.materials || "", activities: Object.fromEntries(Object.keys(appState.content.activities).map(k => [k, a[k] || ""])) }; }
}
function renderDraftControls() {
  const select = document.getElementById("selectMyDraft"); if (!select) return;
  const index = JSON.parse(localStorage.getItem(getDraftIndexKey()) || "[]");
  select.innerHTML = index.map(item => `<option value="${item.id}">${item.label}</option>`).join("");
  select.value = getDraftId();
  document.getElementById("btnImportLegacyDraft").hidden = !(localStorage.getItem("khbd_kntt_saved_state") || localStorage.getItem("khbd_app_saved_state"));
}
function emptyDraftForTarget({ grade, lesson, topic }) {
  const common = { school: appState.school, group: appState.group, teacher: appState.teacher, subject: appState.subject, duration: appState.duration };
  appState.selectedGrade = grade; appState.selectedLesson = lesson; appState.customTopic = topic;
  Object.assign(appState, common);
  appState.teachingContext = normalizeTeachingContext({});
  appState.content = { vision: "", objectives: "", materials: "", activities: { A: "", B: "", C: "", D: "", E: "", F: "", G: "" } };
  appState.images = [];
}
function switchDraft(target) {
  saveStateToLocalStorage();
  const id = buildDraftId(target.grade, target.lesson, target.topic);
  const saved = localStorage.getItem(getDraftKey(id));
  if (saved) applyDraftData(JSON.parse(saved)); else { emptyDraftForTarget(target); saveStateToLocalStorage(); }
  localStorage.setItem(`khbd_drafts_v2:${getDraftScope()}:active`, id);
  populateLessonDropdown(); syncDraftDom(); renderAllTabsPreview(); renderImageGallery();
}
function loadStateFromLocalStorage() {
  try {
    const active = localStorage.getItem(`khbd_drafts_v2:${getDraftScope()}:active`);
    const saved = active && localStorage.getItem(getDraftKey(active));
    if (saved) {
      const data = JSON.parse(saved);
      applyDraftData(data);
      /*
      appState.selectedGrade = data.selectedGrade || "6";
      appState.selectedLesson = data.selectedLesson || "";
      appState.customTopic = data.customTopic || "";
      appState.school = data.school || "TRƯỜNG THCS NGUYỄN DU";
      appState.group = data.group || "TỔ TOÁN - TIN HỌC";
      appState.teacher = data.teacher || "Giáo viên Môn Toán";
      appState.subject = data.subject || "TOÁN";
      appState.duration = data.duration || "02 tiết (90 phút)";
      appState.teachingContext = normalizeTeachingContext(data.teachingContext);
      if (data.content && typeof data.content === "object") {
        const savedActivities = data.content.activities && typeof data.content.activities === "object"
          ? data.content.activities : {};
        appState.content = {
          vision: typeof data.content.vision === "string" ? data.content.vision : "",
          objectives: typeof data.content.objectives === "string" ? data.content.objectives : "",
          materials: typeof data.content.materials === "string" ? data.content.materials : "",
          activities: Object.fromEntries(Object.keys(appState.content.activities).map(key => [
            key, typeof savedActivities[key] === "string" ? savedActivities[key] : ""
          ]))
        };
      }

      // Cập nhật DOM inputs
      document.getElementById("selectGrade").value = appState.selectedGrade;
      document.getElementById("inputSchool").value = appState.school;
      document.getElementById("inputGroup").value = appState.group;
      document.getElementById("inputTeacher").value = appState.teacher;
      document.getElementById("inputSubject").value = appState.subject;
      document.getElementById("inputTopicCustom").value = appState.customTopic;
      document.getElementById("inputDuration").value = appState.duration;
      document.getElementById("inputClassProfileNote").value = appState.teachingContext.classProfileNote;
      document.getElementById("inputSupportNote").value = appState.teachingContext.supportNote;
      document.getElementById("inputSpecialRequirements").value = appState.teachingContext.specialRequirements;
      document.getElementById("toggleDigitalCompetency").checked = appState.teachingContext.integrations.digital;
      document.getElementById("toggleAiCompetency").checked = appState.teachingContext.integrations.ai;
      document.getElementById("toggleForeignLanguage").checked = appState.teachingContext.integrations.foreignLanguage;
      document.getElementById("toggleInclusiveSupport").checked = appState.teachingContext.integrations.inclusive;
      setCheckboxGroupValues(".teaching-method-choice", appState.teachingContext.methods);
      setCheckboxGroupValues(".teaching-technique-choice", appState.teachingContext.techniques);
      setCheckboxGroupValues(".class-profile-choice", appState.teachingContext.classProfileChoices);
      setCheckboxGroupValues(".support-choice", appState.teachingContext.supportChoices);

      // Cập nhật các textareas
      document.getElementById("editorVision").value = appState.content.vision || "";
      document.getElementById("editorObjectives").value = appState.content.objectives || "";
      document.getElementById("editorMaterials").value = appState.content.materials || "";
      document.getElementById("editorActivity").value = appState.content.activities[appState.activeActSubtab] || "";
      */
    }
  } catch (e) {
    console.warn("Lỗi đọc state từ localStorage:", e);
    console.warn("Không thể đọc bản nháp hiện tại; dữ liệu cũ không bị xóa.");
  }
}

function normalizeTeachingContext(context) {
  const source = context && typeof context === "object" ? context : {};
  const integrations = source.integrations && typeof source.integrations === "object" ? source.integrations : {};
  return {
    classProfileChoices: Array.isArray(source.classProfileChoices) ? source.classProfileChoices.filter(value => typeof value === "string").slice(0, 7) : [],
    classProfileNote: typeof source.classProfileNote === "string" ? source.classProfileNote.slice(0, 300) : (typeof source.classProfile === "string" ? source.classProfile.slice(0, 300) : ""),
    supportChoices: Array.isArray(source.supportChoices) ? source.supportChoices.filter(value => typeof value === "string").slice(0, 7) : [],
    supportNote: typeof source.supportNote === "string" ? source.supportNote.slice(0, 300) : (typeof source.supportNeeds === "string" ? source.supportNeeds.slice(0, 300) : ""),
    integrations: {
      digital: Boolean(integrations.digital),
      ai: Boolean(integrations.ai),
      foreignLanguage: Boolean(integrations.foreignLanguage),
      inclusive: Boolean(integrations.inclusive)
    },
    methods: Array.isArray(source.methods) ? source.methods.filter(value => typeof value === "string").slice(0, 20) : [],
    techniques: Array.isArray(source.techniques) ? source.techniques.filter(value => typeof value === "string").slice(0, 20) : [],
    subjectActivities: Array.isArray(source.subjectActivities) ? source.subjectActivities.filter(value => typeof value === "string").slice(0, 20) : [],
    standards: Array.isArray(source.standards) ? source.standards.filter(item => item && typeof item === "object") : [],
    phasePedagogy: source.phasePedagogy && typeof source.phasePedagogy === "object" ? source.phasePedagogy : { A: {}, B: {}, C: {}, D: {} },
    classSize: Math.max(1, Math.min(60, Number(source.classSize) || 40)), readiness: typeof source.readiness === "string" ? source.readiness : "Không đồng đều", grouping: typeof source.grouping === "string" ? source.grouping : "Cá nhân/cặp đôi", facilities: source.facilities && typeof source.facilities === "object" ? source.facilities : { projector:false, internet:false, devices:false },
    specialRequirements: typeof source.specialRequirements === "string" ? source.specialRequirements.slice(0, 600) : "",
    autoPedagogy: source.autoPedagogy && typeof source.autoPedagogy === "object" ? source.autoPedagogy : { methods: [], techniques: { A: [], B: [], C: [], D: [] }, activities: [] }
  };
}

function setCheckboxGroupValues(selector, values) {
  const selected = new Set(values || []);
  document.querySelectorAll(selector).forEach(input => { input.checked = selected.has(input.value); });
}

function currentSubjectId() {
  return String(appState.selectedSubject || "").toLowerCase();
}

function pedagogyRecommendCtx() {
  const context = normalizeTeachingContext(appState.teachingContext);
  return { subjectId: currentSubjectId(), grade: appState.selectedGrade, classSize: context.classSize, facilities: context.facilities };
}

function pedagogyLabel(group, id) {
  const list = (typeof KHBD_PEDAGOGY_CATALOG !== "undefined" && KHBD_PEDAGOGY_CATALOG[group]) || [];
  return list.find(item => item.id === id || item.label === id)?.label || id;
}

function autoPedagogyState() {
  const source = appState.teachingContext.autoPedagogy || {};
  return {
    methods: Array.isArray(source.methods) ? source.methods : [],
    techniques: source.techniques && typeof source.techniques === "object" ? source.techniques : { A: [], B: [], C: [], D: [] },
    activities: Array.isArray(source.activities) ? source.activities : []
  };
}

function renderPedagogyItem(item, className, extraAttrs, checked, autoIds) {
  const rec = typeof isPedagogyRecommended === "function" && isPedagogyRecommended(item, pedagogyRecommendCtx());
  const auto = (autoIds || []).includes(item.id);
  const badge = auto ? ' <small class="pedagogy-fit">Đề xuất theo bài</small>' : (rec ? ' <small class="pedagogy-fit">Phù hợp môn này</small>' : "");
  return `<label class="pedagogy-item${auto || rec ? " is-recommended" : ""}"><input type="checkbox" class="${className}" ${extraAttrs} value="${item.id}" ${checked ? "checked" : ""}> <span><strong>${item.label}</strong><br><small>${item.description || ""}${badge}</small></span></label>`;
}

function isChoiceSelected(selected, item) {
  const set = selected instanceof Set ? selected : new Set(selected || []);
  return set.has(item.id) || set.has(item.label);
}

function renderPedagogyCatalogs() {
  if (typeof KHBD_PEDAGOGY_CATALOG === "undefined") return;
  const catalog = KHBD_PEDAGOGY_CATALOG;
  appState.teachingContext = normalizeTeachingContext(appState.teachingContext);
  const context = appState.teachingContext;
  const auto = autoPedagogyState();
  const methods = new Set(context.methods || []);
  const activities = new Set(context.subjectActivities || []);
  const phase = context.phasePedagogy || (appState.teachingContext.phasePedagogy = { A: {}, B: {}, C: {}, D: {} });

  const methodsPanel = document.getElementById("methodsCatalogPanel");
  if (methodsPanel) {
    methodsPanel.innerHTML = `<details class="pedagogy-block" open><summary>Phương pháp dạy học hiện đại</summary><div class="pedagogy-grid">${catalog.methods.map(item => renderPedagogyItem(item, "pedagogy-method", "", isChoiceSelected(methods, item), auto.methods)).join("")}</div></details>`;
    methodsPanel.querySelectorAll(".pedagogy-method").forEach(input => input.addEventListener("change", () => {
      appState.teachingContext.methods = Array.from(document.querySelectorAll(".pedagogy-method:checked")).map(el => el.value);
      appState.teachingContext.autoPedagogy = autoPedagogyState();
      appState.teachingContext.autoPedagogy.methods = [];
      saveStateToLocalStorage();
    }));
  }

  const techPanel = document.getElementById("techniquesCatalogPanel");
  if (techPanel) {
    const groups = [
      { phase: "A", title: "KỸ THUẬT KHỞI ĐỘNG" },
      { phase: "B", title: "KỸ THUẬT HÌNH THÀNH KIẾN THỨC" },
      { phase: "C", title: "KỸ THUẬT LUYỆN TẬP" },
      { phase: "D", title: "KỸ THUẬT VẬN DỤNG" }
    ];
    techPanel.innerHTML = `<details class="pedagogy-block" open><summary>Kĩ thuật dạy học tích cực</summary>${groups.map(g => {
      const chosen = new Set(phase[g.phase]?.techniques || []);
      const items = catalog.techniques.filter(item => (item.phases || []).includes(g.phase));
      return `<h4 class="pedagogy-subgroup">${g.title}</h4><div class="pedagogy-grid">${items.map(item => renderPedagogyItem(item, "pedagogy-technique", `data-phase="${g.phase}"`, isChoiceSelected(chosen, item), auto.techniques[g.phase] || [])).join("")}</div>`;
    }).join("")}</details>`;
    techPanel.querySelectorAll(".pedagogy-technique").forEach(input => input.addEventListener("change", () => {
      const p = input.dataset.phase;
      appState.teachingContext.phasePedagogy[p] ||= {};
      appState.teachingContext.phasePedagogy[p].techniques = Array.from(document.querySelectorAll(`.pedagogy-technique[data-phase="${p}"]:checked`)).map(el => el.value);
      appState.teachingContext.autoPedagogy = autoPedagogyState();
      appState.teachingContext.autoPedagogy.techniques = appState.teachingContext.autoPedagogy.techniques || { A: [], B: [], C: [], D: [] };
      appState.teachingContext.autoPedagogy.techniques[p] = [];
      saveStateToLocalStorage();
    }));
  }

  const actPanel = document.getElementById("activitiesCatalogPanel");
  if (actPanel) {
    actPanel.innerHTML = `<details class="pedagogy-block" open><summary>Hoạt động đặc thù môn học</summary><div class="pedagogy-grid">${catalog.activities.map(item => renderPedagogyItem(item, "pedagogy-activity", "", isChoiceSelected(activities, item), auto.activities)).join("")}</div></details>`;
    actPanel.querySelectorAll(".pedagogy-activity").forEach(input => input.addEventListener("change", () => {
      appState.teachingContext.subjectActivities = Array.from(document.querySelectorAll(".pedagogy-activity:checked")).map(el => el.value);
      appState.teachingContext.autoPedagogy = autoPedagogyState();
      appState.teachingContext.autoPedagogy.activities = [];
      saveStateToLocalStorage();
    }));
  }
}

function renderPhasePedagogy() {
  renderPedagogyCatalogs();
}

function integrationRecommendContext() {
  return {
    topic: getTopicDisplayName(),
    vision: appState.content.vision || "",
    subjectName: appState.subjectName || appState.subject || "",
    subjectId: currentSubjectId(),
    grade: appState.selectedGrade,
    methods: appState.teachingContext.methods,
    activities: appState.teachingContext.subjectActivities,
    specialRequirements: appState.teachingContext.specialRequirements,
    grouping: appState.teachingContext.grouping,
    facilities: appState.teachingContext.facilities,
    aiOn: Boolean(appState.teachingContext.integrations.ai)
  };
}

function standardsOfKind(kind) {
  const catalog = KHBD_STANDARDS?.[kind];
  if (!catalog) return [];
  return (appState.teachingContext.standards || []).filter(item => item.framework === catalog.framework);
}

function hasAnalyzedLessonContent() {
  return String(appState.content.vision || "").replace(/\s+/g, " ").trim().length >= 80;
}

function pedagogyRecommendFullCtx() {
  const context = normalizeTeachingContext(appState.teachingContext);
  return {
    vision: appState.content.vision || "",
    topic: getTopicDisplayName(),
    subjectName: appState.subjectName || appState.subject || "",
    subjectId: currentSubjectId(),
    grade: appState.selectedGrade,
    classSize: context.classSize,
    readiness: context.readiness,
    facilities: context.facilities
  };
}

function ensureIntegrationStandards({ force = false, silent = false } = {}) {
  if (typeof recommendOfficialStandards !== "function") return false;
  let changed = false;
  const notices = [];
  ["digital", "ai"].forEach(kind => {
    const enabled = appState.teachingContext.integrations[kind];
    const catalog = KHBD_STANDARDS[kind];
    if (!catalog) return;
    if (!enabled) {
      const before = appState.teachingContext.standards.length;
      appState.teachingContext.standards = appState.teachingContext.standards.filter(item => item.framework !== catalog.framework);
      if (appState.teachingContext.standards.length !== before) changed = true;
      return;
    }
    const current = standardsOfKind(kind);
    const onlyAuto = current.length && current.every(item => item.autoSuggested);
    if (!force && current.length && !onlyAuto) return;
    if (!hasAnalyzedLessonContent()) return;
    const recommended = recommendOfficialStandards(kind, integrationRecommendContext());
    appState.teachingContext.standards = appState.teachingContext.standards.filter(item => item.framework !== catalog.framework).concat(recommended);
    changed = true;
    const names = recommended.map(item => item.officialCode ? `${item.officialCode}` : item.officialLabel).join("; ");
    notices.push(kind === "digital"
      ? `NLS (TT 02/2025): ${recommended.length} miền — ${names}`
      : `AI (QĐ 2422): ${recommended.length} mã — ${names}`);
  });
  if (changed) {
    saveStateToLocalStorage();
    renderStandardsCatalog();
    if (!silent && notices.length) showToast(`Đã đề xuất theo nội dung bài: ${notices.join(". ")}. Bạn có thể sửa, tối đa 3 mục/nhóm.`, "info", 5000);
  }
  return changed;
}

function ensurePedagogyFromLesson({ force = false, silent = false } = {}) {
  if (typeof recommendPedagogyFromLesson !== "function") return false;
  if (!hasAnalyzedLessonContent()) return false;
  const rec = recommendPedagogyFromLesson(pedagogyRecommendFullCtx());
  const auto = autoPedagogyState();
  let changed = false;
  const notices = [];
  if (force || !(appState.teachingContext.methods || []).length) {
    appState.teachingContext.methods = rec.methods;
    auto.methods = rec.methods;
    changed = true;
    notices.push(`PPDH: ${rec.methods.map(id => pedagogyLabel("methods", id)).join(", ") || "không"}`);
  }
  appState.teachingContext.phasePedagogy ||= { A: {}, B: {}, C: {}, D: {} };
  auto.techniques ||= { A: [], B: [], C: [], D: [] };
  ["A", "B", "C", "D"].forEach(phase => {
    const current = appState.teachingContext.phasePedagogy[phase]?.techniques || [];
    if (force || !current.length) {
      appState.teachingContext.phasePedagogy[phase] ||= {};
      appState.teachingContext.phasePedagogy[phase].techniques = rec.techniques[phase] || [];
      auto.techniques[phase] = rec.techniques[phase] || [];
      changed = true;
    }
  });
  if (force || !(appState.teachingContext.subjectActivities || []).length) {
    appState.teachingContext.subjectActivities = rec.activities;
    auto.activities = rec.activities;
    changed = true;
    notices.push(`HĐ đặc thù: ${rec.activities.map(id => pedagogyLabel("activities", id)).join(", ") || "không"}`);
  }
  if (changed) {
    appState.teachingContext.autoPedagogy = auto;
    saveStateToLocalStorage();
    renderPedagogyCatalogs();
    if (!silent) showToast(`Đã đề xuất PPDH/kỹ thuật theo nội dung SGK. ${notices.join(". ")}. Bạn có thể sửa.`, "info", 5000);
  }
  return changed;
}

function applyLessonBasedRecommendations({ force = false, silent = false } = {}) {
  if (!hasAnalyzedLessonContent()) {
    if (!silent) showToast("Cần phân tích hoặc dán nội dung SGK ở Bước 0 trước khi đề xuất NLS/AI và PPDH.", "warning");
    return false;
  }
  const ped = ensurePedagogyFromLesson({ force, silent: true });
  const std = ensureIntegrationStandards({ force, silent: true });
  if (!silent && (ped || std)) {
    showToast("Đã đề xuất PPDH và NLS/AI theo nội dung bài đã phân tích. Bạn có thể sửa trên Tab 0.", "success", 5000);
  }
  return ped || std;
}

function renderStandardsCatalog() {
  const grade = Number(appState.selectedGrade);
  ["digital", "ai"].forEach(kind => {
    const panel = document.getElementById(`${kind}StandardsPanel`);
    const enabled = appState.teachingContext.integrations[kind === "digital" ? "digital" : "ai"];
    const catalog = KHBD_STANDARDS?.[kind];
    if (!panel || !catalog) return;
    panel.hidden = !enabled;
    if (!enabled) return;
    const entries = catalog.entries.filter(entry => entry.grades.includes(grade));
    const selectedIds = new Set(standardsOfKind(kind).map(item => item.catalogId));
    const suggestedIds = new Set(standardsOfKind(kind).filter(item => item.autoSuggested).map(item => item.catalogId));
    const maxSelect = catalog.maxSelect || 3;
    const waitHint = hasAnalyzedLessonContent()
      ? `Hệ thống đề xuất 2–3 mục đúng văn bản theo nội dung SGK đã phân tích; bạn có thể đổi, tối đa ${maxSelect} mục.`
      : "Chưa có nội dung bài. Hãy phân tích ảnh/PDF SGK ở Bước 0, sau đó hệ thống mới đề xuất 2–3 mục.";
    panel.innerHTML = `<fieldset class="tool-group"><legend>${catalog.framework} (${catalog.date})</legend><small>${catalog.source}. ${waitHint}</small>${entries.map(entry => {
      const rec = suggestedIds.has(entry.id);
      return `<label style="display:block"><input type="checkbox" class="standard-choice" data-kind="${kind}" value="${entry.id}" ${selectedIds.has(entry.id) ? "checked" : ""}> ${entry.code ? `${entry.code}: ` : "Miền: "}${entry.label}${rec ? ' <small class="pedagogy-fit">Đề xuất theo bài</small>' : ""}</label>`;
    }).join("")}</fieldset>`;
    panel.querySelectorAll(".standard-choice").forEach(input => input.addEventListener("change", () => {
      const checked = Array.from(document.querySelectorAll(`.standard-choice[data-kind="${kind}"]:checked`));
      if (checked.length > maxSelect) {
        input.checked = false;
        showToast(`Một bài chỉ chọn ${maxSelect} mục ${kind === "digital" ? "năng lực số (TT 02)" : "năng lực AI (QĐ 2422)"}.`, "warning");
        return;
      }
      const selected = checked.map(choice => {
        const entry = entries.find(item => item.id === choice.value);
        return standardToRecord(kind, entry, grade, false);
      });
      appState.teachingContext.standards = appState.teachingContext.standards.filter(item => item.framework !== catalog.framework).concat(selected);
      saveStateToLocalStorage();
    }));
  });
}

// =============================================================================
// THIẾT LẬP CÁC SỰ KIỆN GIAO DIỆN (EVENT LISTENERS)
// =============================================================================
function setupEventListeners() {
  // 1. Chuyển Tab chính
  document.querySelectorAll(".nav-tab-btn").forEach(btn => {
    btn.addEventListener("click", () => {
      const tabId = btn.getAttribute("data-tab");
      switchMainTab(tabId);
    });
  });

  // 2. Thay đổi Khối lớp / Bài học
  document.getElementById("selectGrade").addEventListener("change", (e) => {
    const nextGrade = e.target.value;
    const before = appState.teachingContext.standards.length;
    
    // Tự động gợi ý tên trường
    const levelName = getGradeLevelName(nextGrade).toUpperCase();
    if (!appState.school || appState.school.startsWith("TRƯỜNG THCS") || appState.school.startsWith("TRƯỜNG THPT") || appState.school.startsWith("TRƯỜNG TIỂU HỌC")) {
       appState.school = `TRƯỜNG ${levelName} ...`;
    }

    switchDraft({ grade: nextGrade, lesson: "", topic: "" });
    const after = appState.teachingContext.standards.length;
    renderStandardsCatalog();
    renderPedagogyCatalogs();
    if (before !== after) showToast("Đã bỏ lựa chọn tiêu chuẩn không áp dụng cho khối lớp mới.", "info");
  });

  document.getElementById("selectMyDraft").addEventListener("change", e => {
    saveStateToLocalStorage();
    const saved = localStorage.getItem(getDraftKey(e.target.value));
    if (saved) { applyDraftData(JSON.parse(saved)); localStorage.setItem(`khbd_drafts_v2:${getDraftScope()}:active`, e.target.value); location.reload(); }
  });
  document.getElementById("btnClearCurrentDraft").addEventListener("click", () => {
    const id = getDraftId(); localStorage.removeItem(getDraftKey(id));
    const index = JSON.parse(localStorage.getItem(getDraftIndexKey()) || "[]").filter(item => item.id !== id);
    localStorage.setItem(getDraftIndexKey(), JSON.stringify(index));
    showToast("Đã xóa bản nháp hiện tại.", "info"); renderDraftControls();
  });
  document.getElementById("btnImportLegacyDraft").addEventListener("click", () => {
    const legacy = localStorage.getItem("khbd_kntt_saved_state") || localStorage.getItem("khbd_app_saved_state");
    if (!legacy || !confirm("Nhập bản nháp cũ trên trình duyệt này vào tài khoản hiện tại?")) return;
    applyDraftData(JSON.parse(legacy)); saveStateToLocalStorage(); location.reload();
  });

  document.getElementById("selectLesson").addEventListener("change", (e) => {
    const lesson = e.target.value;
    switchDraft({ grade: appState.selectedGrade, lesson, topic: lesson });
  });
  
  document.getElementById("selectSubject").addEventListener("change", e => { 
    saveStateToLocalStorage(); 
    appState.selectedSubject = e.target.value; 
    appState.subjectName = CURRICULUM_DATA.subjects.find(item => item.id === e.target.value)?.name || "Môn học"; 
    appState.subject = appState.subjectName; 
    appState.selectedLesson = ""; 
    appState.customTopic = ""; 
    populateLessonDropdown(); 
    switchDraft({ grade: appState.selectedGrade, lesson: "", topic: "" });
    renderPedagogyCatalogs();
    if ((appState.teachingContext.standards || []).every(item => item.autoSuggested)) {
      ensureIntegrationStandards({ force: true, silent: true });
    }
  });


  document.getElementById("inputTopicCustom").addEventListener("input", (e) => {
    e.target.dataset.pendingTopic = e.target.value;
  });
  document.getElementById("inputTopicCustom").addEventListener("blur", e => {
    const topic = (e.target.dataset.pendingTopic ?? e.target.value).trim();
    if (topic && topic !== appState.customTopic) switchDraft({ grade: appState.selectedGrade, lesson: "", topic });
  });

  document.getElementById("selectModel").addEventListener("change", (e) => {
    geminiAPI.setModel(e.target.value);
    document.getElementById("footerModelName").textContent = e.target.value;
    showToast(`Đã chuyển Model sang: ${e.target.value}`, "info");
  });

  // 3. Inputs thông tin chung
  ["inputSchool", "inputGroup", "inputTeacher", "inputSubject", "inputDuration"].forEach(id => {
    document.getElementById(id).addEventListener("input", (e) => {
      const key = id.replace("input", "").toLowerCase();
      appState[key] = e.target.value;
      saveStateToLocalStorage();
    });
  });

  [["inputClassProfileNote", "classProfileNote"], ["inputSupportNote", "supportNote"], ["inputSpecialRequirements", "specialRequirements"]].forEach(([id, key]) => {
    document.getElementById(id).addEventListener("input", (e) => {
      appState.teachingContext[key] = e.target.value;
      saveStateToLocalStorage();
    });
  });
  [
    ["toggleDigitalCompetency", "digital"], ["toggleAiCompetency", "ai"],
    ["toggleForeignLanguage", "foreignLanguage"], ["toggleInclusiveSupport", "inclusive"]
  ].forEach(([id, key]) => {
    document.getElementById(id).addEventListener("change", (e) => {
      appState.teachingContext.integrations[key] = e.target.checked;
      if (key === "digital" || key === "ai") {
        if (e.target.checked && !hasAnalyzedLessonContent()) {
          renderStandardsCatalog();
          showToast("Hãy phân tích SGK ở Bước 0 trước. Sau khi có nội dung bài, hệ thống sẽ đề xuất 2–3 mục đúng văn bản.", "info", 5000);
        } else {
          ensureIntegrationStandards({ force: e.target.checked && (!standardsOfKind(key).length || standardsOfKind(key).every(item => item.autoSuggested)) });
          renderStandardsCatalog();
        }
      }
      saveStateToLocalStorage();
    });
  });

  [[".class-profile-choice", "classProfileChoices"], [".support-choice", "supportChoices"]].forEach(([selector, key]) => {
    document.querySelectorAll(selector).forEach(input => input.addEventListener("change", () => {
      appState.teachingContext[key] = Array.from(document.querySelectorAll(`${selector}:checked`)).map(choice => choice.value);
      saveStateToLocalStorage();
    }));
  });
  [["inputClassSize", "classSize"], ["selectReadiness", "readiness"], ["selectGrouping", "grouping"]].forEach(([id, key]) => document.getElementById(id).addEventListener("change", e => { appState.teachingContext[key] = e.target.value; saveStateToLocalStorage(); }));
  [["hasProjector", "projector"], ["hasInternet", "internet"], ["hasDevices", "devices"]].forEach(([id, key]) => document.getElementById(id).addEventListener("change", e => {
    appState.teachingContext.facilities[key] = e.target.checked;
    if ((appState.teachingContext.integrations.digital || appState.teachingContext.integrations.ai) &&
        (appState.teachingContext.standards || []).every(item => item.autoSuggested)) {
      ensureIntegrationStandards({ force: true, silent: true });
    }
    saveStateToLocalStorage();
  }));

  // 4. Dropzone & Paste ảnh toàn cục
  const dropzone = document.getElementById("dropzoneContainer");
  const fileInput = document.getElementById("fileInputImages");

  dropzone.addEventListener("click", () => fileInput.click());
  fileInput.addEventListener("change", handleFileSelect);

  dropzone.addEventListener("dragover", (e) => {
    e.preventDefault();
    dropzone.classList.add("dragover");
  });

  dropzone.addEventListener("dragleave", () => {
    dropzone.classList.remove("dragover");
  });

  dropzone.addEventListener("drop", (e) => {
    e.preventDefault();
    dropzone.classList.remove("dragover");
    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      handleFiles(Array.from(e.dataTransfer.files));
    }
  });

  // Lắng nghe Paste ảnh (Ctrl + V)
  window.addEventListener("paste", handleGlobalPaste);

  document.getElementById("btnClearVisionImages").addEventListener("click", () => {
    if (appState.images.length === 0) return;
    if (confirm(`Bạn có chắc muốn xóa tất cả ảnh trang SGK đã tải lên?`)) {
      appState.images = [];
      updateImageCounts();
      renderImageGallery();
      showToast("Đã xóa toàn bộ ảnh.", "info");
    }
  });

  // 5. Subtabs Hoạt động A -> G trong Tab 4
  document.querySelectorAll(".act-tab-btn").forEach(btn => {
    btn.addEventListener("click", () => {
      const actKey = btn.getAttribute("data-act");
      switchActivitySubtab(actKey);
    });
  });

  // 6. Đồng bộ Textarea với KaTeX Preview khi người dùng chỉnh sửa
  setupEditorPreviewSync("editorVision", "previewVision", (val) => { appState.content.vision = val; saveStateToLocalStorage(); });
  const visionEditor = document.getElementById("editorVision");
  if (visionEditor) visionEditor.addEventListener("blur", () => {
    if (hasAnalyzedLessonContent()) applyLessonBasedRecommendations({ silent: true });
  });
  setupEditorPreviewSync("editorObjectives", "previewObjectives", (val) => { appState.content.objectives = val; saveStateToLocalStorage(); });
  setupEditorPreviewSync("editorMaterials", "previewMaterials", (val) => { appState.content.materials = val; saveStateToLocalStorage(); });
  setupEditorPreviewSync("editorActivity", "previewActivity", (val) => { 
    appState.content.activities[appState.activeActSubtab] = val; 
    saveStateToLocalStorage(); 
  });

  // 7. Các nút Tạo nội dung đơn lẻ
  document.getElementById("btnAnalyzeVision").addEventListener("click", handleGenerateVision);
  document.getElementById("btnGenerateObjectives").addEventListener("click", handleGenerateObjectives);
  document.getElementById("btnGenerateMaterials").addEventListener("click", handleGenerateMaterials);
  document.getElementById("btnGenerateCurrentAct").addEventListener("click", handleGenerateCurrentActivity);

  // 8. Nút Tạo Toàn Bộ Giáo Án (1-Click)
  document.getElementById("btn1ClickGenerate").addEventListener("click", handle1ClickGenerate);
  document.getElementById("btnCancelGeneration").addEventListener("click", requestGenerationCancel);

  document.querySelectorAll(".toggle-preview-btn").forEach(btn => {
    btn.addEventListener("click", () => togglePreviewPanel(btn));
  });

  // 9. Các nút Xuất Word (.docx)
  document.getElementById("btnExportObjectivesDocx").addEventListener("click", () => {
    exportTabDocx("I. Mục tiêu", appState.content.objectives, `KHBD_MucTieu_${getSafeTopicName()}`);
  });
  document.getElementById("btnExportMaterialsDocx").addEventListener("click", () => {
    exportTabDocx("II. Thiết bị & Học liệu", appState.content.materials, `KHBD_ThietBi_${getSafeTopicName()}`);
  });
  document.getElementById("btnExportCurrentActDocx").addEventListener("click", () => {
    const act = ACTIVITY_TITLES[appState.activeActSubtab];
    exportTabDocx(act.full, appState.content.activities[appState.activeActSubtab], `KHBD_${act.short.replace(/[^a-zA-Z0-9]/g, "_")}_${getSafeTopicName()}`);
  });
  document.getElementById("btnExportFullDocx").addEventListener("click", handleExportFullDocx);

  // 10. Sao chép Markdown & In ấn trong Tab 5
  document.getElementById("btnCopyFullMarkdown").addEventListener("click", handleCopyFullMarkdown);
  document.getElementById("btnPrintPlan").addEventListener("click", () => window.print());

  // 11. Xóa toàn bộ nội dung
  document.getElementById("btnClearAll").addEventListener("click", handleClearAllContent);

  // 12. Quản lý API Key Modal
  setupApiKeyModal();

  // 13. Quản lý Modal Chọn trang PDF SGK
  setupPdfModal();

  // 14. Key Rotation Callback từ geminiAPI
  geminiAPI.onKeyRotatedCallback = ({ prevIndex, newIndex, totalKeys, reason }) => {
    showToast(`Đã tự động chuyển sang Key #${newIndex + 1}/${totalKeys}. Lý do: ${reason}`, "warning", 4500);
  };
}

// =============================================================================
// CẬP NHẬT DANH SÁCH BÀI HỌC TỪ CURRICULUM DATA
// =============================================================================
function populateLessonDropdown() {
  const subjectSelect = document.getElementById("selectSubject");
  const grade = Number(appState.selectedGrade);
  
  if (subjectSelect) {
    const validSubjects = getSubjectsForGrade(grade);
    subjectSelect.innerHTML = validSubjects.map(item => `<option value="${item.id}">${item.name}</option>`).join("");
    if (!validSubjects.some(s => s.id === appState.selectedSubject)) {
      appState.selectedSubject = validSubjects[0]?.id || "toan";
      appState.subjectName = validSubjects[0]?.name || "Toán";
      appState.subject = appState.subjectName;
    }
    subjectSelect.value = appState.selectedSubject;
  }
  
  const select = document.getElementById("selectLesson");
  const chapters = getLessonsForBook(appState.selectedSubject, "standard", appState.selectedGrade);
  
  select.innerHTML = `<option value="">${chapters.length ? "-- Chọn bài học từ SGK --" : "-- Tự nhập tên bài ở ô bên dưới --"}</option>`;

  chapters.forEach(ch => {
    const optgroup = document.createElement("optgroup");
    optgroup.label = ch.chapter;
    ch.items.forEach(item => {
      const opt = document.createElement("option");
      opt.value = item;
      opt.textContent = item;
      if (item === appState.selectedLesson) opt.selected = true;
      optgroup.appendChild(opt);
    });
    select.appendChild(optgroup);
  });
}

function getSafeTopicName() {
  const topic = appState.customTopic || appState.selectedLesson || "Bai_Hoc";
  return topic.replace(/[^a-zA-Z0-9_\u00C0-\u1EF9]/g, "_").substring(0, 40);
}

function getTopicDisplayName() {
  return appState.customTopic || appState.selectedLesson || "Bài học chưa đặt tên";
}

// =============================================================================
// CHUYỂN TAB & SUBTABS
// =============================================================================
function switchMainTab(tabId) {
  document.querySelectorAll(".nav-tab-btn").forEach(b => b.classList.remove("active"));
  document.querySelectorAll(".tab-pane").forEach(p => p.classList.remove("active"));

  const targetBtn = document.querySelector(`.nav-tab-btn[data-tab="${tabId}"]`);
  const targetPane = document.getElementById(tabId);

  if (targetBtn) targetBtn.classList.add("active");
  if (targetPane) targetPane.classList.add("active");

  appState.activeTab = tabId;

  // Nếu chuyển sang Tab 5 (Toàn bộ Giáo án), tự động cập nhật preview
  if (tabId === "tabFullPreview") {
    renderFullLessonPreview();
  }
}

function switchActivitySubtab(actKey) {
  if (!ACTIVITY_TITLES[actKey]) return;
  document.querySelectorAll(".act-tab-btn").forEach(b => b.classList.remove("active"));
  const targetBtn = document.querySelector(`.act-tab-btn[data-act="${actKey}"]`);
  if (targetBtn) targetBtn.classList.add("active");

  appState.activeActSubtab = actKey;
  const actInfo = ACTIVITY_TITLES[actKey];
  document.getElementById("currentActTitle").textContent = actInfo.full;
  document.getElementById("editorActLabel").textContent = `Nội dung ${actInfo.short}`;

  // Đổ nội dung vào editor
  const content = appState.content.activities[actKey] || "";
  document.getElementById("editorActivity").value = content;
  renderMathPreview(content, "previewActivity");
}

// =============================================================================
// XỬ LÝ ẢNH SGK & PDF (DÁN CTRL+V, KÉO THẢ, QUẢN LÝ)
// =============================================================================
function handleGlobalPaste(e) {
  const clipboardData = e.clipboardData || window.clipboardData;
  if (!clipboardData || !clipboardData.items) return;

  const items = clipboardData.items;
  const imageFiles = [];

  for (let i = 0; i < items.length; i++) {
    if (items[i].type.indexOf("image") !== -1) {
      const file = items[i].getAsFile();
      if (file) {
        file._isPasted = true;
        imageFiles.push(file);
      }
    }
  }

  if (imageFiles.length > 0) {
    if (appState.activeTab !== "tabVision") {
      switchMainTab("tabVision");
    }
    handleFiles(imageFiles);
    showToast(`Đã dán thành công ${imageFiles.length} ảnh trang SGK!`, "success");
  }
}

function handleFileSelect(e) {
  if (e.target.files && e.target.files.length > 0) {
    handleFiles(Array.from(e.target.files));
    e.target.value = ""; // Reset
  }
}

function handleFiles(files) {
  const pdfFiles = files.filter(f => f.type === "application/pdf" || f.name.toLowerCase().endsWith(".pdf"));
  const imgFiles = files.filter(f => f.type !== "application/pdf" && !f.name.toLowerCase().endsWith(".pdf"));

  // Nếu có file PDF, kích hoạt quy trình nạp PDF
  if (pdfFiles.length > 0) {
    handlePdfFile(pdfFiles[0]);
  }

  if (imgFiles.length === 0) return;

  const availableSlots = MAX_IMAGES - appState.images.length;
  const currentBytes = appState.images.reduce((total, image) => total + (image.size || 0), 0);
  let accepted = 0;
  let addedBytes = 0;
  let rejected = 0;

  imgFiles.forEach(file => {
    if (!ALLOWED_IMAGE_TYPES.has(file.type) || file.size > MAX_IMAGE_BYTES || accepted >= availableSlots || currentBytes + addedBytes + file.size > MAX_TOTAL_IMAGE_BYTES) {
      rejected++;
      return;
    }
    accepted++;
    addedBytes += file.size;

    const isPasted = !!file._isPasted;
    const reader = new FileReader();
    reader.onload = (e) => {
      const base64Data = e.target.result;
      appState.images.push({
        id: "img_" + Date.now() + "_" + Math.random().toString(36).substr(2, 5),
        name: isPasted ? `[Ảnh dán] ${new Date().toLocaleTimeString()}` : (file.name || `Trang SGK ${appState.images.length + 1}`),
        mimeType: file.type || "image/jpeg",
        size: file.size,
        sourceType: isPasted ? "paste" : "upload",
        dataUrl: base64Data
      });

      updateImageCounts();
      renderImageGallery();
    };
    reader.readAsDataURL(file);
  });

  if (rejected > 0) {
    showToast(`Bỏ qua ${rejected} ảnh. Tối đa ${MAX_IMAGES} ảnh, mỗi ảnh ${MAX_IMAGE_BYTES / 1024 / 1024} MB, tổng ${MAX_TOTAL_IMAGE_BYTES / 1024 / 1024} MB; chỉ nhận JPG, PNG, WebP hoặc GIF.`, "warning", 6000);
  }
}

// Xử lý mở tài liệu PDF và hiển thị modal chọn trang
async function handlePdfFile(file) {
  if (!window.pdfjsLib) {
    showToast("Thư viện PDF.js chưa sẵn sàng. Vui lòng kiểm tra kết nối mạng và thử lại.", "danger");
    return;
  }

  try {
    showToast(`Đang đọc file PDF: ${file.name}...`, "info");
    currentPdfFile = file;

    const arrayBuffer = await file.arrayBuffer();
    const loadingTask = window.pdfjsLib.getDocument({ data: arrayBuffer });
    currentPdfDoc = await loadingTask.promise;

    const totalPages = currentPdfDoc.numPages;
    const fileInfo = document.getElementById("pdfFileInfo");
    const pagesBadge = document.getElementById("pdfTotalPagesBadge");
    const radioAll = document.getElementById("pdfRadioAll");
    const inputRange = document.getElementById("inputPdfPageRange");
    const renderProgress = document.getElementById("pdfRenderProgress");
    const btnConfirm = document.getElementById("btnConfirmPdfPages");

    if (fileInfo) fileInfo.textContent = `📄 File: ${file.name} (${(file.size / 1024 / 1024).toFixed(2)} MB)`;
    if (pagesBadge) pagesBadge.textContent = `${totalPages} trang`;
    if (radioAll) radioAll.checked = true;
    if (inputRange) {
      inputRange.disabled = true;
      inputRange.value = "";
    }
    if (renderProgress) renderProgress.style.display = "none";
    if (btnConfirm) btnConfirm.disabled = false;

    openModal("modalPdfPageSelect");
  } catch (err) {
    console.error("Lỗi khi đọc file PDF:", err);
    showToast(`Không thể mở file PDF: ${err.message}`, "danger", 5000);
  }
}

// Phân tích chuỗi khoảng trang PDF người dùng nhập (ví dụ: "1-3, 5")
function parsePdfPageRanges(rangeStr, maxPages) {
  const pages = new Set();
  const parts = rangeStr.split(/[,;\s]+/);

  for (const part of parts) {
    if (!part) continue;
    if (part.includes("-")) {
      const [startStr, endStr] = part.split("-");
      const start = parseInt(startStr, 10);
      const end = parseInt(endStr, 10);
      if (!isNaN(start) && !isNaN(end)) {
        const min = Math.min(start, end);
        const max = Math.max(start, end);
        for (let p = min; p <= max; p++) {
          if (p >= 1 && p <= maxPages) {
            pages.add(p);
          }
        }
      }
    } else {
      const p = parseInt(part, 10);
      if (!isNaN(p) && p >= 1 && p <= maxPages) {
        pages.add(p);
      }
    }
  }

  return Array.from(pages).sort((a, b) => a - b);
}

// Khởi tạo các sự kiện trong Modal chọn trang PDF
function setupPdfModal() {
  const radioAll = document.getElementById("pdfRadioAll");
  const radioRange = document.getElementById("pdfRadioRange");
  const inputRange = document.getElementById("inputPdfPageRange");
  const btnConfirm = document.getElementById("btnConfirmPdfPages");

  if (radioAll && radioRange && inputRange) {
    radioAll.addEventListener("change", () => {
      if (radioAll.checked) {
        inputRange.disabled = true;
      }
    });
    radioRange.addEventListener("change", () => {
      if (radioRange.checked) {
        inputRange.disabled = false;
        inputRange.focus();
      }
    });
  }

  if (btnConfirm) {
    btnConfirm.addEventListener("click", handleConfirmPdfPages);
  }
}

// Xử lý nạp các trang PDF đã chọn thành ảnh JPG chất lượng cao
async function handleConfirmPdfPages() {
  if (!currentPdfDoc || !currentPdfFile) {
    showToast("Không tìm thấy tài liệu PDF để xử lý.", "warning");
    closeModal("modalPdfPageSelect");
    return;
  }

  const isAll = document.getElementById("pdfRadioAll").checked;
  const rangeStr = document.getElementById("inputPdfPageRange").value.trim();
  const totalPages = currentPdfDoc.numPages;

  let pagesToRender = [];
  if (isAll) {
    for (let i = 1; i <= totalPages; i++) pagesToRender.push(i);
  } else {
    if (!rangeStr) {
      showToast("Vui lòng nhập khoảng trang cần trích xuất (Ví dụ: 1-3 hoặc 1, 2, 4)!", "warning");
      document.getElementById("inputPdfPageRange").focus();
      return;
    }
    pagesToRender = parsePdfPageRanges(rangeStr, totalPages);
    if (pagesToRender.length === 0) {
      showToast(`Khoảng trang không hợp lệ. Vui lòng nhập từ 1 đến ${totalPages}.`, "warning");
      return;
    }
  }

  // Kiểm tra giới hạn số lượng ảnh
  const availableSlots = MAX_IMAGES - appState.images.length;
  if (pagesToRender.length > availableSlots) {
    if (availableSlots <= 0) {
      showToast(`Bộ sưu tập đã đủ ${MAX_IMAGES} ảnh. Hãy xóa bớt ảnh trước khi nạp thêm trang mới.`, "warning");
      closeModal("modalPdfPageSelect");
      return;
    }
    showToast(`Chỉ còn nạp thêm được ${availableSlots} ảnh nữa. Hệ thống sẽ lấy ${availableSlots} trang đầu tiên được chọn.`, "info", 5000);
    pagesToRender = pagesToRender.slice(0, availableSlots);
  }

  const btnConfirm = document.getElementById("btnConfirmPdfPages");
  const progressContainer = document.getElementById("pdfRenderProgress");
  const statusElem = document.getElementById("pdfRenderStatus");
  const percentElem = document.getElementById("pdfRenderPercent");
  const barElem = document.getElementById("pdfRenderProgressBar");

  btnConfirm.disabled = true;
  progressContainer.style.display = "block";

  try {
    for (let idx = 0; idx < pagesToRender.length; idx++) {
      const pageNum = pagesToRender[idx];
      const percent = Math.round(((idx + 1) / pagesToRender.length) * 100);
      statusElem.textContent = `Đang chuyển đổi trang ${pageNum} (${idx + 1}/${pagesToRender.length})...`;
      percentElem.textContent = `${percent}%`;
      barElem.style.width = `${percent}%`;

      const page = await currentPdfDoc.getPage(pageNum);
      const viewport = page.getViewport({ scale: 2.0 });
      const canvas = document.createElement("canvas");
      const ctx = canvas.getContext("2d");
      canvas.width = viewport.width;
      canvas.height = viewport.height;

      // Đổ nền trắng cho trang
      ctx.fillStyle = "#ffffff";
      ctx.fillRect(0, 0, canvas.width, canvas.height);

      await page.render({ canvasContext: ctx, viewport }).promise;
      const dataUrl = canvas.toDataURL("image/jpeg", 0.85);
      const pdfText = await extractPdfPageText(page);

      appState.images.push({
        id: "pdf_" + Date.now() + "_" + Math.random().toString(36).substr(2, 5),
        name: `[PDF Trang ${pageNum}] ${currentPdfFile.name}`,
        mimeType: "image/jpeg",
        size: Math.round(dataUrl.length * 0.75),
        sourceType: "pdf",
        pageNum: pageNum,
        dataUrl: dataUrl,
        pdfText
      });
    }

    updateImageCounts();
    renderImageGallery();
    closeModal("modalPdfPageSelect");
    showToast(`Đã nạp thành công ${pagesToRender.length} trang PDF thành ảnh chất lượng cao!`, "success");
    if (appState.activeTab !== "tabVision") {
      switchMainTab("tabVision");
    }
  } catch (err) {
    console.error("Lỗi khi chuyển PDF sang ảnh:", err);
    showToast(`Lỗi khi trích xuất trang PDF: ${err.message}`, "danger");
  } finally {
    btnConfirm.disabled = false;
    progressContainer.style.display = "none";
  }
}

function updateImageCounts() {
  const total = appState.images.length;
  document.getElementById("imgCountBadge").textContent = `${total} ảnh`;
}

function renderImageGallery() {
  const list = appState.images;
  const gallery = document.getElementById("imageGallery");
  gallery.innerHTML = "";

  if (list.length === 0) {
    gallery.innerHTML = `<p style="grid-column: 1/-1; text-align: center; color: var(--text-muted); font-size: 0.85rem; padding: 1rem;">Chưa có ảnh nào. Chụp ảnh trang SGK và nhấn Ctrl + V hoặc tải file Ảnh/PDF vào ô phía trên.</p>`;
    return;
  }

  list.forEach((img, idx) => {
    const card = document.createElement("div");
    card.className = "image-thumb-card";
    
    const image = document.createElement("img");
    image.src = img.dataUrl;
    image.alt = img.name;
    
    const badge = document.createElement("span");
    badge.className = "thumb-badge";
    if (img.sourceType === "pdf" || img.name.startsWith("[PDF")) {
      badge.classList.add("badge-pdf");
      badge.textContent = `📄 PDF Trang ${img.pageNum || (idx + 1)}`;
    } else if (img.sourceType === "paste" || img.name.startsWith("[Ảnh dán")) {
      badge.classList.add("badge-paste");
      badge.textContent = `📋 Dán Ctrl+V`;
    } else {
      badge.textContent = `Trang #${idx + 1}`;
    }

    const overlay = document.createElement("div");
    overlay.className = "thumb-overlay";
    
    const zoomButton = document.createElement("button");
    zoomButton.className = "thumb-btn";
    zoomButton.title = "Xem phóng to";
    zoomButton.textContent = "🔍";
    zoomButton.addEventListener("click", () => zoomImage(img.dataUrl, img.name));
    
    const deleteButton = document.createElement("button");
    deleteButton.className = "thumb-btn";
    deleteButton.title = "Xóa ảnh này";
    deleteButton.textContent = "🗑️";
    deleteButton.addEventListener("click", () => deleteImage(img.id));
    
    overlay.append(zoomButton, deleteButton);
    card.append(image, badge, overlay);
    gallery.appendChild(card);
  });
}

window.zoomImage = (src, title) => {
  document.getElementById("zoomImageSrc").src = src;
  document.getElementById("zoomImageTitle").textContent = title || "Xem ảnh chi tiết";
  openModal("modalImageZoom");
};

window.deleteImage = (imgId) => {
  appState.images = appState.images.filter(i => i.id !== imgId);
  updateImageCounts();
  renderImageGallery();
  showToast("Đã xóa 1 ảnh.", "info");
};

// =============================================================================
// KATEX & MARKDOWN PREVIEW ENGINE
// =============================================================================
function setupEditorPreviewSync(editorId, previewId, onSave) {
  const editor = document.getElementById(editorId);
  if (!editor) return;

  let debounceTimer = null;
  editor.addEventListener("input", () => {
    clearTimeout(debounceTimer);
    debounceTimer = setTimeout(() => {
      const val = editor.value;
      renderMathPreview(val, previewId);
      if (typeof onSave === "function") onSave(val);
    }, 300);
  });
}

function renderMathPreview(markdownText, targetElementId) {
  const container = document.getElementById(targetElementId);
  if (!container) return;

  if (!markdownText || !markdownText.trim()) {
    container.replaceChildren();
    const message = document.createElement("p");
    message.style.color = "var(--text-muted)";
    message.style.fontStyle = "italic";
    message.textContent = "Chưa có nội dung. Hãy tạo nội dung bằng AI hoặc nhập vào ô bên cạnh.";
    container.appendChild(message);
    return;
  }

  // 1. Phân tích Markdown sang HTML bằng Marked.js
  let html = "";
  if (window.marked) {
    const renderer = new window.marked.Renderer();
    renderer.html = rawHtml => escapeHtml(rawHtml);
    html = window.marked.parse(prepareLiteralListMarkers(markdownText), { breaks: true, gfm: true, renderer });
  } else {
    html = escapeHtml(markdownText).replace(/\n/g, "<br>");
  }

  const previewContent = sanitizePreviewHtml(html);
  applyLiteralListMarkers(previewContent);
  container.replaceChildren(previewContent);

  // 2. Render công thức Toán học bằng KaTeX Auto-Render
  if (window.renderMathInElement) {
    try {
      window.renderMathInElement(container, {
        delimiters: [
          { left: "$$", right: "$$", display: true },
          { left: "$", right: "$", display: false },
          { left: "\\(", right: "\\)", display: false },
          { left: "\\[", right: "\\]", display: true }
        ],
        throwOnError: false
      });
    } catch (e) {
      console.warn("KaTeX render error:", e);
    }
  }
}

const KHBD_MAJOR_LIST_MARKER = "[[KHBD_MAJOR_LIST_MARKER]]";
const KHBD_MINOR_LIST_MARKER = "[[KHBD_MINOR_LIST_MARKER]]";

function prepareLiteralListMarkers(markdownText) {
  let inCodeFence = false;
  return String(markdownText || "").split(/\r?\n/).map(line => {
    if (/^\s*```/.test(line)) {
      inCodeFence = !inCodeFence;
      return line;
    }
    if (inCodeFence) return line;
    if (/^\s*-\s+/.test(line)) return line.replace(/^(\s*)-\s+/, `$1- ${KHBD_MAJOR_LIST_MARKER} `);
    if (/^\s*\+\s+/.test(line)) return line.replace(/^(\s*)\+\s+/, `$1+ ${KHBD_MINOR_LIST_MARKER} `);
    return line;
  }).join("\n");
}

function applyLiteralListMarkers(documentFragment) {
  documentFragment.querySelectorAll("li").forEach(listItem => {
    const walker = document.createTreeWalker(listItem, NodeFilter.SHOW_TEXT);
    let textNode;
    while ((textNode = walker.nextNode())) {
      const marker = textNode.nodeValue.includes(KHBD_MAJOR_LIST_MARKER)
        ? KHBD_MAJOR_LIST_MARKER
        : textNode.nodeValue.includes(KHBD_MINOR_LIST_MARKER)
          ? KHBD_MINOR_LIST_MARKER
          : null;
      if (!marker) continue;
      const symbol = marker === KHBD_MAJOR_LIST_MARKER ? "-" : "+";
      textNode.nodeValue = textNode.nodeValue.replace(marker, "");
      listItem.style.listStyleType = "none";
      listItem.insertBefore(document.createTextNode(`${symbol} `), listItem.firstChild);
      break;
    }
  });
}

function escapeHtml(value) {
  const div = document.createElement("div");
  div.textContent = value;
  return div.innerHTML;
}

function sanitizePreviewHtml(html) {
  const allowedTags = new Set(["A", "B", "BLOCKQUOTE", "BR", "CODE", "DEL", "EM", "H1", "H2", "H3", "H4", "H5", "H6", "HR", "I", "LI", "OL", "P", "PRE", "STRONG", "TABLE", "TBODY", "TD", "TH", "THEAD", "TR", "UL"]);
  const documentFragment = document.createDocumentFragment();
  const parsed = new DOMParser().parseFromString(html, "text/html");
  const copyNode = (node) => {
    if (node.nodeType === Node.TEXT_NODE) return document.createTextNode(node.textContent);
    if (node.nodeType !== Node.ELEMENT_NODE || !allowedTags.has(node.tagName)) return document.createTextNode(node.textContent || "");
    const clean = document.createElement(node.tagName.toLowerCase());
    if (node.tagName === "A") {
      const href = node.getAttribute("href") || "";
      if (/^(https?:|mailto:)/i.test(href)) clean.href = href;
      clean.rel = "noopener noreferrer";
      clean.target = "_blank";
    }
    ["colspan", "rowspan"].forEach(attribute => {
      if (node.hasAttribute(attribute)) clean.setAttribute(attribute, node.getAttribute(attribute));
    });
    node.childNodes.forEach(child => clean.appendChild(copyNode(child)));
    return clean;
  };
  parsed.body.childNodes.forEach(node => documentFragment.appendChild(copyNode(node)));
  return documentFragment;
}

function togglePreviewPanel(button) {
  const editor = document.getElementById(button.dataset.target);
  const panel = editor?.closest(".panel-box")?.nextElementSibling;
  if (!panel) return;
  const isHidden = panel.hidden = !panel.hidden;
  button.innerHTML = isHidden ? "<i data-lucide=\"eye\"></i> Hiện xem trước" : "<i data-lucide=\"eye-off\"></i> Ẩn xem trước";
  initLucideIcons();
}

function renderAllTabsPreview() {
  renderMathPreview(appState.content.vision, "previewVision");
  renderMathPreview(appState.content.objectives, "previewObjectives");
  renderMathPreview(appState.content.materials, "previewMaterials");
  renderMathPreview(appState.content.activities[appState.activeActSubtab], "previewActivity");
}

// =============================================================================
// XEM TRƯỚC TOÀN BỘ GIÁO ÁN (TAB 5)
// =============================================================================
function getFullLessonPlanMarkdown(options = {}) {
  const topic = getTopicDisplayName();
  const subject = appState.subject || "TOÁN";
  const grade = appState.selectedGrade || "";
  const duration = appState.duration || "02 tiết";
  const c = appState.content;
  const actParts = [];
  ["A", "B", "C", "D"].forEach(k => {
    if (c.activities[k] && c.activities[k].trim()) actParts.push(c.activities[k].trim());
  });
  const fullActMarkdown = actParts.join("\n\n---\n\n");
  const body = [
    c.objectives || "*[Chưa tạo I. Mục tiêu]*",
    `\n---\n`,
    c.materials || "*[Chưa tạo II. Thiết bị dạy học và học liệu]*",
    `\n---\n`,
    `# III. TIẾN TRÌNH DẠY HỌC`,
    fullActMarkdown || "*[Chưa tạo các hoạt động dạy học III.A - D]*"
  ];
  if (options.includeHeader === false) return body.join("\n\n");
  const header = [
    `**TRƯỜNG:** ${appState.school || "................................................"}`,
    `**TỔ CHUYÊN MÔN:** ${appState.group || "................................"}`,
    `**HỌ VÀ TÊN GIÁO VIÊN:** ${appState.teacher || "................................"}`,
    `**Ngày soạn:** .../.../...  **Ngày dạy:** .../.../...`,
    ``,
    `# KẾ HOẠCH BÀI DẠY`,
    `**TÊN BÀI SOẠN:** ${topic.toUpperCase()}`,
    `**MÔN HỌC:** ${subject.toUpperCase()} - **LỚP:** ${grade}`,
    `**BỘ SÁCH:** SGK do giáo viên cung cấp`,
    `**THỜI LƯỢNG THỰC HIỆN:** ${duration}`,
    `\n---\n`
  ];
  return [...header, ...body].join("\n\n");
}

function renderFullLessonPreview() {
  const fullMd = getFullLessonPlanMarkdown();
  renderMathPreview(fullMd, "fullLessonPreview");
}

// =============================================================================
// CÁC HÀM SINH NỘI DUNG AI CHO TỪNG TAB
// =============================================================================
function buildPedagogicalContext() {
  const context = normalizeTeachingContext(appState.teachingContext);
  const enabledIntegrations = [];
  if (context.integrations.digital) enabledIntegrations.push("năng lực số");
  if (context.integrations.ai) enabledIntegrations.push("năng lực AI");
  if (context.integrations.foreignLanguage) enabledIntegrations.push("ngoại ngữ");
  if (context.integrations.inclusive) enabledIntegrations.push("hỗ trợ HS khuyết tật/hòa nhập");
  const classProfile = [...context.classProfileChoices, context.classProfileNote].filter(Boolean).join("; ");
  const support = [...context.supportChoices, context.supportNote].filter(Boolean).join("; ");
  const selectedStandards = context.standards.map(item => `${item.officialCode ? `${item.officialCode}: ` : "Miền NLS: "}${item.officialLabel}`).join("; ");
  const methodLabels = (context.methods || []).map(id => pedagogyLabel("methods", id));
  const activityLabels = (context.subjectActivities || []).map(id => pedagogyLabel("activities", id));
  const techniqueByPhase = ["A", "B", "C", "D"].map(phase => {
    const ids = context.phasePedagogy?.[phase]?.techniques || [];
    const labels = ids.map(id => pedagogyLabel("techniques", id));
    return labels.length ? `${phase}: ${labels.join(", ")}` : "";
  }).filter(Boolean);

  const subjectName = appState.subjectName || "Toán";
  const gradeLevel = getGradeLevelName(appState.selectedGrade);

  return `BỐI CẢNH VÀ RÀNG BUỘC SƯ PHẠM BẮT BUỘC:
- Môn học: ${subjectName} ${gradeLevel}; khối/lớp: ${appState.selectedGrade}; tên bài: ${getTopicDisplayName()}; thời lượng: ${appState.duration || "chưa xác định"}.
- Giới hạn năng lực & phẩm chất: Bài dạy 1–2 tiết CHỈ ĐƯỢC CHỌN 1–2 Năng lực chung, 2–3 Năng lực đặc thù nổi trội nhất (gắn với nhiệm vụ/sản phẩm cụ thể), 1–2 Phẩm chất có hành vi quan sát rõ. CẤM liệt kê dàn trải toàn bộ khung năng lực hay đủ 5 phẩm chất.
- Trình độ/đặc điểm lớp: ${classProfile || `Chưa cung cấp; thiết kế mức độ phù hợp học sinh ${gradeLevel} và có phân hóa vừa sức.`}
- Hỗ trợ chức năng được chọn: ${support || "Không có yêu cầu riêng được chọn."}
- Sĩ số: ${context.classSize}; mức sẵn sàng: ${context.readiness}; tổ chức: ${context.grouping}; điều kiện: ${Object.entries(context.facilities).filter(([, value]) => value).map(([key]) => key).join(", ") || "thiết bị cơ bản"}.
- Phương pháp dạy học được chọn: ${methodLabels.length ? methodLabels.join("; ") : `Chưa chọn; khi soạn chỉ được lấy 1–2 phương pháp phù hợp môn ${subjectName} lớp ${appState.selectedGrade} từ catalog, đúng nguyên nhãn, không bịa tên PPDH ngoài catalog.`}
- Kỹ thuật dạy học theo pha: ${techniqueByPhase.length ? techniqueByPhase.join(" | ") : "Chưa chọn; chỉ dùng kỹ thuật catalog đúng pha A–D phù hợp môn/lớp, đúng nhãn."}
- Hoạt động đặc thù môn học được chọn: ${activityLabels.length ? activityLabels.join("; ") : `Chưa chọn; chỉ dùng 1–2 hoạt động catalog phù hợp môn ${subjectName}.`}
- Yêu cầu/hoạt động đặc thù: ${context.specialRequirements || "Không có."}
- Chỉ được tích hợp các thành phần đã bật: ${enabledIntegrations.length ? enabledIntegrations.join("; ") : "không có thành phần tích hợp bổ sung"}.
- Chuẩn NLS/AI đã chọn (chỉ các mục chính thức): ${selectedStandards || "Không có"}. Một bài chỉ 2–3 miền NLS (TT 02/2025) và/hoặc 2–3 mã AI (QĐ 2422) đã chọn. CẤM bịa mã ngoài danh sách. Khi viết mục tiêu: chỉ mô tả năng lực một dòng, CẤM nhãn Biểu hiện / Nhiệm vụ / Minh chứng. AI chỉ hỗ trợ học ${subjectName}, có kiểm chứng của con người, không biến thành bài AI độc lập.
- Nếu một thành phần không được bật hoặc không được chọn ở trên, TUYỆT ĐỐI không tự thêm mục tiêu, hoạt động, học liệu, đánh giá hay nhiệm vụ liên quan đến thành phần đó. Ràng buộc này ưu tiên hơn mọi gợi ý chung trong mẫu prompt.`;
}

function buildPedagogicalPrompt(prompt) {
  // getPromptTemplate already appends context if provided, but some places might call this directly.
  return `${prompt}\n\n${PROMPTS.OUTPUT_CONTRACT}`;
}

function getGenerationPromptContext(params = {}) {
  if (hasAnalyzedLessonContent()) {
    ensurePedagogyFromLesson({ silent: true });
    ensureIntegrationStandards({ silent: true });
  }
  const prevActs = [];
  ["A", "B", "C", "D"].forEach(k => {
    if (appState.content.activities[k]) prevActs.push(appState.content.activities[k]);
  });
  
  return {
    subject: appState.selectedSubject,
    subjectName: appState.subjectName || 'Môn học',
    grade: appState.selectedGrade,
    gradeLevel: getGradeLevel(appState.selectedGrade),
    gradeLevelName: getGradeLevelName(appState.selectedGrade),
    topic: params.topic || getTopicDisplayName(),
    duration: appState.duration,
    competencies: getSubjectCompetencies(appState.selectedSubject),
    textbook_content: appState.content.vision || "",
    objectives_content: appState.content.objectives || "",
    activities_content: params.activitiesContent || prevActs.join("\n\n---\n\n"),
    yccd_official: typeof getOfficialYccd === "function" ? getOfficialYccd({
      subjectId: currentSubjectId(),
      grade: appState.selectedGrade,
      topic: params.topic || getTopicDisplayName(),
      visionText: appState.content.vision || ""
    }) : "",
    pedagogical_context: buildPedagogicalContext()
  };
}

function buildPhasePedagogyContext(phase) {
  const selected = appState.teachingContext.phasePedagogy?.[phase] || {};
  const techLabels = (selected.techniques || []).map(id => pedagogyLabel("techniques", id)).filter(Boolean);
  const activityLabels = (appState.teachingContext.subjectActivities || []).map(id => pedagogyLabel("activities", id)).filter(Boolean);
  const methodLabels = (appState.teachingContext.methods || []).map(id => pedagogyLabel("methods", id)).filter(Boolean);
  const parts = [];
  if (methodLabels.length) parts.push(`Phương pháp định hướng (không bắt phải xuất hiện mọi bảng): ${methodLabels.join("; ")}`);
  if (techLabels.length) parts.push(`Kỹ thuật bắt buộc của pha ${phase}: ${techLabels.join("; ")}. Mỗi kỹ thuật phải xuất hiện trong bảng d) Tổ chức thực hiện.`);
  if (activityLabels.length) parts.push(`Hoạt động đặc thù đã chọn: ${activityLabels.join("; ")}. Chỉ triển khai nếu phù hợp pha ${phase}.`);
  return parts.length
    ? `\nRÀNG BUỘC PHA ${phase}: ${parts.join(" ")} Không nêu kỹ thuật/hoạt động ngoài catalog như kỹ thuật chính thức.`
    : `\nRÀNG BUỘC PHA ${phase}: không có kỹ thuật pha được chọn; không tự gắn tên kỹ thuật chính thức ngoài catalog.`;
}

function assertPhasePedagogyOutput(phase, output) {
  const selected = appState.teachingContext.phasePedagogy?.[phase] || {};
  const labels = (selected.techniques || []).map(id => pedagogyLabel("techniques", id)).filter(Boolean);
  if (!labels.length) return;
  const tablePart = String(output || "").split("### d)")[1] || String(output || "");
  const missing = labels.filter(label => !tablePart.includes(label));
  if (missing.length) throw new Error(`Nội dung chưa triển khai đúng trong bảng tổ chức thực hiện: ${missing.join(", ")}. Nội dung chưa được lưu.`);
}

function normalizeGeminiLessonOutput(rawOutput) {
  let text = String(rawOutput || "").replace(/^\uFEFF/, "").trim();
  text = text.replace(/^```(?:markdown|md|text)?\s*\n?/i, "").replace(/\n?```\s*$/i, "").trim();
  const conversationalPrefix = /^(?:tuyệt vời[!,.…\s]*|xin chào(?:[^\n]*)|chào bạn(?:[^\n]*)|dưới đây(?:[^\n]*)|sau đây(?:[^\n]*)|tôi (?:sẽ|đã)(?:[^\n]*)|với vai trò(?:[^\n]*))\n+/i;
  while (conversationalPrefix.test(text)) text = text.replace(conversationalPrefix, "").trimStart();
  const opening = text.slice(0, 400);
  const hasResidualMeta = /(?:tuyệt vời|xin chào|chào bạn|dưới đây|sau đây|tôi (?:sẽ|đã)|với vai trò|mình sẽ)/i.test(opening) || /```/.test(text);
  return { text, valid: Boolean(text) && !hasResidualMeta };
}

async function guardGeminiLessonOutput(rawOutput, signal) {
  const normalized = normalizeGeminiLessonOutput(rawOutput);
  if (normalized.valid) return normalized.text;
  const repairPrompt = buildPedagogicalPrompt(`${PROMPTS.OUTPUT_REPAIR}\n\nNỘI DUNG CẦN SỬA:\n${normalized.text || String(rawOutput || "")}`);
  const repaired = await geminiAPI.generateContent(repairPrompt, [], getSystemRole(appState.selectedSubject, appState.selectedGrade), 0.2, signal);
  const repairedNormalized = normalizeGeminiLessonOutput(repaired);
  if (!repairedNormalized.valid) {
    throw new Error("Gemini vẫn trả lời kèm lời dẫn hoặc định dạng không hợp lệ; nội dung chưa được lưu. Vui lòng thử lại.");
  }
  return repairedNormalized.text;
}

async function extractPdfPageText(page) {
  const content = await page.getTextContent({ disableCombineTextItems: false });
  const items = (content.items || [])
    .filter(item => item && typeof item.str === "string" && item.str.trim())
    .map(item => {
      const t = item.transform || [1, 0, 0, 1, 0, 0];
      return { str: item.str, x: t[4], y: t[5], width: item.width || 0, height: item.height || 0 };
    })
    .sort((a, b) => (b.y - a.y) || (a.x - b.x));
  if (!items.length) return "";
  const lines = [];
  let current = { y: items[0].y, parts: [{ x: items[0].x, str: items[0].str, width: items[0].width }] };
  const lineTol = Math.max(3, (items[0].height || 10) * 0.45);
  items.slice(1).forEach(item => {
    if (Math.abs(item.y - current.y) > lineTol) {
      lines.push(current);
      current = { y: item.y, parts: [{ x: item.x, str: item.str, width: item.width }] };
    } else {
      current.parts.push({ x: item.x, str: item.str, width: item.width });
    }
  });
  lines.push(current);
  return lines.map(line => {
    const parts = line.parts.sort((a, b) => a.x - b.x);
    let out = parts[0].str;
    for (let i = 1; i < parts.length; i++) {
      const gap = parts[i].x - (parts[i - 1].x + parts[i - 1].width);
      out += gap > 2.5 ? " " : "";
      out += parts[i].str;
    }
    return out.replace(/\s+/g, " ").trim();
  }).filter(Boolean).join("\n");
}

function isGarbledTextbookText(text) {
  const s = String(text || "").trim();
  if (s.length < 80) return true;
  const vietHits = (s.match(/tập hợp|phần tử|học sinh|bài học|khái niệm|nhận biết|kí hiệu|thuộc|không thuộc|hình |luyện tập|của |và |các |một /gi) || []).length;
  const slash = (s.match(/\\/g) || []).length;
  const pipes = (s.match(/\|/g) || []).length;
  const singles = (s.match(/(^|\s)[^A-Za-zÀ-ỹ0-9\s]{0,2}[A-Za-zÀ-ỹ](\s|$)/g) || []).length;
  if (slash / s.length > 0.015) return true;
  if (pipes > 15 && vietHits < 6) return true;
  if (s.length > 250 && vietHits < 4) return true;
  if (singles > 25 && vietHits < 8) return true;
  return false;
}

function loadScriptOnce(src) {
  return new Promise((resolve, reject) => {
    if (document.querySelector(`script[src="${src}"]`)) {
      resolve();
      return;
    }
    const script = document.createElement("script");
    script.src = src;
    script.async = true;
    script.onload = () => resolve();
    script.onerror = () => reject(new Error("Không tải được thư viện OCR."));
    document.head.appendChild(script);
  });
}

async function ensureTesseract() {
  if (window.Tesseract) return window.Tesseract;
  await loadScriptOnce("https://cdn.jsdelivr.net/npm/tesseract.js@5/dist/tesseract.min.js");
  if (!window.Tesseract) throw new Error("Tesseract.js chưa sẵn sàng.");
  return window.Tesseract;
}

async function ocrImageDataUrl(dataUrl, onProgress, worker) {
  const ownWorker = !worker;
  const Tesseract = await ensureTesseract();
  const active = worker || await Tesseract.createWorker("vie+eng", 1, {
    logger: message => {
      if (typeof onProgress === "function" && message.status === "recognizing text") {
        onProgress(message.progress || 0);
      }
    }
  });
  try {
    const { data } = await active.recognize(dataUrl);
    return String(data?.text || "").trim();
  } finally {
    if (ownWorker) await active.terminate();
  }
}

async function extractTextbookLocally() {
  const images = appState.images || [];
  if (!images.length) throw new Error("Chưa có ảnh/trang SGK.");
  const needOcr = images.some(image => isGarbledTextbookText(image.pdfText || image.ocrText || "") || !(image.pdfText || "").trim());
  let worker = null;
  if (needOcr) {
    updateProgress(8, "Đang tải OCR tiếng Việt trên máy (không dùng Gemini)...");
    const Tesseract = await ensureTesseract();
    worker = await Tesseract.createWorker("vie+eng", 1, {
      logger: message => {
        if (message.status === "loading language traineddata") {
          updateProgress(10, "Đang tải gói ngôn ngữ OCR (lần đầu)...");
        }
      }
    });
  }
  const sections = [];
  try {
    for (let i = 0; i < images.length; i++) {
      const image = images[i];
      const title = image.pageNum ? `Trang PDF ${image.pageNum}` : (image.name || `Ảnh ${i + 1}`);
      updateProgress(Math.round(12 + (i / images.length) * 80), `Đang đọc ${title} (${i + 1}/${images.length})...`);
      let text = String(image.pdfText || "").trim();
      if ((!text || isGarbledTextbookText(text)) && image.sourceType === "pdf" && currentPdfDoc && image.pageNum) {
        try {
          const page = await currentPdfDoc.getPage(image.pageNum);
          const rebuilt = await extractPdfPageText(page);
          if (rebuilt && !isGarbledTextbookText(rebuilt)) {
            text = rebuilt;
            image.pdfText = rebuilt;
          }
        } catch (error) {
          console.warn("Không lấy được lớp chữ PDF:", error);
        }
      }
      if (isGarbledTextbookText(text) && image.dataUrl && worker) {
        text = await ocrImageDataUrl(image.dataUrl, progress => {
          const overall = Math.round(12 + ((i + progress) / images.length) * 80);
          updateProgress(overall, `OCR tiếng Việt ${title} (${i + 1}/${images.length})...`);
        }, worker);
        image.ocrText = text;
      }
      sections.push(`## ${title}\n\n${text || "[Không trích được chữ trên trang này]"}`);
    }
  } finally {
    if (worker) await worker.terminate();
  }
  return `# Nội dung SGK (trích cục bộ, không dùng Gemini)\n\n${sections.join("\n\n---\n\n")}`;
}

async function handleGenerateVision() {
  if (appState.images.length === 0) {
    showToast("Vui lòng dán hoặc chọn ít nhất 1 ảnh/trang SGK!", "warning");
    return;
  }
  if (appState.isGenerating) {
    showToast("Một tác vụ khác đang chạy, vui lòng chờ.", "warning");
    return;
  }

  const btn = document.getElementById("btnAnalyzeVision");
  try {
    appState.isGenerating = true;
    if (btn) btn.disabled = true;
    updateProgress(5, "Đang trích nội dung SGK trên máy (PDF chữ / OCR)...");
    const result = await extractTextbookLocally();
    appState.content.vision = result;
    const editor = document.getElementById("editorVision");
    if (editor) editor.value = result;
    renderMathPreview(result, "previewVision");
    saveStateToLocalStorage();
    updateProgress(100, "Đã trích nội dung SGK!");
    setTimeout(() => hideProgress(), 1200);
    showToast("Đã trích nội dung SGK trên máy, không dùng quota Gemini.", "success");
    applyLessonBasedRecommendations({ silent: false });
  } catch (error) {
    console.error(error);
    hideProgress();
    showToast(`Lỗi trích nội dung SGK: ${error.message}`, "danger", 6000);
  } finally {
    appState.isGenerating = false;
    if (btn) btn.disabled = false;
  }
}

function hasTextbookSource() {
  return (Array.isArray(appState.images) && appState.images.length > 0) || Boolean(String(appState.content.vision || "").trim());
}

function hasOfficialYccdSource() {
  if (typeof getOfficialYccd !== "function") return false;
  return Boolean(getOfficialYccd({
    subjectId: currentSubjectId(),
    grade: appState.selectedGrade,
    topic: getTopicDisplayName(),
    visionText: appState.content.vision || ""
  }).trim());
}

function hasLessonSource() {
  return hasTextbookSource() || hasOfficialYccdSource();
}

async function applyActivityOutput(actKey, result, signal) {
  let finalResult = result;
  try { assertPhasePedagogyOutput(actKey, finalResult); }
  catch (error) {
    const repair = await geminiAPI.generateContent(buildPedagogicalPrompt(`Sửa đúng một lần nội dung pha ${actKey} sau. Giữ Markdown KHBD, bổ sung các lựa chọn đã chọn vào bảng d) Tổ chức thực hiện với bước, vai trò, nhiệm vụ, sản phẩm/minh chứng; không thêm kỹ thuật không chọn.\n\n${finalResult}${buildPhasePedagogyContext(actKey)}`), [], getSystemRole(appState.selectedSubject, appState.selectedGrade), 0.2, signal);
    finalResult = await guardGeminiLessonOutput(repair, signal);
    assertPhasePedagogyOutput(actKey, finalResult);
  }
  appState.content.activities[actKey] = finalResult;
  saveStateToLocalStorage();
  return finalResult;
}

async function handleGenerateObjectives() {
  const context = getGenerationPromptContext();
  const prompt = getPromptTemplate('GENERATE_OBJECTIVES', context);

  await executeAIGeneration({
    buttonId: "btnGenerateObjectives",
    requireSource: true,
    targetEditorId: "editorObjectives",
    targetPreviewId: "previewObjectives",
    operationName: "Tạo I. Mục tiêu",
    prompt,
    onSuccess: (result) => {
      appState.content.objectives = result;
      saveStateToLocalStorage();
    }
  });
}

async function handleGenerateMaterials() {
  const context = getGenerationPromptContext();
  const prompt = getPromptTemplate('GENERATE_MATERIALS', context);

  await executeAIGeneration({
    buttonId: "btnGenerateMaterials",
    targetEditorId: "editorMaterials",
    targetPreviewId: "previewMaterials",
    operationName: "Tạo II. Thiết bị & Học liệu",
    prompt,
    onSuccess: (result) => {
      appState.content.materials = result;
      saveStateToLocalStorage();
    }
  });
}

async function handleGenerateCurrentActivity() {
  const actKey = appState.activeActSubtab;
  const actInfo = ACTIVITY_TITLES[actKey];
  
  if (!actInfo) return;

  const context = getGenerationPromptContext();
  const templateKey = `GENERATE_ACTIVITY_${actKey}`;
  const prompt = getPromptTemplate(templateKey, context) + buildPhasePedagogyContext(actKey);

  await executeAIGeneration({
    buttonId: "btnGenerateCurrentAct",
    targetEditorId: "editorActivity",
    targetPreviewId: "previewActivity",
    operationName: `Tạo ${actInfo.short}`,
    prompt,
    requireTextbook: true,
    onSuccess: async (result) => applyActivityOutput(actKey, result)
  });
}

/**
 * Hàm thực thi gọi AI tổng quát với giao diện khóa nút và hiển thị trạng thái
 */
async function executeAIGeneration({ buttonId, targetEditorId, targetPreviewId, operationName, prompt, images = [], onSuccess, requireTextbook = false, requireSource = false }) {
  if (requireTextbook && !hasTextbookSource()) {
    showToast("Cần dán ảnh/PDF SGK hoặc có nội dung phân tích Bước 0 trước khi soạn hoạt động. Không tự thêm nội dung ngoài nguồn.", "warning");
    return;
  }
  if (requireSource && !hasLessonSource()) {
    showToast("Cần nguồn bài học (ảnh SGK, phân tích Bước 0, hoặc YCCĐ TT 32). Không tự tạo mục tiêu kiến thức.", "warning");
    return;
  }
  const context = normalizeTeachingContext(appState.teachingContext);
  if (context.integrations.digital || context.integrations.ai) {
    ensureIntegrationStandards({ force: false });
    if (!standardsOfKind("digital").length && context.integrations.digital) {
      ensureIntegrationStandards({ force: true });
    }
    if (!standardsOfKind("ai").length && context.integrations.ai) {
      ensureIntegrationStandards({ force: true });
    }
  }
  if (appState.isGenerating) {
    showToast("Một tác vụ AI khác đang được xử lý, vui lòng chờ trong giây lát...", "warning");
    return;
  }

  const btn = document.getElementById(buttonId);
  const editor = document.getElementById(targetEditorId);

  try {
    appState.isGenerating = true;
    if (btn) btn.disabled = true;

    updateProgress(50, `Đang ${operationName}...`);
    document.getElementById("statusFooterText").textContent = `Đang ${operationName}...`;

    const rawResult = await geminiAPI.generateContent(buildPedagogicalPrompt(prompt), images, getSystemRole(appState.selectedSubject, appState.selectedGrade));
    const result = await guardGeminiLessonOutput(rawResult);

    let finalResult = result;
    if (typeof onSuccess === "function") {
      finalResult = (await onSuccess(result)) || result;
    }
    if (editor) editor.value = finalResult;
    if (targetPreviewId) renderMathPreview(finalResult, targetPreviewId);

    updateProgress(100, `Hoàn tất ${operationName}!`);
    setTimeout(() => hideProgress(), 1500);
    showToast(`Đã ${operationName} thành công!`, "success");
    document.getElementById("statusFooterText").textContent = `Sẵn sàng.`;

  } catch (error) {
    console.error(`Lỗi khi ${operationName}:`, error);
    showToast(`Lỗi khi ${operationName}: ${error.message}`, "danger", 6000);
    hideProgress();
    document.getElementById("statusFooterText").textContent = `Lỗi khi ${operationName}.`;
  } finally {
    appState.isGenerating = false;
    if (btn) btn.disabled = false;
  }
}

// =============================================================================
// QUY TRÌNH ⚡ TẠO TOÀN BỘ GIÁO ÁN (1-CLICK)
// =============================================================================
function requestGenerationCancel() {
  if (!appState.isGenerating || !appState.generationController) return;
  appState.cancelRequested = true;
  appState.generationController.abort();
  showToast("Đang hủy tác vụ AI sau yêu cầu hiện tại...", "info");
}

function throwIfGenerationCancelled() {
  if (appState.cancelRequested || appState.generationController?.signal.aborted) {
    throw new DOMException("Đã hủy theo yêu cầu của bạn.", "AbortError");
  }
}

async function generateOneClickContent(prompt, images = []) {
  throwIfGenerationCancelled();
  const rawResult = await geminiAPI.generateContent(buildPedagogicalPrompt(prompt), images, getSystemRole(appState.selectedSubject, appState.selectedGrade), 0.3, appState.generationController.signal);
  throwIfGenerationCancelled();
  const result = await guardGeminiLessonOutput(rawResult, appState.generationController.signal);
  throwIfGenerationCancelled();
  return result;
}

async function handle1ClickGenerate() {
  if (appState.isGenerating) {
    showToast("Tiến trình đang chạy. Vui lòng chờ hoàn tất.", "warning");
    return;
  }

  const keys = geminiAPI.apiKeys;
  if (!keys || keys.length === 0) {
    showToast("Vui lòng cài đặt ít nhất 1 Gemini API Key trước khi bắt đầu!", "warning");
    openModal("modalApiKeys");
    return;
  }
  if (!hasTextbookSource()) {
    showToast("Cần dán ảnh/PDF SGK hoặc có nội dung phân tích Bước 0 trước khi tạo toàn bộ giáo án. Không tự thêm nội dung ngoài nguồn.", "warning");
    switchMainTab("tabVision");
    return;
  }

  const topic = getTopicDisplayName();
  const confirmMsg = `Bạn có muốn bắt đầu TỰ ĐỘNG TẠO KẾ HOẠCH BÀI DẠY LÕI cho bài:\n"${topic}" (Lớp ${appState.selectedGrade})?\n\nTiến trình sẽ chạy tuần tự qua các mục I. Mục tiêu, II. Thiết bị & học liệu và III. Hoạt động A -> D.`;
  
  if (!confirm(confirmMsg)) return;

  appState.isGenerating = true;
  appState.cancelRequested = false;
  appState.generationController = new AbortController();

  const btn1Click = document.getElementById("btn1ClickGenerate");
  const btnCancel = document.getElementById("btnCancelGeneration");
  if (btn1Click) btn1Click.disabled = true;
  if (btnCancel) btnCancel.disabled = false;

  try {
    const context = getGenerationPromptContext();
    
    // BƯỚC 1: Trích nội dung SGK trên máy (không gọi Gemini)
    if (appState.images.length > 0 && !String(appState.content.vision || "").trim()) {
      updateProgress(10, "Bước 1/7: Đang trích nội dung SGK trên máy (không dùng Gemini)...");
      const resVision = await extractTextbookLocally();
      throwIfGenerationCancelled();
      appState.content.vision = resVision;
      document.getElementById("editorVision").value = resVision;
      renderMathPreview(resVision, "previewVision");
      saveStateToLocalStorage();
      await delay(400, appState.generationController.signal);
    }

    context.textbook_content = appState.content.vision || "";
    if (!context.textbook_content.trim()) {
      throw new Error("Chưa có nội dung SGK trong nguồn. Hãy phân tích ảnh/PDF trước.");
    }
    if (typeof getOfficialYccd === "function") {
      context.yccd_official = getOfficialYccd({
        subjectId: currentSubjectId(),
        grade: appState.selectedGrade,
        topic: getTopicDisplayName(),
        visionText: context.textbook_content
      });
    }
    applyLessonBasedRecommendations({ silent: true });
    Object.assign(context, getGenerationPromptContext());
    context.textbook_content = appState.content.vision || context.textbook_content;

    // BƯỚC 2: Tạo I. Mục tiêu
    updateProgress(25, "Bước 2/7: Đang tạo I. Mục tiêu bài học...");
    const promptObj = getPromptTemplate('GENERATE_OBJECTIVES', context);
    const resObj = await generateOneClickContent(promptObj);
    appState.content.objectives = resObj;
    document.getElementById("editorObjectives").value = resObj;
    renderMathPreview(resObj, "previewObjectives");
    await delay(800, appState.generationController.signal);
    context.objectives_content = resObj;

    // BƯỚC 3: Tạo II. Thiết bị dạy học và học liệu
    updateProgress(40, "Bước 3/7: Đang tạo II. Thiết bị dạy học & học liệu...");
    const promptMat = getPromptTemplate('GENERATE_MATERIALS', context);
    const resMat = await generateOneClickContent(promptMat);
    appState.content.materials = resMat;
    document.getElementById("editorMaterials").value = resMat;
    renderMathPreview(resMat, "previewMaterials");
    await delay(800, appState.generationController.signal);

    // BƯỚC 4: Tạo III.A Khởi động
    updateProgress(55, "Bước 4/7: Đang tạo III.A Hoạt động Mở đầu...");
    const promptA = getPromptTemplate('GENERATE_ACTIVITY_A', context) + buildPhasePedagogyContext('A');
    const resA = await generateOneClickContent(promptA);
    await applyActivityOutput("A", resA, appState.generationController.signal);
    await delay(800, appState.generationController.signal);

    // BƯỚC 5: Tạo III.B Hình thành kiến thức mới
    updateProgress(70, "Bước 5/7: Đang tạo III.B Hoạt động Hình thành kiến thức...");
    context.activities_content = appState.content.activities.A;
    const promptB = getPromptTemplate('GENERATE_ACTIVITY_B', context) + buildPhasePedagogyContext('B');
    const resB = await generateOneClickContent(promptB);
    await applyActivityOutput("B", resB, appState.generationController.signal);
    await delay(800, appState.generationController.signal);

    // BƯỚC 6: Tạo III.C Luyện tập
    updateProgress(82, "Bước 6/7: Đang tạo III.C Hoạt động Luyện tập...");
    context.activities_content = appState.content.activities.A + "\n\n---\n\n" + appState.content.activities.B;
    const promptC = getPromptTemplate('GENERATE_ACTIVITY_C', context) + buildPhasePedagogyContext('C');
    const resC = await generateOneClickContent(promptC);
    await applyActivityOutput("C", resC, appState.generationController.signal);
    await delay(800, appState.generationController.signal);

    // BƯỚC 7: Tạo III.D Vận dụng
    updateProgress(94, "Bước 7/7: Đang tạo III.D Hoạt động Vận dụng...");
    context.activities_content += "\n\n---\n\n" + appState.content.activities.C;
    const promptD = getPromptTemplate('GENERATE_ACTIVITY_D', context) + buildPhasePedagogyContext('D');
    const resD = await generateOneClickContent(promptD);
    await applyActivityOutput("D", resD, appState.generationController.signal);
    await delay(800, appState.generationController.signal);

    // Lưu toàn bộ vào localStorage
    saveStateToLocalStorage();

    // Cập nhật giao diện hoạt động hiện tại
    document.getElementById("editorActivity").value = appState.content.activities[appState.activeActSubtab];
    renderMathPreview(appState.content.activities[appState.activeActSubtab], "previewActivity");

    updateProgress(100, "🎉 ĐÃ TẠO XONG KẾ HOẠCH BÀI DẠY LÕI!");
    setTimeout(() => {
      hideProgress();
      switchMainTab("tabFullPreview");
      showToast("Kế hoạch bài dạy lõi I, II và III.A-D đã được tạo. Bạn có thể xuất Word.", "success", 6000);
    }, 1200);

  } catch (err) {
    console.error("Lỗi quy trình 1-Click:", err);
    const cancelled = err?.name === "AbortError" || appState.cancelRequested;
    showToast(cancelled ? "Đã hủy quá trình tạo tự động. Nội dung đã hoàn tất trước đó vẫn được giữ lại." : `Quá trình tạo tự động bị gián đoạn: ${err.message}`, cancelled ? "info" : "danger", 7000);
    hideProgress();
  } finally {
    appState.isGenerating = false;
    appState.generationController = null;
    if (btn1Click) btn1Click.disabled = false;
    if (btnCancel) btnCancel.disabled = true;
  }
}

function delay(ms, signal = null) {
  return new Promise((resolve, reject) => {
    const timer = setTimeout(resolve, ms);
    if (signal) signal.addEventListener("abort", () => {
      clearTimeout(timer);
      reject(new DOMException("Yêu cầu đã bị hủy.", "AbortError"));
    }, { once: true });
  });
}

// =============================================================================
// XUẤT FILE WORD (.DOCX)
// =============================================================================
async function exportTabDocx(title, markdownContent, defaultFileName) {
  if (!markdownContent || !markdownContent.trim()) {
    showToast("Mục này chưa có nội dung để xuất Word!", "warning");
    return;
  }

  try {
    showToast("Đang tạo file Word (.docx)...", "info");
    await docxGenerator.exportSingleTab(title, markdownContent, `${defaultFileName}.docx`);
    showToast("Đã xuất file Word thành công!", "success");
  } catch (e) {
    console.error("Lỗi xuất Word:", e);
    showToast(`Lỗi xuất file Word: ${e.message}`, "danger", 5000);
  }
}

async function handleExportFullDocx() {
  const fullMd = getFullLessonPlanMarkdown();
  if (!appState.content.objectives && !appState.content.activities.A) {
    showToast("Chưa có nội dung giáo án để xuất. Vui lòng tạo nội dung trước!", "warning");
    return;
  }

  const lessonInfo = {
    school: appState.school,
    subjectGroup: appState.group,
    teacher: appState.teacher,
    subject: appState.subject,
    topic: getTopicDisplayName(),
    grade: appState.selectedGrade,
    duration: appState.duration,
  };

  const fileName = `KHBD_${getSafeTopicName()}_${currentSubjectId() || "mon"}${appState.selectedGrade}.docx`;

  try {
    showToast("Đang biên soạn và định dạng toàn bộ Giáo án sang Word...", "info");
    await docxGenerator.exportFullLessonPlan(lessonInfo, getFullLessonPlanMarkdown({ includeHeader: false }), fileName);
    showToast("Đã xuất toàn bộ Giáo án thành công!", "success");
  } catch (e) {
    console.error("Lỗi xuất toàn bộ Giáo án:", e);
    showToast(`Lỗi khi xuất file Word: ${e.message}`, "danger", 5000);
  }
}

function handleCopyFullMarkdown() {
  const fullMd = getFullLessonPlanMarkdown();
  navigator.clipboard.writeText(fullMd).then(() => {
    showToast("Đã sao chép toàn bộ nội dung Markdown vào Clipboard!", "success");
  }).catch(() => {
    showToast("Không thể sao chép tự động. Vui lòng sao chép thủ công.", "warning");
  });
}

// =============================================================================
// XÓA TOÀN BỘ DỮ LIỆU (CÓ XÁC NHẬN)
// =============================================================================
function handleClearAllContent() {
  if (confirm("⚠️ CẢNH BÁO: Bạn có chắc chắn muốn xóa TOÀN BỘ nội dung giáo án đã soạn và ảnh đã tải lên không? Thao tác này không thể hoàn tác.")) {
    appState.content = {
      vision: "",
      objectives: "",
      materials: "",
      activities: {
        A: "", B: "", C: "", D: "",
        E: appState.content.activities.E || "",
        F: appState.content.activities.F || "",
        G: appState.content.activities.G || ""
      }
    };
    appState.images = [];

    document.getElementById("editorVision").value = "";
    document.getElementById("editorObjectives").value = "";
    document.getElementById("editorMaterials").value = "";
    document.getElementById("editorActivity").value = "";

    updateImageCounts();
    renderImageGallery();
    renderAllTabsPreview();
    renderFullLessonPreview();
    saveStateToLocalStorage();

    showToast("Đã xóa toàn bộ nội dung thành công!", "info");
  }
}

// =============================================================================
// PROGRESS BAR & TOAST NOTIFICATIONS
// =============================================================================
function updateProgress(percent, title) {
  const container = document.getElementById("progressContainer");
  const bar = document.getElementById("progressBarInner");
  const titleElem = document.getElementById("progressStepTitle");
  const percentElem = document.getElementById("progressPercent");

  if (container) container.style.display = "block";
  if (bar) bar.style.width = `${percent}%`;
  if (titleElem) titleElem.textContent = title;
  if (percentElem) percentElem.textContent = `${percent}%`;
}

function hideProgress() {
  const container = document.getElementById("progressContainer");
  if (container) container.style.display = "none";
}

function showToast(message, type = "info", duration = 3500) {
  const container = document.getElementById("toastContainer");
  if (!container) return;

  const toast = document.createElement("div");
  toast.className = `toast toast-${type}`;
  
  let icon = "ℹ️";
  if (type === "success") icon = "✅";
  if (type === "warning") icon = "⚠️";
  if (type === "danger") icon = "❌";

  const iconElement = document.createElement("span");
  iconElement.textContent = icon;
  const messageElement = document.createElement("span");
  messageElement.textContent = message;
  toast.append(iconElement, messageElement);
  container.appendChild(toast);

  setTimeout(() => {
    toast.style.opacity = "0";
    setTimeout(() => toast.remove(), 300);
  }, duration);
}

// =============================================================================
// MODAL MANAGEMENT & QUẢN LÝ API KEYS
// =============================================================================
function setupApiKeyModal() {
  document.getElementById("btnManageKeys").addEventListener("click", () => {
    document.getElementById("textareaApiKeys").value = geminiAPI.apiKeys.join("\n");
    document.getElementById("keyValidationStatus").textContent = "";
    openModal("modalApiKeys");
  });

  // Xử lý nạp file Keys (.txt)
  const fileInputTxt = document.getElementById("fileInputApiKeyTxt");
  if (fileInputTxt) {
    fileInputTxt.addEventListener("change", (e) => {
      const file = e.target.files?.[0];
      if (!file) return;

      const reader = new FileReader();
      reader.onload = async (event) => {
        const text = event.target.result || "";
        const keys = text
          .split(/[\r\n,;]+/)
          .map(k => k.trim())
          .filter(k => k.length > 10);

        if (keys.length === 0) {
          showToast("Không tìm thấy API Key hợp lệ (> 10 ký tự) trong file txt!", "warning");
          return;
        }

        const textarea = document.getElementById("textareaApiKeys");
        textarea.value = keys.join("\n");
        await geminiAPI.saveKeysToServer(keys);
        updateKeyCountDisplay();
        showToast(`Đã nạp và lưu ${keys.length} API Keys lên CSDL máy chủ!`, "success");
      };
      reader.readAsText(file);
      e.target.value = ""; // Reset
    });
  }

  document.getElementById("btnSaveApiKeys").addEventListener("click", async () => {
    const text = document.getElementById("textareaApiKeys").value;
    const lines = text.split(/\r?\n/).map(l => l.trim()).filter(l => l.length > 0);
    await geminiAPI.saveKeysToServer(lines);
    updateKeyCountDisplay();
    closeModal("modalApiKeys");
    if (geminiAPI.apiKeys.length > 0) {
      showToast(`Đã lưu ${geminiAPI.apiKeys.length} API Keys lên CSDL máy chủ!`, "success");
    } else {
      showToast(`Đã xóa danh sách API Keys trên CSDL`, "info");
    }
  });

  document.getElementById("btnTestApiKey").addEventListener("click", async () => {
    const text = document.getElementById("textareaApiKeys").value;
    const lines = text.split(/\r?\n/).map(l => l.trim()).filter(l => l.length > 0);
    const statusElem = document.getElementById("keyValidationStatus");

    if (lines.length === 0) {
      statusElem.textContent = "Chưa có key để kiểm tra!";
      statusElem.style.color = "var(--danger)";
      return;
    }

    statusElem.textContent = "Đang kiểm tra Key đầu tiên...";
    statusElem.style.color = "var(--primary)";

    try {
      await geminiAPI.testApiKey(lines[0], geminiAPI.selectedModel);
      statusElem.textContent = "✅ Key hợp lệ và hoạt động tốt!";
      statusElem.style.color = "var(--success)";
    } catch (e) {
      statusElem.textContent = `❌ Lỗi: ${e.message}`;
      statusElem.style.color = "var(--danger)";
    }
  });

  // Nút đóng modal chung
  document.querySelectorAll("[data-close-modal]").forEach(btn => {
    btn.addEventListener("click", () => {
      const modalId = btn.getAttribute("data-close-modal");
      closeModal(modalId);
    });
  });
}

function updateKeyCountDisplay() {
  const count = geminiAPI.apiKeys.length;
  const badge = document.getElementById("keyCountBadge");
  if (badge) badge.textContent = count;
}

function syncGeminiConfigToUI() {
  const modelSelect = document.getElementById("selectModel");
  const footerModel = document.getElementById("footerModelName");
  if (modelSelect) modelSelect.value = geminiAPI.selectedModel;
  if (footerModel) footerModel.textContent = geminiAPI.selectedModel;
}

function openModal(modalId) {
  const modal = document.getElementById(modalId);
  if (modal) modal.classList.add("active");
}

function closeModal(modalId) {
  const modal = document.getElementById(modalId);
  if (modal) modal.classList.remove("active");
}
