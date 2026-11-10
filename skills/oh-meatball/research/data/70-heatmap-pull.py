#!/usr/bin/env python3
"""Pull YouTube 'Most replayed' heatmap + likes/comments for the ids in 70-heatmap-ids.txt.
Run from a network that YouTube is not rate-limiting (the cloud session got HTTP 429 on every watch page).
Usage: python3 70-heatmap-pull.py   -> writes 70-heatmap-metrics.csv
Metrics (heatmap is ~100 points of {start_time,end_time,value}, normalised to the video's own peak):
  opening_peak     = max value in the first 10% of the video
  hm_30s_rel/60s   = value at 30 s / 60 s divided by opening_peak
  hm_lasthalf_rel  = mean value of the last half divided by mean of the first 10%
  likes_per_1000, comments_per_1000
PROXY ONLY: counts replays and seeks, normalised per video; not the private retention graph."""
import json, subprocess, time, csv, statistics as st, sys, os
HERE = os.path.dirname(os.path.abspath(__file__))

def metrics(d):
    h = d.get('heatmap'); v = d.get('view_count') or 0
    r = {'video_id': d['id'], 'title': d.get('title'), 'channel': d.get('channel'), 'views': v,
         'likes_per_1000': round(1000 * d['like_count'] / v, 1) if v and d.get('like_count') is not None else '',
         'comments_per_1000': round(1000 * d['comment_count'] / v, 2) if v and d.get('comment_count') is not None else '',
         'heatmap': bool(h)}
    if h:
        end = h[-1]['end_time']
        first = [p['value'] for p in h if p['start_time'] < 0.1 * end] or [h[0]['value']]
        peak = max(first)
        at = lambda t: next((p['value'] for p in h if p['start_time'] <= t < p['end_time']), None)
        r['opening_peak'] = round(peak, 2)
        r['hm_30s_rel'] = round(at(30) / peak, 2) if end > 30 and at(30) is not None else ''
        r['hm_60s_rel'] = round(at(60) / peak, 2) if end > 60 and at(60) is not None else ''
        r['hm_lasthalf_rel'] = round(st.mean(p['value'] for p in h[len(h)//2:]) / st.mean(first), 2)
    return r

if __name__ == '__main__':
    ids = open(os.path.join(HERE, '70-heatmap-ids.txt')).read().split()
    out = []
    for v in ids:
        for attempt in range(4):
            p = subprocess.run(['yt-dlp', '-j', '--skip-download', '--no-playlist', f'https://www.youtube.com/watch?v={v}'], capture_output=True, text=True)
            if p.stdout.strip():
                out.append(metrics(json.loads(p.stdout.splitlines()[0]))); break
            time.sleep(150 * (attempt + 1))   # back off on 429
        time.sleep(5)
    keys = ['video_id', 'title', 'channel', 'views', 'heatmap', 'opening_peak', 'hm_30s_rel', 'hm_60s_rel', 'hm_lasthalf_rel', 'likes_per_1000', 'comments_per_1000']
    with open(os.path.join(HERE, '70-heatmap-metrics.csv'), 'w', newline='') as f:
        w = csv.DictWriter(f, keys, extrasaction='ignore'); w.writeheader(); w.writerows(out)
