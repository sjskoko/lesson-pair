# LessonPair — explain a video you love in your own English

**You understood the video. Can you explain it?**

One English video, a short conversation with your AI, and a comparison of **your own** first and later attempts. Open-source guided English practice for ChatGPT, compatible agents, and your own model.

[![LessonPair: your video, your AI, your English](docs/social-preview.svg)](https://sjskoko.github.io/lesson-pair/)

**[See the demo](https://sjskoko.github.io/lesson-pair/#demo)** · [Get started](docs/usage.md) · [ChatGPT / Codex plugin](docs/plugin.md) · [한국어](README.ko.md)

[![Checks](https://github.com/sjskoko/lesson-pair/actions/workflows/check.yml/badge.svg)](https://github.com/sjskoko/lesson-pair/actions/workflows/check.yml)
[![MIT license](https://img.shields.io/badge/license-MIT-blue)](LICENSE)

## Three things to do

1. **Bring a video you care about.** Use available English captions or supply a transcript excerpt.
2. **Have a short conversation.** Try explaining it. Your AI helps with what you couldn't express, one question at a time.
3. **See your own before and after.** Try again, then compare your actual attempts. Reuse an expression in a different context later.

No teacher or Notion account required. Start with a few sentences; a 60-second retelling is an optional goal. If captions cannot be accessed, LessonPair asks for them instead of inventing a lesson.

## A fictional preview

All text below was fabricated for the demo. These are not user results or evidence of efficacy.

| Moment | Example |
| --- | --- |
| Learner's first attempt | “Trees makes shade. Roots need place.” |
| AI practice | Focus on “provide shade” and “room to grow”; ask “What do roots need?” |
| Learner's later attempt | “Trees provide shade. Their roots need room to grow.” |
| Later recall | Explain why balcony plants need enough room. |

The difference that matters: **the learner supplies the retry**. An AI rewrite is labeled as AI feedback, never counted as learner progress. Assistance is recorded; no fabricated scores or “fluent in 7 days” promises. [Explore the interaction](examples/guided-demo.md).

## Choose your AI

| Route | What you need | What runs |
| --- | --- | --- |
| ChatGPT / Codex plugin | A supported plugin host | The model already active in your host; no separate provider key |
| Another assistant | A skill loader, or attach the portable instructions | Your existing assistant |
| Your own provider / local model | Python 3.10+, compatible Chat Completions endpoint | A resumable terminal tutor with your endpoint and model |
| Notes only | Python 3.10+ | Offline export and the legacy Notion formatter |

**Plugin package:** [`plugins/lesson-pair`](plugins/lesson-pair) · **Repository marketplace:** [`.agents/plugins/marketplace.json`](.agents/plugins/marketplace.json).

Where supported, register this marketplace:

```bash
codex plugin marketplace add sjskoko/lesson-pair --ref main
```

Then install **LessonPair** through your host's plugin interface. Registration alone does not install it. Workspace policies and host availability apply. This is a repository-distributed plugin, **not an approved public-directory listing**. [Installation and validation](docs/plugin.md).

For a local provider:

```bash
export LESSONPAIR_BASE_URL='http://localhost:11434/v1'
export LESSONPAIR_MODEL='YOUR-INSTALLED-MODEL'
python skills/lesson-pair/scripts/learn.py start --source examples/video.synthetic.txt
python skills/lesson-pair/scripts/learn.py run
python skills/lesson-pair/scripts/learn.py export
```

Start your compatible local model server separately. For HTTPS providers, use an environment variable for the API key. [Provider setup, URL captions, and resuming](skills/lesson-pair/references/own-ai.md).

## Built around your work

- Short, adaptive practice from an actual attempt; cues and examples when needed.
- Originals, AI feedback, learner retries, and assistance kept separate.
- Transcript-grounded prompts; clear fallback when a video is inaccessible.
- Private local session files, interruption recovery, Markdown export, optional Notion pairs.
- English and Korean documentation; explanations can follow the learner's language.

Retrieval and later practice inform the design. **This product's learning impact has not been established by a controlled study.** Text sessions do not assess pronunciation. [Design and evaluation plan](docs/learning-design.md).

## Privacy and cost

Public examples are synthetic. Real transcripts and learner records belong in private storage, not issues or pull requests. `start --source` and `export` run offline; `start --url` uses optional yt-dlp to fetch available English captions; `run` sends your transcript and attempts to your selected AI endpoint. No analytics or key collection is built into the website.

The code and skill are MIT licensed. AI use still consumes tokens and is subject to your host/provider's limits and charges. A free skill is not zero-token inference. API keys stay in environment variables; remote endpoints require HTTPS and redirects are rejected. [Privacy details](SECURITY.md).

## Legacy and contributing

The previous teacher-led, paired Notion workflow is preserved at [`legacy/english`](https://github.com/sjskoko/lesson-pair/tree/legacy/english). Its formatter and schema remain supported on main. Existing study pages are not migrated automatically. [Legacy reference](docs/legacy.md).

```bash
python -m unittest discover -s tests -v
python scripts/build_plugin.py --check
python scripts/build_docs.py --check
python scripts/check_docs.py
```

Try one video. If this helps you practice, **star the repository** and share a synthetic example or a specific improvement. [Contributing](CONTRIBUTING.md) · [Share kit](docs/launch.md) · [AI documentation index](https://sjskoko.github.io/lesson-pair/llms.txt).

Independent project; not affiliated with OpenAI, Notion, YouTube, or any model provider.
