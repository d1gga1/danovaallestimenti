# -*- coding: utf-8 -*-
"""Approfondimenti scritti a mano per le pagine fiere piu' brevi (13 ottobre 2026): un esempio tipico e cosa
   trovate nel preventivo. Inseriti prima del modulo di richiesta (o delle FAQ). Idempotente.
   Chiamato da lib.build e da applica_immagini.py."""
import re
A, B = '<!--fr-extra-->', '<!--/fr-extra-->'
X = {
 '/allestimenti-eventi-showroom-negozi/': ('Un esempio: <span class="grad">la presentazione di un prodotto</span>', [
   "Un'azienda presenta la nuova linea a 120 clienti in uno spazio industriale riconvertito. Serve un palco basso con un ledwall, un'area con i prodotti su podi illuminati, un angolo lounge per le chiacchiere dopo la presentazione e una segnaletica che porti gli ospiti dal parcheggio alla sala.",
   "Lo spazio si allestisce in un giorno e si smonta la notte stessa: per questo usiamo strutture modulari, grafiche in tessuto e arredi a noleggio, e prepariamo in anticipo una pianta con gli allacci elettrici e i percorsi. Lo stesso materiale, con grafiche diverse, può tornare utile per uno showroom temporaneo o una fiera."],
   [("Sopralluogo e pianta.", "Misure dello spazio, accessi per lo scarico, punti di corrente."), ("Strutture e arredi.", "Palco, podi, pareti, lounge, a noleggio o in acquisto."), ("Luci e video.", "Illuminazione dei prodotti, ledwall, audio se serve."), ("Grafica e segnaletica.", "Fondali, totem, indicazioni per gli ospiti."), ("Montaggio e smontaggio.", "Nei tempi della location, anche in notturna.")]),
 '/noleggio-stand-fieristici/': ('Un esempio: <span class="grad">uno stand di 32 mq a noleggio</span>', [
   "Un'azienda alla prima fiera di settore ha uno spazio di 32 metri quadri ad angolo. Con il noleggio sceglie pareti con grafica stampata, un banco reception luminoso, un piccolo ripostiglio chiuso, un tavolo con tre sedie, mensole per i prodotti e illuminazione a binario.",
   "Non deve comprare, trasportare né conservare nulla: a fine fiera smontiamo e ritiriamo tutto. Se la fiera va bene e l'azienda decide di esporre più volte l'anno, lo stesso progetto può diventare uno stand modulare di proprietà, conservato nel nostro magazzino."],
   [("Strutture e pareti.", "Telai, pannelli, ripostiglio, eventuale soppalco."), ("Arredi.", "Banco, tavoli, sedie, vetrine, mensole, appendiabiti."), ("Grafica.", "Stampa su pannelli o tessuto, inclusa nel noleggio o a parte."), ("Impianti.", "Quadro elettrico, luci, dichiarazione di conformità."), ("Logistica.", "Trasporto, montaggio, smontaggio e ritiro.")]),
 '/_vecchio-estero-ora-in-build_europa/': ('Un esempio: <span class="grad">una fiera in Germania, organizzata dall\'Italia</span>', [
   "Un'azienda veneta espone per la prima volta in una grande fiera tedesca con uno stand di 60 metri quadri. Le serve qualcuno che parli con l'organizzatore nella sua lingua, che conosca il regolamento tecnico del quartiere fieristico e che porti lo stand in tempo, senza sorprese doganali o di orari.",
   "Progettiamo e produciamo in Italia, organizziamo il trasporto con la documentazione corretta, prenotiamo gli slot di scarico e montiamo con squadre nostre o con partner locali. Il referente resta lo stesso dal primo schizzo allo smontaggio, e risponde in italiano."],
   [("Progetto e approvazione.", "Render, piante e documenti per l'ente fiera estero."), ("Produzione in Italia.", "Strutture, grafiche e arredi preparati prima della partenza."), ("Trasporto.", "Camion, documenti e slot di scarico prenotati."), ("Montaggio sul posto.", "Squadre nostre o partner locali gestiti da noi."), ("Servizi della fiera.", "Corrente, pulizie, connessione ordinati per voi.")]),
 '/stand-modulari/': ('Un esempio: <span class="grad">uno stand per quattro fiere l\'anno</span>', [
   "Un'azienda espone in quattro fiere l'anno con spazi diversi: 24 metri quadri in linea, 36 ad angolo, un'isola da 48. Uno stand su misura per ciascuna costerebbe troppo; un preallestito ogni volta la renderebbe uguale a tutti gli altri.",
   "La soluzione è un sistema modulare in alluminio con grafiche in tessuto teso: lo stesso kit si configura per le tre metrature, cambiando la disposizione dei moduli e, quando serve, solo le stampe. Tra una fiera e l'altra resta nel nostro magazzino, pronto per la prossima partenza."],
   [("Kit di moduli.", "Telai, pannelli, lightbox, banco e mensole."), ("Configurazioni.", "Una pianta per ogni metratura e tipo di spazio."), ("Grafiche in tessuto.", "Si cambiano senza cambiare la struttura."), ("Magazzino.", "Conservazione e controllo tra una fiera e l'altra."), ("Montaggio.", "Rapido, anche con squadre ridotte.")]),
 '/ledwall-e-illuminazione-stand/': ('Un esempio: <span class="grad">luce e video su uno stand di 80 mq</span>', [
   "Su uno stand di 80 metri quadri, il progetto luci prevede profili LED lineari nella struttura del soffitto per la luce generale, faretti orientabili sui prodotti e una grafica retroilluminata sul lato più visibile dal corridoio. Al centro, un ledwall di 4 per 2,5 metri mostra un video di trenta secondi senza audio.",
   "Prima di confermare, si calcola la potenza elettrica totale e si richiede all'ente fiera l'allaccio adeguato, perché una potenza sottostimata significa salvavita che scatta il primo giorno. Il contenuto del ledwall si prepara nel formato e nella risoluzione giusti, e si prova prima dell'apertura."],
   [("Progetto luci.", "Luce generale, accenti sui prodotti, grafiche retroilluminate."), ("Ledwall.", "Dimensione, passo dei pixel, struttura e regia."), ("Contenuti video.", "Formato corretto, durata breve, leggibili senza audio."), ("Impianto e potenza.", "Calcolo, allaccio e dichiarazione di conformità."), ("Prove.", "Accensione e regolazione prima dell'apertura.")]),
 '/progettazione-stand-fieristici/': ('Un esempio: <span class="grad">dal brief al render in due settimane</span>', [
   "Il brief arriva con tre informazioni: fiera, 48 metri quadri a penisola, obiettivo far provare un macchinario e incontrare distributori esteri. Nella prima settimana prepariamo due proposte in render 3D: una più aperta, con il macchinario al centro, e una con una saletta riunioni chiusa sul fondo.",
   "Il cliente sceglie la seconda, chiede di spostare il banco e di ingrandire il marchio sul lato del corridoio principale. Nella seconda settimana il render è aggiornato, i disegni esecutivi sono pronti per l'ente fiera e il preventivo è dettagliato voce per voce. Da lì parte la produzione."],
   [("Brief.", "Obiettivi, spazio, prodotti, budget, vincoli del regolamento."), ("Render 3D.", "Una o più proposte, modificate fino all'approvazione."), ("Disegni esecutivi.", "Piante, sezioni, prospetti per produzione ed ente fiera."), ("Schede materiali.", "Finiture, reazione al fuoco, certificazioni."), ("Preventivo.", "Voce per voce, dal progetto al montaggio.")]),
 '/stand-fieristici-ecosostenibili/': ('Un esempio: <span class="grad">meno materiale, stesso impatto</span>', [
   "Uno stand ecosostenibile non è uno stand di cartone: è uno stand pensato per durare e per produrre meno scarti. In un progetto tipico, la struttura è un sistema modulare riutilizzabile, le grafiche sono in tessuto riciclabile e si stampano solo quelle che cambiano, l'illuminazione è tutta LED e gli arredi sono a noleggio.",
   "Alla fine della fiera quasi nulla finisce in discarica: la struttura torna in magazzino, gli arredi tornano al noleggio e i tessuti si riusano o si avviano al riciclo. Il messaggio di sostenibilità si vede, perché è vero, e non serve scriverlo su un cartello."],
   [("Strutture riutilizzabili.", "Alluminio e legno pensati per più fiere."), ("Grafiche in tessuto.", "Leggere, riciclabili, stampate solo quando cambiano."), ("Illuminazione LED.", "Meno consumi e meno calore nello stand."), ("Arredi a noleggio.", "Niente acquisti destinati a una sola fiera."), ("Fine vita.", "Cosa si riusa, cosa si ricicla, cosa resta.")]),
 '/stand-preallestiti/': ('Un esempio: <span class="grad">16 mq preallestiti, ma riconoscibili</span>', [
   "Un preallestito standard ha pareti bianche, moquette blu e un fascione con il nome: in un padiglione con duecento stand uguali, è facile non essere visti. Con poco in più si cambia molto: pareti rivestite da una grafica stampata, luce sui prodotti, un banco luminoso e uno schermo con un video breve.",
   "La struttura resta quella del preallestito, e quindi costi e tempi restano contenuti; quello che cambia è la percezione di chi passa nel corridoio. È spesso il modo migliore per una prima fiera o per uno spazio piccolo."],
   [("Struttura.", "Pareti, moquette, fascione, ripostiglio se serve."), ("Grafiche.", "Pannelli o tessuti stampati al posto del bianco."), ("Luci.", "Faretti o bracci luce sui prodotti."), ("Arredi.", "Banco, tavolo, sedie, mensole."), ("Extra.", "Schermo, lightbox, vetrine, a scelta.")]),
 '/grafica-per-stand-fieristici/': ('Un esempio: <span class="grad">la stessa grafica, vista da dieci metri</span>', [
   "Una grafica pensata per un catalogo non funziona su una parete di tre metri vista dal corridoio. In un progetto tipico, il fondo dello stand porta solo il marchio e una frase di cinque parole su cosa fate, in alto, sopra le teste dei visitatori; le informazioni di dettaglio scendono all'altezza degli occhi, vicino ai prodotti.",
   "Prima di stampare si preparano i file nel formato del supporto, con abbondanza, risoluzione e profilo colore corretti, e si fa una prova colore del marchio. Il tessuto teso retroilluminato rende i colori più brillanti; il forex e il dibond sono più adatti a testi piccoli e dettagli."],
   [("Concept grafico.", "Messaggio principale, gerarchia, colori del marchio."), ("Impaginazione.", "File esecutivi per ogni supporto, con le misure reali."), ("Prova colore.", "Per il marchio e i colori critici."), ("Stampa.", "Tessuto, pannelli rigidi, adesivi, lightbox."), ("Posa.", "Montaggio delle grafiche nei giorni di allestimento.")]),
}

def blocco(path):
    t, paras, lista = X[path]
    ps = ''.join(f'\n      <p>{p}</p>' for p in paras)
    li = ''.join(f'\n      <li><b>{b}</b> {d}</li>' for b, d in lista)
    return (f'{A}<section id="esempio">\n  <div class="wrap">\n    <div class="sec-head">\n      <div class="eyebrow mono">Un esempio</div>\n      <h2 class="title" data-rv="up">{t}</h2>\n    </div>\n'
            f'    <div class="pg-testo" data-rv="up">{ps}\n    </div>\n  </div>\n</section>\n'
            f'<section id="preventivo">\n  <div class="wrap">\n    <div class="sec-head">\n      <h2 class="title" data-rv="up">Cosa trovate <span class="grad">nel preventivo</span></h2>\n    </div>\n'
            f'    <ul class="pg-lista" data-rv="up">{li}\n    </ul>\n  </div>\n</section>\n{B}\n')

def inject(s, path):
    if path not in X: return s
    s = re.sub(re.escape(A) + r'.*?' + re.escape(B) + r'\n?', '', s, flags=re.S)
    for anchor in ('<section id="richiesta"', '<section id="faq">'):
        i = s.find(anchor)
        if i >= 0: return s[:i] + blocco(path) + s[i:]
    return s
