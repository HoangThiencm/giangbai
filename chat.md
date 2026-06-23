# Tổng hợp phản biện: Soạn bài Gemini và hệ thống Lộ trình Toán 4–9

Ngày tổng hợp: 23/06/2026

## 1. Mục tiêu sản phẩm

Mục tiêu được thống nhất là xây dựng luồng làm việc:

```text
Ảnh sách giáo khoa
→ soanbaigemini tạo bài học đúng trình độ và đúng cấu trúc
→ chuyển thành gói dữ liệu bài học có schema rõ ràng
→ import vào trình soạn Lộ trình Toán 4–9
→ giáo viên chèn hoặc thay ảnh phù hợp
→ xem thử
→ lưu và công khai cho học sinh
```

Kỳ vọng cuối cùng là phần nội dung và cấu trúc được tự động hóa gần như hoàn toàn. Giáo viên chủ yếu kiểm tra, chèn ảnh và quyết định lưu/công khai.

## 2. Các file và thành phần đã đối chiếu

- `soanbaigemini.html`: nhận ảnh SGK, gọi Gemini, kiểm định nội dung, parse section, tạo ảnh minh họa và xuất Word.
- `lotrinh.js`: giao diện học sinh, tải bài từ API, render nội dung và chấm bài.
- `lotrinhtoan4.html` đến `lotrinhtoan9.html`: các vỏ trang theo từng lớp.
- `lesson-import.js`: module dùng chung — parser Gemini, schema `lesson-import-v1`, validate, build/export package (mới, 23/06/2026).
- `admin-lesson-manager.js`: trình soạn bài của giáo viên; gọi `LessonImport`, import/export JSON, không còn parser trùng.
- `api/lessons.php`: đọc/ghi bài học trong database.

Sáu file `lotrinhtoan4–9.html` chủ yếu khác nhau ở:

- `LOTRINH_PAGE_KEY`
- `LOTRINH_SUBJECT`
- Tiêu đề trang

Toàn bộ các lớp dùng chung lõi `lotrinh.js`, `admin-lesson-manager.js` và API bài học.

## 3. Vấn đề ban đầu: nội dung vượt quá ảnh và trình độ lớp

Prompt cũ trong `soanbaigemini.html` có mâu thuẫn:

- Một mặt yêu cầu không vượt trình độ.
- Mặt khác yêu cầu nội dung phong phú, bài mở rộng và nhiều dạng bài bắt buộc.

Điều này khiến Gemini có xu hướng bổ sung kiến thức liên quan nhưng chưa xuất hiện trong ảnh hoặc thuộc mức cao hơn.

### Nguyên tắc đã cập nhật

- Ảnh SGK là **trần kiến thức chính**.
- Lớp học được chọn là **trần trình độ thứ hai**.
- Nếu ảnh và thông tin lớp có dấu hiệu không khớp, lấy mức thấp hơn.
- Chỉ sử dụng khái niệm, ký hiệu, thuật ngữ, dạng bài và phương pháp xuất hiện trực tiếp hoặc xác định chắc chắn từ ảnh.
- Bài tự tạo chỉ được là bài song sinh: đổi số liệu hoặc bối cảnh nhưng giữ nguyên phương pháp, loại phép tính, số bước và độ khó.
- Không tạo dạng mới hoặc bài mở rộng chỉ vì có liên quan đến chủ đề.
- Hai vòng phản biện phải loại nội dung vượt lớp hoặc vượt ảnh.
- Giảm `temperature` để kết quả bám SGK ổn định hơn.

### Điểm vẫn cần cân nhắc

Prompt hiện còn ép số lượng:

- 3–5 bài tự luận ngắn.
- 2 bài kéo thả vào ô trống.
- 2 bài sắp xếp.
- 1–2 bài nối ô.
- 10 câu trắc nghiệm.
- Một dạng bài toán thực tế.

Khi ảnh SGK ít nội dung, áp lực đủ số lượng vẫn có thể khiến Gemini sáng tác quá nhiều. Đúng schema chưa chắc đồng nghĩa với đúng quy mô sư phạm. Nên cân nhắc số lượng linh hoạt theo lượng kiến thức trong ảnh.

## 4. Kiến trúc hiện tại

Luồng thực tế trong code hiện nay là:

```text
soanbaigemini
→ Gemini trả văn bản có heading
→ (tuỳ chọn) tải lesson-import-v1.json hoặc copy toàn bộ raw
→ tab Khác trong admin: Import text / Import JSON
→ lesson-import.js parse + validate → điền form soạn bài
→ giáo viên chèn ảnh theo manifest
→ bấm Lưu
→ POST payload JSON với action save_content
→ api/lessons.php lưu các cột JSON vào MySQL
→ lotrinh.js GET api/lessons.php
→ render bài cho học sinh
```

Điểm cần nói chính xác:

- Lộ trình **không đọc file `.json` tĩnh**.
- `lotrinh.js` tải bài từ database qua `api/lessons.php`.
- Editor hiện nhập văn bản Gemini, chưa có input file JSON.
- `soanbaigemini.html` hiện xuất Word, chưa xuất JSON.

## 5. Mapping hiện có giữa Soạn bài Gemini và Lộ trình

| Section từ Gemini | Trường lưu bài |
|---|---|
| MỤC TIÊU | `goal_text` khi lưu, `goal` khi API trả về |
| LÝ THUYẾT | `theory` |
| VÍ DỤ | `examples` |
| BÀI TẬP NỘP GIÁO VIÊN | `self_practice` |
| BÀI TẬP TỰ LUẬN NGẮN | `essay_exercises` |
| KÉO THẢ VÀO Ô TRỐNG | `fill_exercises` |
| NỐI Ô / SẮP XẾP | `drag_exercises` |
| TRẮC NGHIỆM | `questions` |
| KỸ NĂNG CẦN ĐẠT | `skills` |
| NHIỆM VỤ HỌC SINH | `tasks` |
| Video | `videos` — hiện chưa có trong đầu ra/import Gemini |

Mapping section đã có tương đối đầy đủ. Tuy nhiên, tỷ lệ hoàn thiện chỉ cao về cấu trúc field, chưa đồng nghĩa với độ tin cậy end-to-end.

## 6. Schema dữ liệu thực tế

Payload `save_content` trong `admin-lesson-manager.js` đã gần với schema import mong muốn.

Các kiểu dữ liệu quan trọng:

```js
theory: [
  { text: "...", ai: false }
]

examples: [
  { title: "DẠNG 1: ...", body: "...", ai: false }
]

self_practice: [
  { title: "DẠNG 1: ...", body: "...", ai: false }
]

questions: [
  {
    id: "q1",
    skill: "skill_id",
    prompt: "...",
    options: ["A", "B", "C", "D"],
    answer: 0
  }
]

essay_exercises: [
  { id: "essay_1", prompt: "...", answer: "4", hint: "..." }
]

fill_exercises: [
  {
    id: "fill_1",
    prompt: "... ___ ...",
    pool: ["..."],
    answer: "..." /* hoặc mảng */,
    hint: "..."
  }
]

drag_exercises: [
  {
    id: "drag_1",
    mode: "match",
    prompt: "...",
    left: ["..."],
    right: ["..."],
    pairs: [{ left: 0, right: 0 }],
    hint: "..."
  },
  {
    id: "drag_2",
    mode: "sort",
    prompt: "...",
    items: ["..."],
    answer: ["..."],
    hint: "..."
  }
]

skills: [
  { id: "skill_id", name: "Tên kỹ năng", target: 80 }
]

tasks: ["..."]
videos: [{ title: "...", url: "..." }]
```

Không cần thiết kế lại toàn bộ schema từ đầu. Cần chuẩn hóa payload đang có thành hợp đồng import/export ổn định.

## 7. Các khoảng trống quan trọng

### 7.1. Chưa có xuất/nhập file JSON

> **Cập nhật 23/06/2026:** Đã triển khai — xem mục 18. Nút tải/nhập JSON có ở `soanbaigemini.html` và tab Khác trong admin.

`soanbaigemini.html` (trước khi triển khai) chỉ:

- Hiển thị văn bản Gemini.
- Parse và xem trước.
- Copy từng section.
- Tạo ảnh minh họa.
- Xuất Word.

Editor hiện chỉ nhận text qua `importGeminiLessonRaw()`. Chưa có:

- Nút tải `lesson-import-v1.json`.
- Input chọn file JSON.
- Validator package trước khi điền form.

### 7.2. Metadata không đi theo import text

Importer hiện không tự điền đầy đủ:

- `subject`
- `chapter`
- `title`
- `slug`
- `order_index`
- `is_published`

Do đó quy trình hiện tại chưa phải “import nguyên bài”.

### 7.3. Ánh xạ kỹ năng–trắc nghiệm đang sai

Schema thật của câu hỏi có trường `skill`, nhưng `soanbaigemini` hiện yêu cầu format sáu cột:

```text
Câu hỏi | A | B | C | D | B
```

Khi thiếu `skill_id`, parser gán câu hỏi vào kỹ năng đầu tiên. Trong khi `lotrinh.js` tính điểm kỹ năng dựa trên `question.skill`. Vì vậy bảng kỹ năng có thể hiển thị đẹp nhưng không phản ánh đúng năng lực.

Format text fallback nên là:

```text
skill_id | Câu hỏi | A | B | C | D | B
```

Parser hiện tại đã hỗ trợ dạng bảy cột này.

Với JSON, mỗi câu phải có:

```json
{
  "skill": "skill_id",
  "prompt": "...",
  "options": ["...", "...", "...", "..."],
  "answer": 1
}
```

### 7.4. Hai bộ parser đang lệch nhau

> **Cập nhật 23/06/2026:** Đã gộp vào `lesson-import.js`; admin không còn parser trùng. `soanbaigemini` ưu tiên `LessonImport`, vẫn giữ fallback cũ — xem mục 18.3.

`soanbaigemini.html` và `admin-lesson-manager.js` (trước khi triển khai) cùng có parser riêng.

Parser trong admin đã tách rõ hơn:

- `dragMatch`
- `dragSort`
- Phân loại bài nối ô và sắp xếp.

Parser trong `soanbaigemini.html` cũ hơn và gộp nhiều trường hợp vào `drag`. Vì vậy preview/copy trong Soạn bài Gemini có thể không hoàn toàn giống kết quả import ở editor.

Không nên tạo thêm một parser thứ ba khi làm JSON. Cần tách logic dùng chung thành module.

### 7.5. Dấu `|` dễ phá cấu trúc

Pipe text dễ hỏng khi nội dung Toán chứa:

```text
a | b
{x | x > 0}
```

Parser có thể coi dấu `|` trong nội dung là dấu phân cột. JSON typed fields giải quyết vấn đề này tốt hơn. Pipe text nên được giữ làm fallback, không phải định dạng chính.

### 7.6. Video chưa nằm trong luồng Gemini

Editor và API có `videos`, nhưng:

- `soanbaigemini` không tạo section video.
- `importGeminiLessonRaw()` không nhập video.

Package JSON đầy đủ nên có `videos: []`, kể cả khi rỗng.

### 7.7. Trang Lộ trình bị scope theo lớp

Mỗi trang Toán 4–9 ép `PAGE_SUBJECT` tương ứng. Nếu mở trang Toán 4 nhưng import package có `subject: "Toán 6"`, hệ thống phải:

- Cảnh báo rõ ràng.
- Không âm thầm đổi môn hoặc lưu sai scope.
- Cho người dùng hủy import hoặc chuyển sang đúng trang.

### 7.8. Không tự lưu hoặc tự công khai

Import JSON chỉ nên điền form. Không được tự gọi API lưu bài.

Quy tắc an toàn:

- `is_published` mặc định là `false`.
- Không mang theo database `id`.
- Giáo viên phải xem preview và bấm Lưu.
- Sau khi lưu, giáo viên quyết định công khai.

## 8. Hình ảnh

### 8.1. Ảnh trong Soạn bài Gemini chưa chuyển thẳng sang Lộ trình

Ảnh Gemini sinh trong `soanbaigemini` là Data URL lưu trong RAM của phiên trình duyệt. Lộ trình chỉ hiển thị URL HTTP(S), thường là Google Drive sau khi giáo viên dán ảnh vào editor.

JSON không nên chứa base64 vì:

- File rất lớn.
- Khó kiểm soát dung lượng.
- Không tương thích trực tiếp với luồng Drive hiện tại.

JSON chỉ nên chứa marker và manifest:

```json
{
  "image_manifest": [
    {
      "id": "HINH_01",
      "section": "theory",
      "alt": "Mô tả ngắn",
      "type": "diagram",
      "prompt": "Mô tả ảnh cần tạo..."
    }
  ]
}
```

Nội dung vẫn đặt marker:

```markdown
![Mô tả ngắn](HINH_01)
```

Sau import, giáo viên dán ảnh thật để editor upload Drive và thay marker bằng URL.

### 8.2. Ảnh trong bài tập tương tác chưa render đúng

Lý thuyết, ví dụ và bài nộp dùng `lessonRichText()`, có thể render Markdown ảnh.

Các đề sau chủ yếu dùng `mathText()`:

- Tự luận.
- Điền khuyết.
- Trắc nghiệm.
- Nối ô và sắp xếp.

Admin cho phép dán ảnh vào các đề này nhưng giao diện học sinh có thể hiển thị Markdown ảnh thành chữ thô. Cần sửa renderer để prompt bài tập có thể dùng ảnh an toàn.

### 8.3. Vị trí marker ảnh

Renderer lý thuyết/ví dụ nhận ảnh chắc chắn nhất khi Markdown ảnh nằm riêng một dòng. Quy ước import nên bắt buộc marker ảnh đứng trên dòng riêng.

## 9. Đánh giá các nhận xét của Grok

### Những điểm Grok bổ sung đúng

- Payload `save_content` đã là nền schema thực tế.
- Cần ghi rõ `theory` và `examples` là mảng object.
- Có hai bộ parser không đồng nhất.
- `videos` còn thiếu trong luồng Gemini.
- Import phải kiểm tra môn theo trang đang mở.
- “70–80%” chỉ đúng về mapping, chưa đúng về độ tin cậy.
- Import không nên tự lưu và không nên ép đủ số lượng nếu bài SGK ngắn.

### Những điểm cần diễn đạt thận trọng hơn

Các nhận xét như:

- “Trắc nghiệm mất khi lưu”.
- “Điền khuyết 3 cột và 4 cột bị lỗi”.
- “Nối ô/sắp xếp bị nhầm”.

hiện là vùng rủi ro hợp lý nhưng chưa được chứng minh là lỗi còn tồn tại trong phiên bản code hiện tại.

Code hiện có:

- Đồng bộ bulk editor trước khi lưu.
- Parser điền khuyết xử lý cả ba và bốn cột bằng heuristic.
- Parser admin tách `dragMatch` và `dragSort`.
- `resolveQuestionsForSave()` đọc lại câu hỏi trước khi tạo payload.

Cần tạo fixture và test round-trip để xác nhận lỗi cụ thể trước khi sửa.

### Điểm không nên áp dụng máy móc

Validator “cảnh báo từ khóa vượt lớp” không đủ tin cậy. Kiến thức vượt lớp không thể xác định tốt chỉ bằng từ khóa.

Validator code nên kiểm tra:

- Kiểu dữ liệu.
- Số lượng và ID.
- Liên kết chéo.
- Đáp án hợp lệ.
- Marker ảnh.
- Môn/lớp.

Kiểm định học thuật vẫn cần prompt phản biện và giáo viên xem thử.

## 10. Kiến trúc đích được thống nhất

Không nên bắt Gemini trả JSON thô trực tiếp. Mô hình có thể tạo JSON thiếu dấu, sai kiểu hoặc sai liên kết ID.

Luồng nên là:

```text
Gemini trả nội dung dễ đọc
→ parser dùng chung chuyển thành object
→ normalize
→ validate
→ xuất lesson-import-v1.json
→ admin nhập JSON
→ validate lần hai
→ điền form và metadata
→ giáo viên chèn ảnh
→ teacher preview
→ giáo viên bấm Lưu
→ giáo viên quyết định công khai
```

Pipe text vẫn được giữ làm fallback cho nội dung cũ.

## 11. Hợp đồng `lesson-import-v1`

Không nên dùng nguyên xi payload API làm file import, vì API hiện có bất đối xứng:

- Gửi vào dùng `goal_text`.
- API trả ra dùng `goal`.
- Payload lưu có `action` và có thể có database `id`.
- API payload không có `schema_version` hoặc `image_manifest`.

Nên có adapter:

```text
lesson-import-v1
↔ normalize/validate
↔ save_content payload
```

Khung package:

```json
{
  "schema_version": "lesson-import-v1",
  "subject": "Toán 6",
  "chapter": "Chương 2: Số tự nhiên",
  "title": "Bài 5: ...",
  "slug": "math6-chuong-2-bai-5",
  "order_index": 5,
  "is_published": false,
  "goal_text": "...",
  "theory": [],
  "examples": [],
  "self_practice": [],
  "essay_exercises": [],
  "fill_exercises": [],
  "drag_exercises": [],
  "questions": [],
  "skills": [],
  "tasks": [],
  "videos": [],
  "image_manifest": []
}
```

### Quy tắc package

- Không chứa database `id`.
- `schema_version` là bắt buộc.
- `subject` phải thuộc `Toán 4` đến `Toán 9`.
- `is_published` khi import luôn được ép về `false`, bất kể file ghi gì.
- `answer` của trắc nghiệm là số từ 0 đến 3.
- Mỗi `questions[].skill` phải trùng một `skills[].id`.
- `drag_exercises[].mode` phải là `match` hoặc `sort`.
- ID trong từng collection phải duy nhất.
- Marker `HINH_xx` phải có entry tương ứng trong `image_manifest` hoặc được cảnh báo.
- Ảnh trong nội dung phải nằm riêng một dòng.

## 12. Validator cần có

### Lỗi chặn import

- JSON không parse được.
- Sai hoặc thiếu `schema_version`.
- Sai kiểu dữ liệu chính.
- Thiếu `subject`, `title` hoặc `slug`.
- Môn không hợp lệ.
- `questions[].answer` ngoài khoảng 0–3.
- Câu trắc nghiệm không có đúng bốn lựa chọn.
- `questions[].skill` không tồn tại.
- `drag_exercises[].mode` không hợp lệ.
- Bài nối ô có index pair vượt phạm vi.

### Cảnh báo nhưng vẫn cho import

- Thiếu video.
- Không có ảnh.
- Không có bài thực tế.
- Số lượng trắc nghiệm ít hơn cấu hình gợi ý.
- Thiếu một loại bài tập tương tác.
- Có marker ảnh chưa có manifest.
- `subject` khác với trang đang mở.
- Slug có nguy cơ trùng bài đang có.

Các cảnh báo về độ khó chỉ nên là gợi ý, không thay thế kiểm định học thuật.

## 13. Test round-trip cần có

Trước khi coi import là ổn định, cần bộ fixture bao phủ:

1. Lý thuyết nhiều đoạn, Markdown và LaTeX.
2. Ví dụ có nhiều heading `DẠNG`.
3. Bài nộp giáo viên.
4. Tự luận có đáp án số nguyên, thập phân, phân số và căn.
5. Điền khuyết một ô và nhiều ô.
6. Điền khuyết ba cột và bốn cột ở pipe fallback.
7. Nối ô có mapping không theo thứ tự 0-0.
8. Sắp xếp có phần tử giống nhau hoặc LaTeX.
9. Trắc nghiệm sáu cột và bảy cột có `skill_id`.
10. Nội dung Toán chứa ký hiệu `|`.
11. Marker ảnh trong lý thuyết, ví dụ và đề bài.
12. Package sai lớp so với trang đang mở.
13. Export → import → lưu → API trả về → render.

Mục tiêu test:

```text
lesson-import-v1
→ import form
→ build save_content payload
→ lưu/đọc API
→ normalize lại
```

Nội dung có ý nghĩa phải được bảo toàn và các liên kết ID không bị thay đổi ngoài những trường được phép chuẩn hóa.

## 14. Lộ trình triển khai đã chốt

> **Trạng thái 23/06/2026:** P0, P0a, P1, P2, P3, P2.5 (một phần), P4 (một phần) đã code — chi tiết từng file ở **mục 18**. P5 và round-trip API đầy đủ chưa xong.

### P0 — Fixture và module dùng chung

- Viết các fixture round-trip tối thiểu.
- Tách parser, normalizer và validator thành module dùng chung, dự kiến `lesson-import.js`.
- Không tạo thêm parser riêng trong admin hoặc `soanbaigemini`.

### P1 — Chuẩn hóa package

- Xây `buildLessonImportPackage()`.
- Xây `normalizeLessonImportPackage()`.
- Xây `validateLessonImportPackage()`.
- Xây adapter package ↔ payload `save_content`.

### P2 — Cập nhật Soạn bài Gemini

- Đổi trắc nghiệm sang format có `skill_id`.
- Parse nội dung bằng module dùng chung.
- Thêm nút tải `lesson-import-v1.json`.
- Đưa metadata từ form vào package.
- Thêm `image_manifest`.
- Không nhúng base64 vào JSON.

### P3 — Cập nhật editor Lộ trình

- Thêm nút Import JSON trong tab Khác.
- Parse và validate file trước khi điền form.
- Kiểm tra `subject` với trang đang mở.
- Điền cả metadata và nội dung.
- Ép `is_published = false`.
- Không tự lưu.
- Hiển thị báo cáo lỗi/cảnh báo dễ hiểu.
- Giữ import text cũ làm fallback.

### P4 — Chất lượng và hình ảnh

- Cho prompt bài tập tương tác render ảnh an toàn.
- Hỗ trợ thay marker `HINH_xx` có kiểm soát.
- Mở teacher preview sau import hoặc cung cấp nút xem thử rõ ràng.
- Kiểm tra ảnh còn thiếu trước khi công khai.

### P5 — Điều chỉnh sư phạm

- Cho phép số lượng bài tập linh hoạt theo nội dung ảnh.
- Giữ mức tối thiểu hợp lý thay vì luôn ép đủ 10 câu.
- Duy trì hai vòng tự giải và phản biện.
- Không dùng keyword validator làm căn cứ chính để kết luận vượt lớp.

## 15. Kết luận chung

Ý tưởng “Soạn bài Gemini tạo đúng cấu trúc rồi import vào Lộ trình, giáo viên chủ yếu chèn ảnh” là đúng hướng.

Tuy nhiên, câu “chỉ việc chèn ảnh” chỉ chính xác sau khi hoàn thiện:

- Import/export JSON có version.
- Metadata.
- Ánh xạ kỹ năng–câu hỏi.
- Validator.
- Module parser dùng chung.
- Kiểm tra scope theo lớp.
- Teacher preview.
- Render ảnh trong bài tập tương tác nếu cần.

Mô tả mục tiêu chính xác hơn:

> `soanbaigemini` tạo một gói bài học có cấu trúc, được kiểm định và xuất theo `lesson-import-v1`; giáo viên import gói đó vào trình soạn, chèn ảnh, xem thử rồi mới lưu và công khai.

Đây không phải bài toán xây lại hệ thống. Phần lớn field và payload lưu đã tồn tại. Công việc trọng tâm là chuẩn hóa hợp đồng dữ liệu, dùng chung parser, kiểm tra round-trip và tạo UX import an toàn.

---

## 16. Phản biện bổ sung (vòng 2 — đối chiếu code, 23/06/2026)

Phần này bổ sung sau khi đọc lại toàn bộ mục 1–15 và đối chiếu trực tiếp với `admin-lesson-manager.js`, `soanbaigemini.html`, `lotrinh.js`. Mục tiêu: cập nhật trạng thái thực tế, chỉ ra lỗ hổng chưa được nói đủ, và điều chỉnh thứ tự ưu tiên triển khai.

### 16.1. Những gì đã cải thiện trong code (xác nhận)

Các vấn đề từng được Grok/ChatGPT nêu ở mức “rủi ro” đã có patch cụ thể trong admin:

| Vấn đề | Trạng thái code hiện tại |
|---|---|
| Trắc nghiệm mất khi lưu (bulk trống ghi đè) | `resolveQuestionsForSave()` + guard bulk trống trong `flushBulkEditorsBeforeSave()` |
| Điền khuyết 3/4 cột lệch | `normalizeFillParts()` + heuristic gợi ý vs đáp án |
| Nối ô / sắp xếp bị nhầm | `poolsLookLikeSortOrder()`, `buildDragExercisesFromItems()`, `classifyInteractivePipeLine()`, tách `dragMatch` / `dragSort` trong `parseGeminiLessonSections()` |
| Parser bulk vs item editor lệch | `parseQuestionToItems()` gọi `parseQuestions()` thay vì tự tách cột |

**Kết luận:** Các bug end-to-end phổ biến nhất đã được xử lý ở tầng admin. Tuy nhiên, chưa có fixture tự động chứng minh round-trip — chỉ xác nhận bằng đọc code, chưa phải bằng test.

### 16.2. Phản biện lại mục 9 — cần cập nhật diễn đạt

Mục 9.2 nói các lỗi TN/điền khuyết/nối ô “chưa được chứng minh còn tồn tại” — đúng tại thời điểm viết, nhưng **sau patch `fill-drag-fix1`** nên đổi thành:

> Đã sửa phần lớn ở admin; rủi ro còn lại nằm ở **heuristic** (edge case) và **preview soanbaigemini ≠ import admin**, không phải ở luồng lưu cơ bản.

Heuristic vẫn có thể sai trong các trường hợp:

- Điền khuyết: Gemini ghi gợi ý dài, đáp án ngắn — `normalizeFillParts()` có thể đảo cột.
- Nối ô: hai pool cùng độ dài, nội dung gần giống — `poolsLookLikeSortOrder()` có thể phân loại sai.
- Pipe chứa `|` trong LaTeX/tập hợp — `splitQuestionParts()` vẫn fragile dù đã có normalize.

Đây là lý do JSON typed vẫn cần thiết; patch text không thay thế hợp đồng dữ liệu.

### 16.3. Lỗ hổng mới phát hiện khi đọc code

#### A. `importGeminiLessonRaw()` — thứ tự skills và đếm TN

Trong `importGeminiLessonRaw()`:

1. Section `questions` được điền **trước** section `skills`.
2. Số câu TN trong `alert()` đếm bằng `parseSkills(el('lessonSkills')?.value)` — tức **skills cũ trên form**, chưa phải skills vừa import.
3. `questionItems` parse lại ở cuối hàm **sau** khi skills đã điền — dữ liệu cuối đúng hơn alert.

**Hệ quả:** Giáo viên có thể thấy “trắc nghiệm (0)” trong alert dù import thành công. Không chặn lưu, nhưng gây nhiễu UX và khó debug.

**Đề xuất:** Đổi thứ tự import — `skills` trước `questions` — hoặc parse/count TN sau khi cả hai đã điền.

#### B. Round-trip drag sau import (dòng 2097 → 2116 → 2142)

Luồng hiện tại:

```text
parseDragExercises() → dragItems (object)
→ syncDragToTextarea() (serialize pipe)
→ parseDragToItems() (deserialize lại)
```

Đây là **kiểm tra idempotency bắt buộc**. Nếu serialize/deserialize không đối xứng, import có thể làm biến dạng mapping `0-0,1-2` hoặc đổi mode match ↔ sort. Fixture #7, #8 trong mục 13 phải chạy **ngay trên nhánh hiện tại**, trước khi làm JSON.

#### C. `soanbaigemini.html` vẫn lệch admin — chưa chỉ là “parser cũ hơn”

Khác biệt không chỉ là version parser:

| Khía cạnh | `soanbaigemini.html` | `admin-lesson-manager.js` |
|---|---|---|
| Nối ô vs sắp xếp | Gộp vào `drag` | Tách `dragMatch`, `dragSort`, `dragMixed` |
| Trắc nghiệm | Prompt 6 cột, không `skill_id` | Parser hỗ trợ 7 cột |
| Preview/copy | Section copy riêng từng phần | `importGeminiLessonRaw()` một lần |
| Phản biện 2 vòng | Có trong prompt Gemini | Không chạy lại khi import admin |

**Hệ quả thực tế:** Giáo viên có hai đường vào editor:

- **Đường A (tốt hơn):** Dán raw Gemini → tab Khác → Import — dùng parser admin mới.
- **Đường B (dễ lỗi hơn):** Copy từng section trong soanbaigemini — có thể thiếu `skill_id`, lẫn nối ô/sắp xếp.

Tài liệu và UI nên **khuyến khích Đường A**, đồng thời sửa prompt soanbaigemini cho khớp admin (P2 không đủ muộn — nên làm sớm, xem 16.7).

#### D. Preview giáo viên ≠ giao diện học sinh

`renderPreview()` trong admin chỉ hiển thị **số lượng** (đoạn lý thuyết, số TN, số nối/sắp xếp). Không render như `lotrinh.js`.

Trong khi đó `lotrinh.js`:

- Lý thuyết/ví dụ/bài nộp: `lessonRichText()` — có ảnh Markdown, placeholder `HINH_xx`.
- Tự luận/điền khuyết/TN/nối ô: `mathText()` — **không** parse `![...](url)`.

**Hệ quả:** Giáo viên có thể dán ảnh vào đề tự luận/điền khuyết, preview admin vẫn “ổn”, nhưng học sinh thấy chuỗi Markdown thô. Mục 8.2 đúng hướng nhưng cần nâng mức ưu tiên: đây là blocker cho “chỉ việc chèn ảnh” nếu ảnh nằm trong đề bài tương tác.

#### E. `DANH SÁCH HÌNH ẢNH` chưa nối vào `image_manifest`

Gemini đã có section `DANH SÁCH HÌNH ẢNH CẦN TẠO` / `PROMPT TẠO ẢNH`, nhưng:

- `parseGeminiLessonSections()` dừng ở `stop` — không parse manifest.
- Marker `HINH_xx` trong nội dung và danh sách ảnh ở cuối bài **không được liên kết tự động**.

Khi làm `lesson-import-v1`, nên có bước:

```text
parse DANH SÁCH HÌNH → image_manifest[]
đối chiếu marker trong theory/examples/... → cảnh báo thiếu/không khớp
```

Không nên bắt giáo viên tự ghép manifest bằng tay.

#### F. Chưa có export ngược (bài đã lưu → JSON)

Kế hoạch P1–P3 mô tả soanbaigemini → JSON → admin. Thiếu chiều ngược:

```text
bài đã lưu trong DB → export lesson-import-v1.json → chỉnh sửa → import lại
```

Chiều ngược quan trọng cho: sao chép bài giữa các lớp, backup, chỉnh sửa hàng loạt, và test round-trip thực (fixture #13).

### 16.4. Phản biện schema `lesson-import-v1`

Schema trong mục 11 đủ cho import, nhưng còn thiếu metadata hữu ích:

```json
{
  "generated_at": "2026-06-23T10:00:00+07:00",
  "source": {
    "tool": "soanbaigemini",
    "prompt_version": "2026-06-scope-v2",
    "model": "gemini-..."
  },
  "import_notes": []
}
```

**Lý do:**

- `prompt_version` giúp biết bài cũ có format 6 cột hay 7 cột TN.
- `generated_at` hỗ trợ audit khi giáo viên import bài cũ.
- Không ảnh hưởng payload lưu — adapter bỏ qua khi `save_content`.

Ngoài ra, nên quy định rõ **`slug` sinh tự động** nếu thiếu:

```text
slug = f(subject, chapter, title) → normalize ASCII, tránh trùng
```

Admin đã có `suggestSlug()` khi lưu; import JSON nên tái dùng logic này thay vì bắt giáo viên gõ slug.

### 16.5. Phản biện validator (mục 12) — bổ sung rule

Ngoài rule đã liệt kê, cần thêm:

**Lỗi chặn:**

- `essay_exercises[].answer` rỗng khi bài có chấm tự động.
- `fill_exercises`: `pool` rỗng hoặc `answer` không nằm trong pool (khi một ô).
- `drag_exercises` mode `sort`: `answer` phải là hoán vị của `items` (cùng multiset).
- Trùng `slug` với bài đã publish cùng `subject` (tra API trước import).

**Cảnh báo:**

- `skills[].target` không phải số 0–100.
- Câu TN gán vào cùng một `skill_id` (>80% câu một skill) — có thể do thiếu cột skill.
- Nội dung có `HINH_xx` nhưng `image_manifest` rỗng.
- `order_index` trùng hoặc nhảy bước lớn so với bài cùng chương.

### 16.6. Phạm vi ngoài JSON import (không lẫn)

`global_config.json` đang bật `ai_test_ds2api_only` — chỉ ảnh hưởng **AI Explain** qua `api/ai_router.php`, không ảnh hưởng soanbaigemini hay import bài. Không nên đưa DS2API vào lộ trình P0–P5.

### 16.7. Điều chỉnh thứ tự ưu tiên (đề xuất thay mục 14)

Thứ tự cũ (P0 → P5) đúng về kiến trúc, nhưng **chưa tối ưu cho giáo viên đang dùng ngay**. Đề xuất chèn milestone ngắn:

| Bước | Việc | Lý do |
|---|---|---|
| **P0a** (1–2 ngày) | Sửa thứ tự import skills→questions; đồng bộ prompt soanbaigemini (7 cột TN, heading NỐI Ô / SẮP XẾP tách) | Giảm lỗi ngay, không cần JSON |
| **P0b** | Fixture thủ công 3–5 bài mẫu, test idempotency drag + fill | Xác nhận patch hiện tại |
| **P0** | `lesson-import.js` dùng chung | Nền cho JSON |
| **P1–P3** | Như mục 14 | |
| **P2.5** | `mathText()` hoặc wrapper `practiceRichText()` cho đề có ảnh | Blocker UX ảnh trong bài tập |
| **P4** | Manifest ảnh từ `DANH SÁCH HÌNH` | Giảm việc tay sau import |
| **P5** | Số lượng bài linh hoạt trong prompt | Giảm sáng tác vượt ảnh |

### 16.8. Tiêu chí “xong” rõ ràng hơn

Chưa nên coi JSON import hoàn tất khi chỉ có nút tải/nhập file. Cần đủ:

1. **Round-trip:** Gemini text → package → import form → lưu → API → render học sinh — nội dung không đổi ý nghĩa.
2. **Skill integrity:** Mỗi câu TN có `skill` đúng; bảng kỹ năng học sinh khớp.
3. **Image integrity:** Marker có manifest; ảnh hiển thị đúng ở cả lý thuyết và đề tương tác (sau P2.5).
4. **Scope safety:** Import Toán 6 trên trang Toán 4 → cảnh báo, không lưu nhầm.
5. **No silent save:** Import không gọi API; `is_published` luôn false.

### 16.9. Kết luận vòng 2

Tài liệu mục 1–15 **đúng hướng và đủ chi tiết kiến trúc**. Sau đối chiếu code, ba điểm cần nhấn mạnh thêm:

1. **Patch admin đã xử lý nhiều bug vận hành**, nhưng chưa có test — rủi ro chuyển sang heuristic và lệch soanbaigemini.
2. **`lesson-import.js` đã triển khai** (xem mục 18); giáo viên có text import + JSON import — cần chạy fixture/smoke test thường xuyên.
3. **“Chỉ việc chèn ảnh”** còn xa nếu ảnh nằm trong đề tương tác (renderer) hoặc manifest ảnh chưa tự sinh từ Gemini.

Mô tả mục tiêu sau vòng 2:

> Luồng ổn định = text import tin cậy (admin) + prompt soanbaigemini khớp + fixture xác nhận → sau đó mới bọc bằng `lesson-import-v1` có validate hai lần; giáo viên import, chèn ảnh theo manifest, xem thử **giao diện học sinh**, rồi mới lưu.

---

## 17. Quyết định hiện tại

Ngày cập nhật: 23/06/2026

Mình đồng ý tiếp tục code theo hướng đã chốt trong tài liệu.

**Đã hoàn thành trong đợt triển khai 23/06/2026** (chi tiết mục 18):

1. Luồng text import qua `lesson-import.js` + admin bridge.
2. Đồng bộ `soanbaigemini.html` — TN 7 cột, parser chung, export JSON.
3. Module dùng chung `lesson-import.js` (parser, normalizer, validator).
4. Import/Export JSON `lesson-import-v1` trong admin.

Ưu tiên tiếp theo:

1. Chạy smoke test + round-trip qua API/DB.
2. Gỡ fallback parser cũ trong `soanbaigemini.html`.
3. Lưu `image_manifest` vào DB (nếu cần).
4. P5 — số lượng bài linh hoạt trong prompt.

Nguyên tắc hiện tại:

- Không đi thẳng vào JSON thô.
- Không tự lưu hoặc tự công khai khi import.
- Ưu tiên P0a trước để giảm lỗi ngay cho giáo viên đang dùng.

---

## 18. Nhật ký triển khai code (23/06/2026)

Phần này ghi lại **các file đã sửa/tạo** và **nội dung thay đổi cụ thể** sau khi triển khai theo phản biện mục 16–17 (P0a → P5). Dùng làm đối chiếu khi review hoặc commit.

### 18.1. Tóm tắt trạng thái

| Hạng mục | Trước | Sau (23/06/2026) |
|---|---|---|
| Parser Gemini | Hai bản trong admin + soanbaigemini | Một module `lesson-import.js`, admin/soanbaigemini gọi chung |
| Import JSON | Chưa có | Có: tải/nhập `lesson-import-v1.json`, validate lỗi → chặn |
| Import text | Parser riêng admin | `LI.buildLessonImportPackage()` — skills trước questions |
| Trắc nghiệm bulk | 6 cột (soanbaigemini cũ) | 7 cột: `skill_id \| Câu \| A \| B \| C \| D \| Đáp án` |
| Ảnh trong đề tương tác | `mathText()` — Markdown thô | `practiceRichText()` trong `lotrinh.js` |
| Manifest ảnh | Thủ công | Parse từ `DANH SÁCH HÌNH`, điền form khi load/import |
| Smoke test | Chưa có | `tests/lesson-import-smoke.js` (Node) + `tests/lesson-import-smoke.html` (browser) |
| Cache script | — | `?v=20260623-lesson-import-v2` trên các trang lộ trình + soanbaigemini |

### 18.2. File mới

#### `lesson-import.js`

Module lõi (`window.LessonImport`), IIFE, không phụ thuộc framework.

- **Schema:** `lesson-import-v1`, `PROMPT_VERSION = '2026-06-scope-v3'`
- **Parser Gemini:** `parseGeminiLessonSections()` — tách `dragMatch` / `dragSort` / `dragMixed`, dừng ở `DANH SÁCH HÌNH`
- **Bulk tương tác:** `parseInteractiveBulkPaste()`, `classifyInteractivePipeLine()`, `resolveInteractiveBulkSection()`
- **Ảnh:** `parseImageManifest()`, `extractImageMarkers()`, `collectMarkersFromPackage()`
- **Trắc nghiệm:** `parseQuestions()` (7 cột + `skill_id`), `formatQuestionsBulk()`, `questionsToEditorItems()`
- **Drag:** `parseDragExercises()`, `buildDragExercisesFromItems()`, `poolsLookLikeSortOrder()`, `parseMatchPairs()`
- **Package:** `buildLessonImportPackage()`, `normalizeLessonImportPackage()`, `validateLessonImportPackage()`
- **Adapter:** `packageFromSavePayload()`, `packageToSavePayload()`, `suggestSlugFromMeta()`, `sectionsToEditorTexts()`

#### `tests/fixtures/gemini-raw-sample.txt`

Fixture mẫu Gemini raw (mục tiêu, lý thuyết, tương tác, TN 7 cột, kỹ năng, danh sách hình) — dùng cho smoke test.

#### `tests/lesson-import-smoke.js`

Smoke test Node (`node tests/lesson-import-smoke.js`). Kiểm tra: schema, skills, questions có skill, drag match+sort, fill, essay, image manifest, `is_published === false`, idempotency drag.

#### `tests/lesson-import-smoke.html`

Phiên bản chạy trên browser (fetch fixture, không cần Node). Mở qua local server / Live Server.

### 18.3. File đã sửa

#### `admin-lesson-manager.js`

Thay đổi chính:

1. **Bắt buộc `lesson-import.js`:** load trước admin; thiếu module → `console.error` + `return` sớm (editor không khởi tạo).
2. **Bridge `LI`:** alias toàn bộ parser/formatter từ `window.LessonImport` (không copy logic).
3. **Gỡ parser trùng (~700+ dòng):** xóa bản sao `parseGeminiLessonSections`, `parseInteractiveBulkPaste`, `normalizeBulkHeading`, `classifyInteractivePipeLine`, … — chỉ giữ logic admin-only (UI editor, Drive upload, format ví dụ có `[AI]`, v.v.).
4. **Import text:** `importGeminiLessonRaw()` → `LI.buildLessonImportPackage()` → `applyLessonPackageToForm()`; **skills điền trước questions** (sửa lỗi 16.3.A).
5. **Import/Export JSON:** `importLessonJsonFile()`, `exportLessonJson()` — lỗi validate chặn import; cảnh báo vẫn cho import; **không tự lưu**; `is_published = false`.
6. **`applyLessonPackageToForm()` / `buildFormLessonPackage()`:** điền form từ package; export ngược từ form.
7. **`formatImageManifestText()`:** khi `fillForm()` — quét marker `HINH_xx` trong nội dung bài, ghép với `image_manifest` đã lưu (nếu có).
8. **`suggestSlug()`:** dùng `LI.suggestSlugFromMeta()` thay logic slug cục bộ.
9. **`serializeQuestionsBulkFromItems()`:** xuất **7 cột** có `skill_id`.
10. **`questionsToEditorItems`:** gọi `LI.questionsToEditorItems(questions, skills)`.
11. **`openStudentPreview()`:** preview phong phú hơn — thống kê, kỹ năng, lý thuyết, ví dụ, 2 câu TN mẫu, cảnh báo manifest thiếu.
12. **`renderPreview()`:** cảnh báo ảnh thiếu manifest (không gọi `buildFormLessonPackage()` để tránh loop).
13. **UI tab Khác:** ô `lessonImageManifest`, nút Import JSON, Export JSON, Xem thử học sinh.
14. **`newLesson()`:** xóa sạch ô manifest ảnh.

#### `soanbaigemini.html`

- Load `lesson-import.js` (cache `v2`).
- `parseAndPreview()` ưu tiên `LI.parseGeminiLessonSections()`; format TN qua `LI.formatQuestionsBulk()`.
- Prompt cũ (block comment) cập nhật TN **7 cột**; hướng dẫn cấu trúc đã có 7 cột.
- Nút **Tải lesson-import-v1.json**; gợi ý import raw vào admin tab Khác.
- Vẫn giữ `parseLessonSectionsFromRaw()` làm fallback khi thiếu `LessonImport` (nên Ctrl+F5 nếu preview lệch).

#### `lotrinh.js`

- Thêm `practiceRichText()` — render ảnh Markdown `![...](url)` trong đề bài tương tác (tự luận, điền khuyết, drag, trắc nghiệm).
- Thay `mathText()` bằng `practiceRichText()` tại các vị trí prompt/option bài luyện tập (sửa mục 16.3.D / 8.2).

#### `lotrinhtoan4.html` … `lotrinhtoan9.html` (6 file)

Thứ tự script:

```html
<script src="lesson-import.js?v=20260623-lesson-import-v2"></script>
<script src="lotrinh.js?v=20260623-lesson-import-v2"></script>
<script src="admin-lesson-manager.js?v=20260623-lesson-import-v2"></script>
```

`lesson-import.js` **phải** load trước `admin-lesson-manager.js`.

### 18.4. Luồng end-to-end sau triển khai

```text
Ảnh SGK
→ soanbaigemini (prompt 7 cột TN, heading tách NỐI Ô / SẮP XẾP)
→ Gemini trả raw text
→ Đường A (khuyến khích): Lộ trình tab Khác → Import text
   hoặc Đường B: Tải lesson-import-v1.json → Import JSON
→ lesson-import.js: parse → normalize → validate
→ admin form (is_published = false, manifest ảnh điền sẵn)
→ giáo viên chèn ảnh thật thay HINH_xx
→ Xem thử (preview nhanh) → Lưu bài học
→ học sinh: lotrinh.js + practiceRichText()
```

### 18.5. Việc còn lại (chưa làm trong đợt này)

| Việc | Ghi chú |
|---|---|
| Chạy smoke test trên máy có Node | `node tests/lesson-import-smoke.js` |
| Round-trip đầy đủ qua API + DB | fixture → import → lưu → render học sinh — cần test thủ công |
| Gỡ fallback parser cũ trong `soanbaigemini.html` | Khi chắc chắn mọi trang luôn load `lesson-import.js` |
| `image_manifest` lưu vào DB | Hiện manifest chỉ trên form/export JSON; API `save_content` chưa field riêng |
| Preview học sinh = `lotrinh.js` thật | `openStudentPreview()` vẫn là HTML tĩnh, chưa embed renderer đầy đủ |
| Validator rule nâng cao (mục 16.5) | Một phần đã có trong `validateLessonImportPackage()`; chưa đủ hết |
| Số lượng bài linh hoạt trong prompt (P5) | Prompt vẫn có thể ép số lượng cố định ở block comment cũ |

### 18.6. Cách kiểm tra nhanh

1. **Ctrl+F5** trang `lotrinhtoan6.html` (hoặc lớp tương ứng).
2. Tab **Khác** → dán `tests/fixtures/gemini-raw-sample.txt` → **Import text**.
3. Kiểm tra: kỹ năng có trước TN, bulk TN 7 cột, manifest ảnh, preview cảnh báo.
4. **Export JSON** → **Import JSON** lại — nội dung không mất.
5. Mở `tests/lesson-import-smoke.html` — tất cả dòng **OK**.
