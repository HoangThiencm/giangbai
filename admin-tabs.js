(function () {
    const tabs = [
        { id: 'lessons', label: 'Bai hoc lo trinh', icon: 'fa-book-open' },
        { id: 'accounts', label: 'Tai khoan hoc sinh', icon: 'fa-user-graduate' },
        { id: 'progress', label: 'Theo doi tien do', icon: 'fa-chart-line' },
        { id: 'settings', label: 'Cai dat he thong', icon: 'fa-sliders' }
    ];

    function el(id) { return document.getElementById(id); }

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
        if (node && node.parentElement !== panel) panel.appendChild(node);
    }

    function findSettingsCard(dashboard) {
        const input = el('cfg_gslides') || el('cfg_github_token');
        return input ? input.closest('.bg-white.rounded-xl') : null;
    }

    function findAccountsTable(dashboard) {
        const body = el('tableBody');
        return body ? body.closest('.bg-white.rounded-xl') : null;
    }

    function activateTab(id) {
        document.querySelectorAll('.admin-tab-button').forEach(button => {
            const active = button.dataset.tab === id;
            button.classList.toggle('bg-blue-600', active);
            button.classList.toggle('text-white', active);
            button.classList.toggle('bg-white', !active);
            button.classList.toggle('text-slate-700', !active);
        });
        document.querySelectorAll('.admin-tab-panel').forEach(panel => {
            panel.classList.toggle('hidden', panel.id !== `adminTab_${id}`);
        });
        localStorage.setItem('admin_active_tab', id);
        if (id === 'progress' && typeof window.refreshAdminProgress === 'function') {
            window.refreshAdminProgress();
        }
    }

    window.ensureAdminTabs = function () {
        const dashboard = el('dashboardSection');
        if (!dashboard) return;

        let shell = el('adminTabsShell');
        if (!shell) {
            shell = document.createElement('div');
            shell.id = 'adminTabsShell';
            shell.className = 'space-y-5';
            shell.innerHTML = `
                <div id="adminTabNav" class="flex flex-wrap gap-2 rounded-xl border border-slate-200 bg-slate-50 p-2"></div>
                <div id="adminTabContent" class="space-y-6"></div>
            `;
            const stats = dashboard.querySelector('.grid.grid-cols-1.md\\:grid-cols-3');
            if (stats && stats.nextSibling) {
                dashboard.insertBefore(shell, stats.nextSibling);
            } else {
                dashboard.prepend(shell);
            }
        }

        const nav = el('adminTabNav');
        const content = el('adminTabContent');
        nav.innerHTML = tabs.map(tab => `
            <button type="button" data-tab="${tab.id}" class="admin-tab-button inline-flex items-center gap-2 rounded px-4 py-2 text-sm font-bold transition">
                <i class="fas ${tab.icon}"></i>${tab.label}
            </button>
        `).join('');

        tabs.forEach(tab => content.appendChild(makePanel(tab.id)));

        moveInto(makePanel('lessons'), el('lessonEditorPanel'));
        moveInto(makePanel('accounts'), el('studentCreatePanel'));
        moveInto(makePanel('accounts'), findAccountsTable(dashboard));
        moveInto(makePanel('progress'), el('adminProgressPanel'));
        moveInto(makePanel('settings'), findSettingsCard(dashboard));

        nav.querySelectorAll('.admin-tab-button').forEach(button => {
            button.onclick = () => activateTab(button.dataset.tab);
        });

        const saved = localStorage.getItem('admin_active_tab');
        activateTab(tabs.some(tab => tab.id === saved) ? saved : 'lessons');
    };

    function boot() {
        if (el('dashboardSection') && !el('dashboardSection').classList.contains('hidden')) {
            window.ensureAdminTabs();
        }
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', boot);
    } else {
        boot();
    }
})();
