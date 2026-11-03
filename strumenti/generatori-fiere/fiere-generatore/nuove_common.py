# -*- coding: utf-8 -*-
# Base comune per le pagine fiere aggiunte l'8 ottobre 2026: fiere, citta' nuove, tipologie, settori, calendario.
import sys,os; sys.path.insert(0,os.path.dirname(__file__))
from lib import *; from it_common import *
import dati_calendario as DC
CAL="/calendario-fiere/"
REQ_JS='<script src="/assets/js/fiere-richiesta.js?v=20261014" defer></script>'
# ---------------- registro di tutte le pagine fiere (vecchie + nuove), per i link interni
FIERA_PAGES=[("vinitaly","Stand Vinitaly"),("marmomac","Stand Marmomac"),("salone-del-mobile","Stand Salone del Mobile"),("eicma","Stand EICMA"),
 ("host","Stand Host Milano"),("cosmoprof","Stand Cosmoprof"),("cersaie","Stand Cersaie"),("eima","Stand EIMA"),("sicam","Stand Sicam"),
 ("samuexpo","Stand Samuexpo"),("sigep","Stand Sigep"),("cibus","Stand Cibus"),("vicenzaoro","Stand VicenzaOro"),("ecomondo","Stand Ecomondo"),
 ("pitti-uomo","Stand Pitti Uomo"),("micam","Stand MICAM"),("mido","Stand MIDO"),("macfrut","Stand Macfrut"),("expo-riva-schuh","Stand Expo Riva Schuh"),
 ("fieracavalli","Stand Fieracavalli"),
 ("lineapelle","Stand Lineapelle"),("key","Stand KEY Energy"),("emo","Stand EMO Milano"),("zoomark","Stand Zoomark"),("lamiera","Stand Lamiera"),("mecspe","Stand MECSPE"),("tuttofood","Stand TUTTOFOOD")]
FIERA_URL={k:f"/stand-{k}/" for k,_ in FIERA_PAGES}
FIERA_LINKS=[(t,FIERA_URL[k]) for k,t in FIERA_PAGES]
CITTA_NUOVE=[("Firenze","firenze"),("Torino","torino"),("Roma","roma"),("Napoli","napoli"),("Bari","bari"),("Genova","genova"),("Bergamo","bergamo"),
 ("Brescia","brescia"),("Venezia","venezia"),("Treviso","treviso"),("Udine","udine"),("Bolzano","bolzano"),("Riva del Garda","riva-del-garda"),
 ("Carrara","carrara"),("Longarone","longarone")]
TUTTE_CITTA=CITTA+CITTA_NUOVE
CITTA_URL={s:f"/allestimenti-fieristici-{s}/" for _,s in TUTTE_CITTA}
CITTA_LINKS_ALL=[(f"Stand a {c}",CITTA_URL[s]) for c,s in TUTTE_CITTA]
TIPI=[("stand-preallestiti","Stand preallestiti"),("stand-a-isola","Stand a isola"),("stand-ad-angolo","Stand ad angolo e a penisola"),
 ("stand-fieristici-piccoli","Stand piccoli (9–24 mq)"),("stand-a-due-piani","Stand a due piani"),("stand-fieristici-ecosostenibili","Stand ecosostenibili"),
 ("progettazione-stand-fieristici","Progettazione stand e render 3D"),("grafica-per-stand-fieristici","Grafica per stand"),("ledwall-e-illuminazione-stand","Ledwall e illuminazione")]
TIPI_LINKS=[(t,f"/{s}/") for s,t in TIPI]
SETTORI=[("stand-fieristici-food-e-vino","Stand per food e vino"),("stand-fieristici-arredo-e-design","Stand per arredo e design"),
 ("stand-fieristici-meccanica-e-industria","Stand per meccanica e industria"),("stand-fieristici-moda-e-calzature","Stand per moda e calzature"),
 ("stand-fieristici-cosmetica-e-beauty","Stand per cosmetica e beauty"),("stand-fieristici-agricoltura","Stand per agricoltura e zootecnia")]
SETTORI_LINKS=[(t,f"/{s}/") for s,t in SETTORI]
SERVIZI_LINKS=[("Allestimenti fieristici",PILLAR),("Calendario fiere 2026–2027",CAL),("Montaggio stand","/montaggio-stand-fieristici/"),
 ("Stand su misura","/stand-fieristici-su-misura/"),("Stand modulari","/stand-modulari/"),("Noleggio stand","/noleggio-stand-fieristici/"),
 ("Quanto costa uno stand","/quanto-costa-uno-stand-fieristico/"),("Fiere all'estero","/allestimenti-fieristici-estero/")]
def uniq(links,exclude):
    seen=set(); out=[]
    for t,u in links:
        if u==exclude or u in seen: continue
        seen.add(u); out.append((t,u))
    return out
# ---------------- blocchi nuovi
def scheda(id,title,rows,lead=None):
    r=''.join(f'\n      <div><dt>{k}</dt><dd>{v}</dd></div>' for k,v in rows)
    return f'''<section id="{id}">
  <div class="wrap">
{head(title,lead)}
    <dl class="fr-scheda" data-rv="up">{r}
    </dl>
  </div>
</section>
'''
SPAZI=["In linea (1 lato aperto)","Ad angolo (2 lati aperti)","A penisola (3 lati aperti)","A isola (4 lati aperti)","Non lo so ancora"]
def richiesta(fiera="",titolo="Richiedi lo stand",lead=None,id="richiesta"):
    """modulo che prepara il messaggio WhatsApp (o email) con la fiera gia' compilata"""
    lead=lead or "Compila i campi: si apre WhatsApp con la richiesta già pronta. Ti rispondiamo con quello che serve e quanto costa."
    opts=''.join(f'<option>{o}</option>' for o in SPAZI)
    return f'''<section id="{id}" class="fr-req-sec">
  <div class="wrap">
    <div class="fr-req-box" data-rv="up">
      <div class="fr-req-txt">
        <h2 class="title">{titolo}</h2>
        <p>{lead}</p>
        <ul class="fr-req-pt"><li>Preventivo voce per voce in meno di 24 ore, gratuito</li><li>Anche con poco preavviso</li><li>Un unico referente fino allo smontaggio</li></ul>
      </div>
      <form class="fr-req" novalidate>
        <div class="fld"><input type="text" name="fiera" id="{id}-fiera" placeholder=" " required value="{E(fiera)}" autocomplete="off"><label for="{id}-fiera">Fiera e città</label></div>
        <div class="fr-req-2">
          <div class="fld"><input type="text" name="mq" id="{id}-mq" placeholder=" " inputmode="numeric"><label for="{id}-mq">Metri quadri (anche indicativi)</label></div>
          <div class="fld"><select name="spazio" id="{id}-spazio"><option value="" selected hidden></option>{opts}</select><label for="{id}-spazio">Tipo di spazio</label></div>
        </div>
        <div class="fr-req-2">
          <div class="fld"><input type="text" name="nome" id="{id}-nome" placeholder=" " required autocomplete="name"><label for="{id}-nome">Nome e cognome</label></div>
          <div class="fld"><input type="text" name="azienda" id="{id}-azienda" placeholder=" " required autocomplete="organization"><label for="{id}-azienda">Azienda</label></div>
        </div>
        <div class="fr-req-2">
          <div class="fld"><input type="tel" name="tel" id="{id}-tel" placeholder=" " required inputmode="tel" autocomplete="tel"><label for="{id}-tel">Telefono</label></div>
          <div class="fld"><input type="email" name="email" id="{id}-email" placeholder=" " autocomplete="email"><label for="{id}-email">Email (facoltativa)</label></div>
        </div>
        <div class="fld"><textarea name="note" id="{id}-note" placeholder=" "></textarea><label for="{id}-note">Cosa ti serve (facoltativo)</label></div>
        <p class="fr-req-err" role="alert"></p>
        <button type="submit" class="btn btn-p" data-mag><span class="sheen"></span><span class="lbl">Invia la richiesta su WhatsApp</span>
          {ARR}</button>
        <p class="form-note">Preferisci l'email? <a class="fr-req-mail" href="mailto:info@danova-tech.com">Scrivici a info@danova-tech.com</a>. Inviando accetti di essere ricontattato; non condividiamo i tuoi dati con nessuno.</p>
      </form>
    </div>
  </div>
</section>
'''
def event_node(fid,url_page=None):
    """BusinessEvent per una fiera con date confermate (None se non confermate)"""
    i,n,v,st,s,e,c,site,nota=DC.FIERE[fid]
    if not c: return None
    vn,city,cc,lat,lon,addr=DC.V[v]
    from event_extra import arricchisci
    return arricchisci({"@type":"BusinessEvent","name":n,"startDate":s,"endDate":e,"url":site,
      "eventStatus":"https://schema.org/EventScheduled","eventAttendanceMode":"https://schema.org/OfflineEventAttendanceMode",
      "location":{"@type":"Place","name":vn,"address":{"@type":"PostalAddress","streetAddress":addr,"addressLocality":city,"addressCountry":cc},
        "geo":{"@type":"GeoCoordinates","latitude":lat,"longitude":lon}},
      "description":f"{n}: fiera di settore {DC.SETT[st].lower()} a {city}."+(" "+nota+"." if nota else "")})
def svc(P,name,stype,desc,offers,areas=None):
    return service_node(SITE+P,name,stype,desc,areas or AREAS_IT,offers,'it')
SERVIZI_CARDS=lambda luogo: [
  ("Progetto e render 3D",f"Lo stand disegnato sulla tua metratura e sulla posizione nel padiglione{luogo}, approvato da te prima di costruirlo."),
  ("Materiali e componentistica","Strutture, pareti, pavimenti, arredi e ogni componente richiesto dal progetto e dal regolamento tecnico della fiera."),
  ("Grafica, luci e impianti","Grafica e stampa, impianto elettrico con dichiarazione di conformità, illuminazione, moquette, schermi e ledwall."),
  ("Montatori in fiera","Montatori partner, gestiti da noi, che montano lo stand nei giorni di allestimento e lo smontano a fine manifestazione."),
  ("Noleggio o acquisto","Stand preallestiti, modulari, in tessuto teso o su misura in legno, a noleggio o di tua proprietà."),
  ("Trasporto, magazzino, pratiche","Logistica, pass e orari di carico, approvazione del progetto da parte dell'ente fiera, magazzino fra una fiera e l'altra.")]
def accorcia(desc,mx=158):
    if len(desc)<=mx: return desc
    parts=re.split(r'(?<=[.!?]) ',desc); out=''
    for x in parts:
        if len((out+' '+x).strip())>mx: break
        out=(out+' '+x).strip()
    return out or desc[:mx-1].rsplit(' ',1)[0]+'…'
def pagina(P,title,desc,ogt,ogd,crumbs,main,qa,nodes,related,cta_t="Parliamo del tuo stand.",wp_extra=None,form=True,fiera_form=""):
    desc=accorcia(desc)
    if form: main+=richiesta(fiera_form)
    main+=faq(FAQ_EY,FAQ_T,qa)
    main+=cta(cta_t,"Dicci fiera, date e metratura: ti rispondiamo con quello che serve e quanto costa, anche con poco preavviso.","Richiedi un preventivo gratuito","#richiesta" if form else CT)
    main+=altri("Approfondisci",uniq(related,P))
    return build('it',P,title,desc,ogt,ogd,crumbs,main,qa,nodes,wp_extra=wp_extra,scripts=REQ_JS if form else '')
