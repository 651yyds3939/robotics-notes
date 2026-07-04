#!/usr/bin/env python3
"""将 README 两张缩略图紧裁空白，并统一画布尺寸便于并排展示。"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from trim_preview_png import process

ROOT = Path(__file__).resolve().parent.parent
MINDMAP = ROOT / "assets" / "robot_system_preview.png"
LIFECYCLE = ROOT / "assets" / "lifecycle_preview.png"
BORDER = 16
CANVAS_W = 580
CONTENT_W = CANVAS_W - 2 * BORDER
CANVAS_H = 2502
CONTENT_H = CANVAS_H - 2 * BORDER


def main() -> None:
    if not MINDMAP.is_file():
        raise SystemExit(f"missing {MINDMAP}")
    if not LIFECYCLE.is_file():
        raise SystemExit(f"missing {LIFECYCLE}")

    # 横向全展开思维导图：按高度撑满同高画布，宽出部分居中裁切
    process(
        MINDMAP,
        border=BORDER,
        col_peak_frac=0.07,
        pad_left=28,
        pad_right=4,
        trim_right=8,
        pad_top=10,
        pad_bottom=10,
        canvas_width=CONTENT_W,
        canvas_height=CONTENT_H,
        content_scale=0.94,
        offset_x=18,
        fit_height=True,
    )

    process(
        LIFECYCLE,
        border=BORDER,
        col_peak_frac=0.05,
        canvas_width=CONTENT_W,
        canvas_height=CONTENT_H,
        content_scale=0.98,
        fit_width=True,
    )

    from PIL import Image
    mw = Image.open(MINDMAP).size
    lw = Image.open(LIFECYCLE).size
    print(f"README previews: mindmap {mw[0]}x{mw[1]}, lifecycle {lw[0]}x{lw[1]}")


if __name__ == "__main__":
    main()
