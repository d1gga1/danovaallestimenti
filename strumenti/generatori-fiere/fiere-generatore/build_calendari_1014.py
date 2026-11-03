# -*- coding: utf-8 -*-
# 14/10/2026: calendari fiere per citta' (Verona, Firenze) e per settore.
# Dati da dati_calendario.py. Uso: python3 build_calendari_1014.py
from nuove_common import *
import datetime
OGGI=TODAY
def page_for(fid):
    k=next((x for x,_ in FIERA_PAGES if fid.startswith(x)),None)
    return FIERA_URL[k] if k else None
def riga(f, citta=False):
    i,n,v,st,s,e,c,site,nota=f; pg=page_for(i)
    nome=f'<a href="{pg}">{n}</a>' if pg else n
    d1=datetime.date.fromisoformat(s); dd=DC.quando(i)
    tbc='<span class="tag tbc">date da confermare</span>' if not c else ''
    luogo=DC.V[v][1]+(f" ({DC.V[v][0]})" if citta else "")
    acts=f'<button type="button" class="cal-btn" data-req="{E(n+" – "+DC.V[v][1]+", "+dd)}">Richiedi lo stand</button>'
    if pg: acts+=f'<a class="cal-btn g" href="{pg}">Scheda stand</a>'
    acts+=f'<a class="cal-btn g" href="{site}" target="_blank" rel="noopener">Sito ufficiale</a>'
    info=" · ".join(x for x in [dd, luogo if citta else DC.SETT[st], nota] if x)
    return f'''
      <li class="cal-ev" id="f-{i}">
        <div class="d">{d1.day if c else DC.MESI[d1.month-1][:3]+'.'}<i>{DC.MESI[d1.month-1][:3]} {d1.year}</i></div>
        <div><h4>{nome}{tbc}</h4><p>{info}</p></div>
        <div class="act">{acts}</div>
      </li>'''
def itemlist(URL,name,evs):
    items=[]
    for f in [f for f in evs if f[6]]:
        items.append({"@type":"ListItem","position":len(items)+1,"item":event_node(f[0])})
    return {"@type":"ItemList","@id":URL+"#fiere","name":name,"numberOfItems":len(items),"itemListOrder":"https://schema.org/ItemListOrderAscending","itemListElement":items}
CITTA_CAL=[("Milano","milano"),("Bologna","bologna"),("Rimini","rimini"),("Parma","parma"),("Verona","verona"),("Firenze","firenze")]
ESPORRE=lambda dove:[f"Ogni quartiere fieristico ha un regolamento tecnico con le regole per gli stand: altezze massime, materiali ignifughi, portata dei pavimenti, appendimenti, consegna del progetto per l'approvazione. Le scadenze cadono di solito uno o due mesi prima della fiera, come l'ordine della potenza elettrica e degli allacci.",
 f"Seguiamo tutto noi: progetto e pratiche con l'ente fiera, produzione degli elementi in legno con i nostri laboratori partner, trasporto, montaggio, smontaggio e magazzino fino alla prossima edizione. Lavoriamo con materiali certificati in Classe 1 di reazione al fuoco e abbiamo già montato oltre 300 stand{dove}.",
 "Se esponi per la prima volta, leggi la <a href=\"/guide/come-preparare-una-fiera/\">guida per preparare una fiera</a> e la pagina sui <a href=\"/contributi-fiere-2026/\">contributi per le fiere 2026</a>."]
TAPPE=[("6 mesi prima.","Prenotazione dell'area e brief dello stand."),("3–4 mesi prima.","Progetto, render 3D e preventivo."),
 ("1–2 mesi prima.","Progetto all'ente fiera, potenza elettrica, pass."),("In fiera.","Montaggio nei giorni di allestimento, smontaggio a fine manifestazione.")]
out=[]
# ---------------- CITTA'
CITY=[('verona','verona','Verona',"https://www.veronafiere.it/calendario-fiere/",
  "Veronafiere è in viale del Lavoro, a sud del centro, a pochi minuti dall'uscita Verona Sud dell'A4. È uno dei poli fieristici più attivi d'Italia: ospita Vinitaly, Marmomac, Fieracavalli e Motor Bike Expo, oltre a fiere per l'agricoltura, l'energia e il collezionismo.",
  " e la produzione di Fontanelle (TV) è a circa due ore da Veronafiere"),
 ('firenze','firenze','Firenze',"https://www.pittimmagine.com",
  "La Fortezza da Basso è il quartiere fieristico di Firenze, a due passi dalla stazione di Santa Maria Novella. È la sede delle fiere di Pitti Immagine (Pitti Uomo, Pitti Bimbo, Pitti Filati) e di Taste, il salone del gusto.",
  "")]
for v,slug,c,official,sede,dove in CITY:
    P=f"/calendario-fiere-{slug}/"; URL=SITE+P
    evs=[f for f in sorted(DC.F,key=lambda f:(f[4],f[1])) if f[2]==v and f[5]>=OGGI]
    vn,city,cc,lat,lon,addr=DC.V[v]
    nomi=", ".join(f[1] for f in evs[:4])
    main=hero(f"Calendario fiere {c} · 2026–2027",f'Calendario fiere {c} 2026–2027: <span class="grad">le date a {vn}</span>.',
      f"Le date delle principali fiere a {vn} nei prossimi mesi: {nomi} e le altre. Per ogni fiera trovi date, settore, sito ufficiale e, se esponi, la richiesta dello stand già compilata.",
      "Vedi le date","#elenco","Richiedi uno stand","#richiesta",
      extra=f'\n    <div class="fr-dates" data-rv="up"><span>{len(evs)} fiere</span><span>{vn}</span><span>Aggiornato al 14 ottobre 2026</span></div>')
    main+=f'''<section id="elenco">
  <div class="wrap">
{head(f"Le fiere a {c}, in ordine di data","Le date sono quelle pubblicate dagli organizzatori; dove un'edizione non ha ancora date ufficiali è indicato il mese previsto. Per l'elenco completo, comprese le manifestazioni per il pubblico, consulta il calendario ufficiale.")}
    <ul class="cal-list">{''.join(riga(f) for f in evs)}
    </ul>
    <p class="cal-count">Calendario ufficiale completo: <a href="{official}" target="_blank" rel="noopener">{official.replace("https://www.","").rstrip("/")}</a></p>
  </div>
</section>
'''
    main+=scheda("sede",f"Il quartiere fieristico di {c}",[("Sede",vn),("Indirizzo",addr),("Fiere in calendario",str(len(evs)))],sede)
    main+=testo("espositori",f'Esporre a {c}: <span class="grad">cosa preparare</span>',None,ESPORRE(dove),TAPPE)
    altre=[(t,FIERA_URL[k]) for k,t in FIERA_PAGES if any(f[0].startswith(k) for f in evs)]
    if altre: main+=chips("stand-fiere",f"Stand per le fiere di {c}",None,altre)
    qa=[(f"Quali sono le prossime fiere a {c}?",f"Le prossime fiere a {vn} sono: "+"; ".join(f"{f[1]} ({DC.quando(f[0])})" for f in evs[:6])+". Le date sono aggiornate a ottobre 2026: verificale sempre sul sito ufficiale prima di prenotare."),
        (f"Dove si trova la fiera di {c}?",f"{vn} si trova in {addr}."),
        ("Le date sono ufficiali?","Sono le date pubblicate dagli organizzatori, raccolte a ottobre 2026. Dove un'edizione non ha ancora date ufficiali è indicato il mese previsto, con la dicitura date da confermare."),
        (f"Allestite stand a {c}?",f"Sì: progettiamo, realizziamo e montiamo stand a {vn}, su misura, modulari o preallestiti, a noleggio o in acquisto. Premi Richiedi lo stand su una fiera dell'elenco e ricevi il preventivo.")]
    rel=[(f"Allestimenti fieristici a {c}",CITTA_URL.get(slug,PILLAR)),("Calendario fiere Italia ed Europa",CAL)]+[(f"Calendario fiere {x}",f"/calendario-fiere-{s}/") for x,s in CITTA_CAL if s!=slug]+SERVIZI_LINKS[2:]
    t=f"Calendario fiere {c} 2026–2027: date a {vn}"
    if len(t)+14<=65: t+=" | Danova Tech"
    out.append(pagina(P,t,f"Calendario fiere {c} 2026 e 2027: date delle principali fiere a {vn}, settori e siti ufficiali. Esponi? Richiedi lo stand chiavi in mano.",
      f"Calendario fiere {c} 2026–2027",f"Le date delle principali fiere a {vn}, con richiesta dello stand.",
      [("Home","/"),("Allestimenti fieristici",PILLAR),("Calendario fiere",CAL),(f"Fiere {c}",None)],main,qa,[itemlist(URL,f"Calendario fiere {c} 2026–2027",evs)],rel,
      wp_extra={"@type":["WebPage","CollectionPage"],"mainEntity":{"@id":URL+"#fiere"}}))
# ---------------- SETTORI
SETT=[
 ("food-e-ristorazione","food e ristorazione",["food","vino"],"/stand-fieristici-food-e-vino/","Stand per food e vino",
  "Food, vino, ristorazione e ospitalità: le fiere dove si incontrano produttori, distributori, buyer della GDO e operatori Horeca.",
  "Nelle fiere food lo stand lavora come un punto vendita: banco di degustazione, cucina o area show cooking, frigoriferi e lavelli, spazio per i buyer. Servono allacci idrici ed elettrici previsti per tempo e materiali facili da pulire."),
 ("meccanica-e-industria","meccanica e industria",["industria","pack"],"/stand-fieristici-meccanica-e-industria/","Stand per meccanica e industria",
  "Macchine utensili, lamiera, subfornitura, automazione e packaging: le fiere dell'industria in Italia e in Europa.",
  "Lo stand di una fiera industriale deve reggere macchine vere: pedane rinforzate, portata dei pavimenti, allacci di forza motrice e aria compressa, sale riunioni per le trattative tecniche."),
 ("moda","moda, calzature e accessori",["moda","gioielli"],"/stand-fieristici-moda-e-calzature/","Stand per moda e calzature",
  "Abbigliamento, calzature, pelletteria, filati, gioielli e accessori: le fiere dove si presentano le collezioni ai buyer.",
  "Nelle fiere moda contano l'esposizione dei campionari e la luce: pareti attrezzate, appenderie, mensole per calzature e borse, illuminazione che restituisce i colori veri dei materiali e un tavolo per gli ordini."),
 ("arredo-e-design","arredo e design",["arredo"],"/stand-fieristici-arredo-e-design/","Stand per arredo e design",
  "Mobili, cucine, illuminazione, finiture e componenti per l'arredo: le fiere del design in Italia e in Europa.",
  "Per le fiere dell'arredo lo stand è un ambiente da abitare: pareti, pavimenti e luci devono valorizzare il prodotto senza rubargli la scena. La qualità delle finiture in legno fa la differenza, ed è il nostro lavoro quotidiano."),
 ("elettronica-e-tecnologia","elettronica e tecnologia",["tech"],None,None,
  "Elettronica, componenti, sistemi audio-video, ICT e smart city: le fiere della tecnologia in Italia e in Europa.",
  "Gli stand tecnologici vivono di demo: monitor e ledwall, cablaggi nascosti, postazioni per provare i prodotti, connessione stabile. Progettiamo lo stand partendo dalle demo che vuoi mostrare."),
 ("edilizia-ed-energia","edilizia ed energia",["edilizia","ambiente"],None,None,
  "Edilizia, ceramica, pietra, impianti, energia rinnovabile e ambiente: le fiere del costruire in Italia e in Europa.",
  "Nelle fiere dell'edilizia si espongono materiali pesanti e campionature di grandi dimensioni: pedane e pareti devono reggerne il peso, e lo stand stesso è spesso la prima vetrina dei materiali dell'espositore."),
 ("agricoltura","agricoltura e zootecnia",["agri"],"/stand-fieristici-agricoltura/","Stand per agricoltura e zootecnia",
  "Macchine agricole, zootecnia, ortofrutta e cavalli: le fiere dell'agricoltura in Italia e in Europa.",
  "Le fiere agricole hanno spazi grandi, spesso all'aperto, e macchine ingombranti: servono strutture robuste, pedane carrabili, coperture e un'area accoglienza per gli incontri con rivenditori e clienti."),
 ("turismo","turismo e ospitalità",["turismo"],None,None,
  "Turismo, viaggi e ospitalità: le fiere dove destinazioni, tour operator e strutture incontrano agenzie e pubblico.",
  "Uno stand per una fiera del turismo deve raccontare un luogo: grafiche di grande formato, ledwall con video, desk informativi e postazioni per gli appuntamenti con le agenzie."),
]
SETT_CAL=[(f"Calendario fiere {x[1]}",f"/calendario-fiere-{x[0]}/") for x in SETT]
for slug,nome,cats,stand_u,stand_t,intro,stand_txt in SETT:
    P=f"/calendario-fiere-{slug}/"; URL=SITE+P
    evs=[f for f in sorted(DC.F,key=lambda f:(f[4],f[1])) if f[3] in cats and f[5]>=OGGI]
    it=[f for f in evs if DC.V[f[2]][2]=='IT']; ee=[f for f in evs if DC.V[f[2]][2]!='IT']
    Nome=nome[0].upper()+nome[1:]
    nomi=", ".join(f[1] for f in evs[:4])
    main=hero(f"Fiere {nome} · 2026–2027",f'Fiere {nome} 2026–2027: <span class="grad">il calendario.</span>',
      f"{intro} Le prossime: {nomi} e le altre, con date, città e sito ufficiale. Se esponi, richiedi lo stand con un clic.",
      "Vedi le date","#italia","Richiedi uno stand","#richiesta",
      extra=f'\n    <div class="fr-dates" data-rv="up"><span>{len(it)} in Italia</span><span>{len(ee)} all\'estero</span><span>Aggiornato al 14 ottobre 2026</span></div>')
    for sid,tit,lst in (("italia",f"Fiere {nome} in Italia",it),("estero",f"Fiere {nome} all'estero",ee)):
        if not lst: continue
        main+=f'''<section id="{sid}">
  <div class="wrap">
{head(tit,"In ordine di data. Le date sono quelle pubblicate dagli organizzatori; verificale sempre sul sito ufficiale prima di prenotare.")}
    <ul class="cal-list">{''.join(riga(f,True) for f in lst)}
    </ul>
  </div>
</section>
'''
    main+=testo("stand",f'Lo stand per una fiera {nome}: <span class="grad">cosa conta</span>',None,[stand_txt]+ESPORRE("")[1:],TAPPE)
    links=[(t,FIERA_URL[k]) for k,t in FIERA_PAGES if any(f[0].startswith(k) for f in evs)]
    if stand_u: links=[(stand_t,stand_u)]+links
    if links: main+=chips("stand-fiere",f"Stand per le fiere {nome}",None,links)
    prime=evs[:6]
    qa=[(f"Quali sono le prossime fiere {nome}?","Le prossime sono: "+"; ".join(f"{f[1]} a {DC.V[f[2]][1]} ({DC.quando(f[0])})" for f in prime)+"."),
        (f"Quali sono le fiere {nome} più importanti in Italia?",("In Italia: "+", ".join(f"{f[1]} ({DC.V[f[2]][1]})" for f in it[:6])+".") if it else "Nei prossimi mesi le principali edizioni sono all'estero: le trovi nell'elenco."),
        ("Le date sono ufficiali?","Sono le date pubblicate dagli organizzatori, raccolte a ottobre 2026. Dove un'edizione non ha ancora date ufficiali è indicato il mese previsto, con la dicitura date da confermare."),
        (f"Fate stand per le fiere {nome}?","Sì: progettiamo, realizziamo e montiamo stand in Italia e in Europa, su misura, modulari o preallestiti. Premi Richiedi lo stand su una fiera dell'elenco e ricevi il preventivo.")]
    rel=[(t,u) for t,u in SETT_CAL if u!=P]+[("Calendario fiere Italia ed Europa",CAL)]+([(stand_t,stand_u)] if stand_u else [])+SERVIZI_LINKS[2:5]
    t=f"Fiere {nome} 2026–2027: calendario Italia ed Europa"
    if len(t)>65: t=f"Fiere {nome} 2026–2027: calendario"
    out.append(pagina(P,t,f"Fiere {nome} 2026 e 2027 in Italia e in Europa: date, città e siti ufficiali delle principali fiere del settore. Esponi? Richiedi lo stand.",
      f"Fiere {nome} 2026–2027",f"Il calendario delle fiere {nome} in Italia e in Europa.",
      [("Home","/"),("Allestimenti fieristici",PILLAR),("Calendario fiere",CAL),(f"Fiere {nome}",None)],main,qa,[itemlist(URL,f"Fiere {nome} 2026–2027",evs)],rel,
      wp_extra={"@type":["WebPage","CollectionPage"],"mainEntity":{"@id":URL+"#fiere"}}))
for o in out: print(o)
