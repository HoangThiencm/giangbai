/**
 * Security Guard - Module bảo vệ chống mở F12, xem mã nguồn và DevTools
 * Hỗ trợ hệ thống giangbai / hoangthiencm.id.vn
 */
(function () {
    'use strict';

    // Bỏ qua bảo vệ nếu chạy trên localhost hoặc đã kích hoạt chế độ Debug bởi Admin
    var isLocalhost = Boolean(
        window.location.hostname === 'localhost' ||
        window.location.hostname === '127.0.0.1' ||
        window.location.hostname.startsWith('192.168.') ||
        window.location.protocol === 'file:'
    );

    var debugModeKey = '__system_debug_unlocked__';
    var isDebugUnlocked = sessionStorage.getItem(debugModeKey) === 'true';

    if (isLocalhost && isDebugUnlocked) {
        return;
    }

    // 1. Chặn menu chuột phải (Context Menu) - Vẫn cho phép thao tác trong ô soạn thảo/input
    document.addEventListener('contextmenu', function (e) {
        if (isDebugUnlocked) return;
        var target = e.target;
        var isEditable = target && (
            target.tagName === 'INPUT' ||
            target.tagName === 'TEXTAREA' ||
            target.isContentEditable ||
            target.tagName === 'MATH-FIELD' ||
            (target.closest && target.closest('math-field, [contenteditable="true"]'))
        );
        if (!isEditable) {
            e.preventDefault();
            e.stopPropagation();
            return false;
        }
    }, true);

    // 2. Chặn các tổ hợp phím tắt xem mã nguồn, mở DevTools, lưu trang
    document.addEventListener('keydown', function (e) {
        if (isDebugUnlocked) return;

        var keyCode = e.keyCode || e.which;
        var isCtrl = e.ctrlKey || e.metaKey; // Ctrl trên Win, Cmd trên Mac
        var isShift = e.shiftKey;
        var isAlt = e.altKey;

        // F12 (123)
        if (keyCode === 123) {
            e.preventDefault();
            e.stopPropagation();
            return false;
        }

        // Ctrl + Shift + I (Inspect Elements)
        // Ctrl + Shift + J (Console)
        // Ctrl + Shift + C (Element Picker)
        // Ctrl + Shift + K (Firefox Console)
        if (isCtrl && isShift && (keyCode === 73 || keyCode === 74 || keyCode === 67 || keyCode === 75)) {
            e.preventDefault();
            e.stopPropagation();
            return false;
        }

        // Ctrl + U (View Source)
        if (isCtrl && keyCode === 85) {
            e.preventDefault();
            e.stopPropagation();
            return false;
        }

        // Ctrl + S (Save page)
        if (isCtrl && keyCode === 83) {
            var target = e.target;
            var isInput = target && (target.tagName === 'INPUT' || target.tagName === 'TEXTAREA');
            if (!isInput) {
                e.preventDefault();
                e.stopPropagation();
                return false;
            }
        }

        // Phím tắt bí mật cho Quản trị viên: Ctrl + Alt + Shift + D để mở khóa Debug
        if (isCtrl && isAlt && isShift && (keyCode === 68 || e.key === 'D' || e.key === 'd')) {
            var key = prompt('Nhập mã xác thực Admin để mở khóa DevTools:');
            if (key) {
                var storedKey = localStorage.getItem('admin_key') || localStorage.getItem('ADMIN_KEY');
                if (storedKey && key === storedKey) {
                    sessionStorage.setItem(debugModeKey, 'true');
                    alert('Đã mở khóa chế độ DevTools cho phiên làm việc này.');
                    window.location.reload();
                } else if (key === 'htcm@admin' || key === 'hoangthien') {
                    sessionStorage.setItem(debugModeKey, 'true');
                    alert('Đã mở khóa chế độ DevTools cho phiên làm việc này.');
                    window.location.reload();
                } else {
                    alert('Mã xác thực không chính xác.');
                }
            }
            e.preventDefault();
            return false;
        }
    }, true);

    // 3. Cơ chế bẫy Debugger Trap khi cố tình mở DevTools
    function triggerDebuggerTrap() {
        if (isDebugUnlocked) return;
        try {
            var startTime = performance.now();
            (function () {
                Function('debugger')();
            })();
            var endTime = performance.now();
            if (endTime - startTime > 100) {
                // Phát hiện DevTools đang dừng ở debugger
                if (console && console.clear) {
                    console.clear();
                }
            }
        } catch (err) {}
    }

    // Chạy bẫy ngắt quãng
    setInterval(triggerDebuggerTrap, 2500);

    // 4. Phát hiện DevTools mở bằng cách đo chênh lệch kích thước cửa sổ
    var devtoolsThreshold = 170;
    function checkDevToolsOpen() {
        if (isDebugUnlocked) return;
        var widthDiff = window.outerWidth - window.innerWidth > devtoolsThreshold;
        var heightDiff = window.outerHeight - window.innerHeight > devtoolsThreshold;
        if (widthDiff || heightDiff) {
            if (console && console.clear) {
                console.clear();
            }
        }
    }
    window.addEventListener('resize', checkDevToolsOpen, { passive: true });

    // 5. Vô hiệu hóa một số hàm console nguy hiểm ở môi trường production
    try {
        if (!isLocalhost && !isDebugUnlocked && window.console) {
            var noop = function () {};
            var methods = ['log', 'debug', 'info', 'dir', 'dirxml', 'trace'];
            for (var i = 0; i < methods.length; i++) {
                // Giữ lại error và warn để không ảnh hưởng bắt lỗi logic
                window.console[methods[i]] = noop;
            }
        }
    } catch (e) {}

})();
