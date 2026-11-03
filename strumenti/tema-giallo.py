#!/usr/bin/env python3
"""Tema Danova Stand: sostituisce il blu Danova Tech con il giallo e centra i titoli.
Da rilanciare dopo ogni migra-da-danovatech.py:  python3 strumenti/tema-giallo.py
"""
import re, os, colorsys, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TARGET_H = 43/360          # giallo caldo (#FFC93C)
FIXED = {'1e6bff': 'ffc93c'}  # colore principale
FIXED_RGB = {(30,107,255): (255,201,60)}

def is_blue(r,g,b):
    h,l,s = colorsys.rgb_to_hls(r/255,g/255,b/255)
    return 0.55 <= h <= 0.66 and s >= 0.5 and not (l > 0.93 and s < 0.6)

def rot(r,g,b):
    if (r,g,b) in FIXED_RGB: return FIXED_RGB[(r,g,b)]
    h,l,s = colorsys.rgb_to_hls(r/255,g/255,b/255)
    r2,g2,b2 = colorsys.hls_to_rgb(TARGET_H, l, s)
    return round(r2*255), round(g2*255), round(b2*255)

def hexsub(m):
    t = m.group(1); low = t.lower()
    full = ''.join(c*2 for c in low) if len(low)==3 else low
    if full in FIXED: return '#'+(FIXED[full].upper() if t.isupper() else FIXED[full])
    r,g,b = (int(full[i:i+2],16) for i in (0,2,4))
    if not is_blue(r,g,b): return m.group(0)
    out = '%02x%02x%02x' % rot(r,g,b)
    return '#'+(out.upper() if t.isupper() else out)

def rgbsub(m):
    r,g,b = int(m.group(2)),int(m.group(3)),int(m.group(4))
    if not is_blue(r,g,b): return m.group(0)
    r2,g2,b2 = rot(r,g,b)
    return f'{m.group(1)}{r2},{g2},{b2}'

HEX = re.compile(r'#([0-9a-fA-F]{6}|[0-9a-fA-F]{3})\b')
RGB = re.compile(r'(rgba?\(\s*)(\d+)\s*,\s*(\d+)\s*,\s*(\d+)')

EXTRA = """
/* === TEMA GIALLO DANOVA STAND (strumenti/tema-giallo.py) === */
.btn-p,.btn-p:hover,.filters button.on,.lgl-tabs button.on,.lgl-done,.skip,
.lang-menu button:hover b,.lang-links a[aria-current="page"],#mob .mob-lang-links a[aria-current="page"],.lgl-done:hover{color:#0b0b0b!important}
.btn-p svg,.btn-p *{color:inherit;stroke:currentColor}
::selection{color:#0b0b0b}
/* titoli e testi principali centrati */
.pg-hero{text-align:center}
.pg-hero h1,.pg-hero .lead,.pg-hero p{margin-left:auto;margin-right:auto}
.pg-hero .hero-cta{justify-content:center}
.pg-hero .eyebrow{justify-content:center}
.sec-head{text-align:center;margin-left:auto;margin-right:auto}
.sec-head .title,.sec-head p,.sec-head .lead{margin-left:auto;margin-right:auto}
.sec-head .eyebrow{justify-content:center}
.pg-crumbs{text-align:center}
/* pagine fiera con illustrazione 3D a destra: su desktop testo a sinistra per non sovrapporsi */
@media (min-width:1181px){
.pg-hero:has(.fr-hero-vis){text-align:left}
body:has(.fr-hero-vis) .pg-crumbs{text-align:left}
.pg-hero:has(.fr-hero-vis) h1,.pg-hero:has(.fr-hero-vis) .lead,.pg-hero:has(.fr-hero-vis) p{margin-left:0;margin-right:0}
.pg-hero:has(.fr-hero-vis) .hero-cta,.pg-hero:has(.fr-hero-vis) .eyebrow{justify-content:flex-start}
}
.dt-bar-call,.dt-bar-call *,.dt-urg-p button[aria-pressed=true]{color:#0b0b0b!important}
/* === FINE TEMA GIALLO === */
"""

changed = 0
for root, dirs, files in os.walk(ROOT):
    dirs[:] = [d for d in dirs if d not in ('.git','strumenti','_google_business','node_modules')]
    for f in files:
        if not f.endswith(('.css','.js','.html','.svg','.webmanifest','.json')): continue
        p = os.path.join(root,f)
        t = open(p, encoding='utf-8', errors='surrogateescape').read()
        n = RGB.sub(rgbsub, HEX.sub(hexsub, t))
        # TESTO_SCURO: testo bianco su giallo diventa scuro
        n = n.replace('background:#FFC93C;color:#fff', 'background:#FFC93C;color:#0b0b0b').replace('border-color:var(--blue,#FFC93C);color:#fff', 'border-color:var(--blue,#FFC93C);color:#0b0b0b')
        if f == 'site.css' and 'TEMA GIALLO' not in n:
            n = n.replace('blu elettrico', 'giallo') + EXTRA
        if n != t:
            open(p,'w',encoding='utf-8',errors='surrogateescape').write(n); changed += 1
import subprocess, shutil
orig = os.path.join(ROOT,'strumenti','logo-blu-originale.png'); logo = os.path.join(ROOT,'assets','img','logo.png')
if os.path.exists(orig) and shutil.which('convert'):
    subprocess.run(['convert', orig, '-modulate', '100,120,5', logo], check=True)
print('file modificati:', changed)
