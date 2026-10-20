"""Apply reviewed half-open frame windows to captions without changing their text."""
import math


def apply_layout(cues, layout, width, height, fps, duration):
    def check(ok, message):
        if not ok:
            raise ValueError(message)

    def number(value):
        check(isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value), 'Caption layout values must be finite numbers')
        return value

    fps = number(fps)
    check(fps > 0, 'Caption fps must be positive')
    if 'fps' in layout:
        check(abs(number(layout['fps'])-fps) < 1e-6, 'Caption layout fps differs from source')
    total = round(duration*fps)

    def position(value):
        check(isinstance(value, (list, tuple)) and len(value) == 2, 'Caption position must be [x,y]')
        x, y = [number(n) for n in value]
        check(0 < x < width and 0 < y < height, 'Caption position outside canvas')
        return [x, y]

    def interval(item):
        if 'start_frame' in item or 'end_frame' in item:
            a, b = item.get('start_frame'), item.get('end_frame')
            check(all(isinstance(n, int) and not isinstance(n, bool) for n in [a, b]), 'Caption frame bounds must be integers')
        else:
            a, b = round(number(item['start'])*fps), round(number(item['end'])*fps)
        check(0 <= a < b <= total, 'Caption window outside source')
        return a, b

    default = position(layout['default_position']) if 'default_position' in layout else None
    suppress = sorted(interval(w) for w in layout.get('suppress_windows', []))
    merged = []
    for a, b in suppress:
        if merged and a <= merged[-1][1]:
            merged[-1] = (merged[-1][0], max(b, merged[-1][1]))
        else:
            merged.append((a, b))
    placements = [(interval(w), position(w['position'])) for w in layout.get('position_windows', [])]
    output, review, hidden = [], [], []
    for index, cue in enumerate(cues):
        a, b = round(number(cue['start'])*fps), round(number(cue['end'])*fps)
        check(0 <= a < b <= total, 'Caption below frame resolution or outside source')
        spans = [(a, b)]
        for lo, hi in merged:
            next_spans = []
            for left, right in spans:
                if right <= lo or left >= hi:
                    next_spans.append((left, right))
                else:
                    if left < lo:
                        next_spans.append((left, lo))
                    if right > hi:
                        next_spans.append((hi, right))
            spans = next_spans
        if not spans:
            hidden.append(index)
        for left, right in spans:
            item = dict(cue, start=left/fps, end=right/fps, start_frame=left, end_frame=right, source_cue_index=index)
            if 'position' in cue:
                anchor = position(cue['position'])
            else:
                choices = {tuple(p) for (lo, hi), p in placements if left < hi and right > lo}
                check(len(choices) <= 1, 'Cue intersects conflicting caption positions; split at a semantic boundary')
                anchor = list(next(iter(choices))) if choices else default
            if anchor is not None:
                item['position'] = anchor
            # Preserve a whole visible phrase at one position instead of a few-frame jump.
            if right-left < max(1, round(.4*fps)):
                review.append(dict(source_cue_index=index, start_frame=left, end_frame=right, reason='short visible caption fragment; review readability'))
            output.append(item)
    return output, dict(fps=fps, source_cues=len(cues), visible_cues=len(output), hidden_source_cue_indices=hidden,
                        suppression_frames=[list(w) for w in merged], review_candidates=review)
