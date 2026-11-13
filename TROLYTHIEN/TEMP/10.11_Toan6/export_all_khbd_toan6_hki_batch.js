/**
 * Script biên dịch và xuất hàng loạt KHBD Toán 6 (Tuần 13 - 18)
 * Thầy Hoàng Tấn Thiên - Năm học 2026 - 2027
 * Chuẩn CV 5512 V2.1 - 100% Word Equation OMML - Đầy đủ Sơ đồ tư duy Mindmap vector 300 DPI
 */

const fs = require('fs');
const path = require('path');
const { createKhbdDocx, createMergedKhbdDocx } = require('../../engine/export_khbd_engine');

const tempDir = path.resolve(__dirname);
const outputDir = path.resolve(__dirname, '../../1_SOAN_KHBD/Ket_qua/10.11/TOAN6');

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

const map37 = getMindmapDataUrl('mindmap_toan6_tiet37.png');
const map42 = getMindmapDataUrl('mindmap_toan6_tiet42.png');
const map43 = getMindmapDataUrl('mindmap_toan6_tiet43.png');
const map44 = getMindmapDataUrl('mindmap_toan6_tiet44_47.png');
const mapH17 = getMindmapDataUrl('mindmap_toan6_hinh_tiet17.png');
const mapH18 = getMindmapDataUrl('mindmap_toan6_hinh_tiet18.png');
const mapH19 = getMindmapDataUrl('mindmap_toan6_hinh_tiet19.png');

const lessons = [
  // SỐ HỌC
  {
    id: "01",
    branch: "SoHoc",
    mdFile: "01_KHBD_Toan6_LuyenTapChung_Tiet37.md",
    outFile: "01_KHBD_Toan6_LuyenTapChung_Tiet37.docx",
    illustrations: map37 ? [{
      id: "mindmap-toan6-tiet37",
      dataUrl: map37,
      width: 580,
      height: 325,
      caption: "Sơ đồ tư duy Luyện tập chung Tiết 37 (Cộng trừ số nguyên & dấu ngoặc)"
    }] : [],
    lessonInfo: {
      topic: "LUYỆN TẬP CHUNG (TRANG 69)",
      ppct: "Tiết 37",
      lessonScope: "Tiết 37",
      duration: "01 tiết (45 phút)"
    }
  },
  {
    id: "02",
    branch: "SoHoc",
    mdFile: "02_KHBD_Toan6_Bai16_PhepNhanSoNguyen_Tiet38-40.md",
    outFile: "02_KHBD_Toan6_Bai16_PhepNhanSoNguyen_Tiet38-40.docx",
    illustrations: [],
    lessonInfo: {
      topic: "BÀI 16: PHÉP NHÂN SỐ NGUYÊN",
      ppct: "Tiết 38, 39, 40",
      lessonScope: "Tiết 38, 39, 40",
      duration: "03 tiết (135 phút)"
    }
  },
  {
    id: "03",
    branch: "SoHoc",
    mdFile: "03_KHBD_Toan6_Bai17_PhepChiaHet_UocBoi_Tiet41.md",
    outFile: "03_KHBD_Toan6_Bai17_PhepChiaHet_UocBoi_Tiet41.docx",
    illustrations: [],
    lessonInfo: {
      topic: "BÀI 17: PHÉP CHIA HẾT. ƯỚC VÀ BỘI CỦA MỘT SỐ NGUYÊN",
      ppct: "Tiết 41",
      lessonScope: "Tiết 41",
      duration: "01 tiết (45 phút)"
    }
  },
  {
    id: "04",
    branch: "SoHoc",
    mdFile: "04_KHBD_Toan6_LuyenTapChung_Tiet42.md",
    outFile: "04_KHBD_Toan6_LuyenTapChung_Tiet42.docx",
    illustrations: map42 ? [{
      id: "mindmap-toan6-tiet42",
      dataUrl: map42,
      width: 580,
      height: 325,
      caption: "Sơ đồ tư duy Luyện tập chung Tiết 42 (Phép nhân & chia, ước bội)"
    }] : [],
    lessonInfo: {
      topic: "LUYỆN TẬP CHUNG (TRANG 75)",
      ppct: "Tiết 42",
      lessonScope: "Tiết 42",
      duration: "01 tiết (45 phút)"
    }
  },
  {
    id: "05",
    branch: "SoHoc",
    mdFile: "05_KHBD_Toan6_BaiTapCuoiChuong3_Tiet43.md",
    outFile: "05_KHBD_Toan6_BaiTapCuoiChuong3_Tiet43.docx",
    illustrations: map43 ? [{
      id: "mindmap-toan6-tiet43",
      dataUrl: map43,
      width: 580,
      height: 325,
      caption: "Sơ đồ tư duy Bài tập cuối chương III (Số nguyên Z)"
    }] : [],
    lessonInfo: {
      topic: "BÀI TẬP CUỐI CHƯƠNG III (SỐ NGUYÊN)",
      ppct: "Tiết 43",
      lessonScope: "Tiết 43",
      duration: "01 tiết (45 phút)"
    }
  },
  {
    id: "06",
    branch: "SoHoc",
    mdFile: "06_KHBD_Toan6_OnTapCuoiHK1_SoHoc_Tiet44-47.md",
    outFile: "06_KHBD_Toan6_OnTapCuoiHK1_SoHoc_Tiet44-47.docx",
    illustrations: map44 ? [{
      id: "mindmap-toan6-tiet44-47",
      dataUrl: map44,
      width: 580,
      height: 325,
      caption: "Sơ đồ tư duy Ôn tập Cuối Học kì I - Phần Số học"
    }] : [],
    lessonInfo: {
      topic: "ÔN TẬP CUỐI HỌC KÌ I (SỐ HỌC)",
      ppct: "Tiết 44, 45, 46, 47",
      lessonScope: "Tiết 44, 45, 46, 47",
      duration: "04 tiết (180 phút)"
    }
  },
  {
    id: "07",
    branch: "SoHoc",
    mdFile: "07_KHBD_Toan6_KiemTraCuoiHK1_SoHoc_Tiet48.md",
    outFile: "07_KHBD_Toan6_KiemTraCuoiHK1_SoHoc_Tiet48.docx",
    illustrations: [],
    lessonInfo: {
      topic: "KIỂM TRA ĐÁNH GIÁ CUỐI HỌC KÌ I (SỐ HỌC 6)",
      ppct: "Tiết 48",
      lessonScope: "Tiết 48",
      duration: "01 tiết (45 phút)"
    }
  },
  {
    id: "08",
    branch: "SoHoc",
    mdFile: "08_KHBD_Toan6_HDTN_SuDungMayTinhCamTay_Tiet49-50.md",
    outFile: "08_KHBD_Toan6_HDTN_SuDungMayTinhCamTay_Tiet49-50.docx",
    illustrations: [],
    lessonInfo: {
      topic: "HOẠT ĐỘNG THỰC HÀNH VÀ TRẢI NGHIỆM: SỬ DỤNG MÁY TÍNH CẦM TAY",
      ppct: "Tiết 49, 50",
      lessonScope: "Tiết 49, 50",
      duration: "02 tiết (90 phút)"
    }
  },

  // HÌNH HỌC
  {
    id: "09",
    branch: "HinhHoc",
    mdFile: "09_KHBD_Toan6_Bai21_HinhCoTrucDoiXung_Tiet13-14.md",
    outFile: "09_KHBD_Toan6_Bai21_HinhCoTrucDoiXung_Tiet13-14.docx",
    illustrations: [],
    lessonInfo: {
      topic: "BÀI 21: HÌNH CÓ TRỤC ĐỐI XỨNG",
      ppct: "Tiết 13, 14",
      lessonScope: "Tiết 13, 14",
      duration: "02 tiết (90 phút)"
    }
  },
  {
    id: "10",
    branch: "HinhHoc",
    mdFile: "10_KHBD_Toan6_Bai22_HinhCoTamDoiXung_Tiet15-16.md",
    outFile: "10_KHBD_Toan6_Bai22_HinhCoTamDoiXung_Tiet15-16.docx",
    illustrations: [],
    lessonInfo: {
      topic: "BÀI 22: HÌNH CÓ TÂM ĐỐI XỨNG",
      ppct: "Tiết 15, 16",
      lessonScope: "Tiết 15, 16",
      duration: "02 tiết (90 phút)"
    }
  },
  {
    id: "11",
    branch: "HinhHoc",
    mdFile: "11_KHBD_Toan6_LuyenTapChung_HinhHoc_Tiet17.md",
    outFile: "11_KHBD_Toan6_LuyenTapChung_HinhHoc_Tiet17.docx",
    illustrations: mapH17 ? [{
      id: "mindmap-toan6-hinh-tiet17",
      dataUrl: mapH17,
      width: 580,
      height: 325,
      caption: "Sơ đồ tư duy Luyện tập chung Tiết 17 (Đối xứng trục & Đối xứng tâm)"
    }] : [],
    lessonInfo: {
      topic: "LUYỆN TẬP CHUNG (HÌNH HỌC TRỰC QUAN CHƯƠNG V)",
      ppct: "Tiết 17",
      lessonScope: "Tiết 17",
      duration: "01 tiết (45 phút)"
    }
  },
  {
    id: "12",
    branch: "HinhHoc",
    mdFile: "12_KHBD_Toan6_BaiTapCuoiChuong5_Tiet18.md",
    outFile: "12_KHBD_Toan6_BaiTapCuoiChuong5_Tiet18.docx",
    illustrations: mapH18 ? [{
      id: "mindmap-toan6-hinh-tiet18",
      dataUrl: mapH18,
      width: 580,
      height: 325,
      caption: "Sơ đồ tư duy Bài tập cuối chương V (Tính đối xứng của hình phẳng)"
    }] : [],
    lessonInfo: {
      topic: "BÀI TẬP CUỐI CHƯƠNG V (TÍNH ĐỐI XỨNG CỦA HÌNH PHẲNG)",
      ppct: "Tiết 18",
      lessonScope: "Tiết 18",
      duration: "01 tiết (45 phút)"
    }
  },
  {
    id: "13",
    branch: "HinhHoc",
    mdFile: "13_KHBD_Toan6_OnTapCuoiHK1_HinhHoc_Tiet19.md",
    outFile: "13_KHBD_Toan6_OnTapCuoiHK1_HinhHoc_Tiet19.docx",
    illustrations: mapH19 ? [{
      id: "mindmap-toan6-hinh-tiet19",
      dataUrl: mapH19,
      width: 580,
      height: 325,
      caption: "Sơ đồ tư duy Ôn tập Cuối Học kì I - Phần Hình học trực quan"
    }] : [],
    lessonInfo: {
      topic: "ÔN TẬP CUỐI HỌC KÌ I (HÌNH HỌC TRỰC QUAN 6)",
      ppct: "Tiết 19",
      lessonScope: "Tiết 19",
      duration: "01 tiết (45 phút)"
    }
  },
  {
    id: "14",
    branch: "HinhHoc",
    mdFile: "14_KHBD_Toan6_KiemTraCuoiHK1_HinhHoc_Tiet20.md",
    outFile: "14_KHBD_Toan6_KiemTraCuoiHK1_HinhHoc_Tiet20.docx",
    illustrations: [],
    lessonInfo: {
      topic: "KIỂM TRA ĐÁNH GIÁ CUỐI HỌC KÌ I (HÌNH HỌC TRỰC QUAN 6)",
      ppct: "Tiết 20",
      lessonScope: "Tiết 20",
      duration: "01 tiết (45 phút)"
    }
  },
  {
    id: "15",
    branch: "HinhHoc",
    mdFile: "15_KHBD_Toan6_HDTN_TamThiep_GeoGebra_Tiet21-22.md",
    outFile: "15_KHBD_Toan6_HDTN_TamThiep_GeoGebra_Tiet21-22.docx",
    illustrations: [],
    lessonInfo: {
      topic: "HOẠT ĐỘNG THỰC HÀNH VÀ TRẢI NGHIỆM: TẤM THIỆP CỦA EM & VẼ HÌNH VỚI GEOGEBRA",
      ppct: "Tiết 21, 22",
      lessonScope: "Tiết 21, 22",
      duration: "02 tiết (90 phút)"
    }
  }
];

async function runBatch() {
  console.log("=== BẮT ĐẦU XUẤT 15 TỆP KHBD TOÁN 6 ĐƠN LẺ ===");
  
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

  console.log("\n=== BẮT ĐẦU GHÉP TỆP CHUYÊN ĐỀ SỐ HỌC 6 (8 BÀI) ===");
  const soHocLessons = lessons
    .filter(l => l.branch === "SoHoc")
    .map(l => ({
      mdFilePath: path.join(tempDir, l.mdFile),
      lessonInfo: l.lessonInfo,
      illustrations: l.illustrations
    }));

  const mergedSoHocPath = path.join(outputDir, "KHBD_Toan6_Ghep_SoHoc_Tuan13-18.docx");
  try {
    const resSoHoc = await createMergedKhbdDocx({
      lessons: soHocLessons,
      outputDocxPath: mergedSoHocPath,
      docTitle: "KẾ HOẠCH BÀI DẠY TOÁN 6 - PHẦN SỐ HỌC (TUẦN 13 - 18)"
    });
    console.log(` -> THÀNH CÔNG TỆP GHÉP SỐ HỌC: ${path.basename(resSoHoc.path)} (${resSoHoc.size} bytes)`);
  } catch (err) {
    console.error(" -> LỖI ghép Số học:", err);
  }

  console.log("\n=== BẮT ĐẦU GHÉP TỆP CHUYÊN ĐỀ HÌNH HỌC 6 (7 BÀI) ===");
  const hinhHocLessons = lessons
    .filter(l => l.branch === "HinhHoc")
    .map(l => ({
      mdFilePath: path.join(tempDir, l.mdFile),
      lessonInfo: l.lessonInfo,
      illustrations: l.illustrations
    }));

  const mergedHinhHocPath = path.join(outputDir, "KHBD_Toan6_Ghep_HinhHoc_Tuan13-18.docx");
  try {
    const resHinhHoc = await createMergedKhbdDocx({
      lessons: hinhHocLessons,
      outputDocxPath: mergedHinhHocPath,
      docTitle: "KẾ HOẠCH BÀI DẠY TOÁN 6 - PHẦN HÌNH HỌC (TUẦN 13 - 18)"
    });
    console.log(` -> THÀNH CÔNG TỆP GHÉP HÌNH HỌC: ${path.basename(resHinhHoc.path)} (${resHinhHoc.size} bytes)`);
  } catch (err) {
    console.error(" -> LỖI ghép Hình học:", err);
  }

  console.log("\n=== HOÀN TẤT XUẤT TOÀN BỘ FILE DOCX TOÁN 6 (TUẦN 13 - 18)! ===");
}

runBatch().catch(console.error);
