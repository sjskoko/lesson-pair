# Installation and everyday use

## Choose your environment

| Environment | Route | Limitation |
| --- | --- | --- |
| Codex with a skill installer | Install `skills/lesson-pair` from this public repository | A host with skill support is required |
| ChatGPT Work with skill creation | Ask the skill creator to install the same folder | Account/workspace availability can differ |
| Another Agent Skills-compatible host | Follow its directory installation instructions | Tool names and Notion access are host-specific |
| A custom GPT without a skill loader | Supply SKILL.md and the references as instructions/knowledge, or use the portable prompt below | This is manual adaptation, not an installed executable skill |
| No AI tools | Run the Python formatter on supplied JSON | No automatic language understanding or Notion writes |

The public skill entry point is [SKILL.md](../skills/lesson-pair/SKILL.md). Fetch it only from a trusted repository version; review changes before installing. No custom server, access-token proxy, or paid API is bundled.

## Portable prompt for an assistant

```text
Organize my language lesson into two linked pages: preparation and review.
Use LessonPair's SKILL.md and read its references only as needed.
Preserve my original writing and teacher feedback verbatim. Label your own
corrections. Do not invent a transcript, missing meaning, score, or completion.
Reuse my existing Notion session if present and verify saved tables and links.
If you cannot write to Notion, give me drafts and clearly say they are unsaved.
```

This prompt does not grant access to private pages. Connect Notion through your assistant's supported authentication flow. Never place credentials in the prompt or repository. If your custom GPT cannot fetch the public files, supply their contents yourself; availability of browsing, knowledge files, and actions depends on that product.

## A lesson from start to finish

1. Give the assistant a video link and an available transcript. It prepares page ①.
2. During the lesson, write and talk in your own words.
3. Paste your original writing and teacher notes with the session number and date.
4. The assistant creates or updates page ② and pairs it with page ① under one session.
5. Complete the hidden-answer exercise and rewrite without looking at the correction.
6. Mark completion yourself. Set your next review date; a date is not automatically a reminder.

## Local JSON format

Use [the synthetic example](../examples/lesson.synthetic.json) as the input shape.

| Field | Requirement |
| --- | --- |
| topic | Required nonempty string |
| session | Optional positive integer |
| lesson_date, organized_date | Optional YYYY-MM-DD; they remain separate |
| video_url | Optional HTTP(S) URL, no embedded credentials |
| learner_original, teacher_trace, teacher_notes | Original strings, not silently corrected |
| segments | Objects with title, original, translation, grammar strings |
| corrections | Objects with original, corrected, reason, source strings |
| grammar | Objects with chunk, rule, example strings |
| chunks, questions | Arrays of strings |
| exercises | Objects with question and answer strings |
| corrected_text | Optional rewritten text; use corrected_text_source to label attribution |

The script validates the shape and renders what you supply. It does not determine whether corrections are accurate. Input JSON is preserved byte-for-byte as `source.json`. Keep this file private for real lessons. The renderer refuses to overwrite existing output files.

## Table checking

```bash
python3 skills/lesson-pair/scripts/lesson_pair.py check path/to/fetched-page.md
```

The checker catches compact one-line table markup, escaped structural table tags, stray closing tags, and inconsistent row widths. It ignores fenced examples. It is a focused regression tool, not a complete Notion parser or visual verifier. Fetch the written Notion page and inspect the stored structure; inspect the UI if visual assurance is needed.
