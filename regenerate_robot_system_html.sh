#!/usr/bin/env bash
# 从 robot_system.md 预渲染 robot_system_photo.html（离线 Markmap）
# 并生成全展开预览图 assets/robot_system_preview.png（供 README 首页展示）
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
MD="$ROOT/robot_system.md"
OUT="$ROOT/robot_system_photo.html"
PREVIEW_HTML="$ROOT/robot_system_preview.html"
PREVIEW_PNG="$ROOT/assets/robot_system_preview.png"
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

export ROOT_JSON_TMP="$JSON_TMP"
export OUT="$OUT"
export PREVIEW_HTML="$PREVIEW_HTML"

python3 << 'PY'
import json
import os
import re
from pathlib import Path

GITHUB_REPO = "https://github.com/651yyds3939/robotics-notes"
BRANCH = "master"
HTML_PREVIEW = "https://htmlpreview.github.io/?https://raw.githubusercontent.com/651yyds3939/robotics-notes/master"

root_json = Path(os.environ["ROOT_JSON_TMP"]).read_text(encoding="utf-8")
root = json.loads(root_json)
out = Path(os.environ["OUT"])
preview_html = Path(os.environ["PREVIEW_HTML"])


def rewrite_href(href: str) -> str:
    if href.startswith(("http://", "https://", "mailto:", "#")):
        return href
    path = href[2:] if href.startswith("./") else href
    anchor = ""
    if "#" in path:
        path, frag = path.split("#", 1)
        anchor = "#" + frag
    if not path:
        return href
    if path.endswith("/"):
        return f"{GITHUB_REPO}/tree/{BRANCH}/{path.rstrip('/')}{anchor}"
    if path.endswith(".html"):
        if path in ("robot_system_preview.html", "robot_system_photo.html"):
            return f"{HTML_PREVIEW}/{path}{anchor}"
        return f"{GITHUB_REPO}/blob/{BRANCH}/{path}{anchor}"
    return f"{GITHUB_REPO}/blob/{BRANCH}/{path}{anchor}"


def rewrite_content(content: str) -> str:
    def repl(match):
        href = match.group(1)
        return f'href="{rewrite_href(href)}"'

    return re.sub(r'href="([^"]+)"', repl, content)


def rewrite_tree(node: dict) -> None:
    if node.get("content"):
        node["content"] = rewrite_content(node["content"])
    for child in node.get("children", []):
        rewrite_tree(child)


root_interactive = json.loads(json.dumps(root))
root_preview = json.loads(json.dumps(root))
rewrite_tree(root_preview)

root_js = json.dumps(root_interactive, ensure_ascii=False).replace("</", r"<\/")
root_preview_js = json.dumps(root_preview, ensure_ascii=False).replace("</", r"<\/")

def build_html(title, expand_level, max_scale, show_toolbar, footer_note, root_data_js):
    toolbar_block = ""
    if show_toolbar:
        toolbar_block = """
    if (Toolbar) {
      try {
        const { el } = Toolbar.create(mm);
        el.style.cssText = 'position:absolute;bottom:20px;right:20px';
        document.body.append(el);
      } catch (toolbarErr) {
        console.warn('Toolbar skipped:', toolbarErr);
      }
    }"""
    footer = ""
    if footer_note:
        footer = f"""
<p style="position:fixed;left:12px;bottom:8px;font-size:12px;color:#666;">
  {footer_note}
</p>"""

    return f"""<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>{title}</title>
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
    const root = {root_data_js};
    const mm = Markmap.create(
      '#mindmap',
      deriveOptions({{
        maxWidth: 300,
        initialExpandLevel: {expand_level},
        colorFreezeLevel: 2,
        autoFit: true,
        maxInitialScale: {max_scale},
        fitRatio: 0.98,
      }}),
      root
    );
    window.mm = mm;
    const refit = () => mm.fit({max_scale});
    requestAnimationFrame(refit);
    window.addEventListener('load', () => setTimeout(refit, 200));
    window.addEventListener('resize', refit);
    if (window.matchMedia('(prefers-color-scheme: dark)').matches) {{
      document.documentElement.classList.add('markmap-dark');
    }}{toolbar_block}
  }} catch (err) {{
    document.body.innerHTML =
      '<pre style="padding:24px;color:#b91c1c;">Markmap 渲染失败: ' +
      err +
      '</pre>';
    console.error(err);
  }}
}})();
</script>{footer}
</body>
</html>
"""

interactive = build_html(
    "机器人全链路系统 · Markmap",
    2,
    2,
    True,
    "离线版 · 由 robot_system.md 预渲染 · 更新 md 后运行 regenerate_robot_system_html.sh",
    root_js,
)
preview = build_html(
    "机器人全链路系统 · 全展开预览",
    -1,
    20,
    True,
    "在线交互版 · 鼠标拖动画布平移 · 滚轮缩放 · 链接跳转 GitHub 渲染页",
    root_preview_js,
)

out.write_text(interactive, encoding="utf-8")
print("Wrote", out, "bytes", len(interactive))
preview_html.write_text(preview, encoding="utf-8")
print("Wrote", preview_html, "bytes", len(preview))
PY

rm -f "$JSON_TMP"

PREVIEW_W=14000
PREVIEW_H=10000
if command -v google-chrome >/dev/null 2>&1; then
  google-chrome --headless=new --disable-gpu --no-sandbox \
    --window-size="${PREVIEW_W},${PREVIEW_H}" \
    --force-device-scale-factor=1 \
    --run-all-compositor-stages-before-draw \
    --virtual-time-budget=15000 \
    --screenshot="$PREVIEW_PNG" \
    "file://$PREVIEW_HTML" 2>/dev/null \
    && echo "Wrote $PREVIEW_PNG (${PREVIEW_W}x${PREVIEW_H}, all nodes expanded)" \
    || echo "Warning: preview PNG skipped (chrome screenshot failed)" >&2
else
  echo "Warning: google-chrome not found; skip $PREVIEW_PNG" >&2
fi
