# Analisi CSV Keyword Planner — 14 novembre 2026

Fonte: 79 CSV leggibili in `~/Downloads/parole_danova_all` (1 file, `V-EN-3 · Fiere italiane.csv`, e' una
previsione e non contiene volumi). Periodo: novembre 2025 - ottobre 2026. 7.240 righe, 3.809 parole uniche
per mercato. Dati uniti in `strumenti/keyword-planner-2026-11.csv`.

**Italia**: numeri esatti mese per mese. **Estero**: solo fasce (50 = 10-100, 500 = 100-1.000,
5.000 = 1.000-10.000, 50.000 = 10.000-100.000).
Google raggruppa le varianti quasi uguali ("stand fiera" e "stand in fiera" hanno lo stesso numero):
non vanno sommate.

## Italia — le parole che contano (ricerche medie al mese)

| Gruppo | Parole e volumi | Pagina |
|---|---|---|
| Servizio principale | stand fiera / stand in fiera 1.000 · allestimenti fieristici / allestitori fieristici 590 · stand fieristici 480 · allestimenti fiere 390 · allestimento stand fiera 260 · stand espositivo 260 · stand per fiere 210 · allestimento stand 170 · progettazione stand fieristici 110 · exhibit design 480 | Home, /servizi/allestimenti-fieristici/, /progettazione-stand-fieristici/ |
| Fiera + anno (pubblico e espositori) | eicma 2026 40.500 · salone del mobile 2026 40.500 · cosmoprof 2026 22.200 · cersaie 2026 8.100 · gia' a ottobre: vinitaly 2027 2.900 · sigep 2027 2.900 · salone del mobile 2027 2.400 · cosmoprof 2027 1.900 · eicma 2027 720 · cibus 2027 590 · mecspe 2027 480 · mido 2027 390 · pitti uomo 2027 320 | Pagine /stand-[fiera]/ |
| Stand + fiera | stand vinitaly 140 · stand salone del mobile 90 · stand eicma 70 · stand cosmoprof 70 · stand cersaie 40 · stand ecomondo 30 · stand tuttofood 30 · stand sigep 20 · tutte le altre 0-10 | Pagine /stand-[fiera]/ |
| Calendari | fiere bologna 2026 1.600 · fiere verona 2026 720 · calendario fiere 2026 590 · fiere milano 2026 480 (picco gen-feb) | /calendario-fiere-*/ |
| Totem ed espositori | totem pubblicitari 1.300 · totem pubblicitari da esterno 590 · totem da esterno 390 · roll up pubblicitari 390 · totem pubblicitario 320 · cavalletto pubblicitario 320 · espositori per fiere 260 · espositori pubblicitari 170 · totem fiera 50 | /totem-pubblicitari/, /espositori-pubblicitari/, /espositori-desk-totem-per-fiere/ |
| Negozi e vetrine | idee vetrine negozi 480 · allestimento negozi 320 · allestimento vetrine 260 · allestimento vetrine natalizie 260 · allestimento negozio abbigliamento 210 · allestimento vetrine negozi 170 | /allestimento-negozi/ |
| Eventi e mostre | allestimenti eventi 390 · allestimento mostre 110 · allestimenti mostre fotografiche 140 · allestimento museale 70 · allestimento eventi aziendali 50 | /allestimenti-eventi/, /allestimento-mostre/ |
| Componenti | moquette fiera 110 · desk fiera 110 · gadget per fiere 260 (non e' un servizio Danova) | pagine servizio |
| Contributi | simest fiere 210 · fondo simest 140 · bando fiere 2026 140 · fondo 394/81 90 · voucher internazionalizzazione 50 | /contributi-fiere-2026/ |
| Citta' | allestimenti fieristici milano 90 · allestitori milano 90 · bologna 50 · verona 40 · rimini 40 · veneto 40 · roma, torino, padova, bergamo, brescia 20 · tutte le altre 0-10 | /allestimenti-fieristici-[citta]/ |
| Prezzi | stand per fiere prezzi 20 · prezzo stand fiera 20 · quanto costa uno stand 10 | /quanto-costa-uno-stand-fieristico/ |
| Noleggio / tipologie | stand personalizzati 90 · stand in legno 70 · stand modulari per fiere 50 · noleggio stand 30 · stand preallestiti 30 · stand modulari 20 · montaggio stand fieristici 20 | pagine tipologia |
| Metrature | stand 9/12/16/.../100 mq: **nessun dato** (0 ricerche) | /stand-XX-mq/ |

Stagionalita' del servizio principale (somma delle varianti, indice): massimo marzo (15.650), alto
gen-mag, crollo luglio-agosto (5.520, -65%), ripresa settembre. I contenuti nuovi vanno pubblicati
entro gennaio.

Nomi di concorrenti cercati: Power Expo Allestimenti (140, +191% sull'anno), Centro Stand, Stipa
Allestimenti, Mood Allestimenti, Colorcom, Allestimenti Disca, Promo Allestimenti.

Da non inseguire (intenzione diversa): stand virtuali 390, stand appendiabiti, totem/stand in cartone,
stand per fiere all'aperto, fai da te.

## Estero (fasce)

- Tedesco: "messebau mailand" 1.000-10.000 (la pagina /de/messebau-mailand/ esiste: e' la parola estera
  piu' preziosa). "messebau", "messestand" 1.000-10.000 ma generici e locali. "messen in italien",
  "messe mailand 2027", "messe bologna 2027" 10-100. Fiere + 2027 (vinitaly, salone, eicma, cosmoprof) 100-1.000.
- Nomi originali delle fiere (cercati in tutti i mercati esteri): cosmoprof bologna e vinitaly
  10.000-100.000; cersaie, cibus, ecomondo, eicma, eima, expo riva schuh, host, mecspe, micam, mido,
  salone del mobile, sigep, tuttofood, vicenzaoro 1.000-10.000.
- Inglese: "cosmoprof bologna italy" e "vicenzaoro italy" 100-1.000; "stand builder italy",
  "exhibition stand design italy", "trade fairs italy" 10-100.
- Francese e spagnolo: ricerche sull'Italia 10-100; "stand parapluie" 1.000-10.000 (prodotto economico).
- Cinese tradizionale: "米蘭家具展" (Salone del Mobile) 100-1.000. Turco: "italya fuarları" 100-1.000.
  Arabo: quasi nulla (si cerca in inglese).

## Modifiche gia' fatte (strumenti/ottimizza-keyword.py)

- Home: title "Stand fiera e allestimenti fieristici | Danova Stand".
- EICMA portata al 2027 in title e description.
- 15 calendari: 2027 in primo piano in title, description, og/twitter e H1.
- "Espositori per fiere: desk, banchi e totem" (espositori per fiere 260 > desk fiera 110).
- "Stand pubblicitari, espositivi e promozionali" (stand espositivo 260).
- 325 pagine: priorita' di caricamento tolta al logo e data alla prima foto del contenuto; foto
  successive caricate in differita (Core Web Vitals / LCP).

## Decisioni del 14/11/2026 (risposte di Devid)

- Totem ed espositori: solo insieme allo stand (niente pagine prodotto da esterno/LED).
- Vetrine: si', tutte (natalizie e stagionali, fisse su misura, per marchi/eventi, grafiche e vetrofanie) -> pagina dedicata.
- Pagine fiera: aggiungere info espositori 2027 (date, padiglioni, scadenze, regolamento) su TUTTE le fiere con pagina.
- Foto reali: non ci sono, solo render -> etichettare i render come tali; case study da pianificare.
- Metrature: unire in /stand-fieristici-per-metratura/, le singole rimandano li'.
- Citta' piccole (Longarone, Carrara, Bolzano, Udine, Pordenone, Bari): non ci lavoriamo -> unire nella regione.
- Contributi: indirizzo senza anno /contributi-fiere/, la pagina 2026 rimanda li'.
- Git: commit si', push lo fa Devid.
- Tedesco: risposte solo per email con traduttore -> pagine DE con modulo in primo piano.
- Gadget: nessuna guida.
- Concorrenti: Power Expo, Centro Stand, Stipa, Mood Allestimenti, Colorcom.
- Google Business Profile e Search Console: entrambi attivi.
- Prezzi: niente prezzi al mq; restano 10.000-30.000 EUR per stand completo + preventivo in 24 ore.
- Team: niente nomi/foto delle persone.
- Numeri "oltre 300 stand", "11 paesi", "20 anni": corretti.

## Search Console (3-10 novembre 2026, primi 8 giorni del dominio)

- 41 clic, 2.912 impressioni, posizione media 16 in Italia. Mobile: posizione 9,2; desktop 35,9.
- Pagine che portano clic: /stand-fieracavalli/ 21 clic (pos 5,7), /stand-eicma/ 5 (pos 6,4), /stand-eima/ 2,
  /stand-vicenzaoro/ 2, /stand-ecomondo/ 1. Le pagine fiera sono gia' in prima pagina quando la fiera e' vicina.
- Paesi: Italia 2.429 impressioni; Paesi Bassi 133 (query "standbouw euroshop / medica dusseldorf /
  messe dusseldorf / interpack / anuga / sial"), Estonia 112, Germania 72, USA 45, Svizzera 21 (Lugano).
- Query senza pagina adatta: "noleggio arredi stand" (26 impr., pos 44), "arredi stand fieristici rho",
  "stand componibili", "stand fieristici soppalcati", "stand fieristici in cartone" (non offerto).
- Rumore di marca: "danova gmbh" (pos 6,5), "vermezzo con zelo milano incendio" (sede operativa citata
  dalla panoramica IA di Google).

## Google Business Profile (controllo del 14/11/2026)

- Esistono DUE schede: "DANOVA STAND | ALLESTIMENTI" (kgmid /g/11_00md98z, Via Rigole, 31040 Rigole TV)
  e "DANOVA STAND | ALLESTIMENTI FIERISTICI" (kgmid /g/11_0363r8f). Stesso telefono, stessa categoria.
- Categoria "Organizzatore di mostre", orari "Aperto 24 ore su 24", nessuna recensione.
- Nome con "| ALLESTIMENTI (FIERISTICI)": le linee guida Google vogliono il nome reale dell'attivita'.
- La panoramica IA di Google mescola Danova Tech e Danova Stand e cita l'email info@danova-tech.com.
- Decisioni: la seconda scheda e' un'altra sede vera (da chiarire quale e con che indirizzo);
  Olanda si', pagine in olandese ("standbouw + beurs"); noleggio arredi no; scheda Google: orari e
  categoria restano come sono.
