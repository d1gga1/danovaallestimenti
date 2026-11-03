# -*- coding: utf-8 -*-
# Pagina /calendario-fiere/ con mappa interattiva (uso: python3 build_calendario.py)
from nuove_common import *
import datetime
OGGI=TODAY
P=CAL; URL=SITE+P
def page_for(fid):
    k=next((x for x,_ in FIERA_PAGES if fid.startswith(x)),None)
    return FIERA_URL[k] if k else None
evs=[f for f in sorted(DC.F,key=lambda f:(f[4],f[1])) if f[5]>=OGGI]
paesi=sorted({DC.V[f[2]][2] for f in evs},key=lambda c:(c!='IT',DC.PAESE[c]))
setts=sorted({f[3] for f in evs},key=lambda k:DC.SETT[k])
mesi=[]
for f in evs:
    ym=f[4][:7]
    if ym not in mesi: mesi.append(ym)
def mese_lab(ym): y,m=ym.split('-'); return f"{DC.MESI[int(m)-1].capitalize()} {y}"
# ---- lista per mese (HTML indicizzabile)
blocchi=''
for ym in mesi:
    items=''
    for f in [x for x in evs if x[4][:7]==ym]:
        i,n,v,st,s,e,c,site,nota=f; vn,city,cc,lat,lon,addr=DC.V[v]; pg=page_for(i)
        d1=datetime.date.fromisoformat(s); d2=datetime.date.fromisoformat(e)
        if c: dd=f"{d1.day}" + (f"–{d2.day}" if d2!=d1 and d2.month==d1.month else (f" {DC.MESI[d1.month-1][:3]} – {d2.day} {DC.MESI[d2.month-1][:3]}" if d2!=d1 else "")) + (f" {DC.MESI[d1.month-1][:3]}" if d2.month==d1.month else "")
        else: dd=DC.MESI[d1.month-1][:3]+"."
        nome=f'<a href="{pg}">{n}</a>' if pg else n
        tbc='<span class="tag tbc">date da confermare</span>' if not c else ''
        req=f"{n} – {city}, {DC.quando(i)}"
        acts=f'<button type="button" class="cal-btn" data-req="{E(req)}">Richiedi lo stand</button>'
        if pg: acts+=f'<a class="cal-btn g" href="{pg}">Scheda stand</a>'
        acts+=f'<a class="cal-btn g" href="{site}" target="_blank" rel="noopener">Sito ufficiale</a>'
        items+=f'''
      <li class="cal-ev" id="f-{i}" data-id="{i}" data-paese="{cc}" data-sett="{st}" data-mese="{ym}" data-end="{e}" data-v="{v}">
        <div class="d">{dd}<i>{d1.year}</i></div>
        <div><h4>{nome}{tbc}</h4><p>{vn}, {city} ({DC.PAESE[cc]}) · {DC.SETT[st]}{(" · "+nota) if nota else ""}</p></div>
        <div class="act">{acts}</div>
      </li>'''
    blocchi+=f'''
    <div class="cal-mese" data-mese="{ym}">
      <h3>{mese_lab(ym)}</h3>
      <ul class="cal-list">{items}
      </ul>
    </div>'''
opt=lambda pairs,all_: f'<option value="">{all_}</option>'+''.join(f'<option value="{a}">{b}</option>' for a,b in pairs)
venues={k:{"n":v[0],"c":v[1],"p":DC.PAESE[v[2]],"lat":v[3],"lon":v[4]} for k,v in DC.V.items() if any(f[2]==k for f in evs)}
data=json.dumps({"v":venues},ensure_ascii=False,separators=(',',':'))
n_it=sum(1 for f in evs if DC.V[f[2]][2]=='IT')
main=hero("Calendario fiere 2026 · 2027",'Calendario fiere 2026–2027 <span class="grad">in Italia e in Europa</span>.',
 f"Le date delle principali fiere internazionali, su una mappa interattiva: {len(evs)} manifestazioni in {len(paesi)} paesi, da Vinitaly al Salone del Mobile, da EICMA a Hannover Messe. Filtra per paese, settore e mese, clicca una fiera e richiedi il tuo stand: progetto, materiali e montatori li organizziamo noi.",
 "Apri la mappa","#mappa","Richiedi uno stand","#richiesta",
 extra=f'\n    <div class="fr-dates" data-rv="up"><span>{len(evs)} fiere</span><span>{n_it} in Italia</span><span>{len(paesi)} paesi</span><span>Aggiornato all’8 ottobre 2026</span></div>')
H_MAPPA=head('Mappa delle fiere','Ogni punto è un quartiere fieristico. Clicca per vedere le fiere in programma e richiedere lo stand.')
H_ELENCO=head('Tutte le fiere, mese per mese',"Le date sono quelle pubblicate dagli organizzatori, raccolte l'8 ottobre 2026. Dove l'edizione non ha ancora date ufficiali indichiamo il mese previsto, «da confermare». Prima di prenotare viaggi e trasporti verifica sempre sul sito ufficiale.")
O_PAESE=opt([(c,DC.PAESE[c]) for c in paesi],"Tutti i paesi"); O_SETT=opt([(k,DC.SETT[k]) for k in setts],"Tutti i settori"); O_MESE=opt([(m,mese_lab(m)) for m in mesi],"Tutti i mesi")
main+=f'''<section id="mappa">
  <div class="wrap">
{H_MAPPA}
    <div class="cal-tools" role="search">
      <input class="q" type="search" id="cal-q" placeholder="Cerca una fiera, una città o un settore…" aria-label="Cerca una fiera">
      <select id="cal-paese" aria-label="Paese">{O_PAESE}</select>
      <select id="cal-sett" aria-label="Settore">{O_SETT}</select>
      <select id="cal-mese" aria-label="Mese">{O_MESE}</select>
    </div>
    <div class="cal-map" id="cal-map" aria-label="Mappa interattiva delle fiere"><div class="ph">Caricamento della mappa…</div></div>
    <p class="cal-count" id="cal-count" aria-live="polite">{len(evs)} fiere in calendario</p>
  </div>
</section>
<section id="elenco">
  <div class="wrap">
{H_ELENCO}
    <div id="cal-elenco">{blocchi}
    </div>
    <p class="cal-empty" id="cal-empty">Nessuna fiera corrisponde ai filtri. Cerchi una fiera che non è in elenco? Scrivila nel modulo qui sotto: allestiamo stand anche per manifestazioni non presenti nel calendario.</p>
  </div>
</section>
<script type="application/json" id="cal-data">{data}</script>
'''
main+=testo("come",'Come usare il calendario per <span class="grad">preparare la fiera</span>',None,
 ["Una fiera si prepara con mesi di anticipo: prima si sceglie la manifestazione e si prenota l'area, poi si progetta lo stand, si chiudono le pratiche con l'ente fiera e si organizzano produzione, trasporto e montaggio. Il calendario ti aiuta a vedere in un colpo d'occhio cosa c'è nel tuo settore nei prossimi mesi, in Italia e all'estero.",
  "Quando hai individuato la fiera, premi \"Richiedi lo stand\": la richiesta arriva a noi già compilata con nome, città e date. Ti rispondiamo con quello che serve e quanto costa, voce per voce. Se la fiera è vicina, scrivici comunque: accettiamo anche richieste urgenti."],
 [("6–9 mesi prima.","Scelta della fiera, prenotazione dell'area, primo brief per lo stand."),
  ("4–6 mesi prima.","Progetto e render 3D, preventivo, scelta fra noleggio e acquisto."),
  ("2–3 mesi prima.","Pratiche con l'ente fiera: progetto, potenza elettrica, allacci, pass."),
  ("Ultimo mese.","Produzione, grafiche, trasporto. Poi montaggio nei giorni di allestimento."),
  ("Dopo la fiera.","Smontaggio, magazzino e richiamo dei contatti raccolti. Vedi la <a href=\"/guide/come-preparare-una-fiera/\">guida per preparare una fiera</a>.")])
main+=chips("pagine","Pagine dedicate alle fiere principali","Per queste manifestazioni trovi una pagina con le esigenze specifiche dello stand.",FIERA_LINKS)
main+=chips("citta-chips","Allestimenti fieristici per città",None,CITTA_LINKS_ALL+[("Fiere all'estero","/allestimenti-fieristici-estero/"),("Fiere in Germania","/allestimenti-fieristici-germania/")])
qa=[("Le date del calendario sono ufficiali?","Sono le date pubblicate dagli organizzatori, raccolte l'8 ottobre 2026 dai siti ufficiali e, per alcune fiere estere, da calendari fieristici di settore. Dove l'edizione non ha ancora date ufficiali indichiamo il mese previsto con la dicitura \"da confermare\". Verifica sempre sul sito ufficiale prima di prenotare viaggi e trasporti."),
 ("Posso richiedere uno stand per una fiera che non è nel calendario?","Sì. Il calendario raccoglie le principali manifestazioni, ma allestiamo stand per qualsiasi fiera in Italia e in Europa: scrivi il nome della fiera nel modulo e ti rispondiamo."),
 ("Lavorate in tutte le fiere del calendario?","Sì, organizziamo progetto, materiali, trasporto e montaggio in tutti i quartieri fieristici italiani e nelle fiere estere, in Germania, Francia, Spagna, Paesi Bassi, Svizzera e Regno Unito. Dove abbiamo già allestito stand lo trovi scritto nella pagina dedicata."),
 ("Con quanto anticipo devo chiedere lo stand?","Idealmente appena hai la conferma dello spazio: per uno stand su misura servono alcuni mesi. Con soluzioni modulari e preallestite lavoriamo anche a poche settimane dalla fiera."),
 ("Ogni quanto aggiornate il calendario?","Aggiorniamo le date quando gli organizzatori pubblicano le nuove edizioni. La data dell'ultimo aggiornamento è indicata in cima alla pagina.")]
items=[]
for idx,f in enumerate([f for f in evs if f[6]],1):
    ev=event_node(f[0]); items.append({"@type":"ListItem","position":idx,"item":ev})
nodes=[{"@type":"ItemList","@id":URL+"#fiere","name":"Calendario fiere 2026–2027 in Italia e in Europa","numberOfItems":len(items),"itemListOrder":"https://schema.org/ItemListOrderAscending","itemListElement":items}]
rel=[("Allestimenti fieristici",PILLAR)]+SERVIZI_LINKS[2:]+[("Guida: come preparare una fiera","/guide/come-preparare-una-fiera/")]
scripts=REQ_JS+'\n<script src="/assets/js/calendario-fiere.js?v=3" defer></script>'
main+=richiesta("",titolo="Richiedi lo stand per la tua fiera",lead="Premi \"Richiedi lo stand\" su una fiera del calendario oppure scrivila qui: si apre WhatsApp con la richiesta già pronta.")
main+=faq(FAQ_EY,FAQ_T,qa)
main+=cta("Hai scelto la fiera?","Dicci quale, le date e la metratura: ti rispondiamo con quello che serve e quanto costa.","Richiedi il preventivo","#richiesta")
main+=altri("Approfondisci",uniq(rel,P))
print(build('it',P,"Calendario fiere 2026–2027 Italia ed Europa | Danova Tech",
 f"Calendario delle principali fiere 2026 e 2027 in Italia ed Europa: date, quartieri fieristici e settori su mappa. Clicca una fiera e richiedi lo stand.",
 "Calendario fiere 2026–2027 in Italia e in Europa","Date, sedi e settori delle principali fiere su mappa interattiva: clicca una fiera e richiedi lo stand.",
 [("Home","/"),("Allestimenti fieristici",PILLAR),("Calendario fiere",None)],main,qa,nodes,
 wp_extra={"@type":["WebPage","CollectionPage"],"mainEntity":{"@id":URL+"#fiere"}},scripts=scripts), len(evs),'fiere', len(items),'con schema')
