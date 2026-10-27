import json,collections,statistics as st
d=json.load(open('/home/user/skills/skills/robinhood-autotrader/paper/history/spy_5min.json'))
days=collections.defaultdict(list)
for k in sorted(d): days[k[:10]].append((k,d[k]))
days={k:v for k,v in days.items() if len(v)>=70}
names=sorted(days)
# bar index i: minutes since open = 5*i ; 10:30 -> i=12, 12:00->30, 14:30->60, 15:30->72
def vw(bars,i):
    pv=sum((b[1][1]+b[1][2]+b[1][3])/3*b[1][4] for b in bars[:i+1]);v=sum(b[1][4] for b in bars[:i+1]);return pv/v
STOP=2.0  # SPY pts ~ -35% on ATM 1DTE (prem~3, delta .52)
THETA_PER_BAR=0.013 # ~ $1.28/day spread over ~ 100 trading 5-min bars incl overnight weight; rough
def run(bars,i,side,exit_i=72,target=None):
    e=bars[i][1][3]
    for j in range(i+1,min(exit_i,len(bars)-1)+1):
        o,h,l,c,v=bars[j][1]
        adv = (e-l) if side>0 else (h-e)
        if adv>=STOP: return -STOP, j-i
        if target:
            fav=(h-e) if side>0 else (e-l)
            if fav>=target: return target,j-i
    c=bars[min(exit_i,len(bars)-1)][1][3]
    return side*(c-e), min(exit_i,len(bars)-1)-i
def opt(pts,nb): return 0.52*pts - THETA_PER_BAR*nb - 0.02  # option $ per share
res=collections.defaultdict(list)
for n in names:
    b=days[n]; op=b[0][1][0]
    # C1 trend-up continuation at 12:00 (i=30): above open by >=0.3%, above VWAP, and no 5m close below VWAP since 10:30
    for side,tag in((1,'C1 trend-up 12:00 call'),(-1,'C2 trend-down 12:00 put')):
        i=30; c=b[i][1][3]; v=vw(b,i)
        ok=all(side*(b[j][1][3]-vw(b,j))>0 for j in range(12,i+1)) and side*(c/op-1)>=0.003
        if ok: res[tag].append((n,)+run(b,i,side))
    # C3 VWAP pullback in uptrend: after 11:00 (i>=18) up >=0.3% on day, low touches VWAP and bar closes back above; first one only, before 14:30
    for side,tag in((1,'C3 VWAP-touch bounce call'),(-1,'C4 VWAP-touch reject put')):
        for i in range(18,60):
            v=vw(b,i-1);o,h,l,c,_=b[i][1]
            trend=side*(b[i-1][1][3]/op-1)>=0.003
            touch=(l<=v and c>v) if side>0 else (h>=v and c<v)
            if trend and touch:
                res[tag].append((n,)+run(b,i,side,exit_i=min(i+12,72))); break
    # C5 opening-range (first hour) breakout after 10:30, first break before 14:30
    hi=max(x[1][1] for x in b[:12]); lo=min(x[1][2] for x in b[:12])
    for i in range(12,60):
        c=b[i][1][3]
        if c>hi: res['C5 1h-range break up call'].append((n,)+run(b,i,1)); break
        if c<lo: res['C6 1h-range break down put'].append((n,)+run(b,i,-1)); break
half=names[len(names)//2]
print('days',len(names),names[0],names[-1],'split',half)
for tag in sorted(res):
    r=res[tag]
    def s(rr):
        if not rr: return 'n=0'
        o=[opt(p,nb) for _,p,nb in rr]; w=sum(x>0 for x in o)/len(o)
        return f"n={len(rr):3d} spyAvg={st.mean(p for _,p,_ in rr):+.2f} optAvg=${100*st.mean(o):+6.0f} win={w:.0%}"
    print(f"{tag:28s} ALL {s(r)} | H1 {s([x for x in r if x[0]<half])} | H2 {s([x for x in r if x[0]>=half])}")
