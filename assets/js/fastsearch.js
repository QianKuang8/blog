import * as params from '@params';

// PaperMod override: input-driven search, readable results and native focus.
const searchBox = document.getElementById('searchbox');
const input = document.getElementById('searchInput');
const resultsList = document.getElementById('searchResults');
const status = document.getElementById('searchStatus');
const retry = document.getElementById('searchRetry');
let fuse;
let indexState = 'idle';
let composing = false;

function queryPattern(query) {
    const terms = [...new Set([query, ...query.split(/\s+/)].filter(Boolean))];
    return new RegExp(terms.sort((a, b) => b.length - a.length)
        .map(term => term.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')).join('|'), 'giu');
}

function appendHighlighted(element, text, query) {
    let offset = 0;
    for (const match of text.matchAll(queryPattern(query))) {
        element.append(document.createTextNode(text.slice(offset, match.index)));
        const mark = document.createElement('mark');
        mark.textContent = match[0];
        element.append(mark);
        offset = match.index + match[0].length;
    }
    element.append(document.createTextNode(text.slice(offset)));
}

function resultSnippet(item, query) {
    const sources = [
        { text: item.summary, label: '摘要' },
        { text: item.content, label: '正文命中' }
    ].map(source => ({ ...source, text: (source.text || '').replace(/\s+/g, ' ').trim() }));
    const matched = sources.find(source => queryPattern(query).test(source.text));
    const source = matched || sources.find(source => source.text);
    if (!source) return null;
    const match = matched && queryPattern(query).exec(source.text);
    let start = match ? Math.max(0, match.index - 38) : 0;
    // Keep a UTF-16 surrogate pair intact when an excerpt starts near an emoji.
    if (start && /[\uDC00-\uDFFF]/.test(source.text[start])) start -= 1;
    const excerpt = [...source.text.slice(start)].slice(0, 150).join('');
    return {
        // Fuzzy matches may have no literal keyword; their text is only a summary.
        label: matched ? source.label : '摘要',
        text: (start ? '…' : '') + excerpt + (start + excerpt.length < source.text.length ? '…' : '')
    };
}

function createResult(item, query) {
    let url;
    try {
        url = new URL(item.permalink, window.location.href);
    } catch {
        return null;
    }
    if (!['http:', 'https:'].includes(url.protocol)) return null;
    const li = document.createElement('li');
    li.className = 'search-result';
    const link = document.createElement('a');
    link.className = 'search-result-link';
    link.href = url.href;
    const heading = document.createElement('h2');
    appendHighlighted(heading, item.title, query);
    link.append(heading);

    const meta = document.createElement('div');
    meta.className = 'search-result-meta';
    if (item.category) {
        const category = document.createElement('span');
        category.textContent = item.category;
        meta.append(category);
    }
    if (item.date) {
        const date = document.createElement('time');
        date.dateTime = item.date;
        date.textContent = item.date;
        meta.append(date);
    }
    link.append(meta);

    const snippet = resultSnippet(item, query);
    if (snippet) {
        const excerpt = document.createElement('p');
        excerpt.className = 'search-result-snippet';
        const label = document.createElement('span');
        label.className = 'search-snippet-label';
        label.textContent = `${snippet.label} · `;
        excerpt.append(label);
        appendHighlighted(excerpt, snippet.text, query);
        link.append(excerpt);
    }
    li.append(link);
    return li;
}

function search() {
    resultsList.replaceChildren();
    if (indexState !== 'ready') return;
    const query = input.value.trim();
    if (!query) {
        status.textContent = '输入关键词，搜索标题、摘要和全文。';
        return;
    }
    const fragment = document.createDocumentFragment();
    let count = 0;
    for (const result of fuse.search(query)) {
        const card = createResult(result.item, query);
        if (card) {
            fragment.append(card);
            count += 1;
        }
    }
    resultsList.append(fragment);
    status.textContent = count ? `找到 ${count} 条结果` : '未找到相关文章，试试更短的关键词。';
}

async function loadIndex() {
    if (indexState === 'loading') return;
    indexState = 'loading';
    status.textContent = '正在加载搜索…';
    resultsList.setAttribute('aria-busy', 'true');
    retry.hidden = true;
    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), 15000);
    try {
        const response = await fetch(searchBox.dataset.indexUrl, { signal: controller.signal });
        if (!response.ok) throw new Error('Search index unavailable');
        const data = await response.json();
        if (!Array.isArray(data) || data.some(item => !item ||
            typeof item.title !== 'string' || typeof item.permalink !== 'string' ||
            typeof item.summary !== 'string' || typeof item.content !== 'string')) {
            throw new Error('Invalid search index');
        }
        const options = params.fuseOpts || {};
        fuse = new Fuse(data, {
            isCaseSensitive: options.iscasesensitive ?? false,
            minMatchCharLength: options.minmatchcharlength ?? 1,
            shouldSort: true,
            ignoreLocation: true,
            threshold: options.threshold ?? 0.3,
            keys: options.keys ?? [
                { name: 'title', weight: 0.55 },
                { name: 'summary', weight: 0.3 },
                { name: 'content', weight: 0.15 }
            ]
        });
        indexState = 'ready';
        // A reader can type before the request finishes, or while retrying it.
        if (!composing) search();
        else status.textContent = '输入关键词，搜索标题、摘要和全文。';
    } catch {
        indexState = 'error';
        resultsList.replaceChildren();
        status.textContent = '暂时无法搜索，请重试。';
        retry.hidden = false;
    } finally {
        clearTimeout(timeout);
        resultsList.setAttribute('aria-busy', 'false');
    }
}

input.addEventListener('compositionstart', () => { composing = true; });
input.addEventListener('compositionend', () => {
    composing = false;
    search();
});
input.addEventListener('input', event => {
    if (!composing && !event.isComposing) search();
});
// Safari's native clear button also emits a search event.
input.addEventListener('search', () => { if (!composing) search(); });
retry.addEventListener('click', () => {
    input.focus();
    loadIndex();
});

searchBox.addEventListener('keydown', event => {
    if (composing || event.isComposing || event.altKey || event.ctrlKey || event.metaKey) return;
    const active = document.activeElement;
    if (event.key === 'Escape') {
        event.preventDefault();
        input.value = '';
        search();
        input.focus();
        return;
    }
    if (!['ArrowDown', 'ArrowUp'].includes(event.key)) return;
    const links = [...resultsList.querySelectorAll('.search-result-link')];
    const current = links.indexOf(active);
    if (active !== input && current === -1) return;
    if (!links.length) return;
    event.preventDefault();
    if (event.key === 'ArrowDown') links[Math.min(current + 1, links.length - 1)].focus();
    else if (current <= 0) input.focus();
    else links[current - 1].focus();
});

// This script is deferred: the DOM is ready without waiting for images/onload.
loadIndex();
