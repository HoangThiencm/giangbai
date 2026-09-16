/**
 * js/khbd-slides.js
 * Sinh bài giảng trình chiếu 16:9 từ SGK/PPCT: khám phá → kiến thức → ví dụ → luyện tập.
 * Web: KaTeX + step-by-step reveal. Xuất PPTX bằng PptxGenJS.
 */
(function (root) {
  "use strict";

  const MIN_COMPLETE_SLIDES = 15;
  const MAX_COMPLETE_SLIDES = 25;

  function strip(text) {
    return String(text || "").replace(/\s+/g, " ").trim();
  }

  function latexToPlain(text) {
    return String(text || "")
      .replace(/\$\$([\s\S]+?)\$\$/g, " $1 ")
      .replace(/\$([^$]+)\$/g, " $1 ")
      .replace(/\\cdot/g, "·")
      .replace(/\\times/g, "×")
      .replace(/\\div/g, "÷")
      .replace(/\\frac\{([^}]+)\}\{([^}]+)\}/g, "($1)/($2)")
      .replace(/\\left|\\right/g, "")
      .replace(/\\[,;!]/g, " ")
      .replace(/[{}]/g, "")
      .replace(/\s+/g, " ")
      .trim();
  }

  function splitLines(text) {
    return String(text || "")
      .split(/\r?\n/)
      .map(line => line.replace(/^\s*[-*+]\s+/, "").trim())
      .filter(Boolean);
  }

  function extractKnowledgeUnits(textbook) {
    const source = String(textbook || "").trim();
    const units = [];
    if (!source) return units;

    if (typeof root.extractTextbookSubsections === "function") {
      const extracted = root.extractTextbookSubsections(source) || [];
      extracted.forEach((item, idx) => {
        units.push({
          index: Number(item.index) || idx + 1,
          title: strip(item.title) || `Mục ${idx + 1}`,
          body: strip(item.body || item.content || "")
        });
      });
    }

    if (!units.length) {
      const headingRe = /(?:^|\n)\s*(?:#{1,3}\s+|(?:Mục|Phần|I{1,3}|IV|V|VI)\s*[\.\):]\s*)([^\n]{3,80})/gi;
      const hits = [];
      let match;
      while ((match = headingRe.exec(source))) {
        hits.push({ title: strip(match[1]), at: match.index + (match[0].startsWith("\n") ? 1 : 0) });
      }
      hits.forEach((hit, i) => {
        const end = i + 1 < hits.length ? hits[i + 1].at : source.length;
        units.push({
          index: i + 1,
          title: hit.title.replace(/^#+\s*/, ""),
          body: source.slice(hit.at, end).trim()
        });
      });
    }

    if (!units.length) {
      const chunks = source.split(/\n{2,}/).map(strip).filter(chunk => chunk.length > 40);
      chunks.slice(0, 4).forEach((chunk, i) => {
        units.push({ index: i + 1, title: `Đơn vị kiến thức ${i + 1}`, body: chunk });
      });
    }

    return units.slice(0, 4);
  }

  function pickExamples(body) {
    const lines = splitLines(body);
    const examples = lines.filter(line => /ví dụ|vd\s*\d|bài\s*\d/i.test(line));
    const practice = lines.filter(line => /luyện tập|thực hành|bài tập/i.test(line));
    const knowledge = lines.filter(line => /định nghĩa|quy tắc|công thức|chú ý|kết luận/i.test(line));
    return {
      explore: lines[0] || "",
      knowledge: knowledge[0] || "",
      example: examples[0] || lines.find(line => /=\s*|\$/.test(line)) || "",
      practice: practice[0] || "",
      evidence: lines
    };
  }

  function slide(type, title, items, meta) {
    return {
      type,
      title,
      items: (items || []).map((item, idx) => {
        if (typeof item === "string") return { text: item, step: idx + 1 };
        return { text: item.text, step: item.step != null ? item.step : idx + 1, role: item.role || "" };
      }),
      meta: meta || {}
    };
  }

  function buildUnitSlides(unit) {
    const bits = pickExamples(unit.body);
    const name = unit.title || `Mục ${unit.index}`;
    const phases = [
      ["explore", "Khám phá", bits.explore],
      ["rule", "Kiến thức trọng tâm", bits.knowledge],
      ["example", "Ví dụ mẫu", bits.example],
      ["practice", "Luyện tập tại chỗ", bits.practice]
    ];
    return phases.filter(function (phase) { return Boolean(phase[2]); }).map(function (phase) {
      const matchingEvidence = bits.evidence.filter(function (line) { return line !== phase[2]; }).slice(0, 4);
      return slide(phase[0], `${phase[1]}: ${name}`, [{ text: phase[2], step: 1 }].concat(
        matchingEvidence.map(function (text, index) { return { text, step: index + 2 }; })
      ), { unit: unit.index, phase: phase[0] });
    });
  }

  function defaultUnits(topic) {
    return [];
  }

  function buildSlideDeck(source) {
    const ctx = source && typeof source === "object" ? source : { textbook: String(source || "") };
    const topic = strip(ctx.topic);
    const subject = strip(ctx.subject);
    const grade = strip(ctx.grade);
    const duration = strip(ctx.duration);
    const textbook = String(ctx.textbook || ctx.vision || ctx.textbook_content || "");
    const units = extractKnowledgeUnits(textbook);
    const usedUnits = units.length ? units : defaultUnits(topic);
    if (!usedUnits.length) throw new Error("Chưa có ngữ cảnh SGK thực để dựng bài giảng.");

    const deck = [];
    if (!topic || !subject || !grade || !duration) throw new Error("Thiếu metadata bài học thực; hãy đọc SGK hoặc điền đủ tên bài, môn, lớp và thời lượng.");
    deck.push(slide("title", topic, [
      { text: `Môn ${subject} · Lớp ${grade}`, step: 1 },
      { text: duration, step: 2 }
    ]));
    deck.push(slide("intro", "Các đề mục SGK", usedUnits.map(function (unit, index) {
      return { text: unit.title, step: index + 1 };
    })));

    usedUnits.forEach(unit => {
      buildUnitSlides(unit).forEach(item => deck.push(item));
    });

    const extraExercises = splitLines(textbook).filter(line => /bài\s*\d|luyện tập|bài tập/i.test(line)).slice(0, 4);
    extraExercises.forEach((ex, idx) => {
      deck.push(slide("exercise", `Bài tập ${idx + 1}`, [
        { text: ex, step: 1 }
      ], { phase: "bai-tap" }));
    });

    deck.push(slide("summary", "Tổng kết", [
      ...usedUnits.map(function (unit, index) { return { text: unit.title, step: index + 1 }; })
    ]));

    const evidence = splitLines(textbook).filter(Boolean);
    while (deck.length < MIN_COMPLETE_SLIDES) {
      const text = evidence[deck.length % evidence.length];
      if (!text) throw new Error("Ngữ cảnh SGK không đủ để dựng deck 15 slide.");
      deck.splice(deck.length - 1, 0, slide("intro", `Trích đoạn SGK ${deck.length}`, [{ text, step: 1 }]));
    }
    return deck.slice(0, MAX_COMPLETE_SLIDES);
  }

  function extractJson(raw) {
    const source = String(raw || "").replace(/^\s*```(?:json)?\s*|\s*```\s*$/gi, "").trim();
    const start = source.indexOf("{");
    if (start < 0) throw new Error("Gemini không trả về JSON kịch bản slide.");
    let depth = 0, quoted = false, escaped = false;
    for (let i = start; i < source.length; i += 1) {
      const char = source[i];
      if (quoted) {
        if (escaped) escaped = false;
        else if (char === "\\") escaped = true;
        else if (char === '"') quoted = false;
      } else if (char === '"') quoted = true;
      else if (char === "{") depth += 1;
      else if (char === "}" && --depth === 0) {
        try { return JSON.parse(source.slice(start, i + 1)); }
        catch (_) { throw new Error("Gemini trả JSON kịch bản slide không hợp lệ."); }
      }
    }
    throw new Error("Gemini trả JSON kịch bản slide chưa hoàn chỉnh.");
  }

  function normalizeAiDeck(payload) {
    const slides = payload && Array.isArray(payload.slides) ? payload.slides : [];
    if (slides.length < MIN_COMPLETE_SLIDES || slides.length > MAX_COMPLETE_SLIDES) {
      throw new Error(`Gemini phải tạo từ ${MIN_COMPLETE_SLIDES} đến ${MAX_COMPLETE_SLIDES} slide (nhận ${slides.length}).`);
    }
    const allowed = new Set(["title", "intro", "explore", "rule", "example", "practice", "summary"]);
    const types = new Set();
    const deck = slides.map(function (entry, index) {
      const type = String(entry && entry.type || "").trim().toLowerCase();
      const title = strip(entry && entry.title);
      const content = strip(entry && entry.content);
      const formula = strip(entry && entry.mathFormula);
      const steps = Array.isArray(entry && entry.steps) ? entry.steps.map(strip).filter(Boolean) : [];
      if (!allowed.has(type) || !title || (!content && !formula && !steps.length)) {
        throw new Error(`Slide ${index + 1} thiếu type/title/content hợp lệ.`);
      }
      types.add(type);
      const items = [];
      if (content) items.push({ text: content, step: 1 });
      if (formula) items.push({ text: `$${formula.replace(/^\$+|\$+$/g, "")}$`, step: 1, role: "formula" });
      steps.forEach(function (text, stepIndex) { items.push({ text, step: stepIndex + 2, role: "step" }); });
      return { type, title, items, meta: { aiGenerated: true, source: "gemini-3-flash-preview" } };
    });
    ["title", "intro", "explore", "rule", "example", "practice", "summary"].forEach(function (type) {
      if (!types.has(type)) throw new Error(`Kịch bản Gemini thiếu slide loại ${type}.`);
    });
    return deck;
  }

  function lessonContextFromApp(source) {
    const ctx = source && typeof source === "object" ? source : collectSourceFromApp();
    const textbook = String(ctx.textbook || ctx.vision || ctx.textbook_content || "").trim();
    if (!textbook) throw new Error("Chưa có ngữ cảnh SGK thực. Hãy đọc SGK trước khi tạo bài giảng.");
    return {
      topic: strip(ctx.topic), subject: strip(ctx.subject), grade: strip(ctx.grade), duration: strip(ctx.duration), textbook
    };
  }

  async function generateAiLessonSlides(source, signal) {
    const client = typeof geminiAPI !== "undefined" ? geminiAPI : root.geminiAPI;
    if (!client || typeof client.generateContent !== "function") {
      throw new Error("Gemini Canvas chưa sẵn sàng để tạo bài giảng.");
    }
    const ctx = lessonContextFromApp(source);
    client.selectedModel = "gemini-3-flash-preview";
    const prompt = `Bạn là chuyên gia thiết kế bài giảng trình chiếu. Chỉ dùng NGỮ CẢNH SGK THẬT bên dưới; không bịa đề mục, định nghĩa, ví dụ, bài tập hoặc đáp án.\n\nBÀI: ${ctx.topic}\nMÔN: ${ctx.subject}; LỚP: ${ctx.grade}; THỜI LƯỢNG: ${ctx.duration}\n\nNGỮ CẢNH SGK THẬT:\n${ctx.textbook}\n\nHãy tạo đúng 15–25 slide bằng tiếng Việt. Với từng đơn vị kiến thức có trong ngữ cảnh, bắt buộc theo chuỗi Khám phá → Quy tắc/định nghĩa → Ví dụ SGK giải từng bước → Luyện tập SGK. Có bìa, mục tiêu, khởi động, củng cố/vận dụng và tổng kết. Nếu ngữ cảnh không đủ dữ liệu cho một chi tiết, nêu rõ “Cần giáo viên bổ sung từ trang SGK đã tải”, tuyệt đối không bịa.\n\nChỉ trả JSON hợp lệ, không markdown: {"slides":[{"type":"title|intro|explore|rule|example|practice|summary","title":"...","content":"nội dung thật bám SGK","steps":["bước click 1", "bước click 2"],"mathFormula":"LaTex nếu có, không có thì chuỗi rỗng"}]}.`;
    const role = typeof root.getSystemRole === "function" ? root.getSystemRole(ctx.subject, ctx.grade) : "";
    const raw = await client.generateContent(prompt, [], role, 0.2, signal || null, { maxOutputTokens: 8192, timeoutMs: 120000 });
    return normalizeAiDeck(extractJson(raw));
  }

  function maxStep(slideItem) {
    return (slideItem.items || []).reduce((n, item) => Math.max(n, Number(item.step) || 1), 1);
  }

  function visibleItems(slideItem, revealed) {
    const step = Math.max(1, Number(revealed) || 1);
    return (slideItem.items || []).filter(item => (Number(item.step) || 1) <= step);
  }

  function escapeHtml(text) {
    return String(text || "")
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  function renderMath(el) {
    if (!el) return;
    if (typeof root.renderMathInElement === "function") {
      root.renderMathInElement(el, {
        delimiters: [
          { left: "$$", right: "$$", display: true },
          { left: "$", right: "$", display: false }
        ],
        throwOnError: false
      });
    }
  }

  function renderSlideHtml(slideItem, revealed) {
    const items = visibleItems(slideItem, revealed);
    const body = items.map(item => `<li data-step="${item.step}">${escapeHtml(item.text)}</li>`).join("");
    return `<article class="khbd-slide-card" data-type="${escapeHtml(slideItem.type)}">
      <h2 class="khbd-slide-title">${escapeHtml(slideItem.title)}</h2>
      <ul class="khbd-slide-items">${body}</ul>
    </article>`;
  }

  const ui = {
    deck: [],
    index: 0,
    revealed: 1,
    stage: null,
    counter: null
  };

  function currentSlide() {
    return ui.deck[ui.index] || null;
  }

  function paint() {
    const slideItem = currentSlide();
    if (ui.stage) {
      if (!slideItem) {
        ui.stage.innerHTML = '<p class="khbd-slide-empty">Chưa có bài giảng. Hãy nạp SGK rồi bấm Tạo bài giảng slides.</p>';
      } else {
        ui.stage.innerHTML = renderSlideHtml(slideItem, ui.revealed);
        renderMath(ui.stage);
      }
    }
    if (typeof document !== "undefined") {
      const overlay = document.getElementById("slidePresentationOverlay");
      const host = document.getElementById("slidePresentationHost");
      if (overlay && !overlay.hidden && host && ui.stage) {
        host.innerHTML = ui.stage.innerHTML;
        renderMath(host);
      }
      const exportBtn = document.getElementById("btnExportPptx");
      if (exportBtn) exportBtn.disabled = !ui.deck.length;
    }
    if (ui.counter) {
      ui.counter.textContent = ui.deck.length ? `Slide ${ui.index + 1} / ${ui.deck.length}` : "Slide 0 / 0";
    }
  }

  function revealOrNext() {
    const slideItem = currentSlide();
    if (!slideItem) return;
    if (ui.revealed < maxStep(slideItem)) {
      ui.revealed += 1;
      paint();
      return;
    }
    if (ui.index < ui.deck.length - 1) {
      ui.index += 1;
      ui.revealed = 1;
      paint();
    }
  }

  function prevSlide() {
    if (ui.index <= 0) {
      ui.revealed = 1;
      paint();
      return;
    }
    ui.index -= 1;
    ui.revealed = 1;
    paint();
  }

  function nextSlide() {
    revealOrNext();
  }

  function goTo(index) {
    if (!ui.deck.length) return;
    ui.index = Math.max(0, Math.min(ui.deck.length - 1, index));
    ui.revealed = 1;
    paint();
  }

  function getAppState() {
    return typeof appState !== "undefined" ? appState : (root.appState || {});
  }

  function syncTextbookMetadata(text) {
    if (typeof document === "undefined") return;
    const state = getAppState();
    const field = label => {
      const match = String(text || "").match(new RegExp("^\\s*-\\s*" + label + ":\\s*(.+)$", "mi"));
      return match ? match[1].trim() : "";
    };
    const topic = field("Chủ đề");
    const grade = field("Khối lớp");
    const subject = field("Môn");
    if (topic) {
      state.customTopic = topic;
      const input = document.getElementById("inputTopicCustom");
      if (input) input.value = topic;
      const title = document.getElementById("slideLessonTitle");
      if (title) title.textContent = topic;
    }
    for (const [id, value, key] of [["selectGrade", grade, "selectedGrade"], ["selectSubject", subject, "selectedSubject"]]) {
      const select = document.getElementById(id);
      const option = select && Array.from(select.options || []).find(item =>
        strip(item.value).toLowerCase() === value.toLowerCase() ||
        strip(item.textContent).toLowerCase() === value.toLowerCase() ||
        (id === "selectGrade" && strip(item.textContent).toLowerCase() === "lớp " + value.toLowerCase()));
      if (value && option) {
        state[key] = option.value;
        select.value = option.value;
      }
    }
    if (subject) state.subject = subject;
    if (typeof root.saveStateToLocalStorage === "function") root.saveStateToLocalStorage();
  }

  function installTextbookMetadataSync(attempt) {
    if (typeof root.applyTextbookOcrResult === "function") {
      const original = root.applyTextbookOcrResult;
      if (original.slidesMetadataSync) return;
      const wrapped = async function (text, options) {
        const state = getAppState();
        if (state.cancelRequested || (state.generationController && state.generationController.signal.aborted)) {
          throw new DOMException("Aborted", "AbortError");
        }
        await original(text, options);
        syncTextbookMetadata(text);
      };
      wrapped.slidesMetadataSync = true;
      root.applyTextbookOcrResult = wrapped;
    } else if (attempt < 100) {
      root.setTimeout(() => installTextbookMetadataSync(attempt + 1), 200);
    }
  }

  function collectSourceFromApp() {
    const state = getAppState();
    const topic = state.customTopic || (typeof document !== "undefined" && document.getElementById("inputTopicCustom") && document.getElementById("inputTopicCustom").value) || "";
    const vision = (state.content && state.content.vision) || (typeof document !== "undefined" && document.getElementById("editorVision") && document.getElementById("editorVision").value) || "";
    return {
      topic: topic || state.selectedLesson || "",
      subject: state.subject || "",
      grade: state.selectedGrade || "",
      duration: state.duration || "",
      textbook: vision
    };
  }

  async function buildFromApp(source, signal, validate) {
    const state = getAppState();
    const activeSignal = signal || (state.generationController && state.generationController.signal);
    const deck = await generateAiLessonSlides(source || collectSourceFromApp(), activeSignal);
    if (activeSignal && activeSignal.aborted) throw new DOMException("Aborted", "AbortError");
    if (typeof validate === "function") validate();
    ui.deck = deck;
    ui.index = 0;
    ui.revealed = 1;
    paint();
    return ui.deck;
  }

  async function exportToPptx(slideDeck) {
    const deck = Array.isArray(slideDeck) && slideDeck.length ? slideDeck : ui.deck;
    if (!deck.length) throw new Error("Chưa có slide để xuất PowerPoint.");
    const PptxGenJS = root.PptxGenJS || root.pptxgen;
    if (typeof PptxGenJS !== "function") throw new Error("Chưa nạp được thư viện PptxGenJS.");
    const pptx = new PptxGenJS();
    pptx.defineLayout({ name: "KHBD_16x9", width: 13.333, height: 7.5 });
    pptx.layout = "KHBD_16x9";
    pptx.author = "Soạn bài giảng trình chiếu AI";
    pptx.title = (deck[0] && deck[0].title) || "Bai giang";

    deck.forEach((item, idx) => {
      const page = pptx.addSlide();
      page.addShape(pptx.ShapeType.rect, { x: 0, y: 0, w: 13.333, h: 0.7, fill: { color: "0F4C81" } });
      page.addText(latexToPlain(item.title || `Slide ${idx + 1}`), {
        x: 0.4, y: 0.12, w: 12.5, h: 0.48, fontSize: 22, bold: true, color: "FFFFFF", fontFace: "Calibri"
      });
      const steps = {};
      (item.items || []).forEach(entry => {
        const step = Number(entry.step) || 1;
        (steps[step] || (steps[step] = [])).push(latexToPlain(entry.text));
      });
      let y = 1.0;
      Object.keys(steps).sort((a, b) => Number(a) - Number(b)).forEach((step, clickIndex) => {
        steps[step].forEach(line => {
          page.addText(line, {
            x: 0.5,
            y,
            w: 12.3,
            h: 0.55,
            fontSize: 18,
            fontFace: "Calibri",
            color: "1F2937",
            valign: "top"
          });
          y += 0.58;
        });
        if (clickIndex > 0) {
          try {
            page.addNotes(`Appear click ${clickIndex + 1}`);
          } catch (_) {}
        }
      });
    });

    const safeName = latexToPlain((deck[0] && deck[0].title) || "bai-giang").replace(/[^\p{L}\p{N}]+/gu, "-").slice(0, 60) || "bai-giang";
    await pptx.writeFile({ fileName: `${safeName}.pptx` });
    return true;
  }

  function enterPresentation() {
    if (typeof document === "undefined") return;
    const overlay = document.getElementById("slidePresentationOverlay");
    const host = document.getElementById("slidePresentationHost");
    if (!overlay || !host) {
      if (ui.stage && ui.stage.requestFullscreen) ui.stage.requestFullscreen().catch(() => {});
      return;
    }
    overlay.hidden = false;
    overlay.classList.add("is-on");
    host.innerHTML = ui.stage ? ui.stage.innerHTML : "";
    renderMath(host);
    if (overlay.requestFullscreen) overlay.requestFullscreen().catch(() => {});
  }

  function exitPresentation() {
    if (typeof document === "undefined") return;
    const overlay = document.getElementById("slidePresentationOverlay");
    if (overlay) {
      overlay.hidden = true;
      overlay.classList.remove("is-on");
    }
    if (document.fullscreenElement) document.exitFullscreen().catch(() => {});
  }

  function bindPresentationKeys(ev) {
    const overlay = typeof document !== "undefined" && document.getElementById("slidePresentationOverlay");
    const presenting = overlay && !overlay.hidden;
    if (ev.key === "F5") {
      ev.preventDefault();
      enterPresentation();
      return;
    }
    if (ev.key === "Escape" && presenting) {
      exitPresentation();
      return;
    }
    if (!presenting && ev.target && /input|textarea|select/i.test(ev.target.tagName)) return;
    if (ev.key === "ArrowRight" || ev.key === " " || ev.key === "PageDown") {
      ev.preventDefault();
      nextSlide();
      if (presenting) {
        const host = document.getElementById("slidePresentationHost");
        if (host && ui.stage) host.innerHTML = ui.stage.innerHTML;
      }
    } else if (ev.key === "ArrowLeft" || ev.key === "PageUp") {
      ev.preventDefault();
      prevSlide();
      if (presenting) {
        const host = document.getElementById("slidePresentationHost");
        if (host && ui.stage) host.innerHTML = ui.stage.innerHTML;
      }
    }
  }

  function mount(options) {
    if (typeof document === "undefined") return;
    const opts = options || {};
    installTextbookMetadataSync(0);
    ui.stage = document.getElementById(opts.stageId || "slideStage");
    ui.counter = document.getElementById(opts.counterId || "slideCounter");
    const prev = document.getElementById(opts.prevId || "btnSlidePrev");
    const next = document.getElementById(opts.nextId || "btnSlideNext");
    const present = document.getElementById(opts.presentId || "btnPresentFullscreen");
    const exportBtn = document.getElementById(opts.exportId || "btnExportPptx");
    const buildBtn = document.getElementById(opts.buildId || "btnBuildSlides");
    if (prev) prev.addEventListener("click", prevSlide);
    if (next) next.addEventListener("click", nextSlide);
    if (ui.stage) ui.stage.addEventListener("click", nextSlide);
    if (present) present.addEventListener("click", enterPresentation);
    if (exportBtn) {
      exportBtn.addEventListener("click", function () {
        exportToPptx(ui.deck).catch(function (err) {
          if (typeof root.showToast === "function") root.showToast(err.message, "danger", 5000);
          else console.error(err);
        });
      });
    }
    if (buildBtn) {
      buildBtn.addEventListener("click", async function () {
        const previousLabel = buildBtn.innerHTML;
        try {
          buildBtn.disabled = true;
          buildBtn.textContent = "Đang tạo slide AI...";
          if (typeof root.handle1ClickGenerate === "function") await root.handle1ClickGenerate();
          else await buildFromApp();
          if (typeof root.showToast === "function") root.showToast("Đã tạo bài giảng slides từ ngữ cảnh SGK thật.", "success", 3500);
        } catch (err) {
          if (typeof root.showToast === "function") root.showToast(err.message || "Không thể tạo bài giảng slides.", "danger", 6000);
          else console.error(err);
        } finally {
          buildBtn.disabled = false;
          buildBtn.innerHTML = previousLabel;
        }
      });
    }
    document.addEventListener("keydown", bindPresentationKeys);
    const overlay = document.getElementById("slidePresentationOverlay");
    if (overlay) overlay.addEventListener("click", nextSlide);
    paint();
  }

  const api = {
    MIN_COMPLETE_SLIDES,
    MAX_COMPLETE_SLIDES,
    extractKnowledgeUnits,
    buildSlideDeck,
    generateAiLessonSlides,
    exportToPptx,
    renderSlideHtml,
    visibleItems,
    maxStep,
    mount,
    buildFromApp,
    syncTextbookMetadata,
    nextSlide,
    prevSlide,
    goTo,
    enterPresentation,
    exitPresentation,
    getDeck: function () { return ui.deck.slice(); }
  };

  root.KhbdSlides = api;
  if (typeof module !== "undefined" && module.exports) {
    module.exports = api;
  }
})(typeof window !== "undefined" ? window : globalThis);
