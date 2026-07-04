#!/usr/bin/env python3
import html, re, sys
from pathlib import Path

def slug(title):
    s = re.sub(r'[^\w\u4e00-\u9fff]+', '-', title.lower())
    return s.strip('-')

def inline(s):
    s = html.escape(s)
    s = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', s)
    s = re.sub(r'\[(.+?)\]\((.+?)\)', r'<a href="\2">\1</a>', s)
    s = re.sub(r'`([^`]+)`', r'<code>\1</code>', s)
    return s

def md_to_html(md):
    lines = md.splitlines()
    out, i = [], 0
    in_code, code_lang, code_buf = False, '', []
    table_rows = []

    def flush_table():
        nonlocal table_rows
        if not table_rows: return
        out.append('<table>')
        for ri, row in enumerate(table_rows):
            tag = 'th' if ri == 0 else 'td'
            out.append('<tr>' + ''.join(f'<{tag}>{inline(c)}</{tag}>' for c in row) + '</tr>')
        out.append('</table>')
        table_rows = []

    while i < len(lines):
        line = lines[i]
        if in_code:
            if line.strip() == '```':
                body = '\n'.join(code_buf)
                if code_lang == 'mermaid':
                    out.append(f'<pre class="mermaid">{html.escape(body)}</pre>')
                else:
                    out.append(f'<pre><code>{html.escape(body)}</code></pre>')
                code_buf, in_code, code_lang = [], False, ''
            else:
                code_buf.append(line)
            i += 1; continue
        if line.strip().startswith('|') and '|' in line.strip()[1:]:
            if re.match(r'^\|[\s\-:|]+\|$', line.strip()):
                i += 1; continue
            table_rows.append([c.strip() for c in line.strip().strip('|').split('|')])
            i += 1; continue
        flush_table()
        if line.startswith('```'):
            in_code, code_lang = True, line.strip()[3:].strip()
            i += 1; continue
        if line.strip() == '---': out.append('<hr/>')
        elif line.startswith('# '): out.append(f'<h1>{inline(line[2:])}</h1>')
        elif line.startswith('## '): out.append(f'<h2 id="{slug(line[3:])}">{inline(line[3:])}</h2>')
        elif line.startswith('### '): out.append(f'<h3>{inline(line[4:])}</h3>')
        elif line.startswith('> '): out.append(f'<blockquote><p>{inline(line[2:])}</p></blockquote>')
        elif line.startswith('- '): out.append(f'<ul><li>{inline(line[2:])}</li></ul>')
        elif line.strip(): out.append(f'<p>{inline(line)}</p>')
        i += 1
    flush_table()
    return '\n'.join(out)



def extract_first_mermaid(md_text: str) -> str:
    m = re.search(r'```mermaid\n(.*?)```', md_text, re.S)
    return m.group(1).strip() if m else ''


PREVIEW_CSS = """
    :root { color-scheme: light; }
    * { box-sizing: border-box; }
    html, body { margin: 0; padding: 8px; background: #fff; color: #222; height: auto; overflow: hidden;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Noto Sans SC", sans-serif; }
    h1 { font-size: 11px; font-weight: 600; margin: 0 0 6px; color: #666; }
    pre.mermaid { margin: 0; padding: 0; background: transparent; border: none; display: inline-block; }
    .foot { display: none; }
"""


def build_preview_page(mermaid_body: str) -> str:
    esc = html.escape(mermaid_body)
    init = (
        "mermaid.initialize({ startOnLoad: true, theme: 'default', "
        "flowchart: { useMaxWidth: true, htmlLabels: true } });"
    )
    return f"""<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="UTF-8"/><meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<title>研发全流程 · 缩略图预览</title>
<script src="./assets/mermaid/mermaid.min.js"></script><style>{PREVIEW_CSS}</style></head><body>
<h1>Phase 0–7 · 竖向总览（README 缩略图）</h1>
<pre class="mermaid">{esc}</pre>
<p class="foot">完整文档：<a href="./robot_development_lifecycle.html">robot_development_lifecycle.html</a></p>
<script>{init}</script>
</body></html>"""


root = Path(__file__).resolve().parent.parent
md_path = root / 'robot_development_lifecycle.md'
out_path = root / 'robot_development_lifecycle.html'
preview_html_path = root / 'robot_development_lifecycle_preview.html'
md_text = md_path.read_text(encoding='utf-8')
body = md_to_html(md_text)
css = '''
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
    a { color: #0969da; } hr { margin: 2em 0; border: none; border-top: 1px solid #ccc; }
    .tip { position: sticky; top: 0; z-index: 9; background: #fff3cd; color: #664d03; border: 1px solid #ffecb5;
      border-radius: 8px; padding: 10px 14px; margin-bottom: 20px; font-size: .9rem; }
'''
page = f'''<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="UTF-8"/><meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<title>机器人研发全流程 · Mermaid 预览</title>
<script src="./assets/mermaid/mermaid.min.js"></script><style>{css}</style></head><body>
<div class="tip">📊 可视化预览：Mermaid 流程图已渲染。修改 .md 后运行 <code>./regenerate_lifecycle_html.sh</code></div>
<article>{body}</article>
<script>mermaid.initialize({{ startOnLoad: true, theme: "default", flowchart: {{ useMaxWidth: true, htmlLabels: true }} }});</script>
</body></html>'''
out_path.write_text(page, encoding='utf-8')
print(f'Wrote {out_path}')

mermaid = extract_first_mermaid(md_text)
if mermaid:
    preview_html_path.write_text(build_preview_page(mermaid), encoding='utf-8')
    print(f'Wrote {preview_html_path}')
else:
    print('Warning: no mermaid in lifecycle md', file=__import__('sys').stderr)
