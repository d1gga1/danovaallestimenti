#!/usr/bin/env python3
"""24/11/2026: aggiunge una sezione di testo esclusivo (id="pratico") alle pagine EN per paese
e alle pagine EN per citta', che condividevano troppo testo tra loro (rischio "duplicati").
Idempotente: se la sezione c'e' gia' la sostituisce. Rilanciare dopo aver rigenerato queste pagine.
Uso: python3 strumenti/arricchisci-pagine-en.py"""
import os, re, html
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

PAESI = {
 "exhibition-stand-builder-for-pakistani-companies": ("Planning your stand from Pakistan", "What changes when the stand is planned from Lahore, Karachi or Sialkot and built in Europe.", [
  ("Time difference.", "Pakistan is four hours ahead of Italy in winter and three in summer. We schedule calls in your late morning and answer WhatsApp messages the same working day."),
  ("Surgical and medical instruments.", "Small, precise products need lit glass showcases at eye level, lockable drawers for samples and a quiet table where buyers can handle instruments under good light."),
  ("Home textiles and apparel.", "Buyers want to touch the fabric: we plan hanging rails, folded stacks on low tables and lighting with high colour rendering, so colours look the same as in your catalogue."),
  ("Leather and sports goods.", "Slatwall panels, adjustable shelves and a few mannequins or ball displays let you change the layout between seasons without rebuilding the stand."),
  ("Visa timing.", "Schengen visa appointments can be busy before the big fairs. Ask the organiser for the invitation letter as soon as your space is confirmed; we plan the build-up around your team's arrival date."),
  ("Samples and exhibits.", "Your forwarder ships the goods; we share the venue's unloading slots and the stand address so the boxes reach the right hall on the right day.")]),
 "exhibition-stand-builder-for-bangladeshi-companies": ("Planning your stand from Bangladesh", "Practical points for manufacturers from Dhaka and Chattogram exhibiting in Europe.", [
  ("Time difference.", "Bangladesh is five hours ahead of Italy in winter and four in summer. We keep one shared timeline so decisions do not wait a day for an answer."),
  ("Garments and home textiles.", "Sourcing buyers compare quality fast: we design a sample wall with your best ranges, a fabric library with swatches and two or three meeting tables for price talks."),
  ("Jute and natural products.", "Natural materials look best on a calm stand: light wood, plain walls and warm light, with products at different heights instead of crowded shelves."),
  ("Frozen fish and food.", "Refrigerated counters and freezers need electrical power ordered from the organiser in advance; we calculate the load and include it in the technical drawings."),
  ("Leather and footwear.", "At MICAM and Lineapelle buyers look at details: shoe shelves with spot lights, a mirror and a seat for fitting, and a lockable store for samples."),
  ("Visa timing.", "Apply for Schengen visas as soon as the organiser sends the invitation letter; we fix the build-up dates around the day your team lands.")]),
 "exhibition-stand-builder-for-indian-companies": ("Planning your stand from India", "What Indian exhibitors usually ask us before their first stand in Europe.", [
  ("Time difference.", "India is four and a half hours ahead of Italy in winter and three and a half in summer: your afternoon is our morning, which makes daily calls easy."),
  ("Granite, marble and stone.", "Heavy slabs need floor-load checks, forklift slots during build-up and strong display frames. At Marmomac we plan the stand around the slab sizes you want to show."),
  ("Spices, rice and food.", "Tasting areas must follow the organiser's hygiene rules: a washable counter, a sink if required and storage behind closed doors keep the stand compliant."),
  ("Gems and jewellery.", "At VicenzaOro security comes first: lockable showcases with safety glass, a private room for buyers and controlled access to the back store."),
  ("Textiles at Heimtextil.", "Large fabric collections need hanging systems, light walls and lighting with high colour rendering so buyers see the true colour of every design."),
  ("Working with your pavilion.", "If your company sits in a national pavilion, we follow the pavilion's rules and upgrade your space without changing its common look.")]),
 "exhibition-stand-builder-for-chinese-companies": ("Planning your stand from China", "Points Chinese exhibitors should settle early with a European stand builder.", [
  ("Time difference.", "China is seven hours ahead of Italy in winter and six in summer. We reply in Chinese and keep important technical decisions confirmed in writing."),
  ("European fire rules.", "Materials and printed graphics must meet the fire classification required by the venue. Graphics printed in China often lack the right certificate, so we usually print them in Europe."),
  ("Design files from your agency.", "Send us the drawings in DWG or PDF with dimensions. We check heights, open sides and electrical layout against the venue rules before production."),
  ("Motorcycles and e-bikes.", "At EICMA vehicles need low platforms, ramps and enough space for visitors to sit on them; we size the stand around the models you bring."),
  ("Electronics and appliances.", "Many screens and working products mean high power demand: we calculate the load and order the right connection from the organiser."),
  ("Several fairs a year.", "If you exhibit at IFA, Ambiente and Hannover Messe, one modular stand can be stored in our warehouse and rebuilt in different sizes.")]),
}

CITTA = {
 "exhibition-stand-builder-vicenza": ("Getting to the Vicenza fairground", [
  ("Location.", "Fiera di Vicenza is on the west side of the city, a few minutes from the Vicenza Ovest exit of the A4 motorway, which makes truck access straightforward."),
  ("Airports.", "Verona airport is about 50 km away and Venice about 80 km: most exhibitors fly into one and drive or take the train to Vicenza."),
  ("Hotels.", "During VicenzaOro hotels in Vicenza fill up early; many teams stay in Padua or Verona and commute by train."),
  ("Build-up days.", "Jewellery shows have short build-up windows and strict security at the gates, so every delivery is booked with its time slot.")]),
 "exhibition-stand-builder-verona": ("Getting to Veronafiere", [
  ("Location.", "Veronafiere is south of the historic centre, next to the Verona Sud exit where the A4 and A22 motorways meet."),
  ("Airport.", "Verona Villafranca airport is about 15 km away; Venice, Milan and Bergamo airports are alternatives with more flights."),
  ("Hotels.", "During Vinitaly the whole area is booked months ahead: reserve rooms for your team as soon as your space is confirmed."),
  ("Traffic.", "In the big fair weeks traffic around the fairground is heavy, so we plan deliveries early in the morning and keep material on site ready for the build.")]),
 "exhibition-stand-builder-parma": ("Getting to Fiere di Parma", [
  ("Location.", "Fiere di Parma is just off the Parma exit of the A1 motorway, north of the city, with direct access for trucks."),
  ("Airports.", "Bologna airport is about an hour away by car; Milan airports are a bit further but have more international flights."),
  ("Food shows.", "Cibus and Cibus Tec mean tasting counters, refrigeration and kitchens: water and power connections are ordered from the organiser with the drawings."),
  ("Hotels.", "Parma is small and fills up during Cibus; some teams stay in Reggio Emilia or Fidenza, a short train ride away.")]),
 "exhibition-stand-builder-riva-del-garda": ("Getting to Riva del Garda", [
  ("Location.", "Riva del Garda Fierecongressi is at the northern tip of Lake Garda; the nearest motorway exit is Rovereto Sud on the A22, about 20 km away."),
  ("Airport.", "Verona airport is about an hour and a half by car; there is no train station in Riva, so teams usually rent a car or book transfers."),
  ("Lake roads.", "The last kilometres are narrow lakeside roads: large trucks need planned arrival times, and we often use smaller vehicles for the final delivery."),
  ("Season.", "Expo Riva Schuh and Hospitality run outside the summer season, so hotels are easier to find than in July and August.")]),
 "exhibition-stand-builder-rimini": ("Getting to the Rimini Expo Centre", [
  ("Location.", "The Rimini Expo Centre is north-west of the city, near the Rimini Nord exit of the A14 motorway."),
  ("Train.", "During the main fairs regional trains stop at the Rimini Fiera station right next to the entrance, which is the easiest way to arrive from Bologna."),
  ("Airports.", "Bologna airport is about 120 km away and has the most international flights; Rimini's own airport has fewer connections."),
  ("Hotels.", "Rimini has a huge number of hotels on the seafront, so even during Sigep and Ecomondo rooms are usually available close to the fair.")]),
 "exhibition-stand-builder-florence": ("Building a stand at the Fortezza da Basso", [
  ("A historic venue.", "The Fortezza da Basso is a 16th-century fortress in the city centre, a short walk from Santa Maria Novella station."),
  ("Access in the city.", "Trucks enter a busy historic area with traffic restrictions, so deliveries follow the organiser's time slots and we keep vehicles small where needed."),
  ("Pavilions of different sizes.", "Halls and pavilions inside the fortress have different heights and floor types: we check the exact pavilion before designing the stand."),
  ("Hotels.", "During Pitti Uomo the centre is full; book early or stay near the station to walk to the Fortezza.")]),
 "exhibition-stand-builder-bologna": ("Getting to BolognaFiere", [
  ("Location.", "BolognaFiere is in the Fiera district north of the centre, with its own exit on the A14 motorway and the ring road."),
  ("Airport.", "Bologna Guglielmo Marconi airport is about 8 km away, one of the closest airports to a major Italian fairground."),
  ("Large shows.", "Cersaie, Cosmoprof and EIMA fill many halls at the same time: delivery slots are tight, so we book them as soon as the organiser opens them."),
  ("Hotels.", "Bologna hotels sell out during the big fairs; Modena and Ferrara are good alternatives, about half an hour away by train.")]),
}

def li(items):
    return "\n".join(f'      <li><b>{html.escape(a, quote=False)}</b> {html.escape(b, quote=False)}</li>' for a, b in items)

def sezione(tit, lead, items):
    lead_html = f'\n      <p class="lead" data-rv="up">{html.escape(lead, quote=False)}</p>' if lead else ''
    return (f'<section id="pratico">\n  <div class="wrap">\n    <div class="sec-head">\n      <h2 class="title" data-rv="up">{html.escape(tit, quote=False)}</h2>{lead_html}\n    </div>\n'
            f'    <ul class="pg-lista" data-rv="up">\n{li(items)}\n    </ul>\n  </div>\n</section>\n')

def applica(slug, blocco):
    p = f"en/{slug}/index.html"
    if not os.path.isfile(p):
        print("manca", p); return 0
    s = open(p, encoding="utf-8").read()
    s = re.sub(r'<section id="pratico">.*?</section>\n?', '', s, flags=re.S)
    i = s.find('<section id="cosa">')
    if i < 0:
        print("ancora non trovata", p); return 0
    s = s[:i] + blocco + s[i:]
    open(p, "w", encoding="utf-8").write(s)
    return 1

n = 0
for slug, (t, lead, items) in PAESI.items(): n += applica(slug, sezione(t, lead, items))
for slug, (t, items) in CITTA.items(): n += applica(slug, sezione(t, "", items))
print("pagine arricchite:", n)
