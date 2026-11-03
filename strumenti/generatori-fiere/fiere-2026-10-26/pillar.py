# -*- coding: utf-8 -*-
"""26/10/2026 - le due pillar della sezione fiere, con ruoli separati per non farsi concorrenza:
  /servizi/allestimenti-fieristici/  -> query "allestimenti fieristici", "allestitore/allestitori fieristici" (pagina servizio)
  /stand-fieristici/                 -> query "stand fieristici", "stand per fiere" (hub: tipi, fiere, citta', prezzi)
Idempotente; chiamato da applica.py."""
import os, re
from applica import ROOT, set_meta, blocco, set_faq, set_jsonld, breve_html

SERV = dict(
 title="Allestimenti fieristici: allestitore stand in Italia ed Europa",
 desc="Allestitore fieristico con sede in Veneto: oltre 300 stand montati, progetto 3D, laboratori partner, montaggio in Italia e in 11 paesi europei. Preventivo in 24 ore.",
 breve="Danova Tech è un <b>allestitore fieristico</b> con sede a Mansuè (Treviso), magazzini a Fontanelle (TV) e Trumello (PV) e uffici a Vermezzo con Zelo (MI). Progetta e realizza <b>allestimenti fieristici chiavi in mano</b> in Italia e in 11 paesi europei: progetto e render 3D, pratiche con l'ente fiera, produzione degli elementi in legno con laboratori partner, grafica, impianto elettrico con dichiarazione di conformità, trasporto, montaggio, smontaggio e magazzino. Il team ha montato oltre 300 stand, tra cui stand al Vinitaly, Marmomac, Salone del Mobile, EICMA, Host, Cosmoprof, Cersaie, EIMA, Sigep, Ecomondo, VicenzaOro e Sicam.",
 dl=[("Sede","Mansuè (TV), via Rigole 48"),("Stand montati","Oltre 300, in Italia e all'estero"),("Dove","Tutta Italia e 11 paesi europei"),("Tipi","Preallestiti, modulari, su misura, a noleggio o in acquisto"),("Materiali","Certificati in Classe 1 di reazione al fuoco"),("Preventivo","Gratuito, voce per voce, entro 24 ore")],
 faq=[("Cosa fa un allestitore fieristico?","Un allestitore fieristico progetta lo stand sulla metratura e sul regolamento della fiera, fa approvare il progetto dall'ente, produce o procura strutture, arredi, grafiche e impianti, li trasporta in fiera, monta lo stand nei giorni di allestimento e lo smonta a fine manifestazione. Danova Tech segue tutte queste fasi con un unico referente."),
  ("Come si sceglie un allestitore fieristico?","Conviene chiedere esempi di stand nella stessa fiera, un preventivo voce per voce, chi monta (squadre proprie o partner coordinati), chi rilascia la dichiarazione di conformità dell'impianto elettrico e dove viene conservato lo stand dopo la fiera. Trovi la lista completa nella <a href=\"/guide/come-scegliere-un-allestitore-fieristico/\">guida per scegliere un allestitore</a>.")])
SERV['ente'] = None

STAND = dict(
 title="Stand fieristici: tipi, misure, fiere e prezzi | Danova Tech",
 desc="Stand fieristici preallestiti, modulari e su misura da 9 a oltre 300 mq: tipi, metrature, fiere, città, prezzi e guide. Oltre 300 stand montati in Italia e in Europa.")

def servizi():
    p = os.path.join(ROOT, 'servizi', 'allestimenti-fieristici', 'index.html')
    s = open(p, encoding='utf-8').read()
    s = set_meta(s, SERV['title'], SERV['desc'])
    s = s.replace('<div class="eyebrow mono" data-scramble>Allestimenti fieristici · Novità</div>',
                  '<div class="eyebrow mono" data-scramble>Allestimenti fieristici · Italia ed Europa</div>')
    s = blocco(s, 'fr-breve', breve_html(SERV, 'X').replace('Allestimenti fieristici a X, <span class="grad">in poche righe</span>',
               'Chi siamo come allestitori, <span class="grad">in poche righe</span>'), '<!--/fr-foto-->')
    s, fin = set_faq(s, SERV['faq'])
    s = set_jsonld(s, fin, SERV['title'], SERV['desc'])
    open(p, 'w', encoding='utf-8').write(s); return p

def stand():
    p = os.path.join(ROOT, 'stand-fieristici', 'index.html')
    s = open(p, encoding='utf-8').read()
    s = set_meta(s, STAND['title'], STAND['desc'])
    open(p, 'w', encoding='utf-8').write(s); return p

if __name__ == '__main__':
    print(servizi()); print(stand())
