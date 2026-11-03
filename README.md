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
