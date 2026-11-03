import re, os, json, html
R=os.path.expanduser('~/mnt/dantech/danovatech')
SVG=r'''<svg class="fr-svg" viewBox="20 -40 470 460" aria-hidden="true" focusable="false">
<defs><linearGradient id="frg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#1E6BFF" stop-opacity=".55"/><stop offset="1" stop-color="#7aa9ff" stop-opacity=".15"/></linearGradient>
<linearGradient id="frc" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#bcd3ff" stop-opacity=".35"/><stop offset="1" stop-color="#bcd3ff" stop-opacity="0"/></linearGradient></defs>
<polygon class="pl fl" points="69.9,263.1 295,393.1 295,384 69.9,254"/><polygon class="pl fr" points="475.2,289.1 295,393.1 295,384 475.2,280"/><polygon class="pl tp" points="250,150 475.2,280 295,384 69.9,254"/><line class="gr" x1="272.5" y1="163" x2="92.4" y2="267"/><line class="gr" x1="295" y1="176" x2="114.9" y2="280"/><line class="gr" x1="317.5" y1="189" x2="137.4" y2="293"/><line class="gr" x1="340.1" y1="202" x2="159.9" y2="306"/><line class="gr" x1="362.6" y1="215" x2="182.5" y2="319"/><line class="gr" x1="385.1" y1="228" x2="205" y2="332"/><line class="gr" x1="407.6" y1="241" x2="227.5" y2="345"/><line class="gr" x1="430.1" y1="254" x2="250" y2="358"/><line class="gr" x1="452.6" y1="267" x2="272.5" y2="371"/><line class="gr" x1="227.5" y1="163" x2="452.6" y2="293"/><line class="gr" x1="205" y1="176" x2="430.1" y2="306"/><line class="gr" x1="182.5" y1="189" x2="407.6" y2="319"/><line class="gr" x1="159.9" y1="202" x2="385.1" y2="332"/><line class="gr" x1="137.4" y1="215" x2="362.6" y2="345"/><line class="gr" x1="114.9" y1="228" x2="340.1" y2="358"/><line class="gr" x1="92.4" y1="241" x2="317.5" y2="371"/><polygon class="wl side" points="250,150 69.9,254 69.9,98 250,-6"/><polygon class="wa fl" points="69.9,254 76.6,257.9 76.6,101.9 69.9,98"/><polygon class="wa fr" points="256.8,153.9 76.6,257.9 76.6,101.9 256.8,-2.1"/><polygon class="wa tp" points="250,-6 256.8,-2.1 76.6,101.9 69.9,98"/><polygon class="wl back" points="250,157.8 468.4,283.9 468.4,127.9 250,1.8"/><polygon class="wa fl" points="250,157.8 468.4,283.9 468.4,127.9 250,1.8"/><polygon class="wa fr" points="475.2,280 468.4,283.9 468.4,127.9 475.2,124"/><polygon class="wa tp" points="256.8,-2.1 475.2,124 468.4,127.9 250,1.8"/><polygon class="gfx" points="301.6,130.6 414.1,195.6 414.1,122.8 301.6,57.8"/><line class="gl" x1="312.6" y1="82.7" x2="393.7" y2="129.5"/><line class="gl" x1="312.6" y1="98.3" x2="371.1" y2="132.1"/><line class="gl" x1="312.6" y1="111.3" x2="353.1" y2="134.7"/><polygon class="sh" points="225.5,130.6 157.9,169.6 171.2,177.3 238.7,138.3"/><polygon class="sh" points="225.5,94.2 157.9,133.2 171.2,140.9 238.7,101.9"/><polygon class="sh" points="225.5,57.8 157.9,96.8 171.2,104.5 238.7,65.5"/><polygon class="hd fl" points="272.5,20 452.6,124 452.6,98 272.5,-6"/><polygon class="hd fr" points="463.9,117.5 452.6,124 452.6,98 463.9,91.5"/><polygon class="hd tp" points="283.8,-12.5 463.9,91.5 452.6,98 272.5,-6"/><line class="arm" x1="299.5" y1="33" x2="272.5" y2="61.6"/><circle class="spot" cx="272.5" cy="61.6" r="3.2"/><polygon class="cone" points="272.5,61.6 234.2,208 261.3,223.6"/><line class="arm" x1="355.8" y1="65.5" x2="328.8" y2="94.1"/><circle class="spot" cx="328.8" cy="94.1" r="3.2"/><polygon class="cone" points="328.8,94.1 290.5,240.5 317.5,256.1"/><line class="arm" x1="412.1" y1="98" x2="385.1" y2="126.6"/><circle class="spot" cx="385.1" cy="126.6" r="3.2"/><polygon class="cone" points="385.1,126.6 346.8,273 373.8,288.6"/><polygon class="tt fl" points="128.4,251.4 150.9,264.4 150.9,155.2 128.4,142.2"/><polygon class="tt fr" points="173.4,251.4 150.9,264.4 150.9,155.2 173.4,142.2"/><polygon class="tt tp" points="150.9,129.2 173.4,142.2 150.9,155.2 128.4,142.2"/><polygon class="ct fl" points="227.5,298.2 304,342.4 304,285.2 227.5,241"/><polygon class="ct fr" points="335.6,324.2 304,342.4 304,285.2 335.6,267"/><polygon class="ct tp" points="259,222.8 335.6,267 304,285.2 227.5,241"/><polygon class="cttop fl" points="218.5,241 304,290.4 304,285.2 218.5,235.8"/><polygon class="cttop fr" points="344.6,267 304,290.4 304,285.2 344.6,261.8"/><polygon class="cttop tp" points="259,212.4 344.6,261.8 304,285.2 218.5,235.8"/><ellipse class="stool" cx="196" cy="251.4" rx="10" ry="5"/><line class="arm" x1="196" y1="290.4" x2="196" y2="251.4"/><circle class="mk" cx="295" cy="384" r="4"/><circle class="mk" cx="69.9" cy="254" r="4"/><circle class="mk" cx="475.2" cy="280" r="4"/><line class="dim" x1="49.6" y1="265.7" x2="274.8" y2="395.7"/></svg>'''

CSS=r'''
/* ===== ALLESTIMENTI FIERISTICI (novita' ottobre 2026) ===== */
#fiere{padding-top:clamp(56px,7vw,100px)}
.fr-card{display:grid;grid-template-columns:minmax(0,1.08fr) minmax(0,.92fr);gap:clamp(24px,4vw,56px);align-items:center;padding:clamp(26px,4.5vw,60px);border-color:rgba(122,169,255,.28);background:radial-gradient(120% 90% at 100% 0%,rgba(30,107,255,.2),transparent 60%),linear-gradient(160deg,rgba(255,255,255,.06),rgba(255,255,255,.012))}
.fr-card .edge{opacity:1}
.fr-top{display:flex;flex-wrap:wrap;align-items:center;gap:12px 16px;margin-bottom:20px}
.fr-top .eyebrow{margin-bottom:0}
.fr-badge{display:inline-flex;align-items:center;gap:8px;padding:7px 13px 7px 11px;border-radius:99px;background:linear-gradient(120deg,var(--blue),#7aa9ff);color:#fff;font:700 11px/1 'JetBrains Mono',ui-monospace,monospace;letter-spacing:.14em;text-transform:uppercase;box-shadow:0 8px 26px -10px rgba(30,107,255,.9)}
.fr-badge i,.news-pill b i{width:7px;height:7px;border-radius:50%;background:#fff;animation:frping 1.8s infinite}
@keyframes frping{0%{box-shadow:0 0 0 0 rgba(255,255,255,.75)}70%,100%{box-shadow:0 0 0 8px rgba(255,255,255,0)}}
.fr-card .title{font-size:clamp(2rem,4.4vw,3.4rem)}
.fr-card .lead{max-width:56ch}
.fr-items{display:grid;gap:12px;margin-top:30px}
.fr-it{display:flex;gap:16px;align-items:flex-start;padding:16px 18px;border:1px solid var(--line);border-radius:16px;background:rgba(255,255,255,.025);transition:border-color .4s,background .4s}
.fr-it:hover{border-color:rgba(122,169,255,.4);background:rgba(30,107,255,.07)}
.fr-ic{flex:none;width:42px;height:42px;border-radius:12px;display:grid;place-items:center;color:#cfe0ff;background:rgba(30,107,255,.16);border:1px solid rgba(122,169,255,.3)}
.fr-ic svg{width:20px;height:20px}
.fr-it h3{font-size:1.06rem;margin:0 0 4px}
.fr-it p{color:var(--muted);font-size:14.5px;line-height:1.55;margin:0}
.fr-pts{list-style:none;display:flex;flex-wrap:wrap;gap:10px 22px;margin:22px 0 0;padding:0}
.fr-pts li{display:flex;gap:8px;align-items:center;font-size:14px;color:#b9c2d6}
.fr-pts svg{width:16px;height:16px;color:var(--blue-2);flex:none}
.fr-cta{margin-top:30px;display:flex;flex-wrap:wrap;gap:12px}
.fr-vis{position:relative}
.fr-vis::before{content:"";position:absolute;inset:12% 6%;background:radial-gradient(closest-side,rgba(30,107,255,.3),transparent);filter:blur(24px)}
.fr-svg{position:relative;width:100%;height:auto;display:block}
.fr-svg *{vector-effect:non-scaling-stroke;stroke-linejoin:round}
.fr-svg .pl.tp{fill:rgba(30,107,255,.07);stroke:rgba(122,169,255,.45);stroke-width:1}
.fr-svg .pl.fl,.fr-svg .pl.fr{fill:rgba(30,107,255,.16);stroke:rgba(122,169,255,.45);stroke-width:1}
.fr-svg .gr{stroke:rgba(122,169,255,.12);stroke-width:1}
.fr-svg .wl{fill:rgba(255,255,255,.035);stroke:rgba(122,169,255,.5);stroke-width:1}
.fr-svg .wl.back{fill:rgba(30,107,255,.06)}
.fr-svg .wa.tp{fill:rgba(122,169,255,.35);stroke:rgba(122,169,255,.6);stroke-width:1}
.fr-svg .wa.fl,.fr-svg .wa.fr{fill:rgba(122,169,255,.18);stroke:rgba(122,169,255,.6);stroke-width:1}
.fr-svg .gfx{fill:url(#frg);stroke:#7aa9ff;stroke-width:1.2}
.fr-svg .gl{stroke:rgba(255,255,255,.75);stroke-width:2.4;stroke-linecap:round}
.fr-svg .sh{fill:rgba(122,169,255,.25);stroke:rgba(122,169,255,.7);stroke-width:1}
.fr-svg .hd.fl{fill:#1E6BFF;stroke:#7aa9ff;stroke-width:1}
.fr-svg .hd.fr{fill:#1550c4;stroke:#7aa9ff;stroke-width:1}
.fr-svg .hd.tp{fill:#5b93ff;stroke:#9fc0ff;stroke-width:1}
.fr-svg .arm{stroke:rgba(188,211,255,.7);stroke-width:1.4}
.fr-svg .spot{fill:#fff;filter:drop-shadow(0 0 6px #7aa9ff)}
.fr-svg .cone{fill:url(#frc);animation:frpulse 4s ease-in-out infinite}
.fr-svg .tt.fl{fill:rgba(30,107,255,.5);stroke:#7aa9ff;stroke-width:1}
.fr-svg .tt.fr{fill:rgba(30,107,255,.3);stroke:#7aa9ff;stroke-width:1}
.fr-svg .tt.tp{fill:#7aa9ff}
.fr-svg .ct.fl{fill:rgba(255,255,255,.1);stroke:rgba(188,211,255,.8);stroke-width:1}
.fr-svg .ct.fr{fill:rgba(255,255,255,.05);stroke:rgba(188,211,255,.8);stroke-width:1}
.fr-svg .ct.tp{fill:rgba(255,255,255,.1)}
.fr-svg .cttop.fl,.fr-svg .cttop.fr{fill:#cfe0ff;stroke:#fff;stroke-width:.6}
.fr-svg .cttop.tp{fill:#eaf1ff}
.fr-svg .stool{fill:rgba(122,169,255,.5);stroke:#bcd3ff;stroke-width:1}
.fr-svg .mk{fill:none;stroke:#7aa9ff;stroke-width:1.4;stroke-dasharray:3 3;animation:frspin 6s linear infinite;transform-box:fill-box;transform-origin:center}
.fr-svg .dim{stroke:rgba(122,169,255,.5);stroke-width:1;stroke-dasharray:4 4}
@keyframes frpulse{0%,100%{opacity:.55}50%{opacity:1}}
@keyframes frspin{to{transform:rotate(360deg)}}
@media (max-width:900px){.fr-card{grid-template-columns:1fr}.fr-vis{order:-1;max-width:420px;margin:0 auto -10px;width:100%}}
@media (prefers-reduced-motion:reduce){.fr-svg .cone,.fr-svg .mk,.fr-badge i,.news-pill b i{animation:none}}
.news-pill{display:inline-flex;align-items:center;gap:10px;max-width:100%;padding:6px 14px 6px 6px;border-radius:99px;border:1px solid rgba(122,169,255,.38);background:rgba(30,107,255,.13);-webkit-backdrop-filter:blur(8px);backdrop-filter:blur(8px);font-size:13.5px;line-height:1.3;color:#dbe6ff;margin-bottom:24px;transition:border-color .3s,background .3s}
.news-pill:hover{border-color:#7aa9ff;background:rgba(30,107,255,.24)}
.news-pill b{display:inline-flex;align-items:center;gap:7px;flex:none;padding:5px 10px;border-radius:99px;background:var(--blue);color:#fff;font:700 10.5px/1 'JetBrains Mono',ui-monospace,monospace;letter-spacing:.12em;text-transform:uppercase}
.news-pill svg{width:14px;height:14px;flex:none}
.links a.nav-new{position:relative}
.links a.nav-new::after{content:"";position:absolute;top:-1px;right:-9px;width:6px;height:6px;border-radius:50%;background:#7aa9ff;box-shadow:0 0 8px #1E6BFF}
'''

IC_MAT='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="m12 3 9 5-9 5-9-5 9-5Z"/><path d="m3 12.5 9 5 9-5"/><path d="m3 17 9 5 9-5"/></svg>'
IC_CMP='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2.5 20.2 7.2v9.6L12 21.5l-8.2-4.7V7.2Z"/><circle cx="12" cy="12" r="3.4"/></svg>'
IC_MNT='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z"/></svg>'
CHK='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4"><path d="M20 6 9 17l-5-5"></path></svg>'
ARR='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 12h14M13 6l6 6-6 6"></path></svg>'

T={
'it':dict(nav='Fiere',badge='Novità',news='Allestimenti fieristici chiavi in mano',eyebrow='Allestimenti fieristici',
 title='Il tuo stand in fiera,<br><span class="grad">chiavi in mano.</span>',
 lead="Da oggi ci occupiamo anche di allestimenti fieristici. Qualunque sia la tua azienda, troviamo noi il materiale necessario, tutta la componentistica richiesta e i montatori che costruiscono lo stand direttamente in fiera. Tu pensi ai clienti, al resto pensiamo noi.",
 a=('Materiali',"Pareti, pavimentazioni, grafiche, arredi e illuminazione: cerchiamo e procuriamo tutto il materiale che serve al tuo stand."),
 b=('Componentistica',"Strutture, profili, raccordi e ogni componente richiesto dal progetto o dal regolamento della fiera, già pronto all'uso."),
 c=('Montatori in fiera',"Squadre di montatori che costruiscono il tuo stand direttamente in fiera, nei tempi di allestimento previsti dall'organizzatore."),
 pts=['Un unico referente dal progetto al montaggio','Preventivo chiaro prima di partire','Per aziende di ogni settore e dimensione'],
 cta='Richiedi un preventivo per lo stand',cta2='Scopri il servizio',opt='Allestimento fieristico'),
'en':dict(nav='Trade fairs',badge='New',news='Turnkey trade fair stands',eyebrow='Trade fair stands',
 title='Your trade fair stand,<br><span class="grad">turnkey.</span>',
 lead="We now also handle trade fair stands. Whatever your company, we source the materials you need, every component required and the installers who build your stand right at the fair. You focus on your customers, we take care of the rest.",
 a=('Materials',"Walls, flooring, graphics, furniture and lighting: we find and supply all the materials your stand needs."),
 b=('Components',"Structures, profiles, fittings and every component required by the project or the fair's technical rules, ready to use."),
 c=('Installers at the fair',"Installation crews who build your stand right at the fair, within the set-up times set by the organiser."),
 pts=['One contact from design to installation','A clear quote before we start','For companies of every sector and size'],
 cta='Get a quote for your stand',cta2='Learn more',opt='Trade fair stand'),
'de':dict(nav='Messen',badge='Neu',news='Messestände schlüsselfertig',eyebrow='Messebau',
 title='Ihr Messestand,<br><span class="grad">schlüsselfertig.</span>',
 lead="Ab sofort übernehmen wir auch den Messebau. Für jedes Unternehmen besorgen wir das nötige Material, alle geforderten Komponenten und die Monteure, die Ihren Stand direkt auf der Messe aufbauen. Sie kümmern sich um Ihre Kunden, wir um den Rest.",
 a=('Material',"Wände, Böden, Grafiken, Möbel und Beleuchtung: Wir finden und liefern das gesamte Material, das Ihr Stand braucht."),
 b=('Komponenten',"Strukturen, Profile, Verbinder und jedes Bauteil, das das Projekt oder die technischen Richtlinien der Messe verlangen – einsatzbereit."),
 c=('Monteure vor Ort',"Montageteams, die Ihren Stand direkt auf der Messe aufbauen – in den vom Veranstalter vorgegebenen Aufbauzeiten."),
 pts=['Ein Ansprechpartner von der Planung bis zum Aufbau','Ein klares Angebot vor dem Start','Für Unternehmen jeder Branche und Größe'],
 cta='Angebot für Ihren Stand anfragen',cta2='Mehr erfahren',opt='Messestand / Messebau'),
'fr':dict(nav='Salons',badge='Nouveau',news='Stands de salon clés en main',eyebrow='Stands de salon',
 title='Votre stand de salon,<br><span class="grad">clés en main.</span>',
 lead="Nous prenons désormais aussi en charge l'aménagement de stands de salon. Quelle que soit votre entreprise, nous trouvons les matériaux nécessaires, tous les composants requis et les monteurs qui construisent votre stand directement sur le salon. Vous vous occupez de vos clients, nous du reste.",
 a=('Matériaux',"Cloisons, sols, graphismes, mobilier et éclairage : nous trouvons et fournissons tous les matériaux dont votre stand a besoin."),
 b=('Composants',"Structures, profilés, raccords et chaque composant exigé par le projet ou le règlement technique du salon, prêts à l'emploi."),
 c=('Monteurs sur place',"Des équipes de monteurs qui construisent votre stand directement sur le salon, dans les délais de montage fixés par l'organisateur."),
 pts=['Un seul interlocuteur, du projet au montage','Un devis clair avant de commencer','Pour les entreprises de tous secteurs et toutes tailles'],
 cta='Demander un devis pour votre stand',cta2='En savoir plus',opt='Stand de salon'),
'es':dict(nav='Ferias',badge='Novedad',news='Stands feriales llave en mano',eyebrow='Montaje de stands',
 title='Tu stand en la feria,<br><span class="grad">llave en mano.</span>',
 lead="Ahora también nos ocupamos del montaje de stands feriales. Sea cual sea tu empresa, encontramos el material necesario, todos los componentes que se requieren y los montadores que construyen tu stand directamente en la feria. Tú te ocupas de tus clientes; nosotros, del resto.",
 a=('Materiales',"Paredes, suelos, gráficas, mobiliario e iluminación: buscamos y suministramos todo el material que necesita tu stand."),
 b=('Componentes',"Estructuras, perfiles, uniones y cualquier componente que exija el proyecto o la normativa técnica de la feria, listos para usar."),
 c=('Montadores en la feria',"Equipos de montadores que construyen tu stand directamente en la feria, dentro de los plazos de montaje fijados por el organizador."),
 pts=['Un único interlocutor del proyecto al montaje','Presupuesto claro antes de empezar','Para empresas de cualquier sector y tamaño'],
 cta='Pide presupuesto para tu stand',cta2='Más información',opt='Stand ferial'),
}
FILES={'it':'index.html','en':'en/index.html','de':'de/index.html','fr':'fr/index.html','es':'es/index.html'}
e=lambda s: html.escape(s,quote=False)

def section(L,t):
    items=''.join(f'''
          <div class="fr-it"><span class="fr-ic">{ic}</span><div><h3 data-i18n="fiere.{k}.t">{e(t[k][0])}</h3><p data-i18n="fiere.{k}.p">{e(t[k][1])}</p></div></div>''' for k,ic in (('a',IC_MAT),('b',IC_CMP),('c',IC_MNT)))
    pts=''.join(f'<li>{CHK}<span data-i18n="fiere.pts.{i}">{e(p)}</span></li>' for i,p in enumerate(t['pts']))
    cta2=f'\n          <a href="/servizi/allestimenti-fieristici/" class="btn btn-g" data-mag><span class="lbl" data-i18n="fiere.cta2">{e(t["cta2"])}</span></a>' if L=='it' else ''
    return f'''<!-- ===== ALLESTIMENTI FIERISTICI (NOVITA') ===== -->
<section id="fiere">
  <div class="wrap">
    <div class="card fr-card" data-rv="up"><i class="edge"></i>
      <div class="fr-txt">
        <div class="fr-top"><span class="fr-badge"><i></i><span data-i18n="fiere.badge">{e(t['badge'])}</span></span><span class="eyebrow mono" data-i18n="fiere.eyebrow">{e(t['eyebrow'])}</span></div>
        <h2 class="title" data-i18n-html="fiere.title">{t['title']}</h2>
        <p class="lead" data-i18n="fiere.lead">{e(t['lead'])}</p>
        <div class="fr-items">{items}
        </div>
        <ul class="fr-pts">{pts}</ul>
        <div class="fr-cta">
          <a href="#contatti" class="btn btn-p" data-mag data-pick-tipo><span class="sheen"></span><span class="lbl" data-i18n="fiere.cta">{e(t['cta'])}</span>
            {ARR}</a>{cta2}
        </div>
      </div>
      <div class="fr-vis">{SVG}</div>
    </div>
  </div>
</section>

<div class="wrap"><div class="divider"></div></div>

'''

for L,f in FILES.items():
    t=T[L]; p=os.path.join(R,f); s=open(p,encoding='utf-8').read()
    assert 'id="fiere"' not in s, 'gia applicato '+f
    # CSS
    i=s.index('</style>'); s=s[:i]+CSS+s[i:]
    # nav (desktop + mobile)
    s,n=re.subn(r'(<a href="#servizi" data-i18n="nav\.servizi"[^>]*>)', lambda m: f'<a href="#fiere" class="nav-new" data-i18n="nav.fiere">{e(t["nav"])}</a>\n      '+m.group(1), s)
    assert n==2,(f,n)
    # hero pill
    pill=f'<a href="#fiere" class="news-pill"><b><i></i><span data-i18n="fiere.badge">{e(t["badge"])}</span></b><span data-i18n="fiere.news">{e(t["news"])}</span>{ARR}</a>\n    '
    s=s.replace('<h1 class="hero-t"',pill+'<h1 class="hero-t"',1)
    # section
    mk='<!-- ===== SERVIZI ===== -->'; assert s.count(mk)==1
    s=s.replace(mk,section(L,t)+mk)
    # form option (static)
    m=re.search(r'(<select id="tipo"[^>]*>.*?)(<option>[^<]*</option></select>)',s,re.S); assert m
    s=s[:m.start()]+m.group(1)+f'<option>{e(t["opt"])}</option>'+m.group(2)+s[m.end():]
    open(p,'w',encoding='utf-8').write(s)
    # dizionario
    jp=os.path.join(R,'assets/js/i18n-%s.js'%L); j=open(jp,encoding='utf-8').read()
    assert 'fiere:' not in j
    j=j.replace('nav:{servizi:','nav:{fiere:%s,servizi:'%json.dumps(t['nav'],ensure_ascii=False),1)
    obj={'badge':t['badge'],'news':t['news'],'eyebrow':t['eyebrow'],'title':t['title'],'lead':t['lead'],
         'a':{'t':t['a'][0],'p':t['a'][1]},'b':{'t':t['b'][0],'p':t['b'][1]},'c':{'t':t['c'][0],'p':t['c'][1]},
         'pts':t['pts'],'cta':t['cta'],'cta2':t['cta2']}
    js='  fiere:'+json.dumps(obj,ensure_ascii=False)+',\n'
    k=j.index('\n  prezzi:{')+1; j=j[:k]+js+j[k:]
    a=j.index('opts:['); b=j.index(']',a); c=j.rindex(',',a,b)
    j=j[:c]+','+json.dumps(t['opt'],ensure_ascii=False)+j[c:]
    open(jp,'w',encoding='utf-8').write(j)
    print('ok',L)

# home.js: il bottone della sezione fiere preseleziona la voce nel modulo
hp=os.path.join(R,'assets/js/home.js'); h=open(hp,encoding='utf-8').read()
if 'data-pick-tipo' not in h:
    h+='''
/* Allestimenti fieristici: il pulsante della sezione preseleziona la voce nel modulo contatti */
document.addEventListener('click',e=>{
  const a=e.target.closest&&e.target.closest('[data-pick-tipo]'); if(!a) return;
  const s=document.getElementById('tipo'); if(!s||s.options.length<3) return;
  s.selectedIndex=s.options.length-2; s.dispatchEvent(new Event('change',{bubbles:true}));
});
'''
    open(hp,'w',encoding='utf-8').write(h); print('ok home.js')
