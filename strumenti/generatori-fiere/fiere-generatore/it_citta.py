# -*- coding: utf-8 -*-
import sys,os; sys.path.insert(0,os.path.dirname(__file__))
from lib import *; from it_common import *
from nuove_common import FIERA_URL, FIERA_PAGES, CAL
import dati_calendario as DC
N2S={'Vinitaly':'vinitaly','Marmomac':'marmomac','Salone del Mobile':'salone-del-mobile','EICMA':'eicma','Host':'host','Cosmoprof':'cosmoprof','Cersaie':'cersaie','EIMA':'eima','Sicam':'sicam','Samuexpo':'samuexpo','Fieracavalli':'fieracavalli','VicenzaOro':'vicenzaoro','Sigep':'sigep','Ecomondo':'ecomondo','Cibus':'cibus'}
C=[
dict(s="verona",c="Verona",q="Veronafiere",gia=["Vinitaly","Marmomac"],altre=["Fieracavalli","Samoter"],
 lead="Allestimenti fieristici a Verona: progettiamo, forniamo e montiamo stand a Veronafiere, dal Vinitaly al Marmomac. Materiali, componentistica, grafica, impianti e montatori direttamente in fiera, con un unico referente.",
 intro=["Veronafiere è uno dei quartieri fieristici più importanti d'Italia, a sud della città e a pochi minuti dall'uscita Verona Sud. Ospita manifestazioni con un pubblico molto internazionale, e questo si vede negli stand: devono funzionare per i buyer che arrivano da tutto il mondo, non solo per i visitatori italiani.",
  "Per noi Verona è quasi casa: siamo in Veneto e lavoriamo a Veronafiere da anni. Abbiamo allestito stand al Vinitaly e al Marmomac, due fiere con esigenze opposte: il vino chiede spazi per degustare e incontrare, la pietra chiede strutture che reggano lastre pesanti."],
 sapere=[("Vinitaly: degustazione e incontri.","Banchi di mescita, frigoriferi e lavelli, retro magazzino per le bottiglie, tavoli per gli appuntamenti con i buyer: lo stand di una cantina è prima di tutto un luogo di lavoro."),
  ("Marmomac: carichi pesanti.","Lastre e blocchi di pietra richiedono pareti e pavimenti portanti, ancoraggi sicuri e una logistica di carico e scarico pensata in anticipo."),
  ("Tempi di allestimento.","Nelle grandi fiere veronesi i giorni di montaggio sono pochi e i padiglioni affollati: materiali e componentistica vanno verificati prima di arrivare."),
  ("Pubblico internazionale.","Grafiche e segnaletica bilingui, spazi per incontri riservati, e, se vuoi, una pagina in inglese per fissare gli appuntamenti.")],
 qa=[("Allestite stand per il Vinitaly?","Sì, abbiamo allestito stand al Vinitaly: banchi di degustazione, frigoriferi, magazzino bottiglie, aree incontri, grafica, luci e montaggio a Veronafiere."),
  ("Potete realizzare uno stand per il Marmomac?","Sì. Al Marmomac progettiamo strutture e pavimenti in grado di sostenere lastre e materiali pesanti, e organizziamo carico e scarico con i tempi della fiera.")]),
dict(s="milano",c="Milano",q="Fiera Milano Rho",gia=["Salone del Mobile","EICMA","Host"],altre=["Allianz MiCo (congressi)"],
 lead="Allestimenti fieristici a Milano: stand per Fiera Milano Rho e per i congressi in città, dal Salone del Mobile all'EICMA e Host. Progetto, materiali, componentistica, impianti e montatori in fiera.",
 intro=["Fiera Milano a Rho è uno dei quartieri fieristici più grandi d'Europa: padiglioni enormi, migliaia di espositori, regole precise su accessi, orari e sicurezza. Qui l'organizzazione conta quanto il progetto: chi arriva impreparato perde ore preziose fra varchi, scarichi e documenti.",
  "Abbiamo allestito stand al Salone del Mobile, all'EICMA e a Host. Tre mondi diversi: il design, dove lo stand è giudicato come un progetto d'arredo; le moto, dove serve spettacolo e un pubblico numeroso; l'ospitalità professionale, dove le macchine devono funzionare davvero."],
 sapere=[("Salone del Mobile: lo stand è il prodotto.","Finiture, luci e proporzioni vengono osservate da progettisti e buyer: lo stand su misura qui è spesso la scelta naturale."),
  ("EICMA: pedane e impatto.","Pedane portanti per i mezzi, illuminazione d'effetto, grandi grafiche e spazi per un pubblico numeroso."),
  ("Host: impianti funzionanti.","Attrezzature professionali in funzione richiedono allacci elettrici adeguati e, spesso, acqua e scarichi da prevedere nel progetto."),
  ("Logistica a Rho.","Orari di accesso, pass dei montatori e prenotazione degli scarichi vanno organizzati con anticipo: ce ne occupiamo noi.")],
 qa=[("Allestite stand per il Salone del Mobile?","Sì, abbiamo allestito stand al Salone del Mobile, dove progettazione e finiture fanno la differenza."),
  ("Lavorate anche per congressi ed eventi a Milano?","Sì, oltre a Fiera Milano Rho allestiamo eventi e congressi in città. Vedi anche <a href=\"/allestimenti-eventi-showroom-negozi/\">allestimenti per eventi</a>.")]),
dict(s="bologna",c="Bologna",q="BolognaFiere",gia=["Cosmoprof","Cersaie","EIMA"],altre=["Arte Fiera","Marca"],
 lead="Allestimenti fieristici a Bologna: stand per BolognaFiere, dal Cosmoprof al Cersaie e all'EIMA. Progetto, materiali, componentistica, grafica, impianti e montatori direttamente in fiera.",
 intro=["BolognaFiere ospita alcune delle fiere internazionali più importanti dei rispettivi settori, con espositori e visitatori da tutto il mondo. È anche una delle sedi dove lavoriamo di più con aziende straniere che espongono in Italia.",
  "Abbiamo allestito stand al Cosmoprof, al Cersaie e all'EIMA. Al Cosmoprof contano luce ed esposizione del prodotto; al Cersaie le pareti devono portare ceramiche e ambientazioni complete; all'EIMA servono spazi ampi e pavimenti per macchine di grandi dimensioni."],
 sapere=[("Cosmoprof: prodotto in vetrina.","Espositori illuminati, banchi per dimostrazioni, magazzino per campioni: la cura del dettaglio fa la differenza fra migliaia di marchi."),
  ("Cersaie: pareti portanti.","Piastrelle, lastre e arredobagno richiedono strutture robuste e ambientazioni realistiche, costruite su misura."),
  ("EIMA: grandi macchine.","Pedane e pavimentazioni portanti, aree ampie e logistica per mezzi di grandi dimensioni."),
  ("Espositori internazionali.","Seguiamo anche aziende straniere: possono scriverci nella loro lingua e affidarci tutto, dalla fornitura al montaggio.")],
 qa=[("Allestite stand per il Cosmoprof?","Sì, abbiamo allestito stand al Cosmoprof, con espositori illuminati, aree dimostrative e magazzino campioni."),
  ("Lavorate con aziende straniere che espongono a Bologna?","Sì, è una parte importante del nostro lavoro: abbiamo pagine in inglese, tedesco, francese, spagnolo, cinese, turco e arabo.")]),
dict(s="padova",c="Padova",q="Fiera di Padova",gia=[],altre=["Fiere di settore","Congressi","Eventi aziendali"],
 lead="Allestimenti fieristici a Padova: stand, congressi ed eventi alla Fiera di Padova e in città. Progetto, materiali, componentistica, grafica e montatori, con un fornitore veneto e un unico referente.",
 intro=["Padova è un polo fieristico e congressuale nel cuore del Veneto, con un quartiere fieristico a ridosso del centro e spazi pensati sia per fiere sia per congressi ed eventi aziendali.",
  "Essere in Veneto per noi significa tempi rapidi: sopralluoghi facili, consegne veloci e la possibilità di intervenire anche con poco preavviso. A Padova allestiamo stand fieristici, aree per congressi e convention, desk di accoglienza, fondali e spazi sponsor."],
 sapere=[("Fiere e congressi insieme.","Molti eventi padovani combinano area espositiva e sala congressi: progettiamo stand, fondali, palchi e segnaletica come un unico allestimento."),
  ("Tempi rapidi.","Essendo in Veneto riusciamo a seguire anche richieste urgenti e modifiche dell'ultimo momento."),
  ("Stand riutilizzabili.","Per chi espone più volte in regione, uno stand modulare di proprietà conservato nel nostro magazzino abbatte il costo per fiera.")],
 qa=[("Allestite anche congressi a Padova?","Sì: aree espositive per sponsor, desk di accoglienza, fondali, palchi, segnaletica, luci e schermi."),
  ("Potete intervenire con poco preavviso a Padova?","Sì, accettiamo richieste urgenti e in Veneto i tempi logistici sono brevi.")]),
dict(s="vicenza",c="Vicenza",q="Fiera di Vicenza",gia=[],altre=["VicenzaOro","T.Gold"],
 lead="Allestimenti fieristici a Vicenza: stand per la Fiera di Vicenza e per VicenzaOro. Vetrine, illuminazione per preziosi, salottini riservati, grafica e montatori in fiera, con un fornitore veneto.",
 intro=["Il quartiere fieristico di Vicenza è legato a doppio filo all'oreficeria e alla gioielleria: VicenzaOro è un appuntamento di riferimento internazionale per il settore, accanto a T.Gold dedicata a macchinari e tecnologie per la lavorazione dei preziosi.",
  "Uno stand per la gioielleria ha esigenze tutte sue: vetrine che proteggono e allo stesso tempo mettono in risalto, luce studiata sul metallo e sulle pietre, spazi riservati dove trattare con i buyer in tranquillità."],
 sapere=[("Vetrine e sicurezza.","Teche e vetrine progettate per esporre in sicurezza, integrate nello stand."),
  ("Luce per i preziosi.","Illuminazione puntuale e temperatura di colore pensate per far brillare metalli e pietre."),
  ("Salottini riservati.","Aree chiuse o semichiuse per le trattative con i buyer, spesso internazionali."),
  ("Veneto, tempi rapidi.","Siamo in regione: sopralluoghi, consegne e interventi veloci.")],
 qa=[("Allestite stand per VicenzaOro?","Sì: vetrine, illuminazione per preziosi, salottini per le trattative, grafica e montaggio in fiera."),
  ("Potete progettare vetrine su misura per la gioielleria?","Sì, nello stand su misura integriamo vetrine e teche progettate sul tuo prodotto.")]),
dict(s="pordenone",c="Pordenone",q="Pordenone Fiere",gia=["Sicam","Samuexpo"],altre=["Ortogiardino"],
 lead="Allestimenti fieristici a Pordenone: stand per Pordenone Fiere, dal Sicam al Samuexpo. Siamo a pochi chilometri, a Mansuè: progetto, materiali, componentistica e montatori in fiera.",
 intro=["Pordenone Fiere è la fiera più vicina alla nostra sede di Mansuè: pochi chilometri, che per chi espone significano sopralluoghi semplici, consegne rapide e interventi immediati anche durante la manifestazione.",
  "Abbiamo allestito stand al Sicam, la fiera internazionale dei componenti, accessori e semilavorati per l'industria del mobile, e al Samuexpo, dedicata a meccanica, subfornitura e lavorazioni industriali. Fiere tecniche, dove lo stand deve far vedere il prodotto da vicino e ospitare incontri con clienti e fornitori."],
 sapere=[("Sicam: il prodotto da toccare.","Ferramenta, componenti, finiture e materiali si espongono su pareti attrezzate e campionari pensati per essere maneggiati."),
  ("Samuexpo: macchine e pesi.","Pedane portanti, allacci elettrici adeguati e logistica per macchinari in esposizione."),
  ("Sede a pochi chilometri.","Possiamo intervenire in tempi brevissimi, anche durante la fiera."),
  ("Per le aziende del territorio.","Friuli e Veneto orientale sono la nostra zona: conosciamo il distretto del mobile e la meccanica locale.")],
 qa=[("Allestite stand per il Sicam?","Sì, abbiamo allestito stand al Sicam, con pareti attrezzate, campionari, aree incontri, grafica e montaggio."),
  ("Siete vicini a Pordenone Fiere?","Sì, la nostra sede è a Mansuè, in provincia di Treviso, a pochi chilometri dal quartiere fieristico.")]),
dict(s="rimini",c="Rimini",q="Rimini Expo Centre",gia=[],altre=["Sigep","Ecomondo","TTG Travel Experience","RiminiWellness"],
 lead="Allestimenti fieristici a Rimini: stand per il Rimini Expo Centre, dal Sigep a Ecomondo e TTG. Progetto, materiali, componentistica, impianti e montatori direttamente in fiera.",
 intro=["Il Rimini Expo Centre ospita fiere di settori molto diversi: dal food service del Sigep (gelateria, pasticceria, panificazione e caffè) all'economia circolare di Ecomondo, dal turismo del TTG al fitness di RiminiWellness.",
  "Ognuna ha esigenze proprie. Nelle fiere del food le macchine sono in funzione e servono impianti adeguati; in quelle del turismo lo stand è un racconto per immagini; nel wellness conta lo spazio per dimostrazioni e pubblico."],
 sapere=[("Sigep: attrezzature in funzione.","Allacci elettrici e idrici, scarichi, banchi di lavoro e aree di assaggio da prevedere fin dal progetto."),
  ("Ecomondo: materiali coerenti.","Per chi espone sull'ambiente, materiali riutilizzabili e stand modulari sono anche un messaggio."),
  ("TTG: immagini grandi.","Grafiche in tessuto teso e ledwall per raccontare destinazioni ed esperienze."),
  ("Pubblico numeroso.","Percorsi, desk di accoglienza e spazi per incontri riservati.")],
 qa=[("Allestite stand per il Sigep?","Sì: banchi di lavoro, aree assaggio, impianti per macchine in funzione, grafica e montaggio in fiera."),
  ("Avete soluzioni riutilizzabili per fiere come Ecomondo?","Sì, gli stand modulari in alluminio e tessuto teso si riutilizzano per anni e riducono materiali e trasporti.")]),
dict(s="parma",c="Parma",q="Fiere di Parma",gia=[],altre=["Cibus","Mercanteinfiera"],
 lead="Allestimenti fieristici a Parma: stand per Fiere di Parma, dal Cibus al Mercanteinfiera. Progetto, materiali, componentistica, grafica, impianti e montatori direttamente in fiera.",
 intro=["Fiere di Parma è il quartiere fieristico della food valley italiana: il Cibus è uno degli appuntamenti di riferimento per l'agroalimentare, con buyer della grande distribuzione e dell'export. Accanto, manifestazioni come Mercanteinfiera dedicate ad antiquariato, modernariato e collezionismo.",
  "Uno stand alimentare deve far assaggiare, conservare e presentare il prodotto nelle condizioni giuste; uno stand d'antiquariato deve valorizzare pezzi unici, con luce e spazi che li facciano respirare."],
 sapere=[("Cibus: assaggi e frigoriferi.","Banchi refrigerati, aree di preparazione e assaggio, magazzino e spazi per incontri con i buyer."),
  ("Export e buyer esteri.","Grafiche bilingui e salottini per trattative, e se vuoi una pagina in inglese per prenotare gli appuntamenti."),
  ("Antiquariato: luce e respiro.","Pannellature neutre, illuminazione puntuale e basamenti per valorizzare i pezzi."),
  ("Stand riutilizzabili.","Per chi fa più fiere del food in Italia e in Europa, uno stand modulare di proprietà riduce i costi.")],
 qa=[("Allestite stand per il Cibus?","Sì: banchi refrigerati, aree assaggio, magazzino, salottini per buyer, grafica e montaggio in fiera."),
  ("Fate anche allestimenti per antiquariato e collezionismo?","Sì, con pannellature, basamenti e illuminazione dedicata. Vedi anche <a href=\"/allestimenti-eventi-showroom-negozi/\">mostre e allestimenti</a>.")]),
]
GEN=[("Accettate richieste urgenti?","Sì, anche a ridosso della fiera: lavoriamo con una rete di montatori partner e valutiamo subito cosa è possibile fare."),
 ("Lo stand è a noleggio o in acquisto?","Tutti e due: stand preallestiti, modulari, in tessuto teso e su misura, a noleggio o di tua proprietà. Se è tuo, possiamo conservarlo in magazzino per la prossima fiera."),
 ("Quanto costa uno stand?","Dipende da metratura, struttura, finiture, impianti e logistica. Ti mandiamo un preventivo su misura voce per voce; nella <a href=\"/quanto-costa-uno-stand-fieristico/\">guida ai costi</a> trovi le voci principali.")]
for d in C:
    c=d['c']; P=f"/allestimenti-fieristici-{d['s']}/"
    m=hero(f"Allestimenti fieristici · {c}",f'Allestimenti fieristici a {c}: <span class="grad">stand chiavi in mano</span> a {d["q"]}.',d['lead'],
      f"Preventivo per uno stand a {c}",CT,"Cosa facciamo","#cosa")
    m+=testo("citta",f"Stand a {c}, <span class=\"grad\">dal progetto al montaggio</span>",None,d['intro'])
    fl=[(f+" ✓",FIERA_URL.get(N2S.get(f,''))) for f in d['gia']]+[(f,FIERA_URL.get(N2S.get(f,''))) for f in d['altre']]
    m+=chips("fiere",f"Fiere a {c}",("Con ✓ le manifestazioni in cui abbiamo già allestito stand." if d['gia'] else f"Alcune delle manifestazioni che si tengono a {c}."),fl)
    evs=[f for f in DC.F if DC.V[f[2]][1]==c]
    if evs:
        lis=[(f[1],DC.quando(f[0])+(f" · <a href=\"{FIERA_URL[k]}\">stand per {f[1].split(' (')[0]}</a>" if (k:=next((x for x,_ in FIERA_PAGES if f[0].startswith(x)),None)) else "")) for f in sorted(evs,key=lambda f:f[4])]
        m+=testo("calendario",f"Prossime fiere a {c}",f"Date pubblicate dagli organizzatori, aggiornate all'8 ottobre 2026. Tutte le fiere d'Italia e d'Europa sono nel <a href=\"{CAL}\">calendario fiere con mappa</a>.",[],lis)
    m+=testo("sapere",f"Cosa sapere per uno stand a {c}",None,[],d['sapere'])
    m+=cards("cosa","Cosa facciamo per il tuo stand",None,
     [("Progetto e render 3D","Lo stand disegnato sulla tua metratura e sulla posizione nel padiglione, prima di costruirlo."),
      ("Materiali e componentistica",f"Troviamo e portiamo a {d['q']} tutto il materiale e la componentistica richiesti dal progetto e dal regolamento."),
      ("Grafica, luci e impianti","Grafica e stampa, impianto elettrico con dichiarazione di conformità, illuminazione, moquette, schermi e LED."),
      ("Montatori in fiera","Montatori partner, gestiti da noi, che montano lo stand nei tempi di allestimento e lo smontano a fine fiera."),
      ("Noleggio o acquisto","Stand preallestiti, modulari, in tessuto teso o su misura, a noleggio o di proprietà."),
      ("Trasporto, magazzino, pratiche","Logistica, magazzino fra una fiera e l'altra, approvazione del progetto, pass e orari di carico.")])
    qa=d['qa']+GEN
    m+=faq(FAQ_EY,FAQ_T,qa)
    m+=cta(f"Esponi a {c}?","Dicci quale fiera, le date e la metratura: ti rispondiamo con quello che serve e quanto costa.","Richiedi un preventivo gratuito",CT)
    m+=altri("Altre città e servizi",related(P))
    node=service_node(SITE+P,f"Allestimenti fieristici a {c}","Allestimento e montaggio di stand fieristici",
      f"Progettazione, fornitura di materiali e componentistica, grafica, impianti, montaggio e smontaggio di stand fieristici a {c} ({d['q']}).",
      [{"@type":"City","name":c}],["Stand preallestiti","Stand modulari","Stand su misura","Montaggio e smontaggio in fiera","Noleggio stand e arredi"],'it')
    node["location"]={"@type":"Place","name":d['q'],"address":{"@type":"PostalAddress","addressLocality":c,"addressCountry":"IT"}}
    del node["location"]  # Service non ammette location: la sede fiera sta nella descrizione
    _t=f"Allestimenti fieristici a {c}: stand a {d['q']}"
    _t=_t+" | Danova Tech" if len(_t)<=51 else _t
    print(build('it',P,_t,
      f"Allestimenti fieristici a {c}: stand chiavi in mano a {d['q']}. Progetto 3D, grafica, impianti e montatori in fiera, a noleggio o in acquisto.",
      f"Allestimenti fieristici a {c} — Danova Tech",f"Stand chiavi in mano a {d['q']}: progetto, materiali, componentistica e montatori in fiera.",
      [("Home","/"),("Allestimenti fieristici",PILLAR),(c,None)],m,qa,[node]))
