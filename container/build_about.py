"""Regenera la lista de feeds de public/about.html a partir de feeds.json.

Sustituye lo que hay entre los marcadores FEEDS:START y FEEDS:END.
"""
import html
import json
import os
import re

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
FEEDS = os.path.join(ROOT, "container", "lambda", "parser", "feeds.json")
ABOUT = os.path.join(ROOT, "public", "about.html")

START = "<!-- FEEDS:START -->"
END = "<!-- FEEDS:END -->"


def feedList():
    with open(FEEDS, encoding="utf-8") as f:
        languages = json.load(f)
    blocks = []
    for lang in languages.values():
        feeds = [feed for section in lang["entries"].values() for feed in section]
        if not feeds:
            continue
        items = "".join(
            '<li>%s: <a href="%s">%s</a></li>\n' % (html.escape(f["name"]), html.escape(f["url"], quote=True), html.escape(f["url"]))
            for f in sorted(feeds, key=lambda f: f["name"].lower())
        )
        blocks.append("<p><strong>%s</strong></p>\n<ul>\n%s</ul>\n" % (html.escape(lang["langFull"]), items))
    return "<p>Feeds used:</p>\n" + "\n".join(blocks)


def main():
    with open(ABOUT, encoding="utf-8") as f:
        page = f.read()
    pattern = re.compile(re.escape(START) + ".*?" + re.escape(END), re.S)
    if not pattern.search(page):
        raise SystemExit("Markers %s / %s not found in %s" % (START, END, ABOUT))
    page = pattern.sub(lambda m: START + "\n" + feedList() + END, page)
    with open(ABOUT, "w", encoding="utf-8") as f:
        f.write(page)


if __name__ == "__main__":
    main()
