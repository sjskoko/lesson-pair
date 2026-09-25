# Legacy English lesson notes workflow

The previous Notion-first workflow is preserved on [legacy/english](https://github.com/sjskoko/lesson-pair/tree/legacy/english).

Pinned snapshot: [00027ce0b0ff655d0add80db9ceaacb754fe3c3e](https://github.com/sjskoko/lesson-pair/tree/00027ce0b0ff655d0add80db9ceaacb754fe3c3e). This includes the original paired video preparation / teacher corrections / review pages and the bilingual documentation site before the guided tutor redesign.

```bash
git clone --branch legacy/english https://github.com/sjskoko/lesson-pair.git lesson-pair-legacy
```

The v0.1.0 release remains available as originally published. The pinned commit above also includes subsequent discovery/documentation improvements.

The current main branch retains `scripts/lesson_pair.py` under the skill, its original JSON input, synthetic fixture, Notion references, and regression tests. [Old formatter usage](legacy-usage.md) is retained for compatibility; its product introduction describes the legacy version.

No existing Notion pages or private lesson records are automatically migrated. The new tutor uses a separate schema (`schema_version: 2`) and writes new private sessions. To revert the installed skill, use the `skills/lesson-pair` directory from the pinned snapshot.
