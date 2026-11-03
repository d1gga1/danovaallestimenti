# -*- coding: utf-8 -*-
# Applica i render alle pagine gia' generate (idempotente). Uso: python3 applica_immagini.py
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from immagini import MAP, inject
R = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
ok = 0
for p in sorted(MAP):
    fn = os.path.join(R, p.strip('/'), 'index.html')
    if not os.path.exists(fn):
        print('manca', p); continue
    s = open(fn, encoding='utf-8').read()
    t = inject(s, p)
    if t != s:
        open(fn, 'w', encoding='utf-8').write(t); ok += 1
    if 'class="fr-foto"' not in t: print('NON inserita', p)
print('pagine aggiornate:', ok, 'di', len(MAP))

# blocco logistica nelle pagine citta'
import citta_extra
n = 0
for s in citta_extra.C:
    p = f'/allestimenti-fieristici-{s}/'
    fn = os.path.join(R, p.strip('/'), 'index.html')
    if not os.path.exists(fn): continue
    a = open(fn, encoding='utf-8').read(); b = citta_extra.inject(a, p)
    if b != a: open(fn, 'w', encoding='utf-8').write(b); n += 1
print('pagine citta con logistica:', n)

# approfondimenti nelle pagine fiere piu' brevi
import fiere_extra
k = 0
for p in fiere_extra.X:
    fn = os.path.join(R, p.strip('/'), 'index.html')
    if not os.path.exists(fn): continue
    x = open(fn, encoding='utf-8').read(); y = fiere_extra.inject(x, p)
    if y != x: open(fn, 'w', encoding='utf-8').write(y); k += 1
print('pagine fiere con approfondimento:', k)
