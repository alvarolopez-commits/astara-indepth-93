// Minimal browser harness for the #93 tests: a static server for the project folder plus headless Chrome driven over
// the DevTools protocol (no npm dependencies; needs Node 22+ for the built-in WebSocket). Set CHROME_PATH to override Chrome.
import { spawn } from 'node:child_process';
import http from 'node:http';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

export const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..', '..');
const TYPES = { '.html': 'text/html; charset=utf-8', '.js': 'text/javascript; charset=utf-8', '.css': 'text/css', '.json': 'application/json', '.svg': 'image/svg+xml', '.webp': 'image/webp', '.png': 'image/png', '.jpg': 'image/jpeg' };

function chromePath() {
  const c = [process.env.CHROME_PATH, 'C:/Program Files/Google/Chrome/Application/chrome.exe', 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe',
    '/usr/bin/google-chrome', '/usr/bin/chromium', '/usr/bin/chromium-browser', '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'];
  const p = c.find(x => x && fs.existsSync(x));
  if (!p) throw new Error('Chrome not found: set CHROME_PATH');
  return p;
}

function serve() {
  const server = http.createServer((req, res) => {
    const u = decodeURIComponent(new URL(req.url, 'http://x').pathname);
    const f = path.join(ROOT, u === '/' ? 'index_93.html' : u);
    if (!f.startsWith(ROOT) || !fs.existsSync(f) || fs.statSync(f).isDirectory()) { res.writeHead(404); return res.end('not found'); }
    res.writeHead(200, { 'content-type': TYPES[path.extname(f)] || 'application/octet-stream' });
    fs.createReadStream(f).pipe(res);
  });
  return new Promise(r => server.listen(0, '127.0.0.1', () => r(server)));
}

class Page {
  constructor(ws) { this.ws = ws; this.id = 0; this.pending = new Map(); this.waiters = []; this.errors = [];
    ws.addEventListener('message', m => { const d = JSON.parse(m.data);
      if (d.id && this.pending.has(d.id)) { const { ok, bad } = this.pending.get(d.id); this.pending.delete(d.id); d.error ? bad(new Error(d.error.message)) : ok(d.result); }
      else if (d.method) {
        if (d.method === 'Runtime.exceptionThrown') this.errors.push(d.params.exceptionDetails.exception?.description || d.params.exceptionDetails.text);
        if (d.method === 'Runtime.consoleAPICalled' && d.params.type === 'error') this.errors.push(d.params.args.map(a => a.value ?? a.description).join(' '));
        this.waiters = this.waiters.filter(w => !(w.method === d.method && (w.fn(), true)));
      } }); }
  send(method, params = {}) { const id = ++this.id; this.ws.send(JSON.stringify({ id, method, params })); return new Promise((ok, bad) => this.pending.set(id, { ok, bad })); }
  once(method) { return new Promise(fn => this.waiters.push({ method, fn })); }
  async eval(expr) { const r = await this.send('Runtime.evaluate', { expression: expr, awaitPromise: true, returnByValue: true });
    if (r.exceptionDetails) throw new Error(r.exceptionDetails.exception?.description || r.exceptionDetails.text); return r.result.value; }
  async viewport(width, height = 900, mobile = true) {
    await this.send('Emulation.setDeviceMetricsOverride', { width, height, deviceScaleFactor: 2, mobile });
    await this.send('Emulation.setTouchEmulationEnabled', { enabled: mobile }); }
  async goto(url) { const loaded = this.once('Page.loadEventFired'); await this.send('Page.navigate', { url }); await loaded;
    await this.eval('new Promise(r => setTimeout(r, 400))'); }
}

export async function withBrowser(fn) {
  const server = await serve();
  const base = `http://127.0.0.1:${server.address().port}`;
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'indepth93-chrome-'));
  const chrome = spawn(chromePath(), ['--headless=new', '--disable-gpu', '--no-first-run', '--hide-scrollbars', `--user-data-dir=${dir}`, '--remote-debugging-port=0', 'about:blank'], { stdio: 'ignore' });
  try {
    let port; for (let i = 0; i < 100 && !port; i++) { await new Promise(r => setTimeout(r, 100));
      try { port = fs.readFileSync(path.join(dir, 'DevToolsActivePort'), 'utf8').split('\n')[0]; } catch {} }
    if (!port) throw new Error('Chrome did not start');
    const open = async () => { const t = await (await fetch(`http://127.0.0.1:${port}/json/new?about:blank`, { method: 'PUT' })).json();
      const ws = new WebSocket(t.webSocketDebuggerUrl); await new Promise((ok, bad) => { ws.onopen = ok; ws.onerror = bad; });
      const page = new Page(ws); await page.send('Page.enable'); await page.send('Runtime.enable'); return page; };
    return await fn({ base, open });
  } finally { chrome.kill(); server.close(); try { fs.rmSync(dir, { recursive: true, force: true }); } catch {} }
}
