import json,sys,collections
d=sys.argv[1]
orders=[]
for f in ['orders_p1.json','orders_p2.json']:
    orders+=json.load(open(f'{d}/{f}'))['data']['orders']
fills=[]
for o in orders:
    if o.get('placed_agent')!='user': continue
    for lg in o['legs']:
        for e in lg.get('executions',[]):
            fills.append(dict(t=e['timestamp'],oid=lg['option_id'],side=lg['side'],eff=lg['position_effect'],
                 px=float(e['price']),q=float(e['quantity']),strike=float(lg['strike_price']),typ=lg['option_type'],exp=lg['expiration_date'],sym=o['chain_symbol']))
fills.sort(key=lambda f:f['t'])
openl=collections.defaultdict(list); trips=[]
for f in fills:
    if f['eff']=='open': openl[f['oid']].append(dict(f))
    else:
        q=f['q']
        while q>1e-9 and openl[f['oid']]:
            lot=openl[f['oid']][0]; take=min(q,lot['q'])
            trips.append(dict(oid=f['oid'],sym=f['sym'],typ=f['typ'],strike=f['strike'],exp=f['exp'],t_in=lot['t'],t_out=f['t'],p_in=lot['px'],p_out=f['px'],q=take))
            lot['q']-=take; q-=take
            if lot['q']<=1e-9: openl[f['oid']].pop(0)
json.dump(trips,open(f'{d}/trips.json','w'))
print('fills',len(fills),'trips',len(trips),'open lots left',sum(len(v) for v in openl.values()))
ids=collections.defaultdict(set)
for t in trips: ids[t['t_in'][:10]].add(t['oid'])
for k in sorted(ids): print(k,len(ids[k]))
pnl=sum((t['p_out']-t['p_in'])*t['q']*100 for t in trips); print('net', round(pnl))
