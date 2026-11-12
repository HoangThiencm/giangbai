/**
 * Script xuất bản hàng loạt 12 bài Tin học 6 Học kì II (Tuần 19 - 35)
 * Thầy Hoàng Tấn Thiên - Trường THCS Chu Văn An
 * Chuẩn Công văn 5512 V2.1 - 100% Bám sát SGK Kết nối tri thức - Hình ảnh minh họa 300 DPI
 */

const fs = require('fs');
const path = require('path');
const { createKhbdDocx, createMergedKhbdDocx } = require('../../engine/export_khbd_engine');

const tempDir = path.resolve(__dirname);
const illDir = path.join(tempDir, 'illustrations');
const outputDir = path.resolve(__dirname, '../../1_SOAN_KHBD/Ket_qua/HK2/TIN6');

if (!fs.existsSync(outputDir)) {
  fs.mkdirSync(outputDir, { recursive: true });
}

function getIllustration(id, filename, width, height, caption) {
  const imgPath = path.join(illDir, filename);
  if (fs.existsSync(imgPath)) {
    const b64 = fs.readFileSync(imgPath).toString('base64');
    return [{
      id: id,
      dataUrl: `data:image/png;base64,${b64}`,
      width: width || 500,
      height: height || 280,
      caption: caption || ''
    }];
  }
  return [];
}

const lessons = [
  {
    id: "01",
    mdFile: "01_KHBD_Tin6_Bai09_AnToanThongTinTrenInternet_Tiet19.md",
    outFile: "01_KHBD_Tin6_Bai09_AnToanThongTinTrenInternet_Tiet19.docx",
    illustrations: [
      ...getIllustration('hinh-virus-tiet19', 'hinh_virus_tiet19.png', 320, 300, 'Minh họa máy tính bị nhiễm virus và mã độc khi tải tệp lạ'),
      ...getIllustration('hinh-hacker-tiet19', 'hinh_hacker_tiet19.png', 280, 280, 'Minh họa nguy cơ kẻ xấu tấn công đánh cắp thông tin cá nhân')
    ],
    lessonInfo: {
      topic: "BÀI 9: AN TOÀN THÔNG TIN TRÊN INTERNET",
      ppct: "TIẾT 19",
      lessonScope: "TIẾT 19",
      duration: "01 tiết (45 phút)"
    }
  },
  {
    id: "02",
    mdFile: "02_KHBD_Tin6_Bai10_SoDoTuDuy_Tiet20-21.md",
    outFile: "02_KHBD_Tin6_Bai10_SoDoTuDuy_Tiet20-21.docx",
    illustrations: [
      ...getIllustration('hinh-sodotuduy-5-2', 'hinh_sodotuduy_5_2.png', 520, 280, 'Sơ đồ tư duy Hình 5.2 do Tony Buzan sáng tạo'),
      ...getIllustration('hinh-mindmaple-soluuniem', 'hinh_mindmaple_soluuniem.png', 540, 280, 'Sơ đồ tư duy Sổ lưu niệm lớp 6A trên phần mềm máy tính'),
      ...getIllustration('hinh-vandung-bai9-mindmap', 'hinh_vandung_bai9_mindmap.png', 520, 280, 'Sơ đồ tư duy Vận dụng tóm tắt Bài 9')
    ],
    lessonInfo: {
      topic: "BÀI 10: SƠ ĐỒ TƯ DUY",
      ppct: "TIẾT 20, 21",
      lessonScope: "TIẾT 20, 21",
      duration: "02 tiết (90 phút)"
    }
  },
  {
    id: "03",
    mdFile: "03_KHBD_Tin6_Bai11_DinhDangVanBan_Tiet22-23.md",
    outFile: "03_KHBD_Tin6_Bai11_DinhDangVanBan_Tiet22-23.docx",
    illustrations: [
      ...getIllustration('hinh-dinhdang-paragraph-5-4', 'hinh_dinhdang_paragraph_5_4.png', 520, 120, 'Các lệnh định dạng đoạn văn bản nhóm Paragraph'),
      ...getIllustration('hinh-baiviet-an-5-8', 'hinh_baiviet_an_5_8.png', 420, 380, 'Bài viết cảm nghĩ của bạn An được định dạng hoàn chỉnh'),
      ...getIllustration('hinh-setup-trang-5-9_10', 'hinh_setup_trang_5_9_10.png', 480, 320, 'Các thao tác thiết lập hướng trang và lề trang trong Page Setup')
    ],
    lessonInfo: {
      topic: "BÀI 11: ĐỊNH DẠNG VĂN BẢN",
      ppct: "TIẾT 22, 23",
      lessonScope: "TIẾT 22, 23",
      duration: "02 tiết (90 phút)"
    }
  },
  {
    id: "04",
    mdFile: "04_KHBD_Tin6_Bai12_TrinhBayThongTinODangBang_Tiet24-25.md",
    outFile: "04_KHBD_Tin6_Bai12_TrinhBayThongTinODangBang_Tiet24-25.docx",
    illustrations: [
      ...getIllustration('hinh-danhsach-so-sanh-5-11', 'hinh_danhsach_so_sanh_5_11.png', 500, 250, 'So sánh cách trình bày danh sách học sinh dạng bảng và dạng liệt kê'),
      ...getIllustration('hinh-chinhsuabang_layout_5_16', 'hinh_chinhsuabang_layout_5_16.png', 540, 120, 'Các lệnh chỉnh sửa bảng trên dải lệnh Table Tools Layout'),
      ...getIllustration('hinh-bang-thanhvien-hoanthanh', 'hinh_bang_thanhvien_hoanthanh.png', 420, 280, 'Bảng danh sách thành viên lớp 6A được tạo lập và định dạng hoàn chỉnh')
    ],
    lessonInfo: {
      topic: "BÀI 12: TRÌNH BÀY THÔNG TIN Ở DẠNG BẢNG",
      ppct: "TIẾT 24, 25",
      lessonScope: "TIẾT 24, 25",
      duration: "02 tiết (90 phút)"
    }
  },
  {
    id: "05",
    mdFile: "05_KHBD_Tin6_Bai13_ThucHanhTimKiemVaThayThe_Tiet26.md",
    outFile: "05_KHBD_Tin6_Bai13_ThucHanhTimKiemVaThayThe_Tiet26.docx",
    illustrations: [],
    lessonInfo: {
      topic: "BÀI 13: THỰC HÀNH: TÌM KIẾM VÀ THAY THẾ",
      ppct: "TIẾT 26",
      lessonScope: "TIẾT 26",
      duration: "01 tiết (45 phút)"
    }
  },
  {
    id: "06",
    mdFile: "06_KHBD_Tin6_Bai14_ThucHanhTongHop_HoanThienSoLuuNiem_Tiet27.md",
    outFile: "06_KHBD_Tin6_Bai14_ThucHanhTongHop_HoanThienSoLuuNiem_Tiet27.docx",
    illustrations: [],
    lessonInfo: {
      topic: "BÀI 14: THỰC HÀNH TỔNG HỢP: HOÀN THIỆN SỔ LƯU NIỆM",
      ppct: "TIẾT 27",
      lessonScope: "TIẾT 27",
      duration: "01 tiết (45 phút)"
    }
  },
  {
    id: "07",
    mdFile: "07_KHBD_Tin6_KiemTraGiuaHK2_Tiet28.md",
    outFile: "07_KHBD_Tin6_KiemTraGiuaHK2_Tiet28.docx",
    illustrations: [],
    lessonInfo: {
      topic: "KIỂM TRA ĐÁNH GIÁ GIỮA HỌC KÌ II",
      ppct: "TIẾT 28",
      lessonScope: "TIẾT 28",
      duration: "01 tiết (45 phút)"
    }
  },
  {
    id: "08",
    mdFile: "08_KHBD_Tin6_Bai15_ThuatToan_Tiet29.md",
    outFile: "08_KHBD_Tin6_Bai15_ThuatToan_Tiet29.docx",
    illustrations: [
      ...getIllustration('hinh-sodokhoi-dongtay-6-2', 'hinh_sodokhoi_dongtay_6_2.png', 480, 360, 'Sơ đồ khối mô tả thuật toán gấp hình trò chơi Đông-Tây-Nam-Bắc')
    ],
    lessonInfo: {
      topic: "BÀI 15: THUẬT TOÁN",
      ppct: "TIẾT 29",
      lessonScope: "TIẾT 29",
      duration: "01 tiết (45 phút)"
    }
  },
  {
    id: "09",
    mdFile: "09_KHBD_Tin6_Bai16_CacCauTrucDieuKhien_Tiet30-31.md",
    outFile: "09_KHBD_Tin6_Bai16_CacCauTrucDieuKhien_Tiet30-31.docx",
    illustrations: [
      ...getIllustration('hinh-sodokhoi-renhanh-6-7', 'hinh_sodokhoi_renhanh_6_7.png', 520, 250, 'Sơ đồ khối cấu trúc rẽ nhánh dạng thiếu và dạng đủ')
    ],
    lessonInfo: {
      topic: "BÀI 16: CÁC CẤU TRÚC ĐIỀU KHIỂN",
      ppct: "TIẾT 30, 31",
      lessonScope: "TIẾT 30, 31",
      duration: "02 tiết (90 phút)"
    }
  },
  {
    id: "10",
    mdFile: "10_KHBD_Tin6_Bai17_ChuongTrinhMayTinh_Tiet32-33.md",
    outFile: "10_KHBD_Tin6_Bai17_ChuongTrinhMayTinh_Tiet32-33.docx",
    illustrations: [
      ...getIllustration('hinh-scratch-giaodien-6-11', 'hinh_scratch_giaodien_6_11.png', 520, 260, 'Giao diện phần mềm lập trình trực quan Scratch 3.0')
    ],
    lessonInfo: {
      topic: "BÀI 17: CHƯƠNG TRÌNH MÁY TÍNH",
      ppct: "TIẾT 32, 33",
      lessonScope: "TIẾT 32, 33",
      duration: "02 tiết (90 phút)"
    }
  },
  {
    id: "11",
    mdFile: "11_KHBD_Tin6_OnTapCuoiHK2_Tiet34.md",
    outFile: "11_KHBD_Tin6_OnTapCuoiHK2_Tiet34.docx",
    illustrations: [],
    lessonInfo: {
      topic: "ÔN TẬP CUỐI HỌC KÌ II",
      ppct: "TIẾT 34",
      lessonScope: "TIẾT 34",
      duration: "01 tiết (45 phút)"
    }
  },
  {
    id: "12",
    mdFile: "12_KHBD_Tin6_KiemTraCuoiHK2_Tiet35.md",
    outFile: "12_KHBD_Tin6_KiemTraCuoiHK2_Tiet35.docx",
    illustrations: [],
    lessonInfo: {
      topic: "KIỂM TRA ĐÁNH GIÁ CUỐI HỌC KÌ II",
      ppct: "TIẾT 35",
      lessonScope: "TIẾT 35",
      duration: "01 tiết (45 phút)"
    }
  }
];

async function runBatch() {
  console.log(`=== BẮT ĐẦU XUẤT 12 BÀI ĐƠN LẺ TIN HỌC 6 HK2 ===`);
  let successCount = 0;
  let failCount = 0;

  for (let i = 0; i < lessons.length; i++) {
    const item = lessons[i];
    const mdPath = path.join(tempDir, item.mdFile);
    const outPath = path.join(outputDir, item.outFile);

    try {
      const res = await createKhbdDocx({
        mdFilePath: mdPath,
        outputDocxPath: outPath,
        illustrations: item.illustrations,
        lessonInfo: item.lessonInfo
      });
      console.log(` [${item.id}/12] THÀNH CÔNG: ${item.outFile} (${res.size} bytes)`);
      successCount++;
    } catch (err) {
      console.error(` [${item.id}/12] LỖI: ${item.outFile} ->`, err.message);
      failCount++;
    }
  }

  console.log(`\nTổng kết xuất đơn lẻ: ${successCount} thành công, ${failCount} thất bại.`);

  // --- GHÉP TOÀN BỘ KHBD TIN HỌC 6 HK2 ---
  console.log("\n=== BẮT ĐẦU GHÉP TỆP TOÀN BỘ KHBD TIN HỌC 6 HK2 (TIẾT 19 - 35) ===");
  const allLessons = lessons.map(l => ({
    mdFilePath: path.join(tempDir, l.mdFile),
    lessonInfo: l.lessonInfo,
    illustrations: l.illustrations
  }));

  const mergedPath = path.join(outputDir, "KHBD_Tin6_Ghep_HK2_Tuan19-35.docx");
  try {
    const resMerged = await createMergedKhbdDocx({
      lessons: allLessons,
      outputDocxPath: mergedPath,
      docTitle: "KẾ HOẠCH BÀI DẠY TIN HỌC 6 - HỌC KÌ II (NĂM HỌC 2026 - 2027)"
    });
    console.log(` -> THÀNH CÔNG TỆP GHÉP TOÀN BỘ: ${path.basename(resMerged.path)} (${resMerged.size} bytes)`);
  } catch (err) {
    console.error(" -> LỖI ghép toàn bộ Tin 6:", err);
  }

  console.log("\n=== HOÀN TẤT XUẤT TOÀN BỘ FILE DOCX TIN HỌC 6 HK2 CHUẨN SƯ PHẠM! ===");
}

runBatch().catch(console.error);
