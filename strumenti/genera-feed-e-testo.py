#!/usr/bin/env python3
"""Danova Stand: feed RSS (guide, lavori, pagine nuove) e llms-full.txt (testo integrale per gli assistenti AI).
Idempotente. Va lanciato dopo ottimizza-geo.py (usa le date della sitemap).

    python3 strumenti/genera-feed-e-testo.py

- feed.xml: le 40 pagine aggiornate più di recente tra lavori, guide, calendari e servizi, in italiano.
  Bing Webmaster Tools e gli aggregatori lo leggono per scoprire subito le novita'.
- llms-full.txt: il testo di tutte le pagine indicizzabili (titolo, indirizzo, data, testo principale),
  cosi' ChatGPT, Claude, Perplexity e gli altri leggono tutto il sito in un solo file.
- llms.txt: riga con il link a llms-full.txt e al feed.
- <link rel="alternate" type="application/rss+xml"> nella home, in /guide/ e in /lavori/.
"""
import datetime, html, os, re
from email.utils import format_datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
SITE = 'https://danovastand.com'
e = html.escape


def testo(h):
    m = re.search(r'<main[^>]*>(.*?)</main>', h, re.S)
    t = m.group(1) if m else h
    t = re.sub(r'<(script|style|svg|form|noscript)[^>]*>.*?</\1>', ' ', t, flags=re.S)
    t = re.sub(r'<!--.*?-->', ' ', t, flags=re.S)
    t = re.sub(r'</(p|h[1-6]|li|tr|div|section|summary|figcaption|dd|dt)>', '\n', t)
    t = re.sub(r'<br\s*/?>', '\n', t)
    t = re.sub(r'<[^>]+>', ' ', t)
    t = html.unescape(t)
    t = re.sub(r'[ \t\xa0]+', ' ', t)
    righe = [r.strip() for r in t.split('\n')]
    out = []
    for r in righe:
        if r and (not out or out[-1] != r): out.append(r)
    return '\n'.join(out)


def main():
    sm = open('sitemap.xml', encoding='utf-8').read()
    pagine = []
    for b in re.findall(r'<url>(.*?)</url>', sm, re.S):
        loc = re.search(r'<loc>(.*?)</loc>', b).group(1)
        data = (re.search(r'<lastmod>(.*?)</lastmod>', b) or [None, '2026-01-01'])[1]
        f = loc.replace(SITE + '/', '') + 'index.html'
        if not os.path.exists(f): continue
        h = open(f, encoding='utf-8').read()
        if 'noindex' in h[:5000]: continue
        lang = (re.search(r'<html[^>]*lang="([^"]+)"', h) or [0, 'it'])[1]
        tit = html.unescape((re.search(r'<title>(.*?)</title>', h, re.S) or [0, ''])[1].strip())
        desc = html.unescape((re.search(r'<meta name="description" content="([^"]*)"', h) or [0, ''])[1])
        img = (re.search(r'<meta property="og:image" content="([^"]+)"', h) or [0, ''])[1]
        pagine.append(dict(loc=loc, data=data, lang=lang, tit=tit, desc=desc, img=img, h=h))

    # ---------------------------------------------------------------- feed RSS
    def priorita(p):
        u = p['loc']
        return ('/lavori/' in u, '/guide/' in u)
    it = [p for p in pagine if p['lang'].startswith('it')]
    it.sort(key=lambda p: (p['data'], priorita(p)), reverse=True)
    items = ''
    for p in it[:40]:
        d = datetime.datetime.fromisoformat(p['data'] + 'T09:00:00+01:00')
        items += (f'  <item>\n    <title>{e(p["tit"])}</title>\n    <link>{p["loc"]}</link>\n    <guid isPermaLink="true">{p["loc"]}</guid>\n'
                  f'    <pubDate>{format_datetime(d)}</pubDate>\n    <description>{e(p["desc"])}</description>\n'
                  + (f'    <enclosure url="{e(p["img"])}" type="image/jpeg" length="0"/>\n' if p['img'].endswith('.jpg') else '') +
                  '  </item>\n')
    ultimo = format_datetime(datetime.datetime.fromisoformat(it[0]['data'] + 'T09:00:00+01:00')) if it else ''
    feed = ('<?xml version="1.0" encoding="UTF-8"?>\n<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">\n<channel>\n'
            '  <title>Danova Stand — stand fieristici e allestimenti</title>\n  <link>https://danovastand.com/</link>\n'
            '  <atom:link href="https://danovastand.com/feed.xml" rel="self" type="application/rss+xml"/>\n'
            '  <description>Lavori realizzati, guide, calendari fiere e servizi di Danova Stand: stand fieristici chiavi in mano in Italia e in Europa.</description>\n'
            f'  <language>it-it</language>\n  <lastBuildDate>{ultimo}</lastBuildDate>\n' + items + '</channel>\n</rss>\n')
    scrivi('feed.xml', feed)

    # ---------------------------------------------------------------- llms-full.txt
    ordine = sorted(pagine, key=lambda p: (not p['lang'].startswith('it'), p['lang'], p['loc']))
    corpo = ['# Danova Stand — testo integrale del sito', '',
             '> Testo di tutte le pagine indicizzabili di https://danovastand.com/ , per assistenti AI e motori di ricerca. '
             'Indice ragionato e informazioni principali: https://danovastand.com/llms.txt . Contatti: info@danova-tech.com, +39 388 470 6887 '
             '(telefono e WhatsApp; al telefono italiano, inglese e rumeno, per iscritto tutte le lingue).', '']
    for p in ordine:
        corpo += ['', '---', '', f'## {p["tit"]}', '', f'URL: {p["loc"]}', f'Lingua: {p["lang"]} · Aggiornata: {p["data"]}', '',
                  p['desc'], '', testo(p['h'])]
    scrivi('llms-full.txt', '\n'.join(corpo).strip() + '\n')

    # ---------------------------------------------------------------- llms.txt e link nel <head>
    s = open('llms.txt', encoding='utf-8').read(); s0 = s
    riga = ('Testo completo di tutte le pagine: https://danovastand.com/llms-full.txt · '
            'Novità (RSS): https://danovastand.com/feed.xml')
    s = re.sub(r'\nTesto completo di tutte le pagine: [^\n]*\n', '\n', s)
    s = s.replace('\n\n## In breve', '\n\n' + riga + '\n\n## In breve', 1)
    if s != s0: open('llms.txt', 'w', encoding='utf-8').write(s)
    tag = '<link rel="alternate" type="application/rss+xml" title="Danova Stand — novità" href="/feed.xml">'
    for f in ('index.html', 'guide/index.html', 'lavori/index.html'):
        if not os.path.exists(f): continue
        h = open(f, encoding='utf-8').read()
        if tag not in h:
            h = h.replace('<link rel="manifest"', tag + '\n<link rel="manifest"', 1)
            open(f, 'w', encoding='utf-8').write(h)
    print(f'feed.xml: {min(40, len(it))} voci · llms-full.txt: {len(pagine)} pagine, {os.path.getsize("llms-full.txt") // 1024} KB')


def scrivi(p, s):
    if os.path.exists(p) and open(p, encoding='utf-8').read() == s: return
    open(p, 'w', encoding='utf-8').write(s)


if __name__ == '__main__':
    main()
