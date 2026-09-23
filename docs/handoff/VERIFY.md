# VERIFY

## Kết luận
PASS

## Đối chiếu scope
- Sửa đúng file mục tiêu `game-treasure.html`, không chạm vào file ngoài scope.
- Triển khai đầy đủ các hạng mục theo `docs/handoff/PLAN.md` và `docs/handoff/IMPLEMENT.md`:
  + Bảng câu hỏi chuyển lên phía trên dòng sông, hiển thị ngay khi bắt đầu.
  + Bỏ đếm ngược 3-2-1, thay bằng còi GO 0.5s; thời gian đua rút xuống 3s (Siêu tốc) hoặc 5s (Tiêu chuẩn).
  + Thuật toán vật lý đàn vịt: phân chia vai (winnerId cán đích `p >= 1`, topIds dừng ở `<= 0.84`, đàn thường bị giữ lại ở giữa sông `0.42 - 0.62`), không còn dồn ứ ở mép phải.
  + Đồ họa canvas vẽ trực tiếp chướng ngại vật (bánh mì, xoáy nước, nitro, rùa thần).
  + Luồng Zero-click: kết thúc đua vinh danh học sinh ngay trên giao diện và mở câu hỏi trả lời, không qua modal trung gian.
  + Phím tắt (Space, 1-4, A-D, Enter, H) và tính năng Vịt cứu trợ hoạt động đầy đủ.

## Test đã chạy
1. `node tests/duck-race-smoke.js`: PASS toàn bộ 8 nhóm kiểm thử (MathText/KaTeX, layout câu hỏi trên sông, còi GO/thời gian đua, vật lý vai vịt/chướng ngại vật, luồng zero-click, phím tắt/vịt cứu trợ, và biên dịch Babel JSX 50220 ký tự thành công không lỗi cú pháp).
2. `node tests/game-suite-smoke.js`: PASS, không gây hồi quy lên các game khác trong hệ thống.
3. `git status --short`: Xác nhận chỉ thay đổi `game-treasure.html` và các tài liệu handoff.

## Pass / Fail từng tiêu chí
- Tiêu chí 1 (Bảng câu hỏi song song, KaTeX, bố cục trên sông): PASS
- Tiêu chí 2 (Xuất phát nhanh 0.5s còi GO, thời gian 3s/5s): PASS
- Tiêu chí 3 (Vật lý tách đàn, chỉ 1 vịt vô địch cán đích): PASS
- Tiêu chí 4 (Vẽ chướng ngại vật trực tiếp trên sông): PASS
- Tiêu chí 5 (Chuyển quyền trả lời Zero-click, không modal chặn): PASS
- Tiêu chí 6 (Phím tắt Space/1-4/A-D/Enter/H & Vịt cứu trợ): PASS
- Tiêu chí 7 (Loại trừ học sinh đã gọi & lịch sử tích điểm): PASS

## Bug
(Không có bug)
