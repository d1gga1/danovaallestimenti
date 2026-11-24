# Analisi Search Console — 24 novembre 2026

Fonte: export "Performance on Search" di danovastand.com (ultimi 12 mesi, ma i dati partono dal 3/11/2026:
il sito e' nuovo). Totale: 96 clic, 7.704 impressioni, CTR 1,2%. 92 clic su 96 dall'Italia.
Mobile posizione media 10, computer 36. Il file query contiene 822 query (3.647 impressioni: il resto
Google lo nasconde perche' sono query rare).

Metodo: `match_gsc.py` confronta ogni query con title, H1, description e indirizzo (TITOLO), con H2/H3
(SEZIONE) e con il testo (TESTO) delle 405 pagine pubblicate. Risultato in `risultato.json`.

| Copertura | Query | Impressioni |
|---|---|---|
| Nel title/H1 di una pagina | 386 | 1.928 |
| Solo in un H2/H3 | 31 | 202 |
| Solo sparsa nel testo | 255 | 1.005 |
| Assente dal sito | 150 | 511 |

Pagina che porta clic: /stand-fieracavalli/ (23 clic su 96, posizione 6,7). EIMA ed EICMA hanno 600
impressioni a posizione 6-7 ma CTR sotto l'1%: lavorare su title/description.

## Gruppi di query senza una pagina dedicata (impressioni, posizione media)

| Gruppo | Impr. | Pos. | Esempi | Proposta |
|---|---|---|---|---|
| Noleggio arredi stand (Rho/Milano) | 314 | 51 | noleggio arredi stand 66, arredi stand fieristici rho 45, area lounge stand rho fiera 19, noleggio desk stand rho fiera 12, noleggio mobili per stand | NUOVA pagina /noleggio-arredi-stand-fieristici/ |
| MEDICA / Düsseldorf / Colonia in olandese e inglese | 259 | 53 | medica düsseldorf stand builder 35, standbouw medica 24, standbouw euroshop 25, standbouw messe düsseldorf 16, standbouw interpack, anuga, sial, keulen | NUOVE pagine NL per MEDICA ed EuroShop/Düsseldorf; rinforzo /en/medica-stand-builder/ col lavoro del padiglione Tunisia |
| Bologna in inglese | 231 | 69 | custom stand bologna 25, stand builders bologna 24, exhibition stand design bologna 22, booth | Rinforzo /en/exhibition-stand-builder-bologna/: "booth", "contractor", "design and build", "custom" |
| Altre citta' in inglese | 165 | 60 | Milano, Parma, Rimini, Firenze, Venezia, Genova + contractor/booth | Stesse parole nelle pagine EN citta'; nuova /en/exhibition-stand-builder-venice/ e -genoa/ |
| Varese, Novara, Como, Ticino | 130 | 52 | stampa stand fieristici luino 14, tradate, malnate, varese, gallarate, busto arsizio, novara, como, arona; totem personalizzati luino | NUOVA pagina /allestimenti-fieristici-varese/ (Varese, Como, Novara, Alto Milanese) |
| Rendering stand | 108 | 56 | rendering per stand fiera 25, rendering per stand fiera milano 24, rendering stand 16 | La parola "rendering" non e' in nessuna pagina: NUOVA /rendering-stand-fieristici/ o rinforzo /progettazione-stand-fieristici/ |
| Idee / esempi stand | 106 | 42 | idee per stand fiera 44, idee stand fiera 10, esempi stand fieristici | /idee-stand-fieristici/ ha title "Stand fieristici innovativi": rimettere "idee" in testa |
| Fiere meccanica / metalmeccanica | 92 | 21 | fiera meccanica 2026 14, fiera metalmeccanica 14, fiere meccanica 2026 12 | "metalmeccanica" non c'e' nel sito: aggiungerla al calendario meccanica |
| Noleggio / affitto stand | 90 | 41 | noleggio stand 13, affitto stand 14, stand noleggio 12 | /noleggio-stand-fieristici/ esiste: piu' "affitto", "noleggio stand fiera" negli H2 |
| Hannover | 79 | 49 | messestand hannover 15 (pos 10), messebau hannover messe 8 (pos 6), hannover messe stand 17 | NUOVA /de/messebau-hannover/ |
| Stand modulari / componibili | 73 | 53 | stand modulari per fiere 28, stand componibili 15 | Rinforzo /stand-modulari/ con "componibili" e "per fiere" |
| Chiavi in mano | 63 | 67 | progetto stand chiavi in mano 20, stand chiavi in mano 15 | Nessuna pagina IT ha "chiavi in mano" nel title generale: NUOVA /stand-chiavi-in-mano/ |
| Congressi / convention / corporate | 59 | 52 | allestimento convention 10, allestimento congressi 10, portanomi | Rinforzo /allestimenti-eventi/ (sezioni congressi, convention, eventi corporate) |
| Showroom | 56 | 45 | stand showroom 21, allestimento showroom 16 | NUOVA /allestimento-showroom/ |
| Turismo / fiere alberghiere | 53 | 47 | fiere alberghiere 19, fiera turismo italia | "alberghiere" nel calendario turismo (Host, TTG, BIT) |
| Noleggio ledwall in fiera | 48 | 44 | Berlino, Stoccarda, Hannover, Düsseldorf, Lione, Parma | Rinforzo /ledwall-e-illuminazione-stand/ con le citta' estere |
| Lugano / Ticino | 47 | 59 | trade fair stand constructor lugano 16, contractors lugano | Dentro la pagina Varese o pagina EN/IT Svizzera |
| Palermo / Sicilia / Sardegna | 44 | 59 | exhibition stand builder palermo 8, allestimenti fieristici palermo | NUOVA /allestimenti-fieristici-palermo/ (se lavorate in Sicilia) |
| Parole singole mancanti | — | — | soppalcati, ecologici, enogastronomici, T-Gold, fieravicola, Chianti/Toscana | Sinonimi nelle pagine esistenti |

Da non inseguire: stand in cartone (16, deciso il 14/11), arredo urbano, query del pubblico tipo
"fiera oggi a milano", "eicma stand dainese".

## Risposte di Devid (24/11/2026) — fatti da rispettare nei testi

- Arredi (lounge e divanetti, desk e banconi, tavoli e sedie riunioni, frigo, macchina caffe', TV):
  **solo insieme a uno stand Danova**, non noleggio a terzi.
- Rendering 3D: **gratis col preventivo** (non si vende da solo), primo render in **24-48 ore**.
- Sicilia (Palermo, Catania): **solo progetti grandi, da 30 mq in su**; niente pagina "locale" troppo promettente.
- Svizzera (Lugano/Ticino, Zurigo, Basilea, Ginevra): **gia' lavorato** (senza nomi). Dogana
  (carnet ATA / spedizioniere partner) **la gestiamo noi**.
- Varese, Como, Novara: stand per fiere ovunque per aziende di quelle zone; **gia' allestito a
  Malpensafiere e Lariofiere**. Niente stampa o totem venduti da soli.
- Germania: **squadra Danova + partner locali**. Lavori citabili senza nomi: altri stand a MEDICA,
  stand ad Anuga/Colonia, stand a Hannover, solo montaggio per terzi.
- Showroom: permanenti su misura, temporanei/pop-up, corner nei negozi.
- Congressi: forniamo **stand sponsor / area expo** (non palchi, non service audio-luci).
- Ledwall: **nostri**, noleggio in **Italia ed estero**.
- Chiavi in mano include: progetto, render e grafica; trasporto, montaggio, smontaggio; impianto
  elettrico e certificati; arredi, ledwall, moquette. **Gestiamo tutte le pratiche con l'ente fiera.**
  Anticipo minimo stand su misura: **2-3 settimane**.
- Materiali: strutture riutilizzabili, tessuti in poliestere riciclabile, legno certificato FSC/PEFC,
  cartone / pannelli riciclati.
- Stand a due piani / soppalcati: **li facciamo** (calcoli strutturali e collaudo).
- Olandese: rispondiamo **per iscritto in olandese**, telefono in inglese/italiano.
- Danova GmbH: **non esiste**, non scriverla.
- VicenzaOro / T-Gold: stand gia' fatti, ma senza foto professionali (citarli a parole).
- Prezzi: **nessun prezzo** nelle pagine nuove.
- OK a cambiare title/description di EIMA, EICMA e Fieracavalli.
- Immagini: foto vere della galleria + render.
