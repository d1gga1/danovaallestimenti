# -*- coding: utf-8 -*-
"""Cinese tradizionale (Hong Kong, Taiwan, Macao): converte tutte le pagine /zh/ in /zh-hant/ con OpenCC (s2t).
14 ottobre 2026. Va lanciato DOPO build_intl.py e lingue.py (che generano le pagine /zh/).
Richiede: pip3 install opencc-python-reimplemented
Uso: python3 build_hant.py"""
import os, re, json, glob
import opencc
R = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
SITE = 'https://danova-tech.com'
CC = opencc.OpenCC('s2t')

def conv_text(s):
    # converte solo il testo cinese: i caratteri ASCII (URL, codice) restano uguali
    return CC.convert(s)

n = 0
for f in sorted(glob.glob(os.path.join(R, 'zh', '*', 'index.html'))):
    rel = os.path.relpath(os.path.dirname(f), os.path.join(R, 'zh')).replace('\\', '/')
    src_path = f'/zh/{rel}/'; dst_path = f'/zh-hant/{rel}/'
    s = open(f, encoding='utf-8').read()
    # blocco hreflang originale (contiene gia' zh-Hant -> /zh-hant/)
    hl = re.findall(r'<link rel="alternate" hreflang="[^"]*" href="[^"]*">\n', s)
    s = conv_text(s)
    s = s.replace('href="/zh/', 'href="/zh-hant/').replace(f'{SITE}/zh/', f'{SITE}/zh-hant/')
    # ripristina hreflang e selettore lingua corretti
    lines = list(re.finditer(r'<link rel="alternate" hreflang="[^"]*" href="[^"]*">\n', s))
    if lines and hl:
        s = s[:lines[0].start()] + ''.join(hl) + ''.join(s[a.end():b.start()] for a, b in zip(lines, lines[1:])) + s[lines[-1].end():]
    s = re.sub(r'<a href="/zh-hant/([^"]*)" hreflang="zh-Hans"', r'<a href="/zh/\1" hreflang="zh-Hans"', s)
    s = re.sub(r'(<a href="/zh/[^"]*" hreflang="zh-Hans") aria-current="page"', r'\1', s)
    s = re.sub(r'(<a href="/zh-hant/[^"]*" hreflang="zh-Hant")(>)', r'\1 aria-current="page"\2', s)
    s = s.replace('<html lang="zh-Hans"', '<html lang="zh-Hant"')
    s = s.replace('"inLanguage": "zh-Hans"', '"inLanguage": "zh-Hant"').replace('"inLanguage": "zh"', '"inLanguage": "zh-Hant"')
    s = s.replace('<meta property="og:locale" content="zh_CN">', '<meta property="og:locale" content="zh_TW">')
    s = re.sub(r'<meta property="og:locale:alternate" content="zh_TW">\n', '<meta property="og:locale:alternate" content="zh_CN">\n', s)
    # il selettore deve mostrare la pagina corrente senza doppio aria-current
    for m in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', s, re.S):
        json.loads(m.group(1))
    out = os.path.join(R, 'zh-hant', rel, 'index.html')
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out, 'w', encoding='utf-8').write(s); n += 1
print('pagine zh-hant:', n)
