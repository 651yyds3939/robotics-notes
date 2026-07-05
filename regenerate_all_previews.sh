#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
"$ROOT/regenerate_robot_system_html.sh"
"$ROOT/regenerate_lifecycle_html.sh"
"$ROOT/regenerate_integration_html.sh"
"$ROOT/regenerate_pipelines_html.sh"
python3 "$ROOT/scripts/normalize_readme_previews.py"
echo "All preview assets regenerated and normalized."
