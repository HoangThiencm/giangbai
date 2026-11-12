# THƯ MỤC DỊCH TRUYỆN TRUNG - VIỆT (GIẢI TRÍ)

Thư mục này được thiết kế để quản lý quá trình dịch thuật, lưu trữ các chương truyện đã dịch sang tiếng Việt và tự động xuất ra file giao diện web đọc sách trực quan, mượt mà.

---

## 1. CẤU TRÚC THƯ MỤC
```text
dich_truyen/
├── README.md                      # Hướng dẫn quy trình dịch và sử dụng
├── build_html.py                  # Script gom các file txt thành 1 file HTML đọc truyện độc lập
├── temp/                          # Thư mục chứa file nháp, nguồn thô tiếng Trung (đã ignore Git)
│   └── .gitkeep
├── templates/
│   └── ho_so_dich_thuat_mau.md    # Mẫu hồ sơ dịch thuật chuẩn (bối cảnh, nhân vật, xưng hô...)
└── <ten_truyen>/                  # Thư mục cho từng bộ truyện cụ thể
    ├── ho_so_dich_thuat.md        # Hồ sơ dịch thuật riêng của bộ truyện
    ├── doc_truyen.html            # File HTML đọc trọn vẹn truyện với giao diện đẹp
    └── chuong/                    # Danh sách các file chương .txt đã dịch
        ├── chuong_001.txt
        ├── chuong_002.txt
        └── ...
```

---

## 2. QUY TRÌNH DỊCH THUẬT CHUẨN

1. **Xác minh truyện & Lập Hồ sơ dịch thuật:**
   - Xác định rõ: Tên tiếng Việt, Tên gốc tiếng Trung, Tác giả, Thể loại, Số chương, Tình trạng phát hành, Link nguồn thô.
   - Tạo file `ho_so_dich_thuat.md` dựa theo `templates/ho_so_dich_thuat_mau.md`.
   - Thiết lập bảng nhân vật chính - phụ, quy tắc xưng hô (hiện đại: tôi - bạn, anh - em; cổ trang: ta - ngươi, huynh - đệ, sư đồ...), và cảnh giới/thuật ngữ cố định.

2. **Dịch theo đợt (Batch 5 - 10 chương)hoặc theo yêu cầu người dùng (có thể hết toàn bộ):**
   - Đọc văn bản nguồn tiếng Trung (đặt file thô vào `dich_truyen/<ten_truyen>/temp/` hoặc `dich_truyen/temp/` nếu cần).
   - Dịch sang tiếng Việt tự nhiên, văn phong tiểu thuyết mượt mà, thuần Việt, tuyệt đối không dịch kiểu convert thô cứng.
   - Đầu mỗi chương ghi rõ: `Chương X: [Tên chương]`.
   - Nếu gặp đoạn mơ hồ/thiếu ngữ cảnh/cần kiểm chứng: Đánh dấu `[CẦN KIỂM TRA]`.
   - Lưu từng chương vào file `.txt` tương ứng trong `chuong/chuong_XXX.txt`.
   - Cập nhật nhật ký từ mới, nhân vật mới vào cuối hồ sơ dịch thuật.

3. **Tổng hợp thành giao diện đọc sách HTML:**
   - Chạy lệnh:
     ```powershell
     python dich_truyen/build_html.py dich_truyen/<ten_truyen>
     ```
   - Script sẽ tạo file `doc_truyen.html` ngay trong thư mục truyện:
     - Giao diện đọc sách êm mắt: Đổi nền **Giấy cũ (Sepia)**, **Sáng**, **Tối (Dark mode)**.
     - Tùy chỉnh font Serif / Sans-serif, tăng giảm cỡ chữ (A- / A+).
     - Menu mục lục trượt (sidebar) có tìm kiếm chương tức thì.
     - Nút chuyển chương trước/sau tiện lợi.
     - Tự động ghi nhớ vị trí đang đọc dở vào trình duyệt.

---

## 3. LƯU Ý BẢO MẬT VÀ QUẢN LÝ GIT
- Toàn bộ thư mục `temp/` và file nháp phát sinh trong `dich_truyen/` đã được cấu hình trong `.gitignore` để không bị đẩy lên GitHub làm nặng kho lưu trữ.
- Chỉ lưu trữ các sản phẩm hoàn chỉnh: File `.txt` chương đã dịch, file `ho_so_dich_thuat.md` và file `doc_truyen.html`.
