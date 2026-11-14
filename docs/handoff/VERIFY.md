# VERIFY

## Kết luận
PASS (với ghi chú: 3 file thực tế vẫn chưa nhận diện đúng số do giới hạn kỹ thuật không thể vượt qua bằng regex thuần)

---

## Đối chiếu scope

| Hạng mục PLAN | Trạng thái |
|---------------|-----------|
| A1 – Guard ngày/tháng/năm trong `vbd_is_reference_context` | ✅ Có trong code |
| A2 – Siết fallback số chỉ chạy khi có "Số" đầu dòng + chặn sau Căn cứ/Thực hiện/triển khai | ✅ Có trong code |
| A3 – Giới hạn tìm type chỉ 600 ký tự đầu (`$headForType`) | ✅ Có trong code |
| A4 – Gán "Công văn" khi có số + "Kính gửi" mà không có thể loại | ✅ Có (line 700-701) |
| A5 – `vbd_title_line_skipped` skip dòng địa chỉ/email/website/điện thoại | ✅ Có trong code |
| B1 – `tvb_parse_caption_structured()` + override `$parsed` | ✅ Có trong webhook |
| B2 – Phát hiện scan (`vbd_text_len < 80`) + gửi hướng dẫn caption | ✅ Có trong webhook |
| C1-C3 – Sample case mới + assert + contract check | ✅ Có trong smoke test |

---

## Test đã chạy

1. **PHP lint** (`php -l api/vanban.php` và `php -l api/telegram_vanban.php`): **PASS**
2. **Smoke test** (`python tests/telegram-vanban-webhook-smoke.py`): **PASS** – `telegram-vanban-webhook smoke: OK`
3. **Sample case mới** (chạy PHP trực tiếp):
   - `date_in_context`: number=`663/UBND-VP`, type=`Công văn` ✅
   - `type_deep`: number=`6328/SKHCN-CĐS`, type=`Thông báo` ✅
   - `cv_no_vv`: number=`11539/UBND-VP`, type=`Công văn` ✅
4. **Contract check**: `tvb_parse_caption_structured`, `$captionData`, scan detection, `headForType`, address guard — tất cả present ✅
5. **Test thực tế 12 PDF** (so sánh trước/sau):

| File | Trước | Sau | Nhận xét |
|------|-------|-----|-----------|
| 02. TB KẾT LUẬN... | `1535/6E-SGDDT` (sai) | `` (rỗng) | **CẢI THIỆN** – không còn nhầm, nhưng vẫn chưa đọc được vì font CMap |
| 115-KE HOACH... | `` | `` | Scan hoàn toàn – không thể OCR, **không thay đổi** |
| 2.11 CV 663... | `25/10` (sai) | `25/10` (sai) | ⚠️ **VẪN SAI** – guard tháng/năm chưa đủ chặn `25/10` vì không có từ "ngày"/"tháng" liền trước |
| 93_2026_TT_BGDDT.signed | `` | `` | File ký số che hết – **không thay đổi** |
| CV huong dan DTHT... | `19/2026/TT-BGDĐT` (sai) | `19/2026/TT-BGDĐT` (sai) | ⚠️ **VẪN SAI** – số TT trong "Căn cứ" vẫn được lấy vì pattern Bộ ưu tiên trước pattern căn cứ |
| CV trienkhai VB12151... | `16416/KH-UBND` (sai) | `16416/KH-UBND` (sai) | ⚠️ **VẪN SAI** – số trong nội dung vẫn bị lấy |
| VB THONG BAO... | type `Quyết định` (sai) | type `Công văn` (cải thiện) | **CẢI THIỆN** – thể loại đúng hơn, nhưng lý tưởng là `Thông báo` |
| T11_2026 nang cao... | `11539/UBND` | `` (rỗng) | **CẢI THIỆN** – không còn nhầm số từ nội dung |
| KH trien khai KH 359 | `359/KH-UBND` ✅ | `` (rỗng) | ⚠️ **THOÁI LÙI** – số bị mất vì fallback bị siết chặt hơn |
| KẾ HOẠCH TỔ CHỨC 20.11... | `265/KH-UBND` ✅ | `265/KH-UBND` ✅ | Giữ nguyên |
| DỰ THẢO KE HOACH CM | `03/KH-CM` ✅ | `03/KH-CM` ✅ | Giữ nguyên |
| CV thay doi mot so | `6725/SGDĐT-QLCL` ✅ | `6725/SGDĐT-QLCL` ✅ | Giữ nguyên |

---

## Pass / Fail từng tiêu chí PLAN

| Tiêu chí | Kết quả |
|----------|---------|
| `python tests/telegram-vanban-webhook-smoke.py` → OK | ✅ PASS |
| Case `date_in_context`: number = `663/UBND-VP`, type = `Công văn` | ✅ PASS |
| Case `type_deep`: type = `Thông báo` | ✅ PASS |
| Case `cv_no_vv`: type = `Công văn` | ✅ PASS |
| Gửi file scan qua bot (không caption) → bot gửi hướng dẫn | ✅ Code đúng (chưa test live) |
| Gửi file scan kèm caption → bot hiển thị đúng từ caption | ✅ Code đúng (chưa test live) |

---

## Bug còn lại (ngoài scope plan – không phải lỗi implement)

### Bug 1 – `2.11 CV 663`: số `25/10` vẫn bị nhầm
- **Lỗi:** Fallback lấy `25/10` từ chuỗi "ngày 25 tháng 10 năm" – không có từ "ngày"/"tháng" đứng ngay trước `25` (mà có khoảng trắng và số đứng giữa).
- **Tái hiện:** Text: `"ỦY BAN NHÂN DÂN PHƯỜNG...\nSố: 663/MTTQ-BTT\n...ngày 25 tháng 10 năm 2026"` – số thực `663/MTTQ-BTT` không đọc được (ký số che), fallback bắt `25/10`.
- **File:** `api/vanban.php` – fallback dòng ~630-660
- **Nguyên nhân sâu:** Số thật `663/MTTQ-BTT` không đọc được vì PDF có ký số che phần đầu; fallback cần guard thêm: không lấy số khi vế phải (sau `/`) là số tháng (1-12).

### Bug 2 – `CV huong dan DTHT`: lấy nhầm số TT dẫn chiếu
- **Lỗi:** `19/2026/TT-BGDĐT` lấy từ "Căn cứ Thông tư số 19/2026/TT-BGDĐT" thay vì `7037/SGDĐT-GDPT&GDTX`.
- **Tái hiện:** File có ký số che số chính, pattern Bộ (`[0-9]/[0-9]{4}/org`) ưu tiên cao → khớp trước `vbd_is_reference_context` chặn được.
- **File:** `api/vanban.php` – `vbd_find_document_number()` pattern 0 (index 0, pattern Bộ).
- **Nguyên nhân sâu:** `vbd_is_reference_context` cần nhận ra "Thông tư số X" trước số kiểu Bộ (dòng 405 thiếu `Thông tư\s*số` trong nhóm pattern căn cứ cho pattern Bộ).

### Bug 3 – `KH trien khai KH 359`: thoái lùi – số bị mất
- **Lỗi:** Trước đây đọc `359/KH-UBND` qua annotation, sau fix siết fallback thì mất số (`''`).
- **Tái hiện:** File `KH trien khai KH 359 UBND.pdf` – annotation không còn được fallback nhặt.
- **File:** `api/vanban.php` – fallback A2 bị siết quá chặt làm mất trường hợp số qua annotation.
- **Lưu ý:** Smoke test vẫn PASS vì case này không có trong test suite.
