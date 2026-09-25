<p align="center"><img src="docs/overview.svg" alt="LessonPair: one language lesson, two connected study pages" width="920"></p>

<h1 align="center">LessonPair</h1>
<p align="center"><strong>Watch. Talk. Rewrite. Keep the learning connected.</strong></p>
<p align="center">
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-2563eb" alt="MIT license"></a>
  <img src="https://img.shields.io/badge/Python-3.10%2B-3776ab" alt="Python 3.10 or later">
  <img src="https://img.shields.io/badge/runtime_dependencies-0-16a34a" alt="Zero third-party runtime dependencies">
  <a href="https://github.com/sjskoko/lesson-pair/actions/workflows/check.yml"><img src="https://github.com/sjskoko/lesson-pair/actions/workflows/check.yml/badge.svg" alt="Checks"></a>
</p>
<p align="center"><a href="README.ko.md">한국어</a> · <a href="#try-it-in-60-seconds">Quick start</a> · <a href="examples/README.md">Synthetic example</a> · <a href="docs/usage.md">Installation & GPT use</a></p>

**An open agent skill that turns a video and a live language lesson into two linked Notion pages: preparation and review.** Keep the original writing, understand the corrections, and practice again without losing the connection to the source.

Designed for English study with Korean explanations; the workflow can be adapted to other languages. The included renderer formats supplied material offline. A connected AI assistant handles understanding and corrections.

## What you get

| Before the lesson | After the lesson |
| --- | --- |
| Video and available transcript | Original writing, preserved unchanged |
| Section-by-section explanation | Teacher notes separate from AI suggestions |
| Grammar notes in context | Correction and grammar tables |
| Three expressions to use | Hidden-answer recall and a timed rewrite |

One session connects both pages. Use Notion views for **all lessons**, **review pending**, **calendar**, and **reusable templates**.

## Why this exists

Study materials and lesson corrections often end up in different places. LessonPair makes them a pair—and keeps the learner's original work intact. It also includes a regression checker for an easy-to-miss failure: a successful Notion write that displays literal `<table>` tags instead of a real table.

- **Source-preserving:** keep learner writing and teacher notes; label AI additions.
- **Repeatable:** reuse session structure without duplicating existing lessons.
- **Honest:** no invented transcripts, grades, completed practice, or automatic reminders.
- **Focused context:** a small skill entry point loads references only when needed.
- **Offline utilities:** standard-library Python, no API key, telemetry, or network calls.

## Try it in 60 seconds

Requires Python 3.10+ and Git. The example is entirely fictional.

```bash
git clone https://github.com/sjskoko/lesson-pair.git
cd lesson-pair
python3 skills/lesson-pair/scripts/lesson_pair.py render examples/lesson.synthetic.json --out output/demo
python3 skills/lesson-pair/scripts/lesson_pair.py check output/demo/02-review.notion.md
```

Open `output/demo/session.md`. The output contains two study drafts and the byte-preserved input JSON. **This command does not call an AI model or upload anything to Notion.** `.notion.md` uses Notion MCP's enhanced Markdown; it is not guaranteed to render when pasted into the ordinary Notion editor.

## Use the skill with your assistant

Install the `skills/lesson-pair` folder using your host's skill installer. For a Codex setup with the built-in installer, ask:

```text
Use $skill-installer to install the lesson-pair skill from
https://github.com/sjskoko/lesson-pair/tree/main/skills/lesson-pair
```

Then, with a connected Notion integration:

```text
Use $lesson-pair to organize this lesson in my Notion study hub.
Pair the existing video preparation page with today's writing and feedback.
Keep my original writing unchanged and give me a short rewrite exercise.
```

For ChatGPT Work, ask its skill creator to install from that folder. Use `@lesson-pair` where supported. Host capabilities and organization policies differ; see [the full guide](docs/usage.md). This repository is a skill package, not a hosted service or a published plugin-directory listing.

## “No tokens” explained

| Action | What it needs |
| --- | --- |
| Read or download this public repository | No GitHub personal access token for ordinary public access; provider rate limits may apply |
| Run the local formatter/checker | Python only; no model tokens or API key |
| Ask an AI to understand and correct a lesson | Model context/tokens and the host's normal usage limits |
| Write private Notion pages | An authenticated Notion connection with access to those pages |

An open-source license cannot remove model usage charges. Publishing here does not automatically install the skill into every GPT. [Official skill documentation](https://learn.chatgpt.com/docs/build-skills) explains the host workflow; [OpenAI's context guidance](https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra) explains lazy-loaded references.

## Privacy

Every sample here is synthetic. No real learner records, teacher conversations, private Notion IDs, or account credentials are included. Keep your own data outside the repository or under an ignored `private/` or `local/` directory. When an assistant uses Notion, its platform and Notion process the data you authorize; the repository itself has no backend.

## Development

```bash
python3 -m unittest discover -s tests -v
```

See [CONTRIBUTING.md](CONTRIBUTING.md) for small, useful contributions: clearer examples, additional languages, and formatting regressions. See [SECURITY.md](SECURITY.md) before reporting sensitive problems.

If this helps your study routine, a star helps others discover it. Share improvements and **synthetic** examples through issues—never private lesson screenshots.

MIT licensed. Independent community project; not affiliated with OpenAI or Notion.
