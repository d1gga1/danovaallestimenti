# -*- coding: utf-8 -*-
# Pagine /stand-<fiera>/  (uso: python3 build_fiere.py)
from nuove_common import *
import dati_pagine_fiere as D
PROC=[("Brief","Fiera, padiglione, metratura e tipo di spazio, obiettivi e budget. Se hai già un progetto, partiamo da quello."),
 ("Progetto e preventivo","Render 3D dello stand e preventivo voce per voce. Si parte solo quando sei d'accordo."),
 ("Pratiche con l'ente fiera","Progetto, impianto elettrico, allacci e pass presentati secondo il regolamento tecnico della manifestazione."),
 ("Produzione e montaggio","Strutture, grafiche e arredi pronti e verificati prima di partire; montaggio nei giorni di allestimento."),
 ("Fiera e smontaggio","Assistenza durante la fiera, smontaggio a fine manifestazione e, se lo stand è tuo, magazzino per la prossima edizione.")]
GEN_QA=[("Quanto costa uno stand per {n}?","Dipende da metratura, tipo di struttura, finiture, impianti e servizi richiesti. Ti mandiamo un preventivo gratuito voce per voce; nella <a href=\"/quanto-costa-uno-stand-fieristico/\">guida ai costi</a> trovi le voci che incidono di più."),
 ("Lo stand è a noleggio o di proprietà?","Come preferisci: preallestito, modulare, in tessuto teso o su misura, a noleggio o in acquisto. Se è tuo, lo conserviamo in magazzino per la prossima edizione.")]
def run():
    out=[]
    for d in D.P:
        k=d['k']; n=d['nome']; P=FIERA_URL[k]; c=d['citta']; q=d['q']
        qs=[DC.quando(x) for x in d['cal']]
        anno=min(DC.FIERE[x][4][:4] for x in d['cal'])
        dates=''.join(f'<span>{DC.FIERE[x][1]}: {DC.quando(x)}</span>' for x in d['cal'])
        extra=f'\n    <div class="fr-dates" data-rv="up">{dates}<span>{q}, {c}</span></div>'
        m=hero(f"Stand · {n}",f'Stand per {n}: <span class="grad">allestimento chiavi in mano</span> a {q}.',d['lead'],
               "Richiedi lo stand per "+n,"#richiesta","Cosa serve allo stand","#esigenze",extra=extra)
        v=DC.V[DC.FIERE[d['cal'][0]][2]]; site=DC.FIERE[d['cal'][0]][7]
        sl=DC.SETT_PAGE.get(d['sett'])
        sett_txt=DC.SETT[d['sett']]+(f' · <a href="{sl}">stand per il settore</a>' if sl else '')
        rows=[("Fiera",n),("Dove",f"{q}, {c}<br><small>{v[5]}</small>"),
              ("Prossima edizione","<br>".join(f"{DC.FIERE[x][1]}: {DC.quando(x)}" for x in d['cal'])),
              ("Cadenza",d['cad']),("Settore",sett_txt),
              ("Sito ufficiale",f'<a href="{site}" rel="noopener" target="_blank">{site.split("//")[1].rstrip("/")}</a>'),
              ("La nostra esperienza",(f"Abbiamo già allestito stand a {n}." if d['exp'] else f"Allestiamo stand per {n} e per le fiere del settore in Italia e all'estero."))]
        m+=scheda("scheda",f"{n} in breve",rows,f"Le date sono quelle pubblicate dall'organizzatore (aggiornate all'{DC.AGG[8:].lstrip('0')} ottobre 2026): verificale sempre sul sito ufficiale prima di prenotare viaggi e trasporti.")
        m+=testo("fiera",f"Cos'è {n} e <span class=\"grad\">cosa chiede allo stand</span>",None,d['intro'])
        m+=testo("esigenze",f"Cosa serve a uno stand per {n}",None,[],d['esig'])
        m+=cards("cosa","Cosa facciamo per il tuo stand",f"Possiamo seguire tutto, dal progetto allo smontaggio, oppure solo la parte che ti manca.",SERVIZI_CARDS(" a "+q))
        m+=testo("tempi",f"Quando iniziare a preparare lo stand per {n}",None,[d['tempi'],f"Tutte le date delle prossime fiere, in Italia e in Europa, sono nel nostro <a href=\"{CAL}\">calendario fiere 2026–2027</a> con mappa interattiva."])
        m+=passi("metodo","Come lavoriamo",f"Dal brief allo stand <span class=\"grad\">pronto a {q}.</span>",None,PROC)
        qa=d['qa']+[(a.format(n=n),b) for a,b in GEN_QA]
        rel=([(f"Allestimenti fieristici a {c}",CITTA_URL[d['cs']])] if d['cs'] in CITTA_URL else [])+[("Calendario fiere 2026–2027",CAL)]
        if sl: rel.append((dict(SETTORI)[sl.strip('/')],sl))
        rel+=[(f"Stand {x['nome']}",FIERA_URL[x['k']]) for x in D.P if x['sett']==d['sett'] and x['k']!=k][:4]
        rel+=[("Stand a isola","/stand-a-isola/"),("Stand preallestiti","/stand-preallestiti/"),("Stand su misura","/stand-fieristici-su-misura/"),
              ("Montaggio stand","/montaggio-stand-fieristici/"),("Quanto costa uno stand","/quanto-costa-uno-stand-fieristico/"),("Allestimenti fieristici",PILLAR)]
        evs=[e for e in (event_node(x) for x in d['cal']) if e]
        node=svc(P,f"Stand per {n}","Allestimento e montaggio di stand fieristici",
            f"Progettazione, fornitura di materiali e componentistica, grafica, impianti, montaggio e smontaggio di stand per {n} a {q} ({c}).",d['off'],[{"@type":"City","name":c}])
        wpx={"mentions":evs} if evs else None
        sn=d.get('short',n)
        title=f"Stand {sn} {anno}: allestimento a {c} | Danova Tech"
        if len(title)>62: title=f"Stand {sn} {anno} a {c} | Danova Tech"
        desc=f"Stand per {n} a {q}: progetto 3D, materiali, grafica, impianti e montatori in fiera. Prossima edizione: {qs[0]}. Preventivo gratuito."
        if len(desc)>160: desc=desc.replace(" Preventivo gratuito.","")
        if len(desc)>160: desc=desc.replace("progetto 3D, materiali, grafica, impianti e montatori in fiera","progetto, materiali, impianti e montaggio")
        if len(desc)>160: desc=desc.replace(" (date da confermare)","")
        crumbs=[("Home","/"),("Allestimenti fieristici",PILLAR),("Calendario fiere",CAL),(f"Stand {n}",None)]
        out.append(pagina(P,title,desc,f"Stand per {n} — Danova Tech",f"Allestimento chiavi in mano a {q}: progetto, materiali, grafica, impianti e montatori in fiera.",
            crumbs,m,qa,[node],rel,cta_t=f"Esponi a {n}?",wp_extra=wpx,fiera_form=f"{n} – {c}, {qs[0]}"))
        print(f"{len(title):3d} {len(desc):3d} {P}")
    return out
if __name__=='__main__': run()
