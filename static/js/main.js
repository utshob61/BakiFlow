/**
 * BakiFlow System Interface Logic v1.0
 */

document.addEventListener('DOMContentLoaded', function() {
    console.log('BakiFlow v1.0 Initialized');

    const htmlElement = document.documentElement;
    const themeToggle = document.getElementById('theme-toggle');

    /**
     * Theme Management Logic
     */
    function applyTheme(theme) {
        htmlElement.setAttribute('data-theme', theme);
        localStorage.setItem('theme', theme);
        updateToggleIcon(theme);
    }

    function updateToggleIcon(theme) {
        if (!themeToggle) return;
        const icon = themeToggle.querySelector('i');
        if (!icon) return;

        if (theme === 'dark') {
            icon.className = 'fa-solid fa-sun';
            themeToggle.title = "Switch to Light Mode";
        } else {
            icon.className = 'fa-solid fa-moon';
            themeToggle.title = "Switch to Dark Mode";
        }
    }

    // Set initial theme from storage or default to dark
    const initialTheme = localStorage.getItem('theme') || 'dark';
    applyTheme(initialTheme);

    if (themeToggle) {
        themeToggle.addEventListener('click', function(e) {
            e.preventDefault();
            const currentTheme = htmlElement.getAttribute('data-theme');
            const targetTheme = currentTheme === 'dark' ? 'light' : 'dark';
            applyTheme(targetTheme);
        });
    }

    /**
     * Navigation Logic
     */
    const currentPath = window.location.pathname.replace(/\/$/, "");

    // Desktop Nav highlighting
    document.querySelectorAll('.nav-link').forEach(link => {
        const href = link.getAttribute('href');
        if (href) {
            const normalizedHref = href.replace(/\/$/, "");
            if (currentPath === normalizedHref) {
                link.classList.add('active-page');
            }
        }
    });

    // Handle form focus visual consistency
    document.querySelectorAll('input').forEach(input => {
        input.addEventListener('focus', () => {
            input.parentElement.classList.add('input-focused');
        });
        input.addEventListener('blur', () => {
            input.parentElement.classList.remove('input-focused');
        });
    });
});
