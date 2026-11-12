/**
 * Script biên dịch và xuất hàng loạt KHBD Toán 8 (Tuần 13 - 18)
 * Thầy Hoàng Tấn Thiên - Năm học 2026 - 2027
 * Chuẩn CV 5512 V2.1 - 100% Word Equation OMML - Đầy đủ Sơ đồ tư duy Mindmap vector 300 DPI
 */

const fs = require('fs');
const path = require('path');
const { createKhbdDocx, createMergedKhbdDocx } = require('../../engine/export_khbd_engine');

const tempDir = path.resolve(__dirname);
const outputDir = path.resolve(__dirname, '../../1_SOAN_KHBD/Ket_qua/10.11/TOAN8');

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

const map26 = getMindmapDataUrl('mindmap_toan8_tiet26.png');
const map27 = getMindmapDataUrl('mindmap_toan8_tiet27.png');
const map34 = getMindmapDataUrl('mindmap_toan8_tiet34.png');
const map35 = getMindmapDataUrl('mindmap_toan8_tiet35.png');
const map37_39 = getMindmapDataUrl('mindmap_toan8_tiet37_39.png');

const mapH25 = getMindmapDataUrl('mindmap_toan8_hinh_tiet25.png');
const mapH26_27 = getMindmapDataUrl('mindmap_toan8_hinh_tiet26_27.png');
const mapH29 = getMindmapDataUrl('mindmap_toan8_hinh_tiet29.png');

const lessons = [
  // ĐẠI SỐ VÀ THỐNG KÊ (12 bài)
  {
    id: "01",
    branch: "DaiSo",
    mdFile: "01_KHBD_Toan8_Bai09_PhanTichDaThucThanhNhanTu_Tiet25.md",
    outFile: "01_KHBD_Toan8_Bai09_PhanTichDaThucThanhNhanTu_Tiet25.docx",
    illustrations: [],
    lessonInfo: {
      topic: "BÀI 9: PHÂN TÍCH ĐA THỨC THÀNH NHÂN TỬ (TIẾT 3)",
      ppct: "Tiết 25",
      lessonScope: "Tiết 25",
      duration: "01 tiết (45 phút)"
    }
  },
  {
    id: "02",
    branch: "DaiSo",
    mdFile: "02_KHBD_Toan8_LuyenTapChung_DaiSo_Tiet26.md",
    outFile: "02_KHBD_Toan8_LuyenTapChung_DaiSo_Tiet26.docx",
    illustrations: map26 ? [{
      id: "mindmap-toan8-tiet26",
      dataUrl: map26,
      width: 580,
      height: 325,
      caption: "Sơ đồ tư duy Luyện tập chung Phân tích đa thức thành nhân tử Toán 8"
    }] : [],
    lessonInfo: {
      topic: "LUYỆN TẬP CHUNG: PHÂN TÍCH ĐA THỨC THÀNH NHÂN TỬ",
      ppct: "Tiết 26",
      lessonScope: "Tiết 26",
      duration: "01 tiết (45 phút)"
    }
  },
  {
    id: "03",
    branch: "DaiSo",
    mdFile: "03_KHBD_Toan8_BaiTapCuoiChuong2_Tiet27.md",
    outFile: "03_KHBD_Toan8_BaiTapCuoiChuong2_Tiet27.docx",
    illustrations: map27 ? [{
      id: "mindmap-toan8-tiet27",
      dataUrl: map27,
      width: 580,
      height: 325,
      caption: "Sơ đồ tư duy Bài tập cuối chương II Hằng đẳng thức và Ứng dụng Toán 8"
    }] : [],
    lessonInfo: {
      topic: "BÀI TẬP CUỐI CHƯƠNG II (HẰNG ĐẲNG THỨC ĐÁNG NHỚ VÀ ỨNG DỤNG)",
      ppct: "Tiết 27",
      lessonScope: "Tiết 27",
      duration: "01 tiết (45 phút)"
    }
  },
  {
    id: "04",
    branch: "DaiSo",
    mdFile: "04_KHBD_Toan8_HDTN_TinhToanDaThuc_GeoGebra_Tiet28.md",
    outFile: "04_KHBD_Toan8_HDTN_TinhToanDaThuc_GeoGebra_Tiet28.docx",
    illustrations: [],
    lessonInfo: {
      topic: "HOẠT ĐỘNG THỰC HÀNH TRẢI NGHIỆM: THỰC HIỆN TÍNH TOÁN TRÊN ĐA THỨC VỚI PHẦN MỀM GEOGEBRA",
      ppct: "Tiết 28",
      lessonScope: "Tiết 28",
      duration: "01 tiết (45 phút)"
    }
  },
  {
    id: "05",
    branch: "DaiSo",
    mdFile: "05_KHBD_Toan8_Bai18_ThuThapPhanLoaiDuLieu_Tiet29-30.md",
    outFile: "05_KHBD_Toan8_Bai18_ThuThapPhanLoaiDuLieu_Tiet29-30.docx",
    illustrations: [],
    lessonInfo: {
      topic: "BÀI 18: THU THẬP VÀ PHÂN LOẠI DỮ LIỆU",
      ppct: "Tiết 29, 30",
      lessonScope: "Tiết 29, 30",
      duration: "02 tiết (90 phút)"
    }
  },
  {
    id: "06",
    branch: "DaiSo",
    mdFile: "06_KHBD_Toan8_Bai19_BieuDienDuLieuBangBieuDo_Tiet31-32.md",
    outFile: "06_KHBD_Toan8_Bai19_BieuDienDuLieuBangBieuDo_Tiet31-32.docx",
    illustrations: [],
    lessonInfo: {
      topic: "BÀI 19: BIỂU DIỄN DỮ LIỆU BẰNG BẢNG, BIỂU ĐỒ",
      ppct: "Tiết 31, 32",
      lessonScope: "Tiết 31, 32",
      duration: "02 tiết (90 phút)"
    }
  },
  {
    id: "07",
    branch: "DaiSo",
    mdFile: "07_KHBD_Toan8_Bai20_PhanTichSoLieuThongKe_Tiet33.md",
    outFile: "07_KHBD_Toan8_Bai20_PhanTichSoLieuThongKe_Tiet33.docx",
    illustrations: [],
    lessonInfo: {
      topic: "BÀI 20: PHÂN TÍCH SỐ LIỆU THỐNG KÊ DỰA VÀO BIỂU ĐỒ",
      ppct: "Tiết 33",
      lessonScope: "Tiết 33",
      duration: "01 tiết (45 phút)"
    }
  },
  {
    id: "08",
    branch: "DaiSo",
    mdFile: "08_KHBD_Toan8_LuyenTapChung_ThongKe_Tiet34.md",
    outFile: "08_KHBD_Toan8_LuyenTapChung_ThongKe_Tiet34.docx",
    illustrations: map34 ? [{
      id: "mindmap-toan8-tiet34",
      dataUrl: map34,
      width: 580,
      height: 325,
      caption: "Sơ đồ tư duy Luyện tập chung Thống kê Toán 8"
    }] : [],
    lessonInfo: {
      topic: "LUYỆN TẬP CHUNG: THU THẬP, BIỂU DIỄN VÀ PHÂN TÍCH DỮ LIỆU THỐNG KÊ",
      ppct: "Tiết 34",
      lessonScope: "Tiết 34",
      duration: "01 tiết (45 phút)"
    }
  },
  {
    id: "09",
    branch: "DaiSo",
    mdFile: "09_KHBD_Toan8_BaiTapCuoiChuong5_Tiet35.md",
    outFile: "09_KHBD_Toan8_BaiTapCuoiChuong5_Tiet35.docx",
    illustrations: map35 ? [{
      id: "mindmap-toan8-tiet35",
      dataUrl: map35,
      width: 580,
      height: 325,
      caption: "Sơ đồ tư duy Tổng kết Chương V Toán 8"
    }] : [],
    lessonInfo: {
      topic: "BÀI TẬP CUỐI CHƯƠNG V (DỮ LIỆU VÀ BIỂU ĐỒ THỐNG KÊ)",
      ppct: "Tiết 35",
      lessonScope: "Tiết 35",
      duration: "01 tiết (45 phút)"
    }
  },
  {
    id: "10",
    branch: "DaiSo",
    mdFile: "10_KHBD_Toan8_HDTN_PhanTichDacDiemKhiHauVN_Tiet36.md",
    outFile: "10_KHBD_Toan8_HDTN_PhanTichDacDiemKhiHauVN_Tiet36.docx",
    illustrations: [],
    lessonInfo: {
      topic: "HOẠT ĐỘNG THỰC HÀNH TRẢI NGHIỆM: PHÂN TÍCH ĐẶC ĐIỂM KHÍ HẬU VIỆT NAM",
      ppct: "Tiết 36",
      lessonScope: "Tiết 36",
      duration: "01 tiết (45 phút)"
    }
  },
  {
    id: "11",
    branch: "DaiSo",
    mdFile: "11_KHBD_Toan8_OnTapCuoiHK1_DaiSo_Tiet37-39.md",
    outFile: "11_KHBD_Toan8_OnTapCuoiHK1_DaiSo_Tiet37-39.docx",
    illustrations: map37_39 ? [{
      id: "mindmap-toan8-tiet37_39",
      dataUrl: map37_39,
      width: 580,
      height: 325,
      caption: "Sơ đồ tư duy Ôn tập Học kì I Đại số và Thống kê Toán 8"
    }] : [],
    lessonInfo: {
      topic: "ÔN TẬP HỌC KÌ I (ĐẠI SỐ VÀ THỐNG KÊ)",
      ppct: "Tiết 37, 38, 39",
      lessonScope: "Tiết 37, 38, 39",
      duration: "03 tiết (135 phút)"
    }
  },
  {
    id: "12",
    branch: "DaiSo",
    mdFile: "12_KHBD_Toan8_KiemTraTraBaiCuoiHK1_DaiSo_Tiet40-41.md",
    outFile: "12_KHBD_Toan8_KiemTraTraBaiCuoiHK1_DaiSo_Tiet40-41.docx",
    illustrations: [],
    lessonInfo: {
      topic: "KIỂM TRA ĐÁNH GIÁ CUỐI HỌC KÌ I VÀ TRẢ BÀI (ĐẠI SỐ)",
      ppct: "Tiết 40, 41",
      lessonScope: "Tiết 40, 41",
      duration: "02 tiết (90 phút)"
    }
  },

  // HÌNH HỌC (5 bài)
  {
    id: "13",
    branch: "HinhHoc",
    mdFile: "13_KHBD_Toan8_HinhHoc_LuyenTapChung_Tiet25.md",
    outFile: "13_KHBD_Toan8_HinhHoc_LuyenTapChung_Tiet25.docx",
    illustrations: mapH25 ? [{
      id: "mindmap-toan8-hinh-tiet25",
      dataUrl: mapH25,
      width: 580,
      height: 325,
      caption: "Sơ đồ tư duy Luyện tập chung Định lí Thalès Toán 8"
    }] : [],
    lessonInfo: {
      topic: "LUYỆN TẬP CHUNG: ĐỊNH LÍ THALÈS VÀ TÍNH CHẤT ĐƯỜNG PHÂN GIÁC",
      ppct: "Tiết 25",
      lessonScope: "Tiết 25",
      duration: "01 tiết (45 phút)"
    }
  },
  {
    id: "14",
    branch: "HinhHoc",
    mdFile: "14_KHBD_Toan8_HinhHoc_BaiTapCuoiChuong4_Tiet26-27.md",
    outFile: "14_KHBD_Toan8_HinhHoc_BaiTapCuoiChuong4_Tiet26-27.docx",
    illustrations: mapH26_27 ? [{
      id: "mindmap-toan8-hinh-tiet26_27",
      dataUrl: mapH26_27,
      width: 580,
      height: 325,
      caption: "Sơ đồ tư duy Bài tập cuối chương IV Hình học 8"
    }] : [],
    lessonInfo: {
      topic: "BÀI TẬP CUỐI CHƯƠNG IV (ĐỊNH LÍ THALÈS)",
      ppct: "Tiết 26, 27",
      lessonScope: "Tiết 26, 27",
      duration: "02 tiết (90 phút)"
    }
  },
  {
    id: "15",
    branch: "HinhHoc",
    mdFile: "15_KHBD_Toan8_HinhHoc_HDTN_VeHinhGeoGebra_Tiet28.md",
    outFile: "15_KHBD_Toan8_HinhHoc_HDTN_VeHinhGeoGebra_Tiet28.docx",
    illustrations: [],
    lessonInfo: {
      topic: "HOẠT ĐỘNG THỰC HÀNH TRẢI NGHIỆM: VẼ HÌNH ĐƠN GIẢN VỚI PHẦN MỀM GEOGEBRA",
      ppct: "Tiết 28",
      lessonScope: "Tiết 28",
      duration: "01 tiết (45 phút)"
    }
  },
  {
    id: "16",
    branch: "HinhHoc",
    mdFile: "16_KHBD_Toan8_HinhHoc_OnTapCuoiHK1_Tiet29.md",
    outFile: "16_KHBD_Toan8_HinhHoc_OnTapCuoiHK1_Tiet29.docx",
    illustrations: mapH29 ? [{
      id: "mindmap-toan8-hinh-tiet29",
      dataUrl: mapH29,
      width: 580,
      height: 325,
      caption: "Sơ đồ tư duy Ôn tập Học kì I Hình học 8"
    }] : [],
    lessonInfo: {
      topic: "ÔN TẬP HỌC KÌ I (HÌNH HỌC)",
      ppct: "Tiết 29",
      lessonScope: "Tiết 29",
      duration: "01 tiết (45 phút)"
    }
  },
  {
    id: "17",
    branch: "HinhHoc",
    mdFile: "17_KHBD_Toan8_HinhHoc_KiemTraTraBaiCuoiHK1_Tiet30-31.md",
    outFile: "17_KHBD_Toan8_HinhHoc_KiemTraTraBaiCuoiHK1_Tiet30-31.docx",
    illustrations: [],
    lessonInfo: {
      topic: "KIỂM TRA ĐÁNH GIÁ CUỐI HỌC KÌ I VÀ TRẢ BÀI (HÌNH HỌC)",
      ppct: "Tiết 30, 31",
      lessonScope: "Tiết 30, 31",
      duration: "02 tiết (90 phút)"
    }
  }
];

async function runBatch() {
  console.log("=== BẮT ĐẦU XUẤT 17 TỆP KHBD TOÁN 8 ĐƠN LẺ ===");

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

  console.log("\n=== BẮT ĐẦU GHÉP TỆP CHUYÊN ĐỀ ĐẠI SỐ & THỐNG KÊ 8 (12 BÀI) ===");
  const daiSoLessons = lessons
    .filter(l => l.branch === "DaiSo")
    .map(l => ({
      mdFilePath: path.join(tempDir, l.mdFile),
      lessonInfo: l.lessonInfo,
      illustrations: l.illustrations
    }));

  const mergedDaiSoPath = path.join(outputDir, "KHBD_Toan8_Ghep_DaiSo_Tuan13-18.docx");
  try {
    const resDaiSo = await createMergedKhbdDocx({
      lessons: daiSoLessons,
      outputDocxPath: mergedDaiSoPath,
      docTitle: "KẾ HOẠCH BÀI DẠY TOÁN 8 - PHẦN ĐẠI SỐ VÀ THỐNG KÊ (TUẦN 13 - 18)"
    });
    console.log(` -> THÀNH CÔNG TỆP GHÉP ĐẠI SỐ: ${path.basename(resDaiSo.path)} (${resDaiSo.size} bytes)`);
  } catch (err) {
    console.error(" -> LỖI ghép Đại số:", err);
  }

  console.log("\n=== BẮT ĐẦU GHÉP TỆP CHUYÊN ĐỀ HÌNH HỌC 8 (5 BÀI) ===");
  const hinhHocLessons = lessons
    .filter(l => l.branch === "HinhHoc")
    .map(l => ({
      mdFilePath: path.join(tempDir, l.mdFile),
      lessonInfo: l.lessonInfo,
      illustrations: l.illustrations
    }));

  const mergedHinhHocPath = path.join(outputDir, "KHBD_Toan8_Ghep_HinhHoc_Tuan13-18.docx");
  try {
    const resHinhHoc = await createMergedKhbdDocx({
      lessons: hinhHocLessons,
      outputDocxPath: mergedHinhHocPath,
      docTitle: "KẾ HOẠCH BÀI DẠY TOÁN 8 - PHẦN HÌNH HỌC (TUẦN 13 - 18)"
    });
    console.log(` -> THÀNH CÔNG TỆP GHÉP HÌNH HỌC: ${path.basename(resHinhHoc.path)} (${resHinhHoc.size} bytes)`);
  } catch (err) {
    console.error(" -> LỖI ghép Hình học:", err);
  }

  console.log("\n=== HOÀN TẤT XUẤT TOÀN BỘ FILE DOCX TOÁN 8 (TUẦN 13 - 18)! ===");
}

runBatch().catch(console.error);
