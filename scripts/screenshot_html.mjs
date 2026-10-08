// Capture native HTML/SVG only after rendering, using Chrome's debugging protocol.
// Node >= 22 supplies WebSocket; no npm packages or remote browser service needed.
import { spawn } from 'node:child_process';
import { mkdtemp, mkdir, writeFile, rm } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { dirname, join, resolve } from 'node:path';
import { pathToFileURL } from 'node:url';

const [chrome, source, destination, widthArg, heightArg, mode] = process.argv.slice(2);
if (mode && mode !== '--full-markmap') throw new Error(`Unknown capture mode: ${mode}`);
const fullMarkmap = mode === '--full-markmap';
if (!chrome || !source || !destination || typeof WebSocket === 'undefined') {
  throw new Error('Usage: node >= 22 screenshot_html.mjs chrome source.html output.png width height');
}
const width = Number(widthArg || 1200), height = Number(heightArg || 8000);
if (!Number.isInteger(width) || !Number.isInteger(height) || width < 100 || height < 100) {
  throw new Error('Invalid viewport size');
}
const profile = await mkdtemp(join(tmpdir(), 'robotics-preview-'));
const child = spawn(chrome, ['--headless=new', '--disable-gpu', '--no-sandbox',
  '--remote-debugging-port=0', `--user-data-dir=${profile}`, '--no-first-run',
  '--no-default-browser-check', 'about:blank'], { stdio: ['ignore', 'ignore', 'pipe'] });
let socket;
const timer = setTimeout(() => child.kill(), 60000);
try {
  const endpoint = await new Promise((resolveEndpoint, reject) => {
    let log = '';
    child.stderr.on('data', data => {
      log = (log + data.toString()).slice(-8000);
      const match = log.match(/DevTools listening on (ws:\/\/[^\s]+)/);
      if (match) resolveEndpoint(match[1]);
    });
    child.once('error', reject);
    child.once('exit', () => reject(new Error('Chrome exited before debugging was ready')));
  });
  socket = new WebSocket(endpoint);
  await new Promise((ready, reject) => {
    socket.addEventListener('open', ready, { once: true });
    socket.addEventListener('error', reject, { once: true });
  });
  const pending = new Map();
  let id = 0;
  socket.addEventListener('message', event => {
    const message = JSON.parse(event.data);
    const callback = pending.get(message.id);
    if (callback) {
      pending.delete(message.id);
      message.error ? callback.reject(new Error(message.error.message)) : callback.resolve(message.result);
    }
  });
  socket.addEventListener('close', () => {
    for (const callback of pending.values()) callback.reject(new Error('Chrome connection closed'));
    pending.clear();
  });
  const send = (method, params = {}, sessionId) => new Promise((resolveCall, reject) => {
    const messageId = ++id;
    pending.set(messageId, { resolve: resolveCall, reject });
    socket.send(JSON.stringify({ id: messageId, method, params, ...(sessionId ? { sessionId } : {}) }));
  });
  const { targetId } = await send('Target.createTarget', { url: 'about:blank' });
  const { sessionId } = await send('Target.attachToTarget', { targetId, flatten: true });
  const call = (method, params) => send(method, params, sessionId);
  await call('Page.enable');
  await call('Emulation.setDeviceMetricsOverride', { width, height, deviceScaleFactor: 1, mobile: false });
  await call('Emulation.setEmulatedMedia', { features: [{ name: 'prefers-color-scheme', value: 'light' }] });
  await call('Page.navigate', { url: pathToFileURL(resolve(source)).href });
  const start = Date.now();
  while (true) {
    const result = await call('Runtime.evaluate', {
      expression: `(() => ({
        status: window.__diagramRenderStatus,
        ready: document.readyState === 'complete' && document.fonts.status === 'loaded',
        nodes: document.querySelectorAll('#mindmap .markmap-node').length,
        diagrams: document.querySelectorAll('pre.mermaid svg').length,
        expected: document.querySelectorAll('pre.mermaid').length,
        error: !!document.querySelector('svg .error-text')
      }))()`, returnByValue: true,
    });
    const state = result.result.value;
    if (state.error || state.status === 'error') throw new Error('Diagram rendering failed');
    if (state.ready && (state.nodes > 0 ||
        (state.status === 'ready' && state.diagrams === state.expected && state.diagrams > 0))) break;
    if (Date.now() - start > 40000) throw new Error('Timed out waiting for rendered SVG');
    await new Promise(ready => setTimeout(ready, 100));
  }
  // Markmap's fit animation follows data layout; let it settle after fonts load.
  await new Promise(ready => setTimeout(ready, 1000));
  await call('Runtime.evaluate', {
    // UI/footer are useful in the interactive page but must not expand thumbnail crops.
    expression: `if (window.mm) {
      for (const element of document.body.children) {
        if (!['svg', 'script'].includes(element.tagName.toLowerCase())) element.style.display = 'none';
      }
    }`,
  });
  let captureWidth = width, captureHeight = height;
  if (fullMarkmap) {
    const result = await call('Runtime.evaluate', {
      expression: `(() => {
        const svg = document.querySelector('#mindmap');
        const graph = svg?.querySelector('g');
        if (!graph || !window.mm) throw new Error('Full Markmap export requires a rendered mindmap');
        const count = node => 1 + (node.children || []).reduce((sum, child) => sum + count(child), 0);
        const expected = count(window.mm.state.data);
        const actual = svg.querySelectorAll('.markmap-node').length;
        if (actual !== expected) throw new Error('Mindmap contains collapsed or missing nodes: ' + actual + '/' + expected);
        const box = graph.getBBox();
        const padding = 32;
        const width = Math.ceil(box.width + padding * 2);
        const height = Math.ceil(box.height + padding * 2);
        window.mm.setOptions({autoFit: false, duration: 0});
        // Keep the data layout, remove only the viewport fit/zoom transform.
        graph.removeAttribute('transform');
        svg.setAttribute('viewBox', [box.x - padding, box.y - padding, width, height].join(' '));
        svg.style.width = width + 'px';
        svg.style.height = height + 'px';
        document.body.style.width = width + 'px';
        document.body.style.height = height + 'px';
        document.documentElement.style.overflow = 'hidden';
        // Screenshot capture may resize the viewport. Freeze a static SVG copy so
        // Markmap's resize/fit listeners cannot re-center the live graph mid-shot.
        svg.replaceWith(svg.cloneNode(true));
        return {width, height, actual, expected};
      })()`, returnByValue: true,
    });
    if (result.exceptionDetails) throw new Error(result.exceptionDetails.exception?.description || 'Full mindmap export failed');
    const bounds = result.result.value;
    captureWidth = bounds.width;
    captureHeight = bounds.height;
    console.log(`Full mindmap: ${bounds.actual}/${bounds.expected} nodes, ${captureWidth}x${captureHeight}`);
    await call('Emulation.setDeviceMetricsOverride', {
      width: captureWidth, height: captureHeight, deviceScaleFactor: 1, mobile: false,
    });
    await call('Runtime.evaluate', {
      expression: 'new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(resolve)))',
      awaitPromise: true,
    });
    const validation = await call('Runtime.evaluate', {
      expression: `(() => {
        const svg = document.querySelector('#mindmap');
        const bounds = svg.getBoundingClientRect();
        return [...svg.querySelectorAll('foreignObject')].every(node => {
          const rect = node.getBoundingClientRect();
          return rect.left >= bounds.left && rect.right <= bounds.right &&
                 rect.top >= bounds.top && rect.bottom <= bounds.bottom;
        });
      })()`, returnByValue: true,
    });
    if (!validation.result.value) throw new Error('A mindmap label falls outside the exported image');
  }
  const { data } = await call('Page.captureScreenshot', {
    format: 'png', fromSurface: true,
    captureBeyondViewport: true,
    clip: { x: 0, y: 0, width: captureWidth, height: captureHeight, scale: 1 },
  });
  await mkdir(dirname(resolve(destination)), { recursive: true });
  await writeFile(destination, Buffer.from(data, 'base64'));
  console.log(`Screenshot: ${destination} (${captureWidth}x${captureHeight}, SVG ready)`);
} finally {
  clearTimeout(timer);
  if (socket) socket.close();
  if (child.exitCode === null && child.signalCode === null) {
    child.kill();
    await new Promise(ready => child.once('exit', ready));
  }
  // Only remove the disposable profile created above, never a user/workspace path.
  await rm(profile, { recursive: true, force: true, maxRetries: 3, retryDelay: 100 });
}
