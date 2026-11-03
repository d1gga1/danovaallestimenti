# -*- coding: utf-8 -*-
"""22/10/2026: aggiunge al calendario le fiere delle nuove pagine e registra gli hreflang
IT <-> EN <-> ZH delle fiere europee e dell'hub Europa in intl_map.py. Idempotente."""
import os, re
H = os.path.dirname(os.path.abspath(__file__))

# ---------------- dati_calendario.py
p = os.path.join(H, 'dati_calendario.py'); s = open(p, encoding='utf-8').read()
NEW_IT = '''("made-expo","MADE expo","rho","edilizia","2027-11-01","2027-11-30",0,"https://www.madeexpo.it","Biennale"),
("cosmofarma","Cosmofarma","bologna","salute","2027-04-01","2027-04-30",0,"https://www.cosmofarma.com",""),
("fieragricola","Fieragricola","verona","agri","2028-02-01","2028-02-29",0,"https://www.fieragricola.it","Biennale"),
("transpotec","Transpotec Logitec","rho","auto","2028-05-01","2028-05-31",0,"https://www.transpotec.com","Biennale"),
'''
NEW_DE = '''("interpack","interpack","duesseldorf","pack","2029-06-01","2029-06-30",0,"https://www.interpack.com","Triennale"),
("euroshop","EuroShop","duesseldorf","arredo","2029-02-01","2029-02-28",0,"https://www.euroshop-tradefair.com","Triennale"),
'''
if '("made-expo"' not in s:
    s = s.replace('# ---------------- GERMANIA\n', NEW_IT + '# ---------------- GERMANIA\n', 1)
if '("interpack"' not in s:
    s = s.replace('# ---------------- FRANCIA\n', NEW_DE + '# ---------------- FRANCIA\n', 1)
# SIAL Paris 2026 si e' chiusa il 21/10: prossima edizione ottobre 2028 (biennale)
s = s.replace('("sial","SIAL Paris","parisn","food","2026-10-17","2026-10-21",1,"https://www.sialparis.com",""),',
              '("sial","SIAL Paris","parisn","food","2028-10-01","2028-10-31",0,"https://www.sialparis.com","Biennale"),')
open(p, 'w', encoding='utf-8').write(s)

# ---------------- intl_map.py
p = os.path.join(H, 'intl_map.py'); s = open(p, encoding='utf-8').read()
ADD = '''
# 22/10/2026: fiere europee (dati_2610_intl) e hub Europa
import dati_2610_intl as DX
for f in DX.FAIRS:
    _add(f"/stand-{f['k']}/", f"/en/{f['en']['slug']}/", f"/zh/{f['zh']['slug']}/")
_add('/allestimenti-fieristici-estero/', '/en/exhibition-stand-builder-europe/', '/zh/europe-exhibition-stand/')
'''
if 'dati_2610_intl' not in s:
    s = s.replace("_add('/guide/come-preparare-una-fiera/', '/en/exhibiting-at-trade-fairs-in-italy/', '/zh/italy-trade-fair-guide/')\n",
                  "_add('/guide/come-preparare-una-fiera/', '/en/exhibiting-at-trade-fairs-in-italy/', '/zh/italy-trade-fair-guide/')\n" + ADD, 1)
    assert 'dati_2610_intl' in s
open(p, 'w', encoding='utf-8').write(s)
print('ok')
