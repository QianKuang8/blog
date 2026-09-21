// Resolve the theme before paint; storage may be unavailable in private contexts.
(() => {
    let theme;
    try { theme = localStorage.getItem('pref-theme'); } catch {}
    const dark = theme === 'dark' || (theme !== 'light' && matchMedia('(prefers-color-scheme: dark)').matches);
    document.documentElement.dataset.theme = dark ? 'dark' : 'light';
    document.documentElement.classList.add('js');
})();
