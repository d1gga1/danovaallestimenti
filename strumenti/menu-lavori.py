#!/usr/bin/env python3
"""Voce "I nostri lavori" in cima al menu (desktop + mobile) di ogni pagina, in ogni lingua.

    python3 strumenti/menu-lavori.py

Idempotente: toglie la voce vecchia (attributo data-ds="lavori") e la rimette.
Porta all'hub dei lavori realizzati: IT /lavori/, FR /fr/realisations/, tutte le altre lingue /en/projects/.
Aggiunge anche lo stile della voce in assets/css/site.css (blocco MENU LAVORI), che migra-da-danovatech.py
sovrascrive: rilanciarlo dopo la migrazione, prima di genera-feed-e-testo.py.
"""
import os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SALTA = {'.git', 'private_area', 'strumenti', 'Claude outputs', '_google_business', 'nuove_foto_newstand', 'assets', 'node_modules'}

HUB = {'it': '/lavori/', 'fr': '/fr/realisations/'}
HUB_DEF = '/en/projects/'
ETICHETTA = {
    'it': 'I nostri lavori', 'en': 'Our work', 'fr': 'Nos réalisations', 'de': 'Referenzen',
    'es': 'Nuestros trabajos', 'pt': 'Nossos trabalhos', 'nl': 'Ons werk', 'sv': 'Våra projekt',
    'pl': 'Nasze realizacje', 'cs': 'Naše realizace', 'hu': 'Munkáink', 'ro': 'Lucrările noastre',
    'bg': 'Нашите проекти', 'hr': 'Naši radovi', 'el': 'Τα έργα μας', 'sq': 'Punët tona',
    'ru': 'Наши работы', 'uk': 'Наші роботи', 'tr': 'Projelerimiz', 'ar': 'أعمالنا',
    'he': 'העבודות שלנו', 'fa': 'نمونه‌کارها', 'ur': 'ہمارا کام', 'hi': 'हमारे काम',
    'bn': 'আমাদের কাজ', 'pa': 'ਸਾਡਾ ਕੰਮ', 'gu': 'અમારું કામ', 'ta': 'எங்கள் பணிகள்',
    'zh-Hans': '我们的案例', 'zh-Hant': '我們的案例', 'ja': '施工実績', 'ko': '시공 사례',
    'id': 'Proyek kami', 'ms': 'Projek kami', 'vi': 'Dự án', 'th': 'ผลงานของเรา',
}

CSS = """/* === MENU LAVORI (strumenti/menu-lavori.py) === */
nav.links a.nav-lavori{color:#fff;background:rgba(255,201,60,.10);border:1px solid var(--line-strong);margin-right:4px}
nav.links a.nav-lavori:hover,nav.links a.nav-lavori[aria-current="page"]{background:rgba(255,201,60,.20);color:#fff}
nav.links a.nav-lavori::before{content:"";display:inline-block;width:6px;height:6px;border-radius:50%;background:var(--blue);margin-right:7px;vertical-align:middle;position:relative;top:-1px}
#mob a.nav-lavori{color:var(--blue-2)}
/* menu lungo (IT, 9 voci): tra 901 e 1240px non ci sta col pulsante "Parliamone", che porta allo stesso modulo di "Contatti" */
@media (min-width:901px) and (max-width:1240px){header:has(nav.links a:nth-child(8)) .nav-r .btn-p{display:none}nav.links a.nav-lavori::before{display:none}}
/* === FINE MENU LAVORI === */
"""

RE_OLD = re.compile(r'\s*<a [^>]*data-ds="lavori"[^>]*>.*?</a>', re.S)
RE_NAV = re.compile(r'(<nav (?:class="links"|id="mob")[^>]*>)(\n?)([ \t]*)')


def lingua(s):
    m = re.search(r'<html[^>]*\blang="([^"]+)"', s)
    return m.group(1) if m else 'it'


def url_pagina(path):
    rel = os.path.relpath(path, ROOT).replace(os.sep, '/')
    if rel == 'index.html':
        return '/'
    return '/' + rel[:-len('index.html')] if rel.endswith('/index.html') else '/' + rel


def main():
    cambiate = 0
    for d, dirs, files in os.walk(ROOT):
        dirs[:] = [x for x in dirs if x not in SALTA and not x.startswith('.')]
        for f in files:
            if not f.endswith('.html'):
                continue
            p = os.path.join(d, f)
            s = open(p, encoding='utf-8').read()
            if 'class="links"' not in s and 'id="mob"' not in s:
                continue
            lg = lingua(s)
            base = lg.split('-')[0] if lg not in ETICHETTA else lg
            hub = HUB.get(base, HUB_DEF)
            lab = ETICHETTA.get(lg) or ETICHETTA.get(base) or ETICHETTA['en']
            cur = ' aria-current="page"' if url_pagina(p).startswith(hub) else ''
            n = RE_OLD.sub('', s)

            def ins(m):
                ind = m.group(3) or '  '
                return f'{m.group(1)}\n{ind}<a href="{hub}" class="nav-lavori" data-ds="lavori"{cur}>{lab}</a>\n{ind}'
            n = RE_NAV.sub(ins, n)
            if n != s:
                open(p, 'w', encoding='utf-8').write(n)
                cambiate += 1

    cp = os.path.join(ROOT, 'assets/css/site.css')
    c = open(cp, encoding='utf-8').read()
    c2 = re.sub(r'/\* === MENU LAVORI.*?FINE MENU LAVORI === \*/\n', '', c, flags=re.S)
    c2 = c2.rstrip('\n') + '\n\n' + CSS
    if c2 != c:
        open(cp, 'w', encoding='utf-8').write(c2)
    print(f'menu-lavori: {cambiate} pagine aggiornate')


if __name__ == '__main__':
    main()
