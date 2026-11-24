#!/usr/bin/env python3
"""Genera la sezione LAVORI REALIZZATI (foto vere di cantiere) in italiano, francese, inglese, tedesco e spagnolo.

    python3 strumenti/genera-lavori.py

Idempotente. Rilancialo dopo ogni migra-da-danovatech.py (prima di ottimizza-geo.py):
 - riscrive gli hub /lavori/, /fr/realisations/, /en/projects/, /de/referenzen/, /es/trabajos-realizados/ e le pagine dei singoli lavori;
 - aggiunge le pagine alla sitemap (se mancano);
 - rimette i link verso i lavori nelle pagine collegate (blocchi <!--ds-lavori-->);
 - aggiorna la sezione "Lavori realizzati" di llms.txt.

Nuovo lavoro: aggiungi un dizionario in LAVORI (testi IT/FR/EN, foto in assets/img/lavori/,
nome file = parola chiave, versioni -800 e -1200 in webp + og 1200x630 in jpg).
"""
import html, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
sys.path.insert(0, os.path.join(ROOT, 'strumenti'))
from galleria_stand import GALLERIA  # altri stand realizzati (solo foto), negli hub
SITE = 'https://danovastand.com'
IMG = '/assets/img/lavori/'
e = html.escape

MODELLI = {'it': 'allestimento-mostre/index.html',
           'fr': 'fr/standiste-salon-italie/index.html',
           'en': 'en/exhibition-stand-builder-italy/index.html'}
LOCALE = {'it': 'it_IT', 'fr': 'fr_FR', 'en': 'en_US'}
HOME = {'it': '/', 'fr': '/fr/standiste-salon-italie/', 'en': '/en/exhibition-stand-builder-italy/'}
HUB = {'it': '/lavori/', 'fr': '/fr/realisations/', 'en': '/en/projects/'}

T = {  # testi fissi dell'interfaccia
    'it': dict(home='Home', hub='Lavori realizzati', foto='Foto di cantiere Danova Stand', faq='Domande frequenti',
               altri='Approfondisci', cliente='Cosa ha scritto il cliente', trad='Traduzione',
               apri='Guarda il lavoro', scheda='Il lavoro in breve', passi='Il montaggio, foto per foto',
               cta='Preventivo per un allestimento come questo', render='Progetti e render di stand'),
    'fr': dict(home='Accueil', hub='Réalisations', foto='Photo de chantier Danova Stand', faq='Questions fréquentes',
               altri='Pour aller plus loin', cliente='Ce que le client nous a écrit', trad='Traduction',
               apri='Voir la réalisation', scheda='La réalisation en bref', passi='Le montage, photo par photo',
               cta='Demander un devis pour un aménagement similaire', render='Stand de salon en Italie'),
    'en': dict(home='Home', hub='Projects', foto='Danova Stand site photo', faq='Frequently asked questions',
               altri='Read more', cliente='What the client wrote', trad='Translation',
               apri='See the project', scheda='The project at a glance', passi='The set-up, photo by photo',
               cta='Get a quote for a similar set-up', render='Exhibition stands in Italy'),
}

HUB_TXT = {
    'it': dict(title='Lavori realizzati: allestimenti con foto vere | Danova Stand',
               desc="Lavori realizzati da Danova Stand con foto vere: oltre 20 stand fieristici e padiglioni divisi per cliente, da MEDICA Düsseldorf all'Arsenale di Venezia.",
               eyebrow='Portfolio · foto di cantiere',
               h1='Lavori realizzati: <span class="grad">foto vere, non render</span>.',
               lead="Qui raccogliamo i lavori fatti, con le foto scattate in cantiere dalla nostra squadra: cosa ci è stato chiesto, cosa abbiamo montato, in quanto tempo e cosa ne pensa il cliente. Per le idee e i render di progetto c'è la pagina dei progetti.",
               testo=['Ogni scheda racconta un lavoro vero: dove e quando, cosa chiedeva il cliente, cosa abbiamo montato noi e cosa hanno fatto gli altri fornitori, i problemi incontrati in cantiere e come li abbiamo risolti. Le foto sono quelle scattate dalla squadra durante il montaggio, non render né immagini di catalogo.', 'Lavoriamo in fiera, negli spazi per eventi e nei luoghi più complicati da raggiungere, come Venezia, dove tutto arriva in barca. Se ti serve un allestimento simile a uno di questi, scrivici dove e quando: ti rispondiamo con un preventivo voce per voce entro 24 ore lavorative.'],
               breve="Danova Stand pubblica qui i lavori realizzati con foto reali di montaggio: allestimenti per eventi, spettacoli, fiere e mostre in Italia e in Europa. Ogni scheda indica luogo, date, lavorazioni eseguite e, quando il cliente lo permette, il suo commento."),
    'fr': dict(title='Nos réalisations : aménagements en photos | Danova Stand',
               desc="Réalisations Danova Stand en photos de chantier : salons et événements en Italie et à l'étranger, de MEDICA à Düsseldorf à l'Arsenal de Venise.",
               eyebrow='Portfolio · photos de chantier',
               h1='Nos réalisations : <span class="grad">de vraies photos, pas des rendus</span>.',
               lead="Nous rassemblons ici nos chantiers, avec les photos prises par notre équipe : la demande, ce que nous avons monté, en combien de temps et l'avis du client.",
               testo=["Chaque fiche raconte un vrai chantier : où et quand, la demande du client, ce que nous avons monté et ce qu'ont fait les autres prestataires, les difficultés rencontrées et comment nous les avons résolues. Les photos sont celles prises par notre équipe pendant le montage, pas des rendus ni des images de catalogue.", "Nous travaillons sur les salons, dans les lieux d'événements et dans les endroits les plus difficiles d'accès, comme Venise, où tout arrive en bateau. Pour un aménagement similaire, écrivez-nous le lieu et les dates : nous répondons par écrit dans votre langue avec un devis détaillé sous 24 heures ouvrées."],
               breve="Danova Stand publie ici ses réalisations avec de vraies photos de montage : aménagements d'événements, spectacles, salons et expositions en Italie et en Europe. Chaque fiche indique le lieu, les dates, les travaux réalisés et, quand le client l'accepte, son commentaire."),
    'en': dict(title='Our projects: real set-up photos | Danova Stand',
               desc='Projects by Danova Stand with real site photos: trade fair and event set-ups in Italy and abroad, from MEDICA Düsseldorf to the Venice Arsenale.',
               eyebrow='Portfolio · site photos',
               h1='Our projects: <span class="grad">real photos, not renders</span>.',
               lead='This is where we collect finished jobs, with photos taken on site by our crew: the brief, what we built, how long it took and what the client said.',
               testo=['Each case study describes a real job: where and when, what the client asked for, what we built and what other suppliers did, the problems we met on site and how we solved them. The photos are the ones our crew took during the set-up, not renders or catalogue images.', 'We work at trade fairs, at event venues and in places that are hard to reach, like Venice, where everything arrives by boat. If you need a similar set-up, tell us where and when: we reply in writing with an itemised quote within 24 working hours.'],
               breve='Danova Stand publishes its completed projects here with real set-up photos: event, show, trade fair and exhibition set-ups in Italy and Europe. Each case study lists the venue, the dates, the work carried out and, where the client agrees, their feedback.'),
}

# ---------------------------------------------------------------------------- lavori
CITAZIONE = ('A big thank you to you and your team. They are doing a great job on the stage, '
             'and I really appreciate how solution-oriented you all are. It makes a real difference for us.')

LAVORI = [{
    'id': 'venezia-arsenale-2026',
    'pubblicato': '2026-11-22',
    'url': {'it': '/lavori/palco-galleggiante-arsenale-venezia/',
            'fr': '/fr/realisations/scene-flottante-arsenal-venise/',
            'en': '/en/projects/floating-stage-venice-arsenale/'},
    'og': 'og-palco-galleggiante-arsenale-venezia.jpg',
    'hero': 'palco-galleggiante-arsenale-venezia-pannelli-neri',
    # (file, larghezza, altezza)
    'foto': [
        ('posizionamento-pontoni-darsena-arsenale-venezia', 1200, 1600),
        ('telaio-acciaio-raccordo-pontoni-arsenale', 1600, 1200),
        ('dettaglio-telaio-acciaio-pontone-galleggiante', 1600, 1200),
        ('raccordo-triangolare-multistrato-piattaforma-galleggiante', 1600, 900),
        ('palco-galleggiante-arsenale-venezia-pannelli-neri', 1600, 900),
        ('piattaforme-galleggianti-darsena-arsenale-venezia', 1600, 900),
    ],
    'citazione': CITAZIONE,
    'citazione_trad': {'it': "Un grande grazie a te e alla tua squadra. Stanno facendo un ottimo lavoro sul palco e apprezzo davvero quanto siate tutti orientati alle soluzioni. Per noi fa davvero la differenza.",
                       'fr': "Un grand merci à toi et à ton équipe. Ils font un excellent travail sur la scène et j'apprécie vraiment à quel point vous êtes tous orientés solutions. Cela fait vraiment la différence pour nous.",
                       'en': ''},
    'citazione_chi': {'it': "Organizzazione di The Heart in Art, cliente francese — email al nostro team, novembre 2026",
                      'fr': "Organisation de The Heart in Art, client français — e-mail à notre équipe, novembre 2026",
                      'en': "The Heart in Art organisers, French client — email to our team, November 2026"},
    'evento': 'The Heart in Art',
    'luogo': {'nome': {'it': 'Arsenale di Venezia', 'fr': 'Arsenal de Venise', 'en': 'Venice Arsenale'},
              'address': {'@type': 'PostalAddress', 'addressLocality': 'Venezia', 'addressRegion': 'VE', 'postalCode': '30122', 'addressCountry': 'IT'}},
    'about': {'it': 'Palco galleggiante', 'fr': 'Scène flottante', 'en': 'Floating stage'},
    'keywords': {'it': "palco galleggiante Venezia, allestimento eventi Venezia, Arsenale di Venezia, piattaforme galleggianti, moquette, pannelli neri lucidi, allestitore Venezia",
                 'fr': "scène flottante Venise, aménagement événementiel Venise, Arsenal de Venise, plateformes flottantes, moquette, standiste Italie",
                 'en': "floating stage Venice, event set-up Venice, Venice Arsenale, floating platforms, carpet, event contractor Italy"},
    # pagine che mostrano il riquadro "Lavoro recente" verso questo lavoro (vince il lavoro più recente)
    'link_in': [('allestimenti-fieristici-venezia/index.html', 'it'), ('allestimenti-eventi/index.html', 'it'),
                ('allestimenti-eventi-showroom-negozi/index.html', 'it'), ('progetti-stand-fieristici/index.html', 'it'),
                ('index.html', 'it'), ('fr/standiste-salon-italie/index.html', 'fr'), ('en/exhibition-stand-builder-italy/index.html', 'en')],
    'box': {'it': 'Guarda il palco galleggiante che abbiamo allestito all\'Arsenale di Venezia (novembre 2026), con le foto del montaggio.',
            'fr': 'Découvrez la scène flottante que nous avons aménagée à l\'Arsenal de Venise (novembre 2026), avec les photos du montage.',
            'en': 'See the floating stage we fitted out at the Venice Arsenale (November 2026), with photos of the set-up.'},
    'video': dict(file='spettacolo-luci-palco-galleggiante-arsenale-venezia', w=540, h=968, durata=32,
                  caricato='2026-11-22T12:00:00+01:00'),
    'it': dict(
        video_tit='Il palco acceso, la sera del 20 novembre',
        video_txt="32 secondi girati dalla riva: le luci dello spettacolo, la nebbia sull'acqua e il palco galleggiante con i lati neri lucidi che riflettono fasci e colori.",
        video_nome="Video: il palco galleggiante acceso all'Arsenale di Venezia",
        title="Palco galleggiante all'Arsenale di Venezia | Danova Stand",
        desc="Arsenale di Venezia, novembre 2026: per The Heart in Art abbiamo livellato, rivestito di moquette e chiuso con pannelli neri lucidi un palco galleggiante.",
        crumb="Palco galleggiante all'Arsenale di Venezia",
        card="Palco galleggiante per lo spettacolo di luci The Heart in Art, Arsenale di Venezia, novembre 2026.",
        eyebrow='Lavoro realizzato · Venezia · novembre 2026',
        h1="Palco galleggiante all'Arsenale di Venezia per <span class=\"grad\">The Heart in Art</span>.",
        lead="Uno spettacolo di luci sull'acqua, nella darsena dell'Arsenale, per un cliente francese. Noi abbiamo trasformato le piattaforme galleggianti in un palco unico: piano livellato, moquette ovunque e lati in nero lucido che riflettono le luci.",
        breve="Il 19 e 20 novembre 2026 Danova Stand ha allestito il palco galleggiante di The Heart in Art, spettacolo di luci nella darsena dell'Arsenale di Venezia, per un cliente francese. Sulle piattaforme galleggianti già posizionate e collegate abbiamo livellato con pannelli di multistrato il raccordo triangolare in acciaio fra i moduli, steso la moquette su tutte le piattaforme e chiuso i lati con pannelli neri lucidi, scelti per riflettere il gioco di luci dello spettacolo. Due giorni di montaggio, in parte sotto la pioggia, con il cliente molto soddisfatto del risultato.",
        hero_alt="Palco galleggiante nella darsena dell'Arsenale di Venezia con pannelli laterali neri lucidi, barre LED e teste mobili, visto da una barca",
        hero_cap="Il palco finito visto dalla barca: lati in nero lucido, sopra le barre LED e le teste mobili dello spettacolo.",
        scheda=[('Dove', "Arsenale di Venezia, darsena accanto alla storica gru idraulica"),
                ('Quando', 'Montaggio il 19 e 20 novembre 2026'),
                ('Evento', 'The Heart in Art, spettacolo di luci sull\'acqua'),
                ('Cliente', 'Organizzatore francese'),
                ('Cosa abbiamo fatto', 'Livellamento in multistrato, moquette, pannelli laterali neri lucidi')],
        foto=[("Piattaforme galleggianti in posizione nella darsena dell'Arsenale di Venezia, nella nebbia, con operai e barca di servizio",
               'Le piattaforme in darsena', "Nei giorni prima del nostro intervento le piattaforme galleggianti vengono portate in posizione e ancorate nella darsena."),
              ("Telaio triangolare in acciaio che unisce due piattaforme galleggianti, sullo sfondo il pontone gru Boscolo Bielo",
               'Il raccordo in acciaio', "Due moduli si incontrano ad angolo: in mezzo resta un telaio triangolare in acciaio, senza piano di calpestio."),
              ("Dettaglio del telaio in acciaio fissato al pontone galleggiante, con l'Arsenale di Venezia sullo sfondo",
               'Il punto da risolvere', "Il telaio collega le piattaforme ma lascia un vuoto e un dislivello: per un palco serve un piano unico."),
              ("Raccordo triangolare chiuso con pannelli di multistrato tagliati su misura, a livello delle piattaforme galleggianti",
               'Livellamento in multistrato', "Abbiamo chiuso il triangolo con pannelli di multistrato tagliati su misura, a filo delle piattaforme: un solo piano continuo."),
              ("Palco galleggiante finito con pannelli laterali neri lucidi, moquette e impianto luci, Arsenale di Venezia",
               'Moquette e lati neri lucidi', "Moquette su tutte le piattaforme e pannelli neri lucidi sui lati, che sull'acqua riflettono le luci dello spettacolo."),
              ("Vista d'insieme delle piattaforme galleggianti con l'impianto luci nella darsena dell'Arsenale di Venezia e la gru storica",
               'Pronto per lo spettacolo', "Il palco finito nella darsena, con le altre piattaforme luci e la gru dell'Arsenale sullo sfondo.")],
        testo_title="Perché <span class=\"grad\">nero lucido</span>",
        testo=["Lo spettacolo era tutto giocato sulla luce. Un fianco grezzo o chiaro avrebbe spezzato la scena; il nero lucido invece sparisce al buio e restituisce i riflessi delle teste mobili e delle barre LED, che si sommano a quelli sull'acqua.",
               "Prima della finitura bisognava però risolvere il piano: le piattaforme galleggianti erano unite ad angolo da un telaio triangolare in acciaio. Lo abbiamo chiuso con multistrato tagliato su misura, alla stessa quota dei moduli, così chi sale sul palco cammina su una superficie unica, senza gradini né fessure, e la moquette corre continua da un capo all'altro."],
        testo2_title="Due giorni di montaggio, <span class=\"grad\">anche sotto la pioggia</span>",
        testo2=["A Venezia si lavora con quello che c'è: materiali che arrivano in barca, spazi stretti, tempi fissati dallo spettacolo. Durante il montaggio è arrivata anche la pioggia, e abbiamo comunque consegnato il palco finito nei tempi previsti.",
                 "Per un allestimento sull'acqua la sequenza conta: prima il piano, poi la moquette, poi i pannelli laterali, infine il passaggio al service luci. Ogni fase deve essere chiusa prima della successiva, perché dalla barca non si torna indietro facilmente."],
        faq=[("Realizzate allestimenti su palchi e piattaforme galleggianti a Venezia?",
              "Sì. All'Arsenale di Venezia, a novembre 2026, abbiamo allestito il palco galleggiante dello spettacolo The Heart in Art: livellamento dei raccordi in multistrato, moquette e pannellatura laterale nera lucida. Organizziamo il lavoro in funzione dei trasporti via acqua."),
             ("Lavorate per clienti stranieri e organizzatori di eventi?",
              "Sì: questo lavoro era per un cliente francese. Seguiamo organizzatori ed espositori esteri in Italia: rispondiamo per iscritto in tutte le lingue e al telefono parliamo italiano, inglese e rumeno."),
             ("Quanto tempo serve per allestire un palco galleggiante?",
              "In questo caso due giorni di montaggio per livellamento, moquette e pannelli laterali, su piattaforme già posizionate. I tempi dipendono da superficie, accessi via acqua, meteo e finiture richieste."),
             ("Si può montare anche con la pioggia?",
              "Sì, con le dovute precauzioni: a Venezia abbiamo lavorato in parte sotto la pioggia e consegnato il palco nei tempi. Le finiture si posano a superficie asciutta, per questo pianifichiamo un margine sul calendario.")],
        altri=[('/allestimenti-fieristici-venezia/', 'Allestimenti a Venezia'),
               ('/allestimenti-eventi/', 'Allestimenti per eventi e congressi'),
               ('/moquette-per-stand-fieristici/', 'Moquette per stand ed eventi'),
               ('/montaggio-stand-fieristici/', 'Montaggio e smontaggio'),
               ('/ledwall-e-illuminazione-stand/', 'Illuminazione e ledwall'),
               ('/lavori/', 'Tutti i lavori realizzati')],
    ),
    'fr': dict(
        video_tit='La scène allumée, le soir du 20 novembre',
        video_txt="32 secondes filmées depuis le quai : les lumières du spectacle, la brume sur l'eau et la scène flottante aux côtés noirs brillants qui reflètent faisceaux et couleurs.",
        video_nome="Vidéo : la scène flottante allumée à l'Arsenal de Venise",
        title="Scène flottante à l'Arsenal de Venise | Danova Stand",
        desc="Arsenal de Venise, novembre 2026 : pour le spectacle The Heart in Art, nous avons nivelé, moquetté et habillé de panneaux noirs brillants une scène flottante.",
        crumb="Scène flottante à l'Arsenal de Venise",
        card="Scène flottante pour le spectacle de lumières The Heart in Art, Arsenal de Venise, novembre 2026.",
        eyebrow='Réalisation · Venise · novembre 2026',
        h1="Scène flottante à l'Arsenal de Venise pour <span class=\"grad\">The Heart in Art</span>.",
        lead="Un spectacle de lumières sur l'eau, dans la darse de l'Arsenal, pour un client français. Nous avons transformé les plateformes flottantes en une scène unique : plancher mis à niveau, moquette partout et côtés noirs brillants qui reflètent les lumières.",
        breve="Les 19 et 20 novembre 2026, Danova Stand a aménagé la scène flottante de The Heart in Art, spectacle de lumières dans la darse de l'Arsenal de Venise, pour un client français. Sur les plateformes flottantes déjà positionnées et reliées, nous avons mis à niveau avec des panneaux de contreplaqué la jonction triangulaire en acier entre les modules, posé la moquette sur toutes les plateformes et habillé les côtés de panneaux noirs brillants, choisis pour refléter les jeux de lumière du spectacle. Deux jours de montage, en partie sous la pluie, et un client très satisfait.",
        hero_alt="Scène flottante dans la darse de l'Arsenal de Venise avec panneaux latéraux noirs brillants, barres LED et lyres, vue depuis un bateau",
        hero_cap="La scène terminée vue du bateau : côtés noirs brillants, barres LED et lyres du spectacle.",
        scheda=[('Lieu', "Arsenal de Venise, darse près de l'ancienne grue hydraulique"),
                ('Dates', 'Montage les 19 et 20 novembre 2026'),
                ('Événement', "The Heart in Art, spectacle de lumières sur l'eau"),
                ('Client', 'Organisateur français'),
                ('Nos travaux', 'Mise à niveau en contreplaqué, moquette, panneaux latéraux noirs brillants')],
        foto=[("Plateformes flottantes en place dans la darse de l'Arsenal de Venise, dans le brouillard, avec techniciens et bateau de service",
               'Les plateformes dans la darse', "Avant notre intervention, les plateformes flottantes sont amenées et ancrées dans la darse."),
              ("Cadre triangulaire en acier reliant deux plateformes flottantes, avec le ponton-grue Boscolo Bielo en arrière-plan",
               'La jonction en acier', "Deux modules se rejoignent en angle : entre eux, un cadre triangulaire en acier, sans plancher."),
              ("Détail du cadre en acier fixé au ponton flottant, avec l'Arsenal de Venise en arrière-plan",
               'Le point à résoudre', "Le cadre relie les plateformes mais laisse un vide et un dénivelé : une scène demande un plancher continu."),
              ("Jonction triangulaire fermée par des panneaux de contreplaqué découpés sur mesure, au niveau des plateformes flottantes",
               'Mise à niveau en contreplaqué', "Nous avons fermé le triangle avec du contreplaqué découpé sur mesure, à fleur des plateformes : un seul plancher."),
              ("Scène flottante terminée avec panneaux latéraux noirs brillants, moquette et éclairage, Arsenal de Venise",
               'Moquette et côtés noirs brillants', "Moquette sur toutes les plateformes et panneaux noirs brillants sur les côtés, qui reflètent les lumières sur l'eau."),
              ("Vue d'ensemble des plateformes flottantes éclairées dans la darse de l'Arsenal de Venise, avec la grue historique",
               'Prête pour le spectacle', "La scène terminée dans la darse, avec les autres plateformes lumière et la grue de l'Arsenal.")],
        testo_title="Pourquoi <span class=\"grad\">le noir brillant</span>",
        testo=["Tout le spectacle reposait sur la lumière. Un côté brut ou clair aurait cassé la scène ; le noir brillant disparaît dans l'obscurité et renvoie les reflets des lyres et des barres LED, qui s'ajoutent à ceux de l'eau.",
               "Avant la finition, il fallait régler le plancher : les plateformes flottantes étaient reliées en angle par un cadre triangulaire en acier. Nous l'avons fermé avec du contreplaqué découpé sur mesure, à la même hauteur que les modules : on marche sur une surface unique, sans marche ni fente, et la moquette court d'un bout à l'autre."],
        testo2_title="Deux jours de montage, <span class=\"grad\">même sous la pluie</span>",
        testo2=["À Venise, on travaille avec les contraintes du lieu : matériel livré en bateau, espaces réduits, calendrier fixé par le spectacle. La pluie est arrivée pendant le montage et nous avons tout de même livré la scène dans les délais.",
                 "Sur l'eau, l'ordre des opérations compte : d'abord le plancher, puis la moquette, puis les panneaux latéraux, enfin le passage à l'équipe lumière. Chaque étape doit être terminée avant la suivante."],
        faq=[("Réalisez-vous des aménagements de scènes et plateformes flottantes à Venise ?",
              "Oui. À l'Arsenal de Venise, en novembre 2026, nous avons aménagé la scène flottante du spectacle The Heart in Art : mise à niveau des jonctions en contreplaqué, moquette et habillage latéral noir brillant. Nous organisons le chantier en fonction du transport par voie d'eau."),
             ("Travaillez-vous pour des organisateurs d'événements étrangers ?",
              "Oui : ce chantier était pour un client français. Nous accompagnons des organisateurs et exposants étrangers en Italie : nous répondons par écrit dans toutes les langues, y compris en français, et au téléphone en italien, anglais et roumain."),
             ("Combien de temps faut-il pour aménager une scène flottante ?",
              "Ici, deux jours de montage pour la mise à niveau, la moquette et les panneaux latéraux, sur des plateformes déjà en place. Les délais dépendent de la surface, des accès par l'eau, de la météo et des finitions."),
             ("Peut-on monter sous la pluie ?",
              "Oui, avec les précautions nécessaires : à Venise nous avons travaillé en partie sous la pluie et livré la scène à temps. Les finitions se posent sur surface sèche, c'est pourquoi nous prévoyons une marge.")],
        altri=[('/fr/standiste-salon-italie/', 'Standiste et aménagements en Italie'),
               ('/fr/realisations/', 'Toutes nos réalisations'),
               ('/fr/contact/', 'Contact')],
    ),
    'en': dict(
        video_tit='The stage lit up, on the evening of 20 November',
        video_txt='32 seconds filmed from the quay: the show lighting, haze on the water and the floating stage with glossy black sides reflecting beams and colours.',
        video_nome='Video: the floating stage lit up at the Venice Arsenale',
        title='Floating stage at the Venice Arsenale | Danova Stand',
        desc='Venice Arsenale, November 2026: for the light show The Heart in Art we levelled, carpeted and clad a floating stage in glossy black panels for a French client.',
        crumb='Floating stage at the Venice Arsenale',
        card='Floating stage for the light show The Heart in Art, Venice Arsenale, November 2026.',
        eyebrow='Case study · Venice · November 2026',
        h1='Floating stage at the Venice Arsenale for <span class="grad">The Heart in Art</span>.',
        lead='A light show on the water, in the basin of the Arsenale, for a French client. We turned the floating platforms into one stage: a level deck, carpet throughout and glossy black sides that reflect the lights.',
        breve='On 19 and 20 November 2026 Danova Stand fitted out the floating stage for The Heart in Art, a light show in the basin of the Venice Arsenale, for a French client. On floating platforms already moored and connected, we levelled the triangular steel joint between the modules with plywood panels, laid carpet on every platform and clad the sides in glossy black panels chosen to reflect the show lighting. Two days on site, partly in the rain, and a very satisfied client.',
        hero_alt='Floating stage in the basin of the Venice Arsenale with glossy black side panels, LED bars and moving heads, seen from a boat',
        hero_cap='The finished stage seen from the boat: glossy black sides, LED bars and moving heads for the show.',
        scheda=[('Venue', 'Venice Arsenale, basin next to the historic hydraulic crane'),
                ('Dates', 'Set-up on 19 and 20 November 2026'),
                ('Event', 'The Heart in Art, a light show on the water'),
                ('Client', 'French event organiser'),
                ('Our work', 'Plywood levelling, carpet, glossy black side panels')],
        foto=[('Floating platforms moored in the basin of the Venice Arsenale in the fog, with crew and a service boat',
               'Platforms in the basin', 'Before our work, the floating platforms are brought in and moored in the basin.'),
              ('Triangular steel frame joining two floating platforms, with the Boscolo Bielo crane pontoon behind',
               'The steel joint', 'Two modules meet at an angle, leaving a triangular steel frame with no deck in between.'),
              ('Close-up of the steel frame fixed to the floating pontoon, with the Venice Arsenale behind',
               'The problem to solve', 'The frame connects the platforms but leaves a gap and a step: a stage needs one continuous deck.'),
              ('Triangular joint closed with made-to-measure plywood panels, flush with the floating platforms',
               'Plywood levelling', 'We closed the triangle with made-to-measure plywood, flush with the platforms: one continuous deck.'),
              ('Finished floating stage with glossy black side panels, carpet and lighting, Venice Arsenale',
               'Carpet and glossy black sides', 'Carpet on every platform and glossy black panels on the sides, reflecting the show lighting on the water.'),
              ('Wide view of the lit floating platforms in the basin of the Venice Arsenale, with the historic crane',
               'Ready for the show', 'The finished stage in the basin, with the other lighting platforms and the Arsenale crane behind.')],
        testo_title='Why <span class="grad">glossy black</span>',
        testo=['The whole show was about light. A raw or pale side would have broken the scene; glossy black disappears in the dark and gives back the reflections of the moving heads and LED bars, adding to those on the water.',
               'Before the finish, the deck had to be solved: the floating platforms were joined at an angle by a triangular steel frame. We closed it with made-to-measure plywood at the same height as the modules, so performers walk on one surface with no steps or gaps, and the carpet runs from end to end.'],
        testo2_title='Two days on site, <span class="grad">rain included</span>',
        testo2=['In Venice you work with what the city gives you: materials delivered by boat, tight spaces and a schedule set by the show. It rained during the set-up and we still handed over the finished stage on time.',
                 'On the water the sequence matters: deck first, then carpet, then side panels, then hand-over to the lighting crew. Each step has to be finished before the next one starts.'],
        faq=[('Do you fit out floating stages and platforms in Venice?',
              'Yes. In November 2026 at the Venice Arsenale we fitted out the floating stage for The Heart in Art: plywood levelling of the joints, carpet and glossy black side cladding. We plan the work around transport by water.'),
             ('Do you work for foreign event organisers?',
              'Yes: this project was for a French client. We support foreign organisers and exhibitors in Italy: we reply in writing in any language, and on the phone we speak Italian, English and Romanian.'),
             ('How long does it take to fit out a floating stage?',
              'Here, two days of set-up for levelling, carpet and side panels on platforms already in place. Timing depends on the area, access by water, weather and the finishes required.'),
             ('Can you work in the rain?',
              'Yes, with the right precautions: in Venice we worked partly in the rain and delivered on time. Finishes are laid on dry surfaces, so we always plan some slack in the schedule.')],
        altri=[('/en/exhibition-stand-builder-italy/', 'Exhibition stand builder in Italy'),
               ('/en/projects/', 'All projects'),
               ('/en/contact/', 'Contact')],
    ),
}]

# MEDICA 2026: collettiva nazionale della Tunisia (inserito in cima: i lavori vanno dal più recente)
LAVORI.insert(0, {
    'id': 'medica-tunisia-2026',
    'pubblicato': '2026-11-23',
    'url': {'it': '/lavori/padiglione-tunisia-medica-dusseldorf/',
            'fr': '/fr/realisations/pavillon-tunisie-medica-dusseldorf/',
            'en': '/en/projects/tunisia-pavilion-medica-dusseldorf/'},
    'og': 'og-padiglione-tunisia-medica-2026.jpg',
    'hero': 'padiglione-tunisia-medica-2026-dusseldorf',   # composizione 1600x900 di due foto verticali
    'foto': [
        ('stand-bioservice-tunisie-collettiva-tunisia-medica-2026', 1200, 1600),
        ('stand-medika-hitex-padiglione-tunisia-medica', 1200, 1600),
        ('stand-alberton-medical-padiglione-tunisia-medica', 1200, 1600),
        ('stand-pec-mi-padiglione-tunisia-medica', 1200, 1600),
        ('lounge-tunisia-export-cepex-medica-dusseldorf', 1200, 1600),
    ],
    'evento': 'MEDICA 2026',
    'luogo': {'nome': {'it': 'Messe Düsseldorf', 'fr': 'Parc des expositions de Düsseldorf', 'en': 'Messe Düsseldorf'},
              'address': {'@type': 'PostalAddress', 'streetAddress': 'Stockumer Kirchstraße 61', 'addressLocality': 'Düsseldorf',
                          'postalCode': '40474', 'addressCountry': 'DE'}},
    'about': {'it': 'Padiglione nazionale della Tunisia', 'fr': 'Pavillon national de la Tunisie', 'en': 'Tunisia national pavilion'},
    'keywords': {'it': "stand MEDICA Düsseldorf, padiglione Tunisia MEDICA 2026, collettiva nazionale fiera, stand settore medicale, allestimenti fieristici Germania, allestitore fiere estero",
                 'fr': "stand MEDICA Düsseldorf, pavillon Tunisie MEDICA 2026, pavillon national salon, stand dispositifs médicaux, standiste Allemagne, standiste salons à l'étranger",
                 'en': "MEDICA Düsseldorf stand, Tunisia pavilion MEDICA 2026, national pavilion trade fair, medical device exhibition stand, stand builder Germany"},
    'link_in': [('stand-medica/index.html', 'it'), ('allestimenti-fieristici-germania/index.html', 'it'),
                ('allestimenti-fieristici-estero/index.html', 'it'), ('progetti-stand-fieristici/index.html', 'it'),
                ('index.html', 'it'), ('fr/standiste-salon-italie/index.html', 'fr'),
                ('en/exhibition-stand-builder-italy/index.html', 'en'), ('en/medica-stand-builder/index.html', 'en'),
                ('en/exhibition-stand-builder-europe/index.html', 'en')],
    'box': {'it': 'Guarda il padiglione della Tunisia che abbiamo allestito a MEDICA 2026 a Düsseldorf: più aziende, un\'unica immagine.',
            'fr': 'Découvrez le pavillon de la Tunisie que nous avons aménagé à MEDICA 2026 à Düsseldorf : plusieurs entreprises, une seule image.',
            'en': 'See the Tunisia pavilion we built at MEDICA 2026 in Düsseldorf: several companies, one identity.'},
    'it': dict(
        title='Padiglione Tunisia a MEDICA 2026 Düsseldorf | Danova Stand',
        desc="MEDICA 2026, Düsseldorf: abbiamo allestito la collettiva della Tunisia, con anello luminoso sospeso, uno stand per ogni azienda e la lounge di Tunisia Export.",
        crumb='Padiglione Tunisia a MEDICA 2026',
        card='Collettiva nazionale della Tunisia a MEDICA 2026, Düsseldorf: più aziende del medicale sotto un unico anello luminoso.',
        eyebrow='Lavoro realizzato · Düsseldorf · novembre 2026',
        h1='Il padiglione della Tunisia a <span class="grad">MEDICA 2026</span>, Düsseldorf.',
        lead="Una collettiva nazionale alla più grande fiera del medicale: più aziende tunisine, ognuna con il proprio stand, riunite sotto un'unica immagine. Il segno che si vede da lontano è l'anello luminoso sospeso con il marchio «Tunisia — Your health… Yes We Care».",
        breve="Per MEDICA 2026 (Messe Düsseldorf, 16-19 novembre 2026) Danova Stand ha allestito il padiglione collettivo della Tunisia: un'area aperta su più lati e divisa in stand per singole aziende del settore medicale, tra cui Bioservice Tunisie, PEC MI, Medika Hitex e Alberton Medical, più la lounge di Tunisia Export. Sopra il padiglione un anello sospeso in tessuto retroilluminato con il marchio del paese; a terra una pedana con pavimento effetto legno e profilo LED; per ogni azienda colonna rossa con il nome, pareti bianche, grafica retroilluminata, mensole illuminate e vetrine.",
        hero_alt="Padiglione della Tunisia a MEDICA 2026 Düsseldorf: anello luminoso sospeso con il marchio Tunisia sopra gli stand di Bioservice Tunisie e Medika Hitex",
        hero_cap="Due lati del padiglione: a sinistra lo stand Bioservice Tunisie, a destra Medika Hitex con i primi visitatori; sopra, l'anello luminoso sospeso.",
        scheda=[('Dove', 'Messe Düsseldorf, Germania'),
                ('Quando', 'MEDICA 2026, dal 16 al 19 novembre 2026'),
                ('Progetto', 'Collettiva nazionale della Tunisia, settore dispositivi medici'),
                ('Espositori', 'Bioservice Tunisie, PEC MI, Medika Hitex, Alberton Medical, Tunisia Export'),
                ('Cosa abbiamo fatto', 'Stand per ogni azienda, anello luminoso sospeso, pedana con LED, vetrine, arredi e luci')],
        passi='Il padiglione, stand per stand',
        foto=[("Stand Bioservice Tunisie nel padiglione Tunisia a MEDICA 2026: grafiche retroilluminate, mensole illuminate, sacche mediche esposte a parete e banco vetrina",
               'Bioservice Tunisie', "Angolo aperto su due lati: banco vetrina illuminato, colonna in vetro, grafiche retroilluminate e prodotti appesi a parete su barre cromate."),
              ("Stand Medika Hitex al padiglione Tunisia di MEDICA 2026 con visitatori al tavolo, grafiche retroilluminate e vetrina a colonna",
               'Medika Hitex', "Due grafiche retroilluminate, tavolo e sgabelli per gli incontri, vetrina a colonna illuminata per i prodotti."),
              ("Stand Alberton Medical al padiglione Tunisia di MEDICA 2026 con banco vetrina illuminato e portadepliant, durante l'allestimento",
               'Alberton Medical', "Banco vetrina con LED e portadepliant, grafica retroilluminata e colonna rossa con il nome: lo stesso schema degli altri stand, adattato all'azienda."),
              ("Stand PEC MI nel padiglione Tunisia a MEDICA 2026 durante l'allestimento, con vetrina a colonna e mensole illuminate",
               'PEC MI, a fine montaggio', "Le ultime ore prima dell'apertura: mensole con LED già accese, vetrine pronte e l'espositore che sistema i prodotti."),
              ("Area lounge di Tunisia Export (CEPEX) nel padiglione Tunisia a MEDICA 2026, con poltroncine, schermo e pannelli retroilluminati",
               'La lounge di Tunisia Export', "Lo spazio istituzionale per gli incontri: due pannelli retroilluminati, schermo a parete, poltroncine e tavolini, ancora con la plastica poco prima dell'apertura.")],
        testo_title='Un padiglione, <span class="grad">più aziende</span>',
        testo=["In una collettiva nazionale ogni azienda vuole il suo spazio, ma il visitatore deve capire a colpo d'occhio di trovarsi nel padiglione di un paese. Per questo abbiamo ripetuto lo stesso schema in ogni stand: colonna rossa con la grafica a icone mediche e la targa con il nome dell'azienda, pareti bianche, una grafica retroilluminata con i contenuti dell'espositore.",
               "Dentro ogni stand cambia solo ciò che serve all'azienda: barre cromate per appendere i prodotti, mensole illuminate nelle nicchie, vetrine a colonna o banchi vetrina con portadepliant, tavolo e sedute per gli incontri e, dove serve, un ripostiglio con porta per scorte e borse."],
        testo2_title="L'anello luminoso <span class=\"grad\">sopra il padiglione</span>",
        testo2=["A MEDICA gli espositori sono migliaia: serviva un segno visibile da lontano. L'anello sospeso, in tessuto retroilluminato, porta il marchio «Tunisia — Your health… Yes We Care» e la bandiera su più lati, così il padiglione si riconosce dalle corsie intorno.",
                "A terra la pedana con pavimento effetto legno e profilo in alluminio con LED delimita lo spazio e lega fra loro gli stand. In una fiera all'estero tutto va preparato prima della partenza: grafiche, arredi e illuminazione arrivano pronti per il montaggio."],
        faq=[("Allestite stand e padiglioni a MEDICA Düsseldorf?",
              "Sì. A MEDICA 2026 (16-19 novembre) abbiamo allestito il padiglione collettivo della Tunisia, con uno stand per ogni azienda del medicale e la lounge di Tunisia Export. Seguiamo progetto, produzione, trasporto e montaggio anche in Germania."),
             ("Realizzate padiglioni nazionali e collettive con più espositori?",
              "Sì: definiamo uno schema comune (identità del paese, insegna sospesa, pedana, colori) e lo adattiamo a ogni azienda con grafiche, vetrine ed esposizione dei prodotti. Ogni espositore ha il suo stand, il visitatore vede un unico padiglione."),
             ("Lavorate con enti e aziende straniere?",
              "Sì: questo padiglione era per aziende tunisine. Rispondiamo per iscritto in tutte le lingue, anche in francese e arabo; al telefono parliamo italiano, inglese e rumeno."),
             ("Cosa comprende un allestimento chiavi in mano per una fiera all'estero?",
              "Progetto, strutture e pareti, grafiche, illuminazione, arredi e vetrine, trasporto, montaggio e smontaggio, con un unico referente. Il preventivo è voce per voce, così si vede cosa è compreso.")],
        altri=[('/stand-medica/', 'Stand per MEDICA Düsseldorf'),
               ('/allestimenti-fieristici-germania/', 'Allestimenti fieristici in Germania'),
               ('/allestimenti-fieristici-estero/', 'Allestimenti per fiere all\'estero'),
               ('/stand-a-isola/', 'Stand a isola'),
               ('/ledwall-e-illuminazione-stand/', 'Illuminazione e ledwall'),
               ('/lavori/', 'Tutti i lavori realizzati')],
    ),
    'fr': dict(
        title='Pavillon Tunisie à MEDICA 2026 Düsseldorf | Danova Stand',
        desc="MEDICA 2026, Düsseldorf : nous avons aménagé le pavillon de la Tunisie, avec anneau lumineux suspendu, un stand par entreprise et le salon de Tunisia Export.",
        crumb='Pavillon Tunisie à MEDICA 2026',
        card='Pavillon national de la Tunisie à MEDICA 2026, Düsseldorf : plusieurs entreprises du médical sous un même anneau lumineux.',
        eyebrow='Réalisation · Düsseldorf · novembre 2026',
        h1='Le pavillon de la Tunisie à <span class="grad">MEDICA 2026</span>, Düsseldorf.',
        lead="Un pavillon national au plus grand salon du médical : plusieurs entreprises tunisiennes, chacune avec son stand, réunies sous une seule image. Le signal visible de loin, c'est l'anneau lumineux suspendu à la marque « Tunisia — Your health… Yes We Care ».",
        breve="Pour MEDICA 2026 (Messe Düsseldorf, du 16 au 19 novembre 2026), Danova Stand a aménagé le pavillon collectif de la Tunisie : un espace ouvert sur plusieurs côtés, divisé en stands pour des entreprises du secteur médical, dont Bioservice Tunisie, PEC MI, Medika Hitex et Alberton Medical, ainsi que le salon de Tunisia Export. Au-dessus, un anneau suspendu en tissu rétroéclairé à la marque du pays ; au sol, une estrade au plancher effet bois avec profil LED ; pour chaque entreprise, une colonne rouge avec son nom, des cloisons blanches, un visuel rétroéclairé, des étagères éclairées et des vitrines.",
        hero_alt="Pavillon de la Tunisie à MEDICA 2026 Düsseldorf : anneau lumineux suspendu à la marque Tunisia au-dessus des stands Bioservice Tunisie et Medika Hitex",
        hero_cap="Deux côtés du pavillon : à gauche le stand Bioservice Tunisie, à droite Medika Hitex avec les premiers visiteurs ; au-dessus, l'anneau lumineux suspendu.",
        scheda=[('Lieu', 'Messe Düsseldorf, Allemagne'),
                ('Dates', 'MEDICA 2026, du 16 au 19 novembre 2026'),
                ('Projet', 'Pavillon national de la Tunisie, dispositifs médicaux'),
                ('Exposants', 'Bioservice Tunisie, PEC MI, Medika Hitex, Alberton Medical, Tunisia Export'),
                ('Nos travaux', 'Un stand par entreprise, anneau lumineux suspendu, estrade avec LED, vitrines, mobilier et éclairage')],
        passi='Le pavillon, stand par stand',
        foto=[("Stand Bioservice Tunisie dans le pavillon Tunisie à MEDICA 2026 : visuels rétroéclairés, étagères éclairées, poches médicales exposées au mur et comptoir vitrine",
               'Bioservice Tunisie', "Angle ouvert sur deux côtés : comptoir vitrine éclairé, colonne vitrée, visuels rétroéclairés et produits suspendus au mur sur barres chromées."),
              ("Stand Medika Hitex au pavillon Tunisie de MEDICA 2026 avec visiteurs à table, visuels rétroéclairés et vitrine colonne",
               'Medika Hitex', "Deux visuels rétroéclairés, table et tabourets pour les rendez-vous, vitrine colonne éclairée pour les produits."),
              ("Stand Alberton Medical au pavillon Tunisie de MEDICA 2026 avec comptoir vitrine éclairé et porte-brochures, pendant le montage",
               'Alberton Medical', "Comptoir vitrine avec LED et porte-brochures, visuel rétroéclairé et colonne rouge au nom de l'entreprise : le même schéma que les autres stands, adapté à l'exposant."),
              ("Stand PEC MI dans le pavillon Tunisie à MEDICA 2026 pendant le montage, avec vitrine colonne et étagères éclairées",
               'PEC MI, fin de montage', "Les dernières heures avant l'ouverture : étagères LED déjà allumées, vitrines prêtes et l'exposant qui installe ses produits."),
              ("Salon de Tunisia Export (CEPEX) dans le pavillon Tunisie à MEDICA 2026, avec fauteuils, écran et panneaux rétroéclairés",
               'Le salon de Tunisia Export', "L'espace institutionnel pour les rendez-vous : deux panneaux rétroéclairés, écran mural, fauteuils et tables basses, encore sous plastique juste avant l'ouverture.")],
        testo_title='Un pavillon, <span class="grad">plusieurs entreprises</span>',
        testo=["Dans un pavillon national, chaque entreprise veut son espace, mais le visiteur doit comprendre d'un coup d'œil qu'il est dans le pavillon d'un pays. Nous avons donc répété le même schéma dans chaque stand : colonne rouge au motif d'icônes médicales avec le nom de l'entreprise, cloisons blanches et un visuel rétroéclairé avec les contenus de l'exposant.",
               "À l'intérieur, seul change ce dont l'entreprise a besoin : barres chromées pour suspendre les produits, étagères éclairées dans les niches, vitrines colonnes ou comptoirs vitrines avec porte-brochures, table et assises pour les rendez-vous et, si besoin, une réserve fermée pour le stock et les bagages."],
        testo2_title="L'anneau lumineux <span class=\"grad\">au-dessus du pavillon</span>",
        testo2=["À MEDICA, les exposants se comptent par milliers : il fallait un signal visible de loin. L'anneau suspendu, en tissu rétroéclairé, porte la marque « Tunisia — Your health… Yes We Care » et le drapeau sur plusieurs côtés, pour que le pavillon se repère depuis les allées voisines.",
                "Au sol, l'estrade au plancher effet bois et au profil aluminium avec LED délimite l'espace et relie les stands entre eux. Pour un salon à l'étranger, tout se prépare avant le départ : visuels, mobilier et éclairage arrivent prêts à monter."],
        faq=[("Aménagez-vous des stands et pavillons à MEDICA Düsseldorf ?",
              "Oui. À MEDICA 2026 (16-19 novembre), nous avons aménagé le pavillon collectif de la Tunisie, avec un stand par entreprise du médical et le salon de Tunisia Export. Nous gérons conception, fabrication, transport et montage, y compris en Allemagne."),
             ("Réalisez-vous des pavillons nationaux avec plusieurs exposants ?",
              "Oui : nous définissons un schéma commun (identité du pays, enseigne suspendue, estrade, couleurs) puis nous l'adaptons à chaque entreprise avec visuels, vitrines et présentation des produits. Chaque exposant a son stand, le visiteur voit un seul pavillon."),
             ("Travaillez-vous avec des organismes et entreprises étrangers ?",
              "Oui : ce pavillon réunissait des entreprises tunisiennes. Nous répondons par écrit dans toutes les langues, y compris en français et en arabe ; au téléphone, nous parlons italien, anglais et roumain."),
             ("Que comprend un stand clés en main pour un salon à l'étranger ?",
              "Conception, structures et cloisons, visuels, éclairage, mobilier et vitrines, transport, montage et démontage, avec un seul interlocuteur. Le devis est détaillé poste par poste.")],
        altri=[('/fr/standiste-salon-italie/', 'Standiste et aménagements en Italie'),
               ('/fr/realisations/', 'Toutes nos réalisations'),
               ('/fr/contact/', 'Contact')],
    ),
    'en': dict(
        title='Tunisia pavilion at MEDICA 2026 Düsseldorf | Danova Stand',
        desc='MEDICA 2026, Düsseldorf: we built the Tunisia national pavilion, with a suspended light ring, a stand for each company and the Tunisia Export lounge.',
        crumb='Tunisia pavilion at MEDICA 2026',
        card='Tunisia national pavilion at MEDICA 2026, Düsseldorf: several medical companies under one light ring.',
        eyebrow='Case study · Düsseldorf · November 2026',
        h1='The Tunisia pavilion at <span class="grad">MEDICA 2026</span>, Düsseldorf.',
        lead='A national pavilion at the largest medical trade fair: several Tunisian companies, each with its own stand, brought together under one identity. The sign you see from afar is the suspended light ring branded “Tunisia — Your health… Yes We Care”.',
        breve='For MEDICA 2026 (Messe Düsseldorf, 16-19 November 2026) Danova Stand built the Tunisia national pavilion: an area open on several sides and divided into stands for individual medical companies, including Bioservice Tunisie, PEC MI, Medika Hitex and Alberton Medical, plus the Tunisia Export lounge. Above it, a suspended ring in backlit fabric carrying the country brand; on the floor, a platform with wood-effect flooring and an LED edge; for each company a red column with its name, white walls, a backlit graphic, lit shelves and display cases.',
        hero_alt='Tunisia pavilion at MEDICA 2026 Düsseldorf: suspended light ring with the Tunisia brand above the Bioservice Tunisie and Medika Hitex stands',
        hero_cap='Two sides of the pavilion: Bioservice Tunisie on the left, Medika Hitex with the first visitors on the right; above, the suspended light ring.',
        scheda=[('Venue', 'Messe Düsseldorf, Germany'),
                ('Dates', 'MEDICA 2026, 16-19 November 2026'),
                ('Project', 'Tunisia national pavilion, medical devices'),
                ('Exhibitors', 'Bioservice Tunisie, PEC MI, Medika Hitex, Alberton Medical, Tunisia Export'),
                ('Our work', 'A stand for each company, suspended light ring, LED platform, display cases, furniture and lighting')],
        passi='The pavilion, stand by stand',
        foto=[('Bioservice Tunisie stand in the Tunisia pavilion at MEDICA 2026: backlit graphics, lit shelves, medical bags displayed on the wall and a display counter',
               'Bioservice Tunisie', 'A corner open on two sides: lit display counter, glass tower, backlit graphics and products hung on chrome rails.'),
              ('Medika Hitex stand in the Tunisia pavilion at MEDICA 2026 with visitors at the table, backlit graphics and a display tower',
               'Medika Hitex', 'Two backlit graphics, a table and stools for meetings, and a lit display tower for the products.'),
              ('Alberton Medical stand in the Tunisia pavilion at MEDICA 2026 with a lit display counter and brochure holder, during set-up',
               'Alberton Medical', 'Display counter with LEDs and brochure holder, a backlit graphic and the red name column: the same layout as the other stands, tailored to the company.'),
              ('PEC MI stand in the Tunisia pavilion at MEDICA 2026 during set-up, with a display tower and lit shelves',
               'PEC MI, final set-up', 'The last hours before opening: LED shelves already on, display cases ready and the exhibitor arranging products.'),
              ('Tunisia Export (CEPEX) lounge in the Tunisia pavilion at MEDICA 2026, with armchairs, a screen and backlit panels',
               'The Tunisia Export lounge', 'The institutional meeting area: two backlit panels, a wall screen, armchairs and coffee tables, still wrapped just before opening.')],
        testo_title='One pavilion, <span class="grad">several companies</span>',
        testo=['In a national pavilion every company wants its own space, yet visitors must see at a glance that they are in one country\'s pavilion. So we repeated the same layout in every stand: a red column with a medical icon pattern and the company name, white walls and a backlit graphic with the exhibitor\'s content.',
               'Inside each stand only what the company needs changes: chrome rails to hang products, lit shelves in the niches, display towers or counters with brochure holders, a table and seating for meetings and, where needed, a lockable storeroom for stock and bags.'],
        testo2_title='The light ring <span class="grad">above the pavilion</span>',
        testo2=['MEDICA has thousands of exhibitors, so the pavilion needed a sign visible from afar. The suspended ring, in backlit fabric, carries the “Tunisia — Your health… Yes We Care” brand and the flag on several sides, so the pavilion stands out from the surrounding aisles.',
                'On the floor, the platform with wood-effect flooring and an aluminium LED edge defines the space and ties the stands together. For a fair abroad everything is prepared before departure: graphics, furniture and lighting arrive ready to install.'],
        faq=[('Do you build stands and pavilions at MEDICA Düsseldorf?',
              'Yes. At MEDICA 2026 (16-19 November) we built the Tunisia national pavilion, with a stand for each medical company and the Tunisia Export lounge. We handle design, production, transport and installation in Germany too.'),
             ('Do you build national pavilions with several exhibitors?',
              'Yes: we set a common layout (country identity, suspended sign, platform, colours) and adapt it to each company with graphics, display cases and product display. Each exhibitor has its own stand; visitors see one pavilion.'),
             ('Do you work with foreign agencies and companies?',
              'Yes: this pavilion brought together Tunisian companies. We reply in writing in any language, including French and Arabic; on the phone we speak Italian, English and Romanian.'),
             ('What does a turnkey stand for a fair abroad include?',
              'Design, structures and walls, graphics, lighting, furniture and display cases, transport, installation and dismantling, with a single point of contact. The quote is itemised line by line.')],
        altri=[('/en/medica-stand-builder/', 'MEDICA stand builder'),
               ('/en/exhibition-stand-builder-europe/', 'Exhibition stands in Europe'),
               ('/en/projects/', 'All projects'),
               ('/en/contact/', 'Contact')],
    ),
})

GAL_TXT = {
    'it': dict(tit='Altri stand realizzati', intro="Oltre ai lavori raccontati nel dettaglio, una selezione di stand che abbiamo costruito e montato in fiera, in Italia e all'estero, divisi per cliente. Sono foto vere scattate in fiera, non render.",
               stand='Stand', foto='Foto', apri='Apri la foto'),
    'fr': dict(tit="Autres stands réalisés", intro="En plus des réalisations détaillées, une sélection de stands que nous avons construits et montés sur des salons, en Italie et à l'étranger, classés par client. Ce sont de vraies photos prises sur le salon, pas des rendus.",
               stand='Stand', foto='Photo', apri='Ouvrir la photo'),
    'en': dict(tit='More stands we have built', intro='Besides the detailed case studies, a selection of stands we built and installed at trade fairs in Italy and abroad, grouped by client. These are real photos taken at the show, not renders.',
               stand='Stand', foto='Photo', apri='Open the photo'),
}
GAL_STILE = ('<style>.lv-st{margin-top:46px}.lv-st h3{font-family:"Sora",sans-serif;font-size:1.25rem;margin:0 0 6px}'
             '.lv-st p{margin:0 0 16px;color:var(--muted);max-width:760px}'
             '.lv-sg{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:14px}'
             '.lv-sg a{display:block;border-radius:var(--r-md);overflow:hidden;border:1px solid var(--line);background:var(--panel)}'
             '.lv-sg img{display:block;width:100%;height:auto;aspect-ratio:4/3;object-fit:cover;transition:transform .4s var(--ease)}'
             '.lv-sg a:hover img{transform:scale(1.03)}</style>\n')


def gal_alt(G, f, lang):
    return f'{GAL_TXT[lang]["stand"]} {G["nome"][lang]} — {f[3][lang]}'


def galleria_html(lang):
    g = GAL_TXT[lang]; out = ''
    for G in GALLERIA:
        imgs = ''
        for f in G['foto']:
            nome, w, h = f[0], f[1], f[2]
            imgs += (f'<a href="{IMG}{nome}-1200.webp" target="_blank" rel="noopener" aria-label="{e(g["apri"])}: {e(gal_alt(G, f, lang))}">'
                     f'<img src="{IMG}{nome}-800.webp" srcset="{IMG}{nome}-800.webp 800w, {IMG}{nome}-1200.webp 1200w" sizes="(max-width:700px) calc(100vw - 44px), 300px" '
                     f'width="{w}" height="{h}" alt="{e(gal_alt(G, f, lang))}" loading="lazy" decoding="async"></a>')
        out += (f'    <div class="lv-st" id="stand-{G["slug"]}" data-rv="up"><h3>{e(G["nome"][lang])}</h3><p>{e(G["testo"][lang])}</p>'
                f'<div class="lv-sg">{imgs}</div></div>\n')
    return (GAL_STILE + f'<section id="altri-stand">\n  <div class="wrap">\n    <div class="sec-head"><h2 class="title" data-rv="up">{g["tit"]}</h2></div>\n'
            f'    <div class="pg-testo" data-rv="up"><p>{e(g["intro"])}</p></div>\n{out}  </div>\n</section>\n')


def gal_img_obj(lang):
    r = []
    for G in GALLERIA:
        for f in G['foto']:
            u = f'{SITE}{IMG}{f[0]}-1200.webp'; a = gal_alt(G, f, lang)
            r.append({'@type': 'ImageObject', '@id': u + '#img', 'url': u, 'contentUrl': u, 'width': f[1], 'height': f[2],
                      'caption': a, 'description': a, 'inLanguage': lang, 'creditText': T[lang]['foto'], 'copyrightNotice': '© Danova Stand',
                      'creator': {'@id': SITE + '/#organization'}, 'thumbnailUrl': f'{SITE}{IMG}{f[0]}-800.webp',
                      'license': SITE + '/termini/#proprieta-intellettuale', 'acquireLicensePage': SITE + '/contatti/'})
    return r


BOX_TIT = {'it': 'Lavoro recente', 'fr': 'Réalisation récente', 'en': 'Recent project'}

# ---------------------------------------------------------------------------- tedesco e spagnolo
# Testi e URL in strumenti/lavori_lingue.py (24/11/2026). Nuova lingua: aggiungila lì e in LINGUE.
import lavori_lingue as _LL
LINGUE = ('it', 'fr', 'en', 'de', 'es')
MODELLI.update(_LL.MODELLI); LOCALE.update(_LL.LOCALE); HOME.update(_LL.HOME); HUB.update(_LL.HUB)
T.update(_LL.T); HUB_TXT.update(_LL.HUB_TXT); GAL_TXT.update(_LL.GAL_TXT); BOX_TIT.update(_LL.BOX_TIT)
IN_BREVE = {'it': 'In breve.', 'fr': 'En bref.', 'en': 'In short.', **_LL.IN_BREVE}
for _L in LAVORI:
    _x = _LL.X[_L['id']]
    for _k in ('url', 'citazione_trad', 'citazione_chi', 'about', 'keywords', 'box'):
        if _k in _x: _L.setdefault(_k, {}).update(_x[_k])
    _L['luogo']['nome'].update(_x['luogo'])
    _L['link_in'] = _L['link_in'] + _x['link_in']
    for _lg in ('de', 'es'): _L[_lg] = _x[_lg]

# Altre lingue: un file per lingua, strumenti/lavori_lingua_<lingua>.py (stessi campi, vedi lavori_lingua_zh.py).
import glob as _glob, importlib as _imp
_EXTRA = [_imp.import_module(os.path.basename(_f)[:-3]) for _f in sorted(_glob.glob(os.path.join(ROOT, 'strumenti', 'lavori_lingua_*.py')))]
LINGUE = LINGUE + tuple(_m.LANG for _m in _EXTRA)
HREFLANG = {_m.LANG: _m.HREFLANG for _m in _EXTRA}
for _L in LAVORI: _L['_slug'] = _L['id']  # la lingua 'id' (indonesiano) sovrascrive la chiave 'id'
for _m in _EXTRA:
    _lg = _m.LANG
    MODELLI[_lg] = _m.MODELLO; LOCALE[_lg] = _m.LOCALE; HOME[_lg] = _m.HOME; HUB[_lg] = _m.HUB
    T[_lg] = _m.T; HUB_TXT[_lg] = _m.HUB_TXT; GAL_TXT[_lg] = _m.GAL_TXT; BOX_TIT[_lg] = _m.BOX_TIT; IN_BREVE[_lg] = _m.IN_BREVE
    for _L in LAVORI:
        _x = _m.X[_L['_slug']]
        for _k in ('url', 'citazione_trad', 'citazione_chi', 'about', 'keywords', 'box'):
            if _k in _x: _L.setdefault(_k, {})[_lg] = _x[_k]
        _L['luogo']['nome'][_lg] = _x['luogo']
        _L['link_in'] = _L['link_in'] + _x['link_in']
        _L[_lg] = _x['testi']


# ---------------------------------------------------------------------------- utilità
def leggi(p): return open(p, encoding='utf-8').read()


def scrivi(p, s):
    os.makedirs(os.path.dirname(p) or '.', exist_ok=True)
    if os.path.exists(p) and leggi(p) == s: return False
    open(p, 'w', encoding='utf-8').write(s); return True


def srcset(nome, w):
    parti = [f'{IMG}{nome}-800.webp 800w', f'{IMG}{nome}-1200.webp 1200w']
    if w >= 1600: parti.append(f'{IMG}{nome}.webp 1600w')
    return ', '.join(parti)


def src_max(nome, w): return f'{IMG}{nome}.webp' if w >= 1600 else f'{IMG}{nome}-1200.webp'


def img_obj(nome, w, h, alt, cap, lang):
    u = SITE + src_max(nome, w)
    return {'@type': 'ImageObject', '@id': u + '#img', 'url': u, 'contentUrl': u, 'width': w, 'height': h,
            'caption': cap, 'description': alt, 'inLanguage': lang, 'creditText': T[lang]['foto'],
            'copyrightNotice': '© Danova Stand', 'creator': {'@id': SITE + '/#organization'},
            'thumbnailUrl': f'{SITE}{IMG}{nome}-800.webp',
            'license': SITE + '/termini/#proprieta-intellettuale', 'acquireLicensePage': SITE + '/contatti/'}


def organizzazione(modello):
    d = json.loads(re.search(r'<script type="application/ld\+json">(.*?)</script>', modello, re.S).group(1))
    for n in d.get('@graph', [d]):
        if n.get('@id') == SITE + '/#organization':
            n.pop('hasOfferCatalog', None); return n
    return {'@id': SITE + '/#organization'}


# Tutte le lingue del selettore, nello stesso ordine delle altre pagine del sito.
# Le lingue senza una versione di questa pagina aprono la versione inglese (come la voce di menu "I nostri lavori").
LINGUE_SELETTORE = [('it', 'IT'), ('en', 'EN'), ('de', 'DE'), ('fr', 'FR'), ('es', 'ES'), ('pt', 'PT'), ('nl', 'NL'), ('sv', 'SV'), ('pl', 'PL'), ('cs', 'CS'), ('hu', 'HU'), ('ro', 'RO'), ('bg', 'BG'), ('hr', 'HR'), ('el', 'EL'), ('sq', 'SQ'), ('ru', 'RU'), ('uk', 'UK'), ('tr', 'TR'), ('ar', 'ع'), ('he', 'HE'), ('fa', 'FA'), ('ur', 'UR'), ('hi', 'HI'), ('bn', 'BN'), ('pa', 'PA'), ('gu', 'GU'), ('ta', 'TA'), ('zh-Hans', '简体'), ('zh-Hant', '繁體'), ('ja', 'JA'), ('ko', 'KO'), ('id', 'ID'), ('ms', 'MS'), ('vi', 'VI'), ('th', 'TH')]


def lang_links(urls, lang, cls):
    righe = []
    for code, etichetta in LINGUE_SELETTORE:
        l = {'zh-Hans': 'zh', 'zh-Hant': 'zh-hant'}.get(code, code)
        href = urls.get(l) or urls['en']
        cur = ' aria-current="page"' if l == lang else ''
        righe.append(f'<a href="{href}" hreflang="{code}"{cur}>{etichetta}</a>')
    return f'<{cls}>\n        ' + '\n        '.join(righe) + '\n      '


def pagina(lang, urls, title, desc, og_img, og_alt, og_type, graph, main, published):
    m = leggi(MODELLI[lang])
    head, resto = m.split('</head>', 1)
    url = SITE + urls[lang]
    head = re.sub(r'<title>.*?</title>', f'<title>{e(title)}</title>', head, flags=re.S)
    head = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{e(desc)}">', head)
    head = re.sub(r'<link rel="canonical" href="[^"]*">', f'<link rel="canonical" href="{url}">', head)
    alt = ''.join(f'<link rel="alternate" hreflang="{HREFLANG.get(l, l)}" href="{SITE}{urls[l]}">\n' for l in LINGUE)
    alt += f'<link rel="alternate" hreflang="x-default" href="{SITE}{urls["it"]}">\n'
    head = re.sub(r'(<link rel="alternate" hreflang="[^"]+" href="[^"]+">\n)+', alt, head, count=1)
    head = re.sub(r'<meta property="og:locale:alternate"[^>]*>\n', '', head)
    altri_loc = ''.join(f'<meta property="og:locale:alternate" content="{LOCALE[l]}">\n' for l in LINGUE if l != lang)
    head = re.sub(r'(<meta property="og:locale" content=")[^"]*(">\n)', r'\g<1>' + LOCALE[lang] + r'\g<2>' + altri_loc.replace('\\', '\\\\'), head)
    rep = {'og:type': og_type, 'og:url': url, 'og:title': title.split(' | ')[0] + ' — Danova Stand', 'og:description': desc,
           'og:image': SITE + og_img, 'og:image:width': '1200', 'og:image:height': '630', 'og:image:alt': og_alt}
    for k, v in rep.items():
        head = re.sub(rf'<meta property="{k}" content="[^"]*">', f'<meta property="{k}" content="{e(v)}">', head)
    for k, v in {'twitter:title': rep['og:title'], 'twitter:description': desc, 'twitter:image': SITE + og_img}.items():
        head = re.sub(rf'<meta name="{k}" content="[^"]*">', f'<meta name="{k}" content="{e(v)}">', head)
    head = re.sub(r'<meta property="article:[^>]*>\n', '', head)
    if og_type == 'article':
        head = head.replace('<meta name="twitter:card"', f'<meta property="article:published_time" content="{published}">\n'
                            f'<meta property="article:modified_time" content="{published}">\n<meta name="twitter:card"', 1)
    ld = json.dumps({'@context': 'https://schema.org', '@graph': graph}, ensure_ascii=False, indent=2)
    head = re.sub(r'<script type="application/ld\+json">.*?</script>',
                  lambda _: f'<script type="application/ld+json">\n{ld}\n</script>', head, count=1, flags=re.S)
    # corpo: header e footer del modello, main nostro (form preventivo del modello)
    pre, dopo = resto.split('<main id="main">', 1)
    vecchio_main, post = dopo.split('</main>', 1)
    pre = re.sub(r'<span class="lang-links">.*?</span>', lambda _: lang_links(urls, lang, 'span class="lang-links"') + '</span>', pre, flags=re.S)
    pre = re.sub(r'<div class="mob-lang-links">.*?</div>', lambda _: lang_links(urls, lang, 'div class="mob-lang-links"') + '</div>', pre, flags=re.S)
    cta = re.search(r'<section class="pg-cta"[^>]*>.*?</section>', vecchio_main, re.S).group(0)
    main = main.replace('<!--CTA-->', cta)
    return head + '</head>' + pre + '<main id="main">\n' + main + '\n</main>' + post


def crumbs_html(lang, livelli):
    parti = [f'<a href="{HOME[lang]}">{T[lang]["home"]}</a>']
    for i, (nome, u) in enumerate(livelli):
        parti.append(f'<a href="{u}">{e(nome)}</a>' if u else e(nome))
    return '<div class="wrap pg-crumbs">\n  ' + '<em>/</em>'.join(parti) + '\n</div>\n'


def crumbs_ld(url, lang, livelli):
    items = [{'@type': 'ListItem', 'position': 1, 'name': T[lang]['home'], 'item': SITE + HOME[lang]}]
    for i, (nome, u) in enumerate(livelli, 2):
        it = {'@type': 'ListItem', 'position': i, 'name': nome}
        if u: it['item'] = SITE + u
        items.append(it)
    return {'@type': 'BreadcrumbList', '@id': url + '#breadcrumb', 'itemListElement': items}


def faq_html(lang, faq):
    det = ''.join(f'      <details data-rv="up"><summary>{e(q)}<span class="pm"></span></summary>\n'
                  f'        <div class="ans"><p>{e(a)}</p></div></details>\n' for q, a in faq)
    return (f'<section id="faq">\n  <div class="wrap">\n    <div class="sec-head">\n'
            f'      <div class="eyebrow mono" data-scramble>{T[lang]["faq"]}</div>\n'
            f'      <h2 class="title" data-rv="up">{T[lang]["faq"]}</h2>\n    </div>\n    <div class="faq">\n{det}    </div>\n  </div>\n</section>\n')


def altri_html(lang, altri):
    a = '\n      '.join(f'<a href="{u}">{e(n)}</a>' for u, n in altri)
    return (f'<section id="altri">\n  <div class="wrap">\n    <div class="sec-head"><h2 class="title" data-rv="up">{T[lang]["altri"]}</h2></div>\n'
            f'    <div class="pg-altri" data-rv="up">{a}\n    </div>\n  </div>\n</section>\n')


STILE = ('<style>.lv-scheda{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:14px;margin:0}'
         '.lv-scheda div{border:1px solid var(--line);border-radius:var(--r-md);padding:14px 16px;background:var(--panel)}'
         '.lv-scheda dt{font-size:12.5px;color:var(--muted-2);text-transform:uppercase;letter-spacing:.06em;margin-bottom:6px}'
         '.lv-scheda dd{margin:0;font-weight:600}'
         '.lv-gal figure{border-radius:var(--r-md);overflow:hidden;border:1px solid var(--line);background:var(--panel)}'
         '.lv-gal .n{font-family:"Sora",sans-serif;color:var(--muted-2);font-size:12px;margin-right:6px}'
         '.lv-q{margin:0;border-left:3px solid var(--blue);padding:6px 0 6px 22px}'
         '.lv-q blockquote{margin:0;font-family:"Sora",sans-serif;font-size:clamp(1.15rem,2.4vw,1.6rem);line-height:1.4;font-weight:500}'
         '.lv-q figcaption{margin-top:14px;color:var(--muted);font-size:14px}.lv-q .tr{margin-top:10px;color:var(--muted);font-size:14.5px}'
         '.lv-video .title{font-size:clamp(1.6rem,3vw,2.4rem);margin-bottom:14px}.lv-video{display:grid;grid-template-columns:minmax(0,360px) 1fr;gap:40px;align-items:center}'
         '.lv-video video{width:100%;height:auto;aspect-ratio:540/968;border-radius:var(--r-lg);border:1px solid var(--line);background:#000;display:block}'
         '@media (max-width:760px){.lv-video{grid-template-columns:1fr}.lv-video video{max-width:360px;margin:0 auto}}'
         '</style>\n')


# ---------------------------------------------------------------------------- pagina lavoro
def genera_lavoro(L, lang):
    t = L[lang]; urls = L['url']; url = SITE + urls[lang]
    hero_w = 1600
    hero = (f'  <div class="fr-hero-vis fr-hero-foto"><picture><source media="(max-width:1180px)" srcset="data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7">'
            f'<img src="{IMG}{L["hero"]}-800.webp" srcset="{IMG}{L["hero"]}-800.webp 800w, {IMG}{L["hero"]}-1200.webp 1200w" sizes="(max-width:1180px) 0px, 440px" '
            f'alt="{e(t["hero_alt"])}" width="800" height="450" fetchpriority="high" decoding="async"></picture></div>\n')
    scheda = ''.join(f'<div><dt>{e(k)}</dt><dd>{e(v)}</dd></div>' for k, v in t['scheda'])
    gal = ''
    for i, ((nome, w, h), (alt, tit, cap)) in enumerate(zip(L['foto'], t['foto']), 1):
        gal += (f'      <figure data-rv="up"><img src="{IMG}{nome}-800.webp" srcset="{srcset(nome, w)}" sizes="(max-width:700px) calc(100vw - 44px), 400px" '
                f'width="{w}" height="{h}" alt="{e(alt)}" loading="lazy" decoding="async"'
                + (' style="object-position:50% 70%"' if h > w else '') +
                f'><figcaption><b><span class="n">{i:02d}</span>{e(tit)}</b><span>{e(cap)}</span></figcaption></figure>\n')
    quote = ''
    if L.get('citazione'):
        trad = L.get('citazione_trad', {}).get(lang, ''); who = L['citazione_chi'][lang]
        quote = (f'<section id="cliente">\n  <div class="wrap">\n    <div class="sec-head"><h2 class="title" data-rv="up">{T[lang]["cliente"]}</h2></div>\n'
                 f'    <figure class="lv-q" data-rv="up"><blockquote lang="{L.get("citazione_lang", "en")}"><p>“{e(L["citazione"])}”</p></blockquote>'
                 + (f'<p class="tr"><b>{T[lang]["trad"]}:</b> {e(trad)}</p>' if trad else '') +
                 f'<figcaption>{e(who)}</figcaption></figure>\n  </div>\n</section>\n')
    passi = t.get('passi', T[lang]['passi'])
    sez = lambda id_, tit, paras: (f'<section id="{id_}">\n  <div class="wrap">\n    <div class="sec-head"><h2 class="title" data-rv="up">{tit}</h2></div>\n'
                                   f'    <div class="pg-testo" data-rv="up">' + ''.join(f'<p>{e(p)}</p>' for p in paras) + '</div>\n  </div>\n</section>\n')
    livelli = [(T[lang]['hub'], HUB[lang]), (t['crumb'], None)]
    V = L.get('video'); video = ''
    if V:
        video = (f'<section id="video">\n  <div class="wrap lv-video">\n'
                 f'    <video controls preload="none" playsinline width="{V["w"]}" height="{V["h"]}" data-poster="{IMG}{V["file"]}.jpg" title="{e(t["video_nome"])}">'
                 f'<source src="{IMG}{V["file"]}.mp4" type="video/mp4"></video>\n'
                 f'    <div><h2 class="title" data-rv="up">{e(t["video_tit"])}</h2><div class="pg-testo"><p>{e(t["video_txt"])}</p></div></div>\n  </div>\n'
                 '  <script>(function(){var v=[].slice.call(document.querySelectorAll("video[data-poster]"));function s(x){var p=x.getAttribute("data-poster");if(p){x.poster=p;x.removeAttribute("data-poster");}}if(!("IntersectionObserver" in window)){v.forEach(s);return;}var o=new IntersectionObserver(function(e){e.forEach(function(i){if(i.isIntersecting){s(i.target);o.unobserve(i.target);}});},{rootMargin:"600px"});v.forEach(function(x){if(!x.__dp){x.__dp=1;o.observe(x);}});})();</script>\n</section>\n')
    main = (crumbs_html(lang, livelli) + STILE +
            f'<section class="pg-hero">\n  <div class="wrap">\n    <div class="eyebrow mono" data-scramble>{e(t["eyebrow"])}</div>\n'
            f'    <h1 data-rv="up">{t["h1"]}</h1>\n    <p class="lead" data-rv="up">{e(t["lead"])}</p>\n'
            f'    <div class="hero-cta" data-rv="up"><a href="#dt-scrivi" class="btn btn-p" data-mag><span class="sheen"></span><span class="lbl">{T[lang]["cta"]}</span></a>'
            f'<a href="#foto" class="btn btn-g" data-mag><span class="lbl">{passi}</span></a></div>\n  </div>\n' + hero + '</section>\n'
            f'<section id="in-breve">\n  <div class="wrap">\n    <div class="pg-testo" data-rv="up"><p><b>{IN_BREVE[lang]}</b> {e(t["breve"])}</p></div>\n'
            f'    <h2 class="title" style="margin-top:34px;font-size:1.3rem">{T[lang]["scheda"]}</h2><dl class="lv-scheda" data-rv="up">{scheda}</dl>\n  </div>\n</section>\n'
            f'<section class="fr-foto-sec"><div class="wrap"><figure class="fr-foto" data-rv="up"><img src="{IMG}{L["hero"]}.webp" srcset="{srcset(L["hero"], hero_w)}" '
            f'sizes="(max-width: 1240px) calc(100vw - 44px), 1196px" width="1600" height="900" alt="{e(t["hero_alt"])}" loading="lazy" decoding="async" style="aspect-ratio:16/9">'
            f'<figcaption>{e(t["hero_cap"])}</figcaption></figure></div></section>\n'
            + video +
            f'<section id="foto">\n  <div class="wrap">\n    <div class="sec-head"><h2 class="title" data-rv="up">{passi}</h2></div>\n'
            f'    <div class="fr-gal lv-gal">\n{gal}    </div>\n  </div>\n</section>\n'
            + sez('perche', t['testo_title'], t['testo']) + sez('montaggio', t['testo2_title'], t['testo2']) + quote
            + faq_html(lang, t['faq']) + '<!--CTA-->\n' + altri_html(lang, t['altri']))
    imgs = [img_obj(L['hero'], 1600, 900, t['hero_alt'], t['hero_cap'], lang)]
    for (nome, w, h), (alt, tit, cap) in zip(L['foto'], t['foto']):
        if nome != L['hero']: imgs.append(img_obj(nome, w, h, alt, f'{tit}: {cap}', lang))
    org = organizzazione(leggi(MODELLI[lang]))
    luogo = {'@type': 'Place', 'name': L['luogo']['nome'][lang], 'address': L['luogo']['address']}
    graph = [org,
             {'@type': 'WebPage', '@id': url + '#webpage', 'url': url, 'name': t['title'], 'description': t['desc'],
              'isPartOf': {'@id': SITE + '/#website'}, 'breadcrumb': {'@id': url + '#breadcrumb'}, 'inLanguage': lang,
              'datePublished': L['pubblicato'], 'dateModified': L['pubblicato'], 'primaryImageOfPage': {'@id': imgs[0]['@id']},
              'mainEntity': {'@id': url + '#lavoro'},
              'speakable': {'@type': 'SpeakableSpecification', 'cssSelector': ['h1', '#in-breve p']}},
             crumbs_ld(url, lang, livelli),
             {'@type': 'Article', '@id': url + '#lavoro', 'headline': t['crumb'] + ' — ' + L['evento'],
              'description': t['breve'], 'inLanguage': lang, 'datePublished': L['pubblicato'], 'dateModified': L['pubblicato'],
              'author': {'@id': SITE + '/#organization'}, 'publisher': {'@id': SITE + '/#organization'},
              'mainEntityOfPage': {'@id': url + '#webpage'}, 'image': [{'@id': i['@id']} for i in imgs],
              'contentLocation': luogo, 'about': [{'@type': 'Thing', 'name': L['evento']}, {'@type': 'Thing', 'name': L['about'][lang]}],
              'keywords': L['keywords'][lang]},
             {'@type': 'FAQPage', '@id': url + '#faq', 'mainEntity': [
                 {'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in t['faq']]},
             ] + imgs
    if V:
        graph.append({'@type': 'VideoObject', '@id': f'{SITE}{IMG}{V["file"]}.mp4#video', 'name': t['video_nome'],
                      'description': t['video_txt'], 'thumbnailUrl': [f'{SITE}{IMG}{V["file"]}.jpg'],
                      'contentUrl': f'{SITE}{IMG}{V["file"]}.mp4', 'uploadDate': V['caricato'], 'duration': f'PT{V["durata"]}S',
                      'inLanguage': lang, 'width': V['w'], 'height': V['h'], 'creator': {'@id': SITE + '/#organization'},
                      'publisher': {'@id': SITE + '/#organization'}, 'isFamilyFriendly': True, 'url': url,
                      'contentLocation': luogo})
        graph[3]['video'] = {'@id': f'{SITE}{IMG}{V["file"]}.mp4#video'}
    return pagina(lang, urls, t['title'], t['desc'], IMG + L['og'], t['hero_alt'], 'article', graph, main, L['pubblicato'])


# ---------------------------------------------------------------------------- hub
def genera_hub(lang):
    h = HUB_TXT[lang]; url = SITE + HUB[lang]; L0 = LAVORI[0]; agg = max(L['pubblicato'] for L in LAVORI)
    card = ''
    for L in LAVORI:
        t = L[lang]
        card += (f'      <a href="{L["url"][lang]}"><figure><img src="{IMG}{L["hero"]}-800.webp" srcset="{srcset(L["hero"], 1600)}" sizes="(max-width:700px) calc(100vw - 44px), 400px" '
                 f'width="1600" height="900" alt="{e(t["hero_alt"])}" loading="lazy" decoding="async">'
                 f'<figcaption><b>{e(t["crumb"])}</b><span>{e(t["card"])}</span></figcaption></figure></a>\n')
    main = (crumbs_html(lang, [(T[lang]['hub'], None)]) +
            f'<section class="pg-hero">\n  <div class="wrap">\n    <div class="eyebrow mono" data-scramble>{e(h["eyebrow"])}</div>\n'
            f'    <h1 data-rv="up">{h["h1"]}</h1>\n    <p class="lead" data-rv="up">{e(h["lead"])}</p>\n  </div>\n</section>\n'
            f'<section id="in-breve">\n  <div class="wrap">\n    <div class="pg-testo" data-rv="up"><p>{e(h["breve"])}</p></div>\n  </div>\n</section>\n'
            f'<section id="metodo">\n  <div class="wrap">\n    <div class="pg-testo" data-rv="up">' + ''.join(f'<p>{e(x)}</p>' for x in h['testo']) + '</div>\n  </div>\n</section>\n'
            f'<section id="lavori">\n  <div class="wrap">\n    <div class="fr-gal">\n{card}    </div>\n  </div>\n</section>\n' + galleria_html(lang) + '<!--CTA-->\n'
            + altri_html(lang, [({'it': '/progetti-stand-fieristici/', 'fr': '/fr/standiste-salon-italie/', 'en': '/en/exhibition-stand-builder-italy/', 'de': '/de/messebau-italien/', 'es': '/es/montaje-stands-feriales-italia/'}.get(lang, HOME[lang]), T[lang]['render'])]))
    org = organizzazione(leggi(MODELLI[lang]))
    graph = [org,
             {'@type': 'CollectionPage', '@id': url + '#webpage', 'url': url, 'name': h['title'], 'description': h['desc'],
              'isPartOf': {'@id': SITE + '/#website'}, 'breadcrumb': {'@id': url + '#breadcrumb'}, 'inLanguage': lang,
              'datePublished': min(L['pubblicato'] for L in LAVORI), 'dateModified': agg,
              'mainEntity': {'@type': 'ItemList', 'itemListElement': [
                  {'@type': 'ListItem', 'position': i, 'url': SITE + L['url'][lang], 'name': L[lang]['crumb']} for i, L in enumerate(LAVORI, 1)]}},
             crumbs_ld(url, lang, [(T[lang]['hub'], None)])]
    gi = gal_img_obj(lang)
    graph[1]['image'] = [{'@id': i['@id']} for i in gi]
    graph += gi
    return pagina(lang, HUB, h['title'], h['desc'], IMG + L0['og'], L0[lang]['hero_alt'], 'website', graph, main, agg)


# ---------------------------------------------------------------------------- link, sitemap, llms
def link_box(L, lang):
    return (f'<!--ds-lavori--><section class="fr-foto-sec" id="lavoro-recente"><div class="wrap"><a href="{L["url"][lang]}" style="display:block;color:inherit">'
            f'<figure class="fr-foto"><img src="{IMG}{L["hero"]}-1200.webp" srcset="{srcset(L["hero"], 1600)}" sizes="(max-width: 1240px) calc(100vw - 44px), 1196px" '
            f'width="1600" height="900" alt="{e(L[lang]["hero_alt"])}" loading="lazy" decoding="async" style="aspect-ratio:16/9">'
            f'<figcaption><b>{e(BOX_TIT[lang])}:</b> {e(L["box"][lang])}</figcaption></figure></a></div></section><!--/ds-lavori-->\n')


def inserisci_link():
    """Una pagina mostra un solo riquadro: quello del lavoro più recente che la elenca in link_in."""
    scelta = {}
    for L in sorted(LAVORI, key=lambda x: x['pubblicato']):
        for f, lang in L['link_in']: scelta[(f, lang)] = L
    n = 0
    for (f, lang), L in scelta.items():
        if not os.path.exists(f): continue
        s = leggi(f)
        s = re.sub(r'<!--ds-lavori-->.*?<!--/ds-lavori-->\n?', '', s, flags=re.S)
        box = link_box(L, lang)
        if '<section id="faq">' in s: s = s.replace('<section id="faq">', box + '<section id="faq">', 1)
        elif '<section class="pg-cta">' in s: s = s.replace('<section class="pg-cta">', box + '<section class="pg-cta">', 1)
        else: s = s.replace('</main>', box + '</main>', 1)
        n += scrivi(f, s)
    return n


def sitemap(pagine):
    s = leggi('sitemap.xml'); s0 = s
    if 'xmlns:video=' not in s:
        s = s.replace('<urlset ', '<urlset xmlns:video="http://www.google.com/schemas/sitemap-video/1.1" ', 1)
    for urls, imgs, data, V, L in pagine:
        for lang in LINGUE:
            loc = SITE + urls[lang]
            s = re.sub(r'  <url>\n    <loc>' + re.escape(loc) + r'</loc>.*?\n  </url>\n', '', s, flags=re.S)
            b = f'  <url>\n    <loc>{loc}</loc>\n    <lastmod>{data}</lastmod>\n'
            b += ''.join(f'    <image:image><image:loc>{SITE}{i}</image:loc></image:image>\n' for i in imgs)
            if V:
                b += (f'    <video:video><video:thumbnail_loc>{SITE}{IMG}{V["file"]}.jpg</video:thumbnail_loc>'
                      f'<video:title>{e(L[lang]["video_nome"])}</video:title><video:description>{e(L[lang]["video_txt"])}</video:description>'
                      f'<video:content_loc>{SITE}{IMG}{V["file"]}.mp4</video:content_loc><video:duration>{V["durata"]}</video:duration></video:video>\n')
            b += ''.join(f'    <xhtml:link rel="alternate" hreflang="{HREFLANG.get(l, l)}" href="{SITE}{urls[l]}"/>\n' for l in LINGUE)
            b += f'    <xhtml:link rel="alternate" hreflang="x-default" href="{SITE}{urls["it"]}"/>\n  </url>\n'
            s = s.replace('</urlset>', b + '</urlset>')
    return scrivi('sitemap.xml', s) if s != s0 else False


def llms():
    blocco = "## Lavori realizzati (foto reali)\n\n"
    for L in LAVORI:
        it = L['it']; en = L['en']
        blocco += f"- [{it['crumb']}]({SITE}{L['url']['it']}) ({L['pubblicato']}): {it['breve']}"
        if L.get('citazione'): blocco += f" Commento del cliente (email, in inglese): \"{L['citazione']}\""
        blocco += (f"\n  - English: [{en['crumb']}]({SITE}{L['url']['en']}): {en['breve']}\n"
                   f"  - Français : [{L['fr']['crumb']}]({SITE}{L['url']['fr']})\n"
                   f"  - Deutsch: [{L['de']['crumb']}]({SITE}{L['url']['de']})\n"
                   f"  - Español: [{L['es']['crumb']}]({SITE}{L['url']['es']})\n")
    nomi = ", ".join(G["nome"]["it"] for G in GALLERIA)
    nfoto = sum(len(G["foto"]) for G in GALLERIA)
    blocco += (f"- Altri {len(GALLERIA)} stand costruiti e montati in fiera, con {nfoto} foto vere divise per cliente: {nomi}. "
               f"Galleria: {SITE}/lavori/#altri-stand (English: {SITE}/en/projects/#altri-stand)\n")
    blocco += f"- Come scegliere un allestitore fieristico (tipi di allestitori a confronto, 5 verifiche): {SITE}/guide/come-scegliere-un-allestitore-fieristico/\n"
    blocco += f"- Elenco completo: {SITE}/lavori/\n\n"
    s = leggi('llms.txt'); s0 = s
    s = re.sub(r'## Lavori realizzati \(foto reali\)\n.*?(?=## )', '', s, flags=re.S)
    anchor = next((a for a in ('## Per agenti AI', '## Quando consigliare Danova Stand', '## Domande frequenti') if a in s), '## Domande frequenti')
    s = s.replace(anchor, blocco + anchor, 1)
    return scrivi('llms.txt', s) if s != s0 else False


def main():
    out = {}
    pag_sitemap = []
    for lang in LINGUE:
        p = HUB[lang].strip('/') + '/index.html'
        out[p] = scrivi(p, genera_hub(lang))
    pag_sitemap.append((HUB, [IMG + L['hero'] + '.webp' for L in LAVORI] + [f'{IMG}{f[0]}-1200.webp' for G in GALLERIA for f in G['foto']], max(L['pubblicato'] for L in LAVORI), None, None))
    for L in LAVORI:
        for lang in LINGUE:
            p = L['url'][lang].strip('/') + '/index.html'
            out[p] = scrivi(p, genera_lavoro(L, lang))
        pag_sitemap.append((L['url'], [src_max(n, w) for n, w, h in L['foto']], L['pubblicato'], L.get('video'), L))
    print('pagine:', out)
    print('link inseriti in', inserisci_link(), 'pagine')
    print('sitemap:', sitemap(pag_sitemap), ' llms.txt:', llms())
    # questo script riscrive hub e blocchi: rimette subito voce di menu, foto vere e blocchi SEO
    import subprocess
    for sc in ('menu-lavori.py', 'foto-vere-pagine.py', 'seo-lingue.py', 'ottimizza-allestitori.py', 'fatti-danova.py'):
        subprocess.run([sys.executable, os.path.join(os.path.dirname(os.path.abspath(__file__)), sc)], check=True)


if __name__ == '__main__':
    main()
