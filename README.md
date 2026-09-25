# LessonPair — turn a video you love into English you can use

**Watch something interesting. Explain it in your own English. See what changed.**

An open-source English learning skill and ChatGPT/Codex plugin that turns one English video into a short, guided conversation. Practice comes from what **you** struggled to say, and your progress card compares **your first answer with your own retry**.

[Website & demo](https://sjskoko.github.io/lesson-pair/) · [Get started](#start-with-your-ai) · [한국어](README.ko.md) · [Legacy version](docs/legacy.md)

[![Checks](https://github.com/sjskoko/lesson-pair/actions/workflows/check.yml/badge.svg)](https://github.com/sjskoko/lesson-pair/actions/workflows/check.yml)
[![MIT](https://img.shields.io/badge/license-MIT-blue)](LICENSE)

[![LessonPair: one video, your first answer, your own retry](docs/social-preview.svg)](https://sjskoko.github.io/lesson-pair/#demo)

## One video. Three things to do.

1. **Pick a video.** Provide an English video URL. The assistant uses available captions; if it cannot access them, paste a transcript or short excerpt.
2. **Have a short conversation.** Try 1–3 sentences first. Your AI picks one or two expression gaps, asks one question at a time, and helps when you get stuck.
3. **See your own before and after.** Explain it again. Compare the two attempts, then try a new-context recall prompt later.

No teacher, Notion account, or long worksheet is required. Explanations can be in your language. A one-minute retelling is an optional goal, not an entry requirement.

## What makes the pair useful?

| First attempt | Practice chosen from that attempt | Learner's retry |
| --- | --- | --- |
| “Trees makes shade. Roots need place.” | Express “provide shade” and “room to grow”; answer one focused question. | “Trees provide shade. Their roots need room to grow.” |

**Fictional demonstration**, not a real learner result or efficacy claim. In a real session, the learner writes both attempts. AI rewrites stay labeled as AI suggestions; an assisted retry stays labeled as assisted. [Read the guided example](examples/guided-demo.md).

Video learning and retrieval practice are established ideas. LessonPair's product focus is the small, personal loop connecting a source to a learner's expressive gaps and a visible retry. We have not demonstrated learning gains in a controlled study.

## Start with your AI

| Route | How it works |
| --- | --- |
| **ChatGPT / Codex plugin** | Install the skills-only plugin through a supported repository marketplace or workspace workflow. It uses your host's current AI. [Installation details](docs/plugin.md). |
| **Another assistant / custom GPT** | Attach the portable skill and two learning references, then paste the starter prompt below. This is manual prompt use. |
| **Your own model endpoint** | Run the local Python tutor with an OpenAI-compatible API, including a local Ollama endpoint. [Provider and privacy guide](skills/lesson-pair/references/own-ai.md). |

Starter prompt after loading the skill:

> Use LessonPair to help me explain this English video in my own words: [URL]. Use available captions, or ask me for an excerpt. Give me one small question at a time. Let me answer before showing a model answer. Explain in [my language].

**Codex repository marketplace:**

```bash
codex plugin marketplace add sjskoko/lesson-pair --ref main
```

Then install **lesson-pair** from the added marketplace in a supported plugin interface. Adding the source alone does not install the plugin. ChatGPT availability depends on your client and workspace; this project is **not yet listed in OpenAI's public plugin directory**. [Portable files and fallback](docs/plugin.md).

## Bring your own model

Python 3.10+; no third-party Python dependency for transcript-file sessions.

```bash
git clone https://github.com/sjskoko/lesson-pair.git
cd lesson-pair
export LESSONPAIR_BASE_URL='http://localhost:11434/v1'
export LESSONPAIR_MODEL='YOUR-INSTALLED-MODEL'
python skills/lesson-pair/scripts/learn.py start --source examples/transcript.synthetic.txt
python skills/lesson-pair/scripts/learn.py run
python skills/lesson-pair/scripts/learn.py export
```

Start your local model server separately. For a remote compatible endpoint, configure its HTTPS base URL, model, and `LESSONPAIR_API_KEY` using your environment/secret manager. Never paste keys into chat, GitHub, or the website. The API contract is tested against a local stub; individual providers and model quality require their own verification.

Optional `yt-dlp` enables `start --url YOUTUBE_URL` to attempt English captions. This is caption retrieval, not automatic transcription; unavailable captions require a supplied transcript. `/hint`, `/example`, and `/quit` keep the terminal session manageable. Attempts survive failed API calls and can be resumed.

## Keep your work portable and private

- Default records stay under ignored `private/`. The CLI sends source text and answers only to the model endpoint you configure. Provider policies and charges apply.
- The plugin uses the active host AI; it includes no credential collection, server, or telemetry. The website has no API-key form.
- Save Markdown, or ask a connected assistant to use the optional [paired Notion workflow](skills/lesson-pair/references/notion-workflow.md). Originals and feedback remain separate; existing records are not migrated automatically.
- No bundled speech recognition, pronunciation scoring, automatic reminders, or guaranteed learning outcomes.
- MIT-licensed code is free; AI inference still uses tokens, compute, and host/provider limits. GitHub hosting cannot make GPT usage unlimited or token-free.
- **All public samples are fabricated.** Do not commit real sessions or transcripts, even when reporting a bug.

## Legacy and development

The previous Notion-first release is preserved on [`legacy/english`](https://github.com/sjskoko/lesson-pair/tree/legacy/english), pinned in [legacy documentation](docs/legacy.md). Its formatter and JSON format still work. The new tutor uses a separate versioned session schema.

```bash
python -m unittest discover -s tests -v
python scripts/build_plugin.py --check
python scripts/build_docs.py --check
python scripts/check_docs.py
```

Edit `skills/lesson-pair`, then run `python scripts/build_plugin.py` to update the plugin copy. See [contributing](CONTRIBUTING.md), [security](SECURITY.md), and [release notes](CHANGELOG.md).

If the workflow is useful, **star it to find it again**. Share a synthetic example or one specific improvement through issues. [Shareable introduction](docs/launch.md) · [AI documentation index](https://sjskoko.github.io/lesson-pair/llms.txt)

Independent project; not affiliated with OpenAI, Notion, Ollama, or video platforms.
