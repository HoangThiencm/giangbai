'use strict';

const assert = require('assert');
const fs = require('fs');
const path = require('path');

const root = path.join(__dirname, '..');
const app = fs.readFileSync(path.join(root, 'js', 'khbd-app.js'), 'utf8');

assert.match(app, /async function analyzeCanvasTextbookSafely/, 'Canvas phải có luồng phân tích SGK riêng');
assert.match(app, /CANVAS_TEXTBOOK_BATCH_SIZE\s*=\s*1/, 'Canvas phải gửi một trang/ảnh cho mỗi lô an toàn');
assert.match(app, /timeoutMs:\s*105000/, 'Canvas phải gửi timeout rõ ràng cho phân tích cấu trúc SGK');
assert.match(app, /prepareCanvasTextbookAnalysisBatches/, 'Canvas phải gom ảnh/PDF đã chọn theo lô');
assert.match(app, /selectedPages: pages/, 'Canvas phải tôn trọng các trang PDF đã chọn');
assert.match(app, /fact extraction/, 'Prompt Canvas phải trích xuất từng trường ngắn, không chép nguyên trang');
assert.match(app, /nguyên văn 100%/, 'Prompt Canvas phải giữ nguyên văn tên đề mục và đề bài');
assert.match(app, /TUYỆT ĐỐI KHÔNG điền chỗ trống bằng trí nhớ/, 'Prompt Canvas phải cấm AI điền SGK theo trí nhớ');
assert.match(app, /Không suy đoán tên đề mục, số mục, số câu, số bài tập hoặc nội dung bài tập/, 'Prompt Canvas phải cấm suy đoán chỉ mục và nội dung bài tập');
assert.match(app, /cần đối chiếu SGK/, 'Thông tin SGK không chắc chắn phải được đánh dấu cần đối chiếu');
assert.match(app, /function sanitizeTextbookSeriesBranding/, 'Phải có bộ lọc tên thương mại SGK dùng chung');
assert.match(app, /Kết\\s\*Nối\\s\*Tri\\s\*Thức/, 'Bộ lọc phải chặn Kết nối tri thức');
assert.match(app, /Cánh\\s\*Diều/, 'Bộ lọc phải chặn Cánh diều');
assert.match(app, /Chân\\s\*Trời\\s\*Sáng\\s\*Tạo/, 'Bộ lọc phải chặn Chân trời sáng tạo');
assert.match(app, /Global\\s\*Success/, 'Bộ lọc phải chặn Global Success');
assert.match(app, /\\?"sections\\?"/, 'Schema Canvas phải có đề mục sections');
assert.match(app, /\\?"exercises\\?"/, 'Schema Canvas phải có danh sách bài tập exercises');
assert.match(app, /\\?"coreKnowledge\\?"/, 'Schema Canvas phải có kiến thức cốt lõi');
assert.match(app, /\\?"activities\\?"/, 'Schema Canvas phải có hoạt động con');
assert.match(app, /subsectionProfiles: canvasRoute \? canvasAnalysis\?\.subsections : null/, 'Hồ sơ Canvas phải được chuyển sang ngữ cảnh giáo án');
assert.match(app, /appState\.textbookSubsectionProfiles = Array\.isArray\(subsectionProfiles\)/, 'Hồ sơ Canvas phải được giữ để phân bổ thời lượng');
assert.match(app.match(/function canvasTextbookAnalysisPrompt[\s\S]*?function parseCanvasTextbookAnalysis/)?.[0] || '', /không chép nguyên trang/, 'Prompt Canvas không được yêu cầu chép nguyên trang');
assert.match(app, /if \(canvasRoute\) \{[\s\S]{0,900}analyzeCanvasTextbookSafely/, 'Canvas phải dùng tuyến hệ thống phân tích thay cho OCR');
assert.match(app, /applyTextbookOcrResult\(ocrText/, 'Kết quả Canvas phải đi vào context/ocrReady hiện có');
assert.match(app, /Gemini không thể phân tích tệp này[\s\S]*không tự gửi lại yêu cầu/, 'RECITATION Canvas phải hướng dẫn, không tự gửi lại');
assert.match(app, /if \(!canvasRoute && canUseMistralOcr\(\)\)/, 'Luồng không phải Canvas vẫn ưu tiên Mistral');
assert.match(app, /extractTextbookOcrTextWithGemini/, 'Fallback Gemini cũ vẫn dành cho luồng không phải Canvas');

console.log('canvas textbook analysis smoke: passed');
