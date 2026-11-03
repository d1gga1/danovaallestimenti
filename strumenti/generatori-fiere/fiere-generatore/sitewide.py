# -*- coding: utf-8 -*-
import os,re,json,sys
sys.path.insert(0,os.path.dirname(__file__))
from it_common import CL,CITY_LINKS
R=os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','..'))
FIERE_COL=[("Allestimenti fieristici","/servizi/allestimenti-fieristici/"),("Stand per metratura","/stand-fieristici-per-metratura/"),("Calendario fiere 2026–2027","/calendario-fiere/"),("Montaggio stand","/montaggio-stand-fieristici/"),
 ("Stand su misura","/stand-fieristici-su-misura/"),("Stand modulari","/stand-modulari/"),("Noleggio stand","/noleggio-stand-fieristici/"),
 ("Quanto costa uno stand","/quanto-costa-uno-stand-fieristico/"),("Eventi, showroom, negozi","/allestimenti-eventi-showroom-negozi/"),
 ("Fiere all'estero","/allestimenti-fieristici-estero/")]+CITY_LINKS
LP={'en':('Services','/en/exhibition-stand-builder-italy/','Exhibition stands'),'de':('Leistungen','/de/messebau-italien/','Messebau'),
    'fr':('Services','/fr/standiste-salon-italie/','Stands de salon'),'es':('Servicios','/es/montaje-stands-feriales-italia/','Stands feriales')}
li=lambda items:''.join(f'\n        <li><a href="{h}">{t}</a></li>' for t,h in items)
n=0
for dp,dn,fn in os.walk(R):
    dn[:]=[d for d in dn if d not in ('seo-tools','assets','.git')]
    if 'index.html' not in fn: continue
    p=os.path.join(dp,'index.html'); rel=os.path.relpath(p,R)
    if rel in ('index.html','en/index.html','de/index.html','fr/index.html','es/index.html'): continue
    L=rel.split('/')[0] if rel.split('/')[0] in ('en','de','fr','es','zh','tr','ar') else 'it'
    s=open(p,encoding='utf-8').read(); o=s
    if L=='it':
        if '<h5>Fiere</h5>' not in s and '<div><h5>Agenzia</h5><ul>' in s:
            s=s.replace('<div><h5>Agenzia</h5><ul>','<div><h5>Fiere</h5><ul>'+li(FIERE_COL)+'\n      </ul></div>\n      <div><h5>Agenzia</h5><ul>',1)
        m=re.search(r'(<h5>Servizi</h5><ul>)(.*?)(</ul>)',s,re.S)
        if m and 'allestimenti-fieristici/"' not in m.group(2):
            s=s[:m.end(2)]+li([("Allestimenti fieristici","/servizi/allestimenti-fieristici/")])+'\n      '+s[m.end(2):]
    elif L in LP:
        col,url,lab=LP[L]
        m=re.search(rf'(<h5>{col}</h5><ul>)(.*?)(</ul>)',s,re.S)
        if m and url not in m.group(2):
            s=s[:m.end(2)]+li([(lab,url)])+'\n      '+s[m.end(2):]
    if s!=o: open(p,'w',encoding='utf-8').write(s); n+=1
print('footer aggiornati:',n)

# ---- home IT: citta' e approfondimenti sotto la sezione fiere
p=os.path.join(R,'index.html'); s=open(p,encoding='utf-8').read()
if 'fr-links' not in s:
    links=''.join(f'<a href="{u}">{t.replace("Stand a ","")}</a>' for t,u in CITY_LINKS)
    extra=f'''
        <div class="fr-links"><span>Lavoriamo in tutte le fiere:</span>{links}<a href="/allestimenti-fieristici-estero/">Estero</a></div>
        <div class="fr-links fr-links2"><a href="/montaggio-stand-fieristici/">Montaggio stand</a><a href="/stand-fieristici-su-misura/">Stand su misura</a><a href="/stand-modulari/">Stand modulari</a><a href="/noleggio-stand-fieristici/">Noleggio stand</a><a href="/quanto-costa-uno-stand-fieristico/">Quanto costa uno stand</a></div>'''
    k=s.index('<div class="fr-vis">'); j=s.rindex('</div>',0,k)  # chiusura di fr-txt
    s=s[:j]+extra.lstrip('\n')+'\n      '+s[j:]
    css='.fr-links{display:flex;flex-wrap:wrap;gap:8px 14px;margin-top:22px;font-size:13.5px;color:var(--muted)}.fr-links span{color:#b9c2d6}.fr-links a{color:#9fc0ff;border-bottom:1px solid rgba(122,169,255,.3)}.fr-links a:hover{color:#fff;border-color:#7aa9ff}.fr-links2{margin-top:10px}\n'
    s=s.replace('</style>',css+'</style>',1)
    open(p,'w',encoding='utf-8').write(s); print('home it ok')
# ---- home altre lingue: secondo pulsante verso la pagina dedicata
for L,(col,url,lab) in LP.items():
    p=os.path.join(R,L,'index.html'); s=open(p,encoding='utf-8').read()
    if url not in s:
        import html
        lab2={'en':'Learn more','de':'Mehr erfahren','fr':'En savoir plus','es':'Más información'}[L]
        btn=f'\n          <a href="{url}" class="btn btn-g" data-mag><span class="lbl" data-i18n="fiere.cta2">{lab2}</span></a>'
        a=s.index('data-pick-tipo'); b=s.index('</a>',a)+4
        s=s[:b]+btn+s[b:]
        open(p,'w',encoding='utf-8').write(s); print('home',L,'ok')
