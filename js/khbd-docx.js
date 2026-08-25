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
    this.fontSizeBody = 26; // 13pt in half-points
    this.fontSizeH1 = 32;   // 16pt
    this.fontSizeH2 = 28;   // 14pt
    this.fontSizeH3 = 26;   // 13pt bold
    this.lineSpacing = 288; // 1.2 line spacing (240 is single, 288 is 1.2)
    this.spaceAfter = 100;  // 5pt
    this.spaceBefore = 60;  // 3pt

    // Chuẩn lề trang A4 Việt Nam (đơn vị dxa: 1cm = 567 dxa)
    this.pageMargins = {
      top: 1134,    // 2.0 cm
      bottom: 1134, // 2.0 cm
      left: 1701,   // 3.0 cm (lề trái đóng gáy)
      right: 1134   // 2.0 cm
    };
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
   * Tách một dòng văn bản chứa các công thức $...$ thành danh sách các docx TextRun
   */
  parseInlineTextToRuns(text) {
    if (!window.docx) return [];
    const { TextRun } = window.docx;

    const runs = [];
    // Regex tìm các khối $...$ hoặc **in đậm** hoặc *in nghiêng*
    const regex = /(\$\$[\s\S]*?\$\$|\$.*?\$|\*\*.*?\*\*|\*.*?\*|`.*?`)/g;
    let lastIndex = 0;
    let match;

    while ((match = regex.exec(text)) !== null) {
      // Phần văn bản thường trước match
      if (match.index > lastIndex) {
        const plain = text.substring(lastIndex, match.index);
        runs.push(new TextRun({
          text: plain,
          font: this.fontFamily,
          size: this.fontSizeBody
        }));
      }

      const token = match[0];

      if (token.startsWith("$$") && token.endsWith("$$")) {
        // Công thức khối
        const mathClean = this.latexToUnicodeMath(token);
        runs.push(new TextRun({
          text: ` ${mathClean} `,
          font: "Cambria Math",
          italics: true,
          bold: true,
          size: this.fontSizeBody,
          color: "003366"
        }));
      } else if (token.startsWith("$") && token.endsWith("$")) {
        // Công thức inline
        const mathClean = this.latexToUnicodeMath(token);
        runs.push(new TextRun({
          text: mathClean,
          font: "Cambria Math",
          italics: true,
          size: this.fontSizeBody,
          color: "002244"
        }));
      } else if (token.startsWith("**") && token.endsWith("**")) {
        // Chữ in đậm
        const boldText = token.substring(2, token.length - 2);
        // Có thể chứa math bên trong bold
        if (boldText.includes("$")) {
          const subRuns = this.parseInlineTextToRuns(boldText);
          subRuns.forEach(r => r.bold = true);
          runs.push(...subRuns);
        } else {
          runs.push(new TextRun({
            text: boldText,
            font: this.fontFamily,
            size: this.fontSizeBody,
            bold: true
          }));
        }
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
          font: "Consolas",
          size: this.fontSizeBody - 2,
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
      AlignmentType, HeadingLevel, BorderStyle, ShadingType
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
          heading: HeadingLevel.HEADING_1,
          alignment: AlignmentType.LEFT,
          spacing: { before: 200, after: 120, line: this.lineSpacing },
          children: [
            new TextRun({
              text: trimmed.substring(2).trim(),
              font: this.fontFamily,
              size: this.fontSizeH1,
              bold: true,
              color: "002B49"
            })
          ]
        }));
        i++;
        continue;
      }

      if (trimmed.startsWith("## ")) {
        elements.push(new Paragraph({
          heading: HeadingLevel.HEADING_2,
          alignment: AlignmentType.LEFT,
          spacing: { before: 160, after: 80, line: this.lineSpacing },
          children: [
            new TextRun({
              text: trimmed.substring(3).trim(),
              font: this.fontFamily,
              size: this.fontSizeH2,
              bold: true,
              color: "0A4D68"
            })
          ]
        }));
        i++;
        continue;
      }

      if (trimmed.startsWith("### ")) {
        elements.push(new Paragraph({
          heading: HeadingLevel.HEADING_3,
          spacing: { before: 120, after: 60, line: this.lineSpacing },
          children: [
            new TextRun({
              text: trimmed.substring(4).trim(),
              font: this.fontFamily,
              size: this.fontSizeH3,
              bold: true,
              color: "088395"
            })
          ]
        }));
        i++;
        continue;
      }

      if (trimmed.startsWith("#### ")) {
        elements.push(new Paragraph({
          spacing: { before: 100, after: 40, line: this.lineSpacing },
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

      // 4. Phân tích DANH SÁCH ĐẦU DÒNG (- hoặc * hoặc +)
      if (/^[-*+]\s+/.test(trimmed)) {
        const bulletText = trimmed.replace(/^[-*+]\s+/, "");
        const runs = this.parseInlineTextToRuns(bulletText);
        elements.push(new Paragraph({
          bullet: { level: 0 },
          spacing: { before: 40, after: 40, line: this.lineSpacing },
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
          spacing: { before: 40, after: 40, line: this.lineSpacing },
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
          spacing: { before: 80, after: 80, line: this.lineSpacing },
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
        alignment: AlignmentType.BOTH, // Căn đều 2 bên chuẩn hành chính
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
    const { Table, TableRow, TableCell, Paragraph, TextRun, WidthType, BorderStyle } = window.docx;

    // Lọc bỏ dòng phân cách (|:---|:---:|)
    const validLines = tableLines.filter(line => !/^[|\s-:]+$/.test(line));
    if (validLines.length === 0) return null;

    const rows = [];

    validLines.forEach((line, rowIndex) => {
      // Tách các ô giữa các dấu |
      const rawCells = line.split("|").slice(1, -1);
      const isHeader = (rowIndex === 0);

      const tableCells = rawCells.map(cellText => {
        const textClean = cellText.trim();
        const runs = this.parseInlineTextToRuns(textClean);

        if (isHeader) {
          runs.forEach(r => r.bold = true);
        }

        return new TableCell({
          children: [
            new Paragraph({
              spacing: { before: 80, after: 80, line: 240 },
              children: runs
            })
          ],
          shading: isHeader ? { fill: "E8EEF5" } : undefined,
          margins: { top: 120, bottom: 120, left: 160, right: 160 }
        });
      });

      rows.push(new TableRow({
        children: tableCells,
        tableHeader: isHeader
      }));
    });

    const borderStyle = {
      style: BorderStyle.SINGLE,
      size: 4,
      color: "888888"
    };

    return new Table({
      rows: rows,
      width: { size: 100, type: WidthType.PERCENTAGE },
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

  /**
   * Tạo phần Header trang trọng cho Giáo án chuẩn (Tên trường, Tổ, Tên bài, Ngày soạn...)
   */
  createDocumentHeader(lessonInfo = {}) {
    if (!window.docx) return [];
    const { Paragraph, TextRun, AlignmentType, BorderStyle } = window.docx;

    const schoolName = lessonInfo.school || "TRƯỜNG THCS ....................................................";
    const groupName = lessonInfo.subjectGroup || "TỔ: TOÁN - TIN HỌC";
    const teacherName = lessonInfo.teacher || "Họ và tên giáo viên: ................................................";
    const subject = (lessonInfo.subject || "TOÁN THCS").toUpperCase();
    const topic = (lessonInfo.topic || "KẾ HOẠCH BÀI DẠY").toUpperCase();
    const grade = lessonInfo.grade ? `LỚP ${lessonInfo.grade}` : "";
    const duration = lessonInfo.duration || "Thời lượng: 02 tiết";
    const bookName = lessonInfo.bookName ? `Bộ sách: ${lessonInfo.bookName}` : "";

    const headers = [];

    // Tiêu ngữ trường & tổ
    headers.push(new Paragraph({
      alignment: AlignmentType.LEFT,
      spacing: { before: 0, after: 40 },
      children: [
        new TextRun({ text: schoolName, font: this.fontFamily, size: this.fontSizeBody, bold: true }),
        new TextRun({ text: `\t\t${groupName}`, font: this.fontFamily, size: this.fontSizeBody, bold: true })
      ]
    }));

    headers.push(new Paragraph({
      alignment: AlignmentType.LEFT,
      spacing: { before: 0, after: 120 },
      children: [
        new TextRun({ text: teacherName, font: this.fontFamily, size: this.fontSizeBody, italics: true })
      ]
    }));

    // TÊN BÀI GIÁO ÁN TO ĐẬM Ở GIỮA
    headers.push(new Paragraph({
      alignment: AlignmentType.CENTER,
      spacing: { before: 160, after: 60 },
      children: [
        new TextRun({
          text: `KẾ HOẠCH BÀI DẠY: ${topic}`,
          font: this.fontFamily,
          size: this.fontSizeH1 + 2,
          bold: true,
          color: "002B49"
        })
      ]
    }));

    // Thông tin môn, lớp, thời lượng, bộ sách
    const subInfo = [subject, grade, duration, bookName].filter(x => x.length > 0).join("  |  ");
    headers.push(new Paragraph({
      alignment: AlignmentType.CENTER,
      spacing: { before: 0, after: 160 },
      children: [
        new TextRun({
          text: subInfo,
          font: this.fontFamily,
          size: this.fontSizeBody,
          italics: true,
          bold: true
        })
      ]
    }));

    // Đường kẻ phân cách
    headers.push(new Paragraph({
      spacing: { before: 60, after: 200 },
      border: {
        bottom: {
          color: "0A4D68",
          space: 2,
          style: BorderStyle.SINGLE,
          size: 12
        }
      }
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
      creator: "Trợ lý Soạn Kế hoạch Bài dạy AI (Môn Toán THCS)",
      title: tabTitle,
      description: `Xuất phần ${tabTitle} chuẩn Công văn 5512`,
      sections: [{
        properties: {
          page: {
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
  async exportFullLessonPlan(lessonInfo, fullMarkdownContent, fileName = "Giao_An_Toan_THCS.docx") {
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
      creator: "Trợ lý Soạn Kế hoạch Bài dạy AI (Môn Toán THCS)",
      title: `KHBD_${lessonInfo.topic || "Toan_THCS"}`,
      description: "Kế hoạch bài dạy môn Toán THCS chuẩn Công văn 5512",
      sections: [{
        properties: {
          page: {
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
