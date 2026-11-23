const fs = require('fs');
const path = require('path');
const { createKhbdDocx } = require('./TROLYTHIEN/engine/export_khbd_engine');

function fileToDataUrl(filePath, mimeType = 'image/png') {
  if (fs.existsSync(filePath)) {
    const b64 = fs.readFileSync(filePath).toString('base64');
    return `data:${mimeType};base64,${b64}`;
  }
  console.warn('File not found for DataURL:', filePath);
  return null;
}

async function exportAll() {
  console.log('=== BẮT ĐẦU XUẤT BẢN WORD 3 TIẾT KIỂM TRA GIỮA HK1 ===');

  const baseOut = path.resolve('TROLYTHIEN/1_SOAN_KHBD/Ket_qua/02.11');
  const tin6OutDir = path.join(baseOut, 'TIN6');
  const toan6OutDir = path.join(baseOut, 'TOAN6');

  if (!fs.existsSync(baseOut)) fs.mkdirSync(baseOut, { recursive: true });
  if (!fs.existsSync(tin6OutDir)) fs.mkdirSync(tin6OutDir, { recursive: true });
  if (!fs.existsSync(toan6OutDir)) fs.mkdirSync(toan6OutDir, { recursive: true });

  // 1. TIN HỌC 6
  console.log('\n--- 1. Đang xuất: Tin học 6 Tiết 10 ---');
  const tin6Ill = [
    {
      id: 'tin6-gk1-cau30',
      dataUrl: fileToDataUrl('TROLYTHIEN/TEMP/02.11_Tin6/hinh_ve/tin6_gk1_cau30.png'),
      caption: 'Bức tranh chữ H dạng lưới 6x9 ô vuông'
    }
  ];
  const tin6Md = path.resolve('TROLYTHIEN/TEMP/02.11_Tin6/02_KiemTraGiuaHK1_Tin6_Tiet10.md');
  const tin6Docx = path.join(tin6OutDir, '02_KiemTraGiuaHK1_Tin6_Tiet10.docx');
  const tin6DocxMain = path.join(baseOut, '02_KiemTraGiuaHK1_Tin6_Tiet10.docx');

  await createKhbdDocx({
    mdFilePath: tin6Md,
    outputDocxPath: tin6Docx,
    lessonInfo: {
      subject: 'TIN HỌC',
      grade: '6',
      unitName: 'TIẾT 10: KIỂM TRA ĐÁNH GIÁ GIỮA HỌC KÌ I',
      author: 'Hoàng Tấn Thiên'
    },
    illustrations: tin6Ill
  });
  fs.copyFileSync(tin6Docx, tin6DocxMain);
  console.log('✓ Hoàn tất xuất Tin học 6:', tin6Docx);

  // 2. TOÁN 6
  console.log('\n--- 2. Đang xuất: Toán 6 Tiết 29 ---');
  const toan6Ill = [
    {
      id: 'toan6-gk1-hinh1',
      dataUrl: fileToDataUrl('TROLYTHIEN/TEMP/02.11_Toan6/hinh_ve/toan6_gk1_hinh1.png'),
      caption: 'Hình 1: Các hình tam giác'
    },
    {
      id: 'toan6-gk1-hinh-tuong',
      dataUrl: fileToDataUrl('TROLYTHIEN/TEMP/02.11_Toan6/hinh_ve/toan6_gk1_hinh_tuong.png'),
      caption: 'Mảng tường trang trí ốp đá'
    }
  ];
  const toan6Md = path.resolve('TROLYTHIEN/TEMP/02.11_Toan6/04_KHBD_Toan6_KiemTraGiuaHK1_Tiet29.md');
  const toan6Docx = path.join(toan6OutDir, '04_KHBD_Toan6_KiemTraGiuaHK1_Tiet29.docx');
  const toan6DocxMain = path.join(baseOut, '04_KHBD_Toan6_KiemTraGiuaHK1_Tiet29.docx');

  await createKhbdDocx({
    mdFilePath: toan6Md,
    outputDocxPath: toan6Docx,
    lessonInfo: {
      subject: 'Toán',
      branch: 'SoHoc',
      grade: '6',
      unitName: 'TIẾT 29: KIỂM TRA ĐÁNH GIÁ GIỮA HỌC KÌ I',
      author: 'Hoàng Tấn Thiên'
    },
    illustrations: toan6Ill
  });
  fs.copyFileSync(toan6Docx, toan6DocxMain);
  console.log('✓ Hoàn tất xuất Toán 6:', toan6Docx);

  // 3. TOÁN 9
  console.log('\n--- 3. Đang xuất: Toán 9 Tiết 26 ---');
  const toan9Ill = [
    {
      id: 'toan9-gk1-hinh1',
      dataUrl: fileToDataUrl('TROLYTHIEN/TEMP/02.11/hinh_ve/toan9_gk1_hinh1.png'),
      caption: 'Hình 1: Tam giác ABC vuông tại A'
    },
    {
      id: 'toan9-gk1-hinh2',
      dataUrl: fileToDataUrl('TROLYTHIEN/TEMP/02.11/hinh_ve/toan9_gk1_hinh2.jpeg', 'image/jpeg'),
      caption: 'Hình 2: Bài toán đo chiều cao cây'
    },
    {
      id: 'toan9-gk1-hinh3',
      dataUrl: fileToDataUrl('TROLYTHIEN/TEMP/02.11/hinh_ve/toan9_gk1_hinh3.png'),
      caption: 'Hình 3: Mảnh đất hình tam giác ABC'
    }
  ];
  const toan9Md = path.resolve('TROLYTHIEN/TEMP/02.11/04b_KHBD_Toan9_KiemTraGiuaHK1_Tiet26.md');
  const toan9Docx = path.join(baseOut, '04b_KHBD_Toan9_KiemTraGiuaHK1_Tiet26.docx');

  await createKhbdDocx({
    mdFilePath: toan9Md,
    outputDocxPath: toan9Docx,
    lessonInfo: {
      subject: 'Toán',
      branch: 'DaiSo',
      grade: '9',
      unitName: 'TIẾT 26: KIỂM TRA ĐÁNH GIÁ GIỮA HỌC KÌ I',
      author: 'Hoàng Tấn Thiên'
    },
    illustrations: toan9Ill
  });
  console.log('✓ Hoàn tất xuất Toán 9:', toan9Docx);

  console.log('\n=== TẤT CẢ 3 TỆP WORD ĐÃ ĐƯỢC XUẤT THÀNH CÔNG 100%! ===');
}

exportAll().catch(err => {
  console.error('LỖI KHI XUẤT DOCX:', err);
  process.exit(1);
});
