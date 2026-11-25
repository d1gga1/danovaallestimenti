# Danova Stand – stato al 24/11/2026 (sera tardi)

Regole fisse
- Commit SENZA il nome di Claude. L'utente fa git da solo; dare il comando:
  cd ~/danova_allestimenti && git add -A -- . ':!Claude outputs' && git commit -m "..." && git push
- Rispondere all'utente in italiano.
- Dopo ogni modifica: python3 strumenti/<generatore>.py, poi ottimizza-geo.py, genera-feed-e-testo.py,
  audit-seo.py > /tmp/audit_N.txt e confronto con l'ultimo /tmp/audit*.txt. Limiti: title <= 65,
  description 70-165 (misurata sulla stringa grezza con &/apostrofi escapati).

## FATTO
1. Pagine fiera (91 fiere) in IT, EN, FR, ES, DE (strumenti/traduzioni/fiere_<lingua>*.py, generatore genera-fiere-lingue.py).
   - ES: es_fix_a..o.py + assemble_dev.py (questa cartella). Rigenerare: python3 "Claude outputs/prossima-sessione/assemble_dev.py" es
   - DE: riscritte 72 fiere (de_fix_a..i.py, applicate con merge_dev.py de). Rapporto parole DE/IT 1.00, nessuna sotto 0.8.
   - FR: completo, similarita' media 0.17.
2. Pagine LAVORI in tutte le 35 lingue del sito: hub + 2 lavori (palco galleggiante Arsenale Venezia, padiglione Tunisia MEDICA).
   - it/fr/en dentro genera-lavori.py; de/es in strumenti/lavori_lingue.py; tutte le altre in strumenti/lavori_lingua_<lingua>.py
     (modello: lavori_lingua_pl.py o lavori_lingua_zh.py), caricati da soli da genera-lavori.py e galleria_stand.py.
   - Hub in HUB di menu-lavori.py e seo-lingue.py (chiavi anche 'zh-Hans' e 'zh-Hant').
   - zh-hant e' generato da lavori_lingua_zh.py con "Claude outputs/prossima-sessione/zh_to_hant.py" (rilanciarlo se cambia zh).
   - Lingua 'id' (indonesiano) sovrascriveva la chiave 'id' del lavoro: genera-lavori.py ora usa L['_slug'].
   - Nuovo lavoro = aggiungere X['<id-lavoro>'] in OGNI lavori_lingua_*.py (+ lavori_lingue.py per de/es + genera-lavori.py per it/fr/en).
   - Audit dopo la generazione: nessun title/desc fuori limite sulle pagine lavori; le 25 nuove pagine hub senza FAQ sono normali
     (anche gli hub gia' esistenti non hanno FAQ).


## SESSIONE 24/11 (completata)
- A FATTO: testo italiano arricchito per le 56 fiere estere (dati_fiere_nuove_3/_4), poi EN/FR/ES/DE aggiornate (rapporto parole >= 0.8 su tutte).
- B FATTO: 91 pagine fiera in portoghese (pt/stand-*), olandese (nl/standbouw-*), polacco (pl/stoisko-*). File: traduzioni/fiere_pt*.py, fiere_nl*.py, fiere_pl*.py; voci pt/nl/pl in traduzioni/ui.py. Audit: 1298 pagine, nessun problema nuovo.
- C: controllo testuale locale delle pagine Lavori ja/ko/th/vi/ta/zh-hant OK (titoli, h1, 0 parole italiane). Hreflang/menu lingue OK su tutte le pagine tradotte. Il controllo visivo nel browser va fatto su danovastand.com DOPO il push (il browser non apre file locali).

## CONTROLLO COMPLETO 24/11 (sera)
- Corretti: moduli contatto (assets/js/contatto.js: domanda "Quando vorresti partire?", errori e conferme in 26 lingue in piu');
  modulo fiere (assets/js/fiere-richiesta.js: pt, nl, pl); modulo in fondo pagina ar/ e tr/ (strumenti/fix-modulo-ar-tr.py);
  menu e footer delle 97 pagine nl/ erano in inglese (strumenti/fix-chrome-nl.py); 4 link a pagine-redirect nelle pagine lavori DE/ES;
  descrizione troppo lunga di Hospitality Riva in 5 lingue (genera-fiere-nuove.py / genera-fiere-lingue.py).
- IMPORTANTE: dopo aver rigenerato pagine nl/, ar/ o tr/ rilanciare fix-chrome-nl.py e fix-modulo-ar-tr.py.
- Restano (scelte vecchie, non errori): ~20 description lunghe 166-219 caratteri create da ottimizza-search-console /
  pagine_search_console (Google le taglia, non penalizza); riga "a brand of Danova Tech / Danova Group" in inglese nel footer di tutte le lingue.

## CANNIBALIZZAZIONE 24/11 (sera)
- Nessun titolo/H1 doppio nella stessa lingua; nessun gruppo hreflang con due pagine della stessa lingua.
- Hub citta' (allestimenti-fieristici-X) <-> pagine fiera e <-> calendario-fiere-X: intenti diversi e link reciproci, ok.
- Corretto: 2 pagine video avevano il titolo "stand fieristico chiavi in mano" (competevano con /stand-chiavi-in-mano/): rinominate
  e collegate alla pagina servizio. Titolo /noleggio-stand-fieristici/ distinto da /noleggio-arredi-stand-fieristici/.
- Aggiunta sezione di testo esclusivo (id="pratico") a 4 pagine EN per paese e 7 pagine EN per citta': strumenti/arricchisci-pagine-en.py
  (rilanciarlo se si rigenerano quelle pagine).
- Restano piu' simili della media (non gravi): hi/ e ur/ europe-exhibition-stand vs italy-exhibition-stand.

## DA FARE
1. Dopo il push: aprire su danovastand.com alcune pagine Lavori (ja/ko/th/vi/ta/zh-hant, es. /ja/projects/) e alcune
   fiere nuove (/pt/stand-bau/, /nl/standbouw-bauma/, /pl/stoisko-drupa/): controllo visivo, menu lingue, link.
2. (FACOLTATIVO) Le pagine hub pt/nl/pl (e de/es/fr) non linkano ancora le pagine fiera: aggiungere un elenco fiere
   nella pagina europe-exhibition-stand / standbouw-beurzen-duitsland-europa di ogni lingua.
3. (FACOLTATIVO) Estendere le pagine fiera ad altre lingue (prossime consigliate: sv, da, cs, ro).
