# PLAN

## Hiện trạng & Phân tích Lỗi thực tế
Từ kết quả chạy thực tế và ảnh chụp màn hình giáo viên phản hồi:
1. **Lỗi vị trí cấy tại Mục I (Mục tiêu):**
   - Hệ thống tìm thấy đoạn `b) Năng lực riêng:` và chèn ngay sau tiêu đề này, làm đứt đoạn nội dung: các gạch đầu dòng của mục b) bị đẩy xuống dưới mục `c) Năng lực số`!
   - Hệ thống gộp 2 mã thành chuỗi ngoặc vuông xấu xí `[[1.2.TC1a], [3.1.TC1a]]` và làm mất nội dung mô tả cụ thể mà giáo viên đã cung cấp trong PPCT.
2. **Lỗi vị trí cấy và phân bổ mã tại Mục III (Tiến trình dạy học):**
   - Hệ thống "lười" gom cả 2 mã khác nhau vào cùng một chỗ và chọn nhầm vào `A. HOẠT ĐỘNG KHỞI ĐỘNG (MỞ ĐẦU)`.
   - Vị trí cấy bị đặt sai hoàn toàn: cấy chen ngang giữa tiêu đề hoạt động và `a) Mục tiêu`, trong khi theo chuẩn Công văn 5512, nội dung tích hợp phải nằm ở phần **`d) Tổ chức thực hiện`** (hoặc trong ô bảng của hoạt động).
3. **Màn hình xem trước không tự cập nhật:**
   - Sau khi cấy DOCX thành công, khung xem trước không hiển thị nội dung file DOCX vừa cấy nên người dùng không thấy sự thay đổi.

## Phạm vi & Giải pháp triệt để
1. **Sửa chuẩn vị trí cấy tại Mục I (Mục tiêu):**
   - Vị trí chèn: Tìm điểm kết thúc của Năng lực đặc thù (ngay **TRƯỚC** tiêu đề `3. Phẩm chất` hoặc `c) Phẩm chất` hoặc `II. THIẾT BỊ DẠY HỌC`).
   - Phân tách độc lập từng mã: Mỗi mã là một gạch đầu dòng riêng biệt, bảo toàn 100% mô tả chi tiết của giáo viên từ PPCT:
     ```
     c) Năng lực số:
     - [1.2.TC1a] Đánh giá dữ liệu, thông tin và nội dung số: Đánh giá tính hợp lý của dữ liệu thực tế về quãng đường và thời gian trong bài Đại lượng tỉ lệ thuận.
     - [3.1.TC1a] Phát triển nội dung số: Sử dụng công cụ số để ghi chép, hệ thống hóa và trình bày kết quả học tập Đại lượng tỉ lệ thuận.
     ```
   - Tuyệt đối không lồng ngoặc vuông `[[...]]`.
2. **Phân bổ mã đúng hoạt động và cấy chuẩn theo 4 bước của phần `d) Tổ chức thực hiện` tại Mục III:**
   - **Phân bổ mã thông minh:**
     + Tuyệt đối không gom các mã khác nhau vào Hoạt động Khởi động.
     + Mã phân tích/đánh giá dữ liệu (như `1.2.TC1a`) -> Phân bổ vào **Hoạt động 2: Hình thành kiến thức** (khám phá kiến thức mới).
     + Mã dùng công cụ số ghi chép/trình bày/sản phẩm (như `3.1.TC1a`) -> Phân bổ vào **Hoạt động 3: Luyện tập** hoặc **Hoạt động 4: Vận dụng**.
   - **Cấu trúc tích hợp chuẩn 4 bước sư phạm theo CV 5512 (chấm dứt viết tràn lan):**
     + Tuyệt đối không viết một khối văn bản lý thuyết dài dòng, chung chung ("Nhiệm vụ...", "Sản phẩm...", "Kiểm chứng...", "Đánh giá...").
     + Nội dung tích hợp phải được đưa gọn gàng vào **4 bước hành động cụ thể** của phần `d) Tổ chức thực hiện`:
       * *Bước 1 (Chuyển giao nhiệm vụ):* GV giao nhiệm vụ học tập gắn với công cụ số / kiểm chứng AI.
       * *Bước 2 (Thực hiện nhiệm vụ):* HS thao tác với công cụ số, xử lý dữ liệu hoặc đối chiếu AI với SGK.
       * *Bước 3 (Báo cáo, thảo luận):* HS nộp sản phẩm số / báo cáo kết quả.
       * *Bước 4 (Kết luận, nhận định):* GV chuẩn hóa kiến thức và nhận xét minh chứng năng lực.
     + Nếu hoạt động dạng bảng: chèn dòng/ô tương ứng trong bảng của Hoạt động 2 hoặc Hoạt động 3.
     + Tuyệt đối không chèn chen ngang trước `a) Mục tiêu`.
3. **Tự động cập nhật màn hình xem trước A4:**
   - Ngay sau khi cấy vào DOCX gốc thành công (`injectedDocxBlob`), dùng `mammoth.convertToHtml` đọc trực tiếp từ Blob này và cập nhật lại `preview.innerHTML`.
   - Tự động cuộn mượt (scroll) đến vị trí tích hợp để giáo viên nhìn thấy ngay thành quả.

## File tác động
- `giaoantichhop.html`:
  + Sửa `buildDeltaPrompt`:
    * Chỉ đạo AI phân tách từng mã riêng biệt, gán đúng vào Hoạt động 2 và Hoạt động 3.
    * Định dạng phần cấy ở Mục III theo đúng 4 bước sư phạm của CV 5512, ngắn gọn, súc tích, thực chiến, không viết lý thuyết tràn lan.
    * Bảo toàn nguyên văn mô tả từ PPCT cho Mục I.
  + Sửa `injectDocxOxml`:
    * Mục I: Chèn trước `Phẩm chất` / `Thiết bị dạy học`, không ngắt đôi mục b).
    * Mục III: Tìm đúng hoạt động (HĐ 2, HĐ 3), tìm tiếp đề mục `d) Tổ chức thực hiện` bên trong hoạt động đó để chèn chuẩn 4 bước.
  + Sửa `integrateAi.onclick`: Gọi `mammoth.convertToHtml` từ `injectedDocxBlob` để render ngay lên màn hình xem trước.

## Các bước thực hiện
### Bước 1: Chuẩn hóa Prompt phân bổ mã và cấu trúc JSON 4 bước
- Cập nhật prompt yêu cầu AI:
  + Mảng `mucTieuNls`: `[{ "ma": "1.2.TC1a", "ten": "Đánh giá dữ liệu...", "moTa": "Đánh giá tính hợp lý..." }]`.
  + Mảng `hoatDongMuc3`: danh sách các hoạt động tương ứng với từng mã, cấu trúc đúng 4 bước CV 5512:
    ```json
    [
      {
        "ma": "1.2.TC1a",
        "tenHoatDong": "Hoạt động 2: Hình thành kiến thức",
        "buoc1_chuyenGiao": "GV yêu cầu HS sử dụng dữ liệu thực tế về thời gian và quãng đường...",
        "buoc2_thucHien": "HS phân tích tính hợp lý của dữ liệu, thảo luận tìm mối quan hệ tỉ lệ thuận...",
        "buoc3_baoCao": "Đại diện nhóm trình bày bảng số liệu và công thức liên hệ...",
        "buoc4_ketLuan": "GV chuẩn hóa kiến thức, đánh giá năng lực đánh giá dữ liệu số của HS."
      },
      {
        "ma": "3.1.TC1a",
        "tenHoatDong": "Hoạt động 3: Luyện tập",
        "buoc1_chuyenGiao": "GV giao bài tập luyện tập, yêu cầu HS dùng công cụ số ghi chép/trình bày...",
        "buoc2_thucHien": "HS làm bài và hệ thống hóa bài giải trên công cụ số...",
        "buoc3_baoCao": "HS chia sẻ bài giải số hóa lên màn chiếu hoặc nộp tệp...",
        "buoc4_ketLuan": "GV nhận xét và xác nhận sản phẩm học tập số."
      }
    ]
    ```

### Bước 2: Nâng cấp thuật toán định vị Anchor trong XML DOM
- **Vị trí Mục I:**
  + Tìm đoạn chứa `phẩm chất` hoặc `thiết bị dạy học` (hoặc `II.`): Chèn ngay trước đoạn này.
  + Nếu không thấy, mới chèn sau đoạn cuối cùng của Mục I.
  + Render từng mã thành dòng riêng: `- [Mã] Tên chuẩn: Mô tả cụ thể của GV`.
- **Vị trí Mục III:**
  + Tìm đoạn tiêu đề hoạt động khớp với `tenHoatDong` (ưu tiên HĐ 2, HĐ 3, không chọn Khởi động).
  + Từ vị trí hoạt động đó, quét tiếp các đoạn tiếp theo để tìm đoạn `d) tổ chức thực hiện` hoặc `tổ chức thực hiện` hoặc `thực hiện nhiệm vụ`.
  + Chèn nội dung tích hợp vào ngay sau đoạn `Tổ chức thực hiện` đó.

### Bước 3: Tự động cập nhật Preview từ chính file DOCX cấy
- Trong `integrateAi.onclick`:
  ```javascript
  injectedDocxBlob = await injectDocxOxml(currentDocxBuffer, delta);
  const { value: renderedHtml } = await mammoth.convertToHtml({ arrayBuffer: await injectedDocxBlob.arrayBuffer() });
  $('preview').innerHTML = renderedHtml;
  ```
- Thêm hiệu ứng cuộn nhẹ đến nội dung vừa cấy.

## Cách kiểm thử
1. Nạp file giáo án Toán 7 và dán PPCT có 2 mã NLS (`1.2.TC1a` và `3.1.TC1a`).
2. Bấm "Tích hợp":
   - Kiểm tra màn hình xem trước tự động hiển thị giáo án mới.
   - Kiểm tra Mục I: Thấy mục c) Năng lực số nằm trọn vẹn SAU toàn bộ mục b) Năng lực riêng, gồm 2 gạch đầu dòng riêng biệt, giữ nguyên mô tả chi tiết của giáo viên.
   - Kiểm tra Mục III: Mã `1.2.TC1a` nằm ở phần `d) Tổ chức thực hiện` của Hoạt động Hình thành kiến thức; mã `3.1.TC1a` nằm ở phần `d) Tổ chức thực hiện` của Hoạt động Luyện tập/Vận dụng. Hoạt động Khởi động không bị chèn sai.
3. Xuất file Word và mở trong Microsoft Word để xác nhận 100% định dạng và vị trí chuẩn mực.

## Tiêu chí nghiệm thu
- Không còn lỗi cấy ngắt đôi mục b) trong Mục I.
- Mỗi mã NLS được phân tách thành dòng riêng biệt, bảo toàn mô tả của giáo viên.
- Các mã khác nhau được phân bổ đúng vào Hoạt động 2 và Hoạt động 3, cấy đúng vào mục `d) Tổ chức thực hiện`.
- Màn hình xem trước tự động cập nhật ngay sau khi bấm tích hợp.
