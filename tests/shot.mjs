// Screenshot helper for looking at the page at phone widths: node tests/shot.mjs <lang> <width> <css selector> <out.png>
import fs from 'node:fs';
import { withBrowser } from './lib/browser.mjs';

const [lang, width, selector, out] = process.argv.slice(2);
await withBrowser(async ({ base, open }) => {
  const page = await open(); await page.viewport(+width, 900, +width < 800);
  await page.goto(`${base}/index_93.html?lang=${lang}`);
  await page.eval(`document.querySelectorAll('.reveal').forEach(e => e.classList.add('visible')); new Promise(r => setTimeout(r, 1800))`);
  const r = await page.eval(`(() => { const e = document.querySelector(${JSON.stringify(selector)}); const b = e.getBoundingClientRect(); return { x: 0, y: b.top + scrollY - 8, width: innerWidth, height: b.height + 16 }; })()`);
  const shot = await page.send('Page.captureScreenshot', { format: 'png', captureBeyondViewport: true, clip: { ...r, scale: 1 } });
  fs.writeFileSync(out, Buffer.from(shot.data, 'base64'));
  console.log('saved', out, r);
});
