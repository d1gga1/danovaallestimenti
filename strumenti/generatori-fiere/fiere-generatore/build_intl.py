# -*- coding: utf-8 -*-
"""Pagine EN e ZH per espositori stranieri (soprattutto cinesi) nelle fiere italiane. 14 ottobre 2026.
Uso (dalla cartella fiere-generatore):  python3 build_intl.py
Genera 12 pagine fiera + 4 citta' + 1 guida in inglese e in cinese, poi aggiorna hreflang e
selettore lingua sulle pagine italiane corrispondenti (intl_map.patch). Idempotente."""
import sys, os, json; sys.path.insert(0, os.path.dirname(__file__))
from lib import *
from nuove_common import scheda
from urllib.parse import quote
import dati_calendario as DC, dati_intl as DI, intl_map as IM

MESI_EN = ['January','February','March','April','May','June','July','August','September','October','November','December']
def when(fid, L):
    _, _, _, _, s, e, c, _, _ = DC.FIERE[fid]
    y1, m1, d1 = map(int, s.split('-')); y2, m2, d2 = map(int, e.split('-'))
    if L == 'en':
        if not c: return f"{MESI_EN[m1-1]} {y1} (dates to be confirmed)"
        if (y1, m1) == (y2, m2): return f"{d1}–{d2} {MESI_EN[m1-1]} {y1}"
        return f"{d1} {MESI_EN[m1-1]} – {d2} {MESI_EN[m2-1]} {y2}"
    if not c: return f"{y1}年{m1}月（日期待定）"
    if (y1, m1) == (y2, m2): return f"{y1}年{m1}月{d1}日至{d2}日"
    return f"{y1}年{m1}月{d1}日至{m2}月{d2}日"

VEN = {'rho': ('Fiera Milano Rho', 'Milan', '米兰Rho展览中心', '米兰'), 'bologna': ('BolognaFiere', 'Bologna', '博洛尼亚展览中心', '博洛尼亚'),
       'verona': ('Veronafiere', 'Verona', '维罗纳展览中心', '维罗纳'), 'vicenza': ('Vicenza Expo Centre', 'Vicenza', '维琴察展览中心', '维琴察'),
       'rimini': ('Rimini Expo Centre', 'Rimini', '里米尼展览中心', '里米尼'),
       'parma': ('Fiere di Parma', 'Parma', '帕尔马展览中心', '帕尔马'), 'firenze': ('Fortezza da Basso', 'Florence', 'Fortezza da Basso展馆', '佛罗伦萨'),
       'riva': ('Riva del Garda Fierecongressi', 'Riva del Garda', '里瓦展览会议中心', '加尔达湖里瓦'), 'pordenone': ('Pordenone Fiere', 'Pordenone', '波代诺内展览中心', '波代诺内')}
PILL = {'en': '/en/exhibition-stand-builder-italy/', 'zh': '/zh/italy-exhibition-stand/'}
GUIDE = {'en': '/en/exhibiting-at-trade-fairs-in-italy/', 'zh': '/zh/italy-trade-fair-guide/'}
FAIR_URL = {L: {f['k']: f"/{L}/{f[L]['slug']}/" for f in DI.FAIRS} for L in ('en', 'zh')}
CITY_URL = {L: {c['s']: f"/{L}/{c[L]['slug']}/" for c in DI.CITIES} for L in ('en', 'zh')}
FAIR_BY = {f['k']: f for f in DI.FAIRS}
W = lambda t: sum(2 if ord(ch) > 0x2e80 else 1 for ch in t)  # larghezza titolo (CJK = 2)

T = {
 'en': dict(home='Home', pillar='Exhibition stands in Italy', req='Request a quote for your stand', how='How we work',
   cards_t='What we do for your stand', cards_l='We can handle everything from design to dismantling, or only the part you are missing.',
   cards=[("Design and 3D render", "Your stand designed on your floor space and position in the hall, approved by you before anything is built."),
     ("Materials and components", "Structures, walls, floors, furniture and every component required by the design and by the fair's technical regulations."),
     ("Graphics, lighting and electrics", "Printing, electrical system with Italian declaration of conformity, lighting, carpet, screens and LED walls."),
     ("Installation crews on site", "Partner crews managed by us build the stand during the official build-up days and dismantle it after the show."),
     ("Rent or buy", "Shell scheme, modular, fabric or custom-built stands, rented or owned."),
     ("Logistics, storage, paperwork", "Transport, passes and unloading slots, approval of the project by the organiser, storage between shows.")],
   foreign_t='Exhibiting from China or from abroad', foreign_l='Most of our international clients have never worked with an Italian stand builder before. This is how we make it simple.',
   foreign=[("One contact person.", "From the first sketch to dismantling you talk to the same person, by email, phone or WhatsApp: in English, or in Chinese with the help of translation tools."),
     ("Coordinated crews, warehouse and production.", "Partner installation crews, our warehouse and trusted workshops for all wood-based structures and furniture, coordinated by one team: one point of control over quality and deadlines."),
     ("Large and two-storey stands.", "From small shell scheme stands to custom stands of over 300 m², including two-storey stands with meeting rooms upstairs."),
     ("We work with your design.", "If your designer in China has already drawn the stand, we build it, check it against the Italian technical regulations and propose changes only where needed."),
     ("Contract with your company.", "We sign and invoice directly with your company, in China or abroad, with an itemised quote in euro."),
     ("Approvals and certificates.", "We submit drawings to the organiser and provide the electrical declaration of conformity and fire-rating certificates."),
     ("Your freight forwarder, our schedule.", "Your exhibits travel with your forwarder; we coordinate unloading slots and times so goods and stand arrive in the right order."),
     ("Storage for the next edition.", "If you exhibit every year, we keep your stand in our warehouse in Italy and bring it back for the next show.")],
   steps_ey='How we work', steps=[("Brief", "Fair, hall, floor space and type of stand, goals and budget. If you already have a design, we start from that."),
     ("Design and quote", "3D render and itemised quote. Work starts only when you approve."),
     ("Organiser approvals", "Drawings, electrical system, connections and passes submitted according to the fair's technical regulations."),
     ("Production and build-up", "Structures, graphics and furniture checked before leaving; installation during the build-up days."),
     ("Show and dismantling", "Assistance during the show, dismantling at the end and, if the stand is yours, storage for next time.")],
   faq_ey='FAQ', faq_t='Questions we are <span class="grad">often asked.</span>',
   gen_qa=[("How much does a stand for {n} cost?", "It depends on floor space, type of structure, finishes, electrics and services. We do not publish standard prices: we send you a free itemised quote for your project."),
     ("Can we communicate in Chinese?", "Yes. Write to us in Chinese or English: we reply in Chinese with the help of translation tools and confirm important technical details in English too, to avoid misunderstandings."),
     ("Is the stand rented or bought?", "As you prefer: shell scheme, modular, fabric or custom-built, rented or bought. If it is yours, we store it for the next edition.")],
   k_t='Exhibiting at {n}?', k_p='Tell us the fair, the dates and your floor space. We will reply with what you need and what it costs, also at short notice.',
   mail='Write to us', wa='WhatsApp', related='Related pages', it_ver='Italian version',
   wa_txt='Hello, we are exhibiting at {n} and need a stand. Company: … Stand size (m²): …',
   subj='Stand request: {n}'),
 'zh': dict(home='首页', pillar='意大利展台搭建', req='获取展台报价', how='服务流程',
   cards_t='我们为您的展台提供的服务', cards_l='从设计到拆除我们都可以全程负责，也可以只做您缺少的那一部分。',
   cards=[("设计与三维效果图", "根据您的展位面积和在展馆中的位置设计展台，经您确认后才开始施工。"),
     ("材料与配件", "结构、墙板、地面、家具，以及设计方案和展会技术规定所需的全部配件。"),
     ("平面、灯光与电气", "印刷制作、带意大利合格声明的电气系统、照明、地毯、显示屏和LED屏。"),
     ("现场搭建团队", "我们自己的团队和合作团队在官方布展期内搭建展台，展会结束后拆除。"),
     ("租赁或购买", "标准展台、模块化展台、张拉布展台或特装展台，可租可买。"),
     ("物流、仓储与手续", "运输、证件和卸货时段、主办方方案审批，以及两次展会之间的仓储。")],
   foreign_t='从中国或海外来意大利参展', foreign_l='我们的大多数国际客户以前从未和意大利搭建商合作过。我们这样让一切变得简单。',
   foreign=[("一位专属联系人。", "从第一张草图到拆展，始终由同一个人对接，通过邮件、电话或WhatsApp沟通：可以用英文，也可以用中文（我们借助翻译工具回复）。"),
     ("自有施工团队、仓库和生产。", "由我们统筹的合作搭建团队、自有仓库，以及长期合作的木制结构和家具工坊：一个团队负责到底，质量和工期更可控。"),
     ("大型展台和双层展台。", "从小型标准展台到300平方米以上的特装展台，包括上层设有会议室的双层展台。"),
     ("可以按您的设计施工。", "如果您在国内的设计师已经完成展台设计，我们负责搭建，并按照意大利技术规定进行核查，只在必要时提出修改。"),
     ("直接与贵公司签约。", "我们直接与贵公司（中国或海外公司）签订合同并开具发票，报价以欧元逐项列明。"),
     ("审批和证书。", "我们向主办方提交图纸，并提供电气合格声明和防火等级证书。"),
     ("您的货代，我们的时间表。", "展品由您的货运代理运输；我们协调卸货时段和时间，确保展品和展台按正确顺序到场。"),
     ("下一届的仓储。", "如果您每年参展，我们可以把展台存放在意大利的仓库，下一届直接使用。")],
   steps_ey='服务流程', steps=[("需求沟通", "展会、展馆、面积和展台类型，参展目标和预算。如果您已有设计，我们从您的设计开始。"),
     ("设计与报价", "三维效果图和逐项报价。经您确认后才开工。"),
     ("主办方审批", "按照展会技术规定提交图纸、电气系统、接驳申请和证件。"),
     ("制作与搭建", "结构、画面和家具出发前全部检查；在布展期内现场搭建。"),
     ("展期与拆除", "展期内现场支持，展会结束后拆除；如果展台归您所有，我们负责仓储到下一次。")],
   faq_ey='常见问题', faq_t='客户经常问的 <span class="grad">问题。</span>',
   gen_qa=[("{n}的展台需要多少钱？", "取决于面积、结构类型、装修、电气和服务内容。我们不公布统一价格，会根据您的项目免费提供逐项报价。"),
     ("可以用中文沟通吗？", "可以。请用中文或英文写信给我们：我们借助翻译工具用中文回复，重要的技术细节会同时用英文确认，避免误解。"),
     ("展台是租赁还是购买？", "按您的需要：标准展台、模块化、张拉布或特装展台，可租可买。如果展台归您所有，我们会仓储到下一届。")],
   k_t='准备参加{n}？', k_p='请告诉我们展会名称、日期和展位面积，我们会回复您所需的内容和费用，临近开幕也可以评估。',
   mail='发送邮件', wa='WhatsApp', related='相关页面', it_ver='意大利语版本',
   wa_txt='您好，我们将参加{n}，需要搭建展台。公司：… 展位面积（平方米）：…',
   subj='展台询价：{n}'),
}


REQ_JS = '<script src="/assets/js/fiere-richiesta.js?v=20261014" defer></script>'
FT = {
 'en': dict(t='Request your stand', p='Fill in the fields: WhatsApp opens with your request ready. No WhatsApp? Use the email link.',
   pts=['Free itemised quote', 'Also at short notice', 'One contact person until dismantling'], fiera='Fair and city', mq='Square metres (approx.)', sp='Type of space',
   sps=['Inline (1 open side)', 'Corner (2 open sides)', 'Peninsula (3 open sides)', 'Island (4 open sides)', 'Not sure yet'],
   nome='Full name', az='Company', tel='Phone (with country code)', em='Email (optional)', note='What you need (optional)', btn='Send the request on WhatsApp',
   alt='Prefer email or cannot use WhatsApp?', mail='Write to info@danova-tech.com', priv='By sending you agree to be contacted; we never share your data.'),
 'zh': dict(t='提交展台询价', p='填写以下信息后会打开WhatsApp，询价内容已自动填好。无法使用WhatsApp？请点击邮件链接。',
   pts=['免费逐项报价', '临近开幕也可评估', '一位联系人负责到撤展'], fiera='展会和城市', mq='面积（平方米，可估算）', sp='展位类型',
   sps=['单开口（1面开放）', '双开口/角位（2面开放）', '三面开放', '岛型（4面开放）', '还不确定'],
   nome='姓名', az='公司', tel='电话（含国家代码）', em='邮箱（选填）', note='您的需求（选填）', btn='通过WhatsApp发送询价',
   alt='更习惯用邮件，或无法使用WhatsApp？', mail='发邮件到 info@danova-tech.com', priv='提交即表示同意我们与您联系；我们不会向任何人分享您的信息。'),
}
def richiesta_l(L, fiera='', id='richiesta'):
    t = FT[L]
    opts = ''.join(f'<option>{o}</option>' for o in t['sps'])
    pts = ''.join(f'<li>{x}</li>' for x in t['pts'])
    return f'''<section id="{id}" class="fr-req-sec">
  <div class="wrap">
    <div class="fr-req-box" data-rv="up">
      <div class="fr-req-txt">
        <h2 class="title">{t['t']}</h2>
        <p>{t['p']}</p>
        <ul class="fr-req-pt">{pts}</ul>
      </div>
      <form class="fr-req" novalidate>
        <div class="fld"><input type="text" name="fiera" id="{id}-fiera" placeholder=" " required value="{E(fiera)}" autocomplete="off"><label for="{id}-fiera">{t['fiera']}</label></div>
        <div class="fr-req-2">
          <div class="fld"><input type="text" name="mq" id="{id}-mq" placeholder=" " inputmode="numeric"><label for="{id}-mq">{t['mq']}</label></div>
          <div class="fld"><select name="spazio" id="{id}-spazio"><option value="" selected hidden></option>{opts}</select><label for="{id}-spazio">{t['sp']}</label></div>
        </div>
        <div class="fr-req-2">
          <div class="fld"><input type="text" name="nome" id="{id}-nome" placeholder=" " required autocomplete="name"><label for="{id}-nome">{t['nome']}</label></div>
          <div class="fld"><input type="text" name="azienda" id="{id}-azienda" placeholder=" " required autocomplete="organization"><label for="{id}-azienda">{t['az']}</label></div>
        </div>
        <div class="fr-req-2">
          <div class="fld"><input type="tel" name="tel" id="{id}-tel" placeholder=" " required inputmode="tel" autocomplete="tel"><label for="{id}-tel">{t['tel']}</label></div>
          <div class="fld"><input type="email" name="email" id="{id}-email" placeholder=" " autocomplete="email"><label for="{id}-email">{t['em']}</label></div>
        </div>
        <div class="fld"><textarea name="note" id="{id}-note" placeholder=" "></textarea><label for="{id}-note">{t['note']}</label></div>
        <p class="fr-req-err" role="alert"></p>
        <button type="submit" class="btn btn-p" data-mag><span class="sheen"></span><span class="lbl">{t['btn']}</span>
          {ARR}</button>
        <p class="form-note">{t['alt']} <a class="fr-req-mail" href="mailto:info@danova-tech.com">{t['mail']}</a>. {t['priv']}</p>
      </form>
    </div>
  </div>
</section>
'''

def contact(L, n):
    t = T[L]
    wa = 'https://wa.me/393884706887?text=' + quote(t['wa_txt'].format(n=n))
    return f'''<section class="pg-cta" id="contatti-fiera">
  <div class="wrap">
    <div class="box" data-rv="up">
      <h2 class="title">{t['k_t'].format(n=n)}</h2>
      <p>{t['k_p']}</p>
      <div class="hero-cta fr-ct">
        <a href="mailto:info@danova-tech.com?subject={quote(t['subj'].format(n=n))}" class="btn btn-p" data-mag><span class="sheen"></span><span class="lbl">{t['mail']} · <bdi dir="ltr">info@danova-tech.com</bdi></span>
          {ARR}</a>
        <a href="{wa}" class="btn btn-g" data-mag rel="noopener"><span class="lbl">{t['wa']} <bdi dir="ltr">+39 388 470 6887</bdi></span></a>
      </div>
    </div>
  </div>
</section>
'''

MESI_EN = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

def event(fid, L):
    i, n, v, st, s, e, c, site, nota = DC.FIERE[fid]
    if not c: return None
    vn, city, cc, lat, lon, addr = DC.V[v]
    n = n.split(' (')[0]
    return {"@type": "BusinessEvent", "name": n, "startDate": s, "endDate": e, "url": site,
      "eventStatus": "https://schema.org/EventScheduled", "eventAttendanceMode": "https://schema.org/OfflineEventAttendanceMode",
      "location": {"@type": "Place", "name": vn, "address": {"@type": "PostalAddress", "streetAddress": addr, "addressLocality": VEN[v][1], "addressCountry": cc},
        "geo": {"@type": "GeoCoordinates", "latitude": lat, "longitude": lon}},
      "organizer": {"@type": "Organization", "name": n, "url": site},
      "description": (f"{n}将于{int(s[:4])}年{int(s[5:7])}月{int(s[8:10])}日至{int(e[5:7])}月{int(e[8:10])}日在意大利{VEN[v][3]}的{vn}举办，是该行业的重要国际专业展会。" if L == 'zh'
        else f"{n}: international trade fair held at {vn}, {VEN[v][1]} (Italy), {int(s[8:10])} {MESI_EN[int(s[5:7])-1]} – {int(e[8:10])} {MESI_EN[int(e[5:7])-1]} {s[:4]}.")}

def svc(L, url, name, desc, offers, area):
    node = service_node(SITE + url, name, name, desc, [{"@type": "City", "name": area}, {"@type": "Country", "name": "Italy"}], offers, L)
    node["availableLanguage"] = ["English", "Chinese", "Italian"]
    return node

def related(L, items, path):
    seen = set(); out = []
    for t, u in items:
        if u == path or u in seen: continue
        seen.add(u); out.append((t, u))
    return altri(T[L]['related'], out)

def fair_label(L, k):
    f = FAIR_BY[k][L]
    return (f"{f.get('short', f['name'])} stand builder" if L == 'en' else f"{f.get('short', f['name'])}展台搭建")

# ---------------------------------------------------------------- fiere
def build_fair(f, L):
    t = T[L]; d = f[L]; P = FAIR_URL[L][f['k']]; it = f"/stand-{f['k']}/"
    vn_en, city_en, vn_zh, city_zh = VEN[f['venue']]
    year = min(DC.FIERE[x][4][:4] for x in f['cal'])
    n = d['name']; sn = d.get('short', n)
    dates = ''.join(f'<span>{DC.FIERE[x][1].replace("(febbraio)","(February)" if L=="en" else "（2月）").replace("(settembre)","(September)" if L=="en" else "（9月）").replace("(giugno)","(June)" if L=="en" else "（6月）")}: {when(x, L)}</span>' for x in f['cal'])
    if L == 'en':
        extra = f'\n    <div class="fr-dates" data-rv="up">{dates}<span>{vn_en}, {city_en}</span></div>'
        h1 = f'{sn} stand builder: <span class="grad">turnkey stands</span> at {vn_en}.'
        eyebrow = f'Exhibition stands · {sn} {year}'
    else:
        extra = f'\n    <div class="fr-dates" data-rv="up">{dates}<span>{city_zh} · {vn_zh}</span></div>'
        h1 = f'{n}展台设计搭建：<span class="grad">一站式交钥匙服务</span>。'
        eyebrow = f'展台搭建 · {sn} {year}'
    m = hero(eyebrow, h1, d['lead'], t['req'], '#contatti-fiera', t['how'], '#metodo', extra=extra)
    site = DC.FIERE[f['cal'][0]][7]
    nxt = '<br>'.join(when(x, L) for x in f['cal'])
    if L == 'en':
        rows = [("Fair", d['full']), ("Where", f"{vn_en}, {city_en}, Italy"), ("Next edition", nxt), ("Sector", d['sector'].capitalize()),
                ("Official website", f'<a href="{site}" rel="noopener" target="_blank">{site.split("//")[1].rstrip("/")}</a>'),
                ("Our experience", f"We have already built stands at {sn}." if f['exp'] else f"We build stands for {sn} and for trade fairs across Italy and Europe.")]
        m += scheda("scheda", f"{sn} at a glance", rows, "Dates are those published by the organiser (checked in October 2026). Always confirm them on the official website before booking travel and transport.")
        m += testo("fiera", f"What {sn} is and <span class=\"grad\">what it asks of a stand</span>", None, d['intro'])
        m += testo("esigenze", f"What a stand for {sn} needs", None, [], d['needs'])
    else:
        rows = [("展会", n), ("地点", f"意大利{city_zh} · {vn_zh}"), ("下一届", nxt), ("行业", d['sector']),
                ("官方网站", f'<a href="{site}" rel="noopener" target="_blank">{site.split("//")[1].rstrip("/")}</a>'),
                ("我们的经验", f"我们已经在{sn}搭建过展台。" if f['exp'] else f"我们为{sn}以及意大利和欧洲各地的展会搭建展台。")]
        m += scheda("scheda", f"{sn}概况", rows, "日期以主办方公布为准（2026年10月核对）。预订行程和运输前，请务必在官方网站上再次确认。")
        m += testo("fiera", f"{sn}是什么展会，<span class=\"grad\">对展台有什么要求</span>", None, d['intro'])
        m += testo("esigenze", f"{sn}展台需要什么", None, [], d['needs'])
    m += cards("cosa", t['cards_t'], t['cards_l'], t['cards'])
    m += testo("estero", t['foreign_t'], t['foreign_l'], [], t['foreign'])
    p_t = (f'From the brief to a stand <span class="grad">ready at {vn_en}.</span>' if L == 'en' else f'从需求沟通 <span class="grad">到{vn_zh}的完工展台。</span>')
    m += passi("metodo", t['steps_ey'], p_t, None, t['steps'])
    qa = d['qa'] + [(a.format(n=sn), b) for a, b in t['gen_qa']]
    m += richiesta_l(L, (f"{sn} {year} – {city_en}" if L == 'en' else f"{n}（{city_zh}）{year}"))
    m += faq(t['faq_ey'], t['faq_t'], qa)
    m += contact(L, f"{sn} {year}")
    rel = [(T[L]['pillar'], PILL[L])]
    if f['city'] in CITY_URL[L]:
        c = next(c for c in DI.CITIES if c['s'] == f['city'])
        rel.append(((f"Exhibition stands in {c['en']['name']}" if L == 'en' else f"{c['zh']['name']}展台搭建"), CITY_URL[L][f['city']]))
    rel += [(fair_label(L, k), FAIR_URL[L][k]) for k in FAIR_URL[L] if k != f['k']]
    rel += [(("Guide: exhibiting in Italy" if L == 'en' else "意大利参展指南"), GUIDE[L]), (t['it_ver'], it)]
    m += related(L, rel, P)
    if L == 'en':
        title = f"{sn} Stand Builder {year} in {city_en} | Danova Tech"
        if len(title) > 60: title = f"{sn} Stand Builder {year} in {city_en}"
        desc = f"{sn} {year} stand builder at {vn_en}: 3D design, materials, graphics, electrics and on-site installation crews. Free itemised quote."
        if len(desc) > 158: desc = desc.replace("on-site installation crews", "installation")
        ogt = f"{sn} stand builder — Danova Tech"; ogd = f"Turnkey stands for {sn} at {vn_en}: design, materials, graphics, electrics and installation."
        crumbs = [("Home", "/en/"), (t['pillar'], PILL['en']), (f"{sn} stand builder", None)]
        name = f"Stand design and build for {sn}"
        sdesc = f"Design, materials and components, graphics, electrics, installation and dismantling of exhibition stands for {d['full']} at {vn_en}, {city_en}."
        offers = [f"Stand design for {sn}", "Modular and custom-built stands", "Installation and dismantling on site", "Stand rental and storage"]
    else:
        title = f"{year}年{n}展台设计搭建 | Danova Tech"
        if W(title) > 64: title = f"{year}年{n}展台设计搭建"
        desc = f"{n}（{city_zh}{vn_zh}）展台设计与搭建：三维设计、材料与配件、平面印刷、电气照明和现场搭建团队。可用中文或英文沟通，免费逐项报价，紧急需求也可评估。"
        ogt = f"{n}展台搭建 — Danova Tech"; ogd = f"{vn_zh}{sn}一站式展台服务：设计、材料、平面、电气和现场搭建。"
        crumbs = [("首页", "/en/"), (t['pillar'], PILL['zh']), (f"{sn}展台搭建", None)]
        name = f"{sn}展台设计与搭建"
        sdesc = f"为{n}（意大利{city_zh}{vn_zh}）提供展台设计、材料与配件、平面印刷、电气、现场搭建与拆除服务。"
        offers = [f"{sn}展台设计", "模块化展台和特装展台", "现场搭建与拆除", "展台租赁与仓储"]
    evs = [e for e in (event(x, L) for x in f['cal']) if e]
    node = svc(L, P, name, sdesc, offers, city_en)
    out = build(L, P, title, desc, ogt, ogd, crumbs, m, qa, [node], IM.ALTS[P], wp_extra=({"mentions": evs} if evs else None), scripts=REQ_JS)
    print(f"{W(title):3d} {len(desc):3d} {P}")

# ---------------------------------------------------------------- citta'
def build_city(c, L):
    t = T[L]; d = c[L]; P = CITY_URL[L][c['s']]; it = f"/allestimenti-fieristici-{c['s']}/"
    vn_en, city_en, vn_zh, city_zh = VEN[c['venue']]
    if L == 'en':
        m = hero(f"Exhibition stands · {d['name']}", f'Exhibition stand builder in {d["name"]}: <span class="grad">turnkey stands</span>.', d['lead'], t['req'], '#contatti-fiera', t['how'], '#metodo')
        m += testo("citta", f"Stands in {d['name']}, <span class=\"grad\">from design to installation</span>", f"Where we work: {d['venue_txt']}.", d['intro'])
        m += chips("fiere", f"Trade fairs in {d['name']} with a dedicated page", None, [(fair_label(L, k), FAIR_URL[L][k]) for k in c['fairs']])
        lab_next = (f"Upcoming trade fairs in {d['name']}", "Dates published by the organisers, checked in October 2026.")
        know_t = f"What to know about building a stand in {d['name']}"
    else:
        m = hero(f"展台搭建 · {d['name']}", f'{d["name"]}展台设计搭建：<span class="grad">一站式交钥匙服务</span>。', d['lead'], t['req'], '#contatti-fiera', t['how'], '#metodo')
        m += testo("citta", f"{d['name']}展台，<span class=\"grad\">从设计到搭建</span>", f"服务场馆：{d['venue_txt']}。", d['intro'])
        m += chips("fiere", f"{d['name']}展会专题页面", None, [(fair_label(L, k), FAIR_URL[L][k]) for k in c['fairs']])
        lab_next = (f"{d['name']}近期展会", "日期以主办方公布为准，2026年10月核对。")
        know_t = f"在{d['name']}搭建展台需要了解的事"
    evs = sorted([x for x in DC.F if x[2] == c['venue']], key=lambda x: x[4])
    if evs:
        def lab(x):
            k = next((f['k'] for f in DI.FAIRS if x[0] in f['cal']), None)
            nm = x[1].replace('(febbraio)', '(February)' if L == 'en' else '（2月）').replace('(settembre)', '(September)' if L == 'en' else '（9月）').replace('(giugno)', '(June)' if L == 'en' else '（6月）')
            link = f' · <a href="{FAIR_URL[L][k]}">{fair_label(L, k)}</a>' if k else ''
            return (nm, when(x[0], L) + link)
        m += testo("calendario", lab_next[0], lab_next[1], [], [lab(x) for x in evs])
    m += testo("sapere", know_t, None, [], d['know'])
    m += cards("cosa", t['cards_t'], t['cards_l'], t['cards'])
    m += testo("estero", t['foreign_t'], t['foreign_l'], [], t['foreign'])
    p_t = (f'From the brief to a stand <span class="grad">ready in {d["name"]}.</span>' if L == 'en' else f'从需求沟通 <span class="grad">到{d["name"]}的完工展台。</span>')
    m += passi("metodo", t['steps_ey'], p_t, None, t['steps'])
    qa = [(a.format(n=d['name']), b) for a, b in t['gen_qa']]
    if L == 'en':
        qa = [(f"Do you build stands at {d['venue_txt']}?", f"Yes. We design, supply and install stands at {d['venue_txt']}, and handle approvals and certificates with the organiser."),
              ("Can you build at short notice?", "We assess urgent requests straight away: with modular structures and fabric graphics we can often deliver a few weeks before opening.")] + qa
    else:
        qa = [(f"你们在{d['venue_txt']}搭建展台吗？", f"是的。我们在{d['venue_txt']}提供展台设计、材料和现场搭建，并负责与主办方之间的审批和证书。"),
              ("临近开幕还能搭建吗？", "我们会立即评估紧急需求：采用模块化结构和印花布，通常在开幕前几周也能完成。")] + qa
    m += richiesta_l(L, (f"Trade fair in {d['name']}" if L == 'en' else f"{d['name']}的展会"))
    m += faq(t['faq_ey'], t['faq_t'], qa)
    m += contact(L, d['name'] if L == 'en' else f"{d['name']}的展会")
    rel = [(T[L]['pillar'], PILL[L])] + [(fair_label(L, k), FAIR_URL[L][k]) for k in c['fairs']]
    rel += [((f"Exhibition stands in {x['en']['name']}" if L == 'en' else f"{x['zh']['name']}展台搭建"), CITY_URL[L][x['s']]) for x in DI.CITIES if x['s'] != c['s']]
    rel += [(("Guide: exhibiting in Italy" if L == 'en' else "意大利参展指南"), GUIDE[L]), (t['it_ver'], it)]
    m += related(L, rel, P)
    if L == 'en':
        title = f"Exhibition Stand Builder in {d['name']} | Danova Tech"
        desc = f"Exhibition stand design and build in {d['name']} ({vn_en}): 3D design, materials, graphics, electrics and installation crews on site. Free itemised quote."
        if len(desc) > 158: desc = f"Exhibition stand design and build in {d['name']}: 3D design, materials, graphics, electrics and installation crews on site. Free itemised quote."
        ogt = f"Exhibition stand builder in {d['name']} — Danova Tech"; ogd = f"Turnkey trade fair stands at {d['venue_txt']}: design, materials and installation."
        crumbs = [("Home", "/en/"), (t['pillar'], PILL['en']), (d['name'], None)]
        name = f"Exhibition stand design and build in {d['name']}"
        sdesc = f"Design, materials and components, graphics, electrics, installation and dismantling of exhibition stands at {d['venue_txt']}."
        offers = ["Custom-built stands", "Modular stands", "Stand installation and dismantling", "Stand rental"]
    else:
        title = f"{d['name']}展台设计搭建公司 | 意大利展会 | Danova Tech"
        if W(title) > 64: title = f"{d['name']}展台设计搭建公司 | Danova Tech"
        desc = f"{d['name']}展台设计与搭建（{vn_zh}）：三维设计、材料与配件、平面印刷、电气照明和现场搭建团队。可用中文或英文沟通，免费逐项报价。"
        ogt = f"{d['name']}展台搭建 — Danova Tech"; ogd = f"{d['venue_txt']}一站式展台服务：设计、材料和现场搭建。"
        crumbs = [("首页", "/en/"), (t['pillar'], PILL['zh']), (d['name'], None)]
        name = f"{d['name']}展台设计与搭建"
        sdesc = f"在{d['venue_txt']}提供展台设计、材料与配件、平面印刷、电气、现场搭建与拆除服务。"
        offers = ["特装展台", "模块化展台", "展台搭建与拆除", "展台租赁"]
    node = svc(L, P, name, sdesc, offers, city_en)
    build(L, P, title, desc, ogt, ogd, crumbs, m, qa, [node], IM.ALTS[P], scripts=REQ_JS)
    print(f"{W(title):3d} {len(desc):3d} {P}")

# ---------------------------------------------------------------- guida
G = {
 'en': dict(title="Exhibiting in Italy: Trade Fair Guide for Foreign Companies",
  desc="How to exhibit at a trade fair in Italy: timeline, technical regulations, electrical certificates, fire-rated materials, build-up, shipping and visas.",
  h1='Exhibiting at a trade fair in Italy: <span class="grad">a practical guide</span> for foreign exhibitors.',
  lead="What a company coming from China or from abroad needs to know before exhibiting at Milan, Bologna, Verona, Rimini or any other Italian fair: the timeline, the organiser's rules, the certificates Italian halls ask for, and the mistakes that cost money on the first build-up day.",
  sections=[
   ("timeline", "When to start: <span class=\"grad\">a realistic timeline</span>", [
     ("9–12 months before.", "Book your space with the organiser. For the big Milan and Bologna shows the best positions go to returning exhibitors, so ask early."),
     ("6–4 months before.", "Choose the stand builder, agree on the design and get the 3D render. Book hotels for your team: during big fairs they fill up fast."),
     ("3–2 months before.", "Submit the stand drawings to the organiser and order services: electrical power, water, internet, cleaning. Each has a deadline in the exhibitor manual."),
     ("6–4 weeks before.", "Graphics files final, shipping of your exhibits organised with the forwarder, visas and invitation letters ready."),
     ("Build-up days.", "Usually two to five days before opening, with strict hours and unloading slots. Dismantling starts right after closing.")]),
   ("regole", "The organiser's <span class=\"grad\">technical regulations</span>", [
     ("Exhibitor manual.", "Every Italian fair publishes a technical regulation (regolamento tecnico): maximum heights, distance from neighbouring stands, rules for two-storey stands and hanging structures. Read it before designing, not after."),
     ("Drawing approval.", "Stands above a certain height, two-storey stands and hanging rigging need drawings and sometimes a structural report signed by an engineer, approved by the organiser."),
     ("Hanging structures.", "Banners and trusses hung from the hall ceiling can only be installed by the organiser's authorised riggers, on request and at extra cost.")]),
   ("certificati", "Certificates Italian halls <span class=\"grad\">will ask for</span>", [
     ("Electrical declaration of conformity.", "The stand's electrical system must be installed by a qualified company, which signs a declaration of conformity under Italian law (Ministerial Decree 37/2008). Without it the organiser will not switch on the power."),
     ("Fire-rated materials.", "Panels, fabrics, carpets and decorations must have the fire reaction class required by the regulation, with certificates available on the stand. Materials bought abroad without Italian or EU certification may be refused."),
     ("Safety on site.", "Build-up and dismantling are construction work under Italian safety rules: crews need safety documentation, protective equipment and, where required, the organiser's passes.")]),
   ("spedizione", "Shipping exhibits and <span class=\"grad\">travelling to Italy</span>", [
     ("Use an exhibition forwarder.", "Most fairs have an official forwarder who knows the halls, the unloading slots and customs. Goods from China usually travel by sea, so plan in months, not weeks."),
     ("Temporary import.", "Exhibits that return home after the show can enter under temporary admission, for example with an ATA Carnet. Your forwarder or chamber of commerce can advise on the right procedure."),
     ("Visas and invitation letters.", "Staff from countries that need a Schengen visa should request an invitation letter from the organiser and apply early, especially before busy seasons."),
     ("Who builds the stand.", "Your exhibits are your forwarder's job; the stand structure, furniture, graphics and electrics are ours. We coordinate the two so they arrive in the right order.")]),
  ],
  qa=[("How early should a foreign company book a stand builder in Italy?", "Four to six months before the fair is comfortable for a custom stand. With modular or rental solutions we can work with much less time; write to us anyway, even close to opening."),
   ("Can an Italian stand builder work from our own design?", "Yes. We build from your designer's drawings, check them against the Italian technical regulations and propose changes only where the rules or the materials require it."),
   ("Do we need Italian certificates for the stand?", "Yes: the electrical declaration of conformity and the fire-rating certificates of the materials. We provide both as part of our service."),
   ("Can we pay and sign the contract from China?", "Yes. We sign directly with your company and send an itemised quote in euro; payment is by international bank transfer.")],
  crumb="Guide: exhibiting in Italy"),
 'zh': dict(title="意大利展会参展指南：外国参展商须知 | Danova Tech",
  desc="在意大利展会参展需要知道什么：时间规划、主办方技术规定、电气合格证明、防火材料、布展、展品运输和签证。写给中国及海外参展企业。",
  h1='意大利展会参展指南：<span class="grad">写给外国参展商的实用须知</span>。',
  lead="从中国或海外来米兰、博洛尼亚、维罗纳、里米尼或意大利其他展会参展之前，需要了解的事情：时间规划、主办方规定、意大利展馆要求的证书，以及会在布展第一天造成损失的常见错误。",
  sections=[
   ("timeline", "什么时候开始：<span class=\"grad\">一份现实的时间表</span>", [
     ("提前9至12个月。", "向主办方预订展位。米兰和博洛尼亚的大型展会，好位置优先给老展商，所以要尽早申请。"),
     ("提前4至6个月。", "选定搭建商，确定设计并获得三维效果图。为团队预订酒店：大型展会期间酒店很快订满。"),
     ("提前2至3个月。", "向主办方提交展台图纸，申请各项服务：电力、给水、网络、清洁。每一项在参展商手册中都有截止日期。"),
     ("提前4至6周。", "画面文件定稿，与货代安排好展品运输，签证和邀请函准备就绪。"),
     ("布展期。", "通常在开幕前两到五天，时间和卸货时段都有严格规定。闭幕后立即开始撤展。")]),
   ("regole", "主办方的<span class=\"grad\">技术规定</span>", [
     ("参展商手册。", "每个意大利展会都会公布技术规定（regolamento tecnico）：最大高度、与相邻展位的距离、双层展台和吊挂结构的规则。请在设计之前阅读，而不是之后。"),
     ("图纸审批。", "超过一定高度的展台、双层展台和吊挂结构，需要提交图纸，有时还需要工程师签字的结构报告，经主办方批准。"),
     ("吊挂结构。", "从展馆屋顶吊挂的横幅和桁架，只能由主办方授权的吊挂公司安装，需要申请并额外付费。")]),
   ("certificati", "意大利展馆<span class=\"grad\">会要求的证书</span>", [
     ("电气合格声明。", "展台电气系统必须由有资质的公司安装，并按照意大利法律（2008年第37号部长令）签署合格声明（dichiarazione di conformità）。没有这份文件，主办方不会给展台通电。"),
     ("防火材料。", "板材、布料、地毯和装饰物必须达到技术规定要求的防火等级，并在展台上备有证书。在国外采购、没有意大利或欧盟认证的材料可能会被拒绝使用。"),
     ("现场安全。", "布展和撤展属于施工作业，适用意大利安全法规：施工人员需要安全文件、防护装备，并按要求办理主办方证件。")]),
   ("spedizione", "展品运输和<span class=\"grad\">赴意大利行程</span>", [
     ("选择展会物流货代。", "大多数展会都有官方指定货代，熟悉展馆、卸货时段和清关。从中国发货通常走海运，所以要按月而不是按周规划。"),
     ("暂时进口。", "展会结束后运回的展品，可以按暂时进口方式入境，例如使用ATA单证册。具体手续请咨询您的货代或贸促会。"),
     ("签证和邀请函。", "需要申根签证的工作人员，应向主办方申请邀请函并尽早递交签证申请，尤其是在旺季之前。"),
     ("展台由谁负责。", "展品由您的货代负责；展台结构、家具、画面和电气由我们负责。我们协调双方，确保按正确顺序到场。")]),
  ],
  qa=[("外国企业应该提前多久预订意大利搭建商？", "特装展台提前4至6个月比较从容。采用模块化或租赁方案，时间可以短得多；即使临近开幕，也欢迎联系我们。"),
   ("意大利搭建商可以按我们自己的设计施工吗？", "可以。我们按照您设计师的图纸施工，按意大利技术规定进行核查，只在规定或材料要求时提出修改。"),
   ("展台需要意大利的证书吗？", "需要：电气合格声明和材料防火等级证书。这两项都包含在我们的服务中。"),
   ("可以在中国签合同和付款吗？", "可以。我们直接与贵公司签约，提供欧元逐项报价，通过国际银行电汇付款。")],
  crumb="意大利参展指南"),
}

def build_guide(L):
    g = G[L]; P = GUIDE[L]; t = T[L]
    m = hero(("Guide · Exhibiting in Italy" if L == 'en' else "指南 · 在意大利参展"), g['h1'], g['lead'], t['req'], '#contatti-fiera',
             ("Start with the timeline" if L == 'en' else "从时间表开始"), '#timeline')
    for sid, title, lista in g['sections']:
        m += testo(sid, title, None, [], lista)
    m += chips("fiere", ("Stand pages for the main Italian fairs" if L == 'en' else "意大利主要展会展台专题"), None, [(fair_label(L, k), FAIR_URL[L][k]) for k in FAIR_URL[L]])
    m += passi("metodo", t['steps_ey'], ('How we work <span class="grad">with foreign exhibitors.</span>' if L == 'en' else '我们如何 <span class="grad">与外国参展商合作。</span>'), None, t['steps'])
    m += richiesta_l(L)
    m += faq(t['faq_ey'], t['faq_t'], g['qa'])
    m += contact(L, ("a fair in Italy" if L == 'en' else "意大利展会"))
    rel = [(t['pillar'], PILL[L])] + [((f"Exhibition stands in {c['en']['name']}" if L == 'en' else f"{c['zh']['name']}展台搭建"), CITY_URL[L][c['s']]) for c in DI.CITIES]
    rel += [(t['it_ver'], '/guide/come-preparare-una-fiera/')]
    m += related(L, rel, P)
    crumbs = [(t['home'], "/en/"), (t['pillar'], PILL[L]), (g['crumb'], None)]
    title = g['title'] if L == 'zh' else g['title']
    node = article_node(SITE + P, IM_STRIP(g['h1']), g['desc'], 'zh-Hans' if L == 'zh' else 'en')
    build(L, P, title, g['desc'], g['title'].split(' | ')[0], g['desc'], crumbs, m, g['qa'], [node], IM.ALTS[P], scripts=REQ_JS)
    print(f"{W(title):3d} {len(g['desc']):3d} {P}")
IM_STRIP = strip_tags

# ---------------------------------------------------------------- pagine IT: hreflang e selettore lingua
def patch_it():
    n = 0
    for p, g in IM.ALTS.items():
        if p != g['it']: continue
        f = os.path.join(R, p.strip('/'), 'index.html')
        if not os.path.exists(f): print('manca', p); continue
        s = open(f, encoding='utf-8').read(); s2 = IM.patch(s, p)
        if s2 != s: open(f, 'w', encoding='utf-8').write(s2); n += 1
    print('pagine IT aggiornate:', n)

if __name__ == '__main__':
    for L in ('en', 'zh'):
        for f in DI.FAIRS: build_fair(f, L)
        for c in DI.CITIES: build_city(c, L)
        build_guide(L)
    patch_it()
