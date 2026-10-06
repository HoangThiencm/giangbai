// -*- coding: utf-8 -*-
/**
 * Export 4 Kế hoạch bài dạy (KHBD) Toán 9 Chương II sang Word .docx
 */
const fs = require('fs');
const path = require('path');
const { createKhbdDocx } = require('../TROLYTHIEN/engine/export_khbd_engine.js');
const { BAI_01_MD, BAI_02_MD, BAI_03_MD, BAI_04_MD } = require('./khbd_content_toan9.js');

const KET_QUA_DIR = path.resolve(__dirname, '../TROLYTHIEN/1_SOAN_KHBD/Ket_qua');
const HINH_DIR = path.resolve(__dirname, '../TROLYTHIEN/engine/hinh_ve_sgk');
const TEMP_DIR = path.resolve(__dirname, 'temp_export');

if (!fs.existsSync(TEMP_DIR)) {
  fs.mkdirSync(TEMP_DIR, { recursive: true });
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
    fileName: 'KHBD_01_Toan9_Bai5_BatDangThucVaTinhChat_Tiet15-17.docx',
    mdContent: BAI_01_MD,
    info: {
      schoolName: 'TRƯỜNG THCS TRẦN PHÚ',
      subjectGroup: 'TỔ TOÁN - TIN HỌC',
      teacherName: 'GIÁO VIÊN TOÁN 9',
      subject: 'Toán',
      grade: '9',
      topic: 'BÀI 5: BẤT ĐẲNG THỨC VÀ TÍNH CHẤT (3 TIẾT)',
      ppct: 'Tiết 15, 16, 17 — Tuần 5, 6',
      duration: '03 tiết (135 phút)',
      bookSeries: 'Kết nối tri thức với cuộc sống'
    },
    illustrations: []
  },
  {
    fileName: 'KHBD_02_Toan9_LuyenTapChung_Tiet18.docx',
    mdContent: BAI_02_MD,
    info: {
      schoolName: 'TRƯỜNG THCS TRẦN PHÚ',
      subjectGroup: 'TỔ TOÁN - TIN HỌC',
      teacherName: 'GIÁO VIÊN TOÁN 9',
      subject: 'Toán',
      grade: '9',
      topic: 'BÀI 5: BẤT ĐẲNG THỨC VÀ TÍNH CHẤT (TIẾT 18: LUYỆN TẬP CHUNG)',
      ppct: 'Tiết 18 — Tuần 6',
      duration: '01 tiết (45 phút)',
      bookSeries: 'Kết nối tri thức với cuộc sống'
    },
    illustrations: [
      loadIll('mindmap-toan9-chuong2-bai5', 'Sơ đồ tư duy Bất đẳng thức và tính chất', 'mindmap_toan9_chuong2_bai5.png', 500, 248)
    ].filter(Boolean)
  },
  {
    fileName: 'KHBD_03_Toan9_Bai6_BatPhuongTrinhBacNhatMotAn_Tiet19-20.docx',
    mdContent: BAI_03_MD,
    info: {
      schoolName: 'TRƯỜNG THCS TRẦN PHÚ',
      subjectGroup: 'TỔ TOÁN - TIN HỌC',
      teacherName: 'GIÁO VIÊN TOÁN 9',
      subject: 'Toán',
      grade: '9',
      topic: 'BÀI 6: BẤT PHƯƠNG TRÌNH BẬC NHẤT MỘT ẨN (2 TIẾT)',
      ppct: 'Tiết 19, 20 — Tuần 7',
      duration: '02 tiết (90 phút)',
      bookSeries: 'Kết nối tri thức với cuộc sống'
    },
    illustrations: []
  },
  {
    fileName: 'KHBD_04_Toan9_BaiTapCuoiChuong2_Tiet21-22.docx',
    mdContent: BAI_04_MD,
    info: {
      schoolName: 'TRƯỜNG THCS TRẦN PHÚ',
      subjectGroup: 'TỔ TOÁN - TIN HỌC',
      teacherName: 'GIÁO VIÊN TOÁN 9',
      subject: 'Toán',
      grade: '9',
      topic: 'BÀI TẬP CUỐI CHƯƠNG II (2 TIẾT)',
      ppct: 'Tiết 21, 22 — Tuần 8',
      duration: '02 tiết (90 phút)',
      bookSeries: 'Kết nối tri thức với cuộc sống'
    },
    illustrations: [
      loadIll('mindmap-toan9-chuong2-tong-hop', 'Sơ đồ tư duy Tổng hợp Chương II', 'mindmap_toan9_chuong2_tong_hop.png', 500, 252)
    ].filter(Boolean)
  }
];

async function runBatch() {
  console.log('=== BẮT ĐẦU QUY TRÌNH XUẤT 4 KHBD TOÁN 9 CHƯƠNG II ===');
  const results = [];

  for (let i = 0; i < lessons.length; i++) {
    const l = lessons[i];
    console.log(`\n[${i + 1}/${lessons.length}] Đang xử lý: ${l.info.topic}...`);

    const tempMdPath = path.join(TEMP_DIR, `temp_${i + 1}.md`);
    fs.writeFileSync(tempMdPath, l.mdContent, 'utf8');

    const outputDocxPath = path.join(KET_QUA_DIR, l.fileName);

    try {
      const res = await createKhbdDocx({
        mdFilePath: tempMdPath,
        outputDocxPath: outputDocxPath,
        lessonInfo: l.info,
        illustrations: l.illustrations
      });

      console.log(` -> THÀNH CÔNG: ${path.basename(res.path)} (${res.size} bytes)`);
      results.push({ success: true, file: path.basename(res.path), size: res.size });
    } catch (err) {
      console.error(` -> LỖI: ${l.fileName}`, err);
      results.push({ success: false, file: l.fileName, error: err.message });
    } finally {
      if (fs.existsSync(tempMdPath)) {
        fs.unlinkSync(tempMdPath);
      }
    }
  }

  // Dọn dẹp thư mục tạm
  if (fs.existsSync(TEMP_DIR)) {
    fs.rmSync(TEMP_DIR, { recursive: true, force: true });
  }

  // Dọn dẹp temp_scans nếu có
  const tempScansDir = path.resolve(__dirname, '../TROLYTHIEN/1_SOAN_KHBD/Dau_vao/temp_scans');
  if (fs.existsSync(tempScansDir)) {
    fs.rmSync(tempScansDir, { recursive: true, force: true });
    console.log('-> Đã xóa sạch thư mục quét ảnh tạm thời temp_scans/.');
  }

  // Quét dọn tuyệt đối Ket_qua: không để bất kỳ file .md hay ảnh rác nào sót lại
  const ketQuaFiles = fs.readdirSync(KET_QUA_DIR);
  for (const f of ketQuaFiles) {
    if (f.endsWith('.md') || f.endsWith('.png') || f.endsWith('.jpg')) {
      fs.unlinkSync(path.join(KET_QUA_DIR, f));
      console.log(`-> Đã dọn file rác: ${f}`);
    }
  }

  console.log('\n=== KẾT QUẢ XUẤT BATCH LOOP ===');
  results.forEach(r => {
    console.log(`- ${r.file}: ${r.success ? 'PASS (' + r.size + ' bytes)' : 'FAIL: ' + r.error}`);
  });
}

runBatch().catch(console.error);
