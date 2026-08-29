/** Static smoke test: PDF scan OCR + tạo bài tập tổng hợp từ file (taobaitap). Node 18+. */
'use strict';

const fs = require('fs');
const path = require('path');

const root = path.join(__dirname, '..');
const files = {
    root: path.join(root, 'taobaitap.html'),
    backup: path.join(root, 'backupcode viettailieu', 'taobaitap.html')
};

function failCount(checks) {
    let failed = 0;
    for (const [name, ok] of checks) {
        console[ok ? 'log' : 'error']((ok ? 'OK: ' : 'FAIL: ') + name);
        if (!ok) failed += 1;
    }
    return failed;
}

function compactPdfNeedsOcr(text) {
    return String(text || '').replace(/\s+/g, '').length < 50;
}

function checksFor(label, html) {
    return [
        [`${label}: chọn PDF/Word/ảnh vào nguồn kiến thức`, /accept="\.pdf,\.docx,\.png,\.jpg,\.jpeg,\.webp"/.test(html)],
        [`${label}: pdfjs đọc text layer`, /pdfjsLib\.getDocument[\s\S]*getTextContent\(/.test(html)],
        [`${label}: OCR khi PDF text dưới 50 ký tự`, html.includes("extractedText.replace(/\\s+/g, '').length >= 50") && html.includes('readDocumentSourceWithOcrFallback')],
        [`${label}: render trang PDF thành ảnh JPEG`, /const renderPdfPagesToImageItems[\s\S]*canvas\.toBlob[\s\S]*image\/jpeg/.test(html)],
        [`${label}: OCR qua extractSourceTextFromImageBatch`, /const ocrText = await extractSourceTextFromImageBatch\(imageItems/.test(html)],
        [`${label}: handleFileUpload dùng OCR fallback`, /const handleFileUpload[\s\S]*readDocumentSourceWithOcrFallback\(file/.test(html)],
        [`${label}: tiến trình đọc PDF scan`, /PDF scan: đang chuyển trang/.test(html)],
        [`${label}: hàm generateSynthesizedFromSource`, /const generateSynthesizedFromSource = async \(\) =>/.test(html)],
        [`${label}: không bắt buộc nhập chủ đề khi tổng hợp từ file`, /KHÔNG cần danh sách chủ đề/.test(html)],
        [`${label}: bám sát 100% học liệu`, /bám sát 100%/.test(html)],
        [`${label}: normalizeQuizItems sau khi sinh tổng hợp`, /const generateSynthesizedFromSource[\s\S]*normalizeQuizItems\(parsedData\)/.test(html)],
        [`${label}: chuyển Bước 2 sau khi sinh tổng hợp`, /const generateSynthesizedFromSource[\s\S]*setStep\(2\)/.test(html)],
        [`${label}: card tạo bài tập tổng hợp`, /Tạo bài tập tổng hợp từ file đã nạp/.test(html) && /border-violet-300/.test(html)],
        [`${label}: nút TẠO BÀI TẬP TỔNG HỢP TỪ FILE`, html.includes('⚡ TẠO BÀI TẬP TỔNG HỢP TỪ FILE')],
        [`${label}: số câu 5/10/15/20`, html.includes('5 câu') && html.includes('10 câu') && html.includes('15 câu') && html.includes('20 câu')],
        [`${label}: tùy chỉnh số câu`, /title="Tùy chỉnh số câu"/.test(html) && /type="number"/.test(html)],
        [`${label}: hình thức trắc nghiệm tổng hợp và tự luận`, html.includes('mixed-quiz') && html.includes('Trắc nghiệm tổng hợp') && html.includes('Tự luận có lời giải')],
        [`${label}: mức độ Cơ bản/Trung bình/Nâng cao/Hỗn hợp`, html.includes('"Cơ bản"') && html.includes('"Trung bình"') && html.includes('"Nâng cao"') && html.includes('"Hỗn hợp"')],
        [`${label}: phân hóa 4 mức độ trong prompt`, /Nhận biết, Thông hiểu, Vận dụng, Vận dụng thực tế/.test(html)],
        [`${label}: generateContent vẫn yêu cầu tên chủ đề`, /const emptyTopics = topicsToGenerate\.filter\(t => !t\.name\.trim\(\)\)/.test(html)],
        [`${label}: giữ xuất Word`, /const exportWord = \(\) =>/.test(html) && html.includes('De_Thi_Tong_Hop.docx')],
        [`${label}: giữ DẠY NGAY`, html.includes('DẠY NGAY') && /const startPresentation/.test(html)]
    ];
}

let failed = 0;
for (const [label, filePath] of Object.entries(files)) {
    if (!fs.existsSync(filePath)) {
        console.error(`FAIL: missing ${label} file ${filePath}`);
        failed += 1;
        continue;
    }
    const html = fs.readFileSync(filePath, 'utf8');
    failed += failCount(checksFor(label, html));
}

const logicChecks = [
    ['ngưỡng OCR: PDF rỗng cần OCR', compactPdfNeedsOcr('') === true],
    ['ngưỡng OCR: PDF scan 20 ký tự cần OCR', compactPdfNeedsOcr('   abcd efgh   ') === true],
    ['ngưỡng OCR: PDF đủ 50 ký tự không OCR', compactPdfNeedsOcr('x'.repeat(50)) === false],
    ['ngưỡng OCR: khoảng trắng không tính vào 50 ký tự', compactPdfNeedsOcr(`${'x'.repeat(49)}     `) === true]
];
failed += failCount(logicChecks);

if (failed) {
    console.error(`FAILED ${failed} check(s)`);
    process.exit(1);
}
console.log('ALL taobaitap plan smoke checks passed.');
process.exit(0);
