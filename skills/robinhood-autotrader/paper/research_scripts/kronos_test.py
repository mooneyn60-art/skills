"""Kronos (open-source K-line foundation model, Tsinghua, AAAI 2026; Kronos-small 24.7M, HF NeoQuasar) walk-forward test.
Nolan, 10/21: "run Kronos and do what you need to do". Requires PyTorch + the cloned repo (path arg 1).
mode intraday: SPY 5-min (spy_5min.json, 167 sessions). Origins at 10:30, 12:00, 13:30 ET (bar 12/30/48 of the day);
  context = previous 400 bars; forecast 12 bars (60 min). Score +30m and +60m direction, and the 60-min range.
mode daily: SPY last 250 sessions + holdings (BE NVDA PLTR ORCL SN HALO SOFI) last 150 each; context 400 days; forecast 1 day.
Each forecast = mean of 5 samples (T=1, top_p=0.9). Only past bars go in. Results -> kronos_<mode>.json."""
import sys, json, time, pandas as pd, torch
from pathlib import Path
torch.set_num_threads(2)
sys.path.insert(0, sys.argv[1]); mode = sys.argv[2]
from model import Kronos, KronosTokenizer, KronosPredictor
P = KronosPredictor(Kronos.from_pretrained("NeoQuasar/Kronos-small"), KronosTokenizer.from_pretrained("NeoQuasar/Kronos-Tokenizer-base"), device="cpu", max_context=512)
H = Path(__file__).resolve().parent.parent / "history"
def fc(rows, keys, i, n, future_ts):
    df = pd.DataFrame(rows[i - 400:i], columns=["open", "high", "low", "close", "volume"])
    return P.predict(df=df, x_timestamp=pd.to_datetime(pd.Series(keys[i - 400:i])), y_timestamp=pd.to_datetime(pd.Series(future_ts)),
                     pred_len=n, T=1.0, top_p=0.9, sample_count=5, verbose=False)
recs = []; t0 = time.time()
if mode == "intraday":
    d = json.load(open(H / "spy_5min.json")); k = sorted(d); rows = [d[x] for x in k]
    first = {}
    for n, x in enumerate(k): first.setdefault(x[:10], n)
    for day, s in sorted(first.items()):
        for off, lab in ((12, "10:30"), (30, "12:00"), (48, "13:30")):
            i = s + off
            if i < 400 or i + 12 > len(k) or k[i + 11][:10] != day: continue
            p = fc(rows, k, i, 12, k[i:i + 12]); c0 = rows[i - 1][3]
            recs.append(dict(day=day, t=lab, c0=c0, p30=float(p["close"].iloc[5]), p60=float(p["close"].iloc[11]),
                             prng=float(p["high"].max() - p["low"].min()), a30=rows[i + 5][3], a60=rows[i + 11][3],
                             arng=max(r[1] for r in rows[i:i + 12]) - min(r[2] for r in rows[i:i + 12]),
                             trng=sum(r[1] - r[2] for r in rows[i - 12:i]) / 12 * 12 ** 0.5))
            if len(recs) % 50 == 0: print(len(recs), round(time.time() - t0), flush=True)
else:
    D = json.load(open(H / "kronos_daily.json"))
    for sym, last in (("SPY", 250), ("BE", 150), ("NVDA", 150), ("PLTR", 150), ("ORCL", 150), ("SN", 150), ("HALO", 150), ("SOFI", 150)):
        k = sorted(D[sym]); rows = [D[sym][x] for x in k]
        for i in range(max(400, len(k) - last), len(k)):
            p = fc(rows, k, i, 1, [k[i]]); c0 = rows[i - 1][3]
            recs.append(dict(sym=sym, day=k[i], c0=c0, p1=float(p["close"].iloc[0]), a1=rows[i][3],
                             prng=float(p["high"].iloc[0] - p["low"].iloc[0]), arng=rows[i][1] - rows[i][2],
                             trng=sum(r[1] - r[2] for r in rows[i - 10:i]) / 10))
            if len(recs) % 100 == 0: print(len(recs), round(time.time() - t0), flush=True)
json.dump(recs, open(Path(__file__).with_name(f"kronos_{mode}.json"), "w"))
print("done", len(recs), round(time.time() - t0))
