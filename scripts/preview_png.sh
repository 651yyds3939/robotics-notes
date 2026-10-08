#!/usr/bin/env bash
# 将本地 HTML 截图为 PNG（四图裁边见 normalize_readme_previews.py）
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

screenshot_html() {
  local html_path="$1"
  local png_path="$2"
  local width="${3:-1200}"
  local height="${4:-8000}"
  local mode="${5:-}"

  local chrome=""
  if command -v google-chrome >/dev/null 2>&1; then
    chrome="google-chrome"
  elif command -v chromium-browser >/dev/null 2>&1; then
    chrome="chromium-browser"
  elif command -v chromium >/dev/null 2>&1; then
    chrome="chromium"
  else
    echo "Error: Chrome/Chromium is required to generate $png_path" >&2
    return 1
  fi

  local mode_args=()
  if [[ -n "$mode" ]]; then
    mode_args+=("$mode")
  fi
  node "$SCRIPT_DIR/screenshot_html.mjs" "$chrome" "$html_path" "$png_path" "$width" "$height" "${mode_args[@]}"
}

if [[ "${BASH_SOURCE[0]:-}" == "${0}" ]] && [[ $# -ge 2 ]]; then
  screenshot_html "$@"
fi
