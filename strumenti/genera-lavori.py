#!/usr/bin/env python3
"""Genera la sezione LAVORI REALIZZATI (foto vere di cantiere) in italiano, francese e inglese.

    python3 strumenti/genera-lavori.py

Idempotente. Rilancialo dopo ogni migra-da-danovatech.py (prima di ottimizza-geo.py):
 - riscrive gli hub /lavori/, /fr/realisations/, /en/projects/ e le pagine dei singoli lavori;
 - aggiunge le pagine alla sitemap (se mancano);
 - rimette i link verso i lavori nelle pagine collegate (blocchi <!--ds-lavori-->);
 - aggiorna la sezione "Lavori realizzati" di llms.txt.

Nuovo lavoro: aggiungi un dizionario in LAVORI (testi IT/FR/EN, foto in assets/img/lavori/,
nome file = parola chiave, versioni -800 e -1200 in webp + og 1200x630 in jpg).
"""
import html, json, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
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
               desc="Lavori realizzati da Danova Stand con foto di cantiere: allestimenti per eventi, spettacoli e fiere. Ultimo: palco galleggiante all'Arsenale di Venezia.",
               eyebrow='Portfolio · foto di cantiere',
               h1='Lavori realizzati: <span class="grad">foto vere, non render</span>.',
               lead="Qui raccogliamo i lavori fatti, con le foto scattate in cantiere dalla nostra squadra: cosa ci è stato chiesto, cosa abbiamo montato, in quanto tempo e cosa ne pensa il cliente. Per le idee e i render di progetto c'è la pagina dei progetti.",
               breve="Danova Stand pubblica qui i lavori realizzati con foto reali di montaggio: allestimenti per eventi, spettacoli, fiere e mostre in Italia e in Europa. Ogni scheda indica luogo, date, lavorazioni eseguite e, quando il cliente lo permette, il suo commento."),
    'fr': dict(title='Nos réalisations : aménagements en photos | Danova Stand',
               desc="Réalisations Danova Stand en photos de chantier : événements, spectacles et salons en Italie. Dernière : scène flottante à l'Arsenal de Venise.",
               eyebrow='Portfolio · photos de chantier',
               h1='Nos réalisations : <span class="grad">de vraies photos, pas des rendus</span>.',
               lead="Nous rassemblons ici nos chantiers, avec les photos prises par notre équipe : la demande, ce que nous avons monté, en combien de temps et l'avis du client.",
               breve="Danova Stand publie ici ses réalisations avec de vraies photos de montage : aménagements d'événements, spectacles, salons et expositions en Italie et en Europe. Chaque fiche indique le lieu, les dates, les travaux réalisés et, quand le client l'accepte, son commentaire."),
    'en': dict(title='Our projects: real set-up photos | Danova Stand',
               desc='Projects by Danova Stand with real site photos: event, show and trade fair set-ups in Italy. Latest: a floating stage at the Venice Arsenale.',
               eyebrow='Portfolio · site photos',
               h1='Our projects: <span class="grad">real photos, not renders</span>.',
               lead='This is where we collect finished jobs, with photos taken on site by our crew: the brief, what we built, how long it took and what the client said.',
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
        pioggia_title="Due giorni di montaggio, <span class=\"grad\">anche sotto la pioggia</span>",
        pioggia=["A Venezia si lavora con quello che c'è: materiali che arrivano in barca, spazi stretti, tempi fissati dallo spettacolo. Durante il montaggio è arrivata anche la pioggia, e abbiamo comunque consegnato il palco finito nei tempi previsti.",
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
        pioggia_title="Deux jours de montage, <span class=\"grad\">même sous la pluie</span>",
        pioggia=["À Venise, on travaille avec les contraintes du lieu : matériel livré en bateau, espaces réduits, calendrier fixé par le spectacle. La pluie est arrivée pendant le montage et nous avons tout de même livré la scène dans les délais.",
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
        pioggia_title='Two days on site, <span class="grad">rain included</span>',
        pioggia=['In Venice you work with what the city gives you: materials delivered by boat, tight spaces and a schedule set by the show. It rained during the set-up and we still handed over the finished stage on time.',
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

# link verso i lavori da inserire in altre pagine: (file, lingua, dove inserire: prima di questo testo)
LINK_IN = [
    ('allestimenti-fieristici-venezia/index.html', 'it'),
    ('allestimenti-eventi/index.html', 'it'),
    ('allestimenti-eventi-showroom-negozi/index.html', 'it'),
    ('progetti-stand-fieristici/index.html', 'it'),
    ('index.html', 'it'),
    ('fr/standiste-salon-italie/index.html', 'fr'),
    ('en/exhibition-stand-builder-italy/index.html', 'en'),
]
BOX_TXT = {
    'it': ('Lavoro recente', 'Guarda il palco galleggiante che abbiamo allestito all\'Arsenale di Venezia (novembre 2026), con le foto del montaggio.'),
    'fr': ('Réalisation récente', 'Découvrez la scène flottante que nous avons aménagée à l\'Arsenal de Venise (novembre 2026), avec les photos du montage.'),
    'en': ('Recent project', 'See the floating stage we fitted out at the Venice Arsenale (November 2026), with photos of the set-up.'),
}


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


def lang_links(urls, lang, cls):
    nomi = {'it': 'IT', 'en': 'EN', 'fr': 'FR'}
    righe = []
    for l in ('it', 'en', 'fr'):
        cur = ' aria-current="page"' if l == lang else ''
        righe.append(f'<a href="{urls[l]}" hreflang="{l}"{cur}>{nomi[l]}</a>')
    return f'<{cls}>\n        ' + '\n        '.join(righe) + '\n      '


def pagina(lang, urls, title, desc, og_img, og_alt, og_type, graph, main, published):
    m = leggi(MODELLI[lang])
    head, resto = m.split('</head>', 1)
    url = SITE + urls[lang]
    head = re.sub(r'<title>.*?</title>', f'<title>{e(title)}</title>', head, flags=re.S)
    head = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{e(desc)}">', head)
    head = re.sub(r'<link rel="canonical" href="[^"]*">', f'<link rel="canonical" href="{url}">', head)
    alt = ''.join(f'<link rel="alternate" hreflang="{l}" href="{SITE}{urls[l]}">\n' for l in ('it', 'fr', 'en'))
    alt += f'<link rel="alternate" hreflang="x-default" href="{SITE}{urls["it"]}">\n'
    head = re.sub(r'(<link rel="alternate" hreflang="[^"]+" href="[^"]+">\n)+', alt, head, count=1)
    head = re.sub(r'<meta property="og:locale:alternate"[^>]*>\n', '', head)
    altri_loc = ''.join(f'<meta property="og:locale:alternate" content="{LOCALE[l]}">\n' for l in ('it', 'fr', 'en') if l != lang)
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
    trad = {'it': "Un grande grazie a te e alla tua squadra. Stanno facendo un ottimo lavoro sul palco e apprezzo davvero quanto siate tutti orientati alle soluzioni. Per noi fa davvero la differenza.",
            'fr': "Un grand merci à toi et à ton équipe. Ils font un excellent travail sur la scène et j'apprécie vraiment à quel point vous êtes tous orientés solutions. Cela fait vraiment la différence pour nous.",
            'en': ''}[lang]
    who = {'it': "Organizzazione di The Heart in Art, cliente francese — email al nostro team, novembre 2026",
           'fr': "Organisation de The Heart in Art, client français — e-mail à notre équipe, novembre 2026",
           'en': "The Heart in Art organisers, French client — email to our team, November 2026"}[lang]
    quote = (f'<section id="cliente">\n  <div class="wrap">\n    <div class="sec-head"><h2 class="title" data-rv="up">{T[lang]["cliente"]}</h2></div>\n'
             f'    <figure class="lv-q" data-rv="up"><blockquote lang="en"><p>“{e(L["citazione"])}”</p></blockquote>'
             + (f'<p class="tr"><b>{T[lang]["trad"]}:</b> {e(trad)}</p>' if trad else '') +
             f'<figcaption>{e(who)}</figcaption></figure>\n  </div>\n</section>\n')
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
            f'<a href="#foto" class="btn btn-g" data-mag><span class="lbl">{T[lang]["passi"]}</span></a></div>\n  </div>\n' + hero + '</section>\n'
            f'<section id="in-breve">\n  <div class="wrap">\n    <div class="pg-testo" data-rv="up"><p><b>{ {"it": "In breve.", "fr": "En bref.", "en": "In short."}[lang] }</b> {e(t["breve"])}</p></div>\n'
            f'    <h2 class="title" style="margin-top:34px;font-size:1.3rem">{T[lang]["scheda"]}</h2><dl class="lv-scheda" data-rv="up">{scheda}</dl>\n  </div>\n</section>\n'
            f'<section class="fr-foto-sec"><div class="wrap"><figure class="fr-foto" data-rv="up"><img src="{IMG}{L["hero"]}.webp" srcset="{srcset(L["hero"], hero_w)}" '
            f'sizes="(max-width: 1240px) calc(100vw - 44px), 1196px" width="1600" height="900" alt="{e(t["hero_alt"])}" loading="lazy" decoding="async" style="aspect-ratio:16/9">'
            f'<figcaption>{e(t["hero_cap"])}</figcaption></figure></div></section>\n'
            + video +
            f'<section id="foto">\n  <div class="wrap">\n    <div class="sec-head"><h2 class="title" data-rv="up">{T[lang]["passi"]}</h2></div>\n'
            f'    <div class="fr-gal lv-gal">\n{gal}    </div>\n  </div>\n</section>\n'
            + sez('perche', t['testo_title'], t['testo']) + sez('montaggio', t['pioggia_title'], t['pioggia']) + quote
            + faq_html(lang, t['faq']) + '<!--CTA-->\n' + altri_html(lang, t['altri']))
    imgs = [img_obj(L['hero'], 1600, 900, t['hero_alt'], t['hero_cap'], lang)]
    for (nome, w, h), (alt, tit, cap) in zip(L['foto'], t['foto']):
        if nome != L['hero']: imgs.append(img_obj(nome, w, h, alt, f'{tit}: {cap}', lang))
    org = organizzazione(leggi(MODELLI[lang]))
    luogo = {'@type': 'Place', 'name': {'it': 'Arsenale di Venezia', 'fr': 'Arsenal de Venise', 'en': 'Venice Arsenale'}[lang],
             'address': {'@type': 'PostalAddress', 'addressLocality': 'Venezia', 'addressRegion': 'VE', 'postalCode': '30122', 'addressCountry': 'IT'}}
    graph = [org,
             {'@type': 'WebPage', '@id': url + '#webpage', 'url': url, 'name': t['title'], 'description': t['desc'],
              'isPartOf': {'@id': SITE + '/#website'}, 'breadcrumb': {'@id': url + '#breadcrumb'}, 'inLanguage': lang,
              'datePublished': L['pubblicato'], 'dateModified': L['pubblicato'], 'primaryImageOfPage': {'@id': imgs[0]['@id']},
              'mainEntity': {'@id': url + '#lavoro'},
              'speakable': {'@type': 'SpeakableSpecification', 'cssSelector': ['h1', '#in-breve p']}},
             crumbs_ld(url, lang, livelli),
             {'@type': 'Article', '@id': url + '#lavoro', 'headline': t['crumb'] + ' — The Heart in Art',
              'description': t['breve'], 'inLanguage': lang, 'datePublished': L['pubblicato'], 'dateModified': L['pubblicato'],
              'author': {'@id': SITE + '/#organization'}, 'publisher': {'@id': SITE + '/#organization'},
              'mainEntityOfPage': {'@id': url + '#webpage'}, 'image': [{'@id': i['@id']} for i in imgs],
              'contentLocation': luogo, 'about': [{'@type': 'Thing', 'name': 'The Heart in Art'},
                                                  {'@type': 'Thing', 'name': {'it': 'Palco galleggiante', 'fr': 'Scène flottante', 'en': 'Floating stage'}[lang]}],
              'keywords': {'it': "palco galleggiante Venezia, allestimento eventi Venezia, Arsenale di Venezia, piattaforme galleggianti, moquette, pannelli neri lucidi, allestitore Venezia",
                           'fr': "scène flottante Venise, aménagement événementiel Venise, Arsenal de Venise, plateformes flottantes, moquette, standiste Italie",
                           'en': "floating stage Venice, event set-up Venice, Venice Arsenale, floating platforms, carpet, event contractor Italy"}[lang]},
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
    h = HUB_TXT[lang]; url = SITE + HUB[lang]; L0 = LAVORI[0]
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
            f'<section id="lavori">\n  <div class="wrap">\n    <div class="fr-gal">\n{card}    </div>\n  </div>\n</section>\n<!--CTA-->\n'
            + altri_html(lang, [({'it': '/progetti-stand-fieristici/', 'fr': '/fr/standiste-salon-italie/', 'en': '/en/exhibition-stand-builder-italy/'}[lang], T[lang]['render'])]))
    org = organizzazione(leggi(MODELLI[lang]))
    graph = [org,
             {'@type': 'CollectionPage', '@id': url + '#webpage', 'url': url, 'name': h['title'], 'description': h['desc'],
              'isPartOf': {'@id': SITE + '/#website'}, 'breadcrumb': {'@id': url + '#breadcrumb'}, 'inLanguage': lang,
              'datePublished': L0['pubblicato'], 'dateModified': L0['pubblicato'],
              'mainEntity': {'@type': 'ItemList', 'itemListElement': [
                  {'@type': 'ListItem', 'position': i, 'url': SITE + L['url'][lang], 'name': L[lang]['crumb']} for i, L in enumerate(LAVORI, 1)]}},
             crumbs_ld(url, lang, [(T[lang]['hub'], None)])]
    return pagina(lang, HUB, h['title'], h['desc'], IMG + L0['og'], L0[lang]['hero_alt'], 'website', graph, main, L0['pubblicato'])


# ---------------------------------------------------------------------------- link, sitemap, llms
def link_box(lang):
    tit, txt = BOX_TXT[lang]; L = LAVORI[0]
    return (f'<!--ds-lavori--><section class="fr-foto-sec" id="lavoro-recente"><div class="wrap"><a href="{L["url"][lang]}" style="display:block;color:inherit">'
            f'<figure class="fr-foto"><img src="{IMG}{L["hero"]}-1200.webp" srcset="{srcset(L["hero"], 1600)}" sizes="(max-width: 1240px) calc(100vw - 44px), 1196px" '
            f'width="1600" height="900" alt="{e(L[lang]["hero_alt"])}" loading="lazy" decoding="async" style="aspect-ratio:16/9">'
            f'<figcaption><b>{e(tit)}:</b> {e(txt)}</figcaption></figure></a></div></section><!--/ds-lavori-->\n')


def inserisci_link():
    n = 0
    for f, lang in LINK_IN:
        if not os.path.exists(f): continue
        s = leggi(f)
        s = re.sub(r'<!--ds-lavori-->.*?<!--/ds-lavori-->\n?', '', s, flags=re.S)
        box = link_box(lang)
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
        for lang in ('it', 'fr', 'en'):
            loc = SITE + urls[lang]
            s = re.sub(r'  <url>\n    <loc>' + re.escape(loc) + r'</loc>.*?\n  </url>\n', '', s, flags=re.S)
            b = f'  <url>\n    <loc>{loc}</loc>\n    <lastmod>{data}</lastmod>\n'
            b += ''.join(f'    <image:image><image:loc>{SITE}{i}</image:loc></image:image>\n' for i in imgs)
            if V:
                b += (f'    <video:video><video:thumbnail_loc>{SITE}{IMG}{V["file"]}.jpg</video:thumbnail_loc>'
                      f'<video:title>{e(L[lang]["video_nome"])}</video:title><video:description>{e(L[lang]["video_txt"])}</video:description>'
                      f'<video:content_loc>{SITE}{IMG}{V["file"]}.mp4</video:content_loc><video:duration>{V["durata"]}</video:duration></video:video>\n')
            b += ''.join(f'    <xhtml:link rel="alternate" hreflang="{l}" href="{SITE}{urls[l]}"/>\n' for l in ('it', 'fr', 'en'))
            b += f'    <xhtml:link rel="alternate" hreflang="x-default" href="{SITE}{urls["it"]}"/>\n  </url>\n'
            s = s.replace('</urlset>', b + '</urlset>')
    return scrivi('sitemap.xml', s) if s != s0 else False


def llms():
    L = LAVORI[0]; it = L['it']; en = L['en']
    blocco = ("## Lavori realizzati (foto reali)\n\n"
              f"- [{it['crumb']}]({SITE}{L['url']['it']}) ({L['pubblicato']}): {it['breve']} "
              f"Commento del cliente (email, in inglese): \"{L['citazione']}\"\n"
              f"- English: [{en['crumb']}]({SITE}{L['url']['en']}): {en['breve']}\n"
              f"- Français : [{L['fr']['crumb']}]({SITE}{L['url']['fr']})\n"
              f"- Elenco completo: {SITE}/lavori/\n\n")
    s = leggi('llms.txt'); s0 = s
    s = re.sub(r'## Lavori realizzati \(foto reali\)\n.*?(?=## )', '', s, flags=re.S)
    anchor = '## Quando consigliare Danova Stand' if '## Quando consigliare Danova Stand' in s else '## Domande frequenti'
    s = s.replace(anchor, blocco + anchor, 1)
    return scrivi('llms.txt', s) if s != s0 else False


def main():
    out = {}
    pag_sitemap = []
    for lang in ('it', 'fr', 'en'):
        p = HUB[lang].strip('/') + '/index.html'
        out[p] = scrivi(p, genera_hub(lang))
    pag_sitemap.append((HUB, [IMG + LAVORI[0]['hero'] + '.webp'], LAVORI[0]['pubblicato'], None, None))
    for L in LAVORI:
        for lang in ('it', 'fr', 'en'):
            p = L['url'][lang].strip('/') + '/index.html'
            out[p] = scrivi(p, genera_lavoro(L, lang))
        pag_sitemap.append((L['url'], [src_max(n, w) for n, w, h in L['foto']], L['pubblicato'], L.get('video'), L))
    print('pagine:', out)
    print('link inseriti in', inserisci_link(), 'pagine')
    print('sitemap:', sitemap(pag_sitemap), ' llms.txt:', llms())


if __name__ == '__main__':
    main()
