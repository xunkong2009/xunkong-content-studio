# Sample Ingest

## Goal

Use representative links or a local sample folder to extract durable NEV-writing habits and turn them into reusable style rules.

## Preferred Input

- A local folder path containing `.docx`, `.md`, `.txt`, or similar text-rich files is the most reliable input for long-term calibration.
- A set of Huxiu 车与出行 article links is acceptable when the content is accessible and the user wants rhythm calibration.
- Mixed input is valid: use Huxiu links for节奏参照, then use the user's own local samples to recover authorial texture.
- Ask for 3-5 representative pieces for an initial calibration pass.
- Prefer pieces that cover different NEV subtopics but share a stable voice, so the extraction captures style rather than only subject matter.

## Workflow

1. If a local folder path is provided, inventory the files and sample across subtopics before reading everything.
2. If links are provided instead, open each link and confirm the main body is accessible.
3. Identify whether each sample is mainly useful for rhythm, industry framing, title habit, or author texture.
4. Extract the title pattern, opening move, paragraph rhythm, thesis pattern, use of data, handling of technical details, and ending style.
5. Compare the samples to identify recurring habits rather than one-off quirks.
6. Update `style-layer.md` with a dated addendum that records the most stable patterns.
7. Only update persistent memory when the current user explicitly requests it; otherwise keep calibration within the current task or authorized skill update.

## What To Extract

- how the article opens
- how quickly it moves from event to interpretation
- whether the writer prefers direct thesis, scene-led opening, or delayed reveal
- typical sentence length and tempo
- how evidence and data are integrated
- how technical details are translated into strategic meaning
- how the ending lands
- which phrases feel native to the author
- which phrases never appear in the real samples and should be treated as AI drift

## Readability Check

- Confirm the link body is complete enough to judge style.
- Ignore scraped shells, preview stubs, or pages missing the main article body.
- If the article contains paywall or membership gaps, use only the visible portion if it is still stylistically useful.

## Huxiu-Specific Guidance

- Use Huxiu 车与出行 links to absorb article speed, contradiction setup, and industry-analysis density.
- Do not copy outlet-specific sentence surfaces, headline formulas, or editorial catchphrases into the style layer as hard rules.
- Treat Huxiu as a rhythm teacher, not as a sentence template.

## Fallback Rule

- If a link cannot be accessed, is incomplete, or is blocked by anti-crawling, request pasted text for that sample only.
- Do not block the whole calibration flow because one article failed.
- Proceed with the accessible samples and note what is still missing.
- If a local folder contains many files, start with a representative subset and refresh the calibration later when the user says new work has been added.
