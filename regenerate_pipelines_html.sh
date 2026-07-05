#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
PREVIEW_HTML="$ROOT/robot_software_pipelines_preview.html"
PREVIEW_PNG="$ROOT/assets/pipelines_preview.png"

python3 "$ROOT/scripts/md_mermaid_to_html.py" \
  "$ROOT/robotics/robot_software_pipelines.md" \
  "$ROOT/robot_software_pipelines.html" \
  --preview "$PREVIEW_HTML" \
  --preview-href "./robot_software_pipelines.html" \
  --title "二次开发软件管线 · Mermaid 预览" \
  --tip '📊 软件管线工序图。修改 <code>robotics/robot_software_pipelines.md</code> 后运行 <code>./regenerate_pipelines_html.sh</code>'

source "$ROOT/scripts/preview_png.sh"
screenshot_html "$PREVIEW_HTML" "$PREVIEW_PNG" 980 7500 30000 || true
