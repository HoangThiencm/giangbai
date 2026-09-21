# PLAN: Xóa 11 File PDF Trong Thư Mục GIAO AN Để Giảm Dung Lượng Dự Án

## 1. Mục Tiêu
- Xóa toàn bộ 11 file `.pdf` trong thư mục `GIAO AN/` để giải phóng **86.06 MB** dung lượng lưu trữ.
- Không ảnh hưởng đến bất kỳ mã nguồn, logic hay giao diện nào của toàn bộ dự án.

---

## 2. Danh Sách 11 File Cần Xóa

1. `GIAO AN/nang luc so/18-bgddt.pdf`
2. `GIAO AN/nang luc so/02-bgddt.pdf`
3. `GIAO AN/TT32_Chuong trình GDPT 2018.pdf`
4. `GIAO AN/nang luc so/23456bgddthuong-dan-trien-khai-thuc-hien_219202522.pdf`
5. `GIAO AN/Công văn 5555_BGDĐT-GDPT (18.08.2026).pdf`
6. `GIAO AN/17-bgddt.pdf`
7. `GIAO AN/5208_BGDDT_GDPT_signed_07709.pdf`
8. `GIAO AN/XAYDUNGPHULUC/FORM.pdf`
9. `GIAO AN/cong-van-5512bgddt_19520238.pdf`
10. `GIAO AN/KHUNG AI/260818-QD2422-KhungAI.pdf`
11. `GIAO AN/KHUNG AI/260818-QD2422-BanHanh-KhungAI.pdf`

---

## 3. Hướng Dẫn Thực Hiện Cho Coder

### Lệnh thực hiện:
Xóa tất cả các file có đuôi `.pdf` trong thư mục `GIAO AN`:
```powershell
Get-ChildItem -Path "GIAO AN" -Filter "*.pdf" -Recurse -File | Remove-Item -Force
```

### Cập nhật `.gitignore` (Khuyến nghị):
Bổ sung vào file `.gitignore` dòng sau để ngăn các file PDF lớn vô tình được đưa vào kho Git trong tương lai:
```gitignore
GIAO AN/**/*.pdf
```

---

## 4. Kế Hoạch Xác Minh (Verification Plan)
1. Chạy kiểm tra không còn file `.pdf` nào trong `GIAO AN/`.
2. Kiểm tra dung lượng dự án đã giảm tương ứng ~86 MB.
3. Chạy smoke test các trang chính (`index.html`, `canvas_soankhbd.html`, `canvas_xaydungphuluc.html`, `trochoi.html`) đảm bảo hoạt động trơn tru 100%.
