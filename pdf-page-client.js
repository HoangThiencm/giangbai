/**
 * Tách PDF thành ảnh từng trang — chạy hoàn toàn trên trình duyệt (pdf.js).
 */
(function (global) {
    function requirePdfJs() {
        const lib = global.pdfjsLib;
        if (!lib) throw new Error('Chưa tải pdf.js. Thêm thư viện pdf.js vào trang.');
        return lib;
    }

    async function splitPdfArrayBuffer(arrayBuffer, options) {
        const opts = options || {};
        const scale = opts.scale || 1.5;
        const mime = opts.mime || 'image/jpeg';
        const quality = opts.quality == null ? 0.82 : opts.quality;
        const pdfjsLib = requirePdfJs();
        const pdf = await pdfjsLib.getDocument({ data: arrayBuffer }).promise;
        const pages = [];

        for (let i = 1; i <= pdf.numPages; i++) {
            const page = await pdf.getPage(i);
            const viewport = page.getViewport({ scale });
            const canvas = document.createElement('canvas');
            canvas.width = Math.max(1, Math.round(viewport.width));
            canvas.height = Math.max(1, Math.round(viewport.height));
            const ctx = canvas.getContext('2d');
            if (!ctx) throw new Error('Canvas không khả dụng.');
            await page.render({ canvasContext: ctx, viewport }).promise;
            const imageData = mime === 'image/png'
                ? canvas.toDataURL('image/png')
                : canvas.toDataURL('image/jpeg', quality);
            pages.push({
                id: `pdf-${Date.now()}-${i}-${Math.random().toString(36).slice(2, 7)}`,
                page_index: i,
                image_data: imageData,
                status: 'pending',
                q_count: 0,
            });
        }
        return pages;
    }

    async function splitPdfFile(file, options) {
        if (!file) throw new Error('Thiếu file PDF.');
        const buf = await file.arrayBuffer();
        return splitPdfArrayBuffer(buf, options);
    }

    global.PdfPageClient = { splitPdfFile, splitPdfArrayBuffer };
})(window);