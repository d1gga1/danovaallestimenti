# -*- coding: utf-8 -*-
# Pagine /allestimenti-fieristici-<citta>/ aggiunte l'8 ottobre 2026 (uso: python3 build_citta_nuove.py)
from nuove_common import *
import dati_citta_nuove as D
GEN=[("Accettate richieste urgenti?","Sì, anche a ridosso della fiera: lavoriamo con una rete di montatori partner e valutiamo subito cosa è possibile fare."),
 ("Lo stand è a noleggio o in acquisto?","Tutti e due: stand preallestiti, modulari, in tessuto teso e su misura, a noleggio o di tua proprietà. Se è tuo, possiamo conservarlo in magazzino per la prossima fiera."),
 ("Quanto costa uno stand?","Dipende da metratura, struttura, finiture, impianti e logistica. Ti mandiamo un preventivo su misura voce per voce; nella <a href=\"/quanto-costa-uno-stand-fieristico/\">guida ai costi</a> trovi le voci principali.")]
VICINI={'firenze':['bologna','rimini','carrara'],'torino':['milano','genova'],'roma':['napoli','firenze'],'napoli':['roma','bari'],'bari':['napoli','rimini'],
 'genova':['carrara','torino','milano'],'bergamo':['milano','brescia'],'brescia':['bergamo','verona','milano'],'venezia':['treviso','padova','vicenza'],
 'treviso':['venezia','pordenone','padova','vicenza'],'udine':['pordenone','treviso'],'bolzano':['riva-del-garda','verona'],'riva-del-garda':['verona','bolzano','brescia'],
 'carrara':['genova','firenze','parma'],'longarone':['treviso','pordenone','bolzano']}
NOMI={s:c for c,s in TUTTE_CITTA}
def run():
    for d in D.C:
        c=d['c']; P=CITTA_URL[d['s']]
        m=hero(f"Allestimenti fieristici · {c}",f'Allestimenti fieristici a {c}: <span class="grad">stand chiavi in mano</span>.',d['lead'],
               f"Preventivo per uno stand a {c}","#richiesta","Cosa facciamo","#cosa")
        m+=testo("citta",f"Stand a {c}, <span class=\"grad\">dal progetto al montaggio</span>",f"Dove lavoriamo: {d['sedi']}.",d['intro'])
        fl=[(n+(" →" if False else ""),FIERA_URL[k] if k else None) for n,k in d['fiere']]
        m+=chips("fiere",f"Fiere ed eventi a {c}","Alcune delle manifestazioni per cui allestiamo stand. Dove c'è il link trovi una pagina dedicata.",fl)
        evs=[f for f in DC.F if DC.V[f[2]][1]==c]
        if evs:
            lis=[(f"{f[1]}",f"{DC.quando(f[0])}"+(f" · <a href=\"{FIERA_URL[k]}\">stand per {f[1].split(' (')[0]}</a>" if (k:=next((x for x,_ in FIERA_PAGES if f[0].startswith(x)),None)) else "")) for f in sorted(evs,key=lambda f:f[4])]
            m+=testo("calendario",f"Prossime fiere a {c}",f"Date pubblicate dagli organizzatori, aggiornate all'8 ottobre 2026. Tutte le fiere d'Italia e d'Europa sono nel <a href=\"{CAL}\">calendario fiere con mappa</a>.",[],lis)
        m+=testo("sapere",f"Cosa sapere per uno stand a {c}",None,[],d['sapere'])
        m+=cards("cosa","Cosa facciamo per il tuo stand",None,SERVIZI_CARDS(""))
        qa=d['qa']+GEN
        rel=[("Allestimenti fieristici",PILLAR),("Calendario fiere 2026–2027",CAL)]
        rel+=[(f"Stand {n}",FIERA_URL[k]) for n,k in d['fiere'] if k]
        rel+=[(f"Allestimenti fieristici a {NOMI[s]}",CITTA_URL[s]) for s in VICINI.get(d['s'],[])]
        rel+=[("Stand preallestiti","/stand-preallestiti/"),("Stand modulari","/stand-modulari/"),("Montaggio stand","/montaggio-stand-fieristici/"),("Quanto costa uno stand","/quanto-costa-uno-stand-fieristico/")]
        node=svc(P,f"Allestimenti fieristici a {c}","Allestimento e montaggio di stand fieristici",
            f"Progettazione, fornitura di materiali e componentistica, grafica, impianti, montaggio e smontaggio di stand fieristici a {c} ({d['q']}).",
            ["Stand preallestiti","Stand modulari","Stand su misura","Montaggio e smontaggio in fiera","Noleggio stand e arredi"],[{"@type":"City","name":c}])
        title=f"Allestimenti fieristici a {c}: allestimento stand | Danova Tech"  # 13/10/2026: keyword "allestimento stand <citta>"
        if len(title)>62: title=f"Allestimenti fieristici a {c}: allestimento stand"
        desc=f"Allestimenti fieristici a {c} ({d['q']}): progetto 3D, materiali, grafica, impianti e montatori in fiera. Stand a noleggio o in acquisto, preventivo gratuito."
        if len(desc)>160: desc=desc.replace(", preventivo gratuito","")
        if len(desc)>160: desc=f"Allestimenti fieristici a {c}: progetto 3D, materiali, grafica, impianti e montatori in fiera. Stand a noleggio o in acquisto."
        pagina(P,title,desc,f"Allestimenti fieristici a {c} — Danova Tech",f"Stand chiavi in mano a {c}: progetto, materiali, componentistica e montatori in fiera.",
            [("Home","/"),("Allestimenti fieristici",PILLAR),(c,None)],m,qa,[node],rel,cta_t=f"Esponi a {c}?",fiera_form=("" if d['s'] in ("treviso","venezia") else f"Fiera a {c}"))
        print(len(title),len(desc),P)
if __name__=='__main__': run()
