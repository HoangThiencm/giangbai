# Ghi chú trao đổi dự án giangbai

Cập nhật: 27/06/2026

Tài liệu tổng hợp các chủ đề đã trao đổi trong phiên chat. Dùng để đọc lại — không phải tài liệu kỹ thuật chính thức (`thongtin.md`).

---

## Mục lục

1. [DNS chặn quảng cáo](#1-dns-chặn-quảng-cáo)
2. [LiteParse + chuyenpdf.html](#2-liteparse--chuyenpdfhtml)
3. [Đã triển khai trên chuyenpdf.html](#3-đã-triển-khai-trên-chuyenpdfhtml)
4. [taobaitap.html — bỏ tab Game](#4-taobaitaphtml--bỏ-tab-game)
5. [vehinh.html — đánh giá & gợi ý bổ sung](#5-vehinhhtml--đánh-giá--gợi-ý-bổ-sung)
6. [Việc chưa làm](#6-việc-chưa-làm)

---

## 1. DNS chặn quảng cáo

### Câu hỏi

Có thể dùng dự án giangbai để làm DNS chặn quảng cáo không?

### Kết luận

| Trong repo giangbai | Song song ở mạng trường/nhà |
|---------------------|------------------------------|
| **Không** — không có DNS server | **Có** — Pi-hole, AdGuard, NextDNS… |

giangbai là web app PHP + HTML. DNS ad block là tầng mạng — hai thứ bổ sung nhau, không gộp vào một repo.

`cloudflare-worker/worker.js` chỉ phục vụ AI giải thích bài, **không** phải DNS filtering.

### Gợi ý theo quy mô

- **Trường:** lọc DNS ở router/Wi‑Fi; whitelist hosting, Drive, CDN, MathJax…
- **Chỉ muốn site sạch:** không cần DNS — site tự host, không có mã quảng cáo bên thứ ba

---

## 2. LiteParse + chuyenpdf.html

### Câu hỏi

Tích hợp LiteParse V2.1 vào `chuyenpdf.html` được không?

### Kết luận

**Có** — nhưng **bổ sung** engine mới (hybrid), không thay Mistral/Gemini.

| Engine | Phù hợp |
|--------|---------|
| **LiteParse (local)** | PDF số — có lớp chữ, Word→PDF |
| **Mistral OCR** | PDF scan, ảnh chụp |
| **Gemini Vision** | Toán + LaTeX, văn bản hành chính khó |

### Luồng hybrid đề xuất

```text
Upload PDF
  → phân tích có lớp chữ hay scan
  → gợi ý engine (user vẫn đổi tay)
  → PDF số     → LiteParse
  → scan/ảnh   → Mistral / Gemini
  → toán LaTeX → Gemini
```

### Lưu ý kỹ thuật

- LiteParse WASM ~4–5 MB, tải từ jsDelivr lần đầu
- Trên browser **không** OCR scan được (chưa gắn Tesseract.js)
- Chế độ Toán + LaTeX **không** dùng LiteParse

### Trao đổi thêm

- User **không cần biết** file scan hay số — app tự phát hiện + **gợi ý**, không ép tự động hoàn toàn
- Môi trường Gemini Canvas: không cần API key Gemini; Mistral đã hardcode
- Code LiteParse gộp **trong một file** `chuyenpdf.html` (không cần `liteparse-client.js` riêng)

---

## 3. Đã triển khai trên chuyenpdf.html

### Tính năng đã thêm

- Dropdown **LiteParse (local, PDF có chữ)**
- Hộp **gợi ý engine** sau khi upload — tiêu đề dạng `Gợi ý: Gemini Vision · gemini-2.5-flash`
- Phân tích PDF bằng `pdf.js` (số trang, ký tự/trang, scan hay số)
- Nút **Dùng gợi ý này**
- Logic LiteParse nằm inline trong `chuyenpdf.html`

### Sửa sau khi dùng thử

| Vấn đề | Cách xử lý |
|--------|------------|
| Mặc định **Toán + LaTeX** → LiteParse báo lỗi dù file không có toán | Đổi mặc định → **Văn bản thường**; chặn LiteParse + LaTeX bằng hộp thoại rõ ràng |
| Chữ ký trong PDF bị nhầm scan → ép Mistral | Chỉ coi scan khi **gần như không có lớp chữ**; chữ ký/ảnh nhúng vẫn gợi ý LiteParse |
| Gợi ý chỉ nói "chế độ LaTeX" | Gợi ý nêu rõ **engine + phân tích file** |

### Gợi ý engine (sau khi sửa)

| File + chế độ | Gợi ý |
|---------------|--------|
| PDF số + Văn bản thường | LiteParse |
| PDF scan thật | Mistral |
| Có toán / LaTeX | Gemini |
| Văn bản hành chính | Gemini (gợi ý, không tự đổi) |
| Ảnh | Mistral |

---

## 4. taobaitap.html — bỏ tab Game

### Yêu cầu

Bỏ tab **Game giáo dục** (link `trochoi.html`).

### Đã làm

- Xóa nút tab Game
- Phần **Chế độ** còn: **Trắc nghiệm** | **Tự luận** (grid 2 cột)

---

## 5. vehinh.html — đánh giá & gợi ý bổ sung

### File liên quan

- `vehinh.html` — giao diện
- `app.js` — logic canvas + AI

### Đã có sẵn

#### Vẽ tay (Fabric.js)

| Công cụ | Có |
|---------|-----|
| Chọn / di chuyển | ✓ |
| Điểm A, B, C… | ✓ |
| Bút tự do (pencil) | ✓ — nét cố định 2px |
| Đoạn thẳng, hình tròn | ✓ |
| Chữ, LaTeX, chèn ảnh | ✓ |
| Undo / Redo, Copy / Paste | ✓ |
| Zoom, pan (Alt + kéo) | ✓ |
| Lưới, hút lưới | ✓ |
| Khóa đối tượng AI | ✓ |
| Dark mode | ✓ |

#### AI vẽ hình

- Nhập mô tả → Gemini sinh **mã JavaScript Fabric.js** → vẽ lên canvas
- Có thể kèm **ảnh tham chiếu**
- GeoGebra iframe — **tách riêng**, không gắn canvas

#### Đưa ảnh vào AI

| Cách | Có |
|------|-----|
| Chọn file (`Tải ảnh lên`) | ✓ |
| Dán ảnh Ctrl+V vào ô đề bài | ✓ |
| Chèn ảnh lên canvas (toolbar) | ✓ |
| **Chụp camera trực tiếp** | ✗ chưa có |

### Có thể bổ sung thêm (vẽ tay)

**Dễ — nên làm trước**

- Slider **độ dày nét** bút tự do
- **Hình chữ nhật**, **mũi tên**, **đa giác**
- **Tẩy** (eraser)
- **Xuất PNG** canvas
- Tối ưu **bút cảm ứng / tablet**

**Trung bình**

- Đoạn song song / vuông góc từ điểm có sẵn
- Nhãn độ trên cung góc (nút tay, AI đã có hàm `addAngleArc`)
- Snap vào điểm / đoạn (hiện chỉ snap lưới)

**Khó**

- Gộp GeoGebra ↔ canvas
- Nhận phác thảo tay → hình chuẩn (cần AI riêng)

### Chụp hình → AI đọc → vẽ: ổn định không?

#### Luồng kỹ thuật (gần sẵn)

```text
Chụp / chọn ảnh
  → activeImageFile
  → Gemini Vision (ảnh + prompt)
  → mã trong thẻ <javascript>...</javascript>
  → executeAiCode() vẽ lên canvas
```

Upload và dán ảnh **đã dùng cùng pipeline**. Thêm camera chỉ là UI:

```html
<input type="file" accept="image/*" capture="environment">
```

#### Đánh giá ổn định

| Tình huống | Mức ổn định |
|------------|-------------|
| Upload / dán ảnh + bấm Vẽ Hình | Ổn nếu có API key Gemini |
| Thêm chụp camera | Tương đương upload |
| Ảnh rõ, hình đơn giản | Khá tốt |
| Ảnh mờ, nhiều hình, chữ nhỏ | Kém — AI hay sai tỷ lệ |
| Mã JS AI sinh ra | Điểm yếu — đôi khi lỗi cú pháp / tọa độ |
| Hết quota API (429) | Có xoay key, vẫn có thể fail |

#### Điều kiện chạy

- Trang **bắt đăng nhập** (`authToken`)
- AI gọi **Gemini trực tiếp** — cần `global_gemini_keys` (Canvas có thể không cần)
- `hf-fallback-client.js` được load nhưng **`app.js` không dùng** — không fallback khi Gemini lỗi

### Gợi ý ưu tiên cho giáo dục

1. Nút **Chụp ảnh / chọn file** gộp một chỗ, rõ ràng
2. **Độ dày bút** + hình chữ nhật / mũi tên
3. **Xuất PNG** sau khi vẽ
4. Quy trình: AI vẽ phác thảo → GV **chỉnh tay** trên canvas

**Chụp → vẽ tự động:**

- Dùng được: ảnh đề SGK chụp rõ, biểu đồ đơn giản
- Không kỳ vọng: scan mờ, hình phức tạp khớp 100%
- Ổn định hơn nếu: ảnh → AI **mô tả** → GV sửa mô tả → mới vẽ

### Câu hỏi mở (vehinh)

Ưu tiên triển khai:

- **(A)** Bổ sung vẽ tay
- **(B)** Thêm chụp ảnh
- **(C)** Cả hai

---

## 6. Việc chưa làm

| Chủ đề | Trạng thái |
|--------|------------|
| DNS ad block Wi‑Fi trường | Chỉ trao đổi |
| Whitelist domain Pi-hole | Chưa liệt kê |
| `MISTRAL_API_KEY` chuyển ra backend | Chưa làm |
| vehinh: chụp camera | Chưa làm |
| vehinh: xuất PNG, tẩy, hình chữ nhật… | Chưa làm |
| vehinh: Tesseract.js cho LiteParse scan | Chưa làm (chuyenpdf) |

---

*Khi triển khai chính thức, cập nhật `thongtin.md`.*