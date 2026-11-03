# Pagine fiere aggiunte l'8 ottobre 2026

53 pagine nuove + collegamenti sulle esistenti. Tutto si rigenera con gli script qui sotto
(dalla cartella seo-tools/fiere-generatore), nell'ordine:

    python3 build_calendario.py     # /calendario-fiere/  (mappa + elenco + richiesta stand)
    python3 build_fiere.py          # /stand-<fiera>/     (20 pagine)
    python3 build_citta_nuove.py    # 15 nuove citta'
    python3 build_tipi.py           # 9 tipologie di stand
    python3 build_settori.py        # 6 settori
    python3 it_pages.py; python3 it_pillar.py; python3 it_citta.py   # pagine esistenti (ora collegate)
    python3 patch_link_nuove.py     # footer, home, llms.txt (idempotente)
    cd .. && python3 genera-sitemap.py && python3 genera-feed-e-llms.py

## Aggiornare le date delle fiere
Tutte le date stanno in `dati_calendario.py` (lista F). Per ogni fiera: inizio, fine, conf (1 = date
ufficiali, 0 = solo mese "da confermare"). Le fiere concluse spariscono da sole dal calendario
(anche lato browser), ma conviene aggiungere le nuove edizioni ogni 2-3 mesi e rilanciare gli script.
Il titolo delle pagine /stand-<fiera>/ contiene l'anno della prossima edizione: si aggiorna da solo
quando cambi le date.

## Esperienza dichiarata
Solo le 10 fiere con exp=True in `dati_pagine_fiere.py` dicono "abbiamo gia' allestito stand".
Se allestite stand in altre fiere, mettete exp=True anche li'.

## File di supporto
- assets/js/fiere-richiesta.js  modulo "Richiedi lo stand" -> WhatsApp (o email)
- assets/js/calendario-fiere.js filtri + mappa (Leaflet 1.9.4 da cdnjs, mappa CARTO dark, caricata solo quando visibile)
- assets/css/fiere.css          stili aggiunti in fondo
- lib.py: build() ha due parametri in piu' (wp_extra, scripts). Backup: *.bak-2026-10-08

## 9 ottobre 2026
Dopo aver rilanciato questi script, rilanciare anche
    python3 seo-tools/link-pagine-2026-10.py
che rimette nei box "Pagine collegate" i link a /contributi-fiere-2026/ (e alle altre pagine
del 9/10). Titoli e description delle pagine citta' ora sono sotto i limiti di Google
(it_citta.py: il marchio "| Danova Tech" si toglie da solo se il titolo e' troppo lungo).
Calendari per citta' (/calendario-fiere-bologna|milano|rimini|parma/): python3 build_calendari_citta.py
(prendono le date da dati_calendario.py: rilanciarlo dopo ogni aggiornamento delle date).

## 13 ottobre 2026: render degli stand, galleria, espositori, hub regionali
60 render 3D generati con IA (Higgsfield, GPT Image 2.5) in `assets/img/stand/`:
`<nome>.webp` 1600px, `<nome>-800.webp` per mobile, `og/<nome>.jpg` 1200x630 per i social.
Sono presentati sempre come "Render di progetto" (didascalia sotto l'immagine): non spacciarli per stand realizzati.

- `dati_render.py`  elenco render: file, pagina, prompt usato, alt e didascalia; RIUSO = pagine che usano un render esistente
- `immagini.py`     inserisce il render sotto l'hero + og:image + ImageObject nel JSON-LD (chiamato da lib.build)
- `citta_extra.py`  blocco "Da Mansuè a <città>: logistica e tempi" nelle 23 pagine città (chiamato da lib.build)
- `applica_immagini.py`  applica entrambi alle pagine già pubblicate (idempotente)
- `build_nuove_1013.py`  /progetti-stand-fieristici/ (galleria), /espositori-desk-totem-per-fiere/,
  /allestimenti-fieristici-veneto|lombardia|emilia-romagna/
- `../link-pagine-2026-10-13.py`  link interni (Approfondisci, footer, home, llms.txt) + titoli città/idee/noleggio

Dopo i build del 8-9 ottobre, in quest'ordine:
    python3 build_nuove_1013.py
    python3 applica_immagini.py          # serve per idee-stand-fieristici e contributi (generati da altri script)
    cd .. && python3 link-pagine-2026-10-13.py && python3 genera-sitemap.py && python3 genera-feed-e-llms.py

Nuovo render per una pagina: aggiungi la riga in dati_render.R (o in RIUSO), metti i 3 file in assets/img/stand/
e rilancia applica_immagini.py. Quando avrete FOTO VERE di stand allestiti, sostituitele ai render nelle pagine
fiera/città e cambiate la didascalia: per Google e per i clienti valgono molto di più.

## 14 ottobre 2026: espositori stranieri (soprattutto cinesi), pagine EN e ZH
34 pagine nuove: 12 fiere (EICMA, Cosmoprof, MICAM, MIDO, Host, Salone del Mobile, Cersaie, Marmomac, EIMA,
VicenzaOro, Ecomondo, Macfrut) + 4 città (Milano, Bologna, Verona, Rimini) + 1 guida, in inglese e in cinese.
- `dati_intl.py`   testi EN/ZH, render e didascalie tradotte
- `intl_map.py`    mappa hreflang IT <-> EN <-> ZH; lib.build la usa da sola, quindi rigenerando le pagine IT gli hreflang restano
- `build_intl.py`  genera le 34 pagine e aggiorna hreflang + selettore lingua (IT/EN/中文) sulle 17 pagine IT corrispondenti
- `lingue.py en zh` rigenera solo i pillar inglese e cinese (ora con la sezione di link alle pagine fiera/città)
Ordine:  python3 build_intl.py && python3 lingue.py en zh && cd .. && python3 genera-sitemap.py && python3 genera-feed-e-llms.py
Le date vengono da dati_calendario.py come per le pagine IT: aggiornate le date lì e rilanciate build_intl.py.

## 14 ottobre 2026 (secondo giro)
- Esperienza vera estesa a 17 fiere (aggiunte Sigep, VicenzaOro, Ecomondo, MICAM, MIDO, Macfrut, Lineapelle).
- Cinese: "rispondiamo in cinese con l'aiuto di strumenti di traduzione" (non promettere madrelingua).
- 7 fiere IT nuove (dati_pagine_fiere_2.py): Lineapelle, KEY, EMO Milano, Zoomark, Lamiera, MECSPE, TUTTOFOOD.
- EN/ZH: 25 fiere + 8 città (dati_intl.py + dati_intl_2.py).
- Pagine per metratura e 7 guide IT: build_metrature_guide.py + link_metrature_guide.py (dati_metrature_guide.py).
- Cinese tradizionale /zh-hant/: build_hant.py converte tutte le pagine /zh/ (OpenCC s2t). Rilanciarlo ogni volta che cambiano le pagine cinesi.
Ordine completo:
    python3 build_fiere.py && python3 build_calendario.py && python3 build_citta_nuove.py && python3 build_settori.py && python3 it_pillar.py && python3 it_citta.py
    cd .. && python3 link-pagine-2026-10.py && cd fiere-generatore && python3 build_calendari_citta.py && python3 build_nuove_1013.py && python3 applica_immagini.py
    python3 build_metrature_guide.py && python3 build_intl.py && python3 lingue.py
    cd .. && python3 link-pagine-2026-10-13.py && cd fiere-generatore && python3 link_metrature_guide.py && python3 build_hant.py
    cd .. && python3 genera-sitemap.py && python3 genera-feed-e-llms.py

## 14 ottobre 2026 (terzo giro)
- legno.py: blocco "Gli elementi in legno li facciamo noi, dalla A alla Z" (IT/EN/ZH/DE/FR/ES) in tutte le pagine allestimenti.
  È agganciato a lib.build; per le pagine già pubblicate: python3 legno.py, poi python3 build_hant.py.
- Software: python3 seo-tools/pagine-build-2.py pagine-dati-8.py && python3 seo-tools/sumisura.py && python3 seo-tools/link-pagine-2026-10-14.py
  sumisura.py inserisce "Un gestionale solo vostro, non un programma uguale per tutti" nelle pagine software IT (rilanciarlo dopo ogni pagine-build).
