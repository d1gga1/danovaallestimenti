#!/usr/bin/env python3
"""Rinforzi dall'analisi Search Console del 24/11/2026 (strumenti/search-console/).

    python3 strumenti/ottimizza-search-console.py

Idempotente. Va lanciato dopo ottimizza-keyword.py e prima di attiva-area-privata.py / ottimizza-geo.py.
1. title, description (e og/twitter) piu' vicini alle query reali: EIMA, EICMA, Fieracavalli, calendari
   meccanica e turismo, idee, stand modulari, pagine inglesi delle citta';
2. blocchi di testo <!--ds-gsc-->...<!--/ds-gsc--> prima delle FAQ con le parole che mancavano
   (metalmeccanica, alberghiere, componibili, affitto, soppalcati, ecologici, enogastronomici, T.Gold,
   booth/contractor, ledwall all'estero, lavori in Germania...);
3. link alle pagine nuove nei box "Approfondisci" (pg-altri) o nei chips;
4. pagine nuove in sitemap.xml e llms.txt.
Fatti: strumenti/search-console/analisi-search-console-2026-11-24.md (risposte di Devid).
"""
import collections, html, json, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITO = 'https://danovastand.com'
e = lambda s: html.escape(s, quote=True)
stats = collections.Counter()

# ---------------------------------------------------------------- 1. title e description
META = {
    'stand-eima': ('Stand EIMA 2028 Bologna: render gratis in 48 ore | Danova Stand',
                   'Stand per EIMA International 2028 a BolognaFiere (novembre 2028, date da confermare): render 3D gratuito in 24-48 ore, stand chiavi in mano per macchine agricole, montaggio e pratiche con la fiera.', None),
    'stand-eicma': ('Stand EICMA 2027: render 3D gratis in 48 ore | Danova Stand',
                    'Stand per EICMA 2027 a Fiera Milano Rho (novembre 2027): render 3D gratuito in 24-48 ore, stand chiavi in mano per moto, caschi e accessori, montaggio e pratiche con la fiera.', None),
    'stand-fieracavalli': ('Stand Fieracavalli 2027: render gratis in 48 ore | Danova Stand',
                           'Stand per Fieracavalli 2027 a Veronafiere (4–7 novembre 2027): render 3D gratuito in 24-48 ore, stand chiavi in mano per allevamenti, selle e attrezzature, montaggio e pratiche.', None),
    'calendario-fiere-meccanica-e-industria': ('Fiere meccanica e metalmeccanica 2027: calendario',
                                               'Fiere della meccanica, metalmeccanica, lamiera e macchine utensili 2027 in Italia e in Europa: date, città e siti ufficiali. Esponi? Richiedi lo stand.',
                                               ('Fiere meccanica e industria 2027: il calendario.', 'Fiere meccanica, metalmeccanica e industria 2027: il calendario.')),
    'calendario-fiere-turismo': ('Fiere turismo e alberghiere 2027: calendario Italia ed Europa',
                                 'Fiere del turismo, alberghiere e dell\'ospitalità 2027 in Italia e in Europa: date, città e siti ufficiali di BIT, TTG, HostMilano, Fitur e altre. Esponi? Richiedi lo stand.', None),
    'idee-stand-fieristici': ('Idee per stand fiera: esempi di stand fieristici innovativi', None, None),
    'stand-modulari': ('Stand modulari e componibili per fiere | Danova Stand',
                       'Stand modulari e componibili per fiere in alluminio e tessuto teso, a noleggio o in acquisto: riutilizzabili, riconfigurabili e montati in fiera, in Italia e all\'estero.', None),
    'en/exhibition-stand-builder-bologna': ('Exhibition Stand Builder & Contractor in Bologna',
                                            'Exhibition stand builder, contractor and booth designer in Bologna (BolognaFiere): custom stands for Cosmoprof, Cersaie, EIMA. Free 3D design in 24-48 hours, crews on site.', None),
    'en/exhibition-stand-builder-milan': ('Exhibition Stand Builder & Contractor in Milan',
                                          'Exhibition stand builder, contractor and booth designer in Milan (Fiera Milano Rho): custom stands, free 3D design in 24-48 hours, furniture, LED walls and installation crews.', None),
    'en/exhibition-stand-builder-parma': ('Exhibition Stand Builder & Contractor in Parma',
                                          'Exhibition stand builder, contractor and booth designer in Parma (Fiere di Parma): custom stands for Cibus and SPS Italia, free 3D design in 24-48 hours, crews on site.', None),
    'en/exhibition-stand-builder-rimini': ('Exhibition Stand Builder & Contractor in Rimini',
                                           'Exhibition stand builder, contractor and booth designer in Rimini: custom stands for Sigep, Ecomondo, Macfrut and KEY. Free 3D design in 24-48 hours, crews on site.', None),
    'en/exhibition-stand-builder-florence': ('Exhibition Stand Builder & Contractor in Florence',
                                             'Exhibition stand builder, contractor and booth designer in Florence (Fortezza da Basso): stands for Pitti Immagine. Free 3D design in 24-48 hours, crews on site.', None),
}


def set_meta(h, title, desc, h1):
    t0 = re.search(r'<title>(.*?)</title>', h, re.S)
    d0 = re.search(r'<meta name="description" content="([^"]*)">', h)
    old_t = html.unescape(t0.group(1)) if t0 else None
    old_d = html.unescape(d0.group(1)) if d0 else None
    if title and old_t != title:
        h = h.replace(t0.group(0), f'<title>{e(title)}</title>', 1)
        short = title.split(' | ')[0]
        for a in ('property="og:title"', 'name="twitter:title"'):
            h = re.sub(r'<meta %s content="[^"]*">' % re.escape(a), lambda m: f'<meta {a} content="{e(short)}">', h, 1)
        if old_t:
            h = h.replace(json.dumps(old_t, ensure_ascii=False)[1:-1], json.dumps(title, ensure_ascii=False)[1:-1])
    if desc and old_d != desc:
        for a in ('name="description"', 'property="og:description"', 'name="twitter:description"'):
            h = re.sub(r'<meta %s content="[^"]*">' % re.escape(a), lambda m: f'<meta {a} content="{e(desc)}">', h, 1)
        if old_d:
            h = h.replace(json.dumps(old_d, ensure_ascii=False)[1:-1], json.dumps(desc, ensure_ascii=False)[1:-1])
    if h1 and h1[0] in h:
        h = h.replace(h1[0], h1[1])
    return h


# ---------------------------------------------------------------- 2. blocchi di testo
def P(*xs): return ''.join(f'<p>{x}</p>' for x in xs)

BLOCCHI = {
    'calendario-fiere-meccanica-e-industria': ('Fiere della metalmeccanica: <span class="grad">quali sono le più importanti</span>', P(
        'Chi cerca una fiera della metalmeccanica in Italia ha quattro appuntamenti principali: <a href="/stand-lamiera/">Lamiera</a> a Milano (lavorazione della lamiera, taglio laser, piegatura), <a href="/stand-emo/">EMO Milano</a> (macchine utensili), <a href="/stand-mecspe/">MECSPE</a> a Bologna (subfornitura e industria 4.0) e <a href="/stand-samuexpo/">Samuexpo</a> a Pordenone. In Europa contano soprattutto la <a href="/stand-hannover-messe/">Hannover Messe</a> e le fiere tedesche della meccanica.',
        'Nel calendario qui sopra trovi le date delle prossime edizioni delle fiere della meccanica e della metalmeccanica, con città e siti ufficiali. Se esponi, ti facciamo lo stand chiavi in mano con render 3D gratuito in 24-48 ore: <a href="/stand-fieristici-meccanica-e-industria/">stand per meccanica e industria</a>.')),
    'calendario-fiere-turismo': ('Fiere alberghiere <span class="grad">e dell\'ospitalità</span>', P(
        'Le fiere alberghiere riuniscono forniture per hotel, ristorazione, caffè e arredo contract. In Italia la più grande è <a href="/stand-host/">HostMilano</a> a Fiera Milano Rho; per il turismo contano <a href="/stand-bit-milano/">BIT Milano</a> e TTG Travel Experience a Rimini, in Europa <a href="/stand-fitur/">FITUR</a> a Madrid.',
        'Per gli enti del turismo, le regioni e le catene alberghiere costruiamo stand e padiglioni collettivi: <a href="/lavori/">abbiamo già realizzato stand per enti del turismo</a> come Telangana, Rajasthan e Uttar Pradesh.')),
    'stand-modulari': ('Stand componibili: <span class="grad">cosa vuol dire</span>', P(
        'Stand modulari e stand componibili sono la stessa cosa: una struttura fatta di pezzi standard (telai in alluminio, pannelli, tessuti tesi) che si montano in combinazioni diverse. Con gli stessi moduli fai uno stand da 9 mq a una fiera e uno da 32 mq a quella dopo, cambiando solo la grafica.',
        'Le strutture sono riutilizzabili e le conserviamo nel nostro magazzino tra una fiera e l\'altra. Nel prezzo dello stand modulare possono entrare anche arredi, luci e ledwall: vedi <a href="/noleggio-arredi-stand-fieristici/">noleggio arredi per stand</a>.')),
    'noleggio-stand-fieristici': ('Affitto stand per fiere: <span class="grad">cosa comprende</span>', P(
        'Affittare uno stand vuol dire usare strutture, pareti, pavimento e luci per la durata della fiera, senza comprarli: a fine manifestazione smontiamo e riportiamo tutto in magazzino. Tu paghi la grafica, che resta tua, e il noleggio dei pezzi.',
        'Con lo stand puoi noleggiare anche lounge, desk e banconi, tavoli e sedie per riunioni, frigo, macchina del caffè e TV: <a href="/noleggio-arredi-stand-fieristici/">noleggio arredi per stand fieristici</a>. Gli arredi li noleggiamo insieme ai nostri stand, non da soli.')),
    'ledwall-e-illuminazione-stand': ('Noleggio ledwall in fiera: <span class="grad">in Italia e in Europa</span>', P(
        'I ledwall che noleggiamo sono nostri: li portiamo e montiamo nelle fiere italiane (Milano Rho, Verona, Bologna, Parma, Vicenza, il Salone Nautico di Genova) e nelle fiere europee, da Berlino a Stoccarda, da Hannover a Düsseldorf, fino a Lione e Parigi.',
        'Il ledwall arriva con lo stand, già inserito nel progetto e nel render 3D, con l\'impianto elettrico e la dichiarazione di conformità richiesta dalla fiera. Vedi anche <a href="/stand-chiavi-in-mano/">stand chiavi in mano</a>.')),
    'stand-vicenzaoro': ('VicenzaOro <span class="grad">e T.Gold</span>', P(
        'Abbiamo già realizzato stand a VicenzaOro. Accanto a VicenzaOro, negli stessi giorni, si svolge T.Gold, il salone delle macchine e delle tecnologie per l\'oreficeria: costruiamo stand anche per T.Gold, con aree per mostrare le macchine in funzione e salette per le trattative.',
        'Per gli stand di gioielleria contano le vetrine illuminate, i banconi con cassetti chiusi a chiave e le salette riservate: li vedi nel render 3D, gratuito in 24-48 ore.')),
    'stand-a-due-piani': ('Stand soppalcati: <span class="grad">li facciamo</span>', P(
        'Stand a due piani e stand soppalcati sono la stessa cosa: al piano terra l\'esposizione, sopra sale riunioni o lounge. Li progettiamo e li costruiamo noi, con calcoli strutturali, collaudo e approvazione del progetto da parte dell\'ente fiera.',
        'Il soppalco va chiesto per tempo: molte fiere fissano una scadenza per i progetti a due piani. Mandaci fiera e metratura, il render arriva in 24-48 ore.')),
    'stand-fieristici-ecosostenibili': ('Stand ecologici: <span class="grad">i materiali che usiamo davvero</span>', P(
        'Per gli stand ecologici usiamo strutture riutilizzabili in alluminio e moduli che tornano in magazzino dopo ogni fiera, tessuti stampati in poliestere riciclabile, legno certificato FSC o PEFC e pannelli in cartone o materiali riciclati per pareti e espositori.',
        'Lo stand più ecologico è quello che si riusa: lo progettiamo perché si possa rimontare alla fiera successiva cambiando solo la grafica.')),
    'stand-fieristici-food-e-vino': ('Stand enogastronomici <span class="grad">e per cantine</span>', P(
        'Gli stand enogastronomici e gli stand per cantine hanno bisogno di banchi di degustazione, lavelli, frigoriferi e magazzino chiuso per cartoni e bottiglie. Li disegniamo con te nel render 3D e li montiamo a <a href="/stand-vinitaly/">Vinitaly</a>, <a href="/stand-cibus/">Cibus</a>, <a href="/stand-tuttofood/">Tuttofood</a>, <a href="/stand-sigep/">Sigep</a> e nelle fiere europee del vino come <a href="/stand-prowein/">ProWein</a> e <a href="/stand-wine-paris/">Wine Paris</a>.',
        'Frigo, macchina del caffè e arredi per l\'area assaggio sono compresi nello stand: <a href="/noleggio-arredi-stand-fieristici/">noleggio arredi per stand</a>.')),
    'allestimenti-fieristici-firenze': ('Stand fieristici <span class="grad">in tutta la Toscana</span>', P(
        'Oltre a Firenze facciamo stand per le aziende di tutta la Toscana: cantine del Chianti e di Montalcino che espongono a Vinitaly, ProWein e Wine Paris, aziende di Prato, Pistoia, Arezzo e Siena alle fiere di moda, arredo e food in Italia e in Europa.',
        'Per gli stand in Toscana valgono gli stessi servizi: render 3D gratuito in 24-48 ore, produzione, trasporto, montaggio e pratiche con l\'ente fiera.')),
    'allestimenti-eventi': ('Stand sponsor <span class="grad">e area expo per congressi</span>', P(
        'Nei congressi e nelle convention costruiamo gli stand degli sponsor e l\'area expo: stand preallestiti o su misura, tutti con la grafica dello sponsor, montati prima dell\'apertura e smontati a fine evento.',
        'Gli stand sponsor nascono come quelli delle fiere: render 3D gratuito in 24-48 ore, preventivo voce per voce, arredi e ledwall compresi se servono. Vedi <a href="/stand-preallestiti/">stand preallestiti</a>.')),
    'progettazione-stand-fieristici': ('Rendering stand: <span class="grad">gratis in 24-48 ore</span>', P(
        'Il rendering 3D dello stand è gratuito e arriva insieme al preventivo in 24-48 ore. Lo modifichiamo con te finché non lo approvi e lo stand montato in fiera è uguale al render.',
        'Tutti i dettagli: <a href="/rendering-stand-fieristici/">rendering stand fieristici</a>.')),
    'stand-hannover-messe': ('Abbiamo già lavorato <span class="grad">a Hannover e in Germania</span>', P(
        'Abbiamo già costruito stand a Hannover e lavoriamo spesso in Germania: altri stand a MEDICA a Düsseldorf, stand ad Anuga a Colonia e montaggi per altri allestitori. In Germania lavoriamo con la nostra squadra e con partner locali.',
        'Pagina in tedesco: <a href="/de/messebau-hannover/">Messebau Hannover</a>.')),
    'allestimenti-fieristici-germania': ('I nostri lavori <span class="grad">in Germania</span>', P(
        'Nel 2026 abbiamo costruito il <a href="/lavori/padiglione-tunisia-medica-dusseldorf/">padiglione della Tunisia a MEDICA</a> a Düsseldorf. Abbiamo realizzato anche altri stand a MEDICA, stand ad Anuga a Colonia e a Hannover, e montaggi per altri allestitori.',
        'In Germania lavoriamo con la nostra squadra dall\'Italia e con partner locali, con un solo capocantiere. Pagine in altre lingue: <a href="/de/messebau-hannover/">Messebau Hannover</a>, <a href="/nl/standbouw-medica-dusseldorf/">standbouw MEDICA Düsseldorf</a>.')),
    'idee-stand-fieristici': ('Esempi di stand fieristici: <span class="grad">render e foto vere</span>', P(
        'Cerchi idee per lo stand in fiera? Guarda i <a href="/progetti-stand-fieristici/">progetti di stand fieristici con i render</a> e le <a href="/lavori/">foto vere degli stand che abbiamo costruito</a>.',
        'Quando hai un\'idea, mandaci fiera e metratura: il <a href="/rendering-stand-fieristici/">rendering 3D del tuo stand</a> è gratuito e arriva in 24-48 ore.')),
    'en/medica-stand-builder': ('Our work <span class="grad">at MEDICA</span>', P(
        'At MEDICA 2026 we built the <a href="/lavori/padiglione-tunisia-medica-dusseldorf/">national pavilion of Tunisia</a>, with the stands of the Tunisian exhibitors and a meeting lounge. We have built other stands at MEDICA too, plus stands at Anuga in Cologne and in Hannover.',
        'In Germany we work with our own crew from Italy and local partners, with one site manager. Dutch-speaking exhibitors can write to us in Dutch: <a href="/nl/standbouw-medica-dusseldorf/">standbouw MEDICA Düsseldorf</a>.')),
}
EN_CITY = ('Stand builder, contractor or booth designer? <span class="grad">All three.</span>', '{c}', P(
    'Whether you call it an exhibition stand builder, a stand contractor, a booth builder or a design and build company, in {c} we do the whole job: custom stand and booth design, a free 3D render within 24-48 hours, production, graphics, furniture, LED walls, electrics with the Italian certificate, installation and dismantling.',
    'You get one contact who replies in English every day, weekends included, and an itemised quote in euro.'))
for slug, c in (('bologna', 'Bologna'), ('milan', 'Milan'), ('parma', 'Parma'), ('rimini', 'Rimini'), ('florence', 'Florence')):
    BLOCCHI[f'en/exhibition-stand-builder-{slug}'] = (EN_CITY[0], EN_CITY[2].replace('{c}', c))

RE_B = re.compile(r'<!--ds-gsc-->.*?<!--/ds-gsc-->\n?', re.S)


def blocco(h, tit, corpo):
    # sostituito sul posto se c'e' gia' (stabile con foto-vere-pagine.py, che mette il suo blocco prima delle FAQ)
    b = (f'<!--ds-gsc--><section id="approfondimento"><div class="wrap"><div class="sec-head"><h2 class="title" data-rv="up">{tit}</h2></div>'
         f'<div class="pg-testo" data-rv="up">{corpo}</div></div></section><!--/ds-gsc-->\n')
    if RE_B.search(h):
        return RE_B.sub(lambda m: b, h, 1)
    i = h.find('<!--ds-foto-vere-->')
    if i < 0:
        i = h.find('<section id="faq"')
    return h[:i] + b + h[i:] if i > 0 else h


# ---------------------------------------------------------------- 3. link interni
LINK_ADD = {
    'servizi/allestimenti-fieristici': [('/stand-chiavi-in-mano/', 'Stand chiavi in mano'), ('/rendering-stand-fieristici/', 'Rendering stand in 24-48 ore'),
                                        ('/noleggio-arredi-stand-fieristici/', 'Noleggio arredi per stand'), ('/allestimenti-fieristici-svizzera/', 'Fiere in Svizzera'),
                                        ('/allestimenti-fieristici-sicilia/', 'Fiere in Sicilia')],
    'noleggio-stand-fieristici': [('/noleggio-arredi-stand-fieristici/', 'Noleggio arredi per stand')],
    'stand-preallestiti': [('/noleggio-arredi-stand-fieristici/', 'Noleggio arredi per stand'), ('/stand-chiavi-in-mano/', 'Stand chiavi in mano')],
    'espositori-desk-totem-per-fiere': [('/noleggio-arredi-stand-fieristici/', 'Noleggio arredi per stand')],
    'progettazione-stand-fieristici': [('/rendering-stand-fieristici/', 'Rendering stand fieristici')],
    'progetti-stand-fieristici': [('/rendering-stand-fieristici/', 'Rendering stand fieristici')],
    'stand-fieristici-su-misura': [('/stand-chiavi-in-mano/', 'Stand chiavi in mano'), ('/rendering-stand-fieristici/', 'Rendering stand fieristici')],
    'allestimenti-eventi-showroom-negozi': [('/allestimento-showroom/', 'Allestimento showroom')],
    'allestimento-negozi': [('/allestimento-showroom/', 'Allestimento showroom')],
    'allestimenti-eventi': [('/allestimento-showroom/', 'Allestimento showroom')],
    'stand-salone-del-mobile': [('/allestimento-showroom/', 'Allestimento showroom'), ('/noleggio-arredi-stand-fieristici/', 'Noleggio arredi per stand')],
    'allestimenti-fieristici-lombardia': [('/allestimenti-fieristici-varese/', 'Varese, Como e Novara')],
    'allestimenti-fieristici-milano': [('/allestimenti-fieristici-varese/', 'Varese, Como e Novara'), ('/noleggio-arredi-stand-fieristici/', 'Noleggio arredi per stand')],
    'allestimenti-fieristici-estero': [('/allestimenti-fieristici-svizzera/', 'Fiere in Svizzera')],
    'allestimenti-fieristici-germania': [('/de/messebau-hannover/', 'Deutsch: Messebau Hannover'), ('/nl/standbouw-medica-dusseldorf/', 'Nederlands: standbouw MEDICA')],
    'allestimenti-fieristici-napoli': [('/allestimenti-fieristici-sicilia/', 'Fiere in Sicilia')],
    'allestimenti-fieristici-bari': [('/allestimenti-fieristici-sicilia/', 'Fiere in Sicilia')],
    'allestimenti-fieristici-venezia': [('/en/exhibition-stand-builder-venice/', 'English: stand builder in Venice')],
    'allestimenti-fieristici-genova': [('/en/exhibition-stand-builder-genoa/', 'English: stand builder in Genoa')],
    'stand-salone-nautico-genova': [('/en/exhibition-stand-builder-genoa/', 'English: stand builder in Genoa')],
    'stand-hannover-messe': [('/de/messebau-hannover/', 'Deutsch: Messebau Hannover')],
    'stand-medica': [('/nl/standbouw-medica-dusseldorf/', 'Nederlands: standbouw MEDICA Düsseldorf')],
    'en/medica-stand-builder': [('/nl/standbouw-medica-dusseldorf/', 'Nederlands: standbouw MEDICA Düsseldorf')],
    'en/hannover-messe-stand-builder': [('/de/messebau-hannover/', 'Deutsch: Messebau Hannover')],
    'nl/standbouw-beurzen-duitsland-europa': [('/nl/standbouw-medica-dusseldorf/', 'Standbouw MEDICA Düsseldorf')],
    'de/messebau-italien': [('/de/messebau-hannover/', 'Messebau Hannover')],
    'de/messebau-mailand': [('/de/messebau-hannover/', 'Messebau Hannover')],
    'en/exhibition-stand-builder-italy': [('/en/exhibition-stand-builder-venice/', 'Venice'), ('/en/exhibition-stand-builder-genoa/', 'Genoa')],
    'en/exhibition-stand-builder-europe': [('/nl/standbouw-medica-dusseldorf/', 'Nederlands: standbouw MEDICA Düsseldorf'), ('/de/messebau-hannover/', 'Deutsch: Messebau Hannover')],
}


def link_add(h, links):
    for href, txt in links:
        if f'href="{href}"' in h or not os.path.exists(os.path.join(ROOT, href.strip('/'), 'index.html')):
            continue
        a = f'<a href="{href}">{html.escape(txt)}</a>'
        if '<div class="pg-altri"' in h:
            h = re.sub(r'(<div class="pg-altri"[^>]*>)(\n?)', lambda m: m.group(1) + m.group(2) + ('      ' if m.group(2) else '') + a + m.group(2), h, 1)
        else:
            h = re.sub(r'(<div class="fr-chips"[^>]*>)(?=<a )', lambda m: m.group(1) + a, h, 1)
    return h


for rel in sorted(set(META) | set(BLOCCHI) | set(LINK_ADD)):
    p = os.path.join(ROOT, rel, 'index.html')
    if not os.path.exists(p):
        print('manca', rel); continue
    h = open(p, encoding='utf-8').read(); h0 = h
    if rel in META:
        h = set_meta(h, *META[rel])
        if h != h0: stats['meta'] += 1
    if rel in BLOCCHI:
        h1 = blocco(h, *BLOCCHI[rel])
        if h1 != h: stats['blocchi'] += 1
        h = h1
    if rel in LINK_ADD:
        h1 = link_add(h, LINK_ADD[rel])
        if h1 != h: stats['link'] += 1
        h = h1
    if h != h0:
        open(p, 'w', encoding='utf-8').write(h); stats['file'] += 1


# ---------------------------------------------------------------- 3b. selettore lingua delle pagine estere nuove
# (generate da modelli di altre citta': la lingua della pagina deve puntare a se stessa)
SELETTORE = {
    'de/messebau-hannover': {'it': '/stand-hannover-messe/', 'en': '/en/hannover-messe-stand-builder/'},
    'nl/standbouw-medica-dusseldorf': {'it': '/stand-medica/', 'en': '/en/medica-stand-builder/', 'zh-Hans': '/zh/europe-exhibition-stand/', 'zh-Hant': '/zh-hant/europe-exhibition-stand/'},
    'en/exhibition-stand-builder-venice': {'it': '/allestimenti-fieristici-venezia/', 'zh-Hans': '/zh/italy-exhibition-stand/', 'zh-Hant': '/zh-hant/italy-exhibition-stand/'},
    'en/exhibition-stand-builder-genoa': {'it': '/allestimenti-fieristici-genova/', 'zh-Hans': '/zh/italy-exhibition-stand/', 'zh-Hant': '/zh-hant/italy-exhibition-stand/'},
}


def selettore(h, rel, mappa):
    lang = rel.split('/')[0]
    mappa = dict(mappa, **{lang: f'/{rel}/'})
    def sub(m):
        lg = m.group(2)
        href = mappa.get(lg, m.group(1))
        return f'<a href="{href}" hreflang="{lg}"' + (' aria-current="page"' if lg == lang else '') + '>'
    return re.sub(r'<a href="([^"]*)" hreflang="([A-Za-z-]+)"(?: aria-current="page")?>', sub, h)


# testi olandesi: rispondiamo per iscritto in olandese (risposta di Devid 24/11/2026)
NL_TESTI = [
    ('Wij communiceren per e-mail in het Engels; uw aanvraag in het Nederlands is welkom.', 'Wij schrijven u in het Nederlands; telefonisch spreken wij Engels en Italiaans.'),
    ('Per e-mail in het Engels, binnen 24 werkuren. U mag ons gerust in het Nederlands schrijven.', 'Schriftelijk (e-mail, WhatsApp) in het Nederlands, binnen 24 uur. Telefonisch spreken wij Engels en Italiaans.'),
    ('Wij antwoorden binnen 24 werkuren. Liever bellen?', 'Wij antwoorden binnen 24 uur, ook schriftelijk in het Nederlands. Liever bellen?'),
]
for rel in list(SELETTORE) + ['nl/standbouw-beurzen-duitsland-europa', 'nl/standbouw-italie']:
    p = os.path.join(ROOT, rel, 'index.html')
    if not os.path.exists(p): continue
    h = open(p, encoding='utf-8').read(); h0 = h
    if rel in SELETTORE:
        h = selettore(h, rel, SELETTORE[rel])
    if rel.startswith('nl/'):
        for a, b in NL_TESTI:
            h = h.replace(a, b)
    if h != h0:
        open(p, 'w', encoding='utf-8').write(h); stats['lingua'] += 1

# ---------------------------------------------------------------- 4. sitemap e llms.txt
NUOVE = [
    ('/noleggio-arredi-stand-fieristici/', 'stand-noleggio-arredi', '- [Noleggio arredi per stand fieristici](https://danovastand.com/noleggio-arredi-stand-fieristici/): lounge, desk e banconi, area riunioni, frigo, macchina del caffè e TV, compresi nello stand Danova (non noleggiati da soli).'),
    ('/rendering-stand-fieristici/', 'progettazione-stand-render-3d', '- [Rendering stand fieristici](https://danovastand.com/rendering-stand-fieristici/): render 3D fotorealistico gratuito con il preventivo, primo render in 24-48 ore, stand costruito uguale al render.'),
    ('/stand-chiavi-in-mano/', 'stand-su-misura-legno-curvo', '- [Stand chiavi in mano](https://danovastand.com/stand-chiavi-in-mano/): progetto, grafica, trasporto, montaggio e smontaggio, impianto elettrico certificato, arredi, ledwall, moquette e tutte le pratiche con l\'ente fiera; almeno 2-3 settimane per uno stand su misura.'),
    ('/allestimento-showroom/', 'allestimento-showroom-evento', '- [Allestimento showroom](https://danovastand.com/allestimento-showroom/): showroom permanenti su misura, temporanei e pop-up, corner nei negozi.'),
    ('/allestimenti-fieristici-varese/', 'stand-milano-rho-tecnologia', '- [Allestimenti fieristici Varese, Como e Novara](https://danovastand.com/allestimenti-fieristici-varese/): stand per Malpensafiere e Lariofiere (dove abbiamo già lavorato), Fiera Milano Rho e fiere all\'estero.'),
    ('/allestimenti-fieristici-svizzera/', 'stand-fiera-estero-padiglione', '- [Allestimenti fieristici in Svizzera](https://danovastand.com/allestimenti-fieristici-svizzera/): Lugano, Zurigo, Basilea, Ginevra; dogana (carnet ATA) e trasporto gestiti da Danova Stand.'),
    ('/allestimenti-fieristici-sicilia/', 'stand-48-mq-isola', '- [Allestimenti fieristici in Sicilia](https://danovastand.com/allestimenti-fieristici-sicilia/): stand da 30 mq in su a Palermo e Catania; stand per aziende siciliane alle fiere italiane ed europee.'),
    ('/de/messebau-hannover/', 'stand-meccanica-macchinari', '- [Messebau Hannover](https://danovastand.com/de/messebau-hannover/): Messestände für Hannover Messe, Agritechnica und EuroTier (Deutsch).'),
    ('/nl/standbouw-medica-dusseldorf/', 'stand-a-isola-quattro-lati', '- [Standbouw MEDICA Düsseldorf](https://danovastand.com/nl/standbouw-medica-dusseldorf/): beursstands voor MEDICA en COMPAMED; paviljoen Tunesië op MEDICA 2026 (Nederlands).'),
    ('/en/exhibition-stand-builder-venice/', 'stand-venezia-evento-storico', '- [Exhibition stand builder in Venice](https://danovastand.com/en/exhibition-stand-builder-venice/): stands, event installations and floating stages in Venice and Mestre (English).'),
    ('/en/exhibition-stand-builder-genoa/', 'stand-genova-salone-nautico', '- [Exhibition stand builder in Genoa](https://danovastand.com/en/exhibition-stand-builder-genoa/): stands for the Genoa International Boat Show (English).'),
]
ANCORA_IT = '- [Allestimento vetrine](https://danovastand.com/allestimento-vetrine/)'
ANCORA_ESTERO = '- [Messebau Verona](https://danovastand.com/de/messebau-verona/)'
sm_p = os.path.join(ROOT, 'sitemap.xml'); sm = open(sm_p, encoding='utf-8').read(); sm0 = sm
ll_p = os.path.join(ROOT, 'llms.txt'); ll = open(ll_p, encoding='utf-8').read(); ll0 = ll
for path, img, riga in reversed(NUOVE):  # inserite dopo l'ancora: al contrario per tenere l'ordine
    if not os.path.exists(os.path.join(ROOT, path.strip('/'), 'index.html')):
        print('pagina non generata', path); continue
    url = SITO + path
    lg = path.split('/')[1] if path.split('/')[1] in ('de', 'en', 'nl') else 'it'
    if f'<loc>{url}</loc>' not in sm:
        sm = sm.replace('</urlset>', f'  <url>\n    <loc>{url}</loc>\n    <lastmod>2026-11-24</lastmod>\n'
                        f'    <image:image><image:loc>{SITO}/assets/img/stand/{img}.webp</image:loc></image:image>\n'
                        f'    <xhtml:link rel="alternate" hreflang="{lg}" href="{url}"/>\n'
                        f'    <xhtml:link rel="alternate" hreflang="x-default" href="{url}"/>\n  </url>\n</urlset>')
    if riga not in ll:
        dopo = ANCORA_ESTERO if lg != 'it' else ANCORA_IT
        i = ll.find(dopo)
        if i >= 0:
            j = ll.find('\n', i)
            ll = ll[:j + 1] + riga + '\n' + ll[j + 1:]
        else:
            ll = ll.rstrip('\n') + '\n' + riga + '\n'
if sm != sm0: open(sm_p, 'w', encoding='utf-8').write(sm); stats['sitemap'] += 1
if ll != ll0: open(ll_p, 'w', encoding='utf-8').write(ll); stats['llms'] += 1
print(dict(stats))
