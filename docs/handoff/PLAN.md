# PLAN: Sửa lỗi trùng lặp mã NLS và AI trong `ppctRowCodes` tại `js/khbd-app.js`

## Hiện trạng & Nguyên nhân

Khi người dùng nhập hoặc chọn một dòng Phân phối chương trình (PPCT), hệ thống đọc mã từ hai nguồn dữ liệu tương thích:
- NLS: `row.nls.codes` và `row.digital_competency`
- AI: `row.ai.codes` và `row.ai_competency`

Trong hàm `ppctRowCodes(row, kind)` tại dòng 6146 của `js/khbd-app.js`:
```javascript
function ppctRowCodes(row, kind) {
  if (kind === "nls") {
    const fromField = Array.isArray(row?.digital_competency) ? row.digital_competency.map(item => item?.code || item).filter(Boolean) : [];
    return (row?.nls?.codes || []).concat(fromField).map(String).filter(Boolean);
  }
  const fromField = Array.isArray(row?.ai_competency) ? row.ai_competency.map(item => item?.code || item).filter(Boolean) : [];
  return (row?.ai?.codes || []).concat(fromField).map(String).filter(Boolean);
}
```
Do hai trường trên cùng chứa dữ liệu mã năng lực (ví dụ cả hai cùng chứa `1.2.TC1a` hoặc `6.A1.1`), việc nối mảng (`concat`) mà không lọc trùng làm mã bị nhân đôi: `["1.2.TC1a", "1.2.TC1a"]`. Khi hiển thị giao diện và khi tự động tick chọn chuẩn tích hợp, mỗi mã bị lặp lại hai lần gây rối mắt và không chính xác.

---

## Phạm vi Thực hiện

1. **Cho phép Coder sửa hàm `ppctRowCodes` trong `js/khbd-app.js`**:
   - Dùng `Array.from(new Set(...))` để loại bỏ hoàn toàn các mã trùng lặp (khử trùng case-insensitive hoặc chuẩn hóa chuỗi `trim()`).
   - Đảm bảo trả về mảng các mã duy nhất.
2. **Kiểm tra và áp dụng tương tự nếu có hàm liên quan**:
   - Rà soát các vị trí nạp và hiển thị mã PPCT để đảm bảo danh sách mã luôn là duy nhất (unique).
3. **Giới hạn phạm vi**:
   - Chỉ sửa đúng hàm `ppctRowCodes` trong `js/khbd-app.js`.
   - Tuyệt đối không thay đổi bất kỳ logic sư phạm hay quy trình sinh KHBD nào khác.
4. **Kiểm thử tự động**:
   - Tạo bài test `tests/ppct-dedupe-smoke.js` kiểm tra `ppctRowCodes` với dữ liệu mẫu có trùng mã ở cả 2 trường, khẳng định kết quả trả về chỉ chứa 1 mã duy nhất.
   - Chạy lại toàn bộ test suite để đảm bảo PASS 100%.

---

## File dự kiến tác động

1. `js/khbd-app.js` (dòng 6146, hàm `ppctRowCodes`)
2. `tests/ppct-dedupe-smoke.js` (MỚI)

---

## Các bước thực hiện chi tiết cho Coder

### Bước 1: Cập nhật `ppctRowCodes` trong `js/khbd-app.js`
Sửa hàm `ppctRowCodes` tại dòng 6146 thành:
```javascript
function ppctRowCodes(row, kind) {
  if (kind === "nls") {
    const fromField = Array.isArray(row?.digital_competency) ? row.digital_competency.map(item => item?.code || item).filter(Boolean) : [];
    const raw = (row?.nls?.codes || []).concat(fromField).map(v => String(v || "").trim()).filter(Boolean);
    return Array.from(new Set(raw));
  }
  const fromField = Array.isArray(row?.ai_competency) ? row.ai_competency.map(item => item?.code || item).filter(Boolean) : [];
  const raw = (row?.ai?.codes || []).concat(fromField).map(v => String(v || "").trim()).filter(Boolean);
  return Array.from(new Set(raw));
}
```

### Bước 2: Tạo kiểm thử tự động `tests/ppct-dedupe-smoke.js`
- Giả lập `row` có `row.digital_competency = ["1.2.TC1a"]`, `row.nls = { codes: ["1.2.TC1a"] }` và `row.ai_competency = ["6.A1.1"]`, `row.ai = { codes: ["6.A1.1"] }`.
- Gọi `ppctRowCodes(row, "nls")` và `ppctRowCodes(row, "ai")`.
- Assert mảng trả về có độ dài 1 và đúng mã tương ứng.

---

## Tiêu chí nghiệm thu

1. Khi chọn bài PPCT có chứa mã năng lực số hoặc AI ở cả 2 trường, danh sách mã hiển thị không bị lặp lại hai lần.
2. Việc tự động tick các checkbox chuẩn tích hợp NLS và AI hoạt động chính xác, không thừa thãi.
3. Toàn bộ test hiện hữu và test mới `tests/ppct-dedupe-smoke.js` đều PASS 100%.
