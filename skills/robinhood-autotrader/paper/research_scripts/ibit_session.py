"""Options-style crypto via IBIT (the Bitcoin ETF): does BTC's move while US markets are closed (20:00 -> 13:30 UTC)
predict BTC during the US session (13:30 -> 20:00 UTC)? That is the 'gap' an IBIT option sees at the open.
3 years of Coinbase hourly BTC, split in halves. Weekdays only (US session days)."""
import json, statistics as st, datetime as dt, math
from pathlib import Path
hb = json.load(open(Path(__file__).resolve().parent.parent / "history" / "crypto" / "btc_hourly.json"))
def px(day, hh):  # open of the hour bar
    v = hb.get(f"{day}T{hh:02d}:00Z"); return v[0] if v else None
days = sorted({k[:10] for k in hb}); rows = []
for i in range(1, len(days)):
    d, p = days[i], days[i - 1]
    if dt.date.fromisoformat(d).weekday() > 4: continue
    a, b, c = px(p, 20), px(d, 13), px(d, 20)
    if a and b and c: rows.append((d, 100 * (b / a - 1), 100 * (c / b - 1)))
mid = rows[len(rows) // 2][0]
def tstat(x): return st.mean(x) / (st.pstdev(x) / math.sqrt(len(x))) if len(x) > 2 and st.pstdev(x) else float("nan")
out = {}
for lab, sel in (("first half", lambda r: r[0] < mid), ("second half", lambda r: r[0] >= mid)):
    R = [r for r in rows if sel(r)]
    for name, f in (("closed-hours up > 2%", lambda g: g > 2), ("closed-hours up 0.5-2%", lambda g: 0.5 < g <= 2), ("flat (-0.5..0.5)", lambda g: -0.5 <= g <= 0.5),
                    ("closed-hours down 0.5-2%", lambda g: -2 <= g < -0.5), ("closed-hours down > 2%", lambda g: g < -2)):
        s = [r[2] for r in R if f(r[1])]
        if len(s) >= 8:
            out[f"{lab} {name}"] = dict(n=len(s), us_session=round(st.mean(s), 2), up=round(100 * sum(x > 0 for x in s) / len(s)), t=round(tstat(s), 2))
            print(f"{lab:11s} {name:26s} n {len(s):3d}  US-session BTC {st.mean(s):+.2f}%  up {100*sum(x>0 for x in s)/len(s):3.0f}%  t {tstat(s):+.2f}")
json.dump(out, open(Path(__file__).with_name("ibit_session.json"), "w"), indent=1)
