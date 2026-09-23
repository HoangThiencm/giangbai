const fs = require('fs');
const path = require('path');
const { createKhbdDocx } = require('./export_khbd_engine.js');

function getImgDataUrl(imgPath) {
  const buf = fs.readFileSync(imgPath);
  return 'data:image/png;base64,' + buf.toString('base64');
}

const illustrations = [
  {
    id: 'hinh-3.40',
    dataUrl: getImgDataUrl(path.join(__dirname, 'hinh_ve_sgk/hinh_3_40.png')),
    width: 400,
    height: 210
  },
  {
    id: 'hinh-3.41',
    dataUrl: getImgDataUrl(path.join(__dirname, 'hinh_ve_sgk/hinh_3_41.png')),
    width: 460,
    height: 140
  },
  {
    id: 'hinh-3.42',
    dataUrl: getImgDataUrl(path.join(__dirname, 'hinh_ve_sgk/hinh_3_42.png')),
    width: 380,
    height: 180
  },
  {
    id: 'hinh-3.44',
    dataUrl: getImgDataUrl(path.join(__dirname, 'hinh_ve_sgk/hinh_3_44.png')),
    width: 380,
    height: 190
  },
  {
    id: 'hinh-3.45',
    dataUrl: getImgDataUrl(path.join(__dirname, 'hinh_ve_sgk/hinh_3_45.png')),
    width: 380,
    height: 180
  },
  {
    id: 'hinh-bai-3.27',
    dataUrl: getImgDataUrl(path.join(__dirname, 'hinh_ve_sgk/hinh_bai_3_27.png')),
    width: 380,
    height: 190
  },
  {
    id: 'hinh-bai-3.28',
    dataUrl: getImgDataUrl(path.join(__dirname, 'hinh_ve_sgk/hinh_bai_3_28.png')),
    width: 360,
    height: 195
  }
];

const lessonInfo = {
  school: 'TRƯỜNG THCS .....................................................',
  teacher: '.....................................................',
  chapter: 'Chương III: Tứ giác',
  topic: 'Bài 13: Hình chữ nhật',
  lessonScope: 'Tiết 8, 9 (Tuần 4 – 5)',
  duration: '02 tiết (90 phút)',
  subject: 'Toán',
  academicYear: '2026-2027'
};

const mdFilePath = path.join(__dirname, 'KHBD_Toan8_Bai13_HinhChuNhat.md');
const outputDocxPath = path.join(__dirname, 'KHBD_Toan8_Bai13_HinhChuNhat.docx');

createKhbdDocx({
  mdFilePath,
  outputDocxPath,
  lessonInfo,
  illustrations
}).then(res => {
  console.log('SUCCESS: Generated KHBD Docx:', res.path, `(${res.size} bytes)`);
}).catch(err => {
  console.error('ERROR generating KHBD Docx:', err);
  process.exit(1);
});
