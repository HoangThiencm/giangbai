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
      explore: lines[0] || "Quan sát tình huống trong SGK và nêu nhận xét ban đầu.",
      knowledge: knowledge[0] || lines[1] || "Chốt quy tắc / công thức trọng tâm của mục.",
      example: examples[0] || lines.find(line => /=\s*|\$/.test(line)) || "Ví dụ mẫu trong SGK.",
      practice: practice[0] || "Bài luyện tập tại chỗ tương ứng mục này."
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

  function buildUnitSlides(unit, topic) {
    const bits = pickExamples(unit.body);
    const name = unit.title || `Mục ${unit.index}`;
    return [
      slide("explore", `Khám phá: ${name}`, [
        { text: `Tình huống / hoạt động mở đầu (SGK) — ${topic || "bài học"}.`, step: 1 },
        { text: bits.explore, step: 1 },
        { text: "Câu hỏi: Em quan sát được gì? Em dự đoán quy tắc nào?", step: 2 },
        { text: "Gợi ý trả lời: Nêu đặc điểm, so sánh, thử với một số liệu nhỏ.", step: 2 }
      ], { unit: unit.index, phase: "kham-pha" }),
      slide("knowledge", `Kiến thức trọng tâm: ${name}`, [
        { text: "Đóng khung quy tắc / định nghĩa / công thức.", step: 1 },
        { text: bits.knowledge, step: 1 },
        { text: "Học sinh ghi vào vở phần in đậm trên khung kiến thức.", step: 2 }
      ], { unit: unit.index, phase: "kien-thuc" }),
      slide("example", `Ví dụ mẫu: ${name}`, [
        { text: "Đề bài ví dụ mẫu (SGK).", step: 1 },
        { text: bits.example, step: 1 },
        { text: "Bước 1: Đọc hiểu — xác định giả thiết và yêu cầu.", step: 2 },
        { text: "Bước 2: Phân tích — chọn quy tắc vừa chốt.", step: 3 },
        { text: "Bước 3: Trình bày lời giải từng dòng.", step: 4 },
        { text: "Bước 4: Đối chiếu kết quả và nêu chú ý sai thường gặp.", step: 5 }
      ], { unit: unit.index, phase: "vi-du" }),
      slide("practice", `Luyện tập tại chỗ: ${name}`, [
        { text: "Đề bài luyện tập / thực hành tương ứng mục.", step: 1 },
        { text: bits.practice, step: 1 },
        { text: "Học sinh làm nháp 1–2 phút.", step: 2 },
        { text: "Đáp án (click để mở): áp dụng đúng quy tắc vừa học, trình bày đủ bước.", step: 3 }
      ], { unit: unit.index, phase: "luyen-tap" })
    ];
  }

  function defaultUnits(topic) {
    const base = topic || "Bài học";
    return [
      { index: 1, title: `${base} — kiến thức cốt lõi`, body: "Định nghĩa và quy tắc trọng tâm. Ví dụ 1. Luyện tập." },
      { index: 2, title: `${base} — vận dụng`, body: "Công thức áp dụng. Ví dụ 2. Bài tập thực hành." }
    ];
  }

  function buildSlideDeck(source) {
    const ctx = source && typeof source === "object" ? source : { textbook: String(source || "") };
    const topic = strip(ctx.topic) || "Bài giảng trình chiếu";
    const subject = strip(ctx.subject) || "Toán";
    const grade = strip(ctx.grade) || "6";
    const duration = strip(ctx.duration) || "02 tiết (90 phút)";
    const textbook = String(ctx.textbook || ctx.vision || ctx.textbook_content || "");
    const units = extractKnowledgeUnits(textbook);
    const usedUnits = units.length ? units : defaultUnits(topic);

    const deck = [];
    deck.push(slide("title", topic, [
      { text: `Môn ${subject} · Lớp ${grade}`, step: 1 },
      { text: duration, step: 1 },
      { text: "Bài giảng trình chiếu theo đơn vị kiến thức SGK", step: 2 }
    ]));
    deck.push(slide("objectives", "Mục tiêu bài học", [
      { text: "Nêu được kiến thức cốt lõi của từng mục SGK.", step: 1 },
      { text: "Giải được ví dụ mẫu theo từng bước.", step: 2 },
      { text: "Luyện tập tại chỗ và vận dụng vào bài toán gần thực tiễn.", step: 3 }
    ]));
    deck.push(slide("warmup", "Khởi động", [
      { text: "Trò chơi / câu hỏi ngắn nhắc lại kiến thức đã học.", step: 1 },
      { text: "Học sinh trả lời nhanh, giáo viên ghi ý chính lên bảng.", step: 2 }
    ]));

    usedUnits.forEach(unit => {
      buildUnitSlides(unit, topic).forEach(item => deck.push(item));
    });

    const extraExercises = splitLines(textbook).filter(line => /bài\s*\d|luyện tập|bài tập/i.test(line)).slice(0, 4);
    (extraExercises.length ? extraExercises : ["Bài tập 1", "Bài tập 2"]).forEach((ex, idx) => {
      deck.push(slide("exercise", `Bài tập ${idx + 1}`, [
        { text: ex, step: 1 },
        { text: "Phân tích: xác định dạng toán và quy tắc cần dùng.", step: 2 },
        { text: "Hướng dẫn giải từng bước (click hiện từng ý).", step: 3 },
        { text: "Đáp án: trình bày đủ lập luận rồi đối chiếu SGK/SBT.", step: 4 }
      ], { phase: "bai-tap" }));
    });

    deck.push(slide("apply", "Vận dụng", [
      { text: "Bài toán gần thực tiễn gắn kiến thức vừa học.", step: 1 },
      { text: "Học sinh mô hình hóa → tính toán → kết luận.", step: 2 }
    ]));
    deck.push(slide("summary", "Tổng kết", [
      { text: "Nhắc lại các quy tắc đã đóng khung.", step: 1 },
      { text: "Giao bài luyện thêm và chuẩn bị bài sau.", step: 2 }
    ]));

    if (deck.length > MAX_COMPLETE_SLIDES) return deck.slice(0, MAX_COMPLETE_SLIDES);
    while (deck.length < MIN_COMPLETE_SLIDES) {
      const n = deck.length - 1;
      deck.splice(deck.length - 1, 0, slide("practice", `Củng cố thêm ${n}`, [
        { text: "Câu hỏi củng cố kiến thức vừa học.", step: 1 },
        { text: "Học sinh trả lời; giáo viên chốt đáp án.", step: 2 }
      ]));
    }
    return deck;
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

  function collectSourceFromApp() {
    const state = root.appState || {};
    const topic = state.customTopic || (typeof document !== "undefined" && document.getElementById("inputTopicCustom") && document.getElementById("inputTopicCustom").value) || "";
    const vision = (state.content && state.content.vision) || (typeof document !== "undefined" && document.getElementById("editorVision") && document.getElementById("editorVision").value) || "";
    const activity = (state.content && (state.content.B || state.content.activity)) || (typeof document !== "undefined" && document.getElementById("editorActivity") && document.getElementById("editorActivity").value) || "";
    return {
      topic: topic || state.selectedLesson || "Bài giảng",
      subject: state.subject || "Toán",
      grade: state.selectedGrade || "6",
      duration: state.duration || "02 tiết (90 phút)",
      textbook: [vision, activity].filter(Boolean).join("\n\n")
    };
  }

  function buildFromApp(source) {
    ui.deck = buildSlideDeck(source || collectSourceFromApp());
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
      buildBtn.addEventListener("click", function () {
        buildFromApp();
        if (typeof root.showToast === "function") root.showToast("Đã tạo bài giảng slides từ SGK.", "success", 3500);
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
    exportToPptx,
    renderSlideHtml,
    visibleItems,
    maxStep,
    mount,
    buildFromApp,
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
