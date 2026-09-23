const fs = require('fs');
const path = require('path');

function loadDocx() {
  try { return require('docx'); } catch (e) {
    const runtimeModule = path.join(process.env.USERPROFILE || '', '.cache', 'codex-runtimes', 'codex-primary-runtime', 'dependencies', 'node', 'node_modules', 'docx');
    if (fs.existsSync(runtimeModule)) return require(runtimeModule);
    throw e;
  }
}

const docx = loadDocx();
const { Document, Packer, Paragraph, TextRun, ImageRun, AlignmentType, Footer, Table, TableRow, TableCell, WidthType, BorderStyle, TableLayoutType, VerticalAlign } = docx;

// Helper: load PNG as base64 Data URL
function getImgDataUrl(imgPath) {
  const buf = fs.readFileSync(imgPath);
  return 'data:image/png;base64,' + buf.toString('base64');
}

// Danh mục hình vẽ cho tiết Luyện tập chung V2 (tinh gọn)
const illustrations = [
  {
    id: 'so-do-tu-duy',
    dataUrl: getImgDataUrl(path.join(__dirname, 'hinh_ve_sgk/so_do_tu_duy_hinh_binh_hanh.png')),
    width: 470,
    height: 257
  },
  {
    id: 'hinh-geogebra-ltc-bai12',
    dataUrl: getImgDataUrl(path.join(__dirname, 'hinh_ve_sgk/hinh_geogebra_ltc_bai12.png')),
    width: 440,
    height: 191
  },
  {
    id: 'hinh-3.39',
    dataUrl: getImgDataUrl(path.join(__dirname, 'hinh_ve_sgk/hinh_3_39.png')),
    width: 470,
    height: 150
  },
  {
    id: 'hinh-bai-3.20',
    dataUrl: getImgDataUrl(path.join(__dirname, 'hinh_ve_sgk/hinh_bai_3_20.png')),
    width: 370,
    height: 170
  },
  {
    id: 'hinh-bai-3.22',
    dataUrl: getImgDataUrl(path.join(__dirname, 'hinh_ve_sgk/hinh_bai_3_22.png')),
    width: 350,
    height: 168
  },
  {
    id: 'hinh-bai-3.24',
    dataUrl: getImgDataUrl(path.join(__dirname, 'hinh_ve_sgk/hinh_bai_3_24.png')),
    width: 380,
    height: 183
  }
];

// Setup global appState for DocxGenerator
global.appState = {
  content: {
    illustrations: illustrations
  },
  teachingContext: {
    lessonScope: 'Tiết 7'
  }
};
global.window = {
  docx: docx,
  appState: global.appState
};

// Require DocxGenerator
const { DocxGenerator } = require('../js/khbd-docx.js');
const generator = new DocxGenerator();

// Override createIllustrationParagraphs to use exact width/height without distortion
generator.createIllustrationParagraphs = function (altText, illustrationId) {
  const safeId = this.safeIllustrationId(illustrationId);
  const ill = illustrations.find(item => item && item.id === safeId);
  if (!ill || !ill.dataUrl) return [this.illustrationFallbackParagraph(altText)];

  const b64 = ill.dataUrl.split(',')[1];
  const bytes = Buffer.from(b64, 'base64');
  const w = ill.width || 380;
  const h = ill.height || 190;

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

// Chuẩn hóa phân vai GV/HS và ngắt dòng trong ô bảng
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
  content = content.replace(/(\*\*GV:\*\*.*?)([."”])\s+HS\s+(?!:)/g, "$1$2<br>- **HS:** ");
  content = content.replace(/(\*\*HS:\*\*.*?)([."”])\s+GV\s+(?!:)/g, "$1$2<br>- **GV:** ");
  content = content.replace(/^(\s*)(?:<br>)+/, "$1");
  if (isTable) content = content.replace(/(\|\s*)(?:<br>)+/g, "$1");
  return content;
}

function formatKhbdRoleLineBreaks(text) {
  return String(text || "").split("\n").map(formatKhbdRoleLine).join("\n");
}

global.window.formatKhbdRoleLineBreaks = formatKhbdRoleLineBreaks;

// QUY CHUẨN MỚI: BẢNG TRONG WORD THÌ ĐỀU CHO BÊN TRÁI, PHẢI ĐỀU 0PT NHÌN CHO DỄ
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

    // QUY CHUẨN: Lề trái và phải trong ô đều là 0pt
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

  // Tỷ lệ cân đối: Cột 1 = 5100 dxa (51.4%), Cột 2 = 4822 dxa (48.6%)
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
        // QUY CHUẨN: LỀ TRÁI, PHẢI ĐỀU 0PT
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

const mdPath = path.join(__dirname, 'KHBD_Toan8_LuyenTapChung_Trang62.md');
const markdownContent = fs.readFileSync(mdPath, 'utf8');

const lessonInfo = {
  school: 'TRƯỜNG THCS .....................................................',
  teacher: '.....................................................',
  chapter: 'Chương III: Tứ giác',
  topic: 'Bài 12: Hình bình hành (Tiết 7: Luyện tập chung)',
  lessonScope: 'Tiết 7 (Tuần 4)',
  duration: '01 tiết (45 phút)',
  subject: 'Toán',
  academicYear: '2026-2027'
};

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

if (typeof Footer === 'function') {
  section.footers = { default: new Footer({ children: footerElements }) };
}

const doc = new Document({
  creator: 'Trợ lý Soạn Kế hoạch Bài dạy AI',
  title: 'KHBD_Toan8_LuyenTapChung_Trang62',
  description: 'Kế hoạch bài dạy chuẩn Công văn 5512 - Tiết 7: Luyện tập chung (trang 62 - 63 SGK Toán 8) tinh gọn 3 hoạt động kèm sơ đồ tư duy',
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

Packer.toBuffer(doc).then(buffer => {
  let outputPath = path.join(__dirname, 'KHBD_Toan8_LuyenTapChung_Trang62.docx');
  try {
    fs.writeFileSync(outputPath, buffer);
  } catch (err) {
    if (err.code === 'EBUSY') {
      outputPath = path.join(__dirname, 'KHBD_Toan8_LuyenTapChung_Trang62_Moi.docx');
      fs.writeFileSync(outputPath, buffer);
      console.log('NOTICE: Original file locked by Word. Saved to:', outputPath);
    } else {
      throw err;
    }
  }
  let fileBaiHocPath = path.join(__dirname, 'FILE BAI HOC', 'KHBD_Toan8_LuyenTapChung_Trang62.docx');
  try {
    fs.writeFileSync(fileBaiHocPath, buffer);
  } catch (err) {
    if (err.code === 'EBUSY') {
      fileBaiHocPath = path.join(__dirname, 'FILE BAI HOC', 'KHBD_Toan8_LuyenTapChung_Trang62_Moi.docx');
      fs.writeFileSync(fileBaiHocPath, buffer);
    }
  }
  console.log('SUCCESS: Written to', outputPath, buffer.length, 'bytes');
}).catch(err => {
  console.error('ERROR in export_word:', err);
  process.exit(1);
});
