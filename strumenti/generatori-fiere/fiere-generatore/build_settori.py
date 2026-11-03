# -*- coding: utf-8 -*-
# Pagine settori merceologici (uso: python3 build_settori.py)
from nuove_common import *
def fiere_settore(keys):
    """chips con le fiere del settore dal calendario: pagina dedicata se c'e', altrimenti calendario"""
    out=[];seen=set()
    for f in sorted(DC.F,key=lambda f:f[4]):
        if f[3] not in keys: continue
        k=next((x for x,_ in FIERA_PAGES if f[0].startswith(x)),None)
        nome=f[1].split(' (')[0]
        if nome in seen: continue
        seen.add(nome)
        out.append((f"{nome} · {DC.V[f[2]][1]}",FIERA_URL[k] if k else None))
    return out
def S(P,title,desc,ey,h1,lead,keys,cardsT,cardsL,testoT,paras,lista,qa,offers,rel,ogd):
    m=hero(ey,h1,lead,"Richiedi un preventivo","#richiesta","Le fiere del settore","#fiere")
    m+=cards("cosa",cardsT,None,cardsL)
    m+=testo("settore",testoT,None,paras,lista)
    m+=chips("fiere","Le fiere del settore in Italia e in Europa",f"Prossime edizioni dal nostro <a href=\"{CAL}\">calendario fiere</a>. Dove c'è il link trovi una pagina dedicata allo stand.",fiere_settore(keys))
    m+=cards("servizi","Cosa facciamo per il tuo stand",None,SERVIZI_CARDS(""))
    name=strip_tags(h1).rstrip('.').split(':')[0]
    fr=[(t,u) for t,u in fiere_settore(keys) if u]
    pagina(P,title,desc,f"{name} — Danova Tech",ogd,crumbs(name),m,qa,[svc(P,name,"Allestimento di stand fieristici per settore",ogd,offers)],rel+fr+[("Calendario fiere 2026–2027",CAL),("Allestimenti fieristici",PILLAR)]+SETTORI_LINKS)
    print(len(title),P)

S("/stand-fieristici-food-e-vino/","Stand fieristici per food e vino | Danova Tech",
 "Stand per aziende alimentari, cantine e distillerie: banchi di degustazione, frigoriferi, aree assaggio, magazzino e montaggio a Vinitaly, Cibus, Sigep, ProWein e nelle fiere food in Europa.",
 "Settore food & wine",'Stand fieristici per <span class="grad">food e vino</span>.',
 "Nelle fiere del food e del vino lo stand è un luogo di lavoro: si assaggia, si conserva il prodotto alla temperatura giusta, si incontrano buyer della distribuzione e importatori. Progettiamo stand che funzionano per quattro giorni di degustazioni e appuntamenti, con l'immagine curata del tuo marchio.",
 ['food','vino'],"Cosa serve a uno stand food o wine",
 [("Degustazione","Banchi di mescita, sputavino, lavabicchieri, piani di lavoro per tagliare e servire."),
  ("Freddo","Frigoriferi, cantinette e banchi refrigerati con la potenza elettrica calcolata."),
  ("Magazzino","Ripostiglio chiuso per cartoni, bottiglie, stoviglie e materiali."),
  ("Incontri","Tavoli e salottini per buyer e importatori, separati dalla zona assaggi."),
  ("Igiene","Superfici lavabili, lavelli, acqua e scarichi dove servono."),
  ("Collettive","Postazioni coordinate per consorzi, regioni e associazioni di produttori.")],
 "Stand che lavorano, non solo vetrine",
 ["Le fiere del settore sono molto diverse fra loro: a Vinitaly e ProWein contano degustazione e appuntamenti, a Cibus, Anuga e SIAL il rapporto con la grande distribuzione e l'export, al Sigep e a Host le macchine in funzione e le dimostrazioni dal vivo. Il progetto parte da come lavorerai allo stand, non da come apparirà in foto.",
  "Per chi fa più fiere food in Italia e in Europa conviene spesso uno stand modulare di proprietà, conservato nel nostro magazzino e riconfigurato di volta in volta, con frigoriferi e attrezzature a noleggio."],
 [("Vino e distillati.","Vedi <a href=\"/stand-vinitaly/\">stand per Vinitaly</a>."),("Agroalimentare.","Vedi <a href=\"/stand-cibus/\">stand per Cibus</a>."),
  ("Foodservice e ospitalità.","Vedi <a href=\"/stand-sigep/\">Sigep</a> e <a href=\"/stand-host/\">Host</a>.")],
 [("Fornite frigoriferi e attrezzature per la degustazione?","Sì, a noleggio insieme allo stand: frigoriferi, cantinette, banchi refrigerati, lavabicchieri, sputavino."),
  ("Potete portare acqua e scarichi nello stand?","Sì, li prevediamo nel progetto e li coordiniamo con i servizi tecnici della fiera."),
  ("Allestite stand collettivi per consorzi?","Sì, con postazioni coordinate, grafica comune e aree condivise."),
  ("Lavorate anche nelle fiere food all'estero?","Sì: ProWein, Anuga, SIAL, Wine Paris, Biofach e le altre fiere europee del settore.")],
 ["Stand per cantine e aziende alimentari","Attrezzature per degustazione a noleggio","Stand collettivi per consorzi","Montaggio in fiera in Italia e all'estero"],
 [("Stand Vinitaly","/stand-vinitaly/"),("Stand Cibus","/stand-cibus/")],
 "Stand per food e vino: degustazione, frigoriferi, aree assaggio, magazzino e montaggio nelle fiere italiane ed europee.")

S("/stand-fieristici-arredo-e-design/","Stand fieristici per arredo e design | Danova Tech",
 "Stand per aziende di arredamento, illuminazione e componenti per il mobile: ambientazioni, finiture di livello, luce, montaggio al Salone del Mobile, Sicam, imm cologne e nelle fiere del settore.",
 "Settore arredo e design",'Stand fieristici per <span class="grad">arredo e design</span>.',
 "Nelle fiere dell'arredo lo stand viene giudicato come un prodotto: proporzioni, materiali, finiture e luce. Progettiamo ambientazioni in cui il mobile si vede in uso, con dettagli costruttivi all'altezza del pubblico di progettisti e rivenditori che le visita.",
 ['arredo'],"Cosa serve a uno stand per l'arredo",
 [("Ambientazioni","Pareti, controsoffitti e pavimenti che ricostruiscono una casa, un ufficio, un hotel."),
  ("Finiture","Laccature, impiallacciati, tessuti e metalli scelti come per un interno di pregio."),
  ("Luce","Progetto illuminotecnico sui materiali, integrazione delle lampade per chi espone illuminazione."),
  ("Campionari","Pareti attrezzate per componenti, ferramenta e finiture, per le fiere di fornitura."),
  ("Materiali certificati","Reazione al fuoco e documentazione per l'ente fiera."),
  ("Riuso","Elementi pensati per tornare in fiera o in showroom dopo la manifestazione.")],
 "Dal Salone del Mobile alle fiere della fornitura",
 ["Il settore ha fiere molto diverse: il Salone del Mobile e imm cologne per il prodotto finito, Sicam e interzum per componenti e semilavorati, Ambiente, Heimtextil e Maison&Objet per complemento e tessile, Arredamont per l'arredo di montagna. Ognuna ha un pubblico e un modo di visitare lo stand.",
  "Spesso gli elementi più curati dello stand possono vivere oltre la fiera: in showroom, in un evento del Fuorisalone, in un negozio. Lo teniamo presente fin dal progetto."],
 [("Prodotto finito.","Vedi <a href=\"/stand-salone-del-mobile/\">stand per il Salone del Mobile</a>."),("Componenti.","Vedi <a href=\"/stand-sicam/\">stand per Sicam</a>."),
  ("Showroom ed eventi.","Vedi <a href=\"/allestimenti-eventi-showroom-negozi/\">allestimenti per showroom</a>.")],
 [("Realizzate ambientazioni complete con controsoffitti e pavimenti?","Sì, costruite su misura e montate in fiera, con impianti e luci integrati."),
  ("Usate materiali certificati per la reazione al fuoco?","Sì, come richiesto dai regolamenti tecnici, con la documentazione per l'ente fiera."),
  ("Gli elementi dello stand si possono riutilizzare in showroom?","Sì, se li progettiamo con questo obiettivo."),
  ("Lavorate anche nelle fiere dell'arredo all'estero?","Sì: imm cologne, interzum, Ambiente, Heimtextil, Maison&Objet.")],
 ["Stand per aziende di arredamento","Ambientazioni e finiture su misura","Stand per componenti del mobile","Montaggio in fiera in Italia e all'estero"],
 [("Stand Salone del Mobile","/stand-salone-del-mobile/"),("Stand Sicam","/stand-sicam/"),("Stand su misura","/stand-fieristici-su-misura/")],
 "Stand per arredo e design: ambientazioni, finiture, luce e montaggio nelle fiere italiane ed europee del settore.")

S("/stand-fieristici-meccanica-e-industria/","Stand fieristici per meccanica e industria | Danova Tech",
 "Stand per aziende meccaniche, subfornitura, automazione e packaging: pedane per macchinari, allacci, schermi, sale incontri e montaggio a EMO, MECSPE, Lamiera, Hannover Messe e nelle fiere industriali.",
 "Settore meccanica e industria",'Stand fieristici per <span class="grad">meccanica e industria</span>.',
 "Nelle fiere industriali il visitatore è un tecnico: vuole vedere la macchina, il pezzo, la tolleranza. Progettiamo stand che espongono macchinari in sicurezza, spiegano processi con schermi e campioni e danno spazio agli incontri tecnici, con l'organizzazione che richiedono carichi e impianti.",
 ['industria','pack','tech'],"Cosa serve a uno stand industriale",
 [("Pedane e basamenti","Calcolati sul peso dei macchinari, con protezioni e distanze di sicurezza."),
  ("Allacci","Potenza elettrica, aria compressa e dati per le macchine in funzione."),
  ("Campioni e vetrine","Pezzi lavorati esposti e illuminati per mostrare finiture e precisione."),
  ("Schermi","Ledwall e monitor per impianti, reparti e lavorazioni che non entrano in fiera."),
  ("Sale tecniche","Tavoli e salette per discutere disegni, lotti e tempi."),
  ("Logistica pesante","Consegne con mezzi di sollevamento coordinate con l'ente fiera.")],
 "Stand che reggono il peso, letteralmente",
 ["Nelle fiere della meccanica il progetto dello stand comincia dai dati tecnici: pesi, ingombri, potenze, aria compressa. Li raccogliamo all'inizio, dimensioniamo pedane e impianti e presentiamo all'ente fiera tutto quello che serve, così la macchina arriva e si accende.",
  "Molte aziende industriali espongono in più fiere in Italia ed Europa: EMO, MECSPE, Lamiera, Samuexpo, Hannover Messe, LIGNA, FachPack. Uno stand modulare di proprietà, conservato nel nostro magazzino, riduce costi e tempi a ogni edizione."],
 [("Subfornitura.","Vedi <a href=\"/stand-samuexpo/\">stand per Samuexpo</a>."),("Macchine agricole.","Vedi <a href=\"/stand-eima/\">stand per EIMA</a>."),
  ("Fiere estere.","Vedi <a href=\"/allestimenti-fieristici-estero/\">stand all'estero</a>.")],
 [("Potete esporre macchinari in funzione?","Sì, con basamenti, protezioni, potenza elettrica e aria compressa previsti nel progetto e approvati dall'ente fiera."),
  ("Gestite carico e scarico dei macchinari?","Coordiniamo consegne, orari e mezzi di sollevamento con l'ente fiera."),
  ("Fate stand riutilizzabili per più fiere industriali?","Sì, con strutture modulari conservate nel nostro magazzino."),
  ("Lavorate nelle fiere industriali tedesche?","Sì: Hannover Messe, LIGNA, Formnext, productronica e le altre. Le date sono nel <a href=\"/calendario-fiere/\">calendario</a>.")],
 ["Stand per aziende meccaniche","Pedane e allacci per macchinari","Stand modulari per fiere industriali","Montaggio in fiera in Italia e all'estero"],
 [("Stand Samuexpo","/stand-samuexpo/"),("Stand EIMA","/stand-eima/"),("Stand modulari","/stand-modulari/")],
 "Stand per meccanica e industria: pedane per macchinari, allacci, schermi, sale tecniche e montaggio in fiera.")

S("/stand-fieristici-moda-e-calzature/","Stand fieristici per moda, calzature e gioielli | Danova Tech",
 "Stand per moda, calzature, occhialeria e gioielleria: allestimenti da boutique, espositori, luce per tessuti e preziosi, montaggio a Pitti, MICAM, MIDO, VicenzaOro, Expo Riva Schuh.",
 "Settore moda e accessori",'Stand fieristici per <span class="grad">moda, calzature e gioielli</span>.',
 "Nelle fiere della moda lo stand è una boutique temporanea: deve raccontare la collezione, esporre molti articoli con ordine, valorizzare tessuti, pellami e metalli con la luce giusta e far lavorare bene i venditori con i buyer.",
 ['moda','gioielli'],"Cosa serve a uno stand per la moda",
 [("Espositori","Appendiabiti, mensole, nicchie, teche e manichini progettati sulla collezione."),
  ("Luce","Resa cromatica alta e temperatura colore scelta su tessuti, pellami o preziosi."),
  ("Tavoli ordini","Postazioni comode per sessioni lunghe di selezione e ordine."),
  ("Magazzino campionario","Retro chiuso per scatole, campioni e taglie."),
  ("Sicurezza","Teche con chiusura per occhiali, orologi e gioielli."),
  ("Riallestimento","Due stagioni l'anno: struttura di proprietà, grafiche nuove.")],
 "Una boutique, due volte l'anno",
 ["Molte fiere del settore hanno due edizioni l'anno: Pitti Uomo, MICAM, Expo Riva Schuh, VicenzaOro. La soluzione più efficiente è uno stand di proprietà, conservato nel nostro magazzino e riallestito a ogni stagione con grafiche e disposizione nuove.",
  "Ogni prodotto chiede la sua luce: i tessuti vogliono luce morbida e fedele al colore, i pellami una luce che ne mostri la grana, i gioielli faretti puntuali che facciano brillare metalli e pietre senza riflessi."],
 [("Abbigliamento.","Vedi <a href=\"/stand-pitti-uomo/\">stand per Pitti Uomo</a>."),("Calzature.","Vedi <a href=\"/stand-micam/\">MICAM</a> ed <a href=\"/stand-expo-riva-schuh/\">Expo Riva Schuh</a>."),
  ("Occhiali e gioielli.","Vedi <a href=\"/stand-mido/\">MIDO</a> e <a href=\"/stand-vicenzaoro/\">VicenzaOro</a>.")],
 [("Potete conservare lo stand tra un'edizione e l'altra?","Sì, lo teniamo nel nostro magazzino e lo riportiamo in fiera con grafiche aggiornate."),
  ("Realizzate vetrine di sicurezza per gioielli e orologi?","Sì, teche con chiusura integrate negli arredi."),
  ("Che luce usate per i tessuti?","LED ad alta resa cromatica, con temperatura colore scelta sulla collezione."),
  ("Lavorate anche nelle fiere della moda all'estero?","Sì: Première Vision, Silmo, Watches and Wonders e le altre. Le date sono nel <a href=\"/calendario-fiere/\">calendario</a>.")],
 ["Stand per moda e abbigliamento","Stand per calzature e pelletteria","Teche per occhialeria e gioielleria","Magazzino e riallestimento stagionale"],
 [("Stand Pitti Uomo","/stand-pitti-uomo/"),("Stand MICAM","/stand-micam/")],
 "Stand per moda, calzature, occhialeria e gioielli: espositori, luce, tavoli ordini, teche e riallestimento stagionale.")

S("/stand-fieristici-cosmetica-e-beauty/","Stand fieristici per cosmetica e beauty | Danova Tech",
 "Stand per cosmetica, profumeria, estetica e packaging: espositori illuminati, postazioni per dimostrazioni con acqua, magazzino campioni e montaggio a Cosmoprof, in-cosmetics e nelle fiere beauty.",
 "Settore cosmetica",'Stand fieristici per <span class="grad">cosmetica e beauty</span>.',
 "Il prodotto cosmetico vince in fiera se si vede bene e si può provare. Progettiamo stand con espositori illuminati e fedeli al colore, postazioni per trattamenti e dimostrazioni, magazzino per i campioni e spazi riservati per gli incontri con distributori e buyer.",
 ['beauty'],"Cosa serve a uno stand beauty",
 [("Espositori illuminati","Mensole retroilluminate e teche con luce ad alta resa cromatica."),
  ("Postazioni demo","Trucco, piega, manicure, trattamenti: con acqua, scarichi ed elettricità."),
  ("Tester e campioni","Banchi per provare i prodotti e magazzino per i campioni."),
  ("Area B2B","Tavoli per distributori, catene e buyer internazionali."),
  ("Conto terzi e packaging","Schermi e campionari per chi presenta formulazioni, impianti e confezionamento."),
  ("Grafica pulita","Fondali essenziali, prodotto e packaging al centro.")],
 "Luce giusta, prodotto vero",
 ["In cosmetica il colore è il prodotto: un rossetto o un fondotinta illuminato male in fiera sembra un altro. Per questo scegliamo LED ad alta resa cromatica e temperature colore studiate sul packaging e sulle texture.",
  "Le linee professionali hanno bisogno di lavorare dal vivo: lavatesta, poltrone, specchi, postazioni manicure. Prevediamo acqua, scarichi e potenze elettriche nel progetto e li coordiniamo con i servizi tecnici della fiera."],
 [("Cosmoprof.","Vedi <a href=\"/stand-cosmoprof/\">stand per Cosmoprof</a>."),("Packaging.","Vedi <a href=\"/stand-fieristici-meccanica-e-industria/\">stand per l'industria</a>.")],
 [("Potete realizzare postazioni con lavatesta?","Sì, con allacci idrici e scarichi coordinati con la fiera."),
  ("Che luce usate per i cosmetici?","LED ad alta resa cromatica, con temperatura colore scelta sul prodotto."),
  ("Fate stand riutilizzabili per le edizioni estere?","Sì, con strutture modulari che si riconfigurano su metrature diverse."),
  ("Lavorate a in-cosmetics e nelle fiere beauty europee?","Sì, le date sono nel <a href=\"/calendario-fiere/\">calendario fiere</a>.")],
 ["Stand per cosmetica e profumeria","Postazioni per dimostrazioni","Espositori illuminati","Montaggio in fiera in Italia e all'estero"],
 [("Stand Cosmoprof","/stand-cosmoprof/"),("Ledwall e illuminazione","/ledwall-e-illuminazione-stand/")],
 "Stand per cosmetica e beauty: espositori illuminati, postazioni per dimostrazioni, magazzino campioni e area B2B.")

S("/stand-fieristici-agricoltura/","Stand fieristici per agricoltura e zootecnia | Danova Tech",
 "Stand per macchine agricole, zootecnia, ortofrutta e filiera agricola: pedane per mezzi pesanti, aree incontri per dealer, montaggio a EIMA, Fieracavalli, Macfrut, EuroTier, Agritechnica.",
 "Settore agricoltura",'Stand fieristici per <span class="grad">agricoltura e zootecnia</span>.',
 "Le fiere agricole mettono insieme mezzi di grandi dimensioni, un pubblico di agricoltori e allevatori e una rete di dealer da incontrare. Progettiamo stand che espongono trattori e attrezzature in sicurezza e accolgono bene clienti e rivenditori.",
 ['agri'],"Cosa serve a uno stand agricolo",
 [("Pedane per mezzi","Pavimentazioni e pedane portanti con rampe per trattori e macchine."),
  ("Grandi superfici","Stand a isola ampi, con percorsi chiari fra i mezzi."),
  ("Area dealer","Uffici e salottini per la rete commerciale, anche su un secondo livello."),
  ("Ortofrutta","Esposizione del fresco e refrigerazione per le fiere della filiera."),
  ("Aree esterne","Strutture per esposizioni all'aperto, dove previste."),
  ("Segnaletica","Insegne alte e schede prodotto vicino a ogni macchina.")],
 "Dai trattori alla frutta fresca",
 ["Il settore va dalle grandi fiere della meccanizzazione, come EIMA e Agritechnica, a quelle della zootecnia come EuroTier e Fieracavalli, fino all'ortofrutta di Macfrut, Fruit Logistica e Fruit Attraction. Esigenze diverse, un elemento comune: carichi pesanti e logistica da organizzare con anticipo.",
  "Siamo abituati a coordinare l'ingresso dei mezzi nei padiglioni con l'ente fiera e a dimensionare pedane e pavimentazioni sui pesi reali."],
 [("Macchine agricole.","Vedi <a href=\"/stand-eima/\">stand per EIMA</a>."),("Ortofrutta.","Vedi <a href=\"/stand-macfrut/\">stand per Macfrut</a>."),
  ("Mondo del cavallo.","Vedi <a href=\"/stand-fieracavalli/\">stand per Fieracavalli</a>.")],
 [("Le pedane reggono trattori e mezzi pesanti?","Sì, le dimensioniamo sui pesi reali, con rampe e protezioni."),
  ("Allestite stand per fiere agricole all'estero?","Sì: Agritechnica, EuroTier, Fruit Logistica, Fruit Attraction. Le date sono nel <a href=\"/calendario-fiere/\">calendario</a>."),
  ("Potete fare uno stand a due piani per i dealer?","Sì, dove il regolamento lo consente. Vedi <a href=\"/stand-a-due-piani/\">stand a due piani</a>."),
  ("Fate stand per fiere agricole locali?","Sì, anche per fiere come Agrimont a Longarone.")],
 ["Stand per macchine agricole","Pedane per mezzi pesanti","Stand per ortofrutta e zootecnia","Montaggio in fiera in Italia e all'estero"],
 [("Stand EIMA","/stand-eima/"),("Stand Macfrut","/stand-macfrut/"),("Stand a isola","/stand-a-isola/")],
 "Stand per agricoltura e zootecnia: pedane per mezzi pesanti, grandi stand a isola, aree dealer e montaggio in fiera.")
