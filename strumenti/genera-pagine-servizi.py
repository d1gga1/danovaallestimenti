#!/usr/bin/env python3
"""Genera le pagine di servizio non fieristiche (negozi, eventi, mostre, stand pubblicitari)
partendo dal modello allestimenti-eventi-showroom-negozi/index.html.

Uso (dalla cartella del sito):  python3 strumenti/genera-pagine-servizi.py [slug ...]
Riscrive solo le cartelle elencate in PAGINE. Ricerca parole chiave: strumenti/ricerca-parole-chiave-2026-11.md
"""
import html, json, os, re, struct, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODELLO = os.path.join(ROOT, "allestimenti-eventi-showroom-negozi", "index.html")
OGGI = "2026-11-06"
SITO = "https://danovastand.com"

e = html.escape


def webp_size(path):
    with open(path, "rb") as f:
        d = f.read(40)
    if d[12:16] == b"VP8X":
        w = 1 + int.from_bytes(d[24:27], "little"); h = 1 + int.from_bytes(d[27:30], "little"); return w, h
    if d[12:16] == b"VP8 ":
        w, h = struct.unpack("<HH", d[26:30]); return w & 0x3FFF, h & 0x3FFF
    if d[12:16] == b"VP8L":
        b = int.from_bytes(d[21:25], "little"); return (b & 0x3FFF) + 1, ((b >> 14) & 0x3FFF) + 1
    return 1600, 1063


PAGINE = [
    {
        "slug": "allestimento-vetrine",
        "title": "Allestimento vetrine natalizie e su misura | Danova Stand",
        "desc": "Allestimento vetrine per negozi: vetrine natalizie e stagionali, vetrine fisse su misura, vetrine per marchi ed eventi, grafiche e vetrofanie. Preventivo in 24 ore.",
        "og_title": "Allestimento vetrine per negozi — Danova Stand",
        "og_desc": "Vetrine natalizie e stagionali, strutture su misura, vetrine per lanci di prodotto, grafiche e vetrofanie: progetto, produzione e montaggio.",
        "crumb": "Allestimento vetrine",
        "img": "stand-vicenzaoro-gioielli",
        "alt": "Render di vetrina espositiva per gioielli con teche illuminate e fondale scuro",
        "caption": "Render di progetto: vetrina espositiva con teche, podi e luce dedicata al prodotto.",
        "eyebrow": "Vetrine per negozi e marchi",
        "h1": "Allestimento vetrine: <span class=\"grad\">natalizie, stagionali e su misura</span>.",
        "lead": "Vetrine per Natale, saldi e cambi di stagione, vetrine fisse costruite su misura, vetrine per lanci di prodotto e marchi, grafiche e vetrofanie. Progettiamo la vetrina in 3D vista dalla strada, la facciamo produrre e la montiamo noi, anche a negozio chiuso.",
        "breve": "Danova Stand allestisce vetrine per negozi in tutta Italia: vetrine natalizie e stagionali (Natale, saldi, San Valentino, primavera, estate, autunno), vetrine fisse su misura con fondali, podi, teche e illuminazione, vetrine sponsorizzate per marchi, lanci di prodotto ed eventi, grafiche e vetrofanie stampate e posate. Progetto e render 3D, produzione, montaggio e smontaggio con un unico referente. Preventivo gratuito entro 24 ore lavorative.",
        "service": "Allestimento vetrine per negozi",
        "service_type": "Allestimento vetrine (visual merchandising)",
        "cards_title": "Le vetrine che allestiamo",
        "cards": [
            ("Vetrine natalizie", "Allestimenti per Natale e le feste: fondali, strutture scenografiche, luci calde e decorazioni progettate sul marchio, non comprate a catalogo."),
            ("Vetrine stagionali e saldi", "Saldi, San Valentino, primavera, estate, rientro e autunno: una struttura base che resta e grafiche che cambiano a ogni stagione."),
            ("Vetrine fisse su misura", "Fondali, podi, mensole, teche e cornici costruiti sulle misure della vetrina, con illuminazione LED dedicata al prodotto."),
            ("Vetrine per marchi e lanci", "Vetrine sponsorizzate nei negozi dei rivenditori, lanci di prodotto ed eventi: uguali in ogni punto vendita, con istruzioni di montaggio."),
            ("Grafiche e vetrofanie", "Vetrofanie adesive, pellicole satinate, pannelli e tessuti stampati, stampati e posati da noi senza lasciare segni sul vetro."),
            ("Luci per la vetrina", "Faretti orientabili, strisce LED e retroilluminazioni che fanno vedere la merce di sera senza scaldarla."),
        ],
        "settori_title": "Idee per le vetrine, stagione per stagione",
        "settori": [
            ("Natale", "un fondale che crea profondità, luci calde a punti, prodotti su podi a diverse altezze e una sola idea forte invece di tante decorazioni."),
            ("Saldi", "grafica grande e leggibile dalla strada, percentuali chiare, struttura semplice che si monta in poche ore."),
            ("San Valentino e feste", "un colore dominante, pochi prodotti scelti e un elemento scenografico che si riusa cambiando solo la grafica."),
            ("Primavera ed estate", "colori chiari, materiali naturali come legno e tessuto, luce più fredda e prodotti in uso."),
            ("Autunno e rientro", "toni caldi, texture, vetrina che racconta la nuova collezione con fondale e mensole su misura."),
        ],
        "testo_title": "Una vetrina si giudica <span class=\"grad\">dalla strada, in tre secondi</span>",
        "testo": [
            "Chi passa davanti al negozio guarda la vetrina per pochi secondi: deve capire subito cosa vendi e avere un motivo per entrare. Per questo progettiamo la vetrina dal punto di vista di chi cammina sul marciapiede, con render 3D che mostrano altezze, profondità, riflessi del vetro e luce di sera.",
            "Lavoriamo come per gli stand fieristici: struttura costruita in laboratorio, grafica stampata sulle misure esatte, montaggio rapido con il negozio chiuso. La struttura base resta e si cambiano grafiche e decorazioni a ogni stagione, così ogni nuovo allestimento costa meno del precedente.",
        ],
        "passi": [
            ("Sopralluogo e misure", "dimensioni della vetrina, profondità, accessi, prese elettriche e vincoli del centro commerciale o del condominio."),
            ("Progetto e render 3D", "la vetrina vista dalla strada di giorno e di sera, con materiali, colori, luci e posizione dei prodotti. La approvi prima della produzione."),
            ("Produzione", "fondali, podi, strutture e teche realizzati da laboratori partner; grafiche e vetrofanie stampate sulle misure reali."),
            ("Montaggio", "nei giorni e negli orari che scegli tu, anche di notte o il giorno di chiusura, con un capocantiere che segue il lavoro."),
            ("Cambio di stagione", "conserviamo strutture e decorazioni nei nostri magazzini e torniamo a cambiare la vetrina quando serve."),
        ],
        "preventivo": [
            ("Rilievo e progetto", "sopralluogo, render 3D e varianti."),
            ("Strutture e arredi", "fondali, podi, mensole, teche, cornici, voce per voce."),
            ("Grafica e vetrofanie", "stampa e posa di vetrofanie, pannelli e tessuti."),
            ("Illuminazione", "faretti, strisce LED, retroilluminazioni."),
            ("Montaggio e cambi stagione", "montaggio, smontaggio, magazzino e trasporto fra un allestimento e l'altro."),
        ],
        "faq": [
            ("Quanto costa allestire una vetrina?", "Dipende dalle misure della vetrina, dalla quantità di strutture su misura, dalla grafica e dalle luci. Facciamo un preventivo voce per voce dopo aver visto misure e foto: è gratuito e arriva entro 24 ore lavorative."),
            ("Allestite vetrine natalizie?", "Sì: progettiamo vetrine di Natale sul tuo marchio, con fondali, strutture scenografiche e luci, e le montiamo a negozio chiuso. Conviene sentirci entro ottobre per avere la vetrina pronta per l'inizio di dicembre."),
            ("Si può riusare la vetrina per più stagioni?", "Sì: progettiamo una struttura base che resta e cambiamo solo grafiche e decorazioni a ogni stagione, così i cambi successivi costano meno."),
            ("Fate anche solo vetrofanie e grafiche?", "Sì: stampiamo e posiamo vetrofanie, pellicole satinate, pannelli e tessuti, anche senza il resto dell'allestimento."),
            ("Potete allestire la stessa vetrina in più negozi?", "Sì: per marchi e reti di rivenditori progettiamo una vetrina standard e la replichiamo nei punti vendita, con le stesse misure, grafiche e istruzioni di montaggio."),
            ("Lavorate in tutta Italia?", "Sì. Abbiamo sede a Mansuè (TV) e magazzini a Fontanelle (TV) e Trumello (PV): seguiamo direttamente Nord e Centro Italia e, con squadra in trasferta, il resto del Paese."),
        ],
        "altri": [
            ("/allestimento-negozi/", "Allestimento negozi su misura"),
            ("/espositori-pubblicitari/", "Espositori pubblicitari e da banco"),
            ("/grafica-per-stand-fieristici/", "Grafica e tessuti stampati"),
            ("/ledwall-e-illuminazione-stand/", "Ledwall e illuminazione"),
            ("/stand-pubblicitari/", "Stand pubblicitari e promozionali"),
            ("/allestimenti-eventi/", "Allestimenti per eventi e congressi"),
            ("/allestimenti-eventi-showroom-negozi/", "Allestimenti per showroom e negozi"),
            ("/progettazione-stand-fieristici/", "Progettazione e render 3D"),
        ],
    },
    {
        "slug": "allestimento-negozi",
        "title": "Allestimento negozi e vetrine su misura | Danova Stand",
        "desc": "Allestimento negozi, vetrine, corner e temporary store: progetto 3D, arredi su misura, espositori, grafica, luci e montaggio. Preventivo gratuito in 24 ore.",
        "og_title": "Allestimento negozi e vetrine su misura — Danova Stand",
        "og_desc": "Arredi, espositori, vetrine, grafica e luci per negozi, corner e temporary store, dal progetto al montaggio.",
        "crumb": "Allestimento negozi e vetrine",
        "img": "stand-moda-calzature-boutique",
        "alt": "Render di allestimento in stile boutique con pareti espositive, mensole illuminate e bancone",
        "caption": "Render di progetto: allestimento retail con pareti attrezzate, mensole illuminate e banco cassa.",
        "eyebrow": "Retail e punti vendita",
        "h1": "Allestimento negozi e vetrine <span class=\"grad\">su misura, dal progetto al montaggio</span>.",
        "lead": "Arredi, espositori, vetrine, grafica e illuminazione per negozi, corner, shop-in-shop e temporary store. Progettiamo lo spazio in 3D sul tuo marchio, facciamo produrre gli arredi su misura da laboratori partner e li montiamo noi, anche di notte o a negozio chiuso.",
        "breve": "Danova Stand allestisce negozi, vetrine, corner e temporary store in tutta Italia: rilievo dello spazio, progetto e render 3D, arredi ed espositori su misura, grafica, illuminazione, montaggio e smontaggio, con un unico referente. Lavoriamo per negozi di abbigliamento, calzature, gioielli, cosmetica, alimentari e prodotti tipici, e per marchi che aprono corner nei negozi dei rivenditori. Il preventivo è gratuito e arriva entro 24 ore lavorative.",
        "service": "Allestimento negozi, vetrine, corner e temporary store",
        "service_type": "Allestimento punti vendita (shop fitting)",
        "cards_title": "Cosa allestiamo nei negozi",
        "cards": [
            ("Negozi completi", "Pareti attrezzate, scaffali, banco cassa, camerini, tavoli espositivi e magazzino a vista: tutto disegnato sulle misure del locale."),
            ("Vetrine", "Allestimento vetrine stagionali e per i saldi, fondali, podi, vetrofanie e luce dedicata ai prodotti. Si cambia la grafica, la struttura resta."),
            ("Corner e shop-in-shop", "Spazi del tuo marchio dentro i negozi dei rivenditori o nei department store, uguali in ogni punto vendita."),
            ("Temporary store e pop-up", "Negozi aperti per qualche settimana: strutture modulari, montaggio veloce, materiali che si riusano per l'apertura successiva."),
            ("Espositori e arredi", "Espositori da banco e da terra, gondole, teche, totem e mensole, prodotti su misura per il tuo prodotto."),
            ("Grafica e luci", "Insegne, pannelli retroilluminati, tessuti stampati e illuminazione LED che fa risaltare la merce senza scaldarla."),
        ],
        "settori_title": "Per quali negozi lavoriamo",
        "settori": [
            ("Abbigliamento e calzature", "pareti con barre appendiabiti e ripiani regolabili, camerini, specchi, tavoli per il piegato, pareti scarpe con mensole a vista."),
            ("Gioiellerie e ottica", "teche e vetrine chiuse, luce dedicata alle pietre e ai metalli, banco vendita con sedute, salottino riservato."),
            ("Profumerie e cosmetica", "gondole e testate per i marchi, tester a portata di mano, luce bianca e neutra per i colori."),
            ("Alimentari e prodotti tipici", "scaffali per il secco, banco per i freschi, espositori per vino e olio, angolo degustazione."),
            ("Showroom e negozi monomarca", "lo spazio che racconta il marchio: materiali, colori e grafica coordinati con stand fieristici e cataloghi."),
        ],
        "testo_title": "Dalla fiera al negozio: <span class=\"grad\">stesso metodo, tempi più comodi</span>",
        "testo": [
            "In fiera uno stand si monta in due o tre giorni e deve funzionare dal primo minuto. Usiamo lo stesso metodo nei negozi: rilievo preciso, progetto 3D approvato prima di produrre, arredi costruiti in laboratorio e non in cantiere, montaggio in pochi giorni per tenere chiuso il negozio il meno possibile.",
            "Se hai già uno stand fieristico, il negozio può riprendere materiali, colori e grafica: il cliente che ti ha conosciuto in fiera ritrova lo stesso marchio in vetrina. E se apri un temporary store, progettiamo arredi modulari che poi tornano utili in fiera o nel punto vendita successivo.",
        ],
        "passi": [
            ("Sopralluogo e rilievo", "misure del locale, altezze, impianti, accessi per lo scarico e vincoli del condominio o del centro commerciale."),
            ("Progetto e render 3D", "pianta, percorsi del cliente, vista della vetrina dalla strada, scelta di materiali e luci. Lo approvi prima che si produca qualsiasi pezzo."),
            ("Produzione", "arredi in legno, metallo e vetro realizzati da laboratori partner con cui lavoriamo da anni; materiali certificati quando serve."),
            ("Grafica e illuminazione", "insegna, vetrofanie, pannelli e luci LED, pensati insieme agli arredi."),
            ("Montaggio", "nei giorni e negli orari che decidi tu, anche di notte, con un capocantiere che segue tutto il lavoro."),
        ],
        "preventivo": [
            ("Rilievo e progetto", "sopralluogo, pianta, render 3D e varianti."),
            ("Arredi su misura", "pareti, scaffali, banco cassa, camerini, teche e vetrine, voce per voce."),
            ("Espositori e grafica", "espositori da banco e da terra, insegna, vetrofanie, pannelli."),
            ("Illuminazione", "binari, faretti, strisce LED e luci per la vetrina."),
            ("Trasporto e montaggio", "consegna, montaggio, smaltimento degli imballi."),
        ],
        "faq": [
            ("Quanto costa allestire un negozio?", "Dipende dai metri quadri, dalla quantità di arredi su misura, dai materiali e dall'illuminazione. Per questo facciamo un preventivo voce per voce dopo il rilievo: è gratuito e arriva entro 24 ore lavorative dalla richiesta completa di misure e foto del locale."),
            ("Allestite anche solo la vetrina?", "Sì: progettiamo vetrine stagionali, per i saldi, per Natale o per il lancio di un prodotto, con strutture che si riusano cambiando solo la grafica."),
            ("Quanto tempo serve per allestire un negozio?", "Per un negozio di dimensioni medie servono di solito 4–8 settimane fra progetto e produzione degli arredi su misura, poi pochi giorni di montaggio. Un temporary store con arredi modulari si prepara in tempi più brevi."),
            ("Lavorate in tutta Italia?", "Sì. Abbiamo sede a Mansuè (TV), magazzini a Fontanelle (TV) e Trumello (PV) e uffici a Vermezzo con Zelo (MI): seguiamo direttamente Nord e Centro Italia e, con trasporto e squadra in trasferta, il resto del Paese."),
            ("Potete allestire corner del nostro marchio in più negozi?", "Sì: progettiamo un corner o uno shop-in-shop standard e lo replichiamo nei punti vendita dei rivenditori, con le stesse misure, grafiche e istruzioni di montaggio."),
            ("Montate anche a negozio chiuso o di notte?", "Sì. Concordiamo con te giorni e orari per ridurre al minimo la chiusura, anche fuori dall'orario di apertura del negozio o del centro commerciale."),
        ],
        "altri": [
            ("/allestimento-vetrine/", "Allestimento vetrine natalizie e stagionali"),
            ("/allestimenti-eventi-showroom-negozi/", "Allestimenti per eventi, showroom e mostre"),
            ("/espositori-pubblicitari/", "Espositori pubblicitari e da banco"),
            ("/totem-pubblicitari/", "Totem pubblicitari personalizzati"),
            ("/stand-pubblicitari/", "Stand pubblicitari e promozionali"),
            ("/allestimenti-eventi/", "Allestimenti per eventi e congressi"),
            ("/grafica-per-stand-fieristici/", "Grafica e tessuti stampati"),
            ("/ledwall-e-illuminazione-stand/", "Ledwall e illuminazione"),
            ("/stand-fieristici-moda-e-calzature/", "Stand per moda e calzature"),
            ("/progettazione-stand-fieristici/", "Progettazione e render 3D"),
        ],
    },
    {
        "slug": "allestimenti-eventi",
        "title": "Allestimenti per eventi, congressi e convention | Danova Stand",
        "desc": "Allestimenti per eventi aziendali, congressi, convention e lanci di prodotto: palchi, fondali, ledwall, desk, aree sponsor e segnaletica. Preventivo in 24 ore.",
        "og_title": "Allestimenti per eventi, congressi e convention — Danova Stand",
        "og_desc": "Palchi, fondali, ledwall, desk di accoglienza, aree sponsor e segnaletica, montati e smontati nei tempi della location.",
        "crumb": "Allestimenti per eventi e congressi",
        "img": "stand-roma-congresso-sponsor",
        "alt": "Render di area espositiva per congresso con desk sponsor, fondali stampati e ledwall",
        "caption": "Render di progetto: area sponsor e accoglienza per un congresso.",
        "eyebrow": "Eventi, congressi, convention",
        "h1": "Allestimenti per eventi e congressi: <span class=\"grad\">pronti all'apertura delle porte</span>.",
        "lead": "Palchi, fondali, ledwall, desk di accoglienza, aree sponsor, lounge e segnaletica per eventi aziendali, convention, congressi, lanci di prodotto e cene di gala. Progetto, materiali, luci, montaggio e smontaggio con un solo referente, nei tempi stretti delle location.",
        "breve": "Danova Stand è un allestitore di eventi con oltre 20 anni di esperienza nelle fiere. Allestiamo eventi aziendali, congressi, convention, lanci di prodotto, inaugurazioni e cene di gala in hotel, centri congressi, spazi industriali e location storiche: palco e fondale, ledwall e luci, desk di accoglienza, stand e corner degli sponsor, arredi lounge, segnaletica e allestimenti scenografici. Montiamo e smontiamo nelle finestre orarie della location, anche di notte. Preventivo gratuito entro 24 ore.",
        "service": "Allestimenti per eventi aziendali, congressi e convention",
        "service_type": "Allestimento eventi e congressi",
        "cards_title": "Cosa allestiamo per un evento",
        "cards": [
            ("Palco e fondale", "Pedane e palchi modulari, fondali stampati o in legno, leggio, quinte: la scena su cui si presenta l'azienda."),
            ("Ledwall, luci e video", "Ledwall per presentazioni e video, illuminazione di palco e di sala, coordinati con il service audio."),
            ("Accoglienza e registrazione", "Desk di accoglienza con grafica, totem, segnaletica dal parcheggio alla sala, guardaroba."),
            ("Aree sponsor ed espositive", "Corner e stand degli sponsor nei congressi, tutti coordinati, con banco, grafica e corrente."),
            ("Lounge e catering", "Arredi lounge, banchi bar e buffet, tavoli alti, piante e tappeti per le pause e il networking."),
            ("Allestimenti scenografici", "Scenografie per lanci di prodotto, inaugurazioni e cene di gala: strutture, tessuti, luci e grafica in grande formato."),
        ],
        "settori_title": "Gli eventi che allestiamo",
        "settori": [
            ("Congressi e convegni", "aree sponsor, poster area, desk di registrazione, segnaletica delle sale, palco per i relatori."),
            ("Convention e meeting aziendali", "palco con ledwall, fondale con il marchio, sala plenaria e sale per i workshop."),
            ("Lanci di prodotto", "il prodotto al centro, su podi illuminati, con un percorso che accompagna gli ospiti fino alla presentazione."),
            ("Inaugurazioni e open house", "allestimento degli spazi aziendali o del nuovo stabilimento, accoglienza e percorsi di visita."),
            ("Cene di gala ed eventi esterni", "scenografie, luci d'atmosfera, strutture per spazi all'aperto e location storiche."),
        ],
        "testo_title": "Perché affidare un evento <span class=\"grad\">a chi fa fiere</span>",
        "testo": [
            "Una fiera insegna a lavorare con tempi stretti, regolamenti rigidi e spazi da consegnare puliti a un'ora precisa. Un congresso in hotel o una convention in uno spazio industriale hanno gli stessi vincoli: si entra la sera prima, si monta di notte, alle otto arrivano gli ospiti.",
            "Per questo prepariamo in anticipo pianta, allacci elettrici, percorsi di scarico e tempi di montaggio, usiamo strutture modulari e grafiche in tessuto che si montano in poche ore, e lavoriamo con materiali certificati in Classe 1 di reazione al fuoco, come chiedono molte location. Gli stessi elementi, con una grafica nuova, possono servire per lo stand della fiera successiva.",
        ],
        "passi": [
            ("Brief e sopralluogo", "numero di ospiti, programma, location: misure, portate dei pavimenti, accessi e orari di carico e scarico."),
            ("Progetto e render", "pianta della sala, palco, aree sponsor, percorsi degli ospiti e vista dalla platea."),
            ("Produzione e noleggi", "strutture, grafiche, arredi a noleggio o su misura, ledwall e luci."),
            ("Montaggio", "nei tempi della location, anche in notturna, con un capocantiere presente fino all'apertura."),
            ("Smontaggio", "a fine evento, spesso la notte stessa, con lo spazio riconsegnato come l'abbiamo trovato."),
        ],
        "preventivo": [
            ("Progetto", "sopralluogo, pianta e render dell'allestimento."),
            ("Strutture", "palco, fondali, pareti, desk, stand degli sponsor."),
            ("Luci e video", "ledwall, illuminazione di palco e di sala."),
            ("Arredi e grafica", "lounge, tavoli, segnaletica, totem, stampe."),
            ("Logistica", "trasporto, montaggio, smontaggio, eventuali turni notturni."),
        ],
        "faq": [
            ("Quanto costa allestire un evento aziendale?", "Dipende da numero di ospiti, dimensione della sala, palco e ledwall, quantità di grafica e arredi, orari di montaggio. Facciamo un preventivo voce per voce, gratuito, entro 24 ore lavorative dal brief."),
            ("Allestite anche gli stand degli sponsor nei congressi?", "Sì: progettiamo un modulo sponsor coordinato (banco, fondale, luce, corrente) e lo realizziamo per tutti gli sponsor, oppure stand su misura per i partner principali."),
            ("Lavorate in hotel e centri congressi?", "Sì: hotel, centri congressi, spazi aziendali, capannoni, location storiche e spazi all'aperto. Verifichiamo con la location regolamento, orari e portate prima di progettare."),
            ("Potete montare la notte prima dell'evento?", "Sì, è la norma: molte location danno accesso solo la sera prima o all'alba. Pianifichiamo il montaggio a turni e lo smontaggio subito dopo la chiusura."),
            ("Vi occupate anche di audio e video?", "Ledwall e illuminazione sì; per audio, regia e traduzione simultanea lavoriamo insieme al service dell'evento o a quello della location."),
            ("Gli allestimenti si possono riusare?", "Sì: fondali, desk e strutture modulari possono essere conservati nei nostri magazzini e riusati, con una grafica nuova, per l'evento o la fiera successiva."),
        ],
        "altri": [
            ("/allestimenti-eventi-showroom-negozi/", "Eventi, showroom, negozi e mostre"),
            ("/allestimento-mostre/", "Allestimento mostre ed esposizioni"),
            ("/allestimento-negozi/", "Allestimento negozi e vetrine"),
            ("/stand-pubblicitari/", "Stand pubblicitari e promozionali"),
            ("/ledwall-e-illuminazione-stand/", "Ledwall e illuminazione"),
            ("/espositori-desk-totem-per-fiere/", "Desk, totem ed espositori"),
            ("/allestimenti-fieristici-roma/", "Allestimenti a Roma (Fiera di Roma e Nuvola)"),
            ("/allestimenti-fieristici-milano/", "Allestimenti a Milano"),
            ("/allestimenti-fieristici-venezia/", "Allestimenti a Venezia e Mestre"),
        ],
    },
    {
        "slug": "allestimento-mostre",
        "title": "Allestimento mostre ed esposizioni temporanee | Danova Stand",
        "desc": "Allestimento mostre d'arte, esposizioni temporanee e spazi museali: pareti e pannellature, teche, basamenti, luci, grafica di sala, montaggio e smontaggio.",
        "og_title": "Allestimento mostre ed esposizioni temporanee — Danova Stand",
        "og_desc": "Pareti, pannellature, teche, basamenti, illuminazione e grafica di sala per mostre d'arte ed esposizioni temporanee.",
        "crumb": "Allestimento mostre",
        "img": "stand-venezia-evento-storico",
        "alt": "Render di allestimento espositivo in uno spazio storico con pannelli, teche e illuminazione dedicata",
        "caption": "Render di progetto: allestimento leggero e reversibile in uno spazio storico.",
        "eyebrow": "Mostre ed esposizioni",
        "h1": "Allestimento mostre: <span class=\"grad\">le opere al centro, l'allestimento al servizio</span>.",
        "lead": "Pareti e pannellature autoportanti, basamenti, teche, illuminazione delle opere, grafica di sala e segnaletica per mostre d'arte, esposizioni temporanee, mostre aziendali e spazi museali. Strutture leggere e reversibili, adatte anche agli edifici storici tutelati.",
        "breve": "Danova Stand realizza allestimenti per mostre d'arte, esposizioni temporanee, mostre aziendali e itineranti: progetto del percorso, pareti e pannellature autoportanti, basamenti e teche, illuminazione delle opere, grafica di sala, didascalie e segnaletica, montaggio e smontaggio. Usiamo strutture leggere e reversibili, che non toccano muri e pavimenti degli spazi storici, e materiali certificati in Classe 1 di reazione al fuoco. Preventivo gratuito entro 24 ore.",
        "service": "Allestimento mostre ed esposizioni temporanee",
        "service_type": "Allestimento mostre ed esposizioni",
        "cards_title": "Cosa realizziamo per una mostra",
        "cards": [
            ("Pareti e pannellature", "Pareti autoportanti e pannelli che disegnano il percorso senza forare muri e pavimenti, verniciati o rivestiti."),
            ("Basamenti e teche", "Basamenti su misura per sculture e oggetti, teche e vetrine per i pezzi delicati o di valore."),
            ("Illuminazione delle opere", "Binari e proiettori con luce calibrata sulle opere, senza riflessi e senza raggi UV."),
            ("Grafica di sala", "Pannelli introduttivi, didascalie, testi di sala, grandi stampe e segnaletica del percorso."),
            ("Mostre itineranti", "Allestimenti smontabili e riutilizzabili per mostre che girano in più sedi, con imballi e istruzioni di montaggio."),
            ("Montaggio e smontaggio", "Squadra di montatori, capocantiere presente e smontaggio con lo spazio riconsegnato in ordine."),
        ],
        "settori_title": "Le mostre che allestiamo",
        "settori": [
            ("Mostre d'arte temporanee", "per gallerie, fondazioni, comuni e curatori: percorso, pareti, luci e grafica."),
            ("Mostre in spazi storici", "palazzi, chiese sconsacrate, ex conventi: strutture appoggiate, reversibili, nel rispetto dei vincoli."),
            ("Mostre aziendali e musei d'impresa", "la storia del marchio, prodotti storici e archivi raccontati in uno spazio permanente o temporaneo."),
            ("Esposizioni e rassegne", "mostre mercato, esposizioni di prodotti tipici, rassegne di artigianato e design."),
            ("Mostre itineranti", "lo stesso allestimento portato in più città, progettato per viaggiare e rimontarsi senza sorprese."),
        ],
        "testo_title": "Allestimenti leggeri <span class=\"grad\">per spazi che non si possono toccare</span>",
        "testo": [
            "Molte mostre si fanno in luoghi tutelati, dove non si può forare un muro né appoggiare carichi pesanti sul pavimento. Per questo usiamo pareti autoportanti, zavorre e strutture modulari che si appoggiano senza fissaggi, e prima di progettare verifichiamo con l'ente o con la soprintendenza cosa è consentito.",
            "Le fiere ci hanno insegnato a lavorare con regolamenti rigidi e materiali certificati: le stesse regole valgono per una mostra aperta al pubblico, dove contano la sicurezza dei visitatori, l'accessibilità del percorso e la conformità degli impianti elettrici.",
        ],
        "passi": [
            ("Sopralluogo", "rilievo degli spazi, vincoli dell'edificio, accessi per le opere e per i materiali."),
            ("Progetto del percorso", "pianta con la sequenza delle sale, posizione delle opere, punti luce e flussi dei visitatori, insieme al curatore."),
            ("Produzione", "pareti, basamenti, teche e grafiche prodotti da laboratori partner, materiali certificati in Classe 1."),
            ("Montaggio e luci", "montaggio delle strutture, puntamento delle luci sulle opere, posa della grafica di sala."),
            ("Smontaggio", "a fine mostra, con possibilità di conservare gli elementi in magazzino per riusarli."),
        ],
        "preventivo": [
            ("Progetto", "sopralluogo, pianta del percorso, render e varianti."),
            ("Strutture", "pareti autoportanti, pannellature, basamenti, teche."),
            ("Illuminazione", "binari, proiettori, alimentazione e certificazioni."),
            ("Grafica", "pannelli, didascalie, stampe di grande formato, segnaletica."),
            ("Montaggio e smontaggio", "squadra, mezzi, eventuale magazzino fra una tappa e l'altra."),
        ],
        "faq": [
            ("Potete allestire mostre in edifici storici tutelati?", "Sì: usiamo pareti autoportanti e strutture appoggiate, senza forare muri o pavimenti, e verifichiamo prima con l'ente proprietario o la soprintendenza cosa è consentito."),
            ("Vi occupate anche dell'illuminazione delle opere?", "Sì: progettiamo e montiamo binari e proiettori con la luce calibrata sulle opere, insieme al curatore."),
            ("Realizzate teche e basamenti su misura?", "Sì, sulle misure degli oggetti da esporre, con vetri e chiusure adatte ai pezzi di valore."),
            ("Fate allestimenti per mostre itineranti?", "Sì: progettiamo strutture smontabili e riutilizzabili, con imballi e istruzioni, che possono essere conservate nei nostri magazzini fra una tappa e l'altra."),
            ("Quanto costa allestire una mostra?", "Dipende da superficie, numero di pareti e basamenti, teche, illuminazione e quantità di grafica. Il preventivo è voce per voce, gratuito, entro 24 ore lavorative dalla richiesta."),
            ("Lavorate con musei e gallerie?", "Sì, e anche con comuni, fondazioni, aziende e curatori indipendenti. Seguiamo il progetto insieme al curatore o all'architetto, oppure lo sviluppiamo noi."),
        ],
        "altri": [
            ("/allestimenti-eventi-showroom-negozi/", "Eventi, showroom, negozi e mostre"),
            ("/allestimenti-eventi/", "Allestimenti per eventi e congressi"),
            ("/allestimento-negozi/", "Allestimento negozi e vetrine"),
            ("/ledwall-e-illuminazione-stand/", "Illuminazione e ledwall"),
            ("/grafica-per-stand-fieristici/", "Grafica e stampe di grande formato"),
            ("/sicurezza-stand-fieristici/", "Materiali in Classe 1 e sicurezza"),
            ("/allestimenti-fieristici-venezia/", "Allestimenti a Venezia"),
            ("/allestimenti-fieristici-firenze/", "Allestimenti a Firenze"),
            ("/progettazione-stand-fieristici/", "Progettazione e render 3D"),
        ],
    },
    {
        "slug": "stand-pubblicitari",
        "title": "Stand pubblicitari e promozionali personalizzati | Danova Stand",
        "desc": "Stand pubblicitari, espositivi e promozionali: banchetti, stand portatili e pop-up, roll-up, fondali in tessuto e strutture modulari con la tua grafica. Preventivo in 24 ore.",
        "og_title": "Stand pubblicitari e promozionali personalizzati — Danova Stand",
        "og_desc": "Banchetti promozionali, stand portatili e pop-up, fondali in tessuto e strutture modulari con la tua grafica.",
        "crumb": "Stand pubblicitari",
        "img": "stand-modulare-alluminio-tessuto",
        "alt": "Render di stand espositivo modulare in alluminio con grafica in tessuto teso retroilluminato",
        "caption": "Render di progetto: stand espositivo modulare in alluminio e tessuto stampato.",
        "eyebrow": "Promozione e punti vendita",
        "h1": "Stand pubblicitari e promozionali: <span class=\"grad\">il tuo marchio, ovunque ci sia gente</span>.",
        "lead": "Stand espositivi, banchetti promozionali, stand portatili e pop-up, fondali in tessuto e strutture modulari con la tua grafica, per centri commerciali, eventi, congressi, punti vendita e fiere. Leggeri da trasportare, veloci da montare, pensati per essere riusati molte volte.",
        "breve": "Uno stand pubblicitario è una struttura espositiva con la grafica del marchio usata per promuovere prodotti e servizi fuori dalla propria sede: in centri commerciali, supermercati, eventi, congressi, punti vendita e fiere. Danova Stand progetta e produce stand pubblicitari personalizzati — banchetti promozionali, stand portatili e pop-up, fondali e pareti in tessuto, strutture modulari in alluminio, totem e desk — e può gestirne trasporto, montaggio e magazzino. Preventivo gratuito entro 24 ore.",
        "service": "Stand pubblicitari, espositivi e promozionali personalizzati",
        "service_type": "Stand pubblicitari e promozionali",
        "cards_title": "I tipi di stand pubblicitari",
        "cards": [
            ("Banchetti promozionali", "Desk e banchi con la tua grafica per degustazioni, sampling, raccolta contatti e promozioni nei punti vendita."),
            ("Stand portatili e pop-up", "Strutture leggere che stanno in una borsa o in una valigia, montabili da una persona in pochi minuti."),
            ("Fondali e pareti in tessuto", "Telai in alluminio con tessuto teso stampato, anche retroilluminati: grafica senza pieghe, si lava e si sostituisce."),
            ("Stand modulari", "Strutture in alluminio componibili che si allargano o si riducono a seconda dello spazio disponibile."),
            ("Totem e roll-up", "Elementi verticali per segnalare la presenza, guidare il pubblico e comunicare l'offerta."),
            ("Corner per centri commerciali", "Postazioni promozionali complete, con banco, fondale, luci ed espositori, conformi ai regolamenti del centro."),
        ],
        "settori_title": "Dove si usano",
        "settori": [
            ("Centri commerciali e gallerie", "postazioni promozionali, presentazioni di prodotto, raccolta contatti e vendita assistita."),
            ("Supermercati e punti vendita", "banchetti per degustazioni, sampling e promozioni dei marchi."),
            ("Eventi, congressi e convegni", "corner degli sponsor, desk di accoglienza, fondali per foto e interviste."),
            ("Fiere e mostre mercato", "stand preallestiti e modulari per chi espone spesso e vuole riusare la struttura."),
            ("Roadshow e tour promozionali", "lo stesso stand in più città, con imballi, trasporto e magazzino gestiti da noi."),
        ],
        "testo_title": "Pensati per essere <span class=\"grad\">riusati, non buttati</span>",
        "testo": [
            "Uno stand pubblicitario conviene quando si usa molte volte. Per questo progettiamo strutture modulari in alluminio e grafiche in tessuto che si montano senza attrezzi, viaggiano in imballi compatti e si aggiornano cambiando solo la stampa: il telaio resta, il messaggio cambia.",
            "Se lo stand deve stare in un centro commerciale o in una location con regolamento, prepariamo noi le schede dei materiali certificati in Classe 1 di reazione al fuoco e la documentazione elettrica per le luci. E se serve, lo conserviamo nei nostri magazzini e lo spediamo dove serve per la promozione successiva.",
        ],
        "passi": [
            ("Brief", "dove verrà usato, quante volte, chi lo monta, quanto spazio c'è e cosa deve contenere."),
            ("Progetto e grafica", "render dello stand con la grafica applicata, misure e pesi."),
            ("Produzione", "strutture, stampe in tessuto o rigide, banchi ed espositori."),
            ("Consegna o montaggio", "te lo consegniamo con le istruzioni, oppure lo montiamo noi sul posto."),
            ("Magazzino e aggiornamenti", "conservazione fra un'uscita e l'altra e nuove grafiche quando cambia la campagna."),
        ],
        "preventivo": [
            ("Struttura", "telai, banchi, pareti e accessori, in acquisto o a noleggio."),
            ("Grafica", "stampa in tessuto o su pannelli rigidi, con prove colore."),
            ("Luci", "retroilluminazione e faretti, con certificazioni."),
            ("Imballi", "borse, valigie o casse per trasportarlo senza danni."),
            ("Servizi", "trasporto, montaggio, magazzino, sostituzione grafiche."),
        ],
        "faq": [
            ("Che differenza c'è fra stand pubblicitario e stand fieristico?", "Lo stand fieristico è progettato per una fiera e il suo regolamento, spesso su misura. Lo stand pubblicitario è più leggero e trasportabile, pensato per essere usato molte volte in luoghi diversi: centri commerciali, punti vendita, eventi, congressi e anche fiere."),
            ("Quanto costa uno stand pubblicitario?", "Dipende da dimensioni, struttura, quantità di grafica e luci. Un banchetto promozionale costa molto meno di una parete modulare retroilluminata: facciamo un preventivo voce per voce, gratuito, entro 24 ore lavorative."),
            ("Lo stand si può montare senza tecnici?", "Sì: i modelli portatili e pop-up si montano da una o due persone senza attrezzi, con le istruzioni che forniamo. Le strutture più grandi le montiamo noi."),
            ("Posso cambiare solo la grafica?", "Sì: con le grafiche in tessuto teso o i pannelli intercambiabili si sostituisce solo la stampa e si riusa la struttura."),
            ("Fate stand per i centri commerciali?", "Sì: corner promozionali con banco, fondale, luci ed espositori, con i materiali certificati e la documentazione che chiede il regolamento del centro."),
            ("Conservate voi lo stand fra un utilizzo e l'altro?", "Sì, nei nostri magazzini di Fontanelle (TV) e Trumello (PV), e lo spediamo o lo montiamo dove serve."),
        ],
        "altri": [
            ("/totem-pubblicitari/", "Totem pubblicitari personalizzati"),
            ("/espositori-pubblicitari/", "Espositori pubblicitari e da banco"),
            ("/espositori-desk-totem-per-fiere/", "Desk, banchi e totem per fiere"),
            ("/stand-modulari/", "Stand modulari in alluminio e tessuto"),
            ("/stand-preallestiti/", "Stand preallestiti"),
            ("/noleggio-stand-fieristici/", "Noleggio stand e arredi"),
            ("/grafica-per-stand-fieristici/", "Grafica e tessuti stampati"),
            ("/allestimenti-eventi/", "Allestimenti per eventi e congressi"),
            ("/allestimento-negozi/", "Allestimento negozi e vetrine"),
        ],
    },
]


def cards_html(cards):
    out = []
    for i, (t, p) in enumerate(cards, 1):
        out.append(f'      <article class="pg-card" data-tilt data-rv="blur">\n        <span class="n">{i:02d}</span>\n        <h3>{e(t)}</h3>\n        <p>{e(p)}</p>\n      </article>')
    return "\n".join(out)


def lista_html(items):
    return "\n".join(f"      <li><b>{e(t)}.</b> {e(p[0].upper() + p[1:])}</li>" for t, p in items)


def build(p, tpl, legno, cta_form, footer_after_main, head_before_ld, head_after_ld, body_before_main):
    slug, url = p["slug"], f"{SITO}/{p['slug']}/"
    img = p["img"]
    w, h = webp_size(os.path.join(ROOT, "assets/img/stand", img + ".webp"))
    imgurl = f"{SITO}/assets/img/stand/{img}.webp"

    # ---- head
    head = head_before_ld
    rep = {
        r"<title>.*?</title>": f"<title>{e(p['title'])}</title>",
        r'<meta name="description" content="[^"]*">': f'<meta name="description" content="{e(p["desc"])}">',
        r'<link rel="canonical" href="[^"]*">': f'<link rel="canonical" href="{url}">',
        r'<link rel="alternate" hreflang="it" href="[^"]*">': f'<link rel="alternate" hreflang="it" href="{url}">',
        r'<link rel="alternate" hreflang="x-default" href="[^"]*">': f'<link rel="alternate" hreflang="x-default" href="{url}">',
        r'<meta property="og:url" content="[^"]*">': f'<meta property="og:url" content="{url}">',
        r'<meta property="og:title" content="[^"]*">': f'<meta property="og:title" content="{e(p["og_title"])}">',
        r'<meta property="og:description" content="[^"]*">': f'<meta property="og:description" content="{e(p["og_desc"])}">',
        r'<meta property="og:image" content="[^"]*">': f'<meta property="og:image" content="{SITO}/assets/img/stand/og/{img}.jpg">',
        r'<meta property="og:image:alt" content="[^"]*">': f'<meta property="og:image:alt" content="{e(p["alt"])}">',
        r'<meta name="twitter:title" content="[^"]*">': f'<meta name="twitter:title" content="{e(p["og_title"])}">',
        r'<meta name="twitter:description" content="[^"]*">': f'<meta name="twitter:description" content="{e(p["og_desc"])}">',
        r'<meta name="twitter:image" content="[^"]*">': f'<meta name="twitter:image" content="{SITO}/assets/img/stand/og/{img}.jpg">',
    }
    for k, v in rep.items():
        head, n = re.subn(k, lambda m, v=v: v, head, count=1, flags=re.S)
        if n != 1:
            sys.exit(f"pattern non trovato nel modello: {k}")

    # ---- JSON-LD
    m = re.search(r'<script type="application/ld\+json">(.*?)</script>', tpl, re.S)
    graph = json.loads(m.group(1))["@graph"]
    org = graph[0]
    nodes = [org,
        {"@type": "WebPage", "@id": url + "#webpage", "url": url, "name": p["title"], "description": p["desc"],
         "isPartOf": {"@id": SITO + "/#website"}, "breadcrumb": {"@id": url + "#breadcrumb"}, "inLanguage": "it",
         "datePublished": OGGI, "dateModified": OGGI, "primaryImageOfPage": {"@id": imgurl + "#img"},
         "about": {"@id": url + "#service"}, "image": {"@id": imgurl + "#img"},
         "speakable": {"@type": "SpeakableSpecification", "cssSelector": ["h1", "#in-breve p"]}},
        {"@type": "BreadcrumbList", "@id": url + "#breadcrumb", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": SITO + "/"},
            {"@type": "ListItem", "position": 2, "name": "Allestimenti per eventi, showroom, negozi e mostre", "item": SITO + "/allestimenti-eventi-showroom-negozi/"},
            {"@type": "ListItem", "position": 3, "name": p["crumb"]}]},
        {"@type": "Service", "@id": url + "#service", "name": p["service"], "serviceType": p["service_type"],
         "description": p["breve"], "provider": {"@id": SITO + "/#organization"}, "url": url,
         "areaServed": [{"@type": "Country", "name": "Italia"}, {"@type": "Place", "name": "Europa"}],
         "availableLanguage": ["Italian", "English", "German"],
         "hasOfferCatalog": {"@type": "OfferCatalog", "name": p["service"], "itemListElement": [
             {"@type": "Offer", "itemOffered": {"@type": "Service", "name": t, "description": d}} for t, d in p["cards"]]}},
        {"@type": "FAQPage", "@id": url + "#faq", "isPartOf": {"@id": url + "#webpage"}, "inLanguage": "it",
         "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in p["faq"]]},
        {"@type": "ImageObject", "@id": imgurl + "#img", "url": imgurl, "contentUrl": imgurl, "width": w, "height": h,
         "caption": p["caption"], "description": p["alt"], "inLanguage": "it", "creditText": "Render di progetto Danova Stand",
         "copyrightNotice": "© Danova Stand", "creator": {"@id": SITO + "/#organization"},
         "thumbnailUrl": f"{SITO}/assets/img/stand/{img}-800.webp",
         "license": SITO + "/termini/#proprieta-intellettuale", "acquireLicensePage": SITO + "/contatti/"},
    ]
    ld = json.dumps({"@context": "https://schema.org", "@graph": nodes}, ensure_ascii=False, indent=2)

    # ---- main
    faq = "\n".join(f'      <details data-rv="up"><summary>{e(q)}<span class="pm"></span></summary>\n        <div class="ans"><p>{e(a)}</p></div></details>' for q, a in p["faq"])
    altri = "\n      ".join(f'<a href="{u}">{e(t)}</a>' for u, t in p["altri"])
    settori = "\n".join(f"      <li><b>{e(t)}:</b> {e(d)}</li>" for t, d in p["settori"])
    passi = "\n".join(f"      <li><b>{i}. {e(t)}:</b> {e(d)}</li>" for i, (t, d) in enumerate(p["passi"], 1))
    testo = "\n".join(f"      <p>{e(x)}</p>" for x in p["testo"])
    main = f'''<main id="main">

<div class="wrap pg-crumbs">
  <a href="/">Home</a><em>/</em><a href="/allestimenti-eventi-showroom-negozi/">Eventi, showroom, negozi e mostre</a><em>/</em>{e(p["crumb"])}
</div>

<section class="pg-hero">
  <div class="wrap">
    <div class="eyebrow mono" data-scramble>{e(p["eyebrow"])}</div>
    <h1 data-rv="up">{p["h1"]}</h1>
    <p class="lead" data-rv="up">{e(p["lead"])}</p>
    <div class="hero-cta" data-rv="up">
      <a href="#dt-scrivi" class="btn btn-p" data-mag><span class="sheen"></span><span class="lbl">Richiedi un preventivo</span>
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 12h14M13 6l6 6-6 6"></path></svg></a>
      <a href="#cosa" class="btn btn-g" data-mag><span class="lbl">{e(p["cards_title"])}</span></a>
    </div>
  </div>
  <div class="fr-hero-vis fr-hero-foto"><picture><source media="(max-width:1180px)" srcset="data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7"><img src="/assets/img/stand/{img}-800.webp" srcset="/assets/img/stand/{img}-800.webp 800w, /assets/img/stand/{img}-1200.webp 1200w" sizes="(max-width:1180px) 0px, 440px" alt="" width="800" height="{round(800*h/w)}" fetchpriority="high" decoding="async"></picture></div>
</section>
<section id="in-breve">
  <div class="wrap">
    <div class="pg-testo" data-rv="up">
      <p><b>In breve.</b> {e(p["breve"])}</p>
    </div>
  </div>
</section>
<!--fr-foto--><section class="fr-foto-sec"><div class="wrap"><figure class="fr-foto" data-rv="up"><img src="/assets/img/stand/{img}.webp" srcset="/assets/img/stand/{img}-800.webp 800w, /assets/img/stand/{img}-1200.webp 1200w, /assets/img/stand/{img}.webp {w}w" sizes="(max-width: 1240px) calc(100vw - 44px), 1196px" width="{w}" height="{h}" alt="{e(p["alt"])}" loading="lazy" decoding="async"><figcaption>{e(p["caption"])}</figcaption></figure></div></section><!--/fr-foto-->
<section id="cosa">
  <div class="wrap">
    <div class="sec-head">
      <h2 class="title" data-rv="up">{e(p["cards_title"])}</h2>
    </div>
    <div class="pg-cards">
{cards_html(p["cards"])}
    </div>
  </div>
</section>
<section id="per-chi">
  <div class="wrap">
    <div class="sec-head">
      <h2 class="title" data-rv="up">{e(p["settori_title"])}</h2>
    </div>
    <ul class="pg-lista" data-rv="up">
{settori}
    </ul>
  </div>
</section>
<section id="perche">
  <div class="wrap">
    <div class="sec-head">
      <h2 class="title" data-rv="up">{p["testo_title"]}</h2>
    </div>
    <div class="pg-testo" data-rv="up">
{testo}
    </div>
  </div>
</section>
<section id="come-lavoriamo">
  <div class="wrap">
    <div class="sec-head">
      <div class="eyebrow mono">Il metodo</div>
      <h2 class="title" data-rv="up">Come lavoriamo, <span class="grad">passo per passo</span></h2>
    </div>
    <ul class="pg-lista" data-rv="up">
{passi}
    </ul>
  </div>
</section>
<section id="preventivo">
  <div class="wrap">
    <div class="sec-head">
      <h2 class="title" data-rv="up">Cosa trovate <span class="grad">nel preventivo</span></h2>
    </div>
    <ul class="pg-lista" data-rv="up">
{lista_html(p["preventivo"])}
    </ul>
  </div>
</section>
{legno}
<section id="faq">
  <div class="wrap">
    <div class="sec-head">
      <div class="eyebrow mono" data-scramble>Domande frequenti</div>
      <h2 class="title" data-rv="up">Le risposte che <span class="grad">servono davvero.</span></h2>
    </div>
    <div class="faq">
{faq}
    </div>
  </div>
</section>
{cta_form}
<section id="altri">
  <div class="wrap">
    <div class="sec-head"><h2 class="title" data-rv="up">Approfondisci</h2></div>
    <div class="pg-altri" data-rv="up">{altri}
    </div>
  </div>
</section>

</main>'''
    body = body_before_main.replace('href="/allestimenti-eventi-showroom-negozi/" hreflang="it" aria-current="page"', f'href="/{slug}/" hreflang="it" aria-current="page"')
    return head + '<script type="application/ld+json">\n' + ld + "\n</script>" + head_after_ld + body + main + footer_after_main


def main():
    tpl = open(MODELLO, encoding="utf-8").read()
    s = tpl.find('<script type="application/ld+json">'); s2 = tpl.find("</script>", s) + len("</script>")
    head_before_ld, head_after_ld_full = tpl[:s], tpl[s2:]
    j = head_after_ld_full.find("<main"); k = head_after_ld_full.find("</main>") + len("</main>")
    rest_head_body, footer = head_after_ld_full[:j], head_after_ld_full[k:]
    hb = rest_head_body.find("</head>")
    head_after_ld, body_before_main = rest_head_body[:hb], rest_head_body[hb:]
    mainhtml = head_after_ld_full[j:k]
    legno = re.search(r"<!--fr-legno-->.*?<!--/fr-legno-->", mainhtml, re.S).group(0)
    cta = re.search(r'<section class="pg-cta">.*?</section>', mainhtml, re.S).group(0)
    cta = cta.replace("Parliamo del tuo stand.", "Parliamo del tuo progetto.").replace("Dicci fiera, date e metratura", "Dicci dove, quando e cosa ti serve")
    solo = set(sys.argv[1:])  # opzionale: rigenera solo gli slug indicati
    for p in PAGINE:
        if solo and p["slug"] not in solo:
            continue
        out = build(p, tpl, legno, cta, footer, head_before_ld, head_after_ld, body_before_main)
        d = os.path.join(ROOT, p["slug"]); os.makedirs(d, exist_ok=True)
        open(os.path.join(d, "index.html"), "w", encoding="utf-8").write(out)
        print("scritta", p["slug"], len(out))


if __name__ == "__main__":
    main()
