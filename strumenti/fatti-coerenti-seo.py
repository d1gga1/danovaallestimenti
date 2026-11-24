#!/usr/bin/env python3
"""Coerenza dei fatti per Google e assistenti AI + popup non invasivo su telefono (24/11/2026).
Idempotente. Lanciarlo dopo migra-da-danovatech.py / genera-chi-siamo.py, prima di ottimizza-geo.py.
1. Lingue: il sito oggi e' in 36 lingue; i vecchi testi dicevano 5 o 8 lingue (chi siamo, FAQ, llms.txt).
   Le AI scartano o confondono un'azienda che dice cose diverse in pagine diverse.
2. Immagine senza alt nella pagina montatori.
3. Popup -3%: su telefono si apre sempre da solo dopo 5-7 s, ma come riquadro piccolo in basso, senza velo scuro
   (Google penalizza su mobile i popup che coprono la pagina): toccando il pulsante si apre il modulo completo.
   Su computer resta com'era.
"""
import os, re, glob
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
cambi = []

def sost(path, vecchio, nuovo):
    if not os.path.exists(path): return
    s = open(path, encoding='utf-8').read()
    if vecchio in s:
        open(path, 'w', encoding='utf-8').write(s.replace(vecchio, nuovo)); cambi.append(path)

# 1. lingue
LINGUE_IT_V = 'pagine dedicate in inglese, tedesco, francese, spagnolo, cinese, turco e arabo'
LINGUE_IT_N = 'il sito in 36 lingue (tra cui inglese, tedesco, francese, spagnolo, cinese, turco e arabo)'
for f in glob.glob('**/index.html', recursive=True):
    if f.startswith(('Claude outputs/', 'strumenti/', 'render/', 'private_area/')): continue
    sost(f, 'abbiamo ' + LINGUE_IT_V, 'abbiamo ' + LINGUE_IT_N)
sost('llms.txt', 'Sito in italiano, inglese, tedesco, francese, spagnolo, cinese, turco e arabo.',
     'Sito in 36 lingue (italiano, inglese, tedesco, francese, spagnolo, portoghese, olandese, polacco, cinese, giapponese, arabo, turco, hindi, urdu e altre).')
sost('llms.txt', 'con pagine in inglese, tedesco, francese, spagnolo, cinese, turco e arabo:',
     'con il sito in 36 lingue (tra cui inglese, tedesco, francese, spagnolo, cinese, turco e arabo):')
CARD_V = '<h3>Cinque lingue</h3><p>Italiano, inglese, tedesco, francese e spagnolo, per aziende italiane ed estere.</p>'
CARD_N = '<h3>36 lingue</h3><p>Sito in 36 lingue; per iscritto rispondiamo in tutte, al telefono in italiano, inglese e rumeno.</p>'
for f in ('chi-siamo/index.html', 'strumenti/genera-chi-siamo.py'): sost(f, CARD_V, CARD_N)

# 2. alt mancante
sost('montatori-fieristici/index.html',
     'sizes="(max-width:1180px) 0px, 440px" alt=""',
     'sizes="(max-width:1180px) 0px, 440px" alt="Montatori fieristici Danova Stand al lavoro su uno stand in fiera"')

# 3. popup su telefono: si apre sempre da solo, ma come riquadro piccolo in basso (circa 1/5 dello schermo),
#    senza velo scuro: la pagina resta visibile e cliccabile. Toccando il pulsante si apre il modulo completo.
JS = 'assets/js/ds-conversioni.js'
# tutto il blocco solo se la versione mini non c'e' ancora: i testi nuovi contengono quelli vecchi
if 'dsnl-esp' not in open(JS, encoding='utf-8').read():
    ORIG = "    setTimeout(function () { prova('dopo ' + Math.round(attesa / 1000) + ' s'); }, attesa);"
    TEL_VECCHIO = ("    var TEL = window.matchMedia ? window.matchMedia('(max-width: 760px)').matches : window.innerWidth <= 760;\n"
         "    /* su telefono niente popup a tutto schermo all'ingresso (regola Google sui popup invasivi): solo la pillola */\n"
         "    setTimeout(function () { if (TEL) { if (puoMostrare()) { ss('ds_nl_vista', '1'); pillola(); } return; } prova('dopo ' + Math.round(attesa / 1000) + ' s'); }, attesa);")
    TIMER = "    setTimeout(function () { prova('dopo ' + Math.round(attesa / 1000) + ' s'); }, attesa);   /* su telefono si apre in versione mini */"
    for v in (TEL_VECCHIO, ORIG): sost(JS, v, TIMER)
    # prova(): su telefono apre la versione mini
    sost(JS, "    apri(da);\n  }\n  var attesa",
             "    apri(da, window.innerWidth <= 760);\n  }\n  var attesa")
    # apri(): classe mini, niente aria-modal quando la pagina resta usabile
    sost(JS, "  function apri(da) {\n    if (iscritto()) return;\n    costruisci(); BOX.classList.add('open');",
             "  function apri(da, mini) {\n    if (iscritto()) return;\n    costruisci(); BOX.classList.toggle('mini', !!mini); BOX.setAttribute('aria-modal', mini ? 'false' : 'true'); BOX.classList.add('open');")
    # pulsante che dalla versione mini apre il modulo completo
    sost(JS, "<button class=\"dsnl-b\" type=\"submit\">' + esc(T.btn) + '</button>",
             "<button class=\"dsnl-b dsnl-esp\" type=\"button\">' + esc(T.btn) + '</button><button class=\"dsnl-b\" type=\"submit\">' + esc(T.btn) + '</button>")
    sost(JS, "    BOX.querySelector('.dsnl-no').onclick = function () { chiudi(true); };\n",
             "    BOX.querySelector('.dsnl-no').onclick = function () { chiudi(true); };\n"
             "    BOX.querySelector('.dsnl-esp').onclick = function () { BOX.classList.remove('mini'); BOX.setAttribute('aria-modal', 'true'); ev('preventivo', 'popup mini espanso'); };\n")
    # stile della versione mini (solo telefono)
    CSS_V = "+ '.dsnl-pill{bottom:calc(84px + env(safe-area-inset-bottom));left:10px}"
    CSS_N = ("+ '.dsnl-esp{display:none}.dsnl.mini{pointer-events:none}.dsnl.mini .dsnl-scrim{display:none}'\n"
             "    + '.dsnl.mini .dsnl-box{pointer-events:auto;left:10px;right:10px;bottom:calc(10px + env(safe-area-inset-bottom));width:auto;max-height:none;overflow:visible;border-radius:18px;grid-template-columns:auto 1fr;align-items:center;box-shadow:0 14px 40px rgba(0,0,0,.55)}'\n"
             "    + '.dsnl.mini .dsnl-vis{padding:14px 12px 14px 16px;justify-content:center;background:none}.dsnl.mini .dsnl-vis small,.dsnl.mini .dsnl-vis .sub{display:none}.dsnl.mini .dsnl-vis b.big{font-size:40px;margin:0}'\n"
             "    + '.dsnl.mini .dsnl-f{padding:14px 14px 14px 0;gap:8px}.dsnl.mini .dsnl-f h2{font-size:15.5px;line-height:1.25;padding-right:34px}'\n"
             "    + '.dsnl.mini .dsnl-sub,.dsnl.mini .dsnl-g,.dsnl.mini .dsnl-ok,.dsnl.mini .dsnl-e,.dsnl.mini .dsnl-no,.dsnl.mini button[type=submit]{display:none}'\n"
             "    + '.dsnl.mini .dsnl-esp{display:block;padding:11px 16px;font-size:14px}.dsnl.mini .dsnl-x{top:8px;right:8px;width:30px;height:30px;font-size:20px}'\n"
             "    " + CSS_V)
    sost(JS, CSS_V, CSS_N)

# 4. LinkedIn (pagina aziendale creata il 24/11/2026): link nel footer accanto agli altri social e in llms.txt.
#    Nello schema (sameAs) lo aggiunge ottimizza-seo.py (lista SOCIAL).
LI = 'https://www.linkedin.com/company/danova-stand/'
FB_LI = '<li><a href="https://www.facebook.com/profile.php?id=61594907955699" target="_blank" rel="noopener me">Facebook Danova Tech</a></li>'
for f in glob.glob('**/index.html', recursive=True):
    if f.startswith(('Claude outputs/', 'strumenti/', 'render/', 'private_area/')): continue
    if LI in open(f, encoding='utf-8').read(): continue
    sost(f, FB_LI, FB_LI + '\n        <li><a href="' + LI + '" target="_blank" rel="noopener me">LinkedIn Danova Stand</a></li>')
if LI not in open('llms.txt', encoding='utf-8').read():
    sost('llms.txt', 'Facebook https://www.facebook.com/profile.php?id=61594907955699', 'Facebook https://www.facebook.com/profile.php?id=61594907955699 · LinkedIn ' + LI)

print('file cambiati:', len(set(cambi)))
for c in sorted(set(cambi)): print('  ', c)
