# PLAN: Nâng cấp Sổ Điểm — Trình chiếu Đề (LaTeX + Ảnh), Tìm kiếm & Sắp xếp Học sinh

## Hiện trạng & Vấn đề Phân tích
1. **Thiếu chế độ trình chiếu đề bài chuyên dụng cho lớp học:**
   - Trong `sodiem.html`, tab "3. Đề & câu hỏi" hiện chỉ có một khung `<article id="questionDisplay">` nhỏ nằm bên dưới textarea.
   - Khi giáo viên gọi học sinh lên bảng hoặc kiểm tra miệng, giáo viên cần chiếu câu hỏi / đề bài lên máy chiếu (projector) hoặc tivi màn hình lớn với cỡ chữ to, giao diện rõ ràng, kèm đồng hồ đếm ngược.
   - Chưa có chế độ Fullscreen / Projector Modal.
2. **Khả năng render LaTeX còn hạn chế:**
   - Hiện tại mã nguồn gọi trực tiếp `katex.render(q, $('questionDisplay'), {throwOnError:false})`.
   - KaTeX sẽ lỗi hoặc hiển thị thô nếu chuỗi `q` là đoạn văn bản thông thường có xen kẽ công thức (ví dụ: `Cho phương trình $x^2 - 4 = 0$, tìm x:`). KaTeX yêu cầu tách biệt giữa text thông thường và khối math (`$...$` hoặc `$$...$$`).
3. **Chưa hỗ trợ dán ảnh đề bài (Paste Image Ctrl+V):**
   - Giáo viên thường chụp ảnh đề bài từ sách giáo khoa, đề kiểm tra Word, tài liệu PDF hoặc trang web bằng công cụ chụp màn hình (Snipping Tool, Zalo, Paint).
   - Hiện tại chưa bắt sự kiện `paste` trên clipboard để nhận ảnh trực tiếp, cũng như chưa có nút tải ảnh đề bài, buộc giáo viên phải gõ lại văn bản rất mất thời gian.
4. **Thiếu công cụ tìm kiếm nhanh học sinh:**
   - Lớp học thường có từ 35–50 học sinh. Khi cần vào điểm cho một học sinh bất kỳ, giáo viên phải cuộn trang và tìm mắt thường rất chậm.
   - Chưa có ô tìm kiếm lọc nhanh theo tên hoặc mã/SBD, đặc biệt là tìm kiếm không phân biệt dấu tiếng Việt ("an" tìm được "An", "hoang" tìm được "Hoàng").
5. **Chưa có tính năng sắp xếp học sinh theo thứ tự chuẩn tiếng Việt:**
   - Danh sách học sinh nạp từ hệ thống hoặc Excel đôi khi bị xáo trộn thứ tự.
   - Giáo viên cần sắp xếp học sinh theo thứ tự Tên (A → Z) chuẩn bảng chữ cái tiếng Việt (tách tên chính ở cuối ra so sánh trước, trùng tên thì xét họ đệm), cũng như sắp xếp theo Mã/SBD hoặc Điểm trung bình (ĐTBtx).

---

## Mục tiêu & Giải pháp Triệt để

### 1. Trình chiếu Đề bài Chuyên nghiệp (Projector Presentation View)
- Bổ sung nút **"Trình chiếu"** (`<button onclick="openPresentation()"><i class="fa fa-tv mr-2"></i> Trình chiếu</button>`) với thiết kế nổi bật, màu sắc trang nhã.
- Xây dựng màn hình trình chiếu toàn màn hình (Modal/Fullscreen `presentationModal`):
  + Nền tối chuyên dụng cho máy chiếu (`bg-slate-950` / `bg-slate-900`) hoặc tùy chọn sáng, chữ màu trắng/vàng tương phản cao, khử chói mắt.
  + Điều khiển linh hoạt:
    * Chuyển câu: Nút `Trước` (`<`), `Tiếp` (`>`), `Bốc ngẫu nhiên` (`fa-shuffle`), hiển thị chỉ số `Câu X / Y`.
    * Phóng to / Thu nhỏ cỡ chữ: Nút `A-`, `A+` để phù hợp với màn hình chiếu kích thước khác nhau.
    * Tích hợp đồng hồ đếm ngược (Countdown Timer) trực tiếp trên thanh điều khiển trình chiếu, có thể tạm dừng/tiếp tục và phát âm thanh chuông báo khi hết giờ.
    * Nút **"Gọi học sinh"** ngay trên giao diện trình chiếu: liên kết nhanh với vòng quay hoặc bốc ngẫu nhiên học sinh trong lớp để trả lời.
    * Hỗ trợ phím tắt bàn phím: Mũi tên Trái/Phải để đổi câu, `Space` để tạm dừng/chạy đồng hồ, `Esc` để đóng trình chiếu.

### 2. Render Công thức LaTeX Chuẩn xác
- Xây dựng hàm parser `renderMathText(content)`:
  + Tự động nhận diện và chuyển đổi:
    * Công thức nội dòng (inline math): `$ ... $` hoặc `\( ... \)`.
    * Công thức khối (display math): `$$ ... $$` hoặc `\[ ... \]`.
  + Sử dụng `katex.renderToString(mathExp, { displayMode: boolean, throwOnError: false })` để thay thế mượt mà các khối công thức, bảo toàn 100% đoạn văn bản tiếng Việt xung quanh.
  + Hỗ trợ xuống dòng tự nhiên và giữ khoảng cách rõ ràng.

### 3. Dán Ảnh Đề bài Trực tiếp (Ctrl+V) & Tải Tệp Ảnh
- Bắt sự kiện `paste` trên tab Đề & câu hỏi và trong textarea:
  + Kiểm tra `e.clipboardData.items`. Nếu có tệp ảnh (`image/*`):
    * Đọc dữ liệu ảnh bằng `FileReader` dưới dạng Base64 Data URL (`data:image/png;base64,...`).
    * Tự động thêm vào danh sách đề bài hoặc đặt làm câu hỏi hiện tại.
- Thêm nút tải tệp: `<label class="..."><i class="fa fa-image mr-1"></i> Tải ảnh đề<input type="file" accept="image/*" onchange="handleImageUpload(event)" hidden></label>`.
- Hiển thị ảnh:
  + Khi câu hỏi là ảnh (chứa `data:image/` hoặc URL ảnh), tự động render thành thẻ `<img>` sắc nét, căn giữa hoàn hảo, tự động co giãn (`max-h-[68vh] object-contain`), có khung viền bo tròn thẩm mỹ.
  + Click vào ảnh để phóng to xem chi tiết nếu ảnh nhỏ.

### 4. Tìm kiếm Nhanh Học sinh (Instant Search)
- Thêm thanh tìm kiếm ngay phía trên bảng điểm:
  + Ô nhập: `<input id="searchStudent" oninput="renderGrades()" placeholder="🔍 Tìm nhanh tên hoặc mã/SBD..." class="border rounded-lg pl-9 pr-8 py-2 text-sm w-full sm:w-72">`.
  + Nút xóa tìm kiếm (x) khi có chữ.
  + Badge hiển thị số lượng: `Tìm thấy X/Y học sinh`.
- Hàm lọc thông minh không dấu tiếng Việt `stripVietnamese(str)`:
  + Loại bỏ dấu thanh, chuyển `đ` thành `d`, chữ thường.
  + Giúp giáo viên gõ không dấu ("hoang", "thien", "an") vẫn tìm ra chính xác ("Hoàng", "Thiện", "An").
- **Tính toàn vẹn dữ liệu:** Khi đang tìm kiếm và bảng điểm chỉ hiển thị các dòng khớp, giáo viên vẫn có thể nhập điểm, sửa tên/SBD, gọi học sinh. Mọi thay đổi đều được ghi chính xác vào mảng gốc `students` theo đúng ID/index thực của học sinh và đồng bộ vào `persist()`.

### 5. Sắp xếp Tên Học sinh Chuẩn Tiếng Việt
- Thêm bộ điều khiển sắp xếp:
  + Dropdown hoặc bấm trực tiếp vào tiêu đề cột "Họ và tên":
    * **Tên A → Z (chuẩn từ điển tiếng Việt):** Tách từ cuối cùng làm Tên chính, so sánh bằng `localeCompare('vi')`. Nếu trùng tên chính, so sánh tiếp Họ và Tên đệm.
    * **Tên Z → A:** Đảo ngược thứ tự từ điển.
    * **Mã/SBD:** Sắp xếp theo số báo danh/mã học sinh tăng dần/giảm dần.
    * **Điểm TB (ĐTBtx):** Sắp xếp học sinh theo điểm trung bình từ cao xuống thấp hoặc từ thấp lên cao.
- Sau khi sắp xếp:
  + Tự động đánh lại số thứ tự (STT: 1, 2, 3...).
  + Tự động lưu thứ tự mới vào `persist()` (localStorage và backend) để không bị mất vị trí.

---

## File tác động
- `sodiem.html`:
  + Thêm thanh tìm kiếm và bộ sắp xếp tại phần bảng điểm (`#grades`).
  + Bổ sung nút Trình chiếu, nút Tải ảnh và bộ lắng nghe sự kiện `paste` tại phần câu hỏi (`#questions`).
  + Thêm cấu trúc Dialog/Modal Trình chiếu toàn màn hình `#presentationModal`.
  + Viết hàm `renderMathText(content)` để render chuẩn KaTeX inline/display math kết hợp văn bản.
  + Viết logic trình chiếu: chuyển câu, đếm ngược, phóng to/thu nhỏ font, bốc câu hỏi, gọi học sinh.
  + Viết hàm `sortStudents(type)` và `stripVietnamese(str)`.

---

## Chi tiết Mã nguồn & Giải pháp Kỹ thuật

### 1. Hàm Render Math & Ảnh Đề bài
```javascript
function renderQuestionContent(content) {
    if (!content) return '<p class="text-slate-400">Chưa có nội dung đề bài.</p>';
    // Nếu là ảnh (data:image/ hoặc url ảnh)
    if (content.startsWith('data:image/') || content.match(/\.(png|jpg|jpeg|gif|webp)(\?.*)?$/i)) {
        return `<div class="flex flex-col items-center justify-center">
            <img src="${content}" class="max-h-[65vh] max-w-full rounded-xl shadow-lg border border-slate-700 object-contain cursor-zoom-in" onclick="zoomImage(this.src)" alt="Đề bài">
            <p class="text-xs text-slate-400 mt-2"><i class="fa fa-magnifying-glass-plus mr-1"></i>Bấm vào ảnh để xem kích thước lớn</p>
        </div>`;
    }
    // Render văn bản trộn công thức LaTeX
    return renderMathText(content);
}

function renderMathText(text) {
    if (!text) return '';
    let escaped = escapeHtml(text);
    // Thay thế block math $$...$$ hoặc \[...\]
    escaped = escaped.replace(/\$\$([\s\S]+?)\$\$|\\\[([\s\S]+?)\\\]/g, (match, p1, p2) => {
        const formula = p1 || p2;
        try {
            return `<div class="my-3 text-center">${katex.renderToString(unescapeHtml(formula), { displayMode: true, throwOnError: false })}</div>`;
        } catch(e) { return match; }
    });
    // Thay thế inline math $...$ hoặc \(...\)
    escaped = escaped.replace(/\$([^\$\n]+?)\$|\\\(([\s\S]+?)\\\)/g, (match, p1, p2) => {
        const formula = p1 || p2;
        try {
            return katex.renderToString(unescapeHtml(formula), { displayMode: false, throwOnError: false });
        } catch(e) { return match; }
    });
    // Giữ định dạng ngắt dòng
    return escaped.replace(/\n/g, '<br>');
}
```

### 2. Xử lý Dán Ảnh Clipboard & Upload
```javascript
// Lắng nghe sự kiện paste trên toàn bộ tài liệu hoặc textarea
$('questionInput').addEventListener('paste', handlePasteEvent);

function handlePasteEvent(e) {
    const items = (e.clipboardData || window.clipboardData)?.items;
    if (!items) return;
    for (const item of items) {
        if (item.type.indexOf('image') !== -1) {
            e.preventDefault();
            const blob = item.getAsFile();
            const reader = new FileReader();
            reader.onload = ev => {
                const base64 = ev.target.result;
                addQuestionItem(base64);
                showCurrentQuestion(base64);
            };
            reader.readAsDataURL(blob);
            break;
        }
    }
}
```

### 3. Tìm kiếm & Sắp xếp Học sinh
```javascript
function stripVietnamese(str) {
    return (str || '')
        .normalize('NFD')
        .replace(/[\u0300-\u036f]/g, '')
        .replace(/đ/g, 'd').replace(/Đ/g, 'D')
        .toLowerCase()
        .trim();
}

function getSortKey(fullName) {
    const parts = (fullName || '').trim().split(/\s+/);
    const firstName = parts.pop() || '';
    const lastName = parts.join(' ');
    return { firstName, lastName };
}

function sortStudents(type) {
    if (type === 'name_asc') {
        students.sort((a, b) => {
            const ka = getSortKey(a.name), kb = getSortKey(b.name);
            const cmp = ka.firstName.localeCompare(kb.firstName, 'vi');
            return cmp !== 0 ? cmp : ka.lastName.localeCompare(kb.lastName, 'vi');
        });
    } else if (type === 'name_desc') {
        students.sort((a, b) => {
            const ka = getSortKey(a.name), kb = getSortKey(b.name);
            const cmp = kb.firstName.localeCompare(ka.firstName, 'vi');
            return cmp !== 0 ? cmp : kb.lastName.localeCompare(ka.lastName, 'vi');
        });
    } else if (type === 'sbd_asc') {
        students.sort((a, b) => String(a.sbd || '').localeCompare(String(b.sbd || ''), 'vi', { numeric: true }));
    } else if (type === 'avg_desc') {
        students.sort((a, b) => (Number(average(b)) || 0) - (Number(average(a)) || 0));
    } else if (type === 'avg_asc') {
        students.sort((a, b) => (Number(average(a)) || 0) - (Number(average(b)) || 0));
    }
    persist();
    renderAll();
}
```

### 4. Giao diện & Điều khiển Trình chiếu
- Dialog `#presentationModal`:
  - Header: Tiêu đề câu hỏi, cỡ chữ `A-`/`A+`, đồng hồ đếm ngược có nút Start/Stop, nút gọi ngẫu nhiên học sinh, nút Toàn màn hình, nút Đóng.
  - Vùng nội dung: Box hiển thị câu hỏi/ảnh cực lớn, căn giữa màn hình, font chữ tự động điều chỉnh linh hoạt.
  - Footer: Nút điều hướng `< Câu trước`, `Câu tiếp >`, `Bốc ngẫu nhiên`.

---

## Kế hoạch Kiểm thử (Verification Plan)
1. **Kiểm thử tự động Smoke Test hiện có:**
   - Chạy `node tests/sodiem-smoke.js` -> Phải PASS 100%.
   - Chạy `node tests/teacher-permissions-smoke.js` -> Phải PASS 100%.
   - Chạy `node tests/security-f12-smoke.js` -> Phải PASS 100%.
2. **Kiểm thử chức năng Trình chiếu:**
   - Bấm nút "Trình chiếu" -> Màn hình trình chiếu mở ra toàn màn hình, hiển thị đẹp mắt.
   - Nhập câu hỏi có công thức `$x^2 + \sqrt{y} = 10$` -> Render KaTeX sắc nét.
   - Dán ảnh từ clipboard (Ctrl+V) -> Hiển thị ảnh đề bài to rõ, căn giữa.
   - Chạy đồng hồ đếm ngược trên màn hình trình chiếu -> Đếm lùi chuẩn xác, hết giờ có âm thanh báo.
   - Bấm nút gọi học sinh trong trình chiếu -> Gọi được học sinh để trả lời câu hỏi.
3. **Kiểm thử chức năng Tìm kiếm & Sắp xếp:**
   - Nhập từ khóa không dấu "nguyen" vào ô tìm kiếm -> Hiển thị chính xác các học sinh có họ "Nguyễn".
   - Bấm sắp xếp Tên A → Z -> Các học sinh tên "An", "Bình", "Cường" được xếp đúng thứ tự từ điển tiếng Việt.
   - Nhập điểm cho học sinh khi đang lọc tìm kiếm -> Điểm được lưu đúng cho học sinh đó trong toàn bộ sổ điểm.

---

## Tiêu chí Nghiệm thu
- Trình chiếu đề bài hoạt động mượt mà trên máy chiếu / màn hình tương tác lớp học.
- Hỗ trợ công thức LaTeX chuẩn và nhận diện dán ảnh Ctrl+V tức thì.
- Tìm kiếm học sinh nhanh chóng không phân biệt dấu tiếng Việt.
- Sắp xếp học sinh chuẩn theo bảng chữ cái tiếng Việt.
- Toàn bộ bài kiểm tra smoke test đạt 100% PASS.
