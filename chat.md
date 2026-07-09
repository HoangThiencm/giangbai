# Xếp thời khóa biểu — bản đánh giá / hoàn thiện

Cập nhật: **09/07/2026** (phiên large hard + orphan)  
Mục đích: tài liệu nhờ review + ghi nhận tiến độ tối ưu.

---

## 1. Kết luận ngắn

| Mức | Đánh giá |
|-----|----------|
| Demo / nội bộ trường vừa (≤16 lớp hard 100%) | **Đủ tốt** — hard + pack soft ổn |
| Large 30 lớp · 840 tiết hard 100% | **Đã PASS ổn định ~5–7s** (mốc mới) |
| Soft “đẹp lịch” (mồ côi GV, lủng large) | **Cải thiện rõ, chưa xong** |
| Production multi-trường tự tin | **Gần hơn** — hard large đã đứng; soft lớn + tenant admin còn siết |
| Multi-tenant an toàn | **Đã siết owner** (`created_by` / admin) |

**Nói gọn:** đã vượt mức “demo vừa”; large hard không còn là điểm nghẽn chính. Còn lại chủ yếu **chất lượng mềm** (orphans, holes large) và chiến lược solver sâu hơn.

---

## 2. Đã xử lý theo phản biện review

### 2.0. Vòng review P1/P2 — đã chốt

| Finding | Xử lý |
|---------|--------|
| **[P1] Admin bị 403** | `tkb_current_user()`: **admin/superadmin** vào API; teacher vẫn cần quyền trang `thoikhoabieu` |
| **[P1] Render kết quả theo state UI** | `resultView()` + `withViewRules()` — dùng **snapshot lúc xếp** |
| **[P2] Engine pha tạp UI** | Marker `// === TKB_ENGINE_END ===`; extract trước freeze/Worker/DOM |
| **[P2] Large 30 lớp** | **Đã chốt hard PASS** (xem §2.6 / §8) |

### 2.1. Snapshot đóng băng

- `freezeSolveSnapshot()` — clone lúc bấm **Xếp lịch**
- Worker + fallback main thread xếp đúng snapshot; restore state UI sau
- `applySolveOutcome(result, snapshot)` — bảng/KPI theo snapshot

### 2.2. Web Worker + engine

| File | Vai trò |
|------|---------|
| `thoikhoabieu-engine.js` | Solver pure (tách từ HTML) |
| `thoikhoabieu-worker.js` | Xếp ngoài main thread |
| `agent-tools/extract-tkb-engine.js` | Chạy lại khi sửa solver trong HTML |

UI ưu tiên Worker; lỗi → fallback main **vẫn dùng snapshot**.

### 2.3. Hard vs soft (UI)

| Tầng | Ý nghĩa |
|------|---------|
| **Hợp lệ (hard)** | Đủ tiết, không trùng GV/lớp/phòng, precheck… |
| **Chất lượng (đẹp)** | Gói tiết đầu, lủng, tiết đôi, mồ côi GV |

KPI: `Hard: 100% … Soft: …`

### 2.4. Multi-tenant API

`api/thoikhoabieu.php` schema **v3**: list/get/save/lock/delete theo **owner** hoặc admin.

### 2.5. Import

Không map `preferredRooms` → `roomNeed` bắt buộc khi import Excel.

### 2.6. Benchmark chuẩn

```text
node agent-tools/extract-tkb-engine.js
node agent-tools/benchmark-tkb.js --size small|medium|large|all
```

**Kết quả đo máy dev (09/07/2026, sau slot-scan + orphan swap):**

| Size | Dataset | Hard | Soft (holes / startLate / orphans) | Thời gian |
|------|---------|------|-------------------------------------|-----------|
| small | 4 lớp · 112 tiết | **112/112 PASS** | 0 / 0 / **~1** | ~3.6 s |
| medium | 16 lớp · 448 tiết | **448/448 PASS** | 0 / 0 / **~18** | ~28 s |
| large | 30 lớp · 840 tiết | **840/840 PASS** | ~22 / ~1 / **~32** | **~5–7 s** |

> Trước đó large: partial (vd 818/840) hoặc CSP treo >100s.  
> Đã **cắt improve/beautify nặng** trên large + **không rơi CSP 840 biến**.

### 2.7. Quản lý đợt

Đơn vị · năm học · đợt · khóa · xóa · lưu hosting (giữ nguyên).

---

## 3. Điểm mạnh

1. Luồng đủ: data → thiết lập → kiểm tra → xếp → audit → xuất/in/lưu.  
2. Hard cơ bản đúng; **large hard 100% nhanh**.  
3. Soft + audit có thật (lủng, tiết đầu, mồ côi).  
4. Engine / Worker / benchmark **có trong repo**.  
5. Snapshot freeze đã vá bug lệch UI.  
6. Heuristic large có hướng rõ: **chia theo ô + multi-seed + chain repair**.

---

## 4. Rủi ro còn lại (thành thật)

| # | Rủi ro | Ghi chú |
|---|--------|---------|
| 1 | **Large soft** (holes ~22, startLate, orphans ~32) | Hard xong; lịch “đẹp” large chưa đạt demo nhỏ |
| 2 | **Mồ côi GV medium ~18** | Đã giảm mạnh (từng ~50–67); chưa về gần 0 |
| 3 | Solver vẫn **heuristic** | Chưa chia bài theo khối tối ưu, progressive timeout UX, seed học được |
| 4 | Worker ≠ rút CPU | Chỉ giữ UI mượt |
| 5 | HTML + extract engine | Phải `extract-tkb-engine.js` sau mỗi sửa solver trong HTML |
| 6 | Admin cross-owner | Cần role admin thật trên môi trường |

---

## 5. File cần review

| File | Nội dung |
|------|----------|
| `thoikhoabieu.html` | UI, snapshot, Worker, **`solveBySlotScan`**, orphan reduce |
| `thoikhoabieu-engine.js` | Solver pure (sinh từ extract) |
| `thoikhoabieu-worker.js` | Worker |
| `api/thoikhoabieu.php` | Multi-đợt + owner |
| `agent-tools/benchmark-tkb.js` | small/medium/large |
| `agent-tools/extract-tkb-engine.js` | Tách engine |

---

## 6. Checklist reviewer

1. Ctrl+F5 → đợt user A không lộ sang user B.  
2. Xếp small/demo → Hard 100%; sửa form giữa chừng **không** lệch snapshot.  
3. `node agent-tools/benchmark-tkb.js --size small` → PASS.  
4. `node agent-tools/benchmark-tkb.js --size medium` → PASS hard, soft holes/startLate = 0.  
5. `node agent-tools/benchmark-tkb.js --size large` → **PASS 840/840**, thời gian &lt; 15s (mốc hiện tại ~5–7s).  
6. Ghi nhận soft orphans medium/large (mốc: ~18 / ~32).  
7. Khóa đợt → không lưu/xếp/xóa được.

---

## 7. Roadmap còn lại

1. ~~Chốt large 100% hard + &lt; 60s~~ → **đã đạt** (~5–7s).  
2. **Soft large:** pass đóng lủng / tiết 1 sau hard (không gỡ hard).  
3. **Orphan densify theo cụm GV** (cluster day, không chỉ move/swap 1-1).  
4. Progressive best-so-far trong Worker khi timeout.  
5. Single source of truth: page import engine, bớt duplicate.  
6. (Tuỳ chọn) Preferred room soft; slot cố định Chào cờ/SH.

---

## 8. Phiên tối ưu large + orphans (09/07/2026)

### Vấn đề trước phiên

1. Large 30 lớp / 840 tiết — **chưa PASS ổn định** (CSP chậm / partial).  
2. Medium hard 100% nhưng **nhiều tiết mồ côi GV**.  
3. Solver heuristic, thiếu chiến lược chia bài toán cho scale lớn.

### Việc đã làm

| Hạng mục | Chi tiết |
|----------|----------|
| **`solveBySlotScan`** | Xếp theo ô (ngày×buổi×tiết), mọi lớp đồng thời; multi-seed (đảo ngày/tiết); residual; repair 1–2 hop; **chain repair depth 3**; steal slot môn mềm cùng lớp |
| **Không rơi CSP large** | `n > 600` trả lời từ wave/slot-scan (tránh treo 100s+) |
| **`reduceTeacherOrphans`** | Dồn ngày dày; ghép 2 orphan cùng GV; **swap cùng lớp**; **không phá pack** (tiết 1 / lủng) |
| **Medium/small** | Orphan pass sau beautify (pack-safe) |
| **Extract + bench** | `extract-tkb-engine.js` → small/medium/large |

### Diễn biến large (hard)

| Mốc | placed | Ghi chú |
|-----|--------|---------|
| Wave/class cũ + CSP | partial / timeout | CSP 840 biến không khả thi |
| Slot-scan v1 | 818/840 ~5s | Kẹt chủ yếu KHTN (nghẽn lịch GV) |
| + ưu tiên môn nhiều tiết + repair | 838/840 | Còn 2 tiết lẻ |
| + chain repair + multi-seed | **840/840 ~5–7s** | **PASS ổn định** |

### Soft (orphans) — xu hướng

| Size | Trước (ước lượng phiên trước) | Sau phiên |
|------|-------------------------------|-----------|
| small | vài orphan | **~1** |
| medium | ~50–67 (pack-safe move ít) → trước swap | **~18** (holes/startLate = 0) |
| large | ~40–55 khi partial/full | **~32** (vẫn holes ~22) |

### Còn mở sau phiên

1. Large: giảm holes/startLate (soft-pack repair sau hard).  
2. Medium/large: đẩy orphans thấp hơn (cluster densify).  
3. Progressive timeout + UX best-so-far.  
4. Không tuyên bố “tối ưu hết” — **hard large xong; soft production lớn chưa xong**.

---

*Dùng file này để nhờ đánh giá. Khi chốt production, chuyển phần ổn định sang `thongtin.md`.*
