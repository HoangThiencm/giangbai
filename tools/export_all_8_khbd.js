/**
 * Export tất cả 8 Kế hoạch bài dạy sang Word .docx
 */

const fs = require('fs');
const path = require('path');
const { createKhbdDocx } = require('../TROLYTHIEN/engine/export_khbd_engine.js');

const KET_QUA_DIR = path.resolve(__dirname, '../TROLYTHIEN/1_SOAN_KHBD/Ket_qua');

const lessons = [
  {
    fileName: 'KHBD_01_Toan6_LuyenTapChung_Tiet12',
    info: {
      schoolName: 'TRƯỜNG THCS TRẦN PHÚ',
      subjectGroup: 'TỔ TOÁN - TIN HỌC',
      teacherName: 'GIÁO VIÊN TOÁN 6',
      subject: 'Toán',
      grade: '6',
      topic: 'BÀI 7. THỨ TỰ THỰC HIỆN CÁC PHÉP TÍNH (TIẾT 12: LUYỆN TẬP CHUNG)',
      ppct: 'Tiết 12 — Tuần 4',
      duration: '01 tiết (45 phút)',
      bookSeries: 'Kết nối tri thức với cuộc sống'
    }
  },
  {
    fileName: 'KHBD_02_Toan6_BaiTapCuoiChuong1_Tiet13',
    info: {
      schoolName: 'TRƯỜNG THCS TRẦN PHÚ',
      subjectGroup: 'TỔ TOÁN - TIN HỌC',
      teacherName: 'GIÁO VIÊN TOÁN 6',
      subject: 'Toán',
      grade: '6',
      topic: 'BÀI TẬP CUỐI CHƯƠNG I (TIẾT 13: ÔN TẬP VÀ GIẢI BÀI TẬP)',
      ppct: 'Tiết 13 — Tuần 5',
      duration: '01 tiết (45 phút)',
      bookSeries: 'Kết nối tri thức với cuộc sống'
    }
  },
  {
    fileName: 'KHBD_03_Toan6_Bai8_QuanHeChiaHetVaTinhChat_Tiet14-15',
    info: {
      schoolName: 'TRƯỜNG THCS TRẦN PHÚ',
      subjectGroup: 'TỔ TOÁN - TIN HỌC',
      teacherName: 'GIÁO VIÊN TOÁN 6',
      subject: 'Toán',
      grade: '6',
      topic: 'BÀI 8. QUAN HỆ CHIA HẾT VÀ TÍNH CHẤT (2 TIẾT)',
      ppct: 'Tiết 14, 15 — Tuần 5',
      duration: '02 tiết (90 phút)',
      bookSeries: 'Kết nối tri thức với cuộc sống'
    }
  },
  {
    fileName: 'KHBD_04_Toan6_Bai9_DauHieuChiaHet_Tiet16-17',
    info: {
      schoolName: 'TRƯỜNG THCS TRẦN PHÚ',
      subjectGroup: 'TỔ TOÁN - TIN HỌC',
      teacherName: 'GIÁO VIÊN TOÁN 6',
      subject: 'Toán',
      grade: '6',
      topic: 'BÀI 9. DẤU HIỆU CHIA HẾT (2 TIẾT)',
      ppct: 'Tiết 16, 17 — Tuần 6',
      duration: '02 tiết (90 phút)',
      bookSeries: 'Kết nối tri thức với cuộc sống'
    }
  },
  {
    fileName: 'KHBD_05_Toan6_Bai10_SoNguyenTo_Tiet18-19',
    info: {
      schoolName: 'TRƯỜNG THCS TRẦN PHÚ',
      subjectGroup: 'TỔ TOÁN - TIN HỌC',
      teacherName: 'GIÁO VIÊN TOÁN 6',
      subject: 'Toán',
      grade: '6',
      topic: 'BÀI 10. SỐ NGUYÊN TỐ (2 TIẾT)',
      ppct: 'Tiết 18, 19 — Tuần 6, 7',
      duration: '02 tiết (90 phút)',
      bookSeries: 'Kết nối tri thức với cuộc sống'
    }
  },
  {
    fileName: 'KHBD_06_Toan6_LuyenTapChung_Tiet20',
    info: {
      schoolName: 'TRƯỜNG THCS TRẦN PHÚ',
      subjectGroup: 'TỔ TOÁN - TIN HỌC',
      teacherName: 'GIÁO VIÊN TOÁN 6',
      subject: 'Toán',
      grade: '6',
      topic: 'CHƯƠNG II: TÍNH CHIA HẾT TRONG TẬP HỢP CÁC SỐ TỰ NHIÊN (TIẾT 20: LUYỆN TẬP CHUNG)',
      ppct: 'Tiết 20 — Tuần 7',
      duration: '01 tiết (45 phút)',
      bookSeries: 'Kết nối tri thức với cuộc sống'
    }
  },
  {
    fileName: 'KHBD_07_Toan6_Bai11_UocChung_UocChungLonNhat_Tiet21-22',
    info: {
      schoolName: 'TRƯỜNG THCS TRẦN PHÚ',
      subjectGroup: 'TỔ TOÁN - TIN HỌC',
      teacherName: 'GIÁO VIÊN TOÁN 6',
      subject: 'Toán',
      grade: '6',
      topic: 'BÀI 11. ƯỚC CHUNG. ƯỚC CHUNG LỚN NHẤT (2 TIẾT)',
      ppct: 'Tiết 21, 22 — Tuần 7, 8',
      duration: '02 tiết (90 phút)',
      bookSeries: 'Kết nối tri thức với cuộc sống'
    }
  },
  {
    fileName: 'KHBD_08_Toan6_Bai12_BoiChung_BoiChungNhoNhat_Tiet23-24',
    info: {
      schoolName: 'TRƯỜNG THCS TRẦN PHÚ',
      subjectGroup: 'TỔ TOÁN - TIN HỌC',
      teacherName: 'GIÁO VIÊN TOÁN 6',
      subject: 'Toán',
      grade: '6',
      topic: 'BÀI 12. BỘI CHUNG. BỘI CHUNG NHỎ NHẤT (2 TIẾT)',
      ppct: 'Tiết 23, 24 — Tuần 8',
      duration: '02 tiết (90 phút)',
      bookSeries: 'Kết nối tri thức với cuộc sống'
    }
  }
];

const HINH_DIR = path.resolve(__dirname, '../TROLYTHIEN/engine/hinh_ve_sgk');

function loadIll(id, caption, filename, width, height) {
  const p = path.join(HINH_DIR, filename);
  if (!fs.existsSync(p)) return null;
  const b64 = fs.readFileSync(p).toString('base64');
  return {
    id,
    caption,
    dataUrl: `data:image/png;base64,${b64}`,
    width,
    height
  };
}

const allIllustrations = [
  loadIll('mindmap-01-thu-tu-phep-tinh', 'Sơ đồ tư duy Thứ tự thực hiện các phép tính', 'mindmap_01_thu_tu_phep_tinh.png', 480, 230),
  loadIll('mindmap-02-tong-hop-chuong-1', 'Sơ đồ tư duy Tổng hợp kiến thức Chương I', 'mindmap_02_tong_hop_chuong_1.png', 480, 240),
  loadIll('hinh-05-so-do-phan-tich', 'Sơ đồ cây và Sơ đồ cột dọc phân tích ra thừa số nguyên tố (SGK Toán 6)', 'so_do_cay_va_cot_so_nguyen_to.png', 480, 215),
  loadIll('mindmap-06-so-nguyen-to', 'Sơ đồ tư duy Số nguyên tố - Hợp số - Phân tích thừa số nguyên tố', 'mindmap_06_so_nguyen_to.png', 480, 230)
].filter(Boolean);

async function run() {
  console.log('--- BẮT ĐẦU XUẤT 8 BÀI WORD KHBD CHUẨN CV 5512 V2.0 ---');
  for (let i = 0; i < lessons.length; i++) {
    const item = lessons[i];
    const mdPath = path.join(KET_QUA_DIR, item.fileName + '.md');
    const docxPath = path.join(KET_QUA_DIR, item.fileName + '.docx');
    console.log(`Đang xử lý [${i + 1}/8]: ${item.fileName}...`);
    const res = await createKhbdDocx({
      mdFilePath: mdPath,
      outputDocxPath: docxPath,
      lessonInfo: item.info,
      illustrations: allIllustrations
    });
    if (/_Moi\.docx$/i.test(res.path)) {
      console.warn(`CẢNH BÁO: ${item.fileName}.docx đang bị Word khóa. Đã ghi ${path.basename(res.path)}. Đóng Word rồi chạy lại.`);
    }
    console.log(`=> THÀNH CÔNG: ${path.basename(res.path)} (${res.size} bytes)`);
  }
  console.log('--- HOÀN TẤT TRỌN VẸN 8/8 BÀI GIẢNG KHBD WORD ---');
}

run().catch(err => {
  console.error('Lỗi xuất file:', err);
  process.exit(1);
});
