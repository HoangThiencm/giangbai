# PLAN: Thiết Kế Tab Chuyên Biệt OLM.vn Trong taobaitap.html Chuẩn 100% File Mẫu OLM

## 1. Yêu Cầu & Bối Cảnh

Dựa trên 4 ảnh mẫu thực tế từ OLM.vn mà người dùng cung cấp:
- Hệ thống OLM yêu cầu cú pháp file Word cực kỳ chặt chẽ:
  + **Phần 1**: `Phần 1. Trắc nghiệm nhiều lựa chọn.` (tiêu đề màu xanh).
  + Câu hỏi: `Câu 1. [NB] ...` (dấu chấm sau số câu, mã mức độ nhận thức).
  + Phương án đúng: `<u>A. Nội dung</u>` hoặc `<u>A.</u> Nội dung`.
  + **Phần 2 (Trắc nghiệm đúng/sai)**:
    - Tiêu đề: `Phần 2. Trắc nghiệm đúng/sai.`
    - **Cú pháp dấu `#` bắt buộc của OLM**:
      * Mệnh đề Đúng: `<u>a)</u> #Nội dung mệnh đề`
      * Mệnh đề Sai: `b) #Nội dung mệnh đề`
  + **Phần 3 (Trả lời ngắn)**: `Phần 3. Trắc nghiệm trả lời ngắn.`, đáp án đặt trong `[[...]]`.
  + Lời giải: Nằm dưới nhãn `[HDG]`.
- Thiết kế riêng **1 Tab / Modal chuyên biệt cho OLM** trên thanh công cụ của `taobaitap.html` tập trung vào **Luyện tập, đề thi**:
  + **Chế độ 1**: Đề thi thông minh OLM (1 file Word chuẩn 100% mẫu OLM ở trên).
  + **Chế độ 2**: Đề thi PDF (Bộ đôi File Đề bài + File Hướng dẫn giải).
  + Xem trước (Preview) theo đúng cấu trúc OLM trước khi tải.

---

## 2. Chi Tiết Thực Hiện Trong `taobaitap.html` Cho Coder

### Bước 1: Cập nhật hàm xuất `exportWordOLM` chuẩn 100% mẫu OLM
Áp dụng đúng cú pháp từ ảnh mẫu:
```javascript
const exportWordOLM = () => {
    const dataToExport = mode === "quiz" ? questions : essays;
    if (!dataToExport || dataToExport.length === 0) {
        showSourceNotice("Chưa có câu hỏi để xuất!");
        return;
    }

    const header = `
    <html xmlns:o='urn:schemas-microsoft-com:office:office' xmlns:w='urn:schemas-microsoft-com:office:word' xmlns='http://www.w3.org/TR/REC-html40'>
    <head>
        <meta charset='utf-8'><title>Đề thi chuẩn OLM.vn</title>
        <style>
            body { font-family: 'Times New Roman', serif; font-size: 12pt; line-height: 1.4; color: #000; }
            p { margin: 3pt 0; text-align: justify; }
            .section-title { color: #0000ff; font-weight: bold; font-size: 13pt; margin-top: 14pt; margin-bottom: 6pt; }
            .q-num { color: #0000ff; font-weight: bold; }
        </style>
    </head><body>`;

    let bodyContent = "";

    const appendExplanation = (q) => {
        if (q.explanation) {
            bodyContent += `<p><b>[HDG]</b></p><p>${q.explanation}</p>`;
        }
    };

    if (mode !== "quiz") {
        dataToExport.forEach((essay, index) => {
            bodyContent += `<p><b class="q-num">Bài ${index + 1}.</b> ${essay.question}</p>`;
            if (essay.solution) bodyContent += `<p><b>[HDG]</b></p><p>${essay.solution}</p>`;
            bodyContent += `<p></p>`;
        });
    } else {
        const { part1, part2, part3 } = collectCv7991ExportParts(dataToExport);
        const useCv7991Sections = synthForm === "cv7991" || part2.length > 0 || part3.length > 0;
        let currentQuestion = 1;

        if (useCv7991Sections) {
            // PHẦN 1: TRẮC NGHIỆM NHIỀU LỰA CHỌN
            if (part1.length > 0) {
                bodyContent += `<p class="section-title"><b>Phần 1. Trắc nghiệm nhiều lựa chọn.</b></p>`;
                part1.forEach((q) => {
                    const levelTag = getOlmLevelTag(q);
                    bodyContent += `<p><b class="q-num">Câu ${currentQuestion}.</b> ${levelTag}${q.question}</p>`;
                    (q.options || []).slice(0, 4).forEach((opt, oIdx) => {
                        const letter = String.fromCharCode(65 + oIdx);
                        const cleanOpt = cleanOptionText(opt);
                        if (q.correctAnswerIndex === oIdx) {
                            bodyContent += `<p><b class="q-num"><u>${letter}.</u></b> ${cleanOpt}</p>`;
                        } else {
                            bodyContent += `<p><b class="q-num">${letter}.</b> ${cleanOpt}</p>`;
                        }
                    });
                    appendExplanation(q);
                    bodyContent += `<p></p>`;
                    currentQuestion++;
                });
            }

            // PHẦN 2: TRẮC NGHIỆM ĐÚNG/SAI (CHUẨN OLM CÓ DẤU #)
            if (part2.length > 0) {
                bodyContent += `<p class="section-title"><b>Phần 2. Trắc nghiệm đúng/sai.</b></p>`;
                part2.forEach((q) => {
                    const levelTag = getOlmLevelTag(q);
                    bodyContent += `<p><b class="q-num">Câu ${currentQuestion}.</b> ${levelTag}${q.question}</p>`;
                    if (isCv7991TrueFalseItem(q)) {
                        getCv7991TrueFalseItems(q).forEach((item, sIdx) => {
                            const label = String.fromCharCode(97 + sIdx);
                            // Đúng: <u>a)</u> #Nội dung | Sai: b) #Nội dung
                            if (item.isCorrect) {
                                bodyContent += `<p><b class="q-num"><u>${label})</u></b> #${item.text}</p>`;
                            } else {
                                bodyContent += `<p><b class="q-num">${label})</b> #${item.text}</p>`;
                            }
                        });
                    } else {
                        const isTrue = q.correctAnswerIndex === 0;
                        bodyContent += isTrue
                            ? `<p><b class="q-num"><u>a)</u></b> #Mệnh đề trên là đúng</p><p><b class="q-num">b)</b> #Mệnh đề trên là sai</p>`
                            : `<p><b class="q-num">a)</b> #Mệnh đề trên là đúng</p><p><b class="q-num"><u>b)</u></b> #Mệnh đề trên là sai</p>`;
                    }
                    appendExplanation(q);
                    bodyContent += `<p></p>`;
                    currentQuestion++;
                });
            }

            // PHẦN 3: TRẮC NGHIỆM TRẢ LỜI NGẮN
            if (part3.length > 0) {
                bodyContent += `<p class="section-title"><b>Phần 3. Trắc nghiệm trả lời ngắn.</b></p>`;
                part3.forEach((q) => {
                    const levelTag = getOlmLevelTag(q);
                    const ans = q.correctAnswer || (q.correctMatches ? formatQuizAnswer(q) : "");
                    bodyContent += `<p><b class="q-num">Câu ${currentQuestion}.</b> ${levelTag}${q.question} [[${ans}]]</p>`;
                    appendExplanation(q);
                    bodyContent += `<p></p>`;
                    currentQuestion++;
                });
            }
        } else {
            // Mặc định duyệt lần lượt
            dataToExport.forEach((q, index) => {
                const num = index + 1;
                const levelTag = getOlmLevelTag(q);
                if (q.type === "true-false") {
                    bodyContent += `<p><b class="q-num">Câu ${num}.</b> ${levelTag}${q.question}</p>`;
                    if (isCv7991TrueFalseItem(q)) {
                        getCv7991TrueFalseItems(q).forEach((item, sIdx) => {
                            const label = String.fromCharCode(97 + sIdx);
                            if (item.isCorrect) {
                                bodyContent += `<p><b class="q-num"><u>${label})</u></b> #${item.text}</p>`;
                            } else {
                                bodyContent += `<p><b class="q-num">${label})</b> #${item.text}</p>`;
                            }
                        });
                    } else {
                        const isTrue = q.correctAnswerIndex === 0;
                        bodyContent += isTrue
                            ? `<p><b class="q-num"><u>a)</u></b> #Đúng</p><p><b class="q-num">b)</b> #Sai</p>`
                            : `<p><b class="q-num">a)</b> #Đúng</p><p><b class="q-num"><u>b)</u></b> #Sai</p>`;
                    }
                } else if (q.type === "short-answer" || q.type === "fill-blank") {
                    const ans = q.correctAnswer || "";
                    bodyContent += `<p><b class="q-num">Câu ${num}.</b> ${levelTag}${q.question} [[${ans}]]</p>`;
                } else {
                    bodyContent += `<p><b class="q-num">Câu ${num}.</b> ${levelTag}${q.question}</p>`;
                    (q.options || []).slice(0, 4).forEach((opt, oIdx) => {
                        const letter = String.fromCharCode(65 + oIdx);
                        const cleanOpt = cleanOptionText(opt);
                        if (q.correctAnswerIndex === oIdx) {
                            bodyContent += `<p><b class="q-num"><u>${letter}.</u></b> ${cleanOpt}</p>`;
                        } else {
                            bodyContent += `<p><b class="q-num">${letter}.</b> ${cleanOpt}</p>`;
                        }
                    });
                }
                appendExplanation(q);
                bodyContent += `<p></p>`;
            });
        }
    }

    try {
        saveDocxFromHtml(header + bodyContent + "</body></html>", "De_Thi_OLM.docx");
        showSourceNotice("Đã xuất file Word chuẩn OLM.vn thành công!");
    } catch (error) {
        showSourceNotice(`Lỗi khi xuất Word OLM: ${error.message}`);
    }
};
```

### Bước 2: Thêm Modal/Tab chuyên biệt "Học liệu OLM.vn" (`showOlmModal`)
Thêm state:
```javascript
const [showOlmModal, setShowOlmModal] = useState(false);
```

Và giao diện Modal trực quan:
- Tiêu đề: **Học liệu OLM.vn (Luyện tập & Đề thi)**.
- Gồm 2 thẻ lựa chọn rõ ràng:
  1. **Thẻ 1: Luyện tập, đề thi (Đề thông minh OLM)**:
     - Mô tả: Dùng cho mục "Luyện tập, đề thi" trên OLM. Tải 1 file `.docx` duy nhất có đầy đủ câu hỏi, đáp án đúng gạch chân, cú pháp `<u>a)</u> #...` và lời giải `[HDG]`. OLM tự động đảo đề, xáo phương án và lưu ngân hàng câu hỏi.
     - Nút: **Tải file Word thông minh (OLM)** (`exportWordOLM`).
  2. **Thẻ 2: Đề thi PDF (Bộ đôi Đề bài & Hướng dẫn giải)**:
     - Mô tả: Dùng cho mục "Đề thi trắc nghiệm từ file PDF hoặc Word" trên OLM. Tải cùng lúc 2 file: 1 file Đề bài sạch (không đáp án) up vào tab Đề bài, 1 file Lời giải chi tiết up vào tab Hướng dẫn giải.
     - Nút: **Tải bộ đôi Đề & Giải PDF** (`exportOlmPdfPair`).

### Bước 3: Nút mở Modal OLM trên Toolbar
Tại toolbar xuất bài tập, đặt nút nổi bật:
```jsx
<button onClick={() => setShowOlmModal(true)} className="px-3.5 py-2 bg-amber-600 hover:bg-amber-700 text-white rounded-lg font-bold text-sm transition flex items-center gap-1.5 shadow-sm" title="Mở trung tâm xuất học liệu chuyên biệt cho OLM.vn">
    <i className="fas fa-graduation-cap text-amber-200"></i> Học liệu OLM
</button>
```

---

## 3. Kiểm Thử (Verification)
1. Cập nhật `tests/taobaitap-olm-export-smoke.js`:
   - Xác nhận có `showOlmModal`, nút `Học liệu OLM`.
   - Xác nhận `exportWordOLM` áp dụng cú pháp OLM chính thức với `#` (`#${item.text}`) và `<u>${label})</u>`.
   - Xác nhận cả 2 hướng Đề thông minh và Bộ đôi PDF đều hoạt động trơn tru.
2. Chạy test:
   ```powershell
   node tests/taobaitap-olm-export-smoke.js
   ```
