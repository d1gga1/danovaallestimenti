# -*- coding: utf-8 -*-
"""Blocco 'Gli elementi in legno li facciamo noi, dalla A alla Z' nelle pagine allestimenti (14 ottobre 2026).
inject(html, path, lang) lo inserisce (o lo sostituisce) prima del modulo di richiesta / contatti / FAQ. Idempotente.
Chiamato da lib.build; applica_legno() lo applica alle pagine gia' pubblicate."""
import os, re, glob
A, B = '<!--fr-legno-->', '<!--/fr-legno-->'
G = '<span class="grad">'; _G = '</span>'
T = {
 'it': dict(ey="Produzione propria", t=f"Gli elementi in legno {G}li facciamo noi, dalla A alla Z.{_G}",
   lead="Pareti, banconi, desk, pedane, espositori, mensole e arredi in legno: li progettiamo noi sul tuo marchio, li facciamo produrre da laboratori partner selezionati, con cui lavoriamo da anni, e gestiamo noi trasporto e montaggio in fiera. Un solo referente segue progetto, produzione, trasporto e montaggio: tu non devi rincorrere fornitori diversi. Usiamo materiali certificati in Classe 1 di reazione al fuoco e abbiamo già montato oltre 300 stand.",
   cards=[("Nessun ricarico di terzi", "Chi non produce compra fuori pareti e arredi e ci aggiunge il proprio margine. Noi no: a parità di stand, il prezzo è più basso."),
          ("Davvero su misura", "Ogni pezzo nasce sulle misure del tuo spazio e dei tuoi prodotti, non si adatta un elemento di catalogo."),
          ("Tempi sotto controllo", "Dal disegno al pezzo finito non dipendiamo da nessuno: anche le modifiche dell'ultimo momento le facciamo noi."),
          ("Un solo responsabile", "Progetto, produzione, montaggio e smontaggio con lo stesso referente: se qualcosa non va, sai a chi chiedere.")]),
 'en': dict(ey="Our own production", t=f"We make every wooden element {G}ourselves, from A to Z.{_G}",
   lead="Walls, counters, desks, platforms, display units, shelves and furniture in wood: we design them around your brand, have them built by selected partner workshops we have worked with for years, and manage transport and installation at the fair ourselves. One contact person runs design, production, transport and installation, so you never have to chase separate suppliers. We use Class 1 fire-rated certified materials and have already built more than 300 stands.",
   cards=[("No third-party mark-up", "Builders without production buy walls and furniture from others and add their margin. We don't: for the same stand, the price is lower."),
          ("Truly made to measure", "Every piece is built on the size of your space and your products, not adapted from a catalogue."),
          ("Deadlines under control", "From drawing to finished piece we depend on no one: even last-minute changes are made by us."),
          ("One responsible partner", "Design, production, installation and dismantling with the same contact person.")]),
 'zh': dict(ey="自主生产", t=f"所有木制构件 {G}都由我们自己从头到尾完成。{_G}",
   lead="墙板、柜台、接待台、地台、展示架、层架和木制家具：由我们根据您的品牌进行设计，交由合作多年的精选合作工坊生产，并由我们统筹展会现场搭建。从设计、生产、运输到搭建，全程由一位联系人负责，您无需对接多个供应商。我们使用防火等级 Class 1 认证材料，已累计搭建超过 300 个展台。",
   cards=[("没有第三方加价", "我们与固定的合作工坊和搭建团队长期合作：流程熟悉、沟通顺畅，质量和工期更可控。"),
          ("真正的量身定制", "每一个构件都按照您的展位和产品尺寸制作，而不是套用目录里的标准件。"),
          ("工期可控", "从图纸到成品不依赖任何外部厂家：即使是最后一刻的修改，也由我们自己完成。"),
          ("一个责任方", "设计、生产、搭建和拆除始终由同一位联系人负责。")]),
 'de': dict(ey="Eigene Fertigung", t=f"Alle Holzelemente {G}fertigen wir selbst, von A bis Z.{_G}",
   lead="Wände, Theken, Counter, Podeste, Displays, Regale und Möbel aus Holz: Wir planen sie passend zu Ihrer Marke, lassen sie von ausgewählten Partnerwerkstätten fertigen, mit denen wir seit Jahren zusammenarbeiten, und koordinieren die Montage auf der Messe. Ein Ansprechpartner steuert Planung, Fertigung, Transport und Montage, Sie müssen keine einzelnen Lieferanten koordinieren. Wir verwenden zertifizierte Materialien der Brandschutzklasse 1 (Italien) und haben bereits über 300 Messestände gebaut.",
   cards=[("Kein Aufschlag Dritter", "Wer nicht selbst fertigt, kauft Wände und Möbel zu und schlägt seine Marge auf. Wir nicht: Gleicher Stand, niedrigerer Preis."),
          ("Wirklich maßgefertigt", "Jedes Teil entsteht nach den Maßen Ihrer Fläche und Ihrer Produkte."),
          ("Termine im Griff", "Von der Zeichnung bis zum fertigen Teil sind wir von niemandem abhängig, auch bei kurzfristigen Änderungen."),
          ("Ein Ansprechpartner", "Planung, Fertigung, Aufbau und Abbau aus einer Hand.")]),
 'fr': dict(ey="Production propre", t=f"Tous les éléments en bois, {G}nous les fabriquons nous-mêmes, de A à Z.{_G}",
   lead="Cloisons, comptoirs, banques d'accueil, podiums, présentoirs, étagères et mobilier en bois : nous les concevons autour de votre marque, les faisons fabriquer par des ateliers partenaires sélectionnés avec lesquels nous travaillons depuis des années, et coordonnons le montage sur le salon. Un seul interlocuteur pilote conception, fabrication, transport et montage : vous n'avez pas à gérer plusieurs fournisseurs. Nous utilisons des matériaux certifiés en Classe 1 de réaction au feu et avons déjà monté plus de 300 stands.",
   cards=[("Pas de marge d'un tiers", "Sans production propre, on achète cloisons et mobilier ailleurs et on ajoute sa marge. Pas nous : à stand égal, le prix est plus bas."),
          ("Vraiment sur mesure", "Chaque pièce est fabriquée aux dimensions de votre espace et de vos produits."),
          ("Délais maîtrisés", "Du dessin à la pièce finie, nous ne dépendons de personne, même pour les changements de dernière minute."),
          ("Un seul interlocuteur", "Conception, fabrication, montage et démontage avec la même personne.")]),
 'es': dict(ey="Producción propia", t=f"Todos los elementos de madera {G}los fabricamos nosotros, de la A a la Z.{_G}",
   lead="Paredes, mostradores, recepciones, tarimas, expositores, estanterías y mobiliario de madera: los diseñamos según tu marca, los fabrican talleres asociados seleccionados con los que trabajamos desde hace años y gestionamos nosotros el montaje en la feria. Un único interlocutor gestiona diseño, fabricación, transporte y montaje: no tienes que coordinar proveedores distintos. Usamos materiales certificados en Clase 1 de reacción al fuego y ya hemos montado más de 300 stands.",
   cards=[("Sin margen de terceros", "Quien no produce compra paredes y muebles fuera y añade su margen. Nosotros no: mismo stand, precio más bajo."),
          ("A medida de verdad", "Cada pieza se fabrica según las medidas de su espacio y de sus productos."),
          ("Plazos bajo control", "Del plano a la pieza terminada no dependemos de nadie, ni siquiera para cambios de última hora."),
          ("Un solo responsable", "Diseño, producción, montaje y desmontaje con la misma persona de contacto.")]),
}

def blocco(lang):
    t = T[lang]
    cs = ''.join(f'''
      <article class="pg-card" data-tilt data-rv="blur">
        <span class="n">{i+1:02d}</span>
        <h3>{h}</h3>
        <p>{p}</p>
      </article>''' for i, (h, p) in enumerate(t['cards']))
    return (f'{A}<section id="legno">\n  <div class="wrap">\n    <div class="sec-head">\n      <div class="eyebrow mono">{t["ey"]}</div>\n'
            f'      <h2 class="title" data-rv="up">{t["t"]}</h2>\n      <p class="lead" data-rv="up">{t["lead"]}</p>\n    </div>\n'
            f'    <div class="pg-cards">{cs}\n    </div>\n  </div>\n</section>\n{B}\n')

def lingua(path):
    seg = path.strip('/').split('/')[0]
    return seg if seg in ('en', 'zh', 'de', 'fr', 'es', 'tr', 'ar', 'zh-hant') else 'it'

FUORI = ('/contributi-fiere-2026/', '/guide/regolamento-tecnico-fiera/', '/guide/dichiarazione-di-conformita-stand/', '/guide/materiali-ignifughi-stand/',
         '/guide/come-attirare-visitatori-allo-stand/', '/guide/come-raccogliere-contatti-in-fiera/', '/guide/come-preparare-una-fiera/',
         '/calendario-fiere-milano/', '/calendario-fiere-bologna/', '/calendario-fiere-rimini/', '/calendario-fiere-parma/')

def pertinente(s, path):
    lang = lingua(path)
    if lang not in T or path in FUORI or path.startswith('/calendario-fiere-'): return False
    return 'fiere.css' in s

def inject(s, path, lang=None):
    lang = lang or lingua(path)
    if lang not in T or not pertinente(s, path): return s
    s = re.sub(re.escape(A) + r'.*?' + re.escape(B) + r'\n?', '', s, flags=re.S)
    for anchor in ('<section id="richiesta"', '<section class="pg-cta" id="contatti-fiera"', '<section id="faq">'):
        i = s.find(anchor)
        if i >= 0: return s[:i] + blocco(lang) + s[i:]
    return s

def applica_legno():
    R = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
    n = 0
    for f in glob.glob(os.path.join(R, '**', 'index.html'), recursive=True):
        rel = os.path.relpath(f, R).replace('\\', '/')
        if rel.startswith(('seo-tools/', 'zh-hant/')): continue
        path = '/' + os.path.dirname(rel) + '/' if os.path.dirname(rel) else '/'
        s = open(f, encoding='utf-8').read(); s2 = inject(s, path)
        if s2 != s: open(f, 'w', encoding='utf-8').write(s2); n += 1
    print('pagine con blocco legno:', n)

if __name__ == '__main__':
    applica_legno()
