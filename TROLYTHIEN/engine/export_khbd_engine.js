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

function loadDocx() {
  try { return require('docx'); } catch (e) {
    const runtimeModule = path.join(process.env.USERPROFILE || '', '.cache', 'codex-runtimes', 'codex-primary-runtime', 'dependencies', 'node', 'node_modules', 'docx');
    if (fs.existsSync(runtimeModule)) return require(runtimeModule);
    throw e;
  }
}

const docx = loadDocx();
const { Document, Packer, Paragraph, TextRun, ImageRun, AlignmentType, Footer, Table, TableRow, TableCell, WidthType, BorderStyle, TableLayoutType, VerticalAlign } = docx;

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

  const { DocxGenerator } = require('../js/khbd-docx.js');
  const generator = new DocxGenerator();

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

  const markdownContent = fs.readFileSync(mdFilePath, 'utf8');
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

module.exports = { createKhbdDocx, loadDocx };
