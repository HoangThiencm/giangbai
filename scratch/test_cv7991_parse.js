const sampleCv7991 = `
PHẦN I. Câu trắc nghiệm nhiều phương án lựa chọn. Thí sinh trả lời từ câu 1 đến câu 2.
Câu 1. Trong các số sau, số nào là số nguyên tố?
A. 4
B. 6
C. 7
D. 9
Đáp án: C

Câu 2. Tập hợp các ước của 6 là:
A. {1; 2; 3; 6}
B. {1; 2; 3}
C. {2; 3; 6}
D. {1; 6}
Đáp án: A

PHẦN II. Câu trắc nghiệm đúng sai. Thí sinh trả lời câu 3.
Câu 3. Cho tam giác ABC vuông tại A có AB = 6, AC = 8.
a) Độ dài cạnh BC bằng 10.
b) Diện tích tam giác ABC bằng 48.
c) Đường cao AH có độ dài bằng 4.8.
d) Bán kính đường tròn ngoại tiếp bằng 5.
Đáp án: a-Đ, b-S, c-Đ, d-Đ

PHẦN III. Câu trắc nghiệm trả lời ngắn. Thí sinh trả lời câu 4.
Câu 4. Cho hình vuông ABCD có chu vi bằng 20cm. Tính diện tích hình vuông ABCD theo cm2.
Đáp án: 25
`;

const normalizeImportedQuizText = (text) => {

    return String(text || "")
        .replace(/\r/g, "\n")
        .replace(/\u00a0/g, " ")
        .replace(/[“”]/g, '"')
        .replace(/[‘’]/g, "'")
        .replace(/\t/g, " ")
        .replace(/[ ]+\n/g, "\n")
        .replace(/\n{3,}/g, "\n\n")
        .trim();
};

const parseLatexWordQuizEnhanced = (rawText) => {
    const normalized = normalizeImportedQuizText(rawText);
    const questionRegex = /(?:^|\n)\s*(?:Câu|Cau|Question|Q)\s*(\d{1,3})\s*[\.\):：-]\s*/gi;
    const questionMatches = [];
    let questionMatch;

    while ((questionMatch = questionRegex.exec(normalized)) !== null) {
        questionMatches.push({
            number: parseInt(questionMatch[1], 10),
            bodyStart: questionRegex.lastIndex,
            markerStart: questionMatch.index
        });
    }

    if (!questionMatches.length) return [];

    return questionMatches.map((item, index) => {
        const next = questionMatches[index + 1];
        let block = normalized.slice(item.bodyStart, next ? next.markerStart : normalized.length).trim();

        // 1. Kiểm tra xem có inline answer
        const inlineAnswerMatch = block.match(/(?:^|\n)\s*(?:đáp\s*án|dap\s*an|answer)\s*[:：]\s*([^\n]+)/i);
        let inlineAnswer = "";
        if (inlineAnswerMatch) {
            inlineAnswer = inlineAnswerMatch[1].trim();
            block = block.slice(0, inlineAnswerMatch.index).trim();
        }

        // 2. Thử bắt các lựa chọn A, B, C, D (In hoa -> Multiple Choice)
        const optionRegexMC = /(?:^|\n)\s*([A-D])\s*[\.\):：-]\s*/g;
        const mcMatches = [];
        let mcMatch;
        while ((mcMatch = optionRegexMC.exec(block)) !== null) {
            mcMatches.push({
                letter: mcMatch[1].toUpperCase(),
                markerStart: mcMatch.index,
                bodyStart: optionRegexMC.lastIndex
            });
        }

        // 3. Thử bắt các ý a, b, c, d (Chữ thường -> True / False)
        const optionRegexTF = /(?:^|\n)\s*([a-d])\s*[\.\):：-]\s*/g;
        const tfMatches = [];
        let tfMatch;
        while ((tfMatch = optionRegexTF.exec(block)) !== null) {
            tfMatches.push({
                letter: tfMatch[1].toLowerCase(),
                markerStart: tfMatch.index,
                bodyStart: optionRegexTF.lastIndex
            });
        }

        // PHÂN LOẠI DẠNG CÂU HỎI:
        // A. Đúng/Sai (TF): Có từ 2 ý a, b, c, d trở lên HOẶC câu dẫn chứa "đúng sai" HOẶC đáp án chứa Đ/S
        const isTF = (tfMatches.length >= 2 && mcMatches.length < 2) || /đúng\s*[-/]?\s*sai/i.test(inlineAnswer);
        if (isTF && tfMatches.length >= 2) {
            const question = block.slice(0, tfMatches[0].markerStart).trim();
            const options = ["a", "b", "c", "d"].map((letter, i) => {
                const cur = tfMatches.find(m => m.letter === letter);
                if (!cur) return "";
                const curIdx = tfMatches.indexOf(cur);
                const nextMarker = tfMatches[curIdx + 1]?.markerStart ?? block.length;
                return block.slice(cur.bodyStart, nextMarker).trim();
            });

            // Parse đáp án đúng sai từ inlineAnswer (vd: "a-Đ, b-S, c-Đ, d-Đ" hoặc "a. Đ, b. S" hoặc "Đ, S, Đ, S")
            const correctAnswers = [true, false, false, false];
            if (inlineAnswer) {
                ["a", "b", "c", "d"].forEach((letter, idx) => {
                    const re = new RegExp(`${letter}\\s*[:：\\-\\.]?\\s*(đ|s|đúng|sai|t|f|true|false)`, 'i');
                    const m = inlineAnswer.match(re);
                    if (m) {
                        correctAnswers[idx] = /đ|đúng|t|true/i.test(m[1]);
                    }
                });
                // Nếu định dạng chỉ là list "Đ, S, Đ, S"
                if (!/[a-d]\s*[:：\\-\\.]/i.test(inlineAnswer)) {
                    const dsList = inlineAnswer.match(/\b(Đ|S|Đúng|Sai|True|False|T|F)\b/gi);
                    if (dsList && dsList.length >= 2) {
                        dsList.slice(0, 4).forEach((ans, idx) => {
                            correctAnswers[idx] = /đ|đúng|t|true/i.test(ans);
                        });
                    }
                }
            }

            return {
                id: Date.now() + Math.random(),
                type: "tf",
                question: question || `Câu ${item.number}`,
                options,
                correct_answers: correctAnswers,
                question_image: null
            };
        }

        // B. Trắc nghiệm nhiều lựa chọn (MC): Có các lựa chọn A, B, C, D
        if (mcMatches.length >= 2) {
            const question = block.slice(0, mcMatches[0].markerStart).trim();
            const optionsByLetter = {};
            mcMatches.forEach((option, optionIndex) => {
                const optionEnd = mcMatches[optionIndex + 1]?.markerStart ?? block.length;
                optionsByLetter[option.letter] = block.slice(option.bodyStart, optionEnd).trim();
            });
            const options = ["A", "B", "C", "D"].map(letter => optionsByLetter[letter] || "");
            const ansLetterMatch = inlineAnswer.match(/\b([A-D])\b/i);
            const answerLetter = ansLetterMatch ? ansLetterMatch[1].toUpperCase() : "";
            const correctIndex = "ABCD".indexOf(answerLetter);

            return {
                id: Date.now() + Math.random(),
                type: "mc",
                question: question || `Câu ${item.number}`,
                options,
                correct_index: correctIndex >= 0 ? correctIndex : 0,
                question_image: null
            };
        }

        // C. Trả lời ngắn (Short Answer): Không có lựa chọn A-D hay a-d, có đáp án dạng text/số
        return {
            id: Date.now() + Math.random(),
            type: "short_answer",
            question: block || `Câu ${item.number}`,
            options: [],
            correct_answer: inlineAnswer || "",
            question_image: null
        };
    }).filter(Boolean);
};

const results = parseLatexWordQuizEnhanced(sampleCv7991);
console.log('Parsed total questions:', results.length);
results.forEach((q, idx) => {
    console.log(`Q${idx+1} [Type: ${q.type}]: ${q.question.slice(0, 40)}...`);
    if (q.type === 'mc') console.log('   Options:', q.options, 'Correct:', q.correct_index);
    if (q.type === 'tf') console.log('   Sub-items:', q.options, 'Correct:', q.correct_answers);
    if (q.type === 'short_answer') console.log('   Correct Answer:', q.correct_answer);
});

