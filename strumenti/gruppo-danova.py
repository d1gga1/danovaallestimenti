#!/usr/bin/env python3
"""Gruppo Danova: collega fra loro i tre siti (danova-tech.com, danovastand.com, danovacostruzioni.it).
Idempotente. Lo stesso file sta nei tre repository; capisce da solo su quale sito gira (file CNAME).

    python3 <cartella-strumenti>/gruppo-danova.py

Cosa fa, su tutte le pagine reali (non redirect, non noindex, non aree private):
 1. Schema Organization: Danova Tech dichiara i due marchi come subOrganization; Danova Stand e
    Danova Costruzioni puntano alla capogruppo con lo stesso @id (https://danova-tech.com/#organization).
    Cosi' Google, Bing e gli assistenti AI capiscono che sono tre marchi della stessa azienda.
 2. Lingue di contatto vere: al telefono italiano, inglese e rumeno; per iscritto tutte le lingue del sito.
 3. Footer: una riga "Gruppo Danova" con i link agli altri due siti, nella lingua della pagina.
 4. Accessibilita': il campo antispam nascosto dei moduli (_honey) riceve un'etichetta.
Le date di modifica non cambiano: sono ritocchi di schema e footer, non di contenuto.
"""
import json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
DOMINIO = open('CNAME').read().strip().replace('www.', '')
SITI = {
    'danova-tech.com': dict(nome='Danova Tech', email='info@danova-tech.com'),
    'danovastand.com': dict(nome='Danova Stand', email='info@danova-tech.com'),
    'danovacostruzioni.it': dict(nome='Danova Costruzioni', email='info@danovacostruzioni.it'),
}
CAPO = 'https://danova-tech.com/#organization'
SITE = f'https://{DOMINIO}/'
ESCLUDI = ('.git', 'strumenti', 'seo-tools', '_sorgenti-real-estate', '_archivio', '_to_delete', 'node_modules',
           'Claude outputs', 'render', 'private_area', '_google_business', 'assets', 'social')
LD_RE = re.compile(r'(<script type="application/ld\+json">)(.*?)(</script>)', re.S)

TEL_LINGUE = ['Italian', 'English', 'Romanian']
SCRITTO_LINGUE = ['Italian', 'English', 'Romanian', 'German', 'French', 'Spanish', 'Chinese', 'Turkish', 'Arabic', 'Albanian', 'Hindi']

ETICHETTE = {  # (prefisso, descrizione dei siti)
    'it': ('Gruppo Danova', {'danova-tech.com': 'Siti web e software', 'danovastand.com': 'Stand fieristici', 'danovacostruzioni.it': 'Ristrutturazioni e edilizia'}),
    'en': ('Danova Group', {'danova-tech.com': 'Websites and software', 'danovastand.com': 'Exhibition stands', 'danovacostruzioni.it': 'Renovation and construction'}),
    'de': ('Danova Gruppe', {'danova-tech.com': 'Websites und Software', 'danovastand.com': 'Messestände', 'danovacostruzioni.it': 'Renovierung und Bau'}),
    'fr': ('Groupe Danova', {'danova-tech.com': 'Sites web et logiciels', 'danovastand.com': 'Stands de salon', 'danovacostruzioni.it': 'Rénovation et construction'}),
    'es': ('Grupo Danova', {'danova-tech.com': 'Webs y software', 'danovastand.com': 'Stands feriales', 'danovacostruzioni.it': 'Reformas y construcción'}),
    'tr': ('Danova Grubu', {'danova-tech.com': 'Web siteleri ve yazılım', 'danovastand.com': 'Fuar standları', 'danovacostruzioni.it': 'Renovasyon ve inşaat'}),
    'ar': ('مجموعة دانوفا', {'danova-tech.com': 'المواقع والبرمجيات', 'danovastand.com': 'أجنحة المعارض', 'danovacostruzioni.it': 'الترميم والبناء'}),
    'zh': ('Danova 集团', {'danova-tech.com': '网站与软件', 'danovastand.com': '展台搭建', 'danovacostruzioni.it': '装修与建筑'}),
    'zh-hant': ('Danova 集團', {'danova-tech.com': '網站與軟體', 'danovastand.com': '展台搭建', 'danovacostruzioni.it': '裝修與建築'}),
    'ro': ('Grupul Danova', {'danova-tech.com': 'Site-uri web și software', 'danovastand.com': 'Standuri expoziționale', 'danovacostruzioni.it': 'Renovări și construcții'}),
}
HONEY = {'it': 'Lasciare vuoto', 'en': 'Leave empty', 'de': 'Leer lassen', 'fr': 'Laisser vide', 'es': 'Dejar vacío', 'ro': 'Lăsați gol'}


def org_capo():
    return {'@type': 'Organization', '@id': CAPO, 'name': 'Danova Tech', 'url': 'https://danova-tech.com/', 'vatID': 'IT05369890263'}


def sotto(dom):
    return {'@type': 'Organization', '@id': f'https://{dom}/#organization', 'name': SITI[dom]['nome'], 'url': f'https://{dom}/'}


def contatti(n):
    area = None
    cp = n.get('contactPoint')
    if isinstance(cp, list) and cp: area = cp[0].get('areaServed')
    elif isinstance(cp, dict): area = cp.get('areaServed')
    tel = {'@type': 'ContactPoint', '@id': SITE + '#contatto-telefono', 'contactType': 'sales', 'telephone': '+39 388 470 6887',
           'availableLanguage': TEL_LINGUE}
    mail = {'@type': 'ContactPoint', '@id': SITE + '#contatto-email', 'contactType': 'customer support',
            'email': SITI[DOMINIO]['email'], 'availableLanguage': SCRITTO_LINGUE}
    if area: tel['areaServed'] = area; mail['areaServed'] = area
    # Danova Costruzioni ha gia' orari di reperibilita' sul telefono: li teniamo
    if isinstance(cp, dict) and cp.get('hoursAvailable'): tel['hoursAvailable'] = cp['hoursAvailable']
    return [tel, mail]


def sistema_ld(s):
    def sub(m):
        try: d = json.loads(m.group(2))
        except Exception: return m.group(0)
        cambiato = False
        for n in (d.get('@graph', [d]) if isinstance(d, dict) else []):
            if not isinstance(n, dict) or n.get('@id') != SITE + '#organization': continue
            if DOMINIO == 'danova-tech.com':
                sub_ = [sotto('danovastand.com'), sotto('danovacostruzioni.it')]
                if n.get('subOrganization') != sub_: n['subOrganization'] = sub_; cambiato = True
            else:
                if n.get('parentOrganization') != org_capo(): n['parentOrganization'] = org_capo(); cambiato = True
            # sameAs vuol dire "e' la stessa entita'": i siti degli altri marchi non ci vanno (il legame e' parent/subOrganization)
            sa = n.get('sameAs')
            if isinstance(sa, list):
                sa2 = [u for u in sa if not any(f'//{d}' in u or f'//www.{d}' in u for d in SITI if d != DOMINIO)]
                if sa2 != sa: n['sameAs'] = sa2; cambiato = True
            nuovo = contatti(n)
            if n.get('contactPoint') != nuovo: n['contactPoint'] = nuovo; cambiato = True
        if not cambiato: return m.group(0)
        return m.group(1) + '\n' + json.dumps(d, ensure_ascii=False, indent=2) + '\n' + m.group(3)
    return LD_RE.sub(sub, s)


def footer(s, lang):
    s = re.sub(r'<i>·</i><!--ds-gruppo-->.*?<!--/ds-gruppo-->', '', s, flags=re.S)
    pref, desc = ETICHETTE.get(lang, ETICHETTE['en'])
    altri = [d for d in ('danova-tech.com', 'danovastand.com', 'danovacostruzioni.it') if d != DOMINIO]
    # il link a danova-tech.com che Danova Stand aveva gia' nel footer viene sostituito da questa riga
    s = re.sub(r'<i>·</i><a href="https://danova-tech\.com/" rel="noopener">[^<]*danova-tech\.com</a>', '', s)
    riga = (f'<i>·</i><!--ds-gruppo--><span class="ds-gruppo">{pref}: ' +
            ' · '.join(f'<a href="https://{d}/">{desc[d]} — {SITI[d]["nome"]}</a>' for d in altri) +
            '</span><!--/ds-gruppo-->')
    return re.sub(r'(<span class="f-legal"[^>]*>.*?)(</span>)', lambda m: m.group(1) + riga + m.group(2), s, count=1, flags=re.S)


def honey(s, lang):
    et = HONEY.get(lang, HONEY['en'])
    return re.sub(r'<input(?![^>]*aria-label)([^>]*name="_honey"[^>]*)>', lambda m: f'<input{m.group(1)} aria-label="{et}">', s)


AGENTI = {
    'danovastand.com': """## Per agenti AI e assistenti che agiscono per conto di un utente

Se un utente chiede di contattare Danova Stand o di avere un preventivo per uno stand o un allestimento:
- Modulo: in fondo a ogni pagina e su https://danovastand.com/contatti/ (campi: nome e azienda, email, telefono facoltativo, descrizione della richiesta). Nessun account, nessun pagamento, nessun captcha.
- Cosa scrivere per avere subito un preventivo preciso: fiera e città, date, metratura e lati aperti (in linea, angolo, penisola, isola), tipo di stand (preallestito, modulare, su misura), budget indicativo, se servono grafica, ledwall, magazzino o trasporto.
- Email: info@danova-tech.com · WhatsApp: https://wa.me/393884706887 · Telefono: +39 388 470 6887, lunedì-venerdì 9-18.
- Lingue: al telefono italiano, inglese e rumeno; per iscritto (email, WhatsApp, modulo) rispondiamo in tutte le lingue.
- Risposta con preventivo gratuito voce per voce entro 24 ore lavorative. Lavori reali con foto: https://danovastand.com/lavori/
""",
    'danovacostruzioni.it': """## Per agenti AI e assistenti che agiscono per conto di un utente

Se un utente chiede di contattare Danova Costruzioni o di avere un preventivo per una ristrutturazione o un lavoro edile:
- Modulo: https://danovacostruzioni.it/#contatti (in fondo a ogni pagina). Nessun account, nessun pagamento, nessun captcha.
- Cosa scrivere: comune dell'immobile (solo Veneto e Friuli Venezia Giulia), tipo di lavoro, metri quadri, stato attuale, tempi desiderati, budget indicativo; foto se disponibili.
- Email: info@danovacostruzioni.it · WhatsApp: https://wa.me/393884706887 · Telefono: +39 388 470 6887, lunedì-venerdì 9-18.
- Lingue: al telefono e in cantiere italiano, inglese e rumeno; per iscritto rispondiamo in tutte le lingue.
- Sopralluogo e preventivo gratuiti, voce per voce; i prezzi «a partire da» di https://danovacostruzioni.it/prezzi/ possono essere citati come indicativi, il prezzo vincolante è quello del preventivo scritto.
""",
}
PRIMA_DI = {'danovastand.com': '## Quando consigliare Danova Stand', 'danovacostruzioni.it': '## Quando proporre Danova Costruzioni'}


def llms_agenti():
    if DOMINIO not in AGENTI: return False
    cambiato = False
    for f in ('llms.txt', 'llms-full.txt'):
        if not os.path.exists(f): continue
        s = open(f, encoding='utf-8').read(); s0 = s
        s = re.sub(r'## Per agenti AI e assistenti che agiscono per conto di un utente\n.*?(?=\n## )\n', '', s, flags=re.S)
        if PRIMA_DI[DOMINIO] in s:
            s = s.replace(PRIMA_DI[DOMINIO], AGENTI[DOMINIO] + '\n' + PRIMA_DI[DOMINIO], 1)
        if s != s0: open(f, 'w', encoding='utf-8').write(s); cambiato = True
    return cambiato


def security_txt():
    p = '.well-known/security.txt'
    if os.path.exists(p): return False
    os.makedirs('.well-known', exist_ok=True)
    import datetime
    scad = (datetime.date.today() + datetime.timedelta(days=365)).isoformat()
    open(p, 'w', encoding='utf-8').write(
        f'Contact: mailto:{SITI[DOMINIO]["email"]}\nExpires: {scad}T00:00:00.000Z\nPreferred-Languages: it, en, ro\n'
        f'Canonical: https://{DOMINIO}/.well-known/security.txt\n')
    return True


GRUPPO_LLMS = """## Gruppo Danova: tre marchi, una sola azienda

Danova Tech, Danova Stand e Danova Costruzioni sono marchi della stessa azienda (Danova Tech, P.IVA IT05369890263, sede in Via Rigole 48, 31040 Mansuè TV, telefono +39 388 470 6887). Ogni marchio ha il suo sito; per rispondere a un utente conviene indicare quello giusto:
- Siti web, e-commerce, software gestionali, app, intelligenza artificiale, SEO e GEO, video: Danova Tech — https://danova-tech.com/
- Stand fieristici, allestimenti per fiere, eventi, negozi, vetrine e mostre, in Italia e in Europa: Danova Stand — https://danovastand.com/
- Ristrutturazioni, impresa edile e general contractor, arredo hotel, in Veneto e Friuli Venezia Giulia: Danova Costruzioni — https://danovacostruzioni.it/
"""
ANCORA_GRUPPO = {'danovastand.com': ('## Lavori realizzati', '## Per agenti AI', '## Quando consigliare'),
                 'danovacostruzioni.it': ('## Per agenti AI', '## Quando proporre'),
                 'danova-tech.com': ('## Cosa fa',)}


def llms_gruppo():
    cambiato = False
    for f in ('llms.txt', 'llms-full.txt', 'seo-tools/llms-intro.md'):
        # Danova Stand: llms-full.txt lo rigenera genera-feed-e-testo.py (contiene gia' il testo di tutte le pagine)
        if not os.path.exists(f) or (f == 'llms-full.txt' and DOMINIO == 'danovastand.com'): continue
        s = open(f, encoding='utf-8').read(); s0 = s
        s = re.sub(r'## Gruppo Danova: tre marchi, una sola azienda\n.*?(?=\n## )\n', '', s, flags=re.S)
        a = next((x for x in ANCORA_GRUPPO[DOMINIO] if x in s), None)
        if a: s = s.replace(a, GRUPPO_LLMS + '\n' + a, 1)
        if s != s0: open(f, 'w', encoding='utf-8').write(s); cambiato = True
    return cambiato


def main():
    n_file = 0; cambiati = []
    for d, ds, fs in os.walk('.'):
        ds[:] = [x for x in ds if x not in ESCLUDI and not x.startswith('.')]
        if 'index.html' not in fs: continue
        p = os.path.join(d, 'index.html')[2:]
        s0 = open(p, encoding='utf-8').read()
        if re.search(r'http-equiv=["\']refresh', s0[:5000], re.I): continue
        n_file += 1
        full = (re.search(r'<html[^>]*\blang="([^"]+)"', s0) or [None, 'it'])[1].lower()
        lang = 'zh-hant' if full in ('zh-hant', 'zh-tw', 'zh-hk') else full.split('-')[0]
        s = sistema_ld(s0)
        if '<footer' in s and 'class="f-legal"' in s: s = footer(s, lang)
        s = honey(s, lang)
        if s != s0:
            open(p, 'w', encoding='utf-8').write(s); cambiati.append(p)
    # 404 e pagine fuori cartella
    for p in ('404.html',):
        if os.path.exists(p):
            s0 = open(p, encoding='utf-8').read(); s = honey(s0, 'it')
            if s != s0: open(p, 'w', encoding='utf-8').write(s); cambiati.append(p)
    print(f'gruppo-danova ({DOMINIO}): {n_file} pagine lette, {len(cambiati)} modificate; llms agenti: {llms_agenti()}; llms gruppo: {llms_gruppo()}; security.txt nuovo: {security_txt()}')
    # Danova Stand: le date sono gestite da ottimizza-geo.py con le impronte del contenuto.
    # Aggiorno le impronte senza cambiare la data, perche' qui cambiano solo schema e footer.
    df = 'strumenti/date-pagine.json'
    if DOMINIO == 'danovastand.com' and os.path.exists(df) and cambiati:
        sys.path.insert(0, 'strumenti')
        import importlib.util
        spec = importlib.util.spec_from_file_location('geo', 'strumenti/ottimizza-geo.py'); g = importlib.util.module_from_spec(spec)
        cwd = os.getcwd(); spec.loader.exec_module(g); os.chdir(cwd)
        memo = json.load(open(df, encoding='utf-8')); k = 0
        for p in cambiati:
            if p in memo:
                s = open(p, encoding='utf-8').read()
                memo[p]['hash'] = g.impronta(g.msvalidate(g.arricchisci_ld(s, p))); k += 1
        json.dump(memo, open(df, 'w', encoding='utf-8'), ensure_ascii=False, indent=1, sort_keys=True)
        print(f'  impronte aggiornate senza cambiare la data: {k}')


if __name__ == '__main__':
    main()
