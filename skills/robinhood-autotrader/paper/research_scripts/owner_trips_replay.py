import json,sys,math
from statistics import mean,median
S=sys.argv[1]
trips=json.load(open(S+'/trips.json'))
sb=json.load(open(S+'/spy_min.json'))['data']['results'][0]['bars']
print('SPY bars interpolated:',sum(bool(x.get('interpolated')) for x in sb),'of',len(sb))
spy={x['begins_at'][:16]:(float(x['open_price']),float(x['high_price']),float(x['low_price']),float(x['close_price'])) for x in sb}
keys=sorted(spy)
def N(x): return 0.5*(1+math.erf(x/math.sqrt(2)))
def bs(c,s,k,t,v):
    if t<=1e-9: return max(0,s-k) if c else max(0,k-s)
    sd=v*math.sqrt(t); d1=(math.log(s/k)+.5*sd*sd)/sd; d2=d1-sd
    return s*N(d1)-k*N(d2) if c else k*N(-d2)-s*N(-d1)
YM=252*390
def tleft(ts,exp):  # trading minutes to 16:00 ET (20:00Z) on exp
    day=ts[:10]; m=int(ts[11:13])*60+int(ts[14:16]); left=max(0,20*60-m)
    import datetime
    d0=datetime.date.fromisoformat(day); d1=datetime.date.fromisoformat(exp); extra=0; d=d0
    while d<d1:
        d+=datetime.timedelta(days=1)
        if d.weekday()<5: extra+=390
    return (left+extra)/YM
def iv_solve(c,s,k,t,px):
    lo,hi=0.01,5.0
    for _ in range(60):
        mid=(lo+hi)/2
        if bs(c,s,k,t,mid)>px: hi=mid
        else: lo=mid
    return (lo+hi)/2
out=[];err=[]
for t in trips:
    if t['sym']!='SPY' or t['t_in'][:10]>='2026-10-15': continue
    tin=t['t_in'][:16]; tout=t['t_out'][:16]
    if tin not in spy or tout not in spy: continue
    c=t['typ']=='call'; k=t['strike']; E=t['p_in']
    s0=spy[tin][3]; iv=iv_solve(c,s0,k,tleft(tin,t['exp']),E)
    path=[m for m in keys if m[:10]==tin[:10] and tin<m<=tin[:10]+'T19:55']
    if not path: continue
    vals=[]
    for m in path:
        o,h,l,cl=spy[m]; tt=tleft(m,t['exp'])
        v=[bs(c,x,k,tt,iv) for x in (o,h,l,cl)]
        vals.append((m,v[0],max(v),min(v),v[3]))
    mx=[v for v in vals if v[0]<=tout]
    model_exit=(mx[-1][4] if mx else E)
    err.append(model_exit/t['p_out']-1)
    def rule(stop,tgt,trail=None):
        peak=E
        for m,o,h,l,cl in vals:
            stp=max(E*(1-stop),peak*(1-trail)) if trail else E*(1-stop)
            if l<=stp: return min(o,stp)/E-1
            if tgt and h>=E*(1+tgt): return tgt
            peak=max(peak,h)
        return vals[-1][4]/E-1
    out.append(dict(day=tin[:10],risk=E*t['q']*100,pnl=(t['p_out']-E)*t['q']*100,actual=t['p_out']/E-1,iv=iv,
        mfe=max(v[2] for v in vals)/E-1,mfe_held=(max(v[2] for v in mx)/E-1) if mx else 0,
        r20_50=rule(.2,.5),r40_100=rule(.4,1.0),r30_tr25=rule(.3,None,.25),eod=vals[-1][4]/E-1,
        post30=(vals[min(len(vals)-1,len(mx)+29)][4]/E-1)))
err=sorted(err)
print('model check: model exit vs your real exit price, median error %+.1f%%, middle 50%% [%+.1f%%, %+.1f%%], n=%d'%(100*median(err),100*err[len(err)//4],100*err[3*len(err)//4],len(err)))
json.dump(out,open(S+'/replay2_out.json','w'))
n=len(out)
print('SPY trips modeled',n)
print('ACTUAL net $%+.0f'%sum(o['pnl'] for o in out))
for k,lab in [('r20_50','stop -20% / take +50%'),('r40_100','stop -40% / take +100%'),('r30_tr25','stop -30%, trail 25% off peak'),('eod','hold to 3:55pm')]:
    print('%-32s net $%+7.0f  per trade %+6.1f%%  win%% %3.0f'%(lab,sum(o[k]*o['risk'] for o in out),100*mean(o[k] for o in out),100*mean(o[k]>0 for o in out)))
print('median max move your way after entry (same day) %+.0f%%; while you held %+.0f%%'%(100*median(o['mfe'] for o in out),100*median(o['mfe_held'] for o in out)))
print('up 20%%+ while held but closed red: %d of %d'%(sum(o['mfe_held']>=.2 and o['actual']<0 for o in out),n))
print('option higher 30 min after your exit: %d of %d'%(sum(o['post30']>o['actual'] for o in out),n))
for d in sorted({o['day'] for o in out}):
    x=[o for o in out if o['day']==d]
    print(d,'n=%2d actual $%+5.0f | -20/+50 $%+6.0f | -40/+100 $%+6.0f | trail $%+6.0f | hold $%+6.0f'%(len(x),sum(o['pnl'] for o in x),sum(o['r20_50']*o['risk'] for o in x),sum(o['r40_100']*o['risk'] for o in x),sum(o['r30_tr25']*o['risk'] for o in x),sum(o['eod']*o['risk'] for o in x)))
