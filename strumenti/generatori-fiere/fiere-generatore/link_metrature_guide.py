# -*- coding: utf-8 -*-
"""Collega pagine per metratura e guide fiere del 14/10/2026: box 'Approfondisci', indice /guide/, llms.txt. Idempotente.
Uso (da seo-tools/fiere-generatore): python3 link_metrature_guide.py"""
import os, re, json
import dati_metrature_guide as D
R = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
HUB = ("/stand-fieristici-per-metratura/", "Stand per metratura")
MQ = {x['mq']: (f"/{x['slug']}/", f"Stand {x['mq']} mq" + (" e oltre" if x['mq'] == 100 else "")) for x in D.M}
GD = {g['slug']: (f"/guide/{g['slug']}/", re.sub(r'<[^>]+>', '', g['h1']).split(':')[0]) for g in D.G}
L = {
 'stand-fieristici-piccoli': [HUB, MQ[9], MQ[12], MQ[16], MQ[24]],
 'stand-ad-angolo': [HUB, MQ[16], MQ[24], MQ[32]],
 'stand-a-isola': [HUB, MQ[48], MQ[100]],
 'stand-a-due-piani': [MQ[100], GD['regolamento-tecnico-fiera']],
 'stand-preallestiti': [MQ[9], MQ[12], MQ[16]],
 'stand-modulari': [HUB, MQ[24], MQ[32]],
 'stand-fieristici-su-misura': [MQ[32], MQ[48], MQ[100]],
 'quanto-costa-uno-stand-fieristico': [HUB, GD['quanto-costa-partecipare-a-una-fiera'], GD['come-scegliere-un-allestitore-fieristico']],
 'servizi/allestimenti-fieristici': [HUB, GD['come-scegliere-un-allestitore-fieristico'], GD['regolamento-tecnico-fiera'], GD['quanto-costa-partecipare-a-una-fiera']],
 'montaggio-stand-fieristici': [GD['dichiarazione-di-conformita-stand'], GD['regolamento-tecnico-fiera'], GD['come-scegliere-un-allestitore-fieristico']],
 'progettazione-stand-fieristici': [GD['regolamento-tecnico-fiera'], HUB],
 'grafica-per-stand-fieristici': [GD['materiali-ignifughi-stand'], GD['come-attirare-visitatori-allo-stand']],
 'ledwall-e-illuminazione-stand': [GD['dichiarazione-di-conformita-stand'], GD['come-attirare-visitatori-allo-stand']],
 'idee-stand-fieristici': [GD['come-attirare-visitatori-allo-stand'], GD['come-raccogliere-contatti-in-fiera'], HUB],
 'espositori-desk-totem-per-fiere': [GD['come-raccogliere-contatti-in-fiera'], GD['come-attirare-visitatori-allo-stand']],
 'contributi-fiere-2026': [GD['quanto-costa-partecipare-a-una-fiera']],
 'guide/come-preparare-una-fiera': [GD['regolamento-tecnico-fiera'], GD['come-attirare-visitatori-allo-stand'], GD['come-raccogliere-contatti-in-fiera'], GD['quanto-costa-partecipare-a-una-fiera'], GD['come-scegliere-un-allestitore-fieristico']],
 'stand-fieristici-ecosostenibili': [GD['materiali-ignifughi-stand']],
 'noleggio-stand-fieristici': [HUB, GD['quanto-costa-partecipare-a-una-fiera']],
 'lead-generation-b2b': [GD['come-raccogliere-contatti-in-fiera']],
 'crm-aziendale': [GD['come-raccogliere-contatti-in-fiera']],
 'calendario-fiere': [HUB, GD['regolamento-tecnico-fiera'], GD['quanto-costa-partecipare-a-una-fiera']],
}
n = 0
for page, links in L.items():
    f = os.path.join(R, page, 'index.html')
    if not os.path.exists(f): print('manca', page); continue
    s = open(f, encoding='utf-8').read(); o = s
    m = re.search(r'<div class="pg-altri" data-rv="up">', s)
    if not m: print('niente box', page); continue
    add = ''.join(f'\n      <a href="{u}">{t}</a>' for u, t in links if f'href="{u}"' not in s[m.end():m.end() + 6000].split('</div>')[0])
    s = s[:m.end()] + add + s[m.end():]
    if s != o: open(f, 'w', encoding='utf-8').write(s); n += 1
print('box Approfondisci aggiornati:', n)

# indice /guide/
f = os.path.join(R, 'guide', 'index.html'); s = open(f, encoding='utf-8').read(); o = s
m = re.search(r'<a class="sect sect-zone" href="/guide/come-preparare-una-fiera/">.*?</a>(?=<a class="sect)', s, re.S)
if m:
    card = m.group(0); ins = ''
    for g in D.G:
        u = f"/guide/{g['slug']}/"
        if f'href="{u}"' in s: continue
        h4 = re.sub(r'<[^>]+>', '', g['h1']).rstrip('.')
        c = card.replace('/guide/come-preparare-una-fiera/', u)
        c = re.sub(r'<h4>.*?</h4>', f'<h4>{h4}</h4>', c, 1, flags=re.S)
        c = re.sub(r'<p>.*?</p>', f"<p>{g['desc']}</p>", c, 1, flags=re.S)
        ins += c
    s = s[:m.end()] + ins + s[m.end():]
    j = re.search(r'(<script type="application/ld\+json">)(.*?)(</script>)', s, re.S)
    try:
        gr = json.loads(j.group(2))
        for node in gr.get('@graph', []):
            if node.get('@type') == 'ItemList':
                have = {x.get('url') for x in node['itemListElement']}
                for g in D.G:
                    u = f"https://danova-tech.com/guide/{g['slug']}/"
                    if u not in have:
                        node['itemListElement'].append({"@type": "ListItem", "position": len(node['itemListElement']) + 1, "url": u, "name": re.sub(r'<[^>]+>', '', g['h1'])})
        s = s[:j.start(2)] + '\n' + json.dumps(gr, ensure_ascii=False, indent=2) + '\n' + s[j.end(2):]
    except Exception as e: print('itemlist', e)
if s != o: open(f, 'w', encoding='utf-8').write(s); print('indice guide aggiornato')

# llms.txt
f = os.path.join(R, 'llms.txt'); s = open(f, encoding='utf-8').read()
if 'Stand per metratura' not in s:
    lines = ["", "### Stand per metratura e guide fiere (14 ottobre 2026)", f"- Stand per metratura: https://danova-tech.com{HUB[0]}"]
    lines += [f"- {t}: https://danova-tech.com{u}" for u, t in MQ.values()]
    lines += [f"- Guida: {t}: https://danova-tech.com{u}" for u, t in GD.values()]
    lines += ["- Dati aziendali: squadre di montaggio proprie, magazzino proprio, produzione interna di strutture e arredi in legno; stand a due piani; stand anche oltre i 300 mq.",
              "- Esperienza dichiarata: Vinitaly, Marmomac, Salone del Mobile, EICMA, Host, Cosmoprof, Cersaie, EIMA, Sigep, MICAM, MIDO, Lineapelle, VicenzaOro, Ecomondo, Macfrut, Sicam, Samuexpo."]
    s = s.replace('\n## Pagine principali', '\n'.join(lines) + '\n\n## Pagine principali', 1)
    open(f, 'w', encoding='utf-8').write(s); print('llms aggiornato')
