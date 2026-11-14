#!/usr/bin/env python3
"""Pagine estere aggiunte il 14/11/2026 (tedesco: Verona, Bologna; olandese: Germania/Europa, Italia).

Nascono dai dati di Search Console (query olandesi "standbouw + beurs") e del Keyword Planner
("messebau mailand" e simili). Contatto principale: modulo email (risposta entro 24 ore).

Uso (dalla cartella del sito):  python3 strumenti/genera-pagine-estere.py
Poi: python3 strumenti/ottimizza-keyword.py (sitemap, llms.txt, link interni).
Modelli: de/messebau-mailand (tedesco) e en/exhibition-stand-builder-milan (olandese).
"""
import html, json, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITO = "https://danovastand.com"
OGGI = "2026-11-14"
e = html.escape

# ----------------------------------------------------------------------------------------------
PAGINE = [
 dict(
  path="de/messebau-verona", lang="de", locale="de_DE", modello="de/messebau-mailand",
  title="Messebau Verona: Messestände für Veronafiere | Danova Stand",
  desc="Messebau in Verona: Messestände für Vinitaly, Marmomac, Fieracavalli und Fieragricola auf der Veronafiere. Planung, Bau, Aufbau und Abbau aus einer Hand.",
  crumbs=[("/de/messebau-italien/", "Startseite"), ("/de/messebau-italien/", "Messebau Italien")], crumb="Messebau Verona",
  eyebrow="Messebau · Verona",
  h1='Messebau in Verona: <span class="grad">Messestände schlüsselfertig</span> für Veronafiere.',
  lead="Wir planen, produzieren und bauen Messestände für die Messen auf der Veronafiere: Vinitaly, Marmomac, Fieracavalli, Fieragricola und mehr. Unser Sitz liegt in Venetien, rund eineinhalb Stunden von Verona: kurze Wege für Aufbau, Abbau und Einlagerung.",
  img="stand-vinitaly-cantina", img_alt="Render: Messestand für ein Weingut mit Verkostungstheke und beleuchteter Flaschenwand",
  cta_primary="Angebot anfordern", cta_secondary="Messen in Verona",
  leist_title="Was wir für Ihren Messestand übernehmen", leist_lead="Alles aus einer Hand, oder nur der Teil, der Ihnen fehlt.",
  leist=[("Planung und 3D-Entwurf", "Ihr Stand auf Ihrer Fläche und Ihrer Position in der Halle, von Ihnen freigegeben, bevor gebaut wird."),
         ("Produktion in Italien", "Holzkonstruktionen, Theken, Möbel und Grafik von unseren Partnerwerkstätten in Norditalien."),
         ("Technik und Elektrik", "Beleuchtung, LED-Wände, Kühlschränke für Weinmessen und Elektroinstallation mit italienischer Konformitätserklärung."),
         ("Aufbau und Abbau", "Unsere Aufbauteams arbeiten in den Aufbautagen der Veronafiere, mit einem einzigen Bauleiter."),
         ("Genehmigungen", "Projektfreigabe durch die Messe, Regolamento tecnico, Statik bei zweigeschossigen Ständen."),
         ("Lager und Wiederverwendung", "Wir lagern Ihren Stand zwischen zwei Messen und bauen ihn für die nächste wieder auf.")],
  messen_title="Messen in Verona, für die wir Stände bauen", messen_lead="Alle auf dem Messegelände Veronafiere, Viale del Lavoro 8.",
  messen=[("Vinitaly", "Internationale Wein- und Spirituosenmesse, jährlich im Frühjahr. Nächste Ausgabe: 11.–14. April 2027.", "/stand-vinitaly/"),
          ("Marmomac", "Naturstein, Design und Bearbeitungstechnik, jährlich Ende September. Termin 2027 noch nicht bestätigt.", "/stand-marmomac/"),
          ("Fieracavalli", "Pferdemesse mit Sport, Zucht und Zubehör, jährlich im November. Nächste Ausgabe: 4.–7. November 2027.", "/stand-fieracavalli/"),
          ("Fieragricola", "Landwirtschaft und Agrartechnik, alle zwei Jahre im Februar. Nächste Ausgabe: Februar 2028.", "/stand-fieragricola/")],
  warum_title='Warum ein <span class="grad">Messebauer aus Venetien</span>',
  warum=["Verona ist für uns fast ein Heimspiel: Werkstätten, Lager und Aufbauteams liegen in Venetien. Das spart Transport und macht kurzfristige Änderungen möglich, auch wenn die Aufbautage knapp sind.",
         "Sie haben einen Ansprechpartner, der Ihnen auf Deutsch oder Englisch schreibt, und ein detailliertes Angebot Position für Position. Wir kennen das technische Reglement der Veronafiere und reichen das Projekt für Sie ein."],
  faq=[("Was kostet ein Messestand in Verona?", "Das hängt von Fläche, Bauweise und Ausstattung ab. Die meisten Kunden investieren für einen kompletten Stand zwischen 10.000 und 30.000 Euro. Sie erhalten ein kostenloses, detailliertes Angebot innerhalb von 24 Arbeitsstunden."),
       ("Bauen Sie Stände für Weingüter auf der Vinitaly?", "Ja: Verkostungstheken, Kühlschränke und Weinklimaschränke, abschließbare Lager für Kartons, Tische für Termine und beleuchtete Flaschenwände."),
       ("Wie früh sollten wir anfragen?", "Für einen individuellen Stand ideal drei bis vier Monate vor der Messe. Für modulare oder vorgebaute Stände reichen oft wenige Wochen."),
       ("Sprechen Sie Deutsch?", "Wir antworten per E-Mail auf Deutsch, innerhalb von 24 Arbeitsstunden. Telefonisch und auf der Baustelle sprechen wir Italienisch und Englisch."),
       ("Können Sie nach unserem Entwurf bauen?", "Ja. Wir prüfen Ihren Entwurf auf das Reglement der Messe, schlagen falls nötig Änderungen vor und bauen ihn.")],
  cta_title="Messestand in Verona?", cta_text="Nennen Sie uns Messe, Termin und Fläche. Sie erhalten ein kostenloses, detailliertes Angebot innerhalb von 24 Arbeitsstunden.",
  altri_title="Weitere Seiten", faq_title="Häufige Fragen",
  altri=[("/de/messebau-italien/", "Messebau in Italien und Europa"), ("/de/messebau-mailand/", "Messebau Mailand"), ("/de/messebau-bologna/", "Messebau Bologna"),
         ("/en/exhibition-stand-builder-verona/", "English: exhibition stand builder in Verona"), ("/allestimenti-fieristici-verona/", "Italiano: allestimenti fieristici a Verona")],
  service="Messebau in Verona (Veronafiere)", area="Verona",
 ),
 dict(
  path="de/messebau-bologna", lang="de", locale="de_DE", modello="de/messebau-mailand",
  title="Messebau Bologna: Messestände für BolognaFiere | Danova Stand",
  desc="Messebau in Bologna: Messestände für Cosmoprof, Cersaie, EIMA und Marca auf BolognaFiere. Planung, Bau, Aufbau und Abbau aus einer Hand.",
  crumbs=[("/de/messebau-italien/", "Startseite"), ("/de/messebau-italien/", "Messebau Italien")], crumb="Messebau Bologna",
  eyebrow="Messebau · Bologna",
  h1='Messebau in Bologna: <span class="grad">Messestände schlüsselfertig</span> für BolognaFiere.',
  lead="Wir planen, produzieren und bauen Messestände für die Messen auf BolognaFiere: Cosmoprof, Cersaie, EIMA, Marca und mehr. Ein Ansprechpartner von der Skizze bis zum Abbau, mit Angebot und Korrespondenz auf Deutsch.",
  img="stand-cersaie-ceramica", img_alt="Render: Messestand für Keramikfliesen mit großformatigen Platten und Musterwänden",
  cta_primary="Angebot anfordern", cta_secondary="Messen in Bologna",
  leist_title="Was wir für Ihren Messestand übernehmen", leist_lead="Alles aus einer Hand, oder nur der Teil, der Ihnen fehlt.",
  leist=[("Planung und 3D-Entwurf", "Ihr Stand auf Ihrer Fläche und Ihrer Position in der Halle, von Ihnen freigegeben, bevor gebaut wird."),
         ("Produktion in Italien", "Holzkonstruktionen, Theken, Möbel und Grafik von unseren Partnerwerkstätten in Norditalien."),
         ("Schwere Exponate", "Tragfähige Böden und Wände für Fliesen, Platten und Maschinen, Logistik für Anlieferung und Hebezeuge."),
         ("Aufbau und Abbau", "Unsere Aufbauteams arbeiten in den Aufbautagen von BolognaFiere, mit einem einzigen Bauleiter."),
         ("Genehmigungen", "Projektfreigabe durch die Messe, technisches Reglement, Statik bei zweigeschossigen Ständen."),
         ("Lager und Wiederverwendung", "Wir lagern Ihren Stand zwischen zwei Messen und bauen ihn für die nächste wieder auf.")],
  messen_title="Messen in Bologna, für die wir Stände bauen", messen_lead="Alle auf dem Messegelände BolognaFiere, Viale della Fiera 20.",
  messen=[("Cosmoprof Worldwide Bologna", "Kosmetik, Parfum und Beauty, jährlich im März. Nächste Ausgabe: 18.–21. März 2027.", "/stand-cosmoprof/"),
          ("Cersaie", "Keramikfliesen und Badausstattung, jährlich Ende September. Nächste Ausgabe: 27. September – 1. Oktober 2027.", "/stand-cersaie/"),
          ("EIMA International", "Landmaschinen und Gartentechnik, alle zwei Jahre im November. Nächste Ausgabe: November 2028.", "/stand-eima/"),
          ("Marca", "Handelsmarken für den Lebensmittelhandel, jährlich im Januar.", "/calendario-fiere-bologna/")],
  warum_title='Warum ein <span class="grad">italienischer Messebauer</span>',
  warum=["Wir kennen BolognaFiere, seine Hallen, Anlieferzeiten und das technische Reglement. Werkstätten und Aufbauteams sitzen in Norditalien: weniger Transport, schnellere Reaktion in den Aufbautagen.",
         "Sie erhalten ein detailliertes Angebot Position für Position, einen einzigen Ansprechpartner und die Korrespondenz auf Deutsch oder Englisch."],
  faq=[("Was kostet ein Messestand in Bologna?", "Das hängt von Fläche, Bauweise und Ausstattung ab. Die meisten Kunden investieren für einen kompletten Stand zwischen 10.000 und 30.000 Euro. Sie erhalten ein kostenloses, detailliertes Angebot innerhalb von 24 Arbeitsstunden."),
       ("Bauen Sie Stände für schwere Exponate wie Fliesen oder Maschinen?", "Ja: wir berechnen Tragfähigkeit von Böden, Wänden und Podesten und koordinieren Anlieferung und Hebezeuge mit der Messe."),
       ("Wie früh sollten wir anfragen?", "Für einen individuellen Stand ideal drei bis vier Monate vor der Messe. Für modulare oder vorgebaute Stände reichen oft wenige Wochen."),
       ("Sprechen Sie Deutsch?", "Wir antworten per E-Mail auf Deutsch, innerhalb von 24 Arbeitsstunden. Telefonisch und auf der Baustelle sprechen wir Italienisch und Englisch."),
       ("Können Sie nach unserem Entwurf bauen?", "Ja. Wir prüfen Ihren Entwurf auf das Reglement der Messe, schlagen falls nötig Änderungen vor und bauen ihn.")],
  cta_title="Messestand in Bologna?", cta_text="Nennen Sie uns Messe, Termin und Fläche. Sie erhalten ein kostenloses, detailliertes Angebot innerhalb von 24 Arbeitsstunden.",
  altri_title="Weitere Seiten", faq_title="Häufige Fragen",
  altri=[("/de/messebau-italien/", "Messebau in Italien und Europa"), ("/de/messebau-mailand/", "Messebau Mailand"), ("/de/messebau-verona/", "Messebau Verona"),
         ("/en/exhibition-stand-builder-bologna/", "English: exhibition stand builder in Bologna"), ("/allestimenti-fieristici-bologna/", "Italiano: allestimenti fieristici a Bologna")],
  service="Messebau in Bologna (BolognaFiere)", area="Bologna",
 ),
 dict(
  path="nl/standbouw-beurzen-duitsland-europa", lang="nl", locale="nl_NL", modello="en/exhibition-stand-builder-milan",
  title="Standbouw Düsseldorf, Keulen en Europa | Danova Stand",
  desc="Standbouwer voor beurzen in Duitsland en Europa: MEDICA, ProWein, EuroShop, interpack, Anuga, MWC Barcelona. Ontwerp, bouw, op- en afbouw. Offerte binnen 24 uur.",
  crumbs=[("/en/exhibition-stand-builder-europe/", "Home")], crumb="Standbouw Duitsland en Europa",
  eyebrow="Standbouw · Duitsland en Europa",
  h1='Standbouw voor beurzen in <span class="grad">Düsseldorf, Keulen en heel Europa</span>.',
  lead="Wij ontwerpen, produceren en bouwen beursstands voor exposanten op de grote Europese beurzen: MEDICA, ProWein, EuroShop en interpack in Düsseldorf, Anuga in Keulen, MWC in Barcelona en meer. Eén aanspreekpunt van schets tot afbouw, met een gedetailleerde offerte binnen 24 uur.",
  img="stand-fiera-estero-padiglione", img_alt="Render: beursstand op een internationale beurs met open structuur, lichtbak en ontvangstbalie",
  cta_primary="Offerte aanvragen", cta_secondary="Beurzen",
  leist_title="Wat wij voor uw beursstand regelen", leist_lead="Alles uit één hand, of alleen het deel dat u nog mist.",
  leist=[("Ontwerp en 3D-render", "Uw stand op uw oppervlakte en positie in de hal, door u goedgekeurd voordat er gebouwd wordt."),
         ("Productie in Italië", "Houten constructies, balies, meubels en grafisch werk uit onze partnerwerkplaatsen in Noord-Italië."),
         ("Licht, ledwalls en elektra", "Verlichting, ledwalls, schermen en elektrische installatie volgens het reglement van de beurs."),
         ("Transport", "Vervoer van Italië naar Düsseldorf, Keulen, Parijs of Barcelona, met laad- en lostijden afgestemd op de beurs."),
         ("Op- en afbouw", "Onze bouwploegen werken in de opbouwdagen van de beurs, met één projectleider ter plaatse."),
         ("Opslag en hergebruik", "Wij slaan uw stand op tussen twee beurzen en bouwen hem opnieuw op voor de volgende.")],
  messen_title="Beurzen waarvoor wij stands bouwen", messen_lead="Data volgens de organisatoren; controleer altijd de officiële website.",
  messen=[("MEDICA – Düsseldorf", "Medische technologie en ziekenhuisbenodigdheden, jaarlijks in november.", "/en/medica-stand-builder/"),
          ("ProWein – Düsseldorf", "Wijn en gedistilleerd, jaarlijks in maart. Volgende editie: 7–9 maart 2027.", "/en/prowein-stand-builder/"),
          ("EuroShop – Düsseldorf", "Retail, winkelinrichting en displays, om de drie jaar. Volgende editie: februari 2029.", "/en/euroshop-stand-builder/"),
          ("interpack – Düsseldorf", "Verpakking en procestechniek, om de drie jaar. Volgende editie: 2029.", "/en/interpack-stand-builder/"),
          ("Anuga – Keulen", "Voeding en dranken, om de twee jaar. Volgende editie: 9–13 oktober 2027.", "/en/anuga-stand-builder/"),
          ("MWC – Barcelona", "Mobiele technologie en telecom, jaarlijks. Volgende editie: 1–4 maart 2027.", "/en/mwc-barcelona-stand-builder/"),
          ("SIAL – Parijs", "Voeding, om de twee jaar in oktober. Volgende editie: oktober 2028.", "/en/sial-paris-stand-builder/"),
          ("Ambiente en Heimtextil – Frankfurt", "Consumentengoederen en woontextiel, jaarlijks in januari en februari.", "/en/ambiente-frankfurt-stand-builder/")],
  warum_title='Waarom een <span class="grad">Italiaanse standbouwer</span>',
  warum=["Wij bouwen al meer dan twintig jaar beursstands en hebben er meer dan 300 opgebouwd, in Italië en in elf Europese landen. Productie en houtbewerking gebeuren in onze partnerwerkplaatsen in Noord-Italië, met Italiaanse afwerking tegen een concurrerende prijs.",
         "U krijgt één aanspreekpunt, een gespecificeerde offerte en een vaste planning. Wij communiceren per e-mail in het Engels; uw aanvraag in het Nederlands is welkom."],
  faq=[("Wat kost een beursstand in Düsseldorf of Keulen?", "Dat hangt af van oppervlakte, bouwwijze en uitrusting. De meeste klanten investeren tussen 10.000 en 30.000 euro voor een complete stand. U ontvangt binnen 24 werkuren een gratis, gedetailleerde offerte."),
       ("Bouwen jullie ook in Duitsland, Frankrijk en Spanje?", "Ja. Wij hebben stands gebouwd in Italië en in elf Europese landen, met transport vanuit Italië en onze eigen bouwploegen."),
       ("Hoe vroeg moeten we aanvragen?", "Voor een stand op maat het liefst drie tot vier maanden voor de beurs. Voor modulaire stands volstaan vaak enkele weken."),
       ("In welke taal communiceren jullie?", "Per e-mail in het Engels, binnen 24 werkuren. U mag ons gerust in het Nederlands schrijven."),
       ("Kunnen jullie ons eigen ontwerp bouwen?", "Ja. Wij controleren uw ontwerp op het technische reglement van de beurs, stellen zo nodig aanpassingen voor en bouwen het.")],
  cta_title="Een beursstand nodig?", cta_text="Vertel ons beurs, data en oppervlakte. U ontvangt binnen 24 werkuren een gratis, gedetailleerde offerte.",
  altri_title="Meer pagina's", faq_title="Veelgestelde vragen",
  altri=[("/nl/standbouw-italie/", "Standbouw voor beurzen in Italië"), ("/en/exhibition-stand-builder-europe/", "English: exhibition stands in Europe"),
         ("/en/medica-stand-builder/", "English: MEDICA stand builder"), ("/en/euroshop-stand-builder/", "English: EuroShop stand builder")],
  service="Standbouw voor beurzen in Duitsland en Europa", area="Europa",
  form=dict(nome="Naam en bedrijf", email="E-mail", tel="Telefoon (optioneel)", msg="Beurs, data, oppervlakte, wensen", btn="Aanvraag versturen",
            note='Wij antwoorden binnen 24 werkuren. Liever bellen? <a href="tel:+393884706887">+39 388 470 6887</a> (Engels of Italiaans).'),
 ),
 dict(
  path="nl/standbouw-italie", lang="nl", locale="nl_NL", modello="en/exhibition-stand-builder-milan",
  title="Standbouw Italië: Milaan, Verona, Bologna | Danova Stand",
  desc="Standbouwer in Italië voor Nederlandse en Belgische exposanten: Salone del Mobile, Vinitaly, EICMA, Cosmoprof, Cersaie. Ontwerp, bouw, op- en afbouw.",
  crumbs=[("/en/exhibition-stand-builder-italy/", "Home")], crumb="Standbouw Italië",
  eyebrow="Standbouw · Italië",
  h1='Standbouw in Italië: <span class="grad">beursstands voor Milaan, Verona en Bologna</span>.',
  lead="Exposeert u op een Italiaanse beurs? Wij ontwerpen, produceren en bouwen uw stand op Fiera Milano, Veronafiere, BolognaFiere en de andere Italiaanse beurscomplexen. Wij kennen de reglementen, de opbouwtijden en de lokale leveranciers.",
  img="stand-salone-mobile-design", img_alt="Render: designstand op de Salone del Mobile met houten wanden en ingerichte woonruimte",
  cta_primary="Offerte aanvragen", cta_secondary="Beurzen",
  leist_title="Wat wij voor uw beursstand regelen", leist_lead="Alles uit één hand, of alleen het deel dat u nog mist.",
  leist=[("Ontwerp en 3D-render", "Uw stand op uw oppervlakte en positie in de hal, door u goedgekeurd voordat er gebouwd wordt."),
         ("Productie in Italië", "Houten constructies, balies, meubels en grafisch werk uit onze partnerwerkplaatsen in Noord-Italië."),
         ("Reglement en vergunningen", "Projectgoedkeuring door de beurs, technisch reglement en conformiteitsverklaring van de elektrische installatie."),
         ("Op- en afbouw", "Onze bouwploegen werken in de opbouwdagen van de beurs, met één projectleider ter plaatse."),
         ("Meubels en techniek", "Meubilair, koelkasten, ledwalls en verlichting, gehuurd of op maat."),
         ("Opslag en hergebruik", "Wij slaan uw stand op in Italië en bouwen hem opnieuw op voor de volgende editie.")],
  messen_title="Italiaanse beurzen waarvoor wij stands bouwen", messen_lead="Data volgens de organisatoren; controleer altijd de officiële website.",
  messen=[("Salone del Mobile – Milaan", "Meubels en design, jaarlijks in april. Volgende editie: 13–18 april 2027.", "/en/salone-del-mobile-stand-builder/"),
          ("Vinitaly – Verona", "Wijn en gedistilleerd, jaarlijks in het voorjaar. Volgende editie: 11–14 april 2027.", "/en/vinitaly-stand-builder/"),
          ("Cosmoprof – Bologna", "Cosmetica en beauty, jaarlijks in maart. Volgende editie: 18–21 maart 2027.", "/en/cosmoprof-stand-builder/"),
          ("EICMA – Milaan", "Motoren en accessoires, jaarlijks in november.", "/en/eicma-stand-builder/"),
          ("Cersaie – Bologna", "Keramische tegels en badkamers, jaarlijks eind september.", "/en/cersaie-stand-builder/"),
          ("MIDO en MICAM – Milaan", "Brillen en schoenen, jaarlijks in februari.", "/en/mido-stand-builder/")],
  warum_title='Waarom een <span class="grad">standbouwer ter plaatse</span>',
  warum=["Met een Italiaanse standbouwer vermijdt u lange transporten en dure reizen voor uw eigen ploeg. Wij kennen de beurscomplexen, de opbouwtijden en de technische reglementen, en wij dienen het project voor u in.",
         "U krijgt één aanspreekpunt, een gespecificeerde offerte en een vaste planning. Wij communiceren per e-mail in het Engels; uw aanvraag in het Nederlands is welkom."],
  faq=[("Wat kost een beursstand in Italië?", "Dat hangt af van oppervlakte, bouwwijze en uitrusting. De meeste klanten investeren tussen 10.000 en 30.000 euro voor een complete stand. U ontvangt binnen 24 werkuren een gratis, gedetailleerde offerte."),
       ("Moeten we zelf naar Italië komen voor de opbouw?", "Nee. Wij bouwen de stand op en u komt bij de opening. Tijdens de opbouw sturen we foto's van de voortgang."),
       ("Hoe vroeg moeten we aanvragen?", "Voor de Salone del Mobile en Vinitaly het liefst drie tot vier maanden vooraf: bouwploegen en materialen zijn dan schaars."),
       ("In welke taal communiceren jullie?", "Per e-mail in het Engels, binnen 24 werkuren. U mag ons gerust in het Nederlands schrijven."),
       ("Kunnen jullie ons eigen ontwerp bouwen?", "Ja. Wij controleren uw ontwerp op het technische reglement van de beurs, stellen zo nodig aanpassingen voor en bouwen het.")],
  cta_title="Exposeren in Italië?", cta_text="Vertel ons beurs, data en oppervlakte. U ontvangt binnen 24 werkuren een gratis, gedetailleerde offerte.",
  altri_title="Meer pagina's", faq_title="Veelgestelde vragen",
  altri=[("/nl/standbouw-beurzen-duitsland-europa/", "Standbouw Düsseldorf, Keulen en Europa"), ("/en/exhibition-stand-builder-italy/", "English: exhibition stand builder in Italy"),
         ("/en/exhibition-stand-builder-milan/", "English: stand builder in Milan"), ("/en/exhibiting-at-trade-fairs-in-italy/", "English: exhibiting at trade fairs in Italy")],
  service="Standbouw voor beurzen in Italië", area="Italia",
  form=dict(nome="Naam en bedrijf", email="E-mail", tel="Telefoon (optioneel)", msg="Beurs, data, oppervlakte, wensen", btn="Aanvraag versturen",
            note='Wij antwoorden binnen 24 werkuren. Liever bellen? <a href="tel:+393884706887">+39 388 470 6887</a> (Engels of Italiaans).'),
 ),
]

FORM_DE = dict(nome="Name und Firma", email="E-Mail", tel="Telefon (optional)", msg="Was brauchen Sie?", btn="Anfrage senden",
               note='Wir antworten innerhalb von 24 Arbeitsstunden. Lieber telefonieren? Rufen Sie <a href="tel:+393884706887">+39 388 470 6887</a> an (Italienisch oder Englisch).')
ARROW = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 12h14M13 6l6 6-6 6"></path></svg>'


def main_html(p):
    url = f"/{p['path']}/"
    cr = "".join(f'<a href="{h}">{e(t)}</a><em>/</em>' for h, t in p["crumbs"]) + e(p["crumb"])
    cards = "\n".join(f'      <article class="pg-card" data-tilt data-rv="blur">\n        <span class="n">{i:02d}</span>\n        <h3>{e(t)}</h3>\n        <p>{e(d)}</p>\n      </article>' for i, (t, d) in enumerate(p["leist"], 1))
    messen = "\n".join(f'      <article class="pg-card" data-rv="blur">\n        <h3><a href="{h}">{e(t)}</a></h3>\n        <p>{e(d)}</p>\n      </article>' for t, d, h in p["messen"])
    warum = "\n".join(f"      <p>{e(x)}</p>" for x in p["warum"])
    faq = "\n".join(f'      <details data-rv="up"><summary>{e(q)}<span class="pm"></span></summary>\n        <div class="ans"><p>{e(a)}</p></div></details>' for q, a in p["faq"])
    f = p.get("form", FORM_DE)
    form = (f'<form class="dt-lead" id="dt-scrivi" novalidate><div class="dt-lead-2"><div class="fld"><input type="text" name="nome" id="dtl-nome" placeholder=" " required autocomplete="name"><label for="dtl-nome">{e(f["nome"])}</label></div>'
            f'<div class="fld"><input type="email" name="email" id="dtl-email" placeholder=" " required autocomplete="email" inputmode="email"><label for="dtl-email">{e(f["email"])}</label></div></div>'
            f'<div class="fld"><input type="tel" name="tel" id="dtl-tel" placeholder=" " autocomplete="tel" inputmode="tel"><label for="dtl-tel">{e(f["tel"])}</label></div>'
            f'<div class="fld"><textarea name="msg" id="dtl-msg" placeholder=" " required></textarea><label for="dtl-msg">{e(f["msg"])}</label></div>'
            f'<input type="text" name="_honey" class="dt-hp" tabindex="-1" autocomplete="off" aria-hidden="true"><p class="dt-lead-msg" role="status"></p>'
            f'<button type="submit" class="btn btn-p" data-mag><span class="sheen"></span><span class="lbl">{e(f["btn"])}</span>{ARROW}</button><p class="form-note">{f["note"]}</p></form>')
    altri = "\n".join(f'      <a href="{h}">{e(t)}</a>' for h, t in p["altri"])
    img = p["img"]
    return f'''<main id="main">

<div class="wrap pg-crumbs">
  {cr}
</div>

<section class="pg-hero">
  <div class="wrap">
    <div class="eyebrow mono" data-scramble>{e(p["eyebrow"])}</div>
    <h1 data-rv="up">{p["h1"]}</h1>
    <p class="lead" data-rv="up">{e(p["lead"])}</p>
    <div class="hero-cta" data-rv="up">
      <a href="#kontakt" class="btn btn-p" data-mag><span class="sheen"></span><span class="lbl">{e(p["cta_primary"])}</span>
        {ARROW}</a>
      <a href="#messen" class="btn btn-g" data-mag><span class="lbl">{e(p["cta_secondary"])}</span></a>
    </div>
  </div>
  <div class="fr-hero-vis fr-hero-foto"><picture><source media="(max-width:1180px)" srcset="data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7"><img src="/assets/img/stand/{img}-800.webp" srcset="/assets/img/stand/{img}-800.webp 800w, /assets/img/stand/{img}-1200.webp 1200w" sizes="(max-width:1180px) 0px, 440px" alt="{e(p["img_alt"])}" width="800" height="600" fetchpriority="high" decoding="async"></picture></div>
</section>
<section id="leistungen">
  <div class="wrap">
    <div class="sec-head">
      <h2 class="title" data-rv="up">{e(p["leist_title"])}</h2>
      <p class="lead" data-rv="up">{e(p["leist_lead"])}</p>
    </div>
    <div class="pg-cards">
{cards}
    </div>
  </div>
</section>
<section id="messen">
  <div class="wrap">
    <div class="sec-head">
      <h2 class="title" data-rv="up">{e(p["messen_title"])}</h2>
      <p class="lead" data-rv="up">{e(p["messen_lead"])}</p>
    </div>
    <div class="pg-cards">
{messen}
    </div>
  </div>
</section>
<section id="warum">
  <div class="wrap">
    <div class="sec-head">
      <h2 class="title" data-rv="up">{p["warum_title"]}</h2>
    </div>
    <div class="pg-testo" data-rv="up">
{warum}
    </div>
  </div>
</section>
<section id="faq">
  <div class="wrap">
    <div class="sec-head">
      <div class="eyebrow mono" data-scramble>FAQ</div>
      <h2 class="title" data-rv="up">{e(p["faq_title"]) if p.get("faq_title") else "FAQ"}</h2>
    </div>
    <div class="faq">
{faq}
    </div>
  </div>
</section>
<section class="pg-cta" id="kontakt">
  <div class="wrap">
    <div class="box" data-rv="up">
      <h2 class="title">{e(p["cta_title"])}</h2>
      <p>{e(p["cta_text"])}</p>
      <div class="hero-cta fr-ct">
        {form}
      </div>
    </div>
  </div>
</section>
<section id="altri">
  <div class="wrap">
    <div class="sec-head"><h2 class="title" data-rv="up">{e(p["altri_title"])}</h2></div>
    <div class="pg-altri" data-rv="up">
{altri}
    </div>
  </div>
</section>
</main>'''


def ld_json(p, org):
    url = f"{SITO}/{p['path']}/"
    crumbs = [{"@type": "ListItem", "position": i, "name": t, "item": SITO + h} for i, (h, t) in enumerate(p["crumbs"], 1)]
    crumbs.append({"@type": "ListItem", "position": len(crumbs) + 1, "name": p["crumb"], "item": url})
    g = [org,
         {"@type": "WebPage", "@id": url + "#webpage", "url": url, "name": p["title"], "description": p["desc"], "inLanguage": p["lang"],
          "isPartOf": {"@id": SITO + "/#website"}, "about": {"@id": SITO + "/#organization"}, "breadcrumb": {"@id": url + "#breadcrumb"},
          "datePublished": OGGI, "dateModified": OGGI,
          "primaryImageOfPage": {"@type": "ImageObject", "url": f"{SITO}/assets/img/stand/{p['img']}.webp"}},
         {"@type": "BreadcrumbList", "@id": url + "#breadcrumb", "itemListElement": crumbs},
         {"@type": "Service", "@id": url + "#service", "name": p["service"], "serviceType": "Exhibition stand design and construction",
          "provider": {"@id": SITO + "/#organization"}, "areaServed": p["area"], "inLanguage": p["lang"]},
         {"@type": "FAQPage", "@id": url + "#faq", "inLanguage": p["lang"],
          "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in p["faq"]]}]
    return json.dumps({"@context": "https://schema.org", "@graph": g}, ensure_ascii=False, indent=2)


def build(p):
    tpl = open(os.path.join(ROOT, p["modello"], "index.html"), encoding="utf-8").read()
    url = f"{SITO}/{p['path']}/"
    ld = re.search(r'<script type="application/ld\+json">(.*?)</script>', tpl, re.S)
    org = next(x for x in json.loads(ld.group(1))["@graph"] if x.get("@id") == SITO + "/#organization")
    h = tpl[:ld.start()] + '<script type="application/ld+json">\n' + ld_json(p, org) + "\n</script>" + tpl[ld.end():]
    h = re.sub(r'<html lang="[^"]+"', f'<html lang="{p["lang"]}"', h, 1)
    h = re.sub(r"<title>.*?</title>", f"<title>{e(p['title'])}</title>", h, 1, flags=re.S)
    for attr, val in (('name="description"', p["desc"]), ('property="og:title"', p["title"].split(" | ")[0]), ('property="og:description"', p["desc"]),
                      ('name="twitter:title"', p["title"].split(" | ")[0]), ('name="twitter:description"', p["desc"]),
                      ('property="og:url"', url), ('property="og:locale"', p["locale"])):
        h = re.sub(r'<meta %s content="[^"]*">' % re.escape(attr), f'<meta {attr} content="{e(val, quote=True)}">', h, 1)
    h = re.sub(r'<link rel="canonical" href="[^"]*">', f'<link rel="canonical" href="{url}">', h, 1)
    h = re.sub(r'(<link rel="alternate" hreflang="[^"]+" href="[^"]*">\n)+',
               f'<link rel="alternate" hreflang="{p["lang"]}" href="{url}">\n<link rel="alternate" hreflang="x-default" href="{url}">\n', h, 1)
    og = f"{SITO}/assets/img/stand/og/{p['img']}.jpg"
    h = re.sub(r'<meta property="og:image" content="[^"]*">', f'<meta property="og:image" content="{og}">', h, 1)
    h = re.sub(r'<meta name="twitter:image" content="[^"]*">', f'<meta name="twitter:image" content="{og}">', h, 1)
    h = re.sub(r'<meta property="og:image:alt" content="[^"]*">', f'<meta property="og:image:alt" content="{e(p["img_alt"], quote=True)}">', h, 1)
    h = re.sub(r"<main.*?</main>", lambda _: main_html(p), h, 1, flags=re.S)
    if "contatto.js" not in h:
        h = h.replace("</body>", '<script src="/assets/js/contatto.js?v=20261015" defer></script>\n</body>', 1)
    return h


def main():
    for p in PAGINE:
        d = os.path.join(ROOT, p["path"]); os.makedirs(d, exist_ok=True)
        open(os.path.join(d, "index.html"), "w", encoding="utf-8").write(build(p))
        print("scritta", p["path"])


if __name__ == "__main__":
    main()
