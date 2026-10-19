# VERIFY

## Kết luận
FAIL

## Đối chiếu scope
- Đã tạo `TROLYTHIEN/14_NHAN_DIEN_VAN_BAN/` (`Dau_vao/`, `Ket_qua/`, `HUONG_DAN_NHAN_DIEN_VAN_BAN.md`, `PROMPT_NHAN_DIEN_VAN_BAN.md`).
- Đã tạo `TROLYTHIEN/engine/nhan_dien_engine.py` với cấu trúc Hybrid Pipeline, kiểm soát kép công thức, tag đỏ `NDxx`, Bảng Audit Log và xuất file JSON metadata.
- Đã cập nhật mục 14 vào `.agents/workflows/thien.md` và `TROLYTHIEN/tro-ly-thien-menu.html`.
- Đã tạo `tests/nhan-dien-van-ban-smoke.py` với 5 ca khó.

## Test đã chạy
- `python tests/nhan-dien-van-ban-smoke.py` → PASS.
- `python -m TROLYTHIEN.engine.nhan_dien_engine --input "TROLYTHIEN/14_NHAN_DIEN_VAN_BAN/Dau_vao/ca2_cong_thuc.json"` → FAIL (UnicodeEncodeError).
- `node tests/trolythien-bai-giang-html-smoke.js` → FAIL (AssertionError: 14 !== 13).
- `node tests/trolythien-chuan-hoa-van-ban-smoke.js` → FAIL (AssertionError: 14 !== 13).
- `node tests/trolythien-chuyen-ghi-am-smoke.js` → FAIL (AssertionError: Menu tương tác 13 tác vụ chính).
- `node tests/trolythien-vehinh-smoke.js` → FAIL (AssertionError: 14 !== 13).

## Pass / Fail từng tiêu chí
- Pass: Cấu trúc thư mục Mục 14 đầy đủ, tài liệu hướng dẫn và master prompt đúng 7 quy chuẩn.
- Pass: Engine nhận diện và xuất Word đạt Times New Roman 14pt, render công thức `m:oMath`, có bảng Audit Log.
- Pass: Bộ test 5 ca khó `tests/nhan-dien-van-ban-smoke.py` đạt PASS.
- Fail: Lỗi chạy CLI trực tiếp trên Windows do `print(CONCLUSION)` gặp `UnicodeEncodeError` (ký tự `\u0110` không mã hóa được trong `cp1252`).
- Fail: Phá vỡ regression của 4 test suite hiện có (`trolythien-bai-giang-html-smoke.js`, `trolythien-chuan-hoa-van-ban-smoke.js`, `trolythien-chuyen-ghi-am-smoke.js`, `trolythien-vehinh-smoke.js`) do các test này kiểm tra số lượng tác vụ menu và tiêu đề 13 tác vụ trong workflow/rules.

## Bug
- Lỗi 1: `UnicodeEncodeError: 'charmap' codec can't encode character '\u0110'` khi chạy `nhan_dien_engine.py` qua CLI trên Windows.
  - Tái hiện: Chạy `python -m TROLYTHIEN.engine.nhan_dien_engine --input "TROLYTHIEN/14_NHAN_DIEN_VAN_BAN/Dau_vao/ca2_cong_thuc.json"`.
  - File liên quan: `TROLYTHIEN/engine/nhan_dien_engine.py`.
  - Khắc phục: Cần thêm `if sys.stdout: sys.stdout.reconfigure(encoding='utf-8')` hoặc xuất chuỗi an toàn mã hóa console.

- Lỗi 2: Lệch số lượng tác vụ Menu chính giữa `.agents/workflows/thien.md`, `.agents/rules/tro-ly-thien.md` và các bài smoke test cũ.
  - Tái hiện: Chạy `node tests/trolythien-bai-giang-html-smoke.js`, `node tests/trolythien-chuan-hoa-van-ban-smoke.js`, `node tests/trolythien-chuyen-ghi-am-smoke.js`, `node tests/trolythien-vehinh-smoke.js`.
  - File liên quan: `.agents/rules/tro-ly-thien.md`, `.agents/workflows/thien.md`, các file smoke test tương ứng.
  - Khắc phục: Đồng bộ danh mục 14 tác vụ sang `.agents/rules/tro-ly-thien.md` và cập nhật kỳ vọng (expect) trong các bài test smoke từ 13 lên 14 tác vụ.
