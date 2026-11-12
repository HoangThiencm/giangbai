/**
 * Script biên dịch và xuất hàng loạt KHBD Toán 6 (Tuần 9 - 12)
 * Thầy Hoàng Tấn Thiên - Năm học 2026 - 2027
 * Chuẩn CV 5512 V2.1 - 100% Word Equation OMML - Đầy đủ Sơ đồ tư duy Mindmap vector 300 DPI
 */

const fs = require('fs');
const path = require('path');
const { createKhbdDocx, createMergedKhbdDocx } = require('../../engine/export_khbd_engine');

const tempDir = path.resolve(__dirname);
const outputDir = path.resolve(__dirname, '../../1_SOAN_KHBD/Ket_qua/02.11/TOAN6');
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

const mindmap01 = getMindmapDataUrl('mindmap_01_luyen_tap_chung_chuong2_tiet25.png');
const mindmap02 = getMindmapDataUrl('mindmap_02_bai_tap_cuoi_chuong2_tiet26.png');
const mindmap03 = getMindmapDataUrl('mindmap_03_on_tap_giua_hk1_sohoc_tiet27_28.png');
const mindmap07 = getMindmapDataUrl('mindmap_07_on_tap_giua_hk1_hinhhoc_tiet09.png');
const mindmap08 = getMindmapDataUrl('mindmap_08_luyen_tap_chung_hinhhoc_tiet11.png');
const mindmap09 = getMindmapDataUrl('mindmap_09_bai_tap_cuoi_chuong4_tiet12.png');

const lessons = [
  {
    id: "01",
    branch: "SoHoc",
    mdFile: "01_LuyenTapChung_Chuong2_Tiet25.md",
    outFile: "01_KHBD_Toan6_LuyenTapChung_Chuong2_Tiet25.docx",
    illustrations: mindmap01 ? [{
      id: "mindmap-tiet25",
      dataUrl: mindmap01,
      width: 580,
      height: 325,
      caption: "Sơ đồ tư duy Luyện tập chung Chương II (ƯCLN & BCNN)"
    }] : [],
    lessonInfo: {
      topic: "LUYỆN TẬP CHUNG (TRANG 54 - 55)",
      ppct: "Tiết 25",
      lessonScope: "Tiết 25",
      duration: "01 tiết (45 phút)"
    }
  },
  {
    id: "02",
    branch: "SoHoc",
    mdFile: "02_BaiTapCuoiChuong2_Tiet26.md",
    outFile: "02_KHBD_Toan6_BaiTapCuoiChuong2_Tiet26.docx",
    illustrations: mindmap02 ? [{
      id: "mindmap-tiet26",
      dataUrl: mindmap02,
      width: 580,
      height: 325,
      caption: "Sơ đồ tư duy Bài tập cuối chương II (Tính chia hết)"
    }] : [],
    lessonInfo: {
      topic: "BÀI TẬP CUỐI CHƯƠNG II (TRANG 56)",
      ppct: "Tiết 26",
      lessonScope: "Tiết 26",
      duration: "01 tiết (45 phút)"
    }
  },
  {
    id: "03",
    branch: "SoHoc",
    mdFile: "03_OnTapGiuaHK1_SoHoc_Tiet27-28.md",
    outFile: "03_KHBD_Toan6_OnTapGiuaHK1_SoHoc_Tiet27-28.docx",
    illustrations: mindmap03 ? [{
      id: "mindmap-tiet27-28",
      dataUrl: mindmap03,
      width: 580,
      height: 325,
      caption: "Sơ đồ tư duy Ôn tập Số học giữa Học kì I"
    }] : [],
    lessonInfo: {
      topic: "ÔN TẬP KIỂM TRA ĐÁNH GIÁ GIỮA HỌC KÌ I (SỐ HỌC)",
      ppct: "Tiết 27, 28",
      lessonScope: "Tiết 27, 28",
      duration: "02 tiết (90 phút)"
    }
  },
  {
    id: "04",
    branch: "SoHoc",
    mdFile: "04_Bai13_TapHopCacSoNguyen_Tiet30-31.md",
    outFile: "04_KHBD_Toan6_Bai13_TapHopCacSoNguyen_Tiet30-31.docx",
    illustrations: [],
    lessonInfo: {
      topic: "BÀI 13: TẬP HỢP CÁC SỐ NGUYÊN",
      ppct: "Tiết 30, 31",
      lessonScope: "Tiết 30, 31",
      duration: "02 tiết (90 phút)"
    }
  },
  {
    id: "05",
    branch: "SoHoc",
    mdFile: "05_Bai14_PhepCongVaPhepTruSoNguyen_Tiet32-34.md",
    outFile: "05_KHBD_Toan6_Bai14_PhepCongVaPhepTruSoNguyen_Tiet32-34.docx",
    illustrations: [],
    lessonInfo: {
      topic: "BÀI 14: PHÉP CỘNG VÀ PHÉP TRỪ SỐ NGUYÊN",
      ppct: "Tiết 32, 33, 34",
      lessonScope: "Tiết 32, 33, 34",
      duration: "03 tiết (135 phút)"
    }
  },
  {
    id: "06",
    branch: "SoHoc",
    mdFile: "06_Bai15_QuyTacDauNgoac_Tiet35-36.md",
    outFile: "06_KHBD_Toan6_Bai15_QuyTacDauNgoac_Tiet35-36.docx",
    illustrations: [],
    lessonInfo: {
      topic: "BÀI 15: QUY TẮC DẤU NGOẶC",
      ppct: "Tiết 35, 36",
      lessonScope: "Tiết 35, 36",
      duration: "02 tiết (90 phút)"
    }
  },
  {
    id: "07",
    branch: "HinhHoc",
    mdFile: "07_OnTapGiuaHK1_HinhHoc_Tiet09.md",
    outFile: "07_KHBD_Toan6_OnTapGiuaHK1_HinhHoc_Tiet09.docx",
    illustrations: mindmap07 ? [{
      id: "mindmap-tiet09",
      dataUrl: mindmap07,
      width: 580,
      height: 325,
      caption: "Sơ đồ tư duy Ôn tập Hình học giữa Học kì I"
    }] : [],
    lessonInfo: {
      topic: "ÔN TẬP KIỂM TRA ĐÁNH GIÁ GIỮA HỌC KÌ I (HÌNH HỌC)",
      ppct: "Tiết 09",
      lessonScope: "Tiết 09",
      duration: "01 tiết (45 phút)"
    }
  },
  {
    id: "08",
    branch: "HinhHoc",
    mdFile: "08_LuyenTapChung_HinhHoc_Tiet11.md",
    outFile: "08_KHBD_Toan6_LuyenTapChung_HinhHoc_Tiet11.docx",
    illustrations: mindmap08 ? [{
      id: "mindmap-tiet11",
      dataUrl: mindmap08,
      width: 580,
      height: 325,
      caption: "Sơ đồ tư duy Luyện tập chung Hình học Chương IV"
    }] : [],
    lessonInfo: {
      topic: "LUYỆN TẬP CHUNG (HÌNH HỌC CHƯƠNG IV)",
      ppct: "Tiết 11",
      lessonScope: "Tiết 11",
      duration: "01 tiết (45 phút)"
    }
  },
  {
    id: "09",
    branch: "HinhHoc",
    mdFile: "09_BaiTapCuoiChuong4_Tiet12.md",
    outFile: "09_KHBD_Toan6_BaiTapCuoiChuong4_Tiet12.docx",
    illustrations: mindmap09 ? [{
      id: "mindmap-tiet12",
      dataUrl: mindmap09,
      width: 580,
      height: 325,
      caption: "Sơ đồ tư duy Bài tập cuối chương IV (Các hình phẳng)"
    }] : [],
    lessonInfo: {
      topic: "BÀI TẬP CUỐI CHƯƠNG IV (CÁC HÌNH PHẲNG TRONG THỰC TIỄN)",
      ppct: "Tiết 12",
      lessonScope: "Tiết 12",
      duration: "01 tiết (45 phút)"
    }
  }
];

async function runBatch() {
  console.log("=== BẮT ĐẦU XUẤT 9 TỆP KHBD TOÁN 6 ĐƠN LẺ ===");
  
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

      // Sao chép thêm bản backup ra thư mục chính Ket_qua/02.11/
      const copyDest = path.join(mainOutputDir, item.outFile);
      fs.copyFileSync(docxPath, copyDest);
    } catch (err) {
      console.error(` -> LỖI khi xuất ${item.outFile}:`, err);
    }
  }

  console.log("\n=== BẮT ĐẦU GHÉP TỆP CHUYÊN ĐỀ SỐ HỌC (6 BÀI) ===");
  const soHocLessons = lessons
    .filter(l => l.branch === "SoHoc")
    .map(l => ({
      mdFilePath: path.join(tempDir, l.mdFile),
      lessonInfo: l.lessonInfo,
      illustrations: l.illustrations
    }));

  const mergedSoHocPath = path.join(outputDir, "KHBD_Toan6_Ghep_SoHoc_Tuan09-12.docx");
  try {
    const resSoHoc = await createMergedKhbdDocx({
      lessons: soHocLessons,
      outputDocxPath: mergedSoHocPath,
      docTitle: "KẾ HOẠCH BÀI DẠY TOÁN 6 - PHẦN SỐ HỌC (TUẦN 9 - 12)"
    });
    console.log(` -> THÀNH CÔNG TỆP GHÉP SỐ HỌC: ${path.basename(resSoHoc.path)} (${resSoHoc.size} bytes)`);
    fs.copyFileSync(mergedSoHocPath, path.join(mainOutputDir, "KHBD_Toan6_Ghep_SoHoc_Tuan09-12.docx"));
  } catch (err) {
    console.error(" -> LỖI ghép Số học:", err);
  }

  console.log("\n=== BẮT ĐẦU GHÉP TỆP CHUYÊN ĐỀ HÌNH HỌC (3 BÀI) ===");
  const hinhHocLessons = lessons
    .filter(l => l.branch === "HinhHoc")
    .map(l => ({
      mdFilePath: path.join(tempDir, l.mdFile),
      lessonInfo: l.lessonInfo,
      illustrations: l.illustrations
    }));

  const mergedHinhHocPath = path.join(outputDir, "KHBD_Toan6_Ghep_HinhHoc_Tuan09-12.docx");
  try {
    const resHinhHoc = await createMergedKhbdDocx({
      lessons: hinhHocLessons,
      outputDocxPath: mergedHinhHocPath,
      docTitle: "KẾ HOẠCH BÀI DẠY TOÁN 6 - PHẦN HÌNH HỌC (TUẦN 9 - 12)"
    });
    console.log(` -> THÀNH CÔNG TỆP GHÉP HÌNH HỌC: ${path.basename(resHinhHoc.path)} (${resHinhHoc.size} bytes)`);
    fs.copyFileSync(mergedHinhHocPath, path.join(mainOutputDir, "KHBD_Toan6_Ghep_HinhHoc_Tuan09-12.docx"));
  } catch (err) {
    console.error(" -> LỖI ghép Hình học:", err);
  }

  console.log("\n=== HOÀN TẤT TOÀN BỘ QUÁ TRÌNH BIÊN DỊCH VÀ XUẤT FILE DOCX TOÁN 6 CÓ MINDMAP! ===");
}

runBatch().catch(console.error);
