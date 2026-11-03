# -*- coding: utf-8 -*-
"""14/10/2026: blocco 'Esporre a <citta>: cosa cambia sul posto' nelle pagine /allestimenti-fieristici-<citta>/.
Contenuto specifico per citta' (accessi, logistica, particolarita' del quartiere), per differenziare le pagine.
Chiamato da lib.build; applica() lo applica alle pagine gia' pubblicate. Idempotente."""
import re, os, glob
A, B = '<!--fr-locale-->', '<!--/fr-locale-->'
D = {
'verona': ("Veronafiere è a sud del centro, a pochi minuti dall'uscita Verona Sud dell'A4 e raggiungibile dalla stazione di Porta Nuova. Durante le fiere più grandi, Vinitaly prima di tutte, il traffico in zona fiera e la disponibilità di alberghi diventano il vero vincolo: chi espone deve prenotare con mesi di anticipo.",
  "Per gli stand del vino servono banchi di degustazione, lavelli, frigoriferi e spazi riservati per i buyer; per Marmomac strutture capaci di reggere lastre e blocchi di pietra. Sono due mondi diversi nello stesso quartiere, e lo stand va pensato per il settore, non solo per la metratura.",
  [("Accesso.","Uscita Verona Sud dell'A4, zona fiera a sud del centro."),("Alloggi.","Per le fiere grandi si prenota con largo anticipo, anche per la squadra di montaggio."),("Settori.","Vino, pietra, agricoltura, cavalli, moto: esigenze di stand molto diverse.")]),
'padova': ("La Fiera di Padova è a ridosso del centro, a pochi passi dalla stazione ferroviaria e vicina all'uscita Padova Est. È un quartiere compatto, con padiglioni e un centro congressi: ospita fiere di settore, manifestazioni per il pubblico e convegni.",
  "Essendo in città, gli orari di carico e scarico vanno coordinati con il traffico urbano, e lo spazio per i mezzi nel piazzale è limitato nei giorni di allestimento. Per questo arriviamo con i materiali già pronti e montaggi pianificati al quarto d'ora.",
  [("Accesso.","Vicina alla stazione e all'uscita Padova Est."),("In città.","Scarichi da coordinare con il traffico urbano."),("Congressi.","Spesso stand sponsor accanto alle sale convegni.")]),
'vicenza': ("Il Vicenza Expo Centre, gestito da Italian Exhibition Group, è a ovest della città, comodo all'uscita Vicenza Ovest dell'A4. È il quartiere di VicenzaOro, uno degli appuntamenti più importanti al mondo per la gioielleria.",
  "Nelle fiere orafe lo stand è prima di tutto sicurezza e luce: vetrine con serratura, illuminazione che fa brillare metalli e pietre senza scaldarli, salottini riservati per le trattative, controllo degli accessi. Lo progettiamo così fin dal primo render.",
  [("Accesso.","Uscita Vicenza Ovest dell'A4."),("Gioielleria.","Vetrine blindate, luce dedicata, aree riservate."),("Industria.","Anche fiere della meccanica e della subfornitura.")]),
'venezia': ("A Venezia gli eventi si tengono spesso in palazzi, scuole grandi, arsenale e spazi storici, dove i materiali arrivano in barca: l'allestimento si organizza in funzione dei trasporti via acqua, del peso che si può portare a mano e dei vincoli di tutela degli edifici.",
  "A Mestre e in terraferma, invece, centri congressi e spazi espositivi sono raggiungibili su gomma. Conoscere la differenza cambia il progetto: a Venezia servono elementi leggeri, modulari e montabili senza attrezzature pesanti.",
  [("Trasporto.","In centro storico i materiali viaggiano su barca da trasporto."),("Spazi storici.","Nessun fissaggio a pareti e pavimenti tutelati."),("Mestre.","Congressi ed eventi raggiungibili su strada.")]),
'treviso': ("Treviso è la nostra provincia: tra Mansuè e Fontanelle lavoriamo a pochi chilometri da ogni spazio espositivo, congressuale ed evento del territorio, dalla città alle colline del Prosecco.",
  "Qui molti allestimenti sono per eventi aziendali, inaugurazioni, showroom, mostre e degustazioni più che per fiere: lavori in cui la vicinanza permette sopralluoghi ripetuti e interventi nella stessa giornata.",
  [("Vicinanza.","Sopralluoghi e consegne in giornata."),("Eventi.","Showroom, inaugurazioni, degustazioni in cantina."),("Riuso.","Stand e arredi conservati nel nostro magazzino.")]),
'longarone': ("Longarone Fiere Dolomiti è in valle del Piave, alla fine dell'A27: è la sede della Mostra Internazionale del Gelato Artigianale e di fiere legate alla montagna e all'arredo.",
  "Le fiere di Longarone cadono spesso nei mesi freddi, in montagna: trasporti e montaggi vanno pianificati tenendo conto del meteo, e gli stand del gelato richiedono allacci elettrici e idrici dimensionati per vetrine e macchine.",
  [("Accesso.","A27 fino a Pian di Vedoia, poi statale."),("Stagione.","Fiere invernali: meteo e trasporti da prevedere."),("Gelato.","Vetrine refrigerate e potenze elettriche adeguate.")]),
'milano': ("Fiera Milano Rho è il quartiere fieristico più grande d'Italia, raggiungibile con la metropolitana M1 (fermata Rho Fiera), in treno e dalle autostrade. Allianz MiCo, in città, ospita congressi ed eventi.",
  "A Rho tutto si gioca sull'organizzazione: prenotazione degli scarichi, pass, orari di montaggio e vie di accesso ai padiglioni. Dai nostri uffici di Vermezzo con Zelo siamo a circa mezz'ora, e per le fiere più grandi la squadra lavora su turni per rispettare finestre di montaggio strette.",
  [("Accesso.","M1 Rho Fiera, treno, autostrade A4 e A8."),("Organizzazione.","Scarichi, pass e orari gestiti da noi."),("Vicinanza.","Uffici a Vermezzo con Zelo, a mezz'ora dalla fiera.")]),
'bergamo': ("La Fiera di Bergamo è a sud della città, accanto all'aeroporto di Orio al Serio e vicina all'uscita Bergamo dell'A4: comoda per chi arriva in aereo o da tutta la Lombardia.",
  "Ospita fiere tecniche dell'industria, della manutenzione e dell'automazione, dove lo stand deve mostrare macchine e impianti: pedane, allacci di forza motrice e spazi per le dimostrazioni dal vivo.",
  [("Accesso.","Accanto all'aeroporto di Orio al Serio, uscita Bergamo dell'A4."),("Industria.","Fiere della manutenzione e dell'automazione."),("Demo.","Allacci e pedane per macchine in funzione.")]),
'brescia': ("Brixia Forum è il polo espositivo di Brescia, vicino al casello di Brescia Ovest; a pochi chilometri, il Centro Fiera di Montichiari ospita fiere dell'agricoltura, della meccanica e del Garda.",
  "Brescia è terra di metallurgia e meccanica: molte fiere portano macchinari pesanti e lamiere, e lo stand deve fare i conti con portate dei pavimenti, mezzi di sollevamento e tempi di posizionamento delle macchine.",
  [("Accesso.","Brixia Forum vicino a Brescia Ovest; Montichiari a sud-est."),("Macchine.","Portate, carrelli e posizionamento coordinati con l'ente."),("Due poli.","Brescia città e Montichiari, con calendari diversi.")]),
'bologna': ("BolognaFiere è a nord-est del centro, con un'uscita dedicata sulla tangenziale: è uno dei quartieri più grandi d'Italia e ospita Cosmoprof, Cersaie, EIMA e decine di fiere internazionali.",
  "Ogni grande fiera bolognese ha esigenze precise: pareti che reggono il peso delle ceramiche al Cersaie, luce e vetrine per la cosmetica al Cosmoprof, spazi enormi e pedane carrabili per le macchine agricole all'EIMA. Nei giorni di allestimento il traffico in tangenziale va messo in conto negli orari.",
  [("Accesso.","Uscita Fiera della tangenziale, A14 e A13."),("Ceramica.","Pareti portanti per lastre e campionature."),("Agricoltura.","Pedane carrabili e aree esterne per l'EIMA.")]),
'rimini': ("Il Rimini Expo Centre ha una fermata ferroviaria dedicata, Rimini Fiera, ed è vicino all'uscita Rimini Nord dell'A14. Ospita Sigep, Ecomondo, Key, Macfrut e TTG.",
  "Le fiere riminesi sono spesso dimostrative: macchine per gelateria e pasticceria al lavoro, impianti per l'ambiente e l'energia, prodotti da assaggiare. Allacci idrici ed elettrici, scarichi e materiali lavabili vanno previsti già nella pianta dello stand.",
  [("Accesso.","Stazione Rimini Fiera, A14 uscita Rimini Nord."),("Dimostrazioni.","Acqua, scarichi e potenza elettrica per le macchine."),("Alta stagione.","Fuori dall'estate gli alberghi vicini sono più disponibili.")]),
'parma': ("Fiere di Parma è a nord della città, vicina all'uscita Parma dell'A1: è la casa di Cibus e Cibus Tec, i punti di riferimento per l'agroalimentare e le tecnologie per l'industria alimentare.",
  "Per Cibus lo stand è una vetrina del prodotto con area di assaggio, frigoriferi, cucina e salottini per i buyer della distribuzione; per Cibus Tec servono spazi per linee e macchine di processo. Dalla sede di Trumello, Parma è a un'ora e mezza di strada.",
  [("Accesso.","Uscita Parma dell'A1."),("Food.","Banchi assaggio, frigoriferi e aree buyer."),("Distanza.","Circa un'ora e mezza da Trumello (PV).")]),
'pordenone': ("Pordenone Fiere è la fiera più vicina alla nostra sede di Mansuè: pochi chilometri, sulla direttrice per la A28. Ospita Sicam, la fiera dei componenti per l'industria del mobile, e Samuexpo.",
  "Essendo a due passi da casa, qui possiamo fare sopralluoghi ripetuti, far arrivare i materiali in poche ore e intervenire durante la fiera in pochi minuti. Per Sicam, gli stand devono mostrare ferramenta e finiture da toccare con mano.",
  [("Vicinanza.","Pochi chilometri da Mansuè e Fontanelle."),("Mobile.","Componenti e finiture da toccare."),("Interventi.","Assistenza durante la fiera in tempi brevi.")]),
'udine': ("Udine e Gorizia Fiere ha il quartiere principale a Martignacco, appena fuori Udine. Ospita fiere per il pubblico e di settore legate al territorio friulano: casa, agricoltura, montagna, enogastronomia.",
  "Per le aziende friulane siamo vicini: dalla sede di Mansuè, Udine è a circa un'ora. Sopralluoghi, consegne rapide e assistenza durante la fiera sono parte del servizio.",
  [("Sede.","Quartiere fieristico di Martignacco, vicino a Udine."),("Settori.","Casa, agricoltura, montagna, enogastronomia."),("Distanza.","Circa un'ora da Mansuè.")]),
'bolzano': ("Fiera Bolzano è nella zona produttiva a sud della città, vicina all'uscita Bolzano Sud dell'A22. Ospita fiere sull'edilizia sostenibile, sul turismo alpino e sull'agricoltura di montagna.",
  "In Alto Adige grafiche, cartelli e materiali informativi dello stand vanno quasi sempre preparati in italiano e in tedesco: li impostiamo bilingue fin dal progetto. Molti espositori chiedono anche materiali certificati e stand dal basso impatto ambientale.",
  [("Accesso.","Uscita Bolzano Sud dell'A22."),("Bilingue.","Grafiche in italiano e tedesco."),("Sostenibilità.","Materiali riutilizzabili e certificati.")]),
'riva-del-garda': ("Riva del Garda Fierecongressi è sul lago, raggiungibile dall'A22 (uscita Rovereto Sud) con un tratto di strada statale. Ospita Expo Riva Schuh e Gardabags, fiere internazionali di calzature e borse, e congressi.",
  "Le strade del Garda e gli spazi di manovra intorno al quartiere rendono importante scegliere i mezzi giusti e programmare gli scarichi. Per le fiere delle calzature servono pareti attrezzate e mensole per centinaia di modelli, con luce che rispetti i colori dei materiali.",
  [("Accesso.","A22 uscita Rovereto Sud, poi statale."),("Mezzi.","Furgoni e camion adatti alle strade del lago."),("Calzature.","Pareti attrezzate per campionari ampi.")]),
'firenze': ("La Fortezza da Basso, sede delle fiere di Pitti Immagine e di Taste, è in pieno centro, a pochi passi dalla stazione di Santa Maria Novella. Lavorare qui significa fare i conti con la zona a traffico limitato, con i permessi per i mezzi e con un complesso storico tutelato.",
  "Per Pitti lo stand è uno showroom: pareti attrezzate per i capi, luce calibrata, materiali di qualità e spazi per gli ordini. Dalla sede di Trumello, Firenze è a circa tre ore di strada; trasporto e accessi in ZTL li organizziamo noi.",
  [("Centro storico.","ZTL e permessi per i mezzi da organizzare."),("Spazio tutelato.","Nessun intervento su strutture storiche."),("Moda.","Stand come showroom per buyer internazionali.")]),
'torino': ("Lingotto Fiere è nell'ex stabilimento del Lingotto, a sud del centro, accanto all'Oval: ospita il Salone del Libro, fiere dell'energia e del restauro e grandi eventi. Dalla nostra sede di Trumello è a circa un'ora e mezza.",
  "Gli spazi del Lingotto hanno accessi e orari di carico precisi, e molti eventi sono aperti al pubblico con grandi flussi di visitatori: lo stand deve reggere molte persone, con percorsi chiari e spazi di vendita.",
  [("Sede.","Lingotto e Oval, a sud del centro di Torino."),("Distanza.","Circa un'ora e mezza da Trumello (PV)."),("Pubblico.","Percorsi e banchi vendita per eventi molto affollati.")]),
'genova': ("La Fiera di Genova è sul mare, al piazzale Kennedy, ed è la casa del Salone Nautico Internazionale. Dalla sede di Trumello è a circa un'ora e un quarto di strada.",
  "Al Salone Nautico molti stand sono sulle banchine e sui pontili, all'aperto: servono strutture resistenti al vento e all'umidità, pavimenti adatti all'esterno e grafiche che reggono il sole. È un allestimento diverso da quello nei padiglioni, e lo progettiamo come tale.",
  [("Sul mare.","Stand su banchine e pontili, all'aperto."),("Materiali.","Resistenti a vento, salsedine e sole."),("Distanza.","Circa un'ora e un quarto da Trumello (PV).")]),
'carrara': ("CarraraFiere è a Marina di Carrara, vicino al porto e al casello di Carrara dell'A12: ospita fiere legate al marmo, alle tecnologie per la pietra e alla nautica.",
  "Nelle fiere della pietra si espongono lastre e blocchi: pareti, pedane e pavimenti devono reggere pesi importanti, e il posizionamento dei materiali va coordinato con i mezzi di sollevamento. Dalla sede di Trumello, Carrara è a circa due ore e mezza.",
  [("Accesso.","Casello di Carrara dell'A12, vicino al porto."),("Pietra.","Strutture portanti per lastre e campionature."),("Distanza.","Circa due ore e mezza da Trumello (PV).")]),
'roma': ("La Fiera di Roma è sulla via Portuense, lungo l'autostrada Roma-Fiumicino, vicino all'aeroporto; La Nuvola all'EUR è il centro congressi più noto della città. A Roma molte occasioni espositive sono legate a congressi, istituzioni e associazioni.",
  "Per i congressi servono stand sponsor, desk di accoglienza e segnaletica montati in finestre di poche ore; per le fiere al quartiere della Portuense, la logistica a distanza: trasporto dedicato, squadra in trasferta e partner locali quando conviene.",
  [("Accesso.","Autostrada Roma-Fiumicino, vicino all'aeroporto."),("Congressi.","Montaggi rapidi alla Nuvola dell'EUR e nei centri congressi."),("A distanza.","Trasporto e squadre organizzati da noi.")]),
'napoli': ("La Mostra d'Oltremare, nel quartiere di Fuorigrotta, è il polo fieristico di Napoli: padiglioni storici immersi nel verde, accanto allo stadio, con fiere per il pubblico, turismo, nautica e congressi.",
  "Gli spazi della Mostra sono in parte storici e all'aperto: il progetto deve tenere conto dei padiglioni esistenti, delle aree esterne e dei grandi flussi di pubblico. Trasporto e squadre li organizziamo dal Nord con largo anticipo.",
  [("Sede.","Mostra d'Oltremare, Fuorigrotta."),("Spazi storici.","Padiglioni tutelati e aree all'aperto."),("A distanza.","Logistica pianificata in anticipo.")]),
'bari': ("La Fiera del Levante è sul lungomare di Bari, a ovest del centro: è il polo espositivo più importante del Sud, con fiere campionarie, agroalimentari, della casa e congressi.",
  "Per le aziende che espongono a Bari organizziamo trasporto dedicato e squadra in trasferta, con partner locali quando conviene. Il clima permette spesso allestimenti anche nelle aree esterne del quartiere, da progettare per sole e vento.",
  [("Sede.","Fiera del Levante, lungomare di Bari."),("Settori.","Agroalimentare, casa, campionaria, congressi."),("A distanza.","Trasporto e squadre organizzati in anticipo.")]),
}
NOMI = {'riva-del-garda':'Riva del Garda'}
def blocco(slug):
    p1, p2, li = D[slug]; c = NOMI.get(slug, slug.capitalize())
    lis = ''.join(f'\n      <li><b>{b}</b> {t}</li>' for b, t in li)
    return (f'{A}<section id="locale">\n  <div class="wrap">\n    <div class="sec-head">\n      <h2 class="title" data-rv="up">Esporre a {c}: <span class="grad">cosa cambia sul posto</span></h2>\n    </div>\n'
            f'    <div class="pg-testo" data-rv="up">\n      <p>{p1}</p>\n      <p>{p2}</p>\n    </div>\n    <ul class="pg-lista" data-rv="up">{lis}\n    </ul>\n  </div>\n</section>\n{B}\n')
def inject(s, path):
    m = re.match(r'^/allestimenti-fieristici-([a-z-]+)/$', path)
    if not m or m.group(1) not in D: return s
    s = re.sub(re.escape(A) + r'.*?' + re.escape(B) + r'\n?', '', s, flags=re.S)
    i = s.find('<!--fr-logistica-->')
    if i < 0: i = s.find('<section id="sapere">')
    if i < 0: return s
    return s[:i] + blocco(m.group(1)) + s[i:]
def applica():
    R = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')); n = 0
    for slug in D:
        f = os.path.join(R, f'allestimenti-fieristici-{slug}', 'index.html')
        if not os.path.exists(f): print('manca', slug); continue
        s = open(f, encoding='utf-8').read(); s2 = inject(s, f'/allestimenti-fieristici-{slug}/')
        if s2 != s: open(f, 'w', encoding='utf-8').write(s2); n += 1
    print('pagine citta con blocco locale:', n)
if __name__ == '__main__': applica()
