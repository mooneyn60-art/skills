#!/usr/bin/env python3
"""Sanity instrumentation for variant (a) pullback. Replays harness run() logic with counters. Data only."""
import mom_screen_base as m
from mom_screen_base import O,H,L,C,SECTORS,sma,vol63,mom_12_1,pullback_ok,first_valid

def trace(dates,bars,spyb,start,slots=8,cost=0.0005):
    syms=sorted(bars); i0=max(next(i for i,d in enumerate(dates) if d>=start),253); i1=len(dates)-1
    cash,pos,pending,watch=1.0,{},[],[]; month=None; eq=[]
    entries=[]; rebuy_same_month=0; rebuy_after_trend_below200=0; picks=[]; wait=[]; stale_inelig=0
    mstart={}  # month -> picks dict sym->(rank day idx, bought day or None)
    stopmonth={}; trendexit={}
    for i in range(i0,i1+1):
        d=dates[i]
        for s in pending:
            if s in pos or bars[s][i] is None or len(pos)>=slots: continue
            equity=cash+sum(p["q"]*bars[x][i][O] for x,p in pos.items())
            px=bars[s][i][O]*(1+cost); amt=min(equity*.85/slots,cash-equity*.15)
            if amt<=0: continue
            q=amt/px; cash-=q*px
            pos[s]=dict(q=q,e=px,hi=bars[s][i][O],stop=.92*px,d0=i,exit_next=False)
            entries.append((d,s))
            pk=mstart.get(month,{})
            if s in pk:
                if pk[s][1] is None: pk[s][1]=i; wait.append(i-pk[s][0])
                else:
                    rebuy_same_month+=1
            s200=sma(bars[s],i-1,200)
            if s200 is not None and bars[s][i-1][C]<s200: rebuy_after_trend_below200+=1
        pending=[]
        for s in list(pos):
            p,b=pos[s],bars[s][i]
            if p["exit_next"]: fill=b[O]*(1-cost); why="trend"
            elif b[L]<=p["stop"]: fill=min(b[O],p["stop"])*(1-cost); why="stop"
            else: continue
            cash+=p["q"]*fill; del pos[s]
        for s,p in pos.items():
            b=bars[s][i]; p["hi"]=max(p["hi"],b[C])
            p["stop"]=max(p["stop"],.8*p["hi"],p["e"] if b[C]>=1.08*p["e"] else 0)
            s200=sma(bars[s],i,200); p["exit_next"]=s200 is not None and b[C]<s200
        eq.append(cash+sum(p["q"]*bars[s][i][C] for s,p in pos.items()))
        new=d[:7]!=month; month=d[:7]
        if new:
            cands=[]
            for s in syms:
                seq=bars[s]
                if seq[i] is None or i-first_valid(seq)<252: continue
                sc=mom_12_1(seq,i); s200,v=sma(seq,i,200),vol63(seq,i)
                if sc is None or sc<=0 or s200 is None or v is None: continue
                if seq[i][C]<=s200 or v>.8: continue
                cands.append((s,sc))
            cands.sort(key=lambda x:-x[1]); watch=cands
            mstart[month]={s:[i,None] for s,_ in cands}
        free=slots-len(pos)-len(pending); sec={}
        for s in pos: sec[SECTORS[s]]=sec.get(SECTORS[s],0)+1
        for s,_ in watch:
            if free<=0: break
            if s in pos or s in pending or sec.get(SECTORS[s],0)>=2: continue
            if not pullback_ok(bars[s],i): continue
            # staleness: watch name no longer passes base eligibility today
            sq=bars[s]; s200=sma(sq,i,200)
            if s200 is not None and sq[i][C]<=s200: stale_inelig+=1
            pending.append(s); sec[SECTORS[s]]=sec.get(SECTORS[s],0)+1; free-=1
    return eq,entries,mstart,wait,rebuy_same_month,rebuy_after_trend_below200,stale_inelig

dates,bars,spyb=m.load("WIDE")
eq,entries,mstart,wait,rb,rb200,stale=trace(dates,bars,spyb,"2021-12-01")
ref=m.run(dates,bars,spyb,start="2021-12-01",entry_mode="pullback")
print("WIDE pullback sanity (instrumented replay vs harness run)")
print(f"  replay final equity {eq[-1]:.6f}  harness final equity {ref['eq'][-1]:.6f}  harness trades {len(ref['trades'])}")
print(f"  entries total: {len(entries)}")
npicks=sum(len(v) for v in mstart.values())
never=sum(1 for v in mstart.values() for r in v.values() if r[1] is None)
first=sum(1 for v in mstart.values() for r in v.values() if r[1] is not None)
print(f"  months with a ranking: {len(mstart)}  monthly picks (eligible names listed): {npicks}")
print(f"  picks bought at least once in their month: {first}")
print(f"  picks never bought in their month: {never}")
print(f"  avg trading days from month-start rank to first entry fill (bought picks): {sum(wait)/len(wait):.2f}  median {sorted(wait)[len(wait)//2]}  max {max(wait)}")
print(f"  re-buys of a name already bought earlier the SAME month (after exit): {rb}")
print(f"  entries where prior-day close was below the 200d SMA (stale watch, not rechecked): {rb200}")
print(f"  signals where signal-day close <= 200d SMA: {stale}")
# entries bought outside the month's picks? and entries per month
from collections import Counter
c=Counter(d[:7] for d,_ in entries); print("  entries by month:", dict(sorted(c.items())))
print("  re-buy list (date,sym) = entries beyond first in month:")
seen=set()
for d,s in entries:
    k=(d[:7],s)
    if k in seen: print("   ",d,s)
    seen.add(k)
