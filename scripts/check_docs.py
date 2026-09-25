#!/usr/bin/env python3
"""Check the published HTML graph, metadata, anchors, and sitemap offline."""
import json
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin, urlsplit, unquote
from xml.etree import ElementTree as ET
from build_docs import BASE, PAGES, ROOT

class Page(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.ids = set()
        self.links = []
        self.canonicals = []
        self.alternates = {}
        self.h1 = 0
        self.lang = None
        self.meta = {}
        self.title = ""
        self.in_title = False
        self.schema = []
        self.in_schema = False
        self.schema_text = ""
        self.feed(text)
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if "id" in a:
            assert a["id"] not in self.ids, f"Duplicate id: {a['id']}"
            self.ids.add(a["id"])
        if tag == "html": self.lang = a.get("lang")
        if tag == "h1": self.h1 += 1
        if tag == "title": self.in_title = True
        if tag == "meta": self.meta[a.get("name", a.get("property"))] = a.get("content")
        if tag in ("a", "link") and a.get("href"): self.links.append(a["href"])
        if tag == "img" and a.get("src"): self.links.append(a["src"])
        if tag == "link" and a.get("rel") == "canonical": self.canonicals.append(a["href"])
        if tag == "link" and a.get("hreflang"): self.alternates[a["hreflang"]] = a["href"]
        if tag == "script":
            assert a.get("type") == "application/ld+json", "Content should not require scripts"
            self.in_schema = True
    def handle_data(self, data):
        if self.in_title: self.title += data
        if self.in_schema: self.schema_text += data
    def handle_endtag(self, tag):
        if tag == "title": self.in_title = False
        if tag == "script" and self.in_schema:
            self.schema.append(json.loads(self.schema_text)); self.schema_text = ""; self.in_schema = False

def main():
    pages = {BASE + path: Page((ROOT / "docs" / path / "index.html").read_text(encoding="utf-8")) for path, *_ in PAGES}
    titles, descriptions = set(), set()
    links = 0
    for path, lang, _, title, description, alternate in PAGES:
        url = BASE + path
        page = pages[url]
        assert page.lang == lang and page.h1 == 1 and "main" in page.ids, url
        assert page.title == title and page.meta.get("description") == description, url
        assert page.canonicals == [url] and "noindex" not in page.meta.get("robots", ""), url
        assert page.meta.get("og:url") == url and page.meta.get("og:title") == title, url
        assert page.meta.get("twitter:card") == "summary_large_image", url
        assert page.title not in titles and description not in descriptions, "Duplicate page metadata"
        titles.add(page.title); descriptions.add(description)
        assert page.alternates[lang] == url and page.alternates["ko" if lang == "en" else "en"] == BASE + alternate, url
        for locale in ("en", "ko", "x-default"):
            assert page.alternates[locale] in pages, url
            assert pages[page.alternates[locale]].alternates[lang] == url, "Nonreciprocal language link"
        graph = page.schema[0]["@graph"]
        assert graph[0]["url"] == url and graph[0]["inLanguage"] == lang
        assert graph[1]["@type"] == "SoftwareSourceCode" and graph[1]["name"] == "LessonPair"
        for link in page.links + [page.meta["og:image"], page.meta["twitter:image"]]:
            target = urljoin(url, link)
            if not target.startswith(BASE): continue
            parts = urlsplit(target)
            basepath = urlsplit(BASE).path
            rel = unquote(parts.path[len(basepath):])
            dest = ROOT / "docs" / rel
            if parts.path.endswith("/"): dest /= "index.html"
            assert dest.is_file(), f"Missing local link from {url}: {target}"
            if parts.fragment:
                page_url = target.split("#")[0]
                assert page_url in pages and unquote(parts.fragment) in pages[page_url].ids, f"Missing anchor: {target}"
            links += 1
    sitemap = ET.parse(ROOT / "docs/sitemap.xml")
    ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9", "xh": "http://www.w3.org/1999/xhtml"}
    locs = [e.text for e in sitemap.findall("sm:url/sm:loc", ns)]
    assert len(locs) == len(pages) and set(locs) == set(pages), "Sitemap coverage mismatch"
    for node in sitemap.findall("sm:url", ns):
        loc = node.find("sm:loc", ns).text
        alternatives = {x.attrib["hreflang"]: x.attrib["href"] for x in node.findall("xh:link", ns)}
        assert alternatives == pages[loc].alternates, "Sitemap language mismatch"
    metadata = json.loads((ROOT / "docs/project.json").read_text(encoding="utf-8"))
    assert metadata["homepage"] == BASE and metadata["license"] == "MIT"
    assert (ROOT / "docs/.nojekyll").is_file()
    print(f"Validated {len(pages)} HTML pages, {links} local links/assets/anchors, reciprocal locales, JSON-LD, and sitemap.")

if __name__ == "__main__": main()
