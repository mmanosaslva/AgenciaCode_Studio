function toggleTheme() {
    var html = document.documentElement;
    var current = html.getAttribute('data-theme');
    var next = current === 'dark' ? 'light' : 'dark';
    html.setAttribute('data-theme', next);
    localStorage.setItem('theme', next);
    updateToggleIcon(next);
}

function updateToggleIcon(theme) {
    var btn = document.getElementById('themeToggle');
    if (!btn) return;
    var icon = btn.querySelector('.material-symbols-outlined');
    if (theme === 'dark') {
        icon.textContent = 'light_mode';
        btn.title = 'Modo claro';
    } else {
        icon.textContent = 'dark_mode';
        btn.title = 'Modo oscuro';
    }
}

(function() {
    var theme = localStorage.getItem('theme') || 'light';
    updateToggleIcon(theme);
})();

document.addEventListener('DOMContentLoaded', function() {
    var sidebar = document.getElementById('sidebar');
    var overlay = document.getElementById('sidebarOverlay');
    var menuBtn = document.getElementById('mobileMenuBtn');

    if (menuBtn && sidebar && overlay) {
        function openSidebar() {
            sidebar.classList.add('open');
            overlay.classList.add('show');
        }
        function closeSidebar() {
            sidebar.classList.remove('open');
            overlay.classList.remove('show');
        }
        menuBtn.addEventListener('click', openSidebar);
        overlay.addEventListener('click', closeSidebar);
    }

    var toasts = document.querySelectorAll('.toast');
    toasts.forEach(function(t) {
        setTimeout(function() {
            t.classList.add('fade');
            setTimeout(function() { t.remove(); }, 300);
        }, 4000);
    });

    var alerts = document.querySelectorAll('.alert');
    alerts.forEach(function(a) {
        setTimeout(function() {
            a.style.transition = 'opacity 0.5s';
            void a.offsetWidth;
            a.style.opacity = '0';
            setTimeout(function() { a.style.display = 'none'; }, 500);
        }, 5000);
    });
});
