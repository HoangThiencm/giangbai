/**
 * Script biên dịch và xuất hàng loạt KHBD Toán 6 Học kì II (Tuần 19 - 35)
 * Thầy Hoàng Tấn Thiên - Năm học 2026 - 2027
 * Chuẩn CV 5512 V2.1 - 100% Word Equation OMML - Đầy đủ 14 Sơ đồ tư duy Mindmap vector 300 DPI
 */

const fs = require('fs');
const path = require('path');
const { createKhbdDocx, createMergedKhbdDocx } = require('../../engine/export_khbd_engine');

const tempDir = path.resolve(__dirname);
const outputDir = path.resolve(__dirname, '../../1_SOAN_KHBD/Ket_qua/HK2/TOAN6');

if (!fs.existsSync(outputDir)) {
  fs.mkdirSync(outputDir, { recursive: true });
}

function getMindmapIllustration(illId, filename, caption) {
  const imgPath = path.join(tempDir, 'mindmaps', filename);
  if (fs.existsSync(imgPath)) {
    const b64 = fs.readFileSync(imgPath).toString('base64');
    return [{
      id: illId,
      dataUrl: `data:image/png;base64,${b64}`,
      width: 580,
      height: 320,
      caption: caption
    }];
  }
  return [];
}

const lessons = [
  // --- CHƯƠNG VI: PHÂN SỐ (TIẾT 51 - 65) ---
  {
    id: "01",
    mdFile: "01_KHBD_Toan6_Bai23_MoRongPhanSo_Tiet51-52.md",
    outFile: "01_KHBD_Toan6_Bai23_MoRongPhanSo_Tiet51-52.docx",
    group: "so_hoc",
    illustrations: [],
    lessonInfo: {
      topic: "BÀI 23: MỞ RỘNG PHÂN SỐ. PHÂN SỐ BẰNG NHAU",
      ppct: "Tiết 51, 52",
      lessonScope: "Tiết 51, 52",
      duration: "02 tiết (90 phút)"
    }
  },
  {
    id: "02",
    mdFile: "02_KHBD_Toan6_Bai24_SoSanhPhanSo_HonSoDuong_Tiet53-54.md",
    outFile: "02_KHBD_Toan6_Bai24_SoSanhPhanSo_HonSoDuong_Tiet53-54.docx",
    group: "so_hoc",
    illustrations: [],
    lessonInfo: {
      topic: "BÀI 24: SO SÁNH PHÂN SỐ. HỖN SỐ DƯƠNG",
      ppct: "Tiết 53, 54",
      lessonScope: "Tiết 53, 54",
      duration: "02 tiết (90 phút)"
    }
  },
  {
    id: "03",
    mdFile: "03_KHBD_Toan6_LuyenTapChung_Tiet55.md",
    outFile: "03_KHBD_Toan6_LuyenTapChung_Tiet55.docx",
    group: "so_hoc",
    illustrations: getMindmapIllustration('mindmap-toan6-tiet55', 'mindmap_toan6_tiet55.png', 'Sơ đồ tư duy Luyện tập chung Tiết 55'),
    lessonInfo: {
      topic: "LUYỆN TẬP CHUNG (TRANG 13)",
      ppct: "Tiết 55",
      lessonScope: "Tiết 55",
      duration: "01 tiết (45 phút)"
    }
  },
  {
    id: "04",
    mdFile: "04_KHBD_Toan6_Bai25_PhepCongVaPhepTruPhanSo_Tiet56-57.md",
    outFile: "04_KHBD_Toan6_Bai25_PhepCongVaPhepTruPhanSo_Tiet56-57.docx",
    group: "so_hoc",
    illustrations: [],
    lessonInfo: {
      topic: "BÀI 25: PHÉP CỘNG VÀ PHÉP TRỪ PHÂN SỐ",
      ppct: "Tiết 56, 57",
      lessonScope: "Tiết 56, 57",
      duration: "02 tiết (90 phút)"
    }
  },
  {
    id: "05",
    mdFile: "05_KHBD_Toan6_Bai26_PhepNhanVaPhepChiaPhanSo_Tiet58-59.md",
    outFile: "05_KHBD_Toan6_Bai26_PhepNhanVaPhepChiaPhanSo_Tiet58-59.docx",
    group: "so_hoc",
    illustrations: [],
    lessonInfo: {
      topic: "BÀI 26: PHÉP NHÂN VÀ PHÉP CHIA PHÂN SỐ",
      ppct: "Tiết 58, 59",
      lessonScope: "Tiết 58, 59",
      duration: "02 tiết (90 phút)"
    }
  },
  {
    id: "06",
    mdFile: "06_KHBD_Toan6_Bai27_HaiBaiToanVePhanSo_Tiet60-61.md",
    outFile: "06_KHBD_Toan6_Bai27_HaiBaiToanVePhanSo_Tiet60-61.docx",
    group: "so_hoc",
    illustrations: [],
    lessonInfo: {
      topic: "BÀI 27: HAI BÀI TOÁN VỀ PHÂN SỐ",
      ppct: "Tiết 60, 61",
      lessonScope: "Tiết 60, 61",
      duration: "02 tiết (90 phút)"
    }
  },
  {
    id: "07",
    mdFile: "07_KHBD_Toan6_LuyenTapChung_Tiet62-63.md",
    outFile: "07_KHBD_Toan6_LuyenTapChung_Tiet62-63.docx",
    group: "so_hoc",
    illustrations: getMindmapIllustration('mindmap-toan6-tiet62-63', 'mindmap_toan6_tiet62_63.png', 'Sơ đồ tư duy Luyện tập chung Tiết 62, 63'),
    lessonInfo: {
      topic: "LUYỆN TẬP CHUNG (TRANG 21)",
      ppct: "Tiết 62, 63",
      lessonScope: "Tiết 62, 63",
      duration: "02 tiết (90 phút)"
    }
  },
  {
    id: "08",
    mdFile: "08_KHBD_Toan6_BaiTapCuoiChuong6_Tiet64-65.md",
    outFile: "08_KHBD_Toan6_BaiTapCuoiChuong6_Tiet64-65.docx",
    group: "so_hoc",
    illustrations: getMindmapIllustration('mindmap-toan6-tiet64-65', 'mindmap_toan6_tiet64_65.png', 'Sơ đồ tư duy Bài tập cuối chương VI Tiết 64, 65'),
    lessonInfo: {
      topic: "BÀI TẬP CUỐI CHƯƠNG VI (TRANG 24)",
      ppct: "Tiết 64, 65",
      lessonScope: "Tiết 64, 65",
      duration: "02 tiết (90 phút)"
    }
  },

  // --- CHƯƠNG VII: SỐ THẬP PHÂN (TIẾT 66 - 80) ---
  {
    id: "09",
    mdFile: "09_KHBD_Toan6_Bai28_SoThapPhan_Tiet66-67.md",
    outFile: "09_KHBD_Toan6_Bai28_SoThapPhan_Tiet66-67.docx",
    group: "so_hoc",
    illustrations: [],
    lessonInfo: {
      topic: "BÀI 28: SỐ THẬP PHÂN",
      ppct: "Tiết 66, 67",
      lessonScope: "Tiết 66, 67",
      duration: "02 tiết (90 phút)"
    }
  },
  {
    id: "10",
    mdFile: "10_KHBD_Toan6_Bai29_TinhToanVoiSoThapPhan_Tiet68-69.md",
    outFile: "10_KHBD_Toan6_Bai29_TinhToanVoiSoThapPhan_Tiet68-69.docx",
    group: "so_hoc",
    illustrations: [],
    lessonInfo: {
      topic: "BÀI 29: TÍNH TOÁN VỚI SỐ THẬP PHÂN",
      ppct: "Tiết 68, 69",
      lessonScope: "Tiết 68, 69",
      duration: "02 tiết (90 phút)"
    }
  },
  {
    id: "11",
    mdFile: "11_KHBD_Toan6_Bai30_LamTronVaUocLuong_Tiet70.md",
    outFile: "11_KHBD_Toan6_Bai30_LamTronVaUocLuong_Tiet70.docx",
    group: "so_hoc",
    illustrations: [],
    lessonInfo: {
      topic: "BÀI 30: LÀM TRÒN VÀ ƯỚC LƯỢNG",
      ppct: "Tiết 70",
      lessonScope: "Tiết 70",
      duration: "01 tiết (45 phút)"
    }
  },
  {
    id: "12",
    mdFile: "12_KHBD_Toan6_OnTapGiuaHK2_Tiet71-72.md",
    outFile: "12_KHBD_Toan6_OnTapGiuaHK2_Tiet71-72.docx",
    group: "so_hoc",
    illustrations: getMindmapIllustration('mindmap-toan6-tiet71-72', 'mindmap_toan6_tiet71_72.png', 'Sơ đồ tư duy Ôn tập giữa HK2 Tiết 71, 72'),
    lessonInfo: {
      topic: "ÔN TẬP GIỮA HỌC KÌ II (SỐ HỌC)",
      ppct: "Tiết 71, 72",
      lessonScope: "Tiết 71, 72",
      duration: "02 tiết (90 phút)"
    }
  },
  {
    id: "13",
    mdFile: "13_KHBD_Toan6_KiemTraGiuaHK2_Tiet73.md",
    outFile: "13_KHBD_Toan6_KiemTraGiuaHK2_Tiet73.docx",
    group: "so_hoc",
    illustrations: [],
    lessonInfo: {
      topic: "KIỂM TRA ĐÁNH GIÁ GIỮA HỌC KÌ II (SỐ HỌC)",
      ppct: "Tiết 73",
      lessonScope: "Tiết 73",
      duration: "01 tiết (45 phút)"
    }
  },
  {
    id: "14",
    mdFile: "14_KHBD_Toan6_Bai31_MotSoBaiToanVeTiSoVaTiSoPhanTram_Tiet74-76.md",
    outFile: "14_KHBD_Toan6_Bai31_MotSoBaiToanVeTiSoVaTiSoPhanTram_Tiet74-76.docx",
    group: "so_hoc",
    illustrations: [],
    lessonInfo: {
      topic: "BÀI 31: MỘT SỐ BÀI TOÁN VỀ TỈ SỐ VÀ TỈ SỐ PHẦN TRĂM",
      ppct: "Tiết 74, 75, 76",
      lessonScope: "Tiết 74, 75, 76",
      duration: "03 tiết (135 phút)"
    }
  },
  {
    id: "15",
    mdFile: "15_KHBD_Toan6_LuyenTapChung_Tiet77-78.md",
    outFile: "15_KHBD_Toan6_LuyenTapChung_Tiet77-78.docx",
    group: "so_hoc",
    illustrations: getMindmapIllustration('mindmap-toan6-tiet77-78', 'mindmap_toan6_tiet77_78.png', 'Sơ đồ tư duy Luyện tập chung Tiết 77, 78'),
    lessonInfo: {
      topic: "LUYỆN TẬP CHUNG (TRANG 41)",
      ppct: "Tiết 77, 78",
      lessonScope: "Tiết 77, 78",
      duration: "02 tiết (90 phút)"
    }
  },
  {
    id: "16",
    mdFile: "16_KHBD_Toan6_BaiTapCuoiChuong7_Tiet79-80.md",
    outFile: "16_KHBD_Toan6_BaiTapCuoiChuong7_Tiet79-80.docx",
    group: "so_hoc",
    illustrations: getMindmapIllustration('mindmap-toan6-tiet79-80', 'mindmap_toan6_tiet79_80.png', 'Sơ đồ tư duy Bài tập cuối chương VII Tiết 79, 80'),
    lessonInfo: {
      topic: "BÀI TẬP CUỐI CHƯƠNG VII (TRANG 43)",
      ppct: "Tiết 79, 80",
      lessonScope: "Tiết 79, 80",
      duration: "02 tiết (90 phút)"
    }
  },

  // --- CHƯƠNG VIII: HÌNH HỌC CƠ BẢN (TIẾT 23 - 39) ---
  {
    id: "17",
    mdFile: "17_KHBD_Toan6_Bai32_DiemVaDuongThang_Tiet23-24.md",
    outFile: "17_KHBD_Toan6_Bai32_DiemVaDuongThang_Tiet23-24.docx",
    group: "hinh_hoc",
    illustrations: [],
    lessonInfo: {
      topic: "BÀI 32: ĐIỂM VÀ ĐƯỜNG THẲNG",
      ppct: "Tiết 23, 24",
      lessonScope: "Tiết 23, 24",
      duration: "02 tiết (90 phút)"
    }
  },
  {
    id: "18",
    mdFile: "18_KHBD_Toan6_Bai33_DiemNamGiuaHaiDiem_Tia_Tiet25.md",
    outFile: "18_KHBD_Toan6_Bai33_DiemNamGiuaHaiDiem_Tia_Tiet25.docx",
    group: "hinh_hoc",
    illustrations: [],
    lessonInfo: {
      topic: "BÀI 33: ĐIỂM NẰM GIỮA HAI ĐIỂM. TIA",
      ppct: "Tiết 25",
      lessonScope: "Tiết 25",
      duration: "01 tiết (45 phút)"
    }
  },
  {
    id: "19",
    mdFile: "19_KHBD_Toan6_Bai34_DoanThang_DoDaiDoanThang_Tiet26-27.md",
    outFile: "19_KHBD_Toan6_Bai34_DoanThang_DoDaiDoanThang_Tiet26-27.docx",
    group: "hinh_hoc",
    illustrations: [],
    lessonInfo: {
      topic: "BÀI 34: ĐOẠN THẲNG. ĐỘ DÀI ĐOẠN THẲNG",
      ppct: "Tiết 26, 27",
      lessonScope: "Tiết 26, 27",
      duration: "02 tiết (90 phút)"
    }
  },
  {
    id: "20",
    mdFile: "20_KHBD_Toan6_Bai35_TrungDiemCuaDoanThang_Tiet28.md",
    outFile: "20_KHBD_Toan6_Bai35_TrungDiemCuaDoanThang_Tiet28.docx",
    group: "hinh_hoc",
    illustrations: [],
    lessonInfo: {
      topic: "BÀI 35: TRUNG ĐIỂM CỦA ĐOẠN THẲNG (TÍCH HỢP AI)",
      ppct: "Tiết 28",
      lessonScope: "Tiết 28",
      duration: "01 tiết (45 phút)"
    }
  },
  {
    id: "21",
    mdFile: "21_KHBD_Toan6_LuyenTapChung_HinhHoc_Tiet29.md",
    outFile: "21_KHBD_Toan6_LuyenTapChung_HinhHoc_Tiet29.docx",
    group: "hinh_hoc",
    illustrations: getMindmapIllustration('mindmap-toan6-hinh-tiet29', 'mindmap_toan6_hinh_tiet29.png', 'Sơ đồ tư duy Luyện tập chung Hình học Tiết 29'),
    lessonInfo: {
      topic: "LUYỆN TẬP CHUNG (TRANG 58)",
      ppct: "Tiết 29",
      lessonScope: "Tiết 29",
      duration: "01 tiết (45 phút)"
    }
  },
  {
    id: "22",
    mdFile: "22_KHBD_Toan6_KiemTraGiuaHK2_HinhHoc_Tiet30.md",
    outFile: "22_KHBD_Toan6_KiemTraGiuaHK2_HinhHoc_Tiet30.docx",
    group: "hinh_hoc",
    illustrations: [],
    lessonInfo: {
      topic: "KIỂM TRA ĐÁNH GIÁ GIỮA HỌC KÌ II (HÌNH HỌC)",
      ppct: "Tiết 30",
      lessonScope: "Tiết 30",
      duration: "01 tiết (45 phút)"
    }
  },
  {
    id: "23",
    mdFile: "23_KHBD_Toan6_Bai36_Goc_Tiet31.md",
    outFile: "23_KHBD_Toan6_Bai36_Goc_Tiet31.docx",
    group: "hinh_hoc",
    illustrations: [],
    lessonInfo: {
      topic: "BÀI 36: GÓC",
      ppct: "Tiết 31",
      lessonScope: "Tiết 31",
      duration: "01 tiết (45 phút)"
    }
  },
  {
    id: "24",
    mdFile: "24_KHBD_Toan6_Bai37_SoDoGoc_Tiet32-33.md",
    outFile: "24_KHBD_Toan6_Bai37_SoDoGoc_Tiet32-33.docx",
    group: "hinh_hoc",
    illustrations: [],
    lessonInfo: {
      topic: "BÀI 37: SỐ ĐO GÓC",
      ppct: "Tiết 32, 33",
      lessonScope: "Tiết 32, 33",
      duration: "02 tiết (90 phút)"
    }
  },
  {
    id: "25",
    mdFile: "25_KHBD_Toan6_LuyenTapChung_HinhHoc_Tiet34.md",
    outFile: "25_KHBD_Toan6_LuyenTapChung_HinhHoc_Tiet34.docx",
    group: "hinh_hoc",
    illustrations: getMindmapIllustration('mindmap-toan6-hinh-tiet34', 'mindmap_toan6_hinh_tiet34.png', 'Sơ đồ tư duy Luyện tập chung Hình học Tiết 34'),
    lessonInfo: {
      topic: "LUYỆN TẬP CHUNG (TRANG 67)",
      ppct: "Tiết 34",
      lessonScope: "Tiết 34",
      duration: "01 tiết (45 phút)"
    }
  },
  {
    id: "26",
    mdFile: "26_KHBD_Toan6_BaiTapCuoiChuong8_Tiet35.md",
    outFile: "26_KHBD_Toan6_BaiTapCuoiChuong8_Tiet35.docx",
    group: "hinh_hoc",
    illustrations: getMindmapIllustration('mindmap-toan6-hinh-tiet35', 'mindmap_toan6_hinh_tiet35.png', 'Sơ đồ tư duy Bài tập cuối chương VIII Tiết 35'),
    lessonInfo: {
      topic: "BÀI TẬP CUỐI CHƯƠNG VIII (TRANG 69)",
      ppct: "Tiết 35",
      lessonScope: "Tiết 35",
      duration: "01 tiết (45 phút)"
    }
  },
  {
    id: "27",
    mdFile: "27_KHBD_Toan6_HDTN_GeoGebra1_Tiet36.md",
    outFile: "27_KHBD_Toan6_HDTN_GeoGebra1_Tiet36.docx",
    group: "hinh_hoc",
    illustrations: [],
    lessonInfo: {
      topic: "HĐTN: VẼ HÌNH ĐƠN GIẢN VỚI PHẦN MỀM GEOGEBRA (TIẾT 1)",
      ppct: "Tiết 36",
      lessonScope: "Tiết 36",
      duration: "01 tiết (45 phút)"
    }
  },
  {
    id: "28",
    mdFile: "28_KHBD_Toan6_OnTapCuoiHK2_HinhHoc_Tiet37.md",
    outFile: "28_KHBD_Toan6_OnTapCuoiHK2_HinhHoc_Tiet37.docx",
    group: "hinh_hoc",
    illustrations: getMindmapIllustration('mindmap-toan6-hinh-tiet37', 'mindmap_toan6_hinh_tiet37.png', 'Sơ đồ tư duy Ôn tập cuối HK2 Hình học Tiết 37'),
    lessonInfo: {
      topic: "ÔN TẬP CUỐI HỌC KÌ II (HÌNH HỌC)",
      ppct: "Tiết 37",
      lessonScope: "Tiết 37",
      duration: "01 tiết (45 phút)"
    }
  },
  {
    id: "29",
    mdFile: "29_KHBD_Toan6_KiemTraCuoiHK2_HinhHoc_Tiet38.md",
    outFile: "29_KHBD_Toan6_KiemTraCuoiHK2_HinhHoc_Tiet38.docx",
    group: "hinh_hoc",
    illustrations: [],
    lessonInfo: {
      topic: "KIỂM TRA ĐÁNH GIÁ CUỐI HỌC KÌ II (HÌNH HỌC)",
      ppct: "Tiết 38",
      lessonScope: "Tiết 38",
      duration: "01 tiết (45 phút)"
    }
  },
  {
    id: "30",
    mdFile: "30_KHBD_Toan6_HDTN_GeoGebra2_Tiet39.md",
    outFile: "30_KHBD_Toan6_HDTN_GeoGebra2_Tiet39.docx",
    group: "hinh_hoc",
    illustrations: [],
    lessonInfo: {
      topic: "HĐTN: VẼ HÌNH ĐƠN GIẢN VỚI PHẦN MỀM GEOGEBRA (TIẾT 2)",
      ppct: "Tiết 39",
      lessonScope: "Tiết 39",
      duration: "01 tiết (45 phút)"
    }
  },

  // --- CHƯƠNG IX: DỮ LIỆU & XÁC SUẤT THỰC NGHIỆM (TIẾT 81 - 101) ---
  {
    id: "31",
    mdFile: "31_KHBD_Toan6_Bai38_DuLieuVaThuThapDuLieu_Tiet81-82.md",
    outFile: "31_KHBD_Toan6_Bai38_DuLieuVaThuThapDuLieu_Tiet81-82.docx",
    group: "so_hoc",
    illustrations: [],
    lessonInfo: {
      topic: "BÀI 38: DỮ LIỆU VÀ THU THẬP DỮ LIỆU",
      ppct: "Tiết 81, 82",
      lessonScope: "Tiết 81, 82",
      duration: "02 tiết (90 phút)"
    }
  },
  {
    id: "32",
    mdFile: "32_KHBD_Toan6_Bai39_BangThongKeVaBieuDoTranh_Tiet83-84.md",
    outFile: "32_KHBD_Toan6_Bai39_BangThongKeVaBieuDoTranh_Tiet83-84.docx",
    group: "so_hoc",
    illustrations: [],
    lessonInfo: {
      topic: "BÀI 39: BẢNG THỐNG KÊ VÀ BIỂU ĐỒ TRANH",
      ppct: "Tiết 83, 84",
      lessonScope: "Tiết 83, 84",
      duration: "02 tiết (90 phút)"
    }
  },
  {
    id: "33",
    mdFile: "33_KHBD_Toan6_Bai40_BieuDoCot_Tiet85-86.md",
    outFile: "33_KHBD_Toan6_Bai40_BieuDoCot_Tiet85-86.docx",
    group: "so_hoc",
    illustrations: [],
    lessonInfo: {
      topic: "BÀI 40: BIỂU ĐỒ CỘT",
      ppct: "Tiết 85, 86",
      lessonScope: "Tiết 85, 86",
      duration: "02 tiết (90 phút)"
    }
  },
  {
    id: "34",
    mdFile: "34_KHBD_Toan6_Bai41_BieuDoCotKep_Tiet87-88.md",
    outFile: "34_KHBD_Toan6_Bai41_BieuDoCotKep_Tiet87-88.docx",
    group: "so_hoc",
    illustrations: [],
    lessonInfo: {
      topic: "BÀI 41: BIỂU ĐỒ CỘT KÉP",
      ppct: "Tiết 87, 88",
      lessonScope: "Tiết 87, 88",
      duration: "02 tiết (90 phút)"
    }
  },
  {
    id: "35",
    mdFile: "35_KHBD_Toan6_LuyenTapChung_Tiet89.md",
    outFile: "35_KHBD_Toan6_LuyenTapChung_Tiet89.docx",
    group: "so_hoc",
    illustrations: getMindmapIllustration('mindmap-toan6-tiet89', 'mindmap_toan6_tiet89.png', 'Sơ đồ tư duy Luyện tập chung Tiết 89'),
    lessonInfo: {
      topic: "LUYỆN TẬP CHUNG: EM SẼ LÀM GÌ TRONG TƯƠNG LAI? (TRANG 91)",
      ppct: "Tiết 89",
      lessonScope: "Tiết 89",
      duration: "01 tiết (45 phút)"
    }
  },
  {
    id: "36",
    mdFile: "36_KHBD_Toan6_Bai42_KetQuaCoTheVaSuKien_Tiet90.md",
    outFile: "36_KHBD_Toan6_Bai42_KetQuaCoTheVaSuKien_Tiet90.docx",
    group: "so_hoc",
    illustrations: [],
    lessonInfo: {
      topic: "BÀI 42: KẾT QUẢ CÓ THỂ VÀ SỰ KIỆN TRONG TRÒ CHƠI, THÍ NGHIỆM",
      ppct: "Tiết 90",
      lessonScope: "Tiết 90",
      duration: "01 tiết (45 phút)"
    }
  },
  {
    id: "37",
    mdFile: "37_KHBD_Toan6_Bai43_XacSuatThucNghiem_Tiet91.md",
    outFile: "37_KHBD_Toan6_Bai43_XacSuatThucNghiem_Tiet91.docx",
    group: "so_hoc",
    illustrations: [],
    lessonInfo: {
      topic: "BÀI 43: XÁC SUẤT THỰC NGHIỆM",
      ppct: "Tiết 91",
      lessonScope: "Tiết 91",
      duration: "01 tiết (45 phút)"
    }
  },
  {
    id: "38",
    mdFile: "38_KHBD_Toan6_LuyenTapChung_Tiet92.md",
    outFile: "38_KHBD_Toan6_LuyenTapChung_Tiet92.docx",
    group: "so_hoc",
    illustrations: getMindmapIllustration('mindmap-toan6-tiet92', 'mindmap_toan6_tiet92.png', 'Sơ đồ tư duy Luyện tập chung Xác suất Tiết 92'),
    lessonInfo: {
      topic: "LUYỆN TẬP CHUNG: XÁC SUẤT THỰC NGHIỆM (TRANG 97)",
      ppct: "Tiết 92",
      lessonScope: "Tiết 92",
      duration: "01 tiết (45 phút)"
    }
  },
  {
    id: "39",
    mdFile: "39_KHBD_Toan6_OnTapCuoiHK2_SoHocThongKe_Tiet93-97.md",
    outFile: "39_KHBD_Toan6_OnTapCuoiHK2_SoHocThongKe_Tiet93-97.docx",
    group: "so_hoc",
    illustrations: getMindmapIllustration('mindmap-toan6-tiet93-97', 'mindmap_toan6_tiet93_97.png', 'Sơ đồ tư duy Ôn tập cuối HK2 Tiết 93-97'),
    lessonInfo: {
      topic: "ÔN TẬP ĐÁNH GIÁ CUỐI HỌC KÌ II (SỐ HỌC VÀ THỐNG KÊ)",
      ppct: "Tiết 93, 94, 95, 96, 97",
      lessonScope: "Tiết 93 - 97",
      duration: "05 tiết (225 phút)"
    }
  },
  {
    id: "40",
    mdFile: "40_KHBD_Toan6_KiemTraCuoiHK2_SoHocThongKe_Tiet98.md",
    outFile: "40_KHBD_Toan6_KiemTraCuoiHK2_SoHocThongKe_Tiet98.docx",
    group: "so_hoc",
    illustrations: [],
    lessonInfo: {
      topic: "KIỂM TRA ĐÁNH GIÁ CUỐI HỌC KÌ II (SỐ HỌC VÀ THỐNG KÊ)",
      ppct: "Tiết 98",
      lessonScope: "Tiết 98",
      duration: "01 tiết (45 phút)"
    }
  },
  {
    id: "41",
    mdFile: "41_KHBD_Toan6_BaiTapCuoiChuong9_Tiet99.md",
    outFile: "41_KHBD_Toan6_BaiTapCuoiChuong9_Tiet99.docx",
    group: "so_hoc",
    illustrations: getMindmapIllustration('mindmap-toan6-tiet99', 'mindmap_toan6_tiet99.png', 'Sơ đồ tư duy Bài tập cuối chương IX Tiết 99'),
    lessonInfo: {
      topic: "BÀI TẬP CUỐI CHƯƠNG IX (TRANG 99)",
      ppct: "Tiết 99",
      lessonScope: "Tiết 99",
      duration: "01 tiết (45 phút)"
    }
  },
  {
    id: "42",
    mdFile: "42_KHBD_Toan6_HDTN_KeHoachChiTieu_Tiet100.md",
    outFile: "42_KHBD_Toan6_HDTN_KeHoachChiTieu_Tiet100.docx",
    group: "so_hoc",
    illustrations: [],
    lessonInfo: {
      topic: "HĐTN: KẾ HOẠCH CHI TIÊU CÁ NHÂN VÀ GIA ĐÌNH",
      ppct: "Tiết 100",
      lessonScope: "Tiết 100",
      duration: "01 tiết (45 phút)"
    }
  },
  {
    id: "43",
    mdFile: "43_KHBD_Toan6_HDTN_MonTheThaoYeuThich_Tiet101.md",
    outFile: "43_KHBD_Toan6_HDTN_MonTheThaoYeuThich_Tiet101.docx",
    group: "so_hoc",
    illustrations: [],
    lessonInfo: {
      topic: "HĐTN: HOẠT ĐỘNG THỂ THAO NÀO ĐƯỢC YÊU THÍCH NHẤT TRONG HÈ",
      ppct: "Tiết 101",
      lessonScope: "Tiết 101",
      duration: "01 tiết (45 phút)"
    }
  }
];

async function runBatch() {
  console.log("=== BẮT ĐẦU XUẤT 43 KHBD TOÁN 6 HỌC KÌ II (TUẦN 19 - 35) ===");

  for (let i = 0; i < lessons.length; i++) {
    const item = lessons[i];
    const mdPath = path.join(tempDir, item.mdFile);
    const docxPath = path.join(outputDir, item.outFile);

    console.log(`[${i + 1}/${lessons.length}] Đang xuất: ${item.outFile}...`);
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

  // --- GHÉP CHUYÊN ĐỀ SỐ HỌC & THỐNG KÊ (29 BÀI) ---
  console.log("\n=== BẮT ĐẦU GHÉP TỆP CHUYÊN ĐỀ SỐ HỌC & THỐNG KÊ TOÁN 6 HK2 (29 BÀI) ===");
  const soHocLessons = lessons.filter(l => l.group === 'so_hoc').map(l => ({
    mdFilePath: path.join(tempDir, l.mdFile),
    lessonInfo: l.lessonInfo,
    illustrations: l.illustrations
  }));

  const mergedSoHocPath = path.join(outputDir, "KHBD_Toan6_Ghep_SoHocThongKe_HK2.docx");
  try {
    const resMerged1 = await createMergedKhbdDocx({
      lessons: soHocLessons,
      outputDocxPath: mergedSoHocPath,
      docTitle: "KẾ HOẠCH BÀI DẠY TOÁN 6 - PHẦN SỐ HỌC VÀ THỐNG KÊ - HỌC KÌ II"
    });
    console.log(` -> THÀNH CÔNG TỆP GHÉP SỐ HỌC: ${path.basename(resMerged1.path)} (${resMerged1.size} bytes)`);
  } catch (err) {
    console.error(" -> LỖI ghép Số học:", err);
  }

  // --- GHÉP CHUYÊN ĐỀ HÌNH HỌC (14 BÀI) ---
  console.log("\n=== BẮT ĐẦU GHÉP TỆP CHUYÊN ĐỀ HÌNH HỌC CƠ BẢN TOÁN 6 HK2 (14 BÀI) ===");
  const hinhHocLessons = lessons.filter(l => l.group === 'hinh_hoc').map(l => ({
    mdFilePath: path.join(tempDir, l.mdFile),
    lessonInfo: l.lessonInfo,
    illustrations: l.illustrations
  }));

  const mergedHinhHocPath = path.join(outputDir, "KHBD_Toan6_Ghep_HinhHoc_HK2.docx");
  try {
    const resMerged2 = await createMergedKhbdDocx({
      lessons: hinhHocLessons,
      outputDocxPath: mergedHinhHocPath,
      docTitle: "KẾ HOẠCH BÀI DẠY TOÁN 6 - PHẦN HÌNH HỌC CƠ BẢN - HỌC KÌ II"
    });
    console.log(` -> THÀNH CÔNG TỆP GHÉP HÌNH HỌC: ${path.basename(resMerged2.path)} (${resMerged2.size} bytes)`);
  } catch (err) {
    console.error(" -> LỖI ghép Hình học:", err);
  }

  console.log("\n=== HOÀN TẤT XUẤT TOÀN BỘ FILE DOCX TOÁN 6 HK2 (TUẦN 19 - 35)! ===");
}

runBatch().catch(console.error);
