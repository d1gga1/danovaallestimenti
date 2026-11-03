# -*- coding: utf-8 -*-
# Collega calendario e nuove pagine fiere a footer e home (idempotente). Uso: python3 patch_link_nuove.py
import os,re
R=os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','..'))
LI='\n        <li><a href="/calendario-fiere/">Calendario fiere 2026–2027</a></li>'
n=0
for dp,dn,fn in os.walk(R):
    dn[:]=[d for d in dn if d not in ('seo-tools','assets','.git','en','de','fr','es','zh','tr','ar')]
    if 'index.html' not in fn: continue
    p=os.path.join(dp,'index.html'); s=open(p,encoding='utf-8').read()
    m=re.search(r'<div><h5>Fiere</h5><ul>(.*?)</ul>',s,re.S)
    if not m or '/calendario-fiere/' in m.group(1): continue
    first=re.search(r'\n\s*<li>.*?</li>',m.group(1)).end()
    k=m.start(1)+first
    s=s[:k]+LI+s[k:]; open(p,'w',encoding='utf-8').write(s); n+=1
print('footer con calendario:',n)
p=os.path.join(R,'index.html'); s=open(p,encoding='utf-8').read()
if '/calendario-fiere/' not in s:
    s=s.replace('<div class="fr-links fr-links2"><a href="/montaggio-stand-fieristici/">','<div class="fr-links fr-links2"><a href="/calendario-fiere/">Calendario fiere 2026–2027</a><a href="/stand-a-isola/">Stand a isola</a><a href="/stand-preallestiti/">Stand preallestiti</a><a href="/montaggio-stand-fieristici/">',1)
    s=s.replace('<a href="/allestimenti-fieristici-estero/">Estero</a></div>','<a href="/allestimenti-fieristici-treviso/">Treviso</a><a href="/allestimenti-fieristici-firenze/">Firenze</a><a href="/allestimenti-fieristici-torino/">Torino</a><a href="/allestimenti-fieristici-roma/">Roma</a><a href="/allestimenti-fieristici-genova/">Genova</a><a href="/allestimenti-fieristici-bolzano/">Bolzano</a><a href="/allestimenti-fieristici-estero/">Estero</a></div>',1)
    s=s.replace('<div class="fr-links fr-links2">','<div class="fr-links fr-links2"><span>Le fiere:</span><a href="/stand-vinitaly/">Vinitaly</a><a href="/stand-salone-del-mobile/">Salone del Mobile</a><a href="/stand-eicma/">EICMA</a><a href="/stand-cosmoprof/">Cosmoprof</a><a href="/stand-marmomac/">Marmomac</a><a href="/stand-host/">Host</a></div>\n        <div class="fr-links fr-links2">',1)
    open(p,'w',encoding='utf-8').write(s); print('home ok', s.count('/calendario-fiere/'))
# ---- llms.txt: nuove pagine fiere
import sys; sys.path.insert(0,os.path.dirname(__file__))
from nuove_common import FIERA_PAGES, FIERA_URL, CITTA_NUOVE, CITTA_URL, TIPI, SETTORI
p=os.path.join(R,'llms.txt'); s=open(p,encoding='utf-8').read()
if '/calendario-fiere/' not in s:
    S='https://danova-tech.com'
    add=f"- Calendario fiere 2026-2027 Italia ed Europa, con mappa e richiesta stand: {S}/calendario-fiere/\n"
    add+=''.join(f"- {c}: {S}{CITTA_URL[x]}\n" for c,x in CITTA_NUOVE)
    add+=''.join(f"- {t} (stand per la fiera): {S}{FIERA_URL[k]}\n" for k,t in FIERA_PAGES)
    add+=''.join(f"- {t}: {S}/{x}/\n" for x,t in TIPI+SETTORI)
    s=s.replace(f"- Parma: {S}/allestimenti-fieristici-parma/\n",f"- Parma: {S}/allestimenti-fieristici-parma/\n"+add,1)
    open(p,'w',encoding='utf-8').write(s); print('llms.txt ok')
