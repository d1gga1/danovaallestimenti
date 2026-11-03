# -*- coding: utf-8 -*-
import sys,os; sys.path.insert(0,os.path.dirname(__file__))
from lib import *; from it_common import *
def svc(P,name,stype,desc,offers): return [service_node(SITE+P,name,stype,desc,AREAS_IT,offers,'it')]
CTA_P="Dicci fiera, date e metratura: ti rispondiamo con quello che serve e quanto costa, anche con poco preavviso."
def page(P,title,desc,ogt,ogd,crumb,main,qa,nodes,cr=None):
    main+=faq(FAQ_EY,FAQ_T,qa)+cta("Parliamo del tuo stand.",CTA_P,"Richiedi un preventivo gratuito",CT)+altri("Approfondisci",related(P))
    print(build('it',P,title,desc,ogt,ogd,cr or crumbs(crumb),main,qa,nodes))

# ============ MONTAGGIO
P="/montaggio-stand-fieristici/"
m=hero("Montaggio stand",'Montaggio stand fieristici: <span class="grad">montatori direttamente in fiera</span>.',
 "Squadre di montatori nostre e partner che costruiscono il tuo stand nel quartiere fieristico, nei tempi di allestimento fissati dall'organizzatore, e lo smontano a fine manifestazione. Montiamo stand progettati da noi o da altri, preallestiti, modulari, in tessuto teso e su misura, in Italia e all'estero.",
 "Richiedi montatori per la tua fiera",CT,"Come funziona","#metodo")
m+=cards("cosa","Cosa comprende il montaggio","Il montaggio non è solo avvitare pannelli: è far arrivare tutto nel posto giusto, nell'ordine giusto, nell'orario giusto.",
 [("Squadre di montatori","Montatori con esperienza in fiera, nostri e di squadre esterne di fiducia, dimensionati sulla metratura e sui tempi di allestimento della manifestazione."),
  ("Materiale e componentistica","Arriviamo con tutto: strutture, profili, raccordi, ferramenta e minuteria. Se manca un pezzo in padiglione si perdono ore, per questo la componentistica si verifica prima di partire."),
  ("Impianto elettrico e luci","Posa dell'impianto elettrico con dichiarazione di conformità, illuminazione, schermi e ledwall, collegati e testati prima dell'apertura."),
  ("Grafiche e finiture","Montaggio di pannelli, tessuti stampati, insegne e vetrofanie, posa di moquette e pavimentazioni sopraelevate."),
  ("Smontaggio","A fine fiera smontiamo, imballiamo e carichiamo tutto nei tempi di disallestimento, lasciando lo spazio come richiesto dall'ente fiera."),
  ("Logistica e pass","Trasporto, orari di carico e scarico, pass per i montatori e registrazioni richieste dal quartiere fieristico.")])
m+=testo("progetti-di-altri","Montiamo anche stand <span class=\"grad\">progettati da altri</span>",None,
 ["Non serve che il progetto sia nostro. Se hai già un architetto, un'agenzia o uno stand di proprietà, possiamo occuparci solo della parte pratica: troviamo il materiale e la componentistica che mancano, organizziamo la squadra e montiamo lo stand in fiera seguendo i disegni esecutivi.",
  "Lo stesso vale per gli stand già usati in altre fiere: li recuperiamo dal tuo magazzino o dal nostro, verifichiamo cosa serve sostituire o adattare alla nuova metratura e li rimontiamo."],
 [("Oltre 20 anni in fiera.","Sappiamo come funzionano gli allestimenti dei grandi quartieri fieristici e cosa chiedono gli enti fiera."),
  ("Squadre nostre e partner.","Possiamo coprire più fiere nello stesso periodo e stand di grandi dimensioni."),
  ("Anche urgenze.","Se la fiera è vicina, valutiamo subito squadra e materiali disponibili."),
  ("Italia ed estero.","Montiamo stand in tutti i quartieri fieristici italiani e nelle fiere in Germania, Francia, Spagna e nel resto d'Europa.")])
m+=passi("metodo","Come funziona","Dal disegno <span class=\"grad\">allo stand acceso.</span>",None,
 [("Sopralluogo sul progetto","Studiamo disegni, metratura, posizione nel padiglione e regolamento tecnico della fiera."),
  ("Lista materiali","Verifichiamo materiali e componentistica, procuriamo quello che manca e prepariamo il carico."),
  ("Squadra e tempi","Dimensioniamo la squadra di montatori sui giorni di allestimento disponibili."),
  ("Montaggio in fiera","Strutture, pavimenti, impianto elettrico, grafiche, arredi. Pulizia finale e consegna."),
  ("Smontaggio","A fine fiera disallestimento, carico e, se serve, magazzino fino alla prossima manifestazione.")])
page(P,"Montaggio stand fieristici: montatori in fiera | Danova Tech",
 "Montaggio e smontaggio di stand fieristici con montatori in fiera, in Italia e all'estero. Materiali, impianto elettrico e grafiche. Anche in urgenza.",
 "Montaggio stand fieristici — montatori direttamente in fiera","Squadre di montatori, materiali e componentistica: montiamo e smontiamo il tuo stand in fiera, anche se il progetto è di altri.",
 "Montaggio stand fieristici",m,[
 ("Montate anche stand progettati da altri?","Sì. Possiamo occuparci solo di materiali, componentistica e montaggio seguendo i disegni del tuo progettista, oppure di rimontare uno stand che hai già."),
 ("Quanti montatori servono per uno stand?","Dipende da metratura, tipo di struttura e giorni di allestimento disponibili. Uno stand preallestito piccolo si monta in poche ore, uno su misura a isola richiede squadre più grandi e più giorni. Dimensioniamo la squadra sul tuo caso."),
 ("Vi occupate anche dello smontaggio?","Sì. A fine manifestazione smontiamo, imballiamo e carichiamo lo stand nei tempi di disallestimento, e se vuoi lo conserviamo in magazzino per la fiera successiva."),
 ("Potete intervenire con poco preavviso?","Sì, accettiamo anche richieste urgenti. Lavorando con la nostra rete di montatori partner riusciamo spesso a organizzare il montaggio anche a ridosso della fiera."),
 ("Lavorate anche nelle fiere all'estero?","Sì, in Germania, Francia, Spagna e nel resto d'Europa, con la stessa organizzazione che usiamo in Italia.")],
 svc(P,"Montaggio stand fieristici","Montaggio e smontaggio di stand fieristici","Montaggio e smontaggio di stand fieristici direttamente in fiera con squadre di montatori proprie e partner, fornitura di materiali e componentistica, impianto elettrico, grafiche, logistica e pass, in Italia e all'estero.",
 ["Squadre di montatori in fiera","Smontaggio e disallestimento","Fornitura componentistica","Impianto elettrico e illuminazione","Posa grafiche e pavimentazioni","Logistica, pass e orari di carico"]))

# ============ SU MISURA
P="/stand-fieristici-su-misura/"
m=hero("Stand su misura",'Stand fieristici <span class="grad">su misura</span>, progettati sul tuo marchio.',
 "Uno stand costruito da zero intorno al tuo prodotto e alla tua immagine: progetto con render 3D, costruzione in legno e materiali scelti, grafica, luci e arredi, fino al montaggio in fiera. Per chi vuole farsi riconoscere da lontano.",
 "Richiedi un progetto",CT,"Come nasce","#metodo")
m+=cards("cosa","Cosa rende uno stand davvero su misura",None,
 [("Progetto e render 3D","Partiamo dal prodotto, dai visitatori che vuoi attirare e dalla posizione nel padiglione. Ti mostriamo lo stand in render 3D e lo affiniamo prima di costruire."),
  ("Costruzione in legno","Pareti, banchi, vetrine e strutture realizzati ad hoc, con forme e finiture che uno stand modulare non permette."),
  ("Materiali e finiture","Laccati, legni, metalli, vetro, tessuti, pavimenti sopraelevati: scegliamo i materiali in base all'immagine e al budget."),
  ("Luce e tecnologia","Illuminazione studiata sul prodotto, schermi e ledwall, impianto elettrico con dichiarazione di conformità."),
  ("Spazi funzionali","Area accoglienza, sala riunioni, magazzino, zona degustazione o demo: lo stand lavora per i tuoi obiettivi commerciali."),
  ("Dalla produzione al montaggio","Produzione, trasporto, montaggio e smontaggio in fiera con un unico referente.")])
m+=testo("quando","Quando conviene lo stand su misura",None,
 ["Lo stand su misura è la scelta giusta quando la fiera è centrale per il tuo fatturato, quando il prodotto ha bisogno di uno spazio pensato per lui (macchinari, degustazioni, materiali da toccare) o quando vuoi uno stand che i clienti ricordino.",
  "Se invece fai molte fiere con metrature diverse, uno <a href=\"/stand-modulari/\">stand modulare</a> personalizzato con grafiche e arredi può darti un ottimo risultato con costi di riuso più bassi. Spesso la soluzione migliore è una via di mezzo: struttura modulare e alcuni elementi costruiti su misura. Te lo diciamo con il preventivo alla mano."],
 [("A isola, angolo, penisola o in linea.","Progettiamo su qualsiasi tipo di spazio."),
  ("Anche a due piani.","Con sala riunioni o area ospiti al piano superiore, nel rispetto del regolamento tecnico della fiera."),
  ("Noleggio o acquisto.","Alcuni elementi possono essere a noleggio, altri di tua proprietà e riutilizzabili."),
  ("Approvazione dell'ente fiera.","Prepariamo e presentiamo noi il progetto secondo il regolamento della manifestazione.")])
m+=passi("metodo","Come nasce","Dall'idea <span class=\"grad\">al padiglione.</span>",None,
 [("Brief","Prodotto, obiettivi, metratura, posizione, budget e fiere previste."),
  ("Concept e render 3D","Una proposta visiva completa di materiali, grafica e luci."),
  ("Esecutivi e approvazioni","Disegni esecutivi, impianto elettrico, approvazione dell'ente fiera."),
  ("Produzione","Costruzione degli elementi, stampa delle grafiche, preparazione di arredi e tecnologia."),
  ("Montaggio e smontaggio","Montaggio in fiera, consegna dello stand e smontaggio a fine manifestazione.")])
page(P,"Stand fieristici su misura in legno, progetto 3D | Danova Tech",
 "Stand fieristici su misura in legno, progettati da noi e costruiti da laboratori partner: progetto 3D, luci e montaggio in fiera. Isole e due piani, prezzi competitivi.",
 "Stand fieristici su misura — Danova Tech","Progetto 3D, costruzione, grafica e montaggio: uno stand unico, costruito sul tuo marchio.",
 "Stand fieristici su misura",m,[
 ("Quanto costa uno stand su misura?","Dipende da metratura, materiali, finiture, tecnologia e città della fiera. Ti diamo un preventivo dettagliato dopo il brief; nella <a href=\"/quanto-costa-uno-stand-fieristico/\">guida ai costi</a> trovi le voci che incidono di più."),
 ("Lo stand su misura si può riutilizzare?","Sì, se lo progettiamo pensando al riuso: alcuni elementi si conservano in magazzino e si adattano a fiere e metrature diverse."),
 ("Fate anche il render 3D?","Sì, ogni progetto su misura parte da un render 3D che puoi modificare prima della produzione."),
 ("In quanto tempo si realizza?","Dipende dalla complessità. Prima ci scrivi, più margine c'è per materiali e finiture, ma valutiamo anche richieste urgenti.")],
 svc(P,"Stand fieristici su misura","Progettazione e realizzazione di stand fieristici su misura","Progettazione con render 3D, costruzione in legno e materiali su misura, grafica, illuminazione e montaggio in fiera di stand personalizzati, anche a isola e a due piani.",
 ["Progettazione e render 3D","Costruzione stand in legno","Stand a isola e a due piani","Grafica, luci e tecnologia","Montaggio e smontaggio in fiera"]))

# ============ MODULARI
P="/stand-modulari/"
m=hero("Stand modulari",'Stand modulari in alluminio e <span class="grad">tessuto teso</span>.',
 "Strutture componibili che si montano in fretta, si adattano a metrature diverse e si riutilizzano fiera dopo fiera. A noleggio o in acquisto, personalizzate con grafiche, luci e arredi, e montate direttamente in fiera da squadre gestite da noi.",
 "Richiedi un preventivo",CT,"Noleggio o acquisto","#formula")
m+=cards("cosa","Perché scegliere uno stand modulare",None,
 [("Si riutilizza","Telai e pannelli si smontano e si rimontano per anni. Cambi le grafiche, non lo stand."),
  ("Si adatta allo spazio","La stessa struttura si riconfigura da uno spazio in linea a uno ad angolo o a isola, su metrature diverse."),
  ("Si monta velocemente","Meno ore di allestimento, utile nelle fiere con tempi stretti o quando si arriva con poco preavviso."),
  ("Grafiche in tessuto teso","Grandi immagini stampate su tessuto, senza giunture, leggere da trasportare e facili da sostituire."),
  ("Personalizzabile","Banchi, vetrine, mensole, porte, magazzino, illuminazione e schermi si integrano nella struttura."),
  ("Trasporto e magazzino","Imballi compatti, meno costi di trasporto, e possiamo conservarlo noi tra una fiera e l'altra.")])
m+=testo("formula","Noleggio o acquisto?",None,
 ["Se esponi una o due volte l'anno, il <a href=\"/noleggio-stand-fieristici/\">noleggio</a> della struttura modulare ti evita l'investimento iniziale e il magazzino. Se fai molte fiere, l'acquisto si ripaga nel tempo e ti dà uno stand sempre uguale, riconoscibile dai clienti.",
  "Facciamo entrambe le cose, e si possono mescolare: struttura di proprietà, arredi a noleggio, grafiche nuove per ogni manifestazione. Quando serve un elemento che il modulare non permette, lo costruiamo <a href=\"/stand-fieristici-su-misura/\">su misura</a> e lo integriamo."],
 [("Alluminio.","Robusto e preciso, ideale per pareti, portali, vetrine e strutture a sbalzo."),
  ("Tessuto teso.","Leggero e d'impatto, perfetto per grafiche grandi e retroilluminate."),
  ("Misto.","Struttura modulare con elementi su misura in legno per banchi e zone prodotto.")])
page(P,"Stand modulari in alluminio e tessuto teso | Danova Tech",
 "Stand fieristici modulari in alluminio e tessuto teso, a noleggio o in acquisto: riutilizzabili, riconfigurabili e montati in fiera. In Italia e all'estero.",
 "Stand modulari riutilizzabili — Danova Tech","Strutture in alluminio e tessuto teso, a noleggio o in acquisto, montate in fiera da squadre gestite da noi.",
 "Stand modulari",m,[
 ("Uno stand modulare si può usare in fiere con metrature diverse?","Sì, è il suo vantaggio principale: la stessa struttura si riconfigura su spazi e forme diverse, aggiungendo o togliendo moduli."),
 ("Si possono cambiare solo le grafiche?","Sì. Con il tessuto teso e i pannelli intercambiabili cambi immagine da una fiera all'altra senza rifare la struttura."),
 ("Lo conservate voi tra una fiera e l'altra?","Sì, possiamo tenerlo nel nostro magazzino e portarlo direttamente alla fiera successiva."),
 ("Uno stand modulare è meno bello di uno su misura?","Non necessariamente. Con grafiche, luci e qualche elemento costruito su misura il risultato è curato e riconoscibile, con costi di riuso più bassi.")],
 svc(P,"Stand modulari","Noleggio e vendita di stand fieristici modulari","Stand fieristici modulari in alluminio e tessuto teso, a noleggio o in acquisto, riconfigurabili e riutilizzabili, con grafiche, illuminazione, arredi, montaggio in fiera e magazzino.",
 ["Stand modulari in alluminio","Stand in tessuto teso","Noleggio stand modulari","Vendita stand modulari","Magazzino e riallestimento"]))

# ============ NOLEGGIO
P="/noleggio-stand-fieristici/"
m=hero("Noleggio stand",'Noleggio stand fieristici, <span class="grad">arredi e attrezzature</span>.',
 "Stand preallestiti e modulari a noleggio, arredi, illuminazione, moquette, schermi e LED: tutto quello che serve per esporre senza comprare niente. Lo portiamo, lo montiamo in fiera e lo riprendiamo a fine manifestazione.",
 "Richiedi un preventivo di noleggio",CT,"Cosa si può noleggiare","#cosa")
m+=cards("cosa","Cosa si può noleggiare",None,
 [("Stand preallestiti","Pareti, moquette, illuminazione, insegna e arredi base. La soluzione più rapida per la prima fiera o per spazi piccoli."),
  ("Strutture modulari","Telai in alluminio e tessuto teso, riconfigurabili sulla tua metratura e personalizzati con le tue grafiche."),
  ("Arredi","Banconi, sedute, tavoli, vetrine, espositori, mensole, frigoriferi e attrezzature per degustazioni."),
  ("Luci, schermi e LED","Illuminazione, monitor e ledwall, con impianto elettrico certificato."),
  ("Pavimentazioni","Moquette, pavimenti sopraelevati e pedane."),
  ("Grafiche","Le grafiche sono tue: le stampiamo per il noleggio o le teniamo per la fiera successiva.")])
m+=testo("quando","Quando conviene il noleggio",None,
 ["Il noleggio conviene se esponi poche volte l'anno, se stai provando una fiera nuova o se non vuoi occuparti di magazzino e manutenzione. Paghi l'uso, non la proprietà, e a fine fiera ce ne occupiamo noi.",
  "Se invece le fiere diventano molte, valutiamo insieme l'<a href=\"/stand-modulari/\">acquisto di uno stand modulare</a>: facciamo il conto con i tuoi numeri e ti diciamo da quale fiera in poi conviene."],
 [("Tutto incluso, se vuoi.","Trasporto, montaggio, smontaggio e ritiro."),
  ("Anche all'ultimo momento.","Accettiamo richieste urgenti, compatibilmente con la disponibilità del materiale."),
  ("Misto noleggio e proprietà.","Struttura a noleggio, grafiche e alcuni elementi tuoi.")])
page(P,"Noleggio stand fieristici: affitto stand e arredi | Danova Tech",
 "Noleggio stand fieristici preallestiti e modulari, arredi, luci, schermi LED, con trasporto e montaggio in fiera. In Italia e all'estero, anche last minute.",
 "Noleggio stand fieristici — Danova Tech","Stand preallestiti e modulari, arredi e tecnologia a noleggio, montati in fiera.",
 "Noleggio stand fieristici",m,[
 ("Cosa comprende il noleggio di uno stand?","Le strutture, gli arredi e le attrezzature che scegli, più, se lo desideri, trasporto, montaggio, smontaggio e ritiro. Le grafiche personalizzate si stampano a parte."),
 ("Si può noleggiare solo l'arredamento?","Sì: banconi, sedute, vetrine, luci, schermi e pavimentazioni si noleggiano anche separatamente."),
 ("Quanto costa noleggiare uno stand?","Dipende da metratura, tipo di struttura, arredi, città e durata della fiera. Facciamo un preventivo su misura voce per voce."),
 ("Conviene noleggiare o comprare?","Per poche fiere l'anno di solito il noleggio; per molte fiere l'acquisto di uno stand modulare. Facciamo il conto insieme.")],
 svc(P,"Noleggio stand fieristici","Noleggio di stand fieristici e arredi","Noleggio di stand fieristici preallestiti e modulari, arredi, illuminazione, pavimentazioni, schermi e LED, con trasporto, montaggio e smontaggio in fiera.",
 ["Noleggio stand preallestiti","Noleggio stand modulari","Noleggio arredi per fiere","Noleggio schermi e LED","Noleggio moquette e pedane"]))

# ============ COSTI
P="/quanto-costa-uno-stand-fieristico/"
m=hero("Costi",'Quanto costa uno stand fieristico: <span class="grad">da cosa dipende il prezzo</span>.',
 "Non esiste un prezzo al metro quadro valido per tutti: due stand della stessa misura possono costare in modo molto diverso. Qui spieghiamo le voci che compongono il costo, così sai cosa chiedere e come confrontare i preventivi.",
 "Richiedi un preventivo su misura",CT,"Le voci di costo","#voci")
m+=cards("voci","Le voci che compongono il costo","Un preventivo serio le elenca separatamente. Se ne mancano, chiedi perché.",
 [("Area espositiva","Lo spazio si paga all'organizzatore della fiera ed è separato dall'allestimento. A volte comprende servizi base come allaccio elettrico o pulizia: va verificato."),
  ("Struttura","Preallestita, modulare, tessuto teso o su misura in legno: è la voce che cambia di più. Noleggio e acquisto hanno logiche diverse."),
  ("Progetto","Progettazione e render 3D, esecutivi e pratiche per l'approvazione dell'ente fiera."),
  ("Grafica e stampa","Pannelli, tessuti, insegne: dipende da superfici, materiali e se le grafiche sono riutilizzabili."),
  ("Impianti e tecnologia","Impianto elettrico con dichiarazione di conformità, illuminazione, schermi, ledwall, eventuali allacci idrici."),
  ("Arredi e pavimenti","Banconi, sedute, vetrine, moquette o pavimento sopraelevato."),
  ("Montaggio e smontaggio","Ore di squadra, numero di montatori, giorni di allestimento, eventuali lavori notturni o urgenti."),
  ("Trasporto e logistica","Distanza della fiera, volumi, orari di carico e scarico, eventuale magazzino.")])
m+=testo("fattori","Cosa fa salire (e scendere) il prezzo",None,
 ["Il costo dipende soprattutto da tre scelte: quanto lo stand è personalizzato, se è a noleggio o di proprietà, e quante volte verrà usato. Uno stand su misura in legno costa di più la prima volta ma comunica di più; uno modulare costa meno a ogni riuso. Per chi espone spesso, il costo vero da guardare è quello per fiera, non quello della prima.",
  "Pesano anche i tempi: una richiesta urgente si può fare, ma riduce la scelta di materiali e può richiedere squadre più numerose. E pesa la città: logistica, orari di accesso e regolamenti cambiano da un quartiere fieristico all'altro."],
 [("Riutilizzare struttura e arredi.","È il modo più efficace per abbassare il costo per fiera."),
  ("Grafiche intercambiabili.","Su tessuto teso o pannelli, cambi messaggio senza rifare lo stand."),
  ("Decidere presto.","Più margine significa più scelta e meno costi di urgenza."),
  ("Un unico fornitore.","Meno passaggi, meno ricarichi, un solo responsabile.")])
m+=testo("preventivo","Come confrontare due preventivi",None,
 ["Controlla che siano confrontabili: stessa metratura, stesso tipo di struttura, stessi servizi inclusi. Chiedi se comprendono impianto elettrico e dichiarazione di conformità, pratiche con l'ente fiera, trasporto, smontaggio e smaltimento. Molte differenze di prezzo stanno in quello che non c'è scritto.",
  "Noi preferiamo non pubblicare un listino, perché ogni stand è diverso: ti mandiamo un preventivo su misura, voce per voce, dopo un breve brief su fiera, metratura e obiettivi."])
qa=[("Quanto costa uno stand fieristico al metro quadro?","Non c'è una cifra unica: il costo al metro quadro cambia molto fra stand preallestito, modulare e su misura, e dipende da finiture, impianti, città e tempi. Per questo facciamo preventivi su misura, voce per voce."),
 ("Il costo dello spazio è compreso nell'allestimento?","No. L'area espositiva si paga all'organizzatore della fiera; l'allestimento è una voce separata."),
 ("Come si risparmia su uno stand?","Riutilizzando struttura e arredi, scegliendo grafiche intercambiabili, decidendo con anticipo e affidando tutto a un unico fornitore."),
 ("Fate preventivi gratuiti?","Sì. Scrivici fiera, date e metratura e ti mandiamo un preventivo dettagliato.")]
page(P,"Quanto costa uno stand fieristico: le voci di costo | Danova Tech",
 "Quanto costa uno stand fieristico? Le voci del prezzo, come confrontare i preventivi e perché chi produce in proprio gli elementi in legno costa meno.",
 "Quanto costa uno stand fieristico — guida alle voci di costo","Le voci che compongono il prezzo di uno stand e come confrontare due preventivi.",
 "Quanto costa uno stand fieristico",m,qa,[article_node(SITE+P,"Quanto costa uno stand fieristico: da cosa dipende il prezzo","Le voci che compongono il costo di uno stand fieristico e come confrontare i preventivi.","it")])

# ============ EVENTI SHOWROOM NEGOZI MOSTRE
P="/allestimenti-eventi-showroom-negozi/"
m=hero("Non solo fiere",'Allestimenti per eventi, congressi, <span class="grad">showroom, negozi e mostre</span>.',
 "Le stesse competenze che usiamo in fiera, applicate a ogni spazio che deve presentare un prodotto o un'idea: eventi aziendali e congressi, showroom, negozi e corner, mostre d'arte. Progetto, materiali, grafica, luci e montaggio con un unico referente.",
 "Richiedi un preventivo",CT,"Cosa allestiamo","#cosa")
m+=cards("cosa","Cosa allestiamo",None,
 [("Eventi e congressi","Palchi, fondali, desk di accoglienza, aree espositive per sponsor, segnaletica, luci e schermi per convention, lanci di prodotto e congressi."),
  ("Showroom","Spazi espositivi aziendali permanenti o temporanei, pensati per far vedere e toccare il prodotto e per ricevere clienti."),
  ("Negozi e retail","Allestimenti di negozi, corner e temporary store: arredi, espositori, vetrine, grafiche e illuminazione."),
  ("Mostre d'arte","Pareti, pannellature, basamenti e teche, illuminazione delle opere e grafiche di sala, montaggio e smontaggio."),
  ("Grafica e comunicazione","Insegne, vetrofanie, pannelli, tessuti stampati, segnaletica: e, se serve, anche il sito o la campagna dell'evento."),
  ("Montaggio e logistica","Trasporto, montaggio, smontaggio e magazzino, con squadre nostre e partner.")])
m+=testo("perche","Un solo partner per spazi fisici e digitali",None,
 ["I nostri oltre 20 anni di fiere ci hanno insegnato a lavorare con tempi stretti, regolamenti rigidi e spazi da allestire in poche ore. Le stesse regole valgono per un congresso in hotel, uno showroom che apre lunedì o una mostra che deve essere pronta per l'inaugurazione.",
  "E siamo anche un'agenzia tech: allo spazio fisico possiamo affiancare <a href=\"/servizi/siti-web-ecommerce/\">landing page</a> per le iscrizioni, <a href=\"/app-prenotazioni/\">prenotazioni</a>, <a href=\"/servizi/meta-ads/\">campagne</a> per portare persone e un <a href=\"/crm-aziendale/\">CRM</a> per non perdere i contatti."])
page(P,"Allestimenti per eventi, showroom, negozi e mostre | Danova Tech",
 "Allestimenti per eventi aziendali e congressi, showroom, negozi, temporary store e mostre: progetto, grafica, luci e montaggio. Un team con oltre 20 anni di esperienza.",
 "Allestimenti per eventi, showroom, negozi e mostre — Danova Tech","Progetto, materiali, grafica e montaggio per eventi, congressi, showroom, retail e mostre d'arte.",
 "Eventi, showroom, negozi e mostre",m,[
 ("Allestite anche eventi fuori dai quartieri fieristici?","Sì: hotel, centri congressi, spazi aziendali, location per eventi, negozi e spazi espositivi."),
 ("Vi occupate di mostre d'arte?","Sì: pannellature, basamenti, teche, illuminazione, grafiche di sala, montaggio e smontaggio."),
 ("Potete allestire uno showroom permanente?","Sì, sia permanente sia temporaneo, dal progetto al montaggio."),
 ("Seguite anche la comunicazione dell'evento?","Se vuoi sì: sito o landing page, iscrizioni, campagne e raccolta contatti.")],
 svc(P,"Allestimenti per eventi, showroom, negozi e mostre","Allestimento di eventi, showroom, punti vendita e mostre","Allestimenti per eventi aziendali e congressi, showroom, negozi e temporary store, mostre d'arte: progetto, materiali, grafica, illuminazione, montaggio e smontaggio.",
 ["Allestimento eventi e congressi","Allestimento showroom","Allestimento negozi e temporary store","Allestimento mostre d'arte","Grafica e segnaletica"]))

# ============ ESTERO
P="/allestimenti-fieristici-estero/"
m=hero("Fiere all'estero",'Stand per fiere all\'estero, <span class="grad">con un fornitore italiano</span>.',
 "Esponi in Germania, Francia, Spagna o nel resto d'Europa? Progettiamo, prepariamo e montiamo il tuo stand anche fuori dall'Italia, con la stessa organizzazione e lo stesso referente. Tu parli in italiano con noi, noi ci occupiamo di trasporto, montatori e regolamenti locali.",
 "Richiedi un preventivo per la fiera",CT,"Come lavoriamo","#metodo")
m+=cards("cosa","Cosa facciamo per le fiere all'estero",None,
 [("Progetto e approvazioni","Progetto secondo il regolamento tecnico del quartiere fieristico estero, documentazione e approvazioni."),
  ("Produzione in Italia","Strutture, grafiche e arredi preparati e verificati prima della partenza."),
  ("Trasporto internazionale","Logistica, imballi e orari di consegna in fiera."),
  ("Montatori in fiera","Squadre nostre e partner che montano e smontano lo stand nei tempi previsti."),
  ("Noleggio sul posto","Quando conviene, noleggiamo arredi e attrezzature vicino alla fiera per ridurre i trasporti."),
  ("Un unico referente","Una persona che parla la tua lingua e segue tutto, prima, durante e dopo la fiera.")])
m+=chips("paesi","Dove lavoriamo","Germania, Francia, Spagna e il resto d'Europa: dai grandi quartieri fieristici tedeschi alle fiere di settore in Francia e Spagna.",
 [("Germania",None),("Francia",None),("Spagna",None),("Austria",None),("Svizzera",None),("Belgio e Paesi Bassi",None),("Resto d'Europa",None)])
m+=passi("metodo","Come lavoriamo","Una fiera all'estero, <span class=\"grad\">organizzata dall'Italia.</span>",None,
 [("Brief","Fiera, paese, date, metratura, obiettivi."),
  ("Progetto e preventivo","Render 3D e preventivo voce per voce, trasporto compreso."),
  ("Approvazioni e logistica","Pratiche con l'ente fiera estero, imballi, spedizione, orari di consegna."),
  ("Montaggio e smontaggio","Squadre in fiera, consegna dello stand, smontaggio e rientro."),
  ("Dopo la fiera","Magazzino per la prossima manifestazione e, se vuoi, gestione dei contatti raccolti.")])
# 13/10/2026: questa pagina ora e' l'hub Europa, generato da build_europa.py
None and page(P,"Stand per fiere all'estero: Germania, Francia, Spagna",
 "Allestimenti fieristici all'estero per aziende italiane: progetto, produzione, trasporto, montatori e smontaggio in Germania, Francia, Spagna e Europa.",
 "Stand per fiere all'estero — Danova Tech","Progetto, trasporto e montatori per le fiere in Germania, Francia, Spagna e in Europa.",
 "Fiere all'estero",m,[
 ("In quali paesi montate stand?","Germania, Francia, Spagna e nel resto d'Europa."),
 ("Conviene portare lo stand dall'Italia o noleggiare sul posto?","Dipende da volumi, distanza e da quante fiere fai. Spesso conviene una via di mezzo: struttura e grafiche dall'Italia, arredi a noleggio sul posto."),
 ("Vi occupate voi del regolamento della fiera estera?","Sì, progetto e documentazione seguono il regolamento tecnico del quartiere fieristico."),
 ("Lavorate anche per aziende straniere?","Sì: abbiamo pagine in inglese, tedesco, francese, spagnolo, cinese, turco e arabo per le aziende che espongono in Italia e in Europa.")],
 [service_node(SITE+P,"Allestimenti fieristici all'estero","Allestimento di stand per fiere internazionali","Progettazione, produzione, trasporto internazionale, montaggio e smontaggio di stand per fiere in Germania, Francia, Spagna e nel resto d'Europa.",
  [{"@type":"Country","name":"Germania"},{"@type":"Country","name":"Francia"},{"@type":"Country","name":"Spagna"},{"@type":"Place","name":"Europa"}],["Stand per fiere in Germania","Stand per fiere in Francia","Stand per fiere in Spagna","Trasporto internazionale stand","Montatori per fiere estere"],'it')])

# ============ GUIDA
P="/guide/come-preparare-una-fiera/"
m=hero("Guida",'Come preparare una fiera: <span class="grad">la checklist completa</span>.',
 "Una fiera si vince prima di arrivare in padiglione. Questa guida mette in ordine quello che serve fare, mese per mese: dalla scelta della manifestazione allo stand, dagli inviti ai contatti da richiamare dopo. Aggiornata l'8 ottobre 2026 · Danova Tech.",
 "Fatti aiutare con lo stand",CT,"La checklist","#mesi")
m+=testo("sintesi","In cinque righe",None,[],
 [("Scegli la fiera per i visitatori, non per gli espositori.","Chiedi all'organizzatore i dati sui visitatori del tuo settore."),
  ("Fissa obiettivi misurabili.","Quanti appuntamenti, quanti contatti, quali clienti incontrare."),
  ("Decidi lo stand presto.","Spazio, progetto e approvazioni hanno scadenze fisse."),
  ("Invita prima di partire.","Lo stand pieno è quello in cui gli appuntamenti sono già fissati."),
  ("Richiama entro una settimana.","Un contatto di fiera si raffredda in pochi giorni.")],"Sintesi")
m+=passi("mesi","Checklist","Mese per mese, <span class=\"grad\">fino all'apertura.</span>",None,
 [("6-12 mesi prima","Scelta della fiera, prenotazione dell'area, budget complessivo e obiettivi. Più presto si prenota, più scelta c'è sulla posizione nel padiglione."),
  ("4-6 mesi prima","Brief per lo stand: metratura, tipo di spazio, prodotti da esporre, funzioni (riunioni, degustazioni, demo). Scelta fra stand <a href=\"/noleggio-stand-fieristici/\">a noleggio</a>, <a href=\"/stand-modulari/\">modulare</a> o <a href=\"/stand-fieristici-su-misura/\">su misura</a>."),
  ("3 mesi prima","Progetto e render 3D, preventivo definitivo, invio del progetto all'ente fiera secondo il regolamento tecnico e le scadenze della manifestazione."),
  ("2 mesi prima","Grafiche e materiali di stampa, cataloghi, campionature. Pagina web per prenotare un appuntamento allo stand e prime campagne di invito."),
  ("1 mese prima","Inviti personali ai clienti chiave, organizzazione del personale allo stand, logistica di prodotti e materiali, pass e orari di carico."),
  ("La settimana della fiera","Montaggio dello stand, prove di luci e schermi, briefing con il personale, modulo per raccogliere i contatti pronto sui dispositivi."),
  ("Durante la fiera","Registrare ogni contatto con note e priorità, foto e video per i social, controllo quotidiano dello stand."),
  ("Dopo la fiera","Smontaggio, magazzino dello stand riutilizzabile, richiamo dei contatti entro una settimana, analisi dei risultati rispetto agli obiettivi.")])
m+=testo("errori","Gli errori più comuni",None,
 ["Il primo è trattare lo stand come un costo d'immagine e non come uno strumento commerciale: senza obiettivi non si può dire se la fiera è andata bene. Il secondo è arrivare tardi con le decisioni, perché le scadenze dell'ente fiera non si spostano e l'urgenza costa. Il terzo è perdere i contatti: biglietti da visita in una scatola che nessuno apre per settimane.",
  "Se vuoi, ti aiutiamo con tutto: <a href=\"/servizi/allestimenti-fieristici/\">allestimento dello stand</a>, pagina e campagne di invito, raccolta dei contatti collegata al tuo CRM."])
page(P,"Come preparare una fiera: checklist mese per mese | Danova Tech",
 "Come preparare una fiera: checklist mese per mese dalla scelta della manifestazione allo stand, dagli inviti al richiamo dei contatti. Gli errori da evitare.",
 "Come preparare una fiera — checklist completa","Dalla scelta della fiera allo stand, dagli inviti ai contatti: cosa fare mese per mese.",
 "Come preparare una fiera",m,[
 ("Con quanto anticipo si prepara una fiera?","Idealmente da sei mesi a un anno per la scelta e la prenotazione dello spazio, e almeno tre-quattro mesi per lo stand. Ma anche con meno tempo si può fare: accettiamo richieste urgenti."),
 ("Come si misura il successo di una fiera?","Con gli obiettivi fissati prima: appuntamenti, contatti qualificati, preventivi richiesti e vendite nei mesi successivi."),
 ("Conviene uno stand a noleggio per la prima fiera?","Spesso sì: uno stand preallestito o modulare a noleggio riduce l'investimento mentre capisci se la fiera funziona per te.")],
 [article_node(SITE+P,"Come preparare una fiera: la checklist completa","Checklist mese per mese per preparare una fiera: stand, inviti, contatti.","it")],[("Home","/"),("Guide","/guide/"),("Come preparare una fiera",None)])
