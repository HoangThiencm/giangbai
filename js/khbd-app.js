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

const MAX_IMAGE_BYTES = 5 * 1024 * 1024;
const MAX_TOTAL_IMAGE_BYTES = 25 * 1024 * 1024;
const VISION_BATCH_SIZE = 4;
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
    if (window.AiDesignConfig && typeof AiDesignConfig.loadHostingFallbackConfig === "function") {
      await AiDesignConfig.loadHostingFallbackConfig();
    }
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

function pedagogyCatalogItem(group, id) {
  const list = (typeof KHBD_PEDAGOGY_CATALOG !== "undefined" && KHBD_PEDAGOGY_CATALOG[group]) || [];
  return list.find(item => item.id === id || item.label === id) || null;
}

function pedagogyLabel(group, id) {
  return pedagogyCatalogItem(group, id)?.label || id;
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
  geminiAPI.onStatusCallback = (info) => {
    const waitSeconds = info?.waitSeconds;
    const text = info?.message || (waitSeconds
      ? `Đang chờ Gemini (quá tải), thử lại sau ${waitSeconds}s...`
      : "");
    if (!text) return;
    const statusEl = document.getElementById("statusFooterText");
    if (statusEl) statusEl.textContent = text;
    const container = document.getElementById("progressContainer");
    const titleElem = document.getElementById("progressStepTitle");
    if (container && container.style.display === "block" && titleElem) {
      titleElem.textContent = text;
    }
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
    const validPdf = pdfFiles.find(file => file.size <= MAX_IMAGE_BYTES);
    if (!validPdf) {
      showToast(`PDF vượt giới hạn ${MAX_IMAGE_BYTES / 1024 / 1024} MB/tệp.`, "warning");
    } else {
      handlePdfFile(validPdf);
    }
  }

  if (imgFiles.length === 0) return;

  const currentBytes = appState.images.reduce((total, image) => total + (image.size || 0), 0);
  let accepted = 0;
  let addedBytes = 0;
  let rejected = 0;

  imgFiles.forEach(file => {
    if (!ALLOWED_IMAGE_TYPES.has(file.type) || file.size > MAX_IMAGE_BYTES || currentBytes + addedBytes + file.size > MAX_TOTAL_IMAGE_BYTES) {
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
    showToast(`Bỏ qua ${rejected} tệp do không đúng định dạng, vượt ${MAX_IMAGE_BYTES / 1024 / 1024} MB/tệp hoặc vượt tổng ${MAX_TOTAL_IMAGE_BYTES / 1024 / 1024} MB.`, "warning", 6000);
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

      const renderedSize = Math.round(dataUrl.length * 0.75);
      const totalBytes = appState.images.reduce((sum, image) => sum + (image.size || 0), 0);
      if (totalBytes + renderedSize > MAX_TOTAL_IMAGE_BYTES) {
        showToast(`Trang ${pageNum} đã chuyển đổi nhưng không được giữ vì vượt tổng dung lượng an toàn.`, "warning", 4500);
        continue;
      }
      appState.images.push({
        id: "pdf_" + Date.now() + "_" + Math.random().toString(36).substr(2, 5),
        name: `[PDF Trang ${pageNum}] ${currentPdfFile.name}`,
        mimeType: "image/jpeg",
        size: renderedSize,
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
    renderer.html = rawHtml => allowPreviewBreakHtml(rawHtml);
    html = window.marked.parse(prepareLiteralListMarkers(markdownText), { breaks: true, gfm: true, renderer });
  } else {
    html = escapeHtml(markdownText).replace(/\n/g, "<br>");
  }

  const previewContent = sanitizePreviewHtml(html);
  applyLiteralListMarkers(previewContent);
  applyIntegrationPreviewColors(previewContent);
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
const KHBD_DETAIL_LIST_MARKER = "[[KHBD_DETAIL_LIST_MARKER]]";

function prepareLiteralListMarkers(markdownText) {
  let inCodeFence = false;
  return String(markdownText || "").split(/\r?\n/).map(line => {
    if (/^\s*```/.test(line)) {
      inCodeFence = !inCodeFence;
      return line;
    }
    if (inCodeFence) return line;
    const trimmedStart = line.trimStart();
    if (trimmedStart.startsWith("|")) return line;
    if (/^-\s+/.test(trimmedStart)) return trimmedStart.replace(/^-\s+/, `- ${KHBD_MAJOR_LIST_MARKER} `);
    if (/^\+\s+/.test(trimmedStart)) return trimmedStart.replace(/^\+\s+/, `  + ${KHBD_MINOR_LIST_MARKER} `);
    if (/^•\s+/.test(trimmedStart)) return trimmedStart.replace(/^•\s+/, `    - ${KHBD_DETAIL_LIST_MARKER} `);
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
          : textNode.nodeValue.includes(KHBD_DETAIL_LIST_MARKER)
            ? KHBD_DETAIL_LIST_MARKER
            : null;
      if (!marker) continue;
      const symbol = marker === KHBD_MAJOR_LIST_MARKER ? "-" : marker === KHBD_MINOR_LIST_MARKER ? "+" : "•";
      const className = marker === KHBD_MAJOR_LIST_MARKER
        ? "khbd-li-major"
        : marker === KHBD_MINOR_LIST_MARKER
          ? "khbd-li-minor"
          : "khbd-li-detail";
      textNode.nodeValue = textNode.nodeValue.replace(marker, "");
      listItem.classList.add(className);
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

function allowPreviewBreakHtml(rawHtml) {
  const placeholder = "[[KHBD_ALLOWED_BR]]";
  return String(rawHtml || "")
    .replace(/<br\s*\/?>/gi, placeholder)
    .split(placeholder)
    .map(part => escapeHtml(part))
    .join("<br>");
}

function isAllowedKhbdClass(value) {
  return /^khbd-(nls|ai)(?:\s+khbd-(nls|ai))?$/.test(String(value || "").trim());
}

function sanitizePreviewHtml(html) {
  const allowedTags = new Set(["A", "B", "BLOCKQUOTE", "BR", "CODE", "DEL", "EM", "H1", "H2", "H3", "H4", "H5", "H6", "HR", "I", "LI", "OL", "P", "PRE", "SPAN", "STRONG", "TABLE", "TBODY", "TD", "TH", "THEAD", "TR", "UL"]);
  const classTags = new Set(["H1", "H2", "H3", "H4", "H5", "H6", "P", "LI", "STRONG", "SPAN"]);
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
    if (classTags.has(node.tagName)) {
      const cls = (node.getAttribute("class") || "").trim();
      if (isAllowedKhbdClass(cls)) clean.setAttribute("class", cls);
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

function paintPreviewIntegrationNode(node, cls) {
  if (!node || node.nodeType !== Node.ELEMENT_NODE) return;
  if (["TABLE", "THEAD", "TBODY"].includes(node.tagName)) return;
  if (["P", "LI", "STRONG", "SPAN"].includes(node.tagName)) node.classList.add(cls);
  if (["UL", "OL", "DIV", "BLOCKQUOTE"].includes(node.tagName)) {
    node.querySelectorAll("p, li, strong, span").forEach(el => {
      if (!el.closest("table")) el.classList.add(cls);
    });
  }
}

function applyIntegrationSectionColors(fragment, heading, cls, kind) {
  heading.classList.add(cls);
  const rank = Number(heading.tagName.slice(1));
  let node = heading.nextElementSibling;
  while (node) {
    if (/^H[1-6]$/.test(node.tagName)) {
      const nextRank = Number(node.tagName.slice(1));
      const text = node.textContent || "";
      const sameKind = kind === "nls" ? /năng lực số/i.test(text) : /năng lực\s*AI/i.test(text);
      if (nextRank <= rank && !sameKind) break;
      if (nextRank <= rank) break;
    }
    paintPreviewIntegrationNode(node, cls);
    node = node.nextElementSibling;
  }
}

function applyIntegrationPreviewColors(fragment) {
  if (!fragment || typeof fragment.querySelectorAll !== "function") return fragment;
  fragment.querySelectorAll("h1, h2, h3, h4, h5, h6").forEach(heading => {
    const text = heading.textContent || "";
    if (/năng lực số/i.test(text)) applyIntegrationSectionColors(fragment, heading, "khbd-nls", "nls");
    else if (/năng lực\s*AI/i.test(text)) applyIntegrationSectionColors(fragment, heading, "khbd-ai", "ai");
  });

  const aiCodeRe = /\d+\.[A-Z]\d+\.\d+/;
  fragment.querySelectorAll("strong, li, p").forEach(el => {
    const text = el.textContent || "";
    const inTable = Boolean(el.closest("table"));
    const strongText = el.tagName === "STRONG" ? text.trim() : "";
    const hasNls = /\bNLS\b/.test(text) || /^NLS$/i.test(strongText);
    const hasAiMarker = /\bAI\b/.test(text) || /^AI$/i.test(strongText) || /năng lực\s*AI/i.test(text);
    const inAiContext = hasAiMarker || Boolean(el.closest(".khbd-ai"));
    if (hasNls) {
      el.classList.add("khbd-nls");
      if (!inTable) {
        const host = el.closest("li, p");
        if (host) host.classList.add("khbd-nls");
      }
    }
    if (hasAiMarker || (aiCodeRe.test(text) && inAiContext)) {
      el.classList.add("khbd-ai");
      if (!inTable && hasAiMarker) {
        const host = el.closest("li, p");
        if (host) host.classList.add("khbd-ai");
      }
    }
  });
  return fragment;
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
function getLessonPlanMetadata() {
  // Chưa có màn hình nhập metadata riêng, nên dùng đúng thông tin cố định của mẫu.
  return {
    dateDraft: ".../.../...",
    dateTeach: ".../.../..."
  };
}

function getFullLessonPlanMarkdown(options = {}) {
  const topic = getTopicDisplayName();
  const subject = appState.subject || "TOÁN";
  const grade = appState.selectedGrade || "";
  const duration = appState.duration || "02 tiết";
  const metadata = getLessonPlanMetadata();
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
    `**Ngày soạn:** ${metadata.dateDraft}`,
    `**Ngày dạy:** ${metadata.dateTeach}`,
    ``,
    `# KẾ HOẠCH BÀI DẠY`,
    `**TÊN BÀI SOẠN:** ${topic.toUpperCase()}`,
    `**MÔN HỌC:** ${subject.toUpperCase()} - **LỚP:** ${grade}`,
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
  const nlsLines = (context.standards || []).filter(item => !item.officialCode).map(item => `NLS: ${item.officialLabel}`);
  const aiLines = (context.standards || []).filter(item => item.officialCode).map(item => `AI: ${item.officialCode}: ${item.officialLabel}`);
  const selectedStandards = [...nlsLines, ...aiLines].join("\n  ");
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
- Chuẩn NLS/AI đã chọn (mỗi mục một dòng; PHẢI xuất hiện đủ trong I.2.c và I.2.d; không được bỏ miền/mã đã chọn):
  ${selectedStandards || "Không có"}
- CẤM bịa mã ngoài danh sách. Khi viết mục tiêu: chỉ mô tả năng lực một dòng, CẤM nhãn Biểu hiện / Nhiệm vụ / Minh chứng. AI chỉ hỗ trợ học ${subjectName}, có kiểm chứng của con người, không biến thành bài AI độc lập.
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
    textbook_content: resolveTextbookContent(),
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

function buildIntegrationActivityConstraint(phase) {
  const context = normalizeTeachingContext(appState.teachingContext);
  const digitalOn = Boolean(context.integrations.digital);
  const aiOn = Boolean(context.integrations.ai);
  if (!digitalOn && !aiOn) return "";
  const nls = standardsOfKind("digital").map(item => item.officialLabel).filter(Boolean);
  const ai = standardsOfKind("ai").map(item => item.officialCode ? `${item.officialCode}: ${item.officialLabel}` : item.officialLabel).filter(Boolean);
  const lines = [
    `TÍCH HỢP NLS/AI PHA ${phase}: lồng vào cách tổ chức bài/câu đã có trong SGK; CẤM bịa đề/số liệu mới; CẤM HTML/span/style/màu; dùng marker markdown **NLS** và **AI** trước nhiệm vụ tích hợp.`
  ];
  if (phase === "A") {
    if (digitalOn) lines.push(`NLS đã chọn: ${nls.join("; ") || "năng lực số"}. Thêm 1 móc ngắn (không bắt đủ mọi miền).`);
    if (aiOn) lines.push(`AI đã chọn: ${ai.join("; ") || "năng lực AI"}. Thêm 1 móc ngắn (không bắt đủ mọi mã).`);
  } else {
    if (digitalOn) {
      lines.push(`NLS đã chọn: ${nls.join("; ") || "năng lực số"}. Mỗi pha B/C/D phải có ÍT NHẤT một nhiệm vụ GV VÀ một nhiệm vụ HS gắn NLS trên bài SGK (ưu tiên miền đã chọn).`);
    }
    if (aiOn) {
      lines.push(`AI đã chọn: ${ai.join("; ") || "năng lực AI"}. Mỗi pha B/C/D phải có ÍT NHẤT một nhiệm vụ GV VÀ HS gắn AI (ưu tiên mã đã chọn: kiểm chứng kết quả AI, hậu quả không xác thực, rủi ro lạm dụng).`);
    }
  }
  return `\n${lines.join(" ")}`;
}

function buildPhasePedagogyContext(phase) {
  const selected = appState.teachingContext.phasePedagogy?.[phase] || {};
  const techItems = (selected.techniques || []).map(id => pedagogyCatalogItem("techniques", id) || { id, label: pedagogyLabel("techniques", id), description: "" });
  const activityLabels = (appState.teachingContext.subjectActivities || []).map(id => pedagogyLabel("activities", id)).filter(Boolean);
  const methodItems = (appState.teachingContext.methods || []).map(id => pedagogyCatalogItem("methods", id) || { id, label: pedagogyLabel("methods", id), description: "" });
  const parts = [];

  // Nhúng kịch bản sư phạm thực chiến chuẩn từ catalog
  const pedagogyGuide = typeof buildDetailedPedagogyGuide === "function"
    ? buildDetailedPedagogyGuide(phase, appState.teachingContext)
    : "";

  if (methodItems.length) {
    parts.push(`PPDH đã chọn: ${methodItems.map(item => `${item.label}${item.description ? ` — ${item.description}` : ""}`).join("; ")}. Nêu cách vận hành ngắn trong Bước 1–2 nếu phù hợp pha ${phase}.`);
  }
  if (techItems.length) {
    parts.push(`Kỹ thuật bắt buộc của pha ${phase} (CẤM chỉ liệt kê tên): ${techItems.map(item => `${item.label}${item.description ? ` — ${item.description}` : ""}`).join("; ")}. Cột TRÁI bảng d): nêu TÊN kỹ thuật và viết CÁCH TIẾN HÀNH theo đúng 4 bước CV 5512.`);
  }
  if (activityLabels.length) parts.push(`Hoạt động đặc thù đã chọn: ${activityLabels.join("; ")}. Chỉ triển khai nếu phù hợp pha ${phase}.`);

  const scriptRequirement = `\nYÊU CẦU KỊCH BẢN THỰC CHIẾN CỘT TRÁI BẢNG d) (Pha ${phase}):
- Bắt buộc đủ 4 bước CV 5512 (ngăn các bước bằng <br>):
  + **GV:** Nói câu gì cụ thể trong ngoặc kép "..." (câu lệnh giao nhiệm vụ, câu hỏi dẫn dắt, câu hỏi gợi mở, câu hỏi phân hóa); Làm gì cụ thể (phát đồ dùng/phiếu học tập, chia nhóm, quan sát phát hiện lỗi sai điển hình: ..., can thiệp hỗ trợ phân hóa).
  + **HS:** Làm gì cụ thể theo từng pha (thao tác cá nhân X phút vào nháp/phiếu -> thảo luận cặp/nhóm Y phút -> tạo sản phẩm trung gian: bảng phụ, sơ đồ, phiếu học tập, sticky note...); Báo cáo và phản biện thế nào.
- CỘT PHẢI BẢNG d): Chỉ ghi kiến thức chốt cho HS chép vào vở (định nghĩa, công thức LaTeX, ví dụ mẫu). CẤM mô tả việc GV/HS ở cột phải.`;

  const integration = buildIntegrationActivityConstraint(phase);
  const base = parts.length
    ? `\nRÀNG BUỘC PHA ${phase}: ${parts.join(" ")} Không nêu kỹ thuật/hoạt động ngoài catalog như kỹ thuật chính thức.`
    : `\nRÀNG BUỘC PHA ${phase}: không có kỹ thuật pha được chọn; không tự gắn tên kỹ thuật chính thức ngoài catalog.`;
  return base + (pedagogyGuide ? `\n${pedagogyGuide}` : "") + scriptRequirement + integration;
}

function pedagogyLabelInText(haystack, label) {
  const fold = value => String(value || "").toLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g, "").replace(/[^a-z0-9]+/g, " ").trim();
  const hay = fold(haystack);
  if (!hay) return false;
  if (hay.includes(fold(label))) return true;
  return String(label).split(/[\/()–—-]+/).map(fold).filter(part => part.length >= 5).some(part => hay.includes(part));
}

function assertPhasePedagogyOutput(phase, output) {
  const text = String(output || "");
  const selected = appState.teachingContext.phasePedagogy?.[phase] || {};
  const labels = (selected.techniques || []).map(id => pedagogyLabel("techniques", id)).filter(Boolean);
  const tablePart = text.split("### d)")[1] || text;

  // 1. Kiểm tra kỹ thuật đã chọn
  if (labels.length) {
    const missing = labels.filter(label => !pedagogyLabelInText(tablePart, label) && !pedagogyLabelInText(text, label));
    if (missing.length) throw new Error(`Nội dung chưa triển khai đúng trong bảng tổ chức thực hiện: ${missing.join(", ")}.`);
  }

  // 2. Kiểm tra đủ 4 bước CV 5512
  const hasStep1 = /bước\s*1|chuyển giao/i.test(tablePart);
  const hasStep2 = /bước\s*2|thực hiện/i.test(tablePart);
  const hasStep3 = /bước\s*3|báo cáo|thảo luận/i.test(tablePart);
  const hasStep4 = /bước\s*4|kết luận|nhận định/i.test(tablePart);
  if (!hasStep1 || !hasStep2 || !hasStep3 || !hasStep4) {
    throw new Error("Bảng tổ chức thực hiện chưa có đủ 4 bước (Bước 1: Chuyển giao -> Bước 2: Thực hiện -> Bước 3: Báo cáo -> Bước 4: Kết luận).");
  }

  // 3. Kiểm tra phân vai GV và HS
  const hasGv = /(?:\bGV\b|giáo viên)/i.test(tablePart);
  const hasHs = /(?:\bHS\b|học sinh)/i.test(tablePart);
  if (!hasGv || !hasHs) {
    throw new Error("Bảng tổ chức thực hiện chưa phân định rõ ràng vai trò GV (câu nói, hành động) và HS (cá nhân, nhóm, sản phẩm).");
  }
}

function assertObjectivesStandards(text) {
  const hay = String(text || "");
  const missing = [];
  standardsOfKind("digital").forEach(item => {
    if (!pedagogyLabelInText(hay, item.officialLabel)) missing.push({ kind: "digital", item });
  });
  standardsOfKind("ai").forEach(item => {
    const code = String(item.officialCode || "");
    if (!code || !hay.includes(code)) missing.push({ kind: "ai", item });
  });
  return missing;
}

function upsertObjectivesStandardSection(markdown, { matchRe, headingLine, bulletLines }) {
  const lines = String(markdown || "").split("\n");
  let headingIdx = lines.findIndex(line => matchRe.test(line.trim()));
  if (headingIdx < 0) {
    let insertAt = lines.findIndex(line => /^##\s*3(\.|[\s:]|$)/.test(line.trim()));
    if (insertAt < 0) insertAt = lines.length;
    const block = [headingLine, ...bulletLines, ""];
    lines.splice(insertAt, 0, ...block);
    return lines.join("\n");
  }
  const level = (lines[headingIdx].trim().match(/^#+/) || ["###"])[0].length;
  let end = headingIdx + 1;
  while (end < lines.length) {
    const m = lines[end].trim().match(/^(#{1,6})\s+/);
    if (m && m[1].length <= level) break;
    end++;
  }
  const sectionText = lines.slice(headingIdx, end).join("\n");
  const extras = bulletLines.filter(line => {
    const key = line.replace(/^\-\s+/, "").split(":")[0].trim();
    return key && !pedagogyLabelInText(sectionText, key) && !sectionText.includes(key);
  });
  if (extras.length) lines.splice(end, 0, ...extras);
  return lines.join("\n");
}

function insertObjectivesMissingStandards(text, missing) {
  let result = String(text || "");
  const digital = missing.filter(row => row.kind === "digital");
  const ai = missing.filter(row => row.kind === "ai");
  if (digital.length) {
    result = upsertObjectivesStandardSection(result, {
      matchRe: /^#{1,6}\s*(?:[a-z]\)\s*)?năng lực số\b/i,
      headingLine: "### c) Năng lực số",
      bulletLines: digital.map(row => `- ${row.item.officialLabel}: ${row.item.officialLabel}`)
    });
  }
  if (ai.length) {
    result = upsertObjectivesStandardSection(result, {
      matchRe: /^#{1,6}\s*(?:[a-z]\)\s*)?năng lực\s*AI\b/i,
      headingLine: "### d) Năng lực AI",
      bulletLines: ai.map(row => `- ${row.item.officialCode}: ${row.item.officialLabel}`)
    });
  }
  return result;
}

function hasRoleNearMarker(text, markerRe) {
  const hay = String(text || "");
  const match = markerRe.exec(hay);
  if (!match) return /(?:\bGV\b|giáo viên)/i.test(hay) && /(?:\bHS\b|học sinh)/i.test(hay);
  const start = Math.max(0, match.index - 600);
  const end = Math.min(hay.length, match.index + match[0].length + 600);
  const window = hay.slice(start, end);
  return /(?:\bGV\b|giáo viên)/i.test(window) && /(?:\bHS\b|học sinh)/i.test(window);
}

function assertActivityIntegrations(phase, text) {
  const context = normalizeTeachingContext(appState.teachingContext);
  const digitalOn = Boolean(context.integrations.digital);
  const aiOn = Boolean(context.integrations.ai);
  if (!digitalOn && !aiOn) return;
  const raw = String(text || "");
  const nlsOk = /\*\*NLS\*\*|\bNLS\b/.test(raw) || standardsOfKind("digital").some(item => pedagogyLabelInText(raw, item.officialLabel));
  const aiOk = /\*\*AI\*\*/.test(raw) || standardsOfKind("ai").some(item => item.officialCode && raw.includes(item.officialCode));
  if (phase === "A") {
    if (digitalOn && !nlsOk && !/năng lực số/i.test(raw)) throw new Error("Pha A chưa có móc NLS.");
    if (aiOn && !aiOk && !/\bAI\b|năng lực\s*AI/i.test(raw)) throw new Error("Pha A chưa có móc AI.");
    return;
  }
  if (digitalOn && !nlsOk) throw new Error("Chưa có nhiệm vụ NLS.");
  if (aiOn && !aiOk) throw new Error("Chưa có nhiệm vụ AI.");
  if (digitalOn && nlsOk && !hasRoleNearMarker(raw, /\*\*NLS\*\*|\bNLS\b|năng lực số/i)) {
    throw new Error("NLS chưa gắn nhiệm vụ GV và HS.");
  }
  if (aiOn && aiOk && !hasRoleNearMarker(raw, /\*\*AI\*\*|năng lực\s*AI|\d+\.[A-Z]\d+\.\d+/i)) {
    throw new Error("AI chưa gắn nhiệm vụ GV và HS.");
  }
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

function compressDataUrl(dataUrl, maxEdge = 1280, quality = 0.72) {
  return new Promise(resolve => {
    const img = new Image();
    img.onload = () => {
      const scale = Math.min(1, maxEdge / Math.max(img.width || 1, img.height || 1));
      const width = Math.max(1, Math.round(img.width * scale));
      const height = Math.max(1, Math.round(img.height * scale));
      const canvas = document.createElement("canvas");
      canvas.width = width;
      canvas.height = height;
      const ctx = canvas.getContext("2d");
      ctx.fillStyle = "#ffffff";
      ctx.fillRect(0, 0, width, height);
      ctx.drawImage(img, 0, 0, width, height);
      resolve({ dataUrl: canvas.toDataURL("image/jpeg", quality), mimeType: "image/jpeg" });
    };
    img.onerror = () => resolve({ dataUrl, mimeType: "image/jpeg" });
    img.src = dataUrl;
  });
}

function chunkVisionPages(pages, batchSize = VISION_BATCH_SIZE) {
  const batches = [];
  for (let index = 0; index < pages.length; index += batchSize) batches.push(pages.slice(index, index + batchSize));
  return batches;
}

async function prepareVisionImages(source = appState.images || []) {
  const prepared = [];
  for (const image of source) {
    if (!image.dataUrl) continue;
    const compressed = await compressDataUrl(image.dataUrl);
    prepared.push({
      mimeType: compressed.mimeType,
      dataUrl: compressed.dataUrl
    });
  }
  return prepared;
}

function buildVisionPdfTextBlock(source = appState.images || []) {
  if (!source.length) return "";
  const pages = [];
  for (const image of source) {
    const text = String(image.pdfText || "").trim();
    if (!text) return "";
    pages.push({ pageNum: image.pageNum, text });
  }
  const combined = pages.map(p => p.text).join("\n\n");
  if (isGarbledTextbookText(combined)) return "";
  const body = pages.map((p, i) => {
    const n = p.pageNum != null ? p.pageNum : (i + 1);
    return `--- Trang ${n} ---\n${p.text}`;
  }).join("\n\n");
  return `NỘI DUNG CHỮ TRÍCH TỪ PDF (không gửi ảnh vì PDF có chữ rõ):\n"""\n${body}\n"""`;
}

function collectPdfTextbookText() {
  const source = appState.images || [];
  const pages = [];
  for (const image of source) {
    const text = String(image.pdfText || "").trim();
    if (!text || isGarbledTextbookText(text)) continue;
    const n = image.pageNum != null ? image.pageNum : (pages.length + 1);
    pages.push(`--- Trang ${n} ---\n${text}`);
  }
  return pages.join("\n\n");
}

function visionHasExerciseMaterial(vision) {
  const s = String(vision || "");
  return /\bbài\s*\d+|\bcâu\s*\d+|luyện tập\s*[:.\-].{8,}|vận dụng\s*[:.\-].{8,}/i.test(s);
}

function resolveTextbookContent() {
  const vision = String(appState.content.vision || "").trim();
  const pdfText = collectPdfTextbookText();
  if (vision.length > 2500 && visionHasExerciseMaterial(vision)) return vision;
  if (pdfText) {
    const sample = pdfText.slice(0, Math.min(80, pdfText.length));
    if (vision && sample && vision.includes(sample)) return vision;
    if (vision) return `${vision}\n\nNỘI DUNG CHỮ TRÍCH TỪ PDF:\n"""\n${pdfText}\n"""`;
    return pdfText;
  }
  return vision;
}

async function resolveVisionRequest(basePrompt, source = appState.images || []) {
  const pdfBlock = buildVisionPdfTextBlock(source);
  if (pdfBlock) {
    return { prompt: `${basePrompt}\n\n${pdfBlock}`, images: [], usedPdfText: true };
  }
  return { prompt: basePrompt, images: await prepareVisionImages(source), usedPdfText: false };
}

async function analyzeTextbookInBatches(basePrompt, { signal = null, onProgress = null } = {}) {
  const batches = chunkVisionPages(appState.images || []);
  const results = [];
  for (let index = 0; index < batches.length; index++) {
    if (signal?.aborted) throw new DOMException("Đã hủy theo yêu cầu của bạn.", "AbortError");
    const request = await resolveVisionRequest(basePrompt, batches[index]);
    if (onProgress) onProgress(index + 1, batches.length, request.usedPdfText);
    const raw = await geminiAPI.generateContent(
      buildPedagogicalPrompt(`${request.prompt}\n\nĐợt trang ${index + 1}/${batches.length}: chỉ phân tích các trang của đợt này.`),
      request.images,
      getSystemRole(appState.selectedSubject, appState.selectedGrade),
      0.2,
      signal,
      { maxOutputTokens: 4096 }
    );
    if (signal?.aborted) throw new DOMException("Đã hủy theo yêu cầu của bạn.", "AbortError");
    results.push(normalizeGeminiLessonOutput(raw).text || raw);
  }
  return results.join("\n\n---\n\n");
}

function generationPauseMs() {
  return 1500;
}

function isGeminiOverloadError(error) {
  return /503|high demand/i.test(String(error?.message || error || ""));
}

async function handleGenerateVision() {
  if (appState.images.length === 0) {
    showToast("Vui lòng dán hoặc chọn ít nhất 1 ảnh/trang SGK!", "warning");
    return;
  }
  if (String(appState.content.vision || "").trim().length >= 80) {
    if (!confirm("Đã có nội dung phân tích SGK. Đọc lại sẽ tốn hạn mức Gemini. Tiếp tục?")) return;
  }
  const context = getGenerationPromptContext();
  await executeAIGeneration({
    buttonId: "btnAnalyzeVision",
    targetEditorId: "editorVision",
    targetPreviewId: "previewVision",
    operationName: "Đọc nội dung SGK",
    prompt: getPromptTemplate("ANALYZE_TEXTBOOK", context),
    skipGuard: true,
    visionBatches: true,
    maxOutputTokens: 4096,
    onSuccess: (result) => {
      appState.content.vision = result;
      saveStateToLocalStorage();
      applyLessonBasedRecommendations({ silent: false });
    }
  });
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

function activityOutputProblem(actKey, output) {
  try { assertPhasePedagogyOutput(actKey, output); }
  catch (error) { return error; }
  try { assertActivityIntegrations(actKey, output); }
  catch (error) { return error; }
  return null;
}

async function applyActivityOutput(actKey, result, signal) {
  let finalResult = result;
  let problem = activityOutputProblem(actKey, finalResult);
  if (problem) {
    try {
      const repairPrompt = buildPedagogicalPrompt(`Sửa đúng một lần nội dung pha ${actKey} sau thành Kịch bản Sư phạm Thực chiến chuẩn CV 5512.
Giữ nguyên định dạng Markdown KHBD và bảng 2 cột mục d).
Yêu cầu sửa:
- Cột TRÁI bảng d): Bắt buộc đủ 4 bước (ngăn bằng <br>), phân định rõ vai trò **GV:** (nói câu cụ thể trong ngoặc kép "...", hành động cụ thể, phát hiện lỗi sai điển hình, can thiệp phân hóa) và **HS:** (làm việc cá nhân -> thảo luận nhóm -> tạo sản phẩm trung gian, báo cáo và phản biện) theo đúng kỹ thuật dạy học đã chọn.
- Cột PHẢI bảng d): Chỉ ghi nội dung bảng/vở chốt cho HS chép (công thức LaTeX, định nghĩa, ví dụ). CẤM mô tả việc GV/HS ở cột phải.
- Nếu bật NLS/AI: lồng nhiệm vụ GV và HS với marker **NLS** / **AI** vào bài SGK đã có; CẤM bịa đề/số liệu mới; CẤM HTML/span/style/màu.
Lỗi cần sửa: ${problem.message}

${finalResult}${buildPhasePedagogyContext(actKey)}`);

      const repair = await geminiAPI.generateContent(repairPrompt, [], getSystemRole(appState.selectedSubject, appState.selectedGrade), 0.2, signal);
      finalResult = await guardGeminiLessonOutput(repair, signal);
      problem = activityOutputProblem(actKey, finalResult);
    } catch (repairError) {
      console.warn(`Giữ nội dung pha ${actKey} dù kỹ thuật/tích hợp chưa khớp đủ:`, repairError);
      problem = repairError;
    }
  }
  if (problem) {
    showToast(`Đã lưu hoạt động ${actKey}; kịch bản phân vai GV-HS hoặc kỹ thuật dạy học chưa ghi đủ. Bạn có thể sửa tay.`, "warning", 5000);
  }
  appState.content.activities[actKey] = finalResult;
  saveStateToLocalStorage();
  return finalResult;
}

async function applyObjectivesOutput(result, signal) {
  let finalResult = result;
  let missing = assertObjectivesStandards(finalResult);
  if (missing.length) {
    try {
      const missingDesc = missing.map(row => row.kind === "ai"
        ? `${row.item.officialCode}: ${row.item.officialLabel}`
        : row.item.officialLabel).join("; ");
      const repair = await geminiAPI.generateContent(buildPedagogicalPrompt(`Sửa đúng một lần phần I. Mục tiêu sau. Giữ nguyên Markdown và các dòng đã có. Chỉ bổ sung đúng các dòng còn thiếu vào ### c) Năng lực số / ### d) Năng lực AI. CẤM xóa dòng đã có. CẤM HTML/span/style/màu. Các mục còn thiếu: ${missingDesc}\n\n${finalResult}`), [], getSystemRole(appState.selectedSubject, appState.selectedGrade), 0.2, signal);
      finalResult = await guardGeminiLessonOutput(repair, signal);
      missing = assertObjectivesStandards(finalResult);
    } catch (error) {
      console.warn("Repair mục tiêu NLS/AI thất bại, sẽ chèn programmatic:", error);
    }
  }
  if (missing.length) {
    finalResult = insertObjectivesMissingStandards(finalResult, missing);
  }
  appState.content.objectives = finalResult;
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
    onSuccess: (result) => applyObjectivesOutput(result)
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
async function executeAIGeneration({ buttonId, targetEditorId, targetPreviewId, operationName, prompt, images = [], onSuccess, requireTextbook = false, requireSource = false, skipGuard = false, maxOutputTokens = null, visionBatches = false }) {
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
    if (visionBatches) {
      appState.cancelRequested = false;
      appState.generationController = new AbortController();
      const cancelButton = document.getElementById("btnCancelGeneration");
      if (cancelButton) cancelButton.disabled = false;
    }
    if (btn) btn.disabled = true;

    updateProgress(50, `Đang ${operationName}...`);
    document.getElementById("statusFooterText").textContent = `Đang ${operationName}...`;

    const rawResult = visionBatches
      ? await analyzeTextbookInBatches(prompt, {
        signal: appState.generationController.signal,
        onProgress: (done, total, usedPdfText) => updateProgress(Math.round((done / total) * 100), `Đang đọc SGK theo đợt ${done}/${total} (${usedPdfText ? "chữ PDF" : "ảnh đã nén"})...`)
      })
      : await geminiAPI.generateContent(buildPedagogicalPrompt(prompt), images, getSystemRole(appState.selectedSubject, appState.selectedGrade), 0.3, null, maxOutputTokens ? { maxOutputTokens } : {});
    const result = skipGuard ? (normalizeGeminiLessonOutput(rawResult).text || rawResult) : await guardGeminiLessonOutput(rawResult);

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
    if (isGeminiOverloadError(error)) {
      showToast("Gemini đang quá tải, hệ thống đã thử lại/đổi model nhưng vẫn lỗi. Thử lại sau hoặc chọn Gemini 2.5 Flash.", "danger", 7000);
    } else {
      showToast(`Lỗi khi ${operationName}: ${error.message}`, "danger", 6000);
    }
    hideProgress();
    document.getElementById("statusFooterText").textContent = `Lỗi khi ${operationName}.`;
  } finally {
    appState.isGenerating = false;
    if (visionBatches) {
      appState.generationController = null;
      const cancelButton = document.getElementById("btnCancelGeneration");
      if (cancelButton) cancelButton.disabled = true;
    }
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
    
    // BƯỚC 1: Đọc SGK (chữ PDF nếu rõ, không thì ảnh đã nén)
    if (appState.images.length > 0 && !String(appState.content.vision || "").trim()) {
      const promptVision = getPromptTemplate("ANALYZE_TEXTBOOK", context);
      const resVision = await analyzeTextbookInBatches(promptVision, {
        signal: appState.generationController.signal,
        onProgress: (done, total, usedPdfText) => updateProgress(
          Math.round(5 + (done / total) * 18),
          `Bước 1/7: Đang đọc SGK theo đợt ${done}/${total} (${usedPdfText ? "chữ PDF" : "ảnh đã nén"})...`
        )
      });
      throwIfGenerationCancelled();
      appState.content.vision = normalizeGeminiLessonOutput(resVision).text || resVision;
      document.getElementById("editorVision").value = appState.content.vision;
      renderMathPreview(appState.content.vision, "previewVision");
      saveStateToLocalStorage();
      await delay(generationPauseMs(), appState.generationController.signal);
    }

    if (!String(appState.content.vision || "").trim()) {
      throw new Error("Chưa có nội dung SGK trong nguồn. Hãy phân tích ảnh/PDF trước.");
    }
    applyLessonBasedRecommendations({ silent: true });
    Object.assign(context, getGenerationPromptContext());

    // BƯỚC 2: Tạo I. Mục tiêu
    updateProgress(25, "Bước 2/7: Đang tạo I. Mục tiêu bài học...");
    const promptObj = getPromptTemplate('GENERATE_OBJECTIVES', context);
    const resObj = await generateOneClickContent(promptObj);
    const finalObj = await applyObjectivesOutput(resObj, appState.generationController.signal);
    document.getElementById("editorObjectives").value = finalObj;
    renderMathPreview(finalObj, "previewObjectives");
    await delay(generationPauseMs(), appState.generationController.signal);
    context.objectives_content = finalObj;

    // BƯỚC 3: Tạo II. Thiết bị dạy học và học liệu
    updateProgress(40, "Bước 3/7: Đang tạo II. Thiết bị dạy học & học liệu...");
    const promptMat = getPromptTemplate('GENERATE_MATERIALS', context);
    const resMat = await generateOneClickContent(promptMat);
    appState.content.materials = resMat;
    document.getElementById("editorMaterials").value = resMat;
    renderMathPreview(resMat, "previewMaterials");
    await delay(generationPauseMs(), appState.generationController.signal);

    // BƯỚC 4: Tạo III.A Khởi động
    updateProgress(55, "Bước 4/7: Đang tạo III.A Hoạt động Mở đầu...");
    const promptA = getPromptTemplate('GENERATE_ACTIVITY_A', context) + buildPhasePedagogyContext('A');
    const resA = await generateOneClickContent(promptA);
    await applyActivityOutput("A", resA, appState.generationController.signal);
    await delay(generationPauseMs(), appState.generationController.signal);

    // BƯỚC 5: Tạo III.B Hình thành kiến thức mới
    updateProgress(70, "Bước 5/7: Đang tạo III.B Hoạt động Hình thành kiến thức...");
    context.activities_content = appState.content.activities.A;
    const promptB = getPromptTemplate('GENERATE_ACTIVITY_B', context) + buildPhasePedagogyContext('B');
    const resB = await generateOneClickContent(promptB);
    await applyActivityOutput("B", resB, appState.generationController.signal);
    await delay(generationPauseMs(), appState.generationController.signal);

    // BƯỚC 6: Tạo III.C Luyện tập
    updateProgress(82, "Bước 6/7: Đang tạo III.C Hoạt động Luyện tập...");
    context.activities_content = appState.content.activities.A + "\n\n---\n\n" + appState.content.activities.B;
    const promptC = getPromptTemplate('GENERATE_ACTIVITY_C', context) + buildPhasePedagogyContext('C');
    const resC = await generateOneClickContent(promptC);
    await applyActivityOutput("C", resC, appState.generationController.signal);
    await delay(generationPauseMs(), appState.generationController.signal);

    // BƯỚC 7: Tạo III.D Vận dụng
    updateProgress(94, "Bước 7/7: Đang tạo III.D Hoạt động Vận dụng...");
    context.activities_content += "\n\n---\n\n" + appState.content.activities.C;
    const promptD = getPromptTemplate('GENERATE_ACTIVITY_D', context) + buildPhasePedagogyContext('D');
    const resD = await generateOneClickContent(promptD);
    await applyActivityOutput("D", resD, appState.generationController.signal);
    await delay(generationPauseMs(), appState.generationController.signal);

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
    if (cancelled) {
      showToast("Đã hủy quá trình tạo tự động. Nội dung đã hoàn tất trước đó vẫn được giữ lại.", "info", 7000);
    } else if (isGeminiOverloadError(err)) {
      showToast("Gemini đang quá tải, hệ thống đã thử lại/đổi model nhưng vẫn lỗi. Thử lại sau hoặc chọn Gemini 2.5 Flash.", "danger", 7000);
    } else {
      showToast(`Quá trình tạo tự động bị gián đoạn: ${err.message}`, "danger", 7000);
    }
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
    ...getLessonPlanMetadata(),
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
