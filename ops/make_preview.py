"""Build the PR preview page from src/index.html.

Adds a clearly visible "ELŐNÉZET" (preview) bar to the top of the page so the
preview artifact can never be mistaken for the live one. The source file is
not changed; the result is written to the given output path.

Usage: python3 ops/make_preview.py <label> <output.html>
       e.g. python3 ops/make_preview.py "PR #6 · v0.5.0" /tmp/preview/index.html
"""
import html
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "src" / "index.html"

BAR = (
    '<div role="note" style="position:sticky;top:0;z-index:10;background:#8a5a00;color:#fff;'
    'font:600 13px/1.4 system-ui,sans-serif;padding:7px 14px;text-align:center">'
    "ELŐNÉZET – {label} · ez nem az élő oldal; az árak az élő oldal másolatai</div>"
)


def main():
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    label, out = sys.argv[1], pathlib.Path(sys.argv[2])
    page = SRC.read_text(encoding="utf-8")
    if page.count("<body>") != 1:
        sys.exit("src/index.html must contain exactly one <body> tag")
    page = page.replace("<body>", "<body>" + BAR.format(label=html.escape(label)), 1)
    page = page.replace("<title>", "<title>[ELŐNÉZET] ", 1)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(page, encoding="utf-8")
    print(f"preview written: {out}")


if __name__ == "__main__":
    main()
