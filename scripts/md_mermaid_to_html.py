#!/usr/bin/env python3
"""Convert Markdown (with mermaid blocks) to standalone HTML preview pages."""
import argparse
import html
import re
import sys
from pathlib import Path

MERMAID_CDN = "https://cdn.jsdelivr.net/npm/mermaid@11.4.0/dist/mermaid.min.js"
MERMAID_LOCAL = "./assets/mermaid/mermaid.min.js"


def slug(title: str) -> str:
    s = re.sub(r"[^\w\u4e00-\u9fff]+", "-", title.lower())
    return s.strip("-")


def inline(s: str) -> str:
    s = html.escape(s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"\[(.+?)\]\((.+?)\)", r'<a href="\2">\1</a>', s)
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    return s


def escape_mermaid(body: str) -> str:
    return body.replace("&", "&amp;").replace("</pre>", "<\\/pre>")


def mermaid_boot_script() -> str:
    return f"""<script>
(function () {{
  function boot() {{
    mermaid.initialize({{
      startOnLoad: true,
      theme: "default",
      securityLevel: "loose",
      flowchart: {{ useMaxWidth: true, htmlLabels: true, curve: "basis" }},
    }});
  }}
  var s = document.createElement("script");
  s.src = "{MERMAID_CDN}";
  s.onload = boot;
  s.onerror = function () {{
    var t = document.createElement("script");
    t.src = "{MERMAID_LOCAL}";
    t.onload = boot;
    document.head.appendChild(t);
  }};
  document.head.appendChild(s);
}})();
</script>"""


def unwrap_blockquote(line: str) -> tuple:
    if line.startswith("> "):
        return True, line[2:]
    if line.startswith(">"):
        return True, line[1:].lstrip()
    return False, line


def md_to_html(md: str) -> str:
    lines = md.splitlines()
    out = []
    i = 0
    in_code, code_lang, code_buf = False, "", []
    table_rows = []
    quote_buf = []

    def flush_table():
        nonlocal table_rows
        if not table_rows:
            return
        out.append("<table>")
        for ri, row in enumerate(table_rows):
            tag = "th" if ri == 0 else "td"
            out.append("<tr>" + "".join(f"<{tag}>{inline(c)}</{tag}>" for c in row) + "</tr>")
        out.append("</table>")
        table_rows = []

    def flush_quote():
        nonlocal quote_buf
        if not quote_buf:
            return
        inner = "".join(f"<p>{inline(part)}</p>" for part in quote_buf)
        out.append(f"<blockquote>{inner}</blockquote>")
        quote_buf = []

    while i < len(lines):
        line = lines[i]
        if in_code:
            if line.strip() == "```":
                body = "\n".join(code_buf)
                if code_lang == "mermaid":
                    out.append(f'<pre class="mermaid">{escape_mermaid(body)}</pre>')
                else:
                    out.append(f"<pre><code>{html.escape(body)}</code></pre>")
                code_buf, in_code, code_lang = [], False, ""
            else:
                code_buf.append(line)
            i += 1
            continue

        bq, content = unwrap_blockquote(line)
        stripped = content.strip()

        if stripped.startswith("|") and "|" in stripped[1:]:
            flush_quote()
            if re.match(r"^\|[\s\-:|]+\|$", stripped):
                i += 1
                continue
            table_rows.append([c.strip() for c in stripped.strip("|").split("|")])
            i += 1
            continue

        flush_table()

        if line.startswith("```"):
            flush_quote()
            in_code, code_lang = True, line.strip()[3:].strip()
            i += 1
            continue
        if stripped == "---":
            flush_quote()
            out.append("<hr/>")
        elif content.startswith("# "):
            flush_quote()
            out.append(f"<h1>{inline(content[2:])}</h1>")
        elif content.startswith("## "):
            flush_quote()
            out.append(f'<h2 id="{slug(content[3:])}">{inline(content[3:])}</h2>')
        elif content.startswith("### "):
            flush_quote()
            out.append(f"<h3>{inline(content[4:])}</h3>")
        elif content.startswith("#### "):
            flush_quote()
            out.append(f"<h4>{inline(content[5:])}</h4>")
        elif content.startswith("- "):
            flush_quote()
            out.append(f"<ul><li>{inline(content[2:])}</li></ul>")
        elif bq:
            if stripped:
                quote_buf.append(content)
        elif stripped:
            flush_quote()
            out.append(f"<p>{inline(content)}</p>")
        i += 1

    flush_table()
    flush_quote()
    return "\n".join(out)


def extract_first_mermaid(md_text: str) -> str:
    m = re.search(r"```mermaid\n(.*?)```", md_text, re.S)
    return m.group(1).strip() if m else ""


FULL_CSS = """
    :root { color-scheme: light dark; }
    body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Noto Sans SC", sans-serif;
      line-height: 1.65; max-width: 1200px; margin: 0 auto; padding: 24px 20px 80px; background: #fafafa; color: #222; }
    @media (prefers-color-scheme: dark) { body { background: #1e1e1e; color: #ddd; } table, th, td { border-color: #444; }
      blockquote { background: #2a2a2a; border-color: #555; } a { color: #6cb6ff; } hr { border-color: #444; } }
    h1 { font-size: 1.8rem; border-bottom: 2px solid #ccc; padding-bottom: .4em; }
    h2 { font-size: 1.35rem; margin-top: 2em; border-bottom: 1px solid #ddd; padding-bottom: .3em; }
    h3 { font-size: 1.1rem; margin-top: 1.4em; }
    blockquote { margin: 1em 0; padding: .6em 1em; border-left: 4px solid #888; background: #f0f0f0; }
    table { border-collapse: collapse; width: 100%; margin: 1em 0; font-size: .92rem; }
    th, td { border: 1px solid #ccc; padding: 8px 10px; text-align: left; vertical-align: top; }
    th { background: rgba(128,128,128,.12); }
    pre.mermaid { background: #fff; border: 1px solid #ddd; border-radius: 8px; padding: 16px; overflow-x: auto; margin: 1.2em 0; }
    @media (prefers-color-scheme: dark) { pre.mermaid { background: #2d2d2d; border-color: #555; } }
    pre:not(.mermaid) { background: #f6f8fa; border: 1px solid #ddd; border-radius: 6px; padding: 12px; overflow-x: auto; }
    a { color: #0969da; } hr { margin: 2em 0; border: none; border-top: 1px solid #ccc; }
    .tip { position: sticky; top: 0; z-index: 9; background: #fff3cd; color: #664d03; border: 1px solid #ffecb5;
      border-radius: 8px; padding: 10px 14px; margin-bottom: 20px; font-size: .9rem; }
"""

PREVIEW_CSS = """
    :root { color-scheme: light; }
    * { box-sizing: border-box; }
    html, body { margin: 0; padding: 8px; background: #fff; color: #222; height: auto; overflow: hidden;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Noto Sans SC", sans-serif; }
    h1 { font-size: 11px; font-weight: 600; margin: 0 0 6px; color: #666; }
    pre.mermaid { margin: 0; padding: 0; background: transparent; border: none; display: inline-block; }
    .foot { display: none; }
"""


def build_full_page(body, title, tip):
    return f"""<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="UTF-8"/><meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<title>{html.escape(title)}</title><style>{FULL_CSS}</style></head><body>
<div class="tip">{tip}</div>
<article>{body}</article>
{mermaid_boot_script()}
</body></html>"""


def build_preview_page(mermaid_body, title, full_href):
    esc = escape_mermaid(mermaid_body)
    return f"""<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="UTF-8"/><meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<title>{html.escape(title)} · 缩略图预览</title><style>{PREVIEW_CSS}</style></head><body>
<h1>{html.escape(title)}</h1>
<pre class="mermaid">{esc}</pre>
<p class="foot">完整文档：<a href="{html.escape(full_href)}">{html.escape(full_href)}</a></p>
{mermaid_boot_script()}
</body></html>"""


def convert(md_path, out_path, title=None, tip=None, preview_path=None, preview_href=None):
    md_text = md_path.read_text(encoding="utf-8")
    body = md_to_html(md_text)
    page_title = title or md_path.stem
    page_tip = tip or f'📊 Mermaid 可视化预览。修改 <code>{md_path.name}</code> 后重新运行对应 regenerate 脚本。'
    out_path.write_text(build_full_page(body, page_title, page_tip), encoding="utf-8")
    print(f"Wrote {out_path}")
    if preview_path is not None:
        mermaid = extract_first_mermaid(md_text)
        if mermaid:
            href = preview_href or out_path.name
            preview_path.write_text(build_preview_page(mermaid, page_title, href), encoding="utf-8")
            print(f"Wrote {preview_path}")
        else:
            print(f"Warning: no mermaid in {md_path}", file=sys.stderr)


def main():
    p = argparse.ArgumentParser(description="Markdown + Mermaid → HTML")
    p.add_argument("md", type=Path)
    p.add_argument("html", type=Path)
    p.add_argument("--preview", type=Path, default=None)
    p.add_argument("--preview-href", default=None)
    p.add_argument("--title", default=None)
    p.add_argument("--tip", default=None)
    args = p.parse_args()
    convert(args.md, args.html, title=args.title, tip=args.tip,
            preview_path=args.preview, preview_href=args.preview_href)


if __name__ == "__main__":
    main()
