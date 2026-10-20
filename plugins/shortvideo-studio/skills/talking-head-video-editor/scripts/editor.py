"""Execute reviewed talking-head edit plans. No automatic editorial decisions."""
import hashlib
import argparse
import json
import math
import re
from fractions import Fraction
from caption_layout import apply_layout
import os
from pathlib import Path
import shutil
import subprocess
import tempfile


def require(ok, message):
    if not ok:
        raise ValueError(message)


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def fresh(path):
    p = Path(path).resolve()
    require(not p.exists(), f'Output exists; choose a new version: {p}')
    require(p.parent.is_dir(), f'Create output directory first: {p.parent}')
    return p


def write_json(path, data):
    with Path(path).open('x', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def run(args):
    return subprocess.run([str(x) for x in args], check=True, capture_output=True, text=True).stdout


class Editor:
    def __init__(self, args):
        self.ff, self.fp, self.encoder = args.ffmpeg, args.ffprobe, args.encoder

    def ffmpeg(self, *args):
        return run([self.ff, '-nostdin', '-n', '-hide_banner', '-loglevel', 'error', *args])

    def probe(self, file):
        return json.loads(run([self.fp, '-v', 'error', '-show_streams', '-show_format', '-of', 'json', file]))

    def video(self, file):
        return next(s for s in self.probe(file)['streams'] if s['codec_type'] == 'video')

    def duration(self, file):
        return float(self.probe(file)['format']['duration'])

    def audio_hash(self, file):
        return self.ffmpeg('-i', file, '-map', '0:a:0', '-c', 'copy', '-f', 'hash', '-hash', 'sha256', '-').strip()

    def codec(self):
        return ['-c:v', self.encoder, '-b:v', '9M'] if self.encoder != 'libx264' else ['-c:v', 'libx264', '-crf', '18', '-preset', 'fast']

    def config(self, plan):
        fps, w, h = plan['fps'], plan['width'], plan['height']
        require(all(isinstance(x, int) and not isinstance(x, bool) and x > 0 for x in (fps, w, h)), 'Positive integer fps/width/height required')
        require(w % 2 == 0 and h % 2 == 0, 'Dimensions must be even')
        return fps, w, h

    def fit(self, fps, w, h):
        return f'fps={fps}:start_time=0,scale={w}:{h}:force_original_aspect_ratio=decrease:force_divisible_by=2,pad={w}:{h}:(ow-iw)/2:(oh-ih)/2,setsar=1,format=yuv420p'

    def concat(self, directory, count, out, base=None):
        manifest = directory / 'concat.txt'
        manifest.write_text(''.join(f"file '{i:04}.mov'\n" for i in range(count)))
        args = ['-f', 'concat', '-safe', '0', '-i', manifest]
        if base:
            args += ['-i', base, '-map', '0:v:0', '-map', '1:a:0', '-c', 'copy']
        else:
            args += ['-map', '0:v:0', '-map', '0:a:0', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '256k']
        self.ffmpeg(*args, '-map_metadata', '-1', '-movflags', '+faststart', out)

    def rough(self, plan, out):
        out = fresh(out)
        side = fresh(out.with_suffix('.timeline.json'))
        fps, w, h = self.config(plan)
        source = str(Path(plan['source']).resolve())
        duration = self.duration(source)
        require(any(s['codec_type'] == 'audio' for s in self.probe(source)['streams']), 'Source has no audio')
        rows, pos, previous = [], 0, 0
        for item in plan['keep']:
            a, b = float(item['in']), float(item['out'])
            require(math.isfinite(a) and math.isfinite(b) and previous <= a < b <= duration, 'Invalid/overlapping keep interval')
            start, end = round(a * fps), round(b * fps)
            require(end > start, 'Interval shorter than one frame')
            rows.append(dict(source_in=start / fps, source_out=end / fps, start_frame=pos, end_frame=pos + end - start, reason=item.get('reason', '')))
            pos += end - start
            previous = b
        require(rows, 'Empty keep plan')
        with tempfile.TemporaryDirectory(prefix='talk-rough-', dir=out.parent) as tmp:
            td = Path(tmp)
            for i, row in enumerate(rows):
                frames = row['end_frame'] - row['start_frame']
                dur = frames / fps
                self.ffmpeg('-ss', row['source_in'], '-i', source, '-t', dur, '-map', '0:v:0', '-map', '0:a:0',
                            '-vf', self.fit(fps, w, h) + ',tpad=stop_mode=clone:stop_duration=0.1',
                            '-af', f'aresample=48000,apad,atrim=duration={dur},asetpts=PTS-STARTPTS,afade=t=in:d=0.004,afade=t=out:st={max(0,dur-.004)}:d=0.004',
                            *self.codec(), '-c:a', 'pcm_s16le', '-map_metadata', '-1', '-metadata:s:v:0', 'rotate=0', '-video_track_timescale', fps * 1000, td / f'{i:04}.mov')
            self.concat(td, len(rows), out)
        write_json(side, dict(source=source, fps=fps, total_frames=pos, cuts=rows))
        return self.verify(out, frames=pos)

    def compose(self, plan, out):
        out = fresh(out)
        side = fresh(out.with_suffix('.timeline.json'))
        fps, w, h = self.config(plan)
        base = str(Path(plan['base']).resolve())
        if plan.get('base_sha256'):
            require(hashlib.sha256(Path(base).read_bytes()).hexdigest() == plan['base_sha256'], 'Wrong locked rough-cut version')
        meta = self.video(base)
        require(meta['r_frame_rate'] == f'{fps}/1' and meta['avg_frame_rate'] == f'{fps}/1', 'Base must be normalized integer CFR')
        require((meta['width'], meta['height']) == (w, h), 'Base dimensions differ')
        require(not any(float(x.get('rotation', 0)) for x in meta.get('side_data_list', [])), 'Normalize base rotation first')
        total = int(meta['nb_frames'])
        rows, pos = [], 0
        for item in plan.get('inserts', []):
            a, b = round(float(item['start']) * fps), round(float(item['end']) * fps)
            require(pos <= a < b <= total, 'Invalid/overlapping insert interval')
            if a > pos:
                rows.append(dict(file=base, kind='video', start_frame=pos, end_frame=a, source_in=pos / fps, source_span=(a-pos)/fps, reason='主播'))
            kind = item['kind']
            require(kind in ('image', 'video'), 'kind must be image or video')
            source = str(Path(item['file']).resolve())
            require(Path(source).is_file(), f'Missing material: {source}')
            si = float(item.get('source_in', 0))
            span = float(item.get('source_span', (b-a)/fps))
            require(math.isfinite(si) and math.isfinite(span) and si >= 0 and span > 0, 'Invalid material source interval')
            if kind == 'video':
                require(si + span <= self.duration(source) + .001, 'Material too short; choose an explicit alternative')
            rows.append(dict(file=source, kind=kind, start_frame=a, end_frame=b, source_in=si, source_span=span, reason=item.get('reason', ''), beat_id=item.get('beat_id'), template_id=item.get('template_id')))
            pos = b
        if pos < total:
            rows.append(dict(file=base, kind='video', start_frame=pos, end_frame=total, source_in=pos/fps, source_span=(total-pos)/fps, reason='主播'))
        with tempfile.TemporaryDirectory(prefix='talk-material-', dir=out.parent) as tmp:
            td = Path(tmp)
            for i, row in enumerate(rows):
                frames = row['end_frame'] - row['start_frame']
                dur = frames / fps
                inp = ['-loop', '1', '-framerate', fps] if row['kind'] == 'image' else ['-ss', row['source_in'], '-t', row['source_span']]
                vf = f'setpts=(PTS-STARTPTS)*{dur/row["source_span"]},' if row['kind'] == 'video' else ''
                self.ffmpeg(*inp, '-i', row['file'], '-map', '0:v:0', '-an', '-vf', vf + self.fit(fps,w,h) + ',tpad=stop_mode=clone:stop_duration=0.1', '-frames:v', frames,
                            *self.codec(), '-map_metadata', '-1', '-metadata:s:v:0', 'rotate=0', '-video_track_timescale', fps*1000, td / f'{i:04}.mov')
                require(int(self.video(td / f'{i:04}.mov')['nb_frames']) == frames, 'Rendered material frame mismatch')
            picture = td / 'picture.mp4'
            self.concat(td, len(rows), picture, base)
            mix_report = self.finish_composite(plan, picture, out, base, fps, w, h, total, td)
        write_json(side, dict(base=base, fps=fps, total_frames=total, cuts=rows, overlays=plan.get('overlays', []), sfx=plan.get('sfx', []), mix=mix_report))
        report = self.verify(out, audio_base=None if plan.get('sfx') else base, frames=total)
        report['mix'] = mix_report
        return report

    def finish_composite(self, plan, picture, out, base, fps, w, h, total, td):
        duration = total / fps
        overlays = plan.get('overlays', [])
        sfx = plan.get('sfx', [])
        require(isinstance(overlays, list) and isinstance(sfx, list), 'overlays and sfx must be arrays')
        def interval(item):
            a, b = float(item['start']), float(item['end'])
            require(math.isfinite(a) and math.isfinite(b) and 0 <= a < b <= duration, 'Invalid overlay/sfx interval')
            return a, b
        def rect(r):
            vals = [r.get(k) for k in ('x', 'y', 'width', 'height')]
            require(all(isinstance(v, (int, float)) and not isinstance(v, bool) and math.isfinite(v) for v in vals), 'Invalid overlay/face rectangle')
            x, y, rw, rh = vals
            require(x >= 0 and y >= 0 and rw > 0 and rh > 0 and x+rw <= w and y+rh <= h, 'Rectangle outside canvas')
            return x, y, rw, rh
        def overlap(a, b):
            x,y,rw,rh=a; xx,yy,ww,hh=b
            return x < xx+ww and x+rw > xx and y < yy+hh and y+rh > yy
        current = picture
        if overlays:
            face_regions = plan.get('face_regions', [])
            require(face_regions, 'Overlays require face_regions measured from actual host footage, including movement margin')
            faces = [rect(face) for face in face_regions]
            args = ['-i', picture]
            filters, label = [], '0:v'
            for i, item in enumerate(overlays):
                a,b = interval(item)
                source = str(Path(item['file']).resolve())
                require(Path(source).is_file(), 'Missing overlay')
                kind = item.get('kind', 'video')
                require(kind in ('image','video'), 'Overlay kind must be image or video')
                si = float(item.get('source_in', 0))
                require(math.isfinite(si) and si >= 0, 'Invalid overlay source_in')
                x,y,ow,oh = rect(item)
                require(all(float(v).is_integer() for v in (x,y,ow,oh)), 'Overlay placement must use integer pixels')
                regions = [rect(r) for r in item.get('content_regions', [item])]
                require(regions, 'Overlay needs a nonempty content region')
                require(all(r[0] >= x and r[1] >= y and r[0]+r[2] <= x+ow and r[1]+r[3] <= y+oh for r in regions), 'Content region outside overlay placement')
                require(not any(overlap(r,face) for r in regions for face in faces), 'Overlay content intersects a face protection region')
                meta = self.video(source)
                alpha = meta.get('pix_fmt','').startswith(('yuva','gbrap','rgba','bgra','argb','abgr')) or str(meta.get('tags',{}).get('alpha_mode',meta.get('tags',{}).get('ALPHA_MODE','0'))) == '1'
                require(alpha, 'Overlay must have an alpha channel; opaque MP4 is a full-screen insert')
                if kind == 'video':
                    require(si+b-a <= self.duration(source)+.001, 'Overlay too short; regenerate instead of silently looping')
                    if meta.get('codec_name') == 'vp9': args += ['-c:v','libvpx-vp9']
                    args += ['-ss',si,'-t',b-a]
                else: args += ['-loop','1','-framerate',fps]
                args += ['-i',source]
                filters.append(f'[{i+1}:v]fps={fps},scale={int(ow)}:{int(oh)},format=rgba,trim=duration={b-a},setpts=PTS-STARTPTS+{a}/TB[ov{i}]')
                filters.append(f'[{label}][ov{i}]overlay=x={int(x)}:y={int(y)}:enable=\'gte(t,{a})*lt(t,{b})\':eof_action=pass:repeatlast=0[v{i}]')
                label=f'v{i}'
            current = td / 'overlaid.mp4'
            self.ffmpeg(*args,'-filter_complex', ';'.join(filters),'-map',f'[{label}]','-map','0:a:0',*self.codec(),'-pix_fmt','yuv420p','-frames:v',total,'-c:a','copy','-movflags','+faststart',current)
        base_hash = self.audio_hash(base)
        require(self.audio_hash(current) == base_hash, 'Narration changed before explicit sound mix')
        report = dict(narration_base=base, narration_audio_hash=base_hash, narration_gain=1, narration_timing_unchanged=True, added_sfx=sfx, actual_listening='not-performed-by-program')
        if sfx:
            args = ['-i',current]
            filters = ['[0:a]aresample=48000,asetpts=PTS-STARTPTS[voice]']
            for i,item in enumerate(sfx):
                a,b = interval(item)
                source = str(Path(item['file']).resolve())
                require(Path(source).is_file(), 'Missing SFX stem')
                si = float(item.get('source_in',0)); gain = float(item.get('gain',1))
                require(math.isfinite(si) and si>=0 and math.isfinite(gain) and 0<gain, 'Invalid SFX source/gain')
                require(si+b-a <= self.duration(source)+.001, 'SFX stem too short')
                args += ['-i',source]
                filters.append(f'[{i+1}:a]atrim=start={si}:duration={b-a},asetpts=PTS-STARTPTS,aresample=48000,volume={gain},adelay={round(a*1000)}:all=1[s{i}]')
            filters.append('[voice]'+''.join(f'[s{i}]' for i in range(len(sfx)))+f'amix=inputs={len(sfx)+1}:duration=first:normalize=0:dropout_transition=0,apad,atrim=duration={duration}[mixed]')
            graph = ';'.join(filters)
            # Measure floating-point linear mix before encoding; never attenuate locked voice via a master limiter.
            peak_cmd = [self.ff, '-nostdin', '-hide_banner', *map(str,args), '-filter_complex', graph+';[mixed]astats=metadata=0:reset=0[measured]',
                        '-map','[measured]','-c:a','pcm_f32le','-f','null','-']
            peak_log = subprocess.run(peak_cmd, check=True, capture_output=True, text=True).stderr
            peaks = [float(n) for n in re.findall(r'Peak level dB: ([+-]?[0-9.]+|-inf)',peak_log)]
            require(peaks and max(peaks) < -.5, 'Mixed audio lacks peak headroom; reduce or stagger SFX instead of limiting narration')
            report.update(linear_mix_peak_db=max(peaks), master_limiter=False, peak_headroom_checked=True)
            self.ffmpeg(*args,'-filter_complex',graph,'-map','0:v:0','-map','[mixed]','-c:v','copy','-c:a','aac','-b:a','256k','-ar','48000','-t',duration,'-movflags','+faststart',out)
            encoded_log = subprocess.run([self.ff,'-nostdin','-hide_banner','-i',str(out),'-map','0:a:0','-af','astats=metadata=0:reset=0','-f','null','-'],check=True,capture_output=True,text=True).stderr
            encoded_peaks = [float(n) for n in re.findall(r'Peak level dB: ([+-]?[0-9.]+|-inf)',encoded_log)]
            require(encoded_peaks and max(encoded_peaks) < 0, 'Encoded audio reaches clipping; revise SFX levels before delivery')
            report['encoded_mix_peak_db'] = max(encoded_peaks)
        else:
            shutil.copy2(current,out)
        return report

    def captions(self, source, cues_path, out, font_path, size, margin_v=None, layout_path=None):
        from fontTools.ttLib import TTFont
        from PIL import ImageFont
        out = fresh(out)
        ass_path, srt_path, log_path = [fresh(out.with_suffix(s)) for s in ('.ass', '.srt', '.render.log')]
        font_path = Path(font_path).resolve()
        font = TTFont(font_path)
        family = font['name'].getDebugName(6) or font['name'].getDebugName(1)
        require(family and ',' not in family and '\n' not in family, 'Unsupported font family')
        cmap = font.getBestCmap()
        measure = ImageFont.truetype(str(font_path), size)
        meta = self.video(source)
        w, h = meta['width'], meta['height']
        if margin_v is None:
            margin_v = round(h*390/1920)  # reviewed chest-lower starting point; override per shot
        require(0 < size < h and 0 <= margin_v < h, 'Invalid subtitle dimensions')
        cues = read(cues_path)
        duration, previous = self.duration(source), 0
        require(cues, 'Empty subtitles')
        for c in cues:
            a, b, text = c['start'], c['end'], c['text']
            require(previous <= a < b <= duration and math.isfinite(a) and math.isfinite(b), 'Invalid/overlapping subtitle times')
            require(text.strip() and not any(ch in text for ch in '{}\\\r'), 'Unsupported subtitle control characters')
            require(len(text.split('\n')) <= 2, 'Split long subtitles into short cues')
            require(not {ch for ch in text if ch != '\n' and ord(ch) not in cmap}, f'Missing font glyph: {text}')
            require(all(measure.getlength(line) <= w-90 for line in text.split('\n')), f'Subtitle too wide; split it: {text}')
            require(round(a*100) < round(b*100), 'Subtitle below ASS timing resolution')
            previous = b
        layout_report = None
        if layout_path:
            fps = float(Fraction(meta['avg_frame_rate']))
            cues, layout_report = apply_layout(cues, read(layout_path), w, h, fps, float(meta['nb_frames'])/fps)
        elif any('position' in c for c in cues):
            cues, layout_report = apply_layout(cues, {}, w, h, float(Fraction(meta['avg_frame_rate'])), duration)
        for c in cues:
            if 'position' in c:
                x, y = c['position']
                widths = [measure.getlength(line) for line in c['text'].split('\n')]
                bounds = [measure.getbbox(line) for line in c['text'].split('\n')]
                text_height = sum(bottom-top for _,top,_,bottom in bounds) + max(0,len(bounds)-1)*size*.3
                require(max(widths)/2+6 <= x <= w-max(widths)/2-6, 'Positioned subtitle extends outside horizontal canvas')
                require(text_height+6 <= y <= h-6, 'Positioned subtitle extends outside vertical canvas')
            require(round(c['start']*100) < round(c['end']*100), 'Visible caption below ASS timing resolution')
        def stamp(t, ass=False):
            div = 100 if ass else 1000
            n = math.floor(t*div+1e-7) if ass and layout_report is not None else round(t*div)
            h0,m,s = n//(3600*div), (n//(60*div))%60, (n//div)%60
            return f'{h0}:{m:02}:{s:02}.{n%div:02}' if ass else f'{h0:02}:{m:02}:{s:02},{n%div:03}'
        header = f'''[Script Info]
ScriptType: v4.00+
PlayResX: {w}
PlayResY: {h}
WrapStyle: 2
ScaledBorderAndShadow: yes
[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,{family},{size},&H00FFFFFF,&H00FFFFFF,&H00111111,&H90000000,0,0,0,0,100,100,0,0,1,2.5,0.8,2,45,45,{margin_v},1
[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
'''
        events = []
        for c in cues:
            text = c['text'].replace('\n', r'\N')
            if 'position' in c:
                x, y = c['position']
                text = f'{{\\an2\\pos({x:g},{y:g})}}'+text
            events.append(f'Dialogue: 0,{stamp(c["start"],True)},{stamp(c["end"],True)},Default,,0,0,0,,{text}')
        ass_path.write_text(header + '\n'.join(events) + '\n', encoding='utf-8')
        srt_path.write_text('\n\n'.join(f'{i+1}\n{stamp(c["start"])} --> {stamp(c["end"])}\n{c["text"]}' for i,c in enumerate(cues))+'\n', encoding='utf-8')
        # Safe local relative filter paths avoid FFmpeg filter escaping of user paths.
        with tempfile.TemporaryDirectory(prefix='talk-captions-') as tmp:
            td = Path(tmp)
            shutil.copy2(ass_path, td/'captions.ass')
            (td/'fonts').mkdir()
            shutil.copy2(font_path, td/'fonts'/('font'+font_path.suffix))
            cmd = [self.ff,'-nostdin','-n','-hide_banner','-i',str(Path(source).resolve()),'-vf',f'ass=captions.ass:fontsdir={td/"fonts"}',*self.codec(),'-map','0:v:0','-map','0:a:0','-c:a','copy','-movflags','+faststart',str(out)]
            with log_path.open('x') as log:
                subprocess.run(cmd, cwd=td, stderr=log, stdout=log, check=True)
        render_log = log_path.read_text(errors='replace')
        require('Glyph ' not in render_log and 'failed to find any fallback' not in render_log, 'Missing rendered glyphs; inspect fontselect/CoreText access before delivery')
        selections = [line for line in render_log.splitlines() if 'fontselect:' in line]
        require(not cues or any('->' in line and family.lower() in line.split('->',1)[1].lower() for line in selections), 'Requested font was not selected; inspect CoreText/font service access')
        report = self.verify(out, audio_base=source, frames=int(meta['nb_frames']))
        report.update(font_family=family, font_file=str(font_path), cues=len(cues), font_selection=selections)
        if layout_report is not None:
            write_json(out.with_suffix('.caption-layout.json'), dict(layout_report, cues=cues))
            report['caption_layout'] = layout_report
        return report

    def verify(self, file, audio_base=None, frames=None):
        meta = self.probe(file)
        video = next(s for s in meta['streams'] if s['codec_type']=='video')
        audio = next(s for s in meta['streams'] if s['codec_type']=='audio')
        if frames is not None:
            require(int(video['nb_frames']) == frames, 'Frame count mismatch')
        require(abs(float(video['duration'])-float(audio['duration'])) <= .1, 'Audio/video duration mismatch')
        self.ffmpeg('-v', 'error', '-xerror', '-i', file, '-map', '0:v:0', '-map', '0:a:0', '-f', 'null', '-')
        equal = self.audio_hash(file) == self.audio_hash(audio_base) if audio_base else None
        require(equal is not False, 'Locked audio changed')
        p = subprocess.run([self.ff,'-nostdin','-hide_banner','-i',str(file),'-vf','blackdetect=d=0.15:pix_th=0.05','-af','silencedetect=n=-45dB:d=0.6','-f','null','-'],capture_output=True,text=True,check=True)
        return dict(file=str(file), full_decode=True, frames=int(video['nb_frames']), audio_identical=equal, video_duration=video['duration'], audio_duration=audio['duration'], review_candidates=[x for x in p.stderr.splitlines() if 'black_start:' in x or 'silence_start:' in x or 'silence_end:' in x])


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--ffmpeg', default=os.environ.get('FFMPEG','ffmpeg'))
    p.add_argument('--ffprobe', default=os.environ.get('FFPROBE','ffprobe'))
    p.add_argument('--encoder', choices=['libx264','h264_videotoolbox'], default='libx264')
    sub = p.add_subparsers(dest='command', required=True)
    s=sub.add_parser('probe'); s.add_argument('file')
    for name in ('rough','compose'):
        s=sub.add_parser(name); s.add_argument('plan'); s.add_argument('output')
    s=sub.add_parser('captions'); s.add_argument('source'); s.add_argument('cues'); s.add_argument('output'); s.add_argument('--font',required=True); s.add_argument('--size',type=int,default=56); s.add_argument('--margin-v',type=int); s.add_argument('--layout',help='JSON default/per-window positions and suppressed frame windows')
    s=sub.add_parser('verify'); s.add_argument('file'); s.add_argument('--audio-base'); s.add_argument('--frames',type=int); s.add_argument('--report')
    a=p.parse_args(); e=Editor(a)
    if a.command=='probe': result=e.probe(a.file)
    elif a.command in ('rough','compose'): result=getattr(e,a.command)(read(a.plan),a.output)
    elif a.command=='captions': result=e.captions(a.source,a.cues,a.output,a.font,a.size,a.margin_v,a.layout)
    else:
        if a.report: fresh(a.report)
        result=e.verify(a.file,a.audio_base,a.frames)
        if a.report: write_json(a.report,result)
    print(json.dumps(result,ensure_ascii=False,indent=2))


if __name__=='__main__':
    main()
