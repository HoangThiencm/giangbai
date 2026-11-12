const fs = require('fs');
const path = require('path');
const { createKhbdDocx } = require('./TROLYTHIEN/engine/export_khbd_engine.js');

const targetDir = path.resolve(__dirname, 'TROLYTHIEN/1_SOAN_KHBD/Ket_qua/05.11');

const items = [
  {
    mdFile: 'KHBD_01_Hoang_Tan_Thien_Toan_9.md',
    docxFile: 'KHBD_01_Hoang_Tan_Thien_Toan_9.docx',
    info: {
      school: 'TRƯỜNG THCS TRẦN PHÚ',
      group: 'TỔ TOÁN - TIN HỌC',
      teacher: 'Hoàng Tấn Thiên',
      topic: 'BÀI 8: KHAI CĂN BẬC HAI VỚI PHÉP NHÂN VÀ PHÉP CHIA',
      ppct: 'Tiết 27',
      duration: '01 tiết (45 phút)',
      grade: '9'
    }
  },
  {
    mdFile: 'KHBD_02_Duong_Quang_Tung_Tin_6.md',
    docxFile: 'KHBD_02_Duong_Quang_Tung_Tin_6.docx',
    info: {
      school: 'TRƯỜNG THCS TRẦN PHÚ',
      group: 'TỔ TOÁN - TIN HỌC',
      teacher: 'Dương Quang Tùng',
      topic: 'BÀI 7: TÌM KIẾM THÔNG TIN TRÊN INTERNET',
      ppct: 'Tiết 13',
      duration: '01 tiết (45 phút)',
      grade: '6'
    }
  },
  {
    mdFile: 'KHBD_03_Nguyen_Thi_Thao_Toan_6.md',
    docxFile: 'KHBD_03_Nguyen_Thi_Thao_Toan_6.docx',
    info: {
      school: 'TRƯỜNG THCS TRẦN PHÚ',
      group: 'TỔ TOÁN - TIN HỌC',
      teacher: 'Nguyễn Thị Thảo',
      topic: 'BÀI 10: SỐ NGUYÊN ÂM VÀ TẬP HỢP CÁC SỐ NGUYÊN',
      ppct: 'Tiết 21',
      duration: '01 tiết (45 phút)',
      grade: '6'
    }
  },
  {
    mdFile: 'KHBD_04_Le_Thi_Binh_Toan_8.md',
    docxFile: 'KHBD_04_Le_Thi_Binh_Toan_8.docx',
    info: {
      school: 'TRƯỜNG THCS TRẦN PHÚ',
      group: 'TỔ TOÁN - TIN HỌC',
      teacher: 'Lê Thị Bình',
      topic: 'BÀI 11: HÌNH THOI VÀ HÌNH VUÔNG',
      ppct: 'Tiết 24',
      duration: '01 tiết (45 phút)',
      grade: '8'
    }
  },
  {
    mdFile: 'KHBD_05_Hoang_Xuan_Anh_Toan_7.md',
    docxFile: 'KHBD_05_Hoang_Xuan_Anh_Toan_7.docx',
    info: {
      school: 'TRƯỜNG THCS TRẦN PHÚ',
      group: 'TỔ TOÁN - TIN HỌC',
      teacher: 'Hoàng Xuân Ánh',
      topic: 'BÀI 10: TIÊN ĐỀ EUCLID. TÍNH CHẤT CỦA HAI ĐƯỜNG THẲNG SONG SONG',
      ppct: 'Tiết 29',
      duration: '01 tiết (45 phút)',
      grade: '7'
    }
  },
  {
    mdFile: 'KHBD_06_Tran_Long_Hai_Toan_8.md',
    docxFile: 'KHBD_06_Tran_Long_Hai_Toan_8.docx',
    info: {
      school: 'TRƯỜNG THCS TRẦN PHÚ',
      group: 'TỔ TOÁN - TIN HỌC',
      teacher: 'Trần Long Hải',
      topic: 'BÀI 8: TỔNG VÀ HIỆU HAI LẬP PHƯƠNG',
      ppct: 'Tiết 18',
      duration: '01 tiết (45 phút)',
      grade: '8'
    }
  },
  {
    mdFile: 'KHBD_07_Tran_Sang_Toan_9.md',
    docxFile: 'KHBD_07_Tran_Sang_Toan_9.docx',
    info: {
      school: 'TRƯỜNG THCS TRẦN PHÚ',
      group: 'TỔ TOÁN - TIN HỌC',
      teacher: 'Trần Sáng',
      topic: 'BÀI 5: BẤT ĐẲNG THỨC VÀ TÍNH CHẤT',
      ppct: 'Tiết 15',
      duration: '01 tiết (45 phút)',
      grade: '9'
    }
  },
  {
    mdFile: 'KHBD_08_Ho_Dang_Danh_Toan_6.md',
    docxFile: 'KHBD_08_Ho_Dang_Danh_Toan_6.docx',
    info: {
      school: 'TRƯỜNG THCS TRẦN PHÚ',
      group: 'TỔ TOÁN - TIN HỌC',
      teacher: 'Hồ Đăng Danh',
      topic: 'BÀI 19: HÌNH CHỮ NHẬT - HÌNH THOI - HÌNH BÌNH HÀNH - HÌNH THANG CÂN',
      ppct: 'Tiết 49',
      duration: '01 tiết (45 phút)',
      grade: '6'
    }
  },
  {
    mdFile: 'KHBD_09_Nguyen_Van_Tinh_HDTN_6.md',
    docxFile: 'KHBD_09_Nguyen_Van_Tinh_HDTN_6.docx',
    info: {
      school: 'TRƯỜNG THCS TRẦN PHÚ',
      group: 'TỔ TOÁN - TIN HỌC',
      teacher: 'Nguyễn Văn Tính',
      topic: 'CHỦ ĐỀ 3: XÂY DỰNG NẾP SỐNG GIA ĐÌNH - TIẾT 1: VĂN HÓA ĐỌC SỐ TRONG GIA ĐÌNH VÀ NHÀ TRƯỜNG',
      ppct: 'Tiết 32',
      duration: '01 tiết (45 phút)',
      grade: '6'
    }
  }
];

async function run() {
  console.log('--- BẮT ĐẦU BIÊN DỊCH 09 KHBD SANG DOCX CHUẨN CV 5512 ---');
  for (const item of items) {
    const mdPath = path.join(targetDir, item.mdFile);
    const docxPath = path.join(targetDir, item.docxFile);
    if (!fs.existsSync(mdPath)) {
      console.error(`Bỏ qua: Không tìm thấy file ${mdPath}`);
      continue;
    }
    try {
      const res = await createKhbdDocx({
        mdFilePath: mdPath,
        outputDocxPath: docxPath,
        lessonInfo: item.info
      });
      console.log(`[OK] Đã xuất: ${item.docxFile} (${Math.round(res.size / 1024)} KB)`);
    } catch (err) {
      console.error(`[LỖI] Xuất file ${item.docxFile} thất bại:`, err.message);
    }
  }
  console.log('--- HOÀN TẤT TẤT CẢ 09 FILE DOCX ---');
}

run();
