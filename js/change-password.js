(function (global) {
    'use strict';

    function escapeHtml(str) {
        return String(str ?? '').replace(/[&<>"']/g, function (m) {
            return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[m];
        });
    }

    function createModalDom() {
        if (document.getElementById('changePasswordModal')) return;

        const modalHtml = `
        <div id="changePasswordModal" class="fixed inset-0 z-[9999] hidden items-center justify-center p-4 bg-slate-900/60 backdrop-blur-sm transition-opacity duration-200">
            <div class="relative w-full max-w-md rounded-2xl bg-white p-6 shadow-2xl border border-slate-100 transform transition-all">
                <div class="flex items-center justify-between border-b border-slate-100 pb-4 mb-4">
                    <div class="flex items-center gap-3">
                        <div class="flex h-10 w-10 items-center justify-center rounded-xl bg-amber-50 text-amber-600 border border-amber-200"><i class="fas fa-key text-lg"></i></div>
                        <div><h3 class="text-lg font-bold text-slate-900">Đổi Mật Khẩu</h3><p id="changePasswordUserSub" class="text-xs text-slate-500">Cập nhật mật khẩu tài khoản</p></div>
                    </div>
                    <button type="button" id="btnCpClose" class="text-slate-400 hover:text-slate-600 p-1 rounded-lg transition"><i class="fas fa-times text-lg"></i></button>
                </div>
                <div id="changePasswordAlert" class="hidden mb-4 rounded-xl p-3 text-sm font-medium border"></div>
                <form id="changePasswordForm" class="space-y-4" onsubmit="ChangePasswordModal.submit(event)">
                    <div><label class="block text-xs font-bold uppercase tracking-wider text-slate-600 mb-1" for="cpCurrentPassword">Mật khẩu hiện tại</label><div class="relative"><span class="absolute inset-y-0 left-0 flex items-center pl-3 text-slate-400"><i class="fas fa-lock text-sm"></i></span><input type="password" id="cpCurrentPassword" required autocomplete="current-password" class="w-full rounded-xl border border-slate-200 py-2.5 pl-10 pr-10 text-sm outline-none transition focus:border-amber-500 focus:ring-2 focus:ring-amber-200" placeholder="Nhập mật khẩu hiện tại"><button type="button" class="absolute inset-y-0 right-0 flex items-center pr-3 text-slate-400 hover:text-slate-600" onclick="ChangePasswordModal.toggleVisibility('cpCurrentPassword', this)"><i class="fas fa-eye text-sm"></i></button></div></div>
                    <div><label class="block text-xs font-bold uppercase tracking-wider text-slate-600 mb-1" for="cpNewPassword">Mật khẩu mới</label><div class="relative"><span class="absolute inset-y-0 left-0 flex items-center pl-3 text-slate-400"><i class="fas fa-shield-alt text-sm"></i></span><input type="password" id="cpNewPassword" required minlength="6" autocomplete="new-password" class="w-full rounded-xl border border-slate-200 py-2.5 pl-10 pr-10 text-sm outline-none transition focus:border-amber-500 focus:ring-2 focus:ring-amber-200" placeholder="Tối thiểu 6 ký tự"><button type="button" class="absolute inset-y-0 right-0 flex items-center pr-3 text-slate-400 hover:text-slate-600" onclick="ChangePasswordModal.toggleVisibility('cpNewPassword', this)"><i class="fas fa-eye text-sm"></i></button></div></div>
                    <div><label class="block text-xs font-bold uppercase tracking-wider text-slate-600 mb-1" for="cpConfirmPassword">Xác nhận mật khẩu mới</label><div class="relative"><span class="absolute inset-y-0 left-0 flex items-center pl-3 text-slate-400"><i class="fas fa-check-circle text-sm"></i></span><input type="password" id="cpConfirmPassword" required minlength="6" autocomplete="new-password" class="w-full rounded-xl border border-slate-200 py-2.5 pl-10 pr-10 text-sm outline-none transition focus:border-amber-500 focus:ring-2 focus:ring-amber-200" placeholder="Nhập lại mật khẩu mới"><button type="button" class="absolute inset-y-0 right-0 flex items-center pr-3 text-slate-400 hover:text-slate-600" onclick="ChangePasswordModal.toggleVisibility('cpConfirmPassword', this)"><i class="fas fa-eye text-sm"></i></button></div></div>
                    <div class="flex items-center justify-end gap-2 pt-2 border-t border-slate-100"><button type="button" id="btnCpCancel" class="rounded-xl border border-slate-200 bg-white px-4 py-2 text-sm font-semibold text-slate-600 transition hover:bg-slate-50">Hủy</button><button type="submit" id="btnCpSubmit" class="inline-flex items-center gap-2 rounded-xl bg-amber-500 hover:bg-amber-600 text-white px-5 py-2 text-sm font-bold shadow-md shadow-amber-200 transition"><span>Lưu thay đổi</span></button></div>
                </form>
            </div>
        </div>`;
        document.body.insertAdjacentHTML('beforeend', modalHtml);
        document.getElementById('btnCpClose')?.addEventListener('click', () => ChangePasswordModal.close());
        document.getElementById('btnCpCancel')?.addEventListener('click', () => ChangePasswordModal.close());
        const modalOverlay = document.getElementById('changePasswordModal');
        modalOverlay?.addEventListener('click', (e) => { if (e.target === modalOverlay) ChangePasswordModal.close(); });
        document.addEventListener('keydown', (e) => { if (e.key === 'Escape' && !modalOverlay?.classList.contains('hidden')) ChangePasswordModal.close(); });
    }

    const ChangePasswordModal = {
        ensureModal: function () { createModalDom(); },
        open: function () {
            this.ensureModal();
            const modal = document.getElementById('changePasswordModal');
            if (!modal) return;
            document.getElementById('changePasswordForm')?.reset();
            const alertBox = document.getElementById('changePasswordAlert');
            if (alertBox) { alertBox.className = 'hidden mb-4 rounded-xl p-3 text-sm font-medium border'; alertBox.textContent = ''; }
            const username = localStorage.getItem('userEmail') || localStorage.getItem('userName') || '';
            const sub = document.getElementById('changePasswordUserSub');
            if (sub && username) sub.textContent = 'Tài khoản: ' + username;
            modal.classList.remove('hidden'); modal.classList.add('flex');
            setTimeout(() => document.getElementById('cpCurrentPassword')?.focus(), 100);
        },
        close: function () {
            const modal = document.getElementById('changePasswordModal');
            if (!modal) return;
            modal.classList.add('hidden'); modal.classList.remove('flex');
            document.getElementById('changePasswordForm')?.reset();
        },
        toggleVisibility: function (inputId, btn) {
            const input = document.getElementById(inputId); if (!input) return;
            const icon = btn?.querySelector('i');
            if (input.type === 'password') { input.type = 'text'; icon?.classList.replace('fa-eye', 'fa-eye-slash'); }
            else { input.type = 'password'; icon?.classList.replace('fa-eye-slash', 'fa-eye'); }
        },
        showAlert: function (message, type) {
            const box = document.getElementById('changePasswordAlert'); if (!box) return;
            box.classList.remove('hidden', 'bg-rose-50', 'text-rose-700', 'border-rose-200', 'bg-emerald-50', 'text-emerald-700', 'border-emerald-200');
            if (type === 'success') { box.classList.add('bg-emerald-50', 'text-emerald-700', 'border-emerald-200'); box.innerHTML = '<i class="fas fa-check-circle mr-2"></i>' + escapeHtml(message); }
            else { box.classList.add('bg-rose-50', 'text-rose-700', 'border-rose-200'); box.innerHTML = '<i class="fas fa-exclamation-circle mr-2"></i>' + escapeHtml(message); }
        },
        submit: async function (e) {
            if (e) e.preventDefault();
            const currentPassword = document.getElementById('cpCurrentPassword')?.value || '';
            const newPassword = document.getElementById('cpNewPassword')?.value || '';
            const confirmPassword = document.getElementById('cpConfirmPassword')?.value || '';
            const submitBtn = document.getElementById('btnCpSubmit');
            if (!currentPassword || !newPassword) return this.showAlert('Vui lòng điền đầy đủ các thông tin.', 'error');
            if (newPassword.length < 6) return this.showAlert('Mật khẩu mới cần ít nhất 6 ký tự.', 'error');
            if (newPassword !== confirmPassword) return this.showAlert('Xác nhận mật khẩu mới không trùng khớp.', 'error');
            if (currentPassword === newPassword) return this.showAlert('Mật khẩu mới không được trùng mật khẩu cũ.', 'error');
            if (submitBtn) { submitBtn.disabled = true; submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin mr-1.5"></i> Đang xử lý...'; }
            try {
                const response = await fetch('api/change_password.php', { method: 'POST', headers: { 'Content-Type': 'application/json' }, credentials: 'include', body: JSON.stringify({ current_password: currentPassword, new_password: newPassword, confirm_password: confirmPassword }) });
                const data = await response.json();
                if (!response.ok) throw new Error(data.error || 'Có lỗi xảy ra khi đổi mật khẩu.');
                this.showAlert(data.message || 'Đổi mật khẩu thành công!', 'success');
                document.getElementById('changePasswordForm')?.reset();
                setTimeout(() => ChangePasswordModal.close(), 1600);
            } catch (err) { this.showAlert(err.message || 'Không thể đổi mật khẩu.', 'error'); }
            finally { if (submitBtn) { submitBtn.disabled = false; submitBtn.innerHTML = '<span>Lưu thay đổi</span>'; } }
        }
    };
    global.ChangePasswordModal = ChangePasswordModal;
    if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', () => ChangePasswordModal.ensureModal());
    else ChangePasswordModal.ensureModal();
})(typeof window !== 'undefined' ? window : this);
