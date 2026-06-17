(function () {
    const tabs = [
        { id: 'lessons', label: 'Tạo bài học', icon: 'fa-book-open' },
        { id: 'accounts', label: 'Tạo tài khoản', icon: 'fa-user-graduate' },
        { id: 'progress', label: 'Theo dõi tiến độ', icon: 'fa-chart-line' },
        { id: 'settings', label: 'Cài đặt hệ thống', icon: 'fa-sliders' }
    ];

    let observerStarted = false;
    let arranging = false;

    function el(id) {
        return document.getElementById(id);
    }

    function makePanel(id) {
        let panel = el(`adminTab_${id}`);
        if (!panel) {
            panel = document.createElement('div');
            panel.id = `adminTab_${id}`;
            panel.className = 'admin-tab-panel space-y-6';
        }
        return panel;
    }

    function moveInto(panel, node) {
        if (node && node.parentElement !== panel) {
            panel.appendChild(node);
        }
    }

    function findStatsGrid(dashboard) {
        return el('statTotal')?.closest('.grid') || dashboard.querySelector('.grid');
    }

    function findSettingsCard() {
        return el('cfg_gslides')?.closest('.bg-white.rounded-xl') || el('cfg_github_token')?.closest('.bg-white.rounded-xl');
    }

    function findAccountsTable() {
        return el('tableBody')?.closest('.bg-white.rounded-xl');
    }

    function activeTabId() {
        const saved = localStorage.getItem('admin_active_tab');
        return tabs.some(tab => tab.id === saved) ? saved : 'lessons';
    }

    function activateTab(id) {
        document.querySelectorAll('.admin-tab-button').forEach(button => {
            const active = button.dataset.tab === id;
            button.classList.toggle('bg-blue-600', active);
            button.classList.toggle('text-white', active);
            button.classList.toggle('border-blue-600', active);
            button.classList.toggle('bg-white', !active);
            button.classList.toggle('text-slate-700', !active);
            button.classList.toggle('border-slate-200', !active);
        });

        document.querySelectorAll('.admin-tab-panel').forEach(panel => {
            panel.classList.toggle('hidden', panel.id !== `adminTab_${id}`);
        });

        localStorage.setItem('admin_active_tab', id);
        if (id === 'progress' && typeof window.refreshAdminProgress === 'function') {
            window.refreshAdminProgress().catch?.(() => {});
        }
    }

    window.ensureAdminTabs = function () {
        const dashboard = el('dashboardSection');
        if (!dashboard || dashboard.classList.contains('hidden') || arranging) return;

        arranging = true;
        try {
            let shell = el('adminTabsShell');
            if (!shell) {
                shell = document.createElement('div');
                shell.id = 'adminTabsShell';
                shell.className = 'space-y-5 mb-8';
                shell.innerHTML = `
                    <div class="rounded-xl border border-slate-200 bg-white p-2 shadow-sm">
                        <div id="adminTabNav" class="flex flex-wrap gap-2"></div>
                    </div>
                    <div id="adminTabContent" class="space-y-6"></div>
                `;

                const stats = findStatsGrid(dashboard);
                if (stats) {
                    stats.insertAdjacentElement('afterend', shell);
                } else {
                    dashboard.prepend(shell);
                }
            }

            const nav = el('adminTabNav');
            const content = el('adminTabContent');
            if (!nav || !content) return;

            nav.innerHTML = tabs.map(tab => `
                <button type="button" data-tab="${tab.id}" class="admin-tab-button inline-flex items-center gap-2 rounded border px-4 py-2 text-sm font-bold transition">
                    <i class="fas ${tab.icon}"></i>${tab.label}
                </button>
            `).join('');

            tabs.forEach(tab => content.appendChild(makePanel(tab.id)));

            moveInto(makePanel('lessons'), el('lessonEditorPanel'));
            moveInto(makePanel('accounts'), el('studentCreatePanel'));
            moveInto(makePanel('accounts'), findAccountsTable());
            moveInto(makePanel('progress'), el('adminProgressPanel'));
            moveInto(makePanel('settings'), findSettingsCard());

            nav.querySelectorAll('.admin-tab-button').forEach(button => {
                button.onclick = () => activateTab(button.dataset.tab);
            });

            activateTab(activeTabId());
        } finally {
            arranging = false;
        }
    };

    function scheduleEnsure() {
        setTimeout(() => window.ensureAdminTabs(), 0);
        setTimeout(() => window.ensureAdminTabs(), 250);
        setTimeout(() => window.ensureAdminTabs(), 1000);
    }

    function wrapLoadUsers() {
        if (typeof window.loadUsers !== 'function' || window.loadUsers.__tabsWrapped) return;
        const original = window.loadUsers;
        const wrapped = async function (...args) {
            const result = await original.apply(this, args);
            scheduleEnsure();
            return result;
        };
        wrapped.__tabsWrapped = true;
        window.loadUsers = wrapped;
    }

    function startObserver() {
        if (observerStarted) return;
        const dashboard = el('dashboardSection');
        if (!dashboard) return;
        observerStarted = true;
        new MutationObserver(() => scheduleEnsure()).observe(dashboard, { childList: true, subtree: true });
    }

    function boot() {
        wrapLoadUsers();
        startObserver();
        scheduleEnsure();
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', boot);
    } else {
        boot();
    }
})();
