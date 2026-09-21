import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import test from 'node:test';
import vm from 'node:vm';

const source = readFileSync(new URL('../assets/js/fastsearch.js', import.meta.url), 'utf8')
    .replace("import * as params from '@params';", 'const params = {};');
const fuseSource = readFileSync(new URL('../assets/js/vendor/fuse.basic.min.js', import.meta.url), 'utf8');

// Small DOM boundary for event regressions. The production search code and the
// bundled Fuse engine run unchanged; browser rendering/focus rings need visual QA.
function fixture(href = 'https://example.test/blog/search/') {
    let activeElement;
    class Element {
        constructor(tagName) {
            this.tagName = tagName;
            this.children = [];
            this.listeners = new Map();
            this.attributes = new Map();
            this.dataset = {};
            this.value = '';
            this.className = '';
        }
        set innerHTML(_) { throw new Error('Search must render through safe DOM methods'); }
        set textContent(text) { this.children = []; this.text = String(text); }
        get textContent() { return (this.text || '') + this.children.map(child => child.textContent).join(''); }
        append(...children) {
            for (const child of children) {
                if (child.tagName === '#fragment') this.append(...child.children);
                else this.children.push(child);
            }
        }
        replaceChildren(...children) { this.children = []; this.text = ''; this.append(...children); }
        setAttribute(key, value) { this.attributes.set(key, String(value)); }
        getAttribute(key) { return this.attributes.get(key); }
        addEventListener(type, listener) {
            if (!this.listeners.has(type)) this.listeners.set(type, []);
            this.listeners.get(type).push(listener);
        }
        dispatch(type, properties = {}) {
            const event = { defaultPrevented: false, preventDefault() { this.defaultPrevented = true; }, ...properties };
            for (const listener of this.listeners.get(type) || []) listener(event);
            return event;
        }
        focus() { activeElement = this; }
        querySelectorAll(selector) {
            return this.children.flatMap(child => [
                ...(selector.startsWith('.') ? child.className.split(' ').includes(selector.slice(1)) : child.tagName === selector) ? [child] : [],
                ...child.querySelectorAll(selector)
            ]);
        }
    }
    const elements = Object.fromEntries(['searchbox', 'searchInput', 'searchResults', 'searchStatus', 'searchRetry']
        .map(id => [id, new Element(id === 'searchInput' ? 'input' : 'div')]));
    elements.searchbox.dataset.indexUrl = '/blog/index.json';
    const document = {
        get activeElement() { return activeElement; },
        getElementById: id => elements[id],
        createElement: tag => new Element(tag),
        createDocumentFragment: () => new Element('#fragment'),
        createTextNode(text) { const node = new Element('#text'); node.textContent = text; return node; }
    };
    const requests = [];
    const timers = new Set();
    const location = { href };
    const history = {
        replacements: [],
        replaceState(_state, _title, url) {
            this.replacements.push(url);
            location.href = url;
        }
    };
    const context = vm.createContext({
        document,
        window: { location, history },
        URL, AbortController,
        setTimeout(callback) { timers.add(callback); return callback; },
        clearTimeout(callback) { timers.delete(callback); },
        fetch(url, { signal }) {
            return new Promise((resolve, reject) => {
                requests.push({ url, resolve, reject });
                signal.addEventListener('abort', () => reject(new Error('Request timed out')));
            });
        }
    });
    vm.runInContext(fuseSource, context);
    vm.runInContext(source, context);
    const flush = () => new Promise(resolve => setImmediate(resolve));
    return {
        ...elements, document, requests, timers, location, history,
        setInput(value, properties = {}) {
            elements.searchInput.value = value;
            elements.searchInput.dispatch('input', properties);
        },
        async respond(data, ok = true) {
            requests.at(-1).resolve({ ok, json: async () => data });
            await flush();
        },
        async reject() { requests.at(-1).reject(new Error('Network unavailable')); await flush(); },
        async timeout() { [...timers].forEach(callback => callback()); await flush(); },
        links() { return elements.searchResults.querySelectorAll('a'); },
        key(key, properties = {}) { return elements.searchbox.dispatch('keydown', { key, ...properties }); }
    };
}

function article(title, overrides = {}) {
    return { title, summary: `${title} 的摘要`, content: `${title} 的正文`, permalink: `/blog/posts/${encodeURIComponent(title)}/`,
        category: '原创文章', date: '2026-09-21', tags: [], ...overrides };
}

test('URL query searches on arrival and remains shareable as it changes or clears', async () => {
    const page = fixture('https://example.test/blog/search/?q=%E4%B8%AD%E6%96%87&from=nav#results');
    assert.equal(page.searchInput.value, '中文');
    await page.respond([article('中文搜索'), article('Alpha')]);
    assert.equal(page.links().length, 1);
    assert.match(page.links()[0].textContent, /中文搜索/);
    page.setInput('Alpha');
    let url = new URL(page.location.href);
    assert.equal(url.searchParams.get('q'), 'Alpha');
    assert.equal(url.searchParams.get('from'), 'nav');
    assert.equal(url.hash, '#results');
    assert.equal(url.pathname, '/blog/search/');
    page.key('Escape');
    url = new URL(page.location.href);
    assert.equal(url.searchParams.has('q'), false);
    assert.equal(page.history.replacements.length, 2);
});

test('URL query uses the input length limit and unfinished IME input does not change it', async () => {
    const page = fixture(`https://example.test/blog/search/?q=${'中'.repeat(100)}`);
    assert.equal(page.searchInput.value.length, 64);
    await page.respond([article('中文搜索')]);
    const retained = page.location.href;
    page.searchInput.dispatch('compositionstart');
    page.setInput('中文', { isComposing: true });
    assert.equal(page.location.href, retained);
    page.searchInput.dispatch('compositionend');
    assert.equal(new URL(page.location.href).searchParams.get('q'), '中文');
    assert.equal(page.links().length, 1);
});

test('starts loading immediately and searches input entered before the index arrives', async () => {
    const page = fixture();
    assert.equal(page.requests.length, 1);
    assert.equal(page.requests[0].url, '/blog/index.json');
    assert.equal(page.searchResults.getAttribute('aria-busy'), 'true');
    assert.match(page.searchStatus.textContent, /正在加载/);
    page.setInput('中文');
    assert.equal(page.links().length, 0);
    await page.respond([article('中文搜索'), article('Alpha')]);
    assert.equal(page.links().length, 1);
    assert.match(page.links()[0].textContent, /中文搜索/);
    assert.equal(page.searchResults.getAttribute('aria-busy'), 'false');
    assert.equal(page.timers.size, 0);
});

test('paste/input replaces previous results; clearing and no-match do not create fake links', async () => {
    const page = fixture();
    await page.respond([article('Alpha'), article('Beta')]);
    page.setInput('Alpha');
    assert.match(page.links()[0].textContent, /Alpha/);
    page.setInput('Beta', { inputType: 'insertFromPaste' });
    assert.equal(page.links().length, 1);
    assert.match(page.links()[0].textContent, /Beta/);
    page.setInput('');
    assert.equal(page.links().length, 0);
    page.setInput('没有任何对应条目的词语');
    assert.equal(page.links().length, 0);
    assert.match(page.searchStatus.textContent, /未找到/);
    page.searchInput.value = '';
    page.searchInput.dispatch('search');
    assert.doesNotMatch(page.searchStatus.textContent, /未找到/);
});

test('HTTP, network, malformed data and timeout failures can retry the current query', async () => {
    for (const failure of ['http', 'network', 'invalid', 'timeout']) {
        const page = fixture();
        page.setInput('Alpha');
        if (failure === 'http') await page.respond([], false);
        if (failure === 'network') await page.reject();
        if (failure === 'invalid') await page.respond([{ title: 'missing fields' }]);
        if (failure === 'timeout') await page.timeout();
        assert.match(page.searchStatus.textContent, /暂时无法搜索/);
        assert.equal(page.searchRetry.hidden, false);
        assert.equal(page.searchInput.value, 'Alpha');
        page.searchRetry.dispatch('click');
        page.searchRetry.dispatch('click');
        assert.equal(page.requests.length, 2);
        assert.equal(page.searchRetry.hidden, true);
        await page.respond([article('Alpha')]);
        assert.equal(page.links().length, 1);
        assert.equal(page.document.activeElement, page.searchInput);
    }
});

test('Chinese IME waits for compositionend and Escape does not cancel composition', async () => {
    const page = fixture();
    await page.respond([article('中文搜索')]);
    page.searchInput.dispatch('compositionstart');
    page.setInput('中', { isComposing: true });
    assert.equal(page.links().length, 0);
    page.key('Escape', { isComposing: true });
    assert.equal(page.searchInput.value, '中');
    page.searchInput.value = '中文';
    page.searchInput.dispatch('compositionend');
    assert.equal(page.links().length, 1);
    assert.equal(page.searchResults.querySelectorAll('mark')[0].textContent, '中文');
});

test('arrow keys use current native focus, respect boundaries, and leave Tab/Enter native', async () => {
    const page = fixture();
    await page.respond([article('中文甲'), article('中文乙')]);
    page.setInput('中文');
    const [first, last] = page.links();
    page.searchInput.focus();
    assert.equal(page.key('ArrowUp').defaultPrevented, true);
    assert.equal(page.document.activeElement, page.searchInput);
    page.key('ArrowDown');
    assert.equal(page.document.activeElement, first);
    assert.equal(page.key('Tab').defaultPrevented, false);
    // Represents a browser Tab focus change; no script-maintained selection exists.
    last.focus();
    page.key('ArrowDown');
    assert.equal(page.document.activeElement, last);
    page.key('ArrowUp');
    assert.equal(page.document.activeElement, first);
    assert.equal(page.key('Enter').defaultPrevented, false);
    page.key('ArrowUp');
    assert.equal(page.document.activeElement, page.searchInput);
    page.key('Escape');
    assert.equal(page.searchInput.value, '');
    assert.equal(page.links().length, 0);
    assert.equal(page.key('ArrowDown').defaultPrevented, false);
});

test('title, snippets and regex-like queries render as text; unsafe URLs are excluded', async () => {
    const page = fixture();
    const title = '<img src=x onerror=alert(1)> [GLM]';
    await page.respond([
        article(title, { summary: '<script>alert(1)</script> [GLM]' }),
        article('[GLM] script', { permalink: 'javascript:alert(1)' }),
        article('[GLM] bad URL', { permalink: 'https://[' })
    ]);
    page.setInput('[GLM]');
    assert.equal(page.links().length, 1);
    assert.equal(page.searchResults.querySelectorAll('h2')[0].textContent, title);
    assert.equal(page.searchResults.querySelectorAll('img').length, 0);
    assert.equal(page.searchResults.querySelectorAll('script').length, 0);
    assert.equal(page.searchResults.querySelectorAll('mark')[0].textContent, '[GLM]');
});

test('title ranks above a full-text mention and late body matches have honest excerpts', async () => {
    const page = fixture();
    await page.respond([
        article('系统实践', { summary: '讨论系统行为', content: '背景材料。'.repeat(60) + 'GLM 推理优化的细节。' }),
        article('GLM 推理优化', { summary: '讨论系统行为', content: '讲解系统实现' })
    ]);
    page.setInput('GLM');
    assert.equal(page.links().length, 2);
    assert.match(page.links()[0].textContent, /^GLM 推理优化/);
    assert.match(page.links()[1].textContent, /正文命中 · ….*GLM/);
    assert.match(page.links()[0].textContent, /原创文章2026-09-21/);
    assert.equal(page.searchResults.querySelectorAll('time')[0].dateTime, '2026-09-21');
});

test('a tag-only query finds both a stable slug and the displayed tag name', async () => {
    const page = fixture();
    await page.respond([
        article('A practical notebook', {
            summary: 'Lessons from recent work', content: 'Review of our development practices.',
            tags: ['engineering-journal', '工程复盘']
        }),
        article('Unrelated essay')
    ]);
    for (const query of ['engineering-journal', '工程复盘']) {
        page.setInput(query);
        assert.equal(page.links().length, 1);
        assert.match(page.links()[0].textContent, /^A practical notebook/);
        // A tag match does not pretend that the query occurs in the body.
        assert.match(page.links()[0].textContent, /摘要 · Lessons from recent work/);
        assert.equal(page.searchResults.querySelectorAll('mark').length, 0);
    }
});

test('malformed tag fields reject the index and keep retry available', async () => {
    for (const tags of ['engineering-journal', [42], null]) {
        const page = fixture();
        await page.respond([article('Notebook', { tags })]);
        assert.match(page.searchStatus.textContent, /暂时无法搜索/);
        assert.equal(page.searchRetry.hidden, false);
        assert.equal(page.links().length, 0);
    }
});

test('a fuzzy-only result shows a summary without fabricating literal highlights', async () => {
    const page = fixture();
    await page.respond([article('Infrastructure', { summary: 'How serving works', content: 'Implementation details' })]);
    page.setInput('Infrastructrue');
    assert.equal(page.links().length, 1);
    assert.match(page.links()[0].textContent, /摘要 · How serving works/);
    assert.equal(page.searchResults.querySelectorAll('mark').length, 0);
});

test('search keeps every match instead of silently applying a result limit', async () => {
    const page = fixture();
    await page.respond(Array.from({ length: 40 }, (_, i) => article(`中文文章 ${i}`)));
    page.setInput('中文');
    assert.equal(page.links().length, 40);
    assert.match(page.searchStatus.textContent, /40/);
});
