# Uso (dalla radice del sito): python3 "Claude outputs/prossima-sessione/assemble_dev.py" es
import glob,sys,os,pprint
lang=sys.argv[1]; here=os.path.dirname(os.path.abspath(__file__))
ORD=[]
for fn in sorted(glob.glob('strumenti/dati_fiere_nuove*.py')):
    g={};exec(open(fn,encoding='utf-8').read(),g); ORD.append([x['k'] for x in g['F']])
T={}
for fn in sorted(glob.glob(f'{here}/{lang}_fix_*.py')):
    g={};exec(open(fn,encoding='utf-8').read(),g); T.update(g['R'])
keys=['sett','cad','date','pub','lead','intro','esig','tempi','qa','off']
hdr={'es':"# Páginas de ferias en español (/es/stand-<feria>/). Claves = \"k\" de strumenti/dati_fiere_nuove*.py."}[lang]
for i,ks in enumerate(ORD):
    name=f'fiere_{lang}.py' if i==0 else f'fiere_{lang}_{i+1}.py'
    lines=['# -*- coding: utf-8 -*-',hdr,'T = {']
    for k in ks:
        v=T[k]; miss=[x for x in keys if x not in v]; assert not miss,(k,miss)
        lines.append(f'{k!r}: dict(')
        if 'nome' in v: lines.append(f' nome={v["nome"]!r},')
        for x in keys: lines.append(f' {x}='+pprint.pformat(v[x],width=200,sort_dicts=False)+',')
        lines.append('),')
    lines.append('}')
    open(f'strumenti/traduzioni/{name}','w',encoding='utf-8').write('\n'.join(lines)+'\n')
print('done',len(T))
