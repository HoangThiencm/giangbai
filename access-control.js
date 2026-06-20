(function () {
    const pageKeys = {
        'lotrinh.html': 'lotrinh',
        'lotrinhtoan4.html': 'lotrinhtoan4',
        'lotrinhtoan6.html': 'lotrinhtoan6',
        'lotrinhtoan7.html': 'lotrinhtoan7',
        'lotrinhtoan8.html': 'lotrinhtoan8',
        'lotrinhtoan9.html': 'lotrinhtoan9',
        'thongketientrinh.html': 'thongketientrinh',
        'gslides.html': 'gslides',
        'smartquiz.html': 'smartquiz',
        'thitructuyen.html': 'thitructuyen',
        'kttx.html': 'kttx'
    };
    const pageUrls = {
        lotrinh: 'lotrinhtoan6.html',
        lotrinhtoan4: 'lotrinhtoan4.html',
        lotrinhtoan6: 'lotrinhtoan6.html',
        lotrinhtoan7: 'lotrinhtoan7.html',
        lotrinhtoan8: 'lotrinhtoan8.html',
        lotrinhtoan9: 'lotrinhtoan9.html',
        thongketientrinh: 'thongketientrinh.html',
        gslides: 'gslides.html',
        smartquiz: 'smartquiz.html',
        thitructuyen: 'thitructuyen.html',
        kttx: 'kttx.html'
    };
    const lotrinhPageKeys = new Set(['lotrinh', 'lotrinhtoan4', 'lotrinhtoan6', 'lotrinhtoan7', 'lotrinhtoan8', 'lotrinhtoan9']);

    const fileName = window.location.pathname.split('/').pop() || 'index.html';
    const pageKey = pageKeys[fileName];
    const params = new URLSearchParams(window.location.search);
    const isOpenExamLink = pageKey === 'thitructuyen' && params.get('mode') === 'student' && !!params.get('examId');
    const token = localStorage.getItem('authToken');
    const role = localStorage.getItem('userRole');

    if (isOpenExamLink) {
        return;
    }

    if (!token) {
        window.location.href = 'login.html';
        return;
    }

    function getAllowedPages() {
        try {
            return JSON.parse(localStorage.getItem('allowedPages') || '[]');
        } catch {
            return [];
        }
    }

    function canOpenPage(pageKeyValue, allowedPages) {
        return allowedPages.includes(pageKeyValue)
            || (pageKeyValue === 'lotrinhtoan6' && allowedPages.includes('lotrinh'));
    }

    function hasLotrinhScope(allowedPages) {
        return allowedPages.some(page => lotrinhPageKeys.has(page));
    }

    function firstAllowedLotrinhUrl(allowedPages) {
        return allowedPages
            .filter(page => lotrinhPageKeys.has(page))
            .map(page => pageUrls[page])
            .find(Boolean);
    }

    if (!pageKey) {
        return;
    }

    if (role === 'student') {
        const allowedPages = getAllowedPages();
        if (pageKey === 'thongketientrinh') {
            alert('Trang thống kê chỉ dành cho giáo viên.');
            const fallback = allowedPages.map(page => pageUrls[page]).find(Boolean);
            window.location.href = fallback || 'login.html';
            return;
        }
        if (!canOpenPage(pageKey, allowedPages)) {
            alert('Tài khoản của em chưa được giáo viên mở trang này.');
            const fallback = allowedPages.map(page => pageUrls[page]).find(Boolean);
            window.location.href = fallback || 'login.html';
        }
        return;
    }

    if (role === 'teacher' && pageKey === 'thongketientrinh') {
        const allowedPages = getAllowedPages();
        if (!hasLotrinhScope(allowedPages)) {
            alert('Tài khoản chưa được admin mở lộ trình nào để theo dõi tiến độ.');
            window.location.href = 'index.html';
        }
        return;
    }

    if (role === 'teacher' && lotrinhPageKeys.has(pageKey)) {
        const allowedPages = getAllowedPages();
        if (!canOpenPage(pageKey, allowedPages)) {
            alert('Tài khoản chưa được admin mở lộ trình này để soạn bài.');
            window.location.href = firstAllowedLotrinhUrl(allowedPages) || 'index.html';
        }
    }
})();