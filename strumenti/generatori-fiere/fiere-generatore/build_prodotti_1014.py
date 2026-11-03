# -*- coding: utf-8 -*-
# 14/10/2026: /totem-pubblicitari/ e /espositori-pubblicitari/ (ricerche di prodotto: totem pubblicitari, espositori per negozi).
from nuove_common import *
ESP="/espositori-desk-totem-per-fiere/"; TOT="/totem-pubblicitari/"; EXP="/espositori-pubblicitari/"
PROD=[("Espositori, desk e totem per fiere",ESP),("Ledwall e illuminazione","/ledwall-e-illuminazione-stand/"),("Grafica per stand","/grafica-per-stand-fieristici/"),
 ("Allestimenti per eventi, showroom e negozi","/allestimenti-eventi-showroom-negozi/"),("Noleggio stand","/noleggio-stand-fieristici/"),("Stand su misura","/stand-fieristici-su-misura/")]
# ---------------- TOTEM
m=hero("Totem pubblicitari",'Totem pubblicitari personalizzati: <span class="grad">progettati e prodotti da noi</span>.',
  "Totem in legno, luminosi, con monitor o touch screen, bifacciali, porta depliant: per fiere, negozi, showroom, hall aziendali ed eventi. Li progettiamo sulla tua grafica, li facciamo produrre dai nostri laboratori partner e li consegniamo pronti, in tutta Italia.",
  "Chiedi un preventivo",CT,"I tipi di totem","#tipi")
m+=cards("tipi","I totem che realizziamo","Ogni totem nasce su misura: dimensioni, materiali, luce e grafica decisi insieme in base a dove andrà e a cosa deve comunicare.",
  [("Totem in legno","Struttura in legno o multistrato, laccata o con finitura a vista, con grafica applicata, logo in rilievo o mensole per il prodotto. Robusto, elegante, riutilizzabile per anni."),
   ("Totem luminosi","Totem retroilluminati a LED con grafica in tessuto teso o pannello in plexiglass: si vedono da lontano anche nei padiglioni più affollati e nei negozi."),
   ("Totem con monitor e touch","Totem con schermo per video, presentazioni o cataloghi interattivi, con cablaggi nascosti e vano tecnico ispezionabile. Ideali per fiere, showroom e reception."),
   ("Totem bifacciali e a colonna","Totem a due facce o colonne con grafica a 360°, per essere letti da ogni direzione: all'ingresso dello stand, al centro del negozio, nei corridoi di un evento."),
   ("Totem porta depliant","Totem con tasche per cataloghi, listini e biglietti da visita, o con porta tablet per raccogliere i contatti dei visitatori."),
   ("Totem per esterni","Per piazzali, ingressi e dehors realizziamo totem con materiali adatti all'aperto e basi zavorrate: ne valutiamo insieme posizione, esposizione e fissaggio.")])
m+=testo("come",'Come lavoriamo: <span class="grad">dal disegno alla consegna</span>',None,
  ["Partiamo da dove andrà il totem e da cosa deve fare: attirare da lontano, mostrare un video, distribuire cataloghi, indicare un percorso. Ti mandiamo un disegno quotato e un render, poi prepariamo i file di stampa con le prove colore.",
   "La struttura la produciamo noi, senza intermediari: per questo possiamo fare pezzi unici o piccole serie coordinate (per esempio un totem per ogni punto vendita) con tempi e prezzi sotto controllo. Per le fiere usiamo materiali certificati in Classe 1 di reazione al fuoco, come chiedono i regolamenti tecnici.",
   "Se il totem serve per una fiera, lo portiamo e lo montiamo direttamente nello stand, insieme a desk, roll-up ed espositori coordinati. Quando lo aggiorni basta cambiare la grafica: la struttura resta."],
  [("Su misura.","Altezza, larghezza, profondità e forma decise sul tuo spazio."),("Grafica compresa.","File di stampa, prove colore e stampa ad alta risoluzione."),
   ("Produzione propria.","Laboratori a Fontanelle (TV) e Trumello (PV): nessun ricarico di terzi."),("Consegna in tutta Italia.","Con trasportatori di fiducia o corriere, montaggio compreso se serve.")])
m+=chips("usi","Dove si usano",None,[("Totem per fiere",ESP),("Stand su misura","/stand-fieristici-su-misura/"),("Negozi, showroom ed eventi","/allestimenti-eventi-showroom-negozi/"),("Espositori pubblicitari per negozi",EXP),("Ledwall e monitor","/ledwall-e-illuminazione-stand/"),("Grafica per stand","/grafica-per-stand-fieristici/")])
qa=[("Realizzate totem pubblicitari personalizzati?","Sì: progettiamo e produciamo totem su misura in legno, luminosi, con monitor o touch screen, bifacciali e porta depliant, con la tua grafica."),
    ("Fate anche totem pubblicitari per esterni?","Sì, con materiali adatti all'aperto e basi zavorrate o fissaggi a terra. Prima valutiamo insieme posizione ed esposizione, perché vento e sole cambiano le scelte di struttura e stampa."),
    ("Si può fare un solo totem o servono quantità minime?","Si può fare anche un pezzo unico. Per catene di negozi o reti di vendita produciamo piccole serie identiche."),
    ("In quanto tempo è pronto un totem?","Dipende da materiali e quantità: dopo l'approvazione del disegno e della grafica ti diamo una data di consegna precisa. Se serve per una fiera, lavoriamo a ritroso dalla data di montaggio."),
    ("Quanto costa un totem pubblicitario?","Dipende da dimensioni, materiali, luce, monitor e quantità. Ti mandiamo un preventivo voce per voce sul tuo progetto, senza impegno."),
    ("Consegnate in tutta Italia?","Sì, con trasportatori di fiducia o con corriere dedicato. Abbiamo sedi in Veneto (Mansuè e Fontanelle, TV) e in Lombardia (Trumello, PV e Vermezzo con Zelo, MI).")]
node=svc(TOT,"Totem pubblicitari personalizzati","Progettazione e produzione di totem pubblicitari",
  "Totem pubblicitari su misura in legno, luminosi, con monitor o touch screen, bifacciali, porta depliant e per esterni, per fiere, negozi, showroom ed eventi.",
  ["Totem in legno personalizzati","Totem luminosi a LED","Totem con monitor e touch screen","Totem bifacciali e a colonna","Totem porta depliant","Totem pubblicitari per esterni"])
print(pagina(TOT,"Totem pubblicitari personalizzati: legno, luminosi, LED",
  "Totem pubblicitari su misura: in legno, luminosi, con monitor, bifacciali e per esterni. Per fiere, negozi ed eventi, prodotti da noi e consegnati in tutta Italia.",
  "Totem pubblicitari personalizzati — Danova Tech","Totem in legno, luminosi, con monitor e per esterni, realizzati su misura con i nostri laboratori partner.",
  crumbs("Totem pubblicitari"),m,qa,[node],[(t,u) for t,u in PROD]+[("Espositori pubblicitari",EXP)]+SERVIZI_LINKS[:2],cta_t="Parliamo del tuo progetto.",form=False))
# ---------------- ESPOSITORI PUBBLICITARI
m=hero("Espositori pubblicitari",'Espositori pubblicitari su misura: <span class="grad">per negozi, showroom e fiere</span>.',
  "Espositori da terra e da banco, a parete, a isola e a gondola, in legno e materiali misti, con la grafica del tuo marchio. Li progettiamo intorno al prodotto e li facciamo produrre dai nostri laboratori partner: un pezzo unico per lo showroom o una serie per tutti i punti vendita.",
  "Chiedi un preventivo",CT,"Per quali prodotti","#prodotti")
m+=cards("prodotti","Espositori per ogni tipo di prodotto","Ogni prodotto ha un modo giusto per essere guardato, preso in mano e comprato: partiamo da lì.",
  [("Espositori per scarpe e borse","Mensole inclinate, ripiani a gradoni e pareti attrezzate per calzature, pelletteria e accessori, con luce che valorizza i materiali."),
   ("Espositori per abbigliamento","Appenderie, pareti a doghe, tavoli espositivi e isole per negozi di abbigliamento e corner monomarca."),
   ("Espositori per piastrelle e ceramiche","Pannelli estraibili, pareti campionarie e cavalletti robusti per piastrelle, pietre, parquet e superfici, anche di grande formato."),
   ("Espositori per profumeria e cosmetica","Espositori da banco e a parete con ripiani in plexiglass, luce LED e tester, per profumerie, farmacie e corner beauty."),
   ("Espositori per alimentari e vino","Gondole, cassette, scaffali per bottiglie ed espositori da banco per gastronomia, enoteche, pane, snack e prodotti tipici."),
   ("Espositori da banco e per riviste","Piccoli espositori per la cassa, porta depliant, porta riviste e porta cataloghi coordinati con il resto dell'arredo.")])
m+=testo("come",'Perché farli <span class="grad">su misura</span>',None,
  ["Un espositore di catalogo va bene per tutti e quindi per nessuno: le misure non tornano, la grafica è un adesivo, il prodotto si vede male. Un espositore su misura invece nasce dalle dimensioni del prodotto, dallo spazio del negozio e da come il cliente si muove.",
   "Produciamo noi le strutture in legno, nei laboratori di Fontanelle (TV) e Trumello (PV): possiamo fare il prototipo, correggerlo e poi produrre la serie per tutti i punti vendita con la stessa qualità. Gli stessi espositori possono andare in fiera, coordinati con lo stand."],
  [("Prototipo.","Un primo pezzo da provare prima della serie."),("Serie coordinate.","Uguali in tutti i negozi della rete."),
   ("Grafica e luce.","Stampa, loghi in rilievo, LED integrati."),("Montaggio.","Consegna e posa in negozio o in fiera.")])
m+=chips("collegati","Pagine collegate",None,[("Totem pubblicitari",TOT),("Allestimenti per negozi e showroom","/allestimenti-eventi-showroom-negozi/"),("Espositori per fiere",ESP),("Stand su misura","/stand-fieristici-su-misura/"),("Stand per moda e calzature","/stand-fieristici-moda-e-calzature/"),("Stand per cosmetica","/stand-fieristici-cosmetica-e-beauty/")])
qa=[("Realizzate espositori per negozi su misura?","Sì: progettiamo e produciamo espositori da terra, da banco, a parete e a isola per negozi, showroom e corner, con la grafica del tuo marchio."),
    ("Potete produrre una serie di espositori per più punti vendita?","Sì. Partiamo da un prototipo, lo approviamo insieme e poi produciamo la serie, identica per tutti i negozi."),
    ("Di che materiali sono gli espositori?","Soprattutto legno e multistrato, laccati o a vista, combinati con metallo, plexiglass, vetro e luci LED secondo il prodotto."),
    ("Gli espositori si possono usare anche in fiera?","Sì: li coordiniamo con lo stand, così gli stessi elementi lavorano in negozio e in fiera."),
    ("Quanto costa un espositore pubblicitario su misura?","Dipende da dimensioni, materiali, finiture e quantità. Ti mandiamo un preventivo voce per voce sul tuo progetto.")]
node=svc(EXP,"Espositori pubblicitari su misura","Progettazione e produzione di espositori per negozi",
  "Espositori pubblicitari su misura per negozi, showroom e fiere: da terra, da banco, a parete e a isola, per scarpe, abbigliamento, piastrelle, cosmetica, alimentari e vino.",
  ["Espositori per scarpe e borse","Espositori per abbigliamento","Espositori per piastrelle","Espositori per profumeria","Espositori per alimentari e vino","Espositori da banco"])
print(pagina(EXP,"Espositori pubblicitari su misura per negozi e fiere",
  "Espositori pubblicitari su misura per negozi, showroom e fiere: scarpe, abbigliamento, piastrelle, cosmetica, vino. Prodotti da noi, anche in serie.",
  "Espositori pubblicitari su misura — Danova Tech","Espositori da terra, da banco e a parete per negozi, showroom e fiere, realizzati su misura con i nostri laboratori partner.",
  crumbs("Espositori pubblicitari"),m,qa,[node],[("Totem pubblicitari",TOT)]+[(t,u) for t,u in PROD]+SERVIZI_LINKS[:2],cta_t="Parliamo del tuo progetto.",form=False))
