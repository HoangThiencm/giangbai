/**
 * Engine chuẩn hóa xuất Kế hoạch bài dạy (KHBD) sang Word (.docx)
 * Đảm bảo:
 * 1. Bảng 0pt lề trái/phải, không thụt đầu dòng (indent: 0pt, margin: 0pt).
 * 2. Đọc file Markdown trực tiếp bằng fs.readFileSync (chống lỗi gãy dòng do ký tự LaTeX \ne, \text, \rightarrow).
 * 3. Chèn hình ảnh độ nét cao với kích thước chuẩn, không méo hình.
 * 4. Tự động xử lý khóa file EBUSY khi người dùng đang mở Word.
 */

const fs = require('fs');
const path = require('path');

/**
 * Khôi phục lệnh LaTeX bị escape thành ký tự điều khiển, rồi chuẩn hoá chia hết.
 * `\v` -> VT làm `\vdots` thành `dots`; `\f` -> FF làm `\frac` thành `rac`.
 */
function sanitizeKhbdMathSource(text) {
  let source = String(text || "");
  // 0. Khắc phục thực thể HTML &nbsp; tránh lỗi lộ mã text thô trong Word
  source = source.replace(/&nbsp;/gi, " ");
  // 1. Khôi phục các ký tự điều khiển ASCII bị nuốt dấu gạch chéo
  source = source.replace(/\u0008egin/g, "\\begin");
  source = source.replace(/\u000bdots/g, "\\vdots");
  source = source.replace(/\u000crac/g, "\\frac");
  source = source.replace(/\u0009ext/g, "\\text");
  source = source.replace(/\u0009imes/g, "\\times");
  source = source.replace(/[\u0000-\u0008\u000b\u000c\u000e-\u001f]/g, "");

  // 2. Khôi phục các lệnh LaTeX bị rụng gạch chéo phổ biến
  source = source.replace(/\\phantom\s*\{[^{}]*\}/g, "");
  source = source.replace(/(?<!\\)\b(?:frac|rac)(?=\{)/g, "\\frac");
  source = source.replace(/(?<!\\)\bbegin(?=\{|\b)/g, "\\begin");
  source = source.replace(/(?<!\\)\bext(?=\{)/g, "\\text");
  source = source.replace(/(?<!\\)\bimes\b/g, "\\times");
  source = source.replace(/\\not\s*\\vdots/g, "\\nmid");
  source = source.replace(/\\not\s*\\mid/g, "\\nmid");
  source = source.replace(/\\\s+\\vdots\s+\\/g, "\\vdots");
  source = source.replace(/(?<=\d|[a-zA-Z])\s*(?:\\dots|\bdots\b)\s*(?=\d|[a-zA-Z])/g, " \\vdots ");
  source = source.replace(/(?<=\d|[a-zA-Z])\s*\\vdots\s*(?=\d|[a-zA-Z])/g, " \\vdots ");

  // 3. BẢN VÁ V2.2: Quy chuẩn Sư phạm THCS & Xử lý triệt để ký hiệu suy ra, tương đương
  source = source.replace(/\\implies\b/g, " \\Rightarrow ");
  source = source.replace(/implies(?=[A-Z\\góc])/g, " \\Rightarrow ");
  source = source.replace(/(?<=[a-zà-ỹ])implies/gi, " \\Rightarrow ");
  source = source.replace(/\bimplies\b/gi, " \\Rightarrow ");
  source = source.replace(/\\iff\b/g, "\\text{ hay }");
  source = source.replace(/\\(?:Leftrightarrow|leftrightarrow)\b/g, "\\text{ hay }");
  source = source.replace(/<=>/g, " hay ");
  source = source.replace(/⇔/g, " hay ");
  source = source.replace(/(?<![<=!])=>/g, " \\Rightarrow ");

  // Đảm bảo các ký hiệu toán/hình học luôn có khoảng cách an toàn, chống dính chữ
  source = source.replace(/\\Rightarrow(?=[^\s])/g, "\\Rightarrow ");
  source = source.replace(/(?<=[^\s])\\Rightarrow/g, " \\Rightarrow");
  source = source.replace(/\\perp(?=[^\s])/g, "\\perp ");
  source = source.replace(/(?<=[^\s])\\perp/g, " \\perp");
  source = source.replace(/\\parallel(?=[^\s])/g, "\\parallel ");
  source = source.replace(/(?<=[^\s])\\parallel/g, " \\parallel");
  source = source.replace(/\\triangle(?=[^\s])/g, "\\triangle ");
  source = source.replace(/(?<=[^\s])\\triangle/g, " \\triangle");

  // 4. BẢN VÁ PHÒNG VỆ: Quét sạch mã thẻ ảnh inline lọt vào câu văn (loại bỏ hoàn toàn đường dẫn/mã rác kỹ thuật)
  source = source.split('\n').map(line => {
    const trimmed = line.trim();
    // Dòng độc lập chứa thẻ ảnh hợp lệ thì giữ nguyên để engine chèn ảnh
    if (/^!\[[^\]]*\]\((?:khbd-ill:)?[^)]+\)$/.test(trimmed)) {
      return line;
    }
    // Dòng văn bản bình thường có dính `![Caption](id)` hoặc ![Caption](id) thì bóc tách lấy caption sạch
    return line
      .replace(/`!\[([^\]]*)\]\((?:khbd-ill:)?[^)]+\)`/g, '$1')
      .replace(/!\[([^\]]*)\]\((?:khbd-ill:)?[^)]+\)/g, '$1');
  }).join('\n');

  // 5. BẢN VÁ V2.1: BỎ HOÀN TOÀN KHỐI THÔNG TIN HÀNH CHÍNH LẶP LẠI TRƯỚC "I. MỤC TIÊU"
  const mucTieuIdx = source.search(/(?:^|\n)#+\s*I\.\s*MỤC TIÊU/i);
  if (mucTieuIdx !== -1) {
    source = source.slice(mucTieuIdx).replace(/^\n+/, "");
  }

  // 6. BẢN VÁ V2.1: BỎ SỐ TIẾT TRONG TIÊU ĐỀ HOẠT ĐỘNG (Ví dụ: "(Tiết 5: 30 phút)" -> "(30 phút)", "(Tiết 4)" -> "")
  source = source.replace(/\(\s*Tiết\s*[\d,\s-]+[:;\-–—]?\s*(\d+\s*phút)\s*\)/gi, "($1)");
  source = source.replace(/\s*\(\s*Tiết\s*[\d,\s-]+\s*\)/gi, "");

  return source;
}

function loadDocx() {
  try { return require('docx'); } catch (e) {
    const runtimeModule = path.join(process.env.USERPROFILE || '', '.cache', 'codex-runtimes', 'codex-primary-runtime', 'dependencies', 'node', 'node_modules', 'docx');
    if (fs.existsSync(runtimeModule)) return require(runtimeModule);
    throw e;
  }
}

const docx = loadDocx();
const { Document, Packer, Paragraph, TextRun, ImageRun, AlignmentType, Header, Footer, Table, TableRow, TableCell, WidthType, BorderStyle, TableLayoutType, VerticalAlign, PageNumber } = docx;

function resolveKhbdSubjectLine(lessonInfo = {}) {
  const norm = { ...lessonInfo };
  let subject = String(norm.subject || "").trim();
  let grade = String(norm.grade || "").trim();
  let branch = String(norm.branch || "").trim();

  // Gom chuỗi ngữ cảnh tổng hợp để nhận diện chính xác
  const searchCorpus = [
    norm.topic,
    norm.unitName,
    norm.subject,
    norm.branch,
    norm.filePath,
    norm.mdFile,
    norm.mdFilePath,
    norm.outFile,
    norm.outputDocxPath,
    norm.ppct
  ].filter(Boolean).join(" ");

  // Phát hiện khối lớp chuẩn xác theo pattern, tránh bắt nhầm số tiết (như Tiết 26, 28)
  if (!grade) {
    const gradeMatch = searchCorpus.match(/(?:Lớp|Toán|Tin\s*học|Khối|Toan|Tin)\s*([6789])/i)
      || searchCorpus.match(/[_\-\/\\](?:Toan|Tin)?([6789])[_\-\/\\]/i);
    if (gradeMatch) {
      grade = gradeMatch[1] || gradeMatch[2];
    } else if (/Toan6|Tin6/i.test(searchCorpus)) {
      grade = "6";
    } else if (/Toan9/i.test(searchCorpus)) {
      grade = "9";
    } else if (/Toan8/i.test(searchCorpus)) {
      grade = "8";
    } else {
      grade = "6";
    }
  }

  // Nếu là môn Tin học
  if (subject.toLowerCase().includes("tin") || /TIN\s*HỌC|TIN6|TIN\s*6/i.test(searchCorpus)) {
    return `Môn: Tin học ${grade || 6}`;
  }

  // Nhận diện phân môn Toán: Hình học hay Số học / Đại số
  const branchLower = branch.toLowerCase();
  const isGeometry = branchLower === "hinhhoc"
    || branchLower.includes("hinh")
    || branchLower.includes("hình")
    || /HÌNH\s*HỌC|HÌNH\s*PHẲNG|TAM\s*GIÁC|HÌNH\s*CHỮ\s*NHẬT|HÌNH\s*VUÔNG|CUNG|DÂY|ĐƯỜNG\s*TRÒN|HỆ\s*THỨC\s*LƯỢNG|LƯỢNG\s*GIÁC|ĐỘ\s*DÀI\s*CUNG/i.test(searchCorpus);

  if (grade === "6") {
    return isGeometry ? "Môn: Toán – Hình học 6" : "Môn: Toán – Số học 6";
  } else if (grade === "9") {
    return isGeometry ? "Môn: Toán – Hình học 9" : "Môn: Toán – Đại số 9";
  } else if (grade === "8") {
    return isGeometry ? "Môn: Toán – Hình học 8" : "Môn: Toán – Đại số 8";
  } else if (grade === "7") {
    return isGeometry ? "Môn: Toán – Hình học 7" : "Môn: Toán – Đại số 7";
  }

  return `Môn: Toán – ${grade}`;
}

function createKhbdPageHeader(generator, lessonInfo = {}) {
  const schoolName = String(lessonInfo.school || "Trường THCS Trần Phú").trim();
  const teacherName = String(lessonInfo.teacher || "Hoàng Tấn Thiên").trim();
  const font = generator.fontFamily || "Times New Roman";
  const tblWidth = generator.tableWidth || 9638;
  const colW = Math.round(tblWidth / 2);

  const borderBlue = { style: BorderStyle.SINGLE, size: 6, color: "5B9BD5" };
  const borderNone = { style: BorderStyle.NONE, size: 0, color: "auto" };

  return new Table({
    width: { size: tblWidth, type: WidthType.DXA },
    columnWidths: [colW, tblWidth - colW],
    borders: {
      top: borderNone,
      left: borderNone,
      right: borderNone,
      bottom: borderBlue,
      insideHorizontal: borderNone,
      insideVertical: borderNone
    },
    rows: [
      new TableRow({
        children: [
          new TableCell({
            width: { size: colW, type: WidthType.DXA },
            margins: { top: 0, bottom: 40, left: 0, right: 0 },
            children: [
              new Paragraph({
                spacing: { before: 0, after: 0, line: 240, lineRule: "auto" },
                children: [
                  new TextRun({ text: schoolName, font: font, size: 22 })
                ]
              })
            ]
          }),
          new TableCell({
            width: { size: tblWidth - colW, type: WidthType.DXA },
            margins: { top: 0, bottom: 40, left: 0, right: 0 },
            children: [
              new Paragraph({
                alignment: AlignmentType.RIGHT,
                spacing: { before: 0, after: 0, line: 240, lineRule: "auto" },
                children: [
                  new TextRun({ text: `Giáo viên: ${teacherName}`, font: font, size: 22 })
                ]
              })
            ]
          })
        ]
      })
    ]
  });
}

function createKhbdPageFooter(generator, lessonInfo = {}) {
  const font = generator.fontFamily || "Times New Roman";
  const tblWidth = generator.tableWidth || 9638;
  const col1 = Math.round(tblWidth * 0.40); // 40% cho Môn
  const col2 = Math.round(tblWidth * 0.25); // 25% cho Trang
  const col3 = tblWidth - col1 - col2;     // 35% cho Năm học

  const borderBlue = { style: BorderStyle.SINGLE, size: 6, color: "5B9BD5" };
  const borderNone = { style: BorderStyle.NONE, size: 0, color: "auto" };

  const subjectText = resolveKhbdSubjectLine(lessonInfo);
  const yearText = String(lessonInfo.academicYear || "Năm học: 2026-2027").trim();
  const yearDisplay = yearText.startsWith("Năm học:") ? yearText : `Năm học: ${yearText}`;

  return new Table({
    width: { size: tblWidth, type: WidthType.DXA },
    columnWidths: [col1, col2, col3],
    borders: {
      top: borderBlue,
      left: borderNone,
      right: borderNone,
      bottom: borderNone,
      insideHorizontal: borderNone,
      insideVertical: borderNone
    },
    rows: [
      new TableRow({
        children: [
          new TableCell({
            width: { size: col1, type: WidthType.DXA },
            margins: { top: 60, bottom: 0, left: 0, right: 0 },
            children: [
              new Paragraph({
                spacing: { before: 0, after: 0, line: 240, lineRule: "auto" },
                children: [
                  new TextRun({ text: subjectText, font: font, size: 22 })
                ]
              })
            ]
          }),
          new TableCell({
            width: { size: col2, type: WidthType.DXA },
            margins: { top: 60, bottom: 0, left: 0, right: 0 },
            children: [
              new Paragraph({
                alignment: AlignmentType.CENTER,
                spacing: { before: 0, after: 0, line: 240, lineRule: "auto" },
                children: [
                  new TextRun({ text: "- Trang ", font: font, size: 22 }),
                  new TextRun({ children: PageNumber?.CURRENT != null ? [PageNumber.CURRENT] : ["X"], font: font, size: 22 }),
                  new TextRun({ text: "-", font: font, size: 22 })
                ]
              })
            ]
          }),
          new TableCell({
            width: { size: col3, type: WidthType.DXA },
            margins: { top: 60, bottom: 0, left: 0, right: 0 },
            children: [
              new Paragraph({
                alignment: AlignmentType.RIGHT,
                spacing: { before: 0, after: 0, line: 240, lineRule: "auto" },
                children: [
                  new TextRun({ text: yearDisplay, font: font, size: 22 })
                ]
              })
            ]
          })
        ]
      })
    ]
  });
}

function formatKhbdRoleLine(line) {
  let content = String(line || "").replace(/<br\s*\/?>/gi, "<br>");
  const isTable = /^\s*\|/.test(content);
  content = content.replace(/(?:<br>\s*)?-\s*\*\*(GV|HS):\*\*/gi, (_, role) => `§BR§§${role.toUpperCase()}§`);
  if (!isTable) {
    content = content.replace(/\s*\|\s*(?:\*\*)?(GV|HS)\s*:(?:\*\*)?/gi, (_, role) => `§BR§§${role.toUpperCase()}§`);
  }
  content = content.replace(/(?<!(?:nhận\s*xét|đánh\s*giá|ý\s*kiến|chữ\s*ký)?\s*của\s+)(?:\*\*)?(GV|HS)\s*:(?:\*\*)?/gi, (_, role) => `§BR§§${role.toUpperCase()}§`);
  content = content.replace(/§BR§/g, "<br>- ");
  content = content.replace(/§GV§/g, "**GV:**");
  content = content.replace(/§HS§/g, "**HS:**");
  content = content.replace(/(\*\*GV:\*\*(?:(?!<br>|\*\*\*|\*\*).)*?)([."”])\s+HS\s+(?!:)/g, "$1$2<br>- **HS:** ");
  content = content.replace(/(\*\*HS:\*\*(?:(?!<br>|\*\*\*|\*\*).)*?)([."”])\s+GV\s+(?!:)/g, "$1$2<br>- **GV:** ");
  content = content.replace(/^(\s*)(?:<br>)+/, "$1");
  if (isTable) content = content.replace(/(\|\s*)(?:<br>)+/g, "$1");
  return content;
}

function formatKhbdRoleLineBreaks(text) {
  return String(text || "").split("\n").map(formatKhbdRoleLine).join("\n");
}

function createKhbdDocx({ mdFilePath, outputDocxPath, lessonInfo, illustrations = [] }) {
  global.appState = {
    content: { illustrations: illustrations },
    teachingContext: { lessonScope: lessonInfo.lessonScope || '' }
  };
  global.window = {
    docx: docx,
    appState: global.appState,
    formatKhbdRoleLineBreaks: formatKhbdRoleLineBreaks
  };

  const khbdDocxPath = fs.existsSync(path.resolve(__dirname, '../../js/khbd-docx.js'))
    ? path.resolve(__dirname, '../../js/khbd-docx.js')
    : path.resolve(__dirname, '../js/khbd-docx.js');
  const { DocxGenerator } = require(khbdDocxPath);
  const generator = new DocxGenerator();

  // BẢN VÁ V2.1: Chuẩn hóa Header tài liệu theo đúng Ảnh 2 (cực kỳ tinh gọn)
  // Bỏ hoàn toàn bảng Trường/Giáo viên và khối thông tin hành chính trùng lặp.
  // Chỉ gồm đúng 2 dòng căn giữa:
  // Dòng 1: Tiết X, Y, Z - BÀI XX: TÊN BÀI DẠY (In hoa đậm, cỡ 13pt / size 26)
  // Dòng 2: Thời lượng thực hiện: XX tiết (YY phút) (In nghiêng, cỡ 13pt)
  generator.createDocumentHeader = function (info = {}) {
    const { Paragraph, TextRun, AlignmentType } = global.window.docx;
    const normInfo = { ...info };
    if (!normInfo.lessonScope && normInfo.ppct) {
      const m = normInfo.ppct.match(/Tiết\s*[\d,\s-]+/i);
      if (m) normInfo.lessonScope = m[0].trim();
    }
    let title = this.formatTietBaiHeading(normInfo)
      .replace(/\s*\(\s*\d+\s*tiết\s*\)\s*$/i, "")
      .replace(/^TIẾT\b/i, "Tiết")
      .trim();
    let durationText = this.formatDurationLine(normInfo.duration) || `Thời lượng thực hiện: ${normInfo.duration || "01 tiết (45 phút)"}`;

    return [
      new Paragraph({
        alignment: AlignmentType.CENTER,
        spacing: { before: 0, after: 60, line: this.lineSpacing, lineRule: this.lineRule },
        children: [
          new TextRun({
            text: title,
            font: this.fontFamily,
            size: 26,
            bold: true
          })
        ]
      }),
      new Paragraph({
        alignment: AlignmentType.CENTER,
        spacing: { before: 0, after: 140, line: this.lineSpacing, lineRule: this.lineRule },
        children: [
          new TextRun({
            text: durationText,
            font: this.fontFamily,
            size: this.fontSizeBody,
            italics: true
          })
        ]
      })
    ];
  };

  // Override createIllustrationParagraphs
  generator.createIllustrationParagraphs = function (altText, illustrationId) {
    const safeId = this.safeIllustrationId(illustrationId);
    const ill = illustrations.find(item => item && item.id === safeId);
    if (!ill || !ill.dataUrl) return [this.illustrationFallbackParagraph(altText)];

    const b64 = ill.dataUrl.split(',')[1];
    const bytes = Buffer.from(b64, 'base64');
    const w = ill.width || 400;
    const h = ill.height || 200;

    return [
      new Paragraph({
        alignment: AlignmentType.CENTER,
        spacing: { before: 80, after: 80 },
        children: [
          new ImageRun({
            data: bytes,
            transformation: { width: w, height: h },
            type: 'png'
          })
        ]
      })
    ];
  };

  // QUY CHUẨN: Lề trái và phải trong ô đều là 0pt
  generator.parseTableCellParagraphs = function (text, isHeader = false) {
    const { Paragraph } = global.window.docx;
    let normalized = String(text || "");
    if (!isHeader) {
      normalized = formatKhbdRoleLineBreaks(normalized);
    }
    const lines = normalized.replace(/<br\s*\/?>/gi, "\n").split("\n").map(line => line.trim());
    const usable = lines.filter(l => l && !/^[-+*•.]\s*$/.test(l.trim()));
    if (!usable.length) {
      return [new Paragraph({ spacing: { before: 0, after: 20, line: this.lineSpacing, lineRule: this.lineRule }, children: [this.coloredTextRun(" ")] })];
    }

    return usable.flatMap(line => {
      const illParts = this.splitIllustrationSegments(line);
      if (illParts.some(part => part.type === "illustration")) {
        return illParts.flatMap(part => {
          if (part.type === "illustration") {
            const block = this.createIllustrationParagraphs(part.caption, part.id);
            return block.length ? block : [this.illustrationFallbackParagraph(part.caption)];
          }
          const content = String(part.text || "").trim();
          if (!content || /^[-+*•.]\s*$/.test(content)) return [];
          const runs = isHeader
            ? [this.coloredTextRun(content, { bold: true })]
            : this.parseInlineTextToRuns(content, this.lineIntegrationColor(content, null));
          return [new Paragraph({
            spacing: { before: 0, after: 20, line: this.lineSpacing, lineRule: this.lineRule },
            children: runs.length ? runs : [this.coloredTextRun(content, { bold: isHeader })]
          })];
        });
      }

      const roleMatch = !isHeader ? line.match(/^(-\s*)?(?:\*\*)?(GV|HS)\s*:(?:\*\*)?\s*(.*)$/i) : null;
      const listMatch = !isHeader && !roleMatch ? line.match(/^([-+.•])\s+(.+)$/) : null;
      const marker = listMatch ? listMatch[1] : (roleMatch ? "-" : "");
      const contentText = roleMatch
        ? `**${roleMatch[2].toUpperCase()}:** ${roleMatch[3] || ""}`.trim()
        : (listMatch ? listMatch[2] : line);
      const displayLine = roleMatch
        ? `- ${contentText}`
        : (listMatch ? `${marker} ${contentText}` : (line || " "));

      const lineColor = isHeader ? undefined : this.lineIntegrationColor(displayLine, null);
      const runs = isHeader
        ? [this.coloredTextRun(line || " ", { bold: true })]
        : this.parseInlineTextToRuns(displayLine, lineColor);

      return [new Paragraph({
        indent: { left: 0, right: 0 },
        spacing: { before: 0, after: 25, line: 240, lineRule: "auto" },
        children: runs.length ? runs : [this.coloredTextRun(displayLine || "", { bold: isHeader, color: lineColor })]
      })];
    });
  };

  generator.parseMarkdownTable = function (lines) {
    const validLines = lines.filter(line => line.trim().startsWith("|") && line.trim().endsWith("|"));
    if (validLines.length === 0) return null;

    const rows = [];
    const tableWidth = this.tableWidth || 9922;
    const headerCells = this.splitMarkdownTableRow(validLines[0]).map(cell => cell.toLowerCase());
    const isActivityTwoCol = headerCells.some(cell => cell.includes("hoạt động của gv"))
      && headerCells.some(cell => cell.includes("nội dung"));
    const columnCount = isActivityTwoCol ? 2 : Math.max(...validLines.map(line => this.splitMarkdownTableRow(line).length));

    const columnWidths = isActivityTwoCol
      ? [5100, 4822]
      : Array.from({ length: columnCount }, (_, idx) => {
          const base = Math.floor(tableWidth / columnCount);
          return idx === columnCount - 1 ? (tableWidth - base * (columnCount - 1)) : base;
        });

    validLines.forEach((line, rowIndex) => {
      const parsedCells = this.splitMarkdownTableRow(line);
      const splitter = typeof semanticSplitActivityRow === "function"
        ? semanticSplitActivityRow
        : (cells => this.semanticSplitActivityRow(cells));
      const rawCells = isActivityTwoCol ? splitter(parsedCells) : parsedCells;
      const isHeader = (rowIndex === 0);

      const tableCells = Array.from({ length: columnCount }, (_, columnIndex) => {
        const cellText = rawCells[columnIndex] || "";
        const paragraphs = this.parseTableCellParagraphs(cellText, isHeader);
        return new TableCell({
          children: paragraphs.length ? paragraphs : [new Paragraph({ children: [new TextRun({ text: "", font: this.fontFamily, size: this.fontSizeBody })] })],
          margins: { top: 60, bottom: 60, left: 0, right: 0 },
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
      size: 4,
      color: "333333"
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
  };

  let markdownContent = sanitizeKhbdMathSource(fs.readFileSync(mdFilePath, 'utf8'));
  const headerElements = generator.createDocumentHeader(lessonInfo);
  const footerElements = generator.createDocumentFooter(lessonInfo);
  const bodyElements = generator.parseMarkdownToDocxElements(markdownContent);

  const section = {
    properties: {
      page: {
        size: generator.pageSize,
        margin: generator.pageMargins
      }
    },
    children: [...headerElements, ...bodyElements]
  };

  const fullLessonInfo = { mdFilePath, outputDocxPath, ...lessonInfo };
  if (typeof Header === 'function') {
    section.headers = { default: new Header({ children: [createKhbdPageHeader(generator, fullLessonInfo)] }) };
  }
  if (typeof Footer === 'function') {
    section.footers = { default: new Footer({ children: [createKhbdPageFooter(generator, fullLessonInfo)] }) };
  }

  const doc = new Document({
    creator: 'Trợ lý Soạn Kế hoạch Bài dạy AI',
    title: lessonInfo.topic || 'Kế hoạch bài dạy',
    styles: {
      default: {
        document: {
          run: { font: generator.fontFamily, size: generator.fontSizeBody },
          paragraph: {
            spacing: { before: 0, after: 30, line: 240, lineRule: "auto" },
            alignment: AlignmentType?.JUSTIFIED
          }
        }
      }
    },
    sections: [section]
  });

  return Packer.toBuffer(doc).then(buffer => {
    let finalPath = outputDocxPath;
    try {
      fs.writeFileSync(finalPath, buffer);
    } catch (err) {
      if (err.code === 'EBUSY') {
        const ext = path.extname(finalPath);
        finalPath = finalPath.replace(ext, `_Moi${ext}`);
        fs.writeFileSync(finalPath, buffer);
        console.warn(`CẢNH BÁO: File Word đang mở nên không ghi đè được. Đã ghi sang ${finalPath}. Hãy đóng Word rồi xuất lại.`);
      } else {
        throw err;
      }
    }

    // Sao lưu vào FILE BAI HOC nếu có
    const fileBaiHocDir = path.join(path.dirname(finalPath), 'FILE BAI HOC');
    if (fs.existsSync(fileBaiHocDir)) {
      const backupPath = path.join(fileBaiHocDir, path.basename(finalPath));
      try {
        fs.writeFileSync(backupPath, buffer);
      } catch (e) {}
    }

    return { success: true, path: finalPath, size: buffer.length };
  });
}


function createMergedKhbdDocx({ lessons = [], outputDocxPath, docTitle }) {
  const sections = [];

  for (const item of lessons) {
    global.appState = {
      content: { illustrations: item.illustrations || [] },
      teachingContext: { lessonScope: item.lessonInfo?.lessonScope || '' }
    };
    global.window = {
      docx: docx,
      appState: global.appState,
      formatKhbdRoleLineBreaks: formatKhbdRoleLineBreaks
    };

    const khbdDocxPath = fs.existsSync(path.resolve(__dirname, '../../js/khbd-docx.js'))
      ? path.resolve(__dirname, '../../js/khbd-docx.js')
      : path.resolve(__dirname, '../js/khbd-docx.js');
    const { DocxGenerator } = require(khbdDocxPath);
    const generator = new DocxGenerator();

    generator.createDocumentHeader = function (info = {}) {
      const { Paragraph, TextRun, AlignmentType } = global.window.docx;
      const normInfo = { ...info };
      if (!normInfo.lessonScope && normInfo.ppct) {
        const m = normInfo.ppct.match(/Tiết\s*[\d,\s-]+/i);
        if (m) normInfo.lessonScope = m[0].trim();
      }
      let title = this.formatTietBaiHeading(normInfo)
        .replace(/\s*\(\s*\d+\s*tiết\s*\)\s*$/i, "")
        .replace(/^TIẾT\b/i, "Tiết")
        .trim();
      let durationText = this.formatDurationLine(normInfo.duration) || `Thời lượng thực hiện: ${normInfo.duration || "01 tiết (45 phút)"}`;

      return [
        new Paragraph({
          alignment: AlignmentType.CENTER,
          spacing: { before: 0, after: 60, line: this.lineSpacing, lineRule: this.lineRule },
          children: [
            new TextRun({
              text: title,
              font: this.fontFamily,
              size: 26,
              bold: true
            })
          ]
        }),
        new Paragraph({
          alignment: AlignmentType.CENTER,
          spacing: { before: 0, after: 140, line: this.lineSpacing, lineRule: this.lineRule },
          children: [
            new TextRun({
              text: durationText,
              font: this.fontFamily,
              size: this.fontSizeBody,
              italics: true
            })
          ]
        })
      ];
    };

    generator.createIllustrationParagraphs = function (altText, illustrationId) {
      const safeId = this.safeIllustrationId(illustrationId);
      const ill = (item.illustrations || []).find(it => it && it.id === safeId);
      if (!ill || !ill.dataUrl) return [this.illustrationFallbackParagraph(altText)];

      const b64 = ill.dataUrl.split(',')[1];
      const bytes = Buffer.from(b64, 'base64');
      const w = ill.width || 400;
      const h = ill.height || 200;

      return [
        new Paragraph({
          alignment: AlignmentType.CENTER,
          spacing: { before: 80, after: 80 },
          children: [
            new ImageRun({
              data: bytes,
              transformation: { width: w, height: h },
              type: 'png'
            })
          ]
        })
      ];
    };

    generator.parseTableCellParagraphs = function (text, isHeader = false) {
      const { Paragraph } = global.window.docx;
      let normalized = String(text || "");
      if (!isHeader) {
        normalized = formatKhbdRoleLineBreaks(normalized);
      }
      const lines = normalized.replace(/<br\s*\/?>/gi, "\n").split("\n").map(line => line.trim());
      const usable = lines.filter(l => l && !/^[-+*•.]\s*$/.test(l.trim()));
      if (!usable.length) {
        return [new Paragraph({ spacing: { before: 0, after: 20, line: this.lineSpacing, lineRule: this.lineRule }, children: [this.coloredTextRun(" ")] })];
      }

      return usable.flatMap(line => {
        const illParts = this.splitIllustrationSegments(line);
        if (illParts.some(part => part.type === "illustration")) {
          return illParts.flatMap(part => {
            if (part.type === "illustration") {
              const block = this.createIllustrationParagraphs(part.caption, part.id);
              return block.length ? block : [this.illustrationFallbackParagraph(part.caption)];
            }
            const content = String(part.text || "").trim();
            if (!content || /^[-+*•.]\s*$/.test(content)) return [];
            const runs = isHeader
              ? [this.coloredTextRun(content, { bold: true })]
              : this.parseInlineTextToRuns(content, this.lineIntegrationColor(content, null));
            return [new Paragraph({
              spacing: { before: 0, after: 20, line: this.lineSpacing, lineRule: this.lineRule },
              children: runs.length ? runs : [this.coloredTextRun(content, { bold: isHeader })]
            })];
          });
        }

        const roleMatch = !isHeader ? line.match(/^(-\s*)?(?:\*\*)?(GV|HS)\s*:(?:\*\*)?\s*(.*)$/i) : null;
        const listMatch = !isHeader && !roleMatch ? line.match(/^([-+.•])\s+(.+)$/) : null;
        const marker = listMatch ? listMatch[1] : (roleMatch ? "-" : "");
        const contentText = roleMatch
          ? `**${roleMatch[2].toUpperCase()}:** ${roleMatch[3] || ""}`.trim()
          : (listMatch ? listMatch[2] : line);
        const displayLine = roleMatch
          ? `- ${contentText}`
          : (listMatch ? `${marker} ${contentText}` : (line || " "));

        const lineColor = isHeader ? undefined : this.lineIntegrationColor(displayLine, null);
        const runs = isHeader
          ? [this.coloredTextRun(line || " ", { bold: true })]
          : this.parseInlineTextToRuns(displayLine, lineColor);

        return [new Paragraph({
          indent: { left: 0, right: 0 },
          spacing: { before: 0, after: 25, line: 240, lineRule: "auto" },
          children: runs.length ? runs : [this.coloredTextRun(displayLine || "", { bold: isHeader, color: lineColor })]
        })];
      });
    };

    generator.parseMarkdownTable = function (lines) {
      const validLines = lines.filter(line => line.trim().startsWith("|") && line.trim().endsWith("|"));
      if (validLines.length === 0) return null;

      const rows = [];
      const tableWidth = this.tableWidth || 9922;
      const headerCells = this.splitMarkdownTableRow(validLines[0]).map(cell => cell.toLowerCase());
      const isActivityTwoCol = headerCells.some(cell => cell.includes("hoạt động của gv"))
        && headerCells.some(cell => cell.includes("nội dung"));
      const columnCount = isActivityTwoCol ? 2 : Math.max(...validLines.map(line => this.splitMarkdownTableRow(line).length));

      const columnWidths = isActivityTwoCol
        ? [5100, 4822]
        : Array.from({ length: columnCount }, (_, idx) => {
            const base = Math.floor(tableWidth / columnCount);
            return idx === columnCount - 1 ? (tableWidth - base * (columnCount - 1)) : base;
          });

      validLines.forEach((line, rowIndex) => {
        const parsedCells = this.splitMarkdownTableRow(line);
        const splitter = typeof semanticSplitActivityRow === "function"
          ? semanticSplitActivityRow
          : (cells => this.semanticSplitActivityRow(cells));
        const rawCells = isActivityTwoCol ? splitter(parsedCells) : parsedCells;
        const isHeader = (rowIndex === 0);

        const tableCells = Array.from({ length: columnCount }, (_, columnIndex) => {
          const cellText = rawCells[columnIndex] || "";
          const paragraphs = this.parseTableCellParagraphs(cellText, isHeader);
          return new TableCell({
            children: paragraphs.length ? paragraphs : [new Paragraph({ children: [new TextRun({ text: "", font: this.fontFamily, size: this.fontSizeBody })] })],
            margins: { top: 60, bottom: 60, left: 0, right: 0 },
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
        size: 4,
        color: "333333"
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
    };

    let markdownContent = sanitizeKhbdMathSource(fs.readFileSync(item.mdFilePath, 'utf8'));
    const headerElements = generator.createDocumentHeader(item.lessonInfo);
    const footerElements = generator.createDocumentFooter(item.lessonInfo);
    const bodyElements = generator.parseMarkdownToDocxElements(markdownContent);

    const section = {
      properties: {
        page: {
          size: generator.pageSize,
          margin: generator.pageMargins
        }
      },
      children: [...headerElements, ...bodyElements]
    };

    const fullLessonInfo = {
      outputDocxPath,
      mdFilePath: item.mdFilePath,
      mdFile: item.mdFile,
      outFile: item.outFile,
      branch: item.branch,
      grade: item.grade,
      subject: item.subject,
      ...(item.lessonInfo || {})
    };

    if (typeof Header === 'function') {
      section.headers = { default: new Header({ children: [createKhbdPageHeader(generator, fullLessonInfo)] }) };
    }
    if (typeof Footer === 'function') {
      section.footers = { default: new Footer({ children: [createKhbdPageFooter(generator, fullLessonInfo)] }) };
    }

    sections.push(section);
  }

  const doc = new Document({
    creator: 'Trợ lý Soạn Kế hoạch Bài dạy AI',
    title: docTitle || 'Kế hoạch bài dạy ghép',
    styles: {
      default: {
        document: {
          run: { font: "Times New Roman", size: 26 },
          paragraph: {
            spacing: { before: 0, after: 30, line: 240, lineRule: "auto" },
            alignment: AlignmentType?.JUSTIFIED
          }
        }
      }
    },
    sections: sections
  });

  return Packer.toBuffer(doc).then(buffer => {
    let finalPath = outputDocxPath;
    try {
      fs.writeFileSync(finalPath, buffer);
    } catch (err) {
      if (err.code === 'EBUSY') {
        const ext = path.extname(finalPath);
        finalPath = finalPath.replace(ext, `_Moi${ext}`);
        fs.writeFileSync(finalPath, buffer);
        console.warn(`CẢNH BÁO: File Word đang mở nên không ghi đè được. Đã ghi sang ${finalPath}. Hãy đóng Word rồi xuất lại.`);
      } else {
        throw err;
      }
    }
    return { success: true, path: finalPath, size: buffer.length };
  });
}

module.exports = { createKhbdDocx, createMergedKhbdDocx, loadDocx, sanitizeKhbdMathSource };
