# Area privata di danovastand.com: guida passo passo

È la stessa area privata di pandooragroup.it (`/private_area/`), adattata a Danova Stand:
niente shop, al posto di Ordini / Clienti / Newsletter c'è la scheda **Richieste**.

| Scheda | Cosa vedi |
|---|---|
| **Live** | chi c'è sul sito adesso, mappa, pagine aperte, azioni di oggi (richieste, WhatsApp, telefono) |
| **Storico** | visitatori, visite, canali, sorgenti, paesi, città, dispositivi, pagine stand e fiere più guardate, azioni, comportamento (solo chi accetta il banner) |
| **Persone** | ogni visitatore con il suo percorso; nome, email e telefono quando invia un modulo |
| **Richieste** | tutte le richieste dei moduli (contatti e "Richiedi lo stand"), con stato, valore, note, chi le ha mandate e cosa aveva guardato. Ricerca del codice **Rif.** dei messaggi WhatsApp |

Le email delle richieste continuano ad arrivare a info@danova-tech.com da FormSubmit come prima:
il database ne tiene una copia in più.

File in questa cartella (`strumenti/supabase`, non viene pubblicata online):

| File | Cosa contiene |
|---|---|
| `1-schema-database.sql` | crea le tabelle: visitatori, sessioni, visualizzazioni, eventi, richieste |
| `2-edge-function-ds.ts` | il "server": statistiche, copia delle richieste, dashboard |

---

## Passo 1: creare il progetto Supabase (uno nuovo, separato da Pandoora)

1. Su supabase.com → **New project**. Nome: `danova-stand`.
2. **Region: Central EU (Frankfurt)**, così i dati restano nell'Unione europea (è scritto anche nella privacy).
3. Inventa una password per il database (non serve dopo) e crea il progetto.
4. Il **codice del progetto** è la parte dell'indirizzo prima di `.supabase.co`
   (Project Settings → General → Project ID, es. `abcdefghijklmnopqrst`). Ti serve al passo 5.

Il piano gratuito permette 2 progetti attivi: Pandoora + Danova Stand ci stanno.

## Passo 2: creare le tabelle

1. Nel progetto: **SQL Editor** → **+ New query**.
2. Apri `1-schema-database.sql` con TextEdit, copia tutto, incolla, **Run**.
3. Deve comparire `ok: tabelle create`.

## Passo 3: impostare i segreti

**Edge Functions → Secrets** → **Add new secret**:

| Nome (esattamente così) | Valore |
|---|---|
| `ADMIN_PASSWORD` | la password per entrare in `danovastand.com/private_area/` |
| `DS_SEGRETO` | una frase lunga a caso. Non cambiarla più dopo l'avvio |
| `IPINFO_TOKEN` | facoltativo: posizione dei visitatori più precisa (token gratuito di ipinfo.io, lo stesso di Pandoora va bene) |

## Passo 4: pubblicare la funzione

1. **Edge Functions → Deploy a new function → Via Editor**.
2. Nome esattamente: `ds`
3. Cancella il codice di esempio, incolla tutto `2-edge-function-ds.ts`, **Deploy function**.
4. **Importante:** apri la funzione `ds` → **Details** → **disattiva "Verify JWT"** e salva.

Controllo: apri `https://CODICE-PROGETTO.supabase.co/functions/v1/ds`
Devi vedere `{"ok":true,"servizio":"ds","sezioni":["s","richiesta","admin"]}`.
Se vedi un errore 401, "Verify JWT" è ancora attivo.

## Passo 5: collegare il sito

Nel Terminale:

    cd ~/danova_allestimenti
    python3 strumenti/attiva-area-privata.py CODICE-PROGETTO

Scrive il codice in `assets/js/ds-live.js` e `private_area/index.html`. Prima di questo passo lo script
delle statistiche è già nelle pagine ma resta spento: non succede niente.

## Passo 6: pubblicare e provare

1. Pubblica come sempre (commit e push su GitHub).
2. Apri `danovastand.com/private_area/` ed entra con `ADMIN_PASSWORD`.
3. Da ogni tuo computer e telefono apri una volta `danovastand.com/?dslive=no`: le tue visite non verranno contate.
4. Da un telefono non escluso apri una pagina fiera, clicca WhatsApp e invia il modulo "Richiedi lo stand":
   in **Live** compare la visita, in **Richieste** la richiesta.

Se qualcosa non va: Supabase → Edge Functions → `ds` → **Logs**.

---

## Da sapere

- **Sicurezza:** RLS attiva su tutte le tabelle, nessuna regola pubblica: le legge e scrive solo la funzione `ds`.
  La dashboard si apre solo con la password; l'accesso dura 12 ore.
- **Privacy:** l'indirizzo IP non viene salvato. I conteggi sono anonimi; clic, sezioni lette e moduli
  solo per chi accetta il banner. Cookie policy e privacy (IT, EN, DE, FR, ES) sono state aggiornate dallo
  script: falle comunque rileggere a chi segue la parte legale.
- **Banner:** compare alla prima visita (non sulle pagine `/render/`). Per toglierlo: in `assets/js/ds-live.js`
  metti `var MOSTRA_BANNER = false;` (restano solo i conteggi anonimi).
- **Pagine render dei clienti:** le visite a `/render/...` vengono contate: in Storico e Persone vedi quando
  il cliente ha aperto il suo progetto.
- **Dopo `migra-da-danovatech.py`** rilancia `python3 strumenti/attiva-area-privata.py` (rimette lo script
  nelle pagine e i testi legali).
- **Cambiare password della dashboard:** Supabase → Edge Functions → Secrets → `ADMIN_PASSWORD`.
- **Piano gratuito:** 500.000 chiamate al mese. Ogni visitatore ne usa qualche decina. Controlla in Supabase → Usage.

---

## Più siti nella stessa area privata (22/11/2026)

La dashboard mostra anche **Danova Costruzioni** (danovacostruzioni.it) e **Danova Tech** (danova-tech.com):
si sceglie il sito dal menu giallo in alto a sinistra (c'è anche "Tutti i siti").
Stesso database, stessa funzione `ds`: ogni sito manda il proprio nome con le visite e le richieste.

- `assets/js/ds-live.js` è **lo stesso file** nei tre siti (il sito si riconosce dal dominio).
  Se lo modifichi qui, ricopialo negli altri con lo script qui sotto.
- Collegare / aggiornare gli altri siti (mette lo script nelle pagine e aggiorna cookie policy e privacy):

      python3 strumenti/attiva-area-privata.py --sito costruzioni ~/danova_costruzioni
      python3 strumenti/attiva-area-privata.py --sito tech ~/Desktop/dantech/danovatech

- Il popup −3% newsletter e la fascia preventivo restano solo su Danova Stand.
- "Non contare le mie visite": il link `?dslive=no` va aperto una volta **per ogni sito**.
- Le visite e richieste raccolte prima di questo aggiornamento risultano di Danova Stand.
