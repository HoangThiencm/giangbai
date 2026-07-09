# Xếp thời khóa biểu — bản đánh giá / hoàn thiện

Cập nhật: **09/07/2026** (chốt large pack soft + hard)  
Mục đích: tài liệu nhờ review ngoài + ghi nhận tiến độ.

---

## 1. Kết luận ngắn

| Mức | Đánh giá |
|-----|----------|
| Demo / nội bộ ≤16 lớp | **Đủ tốt** — hard 100%, pack soft 0 lủng / 0 trễ tiết 1 |
| Large 30 lớp · 840 tiết | **Hard 100% + pack soft đạt** (~12s, &lt; 15s) |
| Soft “đẹp GV” (orphans / tGaps) | **Còn mở** — giảm dần, không phá pack |
| Production multi-trường | **Gần hơn** — hard+pack large ổn; densify GV + tenant còn |
| Multi-tenant | **Đã siết owner** (`created_by` / admin) |

**Nói gọn:**

- **Hard scheduling** đã tối ưu tốt (kể cả 30 lớp).  
- **Pack lớp** (classHoles / startLate) large **đã về 0**.  
- **Chưa tối ưu hết:** teacherOrphans, teacherGaps, progressive UX, single-source engine.

---

## 2. Đã xử lý theo review

### 2.0. Checklist P1/P2 + follow-up soft

| Finding | Trạng thái |
|---------|------------|
| Admin 403 | ✅ `tkb_current_user` cho admin/superadmin |
| Render kết quả lệch UI | ✅ snapshot + `resultView` |
| Engine dính DOM/Worker | ✅ marker `TKB_ENGINE_END` + extract pure |
| Large hard 30 lớp | ✅ **840/840** |
| Large soft pack (lủng / tiết 1) | ✅ **holes=0, startLate=0** |
| Orphans / tGaps | ⏳ backlog (pack-safe only) |

### 2.1. Snapshot đóng băng

- `freezeSolveSnapshot()` lúc bấm **Xếp lịch**  
- Worker + fallback main xếp đúng snapshot; restore state UI sau  
- `applySolveOutcome(result, snapshot)` — bảng/KPI theo snapshot

### 2.2. Web Worker + engine

| File | Vai trò |
|------|---------|
| `thoikhoabieu-engine.js` | Solver pure |
| `thoikhoabieu-worker.js` | Xếp ngoài main thread |
| `agent-tools/extract-tkb-engine.js` | Tách lại sau khi sửa solver trong HTML |

### 2.3. Hard vs soft (UI)

| Tầng | Ý nghĩa |
|------|---------|
| **Hard** | Đủ tiết, không trùng GV/lớp/phòng, precheck |
| **Soft pack** | Gói từ tiết đầu, không lủng lớp |
| **Soft GV** | Í mồ côi / gap GV (ưu tiên thấp hơn pack) |

Thứ tự large: **hard → pack lớp → orphan (chỉ khi pack 0/0)**.

### 2.4. Multi-tenant API

`api/thoikhoabieu.php` schema **v3**: list/get/save/lock/delete theo **owner** hoặc admin.

### 2.5. Import

Không map `preferredRooms` → `roomNeed` bắt buộc.

### 2.6. Benchmark

```text
node agent-tools/extract-tkb-engine.js
node agent-tools/benchmark-tkb.js --size small|medium|large|all
```

**Bench máy dev (09/07/2026, sau repairClassPack + replanClass):**

| Size | Dataset | Hard | holes | startLate | orphans | tGaps | Time |
|------|---------|------|-------|-----------|---------|-------|------|
| small | 4 lớp · 112 tiết | **112/112** | 0 | 0 | ~1 | ~2 | ~3.6 s |
| medium | 16 lớp · 448 tiết | **448/448** | 0 | 0 | ~18 | ~57 | ~25–28 s |
| large | 30 lớp · 840 tiết | **840/840** | **0** | **0** | ~22 | ~129 | **~12 s** |

**Mục tiêu large (đã thống nhất sau review soft):**

| Tiêu chí | Mục tiêu | Kết quả |
|----------|----------|---------|
| Hard | 840/840 | ✅ |
| Thời gian | &lt; 15 s | ✅ ~12 s |
| classHoles | 0 | ✅ |
| startLate | 0 | ✅ |
| teacherOrphans | giảm dần sau | ⏳ ~22 |
| teacherGaps | giảm dần sau | ⏳ ~129 (cao — đánh đổi densify) |

### 2.7. Quản lý đợt

Đơn vị · năm học · đợt · khóa · xóa · lưu hosting.

---

## 3. Điểm mạnh

1. Luồng đủ: data → thiết lập → kiểm tra → xếp → audit → xuất/in/lưu.  
2. Large **hard + pack** đạt mốc demo 30 lớp trong &lt; 15s.  
3. Soft audit có thật; **không** đổi orphan lấy lủng.  
4. Engine pure + Worker + benchmark trong repo.  
5. Snapshot freeze; large path **không** rơi CSP 840 biến.

---

## 4. Rủi ro còn lại

| # | Rủi ro | Ghi chú |
|---|--------|---------|
| 1 | Orphans / tGaps | Pack xong; densify GV chưa ổn (large tGaps cao) |
| 2 | Heuristic only | Chưa progressive timeout / chia khối tối ưu sâu |
| 3 | Worker ≠ nhanh CPU | Chỉ UI mượt |
| 4 | HTML + extract | Bắt buộc extract sau sửa solver |
| 5 | Multi-seed + repair | Seed xấu có thể chậm hơn mốc ~12s |

---

## 5. File review

| File | Nội dung |
|------|----------|
| `thoikhoabieu.html` | UI + `solveBySlotScan` + **`repairClassPack`** + orphan |
| `thoikhoabieu-engine.js` | Pure engine (extract) |
| `thoikhoabieu-worker.js` | Worker |
| `api/thoikhoabieu.php` | Multi-đợt + owner |
| `agent-tools/benchmark-tkb.js` | small / medium / large |
| `agent-tools/extract-tkb-engine.js` | Tách engine |

---

## 6. Checklist reviewer

1. Owner: user B không thấy đợt user A.  
2. Snapshot: sửa form khi đang xếp không lệch kết quả apply.  
3. `benchmark --size small` → PASS, holes/startLate = 0.  
4. `benchmark --size medium` → PASS hard, holes/startLate = 0.  
5. `benchmark --size large` → **840/840**, **holes=0**, **startLate=0**, time **&lt; 15s**.  
6. Ghi orphans / tGaps (mốc large ~22 / ~129; medium ~18 / ~57).  
7. Khóa đợt → không lưu/xếp/xóa.

---

## 7. Roadmap

1. ~~Large hard 100% &lt; 60s~~ → ✅ ~12s.  
2. ~~Large classHoles=0, startLate=0~~ → ✅.  
3. **Densify GV** — giảm orphans + tGaps, **giữ pack 0/0**.  
4. Progressive best-so-far (Worker).  
5. Single source of truth page ↔ engine.  
6. (Tuỳ chọn) Preferred room soft; slot cố định Chào cờ/SH.

---

## 8. Lịch sử phiên tối ưu (tóm tắt)

### 8a. Hard large + orphan

- `solveBySlotScan` (ô × multi-seed × chain repair) → hard 840/840 (từ partial/timeout 300s+).  
- `reduceTeacherOrphans` pack-safe → medium orphans ~67 → ~18.  
- Khi đó large soft vẫn ~22 holes / 1 startLate.

### 8b. Pack soft large (follow-up review)

**Phản biện:** hard tốt; soft large xấu; ưu tiên holes/startLate trước orphans.

**Đã làm:**

| Thành phần | Vai trò |
|------------|---------|
| `repairClassPack` | recompact, slide, pull/push, forcePack, eject, swap chéo, **replanClass** |
| Thứ tự soft | pack → orphan **chỉ nếu** pack 0/0 |
| Multi-seed | chọn / chốt theo điểm pack |

**Diễn biến soft large:**

| Mốc | holes / startLate |
|-----|-------------------|
| Hard-only | ~22 / ~1 |
| Repair strict | ~4 / 0 |
| + replanClass | **0 / 0** ✅ |

**Bench chốt:**

```text
large:  840/840 | holes=0 startLate=0 orphans≈22 tGaps≈129 | ~12s
medium: 448/448 | holes=0 startLate=0 orphans≈18 tGaps≈57  | ~26s
small:  112/112 | holes=0 startLate=0 orphans≈1  tGaps≈2   | ~3.6s
```

---

## 9. Kết luận gửi reviewer

| Đã đạt | Chưa đạt |
|--------|----------|
| Hard small/medium/large 100% | Orphans/tGaps “đẹp như TKB chuyên” |
| Large pack soft 0/0 trong &lt; 15s | Progressive timeout UX |
| Snapshot, owner API, engine pure | Page không còn duplicate solver |
| Demo 30 lớp **ấn tượng** | Tự tin production lớn end-to-end |

*File này để nhờ đánh giá. Khi chốt production, chuyển phần ổn định sang `thongtin.md`.*
