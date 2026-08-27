/**
 * js/khbd-docx.js
 * Module xuất file Word (.docx) chuyên nghiệp chuẩn Công văn 5512 & Nghị định 30/2020/NĐ-CP
 * Sử dụng thư viện docx.js (8.x / 9.x) và FileSaver.js.
 * Hỗ trợ chuyển đổi công thức Toán học LaTeX ($...$, $$...$$) thành biểu thức toán đẹp mắt,
 * Định dạng bảng biểu, font Times New Roman, căn lề chuẩn hành chính Việt Nam.
 */

class DocxGenerator {
  constructor() {
    this.fontFamily = "Times New Roman";
    // Times New Roman 13pt; giãn dòng Multiple 1.3; khổ A4; lề trên/dưới/trái/phải 1.5/1.5/2.5/1.5 cm.
    this.fontSizeBody = 26;
    this.fontSizeH1 = 26;
    this.fontSizeH2 = 26;
    this.fontSizeH3 = 26;
    this.lineSpacing = 312;
    this.lineRule = "auto";
    this.spaceAfter = 60;
    this.spaceBefore = 0;

    this.pageMargins = {
      top: 851,
      bottom: 851,
      left: 1418,
      right: 851
    };
    this.pageSize = { width: 11906, height: 16838, orientation: "portrait" };
  }

  /**
   * Chuyển đổi mã LaTeX thành chuỗi ký tự toán học Unicode chuẩn
   */
  latexToUnicodeMath(latex) {
    if (!latex) return "";
    let s = latex.trim();

    // Loại bỏ dấu bao bọc $ hoặc $$
    s = s.replace(/^\$\$|\$\$$/g, "").replace(/^\$|\$$/g, "").trim();

    // Thay thế các phân số \frac{a}{b} -> (a)/(b) hoặc a/b
    s = s.replace(/\\frac\s*\{([^{}]+)\}\s*\{([^{}]+)\}/g, "($1)/($2)");
    s = s.replace(/\\dfrac\s*\{([^{}]+)\}\s*\{([^{}]+)\}/g, "($1)/($2)");

    // Căn bậc hai \sqrt{x} -> √(x), \sqrt[n]{x} -> ⁿ√(x)
    s = s.replace(/\\sqrt\[(\d+)\]\{([^{}]+)\}/g, "$1√($2)");
    s = s.replace(/\\sqrt\{([^{}]+)\}/g, "√($1)");

    // Chỉ số trên / số mũ
    s = s.replace(/\^0/g, "⁰").replace(/\^1/g, "¹").replace(/\^2/g, "²").replace(/\^3/g, "³")
         .replace(/\^4/g, "⁴").replace(/\^5/g, "⁵").replace(/\^6/g, "⁶").replace(/\^7/g, "⁷")
         .replace(/\^8/g, "⁸").replace(/\^9/g, "⁹").replace(/\^n/g, "ⁿ").replace(/\^x/g, "ˣ")
         .replace(/\^\{([0-9a-zA-Z+-]+)\}/g, "^($1)");

    // Chỉ số dưới
    s = s.replace(/_0/g, "₀").replace(/_1/g, "₁").replace(/_2/g, "₂").replace(/_3/g, "₃")
         .replace(/_4/g, "₄").replace(/_5/g, "₅").replace(/_6/g, "₆").replace(/_7/g, "₇")
         .replace(/_8/g, "₈").replace(/_9/g, "₉").replace(/_\{([0-9a-zA-Z+-]+)\}/g, "_($1)");

    // Các ký hiệu toán học phổ biến
    const mathDict = {
      "\\alpha": "α", "\\beta": "β", "\\gamma": "γ", "\\delta": "δ", "\\Delta": "Δ",
      "\\epsilon": "ε", "\\theta": "θ", "\\lambda": "λ", "\\pi": "π", "\\sigma": "σ",
      "\\omega": "ω", "\\Omega": "Ω", "\\le": "≤", "\\leq": "≤", "\\ge": "≥", "\\geq": "≥",
      "\\ne": "≠", "\\neq": "≠", "\\approx": "≈", "\\pm": "±", "\\mp": "∓",
      "\\times": "×", "\\cdot": "·", "\\div": "÷", "\\in": "∈", "\\notin": "∉",
      "\\subset": "⊂", "\\subseteq": "⊆", "\\supset": "⊃", "\\cup": "∪", "\\cap": "∩",
      "\\emptyset": "∅", "\\infty": "∞", "\\forall": "∀", "\\exists": "∃",
      "\\perp": "⊥", "\\parallel": "∥", "\\angle": "∠", "\\triangle": "△",
      "\\degree": "°", "^{\\circ}": "°", "\\rightarrow": "→", "\\Rightarrow": "⇒",
      "\\Leftrightarrow": "⇔", "\\cdots": "...", "\\ldots": "...", "\\text": "",
      "\\mathbf": "", "\\mathrm": "", "\\left": "", "\\right": "", "\\,": " ", "\\;": " ",
      "\\quad": "  ", "\\qquad": "    "
    };

    for (const [tex, uni] of Object.entries(mathDict)) {
      s = s.split(tex).join(uni);
    }

    // Làm sạch các dấu ngoặc nhọn thừa còn sót lại
    s = s.replace(/[{}]/g, "");
    return s.trim();
  }

  /**
   * Chuẩn hoá các lệnh toán thường gặp trước khi bộ đọc Equation xử lý.
   * Chỉ rút gọn dấu gạch chéo kép khi ngay sau đó là một lệnh toán đã biết;
   * vì vậy lệnh xuống dòng LaTex `\\` vẫn được giữ nguyên.
   */
  normalizeLatexForMath(latex) {
    let source = String(latex || "");
    const supportedCommands = [
      "Leftrightarrow", "Rightarrow", "leftarrow", "rightarrow", "overrightarrow", "subseteq", "supseteq",
      "emptyset", "parallel", "triangle", "varepsilon", "displaystyle", "overline", "widehat",
      "mathbb", "mathcal", "mathfrak", "mathrm", "mathbf", "textrm", "textit", "textbf",
      "nolimits", "limits", "dfrac", "tfrac", "cfrac", "notin", "subset", "supset", "forall",
      "exists", "approx", "equiv", "cdots", "ldots", "times", "cdot", "lbrack", "rbrack",
      "lparen", "rparen", "lbrace", "rbrace", "alpha", "gamma", "delta", "Delta", "theta",
      "Theta", "lambda", "sigma", "Sigma", "omega", "Omega", "nabla", "partial", "infty",
      "angle", "perp", "bullet", "degree", "right", "left", "frac", "sqrt", "beta", "epsilon",
      "varepsilon", "pi", "Pi", "phi", "Phi", "psi", "rho", "mu", "nu", "neq", "leq", "geq",
      "dots", "circ", "hbar", "not", "in", "ni", "ne", "le", "ge", "pm", "mp", "ast", "div",
      "cup", "cap", "sim", "to", "ell", "sin", "cos", "tan", "cot", "sec", "csc", "log", "ln",
      "lg", "lim", "max", "min", "gcd", "lcm", "det", "dim", "ker", "hom", "arg", "exp", "sinh",
      "cosh", "tanh", "vec", "hat", "underline", "quad", "qquad", "text"
    ].sort((a, b) => b.length - a.length);
    const isKnownCommand = value => supportedCommands.some(command => value.startsWith(command));

    // Dữ liệu Markdown có thể giữ nguyên escape kép (\\\\notin). Không đụng tới \\ độc lập.
    source = source.replace(/\\{2,}([A-Za-z]+)/g, (match, commandText) => (
      isKnownCommand(commandText) ? `\\${commandText}` : match
    ));

    // Tách theo lệnh dài nhất: \\notinA -> \\notin A, thay vì coi "notinA" là một lệnh lạ.
    source = source.replace(/\\([A-Za-z]+)/g, (match, commandText) => {
      const command = supportedCommands.find(candidate => commandText.startsWith(candidate));
      if (!command) return match;
      const suffix = commandText.slice(command.length);
      return suffix ? `\\${command} ${suffix}` : match;
    });

    return source;
  }

  /** Chuyển LaTeX ($...$, $$...$$, \\(...\\)) thành Equation Word (OMML). Thất bại thì trả null để fallback Unicode. */
  createNativeMath(latex) {
    const mathApi = window.docx;
    const required = ["Math", "MathRun", "MathFraction", "MathSuperScript", "MathSubScript", "MathSubSuperScript", "MathRadical"];
    if (!required.every(name => typeof mathApi[name] === "function")) return null;

    let source = this.normalizeLatexForMath(latex).trim();
    source = source.replace(/^\$\$([\s\S]*)\$\$$/, "$1").replace(/^\$([\s\S]*)\$$/, "$1");
    source = source.replace(/^\\\(([\s\S]*)\\\)$/, "$1").replace(/^\\\[([\s\S]*)\\\]$/, "$1").trim();
    if (!source) return null;
    source = source
      .replace(/\\dfrac\b/g, "\\frac")
      .replace(/\\tfrac\b/g, "\\frac")
      .replace(/\\cfrac\b/g, "\\frac")
      .replace(/\\displaystyle\b/g, "")
      .replace(/\\nolimits\b/g, "")
      .replace(/\\limits\b/g, "");

    const commandMap = {
      alpha: "α", beta: "β", gamma: "γ", delta: "δ", Delta: "Δ", epsilon: "ε", varepsilon: "ε",
      theta: "θ", Theta: "Θ", lambda: "λ", pi: "π", Pi: "Π", sigma: "σ", Sigma: "Σ",
      omega: "ω", Omega: "Ω", phi: "φ", Phi: "Φ", psi: "ψ", rho: "ρ", mu: "μ", nu: "ν",
      in: "∈", notin: "∉", ni: "∋", neq: "≠", ne: "≠", le: "≤", leq: "≤", ge: "≥", geq: "≥",
      times: "×", cdot: "·", div: "÷", pm: "±", mp: "∓", ast: "∗", circ: "∘", bullet: "•",
      to: "→", rightarrow: "→", leftarrow: "←", Rightarrow: "⇒", Leftrightarrow: "⇔",
      triangle: "△", angle: "∠", parallel: "∥", perp: "⊥", cup: "∪", cap: "∩",
      emptyset: "∅", infty: "∞", forall: "∀", exists: "∃", partial: "∂", nabla: "∇",
      subset: "⊂", subseteq: "⊆", supset: "⊃", sim: "∼", approx: "≈", equiv: "≡",
      cdots: "⋯", ldots: "…", dots: "…", degree: "°", ell: "ℓ", hbar: "ℏ",
      lbrack: "[", rbrack: "]", lbrace: "{", rbrace: "}", lparen: "(", rparen: ")"
    };
    const functions = new Set(["sin", "cos", "tan", "cot", "sec", "csc", "log", "ln", "lg", "lim", "max", "min", "gcd", "lcm", "det", "dim", "ker", "hom", "arg", "exp", "sinh", "cosh", "tanh"]);
    const blackboard = { N: "ℕ", Z: "ℤ", Q: "ℚ", R: "ℝ", C: "ℂ", P: "ℙ" };
    let index = 0;
    const run = value => new mathApi.MathRun(String(value ?? ""));
    const skipSpace = () => { while (index < source.length && /\s/.test(source[index])) index++; };
    const peek = () => source[index];

    const wrapBrackets = (open, inner) => {
      if (open === "(" && typeof mathApi.MathRoundBrackets === "function") return [new mathApi.MathRoundBrackets({ children: inner })];
      if (open === "[" && typeof mathApi.MathSquareBrackets === "function") return [new mathApi.MathSquareBrackets({ children: inner })];
      if ((open === "{" || open === "\\{") && typeof mathApi.MathCurlyBrackets === "function") return [new mathApi.MathCurlyBrackets({ children: inner })];
      const close = { "(": ")", "[": "]", "{": "}" }[open] || "";
      return [run(open === "\\{" ? "{" : open), ...inner, run(close)];
    };

    const readGroup = () => {
      skipSpace();
      if (peek() !== "{") return readAtom(true);
      index++;
      const group = readSequence("}");
      if (peek() === "}") index++;
      return group.length ? group : [run("")];
    };

    const readOptionalBracket = (open, close) => {
      skipSpace();
      if (peek() !== open) return null;
      index++;
      const group = readSequence(close);
      if (peek() === close) index++;
      return group;
    };

    const readScriptAtom = () => {
      skipSpace();
      if (peek() === "{") return readGroup();
      if (peek() === "\\") return readAtom(true);
      if (index < source.length) return [run(source[index++])];
      return [run("")];
    };

    const applyScripts = nodes => {
      skipSpace();
      let subScript = null;
      let superScript = null;
      while (peek() === "^" || peek() === "_") {
        const kind = source[index++];
        const script = readScriptAtom();
        if (kind === "^") superScript = script; else subScript = script;
        skipSpace();
      }
      if (subScript && superScript) return [new mathApi.MathSubSuperScript({ children: nodes, subScript, superScript })];
      if (superScript) return [new mathApi.MathSuperScript({ children: nodes, superScript })];
      if (subScript) return [new mathApi.MathSubScript({ children: nodes, subScript })];
      return nodes;
    };

    const readCommandName = () => {
      const match = source.slice(index).match(/^[A-Za-z]+/);
      if (match) {
        index += match[0].length;
        return match[0];
      }
      return source[index++] || "";
    };

    const readAtom = (bare = false) => {
      skipSpace();
      if (index >= source.length) return [];
      let nodes;
      if (peek() === "{") {
        nodes = readGroup();
      } else if (peek() === "\\") {
        index++;
        const command = readCommandName();
        if (command === "frac") {
          nodes = [new mathApi.MathFraction({ numerator: readGroup(), denominator: readGroup() })];
        } else if (command === "sqrt") {
          const degree = readOptionalBracket("[", "]");
          nodes = [new mathApi.MathRadical(degree ? { children: readGroup(), degree } : { children: readGroup() })];
        } else if (command === "mathbb" || command === "mathcal" || command === "mathfrak") {
          skipSpace();
          let letter = "";
          if (peek() === "{") {
            index++;
            while (index < source.length && peek() !== "}") letter += source[index++];
            if (peek() === "}") index++;
            letter = letter.trim();
          } else if (index < source.length) {
            letter = source[index++];
          }
          nodes = [run(command === "mathbb" ? (blackboard[letter] || letter || "ℕ") : letter || command)];
        } else if (command === "text" || command === "mathrm" || command === "mathbf" || command === "textrm" || command === "textit" || command === "textbf") {
          skipSpace();
          if (peek() === "{") {
            index++;
            let text = "";
            let depth = 1;
            while (index < source.length && depth > 0) {
              const ch = source[index++];
              if (ch === "{") depth++;
              else if (ch === "}") depth--;
              if (depth > 0) text += ch;
            }
            nodes = [run(text.replace(/\\,/g, " ").replace(/\\/g, ""))];
          } else {
            nodes = [run("")];
          }
        } else if (command === "left") {
          skipSpace();
          let open = peek() || "(";
          if (open === "\\") {
            index++;
            open = "\\" + readCommandName();
            if (open === "\\{") open = "{";
            if (open === "\\}") open = "}";
          } else {
            index++;
            if (open === ".") open = "";
          }
          const inner = readSequence(null, true);
          nodes = open ? wrapBrackets(open, inner) : inner;
        } else if (command === "right") {
          skipSpace();
          if (peek() === "\\") {
            index++;
            readCommandName();
          } else if (index < source.length) {
            index++;
          }
          nodes = [];
        } else if (command === "{" || command === "}") {
          nodes = [run(command)];
        } else if (command === "," || command === ";" || command === "!" || command === " " || command === "quad" || command === "qquad") {
          nodes = [run(" ")];
        } else if (command === "overline" || command === "hat" || command === "widehat" || command === "vec" || command === "overrightarrow" || command === "underline") {
          nodes = readGroup();
        } else if (commandMap[command]) {
          nodes = [run(commandMap[command])];
        } else if (functions.has(command)) {
          nodes = [run(command)];
        } else {
          const uni = this.latexToUnicodeMath("\\" + command);
          nodes = [run(uni && uni !== "\\" + command ? uni : command)];
        }
      } else if (peek() === "}" || peek() === "]" || peek() === ")") {
        return [];
      } else if (/\d/.test(peek())) {
        let num = "";
        while (index < source.length && /[0-9.]/.test(peek())) num += source[index++];
        nodes = [run(num)];
      } else if (/[A-Za-z]/.test(peek())) {
        nodes = [run(source[index++])];
      } else {
        const ch = source[index++];
        if (ch === "(" || ch === "[") {
          const close = ch === "(" ? ")" : "]";
          const inner = readSequence(close);
          if (peek() === close) index++;
          nodes = wrapBrackets(ch, inner);
        } else {
          nodes = [run(ch)];
        }
      }

      return bare ? nodes : applyScripts(nodes);
    };

    const readSequence = (stop, stopAtRight = false) => {
      const nodes = [];
      while (index < source.length) {
        skipSpace();
        if (stop && peek() === stop) break;
        if (stopAtRight && source.slice(index, index + 6) === "\\right") break;
        if (peek() === "}" && stop !== "}") break;
        const next = readAtom();
        if (!next.length) break;
        nodes.push(...next);
      }
      return nodes;
    };

    try {
      const children = readSequence(null).filter(Boolean);
      if (!children.length) return null;
      return new mathApi.Math({ children });
    } catch (error) {
      console.warn("Không thể chuyển LaTeX sang Equation Word:", source, error);
      return null;
    }
  }

  headingIntegrationColor(title) {
    const text = String(title || "");
    if (/năng lực số/i.test(text)) return "0369A1";
    if (/năng lực\s*AI/i.test(text)) return "6D28D9";
    return null;
  }

  markerRunColor(text) {
    const t = String(text || "").trim();
    if (/^\[?NLS(?::[^\]\n]+)?\]?$/i.test(t)) return { color: "0369A1", shading: "E0F2FE", bold: true };
    if (/^\[?AI(?::[^\]\n]+)?\]?$/i.test(t)) return { color: "6D28D9", shading: "F3E8FF", bold: true };
    return null;
  }

  lineIntegrationColor(text, inherited) {
    const raw = String(text || "");
    const nls = /\*\*\[?NLS(?::[^\]\n]+)?\]?\*\*|\[NLS(?::[^\]\n]+)?\]|\bNLS\b/.test(raw);
    const aiMarker = /\*\*\[?AI(?::[^\]\n]+)?\]?\*\*|\[AI(?::[^\]\n]+)?\]/.test(raw);
    const aiCode = /\d+\.[A-Z]\d+\.\d+/.test(raw) && (/\bAI\b|năng lực\s*AI/i.test(raw) || inherited === "6D28D9");
    const ai = aiMarker || aiCode;
    if (nls && !ai) return "0369A1";
    if (ai && !nls) return "6D28D9";
    return inherited || undefined;
  }

  coloredTextRun(text, extras = {}) {
    const docxApi = (typeof window !== "undefined" && window.docx) || (typeof require !== "undefined" ? require("docx") : {});
    const { TextRun, ShadingType } = docxApi || {};
    if (typeof TextRun !== "function") return { text };
    const props = {
      text,
      font: extras.font || this.fontFamily,
      size: extras.size || this.fontSizeBody
    };
    if (extras.bold) props.bold = true;
    if (extras.italics) props.italics = true;
    if (extras.color) props.color = extras.color;
    if (extras.shading) {
      const clearType = (ShadingType && ShadingType.CLEAR) || "clear";
      props.shading = {
        type: clearType,
        fill: extras.shading
      };
    }
    return new TextRun(props);
  }

  /**
   * Tách một dòng văn bản chứa các công thức $...$ thành danh sách các docx TextRun
   */
  parseInlineTextToRuns(text, color) {
    if (!window.docx) return [];
    const { TextRun } = window.docx;

    const runs = [];
    const regex = /(\$\$[\s\S]+?\$\$|\\\[[\s\S]+?\\\]|\\\([\s\S]+?\\\)|(?<!\$)\$(?!\$)(?:\\.|[^$\n])+?\$(?!\$)|\*\*[\s\S]+?\*\*|(?<!\*)\*(?!\*)[^*\n]+?\*(?!\*)|`[^`]+?`|\[(?:NLS|AI)(?::\s*[^\]\r\n]+)?\])/g;
    let lastIndex = 0;
    let match;

    const pushMath = (token, display) => {
      const math = this.createNativeMath(token);
      if (math) {
        runs.push(math);
        return;
      }
      runs.push(new TextRun({
        text: this.latexToUnicodeMath(token),
        font: "Cambria Math",
        italics: true,
        bold: Boolean(display),
        size: this.fontSizeBody
      }));
    };

    while ((match = regex.exec(text)) !== null) {
      if (match.index > lastIndex) {
        const plain = text.substring(lastIndex, match.index);
        runs.push(this.coloredTextRun(plain, { color }));
      }

      const token = match[0];

      if ((token.startsWith("$$") && token.endsWith("$$")) || (token.startsWith("\\[") && token.endsWith("\\]"))) {
        pushMath(token, true);
      } else if ((token.startsWith("$") && token.endsWith("$")) || (token.startsWith("\\(") && token.endsWith("\\)"))) {
        pushMath(token, false);
      } else if (token.startsWith("**") && token.endsWith("**")) {
        const boldText = token.substring(2, token.length - 2);
        const markerInfo = this.markerRunColor(boldText);
        if (markerInfo) {
          runs.push(this.coloredTextRun(boldText, {
            bold: markerInfo.bold,
            color: markerInfo.color,
            shading: markerInfo.shading
          }));
        } else {
          const subRuns = this.parseInlineTextToRuns(boldText, color);
          subRuns.forEach(r => {
            if (r instanceof TextRun) r.bold = true;
          });
          runs.push(...subRuns);
        }
      } else if (token.startsWith("[") && (token.startsWith("[NLS") || token.startsWith("[AI"))) {
        const markerInfo = this.markerRunColor(token);
        if (markerInfo) {
          runs.push(this.coloredTextRun(token, {
            bold: markerInfo.bold,
            color: markerInfo.color,
            shading: markerInfo.shading
          }));
        } else {
          runs.push(this.coloredTextRun(token, { color }));
        }
      } else if (token.startsWith("*") && token.endsWith("*")) {
        const italicText = token.substring(1, token.length - 1);
        runs.push(this.coloredTextRun(italicText, { italics: true, color }));
      } else if (token.startsWith("`") && token.endsWith("`")) {
        const codeText = token.substring(1, token.length - 1);
        runs.push(new TextRun({
          text: codeText,
          font: this.fontFamily,
          size: this.fontSizeBody,
          color: "A020F0"
        }));
      }

      lastIndex = regex.lastIndex;
    }

    if (lastIndex < text.length) {
      const remaining = text.substring(lastIndex);
      runs.push(this.coloredTextRun(remaining, { color }));
    }

    if (runs.length === 0) {
      runs.push(this.coloredTextRun("", { color }));
    }

    return runs;
  }

  /**
   * Phân tích nội dung Markdown thành các phần tử docx (Paragraphs, Tables, Headings)
   */
  parseMarkdownToDocxElements(markdown) {
    if (!window.docx) {
      throw new Error("Thư viện docx.js chưa được tải!");
    }

    const {
      Paragraph, TextRun, Table, TableRow, TableCell, WidthType,
      AlignmentType, BorderStyle, ShadingType
    } = window.docx;

    const cleanMarkdown = typeof sanitizeLessonMarkdown === "function" ? sanitizeLessonMarkdown(markdown) : String(markdown || "");
    const elements = [];
    const lines = cleanMarkdown.split(/\r?\n/);
    let i = 0;
    let runColor = null;

    while (i < lines.length) {
      const line = lines[i];
      const trimmed = line.trim();

      // Dòng trống
      if (!trimmed) {
        i++;
        continue;
      }

      // 1. Phân tích BẢNG MARKDOWN (| Cột 1 | Cột 2 | ...)
      if (trimmed.startsWith("|") && trimmed.endsWith("|")) {
        const tableLines = [];
        while (i < lines.length && lines[i].trim().startsWith("|") && lines[i].trim().endsWith("|")) {
          tableLines.push(lines[i].trim());
          i++;
        }

        if (tableLines.length >= 2) {
          const docxTable = this.createDocxTableFromMarkdown(tableLines);
          if (docxTable) {
            elements.push(docxTable);
            // Thêm khoảng cách sau bảng
            elements.push(new Paragraph({
              spacing: { before: 60, after: 120 }
            }));
          }
          continue;
        }
      }

      // 2. Phân tích TIÊU ĐỀ (# H1, ## H2, ### H3, #### H4)
      if (trimmed.startsWith("# ")) {
        const headingText = trimmed.substring(2).trim();
        runColor = this.headingIntegrationColor(headingText);
        elements.push(new Paragraph({
          spacing: { before: 0, after: this.spaceAfter, line: this.lineSpacing, lineRule: this.lineRule },
          children: [
            this.coloredTextRun(headingText, { size: this.fontSizeH1, bold: true, color: runColor })
          ]
        }));
        i++;
        continue;
      }

      if (trimmed.startsWith("## ")) {
        const headingText = trimmed.substring(3).trim();
        runColor = this.headingIntegrationColor(headingText);
        elements.push(new Paragraph({
          spacing: { before: 0, after: this.spaceAfter, line: this.lineSpacing, lineRule: this.lineRule },
          children: [
            this.coloredTextRun(headingText, { size: this.fontSizeH2, bold: true, color: runColor })
          ]
        }));
        i++;
        continue;
      }

      if (trimmed.startsWith("### ")) {
        const headingText = trimmed.substring(4).trim();
        runColor = this.headingIntegrationColor(headingText);
        elements.push(new Paragraph({
          spacing: { before: 0, after: this.spaceAfter, line: this.lineSpacing, lineRule: this.lineRule },
          children: [
            this.coloredTextRun(headingText, { size: this.fontSizeH3, bold: true, color: runColor })
          ]
        }));
        i++;
        continue;
      }

      if (trimmed.startsWith("#### ")) {
        const headingText = trimmed.substring(5).trim();
        runColor = this.headingIntegrationColor(headingText);
        elements.push(new Paragraph({
          spacing: { before: 0, after: this.spaceAfter, line: this.lineSpacing, lineRule: this.lineRule },
          children: [
            this.coloredTextRun(headingText, {
              size: this.fontSizeBody,
              bold: true,
              italics: true,
              color: runColor || "111111"
            })
          ]
        }));
        i++;
        continue;
      }

      const illustrationMatch = trimmed.match(/^!\[([^\]]*)\]\(khbd-ill:([^)]+)\)$/);
      if (illustrationMatch) {
        const imageBlock = this.createIllustrationParagraphs(illustrationMatch[1], illustrationMatch[2]);
        if (imageBlock.length) {
          elements.push(...imageBlock);
          i++;
          continue;
        }
      }

      // 3. Phân tích ĐƯỜNG KẺ NGANG (--- hoặc ***)
      if (trimmed === "---" || trimmed === "***" || trimmed === "___") {
        elements.push(new Paragraph({
          spacing: { before: 120, after: 120 },
          border: {
            bottom: {
              color: "CCCCCC",
              space: 1,
              style: BorderStyle.SINGLE,
              size: 6
            }
          }
        }));
        i++;
        continue;
      }

      // 4. Danh sách KHBD ba cấp: - (ý lớn), + (ý con), . (ý chi tiết); vẫn đọc • cũ.
      const literalListMatch = line.match(/^(\s*)([-+.•])\s+(.+)$/);
      if (literalListMatch) {
        const [, indent, marker, contentText] = literalListMatch;
        const level = marker === "-" ? 0 : marker === "+" ? 1 : 2;
        const lineColor = this.lineIntegrationColor(contentText, runColor);
        const runs = this.parseInlineTextToRuns(`${marker} ${contentText}`, lineColor);
        elements.push(new Paragraph({
          indent: level ? { left: Math.max(level * 360, indent.length * 180) } : undefined,
          spacing: { before: 40, after: this.spaceAfter, line: this.lineSpacing, lineRule: this.lineRule },
          children: runs
        }));
        i++;
        continue;
      }

      // 4b. Danh sách legacy dùng dấu * vẫn giữ Word bullet.
      if (/^\*\s+/.test(trimmed)) {
        const bulletText = trimmed.replace(/^\*\s+/, "");
        const lineColor = this.lineIntegrationColor(bulletText, runColor);
        const runs = this.parseInlineTextToRuns(bulletText, lineColor);
        elements.push(new Paragraph({
          bullet: { level: 0 },
          spacing: { before: 40, after: this.spaceAfter, line: this.lineSpacing, lineRule: this.lineRule },
          children: runs
        }));
        i++;
        continue;
      }

      // 5. Phân tích DANH SÁCH ĐÁNH SỐ (1. 2. a) b)...)
      if (/^(\d+\.|\b[a-z]\))\s+/.test(trimmed)) {
        const matchNum = trimmed.match(/^(\d+\.|\b[a-z]\))\s+/);
        const prefix = matchNum[0].trimEnd() + " ";
        const contentText = trimmed.substring(matchNum[0].length);
        const headingColor = this.headingIntegrationColor(contentText);
        if (headingColor) runColor = headingColor;
        else if (/^\d+\./.test(trimmed)) runColor = null;
        const lineColor = this.lineIntegrationColor(contentText, runColor);
        const runs = this.parseInlineTextToRuns(contentText, lineColor);

        elements.push(new Paragraph({
          spacing: { before: 40, after: this.spaceAfter, line: this.lineSpacing, lineRule: this.lineRule },
          children: [
            this.coloredTextRun(prefix, { bold: true, color: lineColor }),
            ...runs
          ]
        }));
        i++;
        continue;
      }

      // 6. Phân tích BLOCKQUOTE (> ...)
      if (trimmed.startsWith("> ")) {
        const quoteText = trimmed.substring(2).trim();
        const lineColor = this.lineIntegrationColor(quoteText, runColor);
        const runs = this.parseInlineTextToRuns(quoteText, lineColor);
        elements.push(new Paragraph({
          spacing: { before: 80, after: this.spaceAfter, line: this.lineSpacing, lineRule: this.lineRule },
          indent: { left: 567 }, // lùi 1cm
          children: runs
        }));
        i++;
        continue;
      }

      // 7. ĐOẠN VĂN BẢN BÌNH THƯỜNG
      const lineColor = this.lineIntegrationColor(trimmed, runColor);
      const runs = this.parseInlineTextToRuns(trimmed, lineColor);
      elements.push(new Paragraph({
        spacing: { before: this.spaceBefore, after: this.spaceAfter, line: this.lineSpacing, lineRule: this.lineRule },
        children: runs
      }));

      i++;
    }

    return elements;
  }

  /**
   * Tạo bảng docx từ các dòng markdown (| a | b |)
   */
  createDocxTableFromMarkdown(tableLines) {
    if (!window.docx || tableLines.length < 2) return null;
    const { Table, TableRow, TableCell, Paragraph, TextRun, WidthType, BorderStyle, VerticalAlign, TableLayoutType } = window.docx;

    // Lọc bỏ dòng phân cách (|:---|:---:|)
    const validLines = tableLines.filter(line => !/^[|\s-:]+$/.test(line));
    if (validLines.length === 0) return null;

    const rows = [];
    const tableWidth = 9637;
    const columnCount = Math.max(...validLines.map(line => this.splitMarkdownTableRow(line).length));
    const headerCells = this.splitMarkdownTableRow(validLines[0]).map(cell => cell.toLowerCase());
    const isActivityTwoCol = columnCount === 2 && headerCells.some(cell => cell.includes("hoạt động của gv") || cell.includes("nội dung"));
    const columnWidths = isActivityTwoCol
      ? [4818, 4819]
      : Array.from({ length: columnCount }, () => Math.floor(tableWidth / columnCount));

    validLines.forEach((line, rowIndex) => {
      const rawCells = this.splitMarkdownTableRow(line);
      const isHeader = (rowIndex === 0);

      const tableCells = Array.from({ length: columnCount }, (_, columnIndex) => {
        const cellText = rawCells[columnIndex] || "";
        const paragraphs = this.parseTableCellParagraphs(cellText, isHeader);
        return new TableCell({
          children: paragraphs.length ? paragraphs : [new Paragraph({ children: [new TextRun({ text: "", font: this.fontFamily, size: this.fontSizeBody })] })],
          margins: { top: 50, bottom: 50, left: 50, right: 50 },
          verticalAlign: VerticalAlign?.TOP,
          width: { size: columnWidths[columnIndex], type: WidthType.DXA }
        });
      });

      rows.push(new TableRow({
        children: tableCells,
        tableHeader: isHeader,
        cantSplit: isHeader
      }));
    });

    const borderStyle = {
      style: BorderStyle.SINGLE,
      size: 6,
      color: "000000"
    };

    return new Table({
      rows: rows,
      width: { size: tableWidth, type: WidthType.DXA },
      columnWidths,
      layout: TableLayoutType?.FIXED,
      borders: {
        top: borderStyle,
        bottom: borderStyle,
        left: borderStyle,
        right: borderStyle,
        insideHorizontal: borderStyle,
        insideVertical: borderStyle
      }
    });
  }

  splitMarkdownTableRow(line) {
    if (typeof splitKhbdMarkdownTableRow === "function") return splitKhbdMarkdownTableRow(line);
    const cells = [];
    let cell = "";
    let escaped = false;
    let math = 0;
    const content = String(line || "").trim().replace(/^\||\|$/g, "");
    for (let index = 0; index < content.length; index++) {
      const character = content[index];
      const next = content[index + 1];
      if (escaped) {
        cell += character;
        escaped = false;
      } else if (character === "\\" && next === "|") {
        escaped = true;
      } else if (character === "$") {
        if (next === "$") {
          cell += "$$";
          index++;
          math = math === 2 ? 0 : 2;
        } else {
          cell += "$";
          math = math === 1 ? 0 : 1;
        }
      } else if (character === "|" && math === 0) {
        cells.push(cell.trim());
        cell = "";
      } else {
        cell += character;
      }
    }
    cells.push(cell.trim());
    return cells;
  }

  parseTableCellRuns(text) {
    const { TextRun } = window.docx;
    const lines = String(text || "").replace(/<br\s*\/?>/gi, "\n").split("\n");
    return lines.flatMap((line, index) => {
      const lineColor = this.lineIntegrationColor(line, null);
      const runs = this.parseInlineTextToRuns(line, lineColor);
      if (index < lines.length - 1) runs.push(new TextRun({ break: 1 }));
      return runs;
    });
  }

  parseTableCellParagraphs(text, isHeader = false) {
    const { Paragraph } = window.docx;
    const lines = String(text || "").replace(/<br\s*\/?>/gi, "\n").split("\n").map(line => line.trim());
    const usable = lines.length ? lines : [""];
    return usable.map(line => {
      const listMatch = !isHeader ? line.match(/^([-+.•])\s+(.+)$/) : null;
      const marker = listMatch ? listMatch[1] : "";
      const contentText = listMatch ? listMatch[2] : line;
      const displayLine = listMatch ? `${marker} ${contentText}` : (line || " ");
      const indentLeft = marker === "+" ? 360 : (marker === "." || marker === "•") ? 720 : 0;
      const lineColor = isHeader ? undefined : this.lineIntegrationColor(displayLine, null);
      const runs = isHeader
        ? [this.coloredTextRun(line || " ", { bold: true })]
        : this.parseInlineTextToRuns(displayLine, lineColor);
      return new Paragraph({
        indent: indentLeft ? { left: indentLeft } : undefined,
        spacing: { before: 20, after: 20, line: this.lineSpacing, lineRule: this.lineRule },
        children: runs.length ? runs : [this.coloredTextRun(displayLine || "", { bold: isHeader, color: lineColor })]
      });
    });
  }

  /**
   * Tạo phần Header trang trọng cho Giáo án chuẩn (Tên trường, Tổ, Tên bài, Ngày soạn...)
   */
  createDocumentHeader(lessonInfo = {}) {
    if (!window.docx) return [];
    const { Paragraph, TextRun, AlignmentType } = window.docx;

    const schoolName = lessonInfo.school || "TRƯỜNG ....................................................";
    const groupName = lessonInfo.subjectGroup || "TỔ CHUYÊN MÔN: ................................................";
    const teacherName = lessonInfo.teacher || "................................................";
    const subject = (lessonInfo.subject || "MÔN HỌC").toUpperCase();
    const topic = (lessonInfo.topic || "KẾ HOẠCH BÀI DẠY").toUpperCase();
    const grade = lessonInfo.grade ? String(lessonInfo.grade) : "";
    const duration = lessonInfo.duration || "02 tiết";
    const dateDraft = lessonInfo.dateDraft || ".../.../...";
    const dateTeach = lessonInfo.dateTeach || ".../.../...";

    const headers = [];

    headers.push(new Paragraph({
      alignment: AlignmentType.LEFT,
      spacing: { before: 0, after: this.spaceAfter, line: this.lineSpacing, lineRule: this.lineRule },
      children: [
        new TextRun({ text: `TRƯỜNG: ${schoolName}`, font: this.fontFamily, size: this.fontSizeBody })
      ]
    }));
    headers.push(new Paragraph({
      alignment: AlignmentType.LEFT,
      spacing: { before: 0, after: this.spaceAfter, line: this.lineSpacing, lineRule: this.lineRule },
      children: [
        new TextRun({ text: `TỔ CHUYÊN MÔN: ${groupName}`, font: this.fontFamily, size: this.fontSizeBody })
      ]
    }));
    headers.push(new Paragraph({
      alignment: AlignmentType.LEFT,
      spacing: { before: 0, after: this.spaceAfter, line: this.lineSpacing, lineRule: this.lineRule },
      children: [
        new TextRun({ text: `HỌ VÀ TÊN GIÁO VIÊN: ${teacherName}`, font: this.fontFamily, size: this.fontSizeBody })
      ]
    }));
    headers.push(new Paragraph({
      alignment: AlignmentType.LEFT,
      spacing: { before: 0, after: this.spaceAfter, line: this.lineSpacing, lineRule: this.lineRule },
      children: [
        new TextRun({ text: `Ngày soạn: ${dateDraft}`, font: this.fontFamily, size: this.fontSizeBody })
      ]
    }));
    headers.push(new Paragraph({
      alignment: AlignmentType.LEFT,
      spacing: { before: 0, after: this.spaceAfter, line: this.lineSpacing, lineRule: this.lineRule },
      children: [
        new TextRun({ text: `Ngày dạy: ${dateTeach}`, font: this.fontFamily, size: this.fontSizeBody })
      ]
    }));

    headers.push(new Paragraph({
      alignment: AlignmentType.LEFT,
      spacing: { before: 0, after: this.spaceAfter, line: this.lineSpacing, lineRule: this.lineRule },
      children: [
        new TextRun({
          text: "KẾ HOẠCH BÀI DẠY",
          font: this.fontFamily,
          size: this.fontSizeH1,
          bold: true
        })
      ]
    }));
    headers.push(new Paragraph({
      alignment: AlignmentType.LEFT,
      spacing: { before: 0, after: this.spaceAfter, line: this.lineSpacing, lineRule: this.lineRule },
      children: [new TextRun({ text: `TÊN BÀI SOẠN: ${topic}`, font: this.fontFamily, size: this.fontSizeBody, bold: true })]
    }));
    headers.push(new Paragraph({
      alignment: AlignmentType.LEFT,
      spacing: { before: 0, after: this.spaceAfter, line: this.lineSpacing, lineRule: this.lineRule },
      children: [new TextRun({ text: `MÔN HỌC: ${subject} - LỚP: ${grade}`, font: this.fontFamily, size: this.fontSizeBody, bold: true })]
    }));
    headers.push(new Paragraph({
      alignment: AlignmentType.LEFT,
      spacing: { before: 0, after: this.spaceAfter, line: this.lineSpacing, lineRule: this.lineRule },
      children: [new TextRun({ text: `THỜI LƯỢNG THỰC HIỆN: ${duration}`, font: this.fontFamily, size: this.fontSizeBody, bold: true })]
    }));

    return headers;
  }

  illustrationCatalog() {
    if (typeof appState !== "undefined" && Array.isArray(appState.content?.illustrations)) {
      return appState.content.illustrations;
    }
    if (typeof window !== "undefined" && Array.isArray(window.appState?.content?.illustrations)) {
      return window.appState.content.illustrations;
    }
    if (typeof global !== "undefined" && Array.isArray(global.appState?.content?.illustrations)) {
      return global.appState.content.illustrations;
    }
    return [];
  }

  createIllustrationParagraphs(altText, illustrationId) {
    const docxApi = window.docx || (typeof require !== "undefined" ? require("docx") : {});
    const { Paragraph, ImageRun, AlignmentType } = docxApi || {};
    const ill = this.illustrationCatalog().find(item => item && item.id === illustrationId);
    if (!ill || (!ill.dataUrl && !ill.svgContent) || typeof ImageRun !== "function") return [];
    try {
      let dataUrl = ill.dataUrl;
      // Nếu chưa có dataUrl nhưng có svgContent dạng base64 trong môi trường Node.js
      if (!dataUrl && ill.svgContent && typeof Buffer !== "undefined") {
        const b64Svg = Buffer.from(ill.svgContent).toString("base64");
        dataUrl = `data:image/svg+xml;base64,${b64Svg}`;
      }
      if (!dataUrl) return [];

      const comma = String(dataUrl).indexOf(",");
      const header = comma >= 0 ? dataUrl.slice(0, comma) : "";
      const b64 = comma >= 0 ? dataUrl.slice(comma + 1) : "";
      
      let bytes;
      if (typeof atob === "function") {
        const binary = atob(b64);
        bytes = new Uint8Array(binary.length);
        for (let i = 0; i < binary.length; i++) bytes[i] = binary.charCodeAt(i);
      } else if (typeof Buffer !== "undefined") {
        bytes = Buffer.from(b64, "base64");
      } else {
        return [];
      }

      const type = /jpe?g/i.test(header) ? "jpg" : (/svg/i.test(header) ? "svg" : "png");
      const caption = altText || ill.caption || ill.title || illustrationId;
      const kind = ill.kind === "thuc_te" ? "Hình thực tế" : "Hình chuẩn SGK";

      return [
        new Paragraph({
          alignment: AlignmentType.CENTER,
          spacing: { before: 140, after: 80 },
          children: [
            new ImageRun({
              data: bytes,
              transformation: { width: 320, height: 240 },
              type: type === "jpg" ? "jpg" : (type === "svg" ? "svg" : "png")
            })
          ]
        }),
        new Paragraph({
          alignment: AlignmentType.CENTER,
          spacing: { before: 0, after: 80, line: this.lineSpacing, lineRule: this.lineRule },
          children: [
            this.coloredTextRun(`${kind}. ${caption}`, {
              italics: true,
              size: 22,
              color: "475569"
            })
          ]
        })
      ];
    } catch (error) {
      console.warn("Không nhúng được hình minh họa vào Word:", error);
      return [];
    }
  }

  /**
   * Xuất file Word (.docx) cho 1 Tab riêng lẻ
   */
  async exportSingleTab(tabTitle, markdownContent, fileName = "Noi_Dung_Giao_An.docx") {
    if (!window.docx || !window.saveAs) {
      throw new Error("Thư viện docx hoặc FileSaver chưa sẵn sàng. Vui lòng kiểm tra kết nối mạng CDN.");
    }

    const { Document, Packer } = window.docx;
    const bodyElements = this.parseMarkdownToDocxElements(markdownContent);

    const doc = new Document({
      creator: "Trợ lý Soạn Kế hoạch Bài dạy AI",
      title: tabTitle,
      description: `Xuất phần ${tabTitle} chuẩn Công văn 5512`,
      sections: [{
        properties: {
          page: {
            size: this.pageSize,
            margin: this.pageMargins
          }
        },
        children: bodyElements
      }]
    });

    const blob = await Packer.toBlob(doc);
    window.saveAs(blob, fileName.endsWith(".docx") ? fileName : `${fileName}.docx`);
  }

  /**
   * Xuất toàn bộ Giáo án hoàn chỉnh thành 1 file Word .docx duy nhất
   */
  async exportFullLessonPlan(lessonInfo, fullMarkdownContent, fileName = "Giao_An.docx") {
    if (!window.docx || !window.saveAs) {
      throw new Error("Thư viện docx hoặc FileSaver chưa sẵn sàng. Vui lòng kiểm tra kết nối mạng CDN.");
    }

    const { Document, Packer } = window.docx;

    // Tạo phần Header trang trọng
    const headerElements = this.createDocumentHeader(lessonInfo);

    // Tạo phần thân từ Markdown
    const bodyElements = this.parseMarkdownToDocxElements(fullMarkdownContent);

    const allChildren = [...headerElements, ...bodyElements];

    const doc = new Document({
      creator: "Trợ lý Soạn Kế hoạch Bài dạy AI",
      title: `KHBD_${lessonInfo.topic || "Bai_Day"}`,
      description: "Kế hoạch bài dạy chuẩn Công văn 5512",
      sections: [{
        properties: {
          page: {
            size: this.pageSize,
            margin: this.pageMargins
          }
        },
        children: allChildren
      }]
    });

    const blob = await Packer.toBlob(doc);
    window.saveAs(blob, fileName.endsWith(".docx") ? fileName : `${fileName}.docx`);
  }
}

// Khởi tạo instance toàn cục
const docxGenerator = new DocxGenerator();

if (typeof module !== 'undefined' && module.exports) {
  module.exports = { DocxGenerator, docxGenerator };
}
