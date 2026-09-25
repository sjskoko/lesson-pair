# Start with one English video

## Guided chat

Install the [LessonPair plugin](plugin.md) or load the portable skill files. Give the assistant a video URL and your explanation language. It uses accessible captions or asks for a transcript/excerpt; then it guides one small action at a time.

First explain the main idea in 1–3 English sentences. Practice an expression that blocked you. Look away from examples and explain it again. Compare your actual answers. A later prompt reuses the expression in a new context.

The first attempt and retry are learner-written. AI feedback is labeled, help is recorded, and missing work stays unfinished. Typed answers do not support pronunciation scoring.

## Own AI endpoint

See [the setup guide](../skills/lesson-pair/references/own-ai.md). The Python terminal tutor supports a basic OpenAI-compatible Chat Completions contract. Use a local model server or an HTTPS provider you trust. Environment variables configure the model; keys are never stored in session files.

Start from a `.txt`, `.vtt`, or `.srt` transcript. YouTube captions can be attempted using optional yt-dlp. If captions are blocked or absent, supply a file. The tool does not download video, transcribe audio, or bypass access controls.

Default output is `private/session.json`; export produces `private/review.md`. Both paths are ignored by the repository. Use `--session` for a different session, and `/quit` to pause. Existing sessions are never silently overwritten. Failed AI responses leave a pending task for resume.

## Save to Notion, optionally

Ask your authorized, connected assistant to save the session. Keep one parent session with two linked parts: source/practice and attempts/review. Preserve originals and teacher notes in their own sections. [Notion workflow](../skills/lesson-pair/references/notion-workflow.md) includes lookup, idempotent writes, real table handling and read-back checks.

The CLI exports Markdown and does not write to Notion itself. The plugin can use a host's authorized Notion tools, but does not bundle a Notion connector.

## Legacy data

The original JSON formatter still runs:

```bash
python skills/lesson-pair/scripts/lesson_pair.py render examples/lesson.synthetic.json --out output/demo
python skills/lesson-pair/scripts/lesson_pair.py check output/demo/02-review.notion.md
```

See [legacy documentation](legacy.md) for the preserved snapshot and original schema guide.

## Costs and data

Skill code is MIT licensed. Local file formatting/export is offline. AI interpretation uses the active host or configured provider, including normal token limits and billing. The public website does not collect keys or run inference. Source text and answers sent to your model are governed by that provider's policies. Share fabricated examples only.
