# Sample Ingest

## Goal

Use the primary writing corpus to extract the author's durable writing habits and turn them into reusable style rules.

## Preferred Input

- When configured, the preferred long-term corpus is IMA: `项目配置中的 IMA 文章目录` (primary voice) and `项目配置中的 IMA 约稿目录` (secondary structure; formerly called `约稿目录`). Load `ima-corpus.md` for verified folder IDs and the knowledge-base-to-notes reading flow.
- Local folders, uploaded files, or links are now supplemental inputs only when the user explicitly asks to calibrate from them.
- Public article links are acceptable when the content is accessible.
- When the user has provided an accessible corpus and requested a scan, start sampling directly. Ask for representative pieces only if access or authorship is unclear and would materially change the calibration.
- Prefer pieces with different topics but similar voice, so the extraction captures style rather than just subject matter.

## Workflow

1. When the user asks to refresh or consult the long-term corpus, use `ima-skill` and follow `ima-corpus.md` to browse and read the IMA folders `博客灵感（完成）` and `约稿`.
2. Respect the user's named folder first. Resolve actual folder names from the live directory (约稿目录 may be named 约稿); do not assume a missing literal name means the corpus is unavailable. For a requested overall scan, page through the title index and sample across subjects, older/newer pieces and reference-rich/reference-light styles. Record coverage and exclusions; do not equate title browsing with reading every article.
3. If the IMA corpus is temporarily unavailable, stop the corpus-refresh step and report the blockage. Ordinary writing may continue from the existing bundled style layer.
4. If the user explicitly asks to calibrate from links or uploaded files instead, open each link and confirm the main body is accessible.
5. Extract the article's title, opening move, paragraph rhythm, thesis pattern, use of examples, and ending style. Also record which work or everyday action is used, where it enters, what it explains, how the prose returns to the main argument, and whether a scene is personal, reported or hypothetical. Keep source note IDs and short passage locators.
6. Compare the samples to identify recurring habits rather than one-off quirks.
7. When calibration or skill optimization is requested, update the relevant style references with stable patterns and dated evidence. Prefer one maintained operational reference over repeated long addenda. Do not turn individual examples into mandatory templates or quote quotas; retain current explicit user preferences when older samples conflict.
8. A skill update does not authorize unrelated memory changes. Only write long-term memory when the user explicitly requests it, following the environment's memory-write rules; otherwise keep the calibration inside this plugin.

## What To Extract

- how the article opens
- how quickly it moves from event to interpretation
- whether the writer prefers direct thesis, scene-led opening, or delayed reveal
- typical sentence length and tempo
- how evidence is integrated
- how the ending lands
- which phrases feel native to the author
- which phrases never appear in the real samples and should be treated as AI drift

## Readability Check

- Prefer notes that are clearly finished drafts, delivered稿件, or high-signal long-form idea notes from the two IMA folders.
- Confirm the body is complete enough to judge style. A successful CLI exit code can still contain 获取笔记内容失败; reject error messages, empty bodies and title-only returns as unusable, and record them separately.
- Ignore scraped shells, preview stubs, or pages missing the main article body.
- If the article contains paywall or membership gaps, use only the visible portion if it is still stylistically useful.

## Fallback Rule

- If the IMA corpus cannot be accessed because of service, auth, or network issues, note the failure clearly and stop only the corpus-refresh step. Do not block unrelated writing stages.
- If a link cannot be accessed, is incomplete, or is blocked by anti-crawling, request pasted text for that sample only.
- Do not block the whole calibration flow because one article failed.
- Proceed with the accessible samples and note what is still missing.
- If the user explicitly provides a local folder for a separate one-off calibration task, start with a representative subset and refresh later when the user says new work has been added.
