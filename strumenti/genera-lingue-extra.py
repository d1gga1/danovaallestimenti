#!/usr/bin/env python3
"""Tutte le lingue nel selettore + pagine principali nelle lingue extra (22/11/2026).

1. Crea /<lingua>/europe-exhibition-stand/ (pagina principale) per ogni lingua in strumenti/lingue-extra/testi_*.py
   (portoghese, russo, ucraino, polacco, rumeno, ceco, ungherese, greco, bulgaro, croato, albanese, svedese,
   ebraico, persiano, giapponese, coreano, bengalese, punjabi, gujarati, tamil, indonesiano, malese, vietnamita, thai)
   + /<lingua>/ che rimanda li'. Stesso modello grafico delle pagine urdu/hindi (usa genera-pagine-ur-hi.py).
2. Aggiunge le nuove lingue agli hreflang del gruppo "Europa" (IT/EN/ZH/UR/HI...), sitemap, llms.txt, footer.
3. Rifa' il selettore lingua di TUTTE le pagine: tutte le lingue sempre presenti. Se la pagina ha la sua
   traduzione (hreflang) il link porta li', altrimenti alla pagina principale di quella lingua.
4. pagina.js (nomi lingue, RTL) e site.css (menu a tendina su piu' colonne).

Idempotente. Uso:  python3 strumenti/genera-lingue-extra.py
Rilancialo dopo genera-pagine-ur-hi.py (e quindi dopo ogni migra-da-danovatech.py), prima di gruppo-danova.py.
Nuova lingua: aggiungi un blocco in strumenti/lingue-extra/testi_*.py e una riga in ORDINE/CODICE qui sotto.
"""
import glob, html, importlib.util, json, os, re

QUI = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("uh", os.path.join(QUI, "genera-pagine-ur-hi.py"))
UH = importlib.util.module_from_spec(spec); spec.loader.exec_module(UH)
ROOT, SITO, e = UH.ROOT, UH.SITO, html.escape
SLUG = "europe-exhibition-stand"

TESTI = {}
for f in sorted(glob.glob(os.path.join(QUI, "lingue-extra", "testi_*.py"))):
    s = importlib.util.spec_from_file_location(os.path.basename(f)[:-3], f)
    m = importlib.util.module_from_spec(s); s.loader.exec_module(m); TESTI.update(m.TESTI)

# ordine nel menu e pagina principale di ogni lingua
ORDINE = ["it", "en", "de", "fr", "es", "pt", "nl", "sv", "pl", "cs", "hu", "ro", "bg", "hr", "el", "sq", "ru", "uk",
          "tr", "ar", "he", "fa", "ur", "hi", "bn", "pa", "gu", "ta", "zh-Hans", "zh-Hant", "ja", "ko", "id", "ms", "vi", "th"]
MAIN = {"it": "/", "en": "/en/exhibition-stand-builder-italy/", "de": "/de/messebau-italien/", "fr": "/fr/standiste-salon-italie/",
        "es": "/es/montaje-stands-feriales-italia/", "nl": "/nl/standbouw-italie/", "tr": "/tr/italya-fuar-standi/",
        "zh-Hans": "/zh/italy-exhibition-stand/", "zh-Hant": "/zh-hant/italy-exhibition-stand/", "ar": "/ar/italy-exhibition-stand/",
        "ur": "/ur/europe-exhibition-stand/", "hi": "/hi/europe-exhibition-stand/"}
for L in TESTI: MAIN[L] = f"/{L}/{SLUG}/"
CODICE = dict(UH.CODICE, he="HE", fa="FA")
for L in TESTI: CODICE.setdefault(L, L.upper())
NOMI = {"it": "Italiano", "en": "English", "de": "Deutsch", "fr": "Français", "es": "Español", "nl": "Nederlands", "tr": "Türkçe",
        "zh-Hans": "简体中文", "zh-Hant": "繁體中文", "ar": "العربية", "ur": "اردو", "hi": "हिन्दी"}
NOMI.update({L: t["n"] for L, t in TESTI.items()})
RTL = {"ar", "ur", "he", "fa"}
assert set(ORDINE) == set(MAIN), set(ORDINE) ^ set(MAIN)

FIERE = [("Salone del Mobile", "Milano", 0, "salone-del-mobile"), ("Vinitaly", "Verona", 0, "vinitaly"), ("Cosmoprof", "Bologna", 0, "cosmoprof"),
         ("EICMA", "Milano", 0, "eicma"), ("Marmomac", "Verona", 0, "marmomac"), ("MEDICA", "Düsseldorf", 1, "medica"),
         ("Anuga", "Köln", 1, "anuga"), ("Heimtextil", "Frankfurt", 1, "heimtextil"), ("Hannover Messe", "Hannover", 1, "hannover-messe"),
         ("SIAL Paris", "Paris", 2, "sial-paris"), ("Maison&Objet", "Paris", 2, "maison-et-objet"), ("MWC", "Barcelona", 3, "mwc-barcelona"),
         ("Fitur", "Madrid", 3, "fitur"), ("METSTRADE", "Amsterdam", 4, "metstrade")]
EN_LINK = {"bn": "/en/exhibition-stand-builder-for-bangladeshi-companies/", "pa": "/en/exhibition-stand-builder-for-indian-companies/",
           "gu": "/en/exhibition-stand-builder-for-indian-companies/", "ta": "/en/exhibition-stand-builder-for-indian-companies/"}
PAESI_EN = ["Italy", "Germany", "France", "Spain", "Netherlands"]

FONT = {"ja": "'Hiragino Sans','Yu Gothic','Noto Sans JP','Meiryo',sans-serif", "ko": "'Apple SD Gothic Neo','Malgun Gothic','Noto Sans KR',sans-serif",
        "th": "'Noto Sans Thai','Thonburi','Leelawadee UI',Tahoma,sans-serif", "bn": "'Noto Sans Bengali','Kohinoor Bangla','Nirmala UI','Vrinda',sans-serif",
        "pa": "'Noto Sans Gurmukhi','Gurmukhi MN','Nirmala UI','Raavi',sans-serif", "gu": "'Noto Sans Gujarati','Gujarati Sangam MN','Nirmala UI','Shruti',sans-serif",
        "ta": "'Noto Sans Tamil','Tamil Sangam MN','Nirmala UI','Latha',sans-serif", "he": "'Noto Sans Hebrew','Arial Hebrew','Segoe UI',Arial,sans-serif",
        "fa": "'Vazirmatn','Noto Naskh Arabic','Geeza Pro','Segoe UI',Tahoma,sans-serif"}
RTL_CSS = ("[dir=rtl] .dt-lead{text-align:right}[dir=rtl] .fld label{left:auto;right:16px;transform-origin:right;letter-spacing:0!important;text-transform:none!important}"
           "[dir=rtl] .btn svg[fill=currentColor]{transform:none}[dir=rtl] footer li,[dir=rtl] .f-bot span{unicode-bidi:plaintext}"
           "[dir=rtl] a[href^='tel:'],[dir=rtl] a[href^='mailto:']{direction:ltr;unicode-bidi:isolate}")


def stile(L):
    s = f"html[lang={L}] h1,html[lang={L}] h2,html[lang={L}] h3,html[lang={L}] .eyebrow{{letter-spacing:0;text-transform:none}}html[lang={L}] .fld label{{letter-spacing:0!important;text-transform:none!important}}"
    if L in FONT:
        s += (f"html[lang={L}] main,html[lang={L}] footer,html[lang={L}] #mob,html[lang={L}] .links{{font-family:'Inter',{FONT[L]}}}"
              f"html[lang={L}] h1,html[lang={L}] h2,html[lang={L}] h3{{font-family:'Sora',{FONT[L]};line-height:1.4}}html[lang={L}] main p,html[lang={L}] .ans p{{line-height:1.85}}")
    if L in RTL: s += RTL_CSS
    return s


def prepara(L):
    """Inietta i testi nel modulo urdu/hindi e restituisce la pagina."""
    t = TESTI[L]; n1, n2 = t["fm"][5], t["fm"][6]
    UH.T[L] = dict(locale=t["loc"], dir=t["dir"], nome_lingua=t["n"], home=t["home"], nav=[(SLUG, t["hub"])], contatto=t["cont"], parliamo=t["parl"],
                   cta_primary=t["cta"], cta_wa=t["wa"], wa_txt=t["wa_txt"], wa_aria=t["wa_aria"], servizi_title=t["st"], servizi_lead=t["sl"],
                   servizi=t["serv"], faq_title=t["ft"], altri_title=t["at"], cta_text=t["cx"],
                   form=dict(nome=t["fm"][0], email=t["fm"][1], tel=t["fm"][2], msg=t["fm"][3], btn=t["fm"][4],
                             note=f'{e(n1)} <a href="https://wa.me/{UH.WA}" target="_blank" rel="noopener" dir="ltr">+39 388 470 6887</a> ({e(n2)}).'),
                   footer_p=t["fp"], f_stand=t["fs"], f_fiere=t["ff"], f_contatti=t["fc"],
                   f_sedi=f'{e(t["sedi"][0])}: <bdi>Fontanelle (TV) · Trumello (PV)</bdi><br>{e(t["sedi"][1])}: <bdi>Trumello (PV) · Vermezzo con Zelo (MI)</bdi>',
                   f_legal=tuple(t["legal"]))
    UH.STILE[L] = stile(L)
    lista = [(f"{n} – {c}", f"{t['paesi'][i]} · {t['en_pag']}", f"/en/{s}-stand-builder/") for n, c, i, s in FIERE]
    altri = [(EN_LINK.get(L, "/en/exhibition-stand-builder-europe/"), t["en_lab"]), ("/en/exhibition-stand-builder-italy/", "English: Italy"),
             ("/en/exhibiting-at-trade-fairs-in-italy/", "English: exhibiting in Italy")]
    if L in EN_LINK: altri.insert(1, ("/en/exhibition-stand-builder-europe/", "English version"))
    return dict(slug=SLUG, path=f"{L}/{SLUG}", cluster=f"zh/{SLUG}", tipo="hub", title=t["title"], desc=t["desc"], eyebrow=t["eye"], h1=t["h1"],
                lead=t["lead"], img="stand-fiera-estero-padiglione", alt=t["alt"], lista_title=t["lt"], lista_lead=t["ll"], lista=lista,
                why_title=t["wt"], why=t["why"], faq=t["faq"], cta_title=t["ct"], service=t["svc"],
                area=[{"@type": "Country", "name": x} for x in PAESI_EN], altri=altri)


def alts_cluster(src):
    s = UH.leggi(src + "/index.html")
    alts = [(h, u) for h, u in re.findall(r'<link rel="alternate" hreflang="([^"]+)" href="([^"]+)">', s) if h != "x-default"]
    xd = re.search(r'<link rel="alternate" hreflang="x-default" href="([^"]+)">', s).group(1)
    slug = src.split("/", 1)[1]
    gia = {h for h, _ in alts}
    for L in UH.LINGUE: 
        if L not in gia: alts.append((L, f"{SITO}/{L}/{slug}/"))
    if slug == SLUG:
        alts += [(L, f"{SITO}/{L}/{SLUG}/") for L in TESTI if L not in gia]
    return alts, xd


def ld_json(L, p, org):
    t = UH.T[L]; url = f"{SITO}/{p['path']}/"
    g = [org,
         {"@type": "WebPage", "@id": url + "#webpage", "url": url, "name": p["title"], "description": p["desc"], "inLanguage": L,
          "isPartOf": {"@id": SITO + "/#website"}, "about": {"@id": SITO + "/#organization"}, "breadcrumb": {"@id": url + "#breadcrumb"},
          "datePublished": UH.OGGI, "dateModified": UH.OGGI,
          "primaryImageOfPage": {"@type": "ImageObject", "url": f"{SITO}/assets/img/stand/{p['img']}-1200.webp"}},
         {"@type": "BreadcrumbList", "@id": url + "#breadcrumb", "itemListElement": [{"@type": "ListItem", "position": 1, "name": t["home"], "item": url}]},
         {"@type": "Service", "@id": url + "#service", "name": p["service"], "serviceType": "Exhibition stand design and construction",
          "provider": {"@id": SITO + "/#organization"}, "areaServed": p["area"], "inLanguage": L},
         {"@type": "FAQPage", "@id": url + "#faq", "inLanguage": L,
          "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in p["faq"]]}]
    return json.dumps({"@context": "https://schema.org", "@graph": g}, ensure_ascii=False, indent=2)


def footer(L, s):
    t = UH.T[L]
    m = re.search(r"<footer>.*?</footer>", s, re.S); f = m.group(0)
    stand = f'        <li><a href="/{L}/{SLUG}/">{e(t["nav"][0][1])}</a></li>'
    fiere = "\n".join(f'        <li><a href="/en/{sl}-stand-builder/">{e(n)}</a></li>' for n, _, _, sl in FIERE[:8])
    f = re.sub(r"<div><h5>Stands</h5><ul>.*?</ul></div>", lambda _: f'<div><h5>{e(t["f_stand"])}</h5><ul>\n{stand}\n      </ul></div>', f, 1, flags=re.S)
    f = re.sub(r"<div><h5>Trade fairs</h5><ul>.*?</ul></div>", lambda _: f'<div><h5>{e(t["f_fiere"])}</h5><ul>\n{fiere}\n      </ul></div>', f, 1, flags=re.S)
    f = f.replace("<h5>Contact</h5>", f'<h5>{e(t["f_contatti"])}</h5>', 1)
    f = re.sub(r'(<div class="fb">.*?<p>).*?(</p>)', lambda x: x.group(1) + e(t["footer_p"]) + x.group(2), f, 1, flags=re.S)
    f = re.sub(r"<li>Warehouses:.*?</li>", lambda _: f'<li>{t["f_sedi"]}</li>', f, 1, flags=re.S)
    for en_lab, lab in zip((">Privacy Policy<", ">Cookie Policy<", ">Terms of use<", ">Contact<"), t["f_legal"]):
        f = f.replace(en_lab, f">{e(lab)}<", 1)
    return s[:m.start()] + f + s[m.end():]


UH.alts_cluster, UH.ld_json, UH.footer = alts_cluster, ld_json, footer


def redirect(L):
    d = MAIN[L]; rtl = ' dir="rtl"' if L in RTL else ""
    return (f'<!DOCTYPE html>\n<html lang="{L}"{rtl}><head><meta charset="utf-8">\n<title>Danova Stand</title>\n'
            f'<meta name="robots" content="noindex, follow">\n<link rel="canonical" href="{SITO}{d}">\n'
            f'<meta http-equiv="refresh" content="0; url={d}">\n<script>location.replace("{d}")</script>\n'
            f'</head><body>\n<p><a href="{d}">Danova Stand</a></p>\n</body></html>\n')


# ------------------------------------------------------------------ hreflang del gruppo Europa sulle pagine esistenti
def patch_cluster_europa():
    alts, _ = alts_cluster(f"zh/{SLUG}"); n = 0
    for h, u in alts:
        if h in TESTI: continue
        rel = u.replace(SITO + "/", "") + "index.html"
        if not os.path.exists(os.path.join(ROOT, rel)): continue
        s = s0 = UH.leggi(rel); testa = s.split("</head>")[0]
        for L in TESTI:
            if f'hreflang="{L}" href=' not in testa:
                s = s.replace('<link rel="alternate" hreflang="x-default"', f'<link rel="alternate" hreflang="{L}" href="{SITO}/{L}/{SLUG}/">\n<link rel="alternate" hreflang="x-default"', 1)
        if s != s0: UH.scrivi(rel, s); n += 1
    return n


# ------------------------------------------------------------------ selettore lingua su tutte le pagine
def tutte_le_pagine():
    for d, ds, fs in os.walk(ROOT):
        ds[:] = [x for x in ds if not x.startswith(".") and x not in ("strumenti", "render", "private_area", "Claude outputs", "assets", "_google_business")]
        if "index.html" in fs: yield os.path.relpath(os.path.join(d, "index.html"), ROOT)
    if os.path.exists(os.path.join(ROOT, "404.html")): yield "404.html"


def selettore(rel):
    s = UH.leggi(rel); s2 = selettore_html(s, rel)
    return UH.scrivi(rel, s2) if s2 != s else False


def selettore_html(s, rel):
    if 'class="lang-links"' not in s and 'class="mob-lang-links"' not in s: return s
    testa = s.split("</head>")[0]
    m = re.search(r'<html lang="([^"]+)"', s); lang = m.group(1) if m else "it"
    if lang not in MAIN: lang = {"zh": "zh-Hans", "zh-CN": "zh-Hans", "zh-TW": "zh-Hant"}.get(lang, lang)
    alts = {h: u.replace(SITO, "") for h, u in re.findall(r'<link rel="alternate" hreflang="([^"]+)" href="([^"]+)">', testa) if h != "x-default"}
    can = re.search(r'<link rel="canonical" href="([^"]+)">', testa)
    qui = can.group(1).replace(SITO, "") if can else "/" + rel.replace("index.html", "")
    def blocco(mm):
        b = mm.group(0)
        ind = re.search(r"\n([ \t]*)<a ", b); ind = ind.group(1) if ind else "  "
        apri = re.match(r"<(span|div)[^>]*>", b).group(0); tag = re.match(r"<(span|div)", b).group(1)
        righe = []
        for L in ORDINE:
            href = qui if L == lang else alts.get(L, MAIN[L])
            cur = ' aria-current="page"' if L == lang else ""
            righe.append(f'{ind}<a href="{href}" hreflang="{L}"{cur}>{CODICE[L]}</a>')
        chiudi_ind = re.search(r"\n([ \t]*)</" + tag + ">$", b); ci = chiudi_ind.group(1) if chiudi_ind else ""
        return apri + "\n" + "\n".join(righe) + "\n" + ci + f"</{tag}>"
    s2 = re.sub(r'<span class="lang-links">.*?</span>', blocco, s, 1, flags=re.S)
    return re.sub(r'<div class="mob-lang-links">.*?</div>', blocco, s2, 1, flags=re.S)


# ------------------------------------------------------------------ footer "Lingue / Languages"
HI_LI = '<li><a href="/hi/europe-exhibition-stand/" lang="hi">हिन्दी</a></li>'
def li_lingua(L):
    d = ' dir="rtl"' if L in RTL else ""
    return f'<li><a href="/{L}/{SLUG}/" lang="{L}"{d}>{e(TESTI[L]["n"])}</a></li>'

def patch_footer(rel):
    s = UH.leggi(rel)
    if HI_LI not in s: return False
    m = re.search(r"\n([ \t]*)" + re.escape(HI_LI), s); ind = m.group(1)
    mancanti = [L for L in TESTI if f'href="/{L}/{SLUG}/" lang="{L}"' not in s]
    if not mancanti: return False
    s = s.replace(HI_LI, HI_LI + "".join(f"\n{ind}{li_lingua(L)}" for L in mancanti), 1)
    return UH.scrivi(rel, s)


# ------------------------------------------------------------------ js e css
def patch_js_css():
    cambi = []
    p = "assets/js/pagina.js"; s = s0 = UH.leggi(p)
    nomi = "{" + ",".join((f"'{k}'" if "-" in k else k) + ":'" + v.replace("'", "\\'") + "'" for k, v in NOMI.items()) + "}"
    s = re.sub(r"const NOMI=\{[^}]*\};", lambda _: f"const NOMI={nomi};", s, 1)
    s = s.replace("if(/^(ar|ur)$/.test(a.getAttribute('hreflang')))", "if(/^(ar|ur|fa|he)$/.test(a.getAttribute('hreflang')))")
    if s != s0: UH.scrivi(p, s); cambi.append(p)
    p = "assets/css/site.css"; s = UH.leggi(p)
    css = ("/* ds-lingue-extra: menu lingue su piu' colonne (36 lingue) */\n"
           "header .lang-links.ll .ll-menu{display:grid;grid-template-columns:repeat(3,minmax(150px,1fr));column-gap:2px;min-width:0;width:max-content}\n"
           "header .lang-links.ll .ll-menu a{padding:8px 11px}\n"
           "@media (max-width:820px){header .lang-links.ll .ll-menu{grid-template-columns:repeat(2,minmax(140px,1fr));max-height:72vh;overflow-y:auto;"
           "background:rgba(12,10,4,.97);border:1px solid var(--line);border-radius:16px;padding:6px;margin-top:10px}header .lang-links.ll .ll-menu::before{display:none}}\n"
           "#mob .mob-lang-links a{min-width:44px;text-align:center}\n/* /ds-lingue-extra */\n")
    s2 = re.sub(r"/\* ds-lingue-extra.*?/\* /ds-lingue-extra \*/\n", "", s, flags=re.S).rstrip("\n") + "\n" + css
    if s2 != s: UH.scrivi(p, s2); cambi.append(p)
    return cambi


# ------------------------------------------------------------------ sitemap e llms
def sitemap():
    s = s0 = UH.leggi("sitemap.xml")
    alts, xd = alts_cluster(f"zh/{SLUG}")
    righe = "".join(f'\n    <xhtml:link rel="alternate" hreflang="{a}" href="{u}"/>' for a, u in alts) + f'\n    <xhtml:link rel="alternate" hreflang="x-default" href="{xd}"/>'
    urls = {u for _, u in alts}
    # aggiorna le voci gia' presenti del gruppo
    def upd(m):
        blocco = m.group(0); loc = re.search(r"<loc>([^<]+)</loc>", blocco).group(1)
        if loc not in urls: return blocco
        blocco = re.sub(r'\n    <xhtml:link rel="alternate"[^>]*/>', "", blocco)
        return blocco.replace("\n  </url>", righe + "\n  </url>")
    s = re.sub(r"  <url>.*?</url>", upd, s, flags=re.S)
    for L in TESTI:
        url = f"{SITO}/{L}/{SLUG}/"
        if f"<loc>{url}</loc>" in s: continue
        img = "stand-fiera-estero-padiglione"
        s = s.replace("</urlset>", f"  <url>\n    <loc>{url}</loc>\n    <lastmod>{UH.OGGI}</lastmod>\n"
                      f"    <image:image><image:loc>{SITO}/assets/img/stand/{img}-1200.webp</image:loc></image:image>\n"
                      f"    <image:image><image:loc>{SITO}/assets/img/stand/og/{img}.jpg</image:loc></image:image>{righe}\n  </url>\n</urlset>")
    return UH.scrivi("sitemap.xml", s) if s != s0 else False


LLMS_TITOLO = "## Pagine in altre lingue (portoghese, russo, polacco, giapponese, persiano, bengalese...)"
def llms():
    s = UH.leggi("llms.txt")
    righe = [LLMS_TITOLO, "Pagina principale di Danova Stand in ogni lingua: stand chiavi in mano in Italia e in Europa. "
             "Per iscritto (email, WhatsApp, modulo) rispondiamo nella lingua del cliente o in inglese; al telefono italiano, inglese e rumeno.", ""]
    righe += [f"- [{TESTI[L]['title'].split(' | ')[0]}]({SITO}/{L}/{SLUG}/): {TESTI[L]['desc']} ({TESTI[L]['n']})." for L in TESTI]
    blocco = "\n".join(righe)
    if LLMS_TITOLO in s: s2 = re.sub(re.escape(LLMS_TITOLO) + r"\n.*?(?=\n\n## |\Z)", lambda _: blocco, s, 1, flags=re.S)
    else: s2 = s.rstrip("\n") + "\n\n" + blocco
    s2 = s2.rstrip("\n") + "\n"
    return UH.scrivi("llms.txt", s2)


def main():
    tpl = UH.leggi(UH.MODELLO + "/index.html")
    ld = re.search(r'<script type="application/ld\+json">(.*?)</script>', tpl, re.S)
    org = next(x for x in json.loads(ld.group(1))["@graph"] if x.get("@id") == SITO + "/#organization")
    for L in TESTI:
        p = prepara(L)
        rel = p["path"] + "/index.html"
        print(("scritta  " if UH.scrivi(rel, selettore_html(UH.build(L, p, org, tpl), rel)) else "uguale   ") + p["path"])
        UH.scrivi(f"{L}/index.html", redirect(L))
    print("hreflang gruppo Europa aggiornati:", patch_cluster_europa())
    pagine = list(tutte_le_pagine())
    print("selettori lingua aggiornati:", sum(selettore(r) for r in pagine), "su", len(pagine), "pagine")
    print("footer lingue aggiornati:", sum(patch_footer(r) for r in pagine))
    print("js/css:", patch_js_css() or "gia' aggiornati")
    print("sitemap:", sitemap(), " llms.txt:", llms())


if __name__ == "__main__":
    main()
