(function () {
    const pageKeys = {
        'lotrinh.html': 'lotrinh',
        'gslides.html': 'gslides',
        'smartquiz.html': 'smartquiz',
        'thitructuyen.html': 'thitructuyen',
        'kttx.html': 'kttx'
    };

    const fileName = window.location.pathname.split('/').pop() || 'index.html';
    const pageKey = pageKeys[fileName];
    const token = localStorage.getItem('authToken');
    const role = localStorage.getItem('userRole');

    if (!token) {
        window.location.href = 'login.html';
        return;
    }

    if (role !== 'student' || !pageKey) return;

    let allowedPages = [];
    try {
        allowedPages = JSON.parse(localStorage.getItem('allowedPages') || '[]');
    } catch {
        allowedPages = [];
    }

    if (!allowedPages.includes(pageKey)) {
        alert('Tài khoản của em chưa được giáo viên mở trang này.');
        window.location.href = allowedPages.includes('lotrinh') ? 'lotrinh.html' : 'login.html';
    }
})();
