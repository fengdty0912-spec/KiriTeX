#!/usr/bin/env python3
"""mineru2kiritex.py -- convert MinerU Markdown output into a KiriTeX document.

MinerU (https://github.com/opendatalab/MinerU) turns PDFs / images into
structured Markdown whose formulas are LaTeX. This script maps that Markdown to
a KiriTeX ``.tex`` file and cleans up MinerU's OCR-produced LaTeX so the result
compiles cleanly with XeLaTeX.

Typical workflow::

    # 1. parse a PDF/image (pipeline backend, Chinese, CPU)
    mineru -p paper.pdf -o outdir -b pipeline -m auto -l ch

    # 2. convert the Markdown into a KiriTeX document
    python mineru2kiritex.py outdir/paper/auto/paper.md -o paper.tex

    # 3. compile (KiriTeX needs XeLaTeX + ctex)
    xelatex -interaction=nonstopmode paper.tex

The converter performs a *generic structural* mapping (headings -> sections,
display math -> ``\\[ ... \\]``, inline math -> ``$ ... $``, images -> figures,
tables -> tabular). It does NOT guess problem environments; wrap questions in
``problem`` / ``problemchoice`` / ``problemtf`` manually afterwards.
"""

import argparse
import html
import os
import re
import sys


# ---------------------------------------------------------------------------
# Formula cleanup
# ---------------------------------------------------------------------------

def clean_math(src: str) -> str:
    """Normalise MinerU's OCR-generated LaTeX into cleaner LaTeX."""
    s = src

    # \operatorname* { l i m } -> \lim  (and friends). MinerU spaces out the
    # letters of operator names and wraps them in \operatorname*.
    operators = {
        "lim": r"\lim",
        "max": r"\max",
        "min": r"\min",
        "log": r"\log",
        "ln": r"\ln",
        "sin": r"\sin",
        "cos": r"\cos",
        "tan": r"\tan",
        "cot": r"\cot",
        "sec": r"\sec",
        "csc": r"\csc",
        "arcsin": r"\arcsin",
        "arccos": r"\arccos",
        "arctan": r"\arctan",
        "arctan": r"\arctan",
        "exp": r"\exp",
        "det": r"\det",
        "dim": r"\dim",
        "gcd": r"\gcd",
        "sup": r"\sup",
        "inf": r"\inf",
        "arg": r"\arg",
        "deg": r"\deg",
        "hom": r"\hom",
    }
    for name, cmd in operators.items():
        spaced = r"\s+".join(re.escape(c) for c in name)
        s = re.sub(
            r"\\operatorname\*?\s*\{\s*" + spaced + r"\s*\}",
            lambda m, c=cmd: c,
            s,
        )

    # generic \operatorname*{...} -> \operatorname{...}
    s = s.replace(r"\operatorname*{", r"\operatorname{")

    # \overset{...}{...} / \underset{...}{...} -> body_{...} / body^{...}
    s = re.sub(
        r"\\underset\s*\{(?P<sub>[^{}]*)\}\s*\{(?P<body>[^{}]*)\}",
        lambda m: m.group("body") + "_{" + m.group("sub") + "}",
        s,
    )
    s = re.sub(
        r"\\overset\s*\{(?P<sup>[^{}]*)\}\s*\{(?P<body>[^{}]*)\}",
        lambda m: m.group("body") + "^{" + m.group("sup") + "}",
        s,
    )

    # \stackrel{a}{b} -> b (keep the body, drop the stacked annotation)
    s = re.sub(r"\\stackrel\s*\{(?P<a>[^{}]*)\}\s*\{(?P<b>[^{}]*)\}", r"\g<b>", s)

    # \begin{array}{...} / \end{array} -> aligned
    s = re.sub(r"\\begin\s*\{array\}\s*\{[^{}]*\}", r"\\begin{aligned}", s)
    s = s.replace(r"\end{array}", r"\end{aligned}")

    # \cfrac -> \dfrac
    s = s.replace(r"\cfrac", r"\dfrac")

    # normalise MinerU's pervasive whitespace around braces and scripts,
    # iterated to a fixed point:  \frac { 1 } { n } -> \frac{1}{n},
    # e ^ { x } -> e^{x},  a _ { n } -> a_{n},  \mathrm { d } -> \mathrm{d}
    for _ in range(6):
        prev = s
        s = re.sub(r"(?<!\\)\s*\{\s*", "{", s)
        s = re.sub(r"(?<!\\)\s*\}\s*", "}", s)
        s = re.sub(r"(\^|_)\s+(\w)", r"\1\2", s)
        if s == prev:
            break

    # join spaced digit runs: 1 0 0 -> 100
    for _ in range(4):
        s2 = re.sub(r"(?<=\d)\s+(?=\d)", "", s)
        if s2 == s:
            break
        s = s2

    return s


# ---------------------------------------------------------------------------
# Markdown -> LaTeX structural mapping
# ---------------------------------------------------------------------------

def _escape(text: str) -> str:
    """Escape LaTeX special characters in plain text (outside math)."""
    for ch in ["&", "%", "#", "_"]:
        text = text.replace(ch, "\\" + ch)
    return text


def convert_markdown(md_text: str, title: str, author: str, date: str) -> str:
    lines = md_text.splitlines()
    out = []
    in_display = False  # inside $$ ... $$
    display_buf = []

    def flush_paragraph(buf):
        text = "".join(buf).strip()
        if text:
            out.append(text + "\n")

    para = []

    def flush_display():
        nonlocal display_buf
        body = " ".join(display_buf).strip()
        if body:
            out.append("\\[\n" + clean_math(body) + "\n\\]\n")
        display_buf = []

    i = 0
    while i < len(lines):
        raw = lines[i].rstrip()
        line = raw.strip()

        # display math blocks (may span lines)
        if line.startswith("$$"):
            flush_paragraph(para); para = []
            if not in_display:
                in_display = True
                display_buf = [line[2:]]
            else:
                in_display = False
                display_buf.append(line[: -2] if line.endswith("$$") else line)
                flush_display()
            i += 1
            continue

        if in_display:
            display_buf.append(line)
            i += 1
            continue

        # headings
        m = re.match(r"^(#{1,6})\s+(.*)$", line)
        if m:
            flush_paragraph(para); para = []
            level = len(m.group(1))
            heading = _escape(m.group(2))
            cmd = {1: "section", 2: "subsection", 3: "subsubsection"}.get(level)
            if cmd:
                out.append(f"\\{cmd}{{{heading}}}\n")
            i += 1
            continue

        # images
        m = re.match(r"^!\[([^\]]*)\]\s*\(([^)]+)\)$", line)
        if m:
            flush_paragraph(para); para = []
            path = m.group(2)
            out.append(
                "\\begin{figure}[htbp]\n\\centering\n"
                f"\\includegraphics[width=0.7\\textwidth]{{{path}}}\n"
                "\\end{figure}\n"
            )
            i += 1
            continue

        # blank line -> paragraph break
        if not line:
            flush_paragraph(para); para = []
            i += 1
            continue

        # keep inline math and text; clean inline formulas
        def clean_inline(m):
            return "$" + clean_math(m.group(1)) + "$"

        cleaned = re.sub(r"\$(.+?)\$", clean_inline, line)
        # HTML entities MinerU may emit
        cleaned = html.unescape(cleaned)
        # escape characters outside math is skipped for simplicity; math is the
        # dominant content. Escape stray raw ampersands not in math.
        cleaned = re.sub(r"&(?!\w+;)", r"\\&", cleaned)
        para.append(cleaned + "\n")
        i += 1

    flush_paragraph(para)
    if in_display:
        flush_display()

    body = "\n".join(out).strip()

    return (
        "\\documentclass{kiritex}\n\n"
        f"\\title{{{title}}}\n"
        f"\\author{{{author}}}\n"
        f"\\date{{{date}}}\n\n"
        "\\begin{document}\n\n"
        "\\maketitle\n\n"
        "\\tableofcontents\n"
        "\\newpage\n\n"
        + body
        + "\n\n\\end{document}\n"
    )


def lint_tex(path: str) -> int:
    """Read-only conformance check of a KiriTeX .tex file against the math spec.

    Reports violations without modifying the file. Return code = number of
    distinct problems found (0 means clean).
    """
    with open(path, encoding="utf-8") as fh:
        s = fh.read()
    lines = s.splitlines()
    problems = []

    # 1) \dfrac is retired
    for m in re.finditer(r"\\dfrac", s):
        ln = s.count("\n", 0, m.start()) + 1
        problems.append((ln, "\\dfrac 已废弃，请改用 \\displaystyle \\frac"))

    # 2) inline \frac must be display-style via \displaystyle (matrix/cases cells exempt)
    for i, line in enumerate(lines, 1):
        for m in re.finditer(r"\$([^$]*?\\frac[^$]*?)\$", line):
            body = m.group(1)
            if "\\displaystyle" in body:
                continue
            if re.search(r"\\begin\{(?:pmatrix|bmatrix|vmatrix|matrix|cases)\}", body):
                continue
            ctx = body.strip().replace("\n", " ")[:60]
            problems.append((i, f"行内 \\frac 未加 \\displaystyle：{ctx}"))

    # 3) cases/aligned rows: a comma directly before & (no space) needs a space
    for i, line in enumerate(lines, 1):
        if re.search(r",(?=[}]*&)", line):
            problems.append((i, "分段/方程组行内逗号后缺少空格（应为 `, &`）"))

    # 4) structural balance
    if s.count("$") % 2 != 0:
        problems.append((0, "`$` 数量为奇数（存在未闭合的行内公式）"))
    if s.count("{") != s.count("}"):
        problems.append((0, f"花括号不平衡：{{ {s.count('{')} ，}} {s.count('}')}"))
    opens = len(re.findall(r"\\\[", s))
    closes = len(re.findall(r"\\\]", s))
    if opens != closes:
        problems.append((0, f"\\[ ... \\] 不平衡：\\[ {opens} ，\\] {closes}"))
    for env, name in (("problem", "problem"), ("problemtf", "problemtf"),
                      ("problemchoice", "problemchoice")):
        b = len(re.findall(r"\\begin\{" + env + r"\}", s))
        e = len(re.findall(r"\\end\{" + env + r"\}", s))
        if b != e:
            problems.append((0, f"环境 {name}：begin {b} 个，end {e} 个，不平衡"))

    # 5) math quantities MUST be wrapped: flag bare intervals/points in text
    bare_text = re.sub(r"(\$.*?\$)|(\\\[.*?\\\])", "", s, flags=re.S)
    for m in re.finditer(r"[（(][0-9a-zA-Z]+\s*,\s*[0-9a-zA-Z][0-9a-zA-Z，,+\-.]*[）)]", bare_text):
        ln = bare_text.count("\n", 0, m.start()) + 1
        problems.append((ln, f"区间/坐标未放进公式环境：{m.group(0)}"))

    # 6) heuristics (advisory only): bare uppercase letters that may be matrices
    hints = []
    for i, line in enumerate(lines, 1):
        for m in re.finditer(r"\$([^$]{0,40})\$", line):
            body = m.group(1)
            for ch in "ABCEHOPX":
                for mm in re.finditer("(?<![A-Za-z\\\\{])" + ch + "(?![A-Za-z])", body):
                    if "\\bm" not in body[: mm.start()]:
                        hints.append((i, f"可能漏加 \\bm{{}}（若非矩阵请忽略）：{ch} 位于 ${body[:50]}"))
                        break

    # report
    seen = set()
    out = []
    for ln, msg in problems:
        tag = (ln, msg)
        if tag in seen:
            continue
        seen.add(tag)
        out.append(f"{path}:{ln}: {msg}")
    for line in out:
        print(line, file=sys.stderr)
    print(f"{len(out)} problem(s) reported.", file=sys.stderr)
    for ln, msg in hints:
        print(f"{path}:{ln}: [提示] {msg}", file=sys.stderr)
    if hints:
        print(f"{len(hints)} hint(s) — 启发式提示，请人工核对（数学/物理常量如 C、E 可忽略）。", file=sys.stderr)
    return len(out)


def main(argv=None):
    ap = argparse.ArgumentParser(description="Convert MinerU Markdown to KiriTeX LaTeX.")
    ap.add_argument("input", help="MinerU .md file or the output directory containing one")
    ap.add_argument("-o", "--output", help="output .tex path (default: <input>.tex)")
    ap.add_argument("--title", default="真题", help="document title")
    ap.add_argument("--author", default="风待桐叶", help="document author")
    ap.add_argument("--date", default="2026 年 8 月", help="document date")
    ap.add_argument("--check", action="store_true",
                    help="read-only lint mode: check a produced .tex against the math spec")
    args = ap.parse_args(argv)

    if args.check:
        return lint_tex(args.input)

    src = args.input
    if os.path.isdir(src):
        # locate a .md inside the directory tree
        candidates = []
        for root, _, files in os.walk(src):
            candidates += [os.path.join(root, f) for f in files if f.endswith(".md")]
        if not candidates:
            print(f"no .md found under {src}", file=sys.stderr)
            return 2
        src = candidates[0]

    with open(src, encoding="utf-8") as fh:
        md = fh.read()

    tex = convert_markdown(md, args.title, args.author, args.date)

    out = args.output or (os.path.splitext(src)[0] + ".tex")
    with open(out, "w", encoding="utf-8") as fh:
        fh.write(tex)
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
