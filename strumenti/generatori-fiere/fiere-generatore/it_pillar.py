# -*- coding: utf-8 -*-
import sys; sys.path.insert(0,__import__('os').path.dirname(__file__))
from lib import *; from it_common import *
from nuove_common import FIERA_LINKS, FIERA_URL, CITTA_LINKS_ALL, TIPI_LINKS, SETTORI_LINKS, CAL
P=PILLAR; URL=SITE+P
qa=[
("Quanto costa uno stand fieristico?","Dipende da superficie, tipo di struttura (preallestita, modulare o su misura), finiture, grafica, impianto elettrico, trasporto e dalla città della fiera. Per questo non pubblichiamo un listino: ti facciamo un preventivo su misura, voce per voce, così sai esattamente cosa paghi. Nella <a href=\"/quanto-costa-uno-stand-fieristico/\">guida ai costi</a> spieghiamo da cosa dipende ogni voce."),
("Cosa è incluso nel servizio?","Quello che ti serve. Possiamo seguire tutto, dal progetto con render 3D alla grafica e stampa, dalle strutture all'impianto elettrico con illuminazione, moquette e LED, fino a trasporto, montaggio, smontaggio, magazzino e pratiche con l'ente fiera. Oppure solo una parte: per esempio solo materiali e montatori, se il progetto ce l'hai già."),
("Accettate anche richieste urgenti?","Sì. Lavoriamo anche a ridosso della fiera: con la nostra rete di montatori partner riusciamo a organizzare materiali e montaggio in tempi stretti. Prima ci scrivi, più scelta hai su soluzioni e finiture, ma una richiesta urgente non la rifiutiamo a priori."),
("Lo stand si può riutilizzare in più fiere?","Sì, ed è spesso la scelta più conveniente se esponi più volte l'anno. Gli stand modulari in alluminio e in tessuto teso nascono per essere smontati e rimontati, anche in configurazioni diverse; tra una fiera e l'altra possiamo conservarli nel nostro magazzino."),
("Meglio noleggiare o acquistare lo stand?","Se fai una o due fiere l'anno il noleggio di strutture e arredi di solito conviene; se ne fai molte, o vuoi uno stand riconoscibile che ti segue ovunque, l'acquisto si ripaga nel tempo. Facciamo entrambe le cose e te lo diciamo con i numeri del tuo caso."),
("In quali fiere lavorate?","In tutti i principali quartieri fieristici italiani, da Verona a Milano, Bologna, Padova, Vicenza, Pordenone, Rimini e Parma, e nelle fiere all'estero, in Germania, Francia, Spagna e nel resto d'Europa. Abbiamo allestito stand a fiere come Vinitaly, Marmomac, Salone del Mobile, EICMA, Host, Cosmoprof, Cersaie, EIMA, Sigep, MICAM, MIDO, Lineapelle, VicenzaOro, Ecomondo, Macfrut, Sicam e Samuexpo."),
("Vi occupate voi delle pratiche con l'ente fiera?","Sì. Il progetto dello stand va approvato secondo il regolamento tecnico della manifestazione, e servono documenti, pass per i montatori e orari per carico e scarico. Ce ne occupiamo noi, così non devi studiare il regolamento."),
("Lavorate anche con aziende straniere che espongono in Italia?","Sì, è una parte importante del nostro lavoro. Puoi scriverci nella tua lingua: abbiamo pagine dedicate in inglese, tedesco, francese, spagnolo, cinese, turco e arabo, e seguiamo tutto noi in Italia, dalla fornitura al montaggio."),
]
main = hero("Allestimenti fieristici · Novità",
 'Allestimenti fieristici e stand per fiere <span class="grad">chiavi in mano</span>.',
 "Progettiamo, forniamo e montiamo stand fieristici per aziende di ogni settore, in Italia e all'estero. Troviamo il materiale necessario e tutta la componentistica richiesta, e squadre di montatori partner, gestite da noi, costruiscono lo stand direttamente in fiera. Un team con oltre 20 anni di esperienza nel settore fieristico, un unico referente dal primo schizzo allo smontaggio.",
 "Richiedi un preventivo per lo stand",CT,"Come lavoriamo","#metodo")
main+=cards("cosa","Tutto quello che serve allo stand, in un unico fornitore",
 "Uno stand è fatto di decine di pezzi e di tante competenze diverse. Possiamo occuparci di tutto, oppure solo della parte che ti manca.",
 [("Progetto e render 3D","Partiamo da superficie, posizione nel padiglione e obiettivi. Ti mostriamo lo stand in render 3D prima di costruirlo, così decidi vedendolo e non immaginandolo."),
  ("Materiali e componentistica","Strutture, profili, raccordi, pareti, pavimentazioni, arredi: troviamo e procuriamo il materiale necessario e tutta la componentistica richiesta dal progetto e dal regolamento della fiera."),
  ("Grafica e stampa","Pannelli, banner, tessuti stampati, scritte e insegne. Curiamo anche l'impaginazione dei file di stampa, perché in fiera un colore sbagliato si vede da dieci metri."),
  ("Impianto elettrico, luci e LED","Impianto elettrico con dichiarazione di conformità per l'ente fiera, illuminazione, moquette e pavimentazioni, schermi e ledwall."),
  ("Montaggio e smontaggio in fiera","Squadre di montatori, nostre e partner, che costruiscono lo stand direttamente in fiera nei tempi di allestimento previsti, e lo smontano a fine manifestazione."),
  ("Trasporto, magazzino e pratiche","Trasporto e logistica, magazzino tra una fiera e l'altra, approvazione del progetto, pass e orari di carico e scarico con l'ente fiera.")])
main+=testo("tipi","Ogni tipo di stand, <span class=\"grad\">a noleggio o in acquisto</span>",
 "Non c'è uno stand giusto per tutti: dipende da quante fiere fai, da come vuoi presentarti e dal budget.",
 ["Lavoriamo con tutte le principali soluzioni: dallo stand preallestito, il più rapido da organizzare, allo stand su misura in legno progettato da zero sul tuo marchio. In mezzo ci sono le strutture modulari in alluminio e in tessuto teso, che si montano velocemente e si riutilizzano da una fiera all'altra.",
  "Strutture e arredi possono essere a noleggio o in acquisto. Il noleggio è comodo per chi espone poche volte l'anno; l'acquisto conviene a chi partecipa a molte manifestazioni e vuole uno stand sempre riconoscibile, che possiamo conservare in magazzino fra un evento e l'altro."],
 [("Stand preallestiti.","Pareti, moquette, illuminazione e arredi base: la soluzione più veloce, ideale per la prima fiera o per spazi piccoli. <a href=\"/noleggio-stand-fieristici/\">Noleggio stand</a>"),
  ("Stand modulari in alluminio.","Telai e pannelli componibili, riconfigurabili su metrature diverse e riutilizzabili per anni. <a href=\"/stand-modulari/\">Stand modulari</a>"),
  ("Tessuto teso.","Grafiche stampate su tessuto montate su telai leggeri: grandi immagini senza giunture, trasporto leggero, montaggio rapido."),
  ("Su misura in legno.","Progetto unico, costruito ad hoc: forme, materiali e finiture scelti sul tuo marchio. <a href=\"/stand-fieristici-su-misura/\">Stand su misura</a>"),
  ("A isola, ad angolo, a due piani.","Dallo spazio in linea all'isola aperta su quattro lati, fino agli stand a due piani con sala riunioni.")])
main+=chips("fiere","Lavoriamo in <span class=\"grad\">tutte le fiere</span>",
 "Siamo presenti nei principali quartieri fieristici italiani e nelle fiere all'estero. Per ogni città trovi una pagina dedicata.",
 CITTA_LINKS_ALL+[("Fiere all'estero","/allestimenti-fieristici-estero/"),("Fiere in Germania","/allestimenti-fieristici-germania/")])
main+=chips("manifestazioni","Alcune fiere in cui abbiamo allestito stand",None,[(f,FIERA_URL.get({"Salone del Mobile":"salone-del-mobile"}.get(f,f.lower().replace(" ","-")))) for f in FIERE],"Esperienza")
main+=chips("calendario-fiere","Calendario fiere 2026–2027, <span class=\"grad\">con mappa</span>",
 "Le date delle principali fiere in Italia e in Europa su una mappa interattiva: clicca una fiera e richiedi lo stand. Qui sotto le pagine dedicate alle fiere più importanti.",
 [("Apri il calendario fiere",CAL)]+FIERA_LINKS)
main+=chips("tipologie","Ogni forma e misura di stand",None,TIPI_LINKS)
main+=chips("settori","Stand per il tuo settore",None,SETTORI_LINKS)
main+=testo("esperienza","Oltre 20 anni di fiere, <span class=\"grad\">anche quando i tempi sono stretti</span>",None,
 ["In oltre 20 anni di lavoro nel settore fieristico abbiamo imparato una cosa: in fiera i problemi non si risolvono, si prevengono. Un pezzo che manca, un impianto non conforme, un orario di carico sbagliato costano ore che durante l'allestimento non ci sono. Per questo controlliamo materiali, componentistica e documenti prima di partire, non in padiglione.",
  "Lavoriamo con squadre di montatori nostre e con squadre esterne di fiducia. Questo ci permette di seguire più fiere nello stesso periodo e di accettare anche le richieste urgenti, a ridosso dell'apertura, senza rinunciare alla qualità del montaggio."],
 [("Un unico referente.","Una persona che conosce il tuo stand dall'inizio alla fine e risponde di tutto."),
  ("Preventivo voce per voce.","Prima di partire sai cosa comprende e quanto costa ogni parte."),
  ("Urgenze accettate.","Se la fiera è vicina, scrivici lo stesso: valutiamo subito cosa è possibile fare."),
  ("Italia ed estero.","Stessa organizzazione in Italia e nelle fiere in Germania, Francia, Spagna e nel resto d'Europa.")])
main+=testo("digitale","Uno stand che <span class=\"grad\">porta contatti</span>, non solo visite",
 "Siamo anche un'agenzia tech: lo stand può essere l'inizio di un percorso che continua dopo la fiera.",
 ["La fiera costa e dura pochi giorni. Quello che resta, quando lo stand è smontato, sono i contatti raccolti e la capacità di richiamarli. Se vuoi, all'allestimento affianchiamo la parte digitale: una <a href=\"/servizi/siti-web-ecommerce/\">pagina per prenotare un appuntamento allo stand</a>, <a href=\"/servizi/meta-ads/\">campagne Meta</a> e <a href=\"/servizi/google-ads/\">Google Ads</a> per invitare clienti e potenziali clienti nei giorni della fiera, e un modulo da usare in fiera che manda i contatti direttamente nel tuo <a href=\"/servizi/gestionali-crm/\">CRM</a>.",
  "Non è obbligatorio: puoi affidarci solo l'allestimento. Ma se stand e comunicazione li segue lo stesso team, è più facile che i soldi spesi in fiera tornino indietro."])
main+=passi("metodo","Come lavoriamo","Dalle misure dello spazio<br>allo stand <span class=\"grad\">pronto.</span>","Ogni passaggio ha una consegna chiara, così sai sempre a che punto siamo.",
 [("Brief","Fiera, date, metratura e tipo di spazio (in linea, angolo, penisola, isola), obiettivi e budget. Se hai già un progetto, partiamo da quello."),
  ("Progetto e render 3D","Ti mostriamo lo stand come sarà, con materiali, grafica e luci. Lo modifichiamo finché non ti convince."),
  ("Preventivo e approvazioni","Preventivo voce per voce. Poi presentiamo il progetto all'ente fiera secondo il regolamento tecnico della manifestazione."),
  ("Produzione e fornitura","Strutture, componentistica, grafiche, arredi, impianto elettrico: tutto pronto e verificato prima di partire."),
  ("Trasporto e montaggio","Carico, trasporto e montaggio in fiera nei tempi previsti. Quando arrivi, lo stand è pronto."),
  ("Smontaggio e magazzino","A fine fiera smontiamo tutto e, se lo stand è tuo, lo conserviamo per la prossima manifestazione.")])
main+=faq(FAQ_EY,FAQ_T,qa)
main+=cta("Hai una fiera in arrivo?","Dicci quale, quando e quanto è grande lo spazio. Ti rispondiamo con quello che serve e quanto costa, anche se mancano poche settimane.","Richiedi un preventivo gratuito",CT)
main+=altri("Approfondisci",related(P))
nodes=[service_node(URL,"Allestimenti fieristici","Allestimento e montaggio di stand fieristici",
 "Allestimenti fieristici chiavi in mano per aziende di ogni settore in Italia e all'estero: progetto e render 3D, materiali e componentistica, grafica e stampa, impianto elettrico, illuminazione e LED, montaggio e smontaggio in fiera, trasporto, magazzino e pratiche con l'ente fiera. Stand preallestiti, modulari, in tessuto teso e su misura, a noleggio o in acquisto.",
 AREAS_IT,["Progettazione stand e render 3D","Stand preallestiti","Stand modulari in alluminio","Stand in tessuto teso","Stand su misura in legno","Grafica e stampa per stand","Impianto elettrico, illuminazione e LED","Montaggio e smontaggio stand in fiera","Trasporto, logistica e magazzino","Pratiche con l'ente fiera","Noleggio stand e arredi"],'it')]
alts={'it':P,'en':'/en/exhibition-stand-builder-italy/','de':'/de/messebau-italien/','fr':'/fr/standiste-salon-italie/','es':'/es/montaje-stands-feriales-italia/','zh':'/zh/italy-exhibition-stand/','tr':'/tr/italya-fuar-standi/','ar':'/ar/italy-exhibition-stand/'}
print(build('it',P,"Allestimenti fieristici e stand per fiere chiavi in mano",
 "Allestimenti fieristici in Italia e all'estero: stand e arredi in legno su nostro progetto 3D, laboratori partner, impianti e montatori. Prezzi competitivi.",
 "Allestimenti fieristici chiavi in mano — Danova Tech","Progetto, materiali, componentistica e montatori in fiera. Stand preallestiti, modulari e su misura, in Italia e all'estero.",
 [("Home","/"),("Servizi","/#servizi"),("Allestimenti fieristici",None)],main,qa,nodes,alts))
