# -*- coding: utf-8 -*-
"""Pagine del 22 ottobre 2026 (Keyword Planner 22/10): fiere estere e nuove fiere italiane (IT),
le stesse fiere estere in inglese e cinese per gli espositori asiatici, hub Europa EN/ZH,
pagine per paese di provenienza (India, Pakistan, Cina, Bangladesh), Messebau Mailand (DE),
moquette e trasporto/magazzino (IT). Collega le pagine nuove agli hub. Idempotente.
Uso (dalla cartella fiere-generatore):
    python3 build_2610.py
    python3 build_hant.py                       # cinese tradizionale
poi, dalla radice del sito:
    python3 seo-tools/noindex-pagine-lontane.py
    python3 seo-tools/post-build-velocita.py && python3 seo-tools/post-build-contatti.py && python3 seo-tools/schema-licenza-eventi.py
    python3 seo-tools/genera-sitemap.py && python3 seo-tools/genera-feed-e-llms.py && python3 seo-tools/genera-llms-txt.py
"""
import sys, os, re; sys.path.insert(0, os.path.dirname(__file__))
from nuove_common import *
import lib; lib.TODAY = '2026-10-22'
import dati_calendario as DC
import dati_intl as DI, dati_2610_it as DIT, dati_2610_intl as DX, dati_2610_hub as DH
import intl_map as IM
import build_intl as BI
from urllib.parse import quote

ESTERO = "/allestimenti-fieristici-estero/"
PAESE_URL = {"germania": "/allestimenti-fieristici-germania/"}
PAESE_NOME = {"germania": "Germania", "francia": "Francia", "spagna": "Spagna", None: "Europa"}
IT_URL = {d['k']: f"/stand-{d['k']}/" for d in DIT.P3}
OLD_IT = dict(FIERA_PAGES)
ALL_IT_LABEL = {**{k: t for k, t in FIERA_PAGES}, **{d['k']: f"Stand {d.get('short', d['nome'])}" for d in DIT.P3}}
EN_URL = {**{f['k']: f"/en/{f['en']['slug']}/" for f in DI.FAIRS}, **{f['k']: f"/en/{f['en']['slug']}/" for f in DX.FAIRS}}
ZH_URL = {**{f['k']: f"/zh/{f['zh']['slug']}/" for f in DI.FAIRS}, **{f['k']: f"/zh/{f['zh']['slug']}/" for f in DX.FAIRS}}
NAME = {**{f['k']: f['en'].get('short', f['en']['name']) for f in DI.FAIRS}, **{f['k']: f['en']['name'] for f in DX.FAIRS}}
ZNAME = {**{f['k']: f['zh'].get('short', f['zh']['name']) for f in DI.FAIRS}, **{f['k']: f['zh']['short'] for f in DX.FAIRS}}
HUB = {'en': DH.HUB_EN['path'], 'zh': DH.HUB_ZH['path']}
PILL = BI.PILL; GUIDE = BI.GUIDE
COUNTRY_URL = {c['country']: f"/en/{c['slug']}/" for c in DH.COUNTRIES}
W = BI.W
def CARDS(L):
    return [(a, b.replace('with Italian declaration of conformity', 'with declaration of conformity').replace('带意大利合格声明的电气系统', '带合格声明的电气系统')) for a, b in BI.T[L]['cards']]

# ================================================================ IT: pagine fiera
PROC = __import__('build_fiere').PROC
GEN_QA = __import__('build_fiere').GEN_QA

def build_it(d):
    k = d['k']; n = d['nome']; sn = d.get('short', n); P = IT_URL[k]; c = d['citta']; q = d['q']; estero = 'cs' not in d
    qs = [DC.quando(x) for x in d['cal']]
    anno = min(DC.FIERE[x][4][:4] for x in d['cal'])
    dates = ''.join(f'<span>{DC.FIERE[x][1]}: {DC.quando(x)}</span>' for x in d['cal'])
    extra = f'\n    <div class="fr-dates" data-rv="up">{dates}<span>{q}, {c}</span></div>'
    m = hero(f"Stand · {sn}", f'Stand per {n}: <span class="grad">allestimento chiavi in mano</span> a {q}.', d['lead'],
             "Richiedi lo stand per " + sn, "#richiesta", "Cosa serve allo stand", "#esigenze", extra=extra)
    v = DC.V[DC.FIERE[d['cal'][0]][2]]; site = DC.FIERE[d['cal'][0]][7]
    sl = DC.SETT_PAGE.get(d['sett'])
    sett_txt = DC.SETT[d['sett']] + (f' · <a href="{sl}">stand per il settore</a>' if sl else '')
    dove = f"{q}, {c}" + (f" ({PAESE_NOME.get(d.get('paese'), DC.PAESE.get(v[2], ''))})" if estero else '') + f"<br><small>{v[5]}</small>"
    rows = [("Fiera", n), ("Dove", dove), ("Prossima edizione", "<br>".join(f"{DC.FIERE[x][1]}: {DC.quando(x)}" for x in d['cal'])),
            ("Cadenza", d['cad']), ("Settore", sett_txt),
            ("Sito ufficiale", f'<a href="{site}" rel="noopener" target="_blank">{site.split("//")[1].rstrip("/")}</a>'),
            ("La nostra esperienza", f"Allestiamo stand per {sn} e per le fiere del settore in Italia e all'estero.")]
    m += scheda("scheda", f"{sn} in breve", rows, f"Le date sono quelle pubblicate dall'organizzatore (verificate a ottobre 2026): controllale sempre sul sito ufficiale prima di prenotare viaggi e trasporti.")
    m += testo("fiera", f"Cos'è {sn} e <span class=\"grad\">cosa chiede allo stand</span>", None, d['intro'])
    m += testo("esigenze", f"Cosa serve a uno stand per {sn}", None, [], d['esig'])
    m += cards("cosa", "Cosa facciamo per il tuo stand", "Possiamo seguire tutto, dal progetto allo smontaggio, oppure solo la parte che ti manca.", SERVIZI_CARDS(" a " + q))
    if estero:
        t, lst = DIT.ESTERO_TXT
        m += testo("estero", t.format(c=c), None, [], lst)
    m += testo("tempi", f"Quando iniziare a preparare lo stand per {sn}", None,
               [d['tempi'], f"Tutte le date delle prossime fiere, in Italia e in Europa, sono nel nostro <a href=\"{CAL}\">calendario fiere 2026–2027</a>."])
    m += passi("metodo", "Come lavoriamo", f"Dal brief allo stand <span class=\"grad\">pronto a {q}.</span>", None, PROC)
    qa = d['qa'] + [(a.format(n=sn), b) for a, b in GEN_QA]
    rel = []
    if estero:
        p = d.get('paese')
        if p in PAESE_URL: rel.append((f"Allestimenti fieristici in {PAESE_NOME[p]}", PAESE_URL[p]))
        rel.append(("Allestimenti fieristici all'estero", ESTERO))
    elif d['cs'] in CITTA_URL:
        rel.append((f"Allestimenti fieristici a {c}", CITTA_URL[d['cs']]))
    rel.append(("Calendario fiere 2026–2027", CAL))
    if sl: rel.append((dict(SETTORI)[sl.strip('/')], sl))
    rel += [(ALL_IT_LABEL[x['k']], IT_URL[x['k']]) for x in DIT.P3 if x['sett'] == d['sett'] and x['k'] != k][:4]
    if k in ('anuga', 'sial-paris'): rel.append(("Stand Cibus", "/stand-cibus/")); rel.append(("Stand TUTTOFOOD", "/stand-tuttofood/"))
    if k in ('prowein', 'wine-paris'): rel.append(("Stand Vinitaly", "/stand-vinitaly/"))
    if k in ('fruit-logistica',): rel.append(("Stand Macfrut", "/stand-macfrut/"))
    rel += [("Trasporto e magazzino stand", DH.TRA['path']), ("Moquette per fiere", DH.MOQ['path']),
            ("Stand su misura", "/stand-fieristici-su-misura/"), ("Montaggio stand", "/montaggio-stand-fieristici/"),
            ("Quanto costa uno stand", "/quanto-costa-uno-stand-fieristico/"), ("Allestimenti fieristici", PILLAR)]
    evs = [e for e in (event_node(x) for x in d['cal']) if e]
    area = [{"@type": "City", "name": c}] + ([{"@type": "Country", "name": PAESE_NOME.get(d.get('paese'), 'Europa')}] if estero else [])
    node = svc(P, f"Stand per {n}", "Allestimento e montaggio di stand fieristici",
               f"Progettazione, materiali e componentistica, grafica, impianti, trasporto, montaggio e smontaggio di stand per {n} a {q} ({c}).", d['off'], area)
    title = f"Stand {sn} {anno}: allestimento a {c} | Danova Tech"
    if len(title) > 62: title = f"Stand {sn} {anno} a {c} | Danova Tech"
    if len(title) > 62: title = f"Stand {sn} {anno} a {c}"
    desc = f"Stand per {n} a {q}: progetto 3D, materiali, grafica, impianti e montatori in fiera. Prossima edizione: {qs[0]}. Preventivo gratuito."
    if len(desc) > 160: desc = desc.replace(" Preventivo gratuito.", "")
    if len(desc) > 160: desc = desc.replace("progetto 3D, materiali, grafica, impianti e montatori in fiera", "progetto, materiali, impianti e montaggio")
    if len(desc) > 160: desc = desc.replace(" (date da confermare)", "")
    crumbs = [("Home", "/"), ("Allestimenti fieristici", PILLAR)] + ([("Fiere all'estero", ESTERO)] if estero else [("Calendario fiere", CAL)]) + [(f"Stand {sn}", None)]
    pagina(P, title, desc, f"Stand per {n} — Danova Tech", f"Allestimento chiavi in mano a {q}: progetto, materiali, grafica, impianti e montaggio.",
           crumbs, m, qa, [node], rel, cta_t=f"Esponi a {sn}?", wp_extra=({"mentions": evs} if evs else None), fiera_form=f"{sn} – {c}, {qs[0]}")
    print(f"IT {len(title):3d} {len(desc):3d} {P}")

# ================================================================ EN/ZH: pagine fiera estere
MESI_EN = BI.MESI_EN
def event_x(fid, L):
    i, n, v, st, s, e, c, site, nota = DC.FIERE[fid]
    if not c: return None
    vn, city, cc, lat, lon, addr = DC.V[v]
    ven = DX.VEN[v]
    from event_extra import arricchisci
    return arricchisci({"@type": "BusinessEvent", "name": n, "startDate": s, "endDate": e, "url": site,
      "eventStatus": "https://schema.org/EventScheduled", "eventAttendanceMode": "https://schema.org/OfflineEventAttendanceMode",
      "location": {"@type": "Place", "name": vn, "address": {"@type": "PostalAddress", "streetAddress": addr, "addressLocality": ven[1], "addressCountry": cc},
        "geo": {"@type": "GeoCoordinates", "latitude": lat, "longitude": lon}},
      "description": (f"{n}在{ven[5]}{ven[3]}的{ven[2]}举办，是该行业的重要国际专业展会。" if L == 'zh'
        else f"{n}: international trade fair at {vn}, {ven[1]} ({ven[4]}).")})

def node_x(L, url, name, desc, offers, city, country):
    nd = service_node(SITE + url, name, name, desc, [{"@type": "City", "name": city}, {"@type": "Country", "name": country}, {"@type": "Place", "name": "Europe"}], offers, L)
    nd["availableLanguage"] = ["English", "Chinese", "Italian", "Hindi", "Urdu"]
    return nd

def fair_lbl(L, k):
    return f"{NAME[k]} stand builder" if L == 'en' else f"{ZNAME[k]}展台搭建"

def build_x(f, L):
    t = BI.T[L]; d = f[L]; P = (EN_URL if L == 'en' else ZH_URL)[f['k']]; it = IT_URL[f['k']]
    vn_en, city_en, vn_zh, city_zh, cty_en, cty_zh = DX.VEN[f['venue']]
    year = min(DC.FIERE[x][4][:4] for x in f['cal'])
    n = d['name']; sn = d.get('short', n)
    lab = lambda x: DC.FIERE[x][1].replace("(gennaio)", "(January)" if L == 'en' else "（1月）").replace("(settembre)", "(September)" if L == 'en' else "（9月）")
    dates = ''.join(f'<span>{lab(x)}: {BI.when(x, L)}</span>' for x in f['cal'])
    if L == 'en':
        extra = f'\n    <div class="fr-dates" data-rv="up">{dates}<span>{vn_en}, {city_en}</span></div>'
        h1 = f'{sn} stand builder: <span class="grad">turnkey stands</span> at {vn_en}.'
        eyebrow = f'Exhibition stands · {sn} {year}'
    else:
        extra = f'\n    <div class="fr-dates" data-rv="up">{dates}<span>{city_zh} · {vn_zh}</span></div>'
        h1 = f'{n}展台设计搭建：<span class="grad">一站式交钥匙服务</span>。'
        eyebrow = f'展台搭建 · {sn} {year}'
    m = hero(eyebrow, h1, d['lead'], t['req'], '#contatti-fiera', t['how'], '#metodo', extra=extra)
    site = DC.FIERE[f['cal'][0]][7]
    nxt = '<br>'.join(f"{lab(x)}: {BI.when(x, L)}" for x in f['cal'])
    if L == 'en':
        rows = [("Fair", d['full']), ("Where", f"{vn_en}, {city_en}, {cty_en}"), ("Next edition", nxt), ("Sector", d['sector'].capitalize()),
                ("Official website", f'<a href="{site}" rel="noopener" target="_blank">{site.split("//")[1].rstrip("/")}</a>'),
                ("Our experience", f"We build stands for {sn} and for trade fairs across Europe.")]
        m += scheda("scheda", f"{sn} at a glance", rows, "Dates are those published by the organiser (checked in October 2026). Always confirm them on the official website before booking travel and transport.")
        m += testo("fiera", f"What {sn} is and <span class=\"grad\">what it asks of a stand</span>", None, d['intro'])
        m += testo("esigenze", f"What a stand for {sn} needs", None, [], d['needs'])
    else:
        rows = [("展会", n), ("地点", f"{cty_zh}{city_zh} · {vn_zh}"), ("下一届", nxt), ("行业", d['sector']),
                ("官方网站", f'<a href="{site}" rel="noopener" target="_blank">{site.split("//")[1].rstrip("/")}</a>'),
                ("我们的经验", f"我们为{sn}以及欧洲各地的展会搭建展台。")]
        m += scheda("scheda", f"{sn}概况", rows, "日期以主办方公布为准（2026年10月核对）。预订行程和运输前，请务必在官方网站上再次确认。")
        m += testo("fiera", f"{sn}是什么展会，<span class=\"grad\">对展台有什么要求</span>", None, d['intro'])
        m += testo("esigenze", f"{sn}展台需要什么", None, [], d['needs'])
    m += cards("cosa", t['cards_t'], t['cards_l'], CARDS(L))
    if L == 'en':
        ft = 'Exhibiting from Asia or from abroad'
        fl = 'Most of our international clients have never worked with a European stand builder before. This is how we make it simple.'
        fo = [(a, b.replace("in English, or in Chinese with the help of translation tools", "in English, or in your language (Chinese, Hindi, Urdu and more) with the help of translation tools")
               .replace("If your designer in China", "If your designer at home").replace("in China or abroad", "in Asia or anywhere else")
               .replace("our warehouse in Italy", "our warehouse in Italy")) for a, b in t['foreign']]
    else:
        ft = '从中国来欧洲参展'; fl = '我们的大多数国际客户以前从未和欧洲搭建商合作过。我们这样让一切变得简单。'
        fo = [(a, b.replace("意大利技术规定", "当地展馆的技术规定").replace("存放在意大利的仓库", "存放在我们意大利的仓库")) for a, b in t['foreign']]
    m += testo("estero", ft, fl, [], fo)
    p_t = (f'From the brief to a stand <span class="grad">ready at {vn_en}.</span>' if L == 'en' else f'从需求沟通 <span class="grad">到{vn_zh}的完工展台。</span>')
    steps = [(a, b.replace("Italian ", "")) for a, b in t['steps']]
    m += passi("metodo", t['steps_ey'], p_t, None, steps)
    gq = [(a.format(n=sn), b) for a, b in t['gen_qa']]
    if L == 'en':
        gq[1] = ("Can we communicate in our own language?", "Yes. Write to us in English, Chinese, Hindi, Urdu or your language: we reply in your language with the help of translation tools and confirm important technical details in English too.")
    qa = d['qa'] + gq
    m += BI.richiesta_l(L, (f"{sn} {year} – {city_en}" if L == 'en' else f"{n}（{city_zh}）{year}"))
    m += faq(t['faq_ey'], t['faq_t'], qa)
    m += BI.contact(L, f"{sn} {year}")
    rel = [((("Exhibition stands in Europe") if L == 'en' else "欧洲展台搭建"), HUB[L])]
    same = [x['k'] for x in DX.FAIRS if x['country'] == f['country'] and x['k'] != f['k']]
    rel += [(fair_lbl(L, k), (EN_URL if L == 'en' else ZH_URL)[k]) for k in same]
    if L == 'en':
        rel += [(f"Stand builder for {c['adj']} companies", COUNTRY_URL[c['country']]) for c in DH.COUNTRIES if f['k'] in c['fairs']]
    rel += [(t['pillar'], PILL[L]), (("Guide: exhibiting in Italy" if L == 'en' else "意大利参展指南"), GUIDE[L]), (t['it_ver'], it)]
    m += BI.related(L, rel, P)
    if L == 'en':
        title = f"{sn} Stand Builder {year} in {city_en} | Danova Tech"
        if len(title) > 60: title = f"{sn} Stand Builder {year} in {city_en}"
        if len(title) > 60: title = f"{sn} Stand Builder {year}"
        desc = f"{sn} {year} stand builder at {vn_en}: 3D design, production, transport, graphics, electrics and installation. Free itemised quote in euro."
        if len(desc) > 158: desc = f"{sn} {year} stand builder in {city_en}: design, production, transport and installation. Free itemised quote in euro."
        ogt = f"{sn} stand builder — Danova Tech"; ogd = f"Turnkey stands for {sn} at {vn_en}: design, production, transport and installation."
        crumbs = [("Home", "/en/"), ("Exhibition stands in Europe", HUB['en']), (f"{sn} stand builder", None)]
        name = f"Stand design and build for {sn}"
        sdesc = f"Design, production, transport, graphics, electrics, installation and dismantling of exhibition stands for {d['full']} at {vn_en}, {city_en}."
        offers = [f"Stand design for {sn}", "Modular and custom-built stands", "Installation and dismantling on site", "Shell scheme upgrades", "Stand storage"]
    else:
        title = f"{year}年{n}展台设计搭建 | Danova Tech"
        if W(title) > 64: title = f"{year}年{n}展台设计搭建"
        desc = f"{n}（{cty_zh}{city_zh}{vn_zh}）展台设计与搭建：三维设计、意大利生产、运输、平面印刷、电气照明和现场搭建。可用中文沟通，免费欧元逐项报价。"
        ogt = f"{n}展台搭建 — Danova Tech"; ogd = f"{vn_zh}{sn}一站式展台服务：设计、生产、运输和现场搭建。"
        crumbs = [("首页", "/en/"), ("欧洲展台搭建", HUB['zh']), (f"{sn}展台搭建", None)]
        name = f"{sn}展台设计与搭建"
        sdesc = f"为{n}（{cty_zh}{city_zh}{vn_zh}）提供展台设计、生产、运输、平面印刷、电气、现场搭建与拆除服务。"
        offers = [f"{sn}展台设计", "模块化展台和特装展台", "现场搭建与拆除", "标摊升级", "展台仓储"]
    evs = [e for e in (event_x(x, L) for x in f['cal']) if e]
    node = node_x(L, P, name, sdesc, offers, city_en, cty_en)
    build(L, P, title, desc, ogt, ogd, crumbs, m, qa, [node], IM.ALTS[P], wp_extra=({"mentions": evs} if evs else None), scripts=BI.REQ_JS)
    print(f"{L} {W(title):3d} {len(desc):3d} {P}")

# ================================================================ hub Europa EN/ZH
def build_hub(L):
    h = DH.HUB_EN if L == 'en' else DH.HUB_ZH; t = BI.T[L]; P = h['path']
    m = hero(h['eyebrow'], h['h1'], h['lead'], t['req'], '#contatti-fiera', t['how'], '#metodo')
    m += testo("perche", h['why_t'], None, h['why'])
    m += testo("servizio", h['list_t'], None, [], h['lista'])
    URL = EN_URL if L == 'en' else ZH_URL
    m += chips("fiere-europa", h['fairs_t'], h['fairs_l'], [(fair_lbl(L, f['k']), URL[f['k']]) for f in DX.FAIRS])
    m += chips("fiere-italia", h['it_t'], None, [(fair_lbl(L, f['k']), URL[f['k']]) for f in DI.FAIRS])
    if L == 'en':
        m += chips("paesi", h['countries_t'], "Pages for exhibitors coming from Asia.", [(f"Stand builder for {c['adj']} companies", COUNTRY_URL[c['country']]) for c in DH.COUNTRIES])
    m += passi("metodo", t['steps_ey'], ('How we work <span class="grad">with foreign exhibitors.</span>' if L == 'en' else '我们如何 <span class="grad">与海外参展商合作。</span>'), None, [(a, b.replace("Italian ", "")) for a, b in t['steps']])
    m += BI.richiesta_l(L)
    m += faq(t['faq_ey'], t['faq_t'], h['qa'])
    m += BI.contact(L, ("a fair in Europe" if L == 'en' else "欧洲展会"))
    rel = [(t['pillar'], PILL[L]), (("Guide: exhibiting in Italy" if L == 'en' else "意大利参展指南"), GUIDE[L]), (t['it_ver'], ESTERO)]
    m += BI.related(L, rel, P)
    crumbs = [(t['home'], "/en/"), (("Exhibition stands in Europe" if L == 'en' else "欧洲展台搭建"), None)]
    nm = "European exhibition stand design and build" if L == 'en' else "欧洲展台设计搭建"
    node = node_x(L, P, nm, h['desc'], (["Custom exhibition stands", "Modular exhibition stands", "Stand installation and dismantling", "Shell scheme upgrades", "Stand transport and storage"] if L == 'en' else ["特装展台", "模块化展台", "展台搭建与拆除", "标摊升级", "展台运输与仓储"]), "Europe", "Europe")
    build(L, P, h['title'], h['desc'], h['title'].split(' | ')[0], h['desc'], crumbs, m, h['qa'], [node], IM.ALTS[P], scripts=BI.REQ_JS)
    print(f"{L} {W(h['title']):3d} {len(h['desc']):3d} {P}")

# ================================================================ pagine paese (EN)
def build_country(c):
    L = 'en'; t = BI.T['en']; P = COUNTRY_URL[c['country']]
    m = hero(f"Exhibition stands · Exhibitors from {c['country']}", f'Exhibition stand builder for <span class="grad">{c["adj"]} companies</span> in Europe.', c['lead'], t['req'], '#contatti-fiera', t['how'], '#metodo')
    m += testo("settori", f"{c['adj']} exhibitors at European trade fairs", None,
               [f"{c['adj']} companies come to European trade fairs mainly in {c['sectors']}. For many of them the fair is the main way to meet distributors, importers and retail buyers face to face.", c['pavilions']])
    lst = [(fair_lbl('en', k), EN_URL[k]) for k in c['fairs'] if k in EN_URL]
    m += chips("fiere", f"Trade fairs where {c['adj']} companies exhibit", "Each page explains what the fair asks of a stand and how we build it.", lst)
    m += cards("cosa", t['cards_t'], t['cards_l'], CARDS(L))
    fo = [(a, b.replace("in English, or in Chinese with the help of translation tools", "in English, or in your language with the help of translation tools")
           .replace("If your designer in China", "If your designer at home").replace("in China or abroad", f"in {c['country']} or anywhere else")) for a, b in t['foreign']]
    m += testo("estero", f"Exhibiting in Europe from {c['country']}", "This is how we make it simple.", [], fo)
    m += passi("metodo", t['steps_ey'], 'From the brief to a stand <span class="grad">ready at the fair.</span>', None, [(a, b.replace("Italian ", "")) for a, b in t['steps']])
    qa = c['qa'] + [("How much does a stand cost?", "It depends on floor space, structure, finishes, electrics and services. We send you a free itemised quote in euro for your project.")]
    m += BI.richiesta_l('en', f"Fair in Europe – exhibitor from {c['country']}")
    m += faq(t['faq_ey'], t['faq_t'], qa)
    m += BI.contact('en', f"a fair in Europe")
    rel = [("Exhibition stands in Europe", HUB['en']), (t['pillar'], PILL['en'])] + [(f"Stand builder for {x['adj']} companies", COUNTRY_URL[x['country']]) for x in DH.COUNTRIES if x is not c]
    if c['country'] == 'China': rel.append(("中文：欧洲展台搭建", HUB['zh']))
    rel.append(("Guide: exhibiting in Italy", GUIDE['en']))
    m += BI.related('en', rel, P)
    crumbs = [("Home", "/en/"), ("Exhibition stands in Europe", HUB['en']), (f"{c['adj']} exhibitors", None)]
    title = c['title'] if len(c['title']) <= 60 else c['title']
    node = node_x('en', P, f"Exhibition stand design and build for {c['adj']} companies", c['desc'], ["Custom exhibition stands", "Shell scheme upgrades", "Stand installation and dismantling", "Stand transport and storage"], "Europe", "Europe")
    build('en', P, title, c['desc'], title, c['desc'], crumbs, m, qa, [node], {'en': P}, scripts=BI.REQ_JS)
    print(f"en {len(title):3d} {len(c['desc']):3d} {P}")

# ================================================================ DE: Messebau Mailand
def build_de():
    h = DH.DE_MI; P = h['path']
    wa = 'https://wa.me/393884706887?text=' + quote('Hallo, wir brauchen einen Messestand in Mailand. Messe: … Fläche (m²): …')
    m = hero(h['eyebrow'], h['h1'], h['lead'], "Angebot anfordern", "#kontakt", "So arbeiten wir", "#metodo")
    m += cards("leistungen", h['cards_t'], "Alles aus einer Hand, oder nur der Teil, der Ihnen fehlt.", h['cards'])
    m += testo("warum", h['why_t'], None, [], h['why'])
    m += chips("messen", h['fairs_t'], "Fiera Milano Rho und Allianz MiCo.", [(x, None) for x in h['fairs']])
    m += passi("metodo", "Ablauf", 'Vom Briefing bis zum <span class="grad">fertigen Stand in Mailand.</span>', None, h['steps'])
    m += faq("Häufige Fragen", 'Fragen, die uns <span class="grad">oft gestellt werden.</span>', h['qa'])
    m += f'''<section class="pg-cta" id="kontakt">
  <div class="wrap">
    <div class="box" data-rv="up">
      <h2 class="title">Messestand in Mailand?</h2>
      <p>Nennen Sie uns Messe, Termin und Fläche. Sie erhalten ein kostenloses, detailliertes Angebot, auch kurzfristig.</p>
      <div class="hero-cta fr-ct">
        <a href="mailto:info@danova-tech.com?subject={quote('Anfrage Messestand Mailand')}" class="btn btn-p" data-mag><span class="sheen"></span><span class="lbl">E-Mail · info@danova-tech.com</span>
          {ARR}</a>
        <a href="{wa}" class="btn btn-g" data-mag rel="noopener"><span class="lbl">WhatsApp +39 388 470 6887</span></a>
      </div>
    </div>
  </div>
</section>
'''
    m += altri("Weitere Seiten", [("Messebau in Italien und Europa", "/de/messebau-italien/"), ("English: exhibition stand builder in Milan", "/en/exhibition-stand-builder-milan/"),
                                   ("Italiano: allestimenti fieristici a Milano", "/allestimenti-fieristici-milano/"), ("Exhibition stands in Europe (English)", HUB['en'])])
    crumbs = [("Startseite", "/de/"), ("Messebau Italien", "/de/messebau-italien/"), ("Messebau Mailand", None)]
    node = service_node(SITE + P, "Messebau in Mailand", "Messebau", h['desc'], [{"@type": "City", "name": "Mailand"}, {"@type": "Country", "name": "Italien"}],
                        ["Individuelle Messestände", "Systemstände", "Auf- und Abbau", "Einlagerung"], 'de')
    build('de', P, h['title'], h['desc'], h['title'].split(' | ')[0], h['desc'], crumbs, m, h['qa'], [node], {'de': P})
    print(f"de {len(h['title']):3d} {len(h['desc']):3d} {P}")

# ================================================================ IT: moquette, trasporto
def build_servizi():
    h = DH.MOQ; P = h['path']
    m = hero(h['eyebrow'], h['h1'], h['lead'], "Richiedi un preventivo", "#richiesta", "Che moquette usare", "#tipi")
    m += testo("tipi", h['tipi_t'], None, [], h['tipi'])
    m += testo("norme", h['norme_t'], None, h['norme'])
    m += testo("posa", h['posa_t'], None, [], h['posa'])
    rel = [("Materiali ignifughi per stand", "/guide/materiali-ignifughi-stand/"), ("Sicurezza stand fieristici", "/sicurezza-stand-fieristici/"),
           ("Noleggio stand fieristici", "/noleggio-stand-fieristici/"), ("Stand preallestiti", "/stand-preallestiti/"),
           ("Trasporto e magazzino stand", DH.TRA['path']), ("Allestimenti fieristici", PILLAR)]
    node = svc(P, "Moquette per stand fieristici", "Fornitura e posa di moquette per fiere", h['desc'], ["Moquette agugliata ignifuga", "Moquette su pedana", "Quadrotte", "Posa e rimozione in fiera"])
    pagina(P, h['title'], h['desc'], h['title'].split(' | ')[0], h['desc'], [("Home", "/"), ("Allestimenti fieristici", PILLAR), ("Moquette per fiere", None)],
           m, h['qa'], [node], rel, cta_t="Ti serve la moquette per lo stand?")
    print(f"IT {len(h['title']):3d} {len(h['desc']):3d} {P}")
    h = DH.TRA; P = h['path']
    m = hero(h['eyebrow'], h['h1'], h['lead'], "Richiedi un preventivo", "#richiesta", "Cosa facciamo", "#fasi")
    m += testo("fasi", h['fasi_t'], None, [], h['fasi'])
    m += testo("perche", h['perche_t'], None, h['perche'])
    m += chips("estero", "Fiere all'estero dove portiamo stand", None, [(f"Stand {x.get('short', x['nome'])}", IT_URL[x['k']]) for x in DIT.P3 if 'cs' not in x])
    rel = [("Allestimenti fieristici all'estero", ESTERO), ("Allestimenti fieristici in Germania", "/allestimenti-fieristici-germania/"),
           ("Montaggio stand fieristici", "/montaggio-stand-fieristici/"), ("Stand modulari", "/stand-modulari/"), ("Noleggio stand", "/noleggio-stand-fieristici/"),
           ("Moquette per fiere", DH.MOQ['path']), ("Allestimenti fieristici", PILLAR)]
    node = svc(P, "Trasporto e magazzino stand fieristici", "Logistica per stand fieristici", h['desc'], ["Trasporto stand in Italia e in Europa", "Magazzino e custodia stand", "Coordinamento con lo spedizioniere", "Manutenzione fra le fiere"])
    pagina(P, h['title'], h['desc'], h['title'].split(' | ')[0], h['desc'], [("Home", "/"), ("Allestimenti fieristici", PILLAR), ("Trasporto e magazzino", None)],
           m, h['qa'], [node], rel, cta_t="Devi portare lo stand in fiera?")
    print(f"IT {len(h['title']):3d} {len(h['desc']):3d} {P}")

# ================================================================ link dagli hub (box "Approfondisci" .pg-altri)
def aggiungi(rel, links):
    p = os.path.join(R, rel.strip('/'), 'index.html')
    if not os.path.exists(p): print('manca', rel); return 0
    h = open(p, encoding='utf-8').read()
    m = re.search(r'<div class="pg-altri"[^>]*>', h)
    if not m: print('niente pg-altri in', rel); return 0
    box = h[m.end():h.find('</div>', m.end())]
    add = ''.join(f'<a href="{u}">{t}</a>' for t, u in links if f'href="{u}"' not in box and u.strip('/') != rel.strip('/'))
    if not add: return 0
    open(p, 'w', encoding='utf-8').write(h[:m.end()] + add + h[m.end():]); return 1

def collega():
    est = [(f"Stand {x.get('short', x['nome'])}", IT_URL[x['k']]) for x in DIT.P3 if 'cs' not in x]
    ita = [(f"Stand {x.get('short', x['nome'])}", IT_URL[x['k']]) for x in DIT.P3 if 'cs' in x]
    ger = [(f"Stand {x.get('short', x['nome'])}", IT_URL[x['k']]) for x in DIT.P3 if x.get('paese') == 'germania']
    srv = [("Trasporto e magazzino stand", DH.TRA['path']), ("Moquette per fiere", DH.MOQ['path'])]
    n = 0
    n += aggiungi(ESTERO, est + srv)
    n += aggiungi("/allestimenti-fieristici-germania/", ger + srv[:1])
    n += aggiungi(PILLAR, srv + [("Fiere all'estero", ESTERO)])
    n += aggiungi("/stand-fieristici/", srv)
    n += aggiungi(CAL, est + ita)
    n += aggiungi("/montaggio-stand-fieristici/", srv)
    n += aggiungi("/noleggio-stand-fieristici/", srv[1:])
    n += aggiungi("/sicurezza-stand-fieristici/", srv[1:])
    for x in DIT.P3:
        if 'cs' in x and x['cs'] in CITTA_URL: n += aggiungi(CITTA_URL[x['cs']], [(f"Stand {x.get('short', x['nome'])}", IT_URL[x['k']])])
    for k, extra in (("vinitaly", ["prowein", "wine-paris"]), ("cibus", ["anuga", "sial-paris"]), ("tuttofood", ["anuga", "sial-paris"]),
                     ("macfrut", ["fruit-logistica"]), ("eima", ["agritechnica", "fieragricola"]), ("mecspe", ["hannover-messe", "sps-italia"]),
                     ("cosmoprof", ["cosmofarma"]), ("salone-del-mobile", ["maison-et-objet", "ambiente-francoforte"]), ("host", ["ambiente-francoforte"])):
        n += aggiungi(f"/stand-{k}/", [(ALL_IT_LABEL[e], IT_URL[e]) for e in extra])
    # EN / ZH / DE
    n += aggiungi(GUIDE['en'], [("Exhibition stands in Europe", HUB['en'])] + [(f"Stand builder for {c['adj']} companies", COUNTRY_URL[c['country']]) for c in DH.COUNTRIES])
    n += aggiungi(GUIDE['zh'], [("欧洲展台搭建", HUB['zh'])])
    n += aggiungi("/en/exhibition-stand-builder-milan/", [("Deutsch: Messebau Mailand", DH.DE_MI['path'])])
    print('box collegamenti aggiornati:', n)

def sezione_chips(rel, sid, title, lead, links, before='<section id="esperienza"'):
    p = os.path.join(R, rel.strip('/'), 'index.html'); h = open(p, encoding='utf-8').read()
    sec = chips(sid, title, lead, links)
    if f'<section id="{sid}"' in h:
        h2 = re.sub(rf'<section id="{sid}".*?</section>\n', lambda _: sec, h, 1, flags=re.S)
    else:
        i = h.find(before)
        if i < 0: print('manca punto di inserimento in', rel); return 0
        h2 = h[:i] + sec + h[i:]
    if h2 != h: open(p, 'w', encoding='utf-8').write(h2); return 1
    return 0

def collega_lingue():
    n = 0
    n += sezione_chips(PILL['en'], 'fiere-europa', 'Stand pages for European trade fairs',
        'Germany, France, Spain and the Netherlands: the fairs where many Asian companies exhibit, and pages for exhibitors from India, Pakistan, China and Bangladesh.',
        [("Exhibition stands in Europe", HUB['en'])] + [(f"Stand builder for {c['adj']} companies", COUNTRY_URL[c['country']]) for c in DH.COUNTRIES] + [(fair_lbl('en', f['k']), EN_URL[f['k']]) for f in DX.FAIRS])
    n += sezione_chips(PILL['zh'], 'fiere-europa', '欧洲展会展台专题', '德国、法国、西班牙和荷兰中国企业参展最多的展会。',
        [("欧洲展台搭建", HUB['zh'])] + [(fair_lbl('zh', f['k']), ZH_URL[f['k']]) for f in DX.FAIRS])
    n += sezione_chips('/de/messebau-italien/', 'messebau-mailand', 'Messebau in Mailand', 'Messestände für Fiera Milano Rho: Salone del Mobile, EICMA, HostMilano, MICAM, MIDO und mehr.',
        [("Messebau Mailand", DH.DE_MI['path']), ("Exhibition stands in Europe (English)", HUB['en'])])
    print('sezioni lingue:', n)

if __name__ == '__main__':
    for d in DIT.P3: build_it(d)
    for L in ('en', 'zh'):
        for f in DX.FAIRS: build_x(f, L)
        build_hub(L)
    for c in DH.COUNTRIES: build_country(c)
    build_de()
    build_servizi()
    BI.patch_it()
    collega()
    collega_lingue()
