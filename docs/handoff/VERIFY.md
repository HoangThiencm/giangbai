# VERIFY: Bổ sung tính năng tạo đề thi từ Ma trận và Bản đặc tả

## Kết luận
PASS

## Đối chiếu scope
- [x] Bổ sung tạo đề từ ma trận vào Menu Cấp 2. Trên `main` lựa chọn 11 đã là mô phỏng hình học, nên mục này là lựa chọn 12, cùng câu chữ trong `.agents/workflows/thien.md` và `.agents/rules/tro-ly-thien.md`: `12. 📋 Tạo đề thi từ Ma trận & Bản đặc tả (Tự động đọc .docx trong Dau_vao hoặc thư mục chỉ định)`.
- [x] Quy định cơ chế tiếp nhận đường dẫn thư mục tùy biến từ người dùng, quét đệ quy `Dau_vao/` khi không chỉ định, loại bỏ tệp tạm `~$`.
- [x] Biên soạn Master Prompt `TROLYTHIEN/2_TAO_BAI_TAP/HUONG_DAN_TAO_DE_THI_TU_MA_TRAN.md` với đầy đủ quy chuẩn 3 dạng đề (CV 7991, TN + TL kết hợp, 100% TL), bám sát 100% Yêu cầu cần đạt, GDPT 2018 (cấm $\Leftrightarrow$, cấm $S$), xuất công thức Word Equation OMML (`m:oMath`) qua `latex_to_omml`, cấu trúc 3 phần hoàn chỉnh.
- [x] Xây dựng engine `TROLYTHIEN/engine/doc_ma_tran_dac_ta.py` với CLI `--input-dir` và `--file`, bóc tách đầy đủ khung ma trận, bản đặc tả, tổng số câu, mức độ, dạng câu và điểm.
- [x] Đồng bộ tri thức đóng gói trong `app_trolythien/core/prompt_builder.py` (`BUNDLE_MAP` và `REQUIRED_PROMPTS` chứa `02_tao_de_ma_tran.md`) và tệp `app_trolythien/troly/prompts/02_tao_de_ma_tran.md`.
- [x] Smoke test `tests/trolythien-tao-de-ma-tran-smoke.py` bao phủ toàn diện 5 kịch bản kiểm thử.

## Test đã chạy
1. `python tests/trolythien-tao-de-ma-tran-smoke.py`:
   - `test_thu_muc_chi_dinh`: Quét thư mục chỉ định `Dau_vao/12.10/`, đọc 2 tệp Toán 8 và Toán 9, kiểm tra đủ 21 câu, 10 điểm, các mức nhận biết/thông hiểu/vận dụng $\rightarrow$ PASS.
   - `test_thu_muc_mac_dinh`: Quét đệ quy thư mục mặc định `Dau_vao/` $\rightarrow$ PASS.
   - `test_duong_dan_tuong_doi_va_cli`: Chạy CLI qua subprocess với cờ `--file` $\rightarrow$ PASS.
   - `test_duong_dan_sai`: Kiểm tra ném ngoại lệ `DuongDanKhongHopLe` khi thư mục không tồn tại $\rightarrow$ PASS.
   - `test_menu_khop`: So khớp câu chữ Menu lựa chọn 12 giữa `thien.md` và `tro-ly-thien.md` $\rightarrow$ PASS.
2. Kiểm tra `knowledge_ready()` trong `app_trolythien/core/prompt_builder.py`: trả về `(True, ...)` $\rightarrow$ PASS.
3. `test_prompts()` từ `tests/test_verify_dekiemtra.py` $\rightarrow$ PASS.

## Pass / Fail từng tiêu chí
- Tiêu chí 1 (Menu Cấp 2 có lựa chọn 12 khớp nhau, giữ lựa chọn 11 mô phỏng): PASS
- Tiêu chí 2 (Hỗ trợ linh hoạt đường dẫn chỉ định & mặc định): PASS
- Tiêu chí 3 (Tự động nhận diện 3 dạng cấu trúc đề): PASS
- Tiêu chí 4 (Engine bóc tách chính xác 2 file thực tế trong 12.10): PASS
- Tiêu chí 5 (Không ảnh hưởng các tính năng và test hiện có): PASS

## Bug
(Không có bug)
