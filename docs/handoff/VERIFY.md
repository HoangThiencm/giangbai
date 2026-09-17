# VERIFY

## Kết luận
PASS

## Đối chiếu scope theo `docs/handoff/PLAN.md`
- [x] **Module 1**: Đã thêm cờ `pedagogyConfigured` vào `normalizeTeachingContext` và kích hoạt khi user đổi checkbox PPDH/KTDH/Hoạt động (`js/khbd-app.js` dòng 809, 1025, 1049, 1062, 2434) — **PASS**.
- [x] **Module 1**: Sửa `ensurePedagogyFromLesson` tôn trọng `userConfigured`, không ghi đè khi mảng rỗng (`js/khbd-app.js` dòng 2437, 2447, 2454) — **PASS**.
- [x] **Module 1**: Bỏ fallback `"tps-tech"` trong `applyTimeBudgetGateToPedagogy` (`js/khbd-app.js` dòng 2341–2342) — **PASS**.
- [x] **Module 2**: Bỏ fallback `"tps-tech"` trong `applyGate` của `canvas_soankhbd.html` (dòng 1476–1477) và `backupcode viettailieu/canvas_soankhbd.html` (dòng 1423–1424) — **PASS**.
- [x] **Module 3**: Cập nhật `ACTIVITY_TABLE_CONTRACT_COMPACT` cấm KTDH/PPDH khi không chọn ở chế độ rút gọn (`js/khbd-prompts.js` dòng 350) — **PASS**.
- [x] **Module 3**: Cập nhật các prompt template `GENERATE_ACTIVITY_B/C/D` thành chỉ áp dụng có điều kiện (`js/khbd-prompts.js` dòng 746, 812, 866) — **PASS**.
- [x] **Module 3**: Cập nhật `buildPhasePedagogyContext(phase)` thêm `noTechniqueConstraint` và chặn kịch bản khi pha không có KTDH (`js/khbd-app.js` dòng 5437, 5459) — **PASS**.
- [x] **Module 3**: Cập nhật `buildPedagogicalContext()` trong `js/khbd-app.js` (dòng 5178–5180) khi `methodLabels`, `techniqueByPhase`, `activityLabels` rỗng: chỉ thị cấm AI tự ý lấy PPDH/KTDH từ catalog — **PASS**.
- [x] **Module 4**: Bổ sung kiểm thử tự động xác nhận bỏ tick KTDH/PPDH không bị tự động chọn lại trong `tests/canvas-soankhbd-smoke.js` (dòng 56–60) — **PASS**.

---

## Test đã chạy
1. `node tests/canvas-soankhbd-smoke.js` — **PASS 100%**:
   - Kiểm tra cú pháp JavaScript hợp lệ.
   - Đồng bộ tương thích 1-1 giữa `canvas_soankhbd.html` và `backupcode viettailieu/canvas_soankhbd.html`.
   - Kiểm tra cờ `pedagogyConfigured` và xác nhận prompt không chứa câu lệnh ép AI tự lấy KTDH/PPDH từ catalog khi mảng rỗng.
2. `node tests/khbd-pedagogy-rate-smoke.js` — **PASS 100%**:
   - Gate thời lượng 1 tiết, 2 tiết.
   - Chuẩn hóa xuống dòng phân vai GV/HS trong bảng thực hiện.
3. `node tests/khbd-pedagogy-script-smoke.js` — **PASS 100%**:
   - Kịch bản sư phạm thực chiến & xuất Word DOCX.
4. `node tests/khbd-dynamic-time-budgets-smoke.js` — **PASS 100%**:
   - Phân bổ thời lượng động 4 hoạt động A–D.
5. Kiểm tra thực nghiệm Node VM:
   - Khi `pedagogyConfigured = true` và `methods = []`, gọi `getGenerationPromptContext()`: `ctx.methods` giữ nguyên `[]`, không bị `ensurePedagogyFromLesson` ghi đè.
   - Kiểm tra chuỗi `ctx.pedagogical_context`: sinh ra đúng chuẩn:
     `- Phương pháp dạy học: KHÔNG áp dụng PPDH đặc thù riêng (người dùng không chọn hoặc đã bỏ tick)... TUYỆT ĐỐI CẤM tự ý đưa tên PPDH ngoài danh mục...`
     `- Kỹ thuật dạy học theo pha: KHÔNG áp dụng kỹ thuật dạy học riêng nào (người dùng không chọn hoặc đã bỏ tick)... TUYỆT ĐỐI KHÔNG tự ý đưa tên bất kỳ kỹ thuật dạy học nào...`

---

## Bug
Không có.
