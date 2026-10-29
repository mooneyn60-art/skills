"""Chronos-Bolt (Amazon, open forecasting model) on the same walk-forward as kronos_test.py, as a second opinion.
Forecasts closes only: median path for direction; the 10-90% spread at the horizon x 1.5 stands in for the range forecast.
Output records match kronos_test.py, so kronos_score.py scores both (prefix 'chronos')."""
import sys, json, time, torch
from pathlib import Path
from chronos import BaseChronosPipeline
torch.set_num_threads(1)
mode = sys.argv[1]; H = Path(__file__).resolve().parent.parent / "history"
P = BaseChronosPipeline.from_pretrained("amazon/chronos-bolt-small", device_map="cpu", torch_dtype=torch.float32)
def fcast(series_list, n):
    q, m = P.predict_quantiles([torch.tensor(s) for s in series_list], prediction_length=n, quantile_levels=[0.1, 0.5, 0.9])
    return q.numpy()
recs = []; t0 = time.time()
if mode == "intraday":
    d = json.load(open(H / "spy_5min.json")); k = sorted(d); rows = [d[x] for x in k]; first = {}
    for n, x in enumerate(k): first.setdefault(x[:10], n)
    jobs = [(day, s + off, lab) for day, s in sorted(first.items()) for off, lab in ((12, "10:30"), (30, "12:00"), (48, "13:30"))
            if s + off >= 400 and s + off + 12 <= len(k) and k[s + off + 11][:10] == day]
    for b in range(0, len(jobs), 64):
        chunk = jobs[b:b + 64]; q = fcast([[r[3] for r in rows[i - 512:i]] for _, i, _ in chunk], 12)
        for (day, i, lab), qq in zip(chunk, q):
            recs.append(dict(day=day, t=lab, c0=rows[i - 1][3], p30=float(qq[5, 1]), p60=float(qq[11, 1]), prng=float(qq[11, 2] - qq[11, 0]) * 1.5,
                             a30=rows[i + 5][3], a60=rows[i + 11][3], arng=max(r[1] for r in rows[i:i + 12]) - min(r[2] for r in rows[i:i + 12]),
                             trng=sum(r[1] - r[2] for r in rows[i - 12:i]) / 12 * 12 ** 0.5))
else:
    D = json.load(open(H / "kronos_daily.json"))
    for sym, last in (("SPY", 250), ("BE", 150), ("NVDA", 150), ("PLTR", 150), ("ORCL", 150), ("SN", 150), ("HALO", 150), ("SOFI", 150)):
        k = sorted(D[sym]); rows = [D[sym][x] for x in k]; idx = list(range(max(400, len(k) - last), len(k)))
        q = fcast([[r[3] for r in rows[max(0, i - 512):i]] for i in idx], 1)
        for i, qq in zip(idx, q):
            recs.append(dict(sym=sym, day=k[i], c0=rows[i - 1][3], p1=float(qq[0, 1]), a1=rows[i][3], prng=float(qq[0, 2] - qq[0, 0]),
                             arng=rows[i][1] - rows[i][2], trng=sum(r[1] - r[2] for r in rows[i - 10:i]) / 10))
json.dump(recs, open(Path(__file__).with_name(f"chronos_{mode}.json"), "w")); print("done", mode, len(recs), round(time.time() - t0))
