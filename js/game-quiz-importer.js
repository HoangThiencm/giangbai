/**
 * GameQuizImporter - Bộ công cụ đọc và bóc tách câu hỏi từ Word (.docx) và văn bản có công thức toán LaTeX
 * Phục vụ cho tất cả các Game Giáo Dục trong GiangBai Pro.
 */
(function (global) {
    'use strict';

    function normalizeQuizText(text) {
        return String(text || '')
            .replace(/\r\n/g, '\n')
            .replace(/\r/g, '\n')
            .replace(/\u00a0/g, ' ')
            .replace(/[\u201C\u201D]/g, '"')
            .replace(/[\u2018\u2019]/g, "'")
            .replace(/\t/g, ' ')
            .replace(/[ ]+\n/g, '\n')
            .replace(/\n{3,}/g, '\n\n')
            .trim();
    }

    function extractAnswerTable(text) {
        const answerMap = {};
        // Tìm phần bảng đáp án ở cuối văn bản
        const answerSectionMatch = text.match(/(?:^|\n)\s*(?:bảng\s*đáp\s*án|đáp\s*án|dap\s*an|answer\s*key|answers?)\s*[:：]?\s*([\s\S]*)$/i);
        if (!answerSectionMatch) return answerMap;

        const answerSection = answerSectionMatch[1];
        // Nhận diện các cặp: 1.A, 1-A, 1:A, 1A, Câu 1: A...
        const pairRegex = /(?:câu\s*)?(\d{1,3})\s*[\.\)\-:]?\s*([A-D])\b/gi;
        let match;
        while ((match = pairRegex.exec(answerSection)) !== null) {
            const num = parseInt(match[1], 10);
            if (!answerMap[num]) {
                answerMap[num] = match[2].toUpperCase();
            }
        }
        return answerMap;
    }

    function stripAnswerTable(text) {
        const answerSectionMatch = text.match(/(?:^|\n)\s*(?:bảng\s*đáp\s*án|dap\s*an|answer\s*key|answers?)\s*[:：]?\s*([\s\S]*)$/i);
        if (!answerSectionMatch) return text;

        const section = answerSectionMatch[1];
        const count = (section.match(/(?:câu\s*)?\d{1,3}\s*[\.\)\-:]?\s*[A-D]\b/gi) || []).length;
        // Nếu phần sau có từ 2 cặp đáp án trở lên thì xem như đây là bảng đáp án cuối bài
        if (count >= 2) {
            return text.slice(0, answerSectionMatch.index).trim();
        }
        return text;
    }

    function parseQuizQuestions(rawText) {
        const normalized = normalizeQuizText(rawText);
        const answerTable = extractAnswerTable(normalized);
        const text = stripAnswerTable(normalized);

        // Regex nhận diện bắt đầu câu hỏi: Câu 1, Câu 1., Câu 1:, Bài 1, Question 1, 1., 1/, [Câu 1]
        const questionRegex = /(?:^|\n)\s*(?:\[?\s*(?:Câu|Cau|Question|Q|Bài|Bai)\s*(\d{1,3})\s*\]?|(\d{1,3}))\s*[\.\):：\/-]\s*/gi;
        const questionMatches = [];
        let match;

        while ((match = questionRegex.exec(text)) !== null) {
            const num = parseInt(match[1] || match[2], 10);
            questionMatches.push({
                number: num,
                bodyStart: questionRegex.lastIndex,
                markerStart: match.index,
            });
        }

        if (!questionMatches.length) {
            // Thử phân tách theo từng khối nếu không có số thứ tự câu
            return fallbackParseBlocks(text);
        }

        const questions = [];

        for (let i = 0; i < questionMatches.length; i++) {
            const cur = questionMatches[i];
            const next = questionMatches[i + 1];
            let block = text.slice(cur.bodyStart, next ? next.markerStart : text.length).trim();

            // Tìm giải thích/lời giải nếu có
            let explanation = '';
            const expMatch = block.match(/(?:^|\n)\s*(?:hướng\s*dẫn\s*giải|lời\s*giải|giải\s*thích|explanation|loi\s*giai)\s*[:：]\s*([\s\S]*)$/i);
            if (expMatch) {
                explanation = expMatch[1].trim();
                block = block.slice(0, expMatch.index).trim();
            }

            // Tìm đáp án inline nếu có
            let inlineAnswer = '';
            const inlineMatch = block.match(/(?:^|\n|\s{2,})\s*(?:đáp\s*án|dap\s*an|answer|key|đ\/a)\s*[:：]\s*([A-D])\b/i);
            if (inlineMatch) {
                inlineAnswer = inlineMatch[1].toUpperCase();
                block = block.replace(/(?:^|\n|\s{2,})\s*(?:đáp\s*án|dap\s*an|answer|key|đ\/a)\s*[:：]\s*[A-D]\b/i, '').trim();
            }

            // Tìm các lựa chọn A, B, C, D (hỗ trợ cả xuống dòng và inline trên 1 dòng)
            const optionRegex = /(?:^|\n|\s{2,}|\t)\s*([A-D])\s*[\.\):：-]\s*/gi;
            const optionMatches = [];
            let optMatch;

            while ((optMatch = optionRegex.exec(block)) !== null) {
                optionMatches.push({
                    letter: optMatch[1].toUpperCase(),
                    markerStart: optMatch.index,
                    bodyStart: optionRegex.lastIndex,
                });
            }

            if (optionMatches.length < 2) {
                // Không tìm thấy đủ phương án trắc nghiệm A-D
                continue;
            }

            // Lấy nội dung câu hỏi (phần trước lựa chọn đầu tiên)
            const prompt = block.slice(0, optionMatches[0].markerStart).trim() || `Câu hỏi ${cur.number}`;

            // Bóc tách nội dung từng lựa chọn A, B, C, D
            const optionsByLetter = {};
            for (let j = 0; j < optionMatches.length; j++) {
                const optCur = optionMatches[j];
                const optNext = optionMatches[j + 1];
                const optEnd = optNext ? optNext.markerStart : block.length;
                optionsByLetter[optCur.letter] = block.slice(optCur.bodyStart, optEnd).trim();
            }

            const choices = ['A', 'B', 'C', 'D'].map((letter) => optionsByLetter[letter] || '');
            const finalAnswerLetter = inlineAnswer || answerTable[cur.number] || (optionMatches[0]?.letter || 'A');
            const answerIndex = Math.max(0, ['A', 'B', 'C', 'D'].indexOf(finalAnswerLetter));

            questions.push({
                id: `q${questions.length + 1}`,
                number: cur.number,
                type: 'mcq',
                prompt: prompt,
                choices: choices,
                answer: answerIndex >= 0 ? answerIndex : 0,
                explanation: explanation,
            });
        }

        return questions;
    }

    function fallbackParseBlocks(text) {
        // Dự phòng: cố gắng tìm các đoạn có A. B. C. D.
        const lines = text.split(/\n{2,}/);
        const questions = [];
        lines.forEach((block, idx) => {
            const optionRegex = /(?:^|\n|\s{2,}|\t)\s*([A-D])\s*[\.\):：-]\s*/gi;
            const optionMatches = [];
            let optMatch;
            while ((optMatch = optionRegex.exec(block)) !== null) {
                optionMatches.push({
                    letter: optMatch[1].toUpperCase(),
                    markerStart: optMatch.index,
                    bodyStart: optionRegex.lastIndex,
                });
            }
            if (optionMatches.length >= 2) {
                const prompt = block.slice(0, optionMatches[0].markerStart).trim() || `Câu hỏi ${idx + 1}`;
                const optionsByLetter = {};
                for (let j = 0; j < optionMatches.length; j++) {
                    const optCur = optionMatches[j];
                    const optNext = optionMatches[j + 1];
                    const optEnd = optNext ? optNext.markerStart : block.length;
                    optionsByLetter[optCur.letter] = block.slice(optCur.bodyStart, optEnd).trim();
                }
                const choices = ['A', 'B', 'C', 'D'].map((letter) => optionsByLetter[letter] || '');
                questions.push({
                    id: `q${questions.length + 1}`,
                    number: idx + 1,
                    type: 'mcq',
                    prompt: prompt,
                    choices: choices,
                    answer: 0,
                    explanation: '',
                });
            }
        });
        return questions;
    }

    function parseMatchingPairs(rawText) {
        const text = normalizeQuizText(rawText);
        const lines = text.split('\n').map((l) => l.trim()).filter(Boolean);
        const pairs = [];
        const chips = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';

        for (let i = 0; i < lines.length; i++) {
            const line = lines[i].replace(/^(?:Cặp|Cap|\d+)\s*[\.\):：-]\s*/i, '');
            // Dấu phân tách giữa vế trái và vế phải: " - ", " : ", " | ", " -> ", " => "
            const parts = line.split(/\s*(?:[-–—|]|->|=>|:)\s*/);
            if (parts.length >= 2) {
                pairs.push({
                    id: pairs.length + 1,
                    left: parts[0].trim(),
                    right: parts.slice(1).join(' - ').trim(),
                    chip: chips[pairs.length % chips.length],
                    explanation: '',
                });
            }
        }

        // Nếu người dùng dán đề trắc nghiệm thông thường thì chuyển câu hỏi thành left, đáp án đúng thành right
        if (pairs.length === 0) {
            const mcq = parseQuizQuestions(rawText);
            mcq.forEach((q, idx) => {
                const correctChoice = q.choices[q.answer] || q.choices[0] || '';
                pairs.push({
                    id: idx + 1,
                    left: q.prompt,
                    right: correctChoice,
                    chip: chips[idx % chips.length],
                    explanation: q.explanation || '',
                });
            });
        }

        return pairs;
    }

    async function extractTextFromDocx(file) {
        if (!file) throw new Error('Chưa chọn file.');
        if (typeof window !== 'undefined' && !window.mammoth) {
            throw new Error('Chưa tải được thư viện Mammoth để đọc file Word (.docx). Hãy kiểm tra kết nối mạng.');
        }
        const arrayBuffer = await file.arrayBuffer();
        const result = await window.mammoth.extractRawText({ arrayBuffer });
        return (result?.value || '').trim();
    }

    async function extractTextFromFile(file) {
        const name = (file?.name || '').toLowerCase();
        if (name.endsWith('.docx')) {
            return extractTextFromDocx(file);
        }
        if (name.endsWith('.txt')) {
            return (await file.text()).trim();
        }
        throw new Error('Vui lòng chọn file Word (.docx) hoặc file văn bản (.txt).');
    }

    function formatForGame(parsedQuestions, gameType, options = {}) {
        const topic = options.topic || 'Câu hỏi từ Word/LaTeX';
        const numQ = parsedQuestions.length;

        switch (gameType) {
            case 'matching': {
                const pairs = Array.isArray(options.rawPairs) && options.rawPairs.length
                    ? options.rawPairs
                    : parsedQuestions.map((q, idx) => ({
                        id: idx + 1,
                        left: q.prompt,
                        right: q.choices[q.answer] || q.choices[0] || '',
                        chip: String.fromCharCode(65 + (idx % 26)),
                        explanation: q.explanation || '',
                    }));
                return {
                    topicTitle: topic,
                    codewordHint: options.codewordHint || 'Ghép đúng các cặp khái niệm và công thức',
                    pairs: pairs,
                };
            }

            case 'unlock': {
                const questions = parsedQuestions.map((q, idx) => ({
                    id: `lock${idx + 1}`,
                    type: 'mcq',
                    prompt: q.prompt,
                    choices: q.choices,
                    answer: q.answer,
                    hint1: q.explanation ? `Gợi ý: ${q.explanation}` : 'Hãy chú ý công thức và định nghĩa cốt lõi.',
                    hint2: 'Quan sát kỹ các đáp án.',
                    explanation: q.explanation || '',
                }));
                return {
                    codeWord: options.codeWord || 'KIENTHUC',
                    knowledgeCard: {
                        title: topic || 'Mở Khóa Kiến Thức',
                        summary: 'Bạn đã mở khóa thành công toàn bộ từ khóa bí mật!',
                    },
                    questions,
                };
            }

            case 'tower': {
                const questions = parsedQuestions.map((q, idx) => {
                    const level = Math.min(10, Math.max(1, Math.round(((idx + 1) / Math.max(1, numQ)) * 10)));
                    const diff = level <= 3 ? 'easy' : level <= 7 ? 'medium' : 'hard';
                    return {
                        id: `level${idx + 1}`,
                        level: level,
                        difficulty: diff,
                        type: 'mcq',
                        prompt: q.prompt,
                        choices: q.choices,
                        answer: q.answer,
                        explanation: q.explanation || '',
                    };
                });
                return { questions };
            }

            case 'teambattle': {
                const questions = parsedQuestions.map((q, idx) => ({
                    id: `q${idx + 1}`,
                    type: 'mcq',
                    prompt: q.prompt,
                    choices: q.choices,
                    answer: q.answer,
                    individual: idx % 2 === 0,
                    value: (idx % 3 + 1) * 10,
                    isSpecial: idx % 4 === 3,
                    explanation: q.explanation || '',
                }));
                return { questions };
            }

            case 'treasure': {
                return {
                    raceTitle: topic,
                    questions: parsedQuestions.map((q, idx) => ({
                        id: `q${idx + 1}`,
                        type: 'mcq',
                        prompt: q.prompt,
                        choices: q.choices,
                        answer: q.answer,
                        explanation: q.explanation || '',
                    })),
                };
            }

            case 'escape':
            case 'elimination':
            case 'speedscore':
            default: {
                return {
                    questions: parsedQuestions.map((q, idx) => ({
                        id: `q${idx + 1}`,
                        type: 'mcq',
                        prompt: q.prompt,
                        choices: q.choices,
                        answer: q.answer,
                        explanation: q.explanation || '',
                    })),
                };
            }
        }
    }

    const GameQuizImporter = {
        normalizeQuizText,
        extractAnswerTable,
        stripAnswerTable,
        parseQuizQuestions,
        parseMatchingPairs,
        extractTextFromDocx,
        extractTextFromFile,
        formatForGame,
    };

    if (typeof module !== 'undefined' && module.exports) {
        module.exports = GameQuizImporter;
    }
    if (typeof global !== 'undefined') {
        global.GameQuizImporter = GameQuizImporter;
    }
})(typeof window !== 'undefined' ? window : globalThis);
