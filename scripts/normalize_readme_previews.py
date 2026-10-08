#!/usr/bin/env python3
"""Tight-crop all four generated previews without stretching or center clipping."""
from pathlib import Path
from trim_preview_png import process

ROOT = Path(__file__).resolve().parent.parent


def main():
    for name in ("robot_system_preview.png", "lifecycle_preview.png",
                 "integration_preview.png", "pipelines_preview.png"):
        path = ROOT / "assets" / name
        if not path.is_file():
            raise SystemExit(f"Missing preview: {path}")
        if name == "robot_system_preview.png":
            # Full Markmap export already uses the exact SVG bounds and padding.
            # Density-based cropping or downscaling can hide small/deep nodes.
            from PIL import Image
            with Image.open(path) as image:
                width, height = image.size
            print(f"Full mindmap preserved: {name} {width}x{height}")
            continue
        width, height = process(path, border=16, col_peak_frac=0,
                                pad_left=12, pad_right=12,
                                pad_top=12, pad_bottom=12,
                                max_width=1600, max_height=4200)
        print(f"Preview: {name} {width}x{height}")


if __name__ == "__main__":
    main()
