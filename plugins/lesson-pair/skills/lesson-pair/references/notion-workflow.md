# Notion workflow

## Locate and reuse

Use a supplied hub/session URL first. Otherwise discover the connected workspace's tool access and use its available content-search tool with one literal title. Prefer an existing language-learning hub; do not search unrelated personal pages. Discover live tool schemas rather than assuming old tool names.

Fetch the hub, session, and relevant child pages before edits. Obtain data-source IDs and exact property names by fetching the database. If the current connection exposes no writes, prepare drafts and report that nothing was saved. Do not invent API capabilities or ask for credentials in chat.

## Session structure

One database row is one lesson. Place two pages under that row:

- `① 영상 예습 자료 · Session NN · Topic`
- `② 수업·복습 기록 · Session NN · Topic`

Use the same session ID on updates. Add reciprocal native page mentions and a link back to the session. Existing preparation pages should be moved, not duplicated, when pairing is requested. Preserve child pages, original transcripts, comments, attachments, and user edits.

Suggested properties, adapted to an existing schema:

| Property | Type | Purpose |
| --- | --- | --- |
| 수업 | Title | Session NN · topic |
| 회차 | Number | Explicit session number |
| 수업일 | Date | Lesson date, not processing date |
| 구분 | Select | 수업 / 양식 |
| 진행 | Select | 예습 전 / 예습 중 / 수업 완료 / 복습 중 / 복습 완료 |
| 영상 | URL | Source video |
| 예습 자료 | URL | First child |
| 수업 기록 | URL | Second child |
| 핵심 문법 | Multi-select | A few useful tags |
| 다음 복습일 | Date | User-selected; not an automatic reminder |
| 재작문 완료 | Checkbox | False until the learner confirms |

Views: all lessons sorted by lesson date; review pending filtered to lesson rows with 수업 완료/복습 중; calendar by lesson date; templates filtered to 양식. Exclude templates from lesson counts. A duplicate-ready row with children is a reusable template, but not a native database template; state the distinction. When duplicated, update page links to the new children.

## Native formatting and the known table failure

Read the connected Notion tool's current enhanced-Markdown specification before writing. A compact `<table><tr>…` string may be stored as literal text even when the write succeeds. Put the table, row, and each cell on separate lines:

```xml
<table header-row="true">
<tr>
<td>Original</td>
<td>Correction</td>
</tr>
<tr>
<td>She enjoy reading.</td>
<td>She enjoys reading.</td>
</tr>
</table>
```

Do not escape the structural tags themselves. Escape literal special characters in cell text. Use only rich text inside cells; do not put lists, headings, or paragraphs in them. Use tabs to indent toggle/callout children.

Use `<mention-page url="EXISTING_URL"/>` for references. Use a `<page>` tag only to retain/create the intended child relationship: using it with an existing URL may move that page. Removing child tags in a full replacement may delete children. Prefer targeted edits over replacement.

For a repair, fetch and isolate the broken table block, including any stray closing tag emitted by serialization. Replace only that block with multiline markup. Refetch and verify the table has rows/cells and no escaped literal tags. If a tool rejects an operation, do not bypass its guard; use a supported safer edit.

## Completion checks

1. Compare the saved originals against the inputs.
2. Check both child IDs and links in the session and each child.
3. Check the saved headings, toggles, table rows/cells, and incomplete checkboxes.
4. Check filters and dates, including the template exclusion.
5. Preserve any concurrent changes. Re-fetch if a search-and-replace no longer matches.
6. Report the actual result. Do not report visual verification unless you inspected the rendered UI.
