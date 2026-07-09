# Xếp thời khóa biểu — bản đánh giá / hoàn thiện

Cập nhật: **09/07/2026** (phiên large pack soft: holes/startLate → 0)  
Mục đích: tài liệu nhờ review + ghi nhận tiến độ tối ưu.

---

## 1. Kết luận ngắn

| Mức | Đánh giá |
|-----|----------|
| Demo / nội bộ trường vừa (≤16 lớp) | **Đủ tốt** — hard + pack soft ổn |
| Large 30 lớp · 840 tiết | **Hard 100% + pack soft 0 lủng / 0 trễ tiết 1**, ~12s |
| Soft mồ côi GV / teacherGaps | **Còn** — giảm dần sau (large orphans ~22, tGaps cao) |
| Production multi-trường tự tin | **Gần hơn** — mốc pack large đã đạt; densify GV + tenant còn siết |
| Multi-tenant an toàn | **Đã siết owner** (`created_by` / admin) |

**Nói gọn:** hard scheduling + **pack lớp large** đã đạt mục tiêu demo 30 lớp. Chất lượng “đẹp GV” (orphans/gaps) là backlog tiếp theo, không chặn hard/pack.

---

## 2. Đã xử lý theo phản biện review

### 2.0. Vòng review P1/P2 — đã chốt

| Finding | Xử lý |
|---------|--------|
| **[P1] Admin bị 403** | `tkb_current_user()`: **admin/superadmin** vào API |
| **[P1] Render kết quả theo state UI** | `resultView()` + snapshot lúc xếp |
| **[P2] Engine pha tạp UI** | Marker `// === TKB_ENGINE_END ===` |
| **[P2] Large 30 lớp hard** | **PASS 840/840** |
| **Pack soft large** (review follow-up) | **holes=0, startLate=0** (xem §2.6 / §9) |

### 2.1–2.5. Snapshot / Worker / Hard-soft UI / Multi-tenant / Import

(Giữ như các phiên trước — snapshot freeze, Worker+engine pure, owner API, không map preferredRooms→roomNeed.)

### 2.6. Benchmark chuẩn

```text
node agent-tools/extract-tkb-engine.js
node agent-tools/benchmark-tkb.js --size small|medium|large|all
```

**Kết quả đo máy dev (09/07/2026, sau `repairClassPack` + replan):**

| Size | Dataset | Hard | Soft (holes / startLate / orphans) | Thời gian |
|------|---------|------|-------------------------------------|-----------|
| small | 4 lớp · 112 tiết | **112/112 PASS** | 0 / 0 / **~1** | ~3.6 s |
| medium | 16 lớp · 448 tiết | **448/448 PASS** | 0 / 0 / **~18** | ~25–28 s |
| large | 30 lớp · 840 tiết | **840/840 PASS** | **0 / 0 / ~22** | **~12 s** (&lt; 15s) |

**Mục tiêu đã chốt (large):**

| Tiêu chí | Mục tiêu | Kết quả |
|----------|----------|---------|
| Hard | 840/840 | ✅ |
| Thời gian | &lt; 15s | ✅ ~12s |
| classHoles | 0 | ✅ |
| startLate | 0 | ✅ |
| teacherOrphans | giảm dần sau | ⏳ ~22 (đã có pass pack-safe) |
| teacherGaps | giảm dần sau | ⏳ còn cao khi densify |

> Thứ tự soft đúng review: **pack lớp trước** (holes/startLate), **rồi** orphan GV.  
> Orphan chỉ chạy khi pack đã 0/0 — tránh đổi mồ côi lấy lủng.

### 2.7. Quản lý đợt

Đơn vị · năm học · đợt · khóa · xóa · lưu hosting (giữ nguyên).

---

## 3. Điểm mạnh

1. Luồng đủ: data → thiết lập → kiểm tra → xếp → audit → xuất/in/lưu.  
2. **Large hard 100% nhanh** + **pack soft đạt**.  
3. Soft + audit có thật; thứ tự ưu tiên pack → orphan.  
4. Engine / Worker / benchmark trong repo; engine pure sau extract.  
5. Snapshot freeze; multi-seed large không rơi CSP 840 biến.

---

## 4. Rủi ro còn lại

| # | Rủi ro | Ghi chú |
|---|--------|---------|
| 1 | **teacherOrphans / teacherGaps** large & medium | Pack xong; densify GV còn (large tGaps có thể tăng khi dồn) |
| 2 | Solver vẫn heuristic | Chưa progressive timeout UX / chia khối tối ưu thật |
| 3 | Worker ≠ rút CPU | Chỉ giữ UI mượt |
| 4 | HTML + extract | Phải `extract-tkb-engine.js` sau sửa solver trong HTML |
| 5 | Thời large phụ thuộc multi-seed + repair | Seed xấu → repair nặng hơn; mốc ~12s ổn định trên bench hiện tại |

---

## 5. File cần review

| File | Nội dung |
|------|----------|
| `thoikhoabieu.html` | UI + solver: `solveBySlotScan`, **`repairClassPack`**, orphan reduce |
| `thoikhoabieu-engine.js` | Pure engine (extract) |
| `thoikhoabieu-worker.js` | Worker |
| `api/thoikhoabieu.php` | Multi-đợt + owner |
| `agent-tools/benchmark-tkb.js` | small/medium/large |
| `agent-tools/extract-tkb-engine.js` | Tách engine |

---

## 6. Checklist reviewer

1. Owner isolation đợt A/B.  
2. Snapshot: sửa form giữa xếp không lệch kết quả apply.  
3. `benchmark-tkb.js --size small` → PASS, holes/startLate 0.  
4. `--size medium` → PASS hard, holes/startLate 0.  
5. `--size large` → **PASS 840/840**, **holes=0, startLate=0**, time **&lt; 15s**.  
6. Ghi orphans medium/large (mốc ~18 / ~22).  
7. Khóa đợt.

---

## 7. Roadmap còn lại

1. ~~Large hard 100% &lt; 60s~~ → ✅ ~12s.  
2. ~~Large classHoles=0, startLate=0~~ → ✅.  
3. **Densify GV:** giảm orphans + teacherGaps (cluster day, không phá pack).  
4. Progressive best-so-far trong Worker.  
5. Single source of truth page ↔ engine.  
6. (Tuỳ chọn) Preferred room soft; slot cố định Chào cờ/SH.

---

## 8. Phiên hard large + orphan (trước pack soft)

- `solveBySlotScan` multi-seed + chain repair → hard 840/840.  
- `reduceTeacherOrphans` (move / pair / swap cùng lớp, pack-safe).  
- Medium orphans ~67 → ~18; large hard ổn ~5–8s nhưng soft holes ~22.

---

## 9. Phiên pack soft large (09/07/2026) — follow-up review

### Phản biện / mục tiêu

> Hard large đã tốt; soft xấu (22 lủng, 1 startLate).  
> Ưu tiên: large `840/840 < 15s`, `classHoles=0`, `startLate=0`; orphans giảm dần sau.

### Việc đã làm

| Hạng mục | Chi tiết |
|----------|----------|
| **`repairClassPack`** | recompact / slide / pull / push / forcePack / eject / cross-class swap / **replanClass** |
| **Thứ tự soft large** | pack trước → orphan **chỉ khi** holes=startLate=0 → pack lại nhẹ |
| **Multi-seed chọn pack tốt** | chốt sớm khi pack hoàn hảo; early-stop khi gần tốt |
| **Score pack nặng** trong slot-scan | ưu tiên gói tiết đầu / kề dải lớp |

### Diễn biến soft large

| Mốc | holes / startLate | Ghi chú |
|-----|-------------------|---------|
| Sau hard-only (trước phiên) | ~22 / ~1 | “nhét đủ nhanh” |
| repair strict | ~4 / 0 | còn 9B/9C T2 kiểu dải 1–5 |
| + replanClass + multi-round | **0 / 0** | ✅ |
| + orphan pack-safe | orphans ~22 | tGaps có thể tăng (đánh đổi densify) |

### Bench chốt phiên

```text
large:  Hard PASS 840/840 | holes=0 startLate=0 orphans≈22 | ~12s
medium: Hard PASS 448/448 | holes=0 startLate=0 orphans≈18 | ~26s
small:  Hard PASS 112/112 | holes=0 startLate=0 orphans≈1  | ~3.6s
```

### Còn mở

1. Giảm **teacherOrphans** và **teacherGaps** mà **không** phá pack 0/0.  
2. Ổn định thời gian large dưới tải seed xấu.  
3. Progressive UX.

---

*Dùng file này để nhờ đánh giá. Khi chốt production, chuyển phần ổn định sang `thongtin.md`.*
