#!/usr/bin/env python3
"""Scrape every \\todo and \\note (note-to-self) out of the essay/homework
sources and compile them into NOTES.md, each tagged with its source file and
section breadcrumb (\\section > \\subsection > ...).

Runs automatically on every build (wired into .latexmkrc, which latexmk reads
for `make build`, `make watch`, and texlab's on-save build). Also runnable by
hand: `make notes`  or  `python3 scripts/collect-notes.py`.

It scans essay.tex / hw.tex (whichever exist) plus parts/*.tex (skipping the
parts/_*.tex skeletons), reading the .tex directly -- no LaTeX run required.
"""

from pathlib import Path
import re

# Sectioning commands, outermost first; index == depth in the breadcrumb.
SECTIONS = ["part", "chapter", "section", "subsection",
            "subsubsection", "paragraph", "subparagraph"]
LEVEL = {name: i for i, name in enumerate(SECTIONS)}

# \section, \todo, \note, ... possibly starred (\section*).
MACRO = re.compile(r"\\(" + "|".join(SECTIONS) + r"|todo|note)\b\*?")


def files_to_scan():
    """essay.tex / hw.tex (if present), then parts/*.tex minus _skeletons."""
    files = [f for f in ("essay.tex", "hw.tex") if Path(f).exists()]
    files += sorted(p.as_posix() for p in Path("parts").glob("*.tex")
                    if not p.name.startswith("_"))
    return files


def strip_comments(text):
    """Blank out LaTeX comments (% to end of line, honoring \\%) WITHOUT
    changing length, so character offsets -> line numbers stay correct."""
    out = []
    for line in text.split("\n"):
        i, cut = 0, None
        while i < len(line):
            c = line[i]
            if c == "\\":
                i += 2
                continue
            if c == "%":
                cut = i
                break
            i += 1
        if cut is not None:
            line = line[:cut] + " " * (len(line) - cut)
        out.append(line)
    return "\n".join(out)


def read_braced(s, start):
    """Read a {...} group whose opening brace is at index `start`.
    Returns (contents, index just past the closing brace)."""
    depth, i = 0, start
    while i < len(s):
        c = s[i]
        if c == "\\":
            i += 2
            continue
        if c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0:
                return s[start + 1:i], i + 1
        i += 1
    return s[start + 1:], len(s)          # unbalanced: take the rest


def skip_optional(s, i):
    """Skip a [...] optional argument starting at/after index `i`.
    Returns the index just past it, or `i` if there isn't one."""
    j = i
    while j < len(s) and s[j].isspace():
        j += 1
    if j < len(s) and s[j] == "[":
        depth = 0
        while j < len(s):
            if s[j] == "[":
                depth += 1
            elif s[j] == "]":
                depth -= 1
                if depth == 0:
                    return j + 1
            j += 1
    return i


def collapse(text):
    """Squeeze runs of whitespace into single spaces and trim the ends."""
    return re.sub(r"\s+", " ", text).strip()


def scan(path):
    """Yield {line, type, crumb, text} dicts for each \\todo / \\note in a file."""
    s = strip_comments(Path(path).read_text(encoding="utf-8"))
    crumb = []                            # crumb[level] = section title
    consumed = 0                          # skip matches inside a captured group
    pos = 0
    while True:
        m = MACRO.search(s, pos)
        if not m:
            break
        cmd = m.group(1)
        if m.start() < consumed:
            pos = m.end()
            continue

        bi = skip_optional(s, m.end())
        while bi < len(s) and s[bi].isspace():
            bi += 1
        if bi >= len(s) or s[bi] != "{":
            pos = m.end()
            continue

        arg, end = read_braced(s, bi)
        consumed = end
        pos = end

        if cmd in LEVEL:
            lvl = LEVEL[cmd]
            while len(crumb) <= lvl:
                crumb.append("")
            crumb[lvl] = collapse(arg)
            del crumb[lvl + 1:]           # drop any deeper levels
        else:
            yield {
                "line": s.count("\n", 0, m.start()) + 1,
                "type": cmd.upper(),
                "crumb": " › ".join(c for c in crumb if c),
                "text": collapse(arg),
            }


def render(lines, title, files, by_file, kind):
    """Append a `## title` section listing every entry of `kind`, grouped by
    file (###) then section breadcrumb (####)."""
    lines += ["", f"## {title}"]
    found = False
    for f in files:
        rows = [e for e in by_file[f] if e["type"] == kind]
        if not rows:
            continue
        found = True
        lines += ["", f"### {f}"]
        last_crumb = None
        for e in rows:
            crumb = e["crumb"] or "_(before first section)_"
            if crumb != last_crumb:
                lines += ["", f"#### {crumb}", ""]
                last_crumb = crumb
            lines.append(f"- `{f}:{e['line']}` — {e['text']}")
    if not found:
        lines += ["", "_None._"]


def main():
    files = files_to_scan()
    by_file = {f: list(scan(f)) for f in files}
    todos = sum(e["type"] == "TODO" for es in by_file.values() for e in es)
    notes = sum(e["type"] == "NOTE" for es in by_file.values() for e in es)

    lines = [
        "# Notes & TODOs",
        "",
        "_Auto-generated by `scripts/collect-notes.py` on every build — do not "
        "edit by hand; your edits will be overwritten._",
        "",
        f"**{todos} TODO**, **{notes} NOTE** across {len(files)} source file(s).",
    ]

    # All TODOs first, then all NOTEs appended after -- same doc, one pass.
    render(lines, "TODOs", files, by_file, "TODO")
    render(lines, "Notes", files, by_file, "NOTE")

    Path("NOTES.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"NOTES.md: {todos} TODO, {notes} NOTE")


if __name__ == "__main__":
    main()
