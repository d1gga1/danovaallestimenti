# -*- coding: utf-8 -*-
CL=[("Allestimenti fieristici","/servizi/allestimenti-fieristici/"),
 ("Calendario fiere 2026–2027","/calendario-fiere/"),
 ("Montaggio stand fieristici","/montaggio-stand-fieristici/"),
 ("Stand fieristici su misura","/stand-fieristici-su-misura/"),
 ("Stand modulari","/stand-modulari/"),
 ("Noleggio stand fieristici","/noleggio-stand-fieristici/"),
 ("Quanto costa uno stand fieristico","/quanto-costa-uno-stand-fieristico/"),
 ("Allestimenti per eventi, showroom e negozi","/allestimenti-eventi-showroom-negozi/"),
 ("Stand per fiere all'estero","/allestimenti-fieristici-estero/"),
 ("Guida: come preparare una fiera","/guide/come-preparare-una-fiera/")]
CITTA=[("Verona","verona"),("Milano","milano"),("Bologna","bologna"),("Padova","padova"),("Vicenza","vicenza"),("Pordenone","pordenone"),("Rimini","rimini"),("Parma","parma")]
CITY_LINKS=[(f"Stand a {c}",f"/allestimenti-fieristici-{s}/") for c,s in CITTA]
FIERE=["Vinitaly","Marmomac","Salone del Mobile","EICMA","Host","Cosmoprof","Cersaie","EIMA","Sicam","Samuexpo","Sigep","VicenzaOro","Ecomondo","MICAM","MIDO","Macfrut","Lineapelle"]
PILLAR="/servizi/allestimenti-fieristici/"
CT="/#contatti"
FAQ_EY="Domande frequenti"; FAQ_T='Le risposte che <span class="grad">servono davvero.</span>'
def crumbs(name, parent=True):
    c=[("Home","/"),("Servizi","/#servizi")]
    if parent: c.append(("Allestimenti fieristici",PILLAR))
    c.append((name,None)); return c
def related(exclude):
    return [x for x in CL+CITY_LINKS if x[1]!=exclude]
AREAS_IT=[{"@type":"Country","name":"Italia"},{"@type":"Place","name":"Europa"}]
