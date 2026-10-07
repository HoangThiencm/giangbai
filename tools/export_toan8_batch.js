// -*- coding: utf-8 -*-
/**
 * Export trọn bộ 9 Kế hoạch bài dạy (KHBD) Toán 8 (Đại số Chương I & Hình học Chương III) sang Word .docx
 * Sử dụng export_khbd_engine.js chuẩn Công văn 5512 V2.1
 * Xuất 9 file đơn lẻ + 2 file ghép nối (Đại số 1 file, Hình học 1 file)
 */
const fs = require('fs');
const path = require('path');
const { createKhbdDocx, loadDocx, sanitizeKhbdMathSource } = require('../TROLYTHIEN/engine/export_khbd_engine.js');

const KET_QUA_DIR = path.resolve(__dirname, '../TROLYTHIEN/1_SOAN_KHBD/Ket_qua');
const HINH_DIR = path.resolve(__dirname, '../TROLYTHIEN/engine/hinh_ve_sgk');

if (!fs.existsSync(KET_QUA_DIR)) {
  fs.mkdirSync(KET_QUA_DIR, { recursive: true });
}

function loadIll(id, caption, filename, width, height) {
  const p = path.join(HINH_DIR, filename);
  if (!fs.existsSync(p)) {
    console.error(`Không tìm thấy ảnh: ${p}`);
    return null;
  }
  const b64 = fs.readFileSync(p).toString('base64');
  return {
    id,
    caption,
    dataUrl: `data:image/png;base64,${b64}`,
    width,
    height
  };
}

const lessons = [
  {
    fileName: 'KHBD_01_Toan8_Bai05_PhepChiaDaThucChoDonThuc_Tiet9-10.docx',
    mdPath: path.resolve(__dirname, 'khbd_toan8_builder/BAI_01.md'),
    info: {
      subject: 'Toán',
      grade: '8',
      lessonScope: 'Tiết 9, 10',
      topic: 'BÀI 5: PHÉP CHIA ĐA THỨC CHO ĐƠN THỨC',
      ppct: 'Tiết 9, 10 — Tuần 5',
      duration: '02 tiết (90 phút)'
    },
    illustrations: [
      loadIll('hinh_01_khoi_hop_chu_nhat', 'Mô hình hai khối hộp chữ nhật', 'hinh_01_khoi_hop_chu_nhat.png', 420, 225)
    ].filter(Boolean)
  },
  {
    fileName: 'KHBD_02_Toan8_LuyenTapChung_Tiet11.docx',
    mdPath: path.resolve(__dirname, 'khbd_toan8_builder/BAI_02.md'),
    info: {
      subject: 'Toán',
      grade: '8',
      lessonScope: 'Tiết 11',
      topic: 'LUYỆN TẬP CHUNG',
      ppct: 'Tiết 11 — Tuần 6',
      duration: '01 tiết (45 phút)'
    },
    illustrations: [
      loadIll('mindmap_toan8_chuong1_luyentap', 'Sơ đồ tư duy Phép nhân và phép chia đa thức cho đơn thức', 'mindmap_toan8_chuong1_luyentap.png', 520, 265)
    ].filter(Boolean)
  },
  {
    fileName: 'KHBD_03_Toan8_BaiTapCuoiChuong1_Tiet12-13.docx',
    mdPath: path.resolve(__dirname, 'khbd_toan8_builder/BAI_03.md'),
    info: {
      subject: 'Toán',
      grade: '8',
      lessonScope: 'Tiết 12, 13',
      topic: 'BÀI TẬP CUỐI CHƯƠNG I',
      ppct: 'Tiết 12, 13 — Tuần 6, 7',
      duration: '02 tiết (90 phút)'
    },
    illustrations: [
      loadIll('mindmap_toan8_chuong1_tonghop', 'Sơ đồ tư duy Tổng hợp Chương I: Đa thức nhiều biến', 'mindmap_toan8_chuong1_tonghop.png', 520, 265),
      loadIll('hinh_sgk_1_3_gap_hop', 'Hình 1.3. Mô hình gấp hộp chữ nhật không nắp', 'hinh_sgk_1_3_gap_hop.png', 480, 205)
    ].filter(Boolean)
  },
  {
    fileName: 'KHBD_04_Toan8_HDTN_CongThucLaiKep_Tiet14.docx',
    mdPath: path.resolve(__dirname, 'khbd_toan8_builder/BAI_04.md'),
    info: {
      subject: 'Toán',
      grade: '8',
      lessonScope: 'Tiết 14',
      topic: 'HOẠT ĐỘNG THỰC HÀNH TRẢI NGHIỆM: CÔNG THỨC LÃI KÉP',
      ppct: 'Tiết 14 — Tuần 7',
      duration: '01 tiết (45 phút)'
    },
    illustrations: [
      loadIll('hinh_hdtn_cong_thuc_lai_kep', 'Mô hình Toán học & Bảng tính Excel: Công thức lãi kép', 'hinh_hdtn_cong_thuc_lai_kep.png', 520, 250)
    ].filter(Boolean)
  },
  {
    fileName: 'KHBD_05_Toan8_OnTapGiuaHK1_DaiSo_Tiet15-16.docx',
    mdPath: path.resolve(__dirname, 'khbd_toan8_builder/BAI_05.md'),
    info: {
      subject: 'Toán',
      grade: '8',
      lessonScope: 'Tiết 15, 16',
      topic: 'ÔN TẬP GIỮA HỌC KÌ I (ĐẠI SỐ)',
      ppct: 'Tiết 15, 16 — Tuần 8',
      duration: '02 tiết (90 phút)'
    },
    illustrations: [
      loadIll('mindmap_toan8_chuong1_ontap', 'Sơ đồ tư duy Ôn tập giữa HK1 Đại số', 'mindmap_toan8_chuong1_ontap.png', 520, 265)
    ].filter(Boolean)
  },
  {
    fileName: 'KHBD_06_Toan8_Bai14_HinhThoiVaHinhVuong_Tiet10-11.docx',
    mdPath: path.resolve(__dirname, 'khbd_toan8_builder/BAI_06.md'),
    info: {
      subject: 'Toán',
      grade: '8',
      lessonScope: 'Tiết 10, 11',
      topic: 'BÀI 14: HÌNH THOI VÀ HÌNH VUÔNG',
      ppct: 'Tiết 10, 11 — Tuần 5, 6',
      duration: '02 tiết (90 phút)'
    },
    illustrations: [
      loadIll('hinh_sgk_3_46_gap_giay', 'Thao tác gấp giấy cắt hình thoi và hình vuông', 'hinh_sgk_3_46_gap_giay.png', 450, 202),
      loadIll('hinh_sgk_3_47_hinh_thoi', 'Hình 3.47. Hình thoi ABCD', 'hinh_sgk_3_47_hinh_thoi.png', 320, 192),
      loadIll('hinh_sgk_3_48_duong_cheo_hinh_thoi', 'Hình 3.48. Hai đường chéo hình thoi', 'hinh_sgk_3_48_duong_cheo_hinh_thoi.png', 320, 224),
      loadIll('hinh_sgk_3_49_hai_duong_tron', 'Hình 3.49. Hai đường tròn cắt nhau tại B, D', 'hinh_sgk_3_49_hai_duong_tron.png', 360, 208),
      loadIll('hinh_sgk_3_50_nhan_biet_hinh_thoi', 'Hình 3.50. Tứ giác nhận biết hình thoi', 'hinh_sgk_3_50_nhan_biet_hinh_thoi.png', 500, 137),
      loadIll('hinh_sgk_3_51_luyen_tap_1', 'Hình 3.51. Luyện tập 1 nhận biết hình thoi', 'hinh_sgk_3_51_luyen_tap_1.png', 500, 152),
      loadIll('hinh_sgk_3_52_hinh_vuong', 'Hình 3.52. Hình vuông ABCD', 'hinh_sgk_3_52_hinh_vuong.png', 280, 227),
      loadIll('hinh_sgk_3_53_nhan_biet_hinh_vuong', 'Hình 3.53. Ví dụ 3 nhận biết hình vuông', 'hinh_sgk_3_53_nhan_biet_hinh_vuong.png', 420, 233),
      loadIll('hinh_sgk_3_54_luyen_tap_2', 'Hình 3.54. Luyện tập 2 nhận biết hình vuông', 'hinh_sgk_3_54_luyen_tap_2.png', 500, 173),
      loadIll('hinh_sgk_3_55_bai_3_29', 'Hình 3.55. Bài tập 3.29', 'hinh_sgk_3_55_bai_3_29.png', 480, 288),
      loadIll('hinh_sgk_3_56_bai_3_33', 'Hình 3.56. Bài tập 3.33', 'hinh_sgk_3_56_bai_3_33.png', 420, 240)
    ].filter(Boolean)
  },
  {
    fileName: 'KHBD_07_Toan8_LuyenTapChung_HinhHoc_Tiet12.docx',
    mdPath: path.resolve(__dirname, 'khbd_toan8_builder/BAI_07.md'),
    info: {
      subject: 'Toán',
      grade: '8',
      lessonScope: 'Tiết 12',
      topic: 'LUYỆN TẬP CHUNG',
      ppct: 'Tiết 12 — Tuần 6',
      duration: '01 tiết (45 phút)'
    },
    illustrations: [
      loadIll('mindmap_toan8_chuong3_tu_giac', 'Sơ đồ tư duy Mối quan hệ giữa các tứ giác đặc biệt', 'mindmap_toan8_chuong3_tu_giac.png', 520, 265),
      loadIll('hinh_sgk_3_57_vi_du', 'Hình 3.57. Ví dụ: Dựng hình vuông bằng hai đường tròn', 'hinh_sgk_3_57_vi_du.png', 320, 228),
      loadIll('hinh_sgk_3_58_bai_3_35', 'Hình 3.58. Bài tập 3.35: Hình bình hành ABCD và các phân giác', 'hinh_sgk_3_58_bai_3_35.png', 320, 201)
    ].filter(Boolean)
  },
  {
    fileName: 'KHBD_08_Toan8_BaiTapCuoiChuong3_Tiet13-14.docx',
    mdPath: path.resolve(__dirname, 'khbd_toan8_builder/BAI_08.md'),
    info: {
      subject: 'Toán',
      grade: '8',
      lessonScope: 'Tiết 13, 14',
      topic: 'BÀI TẬP CUỐI CHƯƠNG III',
      ppct: 'Tiết 13, 14 — Tuần 7',
      duration: '02 tiết (90 phút)'
    },
    illustrations: [
      loadIll('mindmap_toan8_chuong3_tonghop', 'Sơ đồ tư duy Tổng hợp Chương III: Tứ giác', 'mindmap_toan8_chuong3_tonghop.png', 520, 265),
      loadIll('hinh_sgk_3_59_bai_3_42', 'Hình 3.59. Bài tập 3.42: Tứ giác ABCD có hai đường chéo bằng nhau', 'hinh_sgk_3_59_bai_3_42.png', 360, 188),
      loadIll('hinh_sgk_3_60_bai_3_44', 'Hình 3.60. Bài tập 3.44: Tam giác vuông ABC và các tứ giác', 'hinh_sgk_3_60_bai_3_44.png', 450, 210),
      loadIll('hinh_sgk_3_61_bai_3_45', 'Hình 3.61. Bài tập 3.45: Tam giác cân ABC và hệ thức khoảng cách', 'hinh_sgk_3_61_bai_3_45.png', 420, 263)
    ].filter(Boolean)
  },
  {
    fileName: 'KHBD_09_Toan8_OnTapGiuaHK1_HinhHoc_Tiet15-16.docx',
    mdPath: path.resolve(__dirname, 'khbd_toan8_builder/BAI_09.md'),
    info: {
      subject: 'Toán',
      grade: '8',
      lessonScope: 'Tiết 15, 16',
      topic: 'ÔN TẬP GIỮA HỌC KÌ I (HÌNH HỌC)',
      ppct: 'Tiết 15, 16 — Tuần 8',
      duration: '02 tiết (90 phút)'
    },
    illustrations: [
      loadIll('mindmap_toan8_chuong3_ontap', 'Sơ đồ tư duy Ôn tập giữa HK1 Hình học: Phương pháp chứng minh', 'mindmap_toan8_chuong3_ontap.png', 520, 265)
    ].filter(Boolean)
  }
];

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

/**
 * Hàm ghép nhiều bài học thành 1 file docx hoàn chỉnh nhiều section
 */
async function exportMergedDocx(lessonList, outputFileName, docTitle) {
  const docx = loadDocx();
  const { Document, Packer, Footer, AlignmentType, Paragraph, TextRun, ImageRun, Table, TableRow, TableCell, WidthType, BorderStyle, TableLayoutType, VerticalAlign } = docx;

  const khbdDocxPath = fs.existsSync(path.resolve(__dirname, '../js/khbd-docx.js'))
    ? path.resolve(__dirname, '../js/khbd-docx.js')
    : path.resolve(__dirname, 'js/khbd-docx.js');
  const { DocxGenerator } = require(khbdDocxPath);

  const sections = [];

  for (const lesson of lessonList) {
    const generator = new DocxGenerator();

    global.appState = {
      content: { illustrations: lesson.illustrations },
      teachingContext: { lessonScope: lesson.info.lessonScope || '' }
    };
    global.window = {
      docx: docx,
      appState: global.appState,
      formatKhbdRoleLineBreaks: formatKhbdRoleLineBreaks
    };

    // Header chuẩn V2.1
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

    // Chèn hình
    generator.createIllustrationParagraphs = function (altText, illustrationId) {
      const safeId = this.safeIllustrationId(illustrationId);
      const ill = lesson.illustrations.find(item => item && item.id === safeId);
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
            new docx.ImageRun({
              data: bytes,
              transformation: { width: w, height: h },
              type: 'png'
            })
          ]
        })
      ];
    };

    // Table cell padding 0pt
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

    let markdownContent = sanitizeKhbdMathSource(fs.readFileSync(lesson.mdPath, 'utf8'));
    const headerElements = generator.createDocumentHeader(lesson.info);
    const footerElements = generator.createDocumentFooter(lesson.info);
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

    sections.push(section);
  }

  const doc = new Document({
    creator: 'Trợ lý Soạn Kế hoạch Bài dạy AI',
    title: docTitle,
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
    sections
  });

  const buffer = await Packer.toBuffer(doc);
  let outPath = path.join(KET_QUA_DIR, outputFileName);
  try {
    fs.writeFileSync(outPath, buffer);
  } catch (err) {
    if (err.code === 'EBUSY') {
      const ext = path.extname(outPath);
      outPath = outPath.replace(ext, `_CapNhat${ext}`);
      fs.writeFileSync(outPath, buffer);
      console.warn(`[CẢNH BÁO EBUSY] File đang mở trong Word, đã ghi ra: ${outPath}`);
    } else {
      throw err;
    }
  }
  console.log(`[GHÉP NỐI THÀNH CÔNG] Đã tạo file: ${outPath} (${buffer.length} bytes)`);
  return { path: outPath, size: buffer.length };
}

async function run() {
  console.log('=== BẮT ĐẦU QUY TRÌNH SOẠN BÀI HÀNG LOẠT (BATCH EXPORT) TOÁN 8 ===\n');

  // 1. Xuất từng bài đơn lẻ
  for (let i = 0; i < lessons.length; i++) {
    const lesson = lessons[i];
    const outPath = path.join(KET_QUA_DIR, lesson.fileName);
    console.log(`[${i + 1}/${lessons.length}] Đang xuất: ${lesson.fileName}...`);
    try {
      const res = await createKhbdDocx({
        mdFilePath: lesson.mdPath,
        outputDocxPath: outPath,
        lessonInfo: lesson.info,
        illustrations: lesson.illustrations
      });
      console.log(`   -> Thành công! Kích thước: ${res.size} bytes\n`);
    } catch (err) {
      console.error(`   -> LỖI tại bài ${lesson.fileName}:`, err);
    }
  }

  // 2. Ghép nối 5 bài Đại số (Bài 1 -> Bài 5)
  console.log('--- GHÉP NỐI TOÀN BỘ CÁC BÀI ĐẠI SỐ (CHƯƠNG I) THÀNH 1 FILE ---');
  const daisoLessons = lessons.slice(0, 5);
  await exportMergedDocx(daisoLessons, 'KHBD_Toan8_Ghep_DaiSo_Chuong1.docx', 'Kế hoạch bài dạy Toán 8 - Đại số Chương I');

  // 3. Ghép nối 4 bài Hình học (Bài 6 -> Bài 9)
  console.log('\n--- GHÉP NỐI TOÀN BỘ CÁC BÀI HÌNH HỌC (CHƯƠNG III) THÀNH 1 FILE ---');
  const hinhhocLessons = lessons.slice(5, 9);
  await exportMergedDocx(hinhhocLessons, 'KHBD_Toan8_Ghep_HinhHoc_Chuong3.docx', 'Kế hoạch bài dạy Toán 8 - Hình học Chương III');

  console.log('\n=== HOÀN THÀNH XUẤT TOÀN BỘ 11 TỆP WORD THÀNH PHẨM! ===');
}

run().catch(console.error);
