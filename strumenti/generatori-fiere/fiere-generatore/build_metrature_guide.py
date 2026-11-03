# -*- coding: utf-8 -*-
"""Pagine per metratura (/stand-<n>-mq/ + hub) e guide fiere in italiano. 14 ottobre 2026.
Uso: python3 build_metrature_guide.py   (poi link_metrature_guide.py, sitemap e llms)"""
from nuove_common import *
import dati_metrature_guide as D
HUB = "/stand-fieristici-per-metratura/"

def sezioni(secs):
    m = ''
    for s in secs:
        if s[0] == 't': m += testo(s[1], s[2], s[3], s[4], s[5])
        elif s[0] == 'c': m += cards(s[1], s[2], s[3], s[4])
        elif s[0] == 'p': m += passi(s[1], s[2], s[3], None, s[4])
        elif s[0] == 's': m += scheda(s[1], s[2], s[3], s[4])
    return m

def tit(t):
    return t if len(t) <= 62 else t.replace(' | Danova Tech', '')

def metrature():
    links = [(f"Stand {x['mq']} mq" + (" e oltre" if x['mq'] == 100 else ""), f"/{x['slug']}/") for x in D.M]
    for x in D.M:
        P = f"/{x['slug']}/"
        m = hero(f"Stand per metratura · {x['mq']} mq", x['h1'], x['lead'], f"Preventivo per uno stand di {x['mq']} mq", "#richiesta", "Come si organizza", "#come")
        m += scheda("scheda", f"Stand di {x['mq']} mq in breve", x['rows'])
        m += sezioni(x['sections'])
        m += cards("servizi", "Cosa facciamo per il tuo stand", "Progetto, materiali, grafica, impianti e montaggio, oppure solo la parte che ti manca.", SERVIZI_CARDS(""))
        m += chips("altre", "Altre metrature", None, [l for l in links if l[1] != P] + [("Tutte le metrature", HUB)])
        rel = [("Stand per metratura", HUB), ("Stand piccoli", "/stand-fieristici-piccoli/"), ("Stand ad angolo e a penisola", "/stand-ad-angolo/"), ("Stand a isola", "/stand-a-isola/"),
               ("Stand a due piani", "/stand-a-due-piani/"), ("Quanto costa uno stand", "/quanto-costa-uno-stand-fieristico/"), ("Progetti di stand", "/progetti-stand-fieristici/"), ("Allestimenti fieristici", PILLAR)]
        node = svc(P, f"Stand fieristico di {x['mq']} mq", "Allestimento e montaggio di stand fieristici",
                   f"Progetto, materiali, grafica, impianti, montaggio e smontaggio di stand fieristici di {x['mq']} metri quadri ({x['dims']}).",
                   [f"Stand {x['mq']} mq a noleggio", f"Stand {x['mq']} mq su misura", "Montaggio e smontaggio in fiera"])
        crumbs = [("Home", "/"), ("Allestimenti fieristici", PILLAR), ("Stand per metratura", HUB), (f"{x['mq']} mq", None)]
        pagina(P, tit(x['title']), x['desc'], f"Stand di {x['mq']} mq — Danova Tech", x['desc'], crumbs, m, x['qa'], [node], rel, cta_t=f"Hai uno spazio di {x['mq']} mq?", fiera_form="")
        print(len(tit(x['title'])), len(x['desc']), P)
    # hub
    righe = [(f'<a href="/{x["slug"]}/">Stand {x["mq"]} mq</a>', f"{x['dims']} · " + x['rows'][3][1]) for x in D.M]
    m = hero("Stand per metratura", 'Stand fieristici per metratura: <span class="grad">dal 9 mq alle isole oltre i 300 mq.</span>',
             "La metratura decide quasi tutto: cosa ci sta, quanti lati aperti, se serve una sala incontri, quanto tempo richiede il montaggio. Qui trovi, per ogni misura, i layout che funzionano, gli errori da evitare e le soluzioni più adatte.",
             "Richiedi un preventivo", "#richiesta", "Scegli la metratura", "#metrature")
    m += scheda("metrature", "Scegli la metratura", righe, "Le misure sono indicative: in ogni fiera lo spazio dipende dal padiglione e dal regolamento tecnico.")
    m += testo("come-scegliere", "Come scegliere <span class=\"grad\">la metratura giusta</span>", None, [
        "Parti da cosa deve succedere nello stand. Se devi solo farti vedere e raccogliere contatti, 9–16 mq ben progettati bastano. Se devi far sedere clienti e distributori, servono almeno 24 mq. Se devi mostrare macchine, fare demo e ospitare, si sale a 48 mq e oltre.",
        "Poi guarda il tipo di spazio: un angolo o una penisola con la stessa metratura valgono molto di più di uno spazio in linea, perché si vedono da più corridoi. E se esponi più volte l'anno con metrature diverse, uno stand modulare di proprietà si adatta a tutte."], None)
    m += testo("lati", "Lati aperti", None, [], [("In linea.", "Un lato aperto: il più economico, va progettato per farsi notare."), ("Ad angolo.", "Due lati aperti: più visibilità con poca spesa in più. Vedi <a href=\"/stand-ad-angolo/\">stand ad angolo</a>."),
        ("A penisola.", "Tre lati aperti: lo stand diventa un piccolo showroom."), ("A isola.", "Quattro lati aperti: architettura vera, anche a due piani. Vedi <a href=\"/stand-a-isola/\">stand a isola</a>.")])
    m += cards("servizi", "Cosa facciamo per il tuo stand", None, SERVIZI_CARDS(""))
    qa = [("Che metratura serve per la prima fiera?", "Per una prima fiera di settore 12–16 mq sono spesso sufficienti, meglio se ad angolo. Conta più il progetto che i metri quadri."),
          ("Realizzate anche stand molto grandi?", "Sì, anche oltre i 300 mq, a isola e a due piani, con montatori partner gestiti da noi e laboratori di fiducia."),
          ("Lo stesso stand può servire per metrature diverse?", "Sì, se è modulare: lo configuriamo di volta in volta e lo conserviamo nel nostro magazzino."),
          ("Quanto costa uno stand al metro quadro?", "Il prezzo al metro quadro dice poco: dipende da struttura, finiture, impianti e servizi. Ti mandiamo un preventivo gratuito voce per voce.")]
    rel = [("Stand piccoli", "/stand-fieristici-piccoli/"), ("Stand a isola", "/stand-a-isola/"), ("Stand a due piani", "/stand-a-due-piani/"), ("Quanto costa uno stand", "/quanto-costa-uno-stand-fieristico/"), ("Allestimenti fieristici", PILLAR)]
    node = svc(HUB, "Stand fieristici per metratura", "Allestimento e montaggio di stand fieristici", "Stand fieristici da 9 mq a oltre 300 mq: progetto, materiali, grafica, impianti e montaggio.",
               ["Stand piccoli", "Stand medi", "Stand a isola", "Stand a due piani"])
    pagina(HUB, "Stand fieristici per metratura: da 9 a oltre 300 mq", "Stand fieristici per metratura: 9, 12, 16, 24, 32, 48 e 100 mq e oltre. Cosa ci sta, layout, lati aperti e soluzioni per ogni misura. Preventivo gratuito.",
           "Stand fieristici per metratura — Danova Tech", "Layout e soluzioni per ogni metratura, dal 9 mq alle isole oltre i 300 mq.",
           [("Home", "/"), ("Allestimenti fieristici", PILLAR), ("Stand per metratura", None)], m, qa, [node], rel, cta_t="Che spazio hai prenotato?")
    print('hub', HUB)

def guide():
    for g in D.G:
        P = f"/guide/{g['slug']}/"
        m = hero("Guida · Fiere", g['h1'], g['lead'], "Parla con noi del tuo stand", "#richiesta", "Leggi la guida", "#" + g['sections'][0][1])
        m += sezioni(g['sections'])
        node = article_node(SITE + P, strip_tags(g['h1']), g['desc'], 'it')
        crumbs = [("Home", "/"), ("Guide", "/guide/"), (strip_tags(g['h1']).split(':')[0], None)]
        rel = g['rel'] + [("Allestimenti fieristici", PILLAR), ("Calendario fiere", CAL)]
        pagina(P, tit(g['title']), g['desc'], tit(g['title']).replace(' | Danova Tech', ''), g['desc'], crumbs, m, g['qa'], [node], rel, cta_t="Vuoi una mano con lo stand?")
        print(len(tit(g['title'])), len(g['desc']), P)

if __name__ == '__main__':
    metrature(); guide()
