# PLAN: Tích Hợp Trọn Vẹn Cả 2 Hướng Upload Lên OLM.vn Trong taobaitap.html

## 1. Mục Tiêu & Hai Hướng Đáp Ứng

Giáo viên trên OLM.vn sử dụng 2 kịch bản tạo bài tập khác nhau:

* **Hướng 1: Đề thi thông minh (1 file duy nhất)**:
  - Nút: **`Xuất Word (OLM)`** (Đã tạo xong và pass test).
  - Tải về: `De_Thi_OLM.docx` chứa câu hỏi + đáp án gạch chân `<u>` + `[TF]` + `[[...]]` + `[HDG]`.
  - Tự động trộn câu hỏi, xáo đáp án và lưu ngân hàng câu hỏi.

* **Hướng 2: Bộ đôi file Đề thi PDF (2 file riêng biệt như ảnh chụp thực tế)**:
  - Nút: **`Bộ đôi OLM (Đề & Giải PDF)`**.
  - Tải tự động 2 file riêng rẽ:
    1. **`De_Bai_OLM_PDF.docx`**: Chỉ gồm câu hỏi và phương án A, B, C, D (tuyệt đối không gạch chân, không lộ đáp án hay lời giải) để giáo viên upload vào tab **"Đề bài"**.
    2. **`Huong_Dan_Giai_OLM_PDF.docx`**: Gồm bảng đáp án tổng hợp và lời giải chi tiết từng câu để giáo viên upload vào tab **"Hướng dẫn giải"** (xóa bỏ thông báo *"Giáo viên chưa up hướng dẫn giải..."* trên OLM).

---

## 2. Chi Tiết Thực Hiện Trong `taobaitap.html`

### Bước 1: Thêm hàm xuất bộ đôi `exportOlmPdfPair`
Vị trí: sau hàm `exportWordOLM` (khoảng dòng 16430):
```javascript
            const exportOlmPdfPair = () => {
                const dataToExport = mode === "quiz" ? questions : essays;
                if (!dataToExport || dataToExport.length === 0) {
                    showSourceNotice("Chưa có câu hỏi để xuất!");
                    return;
                }

                const docHeader = (title) => `
                <html xmlns:o='urn:schemas-microsoft-com:office:office' xmlns:w='urn:schemas-microsoft-com:office:word' xmlns='http://www.w3.org/TR/REC-html40'>
                <head>
                    <meta charset='utf-8'><title>${title}</title>
                    <style>
                        body { font-family: 'Times New Roman', serif; font-size: 12pt; line-height: 1.4; color: #000; }
                        h1 { text-align: center; font-size: 15pt; font-weight: bold; margin-bottom: 4px; text-transform: uppercase; }
                        .sub-title { text-align: center; font-style: italic; font-size: 11pt; margin-bottom: 18px; }
                        .section-title { font-weight: bold; font-size: 12.5pt; text-transform: uppercase; margin-top: 14pt; margin-bottom: 4pt; }
                        .question-block { margin-bottom: 12pt; text-align: justify; }
                        .option { margin: 2pt 0 2pt 18pt; }
                        .tf-item { margin-left: 20pt; margin-top: 2pt; margin-bottom: 2pt; }
                        .ans-key { margin-top: 20px; border-top: 1px solid #000; padding-top: 10px; }
                        .solution-box { margin-top: 6pt; margin-bottom: 14pt; padding: 8pt; background: #f9f9f9; border-left: 3px solid #0284c7; }
                    </style>
                </head><body>`;

                // 1. FILE ĐỀ BÀI (KHÔNG LỘ ĐÁP ÁN / LỜI GIẢI)
                let examBody = `<h1>PHIẾU ĐỀ BÀI ÔN TẬP / KIỂM TRA</h1>`;
                examBody += `<div class="sub-title">Thời gian làm bài: 45 phút - Thí sinh chọn đáp án vào phiếu trả lời</div>`;

                if (mode !== "quiz") {
                    dataToExport.forEach((essay, idx) => {
                        examBody += `<div class="question-block"><b>Bài ${idx + 1}:</b> ${essay.question}</div>`;
                    });
                } else {
                    const { part1, part2, part3 } = collectCv7991ExportParts(dataToExport);
                    let qNum = 1;
                    if (synthForm === "cv7991" || (part2.length > 0 || part3.length > 0)) {
                        if (part1.length > 0) {
                            examBody += `<div class="section-title">PHẦN I. CÂU TRẮC NGHIỆM NHIỀU PHƯƠNG ÁN LỰA CHỌN</div>`;
                            part1.forEach((q) => {
                                examBody += `<div class="question-block"><b>Câu ${qNum++}:</b> ${q.question}<br/>`;
                                (q.options || []).slice(0, 4).forEach((opt, oIdx) => {
                                    const letter = String.fromCharCode(65 + oIdx);
                                    examBody += `<div class="option">${letter}. ${cleanOptionText(opt)}</div>`;
                                });
                                examBody += `</div>`;
                            });
                        }
                        if (part2.length > 0) {
                            examBody += `<div class="section-title">PHẦN II. CÂU TRẮC NGHIỆM ĐÚNG SAI</div>`;
                            part2.forEach((q) => {
                                examBody += `<div class="question-block"><b>Câu ${qNum++}:</b> ${q.question}<br/>`;
                                if (isCv7991TrueFalseItem(q)) {
                                    getCv7991TrueFalseItems(q).forEach((item, sIdx) => {
                                        const label = String.fromCharCode(97 + sIdx);
                                        examBody += `<div class="tf-item">${label}) ${item.text}</div>`;
                                    });
                                } else {
                                    examBody += `<div class="tf-item">a) Mệnh đề trên là Đúng</div><div class="tf-item">b) Mệnh đề trên là Sai</div>`;
                                }
                                examBody += `</div>`;
                            });
                        }
                        if (part3.length > 0) {
                            examBody += `<div class="section-title">PHẦN III. CÂU TRẮC NGHIỆM TRẢ LỜI NGẮN</div>`;
                            part3.forEach((q) => {
                                examBody += `<div class="question-block"><b>Câu ${qNum++}:</b> ${q.question}<br/><i>(Ghi kết quả vào phiếu trả lời)</i></div>`;
                            });
                        }
                    } else {
                        dataToExport.forEach((q, idx) => {
                            examBody += `<div class="question-block"><b>Câu ${idx + 1}:</b> ${q.question}<br/>`;
                            if (q.type === "true-false") {
                                if (isCv7991TrueFalseItem(q)) {
                                    getCv7991TrueFalseItems(q).forEach((item, sIdx) => {
                                        examBody += `<div class="tf-item">${String.fromCharCode(97 + sIdx)}) ${item.text}</div>`;
                                    });
                                } else {
                                    examBody += `<div class="tf-item">a) Đúng</div><div class="tf-item">b) Sai</div>`;
                                }
                            } else if (q.type === "short-answer" || q.type === "fill-blank") {
                                examBody += `<i>(Ghi kết quả vào ô trả lời)</i>`;
                            } else {
                                (q.options || []).slice(0, 4).forEach((opt, oIdx) => {
                                    examBody += `<div class="option">${String.fromCharCode(65 + oIdx)}. ${cleanOptionText(opt)}</div>`;
                                });
                            }
                            examBody += `</div>`;
                        });
                    }
                }

                // 2. FILE HƯỚNG DẪN GIẢI CHI TIẾT
                let solBody = `<h1>HƯỚNG DẪN GIẢI CHI TIẾT & ĐÁP ÁN</h1>`;
                solBody += `<div class="sub-title">Tài liệu hướng dẫn giải chi tiết cho đề ôn tập OLM</div>`;

                if (mode !== "quiz") {
                    dataToExport.forEach((essay, idx) => {
                        solBody += `<div class="question-block"><b>Bài ${idx + 1}:</b> ${essay.question}</div>`;
                        solBody += `<div class="solution-box"><b>Lời giải chi tiết:</b><br/>${essay.solution || "Đang cập nhật..."}</div>`;
                    });
                } else {
                    const { part1, part2, part3 } = collectCv7991ExportParts(dataToExport);
                    let qNum = 1;
                    const allNumbered = [];

                    const renderSolItem = (q, num) => {
                        solBody += `<div class="question-block"><b>Câu ${num}:</b> ${q.question}</div>`;
                        let ansText = "";
                        if (q.type === "true-false") {
                            if (isCv7991TrueFalseItem(q)) {
                                const details = getCv7991TrueFalseItems(q).map((it, i) => `${String.fromCharCode(97 + i)}) ${it.isCorrect ? "Đúng" : "Sai"}`).join(", ");
                                ansText = `<b>Đáp án:</b> ${details}`;
                            } else {
                                ansText = `<b>Đáp án:</b> ${q.correctAnswerIndex === 0 ? "Đúng" : "Sai"}`;
                            }
                        } else if (q.type === "short-answer" || q.type === "fill-blank") {
                            ansText = `<b>Đáp án:</b> ${q.correctAnswer || (q.correctMatches ? formatQuizAnswer(q) : "")}`;
                        } else {
                            const letter = String.fromCharCode(65 + (q.correctAnswerIndex >= 0 ? q.correctAnswerIndex : 0));
                            const text = cleanOptionText(q.options?.[q.correctAnswerIndex] || "");
                            ansText = `<b>Đáp án đúng:</b> ${letter}. ${text}`;
                        }
                        solBody += `<div style="margin-left: 10pt; font-weight: bold; color: #0284c7;">${ansText}</div>`;
                        if (q.explanation) {
                            solBody += `<div class="solution-box"><b>Lời giải chi tiết:</b><br/>${q.explanation}</div>`;
                        }
                        solBody += `<div style="height: 8pt;"></div>`;
                    };

                    if (synthForm === "cv7991" || (part2.length > 0 || part3.length > 0)) {
                        part1.forEach((q) => { allNumbered.push({ num: qNum, q }); renderSolItem(q, qNum++); });
                        part2.forEach((q) => { allNumbered.push({ num: qNum, q }); renderSolItem(q, qNum++); });
                        part3.forEach((q) => { allNumbered.push({ num: qNum, q }); renderSolItem(q, qNum++); });
                    } else {
                        dataToExport.forEach((q, idx) => {
                            allNumbered.push({ num: idx + 1, q });
                            renderSolItem(q, idx + 1);
                        });
                    }

                    // Thêm bảng tóm tắt đáp án ở đầu hoặc cuối
                    const key = buildCv7991AnswerKey(allNumbered);
                    solBody += `
                    <div class="ans-key">
                        <h2 style="font-size: 13pt; text-transform: uppercase;">BẢNG TỔNG HỢP ĐÁP ÁN NHANH</h2>
                        ${key.mcLine ? `<p><b>Phần I:</b> ${key.mcLine}</p>` : ""}
                        ${key.tfLines.map(l => `<p>${l}</p>`).join("")}
                        ${key.saLine ? `<p><b>Phần III:</b> ${key.saLine}</p>` : ""}
                    </div>`;
                }

                // Xuất file 1: Đề bài
                saveDocxFromHtml(docHeader("Phiếu đề bài") + examBody + "</body></html>", "De_Bai_OLM_PDF.docx");

                // Xuất file 2: Hướng dẫn giải (delay nhẹ 400ms để trình duyệt tải liên tục 2 file)
                setTimeout(() => {
                    saveDocxFromHtml(docHeader("Hướng dẫn giải chi tiết") + solBody + "</body></html>", "Huong_Dan_Giai_OLM_PDF.docx");
                    showSourceNotice("Đã xuất trọn bộ đôi: 1 File Đề bài + 1 File Hướng dẫn giải OLM!");
                }, 400);
            };
```

### Bước 2: Thêm nút giao diện trên thanh công cụ
Tại dòng 17042 (cạnh nút `Xuất Word (OLM)`):
```jsx
<button onClick={exportOlmPdfPair} className="px-3.5 py-2 bg-sky-600 hover:bg-sky-700 text-white rounded-lg font-bold text-sm transition flex items-center gap-1.5 shadow-sm" title="Xuất cùng lúc 2 file riêng: 1 file Đề bài và 1 file Lời giải để upload vào dạng Đề thi PDF trên OLM">
    <i className="fas fa-copy text-sky-200"></i> Bộ đôi OLM (Đề & Giải PDF)
</button>
```

---

## 3. Kiểm Thử (Verification)
1. Cập nhật `tests/taobaitap-olm-export-smoke.js`:
   - Kiểm tra có cả `exportWordOLM` (Hướng 1: Đề thông minh) và `exportOlmPdfPair` (Hướng 2: Bộ đôi PDF).
   - Kiểm tra tên file xuất: `De_Thi_OLM.docx`, `De_Bai_OLM_PDF.docx`, `Huong_Dan_Giai_OLM_PDF.docx`.
2. Chạy test:
   ```powershell
   node tests/taobaitap-olm-export-smoke.js
   ```
