/**
 * BakiFlow System Interface Logic v1.0
 * Unified Theme & Navigation Management
 */

(function() {
    'use strict';

    document.addEventListener('DOMContentLoaded', function() {
        console.log('BakiFlow v1.0 Framework Initialized');

        const html = document.documentElement;
        const themeToggle = document.getElementById('theme-toggle');

        /**
         * 🌓 Theme Engine
         */
        const updateIcon = (theme) => {
            if (!themeToggle) return;
            const icon = themeToggle.querySelector('i');
            if (icon) {
                icon.className = theme === 'dark' ? 'fa-solid fa-sun' : 'fa-solid fa-moon';
            }
        };

        const setTheme = (theme) => {
            html.setAttribute('data-theme', theme);
            localStorage.setItem('theme', theme);
            updateIcon(theme);
        };

        // Initialize from storage
        const savedTheme = localStorage.getItem('theme') || 'dark';
        setTheme(savedTheme);

        if (themeToggle) {
            themeToggle.addEventListener('click', (e) => {
                e.preventDefault();
                const newTheme = html.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
                setTheme(newTheme);
            });
        }

        /**
         * 🔗 Navigation & UX
         */
        const path = window.location.pathname.replace(/\/$/, "");

        document.querySelectorAll('.nav-link').forEach(link => {
            const href = link.getAttribute('href');
            if (href) {
                const cleanHref = href.replace(/\/$/, "");
                if (path === cleanHref) {
                    link.classList.add('active-page');
                    link.style.color = 'var(--brand-blue)';
                    link.style.fontWeight = '700';
                }
            }
        });

        // Form Alignment & Focus Polish
        document.querySelectorAll('.form-control-custom').forEach(input => {
            input.addEventListener('focus', () => {
                input.closest('.input-wrapper').style.borderColor = 'var(--brand-blue)';
            });
            input.addEventListener('blur', () => {
                input.closest('.input-wrapper').style.borderColor = 'var(--border-color)';
            });
        });
    });
})();
