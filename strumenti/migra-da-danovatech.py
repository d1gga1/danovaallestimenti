#!/usr/bin/env python3
"""
Danova Stand — importa da Danova Tech tutte le pagine sugli allestimenti.

Uso (dalla cartella del repository danova_allestimenti):
    python3 strumenti/migra-da-danovatech.py [cartella-danovatech]

Default cartella sorgente: ~/Desktop/dantech/danovatech

Cosa fa (si puo' rilanciare quante volte vuoi, sovrascrive i file generati):
  1. copia le pagine stand / fiere / allestimenti (elenco: strumenti/pagine.txt)
     piu' pagine legali, contatti e 404, mantenendo gli stessi indirizzi;
  2. dominio danova-tech.com -> danovastand.com, marchio Danova Tech -> Danova Stand;
  3. sostituisce menu e footer con quelli solo-stand, in ogni lingua;
  4. i link a pagine NON importate (siti web, software, SEO...) diventano link
     esterni a https://danova-tech.com/...;
  5. la home "/" e' l'ex hub /stand-fieristici/ (che diventa un redirect);
  6. copia gli asset usati, genera sitemap.xml, robots.txt, llms.txt, manifest,
     redirect-danovatech.csv (vecchio indirizzo -> nuovo, per i 301).
"""
import json, os, re, shutil, sys, datetime, html

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = sys.argv[1] if len(sys.argv) > 1 else os.path.expanduser('~/Desktop/dantech/danovatech')
OLD = 'https://danova-tech.com'
NEW = 'https://danovastand.com'
OLD_BRAND, NEW_BRAND = 'Danova Tech', 'Danova Stand'
EXT = '@@EXT@@'   # segnaposto per link che devono restare su danova-tech.com
DT = '@@DT@@'     # segnaposto per "Danova Tech" da NON rinominare
TODAY = datetime.date.today().isoformat()
YEAR = datetime.date.today().year

PAGES = [l.strip() for l in open(os.path.join(REPO, 'strumenti', 'pagine.txt'), encoding='utf-8')
         if l.strip() and not l.startswith('#')]
LEGAL = ['privacy/', 'cookie-policy/', 'termini/', 'contatti/',
         'en/privacy/', 'en/cookie-policy/', 'en/terms/', 'en/contact/',
         'de/datenschutz/', 'de/cookie-richtlinie/', 'de/agb/', 'de/kontakt/',
         'fr/confidentialite/', 'fr/cookies/', 'fr/conditions/', 'fr/contact/',
         'es/privacidad/', 'es/cookies/', 'es/condiciones/', 'es/contacto/']
ALL = PAGES + LEGAL
MIGRATED = set('/' + p for p in ALL) | {'/'}

HUB = {'it': '/', 'en': '/en/exhibition-stand-builder-italy/', 'de': '/de/messebau-italien/',
       'fr': '/fr/standiste-salon-italie/', 'es': '/es/montaje-stands-feriales-italia/',
       'zh-Hans': '/zh/italy-exhibition-stand/', 'zh-Hant': '/zh-hant/italy-exhibition-stand/',
       'tr': '/tr/italya-fuar-standi/', 'ar': '/ar/italy-exhibition-stand/'}

# indirizzi di Danova Tech che nel nuovo sito puntano a una pagina equivalente
# (per questi si crea anche una pagina-redirect, cosi' non danno 404)
SPECIAL = {
    '/stand-fieristici/': '/',
    '/servizi/': '/servizi/allestimenti-fieristici/',
    '/prezzi/': '/quanto-costa-uno-stand-fieristico/',
    '/lavori/': '/progetti-stand-fieristici/',
    '/guide/': '/#guide',
    '/en/': HUB['en'], '/en/pricing/': HUB['en'], '/en/services/': HUB['en'],
    '/de/': HUB['de'], '/de/preise/': HUB['de'], '/de/leistungen/': HUB['de'],
    '/fr/': HUB['fr'], '/fr/tarifs/': HUB['fr'], '/fr/services/': HUB['fr'],
    '/es/': HUB['es'], '/es/precios/': HUB['es'], '/es/servicios/': HUB['es'],
    '/zh/': HUB['zh-Hans'], '/zh-hant/': HUB['zh-Hant'], '/tr/': HUB['tr'], '/ar/': HUB['ar'],
}


def remap_path(path):
    """path relativo al sito (inizia con /). Ritorna il nuovo href."""
    base, sep, frag = path.partition('#')
    base2, qsep, q = base.partition('?')
    if base2 in SPECIAL:
        tgt = SPECIAL[base2]
        if frag and '#' not in tgt:
            tgt += '#' + frag
        return tgt
    if base2 in MIGRATED or base2.startswith('/assets/') or re.search(r'\.\w{2,12}$', base2):
        if base2 in ('/feed.xml',):
            return EXT + path
        return path
    return EXT + path


def remap_url(u):
    if u.startswith(OLD):
        rest = u[len(OLD):] or '/'
        r = remap_path(rest)
        return r if r.startswith(EXT) else NEW + r
    if u.startswith('/') and not u.startswith('//'):
        return remap_path(u)
    return u


ATTR = re.compile(r'\b(href|src|content|poster|data-src|action)="([^"]*)"')


def remap_attrs(s):
    def f(m):
        name, val = m.group(1), m.group(2)
        if name == 'content' and not (val.startswith(OLD) or val.startswith('/')):
            return m.group(0)
        return '%s="%s"' % (name, remap_url(val))
    s = ATTR.sub(f, s)
    # srcset: lista di url
    s = re.sub(r'\bsrcset="([^"]*)"', lambda m: 'srcset="%s"' % ', '.join(
        ' '.join([remap_url(x.strip().split(' ')[0])] + x.strip().split(' ')[1:])
        for x in m.group(1).split(',') if x.strip()), s)
    return s


# ---------------------------------------------------------------- testi per lingua
T = {
 'it': dict(
    nav=[('Servizi', '/servizi/allestimenti-fieristici/'), ('Tipi di stand', '/#tipi'),
         ('Fiere', '/calendario-fiere/'), ('Città', '/#citta'), ('Progetti', '/progetti-stand-fieristici/'),
         ('Prezzi', '/quanto-costa-uno-stand-fieristico/'), ('Guide', '/#guide')],
    contact='Contatti',
    desc='Stand fieristici e allestimenti chiavi in mano: progetto 3D, produzione, trasporto, montaggio e smontaggio, in Italia e in Europa.',
    cols=[('Stand', [('Allestimenti fieristici', '/servizi/allestimenti-fieristici/'),
                     ('Stand su misura', '/stand-fieristici-su-misura/'), ('Stand modulari', '/stand-modulari/'),
                     ('Stand preallestiti', '/stand-preallestiti/'), ('Noleggio stand', '/noleggio-stand-fieristici/'),
                     ('Progettazione e render 3D', '/progettazione-stand-fieristici/'),
                     ('Montaggio stand', '/montaggio-stand-fieristici/'), ('Grafica per stand', '/grafica-per-stand-fieristici/'),
                     ('Ledwall e illuminazione', '/ledwall-e-illuminazione-stand/'),
                     ('Moquette', '/moquette-per-stand-fieristici/'),
                     ('Espositori, desk e totem', '/espositori-desk-totem-per-fiere/'),
                     ('Trasporto e magazzino', '/trasporto-e-magazzino-stand-fieristici/'),
                     ('Eventi, showroom, negozi', '/allestimenti-eventi-showroom-negozi/'),
                     ('Progetti di stand', '/progetti-stand-fieristici/'),
                     ('Quanto costa uno stand', '/quanto-costa-uno-stand-fieristico/')]),
          ('Fiere e città', [('Calendario fiere', '/calendario-fiere/'), ('Contributi fiere 2026', '/contributi-fiere-2026/'),
                     ('Fiere all\'estero', '/allestimenti-fieristici-estero/'),
                     ('Stand a Verona', '/allestimenti-fieristici-verona/'), ('Stand a Milano', '/allestimenti-fieristici-milano/'),
                     ('Stand a Bologna', '/allestimenti-fieristici-bologna/'), ('Stand a Rimini', '/allestimenti-fieristici-rimini/'),
                     ('Stand a Parma', '/allestimenti-fieristici-parma/'), ('Stand a Padova', '/allestimenti-fieristici-padova/'),
                     ('Stand a Vicenza', '/allestimenti-fieristici-vicenza/'), ('Stand a Treviso', '/allestimenti-fieristici-treviso/'),
                     ('Stand in Germania', '/allestimenti-fieristici-germania/')]),
          ('Guide', [('Come preparare una fiera', '/guide/come-preparare-una-fiera/'),
                     ('Scegliere un allestitore', '/guide/come-scegliere-un-allestitore-fieristico/'),
                     ('Quanto costa una fiera', '/guide/quanto-costa-partecipare-a-una-fiera/'),
                     ('Regolamento tecnico', '/guide/regolamento-tecnico-fiera/'),
                     ('Materiali ignifughi', '/guide/materiali-ignifughi-stand/'),
                     ('Dichiarazione di conformità', '/guide/dichiarazione-di-conformita-stand/'),
                     ('Sicurezza dello stand', '/sicurezza-stand-fieristici/'),
                     ('Idee per stand', '/idee-stand-fieristici/')])],
    legal=[('Privacy Policy', '/privacy/'), ('Cookie Policy', '/cookie-policy/'),
           ('Termini e condizioni d’uso', '/termini/'), ('Contatti', '/contatti/')],
    brandof='un marchio di', sister='Siti web e software: danova-tech.com', home='Torna alla home'),
 'en': dict(
    nav=[('Stand builder Italy', HUB['en']), ('Trade fairs in Italy', '/en/exhibiting-at-trade-fairs-in-italy/'),
         ('Europe', '/en/exhibition-stand-builder-europe/')],
    contact='Contact',
    desc='Turnkey exhibition stands: 3D design, production, transport, installation and dismantling, in Italy and across Europe.',
    cols=[('Stands', [('Exhibition stand builder Italy', HUB['en']),
                      ('Exhibiting at trade fairs in Italy', '/en/exhibiting-at-trade-fairs-in-italy/'),
                      ('Stand builder Europe', '/en/exhibition-stand-builder-europe/'),
                      ('Stand builder Milan', '/en/exhibition-stand-builder-milan/'),
                      ('Stand builder Verona', '/en/exhibition-stand-builder-verona/'),
                      ('Stand builder Bologna', '/en/exhibition-stand-builder-bologna/'),
                      ('Stand builder Rimini', '/en/exhibition-stand-builder-rimini/'),
                      ('Stand builder Parma', '/en/exhibition-stand-builder-parma/')]),
          ('Trade fairs', [('Vinitaly', '/en/vinitaly-stand-builder/'), ('Salone del Mobile', '/en/salone-del-mobile-stand-builder/'),
                      ('EICMA', '/en/eicma-stand-builder/'), ('Cersaie', '/en/cersaie-stand-builder/'),
                      ('Marmomac', '/en/marmomac-stand-builder/'), ('Cosmoprof', '/en/cosmoprof-stand-builder/'),
                      ('Hannover Messe', '/en/hannover-messe-stand-builder/'), ('MWC Barcelona', '/en/mwc-barcelona-stand-builder/')])],
    legal=[('Privacy Policy', '/en/privacy/'), ('Cookie Policy', '/en/cookie-policy/'),
           ('Terms of use', '/en/terms/'), ('Contact', '/en/contact/')],
    brandof='a brand of', sister='Websites and software: danova-tech.com', home='Back to home'),
 'de': dict(
    nav=[('Messebau Italien', HUB['de']), ('Messebau Mailand', '/de/messebau-mailand/')],
    contact='Kontakt',
    desc='Messestände schlüsselfertig: 3D-Planung, Produktion, Transport, Auf- und Abbau – in Italien und in ganz Europa.',
    cols=[('Messebau', [('Messebau Italien', HUB['de']), ('Messebau Mailand', '/de/messebau-mailand/')])],
    legal=[('Datenschutzerklärung', '/de/datenschutz/'), ('Cookie-Richtlinie', '/de/cookie-richtlinie/'),
           ('Allgemeine Nutzungsbedingungen', '/de/agb/'), ('Kontakt', '/de/kontakt/')],
    brandof='eine Marke von', sister='Websites und Software: danova-tech.com', home='Zurück zur Startseite'),
 'fr': dict(
    nav=[('Standiste en Italie', HUB['fr'])], contact='Contact',
    desc='Stands d’exposition clés en main : conception 3D, fabrication, transport, montage et démontage, en Italie et en Europe.',
    cols=[],
    legal=[('Politique de confidentialité', '/fr/confidentialite/'), ('Cookies', '/fr/cookies/'),
           ('Conditions d’utilisation', '/fr/conditions/'), ('Contact', '/fr/contact/')],
    brandof='une marque de', sister='Sites web et logiciels : danova-tech.com', home='Retour à l’accueil'),
 'es': dict(
    nav=[('Stands en Italia', HUB['es'])], contact='Contacto',
    desc='Stands feriales llave en mano: diseño 3D, fabricación, transporte, montaje y desmontaje, en Italia y en Europa.',
    cols=[],
    legal=[('Política de privacidad', '/es/privacidad/'), ('Cookies', '/es/cookies/'),
           ('Condiciones de uso', '/es/condiciones/'), ('Contacto', '/es/contacto/')],
    brandof='una marca de', sister='Webs y software: danova-tech.com', home='Volver al inicio'),
 'zh-Hans': dict(
    nav=[('意大利展台', HUB['zh-Hans']), ('展会指南', '/zh/italy-trade-fair-guide/'), ('欧洲展台', '/zh/europe-exhibition-stand/')],
    contact='联系我们',
    desc='意大利交钥匙展台搭建：3D设计、制作、运输、搭建与拆除，覆盖意大利及欧洲。',
    cols=[], brandof='旗下品牌', sister='网站与软件：danova-tech.com', home='Back to home'),
 'zh-Hant': dict(
    nav=[('義大利展臺', HUB['zh-Hant']), ('展會指南', '/zh-hant/italy-trade-fair-guide/'), ('歐洲展臺', '/zh-hant/europe-exhibition-stand/')],
    contact='聯絡我們',
    desc='義大利交鑰匙展臺搭建：3D設計、製作、運輸、搭建與拆除，涵蓋義大利及歐洲。',
    cols=[], brandof='旗下品牌', sister='網站與軟體：danova-tech.com', home='Back to home'),
 'tr': dict(
    nav=[('İtalya fuar standı', HUB['tr'])], contact='İletişim',
    desc='Anahtar teslim fuar standları: 3D tasarım, üretim, nakliye, kurulum ve söküm; İtalya’da ve Avrupa’da.',
    cols=[], brandof='markasıdır', sister='Web siteleri ve yazılım: danova-tech.com', home='Back to home'),
 'ar': dict(
    nav=[('أجنحة المعارض في إيطاليا', HUB['ar'])], contact='اتصل بنا',
    desc='أجنحة معارض جاهزة بالكامل: تصميم ثلاثي الأبعاد، تصنيع، نقل، تركيب وفك، في إيطاليا وأوروبا.',
    cols=[], brandof='علامة تجارية لـ', sister='المواقع والبرمجيات: danova-tech.com', home='Back to home'),
}
for k in ('zh-Hans', 'zh-Hant', 'tr', 'ar'):
    T[k]['legal'] = T['en']['legal']
LANGCOL = ('Lingue / Languages', [('Italiano', '/'), ('English', HUB['en']), ('Deutsch', HUB['de']),
           ('Français', HUB['fr']), ('Español', HUB['es']), ('简体中文', HUB['zh-Hans']),
           ('繁體中文', HUB['zh-Hant']), ('Türkçe', HUB['tr']), ('العربية', HUB['ar'])])


def norm_lang(lang):
    if lang.startswith('zh'):
        return 'zh-Hant' if 'hant' in lang.lower() else 'zh-Hans'
    l = lang[:2]
    return l if l in T else 'en'


def nav_html(L, cta, cur, indent):
    out = []
    for label, href in T[L]['nav']:
        ac = ' aria-current="page"' if href == cur else ''
        out.append('%s<a href="%s"%s>%s</a>' % (indent, href, ac, html.escape(label, quote=False)))
    out.append('%s<a href="%s">%s</a>' % (indent, cta, T[L]['contact']))
    return '\n'.join(out)


def footer_html(L, contact_col):
    t = T[L]
    cols = list(t['cols']) + [LANGCOL]
    parts = ['<footer>\n  <div class="wrap">\n    <div class="f-top z5">\n      <div class="fb">\n'
             '        <span class="brand"><img width="160" height="160" src="/assets/img/logo.png" alt="Logo Danova Stand" loading="lazy" decoding="async"><span class="wordmark"><b>DANOVA</b><i>STAND</i></span></span>\n'
             '        <p>%s</p>\n      </div>\n' % html.escape(t['desc'], quote=False)]
    for h, links in cols:
        lis = '\n'.join('        <li><a href="%s">%s</a></li>' % (u, html.escape(n, quote=False)) for n, u in links)
        parts.append('      <div><h5>%s</h5><ul>\n%s\n      </ul></div>\n' % (h, lis))
    if contact_col:
        parts.append('      ' + contact_col + '\n')
    legal = '<i>·</i>'.join('<a href="%s">%s</a>' % (u, n) for n, u in t['legal'])
    if L.startswith('zh') or L == 'tr':
        owner = '%s %s' % (DT, t['brandof'])
    else:
        owner = '%s %s' % (t['brandof'], DT)
    parts.append('    </div>\n    <div class="f-bot">\n'
                 '      <span>© <span id="yy">%d</span> Danova Stand — %s — P.IVA 05369890263</span>\n'
                 '      <span class="f-legal">%s<i>·</i><a href="%s/" rel="noopener">%s</a></span></div>\n'
                 '  </div>\n  <div class="giant">DANOVA</div>\n</footer>' % (YEAR, owner, legal, EXT, t['sister']))
    return ''.join(parts)


CONTACT_H5 = ('Contatti', 'Contact', 'Kontakt', 'Contacto', '联系', '聯絡', '聯繫', 'İletişim', 'اتصل', 'تواصل')

STAND_KW = re.compile(r'stand|fier|allest|messe|exhibit|trade fair|ledwall|moquette|espositor|totem|render|evento|event|showroom|grafica|montaggio|salon|feria|展', re.I)


def fix_org(n):
    n['name'] = NEW_BRAND
    n['description'] = ('Danova Stand progetta, produce, trasporta e monta stand fieristici chiavi in mano '
                        '(preallestiti, modulari e su misura) e allestimenti per eventi, showroom e negozi, '
                        'in Italia e in Europa. Sede a Mansuè (TV), magazzini a Fontanelle (TV) e Trumello (PV).')
    n['disambiguatingDescription'] = ('Danova Stand è il marchio di ' + DT + ' (P.IVA IT05369890263) '
                                      'dedicato agli stand fieristici e agli allestimenti.')
    n['parentOrganization'] = {'@type': 'Organization', 'name': DT, 'url': EXT + '/'}
    if isinstance(n.get('knowsAbout'), list):
        k = [x for x in n['knowsAbout'] if isinstance(x, str) and STAND_KW.search(x)]
        n['knowsAbout'] = k or ['Stand fieristici', 'Allestimenti fieristici', 'Progettazione stand', 'Montaggio stand']
    if isinstance(n.get('sameAs'), list):
        n['sameAs'] = [u for u in n['sameAs'] if 'maps.app.goo.gl' in u]
    for k in ('hasOfferCatalog', 'makesOffer'):
        if k in n and not STAND_KW.search(json.dumps(n[k], ensure_ascii=False)):
            n.pop(k)


DT_TXT = ''


EVENT_IMG = 'https://danovastand.com/assets/img/og-cover.jpg'


def fix_event(n):
    # Google Search Console (dati strutturati Eventi): servono 'image', 'performer' e 'offers'
    if not n.get('image'):
        n['image'] = [EVENT_IMG]
    if not n.get('performer') and isinstance(n.get('organizer'), dict):
        n['performer'] = dict(n['organizer'])
    if not n.get('offers'):
        off = {'@type': 'Offer', 'availability': 'https://schema.org/InStock'}
        u = n.get('url') or (n.get('organizer') or {}).get('url')
        if u:
            off['url'] = u
        n['offers'] = off


def is_event(o):
    t = o.get('@type')
    return any(isinstance(x, str) and x.endswith('Event') for x in (t if isinstance(t, list) else [t]))


def walk(o, is_home):
    if isinstance(o, dict):
        if str(o.get('@id', '')).endswith('/#organization') and 'name' in o:
            fix_org(o)
        if is_event(o):
            fix_event(o)
        for k, v in list(o.items()):
            o[k] = walk(v, is_home)
        return o
    if isinstance(o, list):
        return [walk(x, is_home) for x in o]
    if isinstance(o, str):
        if o.startswith(OLD) or o.startswith(EXT):
            if o.startswith(EXT):
                return o
            return remap_url(o)
        return o
    return o


def fix_jsonld(s, is_home):
    def f(m):
        try:
            d = json.loads(m.group(1))
        except Exception:
            return m.group(0)
        if isinstance(d, dict) and '@graph' in d:
            gone = [n.get('@id') for n in d['@graph'] if n.get('@type') == 'VideoObject'
                    and remap_url(str(n.get('url', ''))).startswith(EXT) and n.get('@id')]
            d['@graph'] = [n for n in d['@graph'] if n.get('@id') not in gone]

            def prune(o):
                if isinstance(o, dict):
                    return {k: prune(v) for k, v in o.items()}
                if isinstance(o, list):
                    keep = [prune(x) for x in o if not any(g in json.dumps(x) for g in gone)]
                    if keep and all(isinstance(x, dict) and 'position' in x for x in keep):
                        for i, x in enumerate(keep, 1):
                            x['position'] = i
                    return keep
                return o
            if gone:
                d = prune(d)
                for n in d['@graph']:
                    if 'numberOfItems' in n and isinstance(n.get('itemListElement'), list):
                        n['numberOfItems'] = len(n['itemListElement'])
        d = walk(d, is_home)
        if is_home and isinstance(d, dict) and '@graph' in d:
            d['@graph'] = [n for n in d['@graph'] if n.get('@type') != 'BreadcrumbList']
            for n in d['@graph']:
                n.pop('breadcrumb', None)
        return '<script type="application/ld+json">\n%s\n</script>' % json.dumps(d, ensure_ascii=False, indent=2)
    return re.sub(r'<script type="application/ld\+json">(.*?)</script>', f, s, flags=re.S)


CONTATTI_STAND = '''<section id="come"><div class="wrap"><div class="sec-head"><div class="eyebrow mono">Prima di scriverci</div><h2 class="title">Cosa ci serve per preventivare lo stand</h2><p class="lead">Non serve avere già un progetto: quello lo facciamo noi. Con queste informazioni però il primo preventivo arriva in pochi giorni ed è già vicino a quello finale.</p></div>
<ul class="pg-lista" data-rv="up">
<li><b>Fiera, padiglione e date.</b> Anche solo il mese, se il contratto con l'ente fiera non è ancora firmato.</li>
<li><b>Metratura e tipo di area.</b> In linea, ad angolo, a penisola o a isola. Se avete la planimetria dell'ente fiera, mandatecela.</li>
<li><b>Cosa deve fare lo stand.</b> Prodotti da esporre, quante persone allo stand, se serve una zona riunioni, un magazzino o un bar.</li>
<li><b>Budget indicativo e riutilizzo.</b> Se lo stand servirà anche per altre fiere conviene progettarlo modulare e tenerlo nel nostro magazzino.</li>
<li><b>Logo e riferimenti.</b> Foto di stand precedenti o di stand che vi piacciono: ci aiutano più di qualsiasi descrizione.</li>
</ul></div></section>
<section id="metodo-breve"><div class="wrap"><div class="sec-head"><div class="eyebrow mono">Come si procede</div><h2 class="title">Dal primo contatto allo smontaggio</h2></div><ol class="pg-passi">
<li><b>Rispondiamo entro 24 ore lavorative.</b> A una email, a un messaggio WhatsApp o a una chiamata.</li>
<li><b>Planimetria e regolamento.</b> Verifichiamo l'area, le altezze consentite e le regole tecniche della fiera prima di disegnare.</li>
<li><b>Progetto 3D e preventivo voce per voce.</b> Strutture, grafica, impianto elettrico, luci, moquette, arredi, trasporto e montaggio, ognuno con il suo prezzo.</li>
<li><b>Produzione, montaggio e smontaggio.</b> Un solo capocantiere in fiera, dichiarazione di conformità dell'impianto e, se serve, lo stand resta nel nostro magazzino fino alla fiera successiva.</li>
</ol></div></section>
<section id="zone"><div class="wrap"><div class="sec-head"><div class="eyebrow mono">Dove lavoriamo</div><h2 class="title">In tutte le fiere italiane e in Europa</h2></div><div class="pg-testo"><p>Montiamo stand in tutti i principali quartieri fieristici italiani: Veronafiere, Fiera Milano Rho, BolognaFiere, Rimini Expo Centre, Fiere di Parma, Padova, Vicenza, Pordenone e gli altri. All'estero abbiamo lavorato in 11 paesi europei.</p><p>La sede è a Mansuè (TV); i magazzini sono a Fontanelle (TV) e Trumello (PV), gli uffici a Trumello e a Vermezzo con Zelo (MI), a pochi minuti da Fiera Milano Rho. Il sopralluogo in azienda o in videochiamata è gratuito.</p></div></div></section>
'''


def post_clean(rel, s):
    # box "pagine collegate": via i link a servizi Danova Tech non legati agli stand
    s = re.sub(r'\n[ \t]*<a href="%s/[^"]+">[^<]*</a>[ \t]*(?=\n)' % re.escape(EXT), '', s)
    s = re.sub(r'(<div class="pg-altri"[^>]*>)<a href="%s/[^"]+">[^<]*</a>\s*' % re.escape(EXT), r'\1', s)
    # schede di video non legati agli stand
    s = re.sub(r'<figure(?:(?!</figure>).)*?href="%s/video/(?:(?!</figure>).)*</figure>\s*' % re.escape(EXT), '', s, flags=re.S)
    s = s.replace("E siamo anche un'agenzia tech: allo spazio fisico",
                  "E con %s, l'agenzia digitale del nostro gruppo, allo spazio fisico" % DT)
    s = s.replace("Se vuoi, all'allestimento affianchiamo la parte digitale:",
                  "Se vuoi, con %s, l'agenzia digitale del nostro gruppo, all'allestimento affianchiamo la parte digitale:" % DT)
    if rel == '404.html':
        s = s.replace('oppure vai ai servizi: siti web, SEO, Meta Ads, app e gestionali su misura.',
                      'oppure scopri i nostri stand fieristici e allestimenti chiavi in mano.')
    if rel == 'contatti/':
        s = re.sub(r'<section id="come">.*?<section id="zone">.*?</section>\n', CONTATTI_STAND, s, count=1, flags=re.S)
        s = re.sub(r'<section id="zone-contatti">.*?</section>\n?', '', s, count=1, flags=re.S)
    return s


def transform(rel, s, is_home=False):
    lang = re.search(r'<html[^>]*\blang="([^"]+)"', s).group(1)
    L = norm_lang(lang)
    path = '/' + rel
    cur = remap_path(path)

    # --- contatti dal footer originale (gia' localizzati)
    contact_col = ''
    fm = re.search(r'<footer.*?</footer>', s, re.S)
    if fm:
        for m in re.finditer(r'<div><h5>(.*?)</h5><ul>.*?</ul></div>', fm.group(0), re.S):
            if any(c in m.group(1) for c in CONTACT_H5):
                contact_col = m.group(0).replace(OLD_BRAND, DT)  # i profili social restano di Danova Tech
        s = s[:fm.start()] + footer_html(L, contact_col) + s[fm.end():]

    # --- header
    hm = re.search(r'<header id="hdr">.*?</header>', s, re.S)
    if hm:
        h = hm.group(0)
        btn = re.search(r'<a href="([^"]+)" class="btn btn-p"', h)
        cta = btn.group(1) if btn else T[L]['legal'][-1][1]
        h = re.sub(r'(<nav class="links"[^>]*>).*?(</nav>)',
                   lambda m: m.group(1) + '\n' + nav_html(L, cta, cur, '      ') + '\n    ' + m.group(2), h, flags=re.S)
        h = re.sub(r'<a href="[^"]*" class="brand"', '<a href="%s" class="brand"' % HUB[L], h, count=1)
        s = s[:hm.start()] + h + s[hm.end():]
        mm = re.search(r'<nav id="mob"[^>]*>(.*?)</nav>', s, re.S)
        if mm:
            inner = mm.group(1)
            i = inner.find('<div class="mob-lang-links">')
            rest = inner[i:] if i >= 0 else ''
            new_inner = '\n' + nav_html(L, cta, cur, '  ') + '\n\n  ' + rest
            s = s[:mm.start(1)] + new_inner + s[mm.end(1):]

    # --- feed e statistiche Cloudflare di danova-tech.com (da riattivare col nuovo token)
    s = re.sub(r'<link rel="alternate" type="application/rss\+xml"[^>]*>\n?', '', s)
    s = re.sub(r'<link rel="preconnect" href="https://static\.cloudflareinsights\.com"[^>]*>\n?', '', s)
    s = re.sub(r'<script[^>]*cloudflareinsights[^>]*>\s*</script>\n?', '', s)

    # --- dati strutturati
    s = fix_jsonld(s, is_home)

    # --- link
    s = remap_attrs(s)
    # hreflang verso pagine non importate: via
    s = re.sub(r'<link rel="alternate" hreflang="[^"]+" href="%s[^"]*">\n?' % re.escape(EXT), '', s)
    s = post_clean(rel, s)
    # url rimasti nel testo / script inline
    s = s.replace(OLD, NEW)

    # --- marchio
    s = s.replace('<b>DANOVA</b><i>TECH</i>', '<b>DANOVA</b><i>STAND</i>')
    s = s.replace(OLD_BRAND, NEW_BRAND)
    s = s.replace(DT, OLD_BRAND).replace(EXT, OLD)
    # link esterni a Danova Tech: apri in nuova scheda no, ma rel noopener ok
    return s, L


def home_from_hub(s):
    t = re.search(r'<title>(.*?)</title>', s).group(1)
    newt = 'Stand fieristici e allestimenti chiavi in mano | Danova Stand'
    s = s.replace(t, newt)
    # niente briciole in home, ma resta lo spazio sotto l'header
    s = re.sub(r'<div class="wrap pg-crumbs">.*?</div>', '<div class="wrap pg-crumbs" aria-hidden="true">&nbsp;</div>',
               s, count=1, flags=re.S)
    return s


def redirect_page(target, lang='it'):
    url = target if target.startswith('http') else NEW + target
    return ('<!DOCTYPE html>\n<html lang="%s"><head><meta charset="utf-8">\n<title>Danova Stand</title>\n'
            '<meta name="robots" content="noindex, follow">\n<link rel="canonical" href="%s">\n'
            '<meta http-equiv="refresh" content="0; url=%s">\n'
            '<script>location.replace(%s)</script>\n</head><body>\n'
            '<p><a href="%s">Danova Stand</a></p>\n</body></html>\n') % (lang, url, target, json.dumps(target), target)


def write(rel_file, data):
    p = os.path.join(REPO, rel_file)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, 'w', encoding='utf-8') as f:
        f.write(data)


def main():
    meta = []
    for rel in ALL:
        src = os.path.join(SRC, rel, 'index.html')
        if not os.path.exists(src):
            print('MANCA', rel); continue
        s = open(src, encoding='utf-8').read()
        if rel == 'stand-fieristici/':
            hs, L = transform(rel, s, is_home=True)
            hs = home_from_hub(hs)
            write('index.html', hs)
            meta.append(('/', hs))
            write(rel + 'index.html', redirect_page('/'))
            continue
        out, L = transform(rel, s)
        write(rel + 'index.html', out)
        meta.append(('/' + rel, out))

    # 404
    s = open(os.path.join(SRC, '404.html'), encoding='utf-8').read()
    out, _ = transform('404.html', s)
    write('404.html', out)

    # pagine-redirect per gli indirizzi "speciali"
    for old, new in SPECIAL.items():
        if old == '/stand-fieristici/':
            continue
        if old.strip('/') + '/' in ALL:
            continue
        lang = old.strip('/').split('/')[0] if old.strip('/').split('/')[0] in ('en', 'de', 'fr', 'es', 'zh', 'zh-hant', 'tr', 'ar') else 'it'
        write(old.lstrip('/') + 'index.html', redirect_page(new, lang))

    # asset
    used = set()
    for root, _, files in os.walk(REPO):
        if '/.git' in root or '/strumenti' in root:
            continue
        for fn in files:
            if fn.endswith('.html'):
                t = open(os.path.join(root, fn), encoding='utf-8').read()
                used |= set(re.findall(r'(/assets/[^"\'\s)?#,]+)', t))
    for d in ('css', 'js', 'fonts', 'data'):
        shutil.copytree(os.path.join(SRC, 'assets', d), os.path.join(REPO, 'assets', d), dirs_exist_ok=True)
    shutil.copytree(os.path.join(SRC, 'assets/img/stand'), os.path.join(REPO, 'assets/img/stand'), dirs_exist_ok=True)
    for d in ('css', 'js'):
        for fn in os.listdir(os.path.join(SRC, 'assets', d)):
            used |= set(re.findall(r'(/assets/[^"\'\s)?#,]+)', open(os.path.join(SRC, 'assets', d, fn), encoding='utf-8', errors='ignore').read()))
    used.add('/assets/img/logo.png')
    missing = []
    for a in sorted(used):
        sp, dp = os.path.join(SRC, a.lstrip('/')), os.path.join(REPO, a.lstrip('/'))
        if os.path.isfile(sp):
            if not os.path.exists(dp) or os.path.getsize(dp) != os.path.getsize(sp):
                os.makedirs(os.path.dirname(dp), exist_ok=True)
                shutil.copy2(sp, dp)
        elif not os.path.isdir(sp):
            missing.append(a)
    if missing:
        print('ASSET NON TROVATI:', missing)

    # sitemap con hreflang
    rows = []
    for path, h in meta:
        if re.search(r'<meta name="robots" content="noindex', h):
            continue
        alts = re.findall(r'<link rel="alternate" hreflang="([^"]+)" href="([^"]+)">', h)
        x = '  <url>\n    <loc>%s%s</loc>\n    <lastmod>%s</lastmod>\n' % (NEW, path, TODAY)
        for hl, u in alts:
            x += '    <xhtml:link rel="alternate" hreflang="%s" href="%s"/>\n' % (hl, u)
        rows.append(x + '  </url>')
    write('sitemap.xml', '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
          + '\n'.join(rows) + '\n</urlset>\n')

    # llms.txt
    def tdesc(h):
        t = re.search(r'<title>(.*?)</title>', h); d = re.search(r'<meta name="description" content="([^"]*)"', h)
        return (html.unescape(t.group(1)) if t else ''), (html.unescape(d.group(1)) if d else '')
    lines = ['# Danova Stand', '',
             '> Stand fieristici e allestimenti chiavi in mano in Italia e in Europa: progetto 3D, produzione, trasporto, '
             'montaggio e smontaggio. Marchio di Danova Tech (P.IVA IT05369890263), sede a Mansuè (TV). '
             'Contatti: info@danova-tech.com, +39 388 470 6887.', '']
    groups = {}
    for path, h in meta:
        if path.lstrip('/').split('/')[0] in ('privacy', 'cookie-policy', 'termini') or 'noindex' in h[:3000]:
            continue
        g = path.strip('/').split('/')[0] if path.strip('/').split('/')[0] in ('en', 'de', 'fr', 'es', 'zh', 'zh-hant', 'tr', 'ar') else 'it'
        groups.setdefault(g, []).append((path, *tdesc(h)))
    names = {'it': 'Italiano', 'en': 'English', 'de': 'Deutsch', 'fr': 'Français', 'es': 'Español',
             'zh': '简体中文', 'zh-hant': '繁體中文', 'tr': 'Türkçe', 'ar': 'العربية'}
    for g in names:
        if g not in groups: continue
        lines += ['## ' + names[g], '']
        for path, t, d in sorted(groups[g]):
            lines.append('- [%s](%s%s): %s' % (t, NEW, path, d))
        lines.append('')
    write('llms.txt', '\n'.join(lines))

    # mappa redirect danova-tech.com -> danovastand.com
    red = ['vecchio,nuovo']
    for rel in PAGES:
        new = remap_path('/' + rel)
        red.append('%s/%s,%s%s' % (OLD, rel, NEW, new))
    write('strumenti/redirect-danovatech.csv', '\n'.join(red) + '\n')
    print('Pagine importate:', len(meta), '| asset:', len(used))


if __name__ == '__main__':
    main()
