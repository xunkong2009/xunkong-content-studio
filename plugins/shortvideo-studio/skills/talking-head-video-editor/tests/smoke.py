"""Synthetic integration tests; never reads or changes user videos."""
import argparse
import json
from pathlib import Path
import sys
import tempfile
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from editor import Editor
from review_cuts import build


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--ffmpeg',required=True); p.add_argument('--ffprobe',required=True); p.add_argument('--font',required=True)
    a=p.parse_args(); a.encoder='libx264'; e=Editor(a)
    with tempfile.TemporaryDirectory(prefix='talk-skill-test-') as tmp:
        td=Path(tmp)
        raw=td/'测试原片.mp4'
        e.ffmpeg('-f','lavfi','-i','testsrc2=size=320x480:rate=30:duration=3','-f','lavfi','-i','sine=frequency=440:sample_rate=48000:duration=3','-c:v','libx264','-c:a','aac','-shortest',raw)
        plan=dict(source=str(raw),fps=30,width=320,height=480,keep=[dict(**{'in':.2,'out':1.2},reason='first'),dict(**{'in':1.7,'out':2.7},reason='second')])
        rough=td/'rough.mp4'; r=e.rough(plan,rough)
        assert r['frames']==60
        review=build(rough.with_suffix('.timeline.json'),rough,td/'review',a.ffmpeg,1)
        assert review['status']=='pending_review' and len(review['cuts'])==1
        cut=review['cuts'][0]
        assert cut['output_time']==1 and cut['listening_status']=='not_reviewed'
        assert abs(cut['left']['start']-.2)<.001 and abs(cut['right']['start']-1.7)<.001
        assert abs(e.duration(td/'review'/cut['exported']['file'])-2)<.01
        try: build(rough.with_suffix('.timeline.json'),rough,td/'review',a.ffmpeg,1)
        except FileExistsError: pass
        else: raise AssertionError('Review overwrite accepted')
        try: e.rough(plan,rough)
        except ValueError: pass
        else: raise AssertionError('Overwrite accepted')
        still=td/'素材.png'
        e.ffmpeg('-f','lavfi','-i','color=c=red:size=160x240','-frames:v','1',still)
        material=dict(base=str(rough),fps=30,width=320,height=480,inserts=[dict(start=.2,end=.7,file=str(still),kind='image'),dict(start=1,end=1.5,file=str(raw),kind='video',source_in=.2,source_span=.8)])
        final=td/'final.mp4'; r=e.compose(material,final)
        assert r['frames']==60 and r['audio_identical']
        cues=td/'cues.json'; cues.write_text(json.dumps([dict(start=.1,end=.9,text='第一句'),dict(start=1,end=1.9,text='第二句')]))
        r=e.captions(final,cues,td/'sub.mp4',a.font,24,20)
        assert r['audio_identical'] and r['font_selection']
        material['inserts'][1]['start']=.5
        try: e.compose(material,td/'bad.mp4')
        except ValueError: pass
        else: raise AssertionError('Overlapping insert accepted')
        print(json.dumps(dict(passed=True,tests=['rough_frames','review_source_mapping','actual_exported_join','review_pending_not_passed','review_no_overwrite','no_overwrite','image_and_retimed_video','locked_audio','font_subtitles','reject_overlap']),ensure_ascii=False))


if __name__=='__main__': main()
