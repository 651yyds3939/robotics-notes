#!/usr/bin/env python3
"""Check local Markdown links and credential-shaped strings without printing secrets.

Cross-repository GitHub links are checked against sibling clones when available;
this is not a network availability or anchor validation check.
"""
from pathlib import Path
import re
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parent.parent
KEY = re.compile(r"sk-[A-Za-z0-9_-]{32,}")
LINK = re.compile(r"!?\[[^\]\n]*\]\(\s*(<[^>]+>|[^\s)]+)(?:\s+['\"][^\n]*?['\"])?\s*\)")


def unclosed_fence(text):
    fence = None
    for number, line in enumerate(text.splitlines(), 1):
        match = re.match(r"^\s*(`{3,}|~{3,})(.*)$", line)
        if not match:
            continue
        token, suffix = match.groups()
        # Inline examples like ` ```mermaid ` are not block fences.
        if token[0] in suffix:
            continue
        if fence is None:
            fence = (token, number)
        elif token[0] == fence[0][0] and len(token) >= len(fence[0]):
            fence = None
    return fence[1] if fence else None


def links(text):
    fence = None
    for number, line in enumerate(text.splitlines(), 1):
        marker = re.match(r"^\s*(`{3,}|~{3,})", line)
        if marker:
            token = marker.group(1)
            if fence is None:
                fence = token
            elif token[0] == fence[0] and len(token) >= len(fence):
                fence = None
            continue
        if fence:
            continue
        code_spans = [m.span() for m in re.finditer(r"(`+).*?\1", line)]
        for match in LINK.finditer(line):
            if any(start <= match.start() < end for start, end in code_spans):
                continue
            yield number, unquote(match.group(1).strip("<>"))


def target_path(source, target):
    parsed = urlsplit(target)
    if parsed.netloc == "github.com":
        parts = parsed.path.strip("/").split("/")
        if len(parts) >= 5 and parts[0] == "651yyds3939" and parts[2] in ("blob", "tree"):
            sibling = ROOT.parent / parts[1]
            if sibling.is_dir():
                return sibling / "/".join(parts[4:])
    if parsed.scheme or parsed.netloc or not parsed.path:
        return None
    return source.parent / parsed.path


def main():
    failures = 0
    files = sorted(p for p in ROOT.rglob("*.md") if ".git" not in p.parts)
    for path in files:
        data = path.read_text(encoding="utf-8")
        fence_line = unclosed_fence(data)
        if fence_line:
            print(f"Unclosed code fence: {path.relative_to(ROOT)}:{fence_line}")
            failures += 1
        for number, line in enumerate(data.splitlines(), 1):
            if KEY.search(line):
                print(f"Credential-shaped value: {path.relative_to(ROOT)}:{number} (value hidden)")
                failures += 1
        for number, target in links(data):
            resolved = target_path(path, target)
            if resolved is not None and not resolved.exists():
                print(f"Missing link: {path.relative_to(ROOT)}:{number} -> {target}")
                failures += 1
    print(f"Checked {len(files)} Markdown files; {failures} issue(s).")
    return bool(failures)


if __name__ == "__main__":
    raise SystemExit(main())
