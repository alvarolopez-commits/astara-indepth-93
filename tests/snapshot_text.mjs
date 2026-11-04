// Writes what a reader sees (text, head metadata, accessibility labels, chart marks) for EN and ES, so two builds can be compared.
// Usage: node tests/snapshot_text.mjs <out.json> [width]
import fs from 'node:fs';
import { withBrowser } from './lib/browser.mjs';

const out = process.argv[2], width = +(process.argv[3] || 1440);
const SNAP = `(() => {
  const norm = s => s.replace(/\\s+/g, ' ').trim();
  const lines = [...document.querySelectorAll('body *')].filter(e => !['SCRIPT','STYLE','svg'].includes(e.tagName) && !e.closest('script,style'))
    .map(e => [...e.childNodes].filter(n => n.nodeType === 3).map(n => norm(n.nodeValue)).filter(Boolean).join(' ')).filter(Boolean);
  const attrs = [...document.querySelectorAll('[alt],[aria-label],[title]')].map(e => ['alt','aria-label','title'].filter(a => e.hasAttribute(a)).map(a => a + '=' + norm(e.getAttribute(a))).join('|'));
  const svgText = [...document.querySelectorAll('svg text')].map(e => norm(e.textContent));
  const rows = { ladder: document.querySelectorAll('#v02 .row').length, podium: document.querySelectorAll('#v04 .row').length, human: document.querySelectorAll('#v05 .pan__row').length,
    robots: document.querySelectorAll('#v06 .row').length, people: document.querySelectorAll('#v07 .row').length, goods: document.querySelectorAll('#v08 .row').length, svgs: document.querySelectorAll('svg').length };
  return { lang: document.documentElement.lang, title: document.title, description: document.querySelector('meta[name=description]')?.content, lines, attrs, svgText, rows };
})()`;

const res = {};
await withBrowser(async ({ base, open }) => {
  for (const lang of ['en', 'es']) {
    const page = await open(); await page.viewport(width, 900, width < 800);
    await page.goto(`${base}/index_93.html?lang=${lang}`);
    await page.eval('new Promise(r => setTimeout(r, 1500))');
    res[lang] = await page.eval(SNAP); res[lang].errors = page.errors;
  }
});
fs.writeFileSync(out, JSON.stringify(res, null, 1));
console.log('written', out, Object.fromEntries(Object.entries(res).map(([k, v]) => [k, { lines: v.lines.length, svgText: v.svgText.length, errors: v.errors.length }])));
