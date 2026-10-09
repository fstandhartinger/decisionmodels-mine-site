// Before paint, use only the visitor's own explicit theme preference.
(() => { try { const t = localStorage.getItem('dm-theme'); if (t === 'light' || t === 'dark') document.documentElement.dataset.theme = t; } catch (_) {} })();
