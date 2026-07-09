# Xếp thời khóa biểu — bản đánh giá / hoàn thiện

Cập nhật: **09/07/2026** (đã bắt đầu **Cấu hình nhà trường** + checklist production + báo nghẽn)  
Mục đích: tài liệu review trung thực + hướng phát triển.

---

## 1. Kết luận công bằng (đã thống nhất)

### 1.1. Hai lớp đánh giá — không gộp

| Lớp | Ý nghĩa | Hiện tại |
|-----|---------|----------|
| **Engine / benchmark** | Solver chạy trên dữ liệu *sinh sẵn* (script, RAM) | **Có nền**, bench pass (kể cả large giả lập) |
| **App TKB trường** | Dữ liệu thật + nghiệp vụ đủ + UI đúng | **Chưa đạt** |

Benchmark 30 lớp chỉ chứng minh: *engine có thể xếp một bộ dữ liệu giả lập được thiết kế tương đối hợp lý*.  
Nó **không** chứng minh: *ứng dụng xếp được TKB cho trường thật*.

### 1.2. Kết luận đúng lúc này

| | |
|--|--|
| Engine | Có tiến bộ (hard/pack trên bench) |
| UI / nghiệp vụ | Còn thiếu — gần “công cụ phân công môn–lớp” hơn “hệ TKB nhà trường” |
| Dữ liệu thật | **Chưa** chứng minh xếp 100% |
| Gọi “app TKB tốt / hoàn chỉnh” | **Không** |
| Bước tiếp | **Mô hình dữ liệu nhà trường + ràng buộc thực tế** → solver trên đợt CSDL thật → audit |

**Đừng lấy “100% large benchmark” để kết luận app xong.**

### 1.3. Ưu tiên đúng (thứ tự)

1. **Tách rõ** benchmark kỹ thuật ↔ dữ liệu production (CSDL / đợt UI).  
2. Thêm **Cấu hình nhà trường**: BGH, tổ chuyên môn, GVCN, môn/CT, tiết cố định.  
3. Checklist **dữ liệu thật đã đủ chưa** trước khi xếp.  
4. Khi không 100%: chỉ rõ nghẽn — **lớp / môn / GV / phòng / ràng buộc** nào.  
5. Đo trên **một đợt thật** trong CSDL: `placed/total`, lỗi nghẽn, lủng, tiết đầu, mồ côi GV.

### 1.4. Bảng trạng thái chi tiết

| Phần | Hiện trạng |
|------|------------|
| Engine hard (bench giả lập) | Có nền; large sinh sẵn đã pass kỹ thuật |
| Benchmark 30 lớp / 840 tiết | Test trong RAM — **không** từ CSDL |
| Soft pack / soft GV (bench) | Pack tốt hơn; orphans/tGaps còn |
| UI nhập | Sơ sài |
| Nghiệp vụ trường học | **Thiếu nhiều** |
| Ràng buộc thực tế | Một phần (nghỉ GV cứng, pack, phòng BM…) |
| App TKB hoàn chỉnh | **Chưa đạt** |

---

## 2. Benchmark giả lập — phạm vi và giới hạn

```text
node agent-tools/extract-tkb-engine.js
node agent-tools/benchmark-tkb.js --size small|medium|large|all
```

| | |
|--|--|
| **Là gì** | `buildLarge(30)` / `buildSmall()` trong `agent-tools/benchmark-tkb.js` sinh GV–lớp–PC–phòng **tạm trong RAM** → `thoikhoabieu-engine.js` |
| **Không là gì** | Không đọc CSDL; không phải đợt trong `timetable_projects.project_json` |
| **Chứng minh được** | Engine *có khả năng* xếp một bộ CT2018-like “sạch” (capacity/GV/phòng cân bằng hơn thực tế) |
| **Không chứng minh** | 100% trên dữ liệu nhập tay / import / CSDL thật |

**Mốc kỹ thuật gần nhất (máy dev, chỉ bench):**

| Size | Hard (bench) | Soft pack (bench) | Time (tham chiếu) |
|------|--------------|-------------------|------------------|
| small ~112 tiết | PASS | holes/startLate ~0 | ~3–4s |
| medium ~448 | PASS | holes/startLate ~0 | ~25–30s |
| large ~840 | PASS | holes/startLate ~0 (sau repair) | ~12s |

> Orphans/tGaps trên large bench vẫn có thể cao — soft “đẹp GV” chưa xong.

---

## 3. Đã có (kỹ thuật) — không thổi phồng

| Hạng mục | Ghi chú |
|----------|---------|
| Snapshot lúc xếp | `freezeSolveSnapshot` + render theo snapshot |
| Worker + engine pure | `thoikhoabieu-engine.js` / worker; marker extract |
| Multi-đợt + owner API | `api/thoikhoabieu.php` v3 |
| Nghỉ GV = ràng buộc **cứng** | Cột “Tiết nghỉ / ngày nghỉ”; parse `T2`, `T2S`, `T5S1`, `T6C2-3`… |
| Kiểm tra / KPI hard–soft | Diagnostics + audit sau xếp |
| Solver large path | Slot-scan + repair pack (không rơi CSP 840 treo lâu) |

UI gần đây đã **làm rõ** nghỉ GV (label, placeholder, tóm tắt Kiểm tra). **Chưa** đủ để gọi là mô hình trường đầy đủ.

---

## 4. Thiếu so với TKB nhà trường thật

### 4.1. Nghiệp vụ / cấu trúc

- Cơ cấu BGH: Hiệu trưởng, phó HT, tổ trưởng / tổ chuyên môn  
- **GVCN** theo lớp; tiết SH, chào cờ, HĐTN gắn vai trò  
- Danh mục **môn chuẩn**: nhóm môn, tiết/tuần theo khối, phòng BM, tiết đôi, tránh tiết cuối  
- Lớp đầy đủ: khối, buổi, phòng, GVCN, sĩ số, ghi chú  
- GV: tổ CM, vai trò (GVBM/GVCN/tổ trưởng/BGH), định mức, nghỉ, phòng ưu tiên, lớp được PC  
- Luồng: nhập → kiểm tra → duyệt → khóa đợt → xuất theo lớp/GV/tổ  

### 4.2. Ràng buộc thực tế (mới một phần)

| Có một phần | Còn thiếu / mờ |
|-------------|----------------|
| Nghỉ GV cứng | Tiết cố định toàn trường / lớp (chào cờ, SH) rõ nghiệp vụ |
| Pack từ tiết đầu | “Không xếp môn nặng cuối buổi” cấu hình được |
| Phòng BM / max môn-ngày | Ràng buộc theo tổ, theo khối, theo phòng chi tiết |
| Precheck capacity / ĐM | Báo cáo nghẽn *dễ hiểu* trên dữ liệu thật + gợi ý sửa |

### 4.3. Vì sao dữ liệu thật dễ “không 100%”

1. Phân công thiếu GV / lệch tổ môn  
2. GV nghỉ nhiều → domain hẹp  
3. Phòng BM thiếu  
4. Lớp / ĐM quá tải  
5. UI chưa buộc nhập đủ mô hình → precheck chưa bắt hết trước khi xếp  

**Khi không 100% trên dữ liệu thật**, cần ghi rõ:

1. Đã xếp bao nhiêu / tổng bao nhiêu tiết?  
2. Cảnh báo / blocked lesson: môn–lớp–GV nào?  
3. Nghỉ GV, phòng, ĐM, capacity lớp?  
4. Đủ GV theo từng môn không?

---

## 5. Hướng phát triển đúng (ưu tiên nghiệp vụ, không chỉ label)

Thêm bước **“Cấu hình nhà trường”** *trước* phân công (luồng gợi ý):

| # | Khối | Nội dung chính |
|---|------|----------------|
| 1 | **Nhà trường** | Đơn vị, năm học, BGH; tổ CM + tổ trưởng |
| 2 | **Lớp học** | Khối, tên, buổi, phòng lớp, **GVCN**, SH cố định |
| 3 | **Giáo viên** | Tổ, vai trò, ĐM, **tiết/ngày nghỉ**, môn, phòng ưu tiên |
| 4 | **Môn & CT** | Tiết/tuần theo khối; phòng BM; tiết đôi; tránh tiết cuối |
| 5 | **Phân công** | Lớp–môn–GV–số tiết–phòng–ghi chú |
| 6 | **Ràng buộc** | Toàn trường / lớp / GV / môn / phòng |
| 7 | **Xếp + duyệt + xuất** | Hard/soft KPI; khóa đợt; TKB lớp / GV / tổ |

**Thứ tự kỹ thuật đề xuất:**

1. Mô hình dữ liệu + UI cấu hình (JSON project mở rộng, tương thích bản cũ).  
2. Precheck bám mô hình mới (lỗi đỏ đủ trước khi xếp).  
3. Map ràng buộc mới → domain / soft cost solver.  
4. Đo **100% trên đợt CSDL thật** (không chỉ bench).  
5. Soft đẹp (orphans/gaps) sau khi hard thật đã ổn.

---

## 6. Checklist reviewer (cập nhật)

### Kỹ thuật (bench)

1. `benchmark-tkb.js --size large` → hard PASS (hiểu đúng: **chỉ bench**).  
2. Engine pure, snapshot, owner API.

### Nghiệp vụ / dữ liệu thật (bắt buộc nếu nói “app TKB”)

1. Mở đợt **thật** trên UI/CSDL (không chỉ script).  
2. Xếp → ghi `placed/total`, status, blocked, audit soft.  
3. Kiểm tra: nghỉ GV, phòng, ĐM, capacity, đủ GV theo môn.  
4. Chỉ khi **hard 100% trên đợt thật** mới được gọi “xếp được cho trường này”.

---

## 7. Roadmap ngắn (bám §1.3)

| Ưu tiên | Việc | TT |
|---------|------|-----|
| P0 | Tách benchmark ↔ production (docs + KPI kết quả `source: production-batch`) | ✅ đang |
| P0 | **Cấu hình nhà trường** schema + UI (tab Nhà trường / Môn CT / GVCN / tổ / fixedSlots) | ✅ v1 |
| P0 | Checklist dữ liệu thật trước xếp | ✅ v1 |
| P0 | Fail → nghẽn lớp/môn/GV (bottlenecks) | ✅ v1 |
| P0 | Đo đợt CSDL thật (user: Lưu + Xếp + xem metrics) | ⏳ thao tác |
| P1 | Nối sâu ràng buộc (tiết đôi/tránh cuối từ danh mục môn; SH gán GVCN) | ⏳ |
| P2 | Soft orphans/tGaps; progressive Worker; xuất theo tổ/GVCN | ⏳ |

### 7.1. Đã ship UI/nghiệp vụ v1 (09/07/2026)

| Thành phần | Chi tiết |
|------------|----------|
| Tab **Nhà trường** | BGH (HT/PHT), tổ CM + tổ trưởng |
| Tab **Môn / CT** | Danh mục môn, tiết/khối 6–9, phòng BM, tiết đôi, tránh cuối; nút nạp CT2018 gợi ý |
| Tab **Giáo viên** | + tổ CM, vai trò, tiết/ngày nghỉ (cứng) |
| Tab **Lớp** | + khối, GVCN, sĩ số, tiết cố định lớp |
| **Thiết lập** | `fixedSlots` toàn trường (chào cờ/SH) + blockedSlots |
| **project_json** | `school`, `departments`, `subjects` + field mở rộng (tương thích đợt cũ) |
| **Kiểm tra** | Checklist đủ lớp/GV/PC/phòng; thiếu BGH/tổ/GVCN/môn; vượt ĐM/phòng |
| **Sau xếp** | `metrics`: placed/total, holes, startLate, orphans, tGaps; `bottlenecks` theo lớp/môn/GV |

**Nguyên tắc:** UI/nghiệp vụ trước → solver trên dữ liệu thật → audit; **không** lấy bench 100% kết luận app xong.

---

## 8. Lịch sử kỹ thuật (tóm tắt, không dùng làm “đã production”)

- Snapshot, Worker, extract engine, multi-tenant owner.  
- Large path: slot-scan + `repairClassPack` / replan — bench large hard+pack 0/0 ~12s.  
- UI nghỉ GV: label **Tiết nghỉ / ngày nghỉ**, Kiểm tra tóm tắt ô khả dụng.  
- **Sai cách nói trước đây:** “100% large” như thể đã xong app trường → **chỉ đúng trên bench giả lập**.

---

## 9. Kết luận gửi reviewer

| Được phép nói | Không được nói (cho đến khi có bằng chứng) |
|---------------|---------------------------------------------|
| Có engine xếp riêng, bench CT2018-like pass | “Mạnh / production / xếp tốt mọi trường” |
| Có nền hard + pack trên dữ liệu *sinh sẵn* | “100%” đồng nghĩa dữ liệu CSDL/UI thật |
| UI–nghiệp vụ còn sơ; cần cấu hình nhà trường | “Ứng dụng TKB hoàn chỉnh” |

**Đánh giá chốt:**  
*Ứng dụng đang ở mức **thử nghiệm có engine riêng**. Engine có nền thuật toán; **chưa đủ** nếu dữ liệu thật chưa xếp 100% và mô hình trường còn thiếu. Bước tiếp theo: **nghiệp vụ + dữ liệu + ràng buộc**, rồi mới khẳng định chất lượng xếp trên thực tế.*

---

*File này để nhờ đánh giá. Khi hard 100% trên đợt thật + đủ mô hình trường, chuyển phần ổn định sang `thongtin.md`.*
