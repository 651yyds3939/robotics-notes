#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
PREVIEW_HTML="$ROOT/robot_system_integration_preview.html"
PREVIEW_PNG="$ROOT/assets/integration_preview.png"

python3 "$ROOT/scripts/md_mermaid_to_html.py" \
  "$ROOT/robotics/robot_system_integration.md" \
  "$ROOT/robot_system_integration.html" \
  --preview "$PREVIEW_HTML" \
  --preview-href "./robot_system_integration.html" \
  --title "机器人系统集成 · Mermaid 预览" \
  --tip '📊 运行时数据流与控制闭环。修改 <code>robotics/robot_system_integration.md</code> 后运行 <code>./regenerate_integration_html.sh</code>'

source "$ROOT/scripts/preview_png.sh"
screenshot_html "$PREVIEW_HTML" "$PREVIEW_PNG" 980 7500 30000 || true
