#!/usr/bin/env python3
"""Fascia "Stand che abbiamo costruito" con foto VERE nelle pagine principali (home, servizi, tipologie, settori).

    python3 strumenti/foto-vere-pagine.py

Perche': quasi tutte le pagine mostrano solo render. Google (E-E-A-T, Google Immagini) e gli assistenti AI
premiano le prove concrete di lavori fatti. Ogni foto porta alla scheda dello stand nell'hub dei lavori.
Idempotente: blocco <!--ds-foto-vere-->...<!--/ds-foto-vere--> inserito subito prima di <section id="faq">.
Foto e testi presi da strumenti/galleria_stand.py (stesse foto della galleria /lavori/).
Le pagine nelle altre lingue le gestisce seo-lingue.py.
Per cambiare le foto di una pagina modifica PAGINE qui sotto: (slug stand, numero foto).
"""
import os, re, sys, html
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from galleria_stand import GALLERIA

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG = '/assets/img/lavori/'
G = {g['slug']: g for g in GALLERIA}

# pagina -> (lingua, foto). Le foto sono scelte per somiglianza con l'argomento della pagina,
# senza attribuire fiere o metrature che non conosciamo.
PAGINE = {
    'index.html': ('it', [('asfour-crystal', 1), ('fabtech', 1), ('applied-nutrition', 1), ('telangana-tourism', 1)]),
    'servizi/allestimenti-fieristici/index.html': ('it', [('fabtech', 1), ('asfour-crystal', 2), ('talos-performance', 1), ('polska-poland-tastes-good', 2)]),
    'stand-fieristici-su-misura/index.html': ('it', [('asfour-crystal', 3), ('arama-benet', 1), ('telangana-tourism', 2), ('triveni-turbines-refurb', 1)]),
    'stand-a-isola/index.html': ('it', [('asfour-crystal', 1), ('arama-benet', 2), ('talos-performance', 2), ('thundervolt', 1)]),
    'stand-modulari/index.html': ('it', [('plastona', 1), ('gsb-helmets', 1), ('hd-helmets', 1), ('applied-nutrition', 4)]),
    'stand-preallestiti/index.html': ('it', [('polska-poland-tastes-good', 2), ('gsb-helmets', 2), ('plastona', 2), ('moto-tron-racing', 1)]),
    'progettazione-stand-fieristici/index.html': ('it', [('fabtech', 1), ('arama-benet', 1), ('telangana-tourism', 3), ('triveni-turbines-refurb', 2)]),
    'montaggio-stand-fieristici/index.html': ('it', [('asfour-crystal', 4), ('thundervolt', 1), ('applied-nutrition', 3), ('wrp-wind-trading', 1)]),
    'stand-fieristici-food-e-vino/index.html': ('it', [('polska-poland-tastes-good', 2), ('applied-nutrition', 2), ('arama-benet', 1), ('applied-nutrition', 1)]),
    'stand-fieristici-meccanica-e-industria/index.html': ('it', [('fabtech', 1), ('triveni-turbines-refurb', 1), ('topsun', 1), ('fabtech', 4)]),
    'stand-fieristici-agricoltura/index.html': ('it', [('topsun', 1), ('plastona', 1), ('polska-poland-tastes-good', 2), ('triveni-turbines-refurb', 2)]),
    'stand-fieristici-moda-e-calzature/index.html': ('it', [('asfour-crystal', 2), ('gsb-helmets', 1), ('wrp-wind-trading', 3), ('hd-helmets', 2)]),
    'stand-eicma/index.html': ('it', [('talos-performance', 1), ('thundervolt', 1), ('gsb-helmets', 1), ('moto-tron-racing', 1)]),
    'stand-bit-milano/index.html': ('it', [('telangana-tourism', 1), ('uttar-pradesh-tourism', 2), ('rajasthan-tourism', 1), ('telangana-tourism', 2)]),
    'stand-fitur/index.html': ('it', [('telangana-tourism', 1), ('uttar-pradesh-tourism', 2), ('rajasthan-tourism', 1), ('telangana-tourism', 3)]),
    'chi-siamo/index.html': ('it', [('asfour-crystal', 1), ('fabtech', 1), ('polska-poland-tastes-good', 2), ('telangana-tourism', 1)]),
    'allestimenti-fieristici-estero/index.html': ('it', [('telangana-tourism', 1), ('polska-poland-tastes-good', 2), ('fabtech', 1), ('arama-benet', 1)]),
}

TXT = {
    'it': dict(hub='/lavori/', tit='Stand che abbiamo costruito:', grad='foto vere, non render.',
               intro='Alcuni stand progettati, costruiti e montati da noi in fiera. Clicca una foto per la scheda dello stand.',
               tutti='Vedi tutti i lavori realizzati', stand='Stand', da='realizzato da Danova Stand'),
    'en': dict(hub='/en/projects/', tit='Stands we have built:', grad='real photos, not renders.',
               intro='A few of the stands we designed, built and installed at trade fairs. Click a photo to see the stand.',
               tutti='See all our projects', stand='Stand', da='built by Danova Stand'),
    'fr': dict(hub='/fr/realisations/', tit='Stands que nous avons construits :', grad='vraies photos, pas des rendus.',
               intro="Quelques stands conçus, construits et montés par nos équipes en salon. Cliquez sur une photo pour voir le stand.",
               tutti='Voir toutes nos réalisations', stand='Stand', da='réalisé par Danova Stand'),
}

STILE = ('<style>.dsfv-g{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin-top:26px}'
         '.dsfv-g a{position:relative;display:block;border-radius:var(--r-md);overflow:hidden;border:1px solid var(--line);background:var(--panel)}'
         '.dsfv-g img{width:100%;height:auto;aspect-ratio:4/3;object-fit:cover;transition:transform .6s var(--ease)}'
         '.dsfv-g a:hover img{transform:scale(1.04)}'
         '.dsfv-g figcaption{position:absolute;left:0;right:0;bottom:0;padding:22px 12px 9px;font-size:13px;color:#fff;'
         'background:linear-gradient(transparent,rgba(0,0,0,.78))}'
         '.dsfv-cta{margin-top:22px;text-align:center}'
         '@media (max-width:900px){.dsfv-g{grid-template-columns:repeat(2,1fr)}}</style>')

RE_BLOCCO = re.compile(r'<!--ds-foto-vere-->.*?<!--/ds-foto-vere-->\n?', re.S)
e = lambda s: html.escape(s, quote=True)


def blocco(lang, scelte):
    t = TXT[lang]; figs = ''
    for slug, n in scelte:
        g = G[slug]; f = g['foto'][n - 1]
        nome, w, h, vista = f[0], f[1], f[2], f[3][lang]
        alt = f'{t["stand"]} {g["nome"][lang]} {t["da"]}: {vista}'
        figs += (f'<a href="{t["hub"]}#stand-{slug}"><figure style="margin:0"><img src="{IMG}{nome}-800.webp" '
                 f'srcset="{IMG}{nome}-800.webp 800w, {IMG}{nome}-1200.webp 1200w" sizes="(max-width:900px) 50vw, 300px" '
                 f'width="{w}" height="{h}" alt="{e(alt)}" loading="lazy" decoding="async">'
                 f'<figcaption>{e(g["nome"][lang])}</figcaption></figure></a>')
    return (f'<!--ds-foto-vere--><section id="stand-realizzati">{STILE}<div class="wrap">'
            f'<div class="sec-head"><h2 class="title" data-rv="up">{e(t["tit"])} <span class="grad">{e(t["grad"])}</span></h2></div>'
            f'<div class="pg-testo" data-rv="up"><p>{e(t["intro"])}</p></div>'
            f'<div class="dsfv-g">{figs}</div>'
            f'<p class="dsfv-cta"><a href="{t["hub"]}" class="btn btn-g"><span class="lbl">{e(t["tutti"])} →</span></a></p>'
            f'</div></section><!--/ds-foto-vere-->\n')


def main():
    n = 0
    for rel, (lang, scelte) in PAGINE.items():
        p = os.path.join(ROOT, rel)
        if not os.path.exists(p):
            print('  manca', rel); continue
        s = open(p, encoding='utf-8').read()
        if '<section id="faq"' not in s:
            print('  senza FAQ, saltata', rel); continue
        x = RE_BLOCCO.sub('', s)
        x = x.replace('<section id="faq"', blocco(lang, scelte) + '<section id="faq"', 1)
        if x != s:
            open(p, 'w', encoding='utf-8').write(x); n += 1
    print(f'foto-vere-pagine: {n} pagine aggiornate')


if __name__ == '__main__':
    main()
