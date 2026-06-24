(async function () {
    const pageKeys = {
        'lotrinh.html': 'lotrinh',
        'lotrinhtoan4.html': 'lotrinhtoan4',
        'lotrinhtoan5.html': 'lotrinhtoan5',
        'lotrinhtoan6.html': 'lotrinhtoan6',
        'lotrinhtoan7.html': 'lotrinhtoan7',
        'lotrinhtoan8.html': 'lotrinhtoan8',
        'lotrinhtoan9.html': 'lotrinhtoan9',
        'thongketientrinh.html': 'thongketientrinh',
        'quanlyvanban.html': 'quanlyvanban',
        'quanlyvanban-hanhchinh.html': 'quanlyvanban',
        'quanlyvanban-dang.html': 'quanlyvanban',
        'theodoi-ai.html': 'theodoiai',
        'gslides.html': 'gslides',
        'vehinh.html': 'vehinh',
        'smartquiz.html': 'smartquiz',
        'matrande.html': 'matrande',
        'tronde.html': 'tronde',
        'thitructuyen.html': 'thitructuyen',
        'kttx.html': 'kttx',
        'nopbai-quanly.html': 'nopbai',
        'padlet_ht.html': 'padlet',
        'vietbaocao.html': 'vietbaocao',
        'rutgon.html': 'rutgon'
    };
    const pageUrls = {
        lotrinh: 'lotrinhtoan6.html',
        lotrinhtoan4: 'lotrinhtoan4.html',
        lotrinhtoan5: 'lotrinhtoan5.html',
        lotrinhtoan6: 'lotrinhtoan6.html',
        lotrinhtoan7: 'lotrinhtoan7.html',
        lotrinhtoan8: 'lotrinhtoan8.html',
        lotrinhtoan9: 'lotrinhtoan9.html',
        thongketientrinh: 'thongketientrinh.html',
        quanlyvanban: 'quanlyvanban.html',
        theodoiai: 'theodoi-ai.html',
        gslides: 'gslides.html',
        vehinh: 'vehinh.html',
        smartquiz: 'smartquiz.html',
        matrande: 'matrande.html',
        tronde: 'tronde.html',
        thitructuyen: 'thitructuyen.html',
        kttx: 'kttx.html',
        nopbai: 'nopbai-quanly.html',
        padlet: 'padlet_ht.html',
        vietbaocao: 'vietbaocao.html',
        rutgon: 'rutgon.html'
    };
    const lotrinhPageKeys = new Set(['lotrinh', 'lotrinhtoan4', 'lotrinhtoan5', 'lotrinhtoan6', 'lotrinhtoan7', 'lotrinhtoan8', 'lotrinhtoan9']);
    const lotrinhRouteOrder = ['lotrinhtoan4', 'lotrinhtoan5', 'lotrinhtoan6', 'lotrinhtoan7', 'lotrinhtoan8', 'lotrinhtoan9'];

    const fileName = window.location.pathname.split('/').pop() || 'index.html';
    const pageKey = pageKeys[fileName];
    const params = new URLSearchParams(window.location.search);
    const isOpenExamLink = pageKey === 'thitructuyen' && params.get('mode') === 'student' && !!params.get('examId');
    const token = localStorage.getItem('authToken');

    if (isOpenExamLink) {
        return;
    }

    if (!token) {
        window.location.href = 'login.html';
        return;
    }

    function clearLocalAuth() {
        localStorage.removeItem('authToken');
        localStorage.removeItem('userEmail');
        localStorage.removeItem('userName');
        localStorage.removeItem('userRole');
        localStorage.removeItem('allowedPages');
        localStorage.removeItem('userClassName');
    }

    function redirectToLogin() {
        clearLocalAuth();
        window.location.replace('login.html');
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
        for (const page of lotrinhRouteOrder) {
            if (canOpenPage(page, allowedPages) && pageUrls[page]) {
                return pageUrls[page];
            }
        }
        return null;
    }

    function firstAllowedPageUrl(allowedPages) {
        return firstAllowedLotrinhUrl(allowedPages)
            || allowedPages.map(page => pageUrls[page]).find(Boolean)
            || null;
    }

    async function refreshSessionPages() {
        try {
            const res = await fetch('api/me.php', { cache: 'no-store', credentials: 'include' });
            if (res.status === 401) {
                redirectToLogin();
                return [];
            }
            if (!res.ok) return getAllowedPages();
            const data = await res.json();
            const user = data.user || {};
            const pages = Array.isArray(user.allowed_pages) ? user.allowed_pages : getAllowedPages();
            localStorage.setItem('allowedPages', JSON.stringify(pages));
            if (user.role) localStorage.setItem('userRole', user.role);
            if (user.full_name) localStorage.setItem('userName', user.full_name);
            if (user.username) localStorage.setItem('userEmail', user.username);
            if (user.class_name !== undefined) localStorage.setItem('userClassName', user.class_name || '');
            return pages;
        } catch {
            return getAllowedPages();
        }
    }

    if (!pageKey) {
        return;
    }

    function mergedFeaturesForUser(cfg) {
        const globalFeatures = cfg.features || {};
        const account = localStorage.getItem('userEmail') || '';
        const userFeatures = account && cfg.user_features?.[account] ? cfg.user_features[account] : {};
        return { ...globalFeatures, ...userFeatures };
    }

    async function refreshTeacherTabFlags() {
        try {
            const cacheKey = 'global_config_cache_v1';
            const cached = sessionStorage.getItem(cacheKey);
            if (cached) {
                const parsed = JSON.parse(cached);
                if (parsed?.expiresAt > Date.now() && parsed?.cfg) {
                    const features = mergedFeaturesForUser(parsed.cfg);
                    localStorage.setItem('teacher_design_enabled', features.teacher_design !== false ? '1' : '0');
                    localStorage.setItem('teacher_progress_stats_enabled', features.teacher_progress_stats !== false ? '1' : '0');
                    localStorage.setItem('teacher_ai_stats_enabled', features.teacher_ai_stats !== false ? '1' : '0');
                    return;
                }
            }
            const res = await fetch('global_config.json', { cache: 'no-store' });
            if (!res.ok) return;
            const cfg = await res.json();
            sessionStorage.setItem(cacheKey, JSON.stringify({ cfg, expiresAt: Date.now() + 120000 }));
            const features = mergedFeaturesForUser(cfg);
            localStorage.setItem('teacher_design_enabled', features.teacher_design !== false ? '1' : '0');
            localStorage.setItem('teacher_progress_stats_enabled', features.teacher_progress_stats !== false ? '1' : '0');
            localStorage.setItem('teacher_ai_stats_enabled', features.teacher_ai_stats !== false ? '1' : '0');
        } catch {}
    }

    const [allowedPages] = await Promise.all([
        refreshSessionPages(),
        refreshTeacherTabFlags()
    ]);
    const role = localStorage.getItem('userRole');

    function teacherTabEnabled(flagKey) {
        return localStorage.getItem(flagKey) !== '0';
    }

    if (role === 'student') {
        if (pageKey === 'thongketientrinh' || pageKey === 'theodoiai' || pageKey === 'rutgon' || pageKey === 'quanlyvanban') {
            const msg = pageKey === 'rutgon'
                ? 'Trang rút gọn link chỉ dành cho giáo viên.'
                : (pageKey === 'theodoiai' ? 'Trang theo dõi AI chỉ dành cho giáo viên.' : (pageKey === 'quanlyvanban' ? 'Trang quản lý văn bản chỉ dành cho giáo viên.' : 'Trang thống kê chỉ dành cho giáo viên.'));
            alert(msg);
            window.location.href = firstAllowedPageUrl(allowedPages) || 'login.html';
            return;
        }

        if (!canOpenPage(pageKey, allowedPages)) {
            if (lotrinhPageKeys.has(pageKey)) {
                const lotrinhFallback = firstAllowedLotrinhUrl(allowedPages);
                if (lotrinhFallback && lotrinhFallback !== fileName) {
                    window.location.replace(lotrinhFallback);
                    return;
                }
            }

            const fallback = firstAllowedPageUrl(allowedPages);
            alert('Tài khoản của em chưa được giáo viên mở trang này. Vui lòng liên hệ giáo viên để được mở đúng lộ trình.');
            window.location.href = fallback || 'login.html';
        }
        return;
    }

    if (role === 'teacher' && pageKey === 'thongketientrinh') {
        if (!teacherTabEnabled('teacher_progress_stats_enabled')) {
            alert('Admin đã tắt tab Thống kê tiến trình cho giáo viên.');
            window.location.href = 'index.html';
            return;
        }
        if (!canOpenPage('thongketientrinh', allowedPages)) {
            alert('Tài khoản chưa được admin cấp quyền Thống kê tiến trình.');
            window.location.href = 'index.html';
        }
        return;
    }

    if (role === 'teacher' && pageKey === 'theodoiai') {
        if (!teacherTabEnabled('teacher_ai_stats_enabled')) {
            alert('Admin đã tắt tab Theo dõi AI cho giáo viên.');
            window.location.href = 'index.html';
            return;
        }
        if (!canOpenPage('theodoiai', allowedPages)) {
            alert('Tài khoản chưa được admin cấp quyền xem Theo dõi AI.');
            window.location.href = 'index.html';
        }
        return;
    }

    if (role === 'teacher' && pageKey === 'rutgon') {
        if (!canOpenPage('rutgon', allowedPages)) {
            alert('Tài khoản chưa được admin cấp quyền Link rút gọn & QR.');
            window.location.href = 'index.html';
        }
        return;
    }

    const teacherWorkspaceTools = ['gslides', 'vehinh', 'smartquiz', 'matrande', 'tronde', 'thitructuyen', 'kttx', 'nopbai', 'padlet', 'vietbaocao'];
    if (role === 'teacher' && teacherWorkspaceTools.includes(pageKey)) {
        if (!canOpenPage(pageKey, allowedPages)) {
            alert('Tài khoản chưa được admin cấp quyền mở công cụ này.');
            window.location.href = 'index.html';
        }
        return;
    }

    if (role === 'teacher' && pageKey === 'quanlyvanban') {
        if (!canOpenPage('quanlyvanban', allowedPages)) {
            alert('Tài khoản chưa được admin cấp quyền Quản lý văn bản.');
            window.location.href = 'index.html';
        }
        return;
    }

    if (role === 'teacher' && lotrinhPageKeys.has(pageKey)) {
        if (!teacherTabEnabled('teacher_design_enabled')) {
            alert('Admin đã tắt tab Soạn bài lộ trình cho giáo viên.');
            window.location.href = 'index.html';
            return;
        }
        if (!canOpenPage(pageKey, allowedPages)) {
            const fallback = firstAllowedLotrinhUrl(allowedPages);
            if (fallback && fallback !== fileName) {
                window.location.replace(fallback);
                return;
            }
            alert('Tài khoản chưa được admin mở lộ trình này để soạn bài.');
            window.location.href = fallback || 'index.html';
        }
    }
})();
