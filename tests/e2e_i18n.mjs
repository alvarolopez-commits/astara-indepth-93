// Browser tests for the EN | ES switch and the phone layout (360, 390, 430 px; plus 1280 px for reference).
// Runs the real page in headless Chrome over the DevTools protocol. Usage: node tests/e2e_i18n.mjs   (exit code 1 on any failure)
import { withBrowser } from './lib/browser.mjs';

const WIDTHS = [360, 390, 430, 1280];
const results = []; let failed = 0;
const check = (name, ok, detail = '') => { results.push({ name, ok, detail }); if (!ok) { failed++; console.log(`  FAIL  ${name}${detail ? ' | ' + String(detail).slice(0, 400) : ''}`); } };

/* ---- code that runs inside the page ---- */
const snapshot = () => {
  const norm = s => s.replace(/\s+/g, ' ').trim();
  const text = [...document.querySelectorAll('body *')].filter(e => !e.closest('script,style')).map(e => [...e.childNodes].filter(n => n.nodeType === 3).map(n => norm(n.nodeValue)).filter(Boolean).join(' ')).filter(Boolean).join(' | ');
  const attrs = [...document.querySelectorAll('[alt],[aria-label]')].map(e => `${e.tagName}:${e.getAttribute('alt') ?? ''}:${e.getAttribute('aria-label') ?? ''}`).join(' | ');
  return { text, attrs, title: document.title, description: document.querySelector('meta[name=description]').content, lang: document.documentElement.lang,
    counts: ['#v02 .row', '#v04 .row', '#v05 .pan__row', '#v06 .row', '#v07 .row', '#v08 .row', '#lift svg', '#v03 svg', '.kfig__c', '.info__art', '.lang__b'].map(s => document.querySelectorAll(s).length).join(','), misses: [...window.__i18nMiss] };
};
const overflow = () => {
  const iw = document.documentElement.clientWidth, bad = [];
  for (const e of document.querySelectorAll('body *')) {
    if (e.closest('svg') && e.tagName !== 'svg') continue;
    const cs = getComputedStyle(e); if (cs.display === 'none' || cs.visibility === 'hidden' || e.classList.contains('sr-only')) continue;
    const r = e.getBoundingClientRect(); if (!r.width && !r.height) continue;
    if (r.right > iw + 1 || r.left < -1) bad.push(`${e.tagName.toLowerCase()}.${String(e.className?.baseVal ?? e.className).split(' ')[0]} [${Math.round(r.left)},${Math.round(r.right)}]`);
  }
  return { iw, docScroll: document.documentElement.scrollWidth, bodyScroll: document.body.scrollWidth, bad: [...new Set(bad)].slice(0, 12) };
};
const clipped = () => [...document.querySelectorAll('h1,h2,h3,.fig__title,.cover__title,.chapter-title,.kfig__v,.q__text,button,summary,figcaption,.why__k')]
  .filter(e => e.offsetParent !== null && e.scrollWidth > e.clientWidth + 1).map(e => `${e.tagName.toLowerCase()}.${String(e.className).split(' ')[0]} ${e.scrollWidth}>${e.clientWidth}`);
const legibility = () => {
  const small = [], seen = new Set();
  for (const e of document.querySelectorAll('body *')) {
    if (e.closest('svg') || e.closest('script,style')) continue;
    if (![...e.childNodes].some(n => n.nodeType === 3 && n.nodeValue.trim())) continue;
    const cs = getComputedStyle(e); if (cs.display === 'none' || cs.visibility === 'hidden') continue;
    const px = parseFloat(cs.fontSize); const key = `${e.tagName}.${e.className}|${px}`;
    if (px < 11 && !seen.has(key)) { seen.add(key); small.push(`${e.tagName.toLowerCase()}.${String(e.className).split(' ')[0]} ${px}px`); }
  }
  const svgSmall = [], seen2 = new Set();
  for (const svg of document.querySelectorAll('svg[viewBox]')) {
    const vb = svg.viewBox.baseVal; if (!vb.width || !svg.clientWidth && !svg.getBoundingClientRect().width) continue;
    const scale = svg.getBoundingClientRect().width / vb.width;
    for (const t of svg.querySelectorAll('text')) { const px = parseFloat(getComputedStyle(t).fontSize) * scale; const key = `${svg.closest('[id]')?.id || svg.getAttribute('class')}|${t.getAttribute('class')}|${px.toFixed(1)}`;
      if (px < 9 && !seen2.has(key)) { seen2.add(key); svgSmall.push(`${svg.closest('[id]')?.id || svg.getAttribute('class')} text.${t.getAttribute('class') || ''} ${px.toFixed(1)}px`); } }
  }
  return { small, svgSmall };
};
const targets = () => [...document.querySelectorAll('.lang__b, summary')].map(e => { const r = e.getBoundingClientRect(); return `${e.className || e.tagName} ${Math.round(r.width)}x${Math.round(r.height)}`; });
const englishLeft = () => {
  const stop = /\b(the|and|of|with|for|from|than|which|per kg of|is|are|not|it)\b/i, out = [];
  for (const e of document.querySelectorAll('body *')) {
    if (e.closest('script,style,ol[lang=en]') || e.closest('svg') && false) continue;
    const own = [...e.childNodes].filter(n => n.nodeType === 3).map(n => n.nodeValue.trim()).filter(Boolean).join(' ');
    if (own && stop.test(own)) out.push(own.slice(0, 80));
  }
  return out;
};
const pointNumbers = () => {   // "0.0031" or "2.27" in Spanish text (thousands such as 44.440 are fine)
  const out = [];
  for (const e of document.querySelectorAll('body *')) {
    if (e.closest('script,style,ol[lang=en]')) continue;
    const own = [...e.childNodes].filter(n => n.nodeType === 3).map(n => n.nodeValue).join(' ');
    for (const m of own.matchAll(/(?<![\w.\/])\d+\.\d+(?![\d.])/g)) if (!/^\d{1,3}\.\d{3}$/.test(m[0])) out.push(`${m[0]} in "${own.trim().slice(0, 60)}"`);
  }
  return out;
};
const tooltips = () => ({ titleAttrs: document.querySelectorAll('[title]:not(svg title)').length, tipEls: document.querySelectorAll('.tip,[role=tooltip]').length, svgTitles: document.querySelectorAll('svg title').length });
const imgLabels = () => [...document.querySelectorAll('[role=img]')].map(e => (e.getAttribute('aria-label') || '').trim()).concat([...document.querySelectorAll('img')].map(e => (e.getAttribute('alt') || '').trim()));

/* ---- the run ---- */
await withBrowser(async ({ base, open }) => {
  for (const w of WIDTHS) {
    console.log(`\n== ${w}px ==`);
    const page = await open(); await page.viewport(w, 800, w < 800);
    const tag = s => `${w}px ${s}`;
    await page.goto(`${base}/index_93.html`); await page.eval('localStorage.clear()');
    await page.goto(`${base}/index_93.html`);

    // English first
    const S0 = await page.eval(`(${snapshot})()`);
    check(tag('EN: html lang, no catalog misses'), S0.lang === 'en' && S0.misses.length === 0, JSON.stringify(S0.misses));
    let o = await page.eval(`(${overflow})()`);
    check(tag('EN: no horizontal overflow'), o.docScroll <= o.iw && o.bodyScroll <= o.iw && o.bad.length === 0, JSON.stringify(o));
    check(tag('EN: headings and controls are not clipped'), (await page.eval(`(${clipped})()`)).length === 0, JSON.stringify(await page.eval(`(${clipped})()`)));
    const leg = await page.eval(`(${legibility})()`);
    const minPx = w < 800 ? 11 : 9;   // phones: 11px; desktop: the 9px pill label is the smallest text
    const smallFor = L => L.small.filter(x => parseFloat(x.split(' ').pop()) < minPx);
    check(tag(`EN: text is at least ${minPx}px (HTML)`), smallFor(leg).length === 0, smallFor(leg).join('; '));
    check(tag('EN: chart text is at least 9px on screen'), leg.svgSmall.length === 0, leg.svgSmall.join('; '));
    const tg = await page.eval(`(${targets})()`);
    if (w < 800) check(tag('touch targets: language buttons and the sources toggle are at least 44x44px'), tg.every(t => +t.split(' ').pop().split('x')[1] >= 44 && +t.split(' ').pop().split('x')[0] >= 44), tg.join('; '));

    // tap ES with a touch event (phones) or a click (desktop): no reload
    await page.eval('window.__keep = 123');
    const pt = await page.eval(`(() => { const r = document.querySelector('.lang__b[data-lang=es]').getBoundingClientRect(); return [r.left + r.width / 2, r.top + r.height / 2]; })()`);
    if (w < 800) { await page.send('Input.dispatchTouchEvent', { type: 'touchStart', touchPoints: [{ x: pt[0], y: pt[1] }] }); await page.send('Input.dispatchTouchEvent', { type: 'touchEnd', touchPoints: [] }); }
    else { await page.send('Input.dispatchMouseEvent', { type: 'mousePressed', x: pt[0], y: pt[1], button: 'left', clickCount: 1 }); await page.send('Input.dispatchMouseEvent', { type: 'mouseReleased', x: pt[0], y: pt[1], button: 'left', clickCount: 1 }); }
    await page.eval('new Promise(r => setTimeout(r, 500))');
    check(tag(`ES: ${w < 800 ? 'a tap' : 'a click'} on the button switches language without reloading`), (await page.eval('window.__keep')) === 123 && (await page.eval('document.documentElement.lang')) === 'es');

    const S1 = await page.eval(`(${snapshot})()`);
    check(tag('ES: lang, title, description and no catalog misses'), S1.lang === 'es' && S1.title !== S0.title && S1.description !== S0.description && /kilómetro/.test(S1.title) && S1.misses.length === 0, JSON.stringify({ t: S1.title, m: S1.misses }));
    check(tag('ES: same chart marks and elements as EN'), S1.counts === S0.counts, `${S0.counts} vs ${S1.counts}`);
    check(tag('ES: buttons expose the state (aria-pressed)'), await page.eval(`document.querySelector('.lang__b[data-lang=es]').getAttribute('aria-pressed') === 'true' && document.querySelector('.lang__b[data-lang=en]').getAttribute('aria-pressed') === 'false'`));
    const left = await page.eval(`(${englishLeft})()`);
    check(tag('ES: no English left outside the sources list'), left.length === 0, left.slice(0, 6).join(' / '));
    const pn = await page.eval(`(${pointNumbers})()`);
    check(tag('ES: decimal commas in every number'), pn.length === 0, pn.slice(0, 6).join(' / '));
    const labels = await page.eval(`(${imgLabels})()`);
    check(tag('ES: every chart and image has a non-empty accessible label'), labels.length > 10 && labels.every(Boolean), String(labels.length));
    check(tag('ES: accessible labels changed language'), S1.attrs !== S0.attrs && !/lifts 1 kg|Cost of transport of/.test(S1.attrs));
    check(tag('ES: language group label is translated'), await page.eval(`document.querySelector('.lang').getAttribute('aria-label') === 'Idioma'`));
    o = await page.eval(`(${overflow})()`);
    check(tag('ES: no horizontal overflow'), o.docScroll <= o.iw && o.bodyScroll <= o.iw && o.bad.length === 0, JSON.stringify(o));
    check(tag('ES: headings and controls are not clipped'), (await page.eval(`(${clipped})()`)).length === 0, JSON.stringify(await page.eval(`(${clipped})()`)));
    const leg2 = await page.eval(`(${legibility})()`);
    check(tag(`ES: text is at least ${minPx}px (HTML)`), smallFor(leg2).length === 0, smallFor(leg2).join('; '));
    check(tag('ES: chart text is at least 9px on screen'), leg2.svgSmall.length === 0, leg2.svgSmall.join('; '));

    // persistence and URL
    await page.goto(`${base}/index_93.html`);
    check(tag('ES: the choice survives a reload'), (await page.eval('document.documentElement.lang')) === 'es');
    await page.goto(`${base}/index_93.html?lang=en`);
    check(tag('?lang=en overrides the stored choice'), (await page.eval('document.documentElement.lang')) === 'en');
    await page.goto(`${base}/index_93.html?lang=es`);
    check(tag('?lang=es opens the page in Spanish'), (await page.eval('document.documentElement.lang')) === 'es' && /Ballena/.test(await page.eval('document.querySelector("#lift").textContent')));

    // back to English, three round trips: the content must come back exactly
    for (let i = 0; i < 3; i++) { await page.eval(`document.querySelector('.lang__b[data-lang=en]').click(); document.querySelector('.lang__b[data-lang=es]').click()`); }
    await page.eval(`document.querySelector('.lang__b[data-lang=en]').click()`); await page.eval('new Promise(r => setTimeout(r, 300))');
    const S2 = await page.eval(`(${snapshot})()`);
    check(tag('EN again: text, labels, title and description identical to the first load'), S2.text === S0.text && S2.attrs === S0.attrs && S2.title === S0.title && S2.description === S0.description, S2.text === S0.text ? 'attrs/meta differ' : 'text differs');
    check(tag('EN again: no duplicated charts or legends'), S2.counts === S0.counts);

    // layout changes while in Spanish (rotation): re-drawn charts keep the language and fit
    await page.eval(`document.querySelector('.lang__b[data-lang=es]').click()`);
    await page.viewport(w < 800 ? 844 : 1024, w < 800 ? 390 : 700, w < 800); await page.eval('new Promise(r => setTimeout(r, 600))');
    o = await page.eval(`(${overflow})()`); const S3 = await page.eval(`(${snapshot})()`);
    check(tag('ES after a resize/rotation: still Spanish, no overflow, no misses'), S3.lang === 'es' && o.docScroll <= o.iw && o.bad.length === 0 && S3.misses.length === 0, JSON.stringify(o));

    if (w === WIDTHS[0]) {
      const tt = await page.eval(`(${tooltips})()`);
      check('the page has no tooltips to translate (no title attributes, no tooltip elements)', tt.titleAttrs === 0 && tt.tipEls === 0, JSON.stringify(tt));
    }
    check(tag('no console errors'), page.errors.length === 0, page.errors.join(' / '));
  }
});

const passed = results.filter(r => r.ok).length;
console.log(`\n${passed}/${results.length} browser checks passed${failed ? `, ${failed} FAILED` : ''}`);
process.exit(failed ? 1 : 0);
