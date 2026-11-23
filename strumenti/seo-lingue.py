#!/usr/bin/env python3
"""SEO in tutte le lingue: nelle pagine principali di ogni lingua estera aggiunge
1) la fascia "Stand che abbiamo costruito" con foto VERE (link alla scheda dello stand nell'hub dei lavori);
2) il blocco "Come scegliere un allestitore: 5 verifiche" + domanda "Quali sono i migliori allestitori in Italia/Europa?",
   la stessa domanda anche nello schema FAQPage (per Google e per gli assistenti AI che citano le pagine).

    python3 strumenti/seo-lingue.py

Idempotente: blocco <!--ds-seo-lingue-->...<!--/ds-seo-lingue--> prima di <section id="faq">.
Testi in strumenti/testi_lingue_seo.py, foto da strumenti/galleria_stand.py.
Le pagine italiane hanno la fascia da foto-vere-pagine.py e la guida da ottimizza-allestitori.py.
Rilanciarlo dopo migra-da-danovatech.py e i generatori delle lingue, prima di ottimizza-geo.py.
"""
import os, re, sys, json, html
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from galleria_stand import GALLERIA
from testi_lingue_seo import T

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG = '/assets/img/lavori/'
G = {g['slug']: g for g in GALLERIA}
e = lambda s: html.escape(s, quote=True)

ITALIA = [('asfour-crystal', 1), ('fabtech', 1), ('applied-nutrition', 1), ('telangana-tourism', 1)]
EUROPA = [('polska-poland-tastes-good', 2), ('fabtech', 1), ('telangana-tourism', 2), ('arama-benet', 1)]
MILANO = [('asfour-crystal', 2), ('talos-performance', 1), ('fabtech', 4), ('gsb-helmets', 1)]
VERONA = [('polska-poland-tastes-good', 2), ('arama-benet', 1), ('plastona', 1), ('topsun', 1)]
BOLOGNA = [('applied-nutrition', 1), ('asfour-crystal', 3), ('triveni-turbines-refurb', 1), ('polska-poland-tastes-good', 4)]
CITTA = [('asfour-crystal', 1), ('thundervolt', 1), ('applied-nutrition', 3), ('arama-benet', 2)]
INDIA = [('telangana-tourism', 1), ('uttar-pradesh-tourism', 2), ('triveni-turbines-refurb', 1), ('rajasthan-tourism', 1)]

PAGINE = {
    'en/exhibition-stand-builder-italy': ITALIA, 'en/exhibition-stand-builder-europe': EUROPA,
    'en/exhibiting-at-trade-fairs-in-italy': ITALIA, 'en/exhibition-stand-builder-milan': MILANO,
    'en/exhibition-stand-builder-verona': VERONA, 'en/exhibition-stand-builder-bologna': BOLOGNA,
    'en/exhibition-stand-builder-rimini': CITTA, 'en/exhibition-stand-builder-parma': VERONA,
    'en/exhibition-stand-builder-vicenza': CITTA, 'en/exhibition-stand-builder-florence': CITTA,
    'en/exhibition-stand-builder-riva-del-garda': CITTA,
    'en/exhibition-stand-builder-for-indian-companies': INDIA, 'en/exhibition-stand-builder-for-pakistani-companies': ITALIA,
    'en/exhibition-stand-builder-for-bangladeshi-companies': ITALIA, 'en/exhibition-stand-builder-for-chinese-companies': ITALIA,
    'de/messebau-italien': ITALIA, 'de/messebau-mailand': MILANO, 'de/messebau-verona': VERONA, 'de/messebau-bologna': BOLOGNA,
    'fr/standiste-salon-italie': ITALIA, 'es/montaje-stands-feriales-italia': ITALIA,
    'nl/standbouw-italie': ITALIA, 'nl/standbouw-beurzen-duitsland-europa': EUROPA,
    'tr/italya-fuar-standi': ITALIA, 'ar/italy-exhibition-stand': ITALIA,
    'zh/italy-exhibition-stand': ITALIA, 'zh/europe-exhibition-stand': EUROPA, 'zh/milan-exhibition-stand': MILANO,
    'zh-hant/italy-exhibition-stand': ITALIA, 'zh-hant/europe-exhibition-stand': EUROPA, 'zh-hant/milan-exhibition-stand': MILANO,
    'ur/italy-exhibition-stand': INDIA, 'ur/europe-exhibition-stand': EUROPA,
    'hi/italy-exhibition-stand': INDIA, 'hi/europe-exhibition-stand': EUROPA,
}
for l in 'pt sv pl cs hu ro bg hr el sq ru uk he fa bn pa gu ta ja ko id ms vi th'.split():
    PAGINE[f'{l}/europe-exhibition-stand'] = EUROPA

HUB = {'fr': '/fr/realisations/'}
HUB_DEF = '/en/projects/'

STILE = ('<style>.dsfv-g{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin-top:26px}'
         '.dsfv-g a{position:relative;display:block;border-radius:var(--r-md);overflow:hidden;border:1px solid var(--line);background:var(--panel)}'
         '.dsfv-g img{width:100%;height:auto;aspect-ratio:4/3;object-fit:cover;transition:transform .6s var(--ease)}'
         '.dsfv-g a:hover img{transform:scale(1.04)}'
         '.dsfv-g figcaption{position:absolute;left:0;right:0;bottom:0;padding:22px 12px 9px;font-size:13px;color:#fff;'
         'background:linear-gradient(transparent,rgba(0,0,0,.78))}'
         '.dsfv-cta{margin-top:22px;text-align:center}'
         '.dsal-l{margin:18px 0 0;padding-inline-start:20px}.dsal-l li{margin-bottom:10px}'
         '.dsal-q h3{font-family:"Sora",sans-serif;font-size:1.12rem;color:#fff;margin:26px 0 6px}'
         '@media (max-width:900px){.dsfv-g{grid-template-columns:repeat(2,1fr)}}</style>')

RE_BLOCCO = re.compile(r'<!--ds-seo-lingue-->.*?<!--/ds-seo-lingue-->\n?', re.S)


def lingua(s):
    m = re.search(r'<html[^>]*\blang="([^"]+)"', s)
    return m.group(1) if m else 'en'


def blocco(lg, t, scelte):
    hub = HUB.get(lg, HUB_DEF); figs = ''
    for slug, n in scelte:
        g = G[slug]; f = g['foto'][n - 1]
        nome, w, h = f[0], f[1], f[2]
        vista = f[3].get(lg[:2]) or f[3]['en']
        alt = f'Stand {g["nome"]["en"]} — {t["da"]}' + (f': {vista}' if lg[:2] in ('it', 'fr', 'en') else '')
        figs += (f'<a href="{hub}#stand-{slug}"><figure style="margin:0"><img src="{IMG}{nome}-800.webp" '
                 f'srcset="{IMG}{nome}-800.webp 800w, {IMG}{nome}-1200.webp 1200w" sizes="(max-width:900px) 50vw, 300px" '
                 f'width="{w}" height="{h}" alt="{e(alt)}" loading="lazy" decoding="async">'
                 f'<figcaption>{e(g["nome"]["en"])}</figcaption></figure></a>')
    voci = ''.join(f'<li><b>{e(b)}</b>: {e(x)}</li>' for b, x in t['v'])
    return (f'<!--ds-seo-lingue--><section id="stand-realizzati">{STILE}<div class="wrap">'
            f'<div class="sec-head"><h2 class="title" data-rv="up">{e(t["tit"])} <span class="grad">{e(t["grad"])}</span></h2></div>'
            f'<div class="pg-testo" data-rv="up"><p>{e(t["intro"])}</p></div>'
            f'<div class="dsfv-g">{figs}</div>'
            f'<p class="dsfv-cta"><a href="{hub}" class="btn btn-g"><span class="lbl">{e(t["tutti"])}</span></a></p>'
            f'</div></section>\n'
            f'<section id="scegliere-allestitore"><div class="wrap">'
            f'<div class="sec-head"><h2 class="title" data-rv="up">{e(t["h"])} <span class="grad">{e(t["g"])}</span></h2></div>'
            f'<div class="pg-testo dsal-q" data-rv="up"><ol class="dsal-l">{voci}</ol>'
            f'<h3>{e(t["q"])}</h3><p>{e(t["a"])}</p>'
            f'<p>{e(t["chi"])} <a href="{hub}" style="text-decoration:underline">{e(t["lav"])}</a>.</p></div>'
            f'</div></section><!--/ds-seo-lingue-->\n')


def aggiungi_faq(s, t):
    """Aggiunge la domanda allo schema FAQPage (se non c'e' gia')."""
    if json.dumps(t['q'], ensure_ascii=False) in s or t['q'] in s.split('<section id="faq"')[0].split('</head>')[0]:
        return s
    m = re.search(r'"@type":\s*"FAQPage".*?"mainEntity":\s*\[', s, re.S)
    if not m:
        return s
    q = json.dumps({'@type': 'Question', 'name': t['q'], 'acceptedAnswer': {'@type': 'Answer', 'text': t['a']}}, ensure_ascii=False)
    return s[:m.end()] + q + ',' + s[m.end():]


def main():
    n = 0
    for rel, scelte in PAGINE.items():
        p = os.path.join(ROOT, rel, 'index.html')
        if not os.path.exists(p):
            print('  manca', rel); continue
        s = open(p, encoding='utf-8').read()
        lg = lingua(s)
        t = T.get(lg) or T.get(lg[:2])
        if not t or '<section id="faq"' not in s:
            print('  saltata', rel, lg); continue
        x = RE_BLOCCO.sub('', s)
        x = x.replace('<section id="faq"', blocco(lg, t, scelte) + '<section id="faq"', 1)
        x = aggiungi_faq(x, t)
        for b in re.findall(r'<script type="application/ld\+json">(.*?)</script>', x, re.S):
            json.loads(b)  # se lo schema non e' valido lo script si ferma qui
        if x != s:
            open(p, 'w', encoding='utf-8').write(x); n += 1
    print(f'seo-lingue: {n} pagine aggiornate')


if __name__ == '__main__':
    main()
