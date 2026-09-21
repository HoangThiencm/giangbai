# IMPLEMENT: Xuất Word cho Game Giáo dục

Đã triển khai đúng `docs/handoff/PLAN.md`.

## Thay đổi

- Bổ sung `exportWordForGame()` và nút **Xuất Word cho Game** trong `taobaitap.html`, bản sao lưu và `smartquiz.html`.
- File `De_Thi_Game_Giao_Duc.docx` xuất bằng đoạn văn riêng từng dòng, giữ nguyên LaTeX và có bảng đáp án cuối file.
- Chuyển đổi trắc nghiệm, Đúng/Sai, ý Đúng/Sai CV7991, nối cột, trả lời ngắn và điền khuyết sang cấu trúc Game đọc được.
- Thêm `tests/taobaitap-game-word-export-smoke.js` kiểm tra cấu trúc, đáp án, LaTex và `GameQuizImporter`.

## Kiểm tra

Đã kiểm tra tĩnh các yêu cầu xuất file. Không thể chạy Node smoke test trong môi trường hiện tại vì Windows chặn `node.exe` do nhận diện nhầm là phần mềm không an toàn (`ResourceUnavailable`).
