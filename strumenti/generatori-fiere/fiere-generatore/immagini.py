# -*- coding: utf-8 -*-
"""Render degli stand nelle pagine fiere (13 ottobre 2026).

inject(html, path) -> html  aggiunge (o rimpiazza) sotto l'hero il render della pagina,
og:image/twitter:image dedicati e ImageObject nei dati strutturati. Idempotente.
Usato da lib.build() a ogni rigenerazione e da applica_immagini.py sulle pagine gia' pubblicate.
"""
import os, re, json, html as H
import dati_render as DR
SITE = 'https://danova-tech.com'
DIR = '/assets/img/stand/'
W, HH = 1600, 1063
_BY = {r[0]: r for r in DR.R}
MAP = {}  # path -> (file, alt, caption, lang)
for f, pages, _s, alt, cap in DR.R:
    for p in pages: MAP[p] = (f, alt, cap, 'it')
for p, f in DR.RIUSO.items():
    _, _, _, alt, cap = _BY[f]
    MAP.setdefault(p, (f, alt, cap, 'it'))
for p, (alt, cap) in DR.ESTERO.items():
    MAP[p] = ('stand-isola-legno-rovere', alt, cap, p.strip('/').split('/')[0])
# 14/10/2026: pagine EN e ZH per espositori stranieri (stessi render delle pagine IT, testi tradotti)
try:
    import dati_intl as _DI
    _P = {f['k']: {L: f"/{L}/{f[L]['slug']}/" for L in ('en', 'zh')} for f in _DI.FAIRS}
    _P.update({c['s']: {L: f"/{L}/{c[L]['slug']}/" for L in ('en', 'zh')} for c in _DI.CITIES})
    _P['guide'] = {'en': '/en/exhibiting-at-trade-fairs-in-italy/', 'zh': '/zh/italy-trade-fair-guide/'}
    for _k, (_f, _en, _zh) in _DI.IMG.items():
        MAP[_P[_k]['en']] = (_f, _en, _DI.CAP['en'], 'en')
        MAP[_P[_k]['zh']] = (_f, _zh, _DI.CAP['zh'], 'zh')
except ImportError:
    pass
CREDIT = {'it': 'Render di progetto Danova Tech', 'en': 'Danova Tech design render', 'de': 'Entwurfsrendering Danova Tech',
          'fr': 'Rendu de projet Danova Tech', 'es': 'Render de proyecto Danova Tech', 'zh': 'Danova Tech 设计效果图',
          'tr': 'Danova Tech proje görseli', 'ar': 'تصور تصميمي من Danova Tech'}
A, B = '<!--fr-foto-->', '<!--/fr-foto-->'
E = lambda s: H.escape(s, quote=True)

def url(f, kind=''):
    if kind == 'og': return f'{SITE}{DIR}og/{f}.jpg'
    return f'{SITE}{DIR}{f}{kind}.webp'

def figure(f, alt, cap):
    return (f'{A}<section class="fr-foto-sec"><div class="wrap"><figure class="fr-foto" data-rv="up">'
            f'<img src="{DIR}{f}.webp" srcset="{DIR}{f}-800.webp 800w, {DIR}{f}-1200.webp 1200w, {DIR}{f}.webp 1600w" '
            f'sizes="(max-width: 1240px) calc(100vw - 44px), 1196px" width="{W}" height="{HH}" alt="{E(alt)}" decoding="async">'
            f'<figcaption>{E(cap)}</figcaption></figure></div></section>{B}\n')

def image_object(f, alt, cap, lang):
    return {"@type": "ImageObject", "@id": url(f) + "#img", "url": url(f), "contentUrl": url(f),
            "width": W, "height": HH, "caption": cap, "description": alt, "inLanguage": lang,
            "creditText": CREDIT.get(lang, CREDIT['en']), "copyrightNotice": "© Danova Tech",
            "license": SITE + "/termini/#proprieta-intellettuale" if lang == "it" else SITE + "/en/terms/#intellectual-property", "acquireLicensePage": SITE + "/contatti/" if lang == "it" else SITE + "/en/contact/",
            "creator": {"@id": SITE + "/#organization"}, "thumbnailUrl": url(f, '-800')}

def inject(s, path):
    if path not in MAP: return s
    f, alt, cap, lang = MAP[path]
    # 1) figura sotto l'hero (rimpiazza quella vecchia)
    s = re.sub(re.escape(A) + r'.*?' + re.escape(B) + r'\n?', '', s, flags=re.S)
    m = re.search(r'<section class="pg-hero">.*?</section>\n?', s, re.S)
    if not m: return s
    s = s[:m.end()] + figure(f, alt, cap) + s[m.end():]
    # 2) og / twitter
    og = url(f, 'og')
    s = re.sub(r'(<meta property="og:image" content=")[^"]*(">)', lambda x: x.group(1) + og + x.group(2), s)
    s = re.sub(r'(<meta name="twitter:image" content=")[^"]*(">)', lambda x: x.group(1) + og + x.group(2), s)
    s = re.sub(r'<meta property="og:image:alt" content="[^"]*">\n', '', s)
    s = re.sub(r'(<meta property="og:image:height" content="[^"]*">\n)', lambda x: x.group(1) + f'<meta property="og:image:alt" content="{E(alt)}">\n', s, 1)
    # 3) JSON-LD
    m = re.search(r'(<script type="application/ld\+json">)(.*?)(</script>)', s, re.S)
    if m:
        try: g = json.loads(m.group(2))
        except ValueError: return s
        nodes = g.get('@graph', [g])
        io = image_object(f, alt, cap, lang)
        nodes = [n for n in nodes if not (n.get('@type') == 'ImageObject' and str(n.get('@id', '')).startswith(SITE + DIR))]
        for n in nodes:
            t = n.get('@type'); tt = t if isinstance(t, list) else [t]
            if any(x in ('WebPage', 'CollectionPage', 'AboutPage') for x in tt):
                n['primaryImageOfPage'] = {"@id": io['@id']}
                n['image'] = {"@id": io['@id']}
            if any(x in ('Service', 'Article', 'BlogPosting', 'HowTo') for x in tt):
                n['image'] = {"@id": io['@id']}
        nodes.append(io)
        if '@graph' in g: g['@graph'] = nodes
        else: g = {"@context": "https://schema.org", "@graph": nodes}
        s = s[:m.start(2)] + '\n' + json.dumps(g, ensure_ascii=False, indent=2) + '\n' + s[m.end(2):]
    return s

def tutte():
    """[(path, file, alt, caption, lang)] per sitemap immagini e galleria"""
    return [(p, f, a, c, l) for p, (f, a, c, l) in MAP.items()]
