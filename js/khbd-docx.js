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
    // demo.docx uses Times New Roman 13 pt, single spacing, on Letter paper.
    this.fontSizeBody = 26;
    this.fontSizeH1 = 26;
    this.fontSizeH2 = 26;
    this.fontSizeH3 = 26;
    this.lineSpacing = 240;
    this.spaceAfter = 120;  // 6pt
    this.spaceBefore = 0;

    // Khớp khổ giấy và lề 1 inch của demo.docx (đơn vị dxa).
    this.pageMargins = {
      top: 1440,
      bottom: 1440,
      left: 1440,
      right: 1440
    };
    this.pageSize = { width: 12240, height: 15840, orientation: "portrait" };
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

  /** Chuyển LaTeX ($...$, $$...$$, \\(...\\)) thành Equation Word (OMML). Thất bại thì trả null để fallback Unicode. */
  createNativeMath(latex) {
    const mathApi = window.docx;
    const required = ["Math", "MathRun", "MathFraction", "MathSuperScript", "MathSubScript", "MathSubSuperScript", "MathRadical"];
    if (!required.every(name => typeof mathApi[name] === "function")) return null;

    let source = String(latex || "").trim();
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

  /**
   * Tách một dòng văn bản chứa các công thức $...$ thành danh sách các docx TextRun
   */
  parseInlineTextToRuns(text) {
    if (!window.docx) return [];
    const { TextRun } = window.docx;

    const runs = [];
    const regex = /(\$\$[\s\S]+?\$\$|\\\[[\s\S]+?\\\]|\\\([\s\S]+?\\\)|(?<!\$)\$(?!\$)(?:\\.|[^$\n])+?\$(?!\$)|\*\*[\s\S]+?\*\*|(?<!\*)\*(?!\*)[^*\n]+?\*(?!\*)|`[^`]+?`)/g;
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
        runs.push(new TextRun({
          text: plain,
          font: this.fontFamily,
          size: this.fontSizeBody
        }));
      }

      const token = match[0];

      if ((token.startsWith("$$") && token.endsWith("$$")) || (token.startsWith("\\[") && token.endsWith("\\]"))) {
        pushMath(token, true);
      } else if ((token.startsWith("$") && token.endsWith("$")) || (token.startsWith("\\(") && token.endsWith("\\)"))) {
        pushMath(token, false);
      } else if (token.startsWith("**") && token.endsWith("**")) {
        const boldText = token.substring(2, token.length - 2);
        const subRuns = this.parseInlineTextToRuns(boldText);
        subRuns.forEach(r => {
          if (r instanceof TextRun) r.bold = true;
        });
        runs.push(...subRuns);
      } else if (token.startsWith("*") && token.endsWith("*")) {
        // Chữ in nghiêng
        const italicText = token.substring(1, token.length - 1);
        runs.push(new TextRun({
          text: italicText,
          font: this.fontFamily,
          size: this.fontSizeBody,
          italics: true
        }));
      } else if (token.startsWith("`") && token.endsWith("`")) {
        // Code snippet
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

    // Phần văn bản còn lại sau match cuối
    if (lastIndex < text.length) {
      const remaining = text.substring(lastIndex);
      runs.push(new TextRun({
        text: remaining,
        font: this.fontFamily,
        size: this.fontSizeBody
      }));
    }

    if (runs.length === 0) {
      runs.push(new TextRun({ text: "", font: this.fontFamily, size: this.fontSizeBody }));
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

    const elements = [];
    const lines = markdown.split(/\r?\n/);
    let i = 0;

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
        elements.push(new Paragraph({
          spacing: { before: 0, after: this.spaceAfter, line: this.lineSpacing },
          children: [
            new TextRun({
              text: trimmed.substring(2).trim(),
              font: this.fontFamily,
              size: this.fontSizeH1,
              bold: true
            })
          ]
        }));
        i++;
        continue;
      }

      if (trimmed.startsWith("## ")) {
        elements.push(new Paragraph({
          spacing: { before: 0, after: this.spaceAfter, line: this.lineSpacing },
          children: [
            new TextRun({
              text: trimmed.substring(3).trim(),
              font: this.fontFamily,
              size: this.fontSizeH2,
              bold: true
            })
          ]
        }));
        i++;
        continue;
      }

      if (trimmed.startsWith("### ")) {
        elements.push(new Paragraph({
          spacing: { before: 0, after: this.spaceAfter, line: this.lineSpacing },
          children: [
            new TextRun({
              text: trimmed.substring(4).trim(),
              font: this.fontFamily,
              size: this.fontSizeH3,
              bold: true
            })
          ]
        }));
        i++;
        continue;
      }

      if (trimmed.startsWith("#### ")) {
        elements.push(new Paragraph({
          spacing: { before: 0, after: this.spaceAfter, line: this.lineSpacing },
          children: [
            new TextRun({
              text: trimmed.substring(5).trim(),
              font: this.fontFamily,
              size: this.fontSizeBody,
              bold: true,
              italics: true,
              color: "111111"
            })
          ]
        }));
        i++;
        continue;
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

      // 4. Danh sách KHBD: giữ nguyên ký tự - (ý lớn) và + (ý con) thay vì Word bullet.
      const literalListMatch = line.match(/^(\s*)([-+])\s+(.+)$/);
      if (literalListMatch) {
        const [, indent, marker, contentText] = literalListMatch;
        const runs = this.parseInlineTextToRuns(`${marker} ${contentText}`);
        elements.push(new Paragraph({
          indent: marker === "+" ? { left: Math.max(360, indent.length * 180) } : undefined,
          spacing: { before: 40, after: 120, line: this.lineSpacing },
          children: runs
        }));
        i++;
        continue;
      }

      // 4b. Danh sách legacy dùng dấu * vẫn giữ Word bullet.
      if (/^\*\s+/.test(trimmed)) {
        const bulletText = trimmed.replace(/^\*\s+/, "");
        const runs = this.parseInlineTextToRuns(bulletText);
        elements.push(new Paragraph({
          bullet: { level: 0 },
          spacing: { before: 40, after: 120, line: this.lineSpacing },
          children: runs
        }));
        i++;
        continue;
      }

      // 5. Phân tích DANH SÁCH ĐÁNH SỐ (1. 2. a) b)...)
      if (/^(\d+\.|\b[a-z]\))\s+/.test(trimmed)) {
        const matchNum = trimmed.match(/^(\d+\.|\b[a-z]\))\s+/);
        const prefix = matchNum[0];
        const contentText = trimmed.substring(prefix.length);
        const runs = this.parseInlineTextToRuns(contentText);

        elements.push(new Paragraph({
          spacing: { before: 40, after: 120, line: this.lineSpacing },
          children: [
            new TextRun({
              text: prefix + " ",
              font: this.fontFamily,
              size: this.fontSizeBody,
              bold: true
            }),
            ...runs
          ]
        }));
        i++;
        continue;
      }

      // 6. Phân tích BLOCKQUOTE (> ...)
      if (trimmed.startsWith("> ")) {
        const quoteText = trimmed.substring(2).trim();
        const runs = this.parseInlineTextToRuns(quoteText);
        elements.push(new Paragraph({
          spacing: { before: 80, after: 120, line: this.lineSpacing },
          indent: { left: 567 }, // lùi 1cm
          children: runs
        }));
        i++;
        continue;
      }

      // 7. ĐOẠN VĂN BẢN BÌNH THƯỜNG
      const runs = this.parseInlineTextToRuns(trimmed);
      elements.push(new Paragraph({
        spacing: { before: this.spaceBefore, after: this.spaceAfter, line: this.lineSpacing },
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
    // Vùng nội dung của Letter với lề 1 inch là 9.360 dxa, đúng demo.docx.
    const tableWidth = 9360;
    const columnCount = Math.max(...validLines.map(line => this.splitMarkdownTableRow(line).length));
    const headerCells = this.splitMarkdownTableRow(validLines[0]).map(cell => cell.toLowerCase());
    const isActivityTwoCol = columnCount === 2 && headerCells.some(cell => cell.includes("hoạt động của gv") || cell.includes("nội dung"));
    const columnWidths = isActivityTwoCol
      ? [4680, 4680]
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
    const cells = [];
    let cell = "";
    let escaped = false;
    const content = String(line || "").trim().replace(/^\||\|$/g, "");
    for (const character of content) {
      if (escaped) {
        cell += character;
        escaped = false;
      } else if (character === "\\") {
        escaped = true;
      } else if (character === "|") {
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
      const runs = this.parseInlineTextToRuns(line);
      if (index < lines.length - 1) runs.push(new TextRun({ break: 1 }));
      return runs;
    });
  }

  parseTableCellParagraphs(text, isHeader = false) {
    const { Paragraph, TextRun } = window.docx;
    const lines = String(text || "").replace(/<br\s*\/?>/gi, "\n").split("\n").map(line => line.trim());
    const usable = lines.length ? lines : [""];
    return usable.map(line => {
      // TextRun không hỗ trợ đổi trực tiếp thuộc tính sau khi tạo; tạo riêng cho ô tiêu đề
      // để giữ đúng kiểu đậm của hàng đầu trong demo.docx.
      const runs = isHeader
        ? [new TextRun({ text: line || " ", font: this.fontFamily, size: this.fontSizeBody, bold: true })]
        : this.parseInlineTextToRuns(line || " ");
      return new Paragraph({
        spacing: { before: 40, after: 40, line: 240 },
        children: runs.length ? runs : [new TextRun({ text: line || "", font: this.fontFamily, size: this.fontSizeBody, bold: isHeader })]
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
      spacing: { before: 0, after: this.spaceAfter, line: this.lineSpacing },
      children: [
        new TextRun({ text: `TRƯỜNG: ${schoolName}`, font: this.fontFamily, size: this.fontSizeBody })
      ]
    }));
    headers.push(new Paragraph({
      alignment: AlignmentType.LEFT,
      spacing: { before: 0, after: this.spaceAfter, line: this.lineSpacing },
      children: [
        new TextRun({ text: `TỔ CHUYÊN MÔN: ${groupName}`, font: this.fontFamily, size: this.fontSizeBody })
      ]
    }));
    headers.push(new Paragraph({
      alignment: AlignmentType.LEFT,
      spacing: { before: 0, after: this.spaceAfter, line: this.lineSpacing },
      children: [
        new TextRun({ text: `HỌ VÀ TÊN GIÁO VIÊN: ${teacherName}`, font: this.fontFamily, size: this.fontSizeBody })
      ]
    }));
    headers.push(new Paragraph({
      alignment: AlignmentType.LEFT,
      spacing: { before: 0, after: this.spaceAfter, line: this.lineSpacing },
      children: [
        new TextRun({ text: `Ngày soạn: ${dateDraft}`, font: this.fontFamily, size: this.fontSizeBody })
      ]
    }));
    headers.push(new Paragraph({
      alignment: AlignmentType.LEFT,
      spacing: { before: 0, after: this.spaceAfter, line: this.lineSpacing },
      children: [
        new TextRun({ text: `Ngày dạy: ${dateTeach}`, font: this.fontFamily, size: this.fontSizeBody })
      ]
    }));

    headers.push(new Paragraph({
      alignment: AlignmentType.LEFT,
      spacing: { before: 0, after: this.spaceAfter, line: this.lineSpacing },
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
      spacing: { before: 0, after: this.spaceAfter, line: this.lineSpacing },
      children: [new TextRun({ text: `TÊN BÀI SOẠN: ${topic}`, font: this.fontFamily, size: this.fontSizeBody, bold: true })]
    }));
    headers.push(new Paragraph({
      alignment: AlignmentType.LEFT,
      spacing: { before: 0, after: this.spaceAfter, line: this.lineSpacing },
      children: [new TextRun({ text: `MÔN HỌC: ${subject} - LỚP: ${grade}`, font: this.fontFamily, size: this.fontSizeBody, bold: true })]
    }));
    headers.push(new Paragraph({
      alignment: AlignmentType.LEFT,
      spacing: { before: 0, after: this.spaceAfter, line: this.lineSpacing },
      children: [new TextRun({ text: `THỜI LƯỢNG THỰC HIỆN: ${duration}`, font: this.fontFamily, size: this.fontSizeBody, bold: true })]
    }));

    return headers;
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
