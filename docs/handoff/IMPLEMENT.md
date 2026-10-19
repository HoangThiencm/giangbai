# IMPLEMENT: Sửa FAIL nhận diện văn bản

## Đã sửa theo VERIFY

- `TROLYTHIEN/engine/nhan_dien_engine.py`: `sys.stdout.reconfigure(encoding="utf-8")` trước khi in. CLI in được câu kết luận có chữ Đ trên console Windows.
- Menu 14 được ghi trong `.agents/rules/tro-ly-thien.md`, cùng workflow và menu HTML.
- Các smoke đếm menu cập nhật từ 13 lên 14: `trolythien-bai-giang-html-smoke.js`, `trolythien-chuan-hoa-van-ban-smoke.js`, `trolythien-chuyen-ghi-am-smoke.js`, `trolythien-vehinh-smoke.js`.

## Kiểm tra

- `python -m TROLYTHIEN.engine.nhan_dien_engine --input "TROLYTHIEN/14_NHAN_DIEN_VAN_BAN/Dau_vao/ca2_cong_thuc.json"` in đủ Word, JSON và câu kết luận. Không còn UnicodeEncodeError.
- `node tests/trolythien-chuan-hoa-van-ban-smoke.js` PASS.
- `node tests/trolythien-vehinh-smoke.js` PASS.
- `node tests/trolythien-chuyen-ghi-am-smoke.js` PASS.
- `node tests/trolythien-bai-giang-html-smoke.js` qua được mục đếm 14 lựa chọn, rồi dừng vì thiếu sẵn file `TROLYTHIEN/10_BAI_GIANG_HTML/Ket_qua/export_hoaimy_audio.py`. File này không nằm trong hai lỗi VERIFY.

Chưa commit, chưa push.
