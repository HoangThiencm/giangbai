# Xếp thời khóa biểu — bản đánh giá / hoàn thiện

Cập nhật: **09/07/2026** (cuối phiên)  
Mục đích: tài liệu nhờ review + ghi nhận đã xử lý phản biện.

---

## 1. Kết luận ngắn

| Mức | Đánh giá |
|-----|----------|
| Demo / nội bộ trường vừa (≤16 lớp hard 100%) | **Đủ tốt, vượt prototype thô** |
| Production multi-trường + 30 lớp hard ổn định & nhanh | **Gần hơn**, large vẫn cần đo tiếp / tối ưu thêm |
| Multi-tenant an toàn | **Đã siết owner** (created_by / admin) |

---

## 2. Đã xử lý theo phản biện review

### 2.0. Vòng review tiếp (P1/P2) — đã chốt

| Finding | Xử lý |
|---------|--------|
| **[P1] Admin bị 403** | `tkb_current_user()`: cho **admin/superadmin** vào API; teacher vẫn cần quyền trang `thoikhoabieu` |
| **[P1] Render kết quả theo state UI** | `resultView()` + `withViewRules()` — selector/bảng/badge dùng **snapshot lúc xếp** |
| **[P2] Engine pha tạp UI** | Marker `// === TKB_ENGINE_END ===`; extract cắt trước freeze/Worker/DOM; verify không còn `Worker`/`document` trong engine |
| **[P2] Large 30 lớp** | Vẫn mốc mở (small/medium PASS); không chặn 3 fix trên |

### 2.1. Snapshot đóng băng (đúng phản biện)

**Vấn đề:** `runSolveOnMainThread(payload)` từng bỏ payload, đọc `state` UI; `applySolveOutcome` dựng bảng theo `state.classes` hiện tại → nếu user sửa form trong lúc xếp, kết quả lệch snapshot.

**Đã sửa:**

- `freezeSolveSnapshot()` — `JSON` clone lúc bấm **Xếp lịch**
- Worker nhận snapshot đó
- Fallback main thread: tạm gán `state` = snapshot → solve → **restore** state UI
- `applySolveOutcome(result, snapshot)` — `byClass` / `teacherLoad` / chọn lớp xem theo **snapshot**

### 2.2. Web Worker + engine

| File | Vai trò |
|------|---------|
| `thoikhoabieu-engine.js` | Solver pure (tách từ HTML) |
| `thoikhoabieu-worker.js` | Xếp ngoài main thread |
| `agent-tools/extract-tkb-engine.js` | `node agent-tools/extract-tkb-engine.js` khi sửa solver trong HTML |

UI ưu tiên Worker; lỗi → fallback main **vẫn dùng snapshot**.

### 2.3. Hard vs soft (UI)

| Tầng | Ý nghĩa |
|------|---------|
| **Hợp lệ (hard)** | Đủ tiết, không trùng GV/lớp/phòng, precheck, buổi tránh… |
| **Chất lượng (đẹp)** | Gói tiết đầu, lủng, tiết đôi, mồ côi GV |

KPI + banner: `Hard: 100% … Soft: …`  
Chú thích trên bảng kết quả.

### 2.4. Multi-tenant / phân quyền API

`api/thoikhoabieu.php` schema **v3**:

- List/get/save/lock/delete: chỉ **người tạo đợt** (`created_by`) hoặc **admin/superadmin**
- Xóa đơn vị: chỉ đợt của user (admin: cả unit)
- Không còn “mọi GV có quyền TKB thấy hết đợt”

### 2.5. Import phòng ưu tiên

Không gán `preferredRooms` → `roomNeed` bắt buộc khi import Excel.

### 2.6. Benchmark chuẩn

```text
node agent-tools/extract-tkb-engine.js
node agent-tools/benchmark-tkb.js --size small|medium|large|all
```

**Kết quả đo trên máy dev (engine):**

| Size | Dataset | Hard | Soft (holes / startLate) | Thời gian (tham chiếu) |
|------|---------|------|---------------------------|------------------------|
| small | 4 lớp · 112 tiết | **112/112 PASS** | 0 / 0 (còn vài mồ côi GV) | ~3–5 s |
| medium | 16 lớp · 448 tiết | **448/448 PASS** | 0 / 0 | ~25–65 s (tùy version) |
| large | 30 lớp · 840 tiết | **Chưa ổn định 100%** trong các lần tối ưu; đã nhanh hơn (vài s–hàng chục s partial) hoặc CSP lâu nếu budget cao | holes lớp 0 khi partial gói được | **Điểm còn mở** |

> Lưu ý: large từng treo **300s+** do `improve`/beautify nặng — đã cắt improve/beautify cho large; thời gian rút nhưng **tỷ lệ hard 100% large** cần tiếp tục (data concurrent tổ môn / heuristic).

### 2.7. Quản lý đợt (đã có từ trước, giữ nguyên)

Đơn vị · năm học · đợt · thêm/sửa · khóa · xóa TKB · xóa đợt · xóa đơn vị · lưu hosting.

---

## 3. Điểm mạnh (giữ nguyên nhận xét review)

1. Luồng đủ: data → thiết lập → kiểm tra → xếp → audit → xuất/in/lưu.  
2. Hard cơ bản đúng bài toán trường.  
3. Soft + audit có thật (lủng, tiết đầu, mồ côi).  
4. Engine/Worker/benchmark **có trong repo**, không chỉ roadmap.  
5. Snapshot freeze đã vá đúng bug review chỉ ra.

---

## 4. Rủi ro còn lại (thành thật)

| # | Rủi ro | Ghi chú |
|---|--------|---------|
| 1 | **Large 30 lớp hard 100%** | Chưa chốt PASS ổn định; cần tối ưu/heuristic hoặc nới data demo |
| 2 | Soft mồ côi GV vẫn nhiều (medium ~50–67) | Không phá hard; cần beautify riêng nếu muốn “đẹp” |
| 3 | Worker ≠ rút thời gian CPU | Chỉ giữ UI mượt |
| 4 | HTML vẫn chứa solver + extract engine | Phải chạy `extract-tkb-engine.js` sau mỗi sửa solver trong HTML |
| 5 | Admin role trong app hiện chủ yếu `teacher` | `tkb_is_admin_user` sẵn; cần admin thật nếu muốn xem cross-owner |

---

## 5. File cần review

| File | Nội dung |
|------|----------|
| `thoikhoabieu.html` | UI, snapshot, Worker orchestration, multi-đợt UI |
| `thoikhoabieu-engine.js` | Solver pure |
| `thoikhoabieu-worker.js` | Worker |
| `api/thoikhoabieu.php` | Multi-đợt + **owner access** |
| `agent-tools/benchmark-tkb.js` | small/medium/large |
| `agent-tools/extract-tkb-engine.js` | Tách engine |

---

## 6. Checklist reviewer

1. Ctrl+F5 → tạo đợt (user A) → user B không thấy đợt A (cùng host, quyền TKB).  
2. Xếp lịch small/demo → Hard 100%; sửa form giữa chừng **không** đổi kết quả đang apply (snapshot).  
3. `node agent-tools/benchmark-tkb.js --size small` → PASS.  
4. `node agent-tools/benchmark-tkb.js --size medium` → PASS hard.  
5. Large: chạy và ghi nhận PASS/FAIL + thời gian (mốc production).  
6. Khóa đợt → không lưu/xếp/xóa được.

---

## 7. Roadmap còn lại (nếu production lớn)

1. Chốt **large 100%** hard + thời gian mục tiêu (vd &lt; 60s).  
2. Soft pass: giảm mồ côi GV (beautify worker phase 2).  
3. Single source of truth: page chỉ import engine, không duplicate solver.  
4. (Tuỳ chọn) Preferred room soft cho GV; slot cố định Chào cờ/SH.

---

*Dùng file này để nhờ đánh giá. Khi chốt production, chuyển phần ổn định sang `thongtin.md`.*
