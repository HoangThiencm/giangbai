# Ghi chú trao đổi dự án giangbai — Xếp thời khóa biểu

Cập nhật: 09/07/2026  
Mục đích: tài liệu để **nhờ đánh giá / review** (không phải spec kỹ thuật chính thức).

---

## 1. Tóm tắt một dòng

Phần xếp TKB đã có **nền prototype/triển khai nội bộ đáng giá** (đủ luồng, solver hard cơ bản, làm đẹp, audit, multi-đợt, Web Worker), nhưng **chưa nên gọi là “ổn sản xuất cho trường lớn”** nếu chưa có benchmark 16–30 lớp ổn định, phân quyền theo đơn vị/user, và làm rõ thêm trải nghiệm hard vs soft.

---

## 2. Phạm vi đã làm

### 2.1. Luồng người dùng

```text
Đơn vị / năm học / đợt
  → Dữ liệu (GV → Lớp → Phòng BM → Phân công)
  → Thiết lập (khung sáng/chiều, gói tiết đầu, ngoại lệ, max môn/ngày)
  → Kiểm tra (precheck)
  → Xếp lịch (Worker)
  → Xem theo lớp / GV + audit chất lượng
  → Lưu hosting / xuất CSV / in
```

### 2.2. File chính

| File | Vai trò |
|------|---------|
| `thoikhoabieu.html` | UI + orchestration + (vẫn còn bản solver trong page làm fallback) |
| `thoikhoabieu-engine.js` | Solver **pure** (không DOM) — dùng chung Worker + benchmark |
| `thoikhoabieu-worker.js` | Web Worker xếp ngoài main thread |
| `api/thoikhoabieu.php` | API multi-đợt: list/get/create/save/update_meta/lock/unlock/delete/delete_unit/clear_result |
| `data/tkb-demo-30lop-ct2018.json` | Dữ liệu demo CT 2018 để rà soát |
| `agent-tools/extract-tkb-engine.js` | Tách lại engine từ HTML khi sửa solver |
| `agent-tools/benchmark-tkb.js` | Benchmark chuẩn small / medium / large |
| `agent-tools/build-demo-30-ct2018.js` | Sinh JSON demo 30 lớp |

### 2.3. Ràng buộc **hard** (hợp lệ)

- Không trùng **lớp** cùng ô
- Không trùng **giáo viên** cùng ô
- Không trùng **phòng** cùng ô
- Buổi/tiết **tránh của GV** (`T2S`, `T5S1`, `T6C2-3`…)
- Buổi học của lớp (sáng / chiều / 2 buổi)
- Khung tiết sáng/chiều (từ–đến)
- Ô **ngoại lệ toàn trường** (blocked slots)
- Capacity lớp vs tổng tiết phân công
- Định mức tiết/tuần của GV
- Max cùng môn / ngày / lớp

→ **Hợp lệ 100%** = xếp đủ tiết, không vi phạm hard (precheck + solver).

### 2.4. Tiêu chí **soft / đẹp** (chất lượng)

- Gói từ tiết đầu buổi (không trống tiết 1 rồi mới học tiết 2)
- Không **lủng** giữa buổi (trống cuối buổi vẫn OK)
- Ưu tiên **tiết đôi** liền (Toán/Văn/Anh/KHTN…)
- Giảm **tiết mồ côi GV** (buổi chỉ 1 tiết lẻ)
- Giảm lủng lịch GV; môn chính ưu tiên tiết sớm
- Cân tải ngày trong tuần (mềm)

→ Lịch có thể **hard 100%** nhưng soft vẫn **cảnh báo** (chưa đẹp). UI tách rõ hai tầng này.

### 2.5. Quản lý đợt / đơn vị (API + UI)

| Chức năng | Có |
|-----------|-----|
| Khai báo **đơn vị** | Có |
| **Năm học** | Có |
| **Đợt** xếp TKB (thêm / chọn / sửa tên) | Có |
| **Khóa / mở khóa** đợt | Có |
| Xóa kết quả xếp (giữ data đầu vào) | Có |
| Xóa 1 đợt | Có |
| Xóa **toàn bộ đợt** của đơn vị | Có |
| Lưu project + result lên hosting | Có |

Schema: `unit_name`, `name` (đợt), `school_year`, `is_locked`, `project_json`, `result_json`.

### 2.6. Demo / CT 2018

- Khung tiết gần CT GDPT 2018 THCS (Tin học **1** tiết/tuần, LS+ĐL ≈ 3, KHTN 6–7 gộp / 8–9 tách…).
- Demo nhỏ (4 lớp) và Demo 30 lớp (57 GV ≈ 1,9 GV/lớp).
- Import Excel: **không** gán “phòng ưu tiên GV” thành `roomNeed` bắt buộc (đã sửa).

### 2.7. Worker + benchmark

- Page ưu tiên **Web Worker**; lỗi Worker → fallback main thread.
- Benchmark:

```text
node agent-tools/extract-tkb-engine.js          # khi đổi solver trong HTML
node agent-tools/benchmark-tkb.js --size small  # 4 lớp
node agent-tools/benchmark-tkb.js --size medium # 16 lớp
node agent-tools/benchmark-tkb.js --size large  # 30 lớp
node agent-tools/benchmark-tkb.js --size all
```

**Kết quả small (engine, 09/07/2026):**

| Chỉ số | Giá trị |
|--------|---------|
| Hard | **PASS 112/112** |
| Lủng lớp / trống tiết đầu | **0 / 0** |
| Mồ côi GV (soft) | còn (~5) |
| Thời gian | ~4–5 s |

Medium/large: cần chạy lại khi review (CPU máy dev); kỳ vọng lâu hơn, có thể partial nếu data/constraints chặt.

---

## 3. Đánh giá nhanh (để người review thống nhất)

### Điểm mạnh

1. Đủ **luồng nghiệp vụ** thực tế: GV → lớp → phòng → phân công → kiểm tra → xếp → audit → xuất/in/lưu.
2. Solver xử lý **hard cơ bản** đúng bài toán trường phổ thông.
3. Có **làm đẹp** + audit (lủng, tiết đầu, mồ côi) — không chỉ “nhét đủ tiết”.
4. **Tách hard vs soft** trên UI (người dùng hiểu: hợp lệ ≠ đã đẹp).
5. Multi-đợt / đơn vị / năm học / khóa — nền quản lý, không chỉ một file local.
6. Engine tách + Worker + benchmark — hướng kỹ thuật đúng để scale.

### Điểm yếu / rủi ro

1. **CPU-bound**: 16–30 lớp vẫn có thể 30–120s+; Worker tránh đơ UI nhưng không rút thời gian thuật toán.
2. **Gói tiết đầu**: soft khi xếp (ưu tiên 100%), beautify sau; có thể hard OK + soft còn cảnh báo.
3. **Phòng ưu tiên GV**: chưa có logic soft-prefer riêng (chỉ hết nhầm thành roomNeed khi import).
4. **Benchmark 16/30** chưa gắn CI; script cũ (`loadSampleData16`, demo JScript) lệch so solver hiện tại — đã thay bằng `benchmark-tkb.js` nhưng cần chạy đủ large khi review.
5. **Phân quyền**: GV có quyền trang TKB thấy/sửa các đợt theo danh sách chung — **chưa** giới hạn theo user/đơn vị. Nhiều trường chung host → rủi ro.
6. Solver vẫn **trùng lặp** một phần trong HTML + engine (cần discipline chạy `extract-tkb-engine.js` khi sửa).

### Kết luận mức độ

| Mức | Phù hợp? |
|-----|----------|
| Prototype / demo / dùng nội bộ 1 trường, quy mô vừa | **Có** |
| Production nhiều trường, 30–40+ lớp, SLA vài giây | **Chưa** |

---

## 4. Việc nên ưu tiên tiếp (gợi ý cho đánh giá / roadmap)

| # | Việc | Lý do |
|---|------|--------|
| 1 | Chạy & lưu kết quả benchmark **medium + large** (máy/CI) | Chứng minh scale, không chỉ small |
| 2 | Phân quyền **đơn vị / owner** trên API | An toàn multi-tenant |
| 3 | Soft **preferredRooms** cho GV (không hard) | Đúng nghiệp vụ |
| 4 | Giảm thời gian solver (heuristic tốt hơn / backend job) | Trải nghiệm trường lớn |
| 5 | Đồng bộ single source: HTML chỉ orchestration, engine là chuẩn | Tránh lệch Worker vs page |
| 6 | (Tuỳ chọn) Slot cố định Chào cờ / SH; cờ tiết đôi trên phân công | Gần tkb.com.vn hơn |

---

## 5. Cách reviewer tự kiểm tra nhanh

1. Mở `thoikhoabieu.html` (đăng nhập GV có quyền TKB), **Ctrl+F5**.
2. Thanh **Đơn vị / Năm học / Đợt** → Thêm đợt → Demo nhỏ hoặc Demo 30.
3. Bước **Kiểm tra** → xem lỗi hard.
4. **Xếp lịch** → banner: `Hard: 100%` vs soft; KPI Hợp lệ / Chất lượng.
5. CLI: `node agent-tools/benchmark-tkb.js --size small` (kỳ vọng PASS 112/112).
6. API: tạo / khóa / xóa đợt (cần session teacher + DB).

---

## 6. Tham chiếu nghiệp vụ

- tkb.com.vn / OLM TKB: quy trình khai báo → ràng buộc → xếp → tinh chỉnh.
- CT GDPT 2018 THCS: tiết/tuần quy đổi ~35 tuần (Tin 1, Văn/Toán 4, Anh 3…).

---

*Tài liệu phục vụ review. Khi chốt production, chuyển phần ổn định sang `thongtin.md`.*
