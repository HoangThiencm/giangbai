# IMPLEMENT: MP-01 — Mô phỏng diện tích hình bình hành

**Trạng thái:** HOÀN THÀNH — sẵn sàng chuyển `/verify`  
**File đã sửa:** `TROLYTHIEN/2_TAO_BAI_TAP/Ket_qua/MP01_Dien_Tich_Hinh_Binh_Hanh.html`  
**Nguồn:** `docs/handoff/PLAN.md` (đối chiếu `TASK.md`, `DAC_TA_KY_THUAT_MP01_MVP.md`)

## Việc đã làm

1. Tay kéo `#sliderHandle`: `r="25"` (đường kính 50px); `tabindex="0"`, `role="slider"`, `aria-valuemin/max`, `aria-label`; `aria-valuenow` cập nhật theo %.
2. Kéo bằng `svg.createSVGPoint()` + `getScreenCTM().inverse()`; lưu `dragOffset` lúc `pointerdown`; `currentDx = svgX - TRACK_START - dragOffset`.
3. `#sliderControls .slider-track` và `#sliderProgress`: `pointer-events: none`. Chặn `contextmenu` trên SVG. Phím mũi tên ±5% khi chưa khóa. `.sliding-polygon { cursor: default }`.
4. Nút GV: lúc chạy hiện `⏹ Dừng (GV)` + class `active`; lúc dừng hoặc đạt 100% trả về `🎬 Tự động ghép (GV)`. Thời lượng diễn hoạt `2500` ms cho khớp mốc 2,5 giây trong TASK.
5. Nhãn: chỉ biến `a`, `h`, `S` in nghiêng; `= 4 ô`, đơn vị và dấu `·` in đứng.
6. `[ Không thay đổi ]`: phản hồi tán thành, giải thích bảo toàn diện tích. `[ Có thay đổi ]`: đúng câu lưu ý trong PLAN (hình dạng đổi, diện tích không đổi).
7. `shape-rendering="geometricPrecision"` trên `<svg>` và các `<polygon>`.

## Kiểm thử (Mục 5 PLAN)

| Lệnh | Kết quả |
| :--- | :--- |
| `Select-String` liên kết ngoại `https?://\|cdn\|googleapis` | PASS — không khớp |
| `node` `new Function(script)` | `JS Syntax: PASS` |
| `Select-String` `sliderHandle.*r="2[5-9]"` | PASS — `r="25"` |
| `Start-Process msedge` file HTML | Đã mở. Chưa thao tác được kéo/phím trong phiên này. |

Chưa commit, chưa push.
