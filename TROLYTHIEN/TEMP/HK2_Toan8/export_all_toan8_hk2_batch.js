/**
 * Script biên dịch và xuất hàng loạt KHBD Toán 8 Học kì II (Tuần 19 - 35)
 * Thầy Hoàng Tấn Thiên - Năm học 2026 - 2027
 * Chuẩn CV 5512 V2.1 - 100% Word Equation OMML - Đầy đủ 17 Sơ đồ tư duy Mindmap vector 300 DPI
 */

const fs = require('fs');
const path = require('path');
const { createKhbdDocx, createMergedKhbdDocx } = require('../../engine/export_khbd_engine');

const tempDir = path.resolve(__dirname);
const outputDir = path.resolve(__dirname, '../../1_SOAN_KHBD/Ket_qua/HK2/TOAN8');

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
  {
    id: "01",
    mdFile: "01_KHBD_Toan8_Bai21_PhanThucDaiSo_Tiet42-43.md",
    outFile: "01_KHBD_Toan8_Bai21_PhanThucDaiSo_Tiet42-43.docx",
    group: "dai_so_xac_suat",
    illustrations: [],
    lessonInfo: {
      topic: "BÀI 21: PHÂN THỨC ĐẠI SỐ",
      ppct: "TIẾT 42, 43",
      lessonScope: "TIẾT 42, 43",
      duration: "02 tiết (90 phút)"
    }
  },
  {
    id: "02",
    mdFile: "02_KHBD_Toan8_Bai22_TinhChatCoBanPhanThuc_Tiet44-46.md",
    outFile: "02_KHBD_Toan8_Bai22_TinhChatCoBanPhanThuc_Tiet44-46.docx",
    group: "dai_so_xac_suat",
    illustrations: [],
    lessonInfo: {
      topic: "BÀI 22: TÍNH CHẤT CƠ BẢN CỦA PHÂN THỨC ĐẠI SỐ",
      ppct: "TIẾT 44, 45, 46",
      lessonScope: "TIẾT 44, 45, 46",
      duration: "03 tiết (135 phút)"
    }
  },
  {
    id: "03",
    mdFile: "03_KHBD_Toan8_LuyenTapChung_Tiet47.md",
    outFile: "03_KHBD_Toan8_LuyenTapChung_Tiet47.docx",
    group: "dai_so_xac_suat",
    illustrations: getMindmapIllustration('mindmap-toan8-tiet47', 'mindmap_toan8_tiet47.png', 'Sơ đồ tư duy Luyện tập chung Tiết 47'),
    lessonInfo: {
      topic: "LUYỆN TẬP CHUNG: PHÂN THỨC ĐẠI SỐ (TRANG 13)",
      ppct: "TIẾT 47",
      lessonScope: "TIẾT 47",
      duration: "01 tiết (45 phút)"
    }
  },
  {
    id: "04",
    mdFile: "04_KHBD_Toan8_Bai23_PhepCongVaTruPhanThuc_Tiet48-50.md",
    outFile: "04_KHBD_Toan8_Bai23_PhepCongVaTruPhanThuc_Tiet48-50.docx",
    group: "dai_so_xac_suat",
    illustrations: [],
    lessonInfo: {
      topic: "BÀI 23: PHÉP CỘNG VÀ PHÉP TRỪ PHÂN THỨC ĐẠI SỐ",
      ppct: "TIẾT 48, 49, 50",
      lessonScope: "TIẾT 48, 49, 50",
      duration: "03 tiết (135 phút)"
    }
  },
  {
    id: "05",
    mdFile: "05_KHBD_Toan8_Bai24_PhepNhanVaChiaPhanThuc_Tiet51-52.md",
    outFile: "05_KHBD_Toan8_Bai24_PhepNhanVaChiaPhanThuc_Tiet51-52.docx",
    group: "dai_so_xac_suat",
    illustrations: [],
    lessonInfo: {
      topic: "BÀI 24: PHÉP NHÂN VÀ PHÉP CHIA PHÂN THỨC ĐẠI SỐ",
      ppct: "TIẾT 51, 52",
      lessonScope: "TIẾT 51, 52",
      duration: "02 tiết (90 phút)"
    }
  },
  {
    id: "06",
    mdFile: "06_KHBD_Toan8_LuyenTapChung_Tiet53.md",
    outFile: "06_KHBD_Toan8_LuyenTapChung_Tiet53.docx",
    group: "dai_so_xac_suat",
    illustrations: getMindmapIllustration('mindmap-toan8-tiet53', 'mindmap_toan8_tiet53.png', 'Sơ đồ tư duy Luyện tập chung Tiết 53'),
    lessonInfo: {
      topic: "LUYỆN TẬP CHUNG: CÁC PHÉP TÍNH PHÂN THỨC ĐẠI SỐ (TRANG 23)",
      ppct: "TIẾT 53",
      lessonScope: "TIẾT 53",
      duration: "01 tiết (45 phút)"
    }
  },
  {
    id: "07",
    mdFile: "07_KHBD_Toan8_BaiTapCuoiChuong6_Tiet54.md",
    outFile: "07_KHBD_Toan8_BaiTapCuoiChuong6_Tiet54.docx",
    group: "dai_so_xac_suat",
    illustrations: getMindmapIllustration('mindmap-toan8-tiet54', 'mindmap_toan8_tiet54.png', 'Sơ đồ tư duy Bài tập cuối chương VI Tiết 54'),
    lessonInfo: {
      topic: "BÀI TẬP CUỐI CHƯƠNG VI: PHÂN THỨC ĐẠI SỐ (TRANG 24)",
      ppct: "TIẾT 54",
      lessonScope: "TIẾT 54",
      duration: "01 tiết (45 phút)"
    }
  },
  {
    id: "08",
    mdFile: "08_KHBD_Toan8_Bai25_PhuongTrinhBacNhatMotAn_Tiet55-56.md",
    outFile: "08_KHBD_Toan8_Bai25_PhuongTrinhBacNhatMotAn_Tiet55-56.docx",
    group: "dai_so_xac_suat",
    illustrations: [],
    lessonInfo: {
      topic: "BÀI 25: PHƯƠNG TRÌNH BẬC NHẤT MỘT ẨN",
      ppct: "TIẾT 55, 56",
      lessonScope: "TIẾT 55, 56",
      duration: "02 tiết (90 phút)"
    }
  },
  {
    id: "09",
    mdFile: "09_KHBD_Toan8_OnTapGiuaHK2_DaiSo_Tiet58.md",
    outFile: "09_KHBD_Toan8_OnTapGiuaHK2_DaiSo_Tiet58.docx",
    group: "dai_so_xac_suat",
    illustrations: getMindmapIllustration('mindmap-toan8-tiet58', 'mindmap_toan8_tiet58.png', 'Sơ đồ tư duy Ôn tập giữa HK2 Tiết 58'),
    lessonInfo: {
      topic: "ÔN TẬP GIỮA HỌC KÌ II (ĐẠI SỐ)",
      ppct: "TIẾT 58",
      lessonScope: "TIẾT 58",
      duration: "01 tiết (45 phút)"
    }
  },
  {
    id: "10",
    mdFile: "10_KHBD_Toan8_KiemTraGiuaHK2_DaiSo_Tiet59.md",
    outFile: "10_KHBD_Toan8_KiemTraGiuaHK2_DaiSo_Tiet59.docx",
    group: "dai_so_xac_suat",
    illustrations: [],
    lessonInfo: {
      topic: "KIỂM TRA ĐÁNH GIÁ GIỮA HỌC KÌ II (ĐẠI SỐ)",
      ppct: "TIẾT 59",
      lessonScope: "TIẾT 59",
      duration: "01 tiết (45 phút)"
    }
  },
  {
    id: "11",
    mdFile: "11_KHBD_Toan8_LuyenTapChung_Tiet60.md",
    outFile: "11_KHBD_Toan8_LuyenTapChung_Tiet60.docx",
    group: "dai_so_xac_suat",
    illustrations: getMindmapIllustration('mindmap-toan8-tiet60', 'mindmap_toan8_tiet60.png', 'Sơ đồ tư duy Luyện tập chung Tiết 60'),
    lessonInfo: {
      topic: "LUYỆN TẬP CHUNG: PHƯƠNG TRÌNH BẬC NHẤT MỘT ẨN (TRANG 37)",
      ppct: "TIẾT 60",
      lessonScope: "TIẾT 60",
      duration: "01 tiết (45 phút)"
    }
  },
  {
    id: "12",
    mdFile: "12_KHBD_Toan8_Bai26_GiaiBaiToanBangCachLapPT_Tiet57.md",
    outFile: "12_KHBD_Toan8_Bai26_GiaiBaiToanBangCachLapPT_Tiet57.docx",
    group: "dai_so_xac_suat",
    illustrations: [],
    lessonInfo: {
      topic: "BÀI 26: GIẢI BÀI TOÁN BẰNG CÁCH LẬP PHƯƠNG TRÌNH",
      ppct: "TIẾT 57",
      lessonScope: "TIẾT 57",
      duration: "01 tiết (45 phút)"
    }
  },
  {
    id: "13",
    mdFile: "13_KHBD_Toan8_Bai27_KhaiNiemHamSoVaDoThi_Tiet61-63.md",
    outFile: "13_KHBD_Toan8_Bai27_KhaiNiemHamSoVaDoThi_Tiet61-63.docx",
    group: "dai_so_xac_suat",
    illustrations: [],
    lessonInfo: {
      topic: "BÀI 27: KHÁI NIỆM HÀM SỐ VÀ ĐỒ THỊ CỦA HÀM SỐ",
      ppct: "TIẾT 61, 62, 63",
      lessonScope: "TIẾT 61, 62, 63",
      duration: "03 tiết (135 phút)"
    }
  },
  {
    id: "14",
    mdFile: "14_KHBD_Toan8_Bai28_HamSoBacNhatVaDoThi_Tiet64-65.md",
    outFile: "14_KHBD_Toan8_Bai28_HamSoBacNhatVaDoThi_Tiet64-65.docx",
    group: "dai_so_xac_suat",
    illustrations: [],
    lessonInfo: {
      topic: "BÀI 28: HÀM SỐ BẬC NHẤT VÀ ĐỒ THỊ CỦA HÀM SỐ BẬC NHẤT",
      ppct: "TIẾT 64, 65",
      lessonScope: "TIẾT 64, 65",
      duration: "02 tiết (90 phút)"
    }
  },
  {
    id: "15",
    mdFile: "15_KHBD_Toan8_Bai29_HeSoGocCuaDuongThang_Tiet66.md",
    outFile: "15_KHBD_Toan8_Bai29_HeSoGocCuaDuongThang_Tiet66.docx",
    group: "dai_so_xac_suat",
    illustrations: [],
    lessonInfo: {
      topic: "BÀI 29: HỆ SỐ GÓC CỦA ĐƯỜNG THẲNG",
      ppct: "TIẾT 66",
      lessonScope: "TIẾT 66",
      duration: "01 tiết (45 phút)"
    }
  },
  {
    id: "16",
    mdFile: "16_KHBD_Toan8_LuyenTapChung_Tiet67.md",
    outFile: "16_KHBD_Toan8_LuyenTapChung_Tiet67.docx",
    group: "dai_so_xac_suat",
    illustrations: getMindmapIllustration('mindmap-toan8-tiet67', 'mindmap_toan8_tiet67.png', 'Sơ đồ tư duy Luyện tập chung Tiết 67'),
    lessonInfo: {
      topic: "LUYỆN TẬP CHUNG: HÀM SỐ BẬC NHẤT VÀ ĐỒ THỊ (TRANG 53)",
      ppct: "TIẾT 67",
      lessonScope: "TIẾT 67",
      duration: "01 tiết (45 phút)"
    }
  },
  {
    id: "17",
    mdFile: "17_KHBD_Toan8_BaiTapCuoiChuong7_Tiet68.md",
    outFile: "17_KHBD_Toan8_BaiTapCuoiChuong7_Tiet68.docx",
    group: "dai_so_xac_suat",
    illustrations: getMindmapIllustration('mindmap-toan8-tiet68', 'mindmap_toan8_tiet68.png', 'Sơ đồ tư duy Bài tập cuối chương VII Tiết 68'),
    lessonInfo: {
      topic: "BÀI TẬP CUỐI CHƯƠNG VII: PHƯƠNG TRÌNH VÀ HÀM SỐ BẬC NHẤT (TRANG 54)",
      ppct: "TIẾT 68",
      lessonScope: "TIẾT 68",
      duration: "01 tiết (45 phút)"
    }
  },
  {
    id: "18",
    mdFile: "18_KHBD_Toan8_HDTN_TaiChinhVaGeoGebra_Tiet69-70.md",
    outFile: "18_KHBD_Toan8_HDTN_TaiChinhVaGeoGebra_Tiet69-70.docx",
    group: "dai_so_xac_suat",
    illustrations: [],
    lessonInfo: {
      topic: "HOẠT ĐỘNG THỰC HÀNH TRẢI NGHIỆM: ỨNG DỤNG CỦA HÀM SỐ BẬC NHẤT TRONG TÀI CHÍNH VÀ VẼ ĐỒ THỊ VỚI PHẦN MỀM GEOGEBRA",
      ppct: "TIẾT 69, 70",
      lessonScope: "TIẾT 69, 70",
      duration: "02 tiết (90 phút)"
    }
  },
  {
    id: "19",
    mdFile: "19_KHBD_Toan8_Bai30_KetQuaCoTheVaKetQuaThuanLoi_Tiet71-72.md",
    outFile: "19_KHBD_Toan8_Bai30_KetQuaCoTheVaKetQuaThuanLoi_Tiet71-72.docx",
    group: "dai_so_xac_suat",
    illustrations: [],
    lessonInfo: {
      topic: "BÀI 30: KẾT QUẢ CÓ THỂ VÀ KẾT QUẢ THUẬN LỢI",
      ppct: "TIẾT 71, 72",
      lessonScope: "TIẾT 71, 72",
      duration: "02 tiết (90 phút)"
    }
  },
  {
    id: "20",
    mdFile: "20_KHBD_Toan8_Bai31_CachTinhXacSuatBangTiSo_Tiet73.md",
    outFile: "20_KHBD_Toan8_Bai31_CachTinhXacSuatBangTiSo_Tiet73.docx",
    group: "dai_so_xac_suat",
    illustrations: [],
    lessonInfo: {
      topic: "BÀI 31: CÁCH TÍNH XÁC SUẤT CỦA BIẾN CỐ BẰNG TỈ SỐ",
      ppct: "TIẾT 73",
      lessonScope: "TIẾT 73",
      duration: "01 tiết (45 phút)"
    }
  },
  {
    id: "21",
    mdFile: "21_KHBD_Toan8_Bai32_MoiLienHeXacSuatThucNghiem_Tiet74-75.md",
    outFile: "21_KHBD_Toan8_Bai32_MoiLienHeXacSuatThucNghiem_Tiet74-75.docx",
    group: "dai_so_xac_suat",
    illustrations: [],
    lessonInfo: {
      topic: "BÀI 32: MỐI LIÊN HỆ GIỮA XÁC SUẤT THỰC NGHIỆM VỚI XÁC SUẤT VÀ ỨNG DỤNG",
      ppct: "TIẾT 74, 75",
      lessonScope: "TIẾT 74, 75",
      duration: "02 tiết (90 phút)"
    }
  },
  {
    id: "22",
    mdFile: "22_KHBD_Toan8_LuyenTapChung_Tiet76.md",
    outFile: "22_KHBD_Toan8_LuyenTapChung_Tiet76.docx",
    group: "dai_so_xac_suat",
    illustrations: getMindmapIllustration('mindmap-toan8-tiet76', 'mindmap_toan8_tiet76.png', 'Sơ đồ tư duy Luyện tập chung Tiết 76'),
    lessonInfo: {
      topic: "LUYỆN TẬP CHUNG: XÁC SUẤT CỦA BIẾN CỐ (TRANG 68)",
      ppct: "TIẾT 76",
      lessonScope: "TIẾT 76",
      duration: "01 tiết (45 phút)"
    }
  },
  {
    id: "23",
    mdFile: "23_KHBD_Toan8_BaiTapCuoiChuong8_Tiet77.md",
    outFile: "23_KHBD_Toan8_BaiTapCuoiChuong8_Tiet77.docx",
    group: "dai_so_xac_suat",
    illustrations: getMindmapIllustration('mindmap-toan8-tiet77', 'mindmap_toan8_tiet77.png', 'Sơ đồ tư duy Bài tập cuối chương VIII Tiết 77'),
    lessonInfo: {
      topic: "BÀI TẬP CUỐI CHƯƠNG VIII: MỞ ĐẦU VỀ TÍNH XÁC SUẤT CỦA BIẾN CỐ (TRANG 70)",
      ppct: "TIẾT 77",
      lessonScope: "TIẾT 77",
      duration: "01 tiết (45 phút)"
    }
  },
  {
    id: "24",
    mdFile: "24_KHBD_Toan8_HDTN_Excel_Tiet78.md",
    outFile: "24_KHBD_Toan8_HDTN_Excel_Tiet78.docx",
    group: "dai_so_xac_suat",
    illustrations: [],
    lessonInfo: {
      topic: "HOẠT ĐỘNG THỰC HÀNH TRẢI NGHIỆM: MÔ TẢ THÍ NGHIỆM NGẪU NHIÊN VỚI PHẦN MỀM EXCEL",
      ppct: "TIẾT 78",
      lessonScope: "TIẾT 78",
      duration: "01 tiết (45 phút)"
    }
  },
  {
    id: "25",
    mdFile: "25_KHBD_Toan8_OnTapCuoiHK2_DaiSoXacSuat_Tiet79-81.md",
    outFile: "25_KHBD_Toan8_OnTapCuoiHK2_DaiSoXacSuat_Tiet79-81.docx",
    group: "dai_so_xac_suat",
    illustrations: getMindmapIllustration('mindmap-toan8-tiet79-81', 'mindmap_toan8_tiet79_81.png', 'Sơ đồ tư duy Ôn tập cuối HK2 Tiết 79-81'),
    lessonInfo: {
      topic: "ÔN TẬP ĐÁNH GIÁ CUỐI HỌC KÌ II (ĐẠI SỐ VÀ XÁC SUẤT)",
      ppct: "TIẾT 79, 80, 81",
      lessonScope: "TIẾT 79, 80, 81",
      duration: "03 tiết (135 phút)"
    }
  },
  {
    id: "26",
    mdFile: "26_KHBD_Toan8_KiemTraCuoiHK2_DaiSoXacSuat_Tiet82.md",
    outFile: "26_KHBD_Toan8_KiemTraCuoiHK2_DaiSoXacSuat_Tiet82.docx",
    group: "dai_so_xac_suat",
    illustrations: [],
    lessonInfo: {
      topic: "KIỂM TRA ĐÁNH GIÁ CUỐI HỌC KÌ II (ĐẠI SỐ VÀ XÁC SUẤT)",
      ppct: "TIẾT 82",
      lessonScope: "TIẾT 82",
      duration: "01 tiết (45 phút)"
    }
  },
  {
    id: "27",
    mdFile: "27_KHBD_Toan8_TraBaiKiemTraCuoiHK2_Tiet83.md",
    outFile: "27_KHBD_Toan8_TraBaiKiemTraCuoiHK2_Tiet83.docx",
    group: "dai_so_xac_suat",
    illustrations: [],
    lessonInfo: {
      topic: "TRẢ BÀI KIỂM TRA ĐÁNH GIÁ CUỐI HỌC KÌ II (ĐẠI SỐ VÀ XÁC SUẤT)",
      ppct: "TIẾT 83",
      lessonScope: "TIẾT 83",
      duration: "01 tiết (45 phút)"
    }
  },
  {
    id: "28",
    mdFile: "28_KHBD_Toan8_Bai33_HaiTamGiacDongDang_Tiet32-33.md",
    outFile: "28_KHBD_Toan8_Bai33_HaiTamGiacDongDang_Tiet32-33.docx",
    group: "hinh_hoc",
    illustrations: [],
    lessonInfo: {
      topic: "BÀI 33: HAI TAM GIÁC ĐỒNG DẠNG",
      ppct: "TIẾT 32, 33",
      lessonScope: "TIẾT 32, 33",
      duration: "02 tiết (90 phút)"
    }
  },
  {
    id: "29",
    mdFile: "29_KHBD_Toan8_Bai34_BaTruongHopDongDang_Tiet34-36.md",
    outFile: "29_KHBD_Toan8_Bai34_BaTruongHopDongDang_Tiet34-36.docx",
    group: "hinh_hoc",
    illustrations: [],
    lessonInfo: {
      topic: "BÀI 34: BA TRƯỜNG HỢP ĐỒNG DẠNG CỦA HAI TAM GIÁC",
      ppct: "TIẾT 34, 35, 36",
      lessonScope: "TIẾT 34, 35, 36",
      duration: "03 tiết (135 phút)"
    }
  },
  {
    id: "30",
    mdFile: "30_KHBD_Toan8_LuyenTapChung_Tiet37.md",
    outFile: "30_KHBD_Toan8_LuyenTapChung_Tiet37.docx",
    group: "hinh_hoc",
    illustrations: getMindmapIllustration('mindmap-toan8-hinh-tiet37', 'mindmap_toan8_hinh_tiet37.png', 'Sơ đồ tư duy Luyện tập chung Tam giác đồng dạng Tiết 37'),
    lessonInfo: {
      topic: "LUYỆN TẬP CHUNG KIỂM TRA ĐÁNH GIÁ THƯỜNG XUYÊN",
      ppct: "TIẾT 37",
      lessonScope: "TIẾT 37",
      duration: "01 tiết (45 phút)"
    }
  },
  {
    id: "31",
    mdFile: "31_KHBD_Toan8_Bai35_DinhLiPythagoreVaUngDung_Tiet38-39.md",
    outFile: "31_KHBD_Toan8_Bai35_DinhLiPythagoreVaUngDung_Tiet38-39.docx",
    group: "hinh_hoc",
    illustrations: [],
    lessonInfo: {
      topic: "BÀI 35: ĐỊNH LÍ PYTHAGORE VÀ ỨNG DỤNG",
      ppct: "TIẾT 38, 39",
      lessonScope: "TIẾT 38, 39",
      duration: "02 tiết (90 phút)"
    }
  },
  {
    id: "32",
    mdFile: "32_KHBD_Toan8_Bai36_CacTruongHopDongDangTamGiacVuong_Tiet40-41.md",
    outFile: "32_KHBD_Toan8_Bai36_CacTruongHopDongDangTamGiacVuong_Tiet40-41.docx",
    group: "hinh_hoc",
    illustrations: [],
    lessonInfo: {
      topic: "BÀI 36: CÁC TRƯỜNG HỢP ĐỒNG DẠNG CỦA HAI TAM GIÁC VUÔNG",
      ppct: "TIẾT 40, 41",
      lessonScope: "TIẾT 40, 41",
      duration: "02 tiết (90 phút)"
    }
  },
  {
    id: "33",
    mdFile: "33_KHBD_Toan8_Bai37_HinhDongDang_Tiet42.md",
    outFile: "33_KHBD_Toan8_Bai37_HinhDongDang_Tiet42.docx",
    group: "hinh_hoc",
    illustrations: [],
    lessonInfo: {
      topic: "BÀI 37: HÌNH ĐỒNG DẠNG",
      ppct: "TIẾT 42",
      lessonScope: "TIẾT 42",
      duration: "01 tiết (45 phút)"
    }
  },
  {
    id: "34",
    mdFile: "34_KHBD_Toan8_LuyenTapChung_Tiet43.md",
    outFile: "34_KHBD_Toan8_LuyenTapChung_Tiet43.docx",
    group: "hinh_hoc",
    illustrations: getMindmapIllustration('mindmap-toan8-hinh-tiet43', 'mindmap_toan8_hinh_tiet43.png', 'Sơ đồ tư duy Luyện tập chung Định lí Pythagore và Tam giác vuông đồng dạng Tiết 43'),
    lessonInfo: {
      topic: "LUYỆN TẬP CHUNG",
      ppct: "TIẾT 43",
      lessonScope: "TIẾT 43",
      duration: "01 tiết (45 phút)"
    }
  },
  {
    id: "35",
    mdFile: "35_KHBD_Toan8_BaiTapCuoiChuong9_Tiet44.md",
    outFile: "35_KHBD_Toan8_BaiTapCuoiChuong9_Tiet44.docx",
    group: "hinh_hoc",
    illustrations: getMindmapIllustration('mindmap-toan8-hinh-tiet44', 'mindmap_toan8_hinh_tiet44.png', 'Sơ đồ tư duy Bài tập cuối chương IX Tiết 44'),
    lessonInfo: {
      topic: "BÀI TẬP CUỐI CHƯƠNG IX",
      ppct: "TIẾT 44",
      lessonScope: "TIẾT 44",
      duration: "01 tiết (45 phút)"
    }
  },
  {
    id: "36",
    mdFile: "36_KHBD_Toan8_HDTN_DoChieuCaoKhoangCach_Tiet45.md",
    outFile: "36_KHBD_Toan8_HDTN_DoChieuCaoKhoangCach_Tiet45.docx",
    group: "hinh_hoc",
    illustrations: [],
    lessonInfo: {
      topic: "HOẠT ĐỘNG THỰC HÀNH TRẢI NGHIỆM: ỨNG DỤNG ĐỊNH LÍ THALES, ĐỊNH LÍ PYTHAGORE VÀ TAM GIÁC ĐỒNG DẠNG ĐỂ ĐO CHIỀU CAO, KHOẢNG CÁCH",
      ppct: "TIẾT 45",
      lessonScope: "TIẾT 45",
      duration: "01 tiết (45 phút)"
    }
  },
  {
    id: "37",
    mdFile: "37_KHBD_Toan8_OnTapGiuaHK2_HinhHoc_Tiet46.md",
    outFile: "37_KHBD_Toan8_OnTapGiuaHK2_HinhHoc_Tiet46.docx",
    group: "hinh_hoc",
    illustrations: getMindmapIllustration('mindmap-toan8-hinh-tiet46', 'mindmap_toan8_hinh_tiet46.png', 'Sơ đồ tư duy Ôn tập giữa HK2 Hình học Tiết 46'),
    lessonInfo: {
      topic: "ÔN TẬP GIỮA HỌC KÌ II (HÌNH HỌC)",
      ppct: "TIẾT 46",
      lessonScope: "TIẾT 46",
      duration: "01 tiết (45 phút)"
    }
  },
  {
    id: "38",
    mdFile: "38_KHBD_Toan8_KiemTraGiuaHK2_HinhHoc_Tiet47.md",
    outFile: "38_KHBD_Toan8_KiemTraGiuaHK2_HinhHoc_Tiet47.docx",
    group: "hinh_hoc",
    illustrations: [],
    lessonInfo: {
      topic: "KIỂM TRA ĐÁNH GIÁ GIỮA HỌC KÌ II (HÌNH HỌC)",
      ppct: "TIẾT 47",
      lessonScope: "TIẾT 47",
      duration: "01 tiết (45 phút)"
    }
  },
  {
    id: "39",
    mdFile: "39_KHBD_Toan8_Bai38_HinhChopTamGiacDeu_Tiet48-49.md",
    outFile: "39_KHBD_Toan8_Bai38_HinhChopTamGiacDeu_Tiet48-49.docx",
    group: "hinh_hoc",
    illustrations: [],
    lessonInfo: {
      topic: "BÀI 38: HÌNH CHÓP TAM GIÁC ĐỀU",
      ppct: "TIẾT 48, 49",
      lessonScope: "TIẾT 48, 49",
      duration: "02 tiết (90 phút)"
    }
  },
  {
    id: "40",
    mdFile: "40_KHBD_Toan8_Bai39_HinhChopTuGiacDeu_Tiet50-51.md",
    outFile: "40_KHBD_Toan8_Bai39_HinhChopTuGiacDeu_Tiet50-51.docx",
    group: "hinh_hoc",
    illustrations: [],
    lessonInfo: {
      topic: "BÀI 39: HÌNH CHÓP TỨ GIÁC ĐỀU",
      ppct: "TIẾT 50, 51",
      lessonScope: "TIẾT 50, 51",
      duration: "02 tiết (90 phút)"
    }
  },
  {
    id: "41",
    mdFile: "41_KHBD_Toan8_LuyenTapChung_Tiet52.md",
    outFile: "41_KHBD_Toan8_LuyenTapChung_Tiet52.docx",
    group: "hinh_hoc",
    illustrations: getMindmapIllustration('mindmap-toan8-hinh-tiet52', 'mindmap_toan8_hinh_tiet52.png', 'Sơ đồ tư duy Luyện tập chung Hình chóp tam giác đều và tứ giác đều Tiết 52'),
    lessonInfo: {
      topic: "LUYỆN TẬP CHUNG",
      ppct: "TIẾT 52",
      lessonScope: "TIẾT 52",
      duration: "01 tiết (45 phút)"
    }
  },
  {
    id: "42",
    mdFile: "42_KHBD_Toan8_BaiTapCuoiChuong10_Tiet53.md",
    outFile: "42_KHBD_Toan8_BaiTapCuoiChuong10_Tiet53.docx",
    group: "hinh_hoc",
    illustrations: getMindmapIllustration('mindmap-toan8-hinh-tiet53', 'mindmap_toan8_hinh_tiet53.png', 'Sơ đồ tư duy Bài tập cuối chương X Tiết 53'),
    lessonInfo: {
      topic: "BÀI TẬP CUỐI CHƯƠNG X",
      ppct: "TIẾT 53",
      lessonScope: "TIẾT 53",
      duration: "01 tiết (45 phút)"
    }
  },
  {
    id: "43",
    mdFile: "43_KHBD_Toan8_OnTapCuoiHK2_HinhHoc_Tiet54-55.md",
    outFile: "43_KHBD_Toan8_OnTapCuoiHK2_HinhHoc_Tiet54-55.docx",
    group: "hinh_hoc",
    illustrations: getMindmapIllustration('mindmap-toan8-hinh-tiet54_55', 'mindmap_toan8_hinh_tiet54_55.png', 'Sơ đồ tư duy Ôn tập cuối HK2 Hình học Tiết 54 - 55'),
    lessonInfo: {
      topic: "ÔN TẬP HỌC KÌ II (HÌNH HỌC)",
      ppct: "TIẾT 54, 55",
      lessonScope: "TIẾT 54, 55",
      duration: "02 tiết (90 phút)"
    }
  },
  {
    id: "44",
    mdFile: "44_KHBD_Toan8_KiemTraCuoiHK2_HinhHoc_Tiet56.md",
    outFile: "44_KHBD_Toan8_KiemTraCuoiHK2_HinhHoc_Tiet56.docx",
    group: "hinh_hoc",
    illustrations: [],
    lessonInfo: {
      topic: "KIỂM TRA ĐÁNH GIÁ CUỐI HỌC KÌ II (HÌNH HỌC)",
      ppct: "TIẾT 56",
      lessonScope: "TIẾT 56",
      duration: "01 tiết (45 phút)"
    }
  },
  {
    id: "45",
    mdFile: "45_KHBD_Toan8_TraBaiKiemTraCuoiHK2_HinhHoc_Tiet57.md",
    outFile: "45_KHBD_Toan8_TraBaiKiemTraCuoiHK2_HinhHoc_Tiet57.docx",
    group: "hinh_hoc",
    illustrations: [],
    lessonInfo: {
      topic: "TRẢ BÀI KIỂM TRA HỌC KÌ II (HÌNH HỌC)",
      ppct: "TIẾT 57",
      lessonScope: "TIẾT 57",
      duration: "01 tiết (45 phút)"
    }
  },

];

async function runBatch() {
  console.log(`=== BẮT ĐẦU XUẤT 45 TỆP ĐƠN LẺ KHBD TOÁN 8 HỌC KÌ II ===`);
  let successCount = 0;
  let failCount = 0;

  for (const item of lessons) {
    const mdPath = path.join(tempDir, item.mdFile);
    const outPath = path.join(outputDir, item.outFile);

    if (!fs.existsSync(mdPath)) {
      console.error(` -> BỎ QUA: Không tìm thấy ${item.mdFile}`);
      failCount++;
      continue;
    }

    try {
      const res = await createKhbdDocx({
        mdFilePath: mdPath,
        outputDocxPath: outPath,
        illustrations: item.illustrations,
        lessonInfo: item.lessonInfo
      });
      console.log(` [${item.id}/45] THÀNH CÔNG: ${item.outFile} (${res.size} bytes)`);
      successCount++;
    } catch (err) {
      console.error(` [${item.id}/45] LỖI: ${item.outFile} ->`, err.message);
      failCount++;
    }
  }

  console.log(`\nTổng kết xuất đơn lẻ: ${successCount} thành công, ${failCount} thất bại.`);

  // --- GHÉP CHUYÊN ĐỀ ĐẠI SỐ & XÁC SUẤT (27 BÀI) ---
  console.log("\n=== BẮT ĐẦU GHÉP TỆP CHUYÊN ĐỀ ĐẠI SỐ & XÁC SUẤT TOÁN 8 HK2 (27 BÀI) ===");
  const daiSoLessons = lessons.filter(l => l.group === 'dai_so_xac_suat').map(l => ({
    mdFilePath: path.join(tempDir, l.mdFile),
    lessonInfo: l.lessonInfo,
    illustrations: l.illustrations
  }));

  const mergedDaiSoPath = path.join(outputDir, "KHBD_Toan8_Ghep_DaiSoXacSuat_HK2.docx");
  try {
    const resMerged1 = await createMergedKhbdDocx({
      lessons: daiSoLessons,
      outputDocxPath: mergedDaiSoPath,
      docTitle: "KẾ HOẠCH BÀI DẠY TOÁN 8 - PHẦN ĐẠI SỐ VÀ XÁC SUẤT - HỌC KÌ II"
    });
    console.log(` -> THÀNH CÔNG TỆP GHÉP ĐẠI SỐ & XÁC SUẤT: ${path.basename(resMerged1.path)} (${resMerged1.size} bytes)`);
  } catch (err) {
    console.error(" -> LỖI ghép Đại số & Xác suất:", err);
  }

  // --- GHÉP CHUYÊN ĐỀ HÌNH HỌC (18 BÀI) ---
  console.log("\n=== BẮT ĐẦU GHÉP TỆP CHUYÊN ĐỀ HÌNH HỌC TOÁN 8 HK2 (18 BÀI) ===");
  const hinhHocLessons = lessons.filter(l => l.group === 'hinh_hoc').map(l => ({
    mdFilePath: path.join(tempDir, l.mdFile),
    lessonInfo: l.lessonInfo,
    illustrations: l.illustrations
  }));

  const mergedHinhHocPath = path.join(outputDir, "KHBD_Toan8_Ghep_HinhHoc_HK2.docx");
  try {
    const resMerged2 = await createMergedKhbdDocx({
      lessons: hinhHocLessons,
      outputDocxPath: mergedHinhHocPath,
      docTitle: "KẾ HOẠCH BÀI DẠY TOÁN 8 - PHẦN HÌNH HỌC - HỌC KÌ II"
    });
    console.log(` -> THÀNH CÔNG TỆP GHÉP HÌNH HỌC: ${path.basename(resMerged2.path)} (${resMerged2.size} bytes)`);
  } catch (err) {
    console.error(" -> LỖI ghép Hình học:", err);
  }

  console.log("\n=== HOÀN TẤT XUẤT TOÀN BỘ FILE DOCX TOÁN 8 HK2 (TUẦN 19 - 35)! ===");
}

runBatch().catch(console.error);
