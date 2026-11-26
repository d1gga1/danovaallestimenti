#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Pagine fiera tradotte (24/11/2026) per le 91 fiere di strumenti/dati_fiere_nuove*.py.

Testi d'interfaccia: strumenti/traduzioni/ui.py. Testi delle fiere: strumenti/traduzioni/fiere_<lingua>.py.
Per ogni fiera tradotta crea /<lingua>/<slug>/ (slug in ui.py) e collega tutte le versioni della stessa fiera:
hreflang nell'head, selettore lingua (desktop e mobile), sitemap con gli alternate, llms.txt.
Le lingue senza traduzione restano nel selettore con il link alla pagina generale di quella lingua.
Idempotente. Uso: python3 strumenti/genera-fiere-lingue.py   (lo lancia anche genera-fiere-nuove.py alla fine)
"""
import glob, html, importlib, json, os, re, sys
from datetime import date

RADICE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RADICE, "strumenti"))
sys.path.insert(0, os.path.join(RADICE, "strumenti", "traduzioni"))
SITO = "https://danovastand.com"
OGGI = date.today().isoformat()
e = lambda t: html.escape(t, quote=True)
txt = lambda t: re.sub(r"<[^>]+>", "", t)
FRECCIA = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 12h14M13 6l6 6-6 6"></path></svg>'
HREFLANG = {"zh": "zh-Hans", "zh-hant": "zh-Hant"}  # cartella -> codice hreflang

F, SEDI = [], {}
for _m in sorted(glob.glob(os.path.join(RADICE, "strumenti", "dati_fiere_nuove*.py"))):
    _d = importlib.import_module(os.path.basename(_m)[:-3])
    F += _d.F
    SEDI.update(getattr(_d, "SEDI", {}))
FK = {f["k"]: f for f in F}
from ui import UI  # noqa: E402

TRAD = {}
for lang in UI:
    # fiere_<lingua>.py, fiere_<lingua>_2.py, ... (i testi di una lingua possono stare in piu' file)
    for p in sorted(glob.glob(os.path.join(RADICE, "strumenti", "traduzioni", f"fiere_{lang}.py")) +
                    glob.glob(os.path.join(RADICE, "strumenti", "traduzioni", f"fiere_{lang}_*.py"))):
        T = importlib.import_module(os.path.basename(p)[:-3]).T
        TRAD.setdefault(lang, {}).update({k: v for k, v in T.items() if k in FK})


def leggi(p):
    return open(os.path.join(RADICE, p), encoding="utf-8").read()


def scrivi(p, testo):
    p = os.path.join(RADICE, p)
    vecchio = open(p, encoding="utf-8").read() if os.path.exists(p) else None
    if vecchio is not None:
        m = re.search(r'"datePublished": "([0-9-]+)"', vecchio)
        if m:
            testo = testo.replace(f'"datePublished": "{OGGI}"', f'"datePublished": "{m.group(1)}"', 1)
    if testo != vecchio:
        os.makedirs(os.path.dirname(p), exist_ok=True)
        open(p, "w", encoding="utf-8").write(testo)
        return True
    return False


def url_lingua(lang, k):
    return "/" + UI[lang]["slug"].format(k=k) + "/"


def versioni(k):
    """{hreflang: percorso} di tutte le versioni esistenti della fiera k."""
    v = {"it": f"/stand-{k}/"}
    for lang, T in TRAD.items():
        if k in T:
            v[HREFLANG.get(lang, lang)] = url_lingua(lang, k)
    return v


def alternate_head(v):
    righe = "".join(f'<link rel="alternate" hreflang="{h}" href="{SITO}{u}">\n' for h, u in v.items())
    return righe + f'<link rel="alternate" hreflang="x-default" href="{SITO}{v["it"]}">\n'


def aggiorna_head_e_selettore(p, v, corrente):
    """hreflang nell'head e link del selettore (desktop e mobile) per le lingue che hanno una versione."""
    p = re.sub(r'(<link rel="alternate" hreflang="[^"]+" href="[^"]+">\n)+', lambda _: alternate_head(v), p, count=1)

    def sel(m):
        blocco = m.group(0)
        for h, u in v.items():
            blocco = re.sub(rf'<a href="[^"]*" hreflang="{re.escape(h)}"( aria-current="page")?>',
                            f'<a href="{u}" hreflang="{h}"' + (' aria-current="page"' if h == corrente else "") + ">", blocco)
        if corrente not in v:
            return blocco
        # una sola lingua corrente
        blocco = re.sub(r' aria-current="page"', "", blocco)
        return re.sub(rf'(<a href="[^"]*" hreflang="{re.escape(corrente)}")>', r'\1 aria-current="page">', blocco, 1)
    p = re.sub(r'<span class="lang-links">.*?</span>', sel, p, flags=re.S)
    p = re.sub(r'<div class="mob-lang-links">.*?</div>', sel, p, flags=re.S)
    return p


# Descrizione dell'evento nei dati strutturati (Search Console, campo 'description')
EVENT_DESC = {
    "en": "{nome}: trade fair at {q}, {citta}.",
    "de": "{nome}: Fachmesse in {q}, {citta}.",
    "fr": "{nome} : salon professionnel à {q}, {citta}.",
    "es": "{nome}: feria profesional en {q}, {citta}.",
    "pt": "{nome}: feira profissional em {q}, {citta}.",
    "nl": "{nome}: vakbeurs in {q}, {citta}.",
    "pl": "{nome}: targi branżowe – {q}, {citta}.",
}


def pagina(lang, f, t):
    U, s = UI[lang], SEDI[f["sede"]]
    k, nome, anno = f["k"], t.get("nome", f["nome"]), f["start"][:4]
    citta = U["citta"].get(s["c"], s["c"])
    paese = U["paesi"].get(s["p"], s["p"])
    q = s["q"]
    fmt = dict(nome=nome, anno=anno, citta=citta, q=q, paese=paese, date=t["date"], sett=t["sett"].lower(), k=k)
    url = SITO + url_lingua(lang, k)
    tit = next((x.format(**fmt) for x in U["titolo"] if len(html.escape(x.format(**fmt), quote=False)) <= 62), U["titolo"][-1].format(**fmt))
    desc = U["desc"].format(**fmt)
    if len(desc) > 158:
        desc = U["desc_corta"].format(**fmt)
    if len(desc) > 160:  # 24/11/2026: nomi lunghi, solo la prima parte del nome
        desc = U["desc_corta"].format(**dict(fmt, nome=nome.split(" – ")[0]))
    img, alt = f["img"], U["alt"].format(**fmt)
    p = leggi(U["modello"])
    # ---- head
    p = re.sub(r"<title>.*?</title>", f"<title>{html.escape(tit, quote=False)}</title>", p, 1, re.S)
    p = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{e(desc)}">', p, 1)
    p = re.sub(r'<link rel="canonical" href="[^"]*">', f'<link rel="canonical" href="{url}">', p, 1)
    p = re.sub(r'<meta property="og:locale:alternate"[^>]*>\n', "", p)
    og = {"og:url": url, "og:title": U["og_t"].format(**fmt), "og:description": U["og_d"].format(**fmt),
          "og:image": f"{SITO}/assets/img/stand/og/{img}.jpg", "og:image:alt": alt, "og:type": "website"}
    for kk, vv in og.items():
        p = re.sub(rf'<meta property="{kk}" content="[^"]*">', f'<meta property="{kk}" content="{e(vv)}">', p, 1)
    for kk, vv in (("twitter:title", og["og:title"]), ("twitter:description", og["og:description"]), ("twitter:image", og["og:image"])):
        p = re.sub(rf'<meta name="{kk}" content="[^"]*">', f'<meta name="{kk}" content="{e(vv)}">', p, 1)
    if "/assets/css/fiere.css" not in p:
        p = p.replace('<link rel="stylesheet" href="/assets/css/site.css">', '<link rel="stylesheet" href="/assets/css/site.css">\n<link rel="stylesheet" href="/assets/css/fiere.css">', 1)
    if "fiere-richiesta.js" not in p:
        p = p.replace('<script src="/assets/js/contatto.js', '<script src="/assets/js/fiere-richiesta.js?v=20261124" defer></script>\n<script src="/assets/js/contatto.js', 1)
    p = p.replace("fiere-richiesta.js?v=20261014", "fiere-richiesta.js?v=20261124")
    # ---- JSON-LD
    mj = re.search(r'<script type="application/ld\+json">(.*?)</script>', p, re.S)
    blocco = json.loads(mj.group(1))
    graph = blocco["@graph"] if "@graph" in blocco else [blocco]
    org = next(n for n in graph if "Organization" in str(n.get("@type")) and str(n.get("@id", "")).endswith("#organization"))
    faq = list(t["qa"]) + [(U["q_costo"].format(**fmt), U["a_costo"].format(**fmt))]
    ev = {"@type": "BusinessEvent", "name": nome, "startDate": f["start"] if f["conf"] else f["start"][:7], "url": f["sito"],
          "eventStatus": "https://schema.org/EventScheduled", "eventAttendanceMode": "https://schema.org/OfflineEventAttendanceMode",
          "location": {"@type": "Place", "name": q, "address": {"@type": "PostalAddress", "streetAddress": s["via"], "addressLocality": citta, "addressCountry": s["cc"]},
                       "geo": {"@type": "GeoCoordinates", "latitude": s["lat"], "longitude": s["lon"]}},
          "organizer": {"@type": "Organization", "name": nome, "url": f["sito"]}}
    # Search Console 26/11/2026 (Dati strutturati Eventi): campi 'image', 'description', 'performer'
    ev["description"] = EVENT_DESC.get(lang, EVENT_DESC["en"]).format(**fmt)
    ev["image"] = [og["og:image"]]
    ev["performer"] = dict(ev["organizer"])
    # endDate sempre presente (Search Console): senza data di fine si usa il mese di inizio
    ev["endDate"] = f["end"] or (f["start"] if f["conf"] else f["start"][:7])
    crumbs = [(SITO + h, n) for h, n in U["crumbs"]]
    nuovo = {"@context": "https://schema.org", "@graph": [org,
        {"@type": "WebPage", "@id": url + "#webpage", "url": url, "name": tit, "description": desc, "isPartOf": {"@id": f"{SITO}/#website"},
         "breadcrumb": {"@id": url + "#breadcrumb"}, "inLanguage": U["html_lang"], "datePublished": OGGI, "dateModified": OGGI,
         "about": {"@id": url + "#service"}, "mentions": [ev],
         "primaryImageOfPage": {"@type": "ImageObject", "url": og["og:image"]}},
        {"@type": "BreadcrumbList", "@id": url + "#breadcrumb", "itemListElement":
            [{"@type": "ListItem", "position": i + 1, "name": n, "item": h} for i, (h, n) in enumerate(crumbs)] +
            [{"@type": "ListItem", "position": len(crumbs) + 1, "name": U["crumb_ultimo"].format(**fmt)}]},
        {"@type": "Service", "@id": url + "#service", "name": U["crumb_ultimo"].format(**fmt), "serviceType": U["og_t"].format(**fmt).split(" — ")[0],
         "description": desc, "provider": {"@id": f"{SITO}/#organization"}, "availableLanguage": ["Italian", "English"],
         "areaServed": [{"@type": "City", "name": citta}, {"@type": "Country", "name": paese}],
         "hasOfferCatalog": {"@type": "OfferCatalog", "name": U["crumb_ultimo"].format(**fmt), "itemListElement":
             [{"@type": "Offer", "itemOffered": {"@type": "Service", "name": o}} for o in t["off"]]}},
        {"@type": "FAQPage", "@id": url + "#faq", "isPartOf": {"@id": url + "#webpage"}, "inLanguage": U["html_lang"],
         "mainEntity": [{"@type": "Question", "name": a, "acceptedAnswer": {"@type": "Answer", "text": txt(b)}} for a, b in faq]}]}
    p = p.replace(mj.group(1), "\n" + json.dumps(nuovo, ensure_ascii=False, indent=2) + "\n", 1)
    # ---- main
    nota = U["nota_conf"] if f["conf"] else U["nota_nonconf"]
    sito_lbl = re.sub(r"^https?://", "", f["sito"]).rstrip("/")
    esig = "\n".join(f"      <li><b>{e(b)}</b> {e(x)}</li>" for b, x in t["esig"])
    off = "\n".join(f"      <li><b>{e(o)}.</b></li>" for o in t["off"])
    faq_h = "\n".join(f'      <details data-rv="up"><summary>{e(a)}<span class="pm"></span></summary>\n        <div class="ans"><p>{b}</p></div></details>' for a, b in faq)
    estero = ""
    if s["cc"] != "IT":
        estero = (f'<section id="estero">\n  <div class="wrap">\n    <div class="sec-head">\n      <h2 class="title" data-rv="up">{e(U["h_estero"].format(**fmt))}</h2>\n'
                  f'    </div>\n    <div class="pg-testo" data-rv="up">\n      <p>{e(U["estero"].format(**fmt))}</p>\n    </div>\n  </div>\n</section>\n')
    altri, visti = [], set()
    for kk in [x for x in TRAD[lang] if x != k and FK[x]["sett"] == f["sett"]] + [x for x in TRAD[lang] if x != k and FK[x]["sede"] == f["sede"]] + [x for x in TRAD[lang] if x != k]:
        if kk not in visti and len(visti) < 5:
            visti.add(kk)
            altri.append((url_lingua(lang, kk), U["crumb_ultimo"].format(nome=TRAD[lang].get(kk, {}).get("nome", FK[kk]["nome"]))))
    altri += U["altri_fissi"]
    altri_h = "\n".join(f'      <a href="{h}">{e(n)}</a>' for h, n in altri)
    crumbs_h = "<em>/</em>".join(f'<a href="{h}">{e(n)}</a>' for h, n in U["crumbs"]) + f"<em>/</em>{e(U['crumb_ultimo'].format(**fmt))}"
    legno = "\n".join(f'      <article class="pg-card" data-tilt data-rv="blur">\n        <span class="n">{i:02d}</span>\n        <h3>{e(a)}</h3>\n        <p>{e(b)}</p>\n      </article>' for i, (a, b) in enumerate(U["legno"], 1))
    spazi = "".join(f"<option>{e(x)}</option>" for x in U["f_spazi"])
    req = f"{nome} – {citta}, {t['date']}"
    pt = "".join(f"<li>{e(x)}</li>" for x in U["req_pt"])
    chi = f"\n      <div><dt>{e(U['l_pub'])}</dt><dd>{e(t['pub'])}</dd></div>" if t.get("pub") else ""
    main = f'''<main id="main">

<div class="wrap pg-crumbs">
  {crumbs_h}
</div>

<section class="pg-hero">
  <div class="wrap">
    <div class="eyebrow mono" data-scramble>{e(U["eyebrow"].format(**fmt))}</div>
    <h1 data-rv="up">{U["h1"].format(**{**fmt, "nome": e(nome), "q": e(q)})}</h1>
    <p class="lead" data-rv="up">{e(t["lead"])}</p>
    <div class="fr-dates" data-rv="up"><span>{e(nome)}: {e(t["date"])}</span><span>{e(q)}, {e(citta)}</span></div>
    <div class="hero-cta" data-rv="up">
      <a href="#richiesta" class="btn btn-p" data-mag><span class="sheen"></span><span class="lbl">{e(U["btn_req"].format(**fmt))}</span>
        {FRECCIA}</a>
      <a href="#esigenze" class="btn btn-g" data-mag><span class="lbl">{e(U["btn_esig"])}</span></a>
    </div>
  </div>
  <div class="fr-hero-vis fr-hero-foto"><picture><source media="(max-width:1180px)" srcset="data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7"><img src="/assets/img/stand/{img}-800.webp" srcset="/assets/img/stand/{img}-800.webp 800w, /assets/img/stand/{img}-1200.webp 1200w" sizes="(max-width:1180px) 0px, 440px" alt="{e(alt)}" width="800" height="600" fetchpriority="high" decoding="async"></picture></div>
</section>
<section id="scheda">
  <div class="wrap">
    <div class="sec-head">
      <h2 class="title" data-rv="up">{e(U["glance"].format(**fmt))}</h2>
      <p class="lead" data-rv="up">{e(nota)}</p>
    </div>
    <dl class="fr-scheda" data-rv="up">
      <div><dt>{e(U["l_fiera"])}</dt><dd>{e(nome)}</dd></div>
      <div><dt>{e(U["l_dove"])}</dt><dd>{e(q)}, {e(citta)} ({e(paese)})<br><small>{e(s["via"])}</small></dd></div>
      <div><dt>{e(U["l_ed"])}</dt><dd>{e(t["date"])}</dd></div>
      <div><dt>{e(U["l_cad"])}</dt><dd>{e(t["cad"])}</dd></div>
      <div><dt>{e(U["l_sett"])}</dt><dd>{e(t["sett"])}</dd></div>{chi}
      <div><dt>{e(U["l_sito"])}</dt><dd><a href="{f["sito"]}" rel="noopener" target="_blank">{e(sito_lbl)}</a></dd></div>
      <div><dt>{e(U["l_serv"])}</dt><dd>{e(U["serv"].format(**fmt))}</dd></div>
    </dl>
  </div>
</section>
<section id="fiera">
  <div class="wrap">
    <div class="sec-head">
      <h2 class="title" data-rv="up">{U["h_fiera"].format(**{**fmt, "nome": e(nome)})}</h2>
    </div>
    <div class="pg-testo" data-rv="up">
      <p>{e(t["intro"][0])}</p>
      <p>{e(t["intro"][1])}</p>
    </div>
  </div>
</section>
<section id="esigenze">
  <div class="wrap">
    <div class="sec-head">
      <h2 class="title" data-rv="up">{e(U["h_esig"].format(**fmt))}</h2>
    </div>
    <ul class="pg-lista" data-rv="up">
{esig}
    </ul>
  </div>
</section>
<section id="cosa">
  <div class="wrap">
    <div class="sec-head">
      <h2 class="title" data-rv="up">{e(U["h_cosa"].format(**fmt))}</h2>
      <p class="lead" data-rv="up">{e(U["lead_cosa"].format(**fmt))}</p>
    </div>
    <ul class="pg-lista" data-rv="up">
{off}
    </ul>
  </div>
</section>
{estero}<section id="tempi">
  <div class="wrap">
    <div class="sec-head">
      <h2 class="title" data-rv="up">{e(U["h_tempi"].format(**fmt))}</h2>
    </div>
    <div class="pg-testo" data-rv="up">
      <p>{e(t["tempi"])}</p>
      <p>{U["cal"]}</p>
    </div>
  </div>
</section>
<!--fr-legno--><section id="legno">
  <div class="wrap">
    <div class="sec-head">
      <div class="eyebrow mono">{e(U["legno_eye"])}</div>
      <h2 class="title" data-rv="up">{U["legno_h"]}</h2>
      <p class="lead" data-rv="up">{e(U["legno_p"])}</p>
    </div>
    <div class="pg-cards">
{legno}
    </div>
  </div>
</section>
<!--/fr-legno-->
<section id="richiesta" class="fr-req-sec">
  <div class="wrap">
    <div class="fr-req-box" data-rv="up">
      <div class="fr-req-txt">
        <h2 class="title">{e(U["req_h"])}</h2>
        <p>{e(U["req_p"])}</p>
        <ul class="fr-req-pt">{pt}</ul>
      </div>
      <form class="fr-req" novalidate>
        <div class="fld"><input type="text" name="fiera" id="richiesta-fiera" placeholder=" " required value="{e(req)}" autocomplete="off"><label for="richiesta-fiera">{e(U["f_fiera"])}</label></div>
        <div class="fr-req-2">
          <div class="fld"><input type="text" name="mq" id="richiesta-mq" placeholder=" " inputmode="numeric"><label for="richiesta-mq">{e(U["f_mq"])}</label></div>
          <div class="fld"><select name="spazio" id="richiesta-spazio"><option value="" selected hidden></option>{spazi}</select><label for="richiesta-spazio">{e(U["f_spazio"])}</label></div>
        </div>
        <div class="fr-req-2">
          <div class="fld"><input type="text" name="nome" id="richiesta-nome" placeholder=" " required autocomplete="name"><label for="richiesta-nome">{e(U["f_nome"])}</label></div>
          <div class="fld"><input type="text" name="azienda" id="richiesta-azienda" placeholder=" " required autocomplete="organization"><label for="richiesta-azienda">{e(U["f_azienda"])}</label></div>
        </div>
        <div class="fr-req-2">
          <div class="fld"><input type="tel" name="tel" id="richiesta-tel" placeholder=" " required inputmode="tel" autocomplete="tel"><label for="richiesta-tel">{e(U["f_tel"])}</label></div>
          <div class="fld"><input type="email" name="email" id="richiesta-email" placeholder=" " autocomplete="email"><label for="richiesta-email">{e(U["f_email"])}</label></div>
        </div>
        <div class="fld"><textarea name="note" id="richiesta-note" placeholder=" "></textarea><label for="richiesta-note">{e(U["f_note"])}</label></div>
        <p class="fr-req-err" role="alert"></p>
        <button type="submit" class="btn btn-p" data-mag><span class="sheen"></span><span class="lbl">{e(U["f_invia"])}</span>
          {FRECCIA}</button>
        <p class="form-note">{U["f_nota"]}</p>
      </form>
    </div>
  </div>
</section>
<section id="faq">
  <div class="wrap">
    <div class="sec-head">
      <div class="eyebrow mono" data-scramble>{e(U["faq_eye"])}</div>
      <h2 class="title" data-rv="up">{U["faq_h"]}</h2>
    </div>
    <div class="faq">
{faq_h}
    </div>
  </div>
</section>
<section class="pg-cta">
  <div class="wrap">
    <div class="box" data-rv="up">
      <h2 class="title">{e(U["cta_h"].format(**fmt))}</h2>
      <p>{e(U["cta_p"])}</p>
      <a href="#richiesta" class="btn btn-p" data-mag><span class="sheen"></span><span class="lbl">{e(U["cta_btn"])}</span>
        {FRECCIA}</a>
    </div>
  </div>
</section>
<section id="altri">
  <div class="wrap">
    <div class="sec-head"><h2 class="title" data-rv="up">{e(U["altri_h"])}</h2></div>
    <div class="pg-altri" data-rv="up">
{altri_h}
    </div>
  </div>
</section>

</main>'''
    i, j = p.index('<main id="main">'), p.index("</main>") + len("</main>")
    p = p[:i] + main + p[j:]
    # selettore: base = quello della pagina italiana della fiera (pagine generali per le lingue senza versione)
    it = leggi(f"stand-{k}/index.html")
    for cls in (r'<span class="lang-links">.*?</span>', r'<div class="mob-lang-links">.*?</div>'):
        m_it = re.search(cls, it, re.S)
        if m_it:
            p = re.sub(cls, lambda _: m_it.group(0), p, count=1, flags=re.S)
    return aggiorna_head_e_selettore(p, versioni(k), HREFLANG.get(lang, lang))


def sitemap(cluster):
    p = leggi("sitemap.xml")
    for k, v in cluster.items():
        for h, u in v.items():
            loc = SITO + u
            p = re.sub(r"  <url>\n    <loc>" + re.escape(loc) + r"</loc>.*?</url>\n", "", p, flags=re.S)
            img = FK[k]["img"]
            alt = "".join(f'    <xhtml:link rel="alternate" hreflang="{hh}" href="{SITO}{uu}"/>\n' for hh, uu in v.items())
            alt += f'    <xhtml:link rel="alternate" hreflang="x-default" href="{SITO}{v["it"]}"/>\n'
            p = p.replace("</urlset>", f"  <url>\n    <loc>{loc}</loc>\n    <lastmod>{OGGI}</lastmod>\n"
                          f"    <image:image><image:loc>{SITO}/assets/img/stand/og/{img}.jpg</image:loc></image:image>\n{alt}  </url>\n</urlset>")
    return scrivi("sitemap.xml", p)


def llms():
    p = leggi("llms.txt")
    p = re.sub(r"\n?<!--ds-fiere-lingue-->.*?<!--/ds-fiere-lingue-->\n?", "", p, flags=re.S)
    titoli = {"en": "Stand builder pages by trade fair (English)", "de": "Messestand-Seiten nach Messe (Deutsch)", "fr": "Pages standiste par salon (français)", "es": "Páginas de stands por feria (español)"}
    blocco = ""
    for lang, T in TRAD.items():
        U = UI[lang]
        blocco += f"\n### {titoli.get(lang, lang)}\n\n" + "\n".join(
            f"- [{U['crumb_ultimo'].format(nome=T[k].get('nome', FK[k]['nome']))}]({SITO}{url_lingua(lang, k)}): {T[k]['sett']}, {SEDI[FK[k]['sede']]['q']}. {T[k]['date']}."
            for k in sorted(T, key=lambda x: FK[x]["nome"].lower())) + "\n"
    if blocco:
        p = p.rstrip("\n") + "\n\n<!--ds-fiere-lingue-->" + blocco + "<!--/ds-fiere-lingue-->\n"
    return scrivi("llms.txt", p)


if __name__ == "__main__":
    scritte, cluster = [], {}
    for lang, T in TRAD.items():
        for k, t in T.items():
            if scrivi(url_lingua(lang, k).strip("/") + "/index.html", pagina(lang, FK[k], t)):
                scritte.append(url_lingua(lang, k))
            cluster[k] = versioni(k)
    # pagina italiana: hreflang e selettore verso le traduzioni
    it_agg = [k for k, v in cluster.items() if scrivi(f"stand-{k}/index.html", aggiorna_head_e_selettore(leggi(f"stand-{k}/index.html"), v, "it"))]
    print(f"{len(scritte)} pagine tradotte scritte; {len(it_agg)} pagine italiane ricollegate; sitemap {sitemap(cluster)}; llms {llms()}")
