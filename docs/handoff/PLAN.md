# PLAN: Tích Hợp Chế Độ Thoát Zalo/In-App Browser Vào Hệ Thống Link Rút Gọn & QR Code

## Hiện trạng
1. **Cơ chế chuyển hướng hiện tại (`s.php`):**
   - Khi truy cập `/s/{code}`, máy chủ PHP trả về mã chuyển hướng HTTP 302 trực tiếp (`header('Location: ' . $targetUrl, true, 302)`).
   - Khi quét mã QR hoặc bấm link từ Zalo, In-App Browser (WebView nội bộ) của Zalo sẽ tự động bám theo mã 302 và tải trang đích ngay bên trong WebView.
2. **Hậu quả thực tế:**
   - Các dịch vụ như Google Login, Gemini AI, WebSockets, WebRTC, hoặc Canvas phức tạp bị Zalo chặn hoặc thiếu API, dẫn đến màn hình trắng, lỗi kết nối hoặc không đăng nhập được tài khoản Google.
   - Người dùng thường không biết cách tự bấm dấu `...` để mở trình duyệt ngoài.
3. **Trang quản lý link (`rutgon.html`):**
   - Đã có tính năng tạo link ngắn và mã QR, nhưng chưa có tùy chọn bật/tắt cơ chế Smart Bridge (thoát In-App Browser) và chưa hiển thị chỉ dẫn chuyên biệt cho quét Zalo.

---

## Phạm vi thực hiện
1. **Nâng cấp Cơ chế Chuyển hướng Trung gian (`s.php` - Smart Bridge Escaper):**
   - Phát hiện User-Agent truy cập từ In-App Browser (Zalo, Messenger, Facebook, Instagram, TikTok...).
   - Nếu không phải In-App Browser (Chrome, Safari, Edge, Firefox, Desktop): Giữ nguyên HTTP 302 tức thì về `$targetUrl`.
   - Nếu phát hiện In-App Browser và link có bật `escape_inapp`:
     - **Đối với Android:** Xuất trang cầu nối HTML/JS nhẹ tự động kích hoạt **Android Intent** (`intent://...#Intent;scheme=https;package=com.android.chrome;end`) để tự động "văng" ra Google Chrome hoặc trình duyệt mặc định mà không cần người dùng thao tác.
     - **Đối với iOS (iPhone/iPad):** Vì Apple chặn tự động gọi `safari://`, hiển thị giao diện đệm thông minh (Interstitial Screen):
       + Mũi tên động trực quan hướng thẳng lên góc trên bên phải (vị trí nút `...` của Zalo).
       + Hướng dẫn 2 bước rõ ràng: Bấm `...` $\rightarrow$ Chọn *Mở bằng Safari* / *Trình duyệt mặc định*.
       + Nút 1 chạm "Sao chép liên kết" (để dán vào trình duyệt).
       + Nút "Mở bằng Google Chrome" (`googlechromes://...`).
       + Nút "Vẫn tiếp tục trên Zalo" (fallback).
2. **Nâng cấp CSDL và API (`api/short_links.php`):**
   - Bổ sung cột `escape_inapp TINYINT(1) NOT NULL DEFAULT 1` vào bảng `short_links` (tự động cập nhật qua `short_link_schema()`).
   - Cập nhật các action `list`, `create`, `update` để lưu trữ và trả về thuộc tính `escape_inapp` (mặc định luôn bật = 1 để bảo vệ tối đa người dùng).
3. **Nâng cấp Giao diện Quản lý Link & QR (`rutgon.html`):**
   - Bổ sung tùy chọn checkbox: `Tự động thoát Zalo / In-App Browser (Mở bằng Chrome/Safari)` trong form tạo/sửa link (mặc định tích chọn).
   - Hiển thị huy hiệu `Chống chặn Zalo` trên từng thẻ link trong danh sách.
   - Cải tiến modal QR Code: Thêm thông báo hướng dẫn "Đã bật Smart Bridge chống lỗi Zalo" và nút "Xem thử màn hình Zalo" để giáo viên kiểm tra trước.

---

## Ngoài phạm vi
- Không can thiệp vào các trang nội dung học tập khác (`thitructuyen.html`, `smartquiz.html`, `canvas_soanbaigiang.html`...).
- Không ép buộc cài đặt ứng dụng thứ ba không rõ nguồn gốc lên máy người dùng.

---

## Danh sách File dự kiến tác động
- `s.php` (Bộ xử lý chuyển hướng trung gian, nhận diện User-Agent, Android Intent & màn hình đệm iOS).
- `api/short_links.php` (Schema CSDL, CRUD tham số `escape_inapp`).
- `rutgon.html` (Form cấu hình, hiển thị danh sách, thông tin mã QR).

---

## Chi tiết kỹ thuật cần cài đặt

### 1. `api/short_links.php`
- Trong `short_link_schema()`:
  - Bổ sung lệnh kiểm tra hoặc `ALTER TABLE short_links ADD COLUMN IF NOT EXISTS escape_inapp TINYINT(1) NOT NULL DEFAULT 1;` (hoặc check qua `SHOW COLUMNS`).
- Trong hàm `short_link_public_item()`:
  - Bổ sung trường `'escape_inapp' => (bool)($row['escape_inapp'] ?? 1)`.
- Trong `action === 'create'`:
  - Lấy `$escapeInApp = isset($body['escape_inapp']) ? ((bool)$body['escape_inapp'] ? 1 : 0) : 1;`
  - Thêm trường `escape_inapp` vào câu lệnh `INSERT`.
- Trong `action === 'update'`:
  - Cho phép cập nhật trường `escape_inapp`.

### 2. `s.php`
- Cập nhật hàm `short_redirect_schema()` để đảm bảo cột `escape_inapp` tồn tại.
- Lấy giá trị `escape_inapp` từ `$row`.
- Logic kiểm tra In-App Browser:
  ```php
  $ua = (string)($_SERVER['HTTP_USER_AGENT'] ?? '');
  $isZalo = (bool)preg_match('/(Zalo|ZaloTheme)/i', $ua);
  $isInApp = (bool)preg_match('/(Zalo|FB_IAB|FBAN|FBAV|Instagram|MicroMessenger|Line|Snapchat|Bytedance|TikTok)/i', $ua);
  $isAndroid = (bool)preg_match('/Android/i', $ua);
  $isIOS = (bool)preg_match('/(iPhone|iPad|iPod)/i', $ua);
  $escapeInApp = (bool)($row['escape_inapp'] ?? 1);
  ```
- Nếu `$isInApp && $escapeInApp`:
  - Không gửi `header('Location: ...', true, 302)`.
  - Kết xuất giao diện HTML5 chuẩn UX cao:
    - Android: Chạy script kích hoạt `intent://` URL tự động mở Chrome; fallback sau 1.2s mở generic browser intent.
    - iOS: Hiển thị giao diện chỉ dẫn sinh động:
      + Đồ họa mũi tên nhấp nháy chỉ góc trên bên phải (vị trí `...` của Zalo).
      + Bước 1: Chạm vào dấu **`...`** ở góc trên bên phải.
      + Bước 2: Chọn **"Mở bằng trình duyệt"** (Safari/Chrome).
      + Nút 1 chạm "Sao chép link" (`navigator.clipboard.writeText`).
      + Nút "Thử mở bằng Chrome" (`googlechromes://...`).
      + Link kín: "Tiếp tục xem trong Zalo".

### 3. `rutgon.html`
- Thêm trường checkbox trong `creatorForm`:
  ```html
  <label class="sm:col-span-2">
      <span class="inline-flex items-center gap-2 text-sm font-bold text-slate-700">
          <input id="escapeInApp" type="checkbox" class="h-4 w-4 rounded border-slate-300 text-indigo-600" checked>
          Tự động thoát Zalo / In-App Browser (khuyên dùng khi gửi đề thi, Gemini, Google Form)
      </span>
  </label>
  ```
- Cập nhật `openCreator()`, `openEditor()`, `saveLink()` để đồng bộ trường `escapeInApp`.
- Trong `renderLinks()`: Thêm nhãn `<span class="chip bg-sky-100 text-sky-700"><i class="fas fa-shield-alt mr-1"></i>Thoát Zalo</span>` khi `item.escape_inapp` là true.
- Trong `openQr()`: Thêm ghi chú dưới mã QR để giáo viên an tâm khi gửi cho học sinh/phụ huynh qua Zalo.

---

## Tiêu chí nghiệm thu & Kịch bản kiểm thử
1. **Kiểm thử trên trình duyệt chuẩn (Chrome, Edge Desktop/Mobile):**
   - Truy cập `/s/{code}`: Tự động chuyển hướng 302 trực tiếp đến trang đích ngay lập tức mà không hiện trang đệm.
2. **Kiểm thử giả lập Zalo Android:**
   - Dùng User-Agent Zalo Android: Trang web kích hoạt Intent mở Chrome bên ngoài.
3. **Kiểm thử giả lập Zalo iOS:**
   - Dùng User-Agent Zalo iOS: Trang web hiển thị giao diện hướng dẫn với mũi tên chỉ vào nút `...`, các nút sao chép link và mở Chrome hoạt động mượt mà.
4. **Kiểm thử cấu hình trong `rutgon.html`:**
   - Tạo mới hoặc chỉnh sửa link, bật/tắt tùy chọn "Thoát Zalo", kiểm tra lưu thành công vào CSDL.
   - Tạo mã QR, tải ảnh mã QR bình thường.
