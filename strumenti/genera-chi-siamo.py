#!/usr/bin/env python3
"""Genera /chi-siamo/ (pagina "Chi siamo", 8/11/2026) usando /contatti/ come modello grafico.
Solo fatti gia' dichiarati nel sito: numeri, sedi, metodo, P.IVA. Uso:
    python3 strumenti/genera-chi-siamo.py
Poi: python3 strumenti/ottimizza-seo.py (aggiunge il link nel footer delle altre pagine)."""
import os, re, json
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
URL = 'https://danovastand.com/chi-siamo/'
TITLE = 'Chi siamo: allestitori di stand fieristici | Danova Stand'
DESC = ('Danova Stand, marchio di Danova Tech: oltre 300 stand montati in Italia e in 11 paesi europei, '
        'team con più di 20 anni in fiera. Sedi in Veneto e Lombardia.')
H1 = 'Chi siamo: allestitori di stand fieristici, dal Veneto all\'Europa'
OGIMG = 'https://danovastand.com/assets/img/stand/og/stand-medio-32-mq.jpg'
TODAY = '2026-11-08'

FAQ = [
 ("Chi c'è dietro Danova Stand?",
  "Danova Stand è il marchio di Danova Tech (P.IVA IT05369890263) dedicato a stand fieristici e allestimenti. "
  "La sede legale è in Via Rigole 48 a Mansuè (TV); il team lavora in fiera da più di 20 anni e ha montato oltre 300 stand."),
 ("Danova Stand e Danova Tech sono la stessa azienda?",
  "Sì. Danova Tech è la società; Danova Stand è il suo marchio per stand fieristici, allestimenti di eventi, negozi e mostre. "
  "Siti web e software restano su danova-tech.com."),
 ("Dove si trova Danova Stand?",
  "Sede legale a Mansuè (TV), magazzini e produzione a Fontanelle (TV) e Trumello (PV), uffici a Trumello e a Vermezzo con Zelo (MI), "
  "a pochi minuti da Fiera Milano Rho. Lavoriamo in tutte le fiere italiane e in Europa."),
 ("Producete voi gli stand?",
  "Il progetto e il coordinamento sono nostri. Strutture e arredi in legno li realizzano laboratori partner con cui lavoriamo da anni, "
  "il montaggio squadre partner coordinate da un unico capocantiere. Il cliente ha un solo referente e un solo preventivo."),
 ("In quali lingue lavorate?",
  "In italiano, inglese, tedesco, francese e spagnolo: seguiamo anche aziende estere che espongono nelle fiere italiane."),
]

MAIN = f'''<main id="main">
<div class="wrap pg-crumbs">
  <a href="/">Home</a><em>/</em>Chi siamo
</div>
<section class="pg-hero"><div class="wrap"><div class="eyebrow mono">Chi siamo</div><h1>{H1}</h1><p class="lead"><b>Danova Stand</b> è il marchio di Danova Tech dedicato agli stand fieristici e agli allestimenti. Progettiamo, facciamo produrre, trasportiamo e montiamo stand chiavi in mano, preallestiti, modulari e su misura, da 9 a oltre 300 mq: oltre 300 stand montati in Italia e in 11 paesi europei, con un team che lavora in fiera da più di 20 anni.</p><div class="hero-cta"><a href="/contatti/" class="btn btn-p"><span class="lbl">Parla con noi</span></a> <a href="/progetti-stand-fieristici/" class="btn btn-g"><span class="lbl">Guarda i progetti</span></a></div></div></section>

<section id="numeri"><div class="wrap"><div class="sec-head"><div class="eyebrow mono">In breve</div><h2 class="title">Danova Stand in sei punti</h2><p class="lead">Dati reali del nostro lavoro, gli stessi che trovi nel resto del sito.</p></div>
<div class="pg-cards">
<article class="pg-card"><h3>Oltre 300 stand</h3><p>Montati in Italia e all'estero, soprattutto a Veronafiere, Fiera Milano, BolognaFiere, Rimini e Parma.</p></article>
<article class="pg-card"><h3>Più di 20 anni in fiera</h3><p>L'esperienza del team in progettazione, cantiere e regolamenti tecnici dei quartieri fieristici.</p></article>
<article class="pg-card"><h3>11 paesi europei</h3><p>Stand prodotti in Italia e montati all'estero, con trasporto e squadre gestiti da noi. <a href="/allestimenti-fieristici-estero/">Fiere all'estero</a>.</p></article>
<article class="pg-card"><h3>Materiali in Classe 1</h3><p>Materiali certificati per la reazione al fuoco e impianto elettrico con <a href="/guide/dichiarazione-di-conformita-stand/">dichiarazione di conformità</a>.</p></article>
<article class="pg-card"><h3>Un solo referente</h3><p>Dal primo contatto allo smontaggio: un solo preventivo voce per voce invece di cinque fornitori da coordinare.</p></article>
<article class="pg-card"><h3>Cinque lingue</h3><p>Italiano, inglese, tedesco, francese e spagnolo, per aziende italiane ed estere.</p></article>
</div></div></section>

<section id="come-lavoriamo"><div class="wrap"><div class="sec-head"><div class="eyebrow mono">Metodo</div><h2 class="title">Come lavoriamo</h2></div><div class="pg-testo">
<p>Progettiamo noi ogni stand, sul marchio del cliente e sul regolamento tecnico della fiera. Strutture, pareti e arredi in legno li realizzano laboratori partner con cui lavoriamo da anni; trasporto e montaggio li gestiamo noi, con trasportatori e squadre partner di fiducia e un unico capocantiere in fiera.</p>
<p>Grafica, impianto elettrico, luci, moquette, ledwall e pratiche con l'ente fiera fanno parte dello stesso progetto. Tra una fiera e l'altra lo stand può restare nei nostri magazzini di Fontanelle (TV) e Trumello (PV), pronto per essere riconfigurato.</p>
</div>
<ol class="pg-passi">
<li><b>Ascolto e sopralluogo.</b> Rispondiamo entro 24 ore lavorative; il sopralluogo in azienda o in videochiamata è gratuito.</li>
<li><b>Planimetria e regolamento.</b> Verifichiamo area, altezze consentite e regole tecniche della fiera prima di disegnare.</li>
<li><b>Progetto 3D e preventivo voce per voce.</b> Ogni componente con il suo prezzo: <a href="/quanto-costa-uno-stand-fieristico/">quanto costa uno stand</a>.</li>
<li><b>Produzione, montaggio, smontaggio.</b> Un solo capocantiere, consegna nei tempi dell'ente fiera e magazzino per le fiere successive.</li>
</ol></div></section>

<section id="cosa-facciamo"><div class="wrap"><div class="sec-head"><div class="eyebrow mono">Servizi</div><h2 class="title">Cosa facciamo</h2></div>
<div class="pg-altri">
<a href="/stand-fieristici-su-misura/">Stand su misura</a><a href="/stand-modulari/">Stand modulari</a><a href="/stand-preallestiti/">Stand preallestiti</a><a href="/noleggio-stand-fieristici/">Noleggio stand</a><a href="/progettazione-stand-fieristici/">Progettazione e render 3D</a><a href="/montaggio-stand-fieristici/">Montaggio stand</a><a href="/grafica-per-stand-fieristici/">Grafica per stand</a><a href="/ledwall-e-illuminazione-stand/">Ledwall e illuminazione</a><a href="/allestimenti-eventi/">Allestimenti per eventi</a><a href="/allestimento-negozi/">Allestimento negozi</a><a href="/allestimento-mostre/">Allestimento mostre</a><a href="/stand-pubblicitari/">Stand pubblicitari</a>
</div></div></section>

<section id="sedi"><div class="wrap"><div class="sec-head"><div class="eyebrow mono">Dove siamo</div><h2 class="title">Sedi, magazzini e dati aziendali</h2></div>
<div class="pg-cards">
<article class="pg-card"><h3>Sede legale</h3><p>Danova Tech — marchio Danova Stand<br>Via Rigole 48, 31040 Mansuè (TV), Italia<br>P.IVA IT05369890263</p></article>
<article class="pg-card"><h3>Magazzini e produzione</h3><p>Fontanelle (TV) e Trumello (PV): qui gli stand vengono preparati e conservati tra una fiera e l'altra.</p></article>
<article class="pg-card"><h3>Uffici</h3><p>Trumello (PV) e Vermezzo con Zelo (MI), a pochi minuti da Fiera Milano Rho.</p></article>
<article class="pg-card"><h3>Contatti</h3><p><a href="tel:+393884706887">+39 388 470 6887</a> · lun-ven 9:00-18:00<br><a href="mailto:info@danova-tech.com">info@danova-tech.com</a><br><a href="https://maps.app.goo.gl/gPgYPeA5Rtc12wve8" rel="noopener">Scheda su Google Maps</a></p></article>
</div></div></section>

<section id="faq"><div class="wrap"><div class="sec-head"><div class="eyebrow mono">Domande frequenti</div><h2 class="title">Domande su Danova Stand</h2></div>
<ul class="pg-lista">
''' + '\n'.join(f'<li><b>{q}</b> {a}</li>' for q, a in FAQ) + '''
</ul></div></section>
[[CTA]]
<section><div class="wrap"><div class="sec-head"><h2 class="title">Pagine collegate</h2></div><div class="pg-altri"><a href="/contatti/">Contatti</a><a href="/progetti-stand-fieristici/">Progetti di stand</a><a href="/calendario-fiere/">Calendario fiere</a><a href="/guide/come-scegliere-un-allestitore-fieristico/">Come scegliere un allestitore</a><a href="/termini/">Termini e condizioni d’uso</a></div></div></section>
</main>'''

def main():
    t = open(os.path.join(ROOT, 'contatti/index.html'), encoding='utf-8').read()
    cta = re.search(r'<section class="pg-cta" id="scrivici">.*?</section>', t, re.S).group(0)
    h = t
    h = re.sub(r'<main id="main">.*?</main>', lambda m: MAIN.replace('[[CTA]]', cta), h, flags=re.S)
    old_t = re.search(r'<title>(.*?)</title>', t).group(1)
    old_d = re.search(r'name="description" content="([^"]*)"', t).group(1)
    h = h.replace(f'<title>{old_t}</title>', f'<title>{TITLE}</title>')
    h = h.replace(old_d, DESC)
    h = h.replace('content="Contatti — Danova Stand"', 'content="Chi siamo — Danova Stand"')
    h = h.replace('https://danovastand.com/assets/img/og-cover.jpg', OGIMG)
    # hreflang: la pagina esiste solo in italiano
    h = re.sub(r'<link rel="alternate" hreflang="(en|de|fr|es)"[^>]*>\n', '', h)
    h = h.replace('https://danovastand.com/contatti/', URL)
    # selettore lingue -> home delle lingue
    homes = {'en': '/en/exhibition-stand-builder-italy/', 'de': '/de/messebau-italien/',
             'fr': '/fr/standiste-salon-italie/', 'es': '/es/montaje-stands-feriales-italia/'}
    h = h.replace('href="/contatti/" hreflang="it" aria-current="page"', 'href="/chi-siamo/" hreflang="it" aria-current="page"')
    for lg, u in homes.items():
        h = re.sub(rf'href="/{lg}/[^"]*" hreflang="{lg}"', f'href="{u}" hreflang="{lg}"', h)
    # menu: "Contatti" punta alla pagina contatti, non al modulo
    h = h.replace('<a href="#dt-scrivi">Contatti</a>', '<a href="/contatti/">Contatti</a>')
    # footer: Chi siamo
    h = h.replace('<i>·</i><a href="/contatti/">Contatti</a><i>·</i>', '<i>·</i><a href="/chi-siamo/" aria-current="page">Chi siamo</a><i>·</i><a href="/contatti/">Contatti</a><i>·</i>')
    # JSON-LD
    m = re.search(r'<script type="application/ld\+json">(.*?)</script>', h, re.S)
    j = json.loads(m.group(1))
    g = []
    for it in j['@graph']:
        if it.get('@type') == 'ContactPage':
            it = {'@type': 'AboutPage', '@id': URL + '#webpage', 'url': URL, 'name': TITLE, 'description': DESC,
                  'inLanguage': 'it', 'isPartOf': {'@id': 'https://danovastand.com/#website'},
                  'publisher': {'@id': 'https://danovastand.com/#organization'},
                  'about': {'@id': 'https://danovastand.com/#organization'},
                  'mainEntity': {'@id': 'https://danovastand.com/#organization'},
                  'primaryImageOfPage': {'@type': 'ImageObject', 'url': OGIMG},
                  'breadcrumb': {'@id': URL + '#breadcrumb'},
                  'datePublished': TODAY, 'dateModified': TODAY}
        elif it.get('@type') == 'BreadcrumbList':
            it['@id'] = URL + '#breadcrumb'
            it['itemListElement'][1].update({'name': 'Chi siamo', 'item': URL})
        g.append(it)
    g.append({'@type': 'FAQPage', '@id': URL + '#faq', 'inLanguage': 'it', 'mainEntity': [
        {'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in FAQ]})
    j['@graph'] = g
    h = h.replace(m.group(0), '<script type="application/ld+json">\n' + json.dumps(j, ensure_ascii=False, indent=2) + '\n</script>')
    os.makedirs(os.path.join(ROOT, 'chi-siamo'), exist_ok=True)
    open(os.path.join(ROOT, 'chi-siamo/index.html'), 'w', encoding='utf-8').write(h)
    # sitemap
    sp = os.path.join(ROOT, 'sitemap.xml'); s = open(sp, encoding='utf-8').read()
    if URL not in s:
        s = s.replace('</urlset>', f'  <url>\n    <loc>{URL}</loc>\n    <lastmod>{TODAY}</lastmod>\n  </url>\n</urlset>')
        open(sp, 'w', encoding='utf-8').write(s)
    print('ok chi-siamo')
main()
