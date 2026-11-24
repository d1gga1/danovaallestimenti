#!/usr/bin/env python3
"""24/11/2026: menu, pulsante e footer in olandese su tutte le pagine nl/ (il modello aveva testi inglesi).
Rilanciare dopo aver rigenerato pagine nl/.  Uso: python3 strumenti/fix-chrome-nl.py"""
import glob, os, re
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
NAV_OLD = re.compile(r'(<a href="/nl/projecten/" class="nav-lavori" data-ds="lavori"[^>]*>Ons werk</a>)\s*<a href="/en/exhibition-stand-builder-italy/">Stand builder Italy</a>\s*<a href="/en/exhibiting-at-trade-fairs-in-italy/">Trade fairs in Italy</a>\s*<a href="/en/exhibition-stand-builder-europe/">Europe</a>\s*<a href="#richiesta">Contact</a>')
NAV_NEW = r'\1 <a href="/nl/standbouw-italie/">Standbouw Italië</a> <a href="/nl/standbouw-beurzen-duitsland-europa/">Standbouw Europa</a> <a href="#richiesta">Contact</a>'
R = [
 ('<a href="/en/exhibition-stand-builder-italy/" class="brand"', '<a href="/nl/standbouw-italie/" class="brand"'),
 ('<span class="lbl">Let’s talk</span>', '<span class="lbl">Neem contact op</span>'),
 ('<p>Turnkey exhibition stands: 3D design, production, transport, installation and dismantling, in Italy and across Europe.</p>',
  '<p>Beursstands volledig verzorgd: 3D-ontwerp, productie, transport, opbouw en afbouw, in Italië en in heel Europa.</p>'),
 ('<h5>Stands</h5><ul> <li><a href="/en/exhibition-stand-builder-italy/">Exhibition stand builder Italy</a></li>',
  '<h5>Standbouw</h5><ul> <li><a href="/nl/standbouw-italie/">Standbouw Italië</a></li> <li><a href="/nl/standbouw-beurzen-duitsland-europa/">Standbouw in Europa</a></li>'),
 ('<li><a href="/en/exhibiting-at-trade-fairs-in-italy/">Exhibiting at trade fairs in Italy</a></li>', '<li><a href="/en/exhibiting-at-trade-fairs-in-italy/">Exposeren op beurzen in Italië</a></li>'),
 ('>Stand builder Milan<', '>Standbouw Milaan<'), ('>Stand builder Verona<', '>Standbouw Verona<'),
 ('>Stand builder Bologna<', '>Standbouw Bologna<'), ('>Stand builder Rimini<', '>Standbouw Rimini<'),
 ('>Stand builder Parma<', '>Standbouw Parma<'), ('<h5>Trade fairs</h5>', '<h5>Beurzen</h5>'),
 ('<li>Warehouses: Fontanelle (TV) · Trumello (PV)<br>Offices: Trumello (PV) · Vermezzo con Zelo (MI)</li>',
  '<li>Magazijnen: <bdi>Fontanelle (TV) · Trumello (PV)</bdi><br>Kantoren: <bdi>Trumello (PV) · Vermezzo con Zelo (MI)</bdi></li>'),
 ('<a href="/en/privacy/">Privacy Policy</a>', '<a href="/en/privacy/">Privacybeleid</a>'),
 ('<a href="/en/cookie-policy/">Cookie Policy</a>', '<a href="/en/cookie-policy/">Cookiebeleid</a>'),
 ('<a href="/en/terms/">Terms of use</a>', '<a href="/en/terms/">Gebruiksvoorwaarden</a>'),
]
n = 0
for p in glob.glob('nl/**/index.html', recursive=True):
    s = open(p, encoding='utf-8').read(); o = s
    s = NAV_OLD.sub(NAV_NEW, s)
    s = re.sub(r'\s*<li><a href="/en/exhibition-stand-builder-europe/">Stand builder Europe</a></li>', '', s)
    for a, b in R: s = s.replace(a, b)
    if s != o: open(p, 'w', encoding='utf-8').write(s); n += 1
print('pagine nl corrette:', n)
