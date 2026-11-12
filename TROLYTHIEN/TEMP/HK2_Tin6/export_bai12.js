const fs = require('fs');
const path = require('path');
const { createKhbdDocx } = require('../../engine/export_khbd_engine');

async function exportBai12() {
  const tempDir = path.resolve(__dirname);
  const illDir = path.join(tempDir, 'illustrations');
  const outDir = path.resolve(__dirname, '../../1_SOAN_KHBD/Ket_qua/HK2/TIN6');

  if (!fs.existsSync(outDir)) {
    fs.mkdirSync(outDir, { recursive: true });
  }

  const mdPath = path.join(tempDir, '04_KHBD_Tin6_Bai12_TrinhBayThongTinODangBang_Tiet24-25.md');
  const outPath = path.join(outDir, '04_KHBD_Tin6_Bai12_TrinhBayThongTinODangBang_Tiet24-25.docx');

  // Load illustrations
  const illustrations = [];
  
  const img1 = path.join(illDir, 'hinh_danhsach_so_sanh_5_11.png');
  if (fs.existsSync(img1)) {
    illustrations.push({
      id: 'hinh-danhsach-so-sanh-5-11',
      dataUrl: `data:image/png;base64,${fs.readFileSync(img1).toString('base64')}`,
      width: 500,
      height: 250,
      caption: 'So sánh cách trình bày danh sách học sinh dạng bảng và dạng liệt kê'
    });
  }

  const img2 = path.join(illDir, 'hinh_chinhsuabang_layout_5_16.png');
  if (fs.existsSync(img2)) {
    illustrations.push({
      id: 'hinh-chinhsuabang_layout_5_16',
      dataUrl: `data:image/png;base64,${fs.readFileSync(img2).toString('base64')}`,
      width: 540,
      height: 120,
      caption: 'Các lệnh chỉnh sửa bảng trên dải lệnh Table Tools Layout'
    });
  }

  const img3 = path.join(illDir, 'hinh_bang_thanhvien_hoanthanh.png');
  if (fs.existsSync(img3)) {
    illustrations.push({
      id: 'hinh-bang-thanhvien-hoanthanh',
      dataUrl: `data:image/png;base64,${fs.readFileSync(img3).toString('base64')}`,
      width: 420,
      height: 280,
      caption: 'Bảng danh sách thành viên lớp 6A được tạo lập và định dạng hoàn chỉnh'
    });
  }

  const lessonInfo = {
    topic: "BÀI 12: TRÌNH BÀY THÔNG TIN Ở DẠNG BẢNG",
    ppct: "TIẾT 24, 25",
    lessonScope: "TIẾT 24, 25",
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

exportBai12().catch(console.error);
