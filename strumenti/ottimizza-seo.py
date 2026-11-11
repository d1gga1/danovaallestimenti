#!/usr/bin/env python3
"""Ottimizzazioni SEO / GEO / accessibilita' applicate a tutte le pagine (8/11/2026).

Idempotente: si puo' rilanciare quante volte si vuole. Va rilanciato DOPO
migra-da-danovatech.py, perche' quello script sovrascrive le pagine importate.

    python3 strumenti/ottimizza-seo.py

Cosa fa:
 1. Schema Organization: aggiunge i profili social a sameAs (entita' / Knowledge Panel)
    e amplia knowsAbout con i servizi reali del sito.
 2. Immagini hero con alt="" (oltre 300 pagine): alt descrittivo nella lingua della
    pagina, preso dallo stesso render usato altrove nel sito (Image SEO, accessibilita').
 3. Title e description troppo lunghi (troncati da Google) accorciati.
 4. Link alla pagina "Chi siamo" nel footer italiano (E-E-A-T, brand SERP).
 5. Messaggio WhatsApp precompilato: "Danova Tech" -> "Danova Stand" (coerenza del brand).
"""
import os, re, json, html, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKIP = {'.git', 'strumenti', '_google_business', 'node_modules', '.github', 'render'}

SOCIAL = [
    "https://www.instagram.com/danova_techh/",
    "https://www.tiktok.com/@danova.tech",
    "https://www.facebook.com/profile.php?id=61594907955699",
    "https://danova-tech.com/",
]
KNOWS = [
    "Stand fieristici", "Stand preallestiti", "Stand modulari", "Stand su misura",
    "Progettazione stand e render 3D", "Allestimento eventi", "Allestimento negozi e vetrine",
    "Allestimento mostre", "Grafica per stand", "Ledwall e illuminazione per stand",
    "Regolamenti tecnici fieristici", "Materiali ignifughi Classe 1",
]
TITLES = {
    'index.html': ("Stand per fiere e allestimenti fieristici chiavi in mano | Danova Stand",
                   "Stand per fiere e allestimenti fieristici | Danova Stand"),
}
DESCS = {
    'stand-pubblicitari/index.html': (
        "Stand pubblicitari, espositivi e promozionali: banchetti, stand portatili e pop-up, roll-up, fondali in tessuto e strutture modulari con la tua grafica. Preventivo in 24 ore.",
        "Stand pubblicitari, espositivi e promozionali: banchetti, stand portatili e pop-up, roll-up e fondali in tessuto con la tua grafica. Preventivo in 24 ore."),
    'allestimenti-fieristici-torino/index.html': (
        "Stand a Lingotto Fiere e all&#x27;Oval: Salone del Libro, fiere dell&#x27;automotive e dell&#x27;energia, grandi flussi di pubblico. Allestitore a un&#x27;ora e mezza da Trumello.",
        "Stand a Lingotto Fiere e all&#x27;Oval: Salone del Libro, automotive ed energia, grandi flussi di pubblico. Allestitore a un&#x27;ora e mezza da Trumello."),
}

def pages():
    for d, ds, fs in os.walk(ROOT):
        ds[:] = [x for x in ds if x not in SKIP]
        for f in fs:
            if f.endswith('.html'):
                yield os.path.relpath(os.path.join(d, f), ROOT)

def lang_of(h):
    m = re.search(r'<html[^>]*\blang="([^"]+)"', h)
    return m.group(1) if m else 'it'

def img_key(src):
    b = os.path.basename(src.split('?')[0])
    return re.sub(r'(-\d{3,4})?\.(webp|jpe?g|png|avif)$', '', b)

# --- 1a passata: mappa (lingua, immagine) -> alt piu' usato -------------------
alts = collections.defaultdict(collections.Counter)
cache = {}
for rel in pages():
    h = open(os.path.join(ROOT, rel), encoding='utf-8').read()
    cache[rel] = h
    lg = lang_of(h)
    for tag in re.findall(r'<img\b[^>]*>', h):
        s = re.search(r'\bsrc="([^"]+)"', tag); a = re.search(r'\balt="([^"]+)"', tag)
        if s and a and not a.group(1).lower().startswith('logo'):
            alts[(lg, img_key(s.group(1)))][a.group(1)] += 1

stats = collections.Counter()

def fix_org(m):
    raw = m.group(1)
    if '"https://danovastand.com/#organization"' not in raw or '"sameAs"' not in raw:
        return m.group(0)
    try:
        j = json.loads(raw)
    except Exception:
        return m.group(0)
    changed = False
    for it in (j.get('@graph', [j]) if isinstance(j, dict) else j):
        if it.get('@id') != 'https://danovastand.com/#organization' or 'sameAs' not in it:
            continue
        sa = it['sameAs'] if isinstance(it['sameAs'], list) else [it['sameAs']]
        for s in SOCIAL:
            if s not in sa: sa.append(s); changed = True
        it['sameAs'] = sa
        ka = it.get('knowsAbout', [])
        for k in KNOWS:
            if k not in ka: ka.append(k); changed = True
        it['knowsAbout'] = ka
    if not changed:
        return m.group(0)
    stats['org'] += 1
    nl = '\n' if raw.startswith('\n') else ''
    return '<script type="application/ld+json">' + nl + json.dumps(j, ensure_ascii=False, indent=2) + nl + '</script>'

for rel, h in cache.items():
    orig = h
    lg = lang_of(h)
    # 1. schema Organization
    h = re.sub(r'<script type="application/ld\+json">(.*?)</script>', fix_org, h, flags=re.S)
    # 2. alt delle immagini vuoti
    h1 = re.search(r'<h1[^>]*>(.*?)</h1>', h, re.S)
    h1 = html.unescape(re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', h1.group(1)))).strip() if h1 else ''
    def fix_img(mm):
        tag = mm.group(0)
        if 'alt=""' not in tag: return tag
        s = re.search(r'\bsrc="([^"]+)"', tag)
        if not s or '/assets/img/stand/' not in s.group(1): return tag
        c = alts.get((lg, img_key(s.group(1))))
        alt = c.most_common(1)[0][0] if c else (html.escape(h1, quote=True) if h1 else '')
        if not alt: return tag
        stats['alt'] += 1
        return tag.replace('alt=""', f'alt="{alt}"', 1)
    h = re.sub(r'<img\b[^>]*>', fix_img, h)
    # 3. title / description
    if rel in TITLES:
        a, b = TITLES[rel]
        if f'<title>{a}</title>' in h: h = h.replace(f'<title>{a}</title>', f'<title>{b}</title>'); stats['title'] += 1
    if rel in DESCS:
        a, b = DESCS[rel]
        if f'name="description" content="{a}"' in h:
            h = h.replace(f'name="description" content="{a}"', f'name="description" content="{b}"'); stats['desc'] += 1
    # 4. Chi siamo nel footer italiano
    old = '<i>·</i><a href="/contatti/">Contatti</a><i>·</i>'
    if old in h and 'href="/chi-siamo/">Chi siamo' not in h:
        h = h.replace(old, '<i>·</i><a href="/chi-siamo/">Chi siamo</a>' + old, 1); stats['footer'] += 1
    # 5. WhatsApp
    if 'Ciao%20Danova%20Tech%21' in h:
        h = h.replace('Ciao%20Danova%20Tech%21', 'Ciao%20Danova%20Stand%21'); stats['wa'] += 1
    if h != orig:
        open(os.path.join(ROOT, rel), 'w', encoding='utf-8').write(h); stats['file'] += 1

print(dict(stats))
