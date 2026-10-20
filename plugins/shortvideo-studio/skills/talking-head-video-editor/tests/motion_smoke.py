"""Synthetic overlay/SFX integration: alpha pixels, protected face, voice lock, timing."""
import argparse
import json
from pathlib import Path
import subprocess
import sys
import tempfile
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from editor import Editor

def main():
    p=argparse.ArgumentParser();p.add_argument('--ffmpeg',default='ffmpeg');p.add_argument('--ffprobe',default='ffprobe')
    args=p.parse_args();args.encoder='libx264';e=Editor(args)
    with tempfile.TemporaryDirectory(prefix='nine-overlay-test-') as tmp:
        td=Path(tmp);base=td/'base.mp4';overlay=td/'shoulder.mov';stem=td/'sound.wav'
        e.ffmpeg('-f','lavfi','-i','color=c=blue:size=320x480:rate=30:duration=3','-f','lavfi','-i','sine=frequency=440:sample_rate=48000:duration=3','-c:v','libx264','-c:a','aac','-shortest',base)
        e.ffmpeg('-f','lavfi','-i','color=c=red@0.7:size=80x100:rate=30:duration=1,format=rgba','-c:v','prores_ks','-profile:v','4444','-pix_fmt','yuva444p10le',overlay)
        e.ffmpeg('-f','lavfi','-i','sine=frequency=900:sample_rate=48000:duration=1','-af','volume=0.1','-c:a','pcm_s16le',stem)
        plan=dict(base=str(base),fps=30,width=320,height=480,inserts=[],face_regions=[dict(x=100,y=30,width=110,height=160)],overlays=[dict(start=.5,end=1.5,file=str(overlay),x=220,y=220,width=80,height=100)])
        final=td/'final.mp4';r=e.compose(plan,final);assert r['audio_identical'] and r['frames']==90
        def pixel(file,t,x,y):
            cmd=[args.ffmpeg,'-v','error','-ss',str(t),'-i',str(file),'-vf',f'crop=2:2:{x}:{y},scale=1:1','-frames:v','1','-pix_fmt','rgb24','-f','rawvideo','-']
            return list(subprocess.run(cmd,check=True,capture_output=True).stdout)
        before=pixel(final,.2,240,240);during=pixel(final,1,240,240);after=pixel(final,2,240,240)
        face=pixel(final,1,140,100)
        assert before[2]>200 and after[2]>200 and during[0]>100 and face[2]>200,(before,during,after,face)
        plan['sfx']=[dict(start=.5,end=1.5,file=str(stem),gain=.3)]
        mixed=td/'mixed.mp4';r=e.compose(plan,mixed)
        assert r['frames']==90 and r['audio_identical'] is None and r['mix']['narration_audio_hash']==e.audio_hash(base)
        assert e.audio_hash(mixed)!=e.audio_hash(base)
        bad=dict(plan);bad['overlays']=[dict(plan['overlays'][0],x=120,y=80)]
        try:e.compose(bad,td/'bad-face.mp4')
        except ValueError as ex:assert 'face' in str(ex)
        else:raise AssertionError('Face overlap accepted')
        bad=dict(plan);bad['base_sha256']='0'*64
        try:e.compose(bad,td/'bad-base.mp4')
        except ValueError as ex:assert 'version' in str(ex)
        else:raise AssertionError('Wrong baseline accepted')
        print(json.dumps(dict(passed=True,tests=['alpha_shoulders_allowed','face_pixels_preserved','overlay_start_end','voice_hash_without_sfx','explicit_sfx_mix','voice_source_retained','reject_face_overlap','reject_wrong_baseline']),ensure_ascii=False))
if __name__=='__main__':main()
