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
    if (theme === 'dark') {
        btn.innerHTML = '<i class="bi bi-sun-fill"></i>';
        btn.title = 'Modo claro';
    } else {
        btn.innerHTML = '<i class="bi bi-moon-fill"></i>';
        btn.title = 'Modo oscuro';
    }
}

document.addEventListener('DOMContentLoaded', function () {
    var theme = localStorage.getItem('theme') || 'light';
    updateToggleIcon(theme);

    var toastElList = [].slice.call(document.querySelectorAll('.toast'));
    var toastList = toastElList.map(function (toastEl) {
        return new bootstrap.Toast(toastEl);
    });
});
