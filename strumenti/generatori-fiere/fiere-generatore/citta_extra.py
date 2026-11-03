# -*- coding: utf-8 -*-
"""Blocco 'Da Mansue' a <citta>' per le pagine /allestimenti-fieristici-<citta>/ (13 ottobre 2026).
Distanza stimata su strada (linea d'aria x 1,3, arrotondata) dalla sede di Mansue' (TV) al quartiere
fieristico, organizzazione in base alla distanza e link all'hub regionale. Idempotente."""
import re, math
A, B = '<!--fr-logistica-->', '<!--/fr-logistica-->'
SEDE = (45.826, 12.533)
# Sedi operative (14/10/2026): la distanza si calcola dalla sede piu' vicina al quartiere fieristico
SEDI = [
 ("Mansuè (TV)", "Dalla sede di Mansuè (TV)", "Mansuè", 45.826, 12.533),
 ("Fontanelle (TV)", "Dal magazzino di Fontanelle (TV)", "Fontanelle", 45.834, 12.467),
 ("Trumello (PV)", "Dal magazzino e dagli uffici di Trumello (PV)", "Trumello", 45.094, 8.882),
 ("Vermezzo con Zelo (MI)", "Dagli uffici di Vermezzo con Zelo (MI)", "Vermezzo", 45.392, 8.978),
]
# slug: (citta, sede fieristica, lat, lon, regione-hub or None)
C = {
 'verona': ("Verona", "Veronafiere", 45.4186, 10.9826, 'veneto'),
 'padova': ("Padova", "Fiera di Padova", 45.4110, 11.8890, 'veneto'),
 'vicenza': ("Vicenza", "Vicenza Expo Centre", 45.5172, 11.4866, 'veneto'),
 'venezia': ("Venezia", "Venezia e Mestre", 45.4900, 12.2400, 'veneto'),
 'treviso': ("Treviso", "Treviso", 45.6660, 12.2430, 'veneto'),
 'longarone': ("Longarone", "Longarone Fiere Dolomiti", 46.2710, 12.3000, 'veneto'),
 'milano': ("Milano", "Fiera Milano Rho", 45.5206, 9.0870, 'lombardia'),
 'bergamo': ("Bergamo", "Fiera di Bergamo", 45.6770, 9.6930, 'lombardia'),
 'brescia': ("Brescia", "Brixia Forum", 45.5350, 10.2400, 'lombardia'),
 'bologna': ("Bologna", "BolognaFiere", 44.5126, 11.3655, 'emilia'),
 'rimini': ("Rimini", "Rimini Expo Centre", 44.0499, 12.5822, 'emilia'),
 'parma': ("Parma", "Fiere di Parma", 44.8290, 10.3290, 'emilia'),
 'pordenone': ("Pordenone", "Pordenone Fiere", 45.9670, 12.6750, None),
 'udine': ("Udine", "Udine e Gorizia Fiere", 46.0890, 13.1590, None),
 'bolzano': ("Bolzano", "Fiera Bolzano", 46.4700, 11.3300, None),
 'riva-del-garda': ("Riva del Garda", "Riva del Garda Fierecongressi", 45.8838, 10.8597, None),
 'firenze': ("Firenze", "Fortezza da Basso", 43.7795, 11.2475, None),
 'torino': ("Torino", "Lingotto Fiere", 45.0328, 7.6667, None),
 'genova': ("Genova", "Fiera di Genova", 44.4010, 8.9460, None),
 'carrara': ("Carrara", "CarraraFiere", 44.0400, 10.0500, None),
 'roma': ("Roma", "Fiera di Roma", 41.8128, 12.3567, None),
 'napoli': ("Napoli", "Mostra d'Oltremare", 40.8230, 14.1930, None),
 'bari': ("Bari", "Fiera del Levante", 41.1340, 16.8380, None),
}
HUBS = {'veneto': ("Veneto", "/allestimenti-fieristici-veneto/"), 'lombardia': ("Lombardia", "/allestimenti-fieristici-lombardia/"),
        'emilia': ("Emilia-Romagna", "/allestimenti-fieristici-emilia-romagna/")}

def km(lat, lon, da=None):
    da = da or SEDE
    R = 6371; p1, p2 = math.radians(da[0]), math.radians(lat)
    d = 2 * R * math.asin(math.sqrt(math.sin((p2 - p1) / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(math.radians(lon - da[1]) / 2) ** 2))
    return int(round(d * 1.3 / 10.0)) * 10 or 10

def piu_vicina(lat, lon):
    return min(((km(lat, lon, (a, b)),) + x[:3] for x in SEDI for a, b in [x[3:5]]), key=lambda t: t[0])

def ore(k):
    h = k / 85.0
    if h < 0.75: return "meno di un'ora"
    if h < 1.25: return "circa un'ora"
    q = round(h * 2) / 2
    s = (f"{int(q)}" if q == int(q) else f"{int(q)} e mezza").replace("1 e mezza", "un'ora e mezza")
    return "circa " + (s if "ora" in s else f"{s} ore")

def blocco(slug):
    c, sede, lat, lon, hub = C[slug]
    k, DA, DA_LUNGO, DA_BREVE = piu_vicina(lat, lon)
    if slug == 'treviso':
        d1 = f"Treviso è la nostra provincia: tra la sede di Mansuè e il magazzino di Fontanelle siamo a circa {k} km dal capoluogo. Qui lavoriamo come a casa: sopralluoghi in giornata, consegne rapide e interventi durante l'evento anche con poche ore di preavviso."
    elif k <= 80:
        d1 = f"{DA_LUNGO} a {sede} ci sono circa {k} km, {ore(k)} di furgone. Per {c} lavoriamo come per una fiera di casa: sopralluogo in giornata, materiali consegnati dai nostri trasportatori di fiducia, squadra che rientra la sera e che può tornare in fiera durante la manifestazione se serve un intervento."
    elif k <= 300:
        d1 = f"{DA_LUNGO} a {sede} ci sono circa {k} km, {ore(k)} di strada. Organizziamo il trasporto gestito da noi o corriere dedicato, la squadra di montaggio lavora in trasferta per i giorni di allestimento e un referente resta raggiungibile per tutta la durata della fiera."
    else:
        d1 = f"{DA_LUNGO} a {sede} ci sono circa {k} km. Per una fiera così lontana pianifichiamo tutto in anticipo: stand e materiali viaggiano con trasporto dedicato, la squadra di montaggio è in trasferta (con partner locali quando conviene) e pass, orari di scarico e pratiche con l'ente fiera sono pronti prima di partire."
    d2 = "La distanza non cambia il preventivo a sorpresa: trasporto e trasferta sono voci separate e chiare, così sai da subito quanto pesano sul totale. Se esponi più volte nella stessa zona, uno stand di proprietà conservato in magazzino riduce i costi di ogni fiera."
    lis = [("Distanza dalla sede.", f"Circa {k} km da {DA} a {sede}, stima su strada. Le nostre sedi: Mansuè e Fontanelle (TV), Trumello (PV), Vermezzo con Zelo (MI)."),
           ("Trasporto.", "Con mezzi nostri o corriere dedicato, coordinato con gli orari di scarico della fiera."),
           ("Squadra.", "Montatori nostri e partner di fiducia, con un referente unico dall'arrivo allo smontaggio.")]
    if hub:
        n, u = HUBS[hub]
        lis.append(("In regione.", f"Tutti i quartieri fieristici della regione nella pagina <a href=\"{u}\">allestimenti fieristici in {n}</a>."))
    li = ''.join(f'\n      <li><b>{b}</b> {t}</li>' for b, t in lis)
    return (f'{A}<section id="logistica">\n  <div class="wrap">\n    <div class="sec-head">\n      <h2 class="title" data-rv="up">Da {DA_BREVE} a {c}: <span class="grad">logistica e tempi</span></h2>\n    </div>\n'
            f'    <div class="pg-testo" data-rv="up">\n      <p>{d1}</p>\n      <p>{d2}</p>\n    </div>\n    <ul class="pg-lista" data-rv="up">{li}\n    </ul>\n  </div>\n</section>\n{B}\n')

def inject(s, path):
    m = re.match(r'^/allestimenti-fieristici-([a-z-]+)/$', path)
    if not m or m.group(1) not in C: return s
    s = re.sub(re.escape(A) + r'.*?' + re.escape(B) + r'\n?', '', s, flags=re.S)
    i = s.find('<section id="sapere">')
    if i < 0: i = s.find('<section id="cosa">')
    if i < 0: return s
    return s[:i] + blocco(m.group(1)) + s[i:]
