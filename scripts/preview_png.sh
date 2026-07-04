#!/usr/bin/env bash
# 将本地 HTML 截图为 PNG（裁边与统一尺寸见 normalize_readme_previews.py）
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

screenshot_html() {
  local html_path="$1"
  local png_path="$2"
  local width="${3:-1200}"
  local height="${4:-8000}"
  local wait_ms="${5:-25000}"

  local chrome=""
  if command -v google-chrome >/dev/null 2>&1; then
    chrome="google-chrome"
  elif command -v chromium-browser >/dev/null 2>&1; then
    chrome="chromium-browser"
  elif command -v chromium >/dev/null 2>&1; then
    chrome="chromium"
  else
    echo "Warning: no Chrome/Chromium; skip screenshot $png_path" >&2
    return 1
  fi

  mkdir -p "$(dirname "$png_path")"
  "$chrome" --headless=new --disable-gpu --no-sandbox \
    --window-size="${width},${height}" \
    --force-device-scale-factor=1 \
    --run-all-compositor-stages-before-draw \
    --virtual-time-budget="$wait_ms" \
    --screenshot="$png_path" \
    "file://${html_path}" 2>/dev/null
  echo "Screenshot: $png_path (${width}x${height})"
}

if [[ "${BASH_SOURCE[0]:-}" == "${0}" ]] && [[ $# -ge 2 ]]; then
  screenshot_html "$@"
fi
