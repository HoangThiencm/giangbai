const fs = require('fs');
const path = require('path');
const { createKhbdDocx } = require('../../engine/export_khbd_engine');

async function exportBai09() {
  const tempDir = path.resolve(__dirname);
  const illDir = path.join(tempDir, 'illustrations');
  const outDir = path.resolve(__dirname, '../../1_SOAN_KHBD/Ket_qua/HK2/TIN6');

  if (!fs.existsSync(outDir)) {
    fs.mkdirSync(outDir, { recursive: true });
  }

  const mdPath = path.join(tempDir, '01_KHBD_Tin6_Bai09_AnToanThongTinTrenInternet_Tiet19.md');
  const outPath = path.join(outDir, '01_KHBD_Tin6_Bai09_AnToanThongTinTrenInternet_Tiet19.docx');

  // Load illustrations
  const illustrations = [];
  
  const virusImgPath = path.join(illDir, 'hinh_virus_tiet19.png');
  if (fs.existsSync(virusImgPath)) {
    const b64 = fs.readFileSync(virusImgPath).toString('base64');
    illustrations.push({
      id: 'hinh-virus-tiet19',
      dataUrl: `data:image/png;base64,${b64}`,
      width: 320,
      height: 300,
      caption: 'Minh họa máy tính bị nhiễm virus và mã độc khi tải tệp lạ'
    });
  }

  const hackerImgPath = path.join(illDir, 'hinh_hacker_tiet19.png');
  if (fs.existsSync(hackerImgPath)) {
    const b64 = fs.readFileSync(hackerImgPath).toString('base64');
    illustrations.push({
      id: 'hinh-hacker-tiet19',
      dataUrl: `data:image/png;base64,${b64}`,
      width: 280,
      height: 280,
      caption: 'Minh họa nguy cơ kẻ xấu tấn công đánh cắp thông tin cá nhân'
    });
  }

  const lessonInfo = {
    topic: "BÀI 9: AN TOÀN THÔNG TIN TRÊN INTERNET",
    ppct: "TIẾT 19",
    lessonScope: "TIẾT 19",
    duration: "01 tiết (45 phút)"
  };

  const res = await createKhbdDocx({
    mdFilePath: mdPath,
    outputDocxPath: outPath,
    illustrations: illustrations,
    lessonInfo: lessonInfo
  });

  console.log(`Đã xuất thành công: ${outPath} (${res.size} bytes)`);
}

exportBai09().catch(console.error);
