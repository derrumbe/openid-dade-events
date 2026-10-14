#!/usr/bin/env python3
"""Render a repository markdown document to a standalone HTML page.

Used by `make publish` to put EVENT-CATALOG.md on the
GitHub Pages site alongside the xml2rfc-rendered specification. The
markdown files remain the single source of truth.

Usage: render-md.py <input.md> <output.html> "<Page title>"
"""
import re
import sys

import markdown

CSS = """
:root{--ground:#f7f8fa;--surface:#fff;--surface-2:#eff2f6;--ink:#161a20;
--muted:#5c6672;--rule:#d9dee6;--rule-soft:#e7ebf1;--accent:#c2582f;--maxw:52rem}
@media (prefers-color-scheme:dark){:root:not([data-theme=light]){
--ground:#10141a;--surface:#171c24;--surface-2:#1e242e;--ink:#e7ebf1;
--muted:#96a1b0;--rule:#2c3541;--rule-soft:#232a34;--accent:#e8875c}}
:root[data-theme=dark]{--ground:#10141a;--surface:#171c24;--surface-2:#1e242e;
--ink:#e7ebf1;--muted:#96a1b0;--rule:#2c3541;--rule-soft:#232a34;--accent:#e8875c}
*{box-sizing:border-box}
body{margin:0;padding:2.5rem 1.25rem 6rem;background:var(--ground);color:var(--ink);
font-family:Georgia,"Times New Roman",Times,serif;line-height:1.65;font-size:17px}
.wrap{max-width:var(--maxw);margin:0 auto}
h1,h2,h3,h4,table,code,blockquote{font-family:"Helvetica Neue",Helvetica,Arial,sans-serif}
h1{font-size:1.9rem;line-height:1.15;letter-spacing:-.02em;margin:0 0 .4rem;text-wrap:balance}
h2{font-size:1.3rem;margin:2.4rem 0 .6rem;padding-bottom:.5rem;
border-bottom:1px solid var(--rule);letter-spacing:-.01em;text-wrap:balance}
h3{font-size:1.05rem;margin:1.6rem 0 .3rem;letter-spacing:-.005em}
p{margin:.8rem 0}
a{color:var(--accent)}
ul,ol{padding-left:1.4rem}li{margin:.35rem 0}
blockquote{margin:1.4rem 0;padding:.9rem 1.1rem;background:var(--surface);
border:1px solid var(--rule);border-left:3px solid var(--accent);border-radius:6px;
font-size:.92rem;color:var(--muted)}
blockquote p{margin:.4rem 0}
code{font-family:"SFMono-Regular",Consolas,Menlo,monospace;font-size:.85em;
background:var(--surface-2);padding:.1em .34em;border-radius:3px;word-break:break-word}
pre{background:var(--surface-2);border:1px solid var(--rule);border-radius:6px;
padding:.9rem 1rem;overflow-x:auto}
pre code{background:none;padding:0}
.tablewrap{overflow-x:auto;border:1px solid var(--rule);border-radius:8px;
background:var(--surface);margin:1.1rem 0}
table{border-collapse:collapse;width:100%;font-size:.83rem;min-width:40rem}
th,td{text-align:left;vertical-align:top;padding:.6rem .8rem;
border-top:1px solid var(--rule-soft)}
thead th{border-top:0;border-bottom:1px solid var(--rule);background:var(--surface-2);
font-size:.68rem;text-transform:uppercase;letter-spacing:.08em;color:var(--muted)}
td code{background:none;padding:0;font-weight:500;white-space:nowrap}
hr{border:0;border-top:1px solid var(--rule);margin:2.5rem 0}
.nav{font-family:"Helvetica Neue",Helvetica,Arial,sans-serif;font-size:.8rem;
margin-bottom:2rem;padding-bottom:1rem;border-bottom:1px solid var(--rule);color:var(--muted)}
.nav a{margin-right:1.1rem}
@media print{body{background:#fff;color:#000;padding:0}
.nav{display:none}.tablewrap{overflow:visible}table{min-width:0;font-size:9pt}}
"""

NAV = ('<div class="nav"><a href="./">Specification</a>'
       '<a href="event-catalog.html">Event catalog</a>'
       '<a href="dade-event-reference.html">Event reference</a>'
       '<a href="https://github.com/derrumbe/openid-dade-events">Repository</a></div>')


def main():
    src, dst, title = sys.argv[1], sys.argv[2], sys.argv[3]
    with open(src, encoding="utf-8") as fh:
        text = fh.read()

    html = markdown.markdown(
        text, extensions=["tables", "fenced_code", "attr_list", "sane_lists"]
    )
    # Wide tables scroll inside their own container rather than the page body.
    html = html.replace("<table>", '<div class="tablewrap"><table>')
    html = html.replace("</table>", "</table></div>")
    # Point in-repo markdown links at their rendered counterparts.
    html = html.replace('href="openid-dade-events-1_0.md"', 'href="./"')
    html = html.replace('href="EVENT-CATALOG.md"', 'href="event-catalog.html"')

    with open(dst, "w", encoding="utf-8") as fh:
        fh.write(
            "<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n"
            '<meta charset="utf-8">\n'
            '<meta name="viewport" content="initial-scale=1.0, width=device-width">\n'
            f"<title>{title}</title>\n<style>{CSS}</style>\n</head>\n<body>\n"
            f'<div class="wrap">\n{NAV}\n{html}\n</div>\n</body>\n</html>\n'
        )
    print(f"rendered {src} -> {dst}")


if __name__ == "__main__":
    main()
