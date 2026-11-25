import glob,sys,os,pprint
lang=sys.argv[1]; out='/mnt/user-data/outputs'
IT={};ORD=[]
for fn in sorted(glob.glob(out+'/dati_fiere_nuove*.py')):
    g={};exec(open(fn,encoding='utf-8').read(),g); ORD.append([x['k'] for x in g['F']]); IT.update({x['k']:x for x in g['F']})
T={}
for fn in sorted(glob.glob(f'{out}/fiere_{lang}*.py')):
    g={};exec(open(fn,encoding='utf-8').read(),g); T.update(g['T'])
for fn in sorted(glob.glob(f'/home/claude/{lang}_fix_*.py')):
    g={};exec(open(fn,encoding='utf-8').read(),g)
    for k,v in g['R'].items():
        if k in T: T[k].update(v)
        else: T[k]=v
keys=['sett','cad','date','pub','lead','intro','esig','tempi','qa','off']
hdr={'fr':"# Pages salons en français (/fr/standiste-<salon>/). Clés = \"k\" de strumenti/dati_fiere_nuove*.py.",
     'es':"# Páginas de ferias en español (/es/stand-<feria>/). Claves = \"k\" de strumenti/dati_fiere_nuove*.py."}[lang]
os.makedirs('/home/claude/final',exist_ok=True)
for i,ks in enumerate(ORD):
    name=f'fiere_{lang}.py' if i==0 else f'fiere_{lang}_{i+1}.py'
    lines=['# -*- coding: utf-8 -*-',hdr,'T = {']
    for k in ks:
        if k not in T: continue
        v=T[k]; miss=[x for x in keys if x not in v]
        assert not miss,(k,miss)
        lines.append(f'{k!r}: dict(')
        if 'nome' in v: lines.append(f' nome={v["nome"]!r},')
        for x in keys: lines.append(f' {x}='+pprint.pformat(v[x],width=200,sort_dicts=False)+',')
        lines.append('),')
    lines.append('}')
    open(f'/home/claude/final/{name}','w',encoding='utf-8').write('\n'.join(lines)+'\n')
print('done',len(T))
