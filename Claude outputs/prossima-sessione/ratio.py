import glob,sys
IT={}
for fn in sorted(glob.glob('dati_fiere_nuove*.py')):
    g={};exec(open(fn,encoding='utf-8').read(),g); IT.update({x['k']:x for x in g['F']})
def wc(v): return sum(len(s.split()) for s in v['intro'])+sum(len((a+' '+b).split()) for a,b in v['esig'])+sum(len((a+' '+b).split()) for a,b in v['qa'])+len(v['tempi'].split())
lang=sys.argv[1]
FR={}
for fn in sorted(glob.glob(f'fiere_{lang}*.py')):
    g={};exec(open(fn,encoding='utf-8').read(),g); T=g['T']
    for k,v in g.get('_QA',{}).items(): T[k]['qa']=v
    FR.update({k:(v,fn) for k,v in T.items()})
bad=[]
for k,(v,fn) in FR.items():
    r=wc(v)/wc(IT[k]); 
    if r<0.8: bad.append((round(r,2),k,fn))
print(len(FR),'entries; below 0.8:',len(bad))
for b in sorted(bad): print(*b)
print('missing:',[k for k in IT if k not in FR])
