const fs = require('fs');
const path = require('path');
const { createKhbdDocx } = require('../../engine/export_khbd_engine');

async function exportBai11() {
  const tempDir = path.resolve(__dirname);
  const illDir = path.join(tempDir, 'illustrations');
  const outDir = path.resolve(__dirname, '../../1_SOAN_KHBD/Ket_qua/HK2/TIN6');

  if (!fs.existsSync(outDir)) {
    fs.mkdirSync(outDir, { recursive: true });
  }

  const mdPath = path.join(tempDir, '03_KHBD_Tin6_Bai11_DinhDangVanBan_Tiet22-23.md');
  const outPath = path.join(outDir, '03_KHBD_Tin6_Bai11_DinhDangVanBan_Tiet22-23.docx');

  // Load illustrations
  const illustrations = [];
  
  const img1 = path.join(illDir, 'hinh_dinhdang_paragraph_5_4.png');
  if (fs.existsSync(img1)) {
    illustrations.push({
      id: 'hinh-dinhdang-paragraph-5-4',
      dataUrl: `data:image/png;base64,${fs.readFileSync(img1).toString('base64')}`,
      width: 520,
      height: 120,
      caption: 'Các lệnh định dạng đoạn văn bản nhóm Paragraph'
    });
  }

  const img2 = path.join(illDir, 'hinh_baiviet_an_5_8.png');
  if (fs.existsSync(img2)) {
    illustrations.push({
      id: 'hinh-baiviet-an-5-8',
      dataUrl: `data:image/png;base64,${fs.readFileSync(img2).toString('base64')}`,
      width: 420,
      height: 380,
      caption: 'Bài viết cảm nghĩ của bạn An được định dạng hoàn chỉnh'
    });
  }

  const img3 = path.join(illDir, 'hinh_setup_trang_5_9_10.png');
  if (fs.existsSync(img3)) {
    illustrations.push({
      id: 'hinh-setup-trang-5-9_10',
      dataUrl: `data:image/png;base64,${fs.readFileSync(img3).toString('base64')}`,
      width: 480,
      height: 320,
      caption: 'Các thao tác thiết lập hướng trang và lề trang trong Page Setup'
    });
  }

  const lessonInfo = {
    topic: "BÀI 11: ĐỊNH DẠNG VĂN BẢN",
    ppct: "TIẾT 22, 23",
    lessonScope: "TIẾT 22, 23",
    duration: "02 tiết (90 phút)"
  };

  const res = await createKhbdDocx({
    mdFilePath: mdPath,
    outputDocxPath: outPath,
    illustrations: illustrations,
    lessonInfo: lessonInfo
  });

  console.log(`Đã xuất thành công: ${outPath} (${res.size} bytes)`);
}

exportBai11().catch(console.error);
