# Sample Ingest

## Purpose

Use this guide when the user wants the short-video skill to learn from existing script samples, links, pasted text, or a local folder. Extract durable style rules instead of mimicking one script line by line.

## Default IMA Corpus

When configured, the reference source is: `项目配置中的 IMA 脚本目录`, organized by year and month. Load `ima-corpus.md` and use `ima-skill` to browse the knowledge-base folders and retrieve full script text. Local folders are supplemental only when the user specifies them.

## Inputs To Accept

- Historical scripts in the default IMA corpus

- Local folder paths containing short-video scripts
- Uploaded `.docx`, `.md`, `.txt`, or pasted script text
- Public links that contain full script text or strong style signals

## Workflow

1. Follow `ima-corpus.md` to locate and read the IMA scripts. Sample 3-6 representative scripts across months or topics unless the user requests another scope; monthly files may contain multiple scripts. Record actual titles, locations and reading coverage.
2. Identify the durable patterns that repeat:
   - opening moves
   - sentence length and口语密度
   - concept-naming habits
   - title patterns
   - ending patterns
   - phrases or cadences that feel authentic versus AI-like
3. Separate style from topic:
   - Keep reusable voice and rhythm rules.
   - Discard topic-specific facts or metaphors that only belong to one script.
4. Update your working interpretation of `style-layer.md` before writing.
5. If the user explicitly asks to refresh the skill's baseline style rules, add a dated addendum to `style-layer.md` instead of overwriting prior calibration.

## What To Extract

- How fast the script reaches the real question
- Whether the opening prefers scene, conflict, direct thesis, or rhetorical question
- How examples are introduced and how quickly they turn into explanation
- How theory is simplified into spoken language
- What kind of ending lands best: judgment, frame shift, or prediction

## What Not To Copy

- Exact punchlines from one sample
- Topic-specific claims, facts, or names unless they are needed for the current script
- Surface quirks that do not repeat across the corpus
- Repetitive AI phrasing that appears only in generated drafts rather than authentic samples

## Fallback

- If IMA is unavailable or a sample body cannot be read, report the failure and use the existing `style-layer.md` for ordinary writing. Do not silently fall back to Youdao or the former local folder; read another source only when the user specifies it.
- If samples conflict, trust the patterns that repeat across multiple files instead of chasing the loudest one.
