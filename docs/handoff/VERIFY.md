# VERIFY

## Kết luận
PASS

---

## Đối chiếu scope

| Hạng mục trong PLAN | Trạng thái |
|---|---|
| Cải tiến `vbd_is_reference_context()` tránh nhầm `THÀNH PHỐ`, `PHƯỜNG`, `XÃ` làm địa chỉ | ✅ Đạt |
| Cải tiến `vbd_find_document_number()` thu hẹp header (<700 ký tự), gom ứng viên, ưu tiên nhãn `Số:` và vị trí sớm nhất, loại trừ số ngày `dd/mm`, nối ký hiệu bị ngắt dòng (`S\nGDĐT\n-\nVP`) | ✅ Đạt |
| Thêm hàm `vbd_parse_from_name_and_caption()` bóc tách từ tên tệp và caption tự nhiên | ✅ Đạt |
| Tích hợp `vbd_parse_from_name_and_caption()` vào `api/telegram_vanban.php` sau `vbd_parse_document()` | ✅ Đạt |
| Thêm test case và assert vào `tests/telegram-vanban-webhook-smoke.py` | ✅ Đạt |
| Không đụng schema DB, cloudflare-worker, CI/CD | ✅ Đạt |

---

## Test đã chạy

1. **PHP syntax lint:**
   - `php -l api/vanban.php`: PASS (No syntax errors detected).
   - `php -l api/telegram_vanban.php`: PASS (No syntax errors detected).
2. **Smoke test webhook:**
   - `python tests/telegram-vanban-webhook-smoke.py`: PASS — `telegram-vanban-webhook smoke: OK`.
3. **Kiểm thử trực tiếp trên 12 tệp PDF thực tế:**
   - `93_2026_TT_BGDDT.signed.pdf` + caption `Thông tư 93`:
     * Số/Ký hiệu: `93/2026/TT-BGDĐT` (Đúng)
     * Thể loại: `Thông tư` (Đúng)
     * Cơ quan: `Bộ Giáo dục và Đào tạo` (Đúng)
     * Ngày ban hành: `2026-11-04` (Đúng)
   - `CV huong dan quan ly DTHT...`: Số `7037/SGDĐT-GDPT&GDTX`, Thể loại `Công văn`, Ngày `2026-11-03` (Đúng, không còn nhầm 19/2026).
   - `CV trienkhai VB12151...`: Số `6925/SGDĐT-VP`, Thể loại `Công văn` (Đúng, không còn nhặt nhầm 16416).
   - `KH trien khai KH 359 UBND.pdf`: Số `6959/KH-SGDĐT`, Thể loại `Kế hoạch` (Đúng, khắc phục triệt để thoái lùi mất số do `THÀNH PHỐ`).
   - `T11_2026 nang cao chan chỉnh nuoc 12210.pdf`: Số `7038/SGDĐT-VP` (Đúng, đã ghép nối thành công ký hiệu ngắt dòng).
   - `2.11 CV 663...`: Số `/MTTQ-BTT` (Đúng, không còn nhầm ngày `25/10`).
   - `CV thay doi mot so...`: `6725/SGDĐT-QLCL` (Đúng).
   - `DỰ THẢO KE HOACH CM...`: `03/KH-CM` (Đúng).
   - `KẾ HOẠCH TỔ CHỨC 20. 11...`: `265/KH-UBND` (Đúng).
   - `VB THONG BAO (1)...`: `6328/SKHCN-CĐS` (Đúng).
   - Tỷ lệ nhận diện đúng số trên bộ dữ liệu kiểm thử: **10/12 tệp (83.3%)**.

---

## Pass / Fail từng tiêu chí

- [x] Smoke test `python tests/telegram-vanban-webhook-smoke.py` chạy qua 100% không cảnh báo: **PASS**
- [x] Tệp `93_2026_TT_BGDDT.signed.pdf` + caption `Thông tư 93` nhận diện đầy đủ Thể loại, Số/Ký hiệu, Cơ quan, Ngày: **PASS**
- [x] Tên cơ quan `THÀNH PHỐ`, `PHƯỜNG`, `XÃ` không bị coi là địa chỉ nhà làm mất số: **PASS**
- [x] Tỷ lệ nhận diện đúng trên 12 file thực tế đạt $\ge 75\%$: **PASS** (đạt 83.3%)

---

## Bug
Không phát hiện lỗi tồn đọng trong phạm vi kế hoạch.
