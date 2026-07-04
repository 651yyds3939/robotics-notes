#!/usr/bin/env python3
"""裁掉 PNG 四周空白；README 缩略图可限制最大高度。"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

try:
    import numpy as np
    from PIL import Image
except ImportError as e:
    print(f"trim_preview_png: need Pillow+numpy: {e}", file=sys.stderr)
    sys.exit(1)


def tight_crop(
    arr: np.ndarray,
    *,
    threshold: int = 248,
    min_row_ratio: float = 0.002,
    min_col_ratio: float = 0.002,
    col_peak_frac: float = 0.12,
    row_peak_frac: float = 0.08,
) -> tuple[int, int, int, int]:
    """按墨迹密度求紧包围盒；col_peak_frac 可忽略 Markmap 横贯全屏的细线。"""
    if arr.ndim == 2:
        gray = arr
    else:
        gray = arr.max(axis=2)

    ink = gray < threshold
    h, w = ink.shape

    row_counts = ink.sum(axis=1)
    col_counts = ink.sum(axis=0)
    row_thresh = max(int(w * min_row_ratio), int(row_counts.max() * row_peak_frac), 1)
    col_thresh = max(int(h * min_col_ratio), int(col_counts.max() * col_peak_frac), 1)

    rows = np.where(row_counts >= row_thresh)[0]
    cols = np.where(col_counts >= col_thresh)[0]
    if rows.size == 0 or cols.size == 0:
        return 0, 0, w, h
    return int(cols[0]), int(rows[0]), int(cols[-1]) + 1, int(rows[-1]) + 1


def process(
    path: Path,
    *,
    border: int = 20,
    max_height: int | None = None,
    max_width: int | None = None,
    canvas_width: int | None = None,
    canvas_height: int | None = None,
    threshold: int = 248,
    col_peak_frac: float = 0.12,
    pad_left: int = 0,
    pad_right: int = 0,
    pad_top: int = 0,
    pad_bottom: int = 0,
    content_scale: float = 1.0,
    offset_x: int = 0,
    offset_y: int = 0,
    trim_right: int = 0,
    fit_width: bool = False,
    fit_height: bool = False,
) -> tuple[int, int]:
    img = Image.open(path)
    if img.mode != "RGB":
        img = img.convert("RGB")
    arr = np.array(img)

    h_img, w_img = arr.shape[0], arr.shape[1]
    x0, y0, x1, y1 = tight_crop(
        arr, threshold=threshold, col_peak_frac=col_peak_frac
    )
    x0 = max(0, x0 - pad_left)
    y0 = max(0, y0 - pad_top)
    x1 = min(w_img, x1 + pad_right - trim_right)
    y1 = min(h_img, y1 + pad_bottom)
    cropped = img.crop((x0, y0, x1, y1))

    if max_height or max_width:
        cw, ch = cropped.size
        scale = 1.0
        if max_height and ch > max_height:
            scale = min(scale, max_height / ch)
        if max_width and cw > max_width:
            scale = min(scale, max_width / cw)
        if scale < 1.0:
            nw, nh = max(1, int(cw * scale)), max(1, int(ch * scale))
            cropped = cropped.resize((nw, nh), Image.Resampling.LANCZOS)

    cw, ch = cropped.size
    if canvas_width or canvas_height:
        tw = canvas_width or cw
        th = canvas_height or ch
        if fit_width:
            fit = (tw / cw) * content_scale
            nh = max(1, int(ch * fit))
            if nh > th:
                fit = fit * th / nh
            nw = max(1, int(cw * fit))
            nh = max(1, int(ch * fit))
            if (nw, nh) != (cw, ch):
                cropped = cropped.resize((nw, nh), Image.Resampling.LANCZOS)
                cw, ch = nw, nh
        elif fit_height:
            fit = (th / ch) * content_scale
            nw = max(1, int(cw * fit))
            nh = max(1, int(ch * fit))
            cropped = cropped.resize((nw, nh), Image.Resampling.LANCZOS)
            if nw > tw:
                x0 = max(0, min(nw - tw, (nw - tw) // 2 - offset_x))
                cropped = cropped.crop((x0, 0, x0 + tw, nh))
            cw, ch = cropped.size
        else:
            fit = min(tw / cw, th / ch) * content_scale
            nw = max(1, int(cw * fit))
            nh = max(1, int(ch * fit))
            if (nw, nh) != (cw, ch):
                cropped = cropped.resize((nw, nh), Image.Resampling.LANCZOS)
                cw, ch = nw, nh
        if canvas_height is None:
            th = ch
        canvas = Image.new("RGB", (tw, th), (255, 255, 255))
        ox = max(0, min(tw - cw, (tw - cw) // 2 + offset_x)) if not fit_height else 0
        oy = max(0, min(th - ch, (th - ch) // 2 + offset_y))
        canvas.paste(cropped, (ox, oy))
        cropped = canvas

    cw, ch = cropped.size
    out = Image.new("RGB", (cw + 2 * border, ch + 2 * border), (255, 255, 255))
    out.paste(cropped, (border, border))
    out.save(path, optimize=True)
    return out.size


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("path", type=Path)
    p.add_argument("--border", type=int, default=20)
    p.add_argument("--max-height", type=int, default=None)
    p.add_argument("--max-width", type=int, default=None)
    p.add_argument("--canvas-width", type=int, default=None)
    p.add_argument("--canvas-height", type=int, default=None)
    p.add_argument("--threshold", type=int, default=248)
    p.add_argument("--col-peak-frac", type=float, default=0.12)
    p.add_argument("--pad-left", type=int, default=0)
    p.add_argument("--content-scale", type=float, default=1.0)
    args = p.parse_args()
    size = process(
        args.path,
        border=args.border,
        max_height=args.max_height,
        max_width=args.max_width,
        canvas_width=args.canvas_width,
        canvas_height=args.canvas_height,
        threshold=args.threshold,
        col_peak_frac=args.col_peak_frac,
        pad_left=args.pad_left,
        content_scale=args.content_scale,
    )
    print(f"trim_preview_png: {args.path} -> {size[0]}x{size[1]}")


if __name__ == "__main__":
    main()
