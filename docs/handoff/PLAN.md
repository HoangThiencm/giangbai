# PLAN: Nâng cấp nhận diện số/ngày/thể loại/trích yếu văn bản bot Telegram

**Ngày:** 2026-11-14  
**Vấn đề:** Bot nhận diện số VB, ngày, thể loại, trích yếu thiếu chính xác, đặc biệt với file scan.  
**Phạm vi:** `api/vanban.php`, `api/telegram_vanban.php`, `tests/telegram-vanban-webhook-smoke.py`  
**Không đụng:** schema DB, cloudflare-worker, CI/CD, file ngoài phạm vi trên.

---

## Kết quả test thực tế (12 PDF)

| File | Số nhận diện | Lỗi |
|------|-------------|-----|
| 02. TB KẾT LUẬN... | `1535/6E-SGDDT` | Sai – nhầm font CMap; đúng là `1535/TB-SGDĐT` hoặc tương tự |
| 115-KE HOACH... | `` (rỗng) | File scan hoàn toàn, chars=2732 (binary junk) |
| 2.11 CV 663... | `25/10` | Sai – lấy ngày `25/10` trong context thay số VB; đúng là `663/UBND-VP` hoặc `663/MTTQ-BTT` |
| 93_2026_TT_BGDDT.signed | `` (rỗng) | chars=39, bị ký số che → chỉ đọc được ngày |
| CV huong dan DTHT... | `19/2026/TT-BGDĐT` | Sai – lấy nhầm số TT dẫn chiếu trong "Căn cứ"; đúng là `7037/SGDĐT-GDPT&GDTX` |
| CV trienkhai VB12151... | `16416/KH-UBND` | Sai – số nằm trong nội dung "triển khai Kế hoạch số 16416" |
| VB THONG BAO (1)... | `6328/SKHCN-CĐS` | Đúng số nhưng thể loại sai (`Quyết định` → `Thông báo`) |
| T11_2026 nang cao... | `11539/UBND` | Sai – nhầm số từ nội dung; đúng là `12210/UBND-...` |
| KẾ HOẠCH TỔ CHỨC 20.11... | `265/KH-UBND` | Đúng (qua annotation) nhưng thiếu trích yếu |
| DỰ THẢO KE HOACH CM | `03/KH-CM` | Đúng |
| KH trien khai KH 359 | `359/KH-UBND` | Đúng (qua annotation) |
| CV thay doi mot so | `6725/SGDĐT-QLCL` | Đúng |

**Tỷ lệ đúng:** 4/12 (33%). **Vấn đề chính:**
1. **Số ngày bị nhầm là số VB** (`25/10` → thực ra là ngày 25/10)
2. **Số trong căn cứ dẫn chiếu bị lấy** khi số chính (ký số/scan) không đọc được
3. **Thể loại nhận diện sai** (`Quyết định` thay vì `Thông báo`) do tìm thấy từ type sai ngữ cảnh
4. **File scan** (chars thực ≤100 sau lọc): không có text có nghĩa → cần fallback caption
5. **Font CMap lỗi**: chars cao nhưng text không có nghĩa (02. TB KẾT LUẬN)

---

## A. `api/vanban.php` — Sửa `vbd_find_document_number()` và `vbd_is_reference_context()`

### A1. Loại trừ số ngày bị nhầm là số VB

**Vấn đề:** Pattern `([0-9]*[\/-]org)` khớp `25/10` trong chuỗi "ngày 25/10". Thêm guard.

**Sửa:** Trong `vbd_is_reference_context()`, thêm: nếu `$before` kết thúc bằng pattern ngày (`\bngày\b` hoặc `\btháng\b`) → return true.

Thêm vào dòng 404 (sau block địa chỉ, trước block căn cứ):
```php
if (preg_match('/\b(ngày|tháng|năm)\s*$/ius', $tail)) return true;
```

### A2. Siết pattern fallback để không lấy số từ nội dung

**Vấn đề:** Các fallback ở dòng 627–660 quét `$head` (1400 ký tự) và lấy số đầu tiên dạng `NNNN/XXX` ngay cả khi nằm trong câu "triển khai Kế hoạch số 16416/KH-UBND của...".

**Sửa:** Các fallback chỉ chạy nếu head có từ `Số:` / `Số ` ở 400 ký tự đầu (không phải trong câu dài):
- Dòng 629 (`if (empty($result['document_number']))`): thêm điều kiện `preg_match('/(?:^|\n)\s*Số\s*[:\.]?\s*\d/iu', mb_substr($head, 0, 500))`
- Dòng 643 (siêu cứu hộ): giữ nguyên logic hiện tại nhưng bổ sung: nếu số tìm được nằm ngay sau context "Căn cứ|Thực hiện|triển khai" → bỏ qua.

### A3. Sửa nhận diện thể loại từ type line (`vbd_match_type_line`)

**Vấn đề:** "THÔNG BÁO" xuất hiện trong câu "THÔNG BÁO kết quả cuộc họp" nằm giữa văn bản → bị nhầm là thể loại.

Hiện tại `vbd_match_type_line` đã dùng `^` anchor trong `/^...(THÔNG BÁO|...)/uim`, nhưng vẫn có thể khớp giữa văn bản nếu text layer bị ghép sai xuống dòng.

**Sửa:** Giới hạn tìm type chỉ trong 600 ký tự đầu của `$head` thay vì toàn bộ 1400:
```php
$headForType = function_exists('mb_substr') ? mb_substr($head, 0, 600) : substr($head, 0, 600);
$typeLine = vbd_match_type_line($headForType);
```
(Thay `$head` ở dòng 680 bằng `$headForType`)

Thêm biến `$headForType` vào `vbd_regex_extract()` trước dòng 680.

### A4. Nâng cấp nhận diện "Công văn" từ trích yếu

Hiện tại line 686 chỉ check `V/v` + `Kính gửi`. Thêm: nếu không có thể loại nhưng có số kiểu `NNNN/XXX-XXX` và `Kính gửi` → type = `Công văn`.

```php
if ($result['document_type'] === '' && $result['document_number'] !== '' && preg_match('/Kính\s*gửi\s*:/iu', $head)) {
    $result['document_type'] = 'Công văn';
}
```

(Thêm sau dòng 688, trước comment ngày ban hành)

### A5. Cải thiện trích yếu khi không có V/v

**Vấn đề:** Nhiều văn bản hành chính dùng "Trích yếu:" thay "V/v:". File scan thì không có gì.

**Sửa (dòng 730–738):** Bổ sung pattern tìm trích yếu theo tiêu đề đứng thẳng sau thể loại — hiện đã có `vbd_title_below_type()`. Vấn đề là `vbd_title_line_skipped()` đang skip dòng bắt đầu bằng chữ hoa nhưng không phải thể loại — cần thêm:

```php
// Thêm vào vbd_title_line_skipped: skip dòng địa chỉ cơ quan
if (preg_match('/^(Địa chỉ|Email|Website|Điện thoại|Tel|ĐT\s*:)/iu', $line)) return true;
```

---

## B. `api/telegram_vanban.php` — Xử lý caption và file scan

### B1. Parse caption có cấu trúc (ưu tiên cao nhất)

**Vấn đề:** Khi người dùng gửi file scan kèm caption `Số: 1535/TB-SGDĐT, Ngày: 05/11/2026, Thể loại: Thông báo`, bot hiện tại chỉ dùng caption làm title fallback (dòng 386).

**Sửa:** Thêm hàm `tvb_parse_caption_structured(string $caption): array` trong `telegram_vanban.php`:

```php
function tvb_parse_caption_structured(string $caption): array {
    $result = [];
    // Số: ...
    if (preg_match('/(?:Số|So)\s*[:\.]?\s*([0-9\/\-A-Za-zÀ-ỹĐđ&.]+)/iu', $caption, $m))
        $result['document_number'] = vbd_normalize_doc_number(trim($m[1]));
    // Ngày: dd/mm/yyyy
    if (preg_match('/(?:Ngày|Ngay)\s*[:\.]?\s*(\d{1,2})[\/\-\.](\d{1,2})[\/\-\.](\d{4})/iu', $caption, $m))
        $result['document_date'] = sprintf('%04d-%02d-%02d', (int)$m[3], (int)$m[2], (int)$m[1]);
    // Thể loại: ...
    if (preg_match('/(?:Thể loại|The loai|Loại)\s*[:\.]?\s*([^\n,;]{3,30})/iu', $caption, $m))
        $result['document_type'] = trim($m[1]);
    // Trích yếu: ...
    if (preg_match('/(?:Trích yếu|Trich yeu|V\/v|Về việc)\s*[:\.]?\s*([^\n]{5,200})/iu', $caption, $m))
        $result['title'] = trim($m[1]);
    // Cơ quan: ...
    if (preg_match('/(?:Cơ quan|Co quan|Nơi ban hành)\s*[:\.]?\s*([^\n,;]{3,80})/iu', $caption, $m))
        $result['organization'] = trim($m[1]);
    return $result;
}
```

**Áp dụng (dòng 381–392):** Sau khi có `$parsed` từ `vbd_parse_document`, override từng trường nếu caption có cấu trúc:

```php
$source = tvb_extract_text($temporary, $file['name'], (string)($message['caption'] ?? ''));
try { $parsed = vbd_parse_document($source); } catch (Throwable $ignored) { $parsed = [...]; }

// Override bằng caption structured nếu có
$captionData = tvb_parse_caption_structured((string)($message['caption'] ?? ''));
foreach (['document_number','document_date','document_type','title','organization'] as $field) {
    if (!empty($captionData[$field])) $parsed[$field] = $captionData[$field];
}
```

### B2. Phát hiện file scan / text rỗng và hướng dẫn người dùng

**Điều kiện phát hiện scan:** Sau khi extract, nếu `vbd_text_len($source) < 80` (không đủ text có nghĩa).

**Sửa (thêm sau dòng 381, trước `vbd_parse_document`):**

```php
$isScan = vbd_text_len($source) < 80;
if ($isScan && trim((string)($message['caption'] ?? '')) === '') {
    // Gửi hướng dẫn nhưng vẫn tiếp tục lưu (confidence=low)
    tvb_api('sendMessage', [
        'chat_id' => $chatId,
        'text' => "📸 <b>File scan – không đọc được text.</b>\nGửi lại file và điền caption theo mẫu:\n<code>Số: 1535/TB-SGDĐT\nNgày: 05/11/2026\nThể loại: Thông báo\nTrích yếu: Kết luận cuộc họp chuyên môn cụm 8</code>",
        'parse_mode' => 'HTML',
    ]);
}
```

> **Lưu ý:** Luồng vẫn tiếp tục lưu văn bản (không abort). Người dùng có thể gửi lại với caption nếu muốn điền đúng.

---

## C. Cập nhật smoke test (`tests/telegram-vanban-webhook-smoke.py`)

### C1. Thêm sample case mới

Thêm vào dict `$samples` trong PHP runner string:

```python
'date_in_context' => "UBND PHƯỜNG HÒA AN\nSố: 663/UBND-VP\nngày 25 tháng 10 năm 2026\nKính gửi: Các đơn vị\nV/v phối hợp tuyên truyền, vận động\n",
'type_deep' => "SỞ KHOA HỌC VÀ CÔNG NGHỆ\nSố: 6328/SKHCN-CĐS\n...\nTHÔNG BÁO\nV/v tổ chức bồi dưỡng chuyển đổi số\n",
'cv_no_vv' => "ỦY BAN NHÂN DÂN\nSố: 11539/UBND-VP\nKính gửi: Các đơn vị\nTriển khai công tác nâng cao chấn chỉnh\n",
```

### C2. Thêm assert mới

```python
assert cases['date_in_context']['number'] == '663/UBND-VP', cases['date_in_context']
assert cases['date_in_context']['type'] == 'Công văn', cases['date_in_context']
assert cases['type_deep']['number'] == '6328/SKHCN-CĐS', cases['type_deep']
assert cases['type_deep']['type'] == 'Thông báo', cases['type_deep']
assert cases['cv_no_vv']['number'] == '11539/UBND-VP', cases['cv_no_vv']
assert cases['cv_no_vv']['type'] == 'Công văn', cases['cv_no_vv']
```

### C3. Thêm kiểm tra `tvb_parse_caption_structured` tồn tại trong webhook

```python
assert 'tvb_parse_caption_structured' in webhook, 'Missing caption structured parser'
assert 'captionData' in webhook or 'caption_data' in webhook or '$captionData' in webhook
```

---

## Thứ tự implement

1. **`api/vanban.php`** – Sửa 5 điểm A1→A5 (độc lập nhau, làm theo thứ tự)
2. **`api/telegram_vanban.php`** – Thêm B1 (`tvb_parse_caption_structured`) + B2 (scan detection)
3. **`tests/telegram-vanban-webhook-smoke.py`** – Thêm C1→C3
4. Chạy `python tests/telegram-vanban-webhook-smoke.py` → phải pass
5. Ghi `docs/handoff/IMPLEMENT.md`

---

## Kiểm tra chấp nhận

- [ ] `python tests/telegram-vanban-webhook-smoke.py` → `OK`
- [ ] Case `date_in_context`: number = `663/UBND-VP`, type = `Công văn`
- [ ] Case `type_deep`: type = `Thông báo`
- [ ] Case `cv_no_vv`: type = `Công văn`
- [ ] Gửi file scan qua bot (không caption) → bot gửi tin nhắn hướng dẫn caption
- [ ] Gửi file scan kèm caption có cấu trúc → bot hiển thị đúng số/ngày/thể loại từ caption
