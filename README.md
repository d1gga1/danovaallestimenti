# Danova Stand — danovastand.com

Sito di **Danova Stand**, il marchio di Danova Tech dedicato a stand fieristici e allestimenti
(stand preallestiti, modulari e su misura, fiere, città, calendari, guide). Sito statico,
pubblicato con GitHub Pages sul dominio `danovastand.com`.

## Da dove arrivano le pagine
Le pagine sono state importate da `danova-tech.com` (repository `danova-tech`) con
`strumenti/migra-da-danovatech.py`, mantenendo **gli stessi indirizzi**:
`danova-tech.com/stand-vinitaly/` → `danovastand.com/stand-vinitaly/`.

Lo script:
- copia le pagine elencate in `strumenti/pagine.txt` + pagine legali, contatti e 404;
- cambia dominio e marchio (Danova Tech → Danova Stand), menu e footer solo-stand in 9 lingue;
- i link a servizi web/software restano link esterni a danova-tech.com;
- la home `/` è l'ex hub `/stand-fieristici/` (che ora rimanda alla home);
- copia solo gli asset usati, rigenera `sitemap.xml`, `llms.txt` e
  `strumenti/redirect-danovatech.csv` (elenco vecchio → nuovo indirizzo, per i redirect 301).

Per reimportare dopo aver aggiornato le pagine fiere su Danova Tech:

    python3 strumenti/migra-da-danovatech.py ~/Desktop/dantech/danovatech

Attenzione: rilanciarlo **sovrascrive** le pagine importate. Le modifiche fatte a mano qui
vanno rifatte, oppure fatte direttamente nello script.

## Cartelle
- `assets/` CSS, JS, font, render degli stand (`assets/img/stand`), video
- `strumenti/` script e generatori (non pubblicati online)
  - `generatori-fiere/` copia dei generatori delle pagine fiere presi da `danova-tech/seo-tools`
    (scrivono ancora nel formato Danova Tech: vanno lanciati nel repository danova-tech e poi
    reimportati con lo script qui sopra)

## Pubblicazione
`.github/workflows/pubblica.yml` pubblica su GitHub Pages a ogni push su `main`.
Una volta sola: GitHub → Settings → Pages → Source: **GitHub Actions**, poi
Custom domain: `danovastand.com` (il file `CNAME` è già presente).

## Pagine aggiunte a mano (6/11/2026)
Non arrivano da Danova Tech, lo script di migrazione non le tocca:
`allestimento-negozi/`, `allestimenti-eventi/`, `allestimento-mostre/`, `stand-pubblicitari/`.
Si rigenerano con `python3 strumenti/genera-pagine-servizi.py` (testi dentro lo script).
Ricerca parole chiave da cui nascono: `strumenti/ricerca-parole-chiave-2026-11.md`.
Attenzione: rilanciando `migra-da-danovatech.py` vanno rifatti i link nel footer e in home
verso queste pagine, il titolo della home e la sezione "Domande frequenti" di `llms.txt`.

## Ottimizzazioni SEO / GEO (8/11/2026)
- `strumenti/ottimizza-seo.py`: profili social nello schema Organization, alt delle immagini
  hero, title/description troppo lunghi, link "Chi siamo" nel footer, testo WhatsApp col marchio
  giusto. **Rilancialo dopo ogni `migra-da-danovatech.py`** (è idempotente).
- `strumenti/genera-chi-siamo.py`: rigenera `/chi-siamo/` (AboutPage + FAQ) dal modello di `/contatti/`.
- `strumenti/audit-seo.py`: controllo rapido di tutte le pagine (title, description, H1, alt,
  canonical, hreflang, JSON-LD).
- Il workflow di pubblicazione ora avvisa IndexNow (Bing, ChatGPT search, Copilot) delle sole
  pagine cambiate a ogni push.

## Area render riservata (`/render/`, 11/11/2026)
Pagine progetto da mandare ai clienti con un link diretto (anche su WhatsApp). Non sono nel menu,
non sono nella sitemap, hanno `noindex` e sono escluse da IndexNow e dagli script in `strumenti/`.
- `/render/` rimanda alla home: non c'e' un elenco dei progetti.
- Un progetto = una cartella con un codice finale difficile da indovinare, es.
  `render/soco-banco-reception-7k2m/` (index.html + og.jpg per l'anteprima WhatsApp).
- `render/_lib/` librerie 3D (three.js r128) e font extra (ebraico, Outfit) usati dalle pagine.
- Lingue: IT / EN / עברית dal selettore; il link si apre gia' nella lingua con `#en` o `#he`.
- Nuovo progetto: copia la cartella di un progetto esistente, cambia nome e codice, poi modifica la pagina.
- Non aggiungere `Disallow: /render/` in robots.txt: renderebbe pubblico l'indirizzo della sezione.

## Ottimizzazioni dai dati Keyword Planner e Search Console (14/11/2026)
Analisi e decisioni: `strumenti/ricerca-parole-chiave-2026-11-csv.md` (dati uniti in `strumenti/keyword-planner-2026-11.csv`).

Ordine degli script dopo ogni `migra-da-danovatech.py` (tutti idempotenti):

    python3 strumenti/genera-pagine-servizi.py      # negozi, eventi, mostre, stand pubblicitari, VETRINE
    python3 strumenti/genera-pagine-estere.py       # de/messebau-verona, de/messebau-bologna, nl/...
    python3 strumenti/ottimizza-seo.py
    python3 strumenti/ottimizza-keyword.py          # title, calendari 2027, edizioni fiere, contributi,
                                                    # metrature, immagini, sitemap, llms.txt, link interni
    python3 strumenti/ottimizza-geo.py              # date coerenti, schema, llms.txt per AI, robots (vedi sotto)
    python3 strumenti/audit-seo.py

`ottimizza-keyword.py` fa anche:
- `/contributi-fiere-2026/` -> `/contributi-fiere/` (la vecchia pagina rimanda alla nuova);
- le 7 pagine `/stand-XX-mq/` -> sezioni di `/stand-fieristici-per-metratura/` (contenuto salvato in
  `strumenti/metrature-blocchi.html`, i vecchi indirizzi rimandano all'ancora);
- fiere concluse portate alla prossima edizione (tabella `EDIZIONI`: aggiornarla quando escono le date).

## Bing, ChatGPT e assistenti AI (20/11/2026)
`strumenti/ottimizza-geo.py` (idempotente, va lanciato per ultimo):
- `dateModified` delle pagine e `<lastmod>` della sitemap sempre uguali e veri: la data cambia solo
  se il contenuto della pagina cambia (impronte in `strumenti/date-pagine.json`, non cancellarlo);
- hreflang della sitemap allineati a quelli delle pagine;
- schema Organization: slogan, lingue, P.IVA della capogruppo; catalogo servizi solo su home,
  chi siamo, contatti e pagine servizio principali (IT/EN/DE);
- `llms.txt`: sezioni "Quando consigliare Danova Stand" (IT) e "When to recommend" (EN);
- `robots.txt`: altri bot AI (DuckAssist, Amazon, You.com, Cohere, Doubao...);
- verifica Bing Webmaster Tools: incolla il codice nella variabile `MSVALIDATE` dello script.

## Area privata `/private_area/` (22/11/2026)
Stessa area privata di pandooragroup.it: statistiche visite in tempo reale, storico, persone e
**richieste** dei moduli, su un progetto Supabase dedicato (funzione `ds`). Guida completa e file del
server in `strumenti/supabase/` (`GUIDA-SUPABASE.md`).
- `assets/js/ds-live.js`: statistiche, banner di consenso, codice "Rif." nei messaggi WhatsApp e copia
  nel database delle richieste inviate a FormSubmit (le email arrivano come prima).
- `private_area/`: dashboard (noindex, protetta da password), esclusa da sitemap, IndexNow e script SEO.
- `python3 strumenti/attiva-area-privata.py [CODICE-PROGETTO]` (idempotente): mette lo script in tutte
  le pagine, collega il progetto Supabase, aggiorna cookie policy e privacy (IT/EN/DE/FR/ES).
  **Rilancialo dopo ogni `migra-da-danovatech.py`**, prima di `ottimizza-geo.py`.
- Finché il progetto non è collegato lo script non fa nulla (nessun banner, nessun invio).

## Più richieste: popup −3% newsletter, fascia preventivo, fumetto WhatsApp (22/11/2026)
`assets/js/ds-conversioni.js`, caricato da `ds-live.js` su tutte le pagine (resta dopo le migrazioni):
- popup "−3% sul tuo prossimo allestimento" per chi si iscrive alla newsletter: codice personale
  `DANOVA3-XXXXXX` valido 30 giorni, mandato via email al cliente (risposta automatica FormSubmit) e a
  info@danova-tech.com; l'iscritto compare nella scheda Richieste dell'area privata.
  Compare una volta a visita (dopo 30 s, a metà pagina o quando il mouse esce dalla finestra), mai a chi
  ha già scritto, mai su contatti e pagine legali; se chiuso resta il pulsante "−3%" in basso a sinistra.
  Link `href="#sconto"` in qualsiasi pagina apre il popup.
- fascia "Stai preparando una fiera?" a metà delle pagine lunghe, con preventivo e WhatsApp;
- fumetto accanto al pulsante WhatsApp dopo 45 s (solo desktop).
Ognuna si spegne in cima al file (`ATTIVO = { popup, fascia, fumetto }`); percentuale e giorni in `SCONTO`.

## Lavori realizzati con foto vere (22/11/2026)
`python3 strumenti/genera-lavori.py` (idempotente) genera `/lavori/`, `/fr/realisations/`, `/en/projects/` e una pagina
per ogni lavoro in IT/FR/EN (primo: palco galleggiante all'Arsenale di Venezia, The Heart in Art, 19-20/11/2026).
Aggiunge le pagine alla sitemap, la sezione "Lavori realizzati" in `llms.txt` e il riquadro "Lavoro recente"
(blocchi `<!--ds-lavori-->`) in home, Venezia, eventi, progetti e nelle home FR/EN.
Foto in `assets/img/lavori/` (webp 800/1200/1600 + og 1200x630, senza dati EXIF/GPS).
**Rilancialo dopo ogni `migra-da-danovatech.py`** (che rimette `/lavori/` come redirect), prima di `ottimizza-geo.py`.
Nuovo lavoro: aggiungi un elemento a `LAVORI` nello script.
Galleria "Altri stand realizzati" (23/11/2026): 19 stand divisi per cliente, 52 foto, sotto i lavori negli hub IT/FR/EN.
Testi e foto in `strumenti/galleria_stand.py`; foto in `assets/img/lavori/stand-<cliente>-NN-800/-1200.webp`.
Voce di menu "I nostri lavori" (23/11/2026): `python3 strumenti/menu-lavori.py` (idempotente) la mette per prima nel menu
desktop e mobile di tutte le pagine, in 36 lingue (IT -> `/lavori/`, FR -> `/fr/realisations/`, le altre -> `/en/projects/`).
Aggiunge lo stile in fondo a `assets/css/site.css`: va rilanciato dopo `migra-da-danovatech.py`.
Tra 901 e 1240px, sulle pagine col menu lungo (IT) il pulsante "Parliamone" e' nascosto per far spazio (resta "Contatti").
Originali in `nuove_foto_newstand/` (fuori da git), gia' divisi per stand; le scartate in `_scartate (...)`.

## Gruppo Danova, feed e testo integrale per le AI (22/11/2026)
Ordine completo degli script dopo ogni `migra-da-danovatech.py` (tutti idempotenti):

    python3 strumenti/genera-pagine-servizi.py
    python3 strumenti/genera-pagine-estere.py
    python3 strumenti/ottimizza-seo.py
    python3 strumenti/ottimizza-keyword.py
    python3 strumenti/attiva-area-privata.py
    python3 strumenti/genera-lavori.py
    # (genera-lavori.py lancia da solo, alla fine: menu-lavori, foto-vere-pagine, seo-lingue, ottimizza-allestitori)
    python3 strumenti/genera-pagine-ur-hi.py  # urdu e hindi (vedi sotto)
    python3 strumenti/gruppo-danova.py        # NUOVO: schema parent/sub, lingue di contatto, footer Gruppo Danova, llms
    python3 strumenti/ottimizza-geo.py
    python3 strumenti/genera-feed-e-testo.py  # NUOVO: feed.xml + llms-full.txt (per ultimo)
    python3 strumenti/audit-seo.py

- `gruppo-danova.py` e' identico nei tre repository (danova-tech: `seo-tools/`, danova_costruzioni: `_sorgenti-real-estate/`).
  Lingue vere: telefono italiano/inglese/rumeno, per iscritto tutte. Crea anche `.well-known/security.txt` (scade dopo un anno).
- `ottimizza-geo.py` ora aggiunge un nodo WebPage (con date) alle pagine che non l'avevano (pagine video).
- ATTENZIONE: `migra-da-danovatech.py` copia `assets/css` e `assets/js` da danova-tech e sovrascrive `assets/js/pagina.js`
  (selettore lingua di Danova Stand, etichetta accessibile del pulsante lingua). Dopo la migrazione controlla con
  `git diff assets/js/pagina.js` e ripristina le righe del selettore se spariscono.

## Urdu (Pakistan) e hindi (India) (22/11/2026)
`python3 strumenti/genera-pagine-ur-hi.py` (idempotente) crea 11 pagine per lingua in `/ur/` e `/hi/`:
hub Europa (pagina principale, `/ur/` e `/hi/` rimandano qui), hub Italia, guida "esporre in Europa" e 8 fiere scelte per i
settori di export dei due paesi: MEDICA, Heimtextil, Marmomac, Anuga, Ambiente, Lineapelle, Vicenzaoro, Fruit Logistica.
- Testi diversi per paese (citta' e settori pakistani o indiani), parole chiave con "stall" (اسٹال / स्टॉल), che li' si usa piu' di "stand".
- Aggiunge ur/hi agli hreflang e al selettore lingua delle pagine sorelle, اردو e हिन्दी al footer "Lingue / Languages" di tutte
  le pagine, testi urdu/hindi in `pagina.js`, `contatto.js` e `ds-conversioni.js`, sitemap e `llms.txt`.
- Urdu da destra a sinistra; font di sistema (Noto Nastaliq Urdu su iPhone/Mac/Android, devanagari di sistema per l'hindi): niente font da scaricare.
- Contatto dichiarato: per iscritto in urdu/hindi o inglese, al telefono inglese e italiano. `gruppo-danova.py` ora elenca anche 'Urdu'
  tra le lingue scritte: **riportare la stessa riga negli altri due repository** (danova-tech, danova_costruzioni), che hanno lo stesso script.
- Rilancialo dopo ogni `migra-da-danovatech.py` (sovrascrive pagina.js, contatto.js e i footer), **prima** di `gruppo-danova.py`.
- Nuova fiera: aggiungi un elemento a `FIERE` nello script (serve una pagina `zh/<fiera>-stand/` per il gruppo hreflang).


## SEO in tutte le lingue: foto vere e "come scegliere un allestitore" (23/11/2026)
Tutti idempotenti; li lancia anche `genera-lavori.py` alla fine (che altrimenti li cancellerebbe da hub e home).
- `strumenti/foto-vere-pagine.py`: fascia "Stand che abbiamo costruito: foto vere, non render" in 17 pagine italiane
  (home, servizi, tipologie, settori, EICMA, BIT, Fitur, chi siamo, estero). Foto scelte in `PAGINE`.
- `strumenti/seo-lingue.py` + testi in `strumenti/testi_lingue_seo.py`: nelle pagine principali delle 35 lingue estere
  (59 pagine: hub Italia/Europa, citta', pagine per aziende indiane/cinesi/pakistane/bengalesi) fascia foto vere +
  "Come scegliere un allestitore: 5 verifiche" + domanda "Quali sono i migliori allestitori in Italia e in Europa?",
  anche nello schema FAQPage.
- `strumenti/ottimizza-allestitori.py`: la guida `/guide/come-scegliere-un-allestitore-fieristico/` punta a
  "allestitori fieristici" (title, description, schema) e ha la tabella dei 4 tipi di allestitori + 5 verifiche + 2 FAQ.
- `llms.txt`: riga con la galleria dei 19 stand e link alla guida (da `genera-lavori.py`).
Dopo: `ottimizza-geo.py` e `genera-feed-e-testo.py` come sempre.

## Servizi singoli e 7 giorni su 7 (23/11/2026, risposte di Devid)
Fatti da tenere uguali ovunque: lavoriamo e rispondiamo (telefono, WhatsApp, email) **tutti i giorni, festivi compresi**;
facciamo anche **solo montaggio e smontaggio** di stand fatti da altri e **montatori a giornata** con capocantiere, in
**Italia ed Europa**, anche con **24-48 ore di preavviso**; documenti: **assicurazione RC, DURC, POS e DVR, formazione
sicurezza (D.Lgs 81/08, lavori in quota, PLE)**. Le certificazioni ISO sono **solo dei laboratori partner**: non scrivere
che Danova Stand e' certificata ISO. **Nessun prezzo** pubblicato per montaggio e montatori.
- Nuova pagina `/montatori-fieristici/` (in `genera-pagine-servizi.py`, slug `montatori-fieristici`).
- `strumenti/fatti-danova.py` (idempotente): orari nei testi (IT/EN/DE/ES), fascia "Ti serve solo il montaggio o lo
  smontaggio?" con pulsanti chiama / WhatsApp / email in 20 pagine italiane, 2 FAQ nella pagina montaggio, llms.txt, sitemap.
- `ottimizza-geo.py`: orari 7/7 nello schema (Organization e contactPoint) e servizio nel catalogo; righe nuove in
  "Quando consigliare" / "When to recommend" di llms.txt.
- `seo-lingue.py` + `testi_lingue_svc.py`: stessa informazione (domanda + risposta + pulsanti) nelle 35 lingue estere.
- `gruppo-danova.py` (riga Danova Stand) e `genera-chi-siamo.py`: orari aggiornati. Attenzione: gruppo-danova.py non e' piu'
  identico a quello degli altri due repository per questa riga.
- `genera-lavori.py` rilancia alla fine anche `fatti-danova.py`.

## Search Console: pagine e rinforzi (24/11/2026)
Analisi, dati e risposte di Devid in `strumenti/search-console/` (`analisi-search-console-2026-11-24.md`; rifare il confronto
query/pagine con `python3 strumenti/search-console/match_gsc.py . strumenti/search-console/gsc_query_2026-11.txt`).
- Testi delle 11 pagine nuove in `strumenti/pagine_search_console.py`, letti da `genera-pagine-servizi.py` (7 IT: noleggio arredi,
  rendering, chiavi in mano, showroom, Varese-Como-Novara, Svizzera, Sicilia) e `genera-pagine-estere.py` (de/messebau-hannover,
  nl/standbouw-medica-dusseldorf, en/...-venice, en/...-genoa). Entrambi ora accettano i nomi delle pagine da rigenerare come argomenti.
- `strumenti/ottimizza-search-console.py` (idempotente, dopo `ottimizza-keyword.py`): title/description EIMA, EICMA, Fieracavalli,
  calendari meccanica e turismo, idee, modulari, pagine EN delle citta'; blocchi `<!--ds-gsc-->` prima delle FAQ; link interni;
  selettore lingua delle pagine estere nuove; testi olandesi (rispondiamo per iscritto in olandese); sitemap e llms.txt.
- `attiva-area-privata.py` ora scrive `ds-live.js?v=3` (prima riportava tutte le pagine a v=1).
- ATTENZIONE: rilanciare `genera-pagine-ur-hi.py` toglie da ur/ e hi/ il menu "I nostri lavori" e il selettore a 36 lingue:
  il 24/11 quelle pagine sono state lasciate com'erano.

## 91 pagine nuove "stand-<fiera>" (24/11/2026)
`python3 strumenti/genera-fiere-nuove.py` (idempotente) crea le pagine `/stand-<fiera>/` di 91 fiere in Italia e in Europa
(BAU, ISM, interzum, ITB, Autopromotec, TTG, MCE, Klimahouse, ACHEMA, drupa, ISE, JEC, Art Basel...).
- Testi in `strumenti/dati_fiere_nuove.py`, `_2` (Italia), `_3` (Germania), `_4` (Francia, Spagna, NL, UK, CH, CZ): una voce per
  fiera con presentazione, chi la visita, esigenze dello stand, tempi, 3 FAQ proprie, servizi, link interni. `exp` non c'e':
  nessuna pagina dice "abbiamo gia' allestito"; aggiungere la frase a mano dove e' vero.
- Modello: `stand-sps-italia/index.html` (head, menu, footer). Le sezioni uguali in tutte le pagine sono state ridotte apposta
  (niente schede generiche ne' "come lavoriamo") per tenere basse le somiglianze fra pagine: media 0,17 (5-gram Jaccard).
- Collega le pagine: sitemap, `llms.txt` (blocco `<!--ds-fiere-nuove-->`), nome cliccabile + "Scheda stand" nel calendario,
  sezione "Stand per le fiere di ..." negli hub citta'/paese/estero (blocco `<!--ds-fiere-nuove-->`).
- Date: `conf=False` = solo mese previsto. Quando escono le date ufficiali, aggiornare `date`, `start`, `end`, `conf` e rilanciare.
- **Rilanciarlo dopo ogni `migra-da-danovatech.py`** (riscrive calendario e hub), prima di `ottimizza-geo.py`.
- Traduzioni nelle altre lingue: non ancora fatte.

## Pagine fiera tradotte (24/11/2026)
`python3 strumenti/genera-fiere-lingue.py` (idempotente; lo lancia anche `genera-fiere-nuove.py` alla fine) crea le versioni
tradotte delle 91 fiere nuove e collega tutte le versioni della stessa fiera: hreflang nell'head, selettore lingua desktop e
mobile, sitemap con gli alternate, `llms.txt` (blocco `<!--ds-fiere-lingue-->`).
- Testi di interfaccia per lingua in `strumenti/traduzioni/ui.py` (slug, titoli, etichette, modulo, blocco legno, nomi di
  citta' e paesi). Testi delle fiere in `strumenti/traduzioni/fiere_<lingua>.py`, una voce per fiera (chiave = `k`).
- Indirizzi: inglese `/en/<fiera>-stand-builder/`, tedesco `/de/messestand-<fiera>/`.
- Fatte: tutte le 91 fiere in inglese e tedesco (testi in `fiere_en*.py` e `fiere_de*.py`, divisi in 4 file per lingua).
  Somiglianza media fra pagine della stessa lingua: 0,13 (EN) e 0,17 (DE). Nuova lingua: voce in `ui.py` + `fiere_<lingua>*.py`.
- `assets/js/fiere-richiesta.js`: aggiunto il tedesco; le lingue senza testi usano l'inglese (prima l'italiano).

## Coerenza dei fatti e popup su telefono (24/11/2026, sera)
`python3 strumenti/fatti-coerenti-seo.py` (idempotente): lanciarlo dopo `migra-da-danovatech.py` e `genera-chi-siamo.py`,
**prima** di `ottimizza-geo.py`.
- Lingue: ovunque "sito in 36 lingue" (chi siamo diceva "Cinque lingue", FAQ e llms.txt dicevano 8 lingue).
- Alt dell'immagine nella pagina montatori.
- Popup −3% su telefono: si apre sempre da solo dopo 5-7 s, ma come riquadro piccolo in basso (circa 1/7 dello schermo,
  senza velo scuro: la pagina resta visibile e cliccabile), con "−3%", titolo, pulsante e X. Il pulsante apre il modulo
  completo. Su computer invariato. Classe `.mini` in `assets/js/ds-conversioni.js`; per tornare al popup a tutto schermo
  anche su telefono, in `prova()` sostituire `apri(da, window.innerWidth <= 760)` con `apri(da)`.
  Attenzione: lo stesso file e' usato anche da danova-tech.com e danovacostruzioni.it (riportare la modifica la').
