# -*- coding: utf-8 -*-
# Pagine aggiunte il 13 ottobre 2026 (uso: python3 build_nuove_1013.py)
#  /progetti-stand-fieristici/            galleria dei render (Google Immagini)
#  /espositori-desk-totem-per-fiere/      espositori, desk, banchi, totem, roll-up
#  /allestimenti-fieristici-veneto|lombardia|emilia-romagna/   hub regionali
import re, json
from nuove_common import *
import dati_render as DR
from immagini import MAP, image_object, DIR, W, HH, url as IMGURL
GAL="/progetti-stand-fieristici/"; ESP="/espositori-desk-totem-per-fiere/"
REG={"veneto":"/allestimenti-fieristici-veneto/","lombardia":"/allestimenti-fieristici-lombardia/","emilia":"/allestimenti-fieristici-emilia-romagna/"}

def h1_of(path):
    try: s=open(os.path.join(R,path.strip('/'),'index.html'),encoding='utf-8').read()
    except OSError: return None
    m=re.search(r'<h1[^>]*>(.*?)</h1>',s,re.S)
    return strip_tags(m.group(1)).strip().rstrip('.') if m else None

# ---------------------------------------------------------------- GALLERIA
CAT=[("servizi","Servizi",[(0,10)]),("tipi","Tipologie",[(10,19)]),("metrature","Metrature",[(67,71)]),("settori","Settori",[(19,25)]),("fiere","Fiere",[(25,45),(60,67)]),("citta","Città",[(45,60)]),("guide","Guide",[(71,73)])]  # 14/10/2026: render nuovi
def galleria():
    items=[]
    for key,lab,rng in CAT:
      for a,b in rng:
        for f,pages,_s,alt,cap in DR.R[a:b]:
            p=pages[0]; t=h1_of(p) or alt
            t=t.split(':')[0]
            items.append((key,p,f,alt,cap,t))
    NR=len(items)
    btn='<button type="button" data-f="*" aria-pressed="true">Tutti</button>'+''.join(f'<button type="button" data-f="{k}" aria-pressed="false">{l}</button>' for k,l,_ in CAT)
    cards_=''.join(f'''
      <a href="{p}" data-cat="{k}"><figure><img src="{DIR}{f}-800.webp" srcset="{DIR}{f}-800.webp 800w, {DIR}{f}-1200.webp 1200w, {DIR}{f}.webp 1600w" sizes="(max-width: 700px) 100vw, 400px" width="800" height="532" alt="{E(alt)}" loading="lazy" decoding="async"><figcaption><b>{E(t)}</b><span>{E(cap)}</span></figcaption></figure></a>''' for k,p,f,alt,cap,t in items)
    hd=head(f'{NR} render di stand, <span class="grad">per tipo, settore e fiera</span>',"Clicca un progetto per aprire la pagina dedicata: cosa serve, come lo realizziamo e il modulo per chiedere un preventivo.")
    sec=f'''<section id="progetti">
  <div class="wrap">
{hd}
    <div class="fr-gal-filtri" role="group" aria-label="Filtra i progetti">{btn}</div>
    <div class="fr-gal" id="fr-gal">{cards_}
    </div>
  </div>
</section>
<script>(function(){{var g=document.getElementById('fr-gal'),bs=document.querySelectorAll('.fr-gal-filtri button');bs.forEach(function(b){{b.addEventListener('click',function(){{var f=b.getAttribute('data-f');bs.forEach(function(x){{x.setAttribute('aria-pressed',x===b?'true':'false')}});g.querySelectorAll('a').forEach(function(a){{a.hidden=!(f==='*'||a.getAttribute('data-cat')===f)}})}})}})}})();</script>
'''
    m=hero("Progetti · render 3D",'Progetti di stand fieristici: <span class="grad">60 render</span> da cui partire.',
      "Stand a isola, ad angolo, piccoli, a due piani, su misura e modulari; stand per il vino, l'arredo, la meccanica, la moda e la cosmetica; idee per Vinitaly, Salone del Mobile, EICMA, Cosmoprof e altre fiere. Sono render di progetto: il punto di partenza per disegnare il tuo stand sulla tua metratura e sul tuo marchio.",
      "Richiedi il render del tuo stand","#richiesta","Guarda i progetti","#progetti")
    m+=sec
    m+=testo("come","Come nasce il render del tuo stand",None,
      ["Ogni immagine di questa pagina è un render: una visualizzazione 3D fatta prima di costruire. È lo stesso strumento che usiamo con i clienti: partiamo da metratura, tipo di spazio (in linea, angolo, penisola, isola), prodotti da esporre e budget, e ti mostriamo lo stand com'è prima di produrlo, con materiali, grafica e luci.",
       "Il render serve a decidere vedendo, a confrontare due soluzioni e a fare approvare il progetto all'ente fiera. Quando il progetto ti convince, prepariamo il preventivo voce per voce e organizziamo produzione, trasporto e <a href=\"/montaggio-stand-fieristici/\">montaggio in fiera</a>."],
      [("Render in pochi giorni.","Prima proposta sulla tua metratura, poi modifiche finché non ti convince. <a href=\"/progettazione-stand-fieristici/\">Progettazione e render 3D</a>"),
       ("Su misura o modulare.","Lo stesso progetto si può costruire <a href=\"/stand-fieristici-su-misura/\">su misura in legno</a> o con <a href=\"/stand-modulari/\">strutture modulari</a> riutilizzabili."),
       ("Chiaro sui costi.","Nella <a href=\"/quanto-costa-uno-stand-fieristico/\">guida ai costi</a> trovi da cosa dipende il prezzo di ogni voce.")])
    qa=[("I progetti della galleria sono stand che avete realizzato?","No: sono render di progetto, cioè visualizzazioni 3D di esempio, e lo indichiamo sotto ogni immagine. Servono a mostrare soluzioni e stili possibili per ogni tipo di stand, settore e fiera. Il render del tuo stand lo prepariamo sulla tua metratura e sul tuo marchio."),
        ("Posso chiedere uno stand simile a uno di questi render?","Sì. Indicaci il progetto che ti piace, la fiera e la metratura: lo adattiamo al tuo spazio, ai tuoi prodotti e al budget."),
        ("Quanto costa il render del mio stand?","Il primo render è compreso nella proposta di progetto quando ci chiedi un preventivo per lo stand. Ti spieghiamo prima cosa comprende."),
        ("Il render serve per l'approvazione dell'ente fiera?","Sì: insieme a piante, sezioni e schede dei materiali è parte della documentazione che presentiamo secondo il regolamento tecnico della manifestazione.")]
    gal={"@type":"ImageGallery","@id":SITE+GAL+"#galleria","name":"Progetti e render di stand fieristici","isPartOf":{"@id":SITE+GAL+"#webpage"},
         "image":[image_object(f,alt,cap,'it') for k,p,f,alt,cap,t in items]}
    for io in gal["image"]: io.pop("@id",None)
    out=pagina(GAL,f"Progetti di stand fieristici: {len(DR.R)} render e idee",
      "Render di stand fieristici per tipo, settore e fiera: isola, angolo, due piani, su misura e modulari; vino, arredo, meccanica, moda, cosmetica. Chiedi il render del tuo stand.",
      "Progetti di stand fieristici — Danova Tech","60 render di stand per tipo, settore e fiera: il punto di partenza per il progetto del tuo stand.",
      crumbs("Progetti di stand"),m,qa,[gal],SERVIZI_LINKS+TIPI_LINKS,wp_extra={"@type":["WebPage","CollectionPage"],"mainEntity":{"@id":SITE+GAL+"#galleria"}})
    s=open(out,encoding='utf-8').read()
    og=IMGURL('stand-isola-legno-rovere','og')
    s=re.sub(r'(<meta property="og:image" content=")[^"]*',lambda x:x.group(1)+og,s); s=re.sub(r'(<meta name="twitter:image" content=")[^"]*',lambda x:x.group(1)+og,s)
    open(out,'w',encoding='utf-8').write(s); print(GAL)

# ---------------------------------------------------------------- ESPOSITORI / DESK / TOTEM
def espositori():
    m=hero("Espositori per fiere",'Espositori, desk e totem per fiere: <span class="grad">coordinati con lo stand</span>.',
      "Desk reception, banchi, totem luminosi, roll-up, vetrine, porta depliant, pannelli e mensole: gli espositori per la fiera, a noleggio o su misura, stampati con la tua grafica e consegnati in fiera insieme allo stand. Oppure da soli, se lo stand ce l'hai già.",
      "Chiedi un preventivo","#richiesta","Cosa forniamo","#cosa")
    m+=cards("cosa","Gli espositori che servono in fiera","Possiamo fornire un elemento solo o tutto il set, coordinato per colori, materiali e grafica.",
      [("Desk e banchi reception","Desk dritti o curvi, in legno o in tessuto teso retroilluminato, con ripiano, vano chiuso e prese. È la prima cosa che il visitatore vede: il banco per fiere va pensato come un'insegna."),
       ("Totem e colonne","Totem pubblicitari bifacciali, luminosi o in cartone riciclabile, totem con schermo touch o porta tablet, colonne con grafica a 360° per farsi vedere da lontano nel padiglione."),
       ("Roll-up e banner","Roll-up avvolgibili, banner in tessuto, X-banner e bandiere: leggeri, veloci da montare, perfetti per stand piccoli, congressi ed eventi."),
       ("Vetrine ed espositori prodotto","Vetrine con serratura e luci LED, piedistalli, espositori a gradoni, mensole a parete, espositori da banco: per far vedere e toccare il prodotto in sicurezza."),
       ("Pannelli e pareti grafiche","Pannelli in forex, dibond o legno, tessuto teso su telaio in alluminio, lightbox retroilluminati: la grafica dello stand, anche da montare su strutture esistenti."),
       ("Arredi e accessori","Tavoli alti e sgabelli, porta depliant, appendiabiti, schermi e supporti, ciabatte e illuminazione: tutto quello che manca per lavorare allo stand.")])
    m+=testo("noleggio","A noleggio o su misura?",None,
      ["Per una o due fiere l'anno il noleggio di desk, totem, vetrine e arredi è quasi sempre la scelta più conveniente: cambi la grafica e riusi la struttura. Per chi espone spesso, o vuole elementi unici sul proprio marchio, conviene farli su misura e conservarli nel nostro magazzino tra una fiera e l'altra.",
       "Molti espositori sono modulari: telai in alluminio e grafiche in tessuto si smontano in pochi minuti, viaggiano in borse o casse leggere e si riusano su metrature diverse. Li coordiniamo con il resto dello stand, così colori, luci e finiture parlano la stessa lingua."],
      [("Stampa compresa.","Curiamo anche i file di stampa e le prove colore."),
       ("Consegna in fiera.","Portiamo gli espositori direttamente al tuo stand e li montiamo."),
       ("Anche senza stand.","Se hai già lo stand, o un preallestito dell'organizzatore, forniamo solo gli espositori."),
       ("Riutilizzabili.","Elementi pensati per tornare in fiera, in showroom o in negozio.")])
    m+=chips("dove","Dove li usiamo",None,[("Stand preallestiti","/stand-preallestiti/"),("Stand piccoli","/stand-fieristici-piccoli/"),("Stand modulari","/stand-modulari/"),
      ("Grafica per stand","/grafica-per-stand-fieristici/"),("Ledwall e illuminazione","/ledwall-e-illuminazione-stand/"),("Eventi, showroom e negozi","/allestimenti-eventi-showroom-negozi/"),("Noleggio stand","/noleggio-stand-fieristici/")])
    qa=[("Noleggiate desk e banchi per fiere?","Sì: desk reception, banchi e tavoli alti a noleggio, personalizzati con la tua grafica e consegnati in fiera."),
        ("Fate totem pubblicitari personalizzati?","Sì, totem bifacciali, luminosi, con schermo o in cartone, stampati con la tua grafica, a noleggio o in acquisto."),
        ("Posso ordinare solo gli espositori senza lo stand?","Sì. Forniamo anche singoli elementi da aggiungere al tuo stand o al preallestito dell'organizzatore."),
        ("Gli espositori sono riutilizzabili?","Sì: strutture in alluminio e grafiche in tessuto si smontano e riusano; cambiando solo la stampa li aggiorni per la fiera successiva."),
        ("Quanto costano desk e totem per fiere?","Dipende da dimensioni, materiali, luci e se sono a noleggio o in acquisto. Ti facciamo un preventivo voce per voce in base a cosa ti serve.")]
    node=svc(ESP,"Espositori, desk e totem per fiere","Fornitura e noleggio di espositori per fiere",
      "Desk reception, banchi, totem, roll-up, vetrine, porta depliant, pannelli e arredi per stand fieristici, a noleggio o su misura, stampati con la tua grafica e consegnati in fiera.",
      ["Desk e banchi per fiere","Totem pubblicitari per fiere","Roll-up e banner per fiere","Vetrine ed espositori prodotto","Pannelli per stand fieristici","Noleggio arredi per stand"])
    pagina(ESP,"Espositori per fiere: desk, banchi, totem e roll-up | Danova Tech",
      "Espositori per fiere a noleggio o su misura: desk reception, banchi, totem luminosi, roll-up, vetrine e pannelli con la tua grafica, consegnati e montati in fiera.",
      "Espositori, desk e totem per fiere — Danova Tech","Desk, banchi, totem, roll-up e vetrine per lo stand, a noleggio o su misura, consegnati in fiera.",
      crumbs("Espositori, desk e totem"),m,qa,[node],[("Progetti di stand",GAL)]+SERVIZI_LINKS+TIPI_LINKS)
    print(ESP)

# ---------------------------------------------------------------- HUB REGIONALI
HUB={
"veneto":dict(nome="Veneto",citta=["verona","padova","vicenza","venezia","treviso","longarone"],
  sedi=[("Veronafiere","Vinitaly, Marmomac, Fieracavalli"),("Fiera di Padova","fiere di settore, congressi ed eventi"),("Vicenza Expo Centre","VicenzaOro e fiere della gioielleria"),("Longarone Fiere Dolomiti","fiere del gelato artigianale e della montagna"),("Venezia e Mestre","congressi, mostre ed eventi in spazi storici")],
  lead="Allestimenti fieristici in Veneto, dalla nostra sede di Mansuè (TV): stand per Veronafiere, Fiera di Padova, Vicenza, Longarone e per eventi e congressi a Venezia e Treviso. Progetto, materiali, grafica e montatori, con tempi da fornitore di casa.",
  intro=["Il Veneto è la nostra regione: la sede è a Mansuè, in provincia di Treviso, e da qui raggiungiamo i principali quartieri fieristici veneti in un'ora o due di strada. Significa sopralluoghi facili, consegne rapide e la possibilità di intervenire anche durante la fiera.",
   "Il calendario veneto copre settori molto diversi: il vino e la pietra a Verona, l'oreficeria a Vicenza, il gelato artigianale a Longarone, fiere e congressi a Padova, eventi e mostre negli spazi storici di Venezia. Per le aziende venete che espongono più volte l'anno, uno stand modulare di proprietà conservato nel nostro magazzino è spesso la scelta più conveniente."],
  qa=[("Dove avete sede?","A Mansuè, in provincia di Treviso, con la produzione a Fontanelle (TV): siamo vicini a tutti i quartieri fieristici del Veneto e del Friuli. In Lombardia abbiamo produzione e uffici a Trumello (PV) e uffici a Vermezzo con Zelo (MI)."),
      ("Lavorate a Veronafiere?","Sì, abbiamo allestito stand al Vinitaly e al Marmomac.")]),
"lombardia":dict(nome="Lombardia",citta=["milano","bergamo","brescia"],
  sedi=[("Fiera Milano Rho","Salone del Mobile, EICMA, Host, MICAM, MIDO e le grandi fiere internazionali"),("Allianz MiCo","congressi ed eventi a Milano"),("Fiera di Bergamo","fiere di settore e per il pubblico"),("Brixia Forum e Centro Fiera Montichiari","fiere dell'industria, della meccanica e del Garda")],
  lead="Allestimenti fieristici in Lombardia: stand per Fiera Milano Rho, Allianz MiCo, Fiera di Bergamo, Brixia Forum e Montichiari. Progetto, materiali, componentistica, grafica, impianti e montatori in fiera, con un unico referente.",
  intro=["La Lombardia ospita il quartiere fieristico più grande d'Italia, Fiera Milano a Rho, e un calendario fittissimo di fiere internazionali: dal design del Salone del Mobile alle moto di EICMA, dall'ospitalità di Host alle calzature di MICAM e all'occhialeria di MIDO. Accanto, Bergamo e Brescia con fiere legate all'industria e al territorio.",
   "In Lombardia siamo presenti direttamente: abbiamo una produzione e degli uffici a Trumello, in provincia di Pavia, e uffici a Vermezzo con Zelo, alle porte di Milano, a circa mezz'ora da Fiera Milano Rho. Sopralluoghi, incontri e assistenza durante la fiera senza lunghe trasferte.",
   "A Rho l'organizzazione conta quanto il progetto: varchi, prenotazione degli scarichi, pass e orari di montaggio vanno gestiti con anticipo. Ce ne occupiamo noi, con i nostri montatori partner, così il giorno dell'allestimento non ci sono sorprese."],
  qa=[("Allestite stand a Fiera Milano Rho?","Sì, abbiamo allestito stand al Salone del Mobile, a EICMA e a Host."),
      ("Lavorate anche a Bergamo e Brescia?","Sì, con la stessa organizzazione: trasporto, squadre, pass e pratiche con l'ente fiera gestiti da noi.")]),
"emilia":dict(nome="Emilia-Romagna",citta=["bologna","rimini","parma"],
  sedi=[("BolognaFiere","Cosmoprof, Cersaie, EIMA e le fiere internazionali di Bologna"),("Rimini Expo Centre","Sigep, Ecomondo, TTG, Macfrut"),("Fiere di Parma","Cibus e le fiere dell'agroalimentare"),("Piacenza, Modena, Ferrara, Reggio Emilia","fiere di settore e congressi")],
  lead="Allestimenti fieristici in Emilia-Romagna: stand per BolognaFiere, Rimini Expo Centre, Fiere di Parma e per le fiere di Piacenza, Modena, Ferrara e Reggio Emilia. Progetto, materiali, grafica, impianti e montatori in fiera.",
  intro=["L'Emilia-Romagna è una delle regioni fieristiche più importanti d'Europa: Bologna con Cosmoprof, Cersaie ed EIMA, Rimini con Sigep, Ecomondo e Macfrut, Parma con Cibus. Fiere internazionali, con buyer da tutto il mondo e stand che devono lavorare per giorni di appuntamenti, assaggi e dimostrazioni.",
   "Ogni settore ha le sue esigenze: pareti portanti per le ceramiche, pedane per le macchine agricole, banchi refrigerati e allacci per il food, luce e vetrine per la cosmetica. Abbiamo allestito stand al Cosmoprof, al Cersaie e all'EIMA, e seguiamo anche aziende straniere che espongono in regione."],
  qa=[("Allestite stand a BolognaFiere?","Sì, abbiamo allestito stand al Cosmoprof, al Cersaie e all'EIMA."),
      ("Lavorate anche nelle fiere più piccole della regione?","Sì: Piacenza, Modena, Ferrara, Reggio Emilia e Forlì, con la stessa organizzazione delle grandi fiere.")]),
}
def hubs():
    NOMI={s:c for c,s in TUTTE_CITTA}
    for k,d in HUB.items():
        P=REG[k]; n=d['nome']
        m=hero(f"Allestimenti fieristici · {n}",f'Allestimenti fieristici in {n}: <span class="grad">stand chiavi in mano</span>.',d['lead'],
          f"Preventivo per uno stand in {n}","#richiesta","Le città","#citta-regione")
        m+=testo("regione",f"Stand in {n}, dal progetto al montaggio",None,d['intro'])
        m+=testo("sedi",f"I quartieri fieristici in {n}",None,[],[(a+".",b) for a,b in d['sedi']])
        m+=chips("citta-regione",f"Le nostre pagine per città in {n}","Per ogni città trovi le fiere, cosa sapere per lo stand e il calendario delle prossime edizioni.",[(f"Allestimenti fieristici a {NOMI[s]}",CITTA_URL[s]) for s in d['citta']])
        m+=cards("cosa","Cosa facciamo per il tuo stand",None,SERVIZI_CARDS(""))
        qa=d['qa']+[("Accettate richieste urgenti?","Sì, anche a ridosso della fiera: valutiamo subito cosa è possibile fare con i nostri montatori partner."),
                    ("Lo stand è a noleggio o in acquisto?","Tutti e due: preallestiti, modulari, in tessuto teso e su misura, a noleggio o di tua proprietà, con magazzino tra una fiera e l'altra.")]
        node=svc(P,f"Allestimenti fieristici in {n}","Allestimento e montaggio di stand fieristici",
          f"Progettazione, materiali, grafica, impianti, montaggio e smontaggio di stand fieristici in {n}.",
          ["Stand preallestiti","Stand modulari","Stand su misura","Montaggio e smontaggio in fiera","Noleggio stand e arredi"],[{"@type":"AdministrativeArea","name":n}])
        rel=[(f"Allestimenti fieristici a {NOMI[s]}",CITTA_URL[s]) for s in d['citta']]+[("Progetti di stand",GAL),("Calendario fiere 2026–2027",CAL),("Allestimenti fieristici",PILLAR)]
        tt=f"Allestimenti fieristici in {n}: stand e allestitori | Danova Tech"
        if len(tt)>62: tt=f"Allestimenti fieristici in {n}: stand e allestitori"
        if len(tt)>62: tt=f"Allestimenti fieristici {n}: stand e allestitori"
        pagina(P,tt,
          f"Allestimenti fieristici in {n}: stand chiavi in mano nei quartieri fieristici della regione. Progetto 3D, grafica, impianti e montatori in fiera, a noleggio o in acquisto.",
          f"Allestimenti fieristici in {n} — Danova Tech",f"Stand chiavi in mano in {n}: progetto, materiali, grafica e montatori in fiera.",
          [("Home","/"),("Allestimenti fieristici",PILLAR),(n,None)],m,qa,[node],rel,cta_t=f"Esponi in {n}?",fiera_form=f"Fiera in {n}")
        print(P)

if __name__=='__main__':
    galleria(); espositori(); hubs()
