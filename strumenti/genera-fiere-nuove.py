#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Pagine /stand-<fiera>/ nuove (24/11/2026), testi in strumenti/dati_fiere_nuove.py.

Modello: stand-sps-italia/index.html (head, menu, footer, script e schema Organization restano quelli).
Per ogni fiera riscrive: title, description, canonical, hreflang, og/twitter, JSON-LD della pagina,
selettore lingua e tutto <main>. Idempotente. Uso:
    python3 strumenti/genera-fiere-nuove.py            # tutte
    python3 strumenti/genera-fiere-nuove.py bau ism    # solo alcune
Poi, come sempre: ottimizza-geo.py, genera-feed-e-testo.py, audit-seo.py.
"""
import html, json, os, re, sys
from datetime import date

RADICE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RADICE, "strumenti"))
import glob, importlib  # noqa: E402
F, SEDI, IMG = [], {}, {}
for _m in sorted(glob.glob(os.path.join(RADICE, "strumenti", "dati_fiere_nuove*.py"))):
    _d = importlib.import_module(os.path.basename(_m)[:-3])
    F += _d.F
    SEDI.update(getattr(_d, "SEDI", {}))
    IMG.update(getattr(_d, "IMG", {}))
_k = [f["k"] for f in F]
assert len(_k) == len(set(_k)), "slug ripetuto in dati_fiere_nuove*.py"


def alt_render(nome):
    """Alt del render: da IMG, altrimenti lo stesso alt italiano gia' usato nelle pagine del sito."""
    if nome not in IMG:
        pat = re.compile(re.escape(nome) + r'-800\.webp[^>]*alt="([^"]*)"')
        for fp in glob.glob(os.path.join(RADICE, "*", "index.html")):
            m = pat.search(open(fp, encoding="utf-8").read())
            if m and re.match(r"[A-Za-zÀ-ÿ]", m.group(1)):
                IMG[nome] = html.unescape(m.group(1))
                break
        else:
            raise SystemExit(f"render {nome}: alt non trovato, aggiungilo a IMG")
    return IMG[nome]

SITO = "https://danovastand.com"
MODELLO = os.path.join(RADICE, "stand-sps-italia", "index.html")
OGGI = date.today().isoformat()
MESI = ["", "gennaio", "febbraio", "marzo", "aprile", "maggio", "giugno", "luglio", "agosto",
        "settembre", "ottobre", "novembre", "dicembre"]
e = lambda t: html.escape(t, quote=True)
txt = lambda t: re.sub(r"<[^>]+>", "", t)
FRECCIA = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 12h14M13 6l6 6-6 6"></path></svg>'


def titolo(f, s):
    anno = f["start"][:4]
    for t in (f"Stand {f['nome']} {anno}: allestitore a {s['c']} | Danova Stand",
              f"Stand {f['nome']} {anno}: allestitore a {s['c']}",
              f"Stand {f['nome']} {anno} | Danova Stand",
              f"Stand {f['nome']} {anno}"):
        if len(t) <= 62:
            return t
    return f"Stand {f['nome']} {anno}"


def descrizione(f, s):
    d = (f"Allestitore per {f['nome']} a {s['q']}: stand chiavi in mano con progetto 3D, materiali, "
         f"grafica, impianti e montatori in fiera. Prossima edizione: {f['date']}.")
    if len(d) > 158:
        d = f"Stand per {f['nome']} a {s['q']}: progetto, produzione e montaggio. Prossima edizione: {f['date']}."
    if len(d) > 160:  # 24/11/2026: nomi lunghi (es. "Hospitality – Il Salone dell'Accoglienza"): solo la prima parte
        d = d.replace(f['nome'], f['nome'].split(" – ")[0])
    return d


def main_html(f, s):
    nome, url = f["nome"], f"/stand-{f['k']}/"
    crumbs = ('<a href="/allestimenti-fieristici-estero/">Fiere all\'estero</a>' if f["estero"]
              else '<a href="/calendario-fiere/">Calendario fiere</a>')
    dove = f"{s['q']}, {s['c']}" + (f" ({s['p']})" if f["estero"] else "")
    img, alt = f["img"], alt_render(f["img"])
    nota_date = ("Le date sono quelle pubblicate dall'organizzatore (verificate a novembre 2026): controllale sempre sul sito ufficiale prima di prenotare viaggi e trasporti."
                 if f["conf"] else
                 "Le date ufficiali di questa edizione non sono ancora uscite: indichiamo il mese previsto e le aggiorniamo appena l'organizzatore le pubblica.")
    sito_lbl = re.sub(r"^https?://", "", f["sito"]).rstrip("/")
    if not sito_lbl.startswith("www."):
        sito_lbl = sito_lbl
    esig = "\n".join(f"      <li><b>{e(b)}</b> {e(t)}</li>" for b, t in f["esig"])
    off_h = "\n".join(f"      <li><b>{e(o)}.</b></li>" for o in f["off"])
    estero = ""
    if f["estero"]:
        estero = f'''<section id="estero">
  <div class="wrap">
    <div class="sec-head">
      <h2 class="title" data-rv="up">Dall'Italia a {e(s['c'])} con un solo referente</h2>
    </div>
    <div class="pg-testo" data-rv="up">
      <p>Lo stand per {e(nome)} si produce in Italia con i nostri laboratori partner, si controlla nel nostro magazzino e viaggia con noi fino a {e(s['q'])}. Lì lo montano squadre coordinate da un referente italiano, che segue anche pass, orari di scarico e pratiche con l'organizzatore. A fine fiera, se lo stand è tuo, torna in magazzino per la prossima edizione o per un'altra fiera in {e(s['p'])} o in Italia.</p>
    </div>
  </div>
</section>
'''
    faq = list(f["qa"]) + [
        (f"Quanto costa uno stand per {nome}?", "Dipende da metratura, tipo di struttura, finiture, impianti e servizi richiesti. Ti mandiamo un preventivo gratuito voce per voce; nella <a href=\"/quanto-costa-uno-stand-fieristico/\">guida ai costi</a> trovi le voci che incidono di più."),
    ]
    faq_h = "\n".join(
        f'      <details data-rv="up"><summary>{e(q)}<span class="pm"></span></summary>\n        <div class="ans"><p>{a}</p></div></details>'
        for q, a in faq)
    altri = list(f["altri"]) + [f["hub"]]
    altri += [("/allestimenti-fieristici-estero/", "Allestimenti fieristici all'estero")] if f["estero"] else []
    altri += [("/calendario-fiere/", "Calendario fiere 2026–2027"), ("/stand-fieristici-su-misura/", "Stand su misura"),
              ("/montaggio-stand-fieristici/", "Montaggio stand"), ("/quanto-costa-uno-stand-fieristico/", "Quanto costa uno stand"),
              ("/servizi/allestimenti-fieristici/", "Allestimenti fieristici")]
    visti, alt_h = set(), []
    for h, l in altri:
        if h in visti or h == url:
            continue
        visti.add(h)
        alt_h.append(f'      <a href="{h}">{e(l)}</a>')
    chi = f"\n      <div><dt>Chi la visita</dt><dd>{e(f['pub'])}</dd></div>" if f.get("pub") else ""
    req = f"{nome} – {s['c']}, {f['date'].replace(' (date da confermare)', '')}"
    return f'''<main id="main">

<div class="wrap pg-crumbs">
  <a href="/">Home</a><em>/</em><a href="/servizi/allestimenti-fieristici/">Allestimenti fieristici</a><em>/</em>{crumbs}<em>/</em>Stand {e(nome)}
</div>

<section class="pg-hero">
  <div class="wrap">
    <div class="eyebrow mono" data-scramble>Stand · {e(nome)}</div>
    <h1 data-rv="up">Stand per {e(nome)}: <span class="grad">allestitore chiavi in mano</span> a {e(s['q'])}.</h1>
    <p class="lead" data-rv="up">{e(f['lead'])}</p>
    <div class="fr-dates" data-rv="up"><span>{e(nome)}: {e(f['date'])}</span><span>{e(s['q'])}, {e(s['c'])}</span></div>
    <div class="hero-cta" data-rv="up">
      <a href="#richiesta" class="btn btn-p" data-mag><span class="sheen"></span><span class="lbl">Richiedi lo stand per {e(nome)}</span>
        {FRECCIA}</a>
      <a href="#esigenze" class="btn btn-g" data-mag><span class="lbl">Cosa serve allo stand</span></a>
    </div>
  </div>
  <div class="fr-hero-vis fr-hero-foto"><picture><source media="(max-width:1180px)" srcset="data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7"><img src="/assets/img/stand/{img}-800.webp" srcset="/assets/img/stand/{img}-800.webp 800w, /assets/img/stand/{img}-1200.webp 1200w" sizes="(max-width:1180px) 0px, 440px" alt="{e(alt)}" width="800" height="600" fetchpriority="high" decoding="async"></picture></div>
</section>
<section id="scheda">
  <div class="wrap">
    <div class="sec-head">
      <h2 class="title" data-rv="up">{e(nome)} in breve</h2>
      <p class="lead" data-rv="up">{nota_date}</p>
    </div>
    <dl class="fr-scheda" data-rv="up">
      <div><dt>Fiera</dt><dd>{e(nome)}</dd></div>
      <div><dt>Dove</dt><dd>{e(dove)}<br><small>{e(s['via'])}</small></dd></div>
      <div><dt>Prossima edizione</dt><dd>{e(f['date'])}</dd></div>
      <div><dt>Cadenza</dt><dd>{e(f['cad'])}</dd></div>
      <div><dt>Settore</dt><dd>{e(f['sett'])}</dd></div>{chi}
      <div><dt>Sito ufficiale</dt><dd><a href="{f['sito']}" rel="noopener" target="_blank">{e(sito_lbl)}</a></dd></div>
      <div><dt>Il nostro servizio</dt><dd>Allestiamo stand per {e(nome)} e per le fiere del settore in Italia e all'estero: progetto, produzione, trasporto e montaggio.</dd></div>
    </dl>
  </div>
</section>
<section id="fiera">
  <div class="wrap">
    <div class="sec-head">
      <h2 class="title" data-rv="up">Cos'è {e(nome)} e <span class="grad">cosa chiede allo stand</span></h2>
    </div>
    <div class="pg-testo" data-rv="up">
      <p>{e(f['intro'][0])}</p>
      <p>{e(f['intro'][1])}</p>
    </div>
  </div>
</section>
<section id="esigenze">
  <div class="wrap">
    <div class="sec-head">
      <h2 class="title" data-rv="up">Cosa serve a uno stand per {e(nome)}</h2>
    </div>
    <ul class="pg-lista" data-rv="up">
{esig}
    </ul>
  </div>
</section>
<section id="cosa">
  <div class="wrap">
    <div class="sec-head">
      <h2 class="title" data-rv="up">Cosa fa l'allestitore per il tuo stand a {e(nome)}</h2>
      <p class="lead" data-rv="up">Per {e(nome)} seguiamo progetto e render 3D, produzione, grafica, impianti, trasporto, montaggio e smontaggio a {e(s['q'])}, oppure solo la parte che ti manca, anche il solo montaggio di uno stand che hai già. In particolare:</p>
    </div>
    <ul class="pg-lista" data-rv="up">
{off_h}
    </ul>
  </div>
</section>
{estero}<section id="tempi">
  <div class="wrap">
    <div class="sec-head">
      <h2 class="title" data-rv="up">Quando iniziare a preparare lo stand per {e(nome)}</h2>
    </div>
    <div class="pg-testo" data-rv="up">
      <p>{e(f['tempi'])}</p>
      <p>Tutte le date delle prossime fiere, in Italia e in Europa, sono nel nostro <a href="/calendario-fiere/">calendario fiere 2026–2027</a>.</p>
    </div>
  </div>
</section>
{LEGNO}
<section id="richiesta" class="fr-req-sec">
{RICHIESTA.replace('__REQ__', e(req))}
</section>
<section id="faq">
  <div class="wrap">
    <div class="sec-head">
      <div class="eyebrow mono" data-scramble>Domande frequenti</div>
      <h2 class="title" data-rv="up">Le risposte che <span class="grad">servono davvero.</span></h2>
    </div>
    <div class="faq">
{faq_h}
    </div>
  </div>
</section>
<section class="pg-cta">
  <div class="wrap">
    <div class="box" data-rv="up">
      <h2 class="title">Esponi a {e(nome)}?</h2>
      <p>Dicci fiera, date e metratura: ti rispondiamo con quello che serve e quanto costa, anche con poco preavviso.</p>
      <a href="#richiesta" class="btn btn-p" data-mag><span class="sheen"></span><span class="lbl">Richiedi un preventivo gratuito</span>
        {FRECCIA}</a>
    </div>
  </div>
</section>
<section id="altri">
  <div class="wrap">
    <div class="sec-head"><h2 class="title" data-rv="up">Approfondisci</h2></div>
    <div class="pg-altri" data-rv="up">
{chr(10).join(alt_h)}
    </div>
  </div>
</section>

</main>''', faq


def jsonld(graph_tpl, f, s, faq, tit, desc):
    url = f"{SITO}/stand-{f['k']}/"
    g = []
    for n in graph_tpl:
        t = n.get("@type")
        if t == "WebPage":
            n = json.loads(json.dumps(n))
            n.update({"@id": url + "#webpage", "url": url, "name": tit, "description": desc,
                      "breadcrumb": {"@id": url + "#breadcrumb"}, "about": {"@id": url + "#service"},
                      "datePublished": OGGI, "dateModified": OGGI})
            ev = n["mentions"][0]
            ev.update({"name": f["nome"], "startDate": f["start"] if f["conf"] else f["start"][:7],
                       "url": f["sito"], "description": f"{f['nome']}: fiera di settore {f['sett'].lower()} a {s['c']}.",
                       "organizer": {"@type": "Organization", "name": f["nome"], "url": f["sito"]},
                       "performer": {"@type": "Organization", "name": f["nome"], "url": f["sito"]}})
            if f["end"]:
                ev["endDate"] = f["end"]
            else:
                ev.pop("endDate", None)
            ev["location"] = {"@type": "Place", "name": s["q"],
                              "address": {"@type": "PostalAddress", "streetAddress": s["via"], "addressLocality": s["c"], "addressCountry": s["cc"]},
                              "geo": {"@type": "GeoCoordinates", "latitude": s["lat"], "longitude": s["lon"]}}
        elif t == "BreadcrumbList":
            terzo = (("Fiere all'estero", f"{SITO}/allestimenti-fieristici-estero/") if f["estero"]
                     else ("Calendario fiere", f"{SITO}/calendario-fiere/"))
            n = {"@type": "BreadcrumbList", "@id": url + "#breadcrumb", "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Home", "item": SITO + "/"},
                {"@type": "ListItem", "position": 2, "name": "Allestimenti fieristici", "item": f"{SITO}/servizi/allestimenti-fieristici/"},
                {"@type": "ListItem", "position": 3, "name": terzo[0], "item": terzo[1]},
                {"@type": "ListItem", "position": 4, "name": f"Stand {f['nome']}"}]}
        elif t == "Service":
            n = {"@type": "Service", "@id": url + "#service", "name": f"Stand per {f['nome']}",
                 "serviceType": "Allestimento e montaggio di stand fieristici",
                 "description": f"Progettazione, materiali e componentistica, grafica, impianti, trasporto, montaggio e smontaggio di stand per {f['nome']} a {s['q']} ({s['c']}).",
                 "provider": {"@id": f"{SITO}/#organization"},
                 "areaServed": [{"@type": "City", "name": s["c"]}, {"@type": "Country", "name": s["p"]}],
                 "availableLanguage": ["Italian"],
                 "hasOfferCatalog": {"@type": "OfferCatalog", "name": f"Stand per {f['nome']}", "itemListElement": [
                     {"@type": "Offer", "itemOffered": {"@type": "Service", "name": o}} for o in f["off"]]}}
        elif t == "FAQPage":
            n = {"@type": "FAQPage", "@id": url + "#faq", "isPartOf": {"@id": url + "#webpage"}, "inLanguage": "it",
                 "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": txt(a)}} for q, a in faq]}
        g.append(n)
    return g


def genera(f, modello, graph_tpl, json_block):
    s = SEDI[f["sede"]]
    url = f"{SITO}/stand-{f['k']}/"
    tit, desc = titolo(f, s), descrizione(f, s)
    ogt = f"Stand per {f['nome']} — Danova Stand"
    ogd = f"Allestitore chiavi in mano a {s['q']}: progetto, materiali, grafica, impianti e montaggio."
    img = f"{SITO}/assets/img/stand/og/{f['img']}.jpg"
    for v in (f"og/{f['img']}.jpg", f"{f['img']}-800.webp", f"{f['img']}-1200.webp"):
        if not os.path.exists(os.path.join(RADICE, "assets/img/stand", v)):
            raise SystemExit(f"{f['k']}: manca assets/img/stand/{v}")
    main, faq = main_html(f, s)
    p = modello
    p = re.sub(r"<title>.*?</title>", f"<title>{html.escape(tit, quote=False)}</title>", p, 1, re.S)
    p = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{e(desc)}">', p, 1)
    p = re.sub(r'<link rel="canonical" href="[^"]*">', f'<link rel="canonical" href="{url}">', p, 1)
    p = re.sub(r'(<link rel="alternate" hreflang="(?:it|x-default)" href=")[^"]*(">)', lambda m: m.group(1) + url + m.group(2), p)
    p = re.sub(r'<meta property="og:url" content="[^"]*">', f'<meta property="og:url" content="{url}">', p, 1)
    for k, v in (("og:title", ogt), ("og:description", ogd), ("og:image", img), ("og:image:alt", alt_render(f["img"]))):
        p = re.sub(rf'<meta property="{k}" content="[^"]*">', f'<meta property="{k}" content="{e(v)}">', p, 1)
    for k, v in (("twitter:title", ogt), ("twitter:description", ogd), ("twitter:image", img)):
        p = re.sub(rf'<meta name="{k}" content="[^"]*">', f'<meta name="{k}" content="{e(v)}">', p, 1)
    nuovo = dict(json_block)
    nuovo["@graph"] = jsonld(graph_tpl, f, s, faq, tit, desc)
    p = p.replace(JSON_TESTO, "\n" + json.dumps(nuovo, ensure_ascii=False, indent=2) + "\n", 1)
    # selettore lingua: IT su questa pagina; per le fiere estere EN e cinese alle pagine Europa
    p = p.replace('href="/stand-sps-italia/" hreflang="it"', f'href="/stand-{f["k"]}/" hreflang="it"')
    if f["estero"]:
        p = p.replace('href="/en/exhibition-stand-builder-italy/" hreflang="en"', 'href="/en/exhibition-stand-builder-europe/" hreflang="en"')
        p = p.replace('href="/zh/italy-exhibition-stand/" hreflang="zh-Hans"', 'href="/zh/europe-exhibition-stand/" hreflang="zh-Hans"')
        p = p.replace('href="/zh-hant/italy-exhibition-stand/" hreflang="zh-Hant"', 'href="/zh-hant/europe-exhibition-stand/" hreflang="zh-Hant"')
        p = p.replace('href="/ar/italy-exhibition-stand/" hreflang="ar"', 'href="/ar/europe-exhibition-stand/" hreflang="ar"') if os.path.isdir(os.path.join(RADICE, "ar/europe-exhibition-stand")) else p
    for h in set(re.findall(r'href="(/[^"#?]*)"', main)):
        if not os.path.exists(os.path.join(RADICE, h.strip("/"), "index.html")) and h != "/" and not any(h == f"/stand-{x['k']}/" for x in F):
            raise SystemExit(f"{f['k']}: link interno inesistente {h}")
    i, j = p.index('<main id="main">'), p.index("</main>") + len("</main>")
    p = p[:i] + main + p[j:]
    pulita = re.sub(r'<script type="application/ld\+json">.*?</script>', "", p.replace(main, ""), flags=re.S)  # SPS Italia citata nei testi e nelle FAQ e' voluta
    resto = re.sub(r"SPS[ -]?Italia|sps-italia|spsitalia", "", pulita, flags=re.I)
    if resto != pulita:
        raise SystemExit(f"{f['k']}: nel modello resta un riferimento a SPS Italia, controllare")
    # hreflang e selettore verso le versioni tradotte (strumenti/genera-fiere-lingue.py)
    p = LINGUE.aggiorna_head_e_selettore(p, LINGUE.versioni(f["k"]), "it")
    out = os.path.join(RADICE, f"stand-{f['k']}", "index.html")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    vecchio = open(out, encoding="utf-8").read() if os.path.exists(out) else None
    if vecchio:  # non cambiare la data di pubblicazione rigenerando
        m = re.search(r'"datePublished": "([0-9-]+)"', vecchio)
        if m:
            p = p.replace(f'"datePublished": "{OGGI}"', f'"datePublished": "{m.group(1)}"', 1)
    if p != vecchio:
        open(out, "w", encoding="utf-8").write(p)
        return True
    return False


import importlib.util  # noqa: E402
_spec = importlib.util.spec_from_file_location("genera_fiere_lingue", os.path.join(RADICE, "strumenti", "genera-fiere-lingue.py"))
LINGUE = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(LINGUE)

modello = open(MODELLO, encoding="utf-8").read()
mj = re.search(r'<script type="application/ld\+json">(.*?)</script>', modello, re.S)
JSON_TESTO = mj.group(1)
json_block = json.loads(JSON_TESTO)
graph_tpl = json_block["@graph"]
ml = re.search(r"<!--fr-legno-->.*?<!--/fr-legno-->", modello, re.S)
LEGNO = ml.group(0) if ml else ""
mr = re.search(r'<section id="richiesta" class="fr-req-sec">\n(.*?)\n</section>', modello, re.S)
RICHIESTA = re.sub(r'(id="richiesta-fiera" placeholder=" " required value=")[^"]*(")', r"\1__REQ__\2", mr.group(1))

solo = set(sys.argv[1:])
fatte = [f["k"] for f in F if (not solo or f["k"] in solo) and genera(f, modello, graph_tpl, json_block)]
print(f"{len(fatte)} pagine scritte:", ", ".join(fatte) or "nessuna")


# ---------------------------------------------------------------------------
# Collegamenti (idempotente): sitemap, llms.txt, calendario, pagine hub.
# Va rilanciato anche dopo migra-da-danovatech.py, che riscrive calendario e hub.
CITTA_HUB = {"Milano": "milano", "Bologna": "bologna", "Rimini": "rimini", "Verona": "verona", "Parma": "parma",
             "Torino": "torino", "Bari": "bari", "Bolzano": "bolzano", "Riva del Garda": "riva-del-garda"}
PAESE_HUB = {"Germania": "germania", "Svizzera": "svizzera"}


def _scrivi(percorso, nuovo):
    vecchio = open(percorso, encoding="utf-8").read()
    if nuovo != vecchio:
        open(percorso, "w", encoding="utf-8").write(nuovo)
        return True
    return False


def _blocco(testo, nome, contenuto, prima_di):
    a, b = f"<!--{nome}-->", f"<!--/{nome}-->"
    testo = re.sub(re.escape(a) + r".*?" + re.escape(b) + r"\n?", "", testo, flags=re.S)
    i = testo.find(prima_di)
    if i < 0:
        return testo
    return testo[:i] + a + contenuto + b + "\n" + testo[i:]


def collega():
    cambiati = []
    pagine = [(f, SEDI[f["sede"]]) for f in F]
    # sitemap
    p = os.path.join(RADICE, "sitemap.xml")
    sm = open(p, encoding="utf-8").read()
    nuove = ""
    for f, s in pagine:
        url = f"{SITO}/stand-{f['k']}/"
        if f"<loc>{url}</loc>" in sm:
            continue
        nuove += (f"  <url>\n    <loc>{url}</loc>\n    <lastmod>{OGGI}</lastmod>\n"
                  f"    <image:image><image:loc>{SITO}/assets/img/stand/og/{f['img']}.jpg</image:loc></image:image>\n"
                  f'    <xhtml:link rel="alternate" hreflang="it" href="{url}"/>\n'
                  f'    <xhtml:link rel="alternate" hreflang="x-default" href="{url}"/>\n  </url>\n')
    if nuove and _scrivi(p, sm.replace("</urlset>", nuove + "</urlset>")):
        cambiati.append("sitemap.xml")
    # llms.txt: un elenco breve, una riga per fiera
    p = os.path.join(RADICE, "llms.txt")
    ll = open(p, encoding="utf-8").read()
    righe = "\n### Stand per altre fiere in Italia e in Europa (allestitore per singola fiera)\n\n" + "\n".join(
        f"- [Stand {f['nome']}: allestitore a {s['c']}]({SITO}/stand-{f['k']}/): {f['sett']}, {s['q']} ({s['p']}). "
        f"Prossima edizione: {f['date']}."
        for f, s in sorted(pagine, key=lambda x: x[0]["nome"].lower())) + "\n"
    ll = re.sub(r"\n?<!--ds-fiere-nuove-->.*?<!--/ds-fiere-nuove-->\n?", "", ll, flags=re.S)
    m = re.search(r"\n## (?!Italiano)", ll[ll.find("## Italiano"):]) if "## Italiano" in ll else None
    pos = ll.find("## Italiano") + m.start() if m else len(ll)
    ll = ll[:pos] + "\n<!--ds-fiere-nuove-->" + righe + "<!--/ds-fiere-nuove-->\n" + ll[pos:]
    if _scrivi(p, ll):
        cambiati.append("llms.txt")
    # calendario: nome cliccabile e pulsante "Scheda stand" sulle fiere che ora hanno la pagina
    p = os.path.join(RADICE, "calendario-fiere", "index.html")
    cal = open(p, encoding="utf-8").read()
    per_nome = {re.sub(r"\W", "", f["nome"].lower()): f for f in F}
    alias = {"wtmworldtravelmarket": "wtm-london", "iseintegratedsystemseurope": "ise", "salonedelmobilemilanoeuroluce": None}

    def link_cal(m):
        li = m.group(0)
        if "Scheda stand" in li:
            return li
        h = re.search(r"<h4>([^<]+)</h4>", li)
        if not h:
            return li
        chiave = re.sub(r"\W", "", html.unescape(h.group(1)).lower())
        chiave = re.sub(r"(gennaio|febbraio|settembre|giugno)$", "", chiave)
        f = per_nome.get(chiave) or next((x for x in F if x["k"] == alias.get(chiave)), None)
        if not f:
            return li
        url = f"/stand-{f['k']}/"
        li = li.replace(h.group(0), f'<h4><a href="{url}">{h.group(1)}</a></h4>', 1)
        return re.sub(r'(<button type="button" class="cal-btn"[^>]*>Richiedi lo stand</button>)',
                      rf'\1<a class="cal-btn g" href="{url}">Scheda stand</a>', li, 1)
    cal2 = re.sub(r'<li class="cal-ev".*?</li>', link_cal, cal, flags=re.S)
    if _scrivi(p, cal2):
        cambiati.append("calendario-fiere (%d schede)" % (cal2.count("Scheda stand") - cal.count("Scheda stand")))
    # pagine hub: sezione "Stand per le fiere di ..." prima di "Approfondisci"
    gruppi = {}
    for f, s in pagine:
        hubs = []
        if s["c"] in CITTA_HUB:
            hubs.append(f"allestimenti-fieristici-{CITTA_HUB[s['c']]}")
        if s["p"] in PAESE_HUB:
            hubs.append(f"allestimenti-fieristici-{PAESE_HUB[s['p']]}")
        if f["estero"]:
            hubs.append("allestimenti-fieristici-estero")
        for h in hubs:
            gruppi.setdefault(h, []).append(f)
    for h, ff in gruppi.items():
        p = os.path.join(RADICE, h, "index.html")
        if not os.path.exists(p):
            continue
        t = open(p, encoding="utf-8").read()
        dove = h.replace("allestimenti-fieristici-", "").replace("-", " ").title()
        tit = "all'estero" if h.endswith("estero") else ("in " if dove in ("Germania", "Svizzera") else "a ") + dove
        links = "".join(f'<a href="/stand-{f["k"]}/">Stand {e(f["nome"])}</a>' for f in sorted(ff, key=lambda x: x["nome"].lower()))
        sez = (f'<section id="stand-fiere">\n  <div class="wrap">\n    <div class="sec-head"><h2 class="title" data-rv="up">Stand per le fiere {tit}</h2>'
               f'<p class="lead" data-rv="up">Per ogni fiera una pagina con date, quartiere, cosa serve allo stand e tempi di preparazione.</p></div>\n'
               f'    <div class="pg-altri" data-rv="up">{links}</div>\n  </div>\n</section>\n')
        t2 = _blocco(t, "ds-fiere-nuove", sez, '<section id="altri">')
        if _scrivi(p, t2):
            cambiati.append(h)
    print("collegamenti aggiornati:", ", ".join(cambiati) or "nessuno")


if not solo:
    collega()
    # pagine tradotte: le rigenera e rimette hreflang e selettore sulle pagine italiane appena riscritte
    import subprocess
    subprocess.run([sys.executable, os.path.join(RADICE, "strumenti", "genera-fiere-lingue.py")], check=True)
