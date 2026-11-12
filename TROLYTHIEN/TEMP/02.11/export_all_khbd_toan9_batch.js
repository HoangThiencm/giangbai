/**
 * Script biên dịch và xuất hàng loạt KHBD Toán 9 (Tuần 9 - 12)
 * Thầy Hoàng Tấn Thiên - Năm học 2026 - 2027
 * Chuẩn CV 5512 V2.1 - 100% Word Equation OMML - Đầy đủ Sơ đồ tư duy Mindmap
 */

const fs = require('fs');
const path = require('path');
const { createKhbdDocx, createMergedKhbdDocx } = require('../../engine/export_khbd_engine');

const tempDir = path.resolve(__dirname);
const outputDir = path.resolve(__dirname, '../../1_SOAN_KHBD/Ket_qua/02.11');

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

const mindmap03 = getMindmapDataUrl('mindmap_03_on_tap_dai_so_giua_hk1.png');
const mindmap04 = getMindmapDataUrl('mindmap_04_on_tap_hinh_hoc_giua_hk1.png');
const mindmap07 = getMindmapDataUrl('mindmap_07_luyen_tap_chung_dai_so_tiet29.png');
const mindmap09 = getMindmapDataUrl('mindmap_09_luyen_tap_chung_hinh_hoc_tiet17.png');

const lessons = [
  {
    id: "01",
    branch: "DaiSo",
    mdFile: "01_Bai07_CanBacHaiVaCanThucBacHai.md",
    outFile: "01_KHBD_Toan9_Bai07_CanBacHaiVaCanThucBacHai_Tiet23-24.docx",
    illustrations: [],
    lessonInfo: {
      topic: "BÀI 7: CĂN BẬC HAI VÀ CĂN THỨC BẬC HAI",
      ppct: "Tiết 23, 24",
      lessonScope: "Tiết 23, 24",
      duration: "02 tiết (90 phút)"
    }
  },
  {
    id: "02",
    branch: "HinhHoc",
    mdFile: "02_Bai14_CungVaDayCuaDuongTron.md",
    outFile: "02_KHBD_Toan9_Bai14_CungVaDayCuaDuongTron_Tiet11-12.docx",
    illustrations: [],
    lessonInfo: {
      topic: "BÀI 14: CUNG VÀ DÂY CỦA MỘT ĐƯỜNG TRÒN",
      ppct: "Tiết 11, 12",
      lessonScope: "Tiết 11, 12",
      duration: "02 tiết (90 phút)"
    }
  },
  {
    id: "03",
    branch: "DaiSo",
    mdFile: "03_OnTapGiuaHK1_DaiSo.md",
    outFile: "03_KHBD_Toan9_OnTapGiuaHK1_DaiSo_Tiet25.docx",
    illustrations: mindmap03 ? [{
      id: "mindmap-03",
      dataUrl: mindmap03,
      width: 580,
      height: 325,
      caption: "Sơ đồ tư duy Ôn tập Đại số giữa Học kì I"
    }] : [],
    lessonInfo: {
      topic: "ÔN TẬP GIỮA HỌC KÌ I (ĐẠI SỐ)",
      ppct: "Tiết 25",
      lessonScope: "Tiết 25",
      duration: "01 tiết (45 phút)"
    }
  },
  {
    id: "04",
    branch: "HinhHoc",
    mdFile: "04_OnTapGiuaHK1_HinhHoc.md",
    outFile: "04_KHBD_Toan9_OnTapGiuaHK1_HinhHoc_Tiet13.docx",
    illustrations: mindmap04 ? [{
      id: "mindmap-04",
      dataUrl: mindmap04,
      width: 580,
      height: 325,
      caption: "Sơ đồ tư duy Ôn tập Hình học giữa Học kì I"
    }] : [],
    lessonInfo: {
      topic: "ÔN TẬP GIỮA HỌC KÌ I (HÌNH HỌC)",
      ppct: "Tiết 13",
      lessonScope: "Tiết 13",
      duration: "01 tiết (45 phút)"
    }
  },
  {
    id: "05",
    branch: "DaiSo",
    mdFile: "05_Bai08_KhaiCanBacHaiPhepNhanPhepChia.md",
    outFile: "05_KHBD_Toan9_Bai08_KhaiCanBacHaiPhepNhanPhepChia_Tiet27-28.docx",
    illustrations: [],
    lessonInfo: {
      topic: "BÀI 8: KHAI CĂN BẬC HAI VỚI PHÉP NHÂN VÀ PHÉP CHIA",
      ppct: "Tiết 27, 28",
      lessonScope: "Tiết 27, 28",
      duration: "02 tiết (90 phút)"
    }
  },
  {
    id: "06",
    branch: "HinhHoc",
    mdFile: "06_Bai15_DoDaiCungTron_QuatTron_STEM.md",
    outFile: "06_KHBD_Toan9_Bai15_DoDaiCungTron_QuatTron_STEM_Tiet15-16.docx",
    illustrations: [],
    lessonInfo: {
      topic: "BÀI 15: ĐỘ DÀI CỦA CUNG TRÒN. DIỆN TÍCH HÌNH QUẠT TRÒN VÀ HÌNH VÀNH KHUYÊN (BÀI HỌC STEM)",
      ppct: "Tiết 15, 16",
      lessonScope: "Tiết 15, 16",
      duration: "02 tiết (90 phút)"
    }
  },
  {
    id: "07",
    branch: "DaiSo",
    mdFile: "07_LuyenTapChung_DaiSo_Tiet29.md",
    outFile: "07_KHBD_Toan9_LuyenTapChung_DaiSo_Tiet29.docx",
    illustrations: mindmap07 ? [{
      id: "mindmap-07",
      dataUrl: mindmap07,
      width: 580,
      height: 325,
      caption: "Sơ đồ tư duy Căn bậc hai và Căn thức bậc hai"
    }] : [],
    lessonInfo: {
      topic: "LUYỆN TẬP CHUNG (TRANG 52 - 53)",
      ppct: "Tiết 29",
      lessonScope: "Tiết 29",
      duration: "01 tiết (45 phút)"
    }
  },
  {
    id: "08",
    branch: "DaiSo",
    mdFile: "08_Bai09_BienDoiDonGianVaRutGonCanThuc.md",
    outFile: "08_KHBD_Toan9_Bai09_BienDoiDonGianVaRutGonCanThuc_Tiet30-32.docx",
    illustrations: [],
    lessonInfo: {
      topic: "BÀI 9: BIẾN ĐỔI ĐƠN GIẢN VÀ RÚT GỌN BIỂU THỨC CHỨA CĂN THỨC BẬC HAI",
      ppct: "Tiết 30, 31, 32",
      lessonScope: "Tiết 30, 31, 32",
      duration: "03 tiết (135 phút)"
    }
  },
  {
    id: "09",
    branch: "HinhHoc",
    mdFile: "09_LuyenTapChung_HinhHoc_Tiet17.md",
    outFile: "09_KHBD_Toan9_LuyenTapChung_HinhHoc_Tiet17.docx",
    illustrations: mindmap09 ? [{
      id: "mindmap-09",
      dataUrl: mindmap09,
      width: 580,
      height: 325,
      caption: "Sơ đồ tư duy Chương V: Đường tròn"
    }] : [],
    lessonInfo: {
      topic: "LUYỆN TẬP CHUNG (TRANG 96 - 98)",
      ppct: "Tiết 17",
      lessonScope: "Tiết 17",
      duration: "01 tiết (45 phút)"
    }
  },
  {
    id: "10",
    branch: "HinhHoc",
    mdFile: "10_Bai16_ViTriTuongDoiCuaDuongThangVaDuongTron.md",
    outFile: "10_KHBD_Toan9_Bai16_ViTriTuongDoiCuaDuongThangVaDuongTron_Tiet18-20.docx",
    illustrations: [],
    lessonInfo: {
      topic: "BÀI 16: VỊ TRÍ TƯƠNG ĐỐI CỦA ĐƯỜNG THẲNG VÀ ĐƯỜNG TRÒN",
      ppct: "Tiết 18, 19, 20",
      lessonScope: "Tiết 18, 19, 20",
      duration: "03 tiết (135 phút)"
    }
  }
];

async function runBatch() {
  console.log("=== BẮT ĐẦU XUẤT 10 TỆP KHBD TOÁN 9 ĐƠN LẺ ===");
  
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

  console.log("\n=== BẮT ĐẦU GHÉP TỆP CHUYÊN ĐỀ ĐẠI SỐ (5 BÀI) ===");
  const daiSoLessons = lessons
    .filter(l => l.branch === "DaiSo")
    .map(l => ({
      mdFilePath: path.join(tempDir, l.mdFile),
      lessonInfo: l.lessonInfo,
      illustrations: l.illustrations
    }));

  const mergedDaiSoPath = path.join(outputDir, "KHBD_Toan9_Ghep_DaiSo_Tuan09-12.docx");
  try {
    const resDaiSo = await createMergedKhbdDocx({
      lessons: daiSoLessons,
      outputDocxPath: mergedDaiSoPath,
      docTitle: "KẾ HOẠCH BÀI DẠY TOÁN 9 - PHẦN ĐẠI SỐ (TUẦN 9 - 12)"
    });
    console.log(` -> THÀNH CÔNG TỆP GHÉP ĐẠI SỐ: ${path.basename(resDaiSo.path)} (${resDaiSo.size} bytes)`);
  } catch (err) {
    console.error(" -> LỖI ghép Đại số:", err);
  }

  console.log("\n=== BẮT ĐẦU GHÉP TỆP CHUYÊN ĐỀ HÌNH HỌC (5 BÀI) ===");
  const hinhHocLessons = lessons
    .filter(l => l.branch === "HinhHoc")
    .map(l => ({
      mdFilePath: path.join(tempDir, l.mdFile),
      lessonInfo: l.lessonInfo,
      illustrations: l.illustrations
    }));

  const mergedHinhHocPath = path.join(outputDir, "KHBD_Toan9_Ghep_HinhHoc_Tuan09-12.docx");
  try {
    const resHinhHoc = await createMergedKhbdDocx({
      lessons: hinhHocLessons,
      outputDocxPath: mergedHinhHocPath,
      docTitle: "KẾ HOẠCH BÀI DẠY TOÁN 9 - PHẦN HÌNH HỌC (TUẦN 9 - 12)"
    });
    console.log(` -> THÀNH CÔNG TỆP GHÉP HÌNH HỌC: ${path.basename(resHinhHoc.path)} (${resHinhHoc.size} bytes)`);
  } catch (err) {
    console.error(" -> LỖI ghép Hình học:", err);
  }

  console.log("\n=== HOÀN TẤT TOÀN BỘ QUÁ TRÌNH BIÊN DỊCH VÀ XUẤT FILE DOCX CÓ MINDMAP! ===");
}

runBatch().catch(console.error);
