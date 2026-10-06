const fs = require('fs');
const path = require('path');
const { createKhbdDocx } = require('../TROLYTHIEN/engine/export_khbd_engine.js');

const KET_QUA_DIR = path.resolve(__dirname, '../TROLYTHIEN/1_SOAN_KHBD/Ket_qua');
const HINH_DIR = path.resolve(__dirname, '../TROLYTHIEN/engine/hinh_ve_sgk');

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

const illustrations = [
  loadIll('hinh-01-cong-thuc-3-hinh', 'Công thức chu vi và diện tích hình vuông, hình chữ nhật, hình thang', 'hinh_01_cong_thuc_3_hinh.png', 480, 147),
  loadIll('hinh-02-thua-ruong-luyentap1', 'Thửa ruộng kết hợp hình thang và hình chữ nhật', 'hinh_02_thua_ruong_luyentap1.png', 380, 204),
  loadIll('hinh-03-cat-ghep-hinh-binh-hanh', 'Cắt ghép hình bình hành thành hình chữ nhật', 'hinh_03_cat_ghep_hinh_binh_hanh.png', 480, 145),
  loadIll('hinh-04-cat-ghep-hinh-thoi', 'Cắt ghép hình thoi thành hình chữ nhật', 'hinh_04_cat_ghep_hinh_thoi.png', 480, 151),
  loadIll('hinh-05-luyen-tap-2-manh-dat', 'Mảnh đất trồng hoa và cỏ', 'hinh_05_luyen_tap_2_manh_dat.png', 380, 197),
  loadIll('hinh-06-luyen-tap-3-manh-vuon-hinh-thoi', 'Mảnh vườn có luống hoa hình thoi', 'hinh_06_luyen_tap_3_manh_vuon_hinh_thoi.png', 380, 190),
  loadIll('hinh-07-bai-4-20-mat-san-nha', 'Mặt sàn nhà phân chia các phòng', 'hinh_07_bai_4_20_mat_san_nha.png', 380, 225),
  loadIll('hinh-08-bai-4-21-thua-dat-hinh-thang', 'Thửa đất hình thang vuông ABCD', 'hinh_08_bai_4_21_thua_dat_hinh_thang.png', 380, 190)
].filter(Boolean);

const lessonInfo = {
  schoolName: 'TRƯỜNG THCS TRẦN PHÚ',
  subjectGroup: 'TỔ TOÁN - TIN HỌC',
  teacherName: 'GIÁO VIÊN TOÁN 6',
  subject: 'Toán',
  grade: '6',
  topic: 'BÀI 20: CHU VI VÀ DIỆN TÍCH CỦA MỘT SỐ HÌNH TRONG THỰC TIỄN (3 TIẾT)',
  ppct: 'Tiết 6, 7, 8 — Tuần 6, 7, 8',
  duration: '03 tiết (135 phút)',
  bookSeries: 'Kết nối tri thức với cuộc sống'
};

async function main() {
  const tempMdPath = path.resolve(__dirname, 'temp_bai20.md');
  const docxPath = path.join(KET_QUA_DIR, 'KHBD_Toan6_Bai20_ChuViVaDienTichCuaMotSoHinhTrongThucTien_Tiet6-8.docx');

  // Đọc nội dung Markdown gốc từ tools backup và cập nhật thông tin chuẩn PPCT
  const srcMdPath = path.join(__dirname, 'TROLYTHIEN/1_SOAN_KHBD/Ket_qua/KHBD_Toan6_Bai20_ChuViVaDienTichTuGiac_Tiet34-36.md');
  let mdContent = fs.readFileSync(srcMdPath, 'utf8');

  fs.writeFileSync(tempMdPath, mdContent, 'utf8');

  console.log('Bắt đầu chuyển đổi KHBD Bài 20 sang Word .docx...');
  const res = await createKhbdDocx({
    mdFilePath: tempMdPath,
    outputDocxPath: docxPath,
    lessonInfo: lessonInfo,
    illustrations: illustrations
  });

  console.log(`Xuất thành công: ${res.path} (${res.size} bytes)`);

  // Xóa file tạm
  if (fs.existsSync(tempMdPath)) {
    fs.unlinkSync(tempMdPath);
  }

  // TỰ ĐỘNG DỌN DẸP SẠCH TOÀN BỘ FILE .MD RÁC TRONG KET_QUA CỦA THẦY
  const ketQuaFiles = fs.readdirSync(KET_QUA_DIR);
  for (const f of ketQuaFiles) {
    if (f.endsWith('.md')) {
      const p = path.join(KET_QUA_DIR, f);
      fs.unlinkSync(p);
      console.log(`Đã dọn dẹp file tạm: ${f}`);
    }
  }

  // Xóa file docx cũ sai tên nếu có (phòng khi người dùng đang mở trong Word)
  const oldDocx = path.join(KET_QUA_DIR, 'KHBD_Toan6_Bai20_ChuViVaDienTichTuGiac_Tiet34-36.docx');
  if (fs.existsSync(oldDocx)) {
    try {
      fs.unlinkSync(oldDocx);
      console.log(`Đã xóa file Word cũ: ${path.basename(oldDocx)}`);
    } catch (e) {
      console.log(`File Word cũ đang mở trong Word nên không xóa trực tiếp được.`);
    }
  }
}

main().catch(err => {
  console.error('Lỗi xuất file docx:', err);
  process.exit(1);
});
