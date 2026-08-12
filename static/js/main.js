/**
 * BakiFlow System Interface Logic v1.0
 * Senior Developer Edition - Performance Optimized
 */

(function() {
    'use strict';

    document.addEventListener('DOMContentLoaded', function() {
        const html = document.documentElement;
        const themeToggle = document.getElementById('theme-toggle');

        /**
         * 🌓 Theme Logic
         * Uses CSS variables and local storage for state persistence.
         */
        const updateThemeUI = (theme) => {
            if (!themeToggle) return;
            const icon = themeToggle.querySelector('i');
            if (icon) {
                icon.className = theme === 'dark' ? 'fa-solid fa-sun' : 'fa-solid fa-moon';
                themeToggle.setAttribute('aria-label', theme === 'dark' ? 'Switch to Light Mode' : 'Switch to Dark Mode');
            }
        };

        const setTheme = (theme) => {
            html.setAttribute('data-theme', theme);
            localStorage.setItem('theme', theme);
            updateThemeUI(theme);
        };

        // Initialize from storage (Header guard handles immediate application)
        const initialTheme = localStorage.getItem('theme') || 'dark';
        updateThemeUI(initialTheme);

        if (themeToggle) {
            themeToggle.addEventListener('click', (e) => {
                e.preventDefault();
                const nextTheme = html.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
                setTheme(nextTheme);
            });
        }

        /**
         * 🔗 Navigation Intelligence
         * Highlighting current page and handling trail normalization.
         */
        const currentPath = window.location.pathname.replace(/\/$/, "") || "/";

        document.querySelectorAll('.nav-link').forEach(link => {
            const href = link.getAttribute('href');
            if (href) {
                const normalizedHref = href.replace(/\/$/, "") || "/";
                if (currentPath === normalizedHref) {
                    link.classList.add('active-page');
                }
            }
        });

        // Close alerts automatically or via X
        document.querySelectorAll('.alert-close').forEach(btn => {
            btn.addEventListener('click', () => {
                btn.parentElement.style.opacity = '0';
                setTimeout(() => btn.parentElement.remove(), 300);
            });
        });
    });
})();
