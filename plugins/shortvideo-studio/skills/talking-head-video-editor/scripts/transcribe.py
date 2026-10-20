"""Transcribe with an existing local faster-whisper model; no automatic download."""
import argparse
import json
from pathlib import Path


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('input'); p.add_argument('output')
    p.add_argument('--model', required=True, help='Existing local faster-whisper model directory')
    p.add_argument('--prompt', default=''); p.add_argument('--language', default='zh')
    p.add_argument('--no-vad', action='store_true', help='Keep all audio for independent short-region review')
    a=p.parse_args()
    if not Path(a.input).is_file(): p.error('Input media does not exist')
    if not Path(a.output).parent.is_dir(): p.error('Create output directory first')
    if not Path(a.model).is_dir(): p.error('Local model directory required; obtain a model with user authorization first')
    if Path(a.output).exists(): p.error('Output exists; choose a new version')
    from faster_whisper import WhisperModel
    model=WhisperModel(a.model, device='cpu', compute_type='int8', cpu_threads=6, local_files_only=True)
    segments,_=model.transcribe(a.input, language=a.language, beam_size=5, word_timestamps=True, vad_filter=not a.no_vad, initial_prompt=a.prompt or None, condition_on_previous_text=False)
    rows=[]
    for s in segments:
        rows.append(dict(start=s.start,end=s.end,text=s.text,words=[dict(start=w.start,end=w.end,word=w.word,probability=w.probability) for w in (s.words or [])]))
        print(f'{s.start:.2f}–{s.end:.2f} {s.text}',flush=True)
    with Path(a.output).open('x',encoding='utf-8') as f: json.dump(rows,f,ensure_ascii=False,indent=2)


if __name__=='__main__': main()
