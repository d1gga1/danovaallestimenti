# -*- coding: utf-8 -*-
"""26/10/2026 - ottimizzazione SEO + AI delle pagine /allestimenti-fieristici-<citta|regione>/.
Idempotente: si puo' rilanciare dopo ogni build dei generatori (che riscrivono le pagine da zero).
  python3 seo-tools/fiere-2026-10-26/applica.py
Cosa fa su ogni pagina:
  1. title, meta description, og/twitter, WebPage.name/description, dateModified
  2. box "In breve" (risposta diretta, speakable) dopo l'immagine di apertura
  3. sezione "Il territorio in fiera" (contenuto unico) dopo il blocco locale
  4. lista "Cosa preparare" specifica al posto di quella del generatore
  5. FAQ: via le 3 domande uguali su tutte le pagine, dentro 3 domande specifiche (HTML + JSON-LD)
  6. blocco "legno" ridotto a 2 righe (era identico su 28 pagine)
  7. regioni: tabella dei quartieri fieristici con link alle pagine citta'
"""
import os, re, json, sys, html as H
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))
from dati_citta_a import C as A
from dati_citta_b import C as B
from dati_citta_c import C as Cc
from dati_regioni import R
C = {**A, **B, **Cc}
OGGI = '2026-10-26'
GEN_Q = ('Accettate richieste urgenti?', 'Lo stand è a noleggio o in acquisto?', 'Quanto costa uno stand?')
LEGNO_CORTO = ('<!--fr-legno--><section id="legno">\n  <div class="wrap">\n    <div class="pg-testo" data-rv="up">\n'
  '      <p><b>Elementi in legno su misura.</b> Pareti, banconi, desk, pedane ed espositori li progettiamo noi sul tuo marchio e li facciamo produrre da laboratori partner selezionati; '
  'trasporto e montaggio restano in capo a un solo referente. Dettagli nella pagina <a href="/servizi/allestimenti-fieristici/">allestimenti fieristici</a>.</p>\n'
  '    </div>\n  </div>\n</section>\n<!--/fr-legno-->')

def esc(t): return H.escape(re.sub(r'<[^>]+>', '', t), quote=True)
def testo(t): return re.sub(r'<[^>]+>', '', t)

def set_meta(s, title, desc):
    s = re.sub(r'<title>.*?</title>', '<title>' + H.escape(title, quote=False) + '</title>', s, count=1, flags=re.S)
    for pat, val in [(r'(<meta name="description" content=")[^"]*(")', desc),
                     (r'(<meta property="og:title" content=")[^"]*(")', title),
                     (r'(<meta name="twitter:title" content=")[^"]*(")', title),
                     (r'(<meta property="og:description" content=")[^"]*(")', desc),
                     (r'(<meta name="twitter:description" content=")[^"]*(")', desc)]:
        s = re.sub(pat, lambda m: m.group(1) + esc(val) + m.group(2), s, count=1)
    return s

def blocco(s, nome, nuovo, dopo):
    """Inserisce/sostituisce <!--nome-->...<!--/nome--> subito dopo la stringa `dopo` (prima occorrenza)."""
    a, b = f'<!--{nome}-->', f'<!--/{nome}-->'
    s = re.sub(re.escape(a) + '.*?' + re.escape(b) + r'\n?', '', s, flags=re.S)
    if not nuovo: return s
    i = s.find(dopo)
    if i < 0: raise SystemExit(f'ancora non trovata per {nome}: {dopo[:40]}')
    i += len(dopo)
    return s[:i] + '\n' + a + nuovo + b + s[i:]

def breve_html(d, nome_luogo):
    dl = ''.join(f'<div><dt>{H.escape(k)}</dt><dd>{v}</dd></div>' for k, v in d['dl'])
    if d.get('ente'):
        host = re.sub(r'^https?://(www\.)?|/$', '', d['ente'])
        dl += f'<div><dt>Sito dell\'ente fiera</dt><dd><a href="{d["ente"]}" rel="noopener" target="_blank">{host}</a></dd></div>'
    return (f'<section id="in-breve">\n  <div class="wrap">\n    <div class="sec-head">\n'
            f'      <div class="eyebrow mono" data-scramble>In breve</div>\n'
            f'      <h2 class="title" data-rv="up">Allestimenti fieristici a {nome_luogo}, <span class="grad">in poche righe</span></h2>\n    </div>\n'
            f'    <div class="pg-breve" data-rv="up">\n      <p>{d["breve"]}</p>\n      <dl>{dl}</dl>\n    </div>\n  </div>\n</section>\n')

def dist_html(dist, sid='territorio'):
    t, ps = dist
    body = ''.join(f'      <p>{p}</p>\n' for p in ps)
    return (f'<section id="{sid}">\n  <div class="wrap">\n    <div class="sec-head">\n      <h2 class="title" data-rv="up">{t}</h2>\n    </div>\n'
            f'    <div class="pg-testo" data-rv="up">\n{body}    </div>\n  </div>\n</section>\n')

def tab_html(d):
    righe = ''.join(f'<tr><th scope="row"><a href="{u}">{H.escape(c)}</a></th><td>{H.escape(q)}</td><td>{H.escape(f)}</td><td>{H.escape(b)}</td></tr>'
                    for c, q, f, b, u in d['tab'])
    return (f'<section id="quartieri">\n  <div class="wrap">\n    <div class="sec-head">\n      <h2 class="title" data-rv="up">{d["tab_t"]}</h2>\n'
            f'      <p class="lead" data-rv="up">{d["tab_l"]}</p>\n    </div>\n'
            f'    <div class="price-table-wrap" data-rv="up"><table class="price-table"><thead><tr><th scope="col">Città</th><th scope="col">Quartiere</th>'
            f'<th scope="col">Fiere principali</th><th scope="col">Da noi</th></tr></thead><tbody>{righe}</tbody></table></div>\n  </div>\n</section>\n')

def set_sapere(s, check, citta):
    m = re.search(r'(<section id="sapere">.*?<h2 class="title" data-rv="up">)(.*?)(</h2>.*?<ul class="pg-lista" data-rv="up">)(.*?)(</ul>)', s, re.S)
    if not m: return s
    li = ''.join(f'\n      <li><b>{a}</b> {b}</li>' for a, b in check) + '\n    '
    return s[:m.start()] + m.group(1) + f'Cosa preparare per uno stand a {citta}' + m.group(3) + li + m.group(5) + s[m.end():]

def simile(a, b):
    w = lambda x: {t for t in re.findall(r'\w{4,}', x.lower())}
    A_, B_ = w(a), w(b)
    return len(A_ & B_) / max(1, min(len(A_), len(B_))) >= 0.5

def set_faq(s, nuove, sostituisci_tutto=False):
    m = re.search(r'(<section id="faq">.*?<div class="faq">)(.*?)(\n    </div>\n  </div>\n</section>)', s, re.S)
    if not m: raise SystemExit('faq non trovata')
    vecchie = re.findall(r'<summary>(.*?)<span class="pm"></span></summary>\s*<div class="ans"><p>(.*?)</p></div>', m.group(2), re.S)
    tenute = [] if sostituisci_tutto else [(q, a) for q, a in vecchie if q not in GEN_Q and not any(simile(q, n[0]) for n in nuove)]
    finali = list(nuove) + tenute
    corpo = ''.join(f'\n      <details data-rv="up"><summary>{q}<span class="pm"></span></summary>\n        <div class="ans"><p>{a}</p></div></details>' for q, a in finali)
    s = s[:m.start()] + m.group(1) + corpo + m.group(3) + s[m.end():]
    return s, finali

def set_jsonld(s, finali, title, desc):
    def fix(mm):
        g = json.loads(mm.group(1))
        nodi = g.get('@graph', [g])
        for n in nodi:
            t = n.get('@type')
            if t == 'FAQPage':
                n['mainEntity'] = [{"@type": "Question", "name": testo(q), "acceptedAnswer": {"@type": "Answer", "text": testo(a)}} for q, a in finali]
            if t == 'WebPage':
                n['name'] = title; n['description'] = desc; n['dateModified'] = OGGI
                n['speakable'] = {"@type": "SpeakableSpecification", "cssSelector": ["#in-breve .pg-breve p", "h1"]}
        return '<script type="application/ld+json">' + json.dumps(g, ensure_ascii=False, indent=2) + '</script>'
    return re.sub(r'<script type="application/ld\+json">(.*?)</script>', fix, s, flags=re.S)

def nome_citta(s):
    m = re.search(r'<div class="wrap pg-crumbs">.*?<em>/</em>([^<]+)\n?</div>', s, re.S)
    return m.group(1).strip() if m else None

def applica_citta(k, d):
    p = os.path.join(ROOT, f'allestimenti-fieristici-{k}', 'index.html')
    s = open(p, encoding='utf-8').read()
    citta = nome_citta(s) or k.title()
    s = set_meta(s, d['title'], d['desc'])
    s = blocco(s, 'fr-breve', breve_html(d, citta), '<!--/fr-foto-->' if '<!--/fr-foto-->' in s else '</section>')
    anc = '<!--/fr-locale-->' if '<!--/fr-locale-->' in s else '<!--/fr-breve-->'
    s = blocco(s, 'fr-territorio', dist_html(d['dist']), anc)
    s = set_sapere(s, d['check'], citta)
    s = re.sub(r'<!--fr-legno-->.*?<!--/fr-legno-->', lambda m: LEGNO_CORTO, s, count=1, flags=re.S)
    s, finali = set_faq(s, d['faq'])
    s = set_jsonld(s, finali, d['title'], d['desc'])
    if k == 'bolzano':  # distanza reale Mansue'-Bolzano (via Valsugana/A22)
        s = s.replace('ci sono circa 150 km, circa 2 ore di strada', 'ci sono circa 230 km, circa 3 ore di strada')
    open(p, 'w', encoding='utf-8').write(s)
    return p

def applica_regione(k, d):
    p = os.path.join(ROOT, f'allestimenti-fieristici-{k}', 'index.html')
    s = open(p, encoding='utf-8').read()
    nome = {'veneto': 'Veneto', 'lombardia': 'Lombardia', 'emilia-romagna': 'Emilia-Romagna'}[k]
    s = set_meta(s, d['title'], d['desc'])
    if d.get('h1'):
        s = re.sub(r'(<h1 data-rv="up">).*?(</h1>)', lambda m: m.group(1) + d['h1'] + m.group(2), s, count=1, flags=re.S)
    ancora = '<!--/fr-foto-->' if '<!--/fr-foto-->' in s else '</section>'
    s = blocco(s, 'fr-breve', breve_html(d, 'in ' + nome).replace('a in ', 'in '), ancora)
    s = blocco(s, 'fr-quartieri', tab_html(d), '<!--/fr-breve-->')
    if d.get('dist'):
        s = blocco(s, 'fr-territorio', dist_html(d['dist']), '<!--/fr-quartieri-->')
    s = re.sub(r'<!--fr-legno-->.*?<!--/fr-legno-->', lambda m: LEGNO_CORTO, s, count=1, flags=re.S)
    s, finali = set_faq(s, d['faq'], sostituisci_tutto=True)
    s = set_jsonld(s, finali, d['title'], d['desc'])
    open(p, 'w', encoding='utf-8').write(s)
    return p

CSS_A, CSS_B = '/* fr-2610 */', '/* /fr-2610 */'
CSS = (CSS_A + '.pg-breve{border:1px solid rgba(77,139,255,.35);background:rgba(30,107,255,.07);border-radius:18px;padding:24px 26px;margin-top:8px}'
  '.pg-breve p{margin:0 0 14px;font-size:1.06rem;line-height:1.6}.pg-breve dl{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:12px 22px;margin:0}'
  '.pg-breve dt{font-family:"JetBrains Mono",monospace;font-size:.72rem;letter-spacing:.08em;text-transform:uppercase;opacity:.7}.pg-breve dd{margin:3px 0 0;font-weight:600}'
  '.pg-breve dd a{color:inherit;text-decoration:underline;text-underline-offset:3px}'
  '#quartieri .price-table th[scope=row] a{color:inherit;font-weight:600}' + CSS_B)

def css():
    p = os.path.join(ROOT, 'assets', 'css', 'fiere.css')
    s = open(p, encoding='utf-8').read()
    s = re.sub(re.escape(CSS_A) + '.*?' + re.escape(CSS_B), '', s, flags=re.S).rstrip() + '\n' + CSS + '\n'
    open(p, 'w', encoding='utf-8').write(s)

if __name__ == '__main__':
    css()
    for k, d in C.items():
        if len(d['title']) > 62: print('ATTENZIONE title lungo', k, len(d['title']))
        print('ok', applica_citta(k, d).replace(ROOT, ''))
    for k, d in R.items(): print('ok', applica_regione(k, d).replace(ROOT, ''))
    import pillar; print('ok', pillar.servizi().replace(ROOT, '')); print('ok', pillar.stand().replace(ROOT, ''))
