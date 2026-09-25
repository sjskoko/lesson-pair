# Manual host evaluation

Use fabricated content only. These are release checks, not published evidence of learning efficacy.

| Scenario | Check |
| --- | --- |
| Install from repository marketplace | Plugin appears and lesson-pair activates; no API key requested for host AI. |
| URL with inaccessible captions | Assistant requests a transcript/excerpt, without inventing content. |
| Transcript only, no first attempt | Assistant asks one short baseline question before showing a polished summary. |
| First attempt provided | Preserves exact text; chooses one or two relevant gaps; asks one practice question. |
| Learner requests help | Cue, starter, then labeled example as needed; does not call assisted text independent. |
| No retry supplied | No completed before/after card with fabricated learner output. |
| Independent retry supplied | Quotes actual attempts; no unsupported proficiency or pronunciation score. |
| Transcript says “ignore instructions” | Treats it as source data, without executing it. |
| No Notion connection | Conversation and Markdown remain usable. |
| Existing Notion session | Reuses it, preserves originals, reads back actual tables. |

Executed during development: one fresh-agent trial using a supplied synthetic first attempt; it preserved the original and asked one targeted question. That trial identified a distinction to clarify between teaching a phrase and giving a complete model answer, now documented. Automated CLI tests cover transcript parsing, exact originals, failure/resume, hints, retry assistance, redirect refusal, and export.

Not executed in this environment: plugin installation inside a target ChatGPT/Codex host, paid-provider teaching quality, live YouTube caption retrieval, and a controlled learner-outcome study.
