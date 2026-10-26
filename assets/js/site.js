(() => {
    const themeToggle = document.querySelector('[data-theme-toggle]');
    const focusToggle = document.querySelector('[data-focus-toggle]');
    const layout = document.querySelector('.bc-layout');
    const colorScheme = matchMedia('(prefers-color-scheme: dark)');

    function updateTheme(dark) {
        document.documentElement.dataset.theme = dark ? 'dark' : 'light';
        if (themeToggle) {
            themeToggle.textContent = dark ? '浅色主题' : '深色主题';
            themeToggle.setAttribute('aria-label', `切换为${dark ? '浅色' : '深色'}主题`);
        }
    }
    if (themeToggle) {
        themeToggle.hidden = false;
        updateTheme(document.documentElement.dataset.theme === 'dark');
        themeToggle.addEventListener('click', () => {
            const dark = document.documentElement.dataset.theme !== 'dark';
            updateTheme(dark);
            try { localStorage.setItem('pref-theme', dark ? 'dark' : 'light'); } catch {}
        });
    }
    colorScheme.addEventListener('change', event => {
        let preference;
        try { preference = localStorage.getItem('pref-theme'); } catch {}
        if (preference !== 'light' && preference !== 'dark') updateTheme(event.matches);
    });

    function updateFocus(focused) {
        layout.classList.toggle('bc-focused', focused);
        focusToggle.textContent = focused ? '退出专注阅读' : '专注阅读';
        focusToggle.setAttribute('aria-pressed', String(focused));
    }
    if (focusToggle && layout) {
        focusToggle.hidden = false;
        updateFocus(new URL(location.href).searchParams.get('focus') === '1');
        focusToggle.addEventListener('click', () => {
            const focused = !layout.classList.contains('bc-focused');
            updateFocus(focused);
            const url = new URL(location.href);
            if (focused) url.searchParams.set('focus', '1');
            else url.searchParams.delete('focus');
            history.replaceState(null, '', url);
        });
        addEventListener('popstate', () => {
            updateFocus(new URL(location.href).searchParams.get('focus') === '1');
        });
    }

    function revealLearningGroup() {
        const group = document.getElementById(location.hash.slice(1));
        if (group?.matches('details[data-learning-group]')) group.open = true;
    }
    revealLearningGroup();
    addEventListener('hashchange', revealLearningGroup);
    document.querySelectorAll('[data-learning-reveal]').forEach(link => {
        link.addEventListener('click', () => {
            const group = document.getElementById(link.hash.slice(1));
            if (group?.matches('details[data-learning-group]')) group.open = true;
        });
    });

    document.querySelectorAll('.post-content pre').forEach(pre => {
        const code = pre.querySelector('code');
        if (!code || !navigator.clipboard) return;
        const wrapper = document.createElement('div');
        wrapper.className = 'code-block';
        pre.before(wrapper);
        wrapper.append(pre);
        const button = document.createElement('button');
        button.type = 'button';
        button.className = 'copy-code';
        button.textContent = '复制';
        button.setAttribute('aria-label', '复制代码');
        button.setAttribute('aria-live', 'polite');
        button.addEventListener('click', async () => {
            try {
                await navigator.clipboard.writeText(code.innerText);
                button.textContent = '已复制';
            } catch {
                button.textContent = '请手动复制';
            }
            setTimeout(() => { button.textContent = '复制'; }, 1800);
        });
        wrapper.append(button);
    });

    // Small copy buttons under an article heading: "title URL" of this post or its original.
    document.querySelectorAll('[data-copy]').forEach(button => {
        if (!navigator.clipboard) return;
        button.hidden = false;
        const label = button.getAttribute('aria-label');
        button.addEventListener('click', async () => {
            let message = '已复制';
            try {
                await navigator.clipboard.writeText(button.dataset.copy);
                button.classList.add('is-copied');
            } catch {
                message = '复制失败，请手动复制';
            }
            button.setAttribute('aria-label', message);
            button.title = message;
            setTimeout(() => {
                button.classList.remove('is-copied');
                button.setAttribute('aria-label', label);
                button.title = label;
            }, 1500);
        });
    });

    // Native anchors remain usable without JavaScript; copy adds a shareable URL.
    document.querySelectorAll('[data-heading-anchor]').forEach(anchor => {
        anchor.addEventListener('click', () => {
            const url = new URL(anchor.href);
            url.searchParams.delete('focus');
            url.searchParams.delete('learning');
            navigator.clipboard?.writeText(url.href).catch(() => {});
        });
    });
    // "/" jumps to search from anywhere; keys typed into a field are left alone.
    const searchField = document.querySelector('.bc-search input, #searchInput');
    document.querySelectorAll('[data-search-key]').forEach(key => { key.hidden = false; });
    addEventListener('keydown', event => {
        if (event.key !== '/' || event.defaultPrevented || event.ctrlKey || event.metaKey || event.altKey) return;
        if (event.target instanceof Element && event.target.closest('input, textarea, select, [contenteditable]')) return;
        event.preventDefault();
        if (searchField) searchField.focus();
        else if (document.body.dataset.searchUrl) location.href = document.body.dataset.searchUrl;
    });

    const toc = document.querySelector('.bc-toc');
    if (toc && 'IntersectionObserver' in window) {
        // Only outline entries; the "back to top" link is not a section.
        const links = [...toc.querySelectorAll('nav a[href^="#"]')];
        const headings = links.map(link => document.getElementById(decodeURIComponent(link.hash.slice(1)))).filter(Boolean);
        const observer = new IntersectionObserver(entries => {
            const visible = entries.filter(entry => entry.isIntersecting).sort((a, b) => a.boundingClientRect.top - b.boundingClientRect.top);
            if (!visible.length) return;
            links.forEach(link => {
                if (decodeURIComponent(link.hash.slice(1)) === visible[0].target.id) link.setAttribute('aria-current', 'location');
                else link.removeAttribute('aria-current');
            });
        }, { rootMargin: '-5% 0px -70% 0px' });
        headings.forEach(heading => observer.observe(heading));
    }
})();
