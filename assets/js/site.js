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

    // The query selects a reading view. Learning state comes only from Markdown.
    const learningRecord = document.querySelector('[data-learning-record]');
    if (learningRecord) {
        const learningBack = learningRecord.querySelector('[data-learning-back]');
        const readingBack = document.querySelector('[data-reading-back]');
        const ordinaryBack = readingBack && { href: readingBack.href, text: readingBack.textContent };
        const learningNav = document.querySelector('[data-learning-nav]');
        const nextLinks = [...document.querySelectorAll('[data-reading-path-next]')];
        function updateLearningView() {
            const enabled = new URL(location.href).searchParams.get('learning') === '1';
            learningRecord.hidden = !enabled;
            if (readingBack && learningBack) {
                readingBack.href = enabled ? learningBack.href : ordinaryBack.href;
                readingBack.textContent = enabled ? '← 学习清单' : ordinaryBack.text;
            }
            if (learningNav) {
                if (enabled) learningNav.setAttribute('aria-current', 'page');
                else learningNav.removeAttribute('aria-current');
            }
            nextLinks.forEach(link => {
                const url = new URL(link.href);
                if (enabled) url.searchParams.set('learning', '1');
                else url.searchParams.delete('learning');
                link.href = url.href;
            });
        }
        updateLearningView();
        addEventListener('popstate', updateLearningView);
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

    // Native anchors remain usable without JavaScript; copy adds a shareable URL.
    document.querySelectorAll('[data-heading-anchor]').forEach(anchor => {
        anchor.addEventListener('click', () => {
            const url = new URL(anchor.href);
            url.searchParams.delete('focus');
            url.searchParams.delete('learning');
            navigator.clipboard?.writeText(url.href).catch(() => {});
        });
    });
    const toc = document.querySelector('.bc-toc');
    if (toc && 'IntersectionObserver' in window) {
        const links = [...toc.querySelectorAll('a[href^="#"]')];
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
