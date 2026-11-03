# -*- coding: utf-8 -*-
# Aggiunge organizer/performer/image/offers agli eventi gia' presenti nelle pagine (idempotente).
# Uso: dalla radice del sito -> python3 seo-tools/fiere-generatore/patch_eventi.py
import re,json,glob,sys,os
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from event_extra import arricchisci
def walk(x):
    if isinstance(x,dict):
        t=x.get("@type"); t=t if isinstance(t,list) else [t]
        if any(str(y).endswith("Event") for y in t if y): arricchisci(x)
        for v in x.values(): walk(v)
    elif isinstance(x,list):
        for v in x: walk(v)
tot=0
for f in sorted(glob.glob('*/index.html')+glob.glob('*/*/index.html')):
    s=open(f,encoding='utf-8').read()
    if 'Event"' not in s: continue
    def rep(m):
        t=m.group(2)
        if 'Event"' not in t: return m.group(0)
        d=json.loads(t); walk(d)
        return m.group(1)+'\n'+json.dumps(d,ensure_ascii=False,indent=2)+'\n'+m.group(3)
    s2=re.sub(r'(<script type="application/ld\+json">)(.*?)(</script>)',rep,s,flags=re.S)
    if s2!=s: open(f,'w',encoding='utf-8').write(s2); tot+=1; print('ok',f)
print('pagine aggiornate:',tot)
