# PLAN: Chuẩn Hóa Tiêu Đề Hoạt Động 4 Thành "HOẠT ĐỘNG 4: VẬN DỤNG"

## Mục tiêu
Đổi toàn bộ các vị trí còn dùng chuỗi cũ `"HOẠT ĐỘNG 4: VẬN DỤNG & HƯỚNG DẪN TỰ HỌC"` và nhãn tab `"D. Vận dụng & Hướng dẫn tự học"` thành `"HOẠT ĐỘNG 4: VẬN DỤNG"` và `"D. Vận dụng"` đồng bộ trên:
1. Prompt AI (`js/khbd-prompts.js`)
2. Nút Tab trên các trang HTML (`soankhbd.html`, `canvas_soanbaigiang.html`)
3. Dữ liệu và logic (`js/khbd-app.js`)
4. Toàn bộ kịch bản test (`tests/`)

---

## I. Chi Tiết Các File Cần Sửa

### 1. `js/khbd-prompts.js`
- **Dòng 889**: Trong prompt template `GENERATE_ACTIVITY_D`:
  - Thay:
    ```markdown
    ## D. HOẠT ĐỘNG 4: VẬN DỤNG & HƯỚNG DẪN TỰ HỌC ({time_budget_D})
    ```
  - Bằng:
    ```markdown
    ## D. HOẠT ĐỘNG 4: VẬN DỤNG ({time_budget_D})
    ```
- **Dòng 1122**: Trong prompt template `GENERATE_ACTIVITIES_AD`:
  - Thay:
    ```markdown
    (toàn bộ ## D. HOẠT ĐỘNG 4: VẬN DỤNG & HƯỚNG DẪN TỰ HỌC ({time_budget_D}))
    ```
  - Bằng:
    ```markdown
    (toàn bộ ## D. HOẠT ĐỘNG 4: VẬN DỤNG ({time_budget_D}))
    ```
- **Dòng 1155 - 1156**: Trong prompt template `GENERATE_ACTIVITIES_AD`:
  - Thay:
    ```markdown
    PHA D — VẬN DỤNG & HƯỚNG DẪN TỰ HỌC:
    - Tiêu đề: `## D. HOẠT ĐỘNG 4: VẬN DỤNG & HƯỚNG DẪN TỰ HỌC ({time_budget_D})`.
    ```
  - Bằng:
    ```markdown
    PHA D — VẬN DỤNG:
    - Tiêu đề: `## D. HOẠT ĐỘNG 4: VẬN DỤNG ({time_budget_D})`.
    ```

### 2. `soankhbd.html`
- **Dòng 710**:
  - Thay:
    ```html
    <button class="act-tab-btn" data-act="D">D. Vận dụng &amp; Hướng dẫn tự học</button>
    ```
  - Bằng:
    ```html
    <button class="act-tab-btn" data-act="D">D. Vận dụng</button>
    ```

### 3. `canvas_soanbaigiang.html`
- **Dòng 831**:
  - Thay:
    ```html
    <button class="act-tab-btn" data-act="D">D. Vận dụng &amp; Hướng dẫn tự học</button>
    ```
  - Bằng:
    ```html
    <button class="act-tab-btn" data-act="D">D. Vận dụng</button>
    ```

### 4. `tests/khbd-tabs-reorganized-smoke.js`
- **Dòng 43**:
  - Sửa regex hoặc chuỗi match HTML nếu cần (thành `data-act="D">D\. Vận dụng</button>`).
- **Dòng 62**:
  - Đổi:
    ```javascript
    assert.strictEqual(ACTIVITY_TITLES.D.short, 'D. Vận dụng & Hướng dẫn tự học');
    ```
    thành:
    ```javascript
    assert.strictEqual(ACTIVITY_TITLES.D.short, 'D. Vận dụng');
    ```
- **Dòng 87, 91**:
  - Đổi fixture `appState.content.activities.D` từ `## D. HOẠT ĐỘNG 4: VẬN DỤNG & HƯỚNG DẪN TỰ HỌC (12 phút)` thành `## D. HOẠT ĐỘNG 4: VẬN DỤNG (12 phút)`.
  - Cập nhật assertion tương ứng.

### 5. `tests/khbd-activities-ad-standard-smoke.js`
- **Dòng 57 & 67**:
  - Thay match `/## D\. HOẠT ĐỘNG 4: VẬN DỤNG & HƯỚNG DẪN TỰ HỌC/` bằng `/## D\. HOẠT ĐỘNG 4: VẬN DỤNG \(12 phút\)/`.
- **Dòng 77 & 89**:
  - Cập nhật fixture và assertion tương ứng `## D. HOẠT ĐỘNG 4: VẬN DỤNG (12 phút)`.

### 6. `tests/khbd-table-columns-smoke.js`
- **Dòng 91**:
  - Đổi `## D. HOẠT ĐỘNG 4: VẬN DỤNG & HƯỚNG DẪN TỰ HỌC (18 phút)` thành `## D. HOẠT ĐỘNG 4: VẬN DỤNG (18 phút)`.

---

## II. Kế Hoạch Kiểm Thử (Verification Plan)
Chạy các bài test sau bằng Node.js và đảm bảo 100% PASS:
```bash
node tests/khbd-tabs-reorganized-smoke.js
node tests/khbd-activities-ad-standard-smoke.js
node tests/khbd-table-columns-smoke.js
node tests/canvas-tabs-permissions-smoke.js
```
Ghi lại kết quả vào `docs/handoff/IMPLEMENT.md`.
