# -*- coding: utf-8 -*-
# Pagine per metratura e guide fiere in italiano (14 ottobre 2026).
# Sezioni: ('t', id, titolo, lead, paragrafi, lista) | ('c', id, titolo, lead, cards) | ('p', id, eyebrow, titolo, passi) | ('s', id, titolo, righe, nota)

# ------------------------------------------------------------------ METRATURE
M = [
dict(mq=9, slug="stand-9-mq", dims="3 × 3 m", render="stand-piccolo-12-mq",
 title="Stand 9 mq (3×3): idee, layout e allestimento | Danova Tech",
 desc="Stand fieristico di 9 mq (3×3 m): cosa ci sta, layout che funzionano, preallestito o modulare, grafica e luci. Progetto e montaggio in fiera, preventivo gratuito.",
 h1='Stand 9 mq: <span class="grad">3 metri per 3</span>, usati bene.',
 lead="Nove metri quadri sono il modulo più piccolo che si trova in quasi tutte le fiere: un quadrato di tre metri per lato, spesso aperto su un solo lato. È poco spazio, ma è abbastanza per farsi notare e per parlare con le persone giuste, se ogni centimetro ha uno scopo.",
 rows=[("Misure tipiche","3 × 3 m, altezza pareti di solito 2,5–3 m (dipende dal regolamento)"),("Lati aperti","Di solito uno (in linea), a volte due (angolo)"),("Persone nello stand","Due persone dello staff e due o tre visitatori alla volta"),("Soluzioni adatte","Preallestito personalizzato, modulare in alluminio e tessuto"),("Montaggio","Poche ore nei giorni di allestimento")],
 sections=[
  ('t','come',"Come si organizza uno stand di 9 mq",None,[
    "In nove metri quadri lo spazio si divide in tre fasce: il fondo, che porta il marchio e il messaggio principale; il centro, che resta libero per far entrare le persone; il fronte, dove sta il banco o il prodotto. Se il fondo è pieno di mensole e il centro è occupato da un tavolo, lo stand diventa un corridoio e chi passa tira dritto.",
    "Funziona meglio un solo elemento forte: una parete grafica retroilluminata, un prodotto su un podio illuminato, uno schermo con un video breve. Il ripostiglio, se serve, si ricava in un angolo con una porta, ma in 9 mq si mangia quasi un metro quadro: spesso conviene un banco con vano chiuso."],None),
  ('t','cosa',"Cosa ci sta in 9 metri quadri",None,[],[
    ("Un banco o desk con vano chiuso.","Per brochure, borse e campioni, senza bisogno di un ripostiglio."),
    ("Una parete grafica o un lightbox.","Il marchio in alto, leggibile dal corridoio; testi brevi all'altezza degli occhi."),
    ("Un tavolino alto con due sgabelli.","Per le conversazioni veloci; i tavoli bassi con sedie occupano troppo."),
    ("Mensole o un espositore.","Pochi prodotti, ben illuminati, invece di tutto il catalogo."),
    ("Uno schermo.","Utile se il prodotto è grande o è un servizio: un video di 30 secondi senza audio.")]),
  ('c','layout',"Tre layout che funzionano",None,[
    ("Parete e banco","Parete di fondo retroilluminata con il marchio, banco reception sul fronte spostato di lato, centro libero."),
    ("Prodotto al centro","Un podio illuminato con il prodotto in posizione arretrata, grafica di fondo semplice, tavolino alto di lato."),
    ("Mini showroom","Mensole luminose su un lato, grafica sull'altro, banco piccolo davanti: per chi deve mostrare più referenze.")]),
  ('t','errori',"Errori da evitare in uno stand piccolo",None,[],[
    ("Troppi testi.","Dal corridoio si leggono il marchio e una frase; il resto è per chi entra."),
    ("Il banco come barriera.","Un banco messo in mezzo al fronte chiude lo stand: spostalo di lato."),
    ("Luce insufficiente.","Il preallestito standard ha poca luce: due o tre faretti in più cambiano lo stand."),
    ("Scatole in vista.","In 9 mq si vede tutto: serve un posto chiuso per scatole e borse.")]),
 ],
 qa=[("Meglio un preallestito o uno stand modulare per 9 mq?","Per una fiera singola, un preallestito personalizzato con grafica, luci e arredi scelti è la soluzione più economica. Se esponi più volte l'anno, uno stand modulare di proprietà si ripaga e si adatta anche a spazi più grandi."),
  ("Si può avere un ripostiglio in 9 mq?","Sì, ma occupa quasi un metro quadro. Spesso è meglio un banco con vano chiuso o un mobile contenitore integrato nella parete."),
  ("Quanto tempo serve per montare uno stand di 9 mq?","Di solito poche ore nei giorni di allestimento. Il lavoro vero è prima: progetto, grafiche e pratiche con l'ente fiera."),
  ("Quanto costa uno stand di 9 mq?","Dipende da struttura, grafica, arredi, impianto elettrico e fiera. Non pubblichiamo listini: ti mandiamo un preventivo gratuito voce per voce.")]),

dict(mq=12, slug="stand-12-mq", dims="4 × 3 m o 6 × 2 m", render="stand-piccolo-12-mq",
 title="Stand 12 mq: layout, idee e allestimento in fiera | Danova Tech",
 desc="Stand fieristico di 12 mq (4×3 o 6×2 m): come organizzare lo spazio, cosa ci sta, preallestito o modulare, luci e grafica. Progetto e montaggio, preventivo gratuito.",
 h1='Stand 12 mq: <span class="grad">piccolo, ma con un posto per parlare.</span>',
 lead="Dodici metri quadri sono la metratura in cui uno stand piccolo comincia ad avere due zone: una per farsi vedere dal corridoio e una per sedersi a parlare. Le misure più comuni sono 4 × 3 metri o, nelle fiere con corsie strette, 6 × 2 metri, e cambiano molto il progetto.",
 rows=[("Misure tipiche","4 × 3 m oppure 6 × 2 m"),("Lati aperti","Uno o due"),("Persone nello stand","Due o tre persone dello staff"),("Soluzioni adatte","Preallestito personalizzato, modulare, tessuto teso"),("Montaggio","Mezza giornata o meno")],
 sections=[
  ('t','come',"4 × 3 o 6 × 2: due stand diversi",None,[
    "Un 4 × 3 è quasi quadrato: si lavora in profondità, con la parete di fondo che fa da quinta e una piccola zona incontri in un angolo. Un 6 × 2 è una vetrina lunga e stretta: niente zona incontri seduti, ma un fronte di sei metri sul corridoio che, se ben illuminato, si vede da lontano.",
    "In entrambi i casi conviene decidere subito cosa deve succedere nello stand: mostrare prodotti, fare demo, raccogliere contatti o chiudere ordini. La risposta decide se servono mensole, uno schermo, un tavolo o un banco con vano chiuso."],None),
  ('t','cosa',"Cosa ci sta in 12 metri quadri",None,[],[
    ("Banco con vano chiuso.","Accoglienza e deposito brochure, campioni e borse."),
    ("Una piccola zona incontri.","Un tavolino con due o tre sedie in un angolo, nel 4 × 3."),
    ("Parete grafica e mensole luminose.","Il marchio in alto, i prodotti all'altezza degli occhi."),
    ("Uno schermo o un ledwall piccolo.","Per prodotti grandi o servizi da spiegare."),
    ("Un ripostiglio da 1 mq.","Possibile nel 4 × 3 senza sacrificare troppo.")]),
  ('c','layout',"Tre layout che funzionano",None,[
    ("Vetrina lunga (6 × 2)","Mensole luminose lungo tutto il fondo, banco piccolo a un'estremità, marchio ripetuto in alto."),
    ("Due zone (4 × 3)","Parete grafica e banco sul fronte, tavolino con sedie nell'angolo di fondo, ripostiglio sull'altro lato."),
    ("Demo","Banco dimostrativo al centro del fronte, schermo alle spalle, prodotti su mensole laterali.")]),
  ('t','errori',"Errori da evitare",None,[],[
    ("Mettere un tavolo in un 6 × 2.","Blocca il passaggio e nasconde la vetrina: meglio un tavolino alto."),
    ("Dimenticare l'altezza.","Il marchio deve stare sopra le teste dei visitatori, non dietro di loro."),
    ("Arredi a caso.","Arredi del catalogo standard rendono lo stand uguale a tutti gli altri."),
    ("Prese nel posto sbagliato.","Schermi, luci e frigoriferi vanno decisi prima, per mettere le prese dove servono.")]),
 ],
 qa=[("Per 12 mq conviene il noleggio o l'acquisto?","Per una o due fiere l'anno il noleggio. Se esponi spesso, uno stand modulare di proprietà, conservato nel nostro magazzino, costa meno nel tempo."),
  ("Si può fare una zona incontri in 12 mq?","Sì nel 4 × 3, con un tavolino e due o tre sedie in un angolo. Nel 6 × 2 meglio un tavolino alto con sgabelli."),
  ("Fate anche la grafica?","Sì, impaginiamo e stampiamo grafiche su tessuto, pannelli e lightbox, nelle misure esatte dello stand."),
  ("Quanto costa uno stand di 12 mq?","Dipende da struttura, finiture, arredi, impianti e fiera: ti mandiamo un preventivo gratuito voce per voce.")]),

dict(mq=16, slug="stand-16-mq", dims="4 × 4 m", render="stand-preallestito-personalizzato",
 title="Stand 16 mq (4×4): layout, idee e allestimento | Danova Tech",
 desc="Stand fieristico di 16 mq (4×4 m): layout, zona incontri, ripostiglio, grafica e luci, ad angolo o in linea. Preallestito, modulare o su misura, con montaggio in fiera.",
 h1='Stand 16 mq: <span class="grad">la metratura più richiesta</span> nelle fiere.',
 lead="Sedici metri quadri, di solito un quadrato di 4 × 4 metri, sono la metratura più comune per le aziende che espongono con regolarità. Bastano per avere un'immagine forte, una piccola zona incontri e un ripostiglio, soprattutto se lo spazio è ad angolo, con due lati aperti.",
 rows=[("Misure tipiche","4 × 4 m"),("Lati aperti","Uno (in linea) o due (ad angolo)"),("Persone nello stand","Tre persone dello staff"),("Soluzioni adatte","Preallestito personalizzato, modulare, su misura leggero"),("Montaggio","Mezza giornata – una giornata")],
 sections=[
  ('t','come',"Come si organizza uno stand di 16 mq",None,[
    "Con 4 × 4 metri si possono avere tre zone: un fronte per attirare (prodotto, schermo, grafica forte), una zona incontri per due o tre persone e un ripostiglio di circa un metro quadro. Se lo spazio è ad angolo, il secondo lato aperto raddoppia la visibilità e permette di mettere il marchio su due corridoi.",
    "È anche la metratura in cui uno stand modulare di proprietà comincia a convenire: la stessa struttura si monta come 16 mq ad angolo, come 12 mq in linea o come parte di uno stand più grande, cambiando solo grafiche e configurazione."],None),
  ('t','cosa',"Cosa ci sta in 16 metri quadri",None,[],[
    ("Banco reception.","Sul lato del corridoio principale, mai al centro del fronte."),
    ("Zona incontri.","Un tavolo con tre sedie o due tavolini alti."),
    ("Ripostiglio.","Circa 1 × 1 m con porta, per borse, scatole e cappotti."),
    ("Esposizione.","Mensole luminose, vetrine o un podio per il prodotto principale."),
    ("Schermo o ledwall.","Sulla parete più visibile dal corridoio.")]),
  ('c','layout',"Tre layout che funzionano",None,[
    ("Angolo aperto","Marchio su due lati, banco sull'angolo, zona incontri sul fondo, ripostiglio nell'angolo cieco."),
    ("In linea con quinta","Parete di fondo con ripostiglio integrato, prodotto al centro, banco su un lato, tavolo sull'altro."),
    ("Prodotto protagonista","Podio o pedana per un macchinario o un prodotto grande, grafica di fondo, tavolino alto per le domande.")]),
  ('t','errori',"Errori da evitare",None,[],[
    ("Riempire tutto.","Tre zone chiare funzionano meglio di cinque zone piccole."),
    ("Ripostiglio sul lato aperto.","Toglie visibilità: va sul lato cieco o sul fondo."),
    ("Zona incontri in vista.","Se possibile, separala con una quinta o una tenda leggera."),
    ("Grafica uguale su tutti i lati.","Ogni lato ha un pubblico diverso: adatta messaggi e altezze.")]),
 ],
 qa=[("Uno stand di 16 mq ad angolo vale la differenza?","Spesso sì: con due lati aperti lo stand si vede da due corridoi e si entra più facilmente. Se la fiera lo permette, è uno dei miglioramenti più efficaci."),
  ("Posso riusare lo stand di 16 mq in fiere con spazi diversi?","Sì, se è modulare: lo configuriamo per metrature e lati aperti diversi e lo conserviamo nel nostro magazzino fra una fiera e l'altra."),
  ("Fate stand su misura anche da 16 mq?","Sì, anche in legno e con finiture particolari: su questa metratura il su misura è spesso il modo per distinguersi."),
  ("Quanto costa uno stand di 16 mq?","Dipende da struttura, finiture, impianti, arredi e logistica. Ti mandiamo un preventivo gratuito voce per voce.")]),

dict(mq=24, slug="stand-24-mq", dims="6 × 4 m o 8 × 3 m", render="stand-ad-angolo-penisola",
 title="Stand 24 mq: layout, zona incontri e allestimento | Danova Tech",
 desc="Stand fieristico di 24 mq (6×4 o 8×3 m): come dividere lo spazio fra esposizione, incontri e magazzino, ad angolo o a penisola. Progetto 3D e montaggio in fiera.",
 h1='Stand 24 mq: <span class="grad">esposizione, incontri e magazzino</span> nello stesso spazio.',
 lead="Con ventiquattro metri quadri lo stand smette di essere una vetrina e diventa un piccolo ufficio commerciale: c'è posto per esporre, per far sedere i clienti e per un vero magazzino. Le misure più comuni sono 6 × 4 metri o 8 × 3 metri, in linea, ad angolo o a penisola.",
 rows=[("Misure tipiche","6 × 4 m oppure 8 × 3 m"),("Lati aperti","Da uno a tre"),("Persone nello stand","Tre o quattro persone dello staff"),("Soluzioni adatte","Modulare, tessuto teso, su misura"),("Montaggio","Una giornata circa")],
 sections=[
  ('t','come',"Come si organizza uno stand di 24 mq",None,[
    "Una divisione che funziona quasi sempre: circa metà dello spazio per l'esposizione e l'accoglienza sul lato del corridoio, un terzo per la zona incontri e il resto per il magazzino. Con un 8 × 3 la sequenza è orizzontale, da un'estremità all'altra; con un 6 × 4 si lavora in profondità, con la zona incontri sul fondo.",
    "A questa metratura conviene già pensare a un elemento in altezza: un fascione sospeso, una torre in tessuto retroilluminato o una parete più alta (dove il regolamento lo consente) che faccia riconoscere lo stand da lontano."],None),
  ('t','cosa',"Cosa ci sta in 24 metri quadri",None,[],[
    ("Banco reception e desk demo.","Accoglienza e dimostrazioni veloci sul fronte."),
    ("Zona incontri per 4–6 persone.","Un tavolo con sedie o un salottino, anche separato da una quinta."),
    ("Magazzino di 2 mq.","Con porta, mensole e appendiabiti."),
    ("Esposizione.","Vetrine, mensole, podi o una parete attrezzata."),
    ("Ledwall o schermi.","Per video e presentazioni.")]),
  ('c','layout',"Tre layout che funzionano",None,[
    ("Penisola","Tre lati aperti, magazzino sul lato chiuso, prodotti in giro, banco sull'angolo più trafficato."),
    ("Ufficio in fondo","Fronte espositivo, zona incontri chiusa sul fondo con parete grafica, magazzino in un angolo."),
    ("Vetrina lunga (8 × 3)","Esposizione su tutto il fronte, banco centrale, incontri e magazzino alle estremità.")]),
  ('t','errori',"Errori da evitare",None,[],[
    ("Zona incontri all'ingresso.","Le persone sedute bloccano chi vuole entrare."),
    ("Nessun elemento in alto.","A 24 mq lo stand deve farsi vedere sopra le teste."),
    ("Potenza elettrica sottostimata.","Ledwall, luci e frigoriferi sommati superano facilmente l'allaccio minimo."),
    ("Magazzino troppo piccolo.","Tre giorni di fiera producono più scatole di quanto si pensi.")]),
 ],
 qa=[("È meglio un 6 × 4 o un 8 × 3?","Dipende dalla fiera e dal prodotto: l'8 × 3 ha più fronte sul corridoio, il 6 × 4 più profondità per una zona incontri riservata. Ti aiutiamo a scegliere quando prenoti lo spazio."),
  ("Si può fare un ufficio chiuso in 24 mq?","Sì, una piccola sala per 4 persone con parete grafica e porta, se lo spazio non è troppo stretto."),
  ("Uno stand di 24 mq si può riusare?","Sì, se è modulare o in tessuto teso: lo riconfiguriamo per altre metrature e lo conserviamo in magazzino."),
  ("Quanto costa uno stand di 24 mq?","Dipende da struttura, finiture, impianti, arredi e logistica. Ti mandiamo un preventivo gratuito voce per voce.")]),

dict(mq=32, slug="stand-32-mq", dims="8 × 4 m", render="stand-medio-32-mq",
 title="Stand 32 mq: layout, idee e allestimento in fiera | Danova Tech",
 desc="Stand fieristico di 32 mq (8×4 m): esposizione, sala incontri, magazzino e grafica, ad angolo o a penisola. Progetto 3D, materiali, impianti e montaggio in fiera.",
 h1='Stand 32 mq: <span class="grad">lo spazio di un piccolo showroom.</span>',
 lead="Trentadue metri quadri, di solito 8 × 4 metri, sono la metratura in cui lo stand può diventare un vero showroom: un'area espositiva ampia, una sala incontri separata, un magazzino comodo e un elemento architettonico che si vede da lontano.",
 rows=[("Misure tipiche","8 × 4 m"),("Lati aperti","Da uno a tre"),("Persone nello stand","Quattro o cinque persone dello staff"),("Soluzioni adatte","Modulare, su misura in legno, misto"),("Montaggio","Una o due giornate")],
 sections=[
  ('t','come',"Come si organizza uno stand di 32 mq",None,[
    "Con 8 × 4 metri lo spazio si può dividere in tre ambienti veri: un'area espositiva aperta sul corridoio, una sala incontri chiusa o semi-chiusa e un magazzino di due o tre metri quadri. La sala incontri può stare sul fondo, separata da una parete grafica che è anche lo sfondo dell'esposizione.",
    "È anche la metratura in cui si nota la differenza fra uno stand modulare ben fatto e uno su misura: finiture in legno, controsoffitti, pareti curve e illuminazione progettata trasformano lo stand in un ambiente. La scelta dipende da quante volte lo usi e da quanto deve somigliare al tuo marchio."],None),
  ('t','cosa',"Cosa ci sta in 32 metri quadri",None,[],[
    ("Area espositiva ampia.","Prodotti su podi, vetrine o pareti attrezzate, con percorsi comodi."),
    ("Sala incontri per 4–6 persone.","Chiusa da pareti e porta, o semi-chiusa con quinte."),
    ("Magazzino di 2–3 mq.","Con mensole, appendiabiti e, se serve, frigorifero."),
    ("Banco reception e desk demo.","Sul lato del corridoio principale."),
    ("Elemento in altezza.","Fascione sospeso, torre luminosa o parete alta con il marchio.")]),
  ('c','layout',"Tre layout che funzionano",None,[
    ("Showroom e sala","Esposizione aperta sul fronte, sala incontri chiusa sul fondo, magazzino integrato nella parete."),
    ("Penisola aperta","Tre lati aperti, isole espositive, una quinta centrale con magazzino e schermo."),
    ("Bar e incontri","Per food e beverage: banco assaggio sul fronte, tavoli alti, retro attrezzato con lavello e frigoriferi.")]),
  ('t','errori',"Errori da evitare",None,[],[
    ("Sala incontri senza luce.","Una stanza chiusa senza illuminazione propria diventa un ripostiglio."),
    ("Percorsi stretti.","Lascia almeno un metro e venti fra gli elementi espositivi."),
    ("Grafica fatta per il catalogo.","Le grafiche vanno impaginate per essere lette a distanza."),
    ("Pratiche dell'ente fiera in ritardo.","Su 32 mq con pareti alte e controsoffitti il progetto va spesso approvato.")]),
 ],
 qa=[("Su 32 mq conviene il su misura?","Se l'immagine del marchio conta molto e la fiera è importante, sì. Se esponi in tante fiere diverse, un modulare di qualità con grafiche in tessuto è più flessibile. Spesso la soluzione è mista."),
  ("Potete fare una sala incontri chiusa?","Sì, con pareti, porta, controsoffitto e luce propria, nel rispetto del regolamento tecnico della fiera."),
  ("Conservate lo stand fra una fiera e l'altra?","Sì, nel nostro magazzino, e lo riportiamo in fiera con le grafiche aggiornate."),
  ("Quanto costa uno stand di 32 mq?","Dipende da struttura, finiture, impianti, arredi e logistica. Nella <a href=\"/quanto-costa-uno-stand-fieristico/\">guida ai costi</a> trovi le voci; il preventivo è gratuito.")]),

dict(mq=48, slug="stand-48-mq", dims="8 × 6 m o 12 × 4 m", render="stand-a-isola-quattro-lati",
 title="Stand 48 mq: layout a penisola o a isola, allestimento | Danova Tech",
 desc="Stand fieristico di 48 mq (8×6 o 12×4 m): layout a penisola o a isola, sale incontri, bar, magazzino, ledwall e strutture sospese. Progetto 3D e montaggio in fiera.",
 h1='Stand 48 mq: <span class="grad">un ambiente da vivere</span>, non solo da guardare.',
 lead="Con quarantotto metri quadri lo stand diventa un luogo: si entra, ci si siede, si beve un caffè, si guarda una demo. Le misure più comuni sono 8 × 6 o 12 × 4 metri, spesso a penisola o a isola, e permettono strutture sospese, ledwall e sale incontri vere.",
 rows=[("Misure tipiche","8 × 6 m oppure 12 × 4 m"),("Lati aperti","Tre (penisola) o quattro (isola)"),("Persone nello stand","Cinque–otto persone dello staff"),("Soluzioni adatte","Su misura, modulare di grandi dimensioni, misto"),("Montaggio","Due giornate circa")],
 sections=[
  ('t','come',"Come si organizza uno stand di 48 mq",None,[
    "Su 48 mq si progetta per funzioni: accoglienza, esposizione, demo, incontri, ospitalità e magazzino. Un nucleo centrale o laterale chiuso (magazzino, sala incontri, retro del bar) libera il resto dello spazio, che resta aperto e attraversabile dai corridoi.",
    "A questa scala contano molto gli elementi in altezza: strutture sospese in tessuto (dove la fiera le consente, montate dai rigger autorizzati), torri luminose, ledwall. Sono loro a far riconoscere lo stand da un capo all'altro del padiglione."],None),
  ('t','cosa',"Cosa ci sta in 48 metri quadri",None,[],[
    ("Una o due sale incontri.","Per 4–6 persone, chiuse o semi-chiuse."),
    ("Bar o area ospitalità.","Banco caffè, frigorifero, lavello se l'allaccio idrico è disponibile."),
    ("Area demo con ledwall.","Per presentazioni e prodotti in funzione."),
    ("Magazzino di 3–4 mq.","Con mensole, appendiabiti e frigorifero."),
    ("Esposizione su più lati.","Ogni lato aperto ha la sua vetrina.")]),
  ('c','layout',"Tre layout che funzionano",None,[
    ("Nucleo centrale","Magazzino e sala incontri al centro, esposizione e accoglienza tutt'intorno, marchio sospeso sopra."),
    ("Penisola con lounge","Lato chiuso con sala e bar, area aperta con prodotti e demo verso i tre corridoi."),
    ("Showroom lineare (12 × 4)","Esposizione lungo tutto il fronte, sala incontri e magazzino in fondo a un'estremità.")]),
  ('t','errori',"Errori da evitare",None,[],[
    ("Chiudere i lati aperti.","Pareti piene su un'isola sprecano la visibilità che hai pagato."),
    ("Dimenticare il regolamento.","Altezze, strutture sospese e pareti verso i vicini hanno regole precise."),
    ("Staff insufficiente.","Uno stand grande vuoto di persone sembra chiuso."),
    ("Progetto approvato tardi.","Strutture alte e sospese richiedono approvazioni con settimane di anticipo.")]),
 ],
 qa=[("Si possono appendere strutture al soffitto del padiglione?","Dipende dalla fiera: dove è consentito, le strutture sospese si montano tramite i rigger autorizzati dall'ente fiera, su richiesta e con un progetto approvato. Ce ne occupiamo noi."),
  ("Fate stand a isola da 48 mq?","Sì, su misura o con sistemi modulari di grandi dimensioni, con montatori partner gestiti da noi e laboratori di fiducia per strutture e arredi."),
  ("Potete fare un bar nello stand?","Sì: banco, retro, frigoriferi e, se la fiera lo consente, allaccio idrico e scarico."),
  ("Quanto costa uno stand di 48 mq?","Dipende da struttura, finiture, impianti, arredi e logistica. Ti mandiamo un preventivo gratuito voce per voce.")]),

dict(mq=100, slug="stand-100-mq", dims="10 × 10 m e oltre", render="stand-isola-legno-rovere",
 title="Stand 100 mq e oltre: stand grandi a isola e a due piani | Danova Tech",
 desc="Stand fieristici da 100 mq a oltre 300 mq: isole, stand a due piani, strutture sospese, ledwall e sale riunioni. Montatori partner gestiti da noi, magazzino e laboratori di fiducia.",
 h1='Stand da 100 mq e oltre: <span class="grad">isole, due piani, grandi spazi.</span>',
 lead="Da cento metri quadri in su lo stand è un progetto di architettura temporanea: isole su quattro lati, stand a due piani, strutture sospese, ledwall, bar e sale riunioni. Realizziamo stand anche oltre i 300 metri quadri, con montatori partner gestiti da noi, magazzino e laboratori di fiducia per strutture e arredi in legno.",
 rows=[("Misure tipiche","10 × 10 m, 12 × 10 m, fino a oltre 300 mq"),("Lati aperti","Di solito quattro (isola)"),("Soluzioni adatte","Su misura, sistemi modulari di grandi dimensioni, due piani"),("Squadre","Squadre di montaggio coordinate da un unico capocantiere"),("Montaggio","Da due giorni a una settimana, secondo progetto e fiera")],
 sections=[
  ('t','come',"Come si progetta uno stand grande",None,[
    "Su un'isola grande si parte dai flussi: da dove arrivano i visitatori, dove si fermano, dove si siedono i clienti importanti, dove passa lo staff con il materiale. Il progetto mette al centro i volumi chiusi (magazzini, sale riunioni, cucina del bar) e lascia aperti i fronti sui corridoi.",
    "Lo stand a due piani raddoppia la superficie utile: sale riunioni e lounge al piano superiore, esposizione libera al piano terra. Richiede un calcolo strutturale firmato e l'approvazione dell'ente fiera, e tempi di montaggio più lunghi. Lo progettiamo e lo realizziamo noi, dalle strutture alle finiture."],None),
  ('s','numeri',"Come lavoriamo sugli stand grandi",[("Progetto","Render 3D, esecutivi, calcoli strutturali per due piani e strutture sospese"),("Produzione","Interna: strutture e arredi in legno, dalla A alla Z"),("Montaggio","Squadre nostre con capocantiere, partner per i picchi di lavoro"),("Magazzino","Nostro: lo stand si conserva e si riusa nelle edizioni successive"),("Pratiche","Progetto, impianti, dichiarazione di conformità, certificati dei materiali")],None),
  ('t','cosa',"Cosa può avere uno stand da 100 mq in su",None,[],[
    ("Secondo piano.","Sale riunioni, lounge e terrazza affacciata sul padiglione."),
    ("Strutture sospese.","Anelli, cubi e fascioni in tessuto retroilluminato, montati tramite i rigger autorizzati."),
    ("Ledwall di grandi dimensioni.","Con regia dei contenuti e impianto dimensionato."),
    ("Bar e cucina.","Per l'ospitalità di clienti e distributori, con allacci idrici dove disponibili."),
    ("Più aree di prodotto.","Isole tematiche per linee o mercati diversi.")]),
  ('t','errori',"Errori da evitare",None,[],[
    ("Partire tardi.","Su un'isola grande o a due piani servono mesi: progetto, approvazioni, produzione."),
    ("Sottovalutare l'impianto.","Ledwall, luci, bar e macchine richiedono potenze importanti e un quadro ben progettato."),
    ("Non pensare al riuso.","Uno stand grande progettato per essere riusato abbatte i costi delle edizioni successive."),
    ("Troppi fornitori.","Un solo referente per progetto, produzione, montaggio e pratiche evita buchi e rimpalli.")]),
 ],
 qa=[("Realizzate stand oltre i 300 mq?","Sì, con montatori e laboratori partner coordinati da un unico referente."),
  ("Fate stand a due piani?","Sì, li progettiamo e realizziamo con calcolo strutturale, pratiche con l'ente fiera e montaggio. Vedi anche <a href=\"/stand-a-due-piani/\">stand a due piani</a>."),
  ("Conservate gli stand grandi fra una fiera e l'altra?","Sì, nel nostro magazzino: strutture, arredi e grafiche si controllano e si riportano in fiera alla prossima edizione."),
  ("Quanto costa uno stand da 100 mq?","Dipende da struttura, finiture, impianti, arredi, logistica e fiera. Ti mandiamo un preventivo gratuito voce per voce.")]),
]

# ------------------------------------------------------------------ GUIDE
G = [
dict(slug="regolamento-tecnico-fiera", render="progettazione-stand-render-3d",
 title="Regolamento tecnico fiera: cosa dice e cosa controllare | Danova Tech",
 desc="Il regolamento tecnico di una fiera spiegato: altezze, distanze, stand a due piani, strutture sospese, materiali, impianti, scadenze e approvazioni. Cosa controllare.",
 h1='Regolamento tecnico della fiera: <span class="grad">cosa dice e cosa controllare</span> prima di progettare.',
 lead="Ogni fiera pubblica un regolamento tecnico per gli allestimenti: è il documento che decide quanto può essere alto lo stand, come devono essere le pareti verso i vicini, quali materiali si possono usare e quali documenti servono per l'impianto elettrico. Leggerlo prima di progettare evita modifiche costose e sorprese il primo giorno di allestimento.",
 sections=[
  ('t','cos-e',"Che cos'è il regolamento tecnico",None,[
   "Il regolamento tecnico (a volte chiamato regolamento allestimenti, manuale dell'espositore o technical guidelines) è il documento con cui l'ente fiera fissa le regole per costruire gli stand nei suoi padiglioni. Si trova nell'area riservata agli espositori, insieme ai moduli per ordinare i servizi.",
   "Ogni quartiere fieristico ha il suo, e a volte la singola manifestazione aggiunge regole proprie. Per questo non basta aver fatto una fiera: Milano, Bologna, Verona e Rimini hanno regole diverse su altezze, strutture sospese e scadenze."],None),
  ('t','cosa-dice',"Le regole che contano di più",None,[],[
   ("Altezze massime.","Altezza massima delle pareti e delle strutture, spesso diversa per stand in linea, ad angolo e a isola, e per gli elementi arretrati dal confine."),
   ("Pareti verso i vicini.","Le pareti confinanti con altri stand vanno di solito rifinite in modo neutro, senza grafiche, sopra una certa altezza."),
   ("Lati aperti.","Percentuale minima di fronte libero sui corridoi, soprattutto per gli stand a isola."),
   ("Stand a due piani.","Ammessi solo in alcune aree, con progetto e calcolo strutturale firmati da un tecnico abilitato e approvazione preventiva."),
   ("Strutture sospese.","Appese al soffitto del padiglione solo tramite i rigger autorizzati dall'ente fiera, su richiesta."),
   ("Materiali.","Reazione al fuoco certificata per pannelli, tessuti, moquette e decorazioni."),
   ("Impianto elettrico.","Realizzato da impresa abilitata, con dichiarazione di conformità consegnata prima dell'allaccio."),
   ("Orari e accessi.","Giorni e orari di allestimento e smontaggio, accesso dei mezzi, pass per il personale.")]),
  ('p','scadenze',"Scadenze","Le date da segnare <span class=\"grad\">appena prenoti lo spazio.</span>",[
   ("Invio del progetto","Per stand alti, a due piani o con strutture sospese, spesso 1–2 mesi prima della fiera."),
   ("Ordine dei servizi","Potenza elettrica, acqua, internet, pulizie, appendimenti: ogni servizio ha la sua scadenza, dopo la quale costa di più."),
   ("Pass e personale","Nominativi dei montatori e documenti di sicurezza richiesti."),
   ("Documenti finali","Dichiarazione di conformità dell'impianto e certificati dei materiali, da tenere nello stand.")]),
  ('t','controllo',"Cosa controlliamo noi",None,[
   "Quando progettiamo uno stand leggiamo il regolamento della fiera specifica, verifichiamo altezze, distanze e materiali sul progetto, prepariamo i disegni e i documenti da inviare all'ente fiera e ordiniamo i servizi nei tempi giusti. Se il progetto lo richiede, il calcolo strutturale per stand a due piani o elementi alti viene firmato da un tecnico abilitato.",
   "Se hai già un progetto fatto da un altro studio o dalla tua sede all'estero, lo verifichiamo sul regolamento italiano e proponiamo modifiche solo dove servono."],None),
 ],
 qa=[("Dove trovo il regolamento tecnico della fiera?","Nell'area riservata espositori del sito della manifestazione, insieme al manuale dell'espositore e ai moduli dei servizi. Se non lo trovi, chiedilo all'organizzatore o mandaci il nome della fiera."),
  ("Il regolamento è uguale in tutte le fiere?","No. Ogni quartiere fieristico ha il suo e alcune manifestazioni aggiungono regole proprie su altezze, strutture sospese e scadenze."),
  ("Chi presenta il progetto all'ente fiera?","Possiamo farlo noi per te, con disegni, relazioni e documenti richiesti."),
  ("Cosa succede se lo stand non rispetta il regolamento?","L'ente fiera può chiedere modifiche, anche durante l'allestimento, o non autorizzare l'allaccio elettrico. Per questo conviene verificare tutto in fase di progetto.")],
 rel=[("Dichiarazione di conformità dello stand","/guide/dichiarazione-di-conformita-stand/"),("Materiali ignifughi per stand","/guide/materiali-ignifughi-stand/"),("Stand a due piani","/stand-a-due-piani/"),("Progettazione stand","/progettazione-stand-fieristici/"),("Come preparare una fiera","/guide/come-preparare-una-fiera/")]),

dict(slug="dichiarazione-di-conformita-stand", render="ledwall-illuminazione-stand",
 title="Dichiarazione di conformità impianto elettrico stand | Danova Tech",
 desc="Dichiarazione di conformità dell'impianto elettrico dello stand: cos'è, chi la firma (DM 37/2008), quando serve e come evitare problemi all'allaccio in fiera.",
 h1='Dichiarazione di conformità dello stand: <span class="grad">senza, la corrente non arriva.</span>',
 lead="In tutte le fiere italiane l'impianto elettrico dello stand deve essere realizzato da un'impresa abilitata, che rilascia la dichiarazione di conformità prevista dal Decreto ministeriale 37/2008. È il documento che l'ente fiera chiede prima di dare corrente allo stand: se manca o è incompleto, lo stand resta al buio.",
 sections=[
  ('t','cos-e',"Che cos'è",None,[
   "La dichiarazione di conformità è il documento con cui l'impresa installatrice attesta di aver realizzato l'impianto a regola d'arte, secondo le norme tecniche e il progetto. Per gli stand fieristici riguarda il quadro elettrico, le linee, le prese, l'illuminazione e tutti gli apparecchi collegati in modo fisso.",
   "La firma solo un'impresa abilitata per gli impianti elettrici. Non può firmarla l'espositore, né un elettricista non abilitato, né il fornitore dello stand se non ha i requisiti."],None),
  ('t','cosa-serve',"Cosa serve, in pratica",None,[],[
   ("Impresa abilitata.","L'impianto dello stand va realizzato da un'impresa con i requisiti tecnico-professionali previsti dalla legge."),
   ("Potenza richiesta all'ente fiera.","Prima di tutto si calcola la potenza necessaria (luci, schermi, ledwall, frigoriferi, macchine) e la si ordina entro la scadenza."),
   ("Schema e materiali.","Allo schema dell'impianto si accompagnano, quando richiesti, i riferimenti ai materiali usati."),
   ("Consegna prima dell'allaccio.","Il documento si consegna all'ente fiera secondo le sue procedure, di solito entro l'ultimo giorno di allestimento."),
   ("Copia nello stand.","Conviene tenerne una copia nello stand per eventuali controlli.")]),
  ('t','errori',"Gli errori più comuni",None,[],[
   ("Potenza sottostimata.","Ledwall, faretti, macchine da caffè e frigoriferi sommati superano facilmente l'allaccio base: il salvavita scatta il primo giorno."),
   ("Apparecchi aggiunti all'ultimo.","Uno schermo o un frigorifero portato in fiera all'ultimo momento può non essere previsto dall'impianto."),
   ("Prolunghe e ciabatte.","Le multiprese volanti sono spesso vietate o limitate dal regolamento."),
   ("Documenti consegnati tardi.","Senza il documento consegnato nei tempi, l'allaccio può slittare.")]),
  ('t','noi',"Come lo gestiamo noi",None,[
   "Negli stand che allestiamo l'impianto elettrico fa parte del progetto: calcoliamo la potenza dalle schede tecniche degli apparecchi, la ordiniamo all'ente fiera, realizziamo l'impianto e consegniamo la dichiarazione di conformità nei tempi richiesti. Per gli espositori esteri è uno dei passaggi che crea più dubbi, e lo risolviamo noi."],None),
 ],
 qa=[("Chi firma la dichiarazione di conformità dello stand?","Un'impresa abilitata agli impianti elettrici, che ha realizzato l'impianto. Negli stand che allestiamo ce ne occupiamo noi."),
  ("Serve anche per uno stand preallestito?","Per il preallestito fornito dall'ente fiera l'impianto base è già coperto dall'organizzatore. Se aggiungi luci o apparecchi, le regole cambiano: controlla il regolamento o chiedici."),
  ("Quanta potenza devo richiedere?","Si calcola sommando le potenze di tutti gli apparecchi, con un margine. Ti serve l'elenco di luci, schermi e macchine: il calcolo lo facciamo noi."),
  ("Un espositore straniero può usare il proprio elettricista?","Solo se rispetta i requisiti previsti in Italia e il regolamento della fiera. Di solito è più semplice affidarsi a un'impresa italiana abilitata.")],
 rel=[("Regolamento tecnico della fiera","/guide/regolamento-tecnico-fiera/"),("Ledwall e illuminazione stand","/ledwall-e-illuminazione-stand/"),("Montaggio stand","/montaggio-stand-fieristici/"),("Materiali ignifughi per stand","/guide/materiali-ignifughi-stand/")]),

dict(slug="materiali-ignifughi-stand", render="grafica-stand-tessuto-stampato",
 title="Materiali ignifughi per stand: classe di reazione al fuoco | Danova Tech",
 desc="Materiali ignifughi per stand: classe di reazione al fuoco di pannelli, tessuti, moquette e decorazioni, certificati richiesti e cosa chiede la fiera.",
 h1='Materiali ignifughi per stand: <span class="grad">cosa chiede la fiera</span> e quali certificati servono.',
 lead="Pannelli, tessuti, moquette, tende e decorazioni di uno stand devono avere una reazione al fuoco certificata, secondo quanto chiede il regolamento tecnico della fiera. È una regola di sicurezza che viene controllata davvero: un materiale senza certificato può essere fatto togliere dallo stand.",
 sections=[
  ('t','cos-e',"Cosa significa reazione al fuoco",None,[
   "La reazione al fuoco indica come un materiale contribuisce a un incendio: quanto facilmente si accende, quanto fumo produce, se gocciola. In Italia si usano le classi italiane (da 0 a 5, dove la classe 0 è incombustibile e la classe 1 è quella richiesta più spesso negli allestimenti) e le classi europee equivalenti.",
   "Il regolamento della singola fiera indica la classe minima per ciascun tipo di materiale. Spesso è la classe 1 o la classe europea corrispondente, ma ci sono differenze fra quartieri fieristici e fra tipi di materiale, per esempio fra pareti, pavimenti e tessuti sospesi."],None),
  ('t','materiali',"Materiale per materiale",None,[],[
   ("Pannelli e pareti.","Legno, MDF e pannelli compositi vanno usati nella versione certificata o trattati con prodotti omologati, con la relativa documentazione."),
   ("Tessuti e grafiche in tessuto.","Il tessuto stampato deve essere certificato per la reazione al fuoco: è uno dei punti più controllati."),
   ("Moquette e pavimenti.","Moquette, prati sintetici e rivestimenti a pavimento hanno classi specifiche."),
   ("Tende e controsoffitti.","Teli e velari sospesi sono spesso soggetti a requisiti più severi."),
   ("Decorazioni e allestimenti scenografici.","Piante finte, cartoni, materiali naturali: vanno verificati caso per caso.")]),
  ('t','certificati',"Certificati e documenti",None,[
   "Per ogni materiale soggetto a requisito serve il certificato di reazione al fuoco, con la dichiarazione che il materiale usato è quello certificato. Per i trattamenti ignifughi fatti in opera serve la documentazione del prodotto e del trattamento. I documenti vanno tenuti nello stand e mostrati in caso di controllo.",
   "Attenzione ai materiali comprati all'estero o online: un tessuto o un pannello senza certificazione riconosciuta in Italia o nell'Unione europea può essere rifiutato. È un problema frequente per gli espositori stranieri che portano lo stand dal proprio paese."],None),
 ],
 qa=[("Che classe di reazione al fuoco serve per uno stand?","La indica il regolamento tecnico della fiera per ciascun materiale; spesso è la classe 1 o la classe europea equivalente. Noi la verifichiamo sul regolamento della fiera specifica."),
  ("Le grafiche in tessuto devono essere ignifughe?","Sì, i tessuti stampati usati negli stand devono avere la reazione al fuoco richiesta, con certificato."),
  ("Posso portare uno stand costruito all'estero?","Sì, ma i materiali devono avere certificazioni riconosciute in Italia o nell'UE. Se mancano, possiamo sostituire i materiali non conformi."),
  ("Chi conserva i certificati?","Li prepariamo noi e li consegniamo per lo stand, insieme alla dichiarazione di conformità dell'impianto elettrico.")],
 rel=[("Regolamento tecnico della fiera","/guide/regolamento-tecnico-fiera/"),("Grafica per stand","/grafica-per-stand-fieristici/"),("Stand ecosostenibili","/stand-fieristici-ecosostenibili/"),("Dichiarazione di conformità dello stand","/guide/dichiarazione-di-conformita-stand/")]),

dict(slug="come-attirare-visitatori-allo-stand", render="stand-innovativo-led-interattivo",
 title="Come attirare visitatori allo stand in fiera: 12 idee | Danova Tech",
 desc="Come attirare visitatori allo stand: inviti prima della fiera, messaggio leggibile a distanza, luce, prodotto in azione, staff, demo e follow-up. 12 idee concrete.",
 h1='Come attirare visitatori allo stand: <span class="grad">12 idee che funzionano davvero.</span>',
 lead="Un visitatore passa davanti a uno stand in tre o quattro secondi. In quel tempo deve capire chi sei, cosa fai e perché dovrebbe fermarsi. Queste sono le idee che vediamo funzionare in fiera, dalla preparazione prima dell'apertura a come si comporta lo staff.",
 sections=[
  ('t','prima',"Prima della fiera",None,[],[
   ("1. Invita i clienti con un appuntamento.","Una mail personale due o tre settimane prima, con numero di padiglione e stand e un orario proposto, porta più persone di qualsiasi allestimento."),
   ("2. Usa i canali della fiera.","Catalogo online, app della manifestazione, comunicati: tieni aggiornato il profilo espositore con prodotti e novità."),
   ("3. Dai un motivo per venire.","Un prodotto nuovo, una demo, un ospite, un'offerta riservata ai visitatori della fiera.")]),
  ('t','stand',"Lo stand",None,[],[
   ("4. Un messaggio leggibile a dieci metri.","Il marchio in alto e una frase di cinque parole su cosa fai. Il resto è per chi entra."),
   ("5. La luce.","Uno stand più luminoso dei vicini si nota. Faretti sui prodotti, pareti retroilluminate, temperatura colore coerente."),
   ("6. Il prodotto in azione.","Una macchina che lavora, un prodotto da toccare, un assaggio: il movimento ferma le persone più delle immagini."),
   ("7. Uno schermo, senza audio.","Video brevi, leggibili senza sonoro, che spiegano in trenta secondi cosa fa il prodotto."),
   ("8. Un ingresso libero.","Niente banco messo di traverso sul fronte: le persone entrano se lo spazio è aperto.")]),
  ('t','staff',"Lo staff",None,[],[
   ("9. In piedi e sul bordo.","Lo staff seduto o al telefono è il motivo più comune per cui uno stand resta vuoto."),
   ("10. Una domanda aperta.","Meglio 'Su cosa state lavorando?' che 'Posso aiutarla?'."),
   ("11. Ruoli chiari.","Chi accoglie, chi fa le demo, chi chiude gli incontri: ognuno sa cosa fare.")]),
  ('t','dopo',"Dopo il primo contatto",None,[],[
   ("12. Raccogli il contatto con una nota.","Un contatto senza nota è un biglietto da visita perso. Annota cosa cerca e quando richiamarlo. Vedi la guida su <a href=\"/guide/come-raccogliere-contatti-in-fiera/\">come raccogliere contatti in fiera</a>.")]),
 ],
 qa=[("Cosa attira di più i visitatori in fiera?","Il prodotto in azione e uno staff attivo sul bordo dello stand. Luce e grafica servono a far notare lo stand; il resto lo fanno le persone."),
  ("I gadget servono?","Solo se legati al prodotto o utili. Il gadget generico attira persone che non sono clienti."),
  ("Uno stand piccolo può attirare quanto uno grande?","Sì, se ha un messaggio chiaro, buona luce e uno staff attento. Vedi le idee per lo <a href=\"/stand-9-mq/\">stand da 9 mq</a>."),
  ("Potete progettare lo stand per attirare più visitatori?","Sì: luce, grafiche leggibili a distanza, spazi aperti e punti demo sono parte del progetto.")],
 rel=[("Idee per stand fieristici","/idee-stand-fieristici/"),("Come raccogliere contatti in fiera","/guide/come-raccogliere-contatti-in-fiera/"),("Ledwall e illuminazione","/ledwall-e-illuminazione-stand/"),("Grafica per stand","/grafica-per-stand-fieristici/"),("Come preparare una fiera","/guide/come-preparare-una-fiera/")]),

dict(slug="come-raccogliere-contatti-in-fiera", render="espositori-desk-totem-fiera",
 title="Come raccogliere contatti in fiera (e non perderli dopo) | Danova Tech",
 desc="Come raccogliere contatti in fiera: scanner badge, moduli, QR code, note di qualificazione, privacy e follow-up entro una settimana. Metodo pratico per espositori.",
 h1='Come raccogliere contatti in fiera <span class="grad">e non perderli dopo.</span>',
 lead="La fiera finisce, e sulla scrivania restano un mucchio di biglietti da visita senza note. Il valore di una fiera si decide nei sette giorni dopo la chiusura, e dipende da come i contatti sono stati raccolti allo stand. Ecco un metodo semplice, che funziona anche per stand piccoli.",
 sections=[
  ('t','strumenti',"Gli strumenti",None,[],[
   ("Scanner dei badge.","Molte fiere offrono un'app o un lettore per scansionare il badge dei visitatori: veloce, con i dati già puliti."),
   ("Modulo sul tablet o sul telefono.","Un modulo breve, collegato al tuo CRM o a un foglio condiviso."),
   ("QR code nello stand.","Su banco, totem e brochure: porta a un modulo o a WhatsApp con un messaggio già scritto."),
   ("Biglietti da visita, ma con la nota.","Se li usi, scrivi subito sul retro cosa ha chiesto e quando richiamarlo.")]),
  ('t','qualifica',"Le quattro informazioni da annotare",None,[],[
   ("Chi è.","Azienda, ruolo, paese."),
   ("Cosa cerca.","Prodotto, quantità, tempi."),
   ("Quanto è caldo.","Caldo, tiepido, freddo: una lettera basta."),
   ("Cosa abbiamo promesso.","Listino, campione, visita, preventivo, e entro quando.")]),
  ('p','dopo',"Dopo la fiera","Il follow-up <span class=\"grad\">nei sette giorni dopo.</span>",[
   ("Giorno 1–2","Mail di ringraziamento personalizzata ai contatti caldi, con quanto promesso."),
   ("Giorno 3–5","Telefonata o messaggio ai contatti caldi senza risposta; mail ai tiepidi."),
   ("Giorno 7","Riepilogo: quanti contatti, quanti caldi, quante opportunità aperte."),
   ("Mese successivo","Newsletter o aggiornamento a tutti, nel rispetto del consenso raccolto.")]),
  ('t','privacy',"Privacy",None,[
   "Quando raccogli dati personali in fiera devi informare il visitatore su come li userai, come per qualsiasi altro canale. Un'informativa breve sul modulo e la possibilità di scegliere se ricevere comunicazioni commerciali sono il minimo. Per dubbi specifici, chiedi al tuo consulente privacy."],None),
 ],
 qa=[("Qual è il modo più veloce per raccogliere contatti allo stand?","Lo scanner dei badge offerto dalla fiera o un modulo su tablet. Il punto non è la velocità, ma annotare subito cosa cerca il visitatore."),
  ("Dove mettere il QR code nello stand?","Sul banco reception, su un totem vicino all'ingresso e sulle brochure: dove le persone si fermano."),
  ("Entro quanto bisogna ricontattare i contatti di una fiera?","Entro una settimana, i più caldi entro due giorni: dopo, il ricordo dello stand svanisce."),
  ("Potete integrare QR code e totem nello stand?","Sì, progettiamo totem, desk e grafiche con QR code; e, se ti serve, un modulo collegato al tuo CRM.")],
 rel=[("Come attirare visitatori allo stand","/guide/come-attirare-visitatori-allo-stand/"),("Espositori, desk e totem","/espositori-desk-totem-per-fiere/"),("CRM aziendale","/crm-aziendale/"),("Lead generation B2B","/lead-generation-b2b/"),("Come preparare una fiera","/guide/come-preparare-una-fiera/")]),

dict(slug="quanto-costa-partecipare-a-una-fiera", render="stand-fiera-estero-padiglione",
 title="Quanto costa partecipare a una fiera: tutte le voci | Danova Tech",
 desc="Quanto costa partecipare a una fiera: area espositiva, quota di iscrizione, stand, servizi tecnici, trasporto, viaggi e personale. Le voci e come ridurle, anche con i contributi.",
 h1='Quanto costa partecipare a una fiera: <span class="grad">tutte le voci</span>, non solo lo stand.',
 lead="Il costo di una fiera non è solo lo stand. Ci sono l'area espositiva, la quota di iscrizione, i servizi tecnici, il trasporto, i viaggi e il tempo del personale. Mettere in fila tutte le voci prima di firmare aiuta a scegliere la metratura giusta e a capire quanto deve rendere la fiera.",
 sections=[
  ('t','voci',"Le voci di costo",None,[],[
   ("Area espositiva.","Il prezzo al metro quadro dell'organizzatore, con maggiorazioni per angolo, penisola e isola."),
   ("Quota di iscrizione.","Iscrizione, inserimento nel catalogo, assicurazione e servizi obbligatori."),
   ("Stand.","Progetto, strutture, grafica, arredi, impianto elettrico, montaggio e smontaggio: la voce più variabile. Vedi <a href=\"/quanto-costa-uno-stand-fieristico/\">quanto costa uno stand</a>."),
   ("Servizi tecnici della fiera.","Potenza elettrica, acqua, internet, pulizie, appendimenti, parcheggi e pass."),
   ("Trasporto.","Merce e materiali da esporre, eventuale spedizioniere ufficiale e movimentazione in fiera."),
   ("Viaggi e alloggio.","Hotel, treni o voli, vitto per lo staff: nelle settimane delle grandi fiere i prezzi salgono."),
   ("Promozione.","Inviti, campagne, materiali stampati, gadget, eventi allo stand."),
   ("Tempo del personale.","Giorni di lavoro dello staff in fiera e nella preparazione.")]),
  ('t','ridurre',"Come ridurre i costi senza perdere efficacia",None,[],[
   ("Prenotare presto.","Area, hotel e squadre di montaggio costano meno e si scelgono meglio con anticipo."),
   ("Ordinare i servizi entro le scadenze.","Dopo la scadenza molti servizi della fiera costano di più."),
   ("Uno stand riutilizzabile.","Se esponi più volte, uno stand modulare di proprietà conservato in magazzino abbatte i costi delle fiere successive."),
   ("La metratura giusta.","Meglio 16 mq ben progettati che 32 mq vuoti."),
   ("Contributi.","Regioni, camere di commercio e programmi nazionali finanziano spesso la partecipazione a fiere internazionali: vedi <a href=\"/contributi-fiere-2026/\">contributi per le fiere</a>.")]),
  ('t','misurare',"Come capire se la fiera conviene",None,[
   "Prima della fiera fissa un obiettivo misurabile: numero di incontri, nuovi contatti qualificati, ordini, distributori. Dopo la fiera confronta il costo totale con i risultati, a sei e a dodici mesi, perché molte trattative nate in fiera si chiudono più tardi.",
   "Non pubblichiamo listini per gli stand perché ogni progetto è diverso: ti mandiamo un preventivo gratuito voce per voce, che ti aiuta a completare il budget della fiera."],None),
 ],
 qa=[("Qual è la voce di costo più alta in una fiera?","Di solito l'area espositiva e lo stand; per le fiere all'estero pesano molto anche viaggi e trasporto."),
  ("Esistono contributi per partecipare alle fiere?","Sì, da regioni, camere di commercio e programmi nazionali, soprattutto per le fiere internazionali. Trovi un riepilogo nella pagina sui <a href=\"/contributi-fiere-2026/\">contributi per le fiere</a>."),
  ("Conviene noleggiare o comprare lo stand?","Per una fiera singola il noleggio; per più fiere l'anno uno stand di proprietà, conservato nel nostro magazzino."),
  ("Potete aiutarmi a fare il budget della fiera?","Sì: ti mandiamo un preventivo dettagliato per lo stand e ti indichiamo i servizi della fiera da prevedere.")],
 rel=[("Quanto costa uno stand fieristico","/quanto-costa-uno-stand-fieristico/"),("Contributi per le fiere","/contributi-fiere-2026/"),("Noleggio stand","/noleggio-stand-fieristici/"),("Stand modulari","/stand-modulari/"),("Calendario fiere","/calendario-fiere/")]),

dict(slug="come-scegliere-un-allestitore-fieristico", render="montaggio-stand-in-fiera",
 title="Come scegliere un allestitore fieristico: 10 domande | Danova Tech",
 desc="Come scegliere un allestitore fieristico: 10 domande da fare prima di firmare su produzione, squadre, pratiche, impianti, magazzino e preventivo.",
 h1='Come scegliere un allestitore fieristico: <span class="grad">10 domande</span> da fare prima di firmare.',
 lead="Due preventivi per lo stesso stand possono sembrare simili e nascondere differenze enormi: chi produce davvero, chi monta, chi segue le pratiche con l'ente fiera, cosa succede se qualcosa va storto. Queste sono le domande che faremmo noi, se dovessimo scegliere un allestitore.",
 sections=[
  ('t','domande',"Le 10 domande",None,[],[
   ("1. Chi è il mio referente?","Una persona unica dal progetto allo smontaggio evita rimpalli fra fornitori."),
   ("2. Producete voi o subappaltate?","Strutture e arredi in legno prodotti internamente significano più controllo su qualità e tempi."),
   ("3. Le squadre di montaggio sono vostre?","Squadre proprie, coordinate da un capocantiere, rispondono meglio agli imprevisti dell'allestimento."),
   ("4. Chi segue le pratiche con l'ente fiera?","Progetto, approvazioni, servizi, pass: se non lo fa l'allestitore, lo devi fare tu."),
   ("5. Chi firma la dichiarazione di conformità?","L'impianto elettrico deve essere fatto da un'impresa abilitata."),
   ("6. I materiali sono certificati?","Reazione al fuoco richiesta dal regolamento, con certificati da tenere nello stand."),
   ("7. Il preventivo è voce per voce?","Progetto, strutture, grafica, arredi, impianti, trasporto, montaggio: ogni voce chiara, senza sorprese."),
   ("8. Lo stand è a noleggio o mio?","Se è tuo, dove viene conservato e quanto costa riportarlo in fiera?"),
   ("9. Avete già lavorato in questa fiera?","Conoscere quartiere, regolamento e orari fa risparmiare tempo."),
   ("10. Cosa succede se c'è un problema in fiera?","Chi interviene, in quanto tempo, durante i giorni di manifestazione?")]),
  ('t','noi',"Le nostre risposte",None,[],[
   ("Referente unico.","Dal primo schizzo allo smontaggio."),
   ("Produzione interna.","Tutti gli elementi in legno, dalla A alla Z."),
   ("Squadre nostre.","Con partner per i picchi di lavoro, gestiti da noi."),
   ("Pratiche e certificati.","Progetto, servizi, dichiarazione di conformità e certificati dei materiali."),
   ("Magazzino nostro.","Per conservare e riusare gli stand dei clienti."),
   ("Esperienza.","Stand a Vinitaly, Marmomac, Salone del Mobile, EICMA, Host, Cosmoprof, Cersaie, EIMA, Sigep, MICAM, MIDO, Lineapelle, VicenzaOro, Ecomondo, Macfrut, Sicam e Samuexpo.")]),
 ],
 qa=[("Meglio un allestitore vicino alla fiera o vicino all'azienda?","Conta più che conosca la fiera e abbia squadre e logistica organizzate. Noi lavoriamo in tutta Italia e all'estero, con sede in Veneto."),
  ("Come confronto due preventivi per uno stand?","Mettili voce per voce: progetto, strutture, finiture, grafica, arredi, impianti, trasporto, montaggio, pratiche, magazzino. Spesso la differenza è in ciò che manca."),
  ("Lavorate su progetti fatti da altri?","Sì, produciamo e montiamo stand progettati dal tuo architetto o dalla tua sede, verificandoli sul regolamento della fiera."),
  ("Accettate richieste urgenti?","Sì, valutiamo subito cosa è possibile fare, anche a poche settimane dalla fiera.")],
 rel=[("Allestimenti fieristici","/servizi/allestimenti-fieristici/"),("Montaggio stand","/montaggio-stand-fieristici/"),("Quanto costa uno stand","/quanto-costa-uno-stand-fieristico/"),("Progetti di stand","/progetti-stand-fieristici/"),("Regolamento tecnico della fiera","/guide/regolamento-tecnico-fiera/")]),
]
