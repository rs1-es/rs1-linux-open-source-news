import feedparser
import datetime
import html
import json
import os
import pytz
import func_timeout
from concurrent.futures import ThreadPoolExecutor

with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "feeds.json"), encoding="utf-8") as f:
    strings = json.load(f)
# Cada feed pasa a tupla (url, nombre, web)
for _lang in strings.values():
    for _section, _feeds in _lang["entries"].items():
        _lang["entries"][_section] = [(x["url"], x["name"], x["home"]) for x in _feeds]

# Si OUTPUT_DIR está definido se escribe en local y no se sube nada a S3
OUTPUT_DIR = os.environ.get("OUTPUT_DIR")
BUCKET = "news.rs1.es"
FEED_TIMEOUT = 60  # segundos por feed
WORK_DIR = OUTPUT_DIR or "/tmp"

SITE_NAME = "RS1 Linux & Open Source News"
SITE_URL = "https://news.rs1.es"

# Orden de los idiomas en la barra: los 3 primeros visibles, el resto en el menú "..."
LANGUAGES = ["en", "es", "de", "fr", "pt", "jp"]
LANGUAGES_VISIBLE = LANGUAGES[:3]
LANGUAGES_HIDDEN = LANGUAGES[3:]

# Una entrada por sección: carpeta de salida, etiqueta de la barra y prefijo del <title>
SECTIONS = {
    "news":   {"dir": "",        "label": "NEWS",   "title": None},
    "videos": {"dir": "videos/", "label": "VIDEOS", "title": "Videos"},
    "more":   {"dir": "more/",   "label": "MORE",   "title": "More"},
}

FOOTER = """<footer>
<a href="/"><h2>%s</h2></a>
<div class="footer-content">
<div>
<p>Javascript-free Linux/open source news aggregator.</p>
<p>Linux is a registered trademark of Linus Torvalds.</p>
</div>
</div>
</footer>
</body>
</html>""" % SITE_NAME



# ---------- Feeds ----------

def entryDate(entry, author):
    """Fecha de la entrada normalizada por feedparser (UTC), o None si no tiene."""
    field = "updated" if author in ["DistroWatch", "LWN.net"] else "published"
    parsed = entry.get(field + "_parsed")
    if parsed:
        return datetime.datetime(*parsed[:6], tzinfo=datetime.timezone.utc)
    return None

def parseFeed(url, author, homeURL):
    entries = []
    d = feedparser.parse(url)
    if not d.entries:
        # Motivo del fallo: código HTTP y excepción de feedparser (red, XML inválido...)
        print("%s: no entries (HTTP %s, %s)" % (author, d.get("status", "-"), d.get("bozo_exception", "no error")))
    for entry in d.entries:
        dt = entryDate(entry, author)
        if dt is None:
            print("%s: no date in %s" % (author, entry.get("link")))
            continue
        entries.append([entry.title, entry.link, dt.isoformat(), author, homeURL, dt.timestamp()])
    return entries

def parseFeedSafe(feed):
    """Descarga un feed con timeout; un feed roto no debe afectar al resto."""
    try:
        return func_timeout.func_timeout(FEED_TIMEOUT, parseFeed, args=tuple(feed))
    except func_timeout.FunctionTimedOut:
        print("%s: timeout" % feed[1])
    except Exception as e:
        print("%s: %s" % (feed[1], e))
    return []

def fetchAll():
    """Descarga todos los feeds de todos los idiomas a la vez. Devuelve {url: entradas}."""
    feeds = [f for lang in LANGUAGES for section in SECTIONS for f in strings[lang]["entries"][section]]
    with ThreadPoolExecutor(max_workers=16) as pool:
        results = {f[0]: entries for f, entries in zip(feeds, pool.map(parseFeedSafe, feeds))}
    empty = [f[1] for f in feeds if not results[f[0]]]
    if empty:
        print("Feeds without entries (%d): %s" % (len(empty), ", ".join(empty)))
    return results

def sortFeeds(feed):
    return sorted(feed, key=lambda entry: entry[5], reverse=True)

def limitFeeds(feed):
    return feed[0:150]

def uploadFileS3(localFile):
    import boto3
    boto3.resource('s3').Bucket(BUCKET).upload_file(WORK_DIR + '/' + localFile, localFile, ExtraArgs={'ContentType': 'text/html', 'CacheControl': 'public, max-age=300'})


# ---------- HTML ----------

def sectionUrl(lang, section):
    """URL absoluta de una sección en un idioma: /, /videos/, /es/more/..."""
    prefix = "/" if lang == "en" else "/%s/" % lang
    return prefix + SECTIONS[section]["dir"]

def pageTitle(section, lang):
    sectionTitle = SECTIONS[section]["title"]
    langFull = strings[lang]["langFull"]
    if sectionTitle is None:
        prefix = "" if lang == "en" else "%s - " % langFull
    else:
        prefix = "%s - " % sectionTitle if lang == "en" else "%s (%s) - " % (sectionTitle, langFull)
    return prefix + SITE_NAME

def barItem(cssClass, href, text, active):
    classes = cssClass + (" item-active" if active else "")
    return '<div class="%s">\n<a href="%s">%s</a>\n</div>\n' % (classes, href, text)

def createFilterBar(section, lang):
    def langItem(code):
        return barItem("language-bar-item", sectionUrl(code, section), code.upper(), code == lang)

    topics = "".join(
        barItem("topic-bar-item", sectionUrl(lang, name), info["label"], name == section)
        for name, info in SECTIONS.items()
    )
    return (
        '<div class="filter-bar"><div class="language-bar">\n'
        '<div class="language-bar-title"><span>Language:</span></div>'
        + "".join(langItem(c) for c in LANGUAGES_VISIBLE)
        + '<div class="language-bar-item other-div">\n<span>...</span>\n<div class="other-languages">\n'
        '<div class="language-bar-item no-hover">\n<span>&nbsp;</span>\n</div>\n'
        + "".join(langItem(c) for c in LANGUAGES_HIDDEN)
        + '</div>\n</div>\n</div>\n'
        '<div class="topic-bar">\n<div class="topic-bar-title">\n<span>Topic:</span>\n</div>\n'
        + topics
        + '</div>\n</div>'
    )

def alternateLinks(section):
    """Enlaces hreflang a la misma sección en cada idioma."""
    links = "".join(
        '<link rel="alternate" hreflang="%s" href="%s%s">\n' % (strings[code]["lang"], SITE_URL, sectionUrl(code, section))
        for code in LANGUAGES
    )
    return links + '<link rel="alternate" hreflang="x-default" href="%s%s">\n' % (SITE_URL, sectionUrl("en", section))

def createHeader(section, lang):
    return (
        '<!DOCTYPE html>\n'
        '<html lang="%s">\n'
        '<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
        '<meta name="description" content="%s">\n'
        '<title>%s</title><link rel="shortcut icon" href="/favicon.png" type="image/png">\n'
        + alternateLinks(section) +
        '<link rel="stylesheet" href="/main.min.css">\n</head>\n'
        '<body>\n<div class="topbar">\n<div class="main-title">\n<a href="/"><h1>%s</h1></a>\n</div>\n'
        '<div class="topbar-links"><div class="topbar-link-item"><a href="/about.html">About</a>\n</div>\n</div>\n</div>\n'
    ) % (strings[lang]["lang"], strings[lang]["websiteDesc"], pageTitle(section, lang), SITE_NAME)

def createEntries(file, entries):
    file.write("<div class=\"post-list\">\n")
    for entry in entries:
        dtentry = datetime.datetime.fromisoformat(entry[2])
        tz = pytz.timezone("UTC")
        dtentry = dtentry.astimezone(tz)
        file.write("<div class=\"post-item\">\n")
        file.write("<a target=\"_blank\" rel=\"noopener\" href=\"%s\">\n" % html.escape(entry[1], quote=True))
        file.write("<h2>%s</h2>\n" % html.escape(entry[0]))
        file.write("</a>\n")
        file.write("<a target=\"_blank\" rel=\"noopener\" href=\"%s\">%s</a>\n" % (html.escape(entry[4], quote=True), html.escape(entry[3])))
        file.write("<time datetime=\"%s\">%s</time>\n" % (entry[2], dtentry.strftime('%a, %d %b %Y %H:%M')))
        file.write("</div>\n")
    file.write("</div>\n")

def createPage(file, entries, section, lang):
    file.write(createHeader(section, lang))
    file.write(createFilterBar(section, lang))
    createEntries(file, entries)
    file.write(FOOTER)


# ---------- Proceso principal ----------

def mainProcess(section, feedInfo, lang, fetched):
    path = ("" if lang == "en" else lang + "/") + SECTIONS[section]["dir"]
    receivedFeeds = [e for feed in feedInfo for e in fetched[feed[0]]]

    # Sin ninguna entrada (p. ej. corte de red) se conserva la página anterior en S3
    if feedInfo and not receivedFeeds:
        print("%s: no entries, page not updated" % path)
        return False

    joinFeedSorted = limitFeeds(sortFeeds(receivedFeeds))

    os.makedirs(WORK_DIR + "/" + path, exist_ok=True)
    with open(WORK_DIR + "/" + path + "index.html", "w") as htmlFile:
        createPage(htmlFile, joinFeedSorted, section, lang)
    print(path + "index.html saved")
    if not OUTPUT_DIR:
        uploadFileS3(path + "index.html")
    return True

def main():
    fetched = fetchAll()
    failed = []
    for lang in LANGUAGES:
        for section in SECTIONS:
            if not mainProcess(section, strings[lang]["entries"][section], lang, fetched):
                failed.append("%s/%s" % (lang, section))
    # Falla al final, tras generar el resto, para que Lambda registre el error
    if failed:
        raise RuntimeError("Pages not updated: " + ", ".join(failed))

if __name__ == "__main__":
    main()
