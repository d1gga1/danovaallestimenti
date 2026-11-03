# -*- coding: utf-8 -*-
"""Mappa hreflang IT <-> EN <-> ZH per le pagine fiere e citta' (14 ottobre 2026).
merge(): usata da lib.build, cosi' anche rigenerando le pagine IT gli hreflang restano.
patch(): applica hreflang e selettore lingua alle pagine IT gia' pubblicate (idempotente)."""
import re
import dati_intl as DI
SITE = 'https://danova-tech.com'
ALTS = {}
def _add(it, en, zh):
    g = {'it': it, 'en': en, 'zh': zh, 'zh-hant': zh.replace('/zh/', '/zh-hant/', 1)}
    for p in g.values(): ALTS[p] = g
for f in DI.FAIRS:
    _add(f"/stand-{f['k']}/", f"/en/{f['en']['slug']}/", f"/zh/{f['zh']['slug']}/")
for c in DI.CITIES:
    _add(f"/allestimenti-fieristici-{c['s']}/", f"/en/{c['en']['slug']}/", f"/zh/{c['zh']['slug']}/")
_add('/guide/come-preparare-una-fiera/', '/en/exhibiting-at-trade-fairs-in-italy/', '/zh/italy-trade-fair-guide/')

# 22/10/2026: fiere europee (dati_2610_intl) e hub Europa
import dati_2610_intl as DX
for f in DX.FAIRS:
    _add(f"/stand-{f['k']}/", f"/en/{f['en']['slug']}/", f"/zh/{f['zh']['slug']}/")
_add('/allestimenti-fieristici-estero/', '/en/exhibition-stand-builder-europe/', '/zh/europe-exhibition-stand/')

def merge(path, alts, lang):
    base = dict(alts) if alts else {lang: path}
    if path in ALTS: base.update(ALTS[path])
    if 'zh' in base and 'zh-hant' not in base:  # 14/10/2026: cinese tradizionale
        base['zh-hant'] = base['zh'].replace('/zh/', '/zh-hant/', 1)
    return base if (alts or path in ALTS) else alts

CODE = {'it': 'IT', 'en': 'EN', 'zh': '简体', 'zh-hant': '繁體'}
HL = lambda l: {'zh': 'zh-Hans', 'zh-hant': 'zh-Hant'}.get(l, l)

def patch(s, path):
    """hreflang + og:locale:alternate + selettore lingua su una pagina gia' generata"""
    g = ALTS[path]
    lang = next(l for l, p in g.items() if p == path)
    hl = ''.join(f'<link rel="alternate" hreflang="{HL(l)}" href="{SITE}{p}">\n' for l, p in g.items())
    hl += f'<link rel="alternate" hreflang="x-default" href="{SITE}{g["it"]}">\n'
    lines = list(re.finditer(r'<link rel="alternate" hreflang="[^"]*" href="[^"]*">\n', s))
    if lines:
        s = s[:lines[0].start()] + hl + ''.join(
            s[a.end():b.start()] for a, b in zip(lines, lines[1:])) + s[lines[-1].end():]
    LOC = {'it': 'it_IT', 'en': 'en_US', 'zh': 'zh_CN', 'zh-hant': 'zh_TW'}
    s = re.sub(r'<meta property="og:locale:alternate" content="[^"]*">\n', '', s)
    s = re.sub(r'(<meta property="og:locale" content="[^"]*">\n)',
               lambda m: m.group(1) + ''.join(f'<meta property="og:locale:alternate" content="{LOC[l]}">\n' for l in g if l != lang), s, 1)
    CUR = ' aria-current="page"'
    mk = lambda ind: ''.join(f'\n{ind}<a href="{g[l]}" hreflang="{HL(l)}"{CUR if l == lang else ""}>{CODE[l]}</a>' for l in ('it', 'en', 'zh', 'zh-hant'))
    s = re.sub(r'<span class="lang-links">.*?</span>', lambda _: '<span class="lang-links">' + mk('        ') + '\n      </span>', s, 1, flags=re.S)
    s = re.sub(r'<div class="mob-lang-links">.*?</div>', lambda _: '<div class="mob-lang-links">' + mk('    ') + '\n  </div>', s, 1, flags=re.S)
    return s
