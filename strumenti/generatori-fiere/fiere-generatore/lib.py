# -*- coding: utf-8 -*-
import os, re, json, html
from urllib.parse import urljoin
R=os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','..'))
SITE='https://danova-tech.com'
TODAY='2026-10-08'
TPL={'it':'servizi/meta-ads','en':'en/services/meta-ads','de':'de/leistungen/meta-ads','fr':'fr/services/meta-ads','es':'es/servicios/meta-ads'}
LOCALE={'it':'it_IT','en':'en_US','de':'de_DE','fr':'fr_FR','es':'es_ES','zh':'zh_CN','zh-hant':'zh_TW','tr':'tr_TR','ar':'ar_AR'}
LANGNAME={'it':'Italian','en':'English','de':'German','fr':'French','es':'Spanish','zh':'Chinese','zh-hant':'Chinese','tr':'Turkish','ar':'Arabic'}
CODE={'it':'IT','en':'EN','de':'DE','fr':'FR','es':'ES','zh':'简体','zh-hant':'繁體','tr':'TR','ar':'ع'}
HOMES={'it':'/','en':'/en/','de':'/de/','fr':'/fr/','es':'/es/','zh':'/en/','tr':'/en/','ar':'/en/'}
CUR=' aria-current="page"'
ARR='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 12h14M13 6l6 6-6 6"></path></svg>'
SVG=None
def svg():
    global SVG
    if SVG is None:
        h=open(os.path.join(R,'index.html'),encoding='utf-8').read()
        SVG=re.search(r'<svg class="fr-svg".*?</svg>',h,re.S).group(0)
    return SVG
E=lambda s: html.escape(s,quote=True)
HLC=lambda l: {'zh':'zh-Hans','zh-hant':'zh-Hant'}.get(l,l)  # codici hreflang (14/10/2026)

def absolutize(s, base):
    def fix(m):
        a,v=m.group(1),m.group(2)
        if re.match(r'^(/|#|[a-z][a-z0-9+.-]*:)',v,re.I): return m.group(0)
        return f'{a}="{urljoin(base,v)}"'
    return re.sub(r'\b(href|src)="([^"]*)"',fix,s)

# ---------------- blocchi di contenuto
def hero(eyebrow,h1,lead,cta,cta_href,cta2=None,cta2_href=None,extra=''):
    c2=f'\n      <a href="{cta2_href}" class="btn btn-g" data-mag><span class="lbl">{cta2}</span></a>' if cta2 else ''
    return f'''<section class="pg-hero">
  <div class="wrap">
    <div class="eyebrow mono" data-scramble>{eyebrow}</div>
    <h1 data-rv="up">{h1}</h1>
    <p class="lead" data-rv="up">{lead}</p>{extra}
    <div class="hero-cta" data-rv="up">
      <a href="{cta_href}" class="btn btn-p" data-mag><span class="sheen"></span><span class="lbl">{cta}</span>
        {ARR}</a>{c2}
    </div>
  </div>
  <div class="fr-hero-vis">{svg()}</div>
</section>
'''
def head(title,lead=None,eyebrow=None):
    e=f'\n      <div class="eyebrow mono" data-scramble>{eyebrow}</div>' if eyebrow else ''
    l=f'\n      <p class="lead" data-rv="up">{lead}</p>' if lead else ''
    return f'''    <div class="sec-head">{e}
      <h2 class="title" data-rv="up">{title}</h2>{l}
    </div>'''
def cards(id,title,lead,items,eyebrow=None):
    cs=''.join(f'''
      <article class="pg-card" data-tilt data-rv="blur">
        <span class="n">{i+1:02d}</span>
        <h3>{t}</h3>
        <p>{p}</p>
      </article>''' for i,(t,p) in enumerate(items))
    return f'''<section id="{id}">
  <div class="wrap">
{head(title,lead,eyebrow)}
    <div class="pg-cards">{cs}
    </div>
  </div>
</section>
'''
def testo(id,title,lead,paras,lista=None,eyebrow=None):
    ps=''.join(f'\n      <p>{p}</p>' for p in paras)
    li=''
    if lista: li='\n    <ul class="pg-lista" data-rv="up">'+''.join(f'\n      <li><b>{b}</b> {t}</li>' for b,t in lista)+'\n    </ul>'
    box=f'''
    <div class="pg-testo" data-rv="up">{ps}
    </div>''' if paras else ''
    return f'''<section id="{id}">
  <div class="wrap">
{head(title,lead,eyebrow)}{box}{li}
  </div>
</section>
'''
def passi(id,eyebrow,title,lead,steps):
    st=''.join(f'\n      <li><b>{b}</b><span>{t}</span></li>' for b,t in steps)
    return f'''<section id="{id}">
  <div class="wrap">
{head(title,lead,eyebrow)}
    <ol class="pg-passi" data-rv="up">{st}
    </ol>
  </div>
</section>
'''
def chips(id,title,lead,items,eyebrow=None):
    it=''.join((f'<a href="{u}">{t}</a>' if u else f'<span>{t}</span>') for t,u in items)
    return f'''<section id="{id}" class="fr-chips-sec">
  <div class="wrap">
{head(title,lead,eyebrow)}
    <div class="fr-chips" data-rv="up">{it}</div>
  </div>
</section>
'''
def faq(eyebrow,title,qa):
    d=''.join(f'''
      <details data-rv="up"><summary>{q}<span class="pm"></span></summary>
        <div class="ans"><p>{a}</p></div></details>''' for q,a in qa)
    return f'''<section id="faq">
  <div class="wrap">
{head(title,None,eyebrow)}
    <div class="faq">{d}
    </div>
  </div>
</section>
'''
def cta(title,p,label,href):
    return f'''<section class="pg-cta">
  <div class="wrap">
    <div class="box" data-rv="up">
      <h2 class="title">{title}</h2>
      <p>{p}</p>
      <a href="{href}" class="btn btn-p" data-mag><span class="sheen"></span><span class="lbl">{label}</span>
        {ARR}</a>
    </div>
  </div>
</section>
'''
def altri(title,links,id='altri'):
    a=''.join(f'\n      <a href="{u}">{t}</a>' for t,u in links)
    return f'''<section id="{id}">
  <div class="wrap">
    <div class="sec-head"><h2 class="title" data-rv="up">{title}</h2></div>
    <div class="pg-altri" data-rv="up">{a}
    </div>
  </div>
</section>
'''
def strip_tags(s): return html.unescape(re.sub(r'<[^>]+>','',s))

# ---------------- schema
def service_node(url,name,stype,desc,areas,offers,lang):
    return {"@type":"Service","@id":url+"#service","name":name,"serviceType":stype,"description":desc,
      "provider":{"@id":SITE+"/#organization"},"areaServed":areas,"availableLanguage":[LANGNAME[lang]],
      "hasOfferCatalog":{"@type":"OfferCatalog","name":name,"itemListElement":[{"@type":"Offer","itemOffered":{"@type":"Service","name":o}} for o in offers]}}
def article_node(url,headline,desc,lang):
    return {"@type":"Article","@id":url+"#article","headline":headline,"description":desc,"inLanguage":lang,
      "author":{"@id":SITE+"/#organization"},"publisher":{"@id":SITE+"/#organization"},
      "datePublished":TODAY,"dateModified":TODAY,"mainEntityOfPage":{"@id":url+"#webpage"},"image":SITE+"/assets/img/og-cover.jpg"}

# ---------------- pagina completa
ZH_TR_AR={
 'zh':dict(nav=['服务','展台搭建','流程','常见问题','联系我们'],talk='联系我们',skip='跳到内容',
   blurb='意大利技术公司，提供展台搭建、网站、软件与数字营销服务。',contact='联系方式',more='更多',home='英文主页',legal='隐私政策'),
 'tr':dict(nav=['Hizmetler','Fuar standı','Süreç','SSS','İletişim'],talk='Bize yazın',skip='İçeriğe geç',
   blurb='Fuar standı kurulumu, web siteleri, yazılım ve dijital pazarlama sunan İtalyan teknoloji şirketi.',contact='İletişim',more='Daha fazla',home='İngilizce ana sayfa',legal='Gizlilik politikası'),
 'ar':dict(nav=['الخدمات','تجهيز الأجنحة','طريقة العمل','الأسئلة الشائعة','اتصل بنا'],talk='تواصل معنا',skip='انتقل إلى المحتوى',
   blurb='شركة تقنية إيطالية تقدم تجهيز أجنحة المعارض والمواقع الإلكترونية والبرمجيات والتسويق الرقمي.',contact='التواصل',more='المزيد',home='الصفحة الرئيسية بالإنجليزية',legal='سياسة الخصوصية'),
}

def build(lang,path,title,desc,ogt,ogd,crumbs,main,qa,nodes,alts=None,breadcrumb_name=None,wp_extra=None,scripts=''):
    """path: '/x/y/'  crumbs: [(nome,url)...] ultimo senza url. alts: {lang:path} per hreflang"""
    tl = lang if lang in TPL else 'en'
    tp=TPL[tl]
    s=open(os.path.join(R,tp,'index.html'),encoding='utf-8').read()
    s=absolutize(s,'/'+tp+'/')
    url=SITE+path
    dir_='rtl' if lang=='ar' else 'ltr'
    s=re.sub(r'<html lang="[^"]*" dir="[^"]*"',f'<html lang="{"zh-Hans" if lang=="zh" else lang}" dir="{dir_}"',s,1)
    s=re.sub(r'<title>.*?</title>',f'<title>{E(title)}</title>',s,1,flags=re.S)
    s=re.sub(r'<meta name="description" content="[^"]*">',f'<meta name="description" content="{E(desc)}">',s,1)
    s=re.sub(r'<link rel="canonical" href="[^"]*">',f'<link rel="canonical" href="{url}">',s,1)
    s=re.sub(r'<link rel="alternate" hreflang="[^"]*" href="[^"]*">\n','',s)
    import intl_map; alts=intl_map.merge(path,alts,lang)  # 14/10/2026: hreflang IT<->EN<->ZH
    alts=alts or {lang:path}
    hl=''.join(f'<link rel="alternate" hreflang="{HLC(l)}" href="{SITE+p}">\n' for l,p in alts.items())
    xd=alts.get('it') or alts.get('en') or path
    hl+=f'<link rel="alternate" hreflang="x-default" href="{SITE+xd}">\n'
    s=s.replace(f'<link rel="canonical" href="{url}">\n',f'<link rel="canonical" href="{url}">\n',1)
    s=re.sub(r'(<meta name="color-scheme" content="dark">\n)',r'\1\n'+hl.replace('\\','\\\\'),s,1)
    s=re.sub(r'<meta property="og:url" content="[^"]*">',f'<meta property="og:url" content="{url}">',s)
    s=re.sub(r'<meta property="og:locale:alternate" content="[^"]*">\n','',s)
    loc=f'<meta property="og:locale" content="{LOCALE[lang]}">\n'+''.join(f'<meta property="og:locale:alternate" content="{LOCALE[l]}">\n' for l in alts if l!=lang)
    s=re.sub(r'<meta property="og:locale" content="[^"]*">\n',loc,s,1)
    for k in ('og:title','twitter:title'):
        s=re.sub(rf'(<meta (?:property|name)="{k}" content=")[^"]*"',lambda m:m.group(1)+E(ogt)+'"',s)
    for k in ('og:description','twitter:description'):
        s=re.sub(rf'(<meta (?:property|name)="{k}" content=")[^"]*"',lambda m:m.group(1)+E(ogd)+'"',s)
    # css dedicato
    s=s.replace('<link rel="stylesheet" href="/assets/css/site.css">','<link rel="stylesheet" href="/assets/css/site.css">\n<link rel="stylesheet" href="/assets/css/fiere.css">',1)
    # JSON-LD
    m=re.search(r'(<script type="application/ld\+json">)(.*?)(</script>)',s,re.S)
    g=json.loads(m.group(2)); keep=[]
    for n in g['@graph']:
        t=n.get('@type'); tt=t if isinstance(t,list) else [t]
        if any(x in ('Service','WebPage','BreadcrumbList','FAQPage','Article','ItemList','CollectionPage','HowTo','ImageObject') for x in tt): continue
        if 'Organization' in tt and isinstance(n.get('knowsAbout'),list):
            for k in ('Allestimenti fieristici','Montaggio stand fieristici','Exhibition stand design and build'):
                if k not in n['knowsAbout']: n['knowsAbout'].append(k)
        keep.append(n)
    bc=[{"@type":"ListItem","position":i+1,"name":strip_tags(nm),**({"item":SITE+u} if u else {})} for i,(nm,u) in enumerate(crumbs)]
    wp={"@type":"WebPage","@id":url+"#webpage","url":url,"name":title,"description":desc,"isPartOf":{"@id":SITE+"/#website"},
        "breadcrumb":{"@id":url+"#breadcrumb"},"inLanguage":"zh-Hans" if lang=="zh" else lang,"datePublished":TODAY,"dateModified":TODAY,
        "primaryImageOfPage":{"@type":"ImageObject","url":SITE+"/assets/img/og-cover.jpg"}}
    if nodes: wp["about"]={"@id":nodes[0]["@id"]}
    if wp_extra: wp.update(wp_extra)
    keep+= [wp,{"@type":"BreadcrumbList","@id":url+"#breadcrumb","itemListElement":bc}]+nodes
    if qa: keep.append({"@type":"FAQPage","@id":url+"#faq","isPartOf":{"@id":url+"#webpage"},"inLanguage":wp["inLanguage"],
        "mainEntity":[{"@type":"Question","name":strip_tags(q),"acceptedAnswer":{"@type":"Answer","text":strip_tags(a)}} for q,a in qa]})
    g['@graph']=keep
    s=s[:m.start(2)]+'\n'+json.dumps(g,ensure_ascii=False,indent=2)+'\n'+s[m.end(2):]
    # selettore lingua
    if len(alts)>1:
        order=[l for l in ('it','en','de','fr','es','zh','zh-hant','tr','ar') if l in alts]
        mk=lambda ind: ''.join(f'\n{ind}<a href="{alts[l]}" hreflang="{HLC(l)}"{CUR if l==lang else ""}>{CODE[l]}</a>' for l in order)
    else:
        order=['it','en','de','fr','es']
        mk=lambda ind: ''.join(f'\n{ind}<a href="{path if l==lang else HOMES[l]}" hreflang="{l}"{CUR if l==lang else ""}>{CODE[l]}</a>' for l in order)
    s=re.sub(r'<span class="lang-links">.*?</span>',lambda _: '<span class="lang-links">'+mk('        ')+'\n      </span>',s,1,flags=re.S)
    s=re.sub(r'<div class="mob-lang-links">.*?</div>',lambda _: '<div class="mob-lang-links">'+mk('    ')+'\n  </div>',s,1,flags=re.S)
    if lang in ZH_TR_AR:
        z=ZH_TR_AR[lang]
        navs=[('/en/#servizi',z['nav'][0]),(path,z['nav'][1]),('#metodo',z['nav'][2]),('#faq',z['nav'][3]),('#contatti-fiera',z['nav'][4])]
        nl=''.join(f'\n      <a href="{h}">{t}</a>' for h,t in navs)
        s=re.sub(r'(<nav class="links" aria-label="Menu">).*?(\n    </nav>)',lambda m:m.group(1)+nl+m.group(2),s,1,flags=re.S)
        s=re.sub(r'(<nav id="mob" aria-label="Menu">).*?(\n\n  <div class="mob-lang-links">)',lambda m:m.group(1)+nl.replace('\n      ','\n  ')+m.group(2),s,1,flags=re.S)
        s=s.replace('<span class="lbl">Let’s talk</span>',f'<span class="lbl">{z["talk"]}</span>').replace('href="/en/#contatti" class="btn btn-p"','href="#contatti-fiera" class="btn btn-p"')
        s=re.sub(r'<a href="#main" class="skip">[^<]*</a>',f'<a href="#main" class="skip">{z["skip"]}</a>',s,1)
        fb=f'''<div class="f-top">
      <div class="fb">
        <span class="brand"><img width="160" height="160" src="/assets/img/logo.png" alt="Logo Danova Tech" loading="lazy" decoding="async"><span class="wordmark"><b>DANOVA</b><i>TECH</i></span></span>
        <p>{z["blurb"]}</p>
      </div>
      <div><h5>{z["contact"]}</h5><ul>
        <li><a href="mailto:info@danova-tech.com">info@danova-tech.com</a></li>
        <li><a href="https://wa.me/393884706887">WhatsApp +39 388 470 6887</a></li>
        <li>Via Rigole 48, 31040 Mansuè (TV), Italia</li>
        <li>Fontanelle (TV) · Trumello (PV) · Vermezzo con Zelo (MI)</li>
      </ul></div>
      <div><h5>{z["more"]}</h5><ul>
        <li><a href="/en/exhibition-stand-builder-italy/">English</a></li>
        <li><a href="/de/messebau-italien/">Deutsch</a></li>
        <li><a href="/servizi/allestimenti-fieristici/">Italiano</a></li>
        <li><a href="/en/">{z["home"]}</a></li>
      </ul></div>
    </div>
    <div class="f-bot">'''
        s=re.sub(r'<div class="f-top[^"]*">.*?\n    <div class="f-bot">',lambda _:fb,s,1,flags=re.S)
    # footer: link al servizio fiere se c'e' la colonna servizi
    a=s.index('<main id="main">'); b=s.index('</main>')+len('</main>')
    cr=''.join((f'<a href="{u}">{nm}</a><em>/</em>' if u else nm) for nm,u in crumbs)
    s=s[:a]+f'<main id="main">\n\n<div class="wrap pg-crumbs">\n  {cr}\n</div>\n\n'+main+'\n</main>'+s[b:]
    if scripts: s=s.replace('<script src="/assets/js/pagina.js" defer></script>','<script src="/assets/js/pagina.js" defer></script>\n'+scripts,1)
    if lang in ('zh','ar'): s=s.replace(' data-scramble>','>')
    s=s.replace('>WhatsApp +39 388 470 6887<','>WhatsApp <bdi dir="ltr">+39 388 470 6887</bdi><')
    from immagini import inject  # render stand sotto l'hero, og:image e ImageObject (13/10/2026)
    s=inject(s,path)
    import citta_extra; s=citta_extra.inject(s,path)  # logistica da Mansue' nelle pagine citta'
    import citta_locale; s=citta_locale.inject(s,path)  # 14/10/2026: cosa cambia sul posto, per citta'
    import fiere_extra; s=fiere_extra.inject(s,path)  # esempi e preventivo nelle pagine brevi (13/10/2026)
    import legno; s=legno.inject(s,path,lang)  # 14/10/2026: elementi in legno prodotti da noi
    out=os.path.join(R,path.strip('/'),'index.html'); os.makedirs(os.path.dirname(out),exist_ok=True)
    open(out,'w',encoding='utf-8').write(s)
    return out
