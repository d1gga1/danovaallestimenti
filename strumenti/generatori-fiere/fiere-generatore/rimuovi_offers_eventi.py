# -*- coding: utf-8 -*-
# Rimuove dagli eventi gia' pubblicati gli "offers" incompleti (senza price), segnalati
# da Search Console il 17 ottobre 2026. Idempotente.
# Uso: dalla radice del sito -> python3 seo-tools/fiere-generatore/rimuovi_offers_eventi.py
import re,json,glob
n_ev=0
def walk(x):
    global n_ev
    if isinstance(x,dict):
        t=x.get("@type"); t=t if isinstance(t,list) else [t]
        if any(str(y).endswith("Event") for y in t if y):
            o=x.get("offers")
            if isinstance(o,dict) and "price" not in o: del x["offers"]; n_ev+=1
        for v in x.values(): walk(v)
    elif isinstance(x,list):
        for v in x: walk(v)
tot=0
for f in sorted(glob.glob('*/index.html')+glob.glob('*/*/index.html')+glob.glob('*/*/*/index.html')):
    s=open(f,encoding='utf-8').read()
    if 'Event"' not in s: continue
    def rep(m):
        t=m.group(2)
        if 'Event"' not in t: return m.group(0)
        d=json.loads(t); walk(d)
        return m.group(1)+'\n'+json.dumps(d,ensure_ascii=False,indent=2)+'\n'+m.group(3)
    s2=re.sub(r'(<script type="application/ld\+json">)(.*?)(</script>)',rep,s,flags=re.S)
    if s2!=s: open(f,'w',encoding='utf-8').write(s2); tot+=1
print('eventi corretti:',n_ev,'- pagine aggiornate:',tot)
