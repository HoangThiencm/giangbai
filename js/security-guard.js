/**
 * Security Guard - Module bảo vệ chống mở F12, xem mã nguồn và DevTools
 * Hỗ trợ hệ thống giangbai / hoangthiencm.id.vn
 */
(function () {
    'use strict';

    var debugModeKey = '__system_debug_unlocked__';

    function fingerprint(value) {
        var hash = 2166136261;
        var text = String(value || '');
        for (var i = 0; i < text.length; i++) {
            hash ^= text.charCodeAt(i);
            hash = Math.imul(hash, 16777619);
        }
        return (hash >>> 0).toString(16);
    }

    function storageGet(store, key) {
        try {
            return store && store.getItem ? store.getItem(key) : null;
        } catch (err) {
            return null;
        }
    }

    function storageSet(store, key, value) {
        try {
            if (store && store.setItem) store.setItem(key, value);
        } catch (err) {}
    }

    var hostname = '';
    var protocol = '';
    try {
        hostname = String((window.location && window.location.hostname) || '');
        protocol = String((window.location && window.location.protocol) || '');
    } catch (err) {}

    var isLocalhost = Boolean(
        hostname === 'localhost' ||
        hostname === '127.0.0.1' ||
        hostname === '[::1]' ||
        hostname.indexOf('192.168.') === 0 ||
        protocol === 'file:'
    );

    var isDebugUnlocked = storageGet(sessionStorage, debugModeKey) === 'true';

    // iPadOS may report a desktop Safari user-agent, so combine UA and touch points.
    var isMobileOrTablet = false;
    try {
        var userAgent = String((navigator && navigator.userAgent) || '');
        var maxTouchPoints = Number((navigator && navigator.maxTouchPoints) || 0);
        isMobileOrTablet = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini|Mobile|Tablet/i.test(userAgent) ||
            (/Macintosh/i.test(userAgent) && maxTouchPoints > 1);
    } catch (err) {}

    // Bỏ qua bảo vệ nếu chạy trên localhost hoặc đã kích hoạt chế độ Debug bởi Admin
    if (isLocalhost || isDebugUnlocked) {
        return;
    }

    var nativeConsole = null;
    try {
        if (window.console) {
            nativeConsole = {
                debug: typeof window.console.debug === 'function' ? window.console.debug.bind(window.console) : null,
                clear: typeof window.console.clear === 'function' ? window.console.clear.bind(window.console) : null
            };
        }
    } catch (err) {
        nativeConsole = null;
    }

    function isEditableTarget(target) {
        if (!target) return false;
        var tag = target.tagName;
        return Boolean(
            tag === 'INPUT' ||
            tag === 'TEXTAREA' ||
            target.isContentEditable ||
            tag === 'MATH-FIELD' ||
            (target.closest && target.closest('math-field, [contenteditable="true"]'))
        );
    }

    function blockEvent(e) {
        e.preventDefault();
        e.stopPropagation();
        return false;
    }

    function clearConsoleQuietly() {
        try {
            if (nativeConsole && nativeConsole.clear) nativeConsole.clear();
            else if (console && console.clear) console.clear();
        } catch (err) {}
    }

    var overlayId = '__gb_devtools_lock__';

    function getLockOverlay() {
        try {
            return document.getElementById(overlayId);
        } catch (err) {
            return null;
        }
    }

    function showLockOverlay() {
        if (isDebugUnlocked || isMobileOrTablet) return;
        var el = getLockOverlay();
        if (!el) {
            el = document.createElement('div');
            el.id = overlayId;
            el.setAttribute(
                'style',
                'position:fixed;inset:0;z-index:2147483647;background:rgba(8,12,24,0.97);color:#f8fafc;display:flex;align-items:center;justify-content:center;text-align:center;font:600 18px/1.55 system-ui,sans-serif;padding:24px;'
            );
            el.textContent = 'Phát hiện DevTools. Hãy đóng công cụ phát triển để tiếp tục.';
            var host = document.body || document.documentElement;
            if (host && host.appendChild) host.appendChild(el);
        }
        el.style.display = 'flex';
        try {
            if (document.documentElement && document.documentElement.style) {
                document.documentElement.style.overflow = 'hidden';
            }
        } catch (err) {}
    }

    function hideLockOverlay() {
        var el = getLockOverlay();
        if (el) el.style.display = 'none';
        try {
            if (document.documentElement && document.documentElement.style) {
                document.documentElement.style.overflow = '';
            }
        } catch (err) {}
    }

    var lastStrongDetectAt = 0;

    function onDevToolsDetected() {
        if (isDebugUnlocked || isMobileOrTablet) return;
        lastStrongDetectAt = Date.now();
        clearConsoleQuietly();
        showLockOverlay();
    }

    // 1. Chặn menu chuột phải (Context Menu) - Vẫn cho phép thao tác trong ô soạn thảo/input
    document.addEventListener('contextmenu', function (e) {
        if (isDebugUnlocked) return;
        if (!isEditableTarget(e.target)) {
            return blockEvent(e);
        }
    }, true);

    // 2. Chặn các tổ hợp phím tắt xem mã nguồn, mở DevTools, lưu trang
    document.addEventListener('keydown', function (e) {
        if (isDebugUnlocked) return;

        var keyCode = e.keyCode || e.which;
        var key = String(e.key || '').toLowerCase();
        var code = String(e.code || '');
        var isCtrl = e.ctrlKey || e.metaKey;
        var isShift = e.shiftKey;
        var isAlt = e.altKey;

        if (keyCode === 123 || code === 'F12' || key === 'f12') {
            return blockEvent(e);
        }

        if (isCtrl && isShift && (
            keyCode === 73 || keyCode === 74 || keyCode === 67 || keyCode === 75 || keyCode === 69 ||
            key === 'i' || key === 'j' || key === 'c' || key === 'k' || key === 'e'
        )) {
            return blockEvent(e);
        }

        if (isCtrl && !isShift && (keyCode === 85 || key === 'u')) {
            return blockEvent(e);
        }

        if (isCtrl && !isShift && (keyCode === 83 || key === 's')) {
            if (!isEditableTarget(e.target)) {
                return blockEvent(e);
            }
        }

        // Phím tắt bí mật cho Quản trị viên: Ctrl + Alt + Shift + D để mở khóa Debug
        if (isCtrl && isAlt && isShift && (keyCode === 68 || key === 'd')) {
            var typedKey = prompt('Nhập mã xác thực Admin để mở khóa DevTools:');
            if (typedKey) {
                var storedKey = storageGet(localStorage, 'admin_key') || storageGet(localStorage, 'ADMIN_KEY');
                var typedFp = fingerprint(typedKey);
                var allowedFallback = typedFp === '7731ce4a' || typedFp === 'c3e3eb18';
                if ((storedKey && typedKey === storedKey) || allowedFallback) {
                    storageSet(sessionStorage, debugModeKey, 'true');
                    alert('Đã mở khóa chế độ DevTools cho phiên làm việc này.');
                    window.location.reload();
                } else {
                    alert('Mã xác thực không chính xác.');
                }
            }
            return blockEvent(e);
        }
    }, true);

    // 3. Cơ chế bẫy Debugger Trap khi cố tình mở DevTools
    function triggerDebuggerTrap() {
        if (isDebugUnlocked || isMobileOrTablet) return;
        try {
            var startTime = performance.now();
            (function () {
                Function('debugger')();
            })();
            var endTime = performance.now();
            if (endTime - startTime > 100) {
                onDevToolsDetected();
            }
        } catch (err) {}
    }

    setInterval(triggerDebuggerTrap, 2500);

    // 4. Phát hiện DevTools mở bằng cách đo chênh lệch kích thước cửa sổ
    var devtoolsThreshold = 170;
    function checkDevToolsOpen() {
        if (isDebugUnlocked) return;
        if (isMobileOrTablet) return;
        var widthDiff = window.outerWidth - window.innerWidth > devtoolsThreshold;
        var heightDiff = window.outerHeight - window.innerHeight > devtoolsThreshold;
        if (widthDiff || heightDiff) {
            onDevToolsDetected();
        } else if (Date.now() - lastStrongDetectAt > 3000) {
            hideLockOverlay();
        }
    }
    window.addEventListener('resize', checkDevToolsOpen, { passive: true });
    checkDevToolsOpen();
    setInterval(checkDevToolsOpen, 1500);

    // 5. Vô hiệu hóa một số hàm console nguy hiểm ở môi trường production
    try {
        if (!isLocalhost && !isDebugUnlocked && window.console) {
            var noop = function () {};
            var methods = ['log', 'debug', 'info', 'dir', 'dirxml', 'trace', 'table', 'group', 'groupCollapsed', 'groupEnd'];
            for (var i = 0; i < methods.length; i++) {
                // Giữ lại error và warn để không ảnh hưởng bắt lỗi logic
                window.console[methods[i]] = noop;
            }
        }
    } catch (e) {}

})();
