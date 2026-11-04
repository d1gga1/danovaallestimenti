# -*- coding: utf-8 -*-
"""04/11/2026 - Titoli e H1 allineati alle ricerche reali (Keyword Planner, account DANOVA TECH, Italia, ott 2025 - set 2026).
   - "fiere bologna 2026", "fiere milano 2026", "fiere verona 2026" 1K-10K; "fiere rimini 2026", "fiere 2026",
     "calendario fiere 2026" 100-1K  -> calendari con "Fiere <citta'> 2026 e 2027" in testa
   - "bando fiere 2026", "simest fiere" 100-1K -> pagina contributi con "bandi"
   - "desk per fiere" 100-1K (CPC 6,32) -> pagina desk/totem con "desk per fiere" in testa
   - "espositori da banco" 1K-10K -> pagina espositori pubblicitari
   Idempotente. ATTENZIONE: strumenti/migra-da-danovatech.py sovrascrive queste pagine: dopo una reimportazione rilanciare questo script.
   Uso: python3 strumenti/patch-seo-2026-11-04.py"""
import os, re
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); OGGI = '2026-11-04'
def rd(p): return open(p, encoding='utf-8').read()
def wr(p, s): open(p, 'w', encoding='utf-8').write(s)
CAMBI = {}   # pagina -> [(vecchio, nuovo), ...]
CAL = {'bologna': ('Bologna', 'BolognaFiere'), 'milano': ('Milano', 'Fiera Milano Rho'), 'verona': ('Verona', 'Veronafiere'),
       'parma': ('Parma', 'Fiere di Parma'), 'firenze': ('Firenze', 'Fortezza da Basso')}
for s, (c, q) in CAL.items():
    CAMBI['calendario-fiere-' + s] = [
        ('Calendario fiere %s 2026–2027: date a %s' % (c, q), 'Fiere %s 2026 e 2027: calendario e date a %s' % (c, q)),
        ('Calendario fiere %s 2026–2027: <span class="grad">le date a %s</span>.' % (c, q), 'Fiere %s 2026 e 2027: <span class="grad">il calendario di %s</span>.' % (c, q))]
CAMBI['calendario-fiere-rimini'] = [('Calendario fiere Rimini 2026–2027: <span class="grad">le date a Rimini Expo Centre</span>.',
                                     'Fiere Rimini 2026 e 2027: <span class="grad">il calendario di Rimini Expo Centre</span>.')]
CAMBI['calendario-fiere'] = [('Calendario fiere 2026–2027 Italia ed Europa | Danova Stand', 'Fiere 2026 e 2027: calendario fiere Italia ed Europa')]
CAMBI['contributi-fiere-2026'] = [('Contributi per le fiere 2026: SIMEST e Camere di Commercio', 'Contributi e bandi fiere 2026: SIMEST e Camere di Commercio'),
                                  ('Contributi per le fiere 2026: <span class="grad">', 'Contributi e bandi per le fiere 2026: <span class="grad">')]
CAMBI['espositori-desk-totem-per-fiere'] = [('Espositori per fiere: desk, banchi e totem | Danova Stand', 'Desk per fiere, banchi e totem espositori | Danova Stand'),
                                            ('Espositori, desk e totem per fiere: <span class="grad">', 'Desk per fiere, banchi, totem ed espositori: <span class="grad">')]
CAMBI['espositori-pubblicitari'] = [('Espositori pubblicitari su misura per negozi e fiere', 'Espositori pubblicitari e da banco su misura per negozi'),
                                    ('Espositori pubblicitari su misura: <span class="grad">', 'Espositori pubblicitari e da banco su misura: <span class="grad">')]
toccate = []
for pag, cc in CAMBI.items():
    p = os.path.join(R, pag, 'index.html'); t = rd(p); t0 = t
    for a, b in cc:
        if b not in t and a not in t: print('ATTENZIONE non trovato in', pag, ':', a[:60])
        t = t.replace(a, b)
    if t != t0:
        t = re.sub(r'("@type": ?"WebPage".*?"dateModified": ?")[^"]*', lambda m: m.group(1) + OGGI, t, count=1, flags=re.S)
        wr(p, t); toccate.append(pag)
# llms.txt e sitemap
ll = os.path.join(R, 'llms.txt'); L = rd(ll); L0 = L
for cc in CAMBI.values():
    for a, b in cc:
        if '<span' not in a: L = L.replace(a, b)
if L != L0: wr(ll, L)
sm = os.path.join(R, 'sitemap.xml'); S = rd(sm); S0 = S
for pag in toccate:
    S = re.sub(r'(<loc>https://danovastand\.com/%s/</loc>\s*<lastmod>)[^<]*' % re.escape(pag), r'\g<1>' + OGGI, S)
if S != S0: wr(sm, S)
print('pagine aggiornate:', toccate)
