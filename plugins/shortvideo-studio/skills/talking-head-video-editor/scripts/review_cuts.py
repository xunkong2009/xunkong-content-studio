"""Extract separate source takes and actual exported joins; never mark listening passed."""
import argparse
import json
import math
import subprocess
from pathlib import Path


def build(timeline, video, directory, ffmpeg='ffmpeg', context=3.0):
    if not math.isfinite(context) or context < .5:
        raise ValueError('Context must be at least 0.5 seconds')
    plan=json.loads(Path(timeline).read_text(encoding='utf-8'))
    source=Path(plan['source']).resolve();video=Path(video).resolve()
    if not source.is_file() or not video.is_file():
        raise ValueError('Source and actual exported video must exist')
    cuts=plan['cuts'];fps=plan['fps']
    if fps <= 0 or not cuts:
        raise ValueError('Invalid rough timeline')
    directory=Path(directory).resolve()
    directory.mkdir(parents=True,exist_ok=False)
    rows=[]
    def extract(file,a,b,name):
        if b<=a: raise ValueError('Empty review interval')
        dest=directory/name
        subprocess.run([str(ffmpeg),'-nostdin','-n','-v','error','-ss',str(a),'-i',str(file),'-t',str(b-a),'-vn','-ac','1','-ar','16000',str(dest)],check=True)
        return dict(file=name,source_file=str(file),start=a,end=b)
    total=plan['total_frames']/fps
    for i,(left,right) in enumerate(zip(cuts,cuts[1:]),1):
        if left['end_frame']!=right['start_frame']:
            raise ValueError('Noncontiguous output timeline')
        join=right['start_frame']/fps
        # Restrict each original excerpt to its selected take so repeated takes remain independent.
        before=extract(source,max(left['source_in'],left['source_out']-context),left['source_out'],f'{i:03}-source-left.wav')
        after=extract(source,right['source_in'],min(right['source_out'],right['source_in']+context),f'{i:03}-source-right.wav')
        actual=extract(video,max(0,join-context),min(total,join+context),f'{i:03}-exported-join.wav')
        rows.append(dict(index=i,output_time=join,left=before,right=after,exported=actual,text='',pause_type='unclassified',reason=right.get('reason',''),repeat_review='pending',listening_status='not_reviewed',issues=[]))
    report=dict(source=str(source),video=str(video),timeline=str(Path(timeline).resolve()),context=context,status='pending_review',cuts=rows,note='Local transcript times are relative to each WAV; add its start to map back. Extend excerpts when short context is ambiguous. Whole-take and within-take review still required.')
    with (directory/'review.json').open('x',encoding='utf-8') as f:
        json.dump(report,f,ensure_ascii=False,indent=2)
    return report


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('timeline');p.add_argument('video');p.add_argument('directory')
    p.add_argument('--ffmpeg',default='ffmpeg');p.add_argument('--context',type=float,default=3)
    a=p.parse_args();report=build(a.timeline,a.video,a.directory,a.ffmpeg,a.context)
    print(json.dumps(dict(cuts=len(report['cuts']),status=report['status']),ensure_ascii=False))


if __name__=='__main__': main()
