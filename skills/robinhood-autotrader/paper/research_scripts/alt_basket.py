"""Small/mid altcoins from the 2021 boom: what happened if you bought them? Coinbase daily closes.
Buy on 2022-01-03 (after the 2021 mania) and on 2023-01-02 (near the bottom); value now. Also BTC/ETH for reference."""
import json, time, urllib.request, datetime as dt, statistics as st
from pathlib import Path
COINS = ["SHIB","AVAX","DOT","ATOM","ALGO","FIL","GRT","MANA","SAND","AXS","ICP","LRC","ENJ","CHZ","ANKR","SKL","AMP","CRV","SUSHI","UNI","AAVE","COMP","SNX","1INCH","BAT","ZRX","XLM","LTC","BCH","ETC","LINK","ADA","XTZ","MATIC","STORJ","OXT","NU","CLV","FORTH","BOND"]
def get(pid, start, end):
    u = f"https://api.exchange.coinbase.com/products/{pid}/candles?granularity=86400&start={start}&end={end}"
    try:
        with urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": "tars-research"}), timeout=20) as r: return json.load(r)
    except Exception: return None
def close_on(pid, day):
    d0 = dt.date.fromisoformat(day); data = get(pid, d0.isoformat(), (d0 + dt.timedelta(days=6)).isoformat())
    time.sleep(0.15)
    if not data: return None
    data.sort(); return data[0][4]
def now(pid):
    data = get(pid, (dt.date.today() - dt.timedelta(days=5)).isoformat(), dt.date.today().isoformat()); time.sleep(0.15)
    if not data: return None
    data.sort(); return data[-1][4]
rows = {}
for c in COINS + ["BTC", "ETH"]:
    pid = f"{c}-USD"; a, b, n = close_on(pid, "2022-01-03"), close_on(pid, "2023-01-02"), now(pid)
    rows[c] = dict(p2022=a, p2023=b, now=n, r2022=round(100 * (n / a - 1), 1) if a and n else None, r2023=round(100 * (n / b - 1), 1) if b and n else None, delisted=n is None)
    print(c, rows[c])
alts = [v for k, v in rows.items() if k not in ("BTC", "ETH")]
r22 = [v["r2022"] for v in alts if v["r2022"] is not None]; r23 = [v["r2023"] for v in alts if v["r2023"] is not None]
summ = dict(n_alts=len(alts), delisted_or_gone=sum(v["delisted"] for v in alts),
            buy2022=dict(n=len(r22), median=round(st.median(r22), 1), down_80_plus=sum(x <= -80 for x in r22), beat_btc=sum(x > rows["BTC"]["r2022"] for x in r22), btc=rows["BTC"]["r2022"], eth=rows["ETH"]["r2022"]),
            buy2023=dict(n=len(r23), median=round(st.median(r23), 1), up_5x_plus=sum(x >= 400 for x in r23), beat_btc=sum(x > rows["BTC"]["r2023"] for x in r23), btc=rows["BTC"]["r2023"], eth=rows["ETH"]["r2023"]))
print(json.dumps(summ, indent=1))
json.dump(dict(rows=rows, summary=summ), open(Path(__file__).with_name("alt_basket.json"), "w"), indent=1)
