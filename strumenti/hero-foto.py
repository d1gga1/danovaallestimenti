#!/usr/bin/env python3
"""Sostituisce il disegno 3D stilizzato (svg.fr-svg) in apertura delle pagine fiera con un'immagine
di stand realistica. Idempotente. Rilanciare dopo migra-da-danovatech.py.
Per usare FOTO VERE: metti il file in assets/img/stand/ e indicalo in FOTO_FORZATE qui sotto."""
import os, re
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMGDIR = os.path.join(ROOT, 'assets', 'img', 'stand')
FOTO_FORZATE = {}   # es. {'stand-vinitaly': 'foto-vera-vinitaly-2025'}
GENERICA = 'stand-48-mq-isola'
base = sorted({re.sub(r'-(800|1200)$', '', f[:-5]) for f in os.listdir(IMGDIR) if f.endswith('.webp')})
SIN = {'food':'alimentare','vino':'cantina','wine':'cantina','beauty':'cosmetica','moto':'eicma','gioielli':'vicenzaoro',
       'frankfurt':'estero','berlin':'estero','paris':'estero','messe':'estero'}
def scegli(slug, testo):
    if slug in FOTO_FORZATE: return FOTO_FORZATE[slug]
    usate = re.findall(r'assets/img/stand/([a-z0-9-]+?)(?:-800|-1200)?\.webp', testo)
    if usate: return max(set(usate), key=usate.count)
    tok = set(slug.replace('stand-','').split('-')); tok |= {SIN[t] for t in tok if t in SIN}
    best, bs = GENERICA, 0
    for b in base:
        s = len(tok & set(b.split('-')))
        if s > bs: best, bs = b, s
    return best
PAT = re.compile(r'<div class="fr-hero-vis"><svg class="fr-svg".*?</svg></div>', re.S)
PAT2 = re.compile(r'<div class="fr-hero-vis fr-hero-foto">.*?</div>', re.S)
n = 0
for root, dirs, files in os.walk(ROOT):
    dirs[:] = [d for d in dirs if d not in ('.git','strumenti','_google_business')]
    if 'index.html' not in files: continue
    p = os.path.join(root, 'index.html'); t = open(p, encoding='utf-8').read()
    if 'fr-hero-vis' not in t: continue
    slug = os.path.basename(root)
    img = scegli(slug, PAT2.sub('', t))
    sz = '-800' if os.path.exists(os.path.join(IMGDIR, img+'-800.webp')) else ''
    big = '-1200' if os.path.exists(os.path.join(IMGDIR, img+'-1200.webp')) else ''
    srcset = f' srcset="/assets/img/stand/{img}{sz}.webp 800w, /assets/img/stand/{img}{big}.webp 1200w" sizes="(max-width:1180px) 0px, 440px"' if sz and big else ''
    html = (f'<div class="fr-hero-vis fr-hero-foto"><img src="/assets/img/stand/{img}{sz}.webp"{srcset} '
            f'alt="" width="800" height="600" fetchpriority="high" decoding="async"></div>')
    new = PAT.sub(html, t); new = PAT2.sub(html, new)
    if new != t: open(p, 'w', encoding='utf-8').write(new); n += 1
css = os.path.join(ROOT, 'assets', 'css', 'fiere.css'); c = open(css).read()
if 'fr-hero-foto' not in c:
    c += """
/* immagine realistica in apertura (strumenti/hero-foto.py) */
.fr-hero-foto{transform:translateY(-50%)}
.fr-hero-foto::before{display:none}
@media (min-width:1181px){.pg-hero:has(.fr-hero-foto) h1{max-width:14ch}}
.fr-hero-foto img{display:block;width:100%;height:auto!important;max-height:none;aspect-ratio:4/3;object-fit:cover;border-radius:18px;
  border:1px solid rgba(255,255,255,.08);box-shadow:0 30px 70px -20px rgba(0,0,0,.85),0 0 0 6px rgba(255,255,255,.02)}
"""
    open(css, 'w').write(c)
print('pagine aggiornate:', n)
