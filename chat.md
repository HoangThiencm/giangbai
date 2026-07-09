# Ghi chú trao đổi dự án giangbai

Cập nhật: 09/07/2026

Chỉ nội dung phiên hôm nay.

---

## 1. TKB — demo 30 lớp CT GDPT 2018 + chức năng Kiểm tra

### Yêu cầu

1. Bám **số tiết thực tế CT GDPT 2018** (ví dụ Tin học ≈ **1 tiết/tuần**, không còn 2).
2. Demo **đầy đủ** cho **30 lớp**: đủ môn, đủ GV (≈ 30 × 1,9).
3. **Dữ liệu demo** để user tự kiểm tra (file JSON).
4. Trong app có **chức năng kiểm tra** nhanh (tham khảo tkb.com.vn / OLM TKB / VietSchool).

### Khung tiết/tuần dùng trong demo (THCS, ÷ 35 tuần)

| Môn / hoạt động | Tiết/tuần | Ghi chú |
|-----------------|-----------|---------|
| Ngữ văn | 4 | 140/năm |
| Toán | 4 | 140/năm |
| Ngoại ngữ 1 | 3 | 105/năm |
| Giáo dục công dân | 1 | 35/năm |
| Lịch sử + Địa lí | 3 | 105/năm — tách theo khối |
| KHTN (6–7) / Lý+Hóa+Sinh (8–9) | 4 | 140/năm |
| Công nghệ | 1 | 35/năm |
| **Tin học** | **1** | **35/năm** |
| GDTC | 2 | 70/năm |
| Âm nhạc + Mỹ thuật | 1+1 | Nghệ thuật 70/năm |
| HĐTN-HN | 2 | phần HĐTN-HN |
| Sinh hoạt | 1 | thực tế trường |
| **Tổng** | **~28** | Gần khung 29–29,5 (chưa môn tự chọn) |

**Tách theo khối**

- **Lớp 6–7:** Lịch sử 1 + Địa lí 2; **Khoa học tự nhiên 4** (gộp).
- **Lớp 8–9:** Lịch sử 2 + Địa lí 1; **Vật lí 1 + Hóa 2 + Sinh 1**.

### Demo 30 lớp

| Hạng mục | Giá trị |
|----------|---------|
| Lớp | **30** = 8(K6) + 8(K7) + 7(K8) + 7(K9) |
| GV | **57** (= 30 × 1,9) |
| Phòng BM | 17 |
| Phân công | 448 dòng · **840 tiết/tuần** |
| Tiết/lớp | 28 / capacity sáng 30 |
| Tin học toàn trường | **30 tiết** (= 30 × 1) |

**File kiểm tra dữ liệu:** `data/tkb-demo-30lop-ct2018.json`  
**Nút UI:** `Demo 30 lớp CT2018` · `Xuất dữ liệu` (JSON hiện tại) · tab **Kiểm tra**

Sinh lại JSON:

```text
node agent-tools/build-demo-30-ct2018.js
```

### Chức năng Kiểm tra (diagnostics)

Tham chiếu app TKB chuyên dụng:

| Nguồn | Ý tưởng mang sang |
|-------|-------------------|
| tkb.com.vn | Trợ lý: trùng lịch, cách tiết, tải GV, % hoàn thành |
| OLM TKB | Quy trình nhập → kiểm → xếp; cảnh báo trước xếp |
| VietSchool | Tham số hệ thống, rà phân công, công bố lịch |

**Trong app (`thoikhoabieu.html`):**

- Tab **Kiểm tra** + nút **Kiểm tra** cạnh **Xếp lịch**
- Thẻ tóm tắt: Lớp / GV / tỷ lệ / phòng / tiết / **số lỗi** / **số cảnh báo**
- **Lỗi đỏ** (chặn): vượt capacity lớp, vượt ĐM GV, max môn/ngày, phòng BM thiếu sức chứa, domain rỗng, precheck
- **Cảnh báo vàng**: GV 0 tiết, tải ≥90% ĐM, lệch tải max−min, thiếu môn CT2018 theo lớp, phòng sát trần, lớp quá trống
- Bảng **tải GV** + **tải lớp/capacity** + chip **tổng tiết theo môn**
- Gợi ý sửa nhanh

### Kết quả kiểm tra demo 30 lớp (lần build)

- **Lỗi: 0 · Cảnh báo: 0** → dữ liệu sạch, sẵn sàng xếp
- Curriculum K6/K8 = **28 tiết/lớp**
- Tin học = **30** tiết toàn trường (= 30 × 1)
- Cảnh báo lệch tải chỉ so **trong cùng môn** (không so Tin với Toán)

### File đã đụng

| File | Việc |
|------|------|
| `thoikhoabieu.html` | CT2018 curriculum, Demo 30, tab Kiểm tra, xuất JSON, alias phòng BM |
| `data/tkb-demo-30lop-ct2018.json` | Dữ liệu demo đầy đủ để rà soát |
| `agent-tools/build-demo-30-ct2018.js` | Script sinh JSON + in diagnostics |

### Lỗi “không thấy GV / TKB” (đã sửa)

**Nguyên nhân:** API hosting hoặc localStorage nạp **project rỗng** → app coi như đã có dữ liệu, **không** nạp demo → bảng GV trống. Thời khóa biểu cũng trống nếu chưa bấm **Xếp lịch** (demo chỉ nạp phân công, chưa chạy solver).

**Đã sửa:**

- Bỏ qua project rỗng (hosting + localStorage)
- Mặc định nạp **Demo 30 lớp CT2018** khi không có dữ liệu thật
- Banner trạng thái luôn hiện số GV/lớp/PC
- Sau demo: mở tab **Giáo viên**, thông báo số liệu, lưu localStorage
- Nhắc rõ: bấm **Xếp lịch** mới có bảng TKB

**Cách user kiểm tra:** Ctrl+F5 → thấy banner `57 GV · 30 lớp…` → tab Giáo viên có danh sách → **Xếp lịch**.

### Việc tiếp theo (chưa làm)

- Slot cố định (Chào cờ / SH)
- Cờ tiết đôi trên phân công
- Web Worker khi 30+ lớp
- Chạy thử xếp 100% + beauty trên demo 30 (nặng hơn 16 lớp)

---

*Khi ổn định, bổ sung `thongtin.md`.*
