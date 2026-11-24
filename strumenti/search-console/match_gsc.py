import os, re, sys, json, html, unicodedata
ROOT = sys.argv[1]
QFILE = sys.argv[2]
SKIP = ('render', 'private_area', 'strumenti', 'assets', 'Claude outputs', '_google_business', 'nuove_foto_newstand', '.git')

def norm(s):
    s = unicodedata.normalize('NFKD', s.lower())
    s = ''.join(c for c in s if not unicodedata.combining(c))
    s = re.sub(r'(\d+)\s*(mq|m2|m²)', r'\1 mq', s)
    return s

STOP = set('di da del della delle dei degli per in a e il la le lo i gli un una con su al alla allo the for of in and to at de des du et en der die das und fur von im het van een voor stand stands'.split())
def stem(w):
    w = re.sub(r"[^a-z0-9]", '', w)
    if len(w) > 4 and not w.isdigit():
        for suf in ('ieri','iere','iera','ici','ico','ica','iche','ali','ale','i','e','a','o','s'):
            if w.endswith(suf) and len(w) - len(suf) >= 4:
                return w[:-len(suf)]
    return w

def toks(s):
    return [stem(w) for w in re.split(r"[\s\-_/'’&.,;:!?()]+", norm(s)) if w and w not in STOP]

pages = []
for dp, dn, fn in os.walk(ROOT):
    rel = os.path.relpath(dp, ROOT)
    if rel.split(os.sep)[0] in SKIP:
        dn[:] = []
        continue
    if 'index.html' not in fn:
        continue
    t = open(os.path.join(dp, 'index.html'), encoding='utf-8', errors='ignore').read()
    if 'http-equiv="refresh"' in t[:3000] and len(t) < 4000:
        continue  # redirect
    lang = re.search(r'<html[^>]*lang="([^"]+)"', t)
    title = re.search(r'<title>(.*?)</title>', t, re.S)
    desc = re.search(r'<meta name="description" content="([^"]*)"', t)
    h1 = re.findall(r'<h1[^>]*>(.*?)</h1>', t, re.S)
    h2 = re.findall(r'<h[23][^>]*>(.*?)</h[23]>', t, re.S)
    body = re.sub(r'<script.*?</script>|<style.*?</style>', ' ', t, flags=re.S)
    body = html.unescape(re.sub(r'<[^>]+>', ' ', body))
    strip = lambda x: html.unescape(re.sub(r'<[^>]+>', ' ', x or '')).strip()
    url = '/' + ('' if rel == '.' else rel + '/')
    head = ' '.join([url.replace('-', ' '), strip(title.group(1) if title else ''), strip(desc.group(1) if desc else ''), ' '.join(map(strip, h1))])
    pages.append(dict(url=url, lang=lang.group(1) if lang else '', title=strip(title.group(1) if title else ''),
                      head=set(toks(head)), h2=set(toks(' '.join(map(strip, h2)))), body=set(toks(body)),
                      h2list=[strip(x) for x in h2]))

out = []
for line in open(QFILE, encoding='utf-8'):
    imp, clk, pos, q = line.rstrip('\n').split('|', 3)
    qt = set(toks(q))
    if not qt:
        continue
    best = None
    for p in pages:
        hh = len(qt & p['head']); h2 = len(qt & (p['head'] | p['h2'])); bb = len(qt & p['body'])
        score = (hh == len(qt), h2 == len(qt), bb == len(qt), hh, h2, bb)
        if best is None or score > best[0]:
            best = (score, p['url'])
    s = best[0]
    level = 'TITOLO' if s[0] else ('SEZIONE' if s[1] else ('TESTO' if s[2] else 'MANCA'))
    missing = []
    if level == 'MANCA':
        allb = set().union(*[p['body'] for p in pages])
        missing = sorted(qt - allb)
    out.append(dict(q=q, imp=int(imp), clk=int(clk), pos=float(pos or 0), level=level, page=best[1], missing=missing))

json.dump(dict(pages=[dict(url=p['url'], lang=p['lang'], title=p['title']) for p in pages], res=out), sys.stdout, ensure_ascii=False)
