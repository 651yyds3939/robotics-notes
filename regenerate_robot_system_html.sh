#!/usr/bin/env bash
# 从 robot_system.md 预渲染 robot_system_photo.html（离线 Markmap）
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
MD="$ROOT/robot_system.md"
OUT="$ROOT/robot_system_photo.html"
LIB="$ROOT/assets/markmap/markmap-lib.iife.js"
JSON_TMP="$(mktemp)"

node << NODE > "$JSON_TMP"
const fs = require('fs');
const vm = require('vm');
const code = fs.readFileSync('$LIB', 'utf8');
const sandbox = {
  markmap: {},
  window: { katex: undefined },
  document: { head: { append: () => {} }, createElement: () => ({}) },
};
vm.createContext(sandbox);
vm.runInContext(code, sandbox);
const md = fs.readFileSync('$MD', 'utf8');
const { root } = new sandbox.markmap.Transformer().transform(md);
process.stdout.write(JSON.stringify(root));
process.exit(0);
NODE

python3 << PY
import json
from pathlib import Path

root_json = Path('$JSON_TMP').read_text(encoding='utf-8')
json.loads(root_json)  # validate
root_js = root_json.replace('</', r'<\/')

html = f'''<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>机器人全链路系统 · Markmap</title>
<style>
* {{ margin: 0; padding: 0; }}
html {{
  font-family: ui-sans-serif, system-ui, sans-serif, "Apple Color Emoji",
    "Segoe UI Emoji", "Segoe UI Symbol", "Noto Color Emoji";
}}
#mindmap {{ display: block; width: 100vw; height: 100vh; }}
.markmap-dark {{ background: #27272a; color: white; }}
.markmap-dark a {{ color: #93c5fd; }}
a {{ color: #2563eb; }}
</style>
<link rel="stylesheet" href="assets/markmap/markmap-toolbar.css" />
</head>
<body>
<svg id="mindmap"></svg>
<script src="assets/markmap/d3.min.js"></script>
<script src="assets/markmap/markmap-lib.iife.js"></script>
<script src="assets/markmap/markmap-view.js"></script>
<script src="assets/markmap/markmap-toolbar.js"></script>
<script>
(function () {{
  try {{
    const {{ Markmap, deriveOptions, Toolbar }} = window.markmap;
    const root = {root_js};
    const mm = Markmap.create(
      '#mindmap',
      deriveOptions({{
        maxWidth: 360,
        initialExpandLevel: 2,
        colorFreezeLevel: 2,
        autoFit: true,
      }}),
      root
    );
    window.mm = mm;
    const refit = () => mm.fit();
    requestAnimationFrame(refit);
    window.addEventListener('load', () => setTimeout(refit, 50));
    window.addEventListener('resize', refit);
    if (window.matchMedia('(prefers-color-scheme: dark)').matches) {{
      document.documentElement.classList.add('markmap-dark');
    }}
    if (Toolbar) {{
      try {{
        const {{ el }} = Toolbar.create(mm);
        el.style.cssText = 'position:absolute;bottom:20px;right:20px';
        document.body.append(el);
      }} catch (toolbarErr) {{
        console.warn('Toolbar skipped:', toolbarErr);
      }}
    }}
  }} catch (err) {{
    document.body.innerHTML =
      '<pre style="padding:24px;color:#b91c1c;">Markmap 渲染失败: ' +
      err +
      '</pre>';
    console.error(err);
  }}
}})();
</script>
<p style="position:fixed;left:12px;bottom:8px;font-size:12px;color:#666;">
  离线版 · 由 robot_system.md 预渲染 · 更新 md 后运行 regenerate_robot_system_html.sh
</p>
</body>
</html>
'''
Path('$OUT').write_text(html, encoding='utf-8')
print('Wrote', '$OUT', 'bytes', len(html))
PY

rm -f "$JSON_TMP"
