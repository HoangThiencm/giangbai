/**
 * Script biên dịch và xuất hàng loạt KHBD Toán 9 Học kì II (Tuần 19 - 35)
 * Thầy Hoàng Tấn Thiên - Năm học 2026 - 2027
 * Chuẩn CV 5512 V2.1 - 100% Word Equation OMML - Đầy đủ 16 Sơ đồ tư duy Mindmap vector 300 DPI
 */

const fs = require('fs');
const path = require('path');
const { createKhbdDocx, createMergedKhbdDocx } = require('../../engine/export_khbd_engine');

const tempDir = path.resolve(__dirname);
const outputDir = path.resolve(__dirname, '../../1_SOAN_KHBD/Ket_qua/HK2/TOAN9');

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
    mdFile: "01_KHBD_Toan9_Bai18_HamSoBacHai_Tiet43-45.md",
    outFile: "01_KHBD_Toan9_Bai18_HamSoBacHai_Tiet43-45.docx",
    group: "dai_so_thong_ke_xac_suat",
    illustrations: [],
    lessonInfo: {
      topic: "BÀI 18: HÀM SỐ Y = AX² (A KHÁC 0)",
      ppct: "TIẾT 43, 44, 45",
      lessonScope: "TIẾT 43, 44, 45",
      duration: "03 tiết (135 phút)"
    }
  },
  {
    id: "02",
    mdFile: "02_KHBD_Toan9_Bai19_PhuongTrinhBacHaiMotAn_Tiet46-49.md",
    outFile: "02_KHBD_Toan9_Bai19_PhuongTrinhBacHaiMotAn_Tiet46-49.docx",
    group: "dai_so_thong_ke_xac_suat",
    illustrations: [],
    lessonInfo: {
      topic: "BÀI 19: PHƯƠNG TRÌNH BẬC HAI MỘT ẨN",
      ppct: "TIẾT 46, 47, 48, 49",
      lessonScope: "TIẾT 46, 47, 48, 49",
      duration: "04 tiết (180 phút)"
    }
  },
  {
    id: "03",
    mdFile: "03_KHBD_Toan9_LuyenTapChung_Tiet50.md",
    outFile: "03_KHBD_Toan9_LuyenTapChung_Tiet50.docx",
    group: "dai_so_thong_ke_xac_suat",
    illustrations: getMindmapIllustration('mindmap-toan9-tiet50', 'mindmap_toan9_tiet50.png', 'Sơ đồ tư duy Luyện tập chung Hàm số bậc hai và Phương trình bậc hai Tiết 50'),
    lessonInfo: {
      topic: "LUYỆN TẬP CHUNG: HÀM SỐ Y = AX² VÀ PHƯƠNG TRÌNH BẬC HAI",
      ppct: "TIẾT 50",
      lessonScope: "TIẾT 50",
      duration: "01 tiết (45 phút)"
    }
  },
  {
    id: "04",
    mdFile: "04_KHBD_Toan9_Bai20_DinhLiVieteVaUngDung_Tiet51-52.md",
    outFile: "04_KHBD_Toan9_Bai20_DinhLiVieteVaUngDung_Tiet51-52.docx",
    group: "dai_so_thong_ke_xac_suat",
    illustrations: [],
    lessonInfo: {
      topic: "BÀI 20: ĐỊNH LÍ VIÈTE VÀ ỨNG DỤNG",
      ppct: "TIẾT 51, 52",
      lessonScope: "TIẾT 51, 52",
      duration: "02 tiết (90 phút)"
    }
  },
  {
    id: "05",
    mdFile: "05_KHBD_Toan9_Bai21_GiaiBaiToanBangCachLapPT_Tiet53-54.md",
    outFile: "05_KHBD_Toan9_Bai21_GiaiBaiToanBangCachLapPT_Tiet53-54.docx",
    group: "dai_so_thong_ke_xac_suat",
    illustrations: [],
    lessonInfo: {
      topic: "BÀI 21: GIẢI BÀI TOÁN BẰNG CÁCH LẬP PHƯƠNG TRÌNH",
      ppct: "TIẾT 53, 54",
      lessonScope: "TIẾT 53, 54",
      duration: "02 tiết (90 phút)"
    }
  },
  {
    id: "06",
    mdFile: "06_KHBD_Toan9_LuyenTapChung_Tiet55.md",
    outFile: "06_KHBD_Toan9_LuyenTapChung_Tiet55.docx",
    group: "dai_so_thong_ke_xac_suat",
    illustrations: getMindmapIllustration('mindmap-toan9-tiet55', 'mindmap_toan9_tiet55.png', 'Sơ đồ tư duy Luyện tập chung Định lí Viète Tiết 55'),
    lessonInfo: {
      topic: "LUYỆN TẬP CHUNG: ĐỊNH LÍ VIÈTE VÀ GIẢI TOÁN BẰNG CÁCH LẬP PHƯƠNG TRÌNH",
      ppct: "TIẾT 55",
      lessonScope: "TIẾT 55",
      duration: "01 tiết (45 phút)"
    }
  },
  {
    id: "07",
    mdFile: "07_KHBD_Toan9_BaiTapCuoiChuong6_Tiet56.md",
    outFile: "07_KHBD_Toan9_BaiTapCuoiChuong6_Tiet56.docx",
    group: "dai_so_thong_ke_xac_suat",
    illustrations: getMindmapIllustration('mindmap-toan9-tiet56', 'mindmap_toan9_tiet56.png', 'Sơ đồ tư duy Bài tập cuối chương VI Tiết 56'),
    lessonInfo: {
      topic: "BÀI TẬP CUỐI CHƯƠNG VI",
      ppct: "TIẾT 56",
      lessonScope: "TIẾT 56",
      duration: "01 tiết (45 phút)"
    }
  },
  {
    id: "08",
    mdFile: "08_KHBD_Toan9_OnTapGiuaHK2_DaiSo_Tiet57.md",
    outFile: "08_KHBD_Toan9_OnTapGiuaHK2_DaiSo_Tiet57.docx",
    group: "dai_so_thong_ke_xac_suat",
    illustrations: getMindmapIllustration('mindmap-toan9-tiet57', 'mindmap_toan9_tiet57.png', 'Sơ đồ tư duy Ôn tập giữa HK2 Đại số Tiết 57'),
    lessonInfo: {
      topic: "ÔN TẬP GIỮA HỌC KÌ II (ĐẠI SỐ)",
      ppct: "TIẾT 57",
      lessonScope: "TIẾT 57",
      duration: "01 tiết (45 phút)"
    }
  },
  {
    id: "09",
    mdFile: "09_KHBD_Toan9_KiemTraGiuaHK2_DaiSo_Tiet58.md",
    outFile: "09_KHBD_Toan9_KiemTraGiuaHK2_DaiSo_Tiet58.docx",
    group: "dai_so_thong_ke_xac_suat",
    illustrations: [],
    lessonInfo: {
      topic: "KIỂM TRA ĐÁNH GIÁ GIỮA HỌC KÌ II (ĐẠI SỐ)",
      ppct: "TIẾT 58",
      lessonScope: "TIẾT 58",
      duration: "01 tiết (45 phút)"
    }
  },
  {
    id: "10",
    mdFile: "10_KHBD_Toan9_Bai22_BangTanSoVaBieuDoTanSo_Tiet59-60.md",
    outFile: "10_KHBD_Toan9_Bai22_BangTanSoVaBieuDoTanSo_Tiet59-60.docx",
    group: "dai_so_thong_ke_xac_suat",
    illustrations: [],
    lessonInfo: {
      topic: "BÀI 22: BẢNG TẦN SỐ VÀ BIỂU ĐỒ TẦN SỐ",
      ppct: "TIẾT 59, 60",
      lessonScope: "TIẾT 59, 60",
      duration: "02 tiết (90 phút)"
    }
  },
  {
    id: "11",
    mdFile: "11_KHBD_Toan9_Bai23_BangTanSoTuongDoiVaBieuDo_Tiet61-62.md",
    outFile: "11_KHBD_Toan9_Bai23_BangTanSoTuongDoiVaBieuDo_Tiet61-62.docx",
    group: "dai_so_thong_ke_xac_suat",
    illustrations: [],
    lessonInfo: {
      topic: "BÀI 23: BẢNG TẦN SỐ TƯƠNG ĐỐI VÀ BIỂU ĐỒ TẦN SỐ TƯƠNG ĐỐI",
      ppct: "TIẾT 61, 62",
      lessonScope: "TIẾT 61, 62",
      duration: "02 tiết (90 phút)"
    }
  },
  {
    id: "12",
    mdFile: "12_KHBD_Toan9_LuyenTapChung_Tiet63.md",
    outFile: "12_KHBD_Toan9_LuyenTapChung_Tiet63.docx",
    group: "dai_so_thong_ke_xac_suat",
    illustrations: getMindmapIllustration('mindmap-toan9-tiet63', 'mindmap_toan9_tiet63.png', 'Sơ đồ tư duy Luyện tập chung Tần số và Tần số tương đối Tiết 63'),
    lessonInfo: {
      topic: "LUYỆN TẬP CHUNG: BẢNG TẦN SỐ VÀ BIỂU ĐỒ TẦN SỐ",
      ppct: "TIẾT 63",
      lessonScope: "TIẾT 63",
      duration: "01 tiết (45 phút)"
    }
  },
  {
    id: "13",
    mdFile: "13_KHBD_Toan9_Bai24_BangTanSoGhepNhomVaBieuDo_Tiet64-66.md",
    outFile: "13_KHBD_Toan9_Bai24_BangTanSoGhepNhomVaBieuDo_Tiet64-66.docx",
    group: "dai_so_thong_ke_xac_suat",
    illustrations: [],
    lessonInfo: {
      topic: "BÀI 24: BẢNG TẦN SỐ, TẦN SỐ TƯƠNG ĐỐI GHÉP NHÓM VÀ BIỂU ĐỒ",
      ppct: "TIẾT 64, 65, 66",
      lessonScope: "TIẾT 64, 65, 66",
      duration: "03 tiết (135 phút)"
    }
  },
  {
    id: "14",
    mdFile: "14_KHBD_Toan9_BaiTapCuoiChuong7_Tiet67-68.md",
    outFile: "14_KHBD_Toan9_BaiTapCuoiChuong7_Tiet67-68.docx",
    group: "dai_so_thong_ke_xac_suat",
    illustrations: getMindmapIllustration('mindmap-toan9-tiet67-68', 'mindmap_toan9_tiet67_68.png', 'Sơ đồ tư duy Bài tập cuối chương VII Tiết 67 - 68'),
    lessonInfo: {
      topic: "BÀI TẬP CUỐI CHƯƠNG VII",
      ppct: "TIẾT 67, 68",
      lessonScope: "TIẾT 67, 68",
      duration: "02 tiết (90 phút)"
    }
  },
  {
    id: "15",
    mdFile: "15_KHBD_Toan9_Bai25_PhepThuNgauNhienVaKhongGianMau_Tiet69.md",
    outFile: "15_KHBD_Toan9_Bai25_PhepThuNgauNhienVaKhongGianMau_Tiet69.docx",
    group: "dai_so_thong_ke_xac_suat",
    illustrations: [],
    lessonInfo: {
      topic: "BÀI 25: PHÉP THỬ NGẪU NHIÊN VÀ KHÔNG GIAN MẪU",
      ppct: "TIẾT 69",
      lessonScope: "TIẾT 69",
      duration: "01 tiết (45 phút)"
    }
  },
  {
    id: "16",
    mdFile: "16_KHBD_Toan9_Bai26_XacSuatCuaBienCo_Tiet70-71.md",
    outFile: "16_KHBD_Toan9_Bai26_XacSuatCuaBienCo_Tiet70-71.docx",
    group: "dai_so_thong_ke_xac_suat",
    illustrations: [],
    lessonInfo: {
      topic: "BÀI 26: XÁC SUẤT CỦA BIẾN CỐ LIÊN QUAN TỚI PHÉP THỬ",
      ppct: "TIẾT 70, 71",
      lessonScope: "TIẾT 70, 71",
      duration: "02 tiết (90 phút)"
    }
  },
  {
    id: "17",
    mdFile: "17_KHBD_Toan9_LuyenTapChung_Tiet72.md",
    outFile: "17_KHBD_Toan9_LuyenTapChung_Tiet72.docx",
    group: "dai_so_thong_ke_xac_suat",
    illustrations: getMindmapIllustration('mindmap-toan9-tiet72', 'mindmap_toan9_tiet72.png', 'Sơ đồ tư duy Luyện tập chung Xác suất biến cố Tiết 72'),
    lessonInfo: {
      topic: "LUYỆN TẬP CHUNG: XÁC SUẤT CỦA BIẾN CỐ",
      ppct: "TIẾT 72",
      lessonScope: "TIẾT 72",
      duration: "01 tiết (45 phút)"
    }
  },
  {
    id: "18",
    mdFile: "18_KHBD_Toan9_BaiTapCuoiChuong8_Tiet73-74.md",
    outFile: "18_KHBD_Toan9_BaiTapCuoiChuong8_Tiet73-74.docx",
    group: "dai_so_thong_ke_xac_suat",
    illustrations: getMindmapIllustration('mindmap-toan9-tiet73-74', 'mindmap_toan9_tiet73_74.png', 'Sơ đồ tư duy Bài tập cuối chương VIII Tiết 73 - 74'),
    lessonInfo: {
      topic: "BÀI TẬP CUỐI CHƯƠNG VIII",
      ppct: "TIẾT 73, 74",
      lessonScope: "TIẾT 73, 74",
      duration: "02 tiết (90 phút)"
    }
  },
  {
    id: "19",
    mdFile: "19_KHBD_Toan9_HDTN_GiaiPTVaVeDoThiGeoGebra_Tiet75.md",
    outFile: "19_KHBD_Toan9_HDTN_GiaiPTVaVeDoThiGeoGebra_Tiet75.docx",
    group: "dai_so_thong_ke_xac_suat",
    illustrations: [],
    lessonInfo: {
      topic: "HOẠT ĐỘNG THỰC HÀNH VÀ TRẢI NGHIỆM: GIẢI PHƯƠNG TRÌNH, HỆ PHƯƠNG TRÌNH. VẼ ĐỒ THỊ HÀM SỐ BẰNG PHẦN MỀM GEOGEBRA",
      ppct: "TIẾT 75",
      lessonScope: "TIẾT 75",
      duration: "01 tiết (45 phút)"
    }
  },
  {
    id: "20",
    mdFile: "20_KHBD_Toan9_OnTapCuoiHK2_DaiSoThongKeXacSuat_Tiet76-77.md",
    outFile: "20_KHBD_Toan9_OnTapCuoiHK2_DaiSoThongKeXacSuat_Tiet76-77.docx",
    group: "dai_so_thong_ke_xac_suat",
    illustrations: getMindmapIllustration('mindmap-toan9-tiet76-77', 'mindmap_toan9_tiet76_77.png', 'Sơ đồ tư duy Ôn tập cuối HK2 Đại số, Thống kê và Xác suất Tiết 76 - 77'),
    lessonInfo: {
      topic: "ÔN TẬP HỌC KÌ II (ĐẠI SỐ, THỐNG KÊ VÀ XÁC SUẤT)",
      ppct: "TIẾT 76, 77",
      lessonScope: "TIẾT 76, 77",
      duration: "02 tiết (90 phút)"
    }
  },
  {
    id: "21",
    mdFile: "21_KHBD_Toan9_KiemTraCuoiHK2_DaiSo_Tiet78.md",
    outFile: "21_KHBD_Toan9_KiemTraCuoiHK2_DaiSo_Tiet78.docx",
    group: "dai_so_thong_ke_xac_suat",
    illustrations: [],
    lessonInfo: {
      topic: "KIỂM TRA ĐÁNH GIÁ CUỐI HỌC KÌ II (ĐẠI SỐ)",
      ppct: "TIẾT 78",
      lessonScope: "TIẾT 78",
      duration: "01 tiết (45 phút)"
    }
  },
  {
    id: "22",
    mdFile: "22_KHBD_Toan9_HDTN_ExcelThongKe_Tiet79.md",
    outFile: "22_KHBD_Toan9_HDTN_ExcelThongKe_Tiet79.docx",
    group: "dai_so_thong_ke_xac_suat",
    illustrations: [],
    lessonInfo: {
      topic: "HOẠT ĐỘNG THỰC HÀNH VÀ TRẢI NGHIỆM: XÁC ĐỊNH TẦN SỐ, TẦN SỐ TƯƠNG ĐỐI, VẼ CÁC BIỂU ĐỒ BẰNG EXCEL",
      ppct: "TIẾT 79",
      lessonScope: "TIẾT 79",
      duration: "01 tiết (45 phút)"
    }
  },
  {
    id: "23",
    mdFile: "23_KHBD_Toan9_HDTN_GeneTroiMendel_Tiet80.md",
    outFile: "23_KHBD_Toan9_HDTN_GeneTroiMendel_Tiet80.docx",
    group: "dai_so_thong_ke_xac_suat",
    illustrations: [],
    lessonInfo: {
      topic: "HOẠT ĐỘNG THỰC HÀNH VÀ TRẢI NGHIỆM: GENE TRỘI TRONG CÁC THẾ HỆ LAI",
      ppct: "TIẾT 80",
      lessonScope: "TIẾT 80",
      duration: "01 tiết (45 phút)"
    }
  },
  {
    id: "24",
    mdFile: "24_KHBD_Toan9_Bai27_GocNoiTiep_Tiet31-32.md",
    outFile: "24_KHBD_Toan9_Bai27_GocNoiTiep_Tiet31-32.docx",
    group: "hinh_hoc",
    illustrations: [],
    lessonInfo: {
      topic: "BÀI 27: GÓC NỘI TIẾP",
      ppct: "TIẾT 31, 32",
      lessonScope: "TIẾT 31, 32",
      duration: "02 tiết (90 phút)"
    }
  },
  {
    id: "25",
    mdFile: "25_KHBD_Toan9_Bai28_DuongTronNgoaiTiepVaNoiTiepTamGiac_Tiet33-34.md",
    outFile: "25_KHBD_Toan9_Bai28_DuongTronNgoaiTiepVaNoiTiepTamGiac_Tiet33-34.docx",
    group: "hinh_hoc",
    illustrations: [],
    lessonInfo: {
      topic: "BÀI 28: ĐƯỜNG TRÒN NGOẠI TIẾP VÀ ĐƯỜNG TRÒN NỘI TIẾP CỦA MỘT TAM GIÁC",
      ppct: "TIẾT 33, 34",
      lessonScope: "TIẾT 33, 34",
      duration: "02 tiết (90 phút)"
    }
  },
  {
    id: "26",
    mdFile: "26_KHBD_Toan9_LuyenTapChung_Tiet35-36.md",
    outFile: "26_KHBD_Toan9_LuyenTapChung_Tiet35-36.docx",
    group: "hinh_hoc",
    illustrations: getMindmapIllustration('mindmap-toan9-hinh-tiet35-36', 'mindmap_toan9_hinh_tiet35_36.png', 'Sơ đồ tư duy Luyện tập chung Góc nội tiếp và Đường tròn ngoại tiếp Tiết 35 - 36'),
    lessonInfo: {
      topic: "LUYỆN TẬP CHUNG: GÓC NỘI TIẾP VÀ ĐƯỜNG TRÒN NGOẠI TIẾP, NỘI TIẾP TAM GIÁC",
      ppct: "TIẾT 35, 36",
      lessonScope: "TIẾT 35, 36",
      duration: "02 tiết (90 phút)"
    }
  },
  {
    id: "27",
    mdFile: "27_KHBD_Toan9_Bai29_TuGiacNoiTiep_Tiet37-38.md",
    outFile: "27_KHBD_Toan9_Bai29_TuGiacNoiTiep_Tiet37-38.docx",
    group: "hinh_hoc",
    illustrations: [],
    lessonInfo: {
      topic: "BÀI 29: TỨ GIÁC NỘI TIẾP",
      ppct: "TIẾT 37, 38",
      lessonScope: "TIẾT 37, 38",
      duration: "02 tiết (90 phút)"
    }
  },
  {
    id: "28",
    mdFile: "28_KHBD_Toan9_Bai30_DaGiacDeu_Tiet39-40.md",
    outFile: "28_KHBD_Toan9_Bai30_DaGiacDeu_Tiet39-40.docx",
    group: "hinh_hoc",
    illustrations: [],
    lessonInfo: {
      topic: "BÀI 30: ĐA GIÁC ĐỀU",
      ppct: "TIẾT 39, 40",
      lessonScope: "TIẾT 39, 40",
      duration: "02 tiết (90 phút)"
    }
  },
  {
    id: "29",
    mdFile: "29_KHBD_Toan9_LuyenTapChung_Tiet41-42.md",
    outFile: "29_KHBD_Toan9_LuyenTapChung_Tiet41-42.docx",
    group: "hinh_hoc",
    illustrations: getMindmapIllustration('mindmap-toan9-hinh-tiet41-42', 'mindmap_toan9_hinh_tiet41_42.png', 'Sơ đồ tư duy Luyện tập chung Tứ giác nội tiếp và Đa giác đều Tiết 41 - 42'),
    lessonInfo: {
      topic: "LUYỆN TẬP CHUNG: TỨ GIÁC NỘI TIẾP VÀ ĐA GIÁC ĐỀU",
      ppct: "TIẾT 41, 42",
      lessonScope: "TIẾT 41, 42",
      duration: "02 tiết (90 phút)"
    }
  },
  {
    id: "30",
    mdFile: "30_KHBD_Toan9_BaiTapCuoiChuong9_Tiet43-44.md",
    outFile: "30_KHBD_Toan9_BaiTapCuoiChuong9_Tiet43-44.docx",
    group: "hinh_hoc",
    illustrations: getMindmapIllustration('mindmap-toan9-hinh-tiet43-44', 'mindmap_toan9_hinh_tiet43_44.png', 'Sơ đồ tư duy Bài tập cuối chương IX Tiết 43 - 44'),
    lessonInfo: {
      topic: "BÀI TẬP CUỐI CHƯƠNG IX",
      ppct: "TIẾT 43, 44",
      lessonScope: "TIẾT 43, 44",
      duration: "02 tiết (90 phút)"
    }
  },
  {
    id: "31",
    mdFile: "31_KHBD_Toan9_OnTapGiuaHK2_HinhHoc_Tiet45.md",
    outFile: "31_KHBD_Toan9_OnTapGiuaHK2_HinhHoc_Tiet45.docx",
    group: "hinh_hoc",
    illustrations: getMindmapIllustration('mindmap-toan9-hinh-tiet45', 'mindmap_toan9_hinh_tiet45.png', 'Sơ đồ tư duy Ôn tập giữa HK2 Hình học Tiết 45'),
    lessonInfo: {
      topic: "ÔN TẬP VÀ KIỂM TRA ĐÁNH GIÁ GIỮA HỌC KÌ II (HÌNH HỌC)",
      ppct: "TIẾT 45",
      lessonScope: "TIẾT 45",
      duration: "01 tiết (45 phút)"
    }
  },
  {
    id: "32",
    mdFile: "32_KHBD_Toan9_KiemTraGiuaHK2_HinhHoc_Tiet46.md",
    outFile: "32_KHBD_Toan9_KiemTraGiuaHK2_HinhHoc_Tiet46.docx",
    group: "hinh_hoc",
    illustrations: [],
    lessonInfo: {
      topic: "KIỂM TRA ĐÁNH GIÁ GIỮA HỌC KÌ II (HÌNH HỌC)",
      ppct: "TIẾT 46",
      lessonScope: "TIẾT 46",
      duration: "01 tiết (45 phút)"
    }
  },
  {
    id: "33",
    mdFile: "33_KHBD_Toan9_Bai31_HinhTruVaHinhNon_STEM_Tiet47-50.md",
    outFile: "33_KHBD_Toan9_Bai31_HinhTruVaHinhNon_STEM_Tiet47-50.docx",
    group: "hinh_hoc",
    illustrations: [],
    lessonInfo: {
      topic: "BÀI 31: HÌNH TRỤ VÀ HÌNH NÓN (BÀI HỌC STEM)",
      ppct: "TIẾT 47, 48, 49, 50",
      lessonScope: "TIẾT 47, 48, 49, 50",
      duration: "04 tiết (180 phút)"
    }
  },
  {
    id: "34",
    mdFile: "34_KHBD_Toan9_Bai32_HinhCau_STEM_Tiet51-52.md",
    outFile: "34_KHBD_Toan9_Bai32_HinhCau_STEM_Tiet51-52.docx",
    group: "hinh_hoc",
    illustrations: [],
    lessonInfo: {
      topic: "BÀI 32: HÌNH CẦU (BÀI HỌC STEM)",
      ppct: "TIẾT 51, 52",
      lessonScope: "TIẾT 51, 52",
      duration: "02 tiết (90 phút)"
    }
  },
  {
    id: "35",
    mdFile: "35_KHBD_Toan9_LuyenTapChung_Tiet53.md",
    outFile: "35_KHBD_Toan9_LuyenTapChung_Tiet53.docx",
    group: "hinh_hoc",
    illustrations: getMindmapIllustration('mindmap-toan9-hinh-tiet53', 'mindmap_toan9_hinh_tiet53.png', 'Sơ đồ tư duy Luyện tập chung Hình trụ, Hình nón và Hình cầu Tiết 53'),
    lessonInfo: {
      topic: "LUYỆN TẬP CHUNG: HÌNH TRỤ, HÌNH NÓN VÀ HÌNH CẦU",
      ppct: "TIẾT 53",
      lessonScope: "TIẾT 53",
      duration: "01 tiết (45 phút)"
    }
  },
  {
    id: "36",
    mdFile: "36_KHBD_Toan9_BaiTapCuoiChuong10_Tiet54-55.md",
    outFile: "36_KHBD_Toan9_BaiTapCuoiChuong10_Tiet54-55.docx",
    group: "hinh_hoc",
    illustrations: getMindmapIllustration('mindmap-toan9-hinh-tiet54-55', 'mindmap_toan9_hinh_tiet54_55.png', 'Sơ đồ tư duy Bài tập cuối chương X Tiết 54 - 55'),
    lessonInfo: {
      topic: "BÀI TẬP CUỐI CHƯƠNG X",
      ppct: "TIẾT 54, 55",
      lessonScope: "TIẾT 54, 55",
      duration: "02 tiết (90 phút)"
    }
  },
  {
    id: "37",
    mdFile: "37_KHBD_Toan9_OnTapCuoiHK2_HinhHoc_Tiet56-57.md",
    outFile: "37_KHBD_Toan9_OnTapCuoiHK2_HinhHoc_Tiet56-57.docx",
    group: "hinh_hoc",
    illustrations: getMindmapIllustration('mindmap-toan9-hinh-tiet56-57', 'mindmap_toan9_hinh_tiet56_57.png', 'Sơ đồ tư duy Ôn tập cuối HK2 Hình học Tiết 56 - 57'),
    lessonInfo: {
      topic: "ÔN TẬP VÀ KIỂM TRA ĐÁNH GIÁ CUỐI HỌC KÌ II (HÌNH HỌC)",
      ppct: "TIẾT 56, 57",
      lessonScope: "TIẾT 56, 57",
      duration: "02 tiết (90 phút)"
    }
  },
  {
    id: "38",
    mdFile: "38_KHBD_Toan9_KiemTraCuoiHK2_HinhHoc_Tiet58.md",
    outFile: "38_KHBD_Toan9_KiemTraCuoiHK2_HinhHoc_Tiet58.docx",
    group: "hinh_hoc",
    illustrations: [],
    lessonInfo: {
      topic: "KIỂM TRA ĐÁNH GIÁ CUỐI HỌC KÌ II (HÌNH HỌC)",
      ppct: "TIẾT 58",
      lessonScope: "TIẾT 58",
      duration: "01 tiết (45 phút)"
    }
  },
  {
    id: "39",
    mdFile: "39_KHBD_Toan9_HDTN_VeHinhGeoGebra_Tiet59-60.md",
    outFile: "39_KHBD_Toan9_HDTN_VeHinhGeoGebra_Tiet59-60.docx",
    group: "hinh_hoc",
    illustrations: [],
    lessonInfo: {
      topic: "HOẠT ĐỘNG THỰC HÀNH VÀ TRẢI NGHIỆM: VẼ HÌNH ĐƠN GIẢN VỚI PHẦN MỀM GEOGEBRA",
      ppct: "TIẾT 59, 60",
      lessonScope: "TIẾT 59, 60",
      duration: "02 tiết (90 phút)"
    }
  }
];

async function runBatch() {
  console.log(`=== BẮT ĐẦU XUẤT 39 BÀI ĐƠN LẺ TOÁN 9 HK2 ===`);
  let successCount = 0;
  let failCount = 0;

  for (let i = 0; i < lessons.length; i++) {
    const item = lessons[i];
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
      console.log(` [${item.id}/39] THÀNH CÔNG: ${item.outFile} (${res.size} bytes)`);
      successCount++;
    } catch (err) {
      console.error(` [${item.id}/39] LỖI: ${item.outFile} ->`, err.message);
      failCount++;
    }
  }

  console.log(`\nTổng kết xuất đơn lẻ: ${successCount} thành công, ${failCount} thất bại.`);

  // --- GHÉP CHUYÊN ĐỀ ĐẠI SỐ, THỐNG KÊ VÀ XÁC SUẤT (23 BÀI) ---
  console.log("\n=== BẮT ĐẦU GHÉP TỆP CHUYÊN ĐỀ ĐẠI SỐ, THỐNG KÊ VÀ XÁC SUẤT TOÁN 9 HK2 (23 BÀI) ===");
  const daiSoLessons = lessons.filter(l => l.group === 'dai_so_thong_ke_xac_suat').map(l => ({
    mdFilePath: path.join(tempDir, l.mdFile),
    lessonInfo: l.lessonInfo,
    illustrations: l.illustrations
  }));

  const mergedDaiSoPath = path.join(outputDir, "KHBD_Toan9_Ghep_DaiSoThongKeXacSuat_HK2.docx");
  try {
    const resMerged1 = await createMergedKhbdDocx({
      lessons: daiSoLessons,
      outputDocxPath: mergedDaiSoPath,
      docTitle: "KẾ HOẠCH BÀI DẠY TOÁN 9 - PHẦN ĐẠI SỐ, THỐNG KÊ VÀ XÁC SUẤT - HỌC KÌ II"
    });
    console.log(` -> THÀNH CÔNG TỆP GHÉP ĐẠI SỐ, THỐNG KÊ VÀ XÁC SUẤT: ${path.basename(resMerged1.path)} (${resMerged1.size} bytes)`);
  } catch (err) {
    console.error(" -> LỖI ghép Đại số, Thống kê và Xác suất:", err);
  }

  // --- GHÉP CHUYÊN ĐỀ HÌNH HỌC (16 BÀI) ---
  console.log("\n=== BẮT ĐẦU GHÉP TỆP CHUYÊN ĐỀ HÌNH HỌC TOÁN 9 HK2 (16 BÀI) ===");
  const hinhHocLessons = lessons.filter(l => l.group === 'hinh_hoc').map(l => ({
    mdFilePath: path.join(tempDir, l.mdFile),
    lessonInfo: l.lessonInfo,
    illustrations: l.illustrations
  }));

  const mergedHinhHocPath = path.join(outputDir, "KHBD_Toan9_Ghep_HinhHoc_HK2.docx");
  try {
    const resMerged2 = await createMergedKhbdDocx({
      lessons: hinhHocLessons,
      outputDocxPath: mergedHinhHocPath,
      docTitle: "KẾ HOẠCH BÀI DẠY TOÁN 9 - PHẦN HÌNH HỌC - HỌC KÌ II"
    });
    console.log(` -> THÀNH CÔNG TỆP GHÉP HÌNH HỌC: ${path.basename(resMerged2.path)} (${resMerged2.size} bytes)`);
  } catch (err) {
    console.error(" -> LỖI ghép Hình học:", err);
  }

  console.log("\n=== HOÀN TẤT XUẤT TOÀN BỘ FILE DOCX TOÁN 9 HK2 (TUẦN 19 - 35)! ===");
}

runBatch().catch(console.error);
