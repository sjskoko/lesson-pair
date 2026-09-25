# Contributing

Small, concrete improvements are welcome: another language, clearer study templates, more robust formatting, or a reproducible rendering failure.

1. Open an issue with the problem and expected behavior.
2. Use fictional data only. Do not attach personal lesson records, private Notion URLs, credentials, or student/teacher identities.
3. Keep the installed skill concise; put optional details in references.
4. Preserve original source material and label AI-generated corrections.
5. Run `python3 -m unittest discover -s tests -v` for code changes.

The formatter must remain offline and use Python's standard library only. Do not add analytics, hidden uploads, credential collection, automatic completion, or claims of zero-token AI usage.

By submitting a contribution, you agree that it may be distributed under this project's MIT license. Be respectful and constructive in issues and reviews.

## v0.2 learning workflow and plugin

Edit `skills/lesson-pair`, then run `python scripts/build_plugin.py` and `python scripts/build_docs.py`. CI rejects drift in the generated plugin and bilingual site. Keep the old formatter schema working; new tutor sessions use version 2. Use a local stub for provider tests; never call a paid API in CI.

Prioritize one-question interactions, preservation of the learner's own attempts, and clear source/assistance labels. Use `docs/plugin-evaluation.md` for target-host checks. Keep private transcripts, API keys, sessions, and screenshots out of commits and public issues.
