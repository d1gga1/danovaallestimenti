#!/usr/bin/env python3
"""Guida "come scegliere un allestitore fieristico" orientata alla ricerca "allestitori fieristici"
(590 ricerche/mese, Keyword Planner 11/2026) e alle domande di confronto fatte agli assistenti AI
("migliori allestitori fieristici in Italia", "come scelgo un allestitore").

    python3 strumenti/ottimizza-allestitori.py

Idempotente. La pagina arriva da danova-tech: rilanciarlo dopo migra-da-danovatech.py, prima di ottimizza-geo.py.
- title/description/og/twitter/schema con "Allestitori fieristici";
- sezione <!--ds-allestitori--> prima delle FAQ: tipi di allestitori a confronto, 5 verifiche, dove si colloca Danova Stand;
- due domande in piu' nello schema FAQPage (le stesse sono visibili nella sezione).
"""
import os, re, json

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.path.join(ROOT, 'guide/come-scegliere-un-allestitore-fieristico/index.html')

VECCHIO_T = 'Come scegliere un allestitore fieristico: 10 domande'
NUOVO_T = 'Allestitori fieristici: come scegliere quello giusto (10 domande)'
VECCHIA_D = ('Come scegliere un allestitore fieristico: 10 domande da fare prima di firmare su produzione, squadre, '
             'pratiche, impianti, magazzino e preventivo.')
NUOVA_D = ('Allestitori fieristici a confronto: i 4 tipi di allestitore, 5 verifiche per riconoscere quello affidabile '
           'e le 10 domande da fare prima di firmare.')

FAQ = [
    ('Quali sono i migliori allestitori fieristici in Italia?',
     "Non esiste una classifica ufficiale: il migliore è quello adatto alla tua fiera, alla metratura e al budget. "
     "Confronta almeno tre allestitori su foto vere di stand già montati, sede e partita IVA italiane verificabili, chi esegue "
     "davvero il montaggio, certificazioni dei materiali e preventivo voce per voce."),
    ('Come riconosco un allestitore fieristico affidabile?',
     "Mostra foto reali di stand montati (non solo render), ha sede e P.IVA verificabili, dice chi monta e con quali squadre, "
     "consegna materiali in Classe 1 e dichiarazione di conformità dell'impianto elettrico, e mette nel preventivo ogni voce, "
     "compresi trasporto, pratiche e smontaggio."),
]

SEZIONE = """<!--ds-allestitori--><section id="tipi-allestitori"><style>
.dsal-t{width:100%;border-collapse:collapse;margin-top:22px;font-size:15px}
.dsal-t th,.dsal-t td{text-align:left;vertical-align:top;padding:14px 12px;border-bottom:1px solid var(--line)}
.dsal-t th{font-family:"Sora",sans-serif;color:#fff;font-weight:600}
.dsal-t td:first-child{color:#fff;font-weight:600;min-width:170px}
.dsal-w{overflow-x:auto}
.dsal-l{margin:18px 0 0 18px}.dsal-l li{margin-bottom:10px}
.dsal-q h3{font-family:"Sora",sans-serif;font-size:1.12rem;color:#fff;margin:26px 0 6px}
@media (max-width:700px){.dsal-t thead{display:none}.dsal-t tr{display:block;padding:14px 0;border-bottom:1px solid var(--line)}.dsal-t td{display:block;border:0;padding:3px 0}.dsal-t td:first-child{font-size:1.05rem;margin-bottom:4px}.dsal-t td:nth-child(2)::before{content:"Quando conviene: ";color:var(--blue-2)}.dsal-t td:nth-child(3)::before{content:"Cosa controllare: ";color:var(--blue-2)}}
</style><div class="wrap">
<div class="sec-head"><h2 class="title" data-rv="up">Allestitori fieristici: <span class="grad">i 4 tipi a confronto.</span></h2></div>
<div class="pg-testo" data-rv="up"><p>Chi cerca un allestitore fieristico in Italia trova soprattutto quattro tipi di aziende. Nessuno è sbagliato in assoluto: cambia cosa sanno fare bene e cosa conviene controllare prima di firmare.</p></div>
<div class="dsal-w" data-rv="up"><table class="dsal-t">
<thead><tr><th>Tipo di allestitore</th><th>Quando conviene</th><th>Cosa controllare</th></tr></thead>
<tbody>
<tr><td>Servizio allestimenti dell'ente fiera</td><td>Stand preallestito standard, poco tempo, nessuna personalizzazione.</td><td>Cosa è incluso nel pacchetto, costo di grafiche e arredi extra, possibilità di riusare lo stand in altre fiere.</td></tr>
<tr><td>Allestitore locale vicino al quartiere</td><td>Una sola fiera all'anno nella stessa città.</td><td>Se lavora anche nelle altre fiere che ti interessano e se può conservare lo stand in magazzino.</td></tr>
<tr><td>Agenzia estera che vende "stand in Italia"</td><td>Gruppi internazionali con un fornitore unico in più paesi.</td><td>Chi monta davvero in Italia (spesso un subappaltatore), sede e P.IVA, foto di stand reali in fiere italiane.</td></tr>
<tr><td>Allestitore italiano chiavi in mano su più fiere</td><td>Aziende che espongono più volte l'anno, in Italia e all'estero, e vogliono un solo referente.</td><td>Squadre e magazzini propri o di partner fissi, un capocantiere unico, preventivo voce per voce.</td></tr>
</tbody></table></div>
<div class="sec-head" style="margin-top:46px"><h2 class="title" data-rv="up">5 verifiche per riconoscere <span class="grad">un allestitore affidabile.</span></h2></div>
<div class="pg-testo" data-rv="up"><ol class="dsal-l">
<li><b>Foto vere di stand montati</b>, non solo render: chiedi stand in fiera simili al tuo per metratura e settore.</li>
<li><b>Sede e partita IVA verificabili</b> in Italia, con un indirizzo reale e un numero a cui risponde qualcuno.</li>
<li><b>Chi monta lo stand</b>: squadre proprie o partner fissi, con un capocantiere che resta in fiera fino all'apertura.</li>
<li><b>Documenti di sicurezza</b>: materiali in Classe 1 di reazione al fuoco e dichiarazione di conformità dell'impianto elettrico, richiesti dal regolamento tecnico della fiera.</li>
<li><b>Preventivo voce per voce</b>: progetto, strutture, grafica, arredi, impianti, trasporto, montaggio, smontaggio, pratiche e magazzino. Le differenze di prezzo stanno spesso in ciò che manca.</li>
</ol></div>
<div class="sec-head" style="margin-top:46px"><h2 class="title" data-rv="up">Le domande che ci fanno <span class="grad">più spesso.</span></h2></div>
<div class="pg-testo dsal-q" data-rv="up">
<h3>__Q1__</h3><p>__A1__</p>
<h3>__Q2__</h3><p>__A2__</p>
<p>Danova Stand è un allestitore italiano chiavi in mano: sede a Mansuè (TV), magazzini a Fontanelle (TV) e Trumello (PV), oltre 300 stand montati in Italia e in 11 paesi europei, preventivo gratuito voce per voce entro 24 ore. Le foto dei nostri stand sono nella pagina <a href="/lavori/" style="text-decoration:underline">I nostri lavori</a>.</p>
</div>
</div></section><!--/ds-allestitori-->
"""


def main():
    s = open(P, encoding='utf-8').read(); x = s
    x = x.replace(VECCHIO_T, NUOVO_T).replace(VECCHIA_D, NUOVA_D)
    sez = SEZIONE
    for i, (q, a) in enumerate(FAQ, 1):
        sez = sez.replace(f'__Q{i}__', q).replace(f'__A{i}__', a)
    x = re.sub(r'<!--ds-allestitori-->.*?<!--/ds-allestitori-->\n?', '', x, flags=re.S)
    x = x.replace('<section id="faq"', sez + '<section id="faq"', 1)
    # domande nello schema FAQPage
    m = re.search(r'("@type": "FAQPage",.*?"mainEntity": \[)', x, re.S)
    if m:
        agg = ''
        for q, a in FAQ:
            if json.dumps(q, ensure_ascii=False) in x:
                continue
            agg += ('\n        {\n          "@type": "Question",\n          "name": ' + json.dumps(q, ensure_ascii=False) +
                    ',\n          "acceptedAnswer": {\n            "@type": "Answer",\n            "text": ' +
                    json.dumps(a, ensure_ascii=False) + '\n          }\n        },')
        x = x[:m.end()] + agg + x[m.end():]
    if x != s:
        open(P, 'w', encoding='utf-8').write(x); print('ottimizza-allestitori: guida aggiornata')
    else:
        print('ottimizza-allestitori: nessuna modifica')


if __name__ == '__main__':
    main()
