# -*- coding: utf-8 -*-
# Fiere in Europa (13 ottobre 2026) - uso: python3 build_europa.py
#  /allestimenti-fieristici-estero/            hub Europa (sostituisce la versione di it_pages.py)
#  /allestimenti-fieristici-<paese>/           una pagina per paese (dati in PAESI_PAGINE)
# Dati dichiarati dal cliente: oltre 1.000 fiere all'estero, piu' di 25 anni, produzione in Italia e
# trasporto gestito da noi, montaggio con squadre proprie + partner locali, pratiche con l'ente fiera,
# dogana Svizzera/Regno Unito, magazzino e tour europeo, personale che parla le lingue, anche con poche settimane.
# Nessuna foto reale: si riusano i render (didascalia "Render di progetto").
import os, re
from nuove_common import *
import immagini, lib
lib.TODAY='2026-10-13'

HUB = "/allestimenti-fieristici-estero/"
def P_(slug): return f"/allestimenti-fieristici-{slug}/"
def esiste(path): return os.path.exists(os.path.join(R, path.strip('/'), 'index.html'))
def link(testo, path): return f'<a href="{path}">{testo}</a>' if esiste(path) else testo

# ---------------------------------------------------------------- panoramica paesi (hub)
# slug, nome, "in ...", quartieri fieristici, fiere principali
PAESI = [
 ("germania","Germania","in Germania","Düsseldorf, Colonia, Francoforte, Monaco, Hannover, Norimberga, Berlino, Stoccarda",
  "ProWein, Anuga, ISM, Ambiente, EuroShop, bauma, Hannover Messe, interzum, BIOFACH, Fruit Logistica"),
 ("francia","Francia","in Francia","Paris Nord Villepinte, Paris Expo Porte de Versailles, Eurexpo Lione, Cannes",
  "SIAL Paris, Maison&Objet, SIRHA, Batimat, Première Vision, MIPIM"),
 ("spagna","Spagna","in Spagna","IFEMA Madrid, Fira Barcelona Gran Via e Montjuïc, Feria Valencia, Bilbao Exhibition Centre",
  "Fitur, Alimentaria, Hostelco, Fruit Attraction, Cevisama, Seafood Expo Global, ISE"),
 ("olanda","Olanda","in Olanda","RAI Amsterdam, Jaarbeurs Utrecht, Ahoy Rotterdam",
  "PLMA World of Private Label, IBC, METSTRADE, GreenTech"),
 ("belgio","Belgio","in Belgio","Brussels Expo, Flanders Expo Gand, Kortrijk Xpo",
  "Batibouw, Agribex, Interieur Kortrijk"),
 ("svizzera","Svizzera","in Svizzera","Messe Basel, Palexpo Ginevra, Messe Zürich, Bernexpo",
  "Swissbau, Art Basel, Watches and Wonders, EPHJ"),
 ("austria","Austria","in Austria","Messe Wien, Messezentrum Salisburgo, Messe Innsbruck, Messe Wels",
  "Alles für den Gast, Interalpin, AgrarisWels e le fiere di Vienna"),
 ("polonia","Polonia","in Polonia","MTP Poznań, Ptak Warsaw Expo, EXPO XXI Varsavia, Targi Kielce",
  "Polagra, BUDMA, Warsaw Pack, Plastpol"),
 ("repubblica-ceca","Repubblica Ceca","in Repubblica Ceca","Výstaviště Brno, PVA Expo Praga",
  "MSV Brno (fiera internazionale della meccanica) e le fiere di Praga"),
 ("regno-unito","Regno Unito","nel Regno Unito","ExCeL London, Olympia London, NEC Birmingham",
  "IFE, London Book Fair, Spring Fair e le fiere di settore di Londra e Birmingham"),
 ("portogallo","Portogallo","in Portogallo","FIL Lisbona, Exponor Porto",
  "BTL, Web Summit e le fiere di settore di Lisbona e Porto"),
]
NOME = {s: n for s, n, *_ in PAESI}

NUMERI = [("Fiere all'estero","Oltre 1.000"),("Esperienza","Più di 25 anni"),("Paesi","11 in Europa"),
          ("Trasporto","Con i nostri mezzi"),("Montaggio","Squadre nostre e partner locali"),("Preavviso","Anche poche settimane")]

CARDS_ESTERO = [
 ("Progetto e pratiche con l'ente fiera","Render 3D, piante, calcoli statici per gli stand a due piani, certificati dei materiali: prepariamo e presentiamo noi la documentazione che chiede il regolamento tecnico del quartiere fieristico."),
 ("Produzione in Italia","Strutture, pareti e arredi in legno li realizzano i nostri laboratori partner sul nostro progetto, e noi coordiniamo ogni fase fino al montaggio. In fiera si monta, non si improvvisa."),
 ("Trasporto con i nostri mezzi","Lo stand viaggia sui nostri camion, con i nostri imballi e gli orari di scarico prenotati. Nessun passaggio di mano tra spedizionieri."),
 ("Montatori sul posto","Montatori partner dall'Italia, affiancati da partner locali di fiducia quando lo stand è grande o i tempi di allestimento sono stretti. Il coordinamento resta nostro."),
 ("Dogana Svizzera e Regno Unito","Per le fiere fuori dall'Unione europea prepariamo con lo spedizioniere doganale i documenti per l'importazione temporanea dello stand e il rientro in Italia."),
 ("Magazzino e tour europeo","Conserviamo lo stand tra una fiera e l'altra e lo riportiamo, adattato alla nuova metratura, nella fiera successiva: in Italia o in un altro paese."),
]

def griglia_paesi(escludi=None):
    out=[]
    for s,n,in_,poli,fiere in PAESI:
        if s==escludi: continue
        t = f'<a href="{P_(s)}">Stand {in_}</a>' if esiste(P_(s)) else f"Stand {in_}"
        out.append((t, f"<b>Quartieri fieristici:</b> {poli}.<br><b>Fiere:</b> {fiere}."))
    return out

# ---------------------------------------------------------------- HUB
def hub():
    m = hero("Allestimenti fieristici in Europa",
      'Allestimenti fieristici in Europa: <span class="grad">stand montati in 11 paesi</span>.',
      "Oltre 300 stand montati, da un team in fiera da più di 20 anni. Progettiamo lo stand, lo facciamo costruire in Italia dai nostri laboratori partner, lo spediamo con trasportatori di fiducia in Germania, Francia, Spagna, Benelux, Svizzera, Austria, Polonia, Repubblica Ceca, Regno Unito e Portogallo, e coordiniamo il montaggio con squadre partner, anche locali. Un solo referente, che ti parla in italiano, dal progetto allo smontaggio.",
      "Richiedi un preventivo per la fiera","#richiesta","I paesi in cui lavoriamo","#paesi")
    m += scheda("numeri", "Fiere all'estero, <span class=\"grad\">in numeri</span>", NUMERI)
    m += cards("cosa", "Cosa facciamo per le fiere all'estero",
      "Tutto quello che serve per esporre fuori dall'Italia, gestito da un unico fornitore: niente allestitore locale da cercare, niente lingue da tradurre, niente spedizionieri da coordinare.", CARDS_ESTERO)
    m += cards("paesi", "Dove montiamo stand in Europa",
      "I quartieri fieristici e le fiere in cui lavoriamo più spesso. Per ogni paese trovi una pagina con regole locali, distanze e tempi.", griglia_paesi())
    m += testo("tour", "Lo stesso stand, <span class=\"grad\">in più fiere europee</span>", None,
      ["Molte aziende italiane fanno due, tre o quattro fiere internazionali l'anno: Francoforte o Colonia d'inverno, Barcellona o Parigi in primavera, una fiera di settore in autunno. Costruire uno stand diverso ogni volta costa, e spedire uno stand di proprietà da un paese all'altro senza un'organizzazione dietro è un rischio.",
       "Con il tour europeo progettiamo uno stand che si adatta a metrature e tipi di spazio diversi, di solito una struttura modulare con alcuni elementi su misura. Tra una fiera e l'altra resta nel nostro magazzino: lo controlliamo, cambiamo le grafiche se serve e lo rispediamo in fiera. Tu ricevi un calendario di consegne e un preventivo per l'intera stagione."],
      [("Un progetto, più configurazioni.","Pianta per ogni fiera: in linea, angolo, penisola o isola."),
       ("Grafiche intercambiabili.","Lingua, prodotti e messaggi aggiornati per ogni mercato."),
       ("Magazzino e controllo.","Pulizia, riparazioni e verifica dei pezzi prima di ogni partenza."),
       ("Costi prevedibili.","Trasporti e montaggi pianificati sull'intera stagione.")])
    m += testo("logistica", "Trasporto, dogana e documenti", None,
      ["Lo stand parte dall'Italia: il trasporto lo gestiamo noi, con trasportatori di fiducia. Pianifichiamo il viaggio sugli orari di scarico del quartiere fieristico e sulle regole dei paesi attraversati, come i divieti di circolazione domenicali e festivi per i mezzi pesanti, che in Germania, Austria e Francia possono far perdere un giorno di allestimento.",
       "Dentro l'Unione europea lo stand viaggia senza formalità doganali. Per la Svizzera e il Regno Unito serve l'importazione temporanea: prepariamo con lo spedizioniere doganale il carnet ATA o la dichiarazione equivalente, così lo stand entra, resta in fiera per i giorni della manifestazione e rientra in Italia senza pagare dazi e IVA come se fosse venduto. Per le squadre di montaggio prepariamo i documenti richiesti per il lavoro all'estero, a partire dal modello A1."],
      [("Unione europea.","Nessuna dogana: documenti di trasporto e pass per lo scarico."),
       ("Svizzera.","Importazione temporanea con carnet ATA o dichiarazione doganale."),
       ("Regno Unito.","Dogana dopo la Brexit: dichiarazioni in uscita e in entrata, tempi da calcolare."),
       ("Montatori.","Modello A1 e comunicazioni di distacco previste dal paese.")])
    m += testo("regole", "Ogni quartiere fieristico <span class=\"grad\">ha il suo regolamento</span>", None,
      ["Altezze massime, distanze dai confini dello stand, pareti verso i vicini, classe di reazione al fuoco dei materiali, chi può fare l'allaccio elettrico, chi può appendere strutture al soffitto: ogni ente fiera ha il suo regolamento tecnico, e cambia da paese a paese. In Germania si parla di Technische Richtlinien, in Francia di règlement technique e di classificazione M1, nel Regno Unito di health and safety e di structural calculations.",
       "Leggiamo il regolamento della tua fiera prima di disegnare, non dopo. Così il progetto viene approvato al primo invio, i certificati dei materiali sono pronti allo stand e il giorno dell'allestimento nessuno ti ferma per un pannello o un faretto non conforme."])
    m += passi("metodo","Come lavoriamo","Una fiera all'estero, <span class=\"grad\">organizzata dall'Italia.</span>",None,
      [("Brief","Fiera, paese, date, metratura, tipo di spazio, obiettivi. Anche solo una telefonata."),
       ("Progetto e preventivo","Render 3D e preventivo voce per voce, con trasporto, montaggio e trasferte già dentro."),
       ("Pratiche e logistica","Approvazione dell'ente fiera, servizi ordinati (corrente, rigging, pulizie), viaggio e documenti."),
       ("Montaggio e consegna","Squadre in fiera nei giorni di allestimento, prova di luci e schermi, stand consegnato pulito."),
       ("Smontaggio e rientro","Disallestimento, carico, rientro in Italia o trasferimento alla fiera successiva, magazzino.")])
    m += testo("esempio", "Un esempio: <span class=\"grad\">tre fiere, tre paesi, uno stand</span>", None,
      ["Un'azienda alimentare veneta espone ad Anuga a Colonia con un'isola da 80 metri quadri, poi ad Alimentaria a Barcellona con una penisola da 48 e al SIAL di Parigi con un angolo da 36. Le serve uno stand riconoscibile, con cucina e banco degustazione, che si possa ridurre senza perdere l'impatto.",
       "Progettiamo un sistema in alluminio con pareti in legno e grafiche in tessuto, e tre piante sulle tre metrature. Prepariamo le pratiche con i tre enti fiera, organizziamo il trasporto e coordiniamo il montaggio con squadre partner, compreso un partner locale a Colonia, dove lo stand è più grande. Tra una fiera e l'altra lo stand resta nel nostro magazzino. Il referente, per tutta la stagione, è sempre lo stesso."])
    m += testo("stranieri", "Siete un'azienda straniera?", None,
      ["Lavoriamo anche per aziende estere che espongono in Europa o in Italia. Trovate le nostre pagine in "
       '<a href="/en/exhibition-stand-builder-italy/" hreflang="en">inglese</a>, <a href="/de/messebau-italien/" hreflang="de">tedesco</a>, '
       '<a href="/fr/standiste-salon-italie/" hreflang="fr">francese</a> e <a href="/es/montaje-stands-feriales-italia/" hreflang="es">spagnolo</a>.'])
    qa = [
     ("In quali paesi montate stand?","In Germania, Francia, Spagna, Olanda, Belgio, Svizzera, Austria, Polonia, Repubblica Ceca, Regno Unito e Portogallo. Il nostro team lavora in fiera da oltre 20 anni e abbiamo già montato oltre 300 stand."),
     ("Lo stand viene prodotto in Italia?","Sì. Lo progettiamo noi, lo costruiscono in Italia i nostri laboratori partner e lo spediamo in fiera con trasportatori di fiducia. Quando conviene, noleggiamo sul posto arredi o attrezzature."),
     ("Chi monta lo stand all'estero?","Squadre di montatori partner che partono dall'Italia, affiancate da partner locali di fiducia per gli stand più grandi o quando i tempi di allestimento sono stretti. Il coordinamento resta nostro."),
     ("Vi occupate voi delle pratiche con l'ente fiera?","Sì: progetto, approvazione, calcoli statici per gli stand a due piani, certificati di reazione al fuoco dei materiali, ordini di corrente, rigging e altri servizi della fiera."),
     ("Come funziona per le fiere in Svizzera e nel Regno Unito?","Sono fuori dall'Unione europea: prepariamo con lo spedizioniere doganale l'importazione temporanea dello stand, di solito con carnet ATA, così rientra in Italia senza pagare dazi e IVA."),
     ("Potete conservare lo stand e portarlo in più fiere?","Sì. Lo teniamo nel nostro magazzino, lo controlliamo e lo riportiamo nella fiera successiva, anche in un altro paese, adattandolo alla nuova metratura."),
     ("Con quanto anticipo devo chiedervi lo stand?","Prima è meglio, ma accettiamo incarichi anche a poche settimane dalla fiera: valutiamo subito squadre, mezzi e materiali disponibili."),
     ("Quanto costa uno stand per una fiera all'estero?","Dipende da metratura, tipo di stand, paese, durata dell'allestimento e numero di fiere. Ti facciamo un preventivo voce per voce con trasporto, montaggio e trasferte già compresi. Nella <a href=\"/quanto-costa-uno-stand-fieristico/\">guida ai costi</a> trovi le voci che pesano di più."),
     ("Lavorate anche per aziende straniere?","Sì, abbiamo pagine in inglese, tedesco, francese e spagnolo per le aziende estere che espongono in Europa e in Italia.")]
    areas=[{"@type":"Country","name":n} for _,n,*_ in PAESI]+[{"@type":"Place","name":"Europa"}]
    node=svc(HUB,"Allestimenti fieristici in Europa","Allestimento di stand per fiere internazionali",
      "Progettazione, produzione in Italia, trasporto gestito da noi, pratiche con l'ente fiera, dogana, montaggio e smontaggio di stand per fiere in Germania, Francia, Spagna, Olanda, Belgio, Svizzera, Austria, Polonia, Repubblica Ceca, Regno Unito e Portogallo.",
      [f"Stand per fiere {in_}" for _,_,in_,*_ in PAESI]+["Trasporto e logistica dello stand","Importazione temporanea e carnet ATA","Magazzino e tour europeo"],areas)
    rel=[(f"Stand {in_}",P_(s)) for s,_,in_,*_ in PAESI if esiste(P_(s))]+[("Progetti di stand","/progetti-stand-fieristici/")]+SERVIZI_LINKS+[("Contributi per le fiere 2026","/contributi-fiere-2026/"),("Guida: come preparare una fiera","/guide/come-preparare-una-fiera/")]
    pagina(HUB,"Allestimenti fieristici in Europa: stand per fiere all'estero",
      "Stand per fiere all'estero in 11 paesi europei: progetto, produzione in Italia, trasporto gestito da noi, dogana, montatori e smontaggio. Oltre 1.000 fiere in 25 anni.",
      "Allestimenti fieristici in Europa — Danova Tech","Stand per fiere all'estero: progetto, trasporto, dogana e montaggio in 11 paesi europei.",
      crumbs("Fiere in Europa"),m,qa,[node],rel,cta_t="Esponi all'estero?",fiera_form="")
    print(HUB)

# ---------------------------------------------------------------- PAGINE PAESE
PAESI_PAGINE = {}
PAESI_PAGINE["germania"] = dict(
 render="stand-due-piani-sala-riunioni",
 alt="Render di stand fieristico a due piani con sala riunioni al piano superiore, per una fiera in Germania",
 cap="Render di progetto: stand a due piani per una grande fiera tedesca, con sala riunioni al piano superiore.",
 title="Allestimenti fieristici in Germania: stand e montatori",
 desc="Stand per fiere in Germania a Düsseldorf, Colonia, Francoforte, Monaco, Hannover e Berlino: progetto, trasporto gestito da noi, pratiche e montaggio.",
 h1='Allestimenti fieristici in Germania: <span class="grad">stand chiavi in mano</span>.',
 lead="Esponi a ProWein, Anuga, ISM, Ambiente, bauma o in un'altra fiera tedesca? Progettiamo lo stand, lo facciamo costruire in Italia dai nostri laboratori partner, lo spediamo con trasportatori di fiducia a Düsseldorf, Colonia, Francoforte, Monaco, Hannover, Norimberga o Berlino e coordiniamo il montaggio con squadre partner, anche locali. Le pratiche con la Messe le seguiamo noi, tu parli in italiano con un solo referente.",
 intro=["La Germania è il primo paese fieristico d'Europa e, per molti settori, del mondo. Nei suoi quartieri fieristici si tengono le fiere di riferimento per il vino, l'alimentare, i dolci, la casa, il retail, la meccanica, le costruzioni e l'industria. Per un'azienda italiana esporre in Germania vuol dire incontrare buyer da tutto il mondo, ma anche confrontarsi con le regole più precise e i padiglioni più grandi.",
   "Le fiere tedesche sono organizzatissime: orari di accesso per i camion, aree di attesa, pass per i montatori, regolamenti tecnici dettagliati e controlli in padiglione. Chi arriva senza progetto approvato o senza i certificati dei materiali rischia di perdere ore preziose. Lavoriamo nelle fiere tedesche da anni e sappiamo cosa preparare prima di partire."],
 poli=[
  ("Düsseldorf · Messe Düsseldorf","ProWein (vino e distillati), EuroShop (retail e allestimento negozi), interpack, drupa, MEDICA, boot, K, wire e Tube. Circa 1.050 km dalla nostra sede."),
  ("Colonia · Koelnmesse","Anuga (alimentare), ISM (dolci e snack), interzum (componenti per il mobile), ORGATEC, IDS (dentale), spoga+gafa, gamescom. Circa 1.000 km."),
  ("Francoforte · Messe Frankfurt","Ambiente (casa, tavola, regalo), Heimtextil, Light + Building, ISH, Automechanika, Texprocess, IFFA. Circa 850 km."),
  ("Monaco di Baviera · Messe München","bauma, BAU, IFAT, analytica, electronica, productronica, drinktec, transport logistic, EXPO REAL, INHORGENTA. Circa 430 km."),
  ("Hannover · Deutsche Messe","Hannover Messe, Agritechnica, EuroTier, LIGNA, EMO, IAA Transportation. Circa 1.000 km."),
  ("Norimberga · NürnbergMesse","BIOFACH, Spielwarenmesse, FachPack, embedded world, Interzoo, Chillventa, BrauBeviale. Circa 600 km."),
  ("Berlino · Messe Berlin","Fruit Logistica, ITB, IFA, InnoTrans, Grüne Woche. Circa 1.050 km."),
  ("Stoccarda, Lipsia, Essen, Friedrichshafen","AMB, LogiMAT, CMT, Intervitis Interfructa a Stoccarda; E-world a Essen; Eurobike e AERO a Friedrichshafen. Tra 450 e 1.050 km."),
 ],
 regole_intro="Le fiere tedesche seguono regolamenti tecnici molto simili tra loro (Technische Richtlinien), con differenze da quartiere a quartiere. Quelli che contano di più per il progetto dello stand:",
 regole=[
  ("Approvazione del progetto.","Gli stand a due piani, le strutture alte e le costruzioni particolari vanno approvati dalla Messe prima del montaggio, con disegni e calcolo statico verificabile (Standsicherheitsnachweis)."),
  ("Reazione al fuoco.","I materiali devono essere almeno difficilmente infiammabili: classe B1 secondo DIN 4102 o classe equivalente secondo EN 13501-1. I certificati vanno tenuti allo stand."),
  ("Corrente.","L'allaccio alla rete del padiglione lo fa solo l'elettricista autorizzato dalla fiera; l'impianto dello stand va realizzato secondo le norme VDE."),
  ("Rigging.","Strutture e insegne appese al soffitto si ordinano attraverso il servizio della Messe, con i punti di appendimento e il peso indicati in anticipo."),
  ("Altezze e confini.","Altezza massima costruibile, pareti verso gli stand vicini e lati aperti verso i corridoi seguono regole precise, che variano da padiglione a padiglione."),
  ("Accessi e scarichi.","I camion entrano su prenotazione o tramite aree di attesa, con pass a tempo. Ritardi significano perdere il turno di scarico."),
 ],
 logistica=["Il viaggio dalla nostra sede di Mansuè va da circa 430 km per Monaco a circa 1.050 km per Düsseldorf e Berlino. Per le fiere più lontane i camion partono con un giorno di margine: in Germania i mezzi pesanti non possono circolare la domenica e nei giorni festivi, e un ritardo sul turno di scarico costa più di un giorno di viaggio.",
   "Le squadre partono insieme allo stand o lo raggiungono in fiera. Per i lavoratori in trasferta in Germania prepariamo i documenti richiesti, come il modello A1 e le comunicazioni previste per il distacco dei lavoratori nel settore degli allestimenti. Quando lo stand è grande o i giorni di allestimento sono pochi, affianchiamo partner locali di fiducia, coordinati dal nostro capocantiere."],
 fiere=[("anuga","Anuga"),("ism","ISM"),("prowein","ProWein"),("euroshop","EuroShop"),("ambiente","Ambiente"),("bauma","bauma")],
 esempio=["Un produttore di vino del Veneto passa da uno stand collettivo a uno stand proprio a ProWein, a Düsseldorf: 48 metri quadri a penisola, con banco di degustazione, cella per le bottiglie e un tavolo riservato per gli incontri con gli importatori.",
   "Progettiamo lo stand in legno e tessuto teso, presentiamo il progetto e i certificati dei materiali alla Messe, ordiniamo corrente e acqua per il lavello. I camion partono il venerdì per evitare il divieto domenicale, la squadra monta in due giorni e consegna lo stand pulito la sera prima dell'apertura. A fine fiera lo stand torna nel nostro magazzino, pronto per il Vinitaly."],
 qa=[
  ("In quali città tedesche montate stand?","Düsseldorf, Colonia, Francoforte, Monaco, Hannover, Norimberga, Berlino, Stoccarda, Lipsia, Essen e Friedrichshafen: in tutti i principali quartieri fieristici tedeschi."),
  ("Vi occupate voi dell'approvazione del progetto da parte della Messe?","Sì: disegni, calcolo statico per gli stand a due piani o con strutture alte, certificati di reazione al fuoco dei materiali e tutto quello che chiede il regolamento tecnico della fiera."),
  ("I materiali italiani vanno bene per le fiere tedesche?","Sì, se hanno la classe di reazione al fuoco richiesta: in Germania di solito almeno B1 secondo DIN 4102 o la classe equivalente europea EN 13501-1. Scegliamo materiali certificati e portiamo i certificati in fiera."),
  ("Chi fa l'impianto elettrico?","L'impianto dello stand lo realizziamo noi secondo le norme richieste; l'allaccio alla rete del padiglione è riservato all'elettricista della fiera, che ordiniamo per te insieme agli altri servizi."),
  ("Potete fare uno stand a due piani in Germania?","Sì. Gli stand a due piani richiedono un'approvazione specifica e un calcolo statico verificabile: li prepariamo noi con i tempi chiesti dalla Messe."),
  ("Montate con squadre italiane o tedesche?","Con squadre di montatori partner che partono dall'Italia, affiancate da partner locali di fiducia quando servono più persone o tempi più stretti. Il coordinamento resta sempre nostro."),
  ("Con quanto anticipo devo contattarvi per una fiera in Germania?","Prima è meglio, perché le scadenze per l'approvazione del progetto e per ordinare i servizi sono fisse. Ma accettiamo incarichi anche a poche settimane dalla fiera.")],
 offers=["Stand per fiere a Düsseldorf","Stand per fiere a Colonia","Stand per fiere a Francoforte","Stand per fiere a Monaco di Baviera","Stand per fiere ad Hannover","Stand per fiere a Norimberga","Stand per fiere a Berlino","Stand a due piani in Germania"],
 citta=["Düsseldorf","Colonia","Francoforte sul Meno","Monaco di Baviera","Hannover","Norimberga","Berlino","Stoccarda"],
)

def paese(slug):
    d=PAESI_PAGINE[slug]; n=NOME[slug]; in_=[x[2] for x in PAESI if x[0]==slug][0]; P=P_(slug)
    immagini.MAP[P]=(d['render'],d['alt'],d['cap'],'it')
    m = hero(f"Allestimenti fieristici · {n}", d['h1'], d['lead'], f"Preventivo per una fiera {in_}","#richiesta","I quartieri fieristici","#quartieri")
    m += scheda("numeri", f"Fiere {in_}: <span class=\"grad\">chi siamo</span>",
      [("Esperienza","Più di 25 anni"),("Fiere all'estero","Oltre 1.000"),("Produzione","In Italia"),("Trasporto","Con i nostri mezzi"),("Montaggio","Squadre nostre e partner locali"),("Referente","Unico, in italiano")])
    m += testo("paese", f"Esporre {in_}", None, d['intro'])
    m += testo("quartieri", f"I quartieri fieristici {in_}", "Dove montiamo stand, con le fiere principali e la distanza indicativa su strada dalla nostra sede di Mansuè (Treviso).", [], d['poli'])
    m += testo("regole", f"Le regole delle fiere {in_}", d['regole_intro'], [], d['regole'])
    m += cards("cosa", "Cosa facciamo per il tuo stand", None, CARDS_ESTERO)
    m += testo("logistica", f"Viaggio, squadre e documenti", None, d['logistica'])
    fl=[(f"Stand {t}", f"/stand-{k}/") for k,t in d['fiere']]
    m += chips("fiere", f"Le fiere {in_} che seguiamo più spesso", "Per alcune fiere trovi una pagina dedicata con date, padiglioni e consigli per lo stand.",
      [(t, u if esiste(u) else None) for t,u in fl])
    m += testo("esempio", "Un esempio", None, d['esempio'])
    m += cards("altri-paesi", "Lavoriamo anche in altri paesi", None, griglia_paesi(escludi=slug))
    node=svc(P,f"Allestimenti fieristici {in_}","Allestimento di stand per fiere internazionali",
      f"Progettazione, produzione in Italia, trasporto gestito da noi, pratiche con l'ente fiera, montaggio e smontaggio di stand per fiere {in_}.",
      d['offers'],[{"@type":"Country","name":n}]+[{"@type":"City","name":c} for c in d['citta']])
    rel=[("Fiere in Europa e all'estero",HUB)]+[(t,u) for t,u in fl if esiste(u)]+[(f"Stand {x[2]}",P_(x[0])) for x in PAESI if x[0]!=slug and esiste(P_(x[0]))]+SERVIZI_LINKS
    pagina(P,d['title'],d['desc'],f"Allestimenti fieristici {in_} — Danova Tech",
      f"Stand chiavi in mano {in_}: progetto, trasporto gestito da noi, pratiche con la fiera e montaggio.",
      [("Home","/"),("Allestimenti fieristici",PILLAR),("Fiere in Europa",HUB),(n,None)],m,d['qa'],[node],rel,
      cta_t=f"Esponi {in_}?",fiera_form=f"Fiera {in_}")
    print(P)

if __name__=='__main__':
    import sys
    quali=sys.argv[1:] or list(PAESI_PAGINE)
    for s in quali:
        if s in PAESI_PAGINE: paese(s)
    hub()   # per ultimo: cosi' linka le pagine paese appena create
