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
    python3 strumenti/audit-seo.py

`ottimizza-keyword.py` fa anche:
- `/contributi-fiere-2026/` -> `/contributi-fiere/` (la vecchia pagina rimanda alla nuova);
- le 7 pagine `/stand-XX-mq/` -> sezioni di `/stand-fieristici-per-metratura/` (contenuto salvato in
  `strumenti/metrature-blocchi.html`, i vecchi indirizzi rimandano all'ancora);
- fiere concluse portate alla prossima edizione (tabella `EDIZIONI`: aggiornarla quando escono le date).
