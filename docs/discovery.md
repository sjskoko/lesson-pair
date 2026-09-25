# Search and AI discovery maintenance

The public documentation site is https://sjskoko.github.io/lesson-pair/ with a Korean edition at https://sjskoko.github.io/lesson-pair/ko/. GitHub Pages publishes the `main` branch's `/docs` directory. Generated HTML is committed and `.nojekyll` disables theme processing.

## Edit and validate

Edit the four `site/*.html` bodies, `docs/style.css`, or the page metadata in `scripts/build_docs.py`. The builder also derives the sitemap, project metadata, link index, and full text from repository sources.

```bash
python3 scripts/build_docs.py
python3 scripts/build_docs.py --check
python3 scripts/check_docs.py
```

CI checks that generated files are current and validates internal links, anchors, canonical URLs, language alternatives, JSON-LD, and sitemap coverage. No external dependencies or JavaScript rendering are required for the site's text and links. The only browser interaction is a native answer-reveal disclosure.

## What is configured

- Four useful HTML pages: English/Korean overview and setup guide.
- Unique titles and descriptions, self-canonical URLs, reciprocal `en`/`ko`/`x-default` alternatives.
- XML sitemap containing only canonical HTML URLs; no fictional last-modified dates.
- Open Graph and Twitter preview metadata using the public synthetic preview image.
- `WebPage` and `SoftwareSourceCode` structured data matching visible content; no fabricated ratings, adoption counts, endorsements, or review schema.
- A project-local `llms.txt` link index, a generated plain-text reference bundle, and `project.json` for direct retrieval. These are optional navigation aids, not special ranking signals or access permissions.
- Repository links point to the site and the site points back to installation, source, and contribution paths.

## Crawling and indexing boundaries

This is a GitHub Pages **project site** under `/lesson-pair/`. Crawlers use `https://sjskoko.github.io/robots.txt`, at the origin root. A `robots.txt` under the project directory would not control crawling, so none is presented as an effective crawler policy. Origin-level configuration is separate from this repository. Check the origin policy again if a user/organization site is added or its rules change.

OpenAI documents OAI-SearchBot for ChatGPT search and GPTBot separately for model training. A public site does not need to promise training permission to describe its search availability. We do not claim that reading `llms.txt` makes a GPT automatically install the skill or use zero tokens.

Once a verified Search Console or Bing Webmaster Tools property is available, submit this sitemap through the relevant account:

https://sjskoko.github.io/lesson-pair/sitemap.xml

Publishing the sitemap is not evidence that it was submitted, crawled, or indexed. Search services determine inclusion and ranking. Do not claim a ranking gain or an AI citation without observing it.

## Measure real outcomes

Use available GitHub traffic, referrers, clones, and stars; use the search provider's performance reports after property verification. Record the measurement window and baseline before comparing changes. Check a few relevant queries such as “LessonPair”, “Notion English lesson notes”, and “노션 영어 수업 정리 스킬”, while remembering search results vary and `site:` is not a complete indexing report.

Share the working demo and a concrete workflow problem where community rules permit. Do not manufacture stars, reviews, third-party mentions, or keyword pages. Public feedback and examples must be synthetic; never include learner records or private screenshots.

## Official references

- [Google: optimizing for generative AI features](https://developers.google.com/search/docs/fundamentals/ai-optimization-guide)
- [Google: robots.txt scope](https://developers.google.com/search/docs/crawling-indexing/robots/intro)
- [OpenAI: crawler overview](https://developers.openai.com/api/docs/bots)
- [GitHub: Pages publishing sources](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site)
