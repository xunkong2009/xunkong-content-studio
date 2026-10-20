"""Caption/SFX regression with synthetic media only; not actual project listening."""
import argparse
import json
from pathlib import Path
import subprocess
import sys
import tempfile
sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'scripts'))
from caption_layout import apply_layout
from editor import Editor


def pure():
    cues=[dict(start=0,end=3,text='first'),dict(start=3,end=6,text='second')]
    layout=dict(fps=30,default_position=[160,360],suppress_windows=[dict(start_frame=20,end_frame=40),dict(start_frame=90,end_frame=120)],position_windows=[dict(start_frame=120,end_frame=180,position=[160,420])])
    out, report=apply_layout(cues,layout,320,480,30,6)
    assert [(c['start_frame'],c['end_frame'],c['text'],c['position']) for c in out]==[(0,20,'first',[160,360]),(40,90,'first',[160,360]),(120,180,'second',[160,420])]
    whole,_=apply_layout([dict(start=0,end=1,text='whole')],dict(default_position=[160,360],position_windows=[dict(start_frame=0,end_frame=29,position=[160,420])]),320,480,30,6)
    assert len(whole)==1 and whole[0]['end_frame']==30 and whole[0]['position']==[160,420]
    hidden,r=apply_layout(cues,dict(suppress_windows=[dict(start=0,end=6)]),320,480,30,6)
    assert hidden==[] and r['hidden_source_cue_indices']==[0,1]
    _,r=apply_layout(cues,dict(suppress_windows=[dict(start_frame=1,end_frame=90)]),320,480,30,6)
    assert r['review_candidates'][0]['end_frame']==1
    for bad in [dict(fps=25),dict(default_position=[-1,100]),dict(suppress_windows=[dict(start_frame=-1,end_frame=20)]),dict(position_windows=[dict(start=0,end=1,position=[160,360]),dict(start=1,end=2,position=[160,420])])]:
        try:apply_layout(cues,bad,320,480,30,6)
        except ValueError:pass
        else:raise AssertionError('Invalid/ambiguous caption layout accepted')
    return layout


def main():
    p=argparse.ArgumentParser();p.add_argument('--ffmpeg',required=True);p.add_argument('--ffprobe',required=True);p.add_argument('--font',required=True);a=p.parse_args();a.encoder='libx264';e=Editor(a)
    layout=pure()
    from PIL import Image,ImageChops
    with tempfile.TemporaryDirectory(prefix='caption-layout-test-') as tmp:
        td=Path(tmp);base=td/'base.mp4'
        e.ffmpeg('-f','lavfi','-i','color=c=gray:size=320x480:rate=30:duration=6','-f','lavfi','-i','sine=frequency=440:sample_rate=48000:duration=6','-c:v','libx264','-c:a','aac','-shortest',base)
        cp=td/'cues.json';cp.write_text(json.dumps([dict(start=0,end=3,text='普通字幕'),dict(start=3,end=6,text='补充字幕')]))
        lp=td/'layout.json';lp.write_text(json.dumps(layout));out=td/'sub.mp4';r=e.captions(base,cp,out,a.font,24,None,lp)
        assert r['audio_identical'] and r['cues']==3 and r['caption_layout']['visible_cues']==3
        ass=out.with_suffix('.ass').read_text();assert r'\pos(160,360)' in ass and r'\pos(160,420)' in ass
        def frame(f):
            path=td/f'frame-{f}.png';e.ffmpeg('-i',out,'-vf',f'select=eq(n\\,{f})','-frames:v','1',path);return Image.open(path).convert('RGB')
        empty=frame(20)
        for f in [19,40,89]:
            im=frame(f);diff=ImageChops.difference(im,empty);assert diff.crop((60,300,260,370)).getbbox(),f
        assert ImageChops.difference(frame(39),empty).getextrema()==((0,0),(0,0),(0,0))
        # 90 is the exact first frame of the second suppressed window.
        assert ImageChops.difference(frame(90),empty).getextrema()==((0,0),(0,0),(0,0))
        diff=ImageChops.difference(frame(120),empty);assert diff.crop((60,380,260,430)).getbbox();assert not diff.crop((60,300,260,370)).getbbox()
        stem=td/'sfx.wav';e.ffmpeg('-f','lavfi','-i','sine=frequency=900:sample_rate=48000:duration=1','-af','volume=0.1','-c:a','pcm_s16le',stem)
        plan=dict(base=str(base),fps=30,width=320,height=480,inserts=[],sfx=[dict(start=1,end=2,file=str(stem),gain=3)])
        mixed=td/'mixed.mp4';r=e.compose(plan,mixed);assert r['mix']['narration_gain']==1 and not r['mix']['master_limiter'] and r['mix']['encoded_mix_peak_db']<0
        plan['sfx'][0]['gain']=100
        try:e.compose(plan,td/'too-loud.mp4')
        except ValueError as ex:assert 'headroom' in str(ex)
        else:raise AssertionError('Clipping mix accepted')
        assert not (td/'too-loud.mp4').exists()
    print(json.dumps(dict(passed=True,tests=['half_open_frame_subtraction','no_midcue_position_flash','empty_visible_caption_set','short_fragment_review','invalid_layout_rejected','actual_caption_start_end_frames','actual_caption_positions','audio_stream_unchanged_by_captions','independent_sfx_gain_above_one','no_master_limiter','clipping_rejected']),ensure_ascii=False))

if __name__=='__main__':main()
