#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
PREVIEW_HTML="$ROOT/robot_development_lifecycle_preview.html"
PREVIEW_PNG="$ROOT/assets/lifecycle_preview.png"

python3 "$ROOT/scripts/md_lifecycle_to_html.py"

# shellcheck source=scripts/preview_png.sh
source "$ROOT/scripts/preview_png.sh"
# 仅包住 Mermaid 内容，高度不必过大（后续 normalize 会裁底）
screenshot_html "$PREVIEW_HTML" "$PREVIEW_PNG" 980 7500 30000 || true
