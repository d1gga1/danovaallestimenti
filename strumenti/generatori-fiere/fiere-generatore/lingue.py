# -*- coding: utf-8 -*-
import sys,os; sys.path.insert(0,os.path.dirname(__file__))
from lib import *
from urllib.parse import quote
import lingue_data1,lingue_data2,lingue_zh,lingue_tr,lingue_ar
D={**lingue_data1.D,**lingue_data2.D,**lingue_zh.D,**lingue_tr.D,**lingue_ar.D}
FIERE=["Vinitaly","Marmomac","Salone del Mobile","EICMA","Host","Cosmoprof","Cersaie","EIMA","Sicam","Samuexpo","Sigep","VicenzaOro","Ecomondo","MICAM","MIDO","Macfrut","Lineapelle"]
ALTS={'it':'/servizi/allestimenti-fieristici/',**{l:D[l]['path'] for l in D}}
SUBJ={'en':'Exhibition stand request','de':'Anfrage Messestand','fr':'Demande de stand','es':'Solicitud de stand','zh':'展台询价','tr':'Fuar standı talebi','ar':'طلب جناح معرض'}
ONLY=sys.argv[1:]  # 14/10/2026: es. python3 lingue.py en zh
import dati_intl as DI
INTL_T={'en':("Stand pages for Italian trade fairs","Dedicated pages for the fairs and exhibition cities where most foreign exhibitors, including many Chinese companies, come to Italy.",' stand builder',"Exhibition stands in ","Guide: exhibiting in Italy",'/en/exhibiting-at-trade-fairs-in-italy/'),
 'zh':("意大利主要展会展台专题","外国参展商（包括大量中国企业）最常参加的意大利展会和展会城市专题页面。",'展台搭建',"",'意大利参展指南','/zh/italy-trade-fair-guide/')}
for L,d in D.items():
    if ONLY and L not in ONLY: continue
    ct='#contatti-fiera'
    m=hero(d['eyebrow'],d['h1'],d['lead'],d['cta'],ct,d['cta2'],'#metodo')
    m+=cards('cosa',d['c_t'],d['c_l'],d['cards'])
    m+=testo('perche',d['t_t'],None,d['paras'],d['lista'])
    m+=chips('fiere',d['f_t'],d['f_l'],[(p,None) for p in d['places']])
    if L in INTL_T:
        t1,t2,suf,pre,gt,gu=INTL_T[L]
        fl=[(f[L].get('short',f[L]['name'])+suf,f"/{L}/{f[L]['slug']}/") for f in DI.FAIRS]
        cl=[(pre+c[L]['name']+('' if L=='en' else '展台搭建'),f"/{L}/{c[L]['slug']}/") for c in DI.CITIES]
        m+=chips('fiere-italia',t1,t2,cl+fl+[(gt,gu)])
    m+=chips('esperienza',d['e_t'],None,[(f,None) for f in FIERE])
    m+=passi('metodo',d['p_ey'],d['p_t'],None,d['steps'])
    if L in ('en','zh'):
        from build_intl import richiesta_l  # 14/10/2026 modulo richiesta nelle pagine EN/ZH
        m+=richiesta_l(L)
    m+=faq(d['faq_ey'],d['faq_t'],d['qa'])
    m+=f'''<section class="pg-cta" id="contatti-fiera">
  <div class="wrap">
    <div class="box" data-rv="up">
      <h2 class="title">{d['k_t']}</h2>
      <p>{d['k_p']}</p>
      <div class="hero-cta fr-ct">
        <a href="mailto:info@danova-tech.com?subject={quote(SUBJ[L])}" class="btn btn-p" data-mag><span class="sheen"></span><span class="lbl">{d['mail']} · <bdi dir="ltr">info@danova-tech.com</bdi></span>
          {ARR}</a>
        <a href="https://wa.me/393884706887" class="btn btn-g" data-mag rel="noopener"><span class="lbl">{d['wa']} <bdi dir="ltr">+39 388 470 6887</bdi></span></a>
      </div>
    </div>
  </div>
</section>
'''
    node=service_node(SITE+d['path'],d['svc_name'],d['svc_name'],d['svc_desc'],
      [{"@type":"Country","name":"Italy"},{"@type":"Place","name":"Europe"}],d['offers'],L)
    print(build(L,d['path'],d['title'],d['desc'],d['ogt'],d['ogd'],d['crumbs'],m,d['qa'],[node],ALTS,scripts=('<script src="/assets/js/fiere-richiesta.js?v=20261014" defer></script>' if L in ('en','zh') else '')))
