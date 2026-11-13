const fs = require('fs');
const path = require('path');
const { createKhbdDocx } = require('../../engine/export_khbd_engine.js');

const imgDir = path.resolve(__dirname, '../../1_SOAN_KHBD/Dau_vao/03.11/NCBH_DINH_LY_THALES_TOAN_8/images');

function loadImg(filename, id, w, h) {
  const p = path.join(imgDir, filename);
  if (!fs.existsSync(p)) {
    console.error(`Image not found: ${p}`);
    return null;
  }
  const buf = fs.readFileSync(p);
  return {
    id: id,
    dataUrl: 'data:image/png;base64,' + buf.toString('base64'),
    width: w,
    height: h
  };
}

const illustrations = [
  loadImg('hinh_0_kim_tu_thap_kheops.png', 'hinh_0_kim_tu_thap_kheops', 360, 155),
  loadImg('hinh_hd1_doan_thang_ti_le.png', 'hinh_hd1_doan_thang_ti_le', 300, 165),
  loadImg('hinh_1_tam_giac_thales_luoi.png', 'hinh_1_tam_giac_thales_luoi', 250, 230),
  loadImg('hinh_2_dinh_ly_thales_tong_quat.png', 'hinh_2_dinh_ly_thales_tong_quat', 250, 230),
  loadImg('hinh_luyen_tap_1_thales.png', 'hinh_luyen_tap_1_thales', 250, 190),
  loadImg('hinh_luyen_tap_2_thales.png', 'hinh_luyen_tap_2_thales', 270, 190),
  loadImg('hinh_3_ung_dung_thales_do_bong_nang.png', 'hinh_3_ung_dung_thales_do_bong_nang', 320, 205)
].filter(Boolean);

console.log('Loaded', illustrations.length, 'illustrations:');
illustrations.forEach(ill => console.log(' -', ill.id, `${ill.width}x${ill.height}`));

const mdFilePath = path.resolve(__dirname, '../../1_SOAN_KHBD/Ket_qua/03.11/KHBD_Toan8_Bai15_DinhLiThales_Tiet16_NCBH.md');
const outputDocxPath = path.resolve(__dirname, '../../1_SOAN_KHBD/Ket_qua/03.11/KHBD_Toan8_Bai15_DinhLiThales_Tiet16_NCBH.docx');

const lessonInfo = {
  subject: "Toán",
  grade: "8",
  lessonScope: "Tiết 16",
  lessonTitle: "ĐỊNH LÍ THALÈS TRONG TAM GIÁC",
  duration: "01 tiết (45 phút) - Tiết dạy minh họa Nghiên cứu bài học"
};

createKhbdDocx({
  mdFilePath,
  outputDocxPath,
  lessonInfo,
  illustrations
}).then(res => {
  console.log('SUCCESS! Word document generated at:', res.path, 'Size:', res.size, 'bytes');
}).catch(err => {
  console.error('ERROR during docx generation:', err);
  process.exit(1);
});
