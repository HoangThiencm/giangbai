// -*- coding: utf-8 -*-
/**
 * Export trọn bộ 4 Kế hoạch bài dạy (KHBD) Toán 9 (Chương IV & Chương V) sang Word .docx
 * Sử dụng export_khbd_engine.js chuẩn Công văn 5512 V2.0
 */
const fs = require('fs');
const path = require('path');
const { createKhbdDocx } = require('../TROLYTHIEN/engine/export_khbd_engine.js');

const KET_QUA_DIR = path.resolve(__dirname, '../TROLYTHIEN/1_SOAN_KHBD/Ket_qua');
const HINH_DIR = path.resolve(__dirname, '../TROLYTHIEN/engine/hinh_ve_sgk');

if (!fs.existsSync(KET_QUA_DIR)) {
  fs.mkdirSync(KET_QUA_DIR, { recursive: true });
}

function loadIll(id, caption, filename, width, height) {
  const p = path.join(HINH_DIR, filename);
  if (!fs.existsSync(p)) {
    console.error(`Không tìm thấy ảnh: ${p}`);
    return null;
  }
  const b64 = fs.readFileSync(p).toString('base64');
  return {
    id,
    caption,
    dataUrl: `data:image/png;base64,${b64}`,
    width,
    height
  };
}

const lessons = [
  {
    fileName: 'KHBD_01_Toan9_Bai12_MotSoHeThucGiuaCanhVaGocTamGiacVuong_Tiet4-6.docx',
    mdPath: path.resolve(__dirname, 'BAI_01.md'),
    info: {
      schoolName: 'TRƯỜNG THCS TRẦN PHÚ',
      subjectGroup: 'TỔ TOÁN - TIN HỌC',
      teacherName: 'GIÁO VIÊN TOÁN 9',
      subject: 'Toán',
      grade: '9',
      topic: 'BÀI 12. MỘT SỐ HỆ THỨC GIỮA CẠNH, GÓC TRONG TAM GIÁC VUÔNG VÀ ỨNG DỤNG (3 TIẾT)',
      ppct: 'Tiết 4, 5, 6 — Tuần 4, 5, 6',
      duration: '03 tiết (135 phút)',
      bookSeries: 'Kết nối tri thức với cuộc sống'
    },
    illustrations: [
      loadIll('hinh_sgk_4_11_lau_dai', 'Hình 4.11. Đo chiều cao tòa lâu đài cổ xưa', 'hinh_sgk_4_11_lau_dai.png', 500, 225),
      loadIll('hinh-bai12-tam-giac-vuong-he-thuc', 'Hệ thức giữa cạnh và góc trong tam giác vuông', 'hinh_bai12_tam_giac_vuong_he_thuc.png', 520, 300),
      loadIll('hinh-bai12-goc-nang-goc-ha', 'Khái niệm góc nâng và góc hạ trong đo đạc', 'hinh_bai12_goc_nang_goc_ha.png', 500, 250),
      loadIll('hinh-bai12-do-chieu-cao-thuc-te', 'Mô hình toán học: Đo chiều cao tòa tháp / lâu đài', 'hinh_bai12_do_chieu_cao_thuc_te.png', 500, 290),
      loadIll('hinh_sgk_4_14_chiec_thang', 'Hình 4.14. Mô hình chiếc thang dựa tường', 'hinh_sgk_4_14_chiec_thang.png', 320, 277),
      loadIll('hinh_sgk_4_18_bong_cay', 'Hình 4.18. Bài toán bóng cây trong nắng', 'hinh_sgk_4_18_bong_cay.png', 350, 280),
      loadIll('hinh_sgk_4_22_xe_cho_rac', 'Hình 4.22. Mô hình góc nghiêng thùng xe chở rác', 'hinh_sgk_4_22_xe_cho_rac.png', 350, 275),
      loadIll('hinh_sgk_4_23_mai_nha_kho', 'Hình 4.23. Mái dốc nhà kho', 'hinh_sgk_4_23_mai_nha_kho.png', 450, 250)
    ].filter(Boolean)
  },
  {
    fileName: 'KHBD_02_Toan9_LuyenTapChung_Tiet7.docx',
    mdPath: path.resolve(__dirname, 'BAI_02.md'),
    info: {
      schoolName: 'TRƯỜNG THCS TRẦN PHÚ',
      subjectGroup: 'TỔ TOÁN - TIN HỌC',
      teacherName: 'GIÁO VIÊN TOÁN 9',
      subject: 'Toán',
      grade: '9',
      topic: 'BÀI 12. MỘT SỐ HỆ THỨC GIỮA CẠNH, GÓC TRONG TAM GIÁC VUÔNG VÀ ỨNG DỤNG (TIẾT 7: LUYỆN TẬP CHUNG)',
      ppct: 'Tiết 7 — Tuần 7',
      duration: '01 tiết (45 phút)',
      bookSeries: 'Kết nối tri thức với cuộc sống'
    },
    illustrations: [
      loadIll('mindmap-toan9-chuong4-he-thuc-luong', 'Sơ đồ tư duy: Hệ thống kiến thức Bài 11 & Bài 12', 'mindmap_toan9_chuong4_he_thuc_luong.png', 520, 305),
      loadIll('hinh_sgk_4_26_buc_tuong_hinh_thang', 'Hình 4.26. Mặt cắt bức tường hình thang', 'hinh_sgk_4_26_buc_tuong_hinh_thang.png', 350, 280),
      loadIll('hinh_sgk_4_25_tam_giac_vuong', 'Hình 4.25. Tam giác vuông kích thước trang sách', 'hinh_sgk_4_25_tam_giac_vuong.png', 360, 200),
      loadIll('hinh_sgk_4_27_dong_song', 'Hình 4.27. Đo khoảng cách khúc sông', 'hinh_sgk_4_27_dong_song.png', 350, 268),
      loadIll('hinh_sgk_4_29_ho_nuoc', 'Hình 4.29. Đo khoảng cách AB qua hồ nước', 'hinh_sgk_4_29_ho_nuoc.png', 360, 240),
      loadIll('hinh_sgk_4_31_tau_ngam', 'Hình 4.31. Quỹ đạo lặn của tàu ngầm', 'hinh_sgk_4_31_tau_ngam.png', 360, 243)
    ].filter(Boolean)
  },
  {
    fileName: 'KHBD_03_Toan9_BaiTapCuoiChuong4_Tiet8.docx',
    mdPath: path.resolve(__dirname, 'BAI_03.md'),
    info: {
      schoolName: 'TRƯỜNG THCS TRẦN PHÚ',
      subjectGroup: 'TỔ TOÁN - TIN HỌC',
      teacherName: 'GIÁO VIÊN TOÁN 9',
      subject: 'Toán',
      grade: '9',
      topic: 'BÀI TẬP CUỐI CHƯƠNG IV (1 TIẾT)',
      ppct: 'Tiết 8 — Tuần 7',
      duration: '01 tiết (45 phút)',
      bookSeries: 'Kết nối tri thức với cuộc sống'
    },
    illustrations: [
      loadIll('hinh_sgk_4_32_trac_nghiem', 'Hình 4.32. Tam giác vuông ABC cho bài trắc nghiệm 4.21', 'hinh_sgk_4_32_trac_nghiem.png', 320, 215),
      loadIll('mindmap-toan9-chuong4-tong-hop', 'Sơ đồ tư duy: Tổng hợp toàn bộ Chương IV (Hệ thức lượng)', 'mindmap_toan9_chuong4_tong_hop.png', 520, 312),
      loadIll('hinh_sgk_4_35_tup_leu', 'Hình 4.35. Mô hình túp lều hình tam giác cân', 'hinh_sgk_4_35_tup_leu.png', 500, 142),
      loadIll('hinh_sgk_4_36_cay_gay', 'Hình 4.36. Bài toán cây gãy dựa tường', 'hinh_sgk_4_36_cay_gay.png', 500, 208),
      loadIll('hinh_sgk_4_38_trai_dat', 'Hình 4.38. Phương pháp đo chu vi Trái Đất của Eratosthenes', 'hinh_sgk_4_38_trai_dat.png', 350, 370)
    ].filter(Boolean)
  },
  {
    fileName: 'KHBD_04_Toan9_Bai13_MoDauVeDuongTron_Tiet9-10.docx',
    mdPath: path.resolve(__dirname, 'BAI_04.md'),
    info: {
      schoolName: 'TRƯỜNG THCS TRẦN PHÚ',
      subjectGroup: 'TỔ TOÁN - TIN HỌC',
      teacherName: 'GIÁO VIÊN TOÁN 9',
      subject: 'Toán',
      grade: '9',
      topic: 'BÀI 13. MỞ ĐẦU VỀ ĐƯỜNG TRÒN (2 TIẾT)',
      ppct: 'Tiết 9, 10 — Tuần 8',
      duration: '02 tiết (90 phút)',
      bookSeries: 'Kết nối tri thức với cuộc sống'
    },
    illustrations: [
      loadIll('hinh-bai13-duong-tron-vi-tri-diem', 'Đường tròn và vị trí tương đối của điểm', 'hinh_bai13_duong_tron_vi_tri_diem.png', 520, 304),
      loadIll('hinh_sgk_5_1_vi_tri_diem', 'Hình 5.1. Vị trí của điểm đối với đường tròn', 'hinh_sgk_5_1_vi_tri_diem.png', 320, 270),
      loadIll('hinh_sgk_5_2_duong_kinh_ab', 'Hình 5.2. Đường kính AB của đường tròn', 'hinh_sgk_5_2_duong_kinh_ab.png', 320, 246),
      loadIll('hinh-bai13-tam-va-truc-doi-xung', 'Tính đối xứng của đường tròn: Tâm và trục đối xứng', 'hinh_bai13_tam_va_truc_doi_xung.png', 520, 304),
      loadIll('hinh_sgk_5_3_doi_xung_tam', 'Hình 5.3. Tính đối xứng tâm của đường tròn', 'hinh_sgk_5_3_doi_xung_tam.png', 500, 137),
      loadIll('hinh_sgk_5_4_doi_xung_truc', 'Hình 5.4. Tính đối xứng trục của đường tròn', 'hinh_sgk_5_4_doi_xung_truc.png', 500, 142)
    ].filter(Boolean)
  }
];

async function runBatch() {
  console.log('=== BẮT ĐẦU QUY TRÌNH XUẤT 4 KHBD TOÁN 9 (CHƯƠNG IV & CHƯƠNG V) ===');
  const results = [];

  for (let i = 0; i < lessons.length; i++) {
    const l = lessons[i];
    console.log(`\n[${i + 1}/${lessons.length}] Đang xử lý: ${l.info.topic}...`);

    const outputDocxPath = path.join(KET_QUA_DIR, l.fileName);

    try {
      const res = await createKhbdDocx({
        mdFilePath: l.mdPath,
        outputDocxPath: outputDocxPath,
        lessonInfo: l.info,
        illustrations: l.illustrations
      });

      console.log(` -> THÀNH CÔNG: ${path.basename(res.path)} (${res.size} bytes)`);
      results.push({ success: true, file: path.basename(res.path), size: res.size });
    } catch (err) {
      console.error(` -> LỖI: ${l.fileName}`, err);
      results.push({ success: false, file: l.fileName, error: err.message });
    }
  }

  // Dọn dẹp các file md tạm trong tools
  ['BAI_01.md', 'BAI_02.md', 'BAI_03.md', 'BAI_04.md'].forEach(f => {
    const p = path.resolve(__dirname, f);
    if (fs.existsSync(p)) fs.unlinkSync(p);
  });
  const jsContentPath = path.resolve(__dirname, 'khbd_content_toan9_chuong4_5.js');
  if (fs.existsSync(jsContentPath)) fs.unlinkSync(jsContentPath);

  // Dọn dẹp temp_scans_new và temp_render_crops
  const tempScansNew = path.resolve(__dirname, 'temp_scans_new');
  if (fs.existsSync(tempScansNew)) {
    fs.rmSync(tempScansNew, { recursive: true, force: true });
    console.log('-> Đã xóa sạch thư mục quét ảnh tạm thời tools/temp_scans_new/.');
  }
  const tempRenderCrops = path.resolve(__dirname, 'temp_render_crops');
  if (fs.existsSync(tempRenderCrops)) {
    fs.rmSync(tempRenderCrops, { recursive: true, force: true });
    console.log('-> Đã xóa sạch thư mục render ảnh tạm tools/temp_render_crops/.');
  }

  // Quét dọn tuyệt đối Ket_qua: không để bất kỳ file .md hay ảnh rác nào sót lại
  const ketQuaFiles = fs.readdirSync(KET_QUA_DIR);
  for (const f of ketQuaFiles) {
    if (f.endsWith('.md') || f.endsWith('.png') || f.endsWith('.jpg') || f.endsWith('.txt')) {
      fs.unlinkSync(path.join(KET_QUA_DIR, f));
      console.log(`-> Đã dọn file trung gian trong Ket_qua: ${f}`);
    }
  }

  console.log('\n=== KẾT QUẢ XUẤT TRỌN BỘ 4 KHBD ===');
  results.forEach(r => {
    console.log(`- ${r.file}: ${r.success ? 'PASS (' + r.size + ' bytes)' : 'FAIL: ' + r.error}`);
  });
}

runBatch().catch(console.error);
