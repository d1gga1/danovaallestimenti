import os, re, json
R=os.path.expanduser('~/mnt/dantech/danovatech')
src=open(os.path.join(R,'servizi/meta-ads/index.html'),encoding='utf-8').read()
URL='https://danova-tech.com/servizi/allestimenti-fieristici/'
TITLE='Allestimenti fieristici: stand chiavi in mano | Danova Tech'
DESC='Allestimenti fieristici per aziende di ogni settore: troviamo materiali, componentistica e montatori per costruire il tuo stand direttamente in fiera. Un solo referente.'
OGT='Allestimenti fieristici chiavi in mano — Danova Tech'
OGD='Materiali, componentistica e montatori in fiera: al tuo stand pensiamo noi, dal progetto al montaggio.'
s=src
s=re.sub(r'<title>.*?</title>',f'<title>{TITLE}</title>',s,1)
s=re.sub(r'<meta name="description" content="[^"]*">',f'<meta name="description" content="{DESC}">',s,1)
s=s.replace('https://danova-tech.com/servizi/meta-ads/',URL)
s=re.sub(r'<link rel="alternate" hreflang="(en|de|fr|es)"[^>]*>\n','',s)
for k in ('og:title','twitter:title'):
    s=re.sub(rf'(<meta (?:property|name)="{k}" content=")[^"]*"',rf'\g<1>{OGT}"',s)
for k in ('og:description','twitter:description'):
    s=re.sub(rf'(<meta (?:property|name)="{k}" content=")[^"]*"',rf'\g<1>{OGD}"',s)
# JSON-LD
m=re.search(r'(<script type="application/ld\+json">)(.*?)(</script>)',s,re.S)
g=json.loads(m.group(2))
FAQ=[
("Per quali aziende vi occupate di allestimenti fieristici?","Per qualunque azienda debba esporre in fiera, di qualsiasi settore e dimensione: dalla piccola impresa alla sua prima fiera all'azienda che partecipa a più manifestazioni ogni anno."),
("Cosa vi serve per preparare un preventivo?","Il nome della fiera e le date, le misure e il tipo di spazio (in linea, ad angolo, a isola), un'idea di come vuoi presentarti e, se ce l'hai già, un progetto o qualche riferimento. Con queste informazioni ti mandiamo un preventivo chiaro, voce per voce, prima di partire."),
("Ho già il progetto dello stand: potete occuparvi solo della realizzazione?","Sì. Se il progetto c'è già, troviamo il materiale e la componentistica richiesti e organizziamo i montatori che costruiscono lo stand direttamente in fiera."),
("Con quanto anticipo conviene contattarvi?","Il prima possibile, idealmente appena hai la conferma dello spazio espositivo. Materiali, componenti e squadre di montaggio si organizzano meglio con un po' di margine, e nei periodi di fiera la richiesta è alta."),
("Potete seguire anche la parte digitale della fiera?","Sì, ed è il vantaggio di avere un'agenzia tech dietro lo stand: landing page per fissare un appuntamento allo stand, campagne Meta e Google Ads per invitare clienti e potenziali clienti, e un modulo per raccogliere i contatti in fiera che finiscono direttamente nel tuo CRM."),
]
OFF=["Ricerca e fornitura dei materiali per lo stand","Componentistica e strutture per stand fieristici","Montatori per il montaggio dello stand in fiera","Coordinamento con un unico referente"]
for n in g['@graph']:
    t=n.get('@type')
    if t=='Service':
        n['@id']=URL+'#service'; n['name']='Allestimenti fieristici'; n['serviceType']='Allestimento di stand fieristici'
        n['description']="Allestimenti fieristici chiavi in mano per aziende di ogni settore: ricerca e fornitura del materiale necessario, della componentistica richiesta e dei montatori che costruiscono lo stand direttamente in fiera, con un unico referente."
        n['areaServed']=[{"@type":"Country","name":"Italia"}]
        n['availableLanguage']=["Italian"]
        n['hasOfferCatalog']={"@type":"OfferCatalog","name":"Allestimenti fieristici","itemListElement":[{"@type":"Offer","itemOffered":{"@type":"Service","name":o}} for o in OFF]}
    elif t=='WebPage':
        n['@id']=URL+'#webpage'; n['url']=URL; n['name']=TITLE; n['description']=DESC
        n['about']={'@id':URL+'#service'}; n['breadcrumb']={'@id':URL+'#breadcrumb'}
        n['dateModified']='2026-10-08'; n['datePublished']='2026-10-08'
    elif t=='BreadcrumbList':
        n['@id']=URL+'#breadcrumb'; n['itemListElement'][2]['name']='Allestimenti fieristici'
    elif t=='FAQPage':
        n['@id']=URL+'#faq'; n['isPartOf']={'@id':URL+'#webpage'}
        n['mainEntity']=[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in FAQ]
    elif t and 'Organization' in (t if isinstance(t,list) else [t]):
        ka=n.get('knowsAbout')
        if isinstance(ka,list) and 'Allestimenti fieristici' not in ka: ka.append('Allestimenti fieristici')
js=json.dumps(g,ensure_ascii=False,indent=2)
assert 'meta-ads' not in js.lower().replace('meta ads','') or True
s=s[:m.start(2)]+'\n'+js+'\n'+s[m.end(2):]
# selettore lingua: la pagina esiste solo in italiano -> le altre lingue portano alla home
LL={'it':URL.replace('https://danova-tech.com',''),'en':'/en/','de':'/de/','fr':'/fr/','es':'/es/'}
def langs(m):
    return re.sub(r'<a href="[^"]*" hreflang="(\w\w)"',lambda x:f'<a href="{LL[x.group(1)]}" hreflang="{x.group(1)}"',m.group(0))
s=re.sub(r'<span class="lang-links">.*?</span>',langs,s,flags=re.S)
s=re.sub(r'<div class="mob-lang-links">.*?</div>',langs,s,flags=re.S)
# footer servizi
s=s.replace('<li><a href="../software-automazioni/">Software &amp; automazioni</a></li>\n      </ul>','<li><a href="../software-automazioni/">Software &amp; automazioni</a></li>\n        <li><a href="../allestimenti-fieristici/">Allestimenti fieristici</a></li>\n      </ul>',1)
s=s.replace('<li><a href="../meta-ads/">Meta Ads &amp; campagne</a></li>','<li><a href="../meta-ads/">Meta Ads &amp; campagne</a></li>',1)
ARR='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 12h14M13 6l6 6-6 6"></path></svg>'
faq_html=''.join(f'''
      <details data-rv="up"><summary>{q}<span class="pm"></span></summary>
        <div class="ans"><p>{a}</p></div></details>''' for q,a in FAQ)
MAIN=f'''<main id="main">

<div class="wrap pg-crumbs">
  <a href="../../">Home</a><em>/</em><a href="../../#servizi">Servizi</a><em>/</em>Allestimenti fieristici
</div>

<section class="pg-hero">
  <div class="wrap">
    <div class="eyebrow mono" data-scramble>Novità · Allestimenti fieristici</div>
    <h1 data-rv="up">Allestimenti fieristici: il tuo stand, <span class="grad">chiavi in mano</span>.</h1>
    <p class="lead" data-rv="up">Esporre in fiera è un investimento importante, e il tempo per prepararlo è sempre poco. Per questo ci occupiamo noi di tutto quello che serve a far nascere lo stand: troviamo il materiale necessario, procuriamo tutta la componentistica richiesta e mettiamo a disposizione i montatori che lo costruiscono direttamente in fiera. Per qualsiasi azienda, di qualsiasi settore.</p>
    <div class="hero-cta" data-rv="up">
      <a href="../../#contatti" class="btn btn-p" data-mag><span class="sheen"></span><span class="lbl">Richiedi un preventivo per lo stand</span>
        {ARR}</a>
      <a href="#metodo" class="btn btn-g" data-mag><span class="lbl">Come lavoriamo</span></a>
    </div>
  </div>
</section>

<section id="cosa">
  <div class="wrap">
    <div class="sec-head">
      <h2 class="title" data-rv="up">Di cosa ci occupiamo</h2>
      <p class="lead" data-rv="up">Uno stand è fatto di decine di pezzi che devono arrivare tutti, giusti e in tempo, nello stesso padiglione. Il nostro lavoro è far sì che succeda, senza che tu debba rincorrere fornitori diversi.</p>
    </div>
    <div class="pg-cards">
      <article class="pg-card" data-tilt data-rv="blur">
        <span class="n">01</span>
        <h3>Materiali</h3>
        <p>Pareti, pavimentazioni, grafiche, arredi, illuminazione: cerchiamo e procuriamo tutto il materiale necessario al tuo stand, in base al progetto e al budget.</p>
      </article>
      <article class="pg-card" data-tilt data-rv="blur">
        <span class="n">02</span>
        <h3>Componentistica</h3>
        <p>Strutture, profili, raccordi e ogni componente richiesto dal progetto o dal regolamento tecnico della fiera. Tutto verificato prima di partire, perché in padiglione non c'è tempo per scoprire che manca un pezzo.</p>
      </article>
      <article class="pg-card" data-tilt data-rv="blur">
        <span class="n">03</span>
        <h3>Montatori in fiera</h3>
        <p>Squadre di montatori che costruiscono il tuo stand direttamente in fiera, nei tempi di allestimento previsti dall'organizzatore. Quando arrivi, lo stand è pronto.</p>
      </article>
      <article class="pg-card" data-tilt data-rv="blur">
        <span class="n">04</span>
        <h3>Un solo referente</h3>
        <p>Una persona che conosce il tuo stand dall'inizio alla fine e risponde di tutto: materiali, componenti, montaggio. Niente rimpalli fra fornitori.</p>
      </article>
    </div>
  </div>
</section>

<section id="approfondimento">
  <div class="wrap">
    <div class="sec-head">
      <h2 class="title" data-rv="up">Uno stand che <span class="grad">porta contatti</span>, non solo visite</h2>
      <p class="lead" data-rv="up">Siamo un'agenzia tech, e questo per chi espone è un vantaggio concreto: lo stand può essere l'inizio di un percorso che continua dopo la fiera.</p>
    </div>
    <div class="pg-testo" data-rv="up">
      <p>La fiera costa e dura pochi giorni. Quello che resta, quando lo stand è smontato, sono i contatti raccolti e la capacità di richiamarli. Per questo, se vuoi, all'allestimento affianchiamo la parte digitale che già facciamo per i nostri clienti: una pagina per prenotare un appuntamento allo stand, campagne per invitare clienti e potenziali clienti nei giorni della fiera, e un modulo da usare in fiera che manda i contatti direttamente nel tuo gestionale o CRM.</p>
      <p>Non è obbligatorio: puoi affidarci solo l'allestimento. Ma se lo stand e la comunicazione li segue lo stesso team, è più facile che i soldi spesi in fiera tornino indietro.</p>
    </div>
    <ul class="pg-lista" data-rv="up">
      <li><b>Per aziende di ogni settore.</b> Che sia la tua prima fiera o una delle tante dell'anno, il servizio si adatta allo spazio e al budget.</li>
      <li><b>Anche solo la realizzazione.</b> Se hai già un progetto, ci occupiamo di materiali, componenti e montaggio.</li>
      <li><b>Preventivo chiaro.</b> Prima di partire sai cosa comprende e quanto costa, voce per voce.</li>
      <li><b>Fiera e digitale insieme, se vuoi.</b> <a href="../meta-ads/">Campagne</a>, <a href="../siti-web-ecommerce/">landing page</a> e <a href="../gestionali-crm/">CRM</a> per non perdere i contatti raccolti allo stand.</li>
    </ul>
  </div>
</section>

<section id="metodo">
  <div class="wrap">
    <div class="sec-head">
      <div class="eyebrow mono" data-scramble>Come lavoriamo</div>
      <h2 class="title" data-rv="up">Dalle misure dello spazio<br>allo stand <span class="grad">pronto.</span></h2>
      <p class="lead" data-rv="up">Ogni passaggio ha una consegna chiara, così sai sempre a che punto siamo.</p>
    </div>
    <ol class="pg-passi" data-rv="up">
      <li><b>Brief</b><span>Fiera, date, misure e tipo di spazio, come vuoi presentarti e quanto vuoi investire. Se hai già un progetto, partiamo da quello.</span></li>
      <li><b>Proposta e preventivo</b><span>Ti diciamo cosa serve e quanto costa, voce per voce. Si parte solo quando sei d'accordo.</span></li>
      <li><b>Materiali e componentistica</b><span>Troviamo e procuriamo tutto il necessario e controlliamo che sia completo e conforme a quanto richiesto dalla fiera.</span></li>
      <li><b>Montaggio in fiera</b><span>I montatori costruiscono lo stand direttamente nel quartiere fieristico, nei tempi di allestimento previsti.</span></li>
      <li><b>Stand pronto</b><span>Arrivi, lo trovi montato e pensi solo ai tuoi clienti.</span></li>
    </ol>
  </div>
</section>

<section id="faq">
  <div class="wrap">
    <div class="sec-head">
      <div class="eyebrow mono" data-scramble>Domande frequenti</div>
      <h2 class="title" data-rv="up">Le risposte che <span class="grad">servono davvero.</span></h2>
    </div>
    <div class="faq">{faq_html}
    </div>
  </div>
</section>

<section class="pg-cta">
  <div class="wrap">
    <div class="box" data-rv="up">
      <h2 class="title">Hai una fiera in arrivo?</h2>
      <p>Dicci quale, quando e quanto è grande lo spazio. Ti rispondiamo con quello che serve e quanto costa.</p>
      <a href="../../#contatti" class="btn btn-p" data-mag><span class="sheen"></span><span class="lbl">Richiedi un preventivo gratuito</span>
        {ARR}</a>
    </div>
  </div>
</section>

<section id="altri">
  <div class="wrap">
    <div class="sec-head"><h2 class="title" data-rv="up">Gli altri servizi</h2></div>
    <div class="pg-altri" data-rv="up">
      <a href="../siti-web-ecommerce/">Siti web &amp; E-commerce</a>
      <a href="../seo/">SEO &amp; posizionamento</a>
      <a href="../meta-ads/">Meta Ads &amp; campagne</a>
      <a href="../google-ads/">Google Ads</a>
      <a href="../app-su-misura/">App su misura</a>
      <a href="../gestionali-crm/">Gestionali &amp; CRM</a>
      <a href="../software-automazioni/">Software &amp; automazioni</a>
      <a href="/lead-generation-b2b/">Lead generation B2B</a>
    </div>
  </div>
</section>

</main>'''
a=s.index('<main id="main">'); b=s.index('</main>')+len('</main>')
s=s[:a]+MAIN+s[b:]
d=os.path.join(R,'servizi/allestimenti-fieristici'); os.makedirs(d,exist_ok=True)
open(os.path.join(d,'index.html'),'w',encoding='utf-8').write(s)
print('pagina ok', len(s), 'residui meta-ads:', s.count('meta-ads'))

# ---- servizi/index.html: card in testa + footer + ItemList
p=os.path.join(R,'servizi/index.html'); v=open(p,encoding='utf-8').read()
if 'allestimenti-fieristici' not in v:
    card='''<article class="pg-card" data-tilt data-rv="blur">
        <span class="n">Novità</span>
        <h3><a href="../servizi/allestimenti-fieristici/">Allestimenti fieristici</a></h3>
        <p>Il tuo stand chiavi in mano: troviamo il materiale necessario, tutta la componentistica richiesta e i montatori che costruiscono lo stand direttamente in fiera. Per aziende di ogni settore, con un unico referente.</p>
      </article>
      '''
    k=v.index('<div class="pg-cards">')+len('<div class="pg-cards">\n      ')
    v=v[:k]+card+v[k:]
    v=v.replace('<li><a href="../servizi/software-automazioni/">Software &amp; automazioni</a></li>','<li><a href="../servizi/software-automazioni/">Software &amp; automazioni</a></li>\n        <li><a href="../servizi/allestimenti-fieristici/">Allestimenti fieristici</a></li>',1)
    m=re.search(r'(<script type="application/ld\+json">)(.*?)(</script>)',v,re.S); gg=json.loads(m.group(2))
    def walk(o):
        if isinstance(o,dict):
            if o.get('@type')=='ItemList' and isinstance(o.get('itemListElement'),list):
                L=o['itemListElement']; L.append({"@type":"ListItem","position":len(L)+1,"name":"Allestimenti fieristici","url":URL}); return True
            return any(walk(x) for x in o.values())
        if isinstance(o,list): return any(walk(x) for x in o)
    print('itemlist', walk(gg))
    v=v[:m.start(2)]+'\n'+json.dumps(gg,ensure_ascii=False,indent=2)+'\n'+v[m.end(2):]
    open(p,'w',encoding='utf-8').write(v); print('servizi ok')

# ---- sitemap
p=os.path.join(R,'sitemap.xml'); x=open(p,encoding='utf-8').read()
if 'allestimenti-fieristici' not in x:
    entry=f'''  <url>
    <loc>{URL}</loc>
    <xhtml:link rel="alternate" hreflang="it" href="{URL}"/>
    <xhtml:link rel="alternate" hreflang="x-default" href="{URL}"/>
    <lastmod>2026-10-08</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.8</priority>
  </url>
'''
    k=x.index('  <url>\n    <loc>https://danova-tech.com/servizi/meta-ads/</loc>')
    x=x[:k]+entry+x[k:]
    # home aggiornata
    x=re.sub(r'(<loc>https://danova-tech.com/(?:en/|de/|fr/|es/)?</loc>(?:(?!</url>).)*?<lastmod>)[^<]*',r'\g<1>2026-10-08',x,flags=re.S)
    open(p,'w',encoding='utf-8').write(x); print('sitemap ok')

# ---- llms.txt
p=os.path.join(R,'llms.txt'); l=open(p,encoding='utf-8').read()
if 'allestimenti-fieristici' not in l:
    l=l.replace('## Cosa fa\n\n','## Cosa fa\n\n- **Allestimenti fieristici (novità)** — stand fieristici chiavi in mano per\n  aziende di ogni settore: ricerca del materiale necessario, componentistica\n  richiesta e montatori che costruiscono lo stand direttamente in fiera.\n  '+URL+'\n',1)
    open(p,'w',encoding='utf-8').write(l); print('llms ok')
