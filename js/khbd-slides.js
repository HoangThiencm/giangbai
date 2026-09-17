/**
 * js/khbd-slides.js
 * Sinh bài giảng trình chiếu 16:9 từ SGK/PPCT: khám phá → kiến thức → ví dụ → luyện tập.
 * Web: KaTeX + step-by-step reveal. Xuất PPTX bằng PptxGenJS.
 */
(function (root) {
  "use strict";

  const MIN_COMPLETE_SLIDES = 15;
  const MAX_COMPLETE_SLIDES = 25;
  const ALLOWED_TYPES = ["title", "intro", "explore", "rule", "example", "practice", "summary"];
  const SPLIT_TYPES = { explore: 1, example: 1, practice: 1 };
  const SLIDE_W = 13.333;
  const SLIDE_H = 7.5;

  function strip(text) {
    return String(text || "").replace(/\s+/g, " ").trim();
  }

  function isMetaInstruction(text) {
    const t = strip(text);
    if (!t) return true;
    if (/^(hiển thị|liệt kê|xuất hiện)(?:\s|$)/i.test(t)) return true;
    if (/^thực hiện phép(?: thế| cộng| trừ)?\.?$/i.test(t)) return true;
    if (/^(click để|bấm để|hiện thị)(?:\s|$)/i.test(t)) return true;
    return false;
  }

  function mapSuperscript(ch) {
    const map = { "0": "⁰", "1": "¹", "2": "²", "3": "³", "4": "⁴", "5": "⁵", "6": "⁶", "7": "⁷", "8": "⁸", "9": "⁹", "+": "⁺", "-": "⁻", "n": "ⁿ", "i": "ⁱ" };
    return map[ch] || null;
  }

  function mapSubscript(ch) {
    const map = { "0": "₀", "1": "₁", "2": "₂", "3": "₃", "4": "₄", "5": "₅", "6": "₆", "7": "₇", "8": "₈", "9": "₉", "+": "₊", "-": "₋", "a": "ₐ", "e": "ₑ", "i": "ᵢ", "o": "ₒ", "x": "ₓ", "n": "ₙ", "k": "ₖ", "m": "ₘ" };
    return map[ch] || null;
  }

  function scriptRun(body, mapper, fallbackPrefix) {
    const chars = String(body || "").split("");
    if (chars.every(function (ch) { return mapper(ch) || ch === " "; })) {
      return chars.map(function (ch) { return ch === " " ? " " : mapper(ch); }).join("");
    }
    return fallbackPrefix + body;
  }

  function envBodyToLines(body) {
    return String(body || "")
      .split(/\\\\/)
      .map(function (line) { return line.replace(/&/g, " ").replace(/\s+/g, " ").trim(); })
      .filter(Boolean);
  }

  function latexToPlain(text) {
    let s = String(text || "");
    s = s.replace(/\$\$([\s\S]+?)\$\$/g, "\n$1\n");
    s = s.replace(/\$([^$]+)\$/g, "$1");
    s = s.replace(/\\begin\{cases\}([\s\S]*?)\\end\{cases\}/gi, function (_, body) {
      const lines = envBodyToLines(body);
      if (!lines.length) return "";
      return lines.map(function (line, i) { return (i === 0 ? "{ " : "  ") + line; }).join("\n");
    });
    s = s.replace(/\\begin\{(?:aligned|align\*?|array|gathered|eqnarray\*?|split)\}([\s\S]*?)\\end\{(?:aligned|align\*?|array|gathered|eqnarray\*?|split)\}/gi, function (_, body) {
      return envBodyToLines(body).join("\n");
    });
    s = s.replace(/\\begin\{[a-zA-Z*]+\}|\\end\{[a-zA-Z*]+\}/g, "");
    let guard = 0;
    while (guard < 8) {
      const next = s
        .replace(/\\(?:text|mathrm|mathbf|mathit|textrm|textbf|textit|operatorname)\{([^{}]*)\}/g, "$1")
        .replace(/\\(?:dfrac|tfrac|frac)\{([^{}]*)\}\{([^{}]*)\}/g, "($1)/($2)")
        .replace(/\\sqrt\[([^\]]+)\]\{([^{}]*)\}/g, "√[$1]($2)")
        .replace(/\\sqrt\{([^{}]*)\}/g, "√($1)")
        .replace(/\\overline\{([^{}]*)\}/g, "$1")
        .replace(/\\overrightarrow\{([^{}]*)\}/g, "$1→")
        .replace(/\\vec\{([^{}]*)\}/g, "$1");
      if (next === s) break;
      s = next;
      guard += 1;
    }
    s = s.replace(/\^\{([^{}]+)\}/g, function (_, body) { return scriptRun(body, mapSuperscript, "^"); });
    s = s.replace(/\^([0-9A-Za-z+\-])/g, function (_, ch) { return mapSuperscript(ch) || "^" + ch; });
    s = s.replace(/_\{([^{}]+)\}/g, function (_, body) { return scriptRun(body, mapSubscript, "_"); });
    s = s.replace(/_([0-9A-Za-z+\-])/g, function (_, ch) { return mapSubscript(ch) || "_" + ch; });
    const symbols = [
      [/\\cdot\b/g, "·"], [/\\times\b/g, "×"], [/\\div\b/g, "÷"], [/\\pm\b/g, "±"], [/\\mp\b/g, "∓"],
      [/\\leq\b|\\le\b/g, "≤"], [/\\geq\b|\\ge\b/g, "≥"], [/\\neq\b|\\ne\b/g, "≠"], [/\\approx\b/g, "≈"],
      [/\\equiv\b/g, "≡"], [/\\infty\b/g, "∞"], [/\\in\b/g, "∈"], [/\\notin\b/g, "∉"],
      [/\\subset\b/g, "⊂"], [/\\cup\b/g, "∪"], [/\\cap\b/g, "∩"], [/\\emptyset\b/g, "∅"],
      [/\\rightarrow\b|\\to\b/g, "→"], [/\\leftarrow\b/g, "←"], [/\\Rightarrow\b/g, "⇒"],
      [/\\Leftrightarrow\b|\\iff\b/g, "⇔"], [/\\angle\b/g, "∠"], [/\\triangle\b/g, "△"],
      [/\\perp\b/g, "⊥"], [/\\parallel\b/g, "∥"], [/\\circ\b/g, "°"], [/\\pi\b/g, "π"],
      [/\\alpha\b/g, "α"], [/\\beta\b/g, "β"], [/\\gamma\b/g, "γ"], [/\\theta\b/g, "θ"],
      [/\\lambda\b/g, "λ"], [/\\mu\b/g, "μ"], [/\\sigma\b/g, "σ"], [/\\omega\b/g, "ω"],
      [/\\Delta\b/g, "Δ"], [/\\sum\b/g, "Σ"], [/\\prod\b/g, "Π"], [/\\int\b/g, "∫"],
      [/\\sin\b/g, "sin"], [/\\cos\b/g, "cos"], [/\\tan\b/g, "tan"], [/\\log\b/g, "log"], [/\\ln\b/g, "ln"],
      [/\\left\b|\\right\b/g, ""], [/\\displaystyle\b|\\textstyle\b|\\limits\b/g, ""],
      [/\\,|\\;|\\!|\\:|\\quad\b|\\qquad\b/g, " "], [/\\\\/g, "\n"], [/\\ /g, " "]
    ];
    symbols.forEach(function (pair) { s = s.replace(pair[0], pair[1]); });
    s = s.replace(/\\[a-zA-Z]+\*?/g, "");
    s = s.replace(/[{}]/g, "");
    s = s.replace(/&/g, " ");
    s = s.replace(/[ \t]+/g, " ").replace(/ *\n */g, "\n").replace(/\n{3,}/g, "\n\n").trim();
    return s;
  }

  function estimateTextHeight(text, widthInches, fontSizePt, lineHeight) {
    const lh = lineHeight || 1.28;
    const size = Math.max(10, Number(fontSizePt) || 16);
    const width = Math.max(1, Number(widthInches) || 6);
    const avgChar = (size * 0.52) / 72;
    const charsPerLine = Math.max(8, Math.floor(width / avgChar));
    const lines = String(text == null ? "" : text).split(/\n/).reduce(function (sum, line) {
      return sum + Math.max(1, Math.ceil((line.length || 1) / charsPerLine));
    }, 0);
    return Math.max(0.28, lines * (size / 72) * lh);
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
        if (typeof item === "string") return { text: item, step: idx + 1, role: "", label: "" };
        return {
          text: item.text,
          step: item.step != null ? item.step : idx + 1,
          role: item.role || "",
          label: item.label || ""
        };
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
      const firstRole = phase[0] === "rule" ? "rule" : "problem";
      return slide(phase[0], `${phase[1]}: ${name}`, [{ text: phase[2], step: 1, role: firstRole }].concat(
        matchingEvidence.map(function (text, index) {
          return { text, step: index + 2, role: "step", label: "Bước " + (index + 1) };
        })
      ), { unit: unit.index, phase: phase[0], problem: firstRole === "problem" ? phase[2] : "", ruleBox: firstRole === "rule" ? phase[2] : "" });
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
    ], { subtitle: `Môn ${subject} · Lớp ${grade}` }));
    deck.push(slide("intro", "Các đề mục SGK", usedUnits.map(function (unit, index) {
      return { text: unit.title, step: index + 1 };
    })));

    usedUnits.forEach(unit => {
      buildUnitSlides(unit).forEach(item => deck.push(item));
    });

    const extraExercises = splitLines(textbook).filter(line => /bài\s*\d|luyện tập|bài tập/i.test(line)).slice(0, 4);
    extraExercises.forEach((ex, idx) => {
      deck.push(slide("exercise", `Bài tập ${idx + 1}`, [
        { text: ex, step: 1, role: "problem" }
      ], { phase: "bai-tap", problem: ex }));
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

  function normalizeType(raw) {
    const type = String(raw || "").trim().toLowerCase();
    if (type === "concept") return "rule";
    if (type === "objective") return "intro";
    return type;
  }

  function normalizeStepEntry(raw, index) {
    if (raw && typeof raw === "object") {
      const label = strip(raw.label || raw.title || "");
      const text = strip(raw.text || raw.content || raw.body || "");
      const combined = label && text && text.indexOf(label) !== 0 ? (label + ": " + text) : (text || label);
      return { label: label || ("Bước " + (index + 1)), text: combined };
    }
    const text = strip(raw);
    const match = text.match(/^(bước\s*\d+)\s*[:.\-–]\s*(.+)$/i);
    if (match) return { label: match[1], text: text };
    return { label: "Bước " + (index + 1), text: text };
  }

  function fallbackSplitContent(content) {
    const lines = splitLines(content);
    let problem = "";
    let explanation = "";
    const steps = [];
    let mode = "body";
    lines.forEach(function (line) {
      if (/^(đề bài|ví dụ|bài toán|tình huống)\b/i.test(line)) {
        mode = "problem";
        problem = line.replace(/^(đề bài|ví dụ[^:]*|bài toán|tình huống)\s*[:.\-–]\s*/i, "");
        return;
      }
      if (/^(phân tích|gợi ý|nhận xét|giải thích)\b/i.test(line)) {
        mode = "explain";
        explanation = line.replace(/^(phân tích|gợi ý|nhận xét|giải thích)\s*[:.\-–]\s*/i, "");
        return;
      }
      if (/^bước\s*\d+/i.test(line) || /^\d+[\.\)]\s+\S/.test(line)) {
        mode = "steps";
        steps.push(line);
        return;
      }
      if (mode === "problem") problem = problem ? problem + " " + line : line;
      else if (mode === "explain") explanation = explanation ? explanation + " " + line : line;
      else if (mode === "steps") steps.push(line);
    });
    return { problem: strip(problem), explanation: strip(explanation), steps: steps };
  }

  function wrapFormula(formula) {
    const inner = String(formula || "").replace(/^\$+|\$+$/g, "").trim();
    if (!inner) return "";
    const display = /\\begin\{|\\frac|\\dfrac|\\\\/.test(inner);
    return display ? "$$" + inner + "$$" : "$" + inner + "$";
  }

  function normalizeAiDeck(payload) {
    const slides = payload && Array.isArray(payload.slides) ? payload.slides : [];
    if (slides.length < MIN_COMPLETE_SLIDES || slides.length > MAX_COMPLETE_SLIDES) {
      throw new Error(`Gemini phải tạo từ ${MIN_COMPLETE_SLIDES} đến ${MAX_COMPLETE_SLIDES} slide (nhận ${slides.length}).`);
    }
    const allowed = new Set(ALLOWED_TYPES);
    const types = new Set();
    const deck = slides.map(function (entry, index) {
      const type = normalizeType(entry && entry.type);
      const title = strip(entry && entry.title);
      let content = strip(entry && entry.content);
      let problem = strip(entry && entry.problem);
      let explanation = strip(entry && entry.explanation);
      let ruleBox = strip(entry && (entry.ruleBox || entry.rule_box));
      let note = strip(entry && entry.note);
      const subtitle = strip(entry && entry.subtitle);
      const formula = strip(entry && entry.mathFormula);
      const rawSteps = Array.isArray(entry && entry.steps) ? entry.steps : [];
      if (isMetaInstruction(content)) content = "";
      if (isMetaInstruction(problem)) problem = "";
      if (isMetaInstruction(explanation)) explanation = "";
      if (isMetaInstruction(ruleBox)) ruleBox = "";
      if (isMetaInstruction(note)) note = "";
      let steps = rawSteps.map(function (item, stepIndex) { return normalizeStepEntry(item, stepIndex); })
        .filter(function (item) { return item.text && !isMetaInstruction(item.text); });
      if (SPLIT_TYPES[type] && (!problem || !steps.length) && content) {
        const split = fallbackSplitContent(content);
        if (!problem && split.problem) problem = split.problem;
        if (!explanation && split.explanation) explanation = split.explanation;
        if (!steps.length && split.steps.length) {
          steps = split.steps.map(function (item, stepIndex) { return normalizeStepEntry(item, stepIndex); })
            .filter(function (item) { return item.text && !isMetaInstruction(item.text); });
        }
      }
      if (!allowed.has(type) || !title || (!content && !formula && !steps.length && !problem && !ruleBox && !explanation && !note && !subtitle)) {
        throw new Error(`Slide ${index + 1} thiếu type/title/content hợp lệ.`);
      }
      types.add(type);
      const items = [];
      if (problem) items.push({ text: problem, step: 1, role: "problem" });
      if (content && content !== problem && content !== ruleBox) {
        items.push({ text: content, step: 1, role: SPLIT_TYPES[type] && !problem ? "problem" : (type === "rule" ? "rule" : "content") });
      }
      if (explanation) items.push({ text: explanation, step: 1, role: "explanation" });
      if (ruleBox && ruleBox !== content) items.push({ text: ruleBox, step: 1, role: "rule" });
      if (formula) items.push({ text: wrapFormula(formula), step: 1, role: "formula" });
      steps.forEach(function (item, stepIndex) {
        items.push({ text: item.text, step: stepIndex + 2, role: "step", label: item.label });
      });
      if (note) items.push({ text: note, step: Math.max(2, steps.length + 2), role: "note" });
      return {
        type,
        title,
        items,
        meta: {
          aiGenerated: true,
          source: "gemini-3-flash-preview",
          subtitle: subtitle,
          problem: problem,
          explanation: explanation,
          ruleBox: ruleBox,
          note: note,
          mathFormula: formula
        }
      };
    });
    ALLOWED_TYPES.forEach(function (type) {
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

  function buildSlidePrompt(ctx) {
    return [
      "Bạn là chuyên gia thiết kế bài giảng trình chiếu 16:9, bám sát SGK. Chỉ dùng NGỮ CẢNH SGK THẬT bên dưới; không bịa đề mục, định nghĩa, ví dụ, bài tập hoặc đáp án.",
      "",
      "BÀI: " + ctx.topic,
      "MÔN: " + ctx.subject + "; LỚP: " + ctx.grade + "; THỜI LƯỢNG: " + ctx.duration,
      "",
      "NGỮ CẢNH SGK THẬT:",
      ctx.textbook,
      "",
      "Hãy tạo đúng 15–25 slide bằng tiếng Việt. Với từng đơn vị kiến thức có trong ngữ cảnh, bắt buộc theo chuỗi Khám phá → Quy tắc/định nghĩa → Ví dụ SGK giải từng bước → Luyện tập SGK. Có bìa, mục tiêu, khởi động, củng cố/vận dụng và tổng kết. Nếu ngữ cảnh không đủ dữ liệu cho một chi tiết, nêu rõ “Cần giáo viên bổ sung từ trang SGK đã tải”, tuyệt đối không bịa.",
      "",
      "HỢP ĐỒNG SƯ PHẠM — mỗi slide phải có nội dung thật, câu giải thật, kết quả thật bám SGK:",
      "- title: title = tên bài; subtitle = môn, khối, thời lượng; content = thông điệp mở đầu.",
      "- intro (mục tiêu): chia rõ 3 nhóm trong steps: Kiến thức cốt lõi; Năng lực bộ môn/công cụ (MTCT/vẽ hình); Phẩm chất/Vận dụng.",
      "- explore: problem = tình huống/câu hỏi mở đầu; steps = nhận xét hoặc kết quả quan sát thật.",
      "- rule: ruleBox = tên quy tắc + nội dung công thức; note = lưu ý cần nhớ; mathFormula = LaTeX nếu có.",
      "- example: problem = đề bài; explanation = phân tích ngắn; steps = lời giải từng bước (Bước 1, Bước 2, Bước 3...) + kết luận nghiệm.",
      "- practice: problem = đề bài luyện tập; explanation = gợi ý phương pháp; steps = lời giải chi tiết (hiện khi click).",
      "- summary: content/steps = sơ đồ tóm tắt kiến thức cốt lõi + hướng dẫn tự học ở nhà.",
      "",
      "CẤM TUYỆT ĐỐI placeholder / chỉ dẫn thao tác giả tạo, ví dụ: \"Hiển thị...\", \"Liệt kê...\", \"Thực hiện...\", \"Xuất hiện...\". Không viết meta-prompt. Mỗi phần tử steps là nội dung toán/văn thật.",
      "Công thức toán để trong mathFormula bằng LaTeX (được phép dùng \\begin{cases}, \\frac, \\text).",
      "",
      "Chỉ trả JSON hợp lệ, không markdown: {\"slides\":[{\"type\":\"title|intro|explore|rule|example|practice|summary\",\"title\":\"...\",\"subtitle\":\"...\",\"content\":\"nội dung thật bám SGK\",\"problem\":\"đề bài thật nếu có\",\"explanation\":\"phân tích hoặc gợi ý\",\"steps\":[{\"label\":\"Bước 1\",\"text\":\"câu giải thật\"}],\"ruleBox\":\"quy tắc đóng khung\",\"note\":\"lưu ý cần nhớ\",\"mathFormula\":\"LaTeX nếu có, không có thì chuỗi rỗng\"}]}."
    ].join("\n");
  }

  async function generateAiLessonSlides(source, signal) {
    const client = typeof geminiAPI !== "undefined" ? geminiAPI : root.geminiAPI;
    if (!client || typeof client.generateContent !== "function") {
      throw new Error("Gemini Canvas chưa sẵn sàng để tạo bài giảng.");
    }
    const ctx = lessonContextFromApp(source);
    client.selectedModel = "gemini-3-flash-preview";
    const prompt = buildSlidePrompt(ctx);
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

  function itemsByRole(items, role) {
    return (items || []).filter(function (item) { return item.role === role; });
  }

  function renderItemHtml(item) {
    const badge = item.role === "step"
      ? `<span class="khbd-step-badge">${escapeHtml(item.label || ("Bước " + item.step))}</span>`
      : "";
    return `<li data-step="${item.step}" data-role="${escapeHtml(item.role || "")}">${badge}${escapeHtml(item.text)}</li>`;
  }

  function renderList(items, className) {
    if (!items || !items.length) return "";
    return `<ul class="${className || "khbd-slide-items"}">${items.map(renderItemHtml).join("")}</ul>`;
  }

  function renderSlideHtml(slideItem, revealed) {
    const type = slideItem && slideItem.type || "";
    const items = visibleItems(slideItem, revealed);
    const meta = (slideItem && slideItem.meta) || {};
    const title = escapeHtml(slideItem && slideItem.title || "");
    if (type === "title") {
      const kicker = escapeHtml(meta.subtitle || (items[0] && items[0].text) || "");
      return `<article class="khbd-slide-card khbd-slide-titlecard" data-type="title">
      <p class="khbd-slide-kicker">${kicker}</p>
      <h2 class="khbd-slide-title">${title}</h2>
      ${renderList(items)}
    </article>`;
    }
    if (type === "rule") {
      const boxItems = items.filter(function (item) { return item.role === "rule" || item.role === "formula" || item.role === "content" || !item.role; });
      const extra = items.filter(function (item) { return item.role === "note" || item.role === "step"; });
      return `<article class="khbd-slide-card" data-type="rule">
      <h2 class="khbd-slide-title">${title}</h2>
      <div class="khbd-slide-rulebox">
        <span class="khbd-slide-rule-label">GHI NHỚ / TRỌNG TÂM</span>
        ${renderList(boxItems)}
      </div>
      ${extra.length ? renderList(extra) : ""}
    </article>`;
    }
    if (SPLIT_TYPES[type]) {
      const left = itemsByRole(items, "problem");
      const hints = itemsByRole(items, "explanation").concat(itemsByRole(items, "formula")).concat(itemsByRole(items, "content"));
      const right = itemsByRole(items, "step").concat(itemsByRole(items, "note"));
      const leftItems = left.length ? left.concat(hints.filter(function (item) { return item.role === "formula"; })) : items.slice(0, 1);
      const rightItems = right.length ? right : items.slice(leftItems.length);
      const leftLabel = type === "explore" ? "Tình huống / Đề bài" : "Đề bài";
      const rightLabel = type === "practice" ? "Gợi ý & lời giải" : "Lời giải";
      return `<article class="khbd-slide-card" data-type="${escapeHtml(type)}">
      <h2 class="khbd-slide-title">${title}</h2>
      <div class="khbd-slide-split">
        <div class="khbd-slide-col-left">
          <div class="khbd-slide-problem">
            <span class="khbd-slide-col-label">${leftLabel}</span>
            ${renderList(leftItems)}
          </div>
        </div>
        <div class="khbd-slide-col-right">
          <div class="khbd-slide-solution">
            <span class="khbd-slide-col-label">${rightLabel}</span>
            ${rightItems.length ? `<ol class="khbd-slide-steps">${rightItems.map(renderItemHtml).join("")}</ol>` : `<p class="khbd-slide-hint">Click để hiện từng bước giải.</p>`}
            ${renderList(hints.filter(function (item) { return item.role === "explanation"; }), "khbd-slide-items khbd-slide-hintlist")}
          </div>
        </div>
      </div>
    </article>`;
    }
    return `<article class="khbd-slide-card" data-type="${escapeHtml(type)}">
      <h2 class="khbd-slide-title">${title}</h2>
      ${renderList(items)}
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

  function roundShape(pptx) {
    return (pptx.ShapeType && (pptx.ShapeType.roundRect || pptx.ShapeType.roundedRect)) || "roundRect";
  }

  function toParagraphs(text, options) {
    const opts = options || {};
    const lines = String(text == null ? "" : text).split(/\n/);
    return lines.map(function (line) {
      return {
        text: line || " ",
        options: Object.assign({ fontFace: "Calibri" }, opts, { breakLine: true })
      };
    });
  }

  function addHeaderBar(page, pptx, title) {
    page.addShape(pptx.ShapeType.rect, { x: 0, y: 0, w: SLIDE_W, h: 0.72, fill: { color: "0F4C81" } });
    page.addText(latexToPlain(title || ""), {
      x: 0.4, y: 0.14, w: 12.5, h: 0.46, fontSize: 22, bold: true, color: "FFFFFF", fontFace: "Calibri"
    });
  }

  function addLabeledCard(page, pptx, spec) {
    page.addShape(roundShape(pptx), {
      x: spec.x,
      y: spec.y,
      w: spec.w,
      h: spec.h,
      fill: { color: spec.fill || "F8FAFC" },
      line: { color: spec.line || "94A3B8", width: 1.15 },
      rectRadius: 0.1
    });
    if (spec.label) {
      page.addText(spec.label, {
        x: spec.x + 0.16,
        y: spec.y + 0.1,
        w: spec.w - 0.32,
        h: 0.28,
        fontSize: 11,
        bold: true,
        color: spec.labelColor || "0F4C81",
        fontFace: "Calibri"
      });
    }
    const paras = spec.paragraphs || [];
    if (!paras.length) return;
    const labelH = spec.label ? 0.4 : 0.12;
    page.addText(paras, {
      x: spec.x + 0.16,
      y: spec.y + labelH,
      w: spec.w - 0.32,
      h: Math.max(0.4, spec.h - labelH - 0.14),
      valign: "top",
      fontFace: "Calibri",
      fontSize: spec.fontSize || 16,
      color: "1F2937",
      margin: 0
    });
  }

  function itemPlain(item) {
    return latexToPlain(item && item.text || "");
  }

  function buildStepParagraphs(items) {
    const paras = [];
    (items || []).forEach(function (item, idx) {
      const label = item.label || (item.role === "step" ? ("Bước " + (idx + 1)) : "");
      const body = itemPlain(item);
      const lines = body.split(/\n/);
      if (label) {
        paras.push({ text: label + "  ", options: { bold: true, color: "0F4C81", breakLine: false, fontFace: "Calibri", fontSize: 15 } });
        paras.push({ text: lines[0] || " ", options: { breakLine: true, fontFace: "Calibri", fontSize: 15, color: "1F2937" } });
        lines.slice(1).forEach(function (line) {
          paras.push({ text: line || " ", options: { breakLine: true, fontFace: "Calibri", fontSize: 15, color: "1F2937" } });
        });
      } else {
        toParagraphs(body, { fontSize: 15, color: "1F2937", breakLine: true }).forEach(function (p) { paras.push(p); });
      }
    });
    if (paras.length) paras[paras.length - 1].options.breakLine = false;
    return paras;
  }

  function renderTitlePptx(page, pptx, item) {
    page.addShape(pptx.ShapeType.rect, { x: 0, y: 0, w: SLIDE_W, h: SLIDE_H, fill: { color: "F8FAFC" } });
    page.addShape(pptx.ShapeType.rect, { x: 0, y: 0, w: SLIDE_W, h: 0.18, fill: { color: "0F4C81" } });
    page.addShape(pptx.ShapeType.rect, { x: 0, y: 7.32, w: SLIDE_W, h: 0.18, fill: { color: "0F4C81" } });
    const subtitle = latexToPlain((item.meta && item.meta.subtitle) || "") || itemPlain((item.items || [])[0]);
    const duration = itemPlain((item.items || []).find(function (entry) { return /tiết|phút/i.test(entry.text || ""); }) || {});
    const message = (item.items || []).filter(function (entry) {
      const plain = itemPlain(entry);
      return plain && plain !== subtitle && plain !== duration;
    }).map(itemPlain).join("\n");
    if (subtitle) {
      page.addText(subtitle, {
        x: 1.2, y: 1.85, w: 10.9, h: 0.4, fontSize: 16, bold: true, color: "0F4C81", align: "center", fontFace: "Calibri"
      });
    }
    page.addText(latexToPlain(item.title || ""), {
      x: 1, y: 2.35, w: 11.3, h: 1.35, fontSize: 34, bold: true, color: "0F4C81", align: "center", valign: "middle", fontFace: "Calibri"
    });
    if (duration) {
      page.addShape(roundShape(pptx), {
        x: 4.55, y: 3.9, w: 4.2, h: 0.48, fill: { color: "EFF6FF" }, line: { color: "0F4C81", width: 1 }, rectRadius: 0.2
      });
      page.addText(duration, {
        x: 4.55, y: 3.94, w: 4.2, h: 0.4, fontSize: 14, align: "center", color: "0F4C81", fontFace: "Calibri", bold: true
      });
    }
    if (message) {
      page.addText(message, {
        x: 1.8, y: 4.6, w: 9.7, h: 1.4, fontSize: 16, align: "center", color: "334155", fontFace: "Calibri", valign: "top"
      });
    }
  }

  function renderSplitPptx(page, pptx, item, idx) {
    addHeaderBar(page, pptx, item.title || ("Slide " + (idx + 1)));
    const items = item.items || [];
    const leftItems = items.filter(function (entry) { return entry.role === "problem" || entry.role === "formula"; });
    const rightItems = items.filter(function (entry) { return entry.role === "step" || entry.role === "note" || entry.role === "explanation"; });
    const fallbackLeft = leftItems.length ? leftItems : items.slice(0, 1);
    const fallbackRight = rightItems.length ? rightItems : items.slice(fallbackLeft.length);
    const top = 0.96;
    const height = 6.22;
    const leftX = 0.35;
    const leftW = 4.85;
    const gap = 0.22;
    const rightX = leftX + leftW + gap;
    const rightW = SLIDE_W - rightX - 0.35;
    const leftParas = [];
    fallbackLeft.forEach(function (entry) {
      toParagraphs(itemPlain(entry), { fontSize: 16, color: "1F2937" }).forEach(function (p) { leftParas.push(p); });
    });
    addLabeledCard(page, pptx, {
      x: leftX, y: top, w: leftW, h: height,
      fill: "F1F5F9", line: "CBD5E1",
      label: item.type === "explore" ? "TÌNH HUỐNG / ĐỀ BÀI" : "ĐỀ BÀI",
      paragraphs: leftParas, fontSize: 16
    });
    addLabeledCard(page, pptx, {
      x: rightX, y: top, w: rightW, h: height,
      fill: "FFFFFF", line: "E2E8F0",
      label: item.type === "practice" ? "GỢI Ý & LỜI GIẢI" : "LỜI GIẢI TỪNG BƯỚC",
      paragraphs: buildStepParagraphs(fallbackRight), fontSize: 15
    });
  }

  function renderRulePptx(page, pptx, item, idx) {
    addHeaderBar(page, pptx, item.title || ("Slide " + (idx + 1)));
    const items = item.items || [];
    const paras = [];
    items.forEach(function (entry) {
      toParagraphs(itemPlain(entry), { fontSize: 18, color: "1F2937" }).forEach(function (p) { paras.push(p); });
    });
    addLabeledCard(page, pptx, {
      x: 0.55, y: 1.05, w: 12.23, h: 5.95,
      fill: "EFF6FF", line: "0F4C81",
      label: "GHI NHỚ / TRỌNG TÂM",
      labelColor: "0F4C81",
      paragraphs: paras,
      fontSize: 18
    });
  }

  function renderDefaultPptx(page, pptx, item, idx) {
    addHeaderBar(page, pptx, item.title || ("Slide " + (idx + 1)));
    const paras = [];
    (item.items || []).forEach(function (entry) {
      toParagraphs(itemPlain(entry), { fontSize: 18, color: "1F2937" }).forEach(function (p) { paras.push(p); });
    });
    addLabeledCard(page, pptx, {
      x: 0.45, y: 1.05, w: 12.43, h: 5.95,
      fill: "FFFFFF", line: "E2E8F0",
      paragraphs: paras,
      fontSize: 18
    });
  }

  async function exportToPptx(slideDeck) {
    const deck = Array.isArray(slideDeck) && slideDeck.length ? slideDeck : ui.deck;
    if (!deck.length) throw new Error("Chưa có slide để xuất PowerPoint.");
    const PptxGenJS = root.PptxGenJS || root.pptxgen;
    if (typeof PptxGenJS !== "function") throw new Error("Chưa nạp được thư viện PptxGenJS.");
    const pptx = new PptxGenJS();
    pptx.defineLayout({ name: "KHBD_16x9", width: SLIDE_W, height: SLIDE_H });
    pptx.layout = "KHBD_16x9";
    pptx.author = "Soạn bài giảng trình chiếu AI";
    pptx.title = (deck[0] && deck[0].title) || "Bai giang";

    deck.forEach((item, idx) => {
      const page = pptx.addSlide();
      if (item.type === "title") renderTitlePptx(page, pptx, item);
      else if (SPLIT_TYPES[item.type]) renderSplitPptx(page, pptx, item, idx);
      else if (item.type === "rule") renderRulePptx(page, pptx, item, idx);
      else renderDefaultPptx(page, pptx, item, idx);
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
    normalizeAiDeck,
    exportToPptx,
    renderSlideHtml,
    latexToPlain,
    estimateTextHeight,
    isMetaInstruction,
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
