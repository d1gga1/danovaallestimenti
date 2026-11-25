import glob,sys
IT={};EN={}
for fn in sorted(glob.glob('/mnt/user-data/outputs/dati_fiere_nuove*.py')):
    g={};exec(open(fn,encoding='utf-8').read(),g); IT.update({x['k']:x for x in g['F']})
for fn in sorted(glob.glob('/mnt/user-data/outputs/fiere_en*.py')):
    g={};exec(open(fn,encoding='utf-8').read(),g); EN.update(g['T'])
for k in sys.argv[1:]:
    x=IT[k]; print('##',k)
    for f in ['sett','cad','date','lead','intro','esig','tempi','qa','off']: print(f,'=',x[f])
    print('pub(EN) =',EN[k]['pub'])
