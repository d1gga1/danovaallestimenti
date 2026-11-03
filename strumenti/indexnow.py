#!/usr/bin/env python3
"""Avvisa subito Bing (e quindi ChatGPT search e Copilot), Yandex, Seznam e Naver
che le pagine del sito sono nuove o cambiate, tramite IndexNow.

Uso, DOPO aver pubblicato il sito (push su main e GitHub Pages aggiornato):
    python3 strumenti/indexnow.py            # invia tutte le pagine della sitemap
    python3 strumenti/indexnow.py /stand-eicma/ /prezzi/   # solo alcune pagine

La chiave e' il file 431f85a1f959c91d9e984e63689aa560.txt nella radice del sito: non cancellarlo.
"""
import json, re, sys, urllib.request
HOST = "danovastand.com"
KEY = "431f85a1f959c91d9e984e63689aa560"
here = __file__.rsplit("/", 2)[0] if "/" in __file__ else "."
if len(sys.argv) > 1:
    urls = ["https://" + HOST + (u if u.startswith("/") else "/" + u) for u in sys.argv[1:]]
else:
    urls = re.findall(r"<loc>(.*?)</loc>", open(here + "/sitemap.xml", encoding="utf-8").read())
body = json.dumps({"host": HOST, "key": KEY, "keyLocation": f"https://{HOST}/{KEY}.txt", "urlList": urls[:10000]}).encode()
req = urllib.request.Request("https://api.indexnow.org/indexnow", data=body,
                             headers={"Content-Type": "application/json; charset=utf-8"})
with urllib.request.urlopen(req, timeout=30) as r:
    print(r.status, "-", len(urls), "indirizzi inviati a IndexNow")  # 200 o 202 = ok
