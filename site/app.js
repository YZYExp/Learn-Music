(() => {
  'use strict';
  const body = document.body;
  const base = body.dataset.base;
  const slug = body.dataset.slug;
  const readKey = 'hearing-instruments:last-read';
  if (slug) {
    try { localStorage.setItem(readKey, JSON.stringify({ slug, title: body.dataset.title })); } catch (_) {}
    const details = document.querySelector('.book-nav details');
    if (details && window.matchMedia('(max-width:650px)').matches) details.open = false;
    const bar = document.querySelector('.reader-progress');
    const update = () => { const h = document.documentElement.scrollHeight - window.innerHeight; if (bar) bar.style.width = (h > 0 ? 100 * window.scrollY / h : 0) + '%'; };
    window.addEventListener('scroll', update, { passive: true }); update();
  } else {
    const resume = document.querySelector('#resume');
    try {
      const last = JSON.parse(localStorage.getItem(readKey));
      if (resume && last && /^[a-z0-9-]+$/.test(last.slug)) {
        resume.textContent = '继续阅读 · ' + last.title;
        resume.href = base + 'read/' + last.slug + '/'; resume.hidden = false;
      }
    } catch (_) {}
  }
  const cards = [...document.querySelectorAll('.chapter-card')];
  const buttons = document.querySelectorAll('.filter');
  let active = 'all';
  const input = document.querySelector('#chapter-search');
  const status = document.querySelector('#search-status');
  const results = document.querySelector('#search-results');
  let indexPromise;
  let revision = 0;
  const filter = async () => {
    const q = input ? input.value.trim().toLocaleLowerCase() : '';
    const now = ++revision;
    for (const card of cards) card.hidden = q.length > 0 || (active !== 'all' && card.dataset.group !== active);
    if (!input || !results) return;
    results.replaceChildren();
    if (!q) { status.textContent = ''; return; }
    status.textContent = '正在查找正文…';
    try {
      indexPromise ||= fetch(base + 'search.json').then(r => { if (!r.ok) throw Error(); return r.json(); });
      const index = await indexPromise;
      if (now !== revision) return;
      const hits = index.filter(x => (active === 'all' || x.group === active) && (x.title + ' ' + x.text).toLocaleLowerCase().includes(q));
      status.textContent = hits.length ? `找到 ${hits.length} 个章节` : '没有找到匹配章节，请试试乐器名或原理词。';
      for (const hit of hits) {
        const a = document.createElement('a'); a.href = base + 'read/' + hit.slug + '/';
        const title = document.createElement('strong'); title.textContent = hit.id + ' · ' + hit.title;
        const p = document.createElement('p'); const start = Math.max(0, hit.text.toLocaleLowerCase().indexOf(q) - 30);
        p.textContent = (start ? '…' : '') + hit.text.slice(start, start + 110) + '…';
        a.append(title, p); results.append(a);
      }
    } catch (_) { if (now === revision) status.textContent = '正文搜索暂时不可用；可通过下方章节分类浏览。'; for (const c of cards) c.hidden = active !== 'all' && c.dataset.group !== active; }
  };
  for (const button of buttons) button.addEventListener('click', () => {
    active = button.dataset.group;
    for (const b of buttons) b.setAttribute('aria-pressed', String(b === button)); filter();
  });
  if (input) input.addEventListener('input', filter);
})();
