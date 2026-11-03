# -*- coding: utf-8 -*-
# Calendari fiere per citta' (9/10/2026): /calendario-fiere-<citta>/
# Dati da dati_calendario.py: aggiornando le date li' e rilanciando questo script si aggiornano anche queste pagine.
# Uso: python3 build_calendari_citta.py
from nuove_common import *
import datetime
OGGI=TODAY
def page_for(fid):
    k=next((x for x,_ in FIERA_PAGES if fid.startswith(x)),None)
    return FIERA_URL[k] if k else None
CITY=[  # (venue, slug, nome, sito ufficiale calendario, testo sede)
 ('bologna','bologna','Bologna',"https://www.bolognafiere.it",
  "BolognaFiere è uno dei quartieri fieristici più grandi d'Italia, a nord-est del centro, vicino alla tangenziale e all'uscita Fiera. Ospita fiere internazionali di riferimento per agricoltura, cosmetica, ceramica, meccanica ed editoria per ragazzi."),
 ('rho','milano','Milano',"https://www.fieramilano.it",
  "Fiera Milano Rho è il quartiere fieristico più grande d'Italia, raggiungibile in metropolitana (linea M1, fermata Rho Fiera), in treno e dall'autostrada. È la sede del Salone del Mobile, di EICMA, HostMilano, MIDO, MICAM e di molte altre fiere internazionali."),
 ('rimini','rimini','Rimini',"https://www.iegexpo.it",
  "Il Rimini Expo Centre, gestito da Italian Exhibition Group, ha una fermata ferroviaria dedicata sulla linea Bologna–Ancona. Ospita fiere di riferimento per ambiente ed energia, gelateria e pasticceria, ortofrutta, food & beverage e benessere."),
 ('parma','parma','Parma',"https://www.fiereparma.it",
  "Fiere di Parma si trova a nord della città, vicino all'uscita Parma dell'autostrada A1. È la sede di Cibus e Cibus Tec, punti di riferimento per l'agroalimentare e le tecnologie alimentari, e di fiere per l'automazione e il collezionismo."),
]
def riga(f):
    i,n,v,st,s,e,c,site,nota=f; pg=page_for(i)
    nome=f'<a href="{pg}">{n}</a>' if pg else n
    d1=datetime.date.fromisoformat(s)
    dd=DC.quando(i)
    tbc='<span class="tag tbc">date da confermare</span>' if not c else ''
    acts=f'<button type="button" class="cal-btn" data-req="{E(n+" – "+DC.V[v][1]+", "+dd)}">Richiedi lo stand</button>'
    if pg: acts+=f'<a class="cal-btn g" href="{pg}">Scheda stand</a>'
    acts+=f'<a class="cal-btn g" href="{site}" target="_blank" rel="noopener">Sito ufficiale</a>'
    return f'''
      <li class="cal-ev" id="f-{i}">
        <div class="d">{d1.day if c else DC.MESI[d1.month-1][:3]+'.'}<i>{DC.MESI[d1.month-1][:3]} {d1.year}</i></div>
        <div><h4>{nome}{tbc}</h4><p>{dd} · {DC.SETT[st]}{(" · "+nota) if nota else ""}</p></div>
        <div class="act">{acts}</div>
      </li>'''
for v,slug,c,official,sede in CITY:
    P=f"/calendario-fiere-{slug}/"; URL=SITE+P
    evs=[f for f in sorted(DC.F,key=lambda f:(f[4],f[1])) if f[2]==v and f[5]>=OGGI]
    vn,city,cc,lat,lon,addr=DC.V[v]
    lista=''.join(riga(f) for f in evs)
    nomi=", ".join(f[1] for f in evs[:4])
    main=hero(f"Calendario fiere {c} · 2026–2027",f'Calendario fiere {c} 2026–2027: <span class="grad">le date a {vn}</span>.',
      f"Le date delle principali fiere internazionali a {vn} nei prossimi mesi: {nomi} e le altre. Per ogni fiera trovi date, settore, sito ufficiale e, se esponi, la richiesta dello stand già compilata.",
      "Vedi le date","#elenco","Richiedi uno stand","#richiesta",
      extra=f'\n    <div class="fr-dates" data-rv="up"><span>{len(evs)} fiere</span><span>{vn}</span><span>Aggiornato al {datetime.date.fromisoformat(DC.AGG).day} ottobre 2026</span></div>')
    main+=f'''<section id="elenco">
  <div class="wrap">
{head(f"Le fiere a {c}, in ordine di data","Le date sono quelle pubblicate dagli organizzatori. Il calendario riporta le principali fiere internazionali e di settore: per l'elenco completo, comprese le fiere per il pubblico, consulta il calendario ufficiale del quartiere fieristico.")}
    <ul class="cal-list">{lista}
    </ul>
    <p class="cal-count">Calendario ufficiale completo: <a href="{official}" target="_blank" rel="noopener">{official.replace("https://www.","")}</a></p>
  </div>
</section>
'''
    main+=scheda("sede",f"Il quartiere fieristico di {c}",[("Sede",vn),("Indirizzo",addr),("Fiere in calendario",str(len(evs)))],sede)
    main+=testo("espositori",f'Esporre a {c}: <span class="grad">cosa preparare</span>',None,
     [f"Ogni fiera a {vn} ha un regolamento tecnico con le regole per gli stand: altezze massime, materiali ignifughi, portata dei pavimenti, appendimenti al soffitto, consegna del progetto per l'approvazione. Le scadenze per inviarlo cadono di solito uno o due mesi prima della fiera, e lo stesso vale per l'ordine della potenza elettrica e degli allacci.",
      "I giorni di allestimento sono pochi e gli orari di carico e scarico sono assegnati: per uno stand su misura servono una squadra che conosce il quartiere, i mezzi giusti e i materiali già pronti. Noi seguiamo tutto: progetto e pratiche con l'ente fiera, produzione, trasporto, montaggio, smontaggio e magazzino fino alla prossima edizione.",
      f"Se esponi a {c} per la prima volta, leggi anche la nostra <a href=\"/guide/come-preparare-una-fiera/\">guida per preparare una fiera</a> e la pagina con <a href=\"/contributi-fiere-2026/\">i contributi per le fiere 2026</a>."],
     [("6 mesi prima.","Prenotazione dell'area e brief dello stand."),("3–4 mesi prima.","Progetto, render 3D e preventivo."),
      ("1–2 mesi prima.","Progetto all'ente fiera, potenza elettrica, pass."),("In fiera.","Montaggio nei giorni di allestimento, smontaggio a fine manifestazione.")])
    altre_pg=[(t,FIERA_URL[k]) for k,t in FIERA_PAGES if any(f[0].startswith(k) for f in evs)]
    if altre_pg: main+=chips("stand-fiere",f"Stand per le fiere di {c}",None,altre_pg)
    qa=[(f"Quali sono le prossime fiere a {c}?",f"Le prossime fiere internazionali a {vn} sono: "+"; ".join(f"{f[1]} ({DC.quando(f[0])})" for f in evs[:6])+". Le date sono aggiornate a ottobre 2026: verificale sempre sul sito ufficiale prima di prenotare."),
        (f"Dove si trova la fiera di {c}?",f"{vn} si trova in {addr}."),
        ("Le date sono ufficiali?","Sono le date pubblicate dagli organizzatori, raccolte a ottobre 2026. Dove un'edizione non ha ancora date ufficiali è indicato il mese previsto, con la dicitura date da confermare."),
        ("Il calendario comprende tutte le fiere?",f"No: riporta le principali fiere internazionali e di settore. Per l'elenco completo, comprese le manifestazioni per il pubblico, consulta il calendario ufficiale di {vn}."),
        (f"Allestite stand a {c}?",f"Sì: progettiamo, realizziamo e montiamo stand a {vn}, su misura, modulari o preallestiti, a noleggio o in acquisto. Premi Richiedi lo stand su una fiera dell'elenco e ricevi il preventivo.")]
    items=[]
    for idx,f in enumerate([f for f in evs if f[6]],1):
        ev=event_node(f[0]); items.append({"@type":"ListItem","position":idx,"item":ev})
    nodes=[{"@type":"ItemList","@id":URL+"#fiere","name":f"Calendario fiere {c} 2026–2027","numberOfItems":len(items),"itemListOrder":"https://schema.org/ItemListOrderAscending","itemListElement":items}]
    rel=[(f"Allestimenti fieristici a {c}",CITTA_URL.get(slug,PILLAR)),("Calendario fiere Italia ed Europa",CAL),("Allestimenti fieristici",PILLAR)]+[(f"Calendario fiere {x[2]}",f"/calendario-fiere-{x[1]}/") for x in CITY if x[1]!=slug]+SERVIZI_LINKS[2:]
    t=f"Calendario fiere {c} 2026–2027: date a {vn}"
    if len(t)+14<=65: t+=" | Danova Tech"
    print(pagina(P,t,
      f"Calendario fiere {c} 2026 e 2027: date delle principali fiere a {vn}, settori e siti ufficiali. Esponi? Richiedi lo stand chiavi in mano.",
      f"Calendario fiere {c} 2026–2027",f"Le date delle principali fiere a {vn}, con richiesta dello stand.",
      [("Home","/"),("Allestimenti fieristici",PILLAR),("Calendario fiere",CAL),(f"Fiere {c}",None)],main,qa,nodes,rel,
      wp_extra={"@type":["WebPage","CollectionPage"],"mainEntity":{"@id":URL+"#fiere"}}),len(evs))
