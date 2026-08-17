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

        /**
         * 🤖 AI Chatbot Logic
         */
        const chatBubble = document.getElementById('chat-bubble');
        const chatWindow = document.getElementById('chat-window');
        const closeChat = document.getElementById('close-chat');
        const sendChat = document.getElementById('send-chat');
        const chatInput = document.getElementById('chat-input');
        const chatMessages = document.getElementById('chat-messages');

        if (chatBubble && chatWindow) {
            chatBubble.addEventListener('click', () => {
                const isVisible = chatWindow.style.display === 'flex';
                chatWindow.style.display = isVisible ? 'none' : 'flex';
                if (!isVisible) chatInput.focus();
            });

            closeChat.addEventListener('click', () => {
                chatWindow.style.display = 'none';
            });

            const appendMessage = (text, sender) => {
                const msg = document.createElement('div');
                msg.className = `message ${sender}`;
                msg.textContent = text;
                chatMessages.appendChild(msg);
                chatMessages.scrollTop = chatMessages.scrollHeight;
            };

            const handleSend = async () => {
                const text = chatInput.value.trim();
                if (!text) return;

                appendMessage(text, 'user');
                chatInput.value = '';

                // Simulate AI Thinking
                const typing = document.createElement('div');
                typing.className = 'message bot';
                typing.textContent = '...';
                chatMessages.appendChild(typing);

                try {
                    const response = await fetch('/api/v1/chatbot/ask/', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                            'X-CSRFToken': getCookie('csrftoken')
                        },
                        body: JSON.stringify({ query: text })
                    });
                    const data = await response.json();
                    typing.remove();
                    appendMessage(data.response, 'bot');
                } catch (e) {
                    typing.remove();
                    appendMessage("Sorry, I'm having trouble connecting to the brain right now. 🧠", 'bot');
                }
            };

            if (sendChat) sendChat.addEventListener('click', handleSend);
            if (chatInput) chatInput.addEventListener('keypress', (e) => {
                if (e.key === 'Enter') handleSend();
            });
        }

        function getCookie(name) {
            let cookieValue = null;
            if (document.cookie && document.cookie !== '') {
                const cookies = document.cookie.split(';');
                for (let i = 0; i < cookies.length; i++) {
                    const cookie = cookies[i].trim();
                    if (cookie.substring(0, name.length + 1) === (name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
        }
    });
})();
