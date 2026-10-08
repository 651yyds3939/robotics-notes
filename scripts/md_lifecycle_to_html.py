#!/usr/bin/env python3
"""Lifecycle entry point; reuse the shared Markdown/Mermaid renderer."""
from pathlib import Path
from md_mermaid_to_html import convert


def main():
    root = Path(__file__).resolve().parent.parent
    convert(
        root / "robot_development_lifecycle.md",
        root / "robot_development_lifecycle.html",
        title="机器人研发生命周期 · Mermaid 预览",
        tip='研发流程可视化。修改 Markdown 后运行 <code>./regenerate_lifecycle_html.sh</code>；本地 Mermaid 资源支持离线渲染。',
        preview_path=root / "robot_development_lifecycle_preview.html",
        preview_href="./robot_development_lifecycle.html",
    )


if __name__ == "__main__":
    main()
