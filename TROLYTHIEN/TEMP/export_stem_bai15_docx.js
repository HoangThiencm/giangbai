const fs = require('fs');
const path = require('path');
const { createKhbdDocx } = require('../engine/export_khbd_engine');

async function main() {
  const mdPath = path.resolve(__dirname, 'KHBD_Toan9_Bai15_STEM_VongQuayHanhDongXanh.md');
  const imgPath = path.resolve(__dirname, 'stem_images/image1.jpeg');

  if (!fs.existsSync(imgPath)) {
    throw new Error('Image not found: ' + imgPath);
  }

  const b64 = fs.readFileSync(imgPath).toString('base64');
  const illustrations = [
    {
      id: 'vong-quay-hanh-dong-xanh',
      dataUrl: `data:image/jpeg;base64,${b64}`,
      width: 520,
      height: 346,
      caption: 'Hình 1: Mô hình thực tế "Vòng quay hành động xanh" hoàn chỉnh của học sinh (Bán kính R = 15 cm, 4 hình quạt tròn và viền vành khuyên)'
    }
  ];

  const lessonInfo = {
    topic: 'BÀI 15: ĐỘ DÀI CỦA CUNG TRÒN. DIỆN TÍCH HÌNH QUẠT TRÒN VÀ HÌNH VÀNH KHUYÊN (BÀI HỌC STEM)',
    ppct: 'Tiết 15, 16',
    lessonScope: 'Tiết 15, 16',
    duration: '02 tiết (90 phút)'
  };

  const outPaths = [
    path.resolve(__dirname, '../1_SOAN_KHBD/Ket_qua/TOAN9_STEM_Bai15_DoDaiCungTron_DienTichHinhQuatTron.docx'),
    path.resolve(__dirname, '../1_SOAN_KHBD/Ket_qua/10.11/TOAN9_STEM_Bai15_DoDaiCungTron_DienTichHinhQuatTron.docx')
  ];

  for (const outPath of outPaths) {
    fs.mkdirSync(path.dirname(outPath), { recursive: true });
    console.log(`Đang xuất file: ${outPath}...`);
    const res = await createKhbdDocx({
      mdFilePath: mdPath,
      outputDocxPath: outPath,
      lessonInfo: lessonInfo,
      illustrations: illustrations
    });
    console.log(`-> Thành công: ${path.basename(res.path)} (${res.size} bytes)`);
  }
}

main().catch(err => {
  console.error('Lỗi xuất bản docx:', err);
  process.exit(1);
});
