# IMPLEMENT: Nâng cấp game-racing.html → Đua Xe F1 Mario Kart

Đã triển khai đúng `docs/handoff/PLAN.md` trên `game-racing.html`.

## Thay đổi

### Đường đua & đồ họa F1
- Nền nhựa đường `#0f172a`, vạch sơn animation `trackMove`, hàng rào đỏ-trắng, khán đài cờ hoa.
- Đèn xuất phát 5 đèn đỏ → GO xanh (`soundEngine.f1Lights`).
- 4 siêu xe SVG/CSS: Scuderia Red / Cyan Lightning / Golden Thunder / Neon Phantom.
- Hiệu ứng `nitro-flame`, `smoke-trail`, rung khi sai, spin 360 khi dính chuối; vạch đích ca-rô.

### Cơ chế cả 4 tổ cùng chơi
- Câu hỏi + KaTeX `MathText`, đồng hồ 15/30/45s + thanh co dần.
- GV tick nhiều tổ đúng (nút hoặc phím `1–4`), Enter / nút **XÁC NHẬN BỨT TỐC** → các xe đúng vọt đồng loạt.
- Chuỗi đúng ≥ 2 → SUPER NITRO (+thêm bước + lửa).

### Hộp vật phẩm Mario Kart (bật/tắt trong cài đặt)
- 🚀 Nitro, 🛡️ Khiên, 🍌 Vỏ chuối, ⚡ Tia sét.

### Âm thanh Web Audio (offline)
- `f1Lights`, `engineRev`, `tireScreech`, `nitroBoost`, `podiumFanfare`, tick đồng hồ; nút mute góc trên.

### Bục vinh quang
- Confetti + fanfare; podium 🥇🥈🥉 + danh hiệu; bảng đúng/bước; Đua lại / Về menu.

## Kiểm tra
- Static marker check PLAN features trên `game-racing.html` — PASS.
- Chưa verify tương tác trình duyệt (không có browser tool). Bước tiếp: Antigravity `/verify`.
