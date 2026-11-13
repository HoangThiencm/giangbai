/**
 * Script biên dịch và xuất hàng loạt KHBD Tin học 6 (Tuần 9 - 12)
 * Thầy Hoàng Tấn Thiên - Năm học 2026 - 2027
 * Chuẩn CV 5512 V2.1 - 100% Word Equation OMML - Đầy đủ Sơ đồ tư duy Mindmap vector 300 DPI
 */

const fs = require('fs');
const path = require('path');
const { createKhbdDocx, createMergedKhbdDocx } = require('../../engine/export_khbd_engine');

const tempDir = path.resolve(__dirname);
const outputDir = path.resolve(__dirname, '../../1_SOAN_KHBD/Ket_qua/02.11/TIN6');
const mainOutputDir = path.resolve(__dirname, '../../1_SOAN_KHBD/Ket_qua/02.11');

if (!fs.existsSync(outputDir)) {
  fs.mkdirSync(outputDir, { recursive: true });
}

// Hàm đọc ảnh thành Base64 DataURL
function getMindmapDataUrl(filename) {
  const imgPath = path.join(tempDir, 'mindmaps', filename);
  if (fs.existsSync(imgPath)) {
    const b64 = fs.readFileSync(imgPath).toString('base64');
    return `data:image/png;base64,${b64}`;
  }
  return null;
}

const mindmap01 = getMindmapDataUrl('mindmap_01_on_tap_giua_hk1_tin6_tiet09.png');
const mindmap03 = getMindmapDataUrl('mindmap_03_mang_thong_tin_toan_cau_tiet11_12.png');

const lessons = [
  {
    id: "01",
    mdFile: "01_OnTapGiuaHK1_Tin6_Tiet09.md",
    outFile: "01_KHBD_Tin6_OnTapGiuaHK1_Tiet09.docx",
    illustrations: mindmap01 ? [{
      id: "mindmap-tiet09",
      dataUrl: mindmap01,
      width: 580,
      height: 325,
      caption: "Sơ đồ tư duy Ôn tập Giữa Học kì I - Môn Tin học 6"
    }] : [],
    lessonInfo: {
      topic: "ÔN TẬP KIỂM TRA ĐÁNH GIÁ GIỮA HỌC KÌ I",
      ppct: "Tiết 09",
      lessonScope: "Tiết 09",
      duration: "01 tiết (45 phút)"
    }
  },
  {
    id: "02",
    mdFile: "02_KiemTraGiuaHK1_Tin6_Tiet10.md",
    outFile: "02_KHBD_Tin6_KiemTraGiuaHK1_Tiet10.docx",
    illustrations: [],
    lessonInfo: {
      topic: "KIỂM TRA ĐÁNH GIÁ GIỮA HỌC KÌ I (TIN HỌC 6)",
      ppct: "Tiết 10",
      lessonScope: "Tiết 10",
      duration: "01 tiết (45 phút)"
    }
  },
  {
    id: "03",
    mdFile: "03_Bai06_MangThongTinToanCau_Tiet11-12.md",
    outFile: "03_KHBD_Tin6_Bai06_MangThongTinToanCau_Tiet11-12.docx",
    illustrations: mindmap03 ? [{
      id: "mindmap-tiet11-12",
      dataUrl: mindmap03,
      width: 580,
      height: 325,
      caption: "Sơ đồ tư duy Bài 6: Mạng thông tin toàn cầu (World Wide Web)"
    }] : [],
    lessonInfo: {
      topic: "BÀI 6: MẠNG THÔNG TIN TOÀN CẦU",
      ppct: "Tiết 11, 12",
      lessonScope: "Tiết 11, 12",
      duration: "02 tiết (90 phút)"
    }
  }
];

async function runBatch() {
  console.log("=== BẮT ĐẦU XUẤT 3 TỆP KHBD TIN HỌC 6 ĐƠN LẺ ===");
  
  for (const item of lessons) {
    const mdPath = path.join(tempDir, item.mdFile);
    const docxPath = path.join(outputDir, item.outFile);
    
    console.log(`[Đang xuất] ${item.outFile} (Mindmaps: ${item.illustrations.length})...`);
    try {
      const res = await createKhbdDocx({
        mdFilePath: mdPath,
        outputDocxPath: docxPath,
        lessonInfo: item.lessonInfo,
        illustrations: item.illustrations
      });
      console.log(` -> THÀNH CÔNG: ${path.basename(res.path)} (${res.size} bytes)`);

      // Sao chép bản backup ra Ket_qua/02.11/
      const copyDest = path.join(mainOutputDir, item.outFile);
      fs.copyFileSync(docxPath, copyDest);
    } catch (err) {
      console.error(` -> LỖI khi xuất ${item.outFile}:`, err);
    }
  }

  console.log("\n=== BẮT ĐẦU GHÉP TỆP CHUYÊN ĐỀ TIN HỌC 6 (TUẦN 9 - 12) ===");
  const allTinLessons = lessons.map(l => ({
    mdFilePath: path.join(tempDir, l.mdFile),
    lessonInfo: l.lessonInfo,
    illustrations: l.illustrations
  }));

  const mergedTinPath = path.join(outputDir, "KHBD_Tin6_Ghep_Tuan09-12.docx");
  try {
    const resTin = await createMergedKhbdDocx({
      lessons: allTinLessons,
      outputDocxPath: mergedTinPath,
      docTitle: "KẾ HOẠCH BÀI DẠY TIN HỌC 6 (TUẦN 9 - 12)"
    });
    console.log(` -> THÀNH CÔNG TỆP GHÉP TIN HỌC 6: ${path.basename(resTin.path)} (${resTin.size} bytes)`);
    fs.copyFileSync(mergedTinPath, path.join(mainOutputDir, "KHBD_Tin6_Ghep_Tuan09-12.docx"));
  } catch (err) {
    console.error(" -> LỖI ghép Tin học 6:", err);
  }

  console.log("\n=== HOÀN TẤT TOÀN BỘ QUÁ TRÌNH BIÊN DỊCH VÀ XUẤT FILE DOCX TIN HỌC 6! ===");
}

runBatch().catch(console.error);
