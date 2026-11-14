#!/usr/bin/env python3
"""Ottimizzazioni dai dati del Keyword Planner (CSV del 14/11/2026, periodo nov 2025 - ott 2026).

Idempotente. Va rilanciato DOPO migra-da-danovatech.py e DOPO ottimizza-seo.py:

    python3 strumenti/ottimizza-keyword.py

Cosa fa (dati e motivazioni in strumenti/ricerca-parole-chiave-2026-11-csv.md):
 1. Title / description / H1 allineati alle parole con piu' ricerche reali.
 2. Calendari fiere: anno 2027 in primo piano (le ricerche "fiere <citta> 2026"
    sono finite; "fiere <citta> 2027" stanno partendo, picco atteso gen-mar 2027).
 3. EICMA: pagina portata al 2027 (edizione 2026 conclusa l'8/11).
 5. Fiere concluse portate alla prossima edizione (date, titolo, dati Event).
 6. Pagine nuove aggiunte a sitemap.xml e llms.txt.
 7. Contributi: /contributi-fiere-2026/ -> /contributi-fiere/ (pagina 2027), link interni aggiornati.
 8. Metrature: /stand-XX-mq/ unite in /stand-fieristici-per-metratura/ (sezioni con ancora).
 4. Velocita' (LCP): la priorita' alta di caricamento passa dal logo alla prima
    immagine del contenuto; le immagini successive vengono caricate in differita.
"""
import os, re, collections, html

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKIP = {'.git', 'strumenti', '_google_business', 'node_modules', '.github', 'render'}

# vecchio -> nuovo: sostituiti ovunque nel file (title, og:title, twitter:title, schema)
REPLACE = {
    'index.html': [
        ("Stand per fiere e allestimenti fieristici | Danova Stand",
         "Stand fiera e allestimenti fieristici | Danova Stand"),
    ],
    'stand-eicma/index.html': [
        ("Stand EICMA 2026 (3–8 novembre) chiavi in mano | Danova Stand",
         "Stand EICMA 2027 chiavi in mano a Fiera Milano Rho | Danova Stand"),
        ("Stand per EICMA 2026 a Fiera Milano Rho (3–8 novembre): progetto 3D, grafica, impianti e montaggio in fiera. Valutiamo anche richieste urgenti. Risposta in 24 ore.",
         "Stand per EICMA 2027 a Fiera Milano Rho (novembre 2027): progetto 3D, grafica, impianti e montaggio in fiera. Prenota presto: risposta in 24 ore."),
    ],
    'espositori-desk-totem-per-fiere/index.html': [
        ("Desk per fiere, banchi e totem espositori | Danova Stand",
         "Espositori per fiere: desk, banchi e totem | Danova Stand"),
    ],
    'stand-pubblicitari/index.html': [
        ("Stand pubblicitari e promozionali personalizzati | Danova Stand",
         "Stand pubblicitari, espositivi e promozionali | Danova Stand"),
    ],
    'calendario-fiere/index.html': [
        ("Fiere 2026 e 2027: calendario fiere Italia ed Europa",
         "Calendario fiere 2027: le fiere in Italia ed Europa"),
    ],
    'calendario-fiere-rimini/index.html': [
        ("Fiere Rimini 2026–2027: calendario (Ecomondo, Sigep, Macfrut)",
         "Fiere Rimini 2027: calendario (Sigep, Macfrut, Ecomondo)"),
    ],
}
YEAR_RX = re.compile(r'2026\s*(?:e|–|-)\s*2027')

def pages():
    for d, ds, fs in os.walk(ROOT):
        ds[:] = [x for x in ds if x not in SKIP]
        for f in fs:
            if f.endswith('.html'):
                yield os.path.relpath(os.path.join(d, f), ROOT)

def calendar_years(h):
    """Nei calendari: 2026 e 2027 -> 2027 solo in title, og/twitter title, description e H1."""
    def tag(m): return YEAR_RX.sub('2027', m.group(0))
    h = re.sub(r'<title>[^<]*</title>', tag, h)
    h = re.sub(r'<meta (?:property|name)="(?:og:title|twitter:title|description|og:description|twitter:description)" content="[^"]*"', tag, h)
    h = re.sub(r'<h1[^>]*>.*?</h1>', tag, h, flags=re.S)
    return h

def images(h):
    tags = list(re.finditer(r'<img\b[^>]*>', h))
    content = [m for m in tags if '/assets/img/stand/' in m.group(0)]
    if not content:
        return h
    first = content[0]
    out, pos = [], 0
    for m in tags:
        t = m.group(0); n = t
        if 'logo' in t and 'fetchpriority="high"' in t:
            n = t.replace(' fetchpriority="high"', '')
        elif m is first:
            if 'loading=' not in t and 'fetchpriority' not in t:
                n = t[:-1].rstrip('/').rstrip() + ' fetchpriority="high">'
        elif '/assets/img/stand/' in t and 'loading=' not in t and 'fetchpriority' not in t:
            n = t[:-1].rstrip('/').rstrip() + ' loading="lazy">'
            if 'decoding=' not in n:
                n = n[:-1] + ' decoding="async">'
        out.append(h[pos:m.start()]); out.append(n); pos = m.end()
    out.append(h[pos:])
    return ''.join(out)


# --- 5. Fiere concluse: pagine portate alla prossima edizione (date verificate il 14/11/2026) ----
# chiave: (vecchio inizio, vecchia fine, nuovo inizio, nuova fine, anno nuovo,
#          [(vecchia etichetta, nuova etichetta) per IT, EN, ZH, ZH-HANT])
TBC_IT, TBC_EN, TBC_ZH, TBC_ZHT = 'date da confermare', 'dates to be confirmed', '日期待确认', '日期待確認'
EDIZIONI = {
 'sicam': ('2026-10-20', '2026-10-23', '2027-10-19', '2027-10-22', '2027', [
    ('20–23 ottobre 2026', '19–22 ottobre 2027'), ('20–23 October 2026', '19–22 October 2027'),
    ('2026年10月20日至23日', '2027年10月19日至22日')]),
 'ecomondo': ('2026-11-03', '2026-11-06', '2027-11', '2027-11', '2027', [
    ('3–6 novembre 2026', f'novembre 2027 ({TBC_IT})'), ('3–6 November 2026', f'November 2027 ({TBC_EN})'),
    ('2026年11月3日至6日', '2027年11月（%s）')]),
 'eicma': ('2026-11-03', '2026-11-08', '2027-11', '2027-11', '2027', [
    ('3–8 novembre 2026', f'novembre 2027 ({TBC_IT})'), ('3–8 November 2026', f'November 2027 ({TBC_EN})'),
    ('2026年11月3日至8日', '2027年11月（%s）')]),
 'fieracavalli': ('2026-11-05', '2026-11-08', '2027-11-04', '2027-11-07', '2027', [
    ('5–8 novembre 2026', '4–7 novembre 2027')]),
 'eima': ('2026-11-10', '2026-11-14', '2028-11', '2028-11', '2028', [   # biennale
    ('10–14 novembre 2026', f'novembre 2028 ({TBC_IT})'), ('10–14 November 2026', f'November 2028 ({TBC_EN})'),
    ('2026年11月10日至14日', '2028年11月（%s）')]),
 'electronica': ('2026-11-10', '2026-11-13', '2028-11-14', '2028-11-17', '2028', [   # biennale
    ('10–13 novembre 2026', '14–17 novembre 2028'), ('10–13 November 2026', '14–17 November 2028'),
    ('2026年11月10日至13日', '2028年11月14日至17日')]),
}
SKIP_BEFORE = ('ottobre ', 'October ', 'fiere ', 'Fiere ', 'fairs ', '=', '-', '/', '%2F')
SKIP_AFTER = ('–', '-', '年10月', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9')

def fair_of(rel):
    m = re.match(r'(?:stand-([a-z]+)/|(?:en|zh|zh-hant)/([a-z]+)-stand(?:-builder)?/)index\.html$', rel)
    k = m and (m.group(1) or m.group(2))
    return k if k in EDIZIONI else None

def edizione(rel, h):
    k = fair_of(rel)
    if not k: return h
    s0, e0, s1, e1, yr, labels = EDIZIONI[k]
    if f'"startDate": "{s0}"' not in h: return h   # gia' aggiornata o pagina diversa
    tbc = TBC_ZHT if rel.startswith('zh-hant/') else TBC_ZH
    for a, b in labels:
        h = h.replace(a, b.replace('%s', tbc) if '%s' in b else b)
    h = h.replace(f'"startDate": "{s0}"', f'"startDate": "{s1}"').replace(f'"endDate": "{e0}"', f'"endDate": "{e1}"')
    def yr_sub(m):
        i = m.start(); bef = h[max(0, i - 8):i]; aft = h[m.end():m.end() + 4]
        if bef.endswith(SKIP_BEFORE) or aft.startswith(SKIP_AFTER) or 'contributi' in h[max(0, i - 20):i].lower():
            return m.group(0)
        return yr
    h = re.sub(r'(?<!\d)2026', yr_sub, h)
    for nm in ('EICMA', 'Ecomondo', 'Sicam', 'SICAM', 'EIMA', 'International', 'Fieracavalli', 'electronica'):
        h = h.replace(f'{nm}%202026', f'{nm}%20{yr}')
    h = h.replace("aggiornate all'8 ottobre 2026", "aggiornate al 14 novembre 2026")
    return h


# --- 7. Contributi: indirizzo senza anno /contributi-fiere/ (la pagina 2026 rimanda li') -------
CONTR_OLD, CONTR_NEW = 'contributi-fiere-2026', 'contributi-fiere'
CONTR_TESTI = [
    ('Contributi e bandi fiere 2026: SIMEST e Camere di Commercio', 'Contributi e bandi fiere 2027: SIMEST e Camere di Commercio'),
    ('Contributi e bandi per le fiere 2026:', 'Contributi e bandi per le fiere 2027:'),
    ('Contributi per le fiere 2026 — Danova Stand', 'Contributi per le fiere 2027 — Danova Stand'),
    ('partecipare alle fiere nel 2026', 'partecipare alle fiere nel 2027'),
    ('Esistono contributi per partecipare alle fiere nel 2026?', 'Esistono contributi per partecipare alle fiere nel 2027?'),
    ('aperto per tutto il 2026', 'aperto a sportello, senza una scadenza annuale fissa'),
    ('è aperta per tutto il 2026, a sportello:', 'è aperta a sportello, senza una scadenza annuale fissa:'),
]
LINK_TESTI = [('>Contributi fiere 2026<', '>Contributi fiere 2027<'), ('>Contributi per le fiere 2026<', '>Contributi per le fiere 2027<'),
              ('>contributi per le fiere 2026<', '>contributi per le fiere 2027<'), ('>i contributi per le fiere 2026<', '>i contributi per le fiere 2027<')]
STUB = """<!DOCTYPE html>
<html lang="it"><head><meta charset="utf-8">
<title>Contributi per le fiere | Danova Stand</title>
<meta name="robots" content="noindex, follow">
<link rel="canonical" href="https://danovastand.com/contributi-fiere/">
<meta http-equiv="refresh" content="0; url=/contributi-fiere/">
<script>location.replace("/contributi-fiere/")</script>
</head><body>
<p><a href="/contributi-fiere/">Contributi per le fiere</a></p>
</body></html>
"""

def contributi():
    old_p = os.path.join(ROOT, CONTR_OLD, 'index.html'); new_d = os.path.join(ROOT, CONTR_NEW)
    h = open(old_p, encoding='utf-8').read()
    if len(h) > 5000:   # pagina vera (appena reimportata): diventa /contributi-fiere/
        h = h.replace(f'https://danovastand.com/{CONTR_OLD}/', f'https://danovastand.com/{CONTR_NEW}/').replace(f'/{CONTR_OLD}/', f'/{CONTR_NEW}/')
        for a, b in CONTR_TESTI + LINK_TESTI: h = h.replace(a, b)
        os.makedirs(new_d, exist_ok=True)
        open(os.path.join(new_d, 'index.html'), 'w', encoding='utf-8').write(h)
        open(old_p, 'w', encoding='utf-8').write(STUB); stats['contributi'] += 1
    for name in ('sitemap.xml', 'llms.txt'):
        fp = os.path.join(ROOT, name); t = open(fp, encoding='utf-8').read()
        t2 = t.replace(f'/{CONTR_OLD}/', f'/{CONTR_NEW}/').replace('Contributi e bandi fiere 2026', 'Contributi e bandi fiere 2027')
        if t2 != t: open(fp, 'w', encoding='utf-8').write(t2); stats['contributi-' + name] += 1

def contributi_link(rel, h):
    if rel == f'{CONTR_OLD}/index.html': return h
    if f'/{CONTR_OLD}/' in h:
        h = h.replace(f'/{CONTR_OLD}/', f'/{CONTR_NEW}/')
        for a, b in LINK_TESTI: h = h.replace(a, b)
    return h


# --- 8. Metrature: le 7 pagine /stand-XX-mq/ diventano sezioni di /stand-fieristici-per-metratura/ --
# (zero ricerche su Google per "stand N mq"; contenuto conservato, vecchi indirizzi rimandano all'ancora)
MQ = [9, 12, 16, 24, 32, 48, 100]
HUB = 'stand-fieristici-per-metratura'
MQ_CACHE = os.path.join(ROOT, 'strumenti', 'metrature-blocchi.html')

def mq_stub(m):
    u = f'/{HUB}/#stand-{m}-mq'
    return f"""<!DOCTYPE html>
<html lang="it"><head><meta charset="utf-8">
<title>Stand {m} mq | Danova Stand</title>
<meta name="robots" content="noindex, follow">
<link rel="canonical" href="https://danovastand.com/{HUB}/">
<meta http-equiv="refresh" content="0; url={u}">
<script>location.replace("{u}")</script>
</head><body>
<p><a href="{u}">Stand {m} mq</a></p>
</body></html>
"""

def mq_blocco(m, h):
    main = re.search(r'<main.*?</main>', h, re.S).group(0)
    sec = {}
    for x in re.findall(r'<section[^>]*>.*?</section>', main, re.S):
        mm = re.match(r'<section(?: id="([^"]+)")?(?: class="([^"]+)")?', x)
        sec[(mm.group(1) or mm.group(2) or '')] = x
    hero = sec.get('pg-hero', '')
    h1 = re.search(r'<h1[^>]*>(.*?)</h1>', hero, re.S).group(1)
    lead = re.search(r'<p class="lead"[^>]*>(.*?)</p>', hero, re.S)
    def inner(key):
        x = sec.get(key, '')
        x = re.sub(r'^<section[^>]*>\s*<div class="wrap">', '', x); x = re.sub(r'</div>\s*</section>$', '', x)
        x = re.sub(r'<h2 class="title"[^>]*>(.*?)</h2>', r'<h3 class="mq-sub">\1</h3>', x, flags=re.S)
        return x
    foto = re.search(r'<figure.*?</figure>', sec.get('fr-foto-sec', ''), re.S)
    foto = foto.group(0) if foto else ''
    if foto and 'loading=' not in foto: foto = foto.replace('<img ', '<img loading="lazy" ', 1)
    foto = re.sub(r' fetchpriority="high"', '', foto)
    return (f'<section id="stand-{m}-mq" class="mq-blocco">\n  <div class="wrap">\n    <div class="sec-head">\n'
            f'      <h2 class="title" data-rv="up">{h1}</h2>\n'
            + (f'      <p class="lead" data-rv="up">{lead.group(1)}</p>\n' if lead else '') +
            '    </div>\n' + foto + inner('scheda') + inner('come') + inner('cosa') + inner('layout') + inner('errori') +
            '\n  </div>\n</section>\n')

def metrature():
    blocchi = {}
    for m in MQ:
        fp = os.path.join(ROOT, f'stand-{m}-mq', 'index.html')
        if not os.path.exists(fp): continue
        h = open(fp, encoding='utf-8').read()
        if len(h) > 5000:
            blocchi[m] = mq_blocco(m, h)
            open(fp, 'w', encoding='utf-8').write(mq_stub(m)); stats['mq-stub'] += 1
    if blocchi:
        open(MQ_CACHE, 'w', encoding='utf-8').write('\n'.join(f'<!--mq {m}-->\n{b}' for m, b in sorted(blocchi.items())))
    if not os.path.exists(MQ_CACHE): return
    cache = open(MQ_CACHE, encoding='utf-8').read()
    hp = os.path.join(ROOT, HUB, 'index.html'); h = open(hp, encoding='utf-8').read(); h0 = h
    tutti = '<!--mq-blocchi-->\n' + re.sub(r'<!--mq \d+-->\n', '', cache) + '<!--/mq-blocchi-->\n'
    if '<!--mq-blocchi-->' in h:
        h = re.sub(r'<!--mq-blocchi-->.*?<!--/mq-blocchi-->\n', lambda _: tutti, h, flags=re.S)
    else:
        h = h.replace('<section id="lati">', tutti + '<section id="lati">', 1)
    for m in MQ:
        h = h.replace(f'<a href="/stand-{m}-mq/">', f'<a href="#stand-{m}-mq">')
    if '.mq-sub{' not in h:
        h = h.replace('</head>', '<style>.mq-blocco .mq-sub{font-size:1.25rem;margin:2.2rem 0 1rem}.mq-blocco .fr-foto{margin:1.5rem 0}</style>\n</head>', 1)
    if h != h0: open(hp, 'w', encoding='utf-8').write(h); stats['mq-hub'] += 1
    # sitemap e llms: via le 7 pagine
    for name in ('sitemap.xml', 'llms.txt'):
        fp = os.path.join(ROOT, name); t = open(fp, encoding='utf-8').read(); t0 = t
        for m in MQ:
            if name == 'sitemap.xml':
                t = re.sub(r'  <url>\n    <loc>https://danovastand.com/stand-%d-mq/</loc>.*?</url>\n' % m, '', t, flags=re.S)
            else:
                t = re.sub(r'^- \[[^\]]*\]\(https://danovastand.com/stand-%d-mq/\):[^\n]*\n' % m, '', t, flags=re.M)
                t = t.replace(f'https://danovastand.com/stand-{m}-mq/', f'https://danovastand.com/{HUB}/#stand-{m}-mq')
        if t != t0: open(fp, 'w', encoding='utf-8').write(t); stats['mq-' + name] += 1

def mq_link(rel, h):
    if rel.startswith(HUB + '/') or re.match(r'stand-\d+-mq/', rel): return h
    for m in MQ:
        h = h.replace(f'href="/stand-{m}-mq/"', f'href="/{HUB}/#stand-{m}-mq"')
    return h


LINK_ADD = {   # pagina -> link da aggiungere nel box "pagine collegate" (pg-altri)
    'de/messebau-italien/index.html': [('/de/messebau-verona/', 'Messebau Verona'), ('/de/messebau-bologna/', 'Messebau Bologna')],
    'de/messebau-mailand/index.html': [('/de/messebau-verona/', 'Messebau Verona'), ('/de/messebau-bologna/', 'Messebau Bologna')],
    'en/exhibition-stand-builder-europe/index.html': [('/nl/standbouw-beurzen-duitsland-europa/', 'Nederlands: standbouw Düsseldorf, Keulen en Europa')],
    'en/exhibition-stand-builder-italy/index.html': [('/nl/standbouw-italie/', 'Nederlands: standbouw Italië')],
    'allestimenti-eventi-showroom-negozi/index.html': [('/allestimento-vetrine/', 'Allestimento vetrine')],
}

def link_add(rel, h):
    for href, txt in LINK_ADD.get(rel, []):
        if f'href="{href}"' in h: continue
        a = f'<a href="{href}">{html.escape(txt)}</a>'
        if '<div class="pg-altri"' in h:
            h = re.sub(r'(<div class="pg-altri"[^>]*>)(\n?)', lambda m: m.group(1) + m.group(2) + ('      ' if m.group(2) else '') + a + m.group(2), h, 1)
        else:   # box a "chips" con link (prima occorrenza che contiene link)
            h = re.sub(r'(<div class="fr-chips"[^>]*>)(?=<a )', lambda m: m.group(1) + a, h, 1)
    return h

stats = collections.Counter()
contributi()
metrature()
for rel in pages():
    p = os.path.join(ROOT, rel)
    h = open(p, encoding='utf-8').read(); orig = h
    for a, b in REPLACE.get(rel, []):
        if a in h:
            h = h.replace(a, b); stats['testi'] += 1
    if rel.startswith('calendario-fiere'):
        h2 = calendar_years(h)
        if h2 != h: stats['calendari'] += 1; h = h2
    h2 = link_add(rel, h)
    if h2 != h: stats['link-nuovi'] += 1; h = h2
    h2 = mq_link(rel, h)
    if h2 != h: stats['link-mq'] += 1; h = h2
    h2 = contributi_link(rel, h)
    if h2 != h: stats['link-contributi'] += 1; h = h2
    h2 = edizione(rel, h)
    if h2 != h: stats['edizioni'] += 1; h = h2
    h2 = images(h)
    if h2 != h: stats['immagini'] += 1; h = h2
    if h != orig:
        open(p, 'w', encoding='utf-8').write(h); stats['file'] += 1

# --- 6. Pagine nuove: sitemap.xml e llms.txt (idempotente) -----------------------------------
NUOVE = [
    # (percorso, immagine, lastmod, riga llms "Pagine", riga llms dopo cui inserirla)
    ('/de/messebau-verona/', 'stand-vinitaly-cantina', '2026-11-14',
     '- [Messebau Verona](https://danovastand.com/de/messebau-verona/): Messestände für Vinitaly, Marmomac, Fieracavalli und Fieragricola (Deutsch).', None),
    ('/de/messebau-bologna/', 'stand-cersaie-ceramica', '2026-11-14',
     '- [Messebau Bologna](https://danovastand.com/de/messebau-bologna/): Messestände für Cosmoprof, Cersaie, EIMA und Marca (Deutsch).', None),
    ('/nl/standbouw-beurzen-duitsland-europa/', 'stand-fiera-estero-padiglione', '2026-11-14',
     '- [Standbouw Düsseldorf, Keulen en Europa](https://danovastand.com/nl/standbouw-beurzen-duitsland-europa/): beursstands voor MEDICA, ProWein, EuroShop, interpack, Anuga, MWC (Nederlands).', None),
    ('/nl/standbouw-italie/', 'stand-salone-mobile-design', '2026-11-14',
     '- [Standbouw Italië](https://danovastand.com/nl/standbouw-italie/): beursstands voor Salone del Mobile, Vinitaly, Cosmoprof, EICMA, Cersaie (Nederlands).', None),
    ('/allestimento-vetrine/', 'stand-vicenzaoro-gioielli', '2026-11-14',
     '- [Allestimento vetrine](https://danovastand.com/allestimento-vetrine/): vetrine natalizie e stagionali, vetrine fisse su misura, vetrine per marchi ed eventi, grafiche e vetrofanie.',
     '- [Allestimento negozi e vetrine](https://danovastand.com/allestimento-negozi/): negozi, corner e temporary store.'),
]
def sitemap_e_llms():
    sm_p = os.path.join(ROOT, 'sitemap.xml'); sm = open(sm_p, encoding='utf-8').read(); sm0 = sm
    ll_p = os.path.join(ROOT, 'llms.txt'); ll = open(ll_p, encoding='utf-8').read(); ll0 = ll
    for path, img, lm, riga, dopo in NUOVE:
        url = 'https://danovastand.com' + path
        lg = path.split('/')[1] if path.split('/')[1] in ('de', 'en', 'nl', 'fr', 'es') else 'it'
        if f'<loc>{url}</loc>' not in sm:
            ent = (f'  <url>\n    <loc>{url}</loc>\n    <lastmod>{lm}</lastmod>\n'
                   f'    <image:image><image:loc>https://danovastand.com/assets/img/stand/{img}.webp</image:loc></image:image>\n'
                   f'    <xhtml:link rel="alternate" hreflang="{lg}" href="{url}"/>\n'
                   f'    <xhtml:link rel="alternate" hreflang="x-default" href="{url}"/>\n  </url>\n')
            sm = sm.replace('</urlset>', ent + '</urlset>')
        if riga and riga not in ll:
            ll = ll.replace(dopo, dopo + '\n' + riga, 1) if dopo and dopo in ll else ll.rstrip('\n') + '\n' + riga + '\n'
    if sm != sm0: open(sm_p, 'w', encoding='utf-8').write(sm); stats['sitemap'] += 1
    if ll != ll0: open(ll_p, 'w', encoding='utf-8').write(ll); stats['llms'] += 1

sitemap_e_llms()

print(dict(stats))
