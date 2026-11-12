/**
 * Script biên dịch và xuất hàng loạt KHBD Toán 9 (Tuần 13 - 18)
 * Thầy Hoàng Tấn Thiên - Năm học 2026 - 2027
 * Chuẩn CV 5512 V2.1 - 100% Word Equation OMML - Đầy đủ Sơ đồ tư duy Mindmap vector 300 DPI
 */

const fs = require('fs');
const path = require('path');
const { createKhbdDocx, createMergedKhbdDocx } = require('../../engine/export_khbd_engine');

const tempDir = path.resolve(__dirname);
const outputDir = path.resolve(__dirname, '../../1_SOAN_KHBD/Ket_qua/10.11/TOAN9');

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

const map35 = getMindmapDataUrl('mindmap_toan9_tiet35.png');
const map36_37 = getMindmapDataUrl('mindmap_toan9_tiet36_37.png');
const map38_39 = getMindmapDataUrl('mindmap_toan9_tiet38_39.png');

const mapH23 = getMindmapDataUrl('mindmap_toan9_hinh_tiet23.png');
const mapH24_25 = getMindmapDataUrl('mindmap_toan9_hinh_tiet24_25.png');
const mapH26_27 = getMindmapDataUrl('mindmap_toan9_hinh_tiet26_27.png');

const lessons = [
  // ĐẠI SỐ (7 bài)
  {
    id: "01",
    branch: "DaiSo",
    mdFile: "01_KHBD_Toan9_Bai09_BienDoiRutGonCanThuc_Tiet32.md",
    outFile: "01_KHBD_Toan9_Bai09_BienDoiRutGonCanThuc_Tiet32.docx",
    illustrations: [],
    lessonInfo: {
      topic: "BÀI 9: BIẾN ĐỔI ĐƠN GIẢN VÀ RÚT GỌN BIỂU THỨC CHỨA CĂN THỨC BẬC HAI (TIẾT 3)",
      ppct: "Tiết 32",
      lessonScope: "Tiết 32",
      duration: "01 tiết (45 phút)"
    }
  },
  {
    id: "02",
    branch: "DaiSo",
    mdFile: "02_KHBD_Toan9_Bai10_CanBacBaVaCanThucBacBa_Tiet33-34.md",
    outFile: "02_KHBD_Toan9_Bai10_CanBacBaVaCanThucBacBa_Tiet33-34.docx",
    illustrations: [],
    lessonInfo: {
      topic: "BÀI 10: CĂN BẬC BA VÀ CĂN THỨC BẬC BA",
      ppct: "Tiết 33, 34",
      lessonScope: "Tiết 33, 34",
      duration: "02 tiết (90 phút)"
    }
  },
  {
    id: "03",
    branch: "DaiSo",
    mdFile: "03_KHBD_Toan9_LuyenTapChung_DaiSo_Tiet35.md",
    outFile: "03_KHBD_Toan9_LuyenTapChung_DaiSo_Tiet35.docx",
    illustrations: map35 ? [{
      id: "mindmap-toan9-tiet35",
      dataUrl: map35,
      width: 580,
      height: 325,
      caption: "Sơ đồ tư duy Luyện tập chung Căn bậc hai và Căn bậc ba Toán 9"
    }] : [],
    lessonInfo: {
      topic: "LUYỆN TẬP CHUNG: CĂN BẬC HAI VÀ CĂN BẬC BA",
      ppct: "Tiết 35",
      lessonScope: "Tiết 35",
      duration: "01 tiết (45 phút)"
    }
  },
  {
    id: "04",
    branch: "DaiSo",
    mdFile: "04_KHBD_Toan9_BaiTapCuoiChuong3_Tiet36-37.md",
    outFile: "04_KHBD_Toan9_BaiTapCuoiChuong3_Tiet36-37.docx",
    illustrations: map36_37 ? [{
      id: "mindmap-toan9-tiet36_37",
      dataUrl: map36_37,
      width: 580,
      height: 325,
      caption: "Sơ đồ tư duy Bài tập cuối chương III Căn bậc hai và Căn bậc ba Toán 9"
    }] : [],
    lessonInfo: {
      topic: "BÀI TẬP CUỐI CHƯƠNG III (CĂN BẬC HAI VÀ CĂN BẬC BA)",
      ppct: "Tiết 36, 37",
      lessonScope: "Tiết 36, 37",
      duration: "02 tiết (90 phút)"
    }
  },
  {
    id: "05",
    branch: "DaiSo",
    mdFile: "05_KHBD_Toan9_OnTapCuoiHK1_DaiSo_Tiet38-39.md",
    outFile: "05_KHBD_Toan9_OnTapCuoiHK1_DaiSo_Tiet38-39.docx",
    illustrations: map38_39 ? [{
      id: "mindmap-toan9-tiet38_39",
      dataUrl: map38_39,
      width: 580,
      height: 325,
      caption: "Sơ đồ tư duy Ôn tập Học kì I Đại số Toán 9"
    }] : [],
    lessonInfo: {
      topic: "ÔN TẬP CUỐI HỌC KÌ I (ĐẠI SỐ)",
      ppct: "Tiết 38, 39",
      lessonScope: "Tiết 38, 39",
      duration: "02 tiết (90 phút)"
    }
  },
  {
    id: "06",
    branch: "DaiSo",
    mdFile: "06_KHBD_Toan9_KiemTraCuoiHK1_DaiSo_Tiet40.md",
    outFile: "06_KHBD_Toan9_KiemTraCuoiHK1_DaiSo_Tiet40.docx",
    illustrations: [],
    lessonInfo: {
      topic: "KIỂM TRA ĐÁNH GIÁ CUỐI HỌC KÌ I (ĐẠI SỐ)",
      ppct: "Tiết 40",
      lessonScope: "Tiết 40",
      duration: "01 tiết (45 phút)"
    }
  },
  {
    id: "07",
    branch: "DaiSo",
    mdFile: "07_KHBD_Toan9_HDTN_PhaCheDungDich_STEM_Tiet41-42.md",
    outFile: "07_KHBD_Toan9_HDTN_PhaCheDungDich_STEM_Tiet41-42.docx",
    illustrations: [],
    lessonInfo: {
      topic: "HOẠT ĐỘNG THỰC HÀNH VÀ TRẢI NGHIỆM: PHA CHẾ DUNG DỊCH THEO NỒNG ĐỘ YÊU CẦU (KHBD STEM)",
      ppct: "Tiết 41, 42",
      lessonScope: "Tiết 41, 42",
      duration: "02 tiết (90 phút)"
    }
  },

  // HÌNH HỌC (7 bài)
  {
    id: "08",
    branch: "HinhHoc",
    mdFile: "08_KHBD_Toan9_HinhHoc_Bai16_ViTriTuongDoiDuongThangDuongTron_Tiet19-20.md",
    outFile: "08_KHBD_Toan9_HinhHoc_Bai16_ViTriTuongDoiDuongThangDuongTron_Tiet19-20.docx",
    illustrations: [],
    lessonInfo: {
      topic: "BÀI 16: VỊ TRÍ TƯƠNG ĐỐI CỦA ĐƯỜNG THẲNG VÀ ĐƯỜNG TRÒN",
      ppct: "Tiết 19, 20",
      lessonScope: "Tiết 19, 20",
      duration: "02 tiết (90 phút)"
    }
  },
  {
    id: "09",
    branch: "HinhHoc",
    mdFile: "09_KHBD_Toan9_HinhHoc_Bai17_ViTriTuongDoiHaiDuongTron_Tiet21-22.md",
    outFile: "09_KHBD_Toan9_HinhHoc_Bai17_ViTriTuongDoiHaiDuongTron_Tiet21-22.docx",
    illustrations: [],
    lessonInfo: {
      topic: "BÀI 17: VỊ TRÍ TƯƠNG ĐỐI CỦA HAI ĐƯỜNG TRÒN",
      ppct: "Tiết 21, 22",
      lessonScope: "Tiết 21, 22",
      duration: "02 tiết (90 phút)"
    }
  },
  {
    id: "10",
    branch: "HinhHoc",
    mdFile: "10_KHBD_Toan9_HinhHoc_LuyenTapChung_Tiet23.md",
    outFile: "10_KHBD_Toan9_HinhHoc_LuyenTapChung_Tiet23.docx",
    illustrations: mapH23 ? [{
      id: "mindmap-toan9-hinh-tiet23",
      dataUrl: mapH23,
      width: 580,
      height: 325,
      caption: "Sơ đồ tư duy Luyện tập chung Vị trí tương đối đường thẳng và đường tròn Toán 9"
    }] : [],
    lessonInfo: {
      topic: "LUYỆN TẬP CHUNG: VỊ TRÍ TƯƠNG ĐỐI CỦA ĐƯỜNG THẲNG VÀ ĐƯỜNG TRÒN",
      ppct: "Tiết 23",
      lessonScope: "Tiết 23",
      duration: "01 tiết (45 phút)"
    }
  },
  {
    id: "11",
    branch: "HinhHoc",
    mdFile: "11_KHBD_Toan9_HinhHoc_BaiTapCuoiChuong5_Tiet24-25.md",
    outFile: "11_KHBD_Toan9_HinhHoc_BaiTapCuoiChuong5_Tiet24-25.docx",
    illustrations: mapH24_25 ? [{
      id: "mindmap-toan9-hinh-tiet24_25",
      dataUrl: mapH24_25,
      width: 580,
      height: 325,
      caption: "Sơ đồ tư duy Bài tập cuối chương V Đường tròn Toán 9"
    }] : [],
    lessonInfo: {
      topic: "BÀI TẬP CUỐI CHƯƠNG V (ĐƯỜNG TRÒN)",
      ppct: "Tiết 24, 25",
      lessonScope: "Tiết 24, 25",
      duration: "02 tiết (90 phút)"
    }
  },
  {
    id: "12",
    branch: "HinhHoc",
    mdFile: "12_KHBD_Toan9_HinhHoc_OnTapCuoiHK1_Tiet26-27.md",
    outFile: "12_KHBD_Toan9_HinhHoc_OnTapCuoiHK1_Tiet26-27.docx",
    illustrations: mapH26_27 ? [{
      id: "mindmap-toan9-hinh-tiet26_27",
      dataUrl: mapH26_27,
      width: 580,
      height: 325,
      caption: "Sơ đồ tư duy Ôn tập Học kì I Hình học Toán 9"
    }] : [],
    lessonInfo: {
      topic: "ÔN TẬP CUỐI HỌC KÌ I (HÌNH HỌC)",
      ppct: "Tiết 26, 27",
      lessonScope: "Tiết 26, 27",
      duration: "02 tiết (90 phút)"
    }
  },
  {
    id: "13",
    branch: "HinhHoc",
    mdFile: "13_KHBD_Toan9_HinhHoc_KiemTraCuoiHK1_Tiet28.md",
    outFile: "13_KHBD_Toan9_HinhHoc_KiemTraCuoiHK1_Tiet28.docx",
    illustrations: [],
    lessonInfo: {
      topic: "KIỂM TRA ĐÁNH GIÁ CUỐI HỌC KÌ I (HÌNH HỌC)",
      ppct: "Tiết 28",
      lessonScope: "Tiết 28",
      duration: "01 tiết (45 phút)"
    }
  },
  {
    id: "14",
    branch: "HinhHoc",
    mdFile: "14_KHBD_Toan9_HinhHoc_HDTN_TinhChieuCaoKhoangCach_STEM_Tiet29-30.md",
    outFile: "14_KHBD_Toan9_HinhHoc_HDTN_TinhChieuCaoKhoangCach_STEM_Tiet29-30.docx",
    illustrations: [],
    lessonInfo: {
      topic: "HOẠT ĐỘNG THỰC HÀNH VÀ TRẢI NGHIỆM: TÍNH CHIỀU CAO VÀ XÁC ĐỊNH KHOẢNG CÁCH (KHBD STEM)",
      ppct: "Tiết 29, 30",
      lessonScope: "Tiết 29, 30",
      duration: "02 tiết (90 phút)"
    }
  }
];

async function runBatch() {
  console.log("=== BẮT ĐẦU XUẤT 14 TỆP KHBD TOÁN 9 ĐƠN LẺ ===");

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

  console.log("\n=== BẮT ĐẦU GHÉP TỆP CHUYÊN ĐỀ ĐẠI SỐ 9 (7 BÀI) ===");
  const daiSoLessons = lessons
    .filter(l => l.branch === "DaiSo")
    .map(l => ({
      mdFilePath: path.join(tempDir, l.mdFile),
      lessonInfo: l.lessonInfo,
      illustrations: l.illustrations
    }));

  const mergedDaiSoPath = path.join(outputDir, "KHBD_Toan9_Ghep_DaiSo_Tuan13-18.docx");
  try {
    const resDaiSo = await createMergedKhbdDocx({
      lessons: daiSoLessons,
      outputDocxPath: mergedDaiSoPath,
      docTitle: "KẾ HOẠCH BÀI DẠY TOÁN 9 - PHẦN ĐẠI SỐ (TUẦN 13 - 18)"
    });
    console.log(` -> THÀNH CÔNG TỆP GHÉP ĐẠI SỐ: ${path.basename(resDaiSo.path)} (${resDaiSo.size} bytes)`);
  } catch (err) {
    console.error(" -> LỖI ghép Đại số:", err);
  }

  console.log("\n=== BẮT ĐẦU GHÉP TỆP CHUYÊN ĐỀ HÌNH HỌC 9 (7 BÀI) ===");
  const hinhHocLessons = lessons
    .filter(l => l.branch === "HinhHoc")
    .map(l => ({
      mdFilePath: path.join(tempDir, l.mdFile),
      lessonInfo: l.lessonInfo,
      illustrations: l.illustrations
    }));

  const mergedHinhHocPath = path.join(outputDir, "KHBD_Toan9_Ghep_HinhHoc_Tuan13-18.docx");
  try {
    const resHinhHoc = await createMergedKhbdDocx({
      lessons: hinhHocLessons,
      outputDocxPath: mergedHinhHocPath,
      docTitle: "KẾ HOẠCH BÀI DẠY TOÁN 9 - PHẦN HÌNH HỌC (TUẦN 13 - 18)"
    });
    console.log(` -> THÀNH CÔNG TỆP GHÉP HÌNH HỌC: ${path.basename(resHinhHoc.path)} (${resHinhHoc.size} bytes)`);
  } catch (err) {
    console.error(" -> LỖI ghép Hình học:", err);
  }

  console.log("\n=== HOÀN TẤT XUẤT TOÀN BỘ FILE DOCX TOÁN 9 (TUẦN 13 - 18)! ===");
}

runBatch().catch(console.error);
