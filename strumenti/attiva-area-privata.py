#!/usr/bin/env python3
"""Danova — area privata danovastand.com/private_area/ (stessa di pandooragroup.it), idempotente.
Una sola dashboard per tre siti: Danova Stand (questo), Danova Costruzioni, Danova Tech.

    python3 strumenti/attiva-area-privata.py                 # Danova Stand: aggiorna pagine e testi legali
    python3 strumenti/attiva-area-privata.py abcdefghijklmn  # in più collega il progetto Supabase (codice del progetto)
    python3 strumenti/attiva-area-privata.py --sito costruzioni ~/danova_costruzioni   # collega un altro sito
    python3 strumenti/attiva-area-privata.py --sito tech ~/Desktop/dantech/danovatech
  Per gli altri siti copia anche assets/js/ds-live.js (lo stesso file per tutti: il sito si riconosce dal dominio).

Cosa fa:
  1. aggiunge <script src="/assets/js/ds-live.js" defer> a tutte le pagine del sito
     (non a strumenti/, private_area/ e alle pagine di solo reindirizzamento);
  2. se gli passi il codice del progetto Supabase, lo scrive in assets/js/ds-live.js e in
     private_area/index.html (e lo ricorda in strumenti/supabase/progetto.txt);
  3. aggiorna Cookie policy e Privacy (IT, EN, DE, FR, ES): statistiche interne e banner.
Va rilanciato dopo ogni migra-da-danovatech.py (che riscrive le pagine), insieme agli altri script.
"""
import os, re, sys

QUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))   # repository di Danova Stand
args = sys.argv[1:]
SITO = 'stand'
if '--sito' in args:
    i = args.index('--sito'); SITO = args[i + 1]; del args[i:i + 2]
    if SITO not in ('stand', 'costruzioni', 'tech'): sys.exit('--sito deve essere stand, costruzioni o tech')
REPO = QUI
if SITO != 'stand':
    if not args: sys.exit('Indica la cartella del sito, es. --sito costruzioni ~/danova_costruzioni')
    REPO = os.path.abspath(os.path.expanduser(args.pop(0)))
    os.makedirs(os.path.join(REPO, 'assets', 'js'), exist_ok=True)
    src = open(os.path.join(QUI, 'assets', 'js', 'ds-live.js'), encoding='utf-8').read()
    open(os.path.join(REPO, 'assets', 'js', 'ds-live.js'), 'w', encoding='utf-8').write(src)
    print('Copiato assets/js/ds-live.js in', REPO)
MAIL = {'stand': 'info@danova-tech.com', 'costruzioni': 'info@danovacostruzioni.it', 'tech': 'info@danova-tech.com'}[SITO]
SALTA = {'.git', '.github', 'strumenti', 'private_area', '_google_business', 'Claude outputs', 'node_modules', 'seo-tools', 'social', 'assets'}
TAG = '<script src="/assets/js/ds-live.js?v=1" defer></script>'
PROG_FILE = os.path.join(QUI, 'strumenti', 'supabase', 'progetto.txt')


def leggi(p): return open(p, encoding='utf-8').read()
def scrivi(p, t): open(p, 'w', encoding='utf-8').write(t)


# ---------- 1. script statistiche in tutte le pagine ----------
def pagine():
    for root, dirs, files in os.walk(REPO):
        rel = os.path.relpath(root, REPO)
        dirs[:] = [d for d in dirs if d not in SALTA and not d.startswith('_')]
        for f in files:
            if f.endswith('.html'):
                yield os.path.join(root, f), os.path.join(rel, f)

aggiunte = gia = salt = 0
for p, rel in pagine():
    t = leggi(p)
    if 'http-equiv="refresh"' in t and len(t) < 3000:
        salt += 1; continue
    if '/assets/js/ds-live.js' in t:
        nuovo = re.sub(r'<script src="/assets/js/ds-live\.js[^"]*" defer></script>', TAG, t)
        if nuovo != t: scrivi(p, nuovo)
        gia += 1; continue
    if '</head>' not in t:
        print('  senza </head>:', rel); continue
    scrivi(p, t.replace('</head>', TAG + '\n</head>', 1)); aggiunte += 1
print(f'Script statistiche: aggiunto a {aggiunte} pagine, già presente in {gia}, {salt} reindirizzamenti saltati.')

# ---------- 2. progetto Supabase ----------
ref = args[0].strip() if args else (leggi(PROG_FILE).strip() if os.path.exists(PROG_FILE) else '')
ref = re.sub(r'^https?://', '', ref).split('.')[0]
if ref:
    if not re.fullmatch(r'[a-z0-9]{10,40}', ref):
        sys.exit('Codice progetto non valido: è la parte prima di .supabase.co, es. abcdefghijklmnopqrst')
    for rel in ('assets/js/ds-live.js', 'private_area/index.html'):
        p = os.path.join(REPO, rel)
        if not os.path.exists(p): continue
        t = leggi(p)
        t2 = re.sub(r'https://[a-zA-Z0-9-]+\.supabase\.co/functions/v1/ds', f'https://{ref}.supabase.co/functions/v1/ds', t)
        if t2 != t: scrivi(p, t2)
    if SITO == 'stand': os.makedirs(os.path.dirname(PROG_FILE), exist_ok=True); scrivi(PROG_FILE, ref + '\n')
    print(f'Progetto Supabase collegato: https://{ref}.supabase.co/functions/v1/ds')
else:
    print('Progetto Supabase non ancora indicato: le statistiche restano spente finché non lanci lo script con il codice del progetto.')

# ---------- 3. testi legali ----------
M0, M1 = '<!-- ds-statistiche -->', '<!-- /ds-statistiche -->'
COOKIE = {
    'cookie-policy/index.html': ('I cookie usati da questo sito', '''<p>Questo sito <b>non installa cookie di profilazione o di marketing</b> e non usa Google Analytics, Meta Pixel o tecnologie pubblicitarie equivalenti.</p>
          <p><b>Statistiche interne.</b> Per capire quali pagine sono utili e migliorare il sito, uno script nostro (<code>ds-live.js</code>) salva nel <b>local storage</b> del browser un codice casuale, che serve a riconoscere le visite successive dallo stesso dispositivo, e registra in forma anonima le pagine viste, la provenienza della visita, il tipo di dispositivo e la zona approssimativa ricavata dall'indirizzo IP (città o regione: l'indirizzo IP non viene salvato). Registra anche i clic su WhatsApp, telefono ed email. I dati restano in un nostro database (Supabase) e non vengono ceduti a terzi né usati per pubblicità; si conservano per 25 mesi.</p>
          <p><b>Statistiche dettagliate, solo con il tuo consenso.</b> Alla prima visita un avviso ti chiede se accetti: solo in quel caso registriamo anche come navighi (clic, sezioni lette, moduli iniziati, inviati o lasciati a metà: <b>mai quello che scrivi nei campi</b>). Puoi cambiare idea quando vuoi da <a href="#cookie">questo link</a>; la scelta vale 6 mesi.</p>
          <p>Se invii un modulo di contatto, la richiesta viene salvata anche nel nostro database ed è collegata alle visite fatte dallo stesso dispositivo, per poterti rispondere meglio. Per non essere contato puoi cancellare i dati del sito dal browser o bloccare lo script: il sito funziona comunque.</p>
          <p>Per contare le visite in forma aggregata il sito usa anche <b>Cloudflare Web Analytics</b>, che non installa cookie e non salva nulla sul tuo dispositivo: i dettagli sono nella sezione sui servizi di terze parti.</p>'''),
    'en/cookie-policy/index.html': ('Cookies used by this site', '''<p>This website <b>installs no profiling or marketing cookies</b> and uses no Google Analytics, Meta Pixel or equivalent advertising technology.</p>
          <p><b>Internal statistics.</b> To understand which pages are useful and improve the site, a script of ours (<code>ds-live.js</code>) stores a random code in your browser's <b>local storage</b>, used to recognise later visits from the same device, and records anonymously the pages viewed, where the visit came from, the device type and the approximate area derived from the IP address (city or region: the IP address itself is not stored). It also records clicks on WhatsApp, phone and email links. The data stays in our own database (Supabase), is never sold or used for advertising and is kept for 25 months.</p>
          <p><b>Detailed statistics, only with your consent.</b> On your first visit a notice asks whether you accept: only then do we also record how you browse (clicks, sections read, forms started, sent or abandoned: <b>never what you type</b>). You can change your mind at any time with <a href="#cookie">this link</a>; your choice lasts 6 months.</p>
          <p>If you send a contact form, the request is also saved in our database and linked to the visits made from the same device, so we can answer you better. To avoid being counted you can clear the site's data in your browser or block the script: the site works either way.</p>
          <p>Visits are also counted in aggregate with <b>Cloudflare Web Analytics</b>, which sets no cookies and stores nothing on your device: details are in the third-party services section.</p>'''),
    'de/cookie-richtlinie/index.html': ('Von dieser Website verwendete Cookies', '''<p>Diese Website setzt <b>keine Profiling- oder Marketing-Cookies</b> ein und verwendet weder Google Analytics noch Meta Pixel oder vergleichbare Werbetechnologien.</p>
          <p><b>Interne Statistiken.</b> Um zu verstehen, welche Seiten nützlich sind, speichert ein eigenes Skript (<code>ds-live.js</code>) einen zufälligen Code im <b>Local Storage</b> Ihres Browsers, um spätere Besuche vom selben Gerät zu erkennen, und erfasst anonym die aufgerufenen Seiten, die Herkunft des Besuchs, den Gerätetyp und die ungefähre Region anhand der IP-Adresse (Stadt oder Region: die IP-Adresse selbst wird nicht gespeichert). Außerdem werden Klicks auf WhatsApp-, Telefon- und E-Mail-Links erfasst. Die Daten bleiben in unserer eigenen Datenbank (Supabase), werden nicht weitergegeben oder für Werbung genutzt und 25 Monate aufbewahrt.</p>
          <p><b>Detaillierte Statistiken nur mit Ihrer Einwilligung.</b> Beim ersten Besuch fragt ein Hinweis, ob Sie zustimmen: Nur dann erfassen wir auch, wie Sie navigieren (Klicks, gelesene Abschnitte, begonnene, gesendete oder abgebrochene Formulare: <b>nie, was Sie eingeben</b>). Sie können Ihre Wahl jederzeit über <a href="#cookie">diesen Link</a> ändern; sie gilt 6 Monate.</p>
          <p>Wenn Sie ein Kontaktformular senden, wird die Anfrage auch in unserer Datenbank gespeichert und mit den Besuchen vom selben Gerät verknüpft, damit wir Ihnen besser antworten können. Sie können die Website-Daten im Browser löschen oder das Skript blockieren: Die Website funktioniert in jedem Fall.</p>
          <p>Zusätzlich werden Besuche mit <b>Cloudflare Web Analytics</b> aggregiert gezählt, das keine Cookies setzt und nichts auf Ihrem Gerät speichert: Einzelheiten im Abschnitt zu Diensten Dritter.</p>'''),
    'fr/cookies/index.html': ('Cookies utilisés par ce site', '''<p>Ce site <b>n'installe aucun cookie de profilage ou de marketing</b> et n'utilise ni Google Analytics, ni Pixel Meta, ni technologie publicitaire équivalente.</p>
          <p><b>Statistiques internes.</b> Pour savoir quelles pages sont utiles, un script qui nous appartient (<code>ds-live.js</code>) enregistre un code aléatoire dans le <b>stockage local</b> de votre navigateur, afin de reconnaître les visites suivantes depuis le même appareil, et enregistre de façon anonyme les pages vues, la provenance de la visite, le type d'appareil et la zone approximative déduite de l'adresse IP (ville ou région : l'adresse IP elle-même n'est pas conservée). Il enregistre aussi les clics sur WhatsApp, le téléphone et l'e-mail. Les données restent dans notre propre base (Supabase), ne sont ni cédées ni utilisées à des fins publicitaires et sont conservées 25 mois.</p>
          <p><b>Statistiques détaillées, uniquement avec votre consentement.</b> Lors de la première visite, un message vous demande si vous acceptez : seulement dans ce cas nous enregistrons aussi votre navigation (clics, sections lues, formulaires commencés, envoyés ou abandonnés : <b>jamais ce que vous écrivez</b>). Vous pouvez changer d'avis à tout moment via <a href="#cookie">ce lien</a> ; votre choix vaut 6 mois.</p>
          <p>Si vous envoyez un formulaire de contact, la demande est aussi enregistrée dans notre base et reliée aux visites faites depuis le même appareil, pour mieux vous répondre. Vous pouvez effacer les données du site dans votre navigateur ou bloquer le script : le site fonctionne dans tous les cas.</p>
          <p>Les visites sont aussi comptées de façon agrégée avec <b>Cloudflare Web Analytics</b>, qui ne dépose aucun cookie et ne stocke rien sur votre appareil : détails dans la section consacrée aux services tiers.</p>'''),
    'es/cookies/index.html': ('Cookies que usa esta web', '''<p>Esta web <b>no instala cookies de perfilado ni de marketing</b> y no usa Google Analytics, Píxel de Meta ni tecnologías publicitarias equivalentes.</p>
          <p><b>Estadísticas internas.</b> Para saber qué páginas son útiles, un script propio (<code>ds-live.js</code>) guarda un código aleatorio en el <b>almacenamiento local</b> del navegador, para reconocer las visitas siguientes desde el mismo dispositivo, y registra de forma anónima las páginas vistas, la procedencia de la visita, el tipo de dispositivo y la zona aproximada obtenida de la dirección IP (ciudad o región: la IP no se guarda). También registra los clics en WhatsApp, teléfono y email. Los datos permanecen en nuestra propia base de datos (Supabase), no se ceden ni se usan para publicidad y se conservan 25 meses.</p>
          <p><b>Estadísticas detalladas, solo con tu consentimiento.</b> En la primera visita un aviso te pregunta si aceptas: solo en ese caso registramos también cómo navegas (clics, secciones leídas, formularios empezados, enviados o abandonados: <b>nunca lo que escribes</b>). Puedes cambiar de opinión cuando quieras desde <a href="#cookie">este enlace</a>; la elección vale 6 meses.</p>
          <p>Si envías un formulario de contacto, la solicitud se guarda también en nuestra base de datos y se vincula a las visitas hechas desde el mismo dispositivo, para responderte mejor. Puedes borrar los datos del sitio en el navegador o bloquear el script: la web funciona igualmente.</p>
          <p>Las visitas también se cuentan de forma agregada con <b>Cloudflare Web Analytics</b>, que no instala cookies ni guarda nada en tu dispositivo: detalles en el apartado de servicios de terceros.</p>'''),
}
PRIVACY = {
    'privacy/index.html': ('Come funziona il modulo di contatto', 'Statistiche del sito', '''<p>Per migliorare il sito registriamo in forma anonima le pagine viste, la provenienza della visita, il tipo di dispositivo e la zona approssimativa ricavata dall'indirizzo IP (l'indirizzo IP non viene salvato), riconoscendo le visite successive con un codice casuale salvato nel browser. Solo se accetti l'avviso sui cookie registriamo anche clic, sezioni lette e moduli iniziati o lasciati a metà, mai il contenuto dei campi. Le richieste inviate con i moduli vengono salvate anche nel nostro database e collegate alle visite dello stesso dispositivo, per risponderti meglio. Base giuridica: legittimo interesse a migliorare il sito e gestire le richieste (statistiche anonime e richieste) e consenso (statistiche dettagliate). Il database è ospitato da Supabase (fornitore che tratta i dati per nostro conto); i dati si conservano per 25 mesi. Dettagli nella <a href="/cookie-policy/">Cookie policy</a>. Se ti iscrivi alla newsletter (riquadro dello sconto del 3%), usiamo nome, email e gli altri dati che ci lasci per mandarti novità e offerte di Danova Stand e per ricontattarti, sulla base del tuo consenso, finché non ti cancelli: basta rispondere a una nostra email o scrivere a info@danova-tech.com.</p>'''),
    'en/privacy/index.html': ('How the contact form works', 'Website statistics', '''<p>To improve the site we record anonymously the pages viewed, where the visit came from, the device type and the approximate area derived from the IP address (the IP address itself is not stored), recognising later visits with a random code saved in the browser. Only if you accept the cookie notice do we also record clicks, sections read and forms started or abandoned, never what you type. Requests sent through the forms are also saved in our database and linked to the visits from the same device, so we can answer you better. Legal basis: legitimate interest in improving the site and handling requests (anonymous statistics and requests) and consent (detailed statistics). The database is hosted by Supabase, a processor acting on our behalf; data is kept for 25 months. Details in the <a href="/en/cookie-policy/">Cookie policy</a>. If you subscribe to the newsletter (the 3% discount box), we use your name, email and the other details you give us to send you Danova Stand news and offers and to contact you, based on your consent, until you unsubscribe: just reply to one of our emails or write to info@danova-tech.com.</p>'''),
    'de/datenschutz/index.html': ('Funktionsweise des Kontaktformulars', 'Statistiken der Website', '''<p>Um die Website zu verbessern, erfassen wir anonym die aufgerufenen Seiten, die Herkunft des Besuchs, den Gerätetyp und die ungefähre Region anhand der IP-Adresse (die IP-Adresse selbst wird nicht gespeichert) und erkennen spätere Besuche an einem zufälligen Code im Browser. Nur wenn Sie dem Cookie-Hinweis zustimmen, erfassen wir auch Klicks, gelesene Abschnitte und begonnene oder abgebrochene Formulare, nie den Inhalt der Felder. Über die Formulare gesendete Anfragen werden auch in unserer Datenbank gespeichert und mit den Besuchen vom selben Gerät verknüpft. Rechtsgrundlage: berechtigtes Interesse an der Verbesserung der Website und der Bearbeitung von Anfragen (anonyme Statistiken und Anfragen) sowie Einwilligung (detaillierte Statistiken). Die Datenbank wird von Supabase als Auftragsverarbeiter gehostet; Speicherdauer 25 Monate. Einzelheiten in der <a href="/de/cookie-richtlinie/">Cookie-Richtlinie</a>. Wenn Sie den Newsletter abonnieren (Feld mit 3 % Rabatt), verwenden wir Name, E-Mail und Ihre weiteren Angaben auf Grundlage Ihrer Einwilligung, um Ihnen Neuigkeiten und Angebote von Danova Stand zu senden und Sie zu kontaktieren, bis Sie sich abmelden: Antworten Sie einfach auf eine unserer E-Mails oder schreiben Sie an info@danova-tech.com.</p>'''),
    'fr/confidentialite/index.html': ('Comment fonctionne le formulaire de contact', 'Statistiques du site', '''<p>Pour améliorer le site, nous enregistrons de façon anonyme les pages vues, la provenance de la visite, le type d'appareil et la zone approximative déduite de l'adresse IP (l'adresse IP elle-même n'est pas conservée), en reconnaissant les visites suivantes grâce à un code aléatoire enregistré dans le navigateur. Seulement si vous acceptez le message sur les cookies, nous enregistrons aussi les clics, les sections lues et les formulaires commencés ou abandonnés, jamais le contenu des champs. Les demandes envoyées via les formulaires sont aussi enregistrées dans notre base et reliées aux visites du même appareil. Base légale : intérêt légitime à améliorer le site et à traiter les demandes (statistiques anonymes et demandes) et consentement (statistiques détaillées). La base est hébergée par Supabase, sous-traitant agissant pour notre compte ; conservation 25 mois. Détails dans la page <a href="/fr/cookies/">Cookies</a>. Si vous vous abonnez à la newsletter (encadré de la réduction de 3 %), nous utilisons votre nom, votre e-mail et les autres informations fournies pour vous envoyer les nouveautés et offres de Danova Stand et vous recontacter, sur la base de votre consentement, jusqu'à votre désinscription : il suffit de répondre à l'un de nos e-mails ou d'écrire à info@danova-tech.com.</p>'''),
    'es/privacidad/index.html': (None, 'Estadísticas de la web', '''<p>Para mejorar la web registramos de forma anónima las páginas vistas, la procedencia de la visita, el tipo de dispositivo y la zona aproximada obtenida de la dirección IP (la IP no se guarda), reconociendo las visitas siguientes con un código aleatorio guardado en el navegador. Solo si aceptas el aviso de cookies registramos también clics, secciones leídas y formularios empezados o abandonados, nunca el contenido de los campos. Las solicitudes enviadas con los formularios se guardan también en nuestra base de datos y se vinculan a las visitas del mismo dispositivo. Base jurídica: interés legítimo en mejorar la web y gestionar las solicitudes (estadísticas anónimas y solicitudes) y consentimiento (estadísticas detalladas). La base de datos está alojada en Supabase, encargado del tratamiento; los datos se conservan 25 meses. Detalles en la página de <a href="/es/cookies/">Cookies</a>. Si te suscribes a la newsletter (recuadro del 3% de descuento), usamos tu nombre, email y los demás datos que nos dejes para enviarte novedades y ofertas de Danova Stand y contactarte, con base en tu consentimiento, hasta que te des de baja: basta con responder a uno de nuestros emails o escribir a info@danova-tech.com.</p>'''),
}
# paragrafo "Aggiornamenti" delle cookie policy: il banner adesso c'è
AGGIORNAMENTI = [
    ('Se in futuro introdurremo strumenti', "Da novembre 2026 il sito usa le statistiche interne descritte sopra, con un avviso che chiede il consenso per quelle dettagliate. Se introdurremo altri strumenti di misurazione o di marketing aggiorneremo questa pagina prima dell'attivazione."),
    ('If we introduce measurement', 'Since November 2026 the site uses the internal statistics described above, with a notice asking for consent to the detailed ones. If we introduce other measurement or marketing tools we will update this page before they go live.'),
    ('Sollten wir künftig', 'Seit November 2026 nutzt die Website die oben beschriebenen internen Statistiken, mit einem Hinweis, der die Einwilligung für die detaillierten Statistiken einholt. Sollten wir weitere Mess- oder Marketingwerkzeuge einsetzen, aktualisieren wir diese Seite vor der Inbetriebnahme.'),
    ('Si nous introduisons à', "Depuis novembre 2026, le site utilise les statistiques internes décrites ci-dessus, avec un message demandant le consentement pour les statistiques détaillées. Si nous introduisons d'autres outils de mesure ou de marketing, nous mettrons cette page à jour avant leur mise en service."),
    ('Si en el futuro introducimos', 'Desde noviembre de 2026 la web usa las estadísticas internas descritas arriba, con un aviso que pide el consentimiento para las detalladas. Si introducimos otras herramientas de medición o de marketing, actualizaremos esta página antes de ponerlas en marcha.'),
]
def sezione(titolo, corpo):
    return f'{M0}<section><div class="wrap"><div class="sec-head"><h2 class="title">{titolo}</h2></div><div class="pg-testo">{corpo}</div></div></section>{M1}\n'

for rel, (titolo, corpo) in COOKIE.items():
    p = os.path.join(REPO, rel)
    if not os.path.exists(p): print('  manca', rel); continue
    t = leggi(p)
    m = re.search(re.escape(M0) + r'.*?' + re.escape(M1) + r'\n?', t, re.S)   # già aggiornata: si riscrive
    if not m:
        m = re.search(r'<section><div class="wrap"><div class="sec-head"><h2 class="title">' + re.escape(titolo) + r'</h2>.*?</section>\n?', t, re.S)
    if not m: print('  sezione cookie non trovata in', rel); continue
    t = t[:m.start()] + sezione(titolo, corpo) + t[m.end():]
    t = re.sub(r'(Ultimo aggiornamento|Last updated|Letzte Aktualisierung|Dernière mise à jour|Última actualización)(\s*):\s*[^<]*', lambda x: x.group(1) + x.group(2) + ': ' + {'U': 'novembre 2026', 'L': 'November 2026', 'D': 'novembre 2026', 'Ú': 'noviembre 2026'}[x.group(1)[0]], t, count=1)
    for vecchio, nuovo in AGGIORNAMENTI:
        t = re.sub(r'<p>' + re.escape(vecchio) + r'[^<]*</p>', '<p>' + nuovo + '</p>', t)
    scrivi(p, t); print('Aggiornata', rel)

NEWS = (" Se ti iscrivi alla newsletter", " If you subscribe to the newsletter", " Wenn Sie den Newsletter abonnieren", " Si vous vous abonnez à la newsletter", " Si te suscribes a la newsletter")
for rel, (dopo, titolo, corpo) in PRIVACY.items():
    if SITO != 'stand':   # il popup della newsletter c'è solo su Danova Stand
        for n in NEWS:
            if n in corpo: corpo = corpo[:corpo.index(n)] + '</p>'
    corpo = corpo.replace('info@danova-tech.com', MAIL)
    p = os.path.join(REPO, rel)
    if not os.path.exists(p): print('  manca', rel); continue
    t = leggi(p)
    t = re.sub(re.escape(M0) + r'.*?' + re.escape(M1) + r'\n?', '', t, flags=re.S)
    if dopo:
        m = re.search(r'<section><div class="wrap"><div class="sec-head"><h2 class="title">' + re.escape(dopo) + r'</h2>.*?</section>\n?', t, re.S)
    else:   # la terza sezione della pagina
        ms = list(re.finditer(r'<section><div class="wrap"><div class="sec-head"><h2 class="title">.*?</section>\n?', t, re.S)); m = ms[2] if len(ms) > 2 else None
    if not m: print('  sezione privacy non trovata in', rel); continue
    t = t[:m.end()] + sezione(titolo, corpo) + t[m.end():]
    scrivi(p, t); print('Aggiornata', rel)
print('Fatto.')
