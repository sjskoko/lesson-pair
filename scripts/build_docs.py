#!/usr/bin/env python3
"""Build a crawlable bilingual GitHub Pages site using only Python's stdlib."""
import argparse
import html
import json
from pathlib import Path
from xml.etree import ElementTree as ET
ROOT = Path(__file__).resolve().parents[1]
BASE = "https://sjskoko.github.io/lesson-pair/"
REPO = "https://github.com/sjskoko/lesson-pair"
RAW = "https://raw.githubusercontent.com/sjskoko/lesson-pair/main/"
PAGES = [
    ("", "en", "site/en.html", "LessonPair — Notion English Lesson Notes & AI Skill", "Pair video preparation, English writing corrections, and recall practice in Notion. Open-source agent skill, synthetic demo, and offline Python formatter.", "ko/"),
    ("ko/", "ko", "site/ko.html", "LessonPair — 노션 영어 학습·수업 정리 AI 스킬", "영상 예습부터 영어 작문 교정과 복습까지 노션 페이지 두 개로 연결하세요. LessonPair 오픈소스 스킬의 가상 예시와 설치 방법을 확인하세요.", ""),
    ("guide/", "en", "site/guide.html", "Install LessonPair — Notion English Learning Skill Guide", "Install the LessonPair agent skill, set up paired Notion lesson pages, or run the offline Python demo. Includes privacy guidance and AI-readable source links.", "ko/guide/"),
    ("ko/guide/", "ko", "site/guide.ko.html", "LessonPair 설치 가이드 — 노션 영어 수업·복습 정리", "Codex·ChatGPT Work용 LessonPair 설치, 노션 수업 구조, Python 로컬 실행, 표 오류 해결 방법과 AI가 읽을 공개 자료를 안내합니다.", "guide/"),
]

def build():
    output = {}
    for path, lang, source, title, description, alternate in PAGES:
        ko = lang == "ko"
        home = BASE + ("ko/" if ko else "")
        guide = home + "guide/"
        en_url = BASE + (alternate if ko else path)
        ko_url = BASE + (path if ko else alternate)
        url = BASE + path
        schema = {"@context": "https://schema.org", "@graph": [
            {"@type": "WebPage", "@id": url + "#page", "url": url, "name": title, "description": description, "inLanguage": lang, "about": {"@id": BASE + "#software"}},
            {"@type": "SoftwareSourceCode", "@id": BASE + "#software", "name": "LessonPair", "description": "Open-source agent skill and offline Python formatter for paired Notion English lesson notes.", "url": BASE, "codeRepository": REPO, "license": REPO + "/blob/main/LICENSE", "programmingLanguage": "Python", "runtimePlatform": "Python 3.10+", "inLanguage": ["en", "ko"], "keywords": ["Notion", "English learning", "lesson notes", "Agent Skills"], "image": BASE + "social-preview.png"}]}
        body = (ROOT / source).read_text(encoding="utf-8")
        output["docs/" + path + "index.html"] = f'''<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(description, quote=True)}">
<meta name="robots" content="index,follow,max-image-preview:large">
<meta name="theme-color" content="#0b1120">
<link rel="canonical" href="{url}">
<link rel="alternate" hreflang="en" href="{en_url}">
<link rel="alternate" hreflang="ko" href="{ko_url}">
<link rel="alternate" hreflang="x-default" href="{en_url}">
<link rel="sitemap" type="application/xml" href="{BASE}sitemap.xml">
<link rel="alternate" type="text/plain" href="{BASE}llms.txt" title="AI documentation index">
<link rel="stylesheet" href="{BASE}style.css">
<link rel="icon" type="image/svg+xml" href="{BASE}favicon.svg">
<meta property="og:type" content="website">
<meta property="og:site_name" content="LessonPair">
<meta property="og:title" content="{html.escape(title, quote=True)}">
<meta property="og:description" content="{html.escape(description, quote=True)}">
<meta property="og:url" content="{url}">
<meta property="og:locale" content="{'ko_KR' if ko else 'en_US'}">
<meta property="og:locale:alternate" content="{'en_US' if ko else 'ko_KR'}">
<meta property="og:image" content="{BASE}social-preview.png">
<meta property="og:image:width" content="1280">
<meta property="og:image:height" content="640">
<meta property="og:image:alt" content="LessonPair: turn your English mistakes into your next practice session">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{html.escape(title, quote=True)}">
<meta name="twitter:description" content="{html.escape(description, quote=True)}">
<meta name="twitter:image" content="{BASE}social-preview.png">
<script type="application/ld+json">{json.dumps(schema, ensure_ascii=False)}</script>
</head>
<body>
<a class="skip" href="#main">{'본문으로 이동' if ko else 'Skip to content'}</a>
<header><a class="brand" href="{home}"><span class="mark" aria-hidden="true">LP</span>LessonPair</a><nav class="nav" aria-label="{'주 메뉴' if ko else 'Main navigation'}"><a href="{home}#demo">{'예시' if ko else 'Demo'}</a><a href="{guide}">{'설치 가이드' if ko else 'Get started'}</a><a href="{BASE + alternate}" lang="{'en' if ko else 'ko'}">{'English' if ko else '한국어'}</a><a href="{REPO}">GitHub ↗</a></nav></header>
<main id="main"{' class="guide-main"' if 'guide/' in path else ''}>
{body}</main>
<footer><div class="footer-links"><a href="{REPO}">GitHub</a><a href="{REPO}/blob/main/LICENSE">MIT license</a><a href="{BASE}llms.txt">AI index</a><a href="{BASE}sitemap.xml">Sitemap</a><a href="{REPO}/issues/new?template=feature_request.yml">{'개선 제안' if ko else 'Suggest an improvement'}</a></div><p>{'공개 예시는 모두 가상 자료입니다. 실제 학습 기록을 공개 이슈에 올리지 마세요.' if ko else 'Every public example is synthetic. Keep real lesson records out of public issues.'}</p><p>{'OpenAI·Notion과 제휴하지 않은 독립 오픈소스 프로젝트입니다.' if ko else 'Independent open-source project. Not affiliated with OpenAI or Notion.'}</p></footer>
</body>
</html>
'''
    ns = "http://www.sitemaps.org/schemas/sitemap/0.9"
    xh = "http://www.w3.org/1999/xhtml"
    ET.register_namespace("", ns)
    ET.register_namespace("xhtml", xh)
    urlset = ET.Element(f"{{{ns}}}urlset")
    for path, lang, _, _, _, alternate in PAGES:
        url = ET.SubElement(urlset, f"{{{ns}}}url")
        ET.SubElement(url, f"{{{ns}}}loc").text = BASE + path
        en = BASE + (alternate if lang == "ko" else path)
        ko = BASE + (path if lang == "ko" else alternate)
        for locale, target in [("en", en), ("ko", ko), ("x-default", en)]:
            ET.SubElement(url, f"{{{xh}}}link", {"rel": "alternate", "hreflang": locale, "href": target})
    ET.indent(urlset)
    output["docs/sitemap.xml"] = '<?xml version="1.0" encoding="utf-8"?>\n' + ET.tostring(urlset, encoding="unicode") + "\n"
    output["docs/.nojekyll"] = ""
    output["docs/favicon.svg"] = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="14" fill="#d6f879"/><path d="M14 17v30h16v-7H21V17zm22 0v30h7V36h5c15 0 15-19 0-19zm7 7h5c5 0 5 5 0 5h-5z" fill="#0b1120"/></svg>\n'
    index = f'''# LessonPair

> Open-source agent skill for Notion English lesson notes: pair video preparation with original writing, attributed corrections, and recall practice. Includes a standard-library Python formatter.

This is a project-specific index at {BASE}llms.txt. It is a navigation aid for direct retrieval, not a crawler-control file or an automatic installation mechanism.

## Start here
- [English overview]({BASE}): purpose, fictional demo, workflow, and FAQ.
- [한국어 소개]({BASE}ko/): 노션 영어 학습 스킬 소개와 가상 예시.
- [Installation guide]({BASE}guide/): host options, Notion structure, offline use, privacy.
- [한국어 설치 가이드]({BASE}ko/guide/): 설치·수업 구조·표 오류 해결.
- [Repository]({REPO}): canonical source and contributions.

## Skill source (read progressively)
- [SKILL.md]({RAW}skills/lesson-pair/SKILL.md): entry point and workflow selection.
- [Notion workflow]({RAW}skills/lesson-pair/references/notion-workflow.md): setup, writes, idempotence, verification.
- [Page templates]({RAW}skills/lesson-pair/references/page-templates.md): preparation and review page structure.
- [Python formatter]({RAW}skills/lesson-pair/scripts/lesson_pair.py): render supplied JSON; check Notion table markup.

## Examples and project facts
- [Synthetic input]({RAW}examples/lesson.synthetic.json): fictional material, never a real learner record.
- [Clickable demo]({REPO}/blob/main/examples/demo.md): paired pages and hidden answers on GitHub.
- [Plain-text reference bundle]({BASE}llms-full.txt): overview, installation, and skill references in one file.
- [Project metadata]({BASE}project.json): stable URLs, requirements, license, and limitations.
- [MIT license]({RAW}LICENSE)

AI execution still uses model tokens and the host's limits. Private Notion writes require an authorized connection. The local formatter has no network calls, telemetry, or automatic language correction. Missing transcripts, meaning, scores, or completion must not be invented. Public examples are synthetic.
'''
    output["docs/llms.txt"] = index
    output["llms.txt"] = index
    refs = ["README.md", "README.ko.md", "docs/usage.md", "skills/lesson-pair/SKILL.md", "skills/lesson-pair/references/notion-workflow.md", "skills/lesson-pair/references/page-templates.md"]
    output["docs/llms-full.txt"] = "# LessonPair — public reference bundle\n\nGenerated from repository sources. For the smallest context, start with llms.txt and fetch only relevant files. All example material is synthetic.\n\n" + "\n\n".join(f"---\nSource: {RAW}{p}\n\n{(ROOT / p).read_text(encoding='utf-8').strip()}" for p in refs) + "\n"
    output["docs/project.json"] = json.dumps({
        "name": "LessonPair", "slug": "lesson-pair", "description": "Open-source Notion English lesson notes skill with paired preparation and review pages.",
        "homepage": BASE, "repository": REPO, "license": "MIT", "languages": ["en", "ko"],
        "skill_entrypoint": RAW + "skills/lesson-pair/SKILL.md", "install_directory": REPO + "/tree/main/skills/lesson-pair",
        "documentation": {"en": BASE + "guide/", "ko": BASE + "ko/guide/", "index": BASE + "llms.txt", "full_text": BASE + "llms-full.txt"},
        "requirements": {"offline_formatter": "Python >= 3.10", "ai_workflow": "Compatible skill host; authorized Notion integration for page writes"},
        "limitations": ["No bundled transcription or automatic speech scoring", "Offline formatter does not generate corrections or write to Notion", "AI execution uses model tokens and host limits", "All public examples are synthetic"]
    }, ensure_ascii=False, indent=2) + "\n"
    return output

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Fail if committed generated files are stale")
    args = parser.parse_args()
    output = build()
    if args.check:
        stale = [p for p, content in output.items() if not (ROOT / p).exists() or (ROOT / p).read_text(encoding="utf-8") != content]
        if stale:
            raise SystemExit("Rebuild docs; stale files: " + ", ".join(stale))
        print(f"Generated documentation is current ({len(output)} files).")
    else:
        for path, content in output.items():
            target = ROOT / path
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(content, encoding="utf-8")
        print(f"Built {len(output)} documentation files.")

if __name__ == "__main__":
    main()
