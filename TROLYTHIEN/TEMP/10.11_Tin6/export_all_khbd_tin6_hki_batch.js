/**
 * Script biên dịch và xuất hàng loạt KHBD Tin học 6 (Tuần 13 - 18)
 * Thầy Hoàng Tấn Thiên - Năm học 2026 - 2027
 * Chuẩn CV 5512 V2.1 - 100% Word Equation OMML - Đầy đủ Sơ đồ tư duy Mindmap vector 300 DPI
 */

const fs = require('fs');
const path = require('path');
const { createKhbdDocx, createMergedKhbdDocx } = require('../../engine/export_khbd_engine');

const tempDir = path.resolve(__dirname);
const outputDir = path.resolve(__dirname, '../../1_SOAN_KHBD/Ket_qua/10.11/TIN6');

if (!fs.existsSync(outputDir)) {
  fs.mkdirSync(outputDir, { recursive: true });
}

function getMindmapDataUrl(filename) {
  const imgPath = path.join(tempDir, 'mindmaps', filename);
  if (fs.existsSync(imgPath)) {
    const b64 = fs.readFileSync(imgPath).toString('base64');
    return `data:image/png;base64,${b64}`;
  }
  return null;
}

const mindmap17 = getMindmapDataUrl('mindmap_03_on_tap_cuoi_hk1_tin6_tiet17.png');

const lessons = [
  {
    id: "01",
    mdFile: "01_Bai07_TimKiemThongTinTrenInternet_Tiet13-14.md",
    outFile: "01_KHBD_Tin6_Bai07_TimKiemThongTinTrenInternet_Tiet13-14.docx",
    illustrations: [],
    lessonInfo: {
      topic: "BÀI 7: TÌM KIẾM THÔNG TIN TRÊN INTERNET",
      ppct: "Tiết 13, 14",
      lessonScope: "Tiết 13, 14",
      duration: "02 tiết (90 phút)"
    }
  },
  {
    id: "02",
    mdFile: "02_Bai08_ThuDienTu_Tiet15-16.md",
    outFile: "02_KHBD_Tin6_Bai08_ThuDienTu_Tiet15-16.docx",
    illustrations: [],
    lessonInfo: {
      topic: "BÀI 8: THƯ ĐIỆN TỬ",
      ppct: "Tiết 15, 16",
      lessonScope: "Tiết 15, 16",
      duration: "02 tiết (90 phút)"
    }
  },
  {
    id: "03",
    mdFile: "03_OnTapCuoiHK1_Tin6_Tiet17.md",
    outFile: "03_KHBD_Tin6_OnTapCuoiHK1_Tiet17.docx",
    illustrations: mindmap17 ? [{
      id: "mindmap-tiet17",
      dataUrl: mindmap17,
      width: 580,
      height: 325,
      caption: "Sơ đồ tư duy Ôn tập Cuối Học kì I - Môn Tin học 6"
    }] : [],
    lessonInfo: {
      topic: "ÔN TẬP CUỐI HỌC KÌ I (TIN HỌC 6)",
      ppct: "Tiết 17",
      lessonScope: "Tiết 17",
      duration: "01 tiết (45 phút)"
    }
  },
  {
    id: "04",
    mdFile: "04_KiemTraCuoiHK1_Tin6_Tiet18.md",
    outFile: "04_KHBD_Tin6_KiemTraCuoiHK1_Tiet18.docx",
    illustrations: [],
    lessonInfo: {
      topic: "KIỂM TRA ĐÁNH GIÁ CUỐI HỌC KÌ I (TIN HỌC 6)",
      ppct: "Tiết 18",
      lessonScope: "Tiết 18",
      duration: "01 tiết (45 phút)"
    }
  }
];

async function runBatch() {
  console.log("=== BẮT ĐẦU XUẤT 4 TỆP KHBD TIN HỌC 6 (TUẦN 13 - 18) ===");
  
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
    } catch (err) {
      console.error(` -> LỖI khi xuất ${item.outFile}:`, err);
    }
  }

  console.log("\n=== BẮT ĐẦU GHÉP TỆP CHUYÊN ĐỀ TIN HỌC 6 (TUẦN 13 - 18) ===");
  const allTinLessons = lessons.map(l => ({
    mdFilePath: path.join(tempDir, l.mdFile),
    lessonInfo: l.lessonInfo,
    illustrations: l.illustrations
  }));

  const mergedTinPath = path.join(outputDir, "KHBD_Tin6_Ghep_Tuan13-18.docx");
  try {
    const resTin = await createMergedKhbdDocx({
      lessons: allTinLessons,
      outputDocxPath: mergedTinPath,
      docTitle: "KẾ HOẠCH BÀI DẠY TIN HỌC 6 (TUẦN 13 - 18)"
    });
    console.log(` -> THÀNH CÔNG TỆP GHÉP TIN HỌC 6: ${path.basename(resTin.path)} (${resTin.size} bytes)`);
  } catch (err) {
    console.error(" -> LỖI ghép Tin học 6:", err);
  }

  console.log("\n=== HOÀN TẤT XUẤT FILE DOCX TIN HỌC 6 (TUẦN 13 - 18)! ===");
}

runBatch().catch(console.error);
