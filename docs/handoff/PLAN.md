# PLAN: Khắc phục lỗi Phân đoạn PPCT đa tuần (1/1 thay vì 1/3) & Hiển thị Thời khoá biểu

Trạng thái: CHỜ CODER THỰC HIỆN

---

## 1. Vấn đề & Hiện trạng

### 1.1. Lỗi 1: Bài nhiều tiết trải qua nhiều tuần hiển thị 1/1 thay vì 1/3, 2/3, 3/3 (Bài 11 - Toán 9)
- **Hiện tượng**:
  - Bài 11 (*Tỉ số lượng giác của góc nhọn*, Hình học 9) có tổng cộng 3 tiết: Tuần 1 học 1 tiết, Tuần 2 học 2 tiết.
  - Trên Lịch báo giảng: Tuần 1 hiển thị `1/1` thay vì `1/3`; Tuần 2 hiển thị `1/2, 2/2` thay vì `2/3, 3/3`.
- **Nguyên nhân cốt lõi**:
  - Trong chương trình Toán THCS, PPCT sắp xếp tuần tự theo tuần, xen kẽ giữa các mạch nội dung (ví dụ dòng Đại số nằm xen kẽ giữa dòng Hình học Tuần 1 và Hình học Tuần 2).
  - Trong hàm `parseBaoGiangCurriculum(text)`:
    - Block đang được lưu trong `blocksByPlan.get(key)` với `key = baoGiangKey(entry.class_name, entry.subject)` (chỉ gồm lớp và môn "9|Toán").
    - Khi dòng Hình học Tuần 1 chạy xong, block Bài 11 được lưu vào `blocksByPlan.get("9|Toán")`.
    - Dòng tiếp theo là Đại số Tuần 2 (ví dụ Bài 2) chạy qua, nó đè lên `blocksByPlan.get("9|Toán")` thành block Đại số.
    - Đến khi dòng Hình học Tuần 2 chạy, nó so sánh với `previousBlock` (đang là Đại số) -> không khớp -> tạo một block mới toanh với `totalPeriods = 2`!
    - Kết quả: Bài 11 bị xé làm 2 block riêng biệt: Tuần 1 có `totalPeriods = 1` (`1/1`), Tuần 2 có `totalPeriods = 2` (`1/2, 2/2`).

### 1.2. Lỗi 2: Thời khóa biểu giáo viên đã nhận diện/có số tiết nhưng bảng Buổi sáng và Buổi chiều không hiển thị
- **Hiện tượng**:
  - Cột bên trái hiển thị danh sách GV với huy hiệu `✓ Đã có TKB (12 tiết)`.
  - Nhưng khung bên phải dưới `Buổi sáng` và `Buổi chiều` lại trống trơn.
- **Nguyên nhân cốt lõi**:
  - Khi mở tab, `renderTimetableView()` chỉ gán `selectedTimetableTeacherId` mà không gọi `selectTimetableTeacher()`, biến `editingTimetable` giữ giá trị `null` và bị gán đè `emptyTimetable()`.
  - So sánh `t.id === teacherId` strict so sánh chuỗi với số (khi truyền từ thuộc tính HTML) trả về `undefined`.
  - Trong `applyAiTimetableResult()`, khi bật cờ tự động đồng bộ phân công `autoApply`, nếu phát sinh lỗi ở `renderPool()` hoặc `renderTeachers()`, ngoại lệ ngắt luồng trước khi `renderTimetableWorkspace()` kịp vẽ bảng.
  - Hàm `normalizeTeacherTimetable(raw)` chưa hỗ trợ trường hợp `raw` là JSON string từ CSDL/storage.

---

## 2. Giải pháp kỹ thuật chi tiết (`phancongtochuyenmon.html`)

### 2.1. Sửa thuật toán gom cụm PPCT theo từng mạch (Strand) trong `parseBaoGiangCurriculum`
1. Khóa theo dõi block bài học phải kết hợp cả `key` và `strandKey`:
   ```javascript
   const strandKey = foldText(entry.strand || '');
   const strandBlockKey = `${key}::${strandKey}`;
   const lessonKey = foldText(normalizeBaoGiangLessonTitle(entry.lesson));
   const previousBlock = blocksByStrand.get(strandBlockKey);
   const block = previousBlock && previousBlock.lessonKey === lessonKey
       ? previousBlock
       : { strandKey, lessonKey, totalPeriods: 0, allocatedPeriods: 0 };
   block.totalPeriods += entry.periods;
   blocksByStrand.set(strandBlockKey, block);
   ```
2. Phân đoạn của từng tiết trong block:
   - Khi lặp từng tiết trong dòng: `segment = `${block.allocatedPeriods + index + 1}/${block.totalPeriods}``.
   - Gắn `_segmentBlock = block` vào đối tượng `lesson`.
   - Sau khi duyệt hết toàn bộ entries, chạy một lượt hậu xử lý để chuẩn hoá mẫu số của phân đoạn về đúng `block.totalPeriods` lũy kế cuối cùng:
     ```javascript
     plans.forEach(plan => {
         plan.all.forEach(lesson => {
             const block = lesson._segmentBlock;
             if (block && block.totalPeriods > 0) {
                 lesson.segment = lesson.segment.replace(/\/\d+$/, `/${block.totalPeriods}`);
             }
             delete lesson._segmentBlock;
         });
     });
     ```
   - Tăng `block.allocatedPeriods += entry.periods` sau mỗi entry.

### 2.2. Hoàn thiện và củng cố module Thời khoá biểu
1. `normalizeTeacherTimetable(raw)`: Thêm giải mã an toàn nếu `raw` là chuỗi JSON:
   ```javascript
   function normalizeTeacherTimetable(raw) {
       let parsedRaw = raw;
       if (typeof parsedRaw === 'string') {
           try { parsedRaw = JSON.parse(parsedRaw); } catch (_) { parsedRaw = null; }
       }
       const base = emptyTimetable();
       if (!parsedRaw || typeof parsedRaw !== 'object') return base;
       ...
   }
   ```
2. Giữ vững các cải tiến đã thực hiện:
   - `renderTimetableView()`: Gọi `selectTimetableTeacher(targetId)` ngay khi mở tab.
   - So sánh `String(t.id) === String(teacherId)` trên toàn bộ các hàm TKB.
   - Khung tiết fallback: Sáng `[1, 2, 3, 4, 5]`, Chiều `[1, 2, 3, 4]`.
   - Bọc `applyTimetableToAssignments` trong `try...catch` an toàn ở `applyAiTimetableResult()`, đảm bảo `renderTimetableWorkspace()` và `renderTimetableTeacherList()` luôn luôn được thực thi.

---

## 3. Danh sách File tác động

1. `phancongtochuyenmon.html`:
   - Hàm `parseBaoGiangCurriculum(text)`: Quản lý block bài học theo `strandBlockKey` (`key::strandKey`).
   - Hàm `normalizeTeacherTimetable(raw)`: Thêm hỗ trợ parse chuỗi JSON.
2. `tests/baogiang-weekday-segment-smoke.js`:
   - Thêm test case PPCT có các dòng Đại số và Hình học xen kẽ nhau giữa các tuần:
     - Dòng 1: Tuần 1, Đại số, Bài 1 (2 tiết)
     - Dòng 2: Tuần 1, Hình học, Bài 11. Tỉ số lượng giác của góc nhọn (1 tiết)
     - Dòng 3: Tuần 2, Đại số, Bài 2 (2 tiết)
     - Dòng 4: Tuần 2, Hình học, Bài 11. Tỉ số lượng giác của góc nhọn (tiếp theo) (2 tiết)
   - Kiểm tra kết quả: Tiết hình học tuần 1 phải là `1/3`; tuần 2 phải là `2/3` và `3/3`.
3. `tests/timetable-render-smoke.js`:
   - Kiểm tra hiển thị TKB với dữ liệu giáo viên, string ID, fallback tiết và parse JSON string.

---

## 4. Tiêu chí nghiệm thu (Acceptance Criteria)

1. **PPCT đa tuần**:
   - Đối với môn có nhiều mạch xen kẽ (Toán 9 gồm Đại số & Hình học): Bài 11 (*Tỉ số lượng giác của góc nhọn*) dạy 1 tiết ở Tuần 1 và 2 tiết ở Tuần 2 hiển thị chính xác:
     - Tuần 1: `1 · 1/3`
     - Tuần 2: `2 · 2/3`, `3 · 3/3`
   - Không bị dòng Đại số xen giữa làm đứt đoạn thành `1/1` và `1/2, 2/2`.
2. **Thời khóa biểu**:
   - Khi bấm chuyển sang tab "2. Thời khoá biểu GV", lưới TKB Buổi sáng và Buổi chiều hiển thị đầy đủ các tiết học của giáo viên được chọn.
   - Khi bấm chọn giáo viên khác trong danh sách, bảng cập nhật đúng dữ liệu TKB của GV đó.
   - Khi bấm "AI nhận diện TKB", bảng TKB tự động render ngay sau khi AI quét xong mà không bị trắng bảng.
3. **Kiểm thử**:
   - Test `tests/baogiang-weekday-segment-smoke.js` và `tests/timetable-render-smoke.js` đều đạt PASS.
