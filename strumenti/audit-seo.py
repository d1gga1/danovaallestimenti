#!/usr/bin/env python3
"""Audit SEO/GEO di tutte le pagine HTML del sito. Uso: python3 strumenti/audit-seo.py"""
import re, os, json, collections, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
pages = []
for d, ds, fs in os.walk(ROOT):
    ds[:] = [x for x in ds if x not in ('.git', 'strumenti', '_google_business', 'node_modules', 'render')]
    for f in fs:
        if f.endswith('.html'): pages.append(os.path.join(d, f))
issues = collections.defaultdict(list)
types = collections.Counter(); titles = collections.defaultdict(list); descs = collections.defaultdict(list)
for p in sorted(pages):
    rel = os.path.relpath(p, ROOT)
    h = open(p, encoding='utf-8').read()
    def has(rx): return re.search(rx, h, re.I | re.S)
    t = has(r'<title>(.*?)</title>'); t = t.group(1).strip() if t else ''
    titles[t].append(rel)
    if not t: issues['no-title'].append(rel)
    elif len(t) > 65: issues['title>65'].append(f'{rel} ({len(t)})')
    m = has(r'<meta\s+name="description"\s+content="(.*?)"')
    d_ = m.group(1) if m else ''
    descs[d_].append(rel)
    if not d_: issues['no-desc'].append(rel)
    elif len(d_) > 165: issues['desc>165'].append(f'{rel} ({len(d_)})')
    elif len(d_) < 70: issues['desc<70'].append(rel)
    if not has(r'<link[^>]+rel="canonical"'): issues['no-canonical'].append(rel)
    if not has(r'<html[^>]+lang='): issues['no-lang'].append(rel)
    if not has(r'hreflang='): issues['no-hreflang'].append(rel)
    if not has(r'property="og:image"'): issues['no-og-image'].append(rel)
    if not has(r'name="twitter:card"'): issues['no-twitter'].append(rel)
    if not has(r'name="viewport"'): issues['no-viewport'].append(rel)
    if has(r'name="robots"[^>]+noindex'): issues['noindex'].append(rel)
    n1 = len(re.findall(r'<h1[\s>]', h, re.I))
    if n1 != 1: issues[f'h1!=1'].append(f'{rel} ({n1})')
    for img in re.findall(r'<img\b[^>]*>', h, re.I):
        if not re.search(r'\balt=', img): issues['img-no-alt'].append(rel)
        elif re.search(r'\balt=""', img): issues['img-empty-alt'].append(rel)
        if not re.search(r'\bwidth=', img): issues['img-no-dim'].append(rel)
        if not re.search(r'loading=', img) and not re.search(r'fetchpriority', img): issues['img-no-loading'].append(rel)
    blocks = re.findall(r'<script type="application/ld\+json">(.*?)</script>', h, re.S)
    if not blocks: issues['no-jsonld'].append(rel)
    for b in blocks:
        try:
            j = json.loads(b)
        except Exception as e:
            issues['jsonld-invalid'].append(f'{rel}: {e}'); continue
        items = j.get('@graph', [j]) if isinstance(j, dict) else j
        for it in items:
            ty = it.get('@type'); ty = ty if isinstance(ty, list) else [ty]
            for x in ty: types[x] += 1
    if 'BreadcrumbList' not in h and rel != 'index.html': issues['no-breadcrumb-ld'].append(rel)
    if not has(r'dateModified'): issues['no-dateModified'].append(rel)
    if has(r'<script(?![^>]*(defer|async|type="application/ld))[^>]*src='): issues['render-blocking-js'].append(rel)
    if 'FAQPage' not in h: issues['no-faq'].append(rel)
print('PAGINE:', len(pages))
print('TIPI JSON-LD:', dict(types.most_common()))
for k, v in sorted(issues.items(), key=lambda x: -len(x[1])):
    u = sorted(set(v)); print(f'\n## {k}: {len(u)}'); [print('  ', x) for x in u[:8]]
dup = {k: v for k, v in titles.items() if len(v) > 1}
print('\n## titoli duplicati:', len(dup)); [print('  ', k[:70], v[:3]) for k, v in list(dup.items())[:8]]
dup = {k: v for k, v in descs.items() if len(v) > 1 and k}
print('## description duplicate:', len(dup)); [print('  ', k[:70], v[:3]) for k, v in list(dup.items())[:8]]
