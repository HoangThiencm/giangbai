const fs = require('fs');
const path = require('path');
const { createKhbdDocx } = require('../../engine/export_khbd_engine');

async function exportBai10() {
  const tempDir = path.resolve(__dirname);
  const illDir = path.join(tempDir, 'illustrations');
  const outDir = path.resolve(__dirname, '../../1_SOAN_KHBD/Ket_qua/HK2/TIN6');

  if (!fs.existsSync(outDir)) {
    fs.mkdirSync(outDir, { recursive: true });
  }

  const mdPath = path.join(tempDir, '02_KHBD_Tin6_Bai10_SoDoTuDuy_Tiet20-21.md');
  const outPath = path.join(outDir, '02_KHBD_Tin6_Bai10_SoDoTuDuy_Tiet20-21.docx');

  // Load illustrations
  const illustrations = [];
  
  const img1 = path.join(illDir, 'hinh_sodotuduy_5_2.png');
  if (fs.existsSync(img1)) {
    illustrations.push({
      id: 'hinh-sodotuduy-5-2',
      dataUrl: `data:image/png;base64,${fs.readFileSync(img1).toString('base64')}`,
      width: 520,
      height: 280,
      caption: 'Sơ đồ tư duy Hình 5.2 do Tony Buzan sáng tạo'
    });
  }

  const img2 = path.join(illDir, 'hinh_mindmaple_soluuniem.png');
  if (fs.existsSync(img2)) {
    illustrations.push({
      id: 'hinh-mindmaple-soluuniem',
      dataUrl: `data:image/png;base64,${fs.readFileSync(img2).toString('base64')}`,
      width: 540,
      height: 280,
      caption: 'Sơ đồ tư duy Sổ lưu niệm lớp 6A trên phần mềm máy tính'
    });
  }

  const img3 = path.join(illDir, 'hinh_vandung_bai9_mindmap.png');
  if (fs.existsSync(img3)) {
    illustrations.push({
      id: 'hinh-vandung-bai9-mindmap',
      dataUrl: `data:image/png;base64,${fs.readFileSync(img3).toString('base64')}`,
      width: 520,
      height: 280,
      caption: 'Sơ đồ tư duy Vận dụng tóm tắt Bài 9'
    });
  }

  const lessonInfo = {
    topic: "BÀI 10: SƠ ĐỒ TƯ DUY",
    ppct: "TIẾT 20, 21",
    lessonScope: "TIẾT 20, 21",
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

exportBai10().catch(console.error);
