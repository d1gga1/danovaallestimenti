"""Search Console 26/11/2026 - Dati strutturati Eventi: aggiunge 'image', 'description' e
'performer' ai BusinessEvent delle pagine fiere che ne sono prive. Idempotente."""
import glob, json, os, re

RADICE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EVENT_DESC = {
    "en": "{nome}: trade fair at {q}, {citta}.",
    "de": "{nome}: Fachmesse in {q}, {citta}.",
    "fr": "{nome} : salon professionnel à {q}, {citta}.",
    "es": "{nome}: feria profesional en {q}, {citta}.",
    "pt": "{nome}: feira profissional em {q}, {citta}.",
    "nl": "{nome}: vakbeurs in {q}, {citta}.",
    "pl": "{nome}: targi branżowe – {q}, {citta}.",
    "it": "{nome}: fiera di settore a {q}, {citta}.",
}
IMG_DEF = "https://danovastand.com/assets/img/og-cover.jpg"


def eventi(o, out):
    if isinstance(o, dict):
        t = o.get("@type")
        if t in ("Event", "BusinessEvent", "ExhibitionEvent"):
            out.append(o)
        for v in o.values():
            eventi(v, out)
    elif isinstance(o, list):
        for v in o:
            eventi(v, out)


tot_p = tot_e = 0
for f in glob.glob(os.path.join(RADICE, "**", "*.html"), recursive=True):
    if "Claude outputs" in f:
        continue
    s = open(f, encoding="utf-8").read()
    if "Event" not in s:
        continue
    lang = (re.search(r'<html[^>]*lang="([a-zA-Z]+)', s) or [None, "en"])[1].lower()
    mi = re.search(r'<meta property="og:image" content="([^"]+)"', s)
    img = mi.group(1) if mi else IMG_DEF
    nuovo, cambiato = s, False
    for m in re.finditer(r'(<script type="application/ld\+json">)(.*?)(</script>)', s, re.S):
        try:
            d = json.loads(m.group(2))
        except ValueError:
            continue
        ev = []
        eventi(d, ev)
        mod = False
        for e in ev:
            loc = e.get("location") or {}
            fmt = dict(nome=e.get("name", ""), q=loc.get("name", ""),
                       citta=(loc.get("address") or {}).get("addressLocality", ""))
            if not e.get("description"):
                e["description"] = EVENT_DESC.get(lang, EVENT_DESC["en"]).format(**fmt).replace(", .", ".")
                mod = True
            if not e.get("image"):
                e["image"] = [img]
                mod = True
            if not e.get("performer"):
                e["performer"] = dict(e["organizer"]) if isinstance(e.get("organizer"), dict) else \
                    {"@type": "Organization", "name": e.get("name", "")}
                mod = True
            tot_e += mod
        if mod:
            ind = 2 if "\n  " in m.group(2) else None
            nuovo = nuovo.replace(m.group(0), m.group(1) + "\n" + json.dumps(d, ensure_ascii=False, indent=ind) + "\n" + m.group(3), 1)
            cambiato = True
    if cambiato:
        open(f, "w", encoding="utf-8").write(nuovo)
        tot_p += 1
print(f"pagine corrette: {tot_p}, eventi completati: {tot_e}")
