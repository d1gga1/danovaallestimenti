# Uso (dalla radice del sito): python3 "Claude outputs/prossima-sessione/merge_dev.py" de [--dry]
# Aggiorna i campi presenti in <lang>_fix_*.py dentro strumenti/traduzioni/fiere_<lang>*.py, mantenendo il resto.
import glob,sys,os,pprint,re
lang=sys.argv[1]; dry='--dry' in sys.argv; here=os.path.dirname(os.path.abspath(__file__))
R={}
for fn in sorted(glob.glob(f'{here}/{lang}_fix_*.py')):
    g={};exec(open(fn,encoding='utf-8').read(),g); R.update(g['R'])
IT={}
for fn in sorted(glob.glob('strumenti/dati_fiere_nuove*.py')):
    g={};exec(open(fn,encoding='utf-8').read(),g); IT.update({x['k']:x for x in g['F']})
def body(v): return ' '.join(v['intro']+[a+' '+b for a,b in v['esig']]+[a+' '+b for a,b in v['qa']]+[v['tempi']])
wc=lambda v: len(body(v).split()); cc=lambda v: len(re.sub(r'<[^>]+>','',body(v)))
keys=['nome','sett','cad','date','pub','lead','intro','esig','tempi','qa','off']
done=0; low=[]
for fn in sorted(glob.glob(f'strumenti/traduzioni/fiere_{lang}*.py')):
    src=open(fn,encoding='utf-8').read()
    head=src[:src.index('T = {')]
    g={};exec(src,g); T=g['T']
    for k in T:
        if k in R: T[k].update(R[k]); done+=1
    for k,v in T.items():
        r=wc(v)/wc(IT[k]); c=cc(v)/cc(IT[k])
        if r<0.8: low.append((round(r,2),round(c,2),k))
    if dry: continue
    out=[head+'T = {']
    for k,v in T.items():
        out.append(f'{k!r}: dict(')
        for x in keys:
            if x in v: out.append(f' {x}='+pprint.pformat(v[x],width=200,sort_dicts=False)+',')
        out.append('),')
    out.append('}')
    open(fn,'w',encoding='utf-8').write('\n'.join(out)+'\n')
print('aggiornate',done,'| sotto 0.8:',len(low)); [print(*x) for x in sorted(low)]
