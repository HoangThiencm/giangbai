# IMPLEMENT: Tạo đề thi từ Ma trận và Bản đặc tả

## Đã làm
1. Menu Cấp 2 của "3/ Tạo bài tập" có lựa chọn 12, cùng một câu chữ trong `.agents/workflows/thien.md` và `.agents/rules/tro-ly-thien.md`. Lựa chọn 11 giữ mô phỏng hình học đã có trên `main`:
   `12. 📋 Tạo đề thi từ Ma trận & Bản đặc tả (Tự động đọc .docx trong Dau_vao hoặc thư mục chỉ định)`
2. Hai file quy tắc nêu cách nhận đường dẫn giáo viên chỉ định, quét đệ quy `Dau_vao/` khi không chỉ định, gọi engine, bám yêu cầu cần đạt, giới hạn GDPT 2018, xuất Word Equation và lưu `Ket_qua/De_Kiem_Tra_[Mon]_[Lop]_[KyThi].docx`.
3. Master Prompt: `TROLYTHIEN/2_TAO_BAI_TAP/HUONG_DAN_TAO_DE_THI_TU_MA_TRAN.md`.
4. Engine `TROLYTHIEN/engine/doc_ma_tran_dac_ta.py`:
   - `quet_file_dau_vao(input_path=None)` quét mặc định hoặc đường dẫn thư mục/tệp. Bỏ tệp tạm `~$`. Đường dẫn sai ném `DuongDanKhongHopLe`.
   - `phan_tich_ma_tran_dac_ta(docx_path)` tách khung ma trận, bản đặc tả, tổng số câu, mức độ, yêu cầu cần đạt, dạng câu và điểm.
   - CLI: `--input-dir` hoặc `--file`.
5. `BUNDLE_MAP` thêm `2_TAO_BAI_TAP/HUONG_DAN_TAO_DE_THI_TU_MA_TRAN.md` → `prompts/02_tao_de_ma_tran.md`. `REQUIRED_PROMPTS` có `02_tao_de_ma_tran.md`. Bản đóng gói nằm ở `app_trolythien/troly/prompts/02_tao_de_ma_tran.md`.
6. Smoke test: `tests/trolythien-tao-de-ma-tran-smoke.py`.

## Chưa đụng
- Không sửa 10 định dạng bài tập cũ.
- Không sửa engine trộn đề, CV 7991, hay giao diện tab đề kiểm tra.

## Kiểm thử
- `python tests/trolythien-tao-de-ma-tran-smoke.py` — PASS. Hai tệp trong `Dau_vao/12.10/` đều ra 21 câu, 10 điểm, có nhận biết / thông hiểu / vận dụng và yêu cầu cần đạt. Quét mặc định, CLI `--file` và đường dẫn không tồn tại đều đúng.
- `python tests/test_verify_dekiemtra.py`: Test 1 đến Test 7 in PASS. Sau Test 7, tiến trình tắt trong `MainWindow._preflight.wait` (không có traceback Python). `test_exe()` chạy riêng: PASS (TroLyHoangThien.exe 2MB). Lỗi thoát nằm ở luồng kiểm tra agy, ngoài phần ma trận vừa thêm.

## Bước tiếp
Antigravity IDE, chat mới: `/verify`
