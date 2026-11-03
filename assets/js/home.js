(function(){
"use strict";
  const ALT_PRJ={"it": "Progetto Danova Tech", "en": "Danova Tech project", "de": "Danova Tech Projekt", "fr": "Projet Danova Tech", "es": "Proyecto Danova Tech"};
const RM = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
const $  = (s,c)=> (c||document).querySelector(s);
const $$ = (s,c)=> Array.from((c||document).querySelectorAll(s));
const lerp=(a,b,t)=>a+(b-a)*t;
const clamp=(v,a,b)=>Math.min(b,Math.max(a,v));
const dig=(o,p)=>p.split('.').reduce((a,k)=>a==null?a:a[k],o);

/* ---- CONFIG RAPIDA ---------------------------------------------------- */
const DEST='info@danova-tech.com';
const WA='393884706887';                       // <<< numero WhatsApp destinatario del form           // <<< email destinataria del form
const NUMS_HERO=[120,98,14,24];            // numeri hero
const NUMS_HERO_SUF=['+','%','',''];       // suffissi hero (il 3° prende " gg"/" days" dalla lingua)
const NUMS_BIG=[120,9,3,98];               // numeri sezione statistiche
/* ----------------------------------------------------------------------- */

let LANG='it';
const T=()=>window.I18N[LANG];

document.documentElement.classList.remove('no-js');

/* URL delle tre versioni linguistiche (aggiornate dal cambio lingua) */
const LANG_URL={it:'/',en:'/en/',de:'/de/',fr:'/fr/',es:'/es/'};
const LANG_ABS={it:'https://danova-tech.com/',en:'https://danova-tech.com/en/',de:'https://danova-tech.com/de/',fr:'https://danova-tech.com/fr/',es:'https://danova-tech.com/es/'};
function syncLangUrl(){
  try{
    history.replaceState(null,'',LANG_URL[LANG]);
    const c=document.querySelector('link[rel="canonical"]'); if(c) c.href=LANG_ABS[LANG];
    const o=document.querySelector('meta[property="og:url"]'); if(o) o.content=LANG_ABS[LANG];
  }catch(e){}
}

/* =========================================================
   1. PRELOADER
   ========================================================= */
const pre=$('#pre');
document.body.style.overflow='hidden';

(function buildPreloader(){
  const rig=$('#preRig'), front=$('#preMark'), shards=$('#preShards');

  /* lunghezze dei tracciati per il disegno progressivo */
  const LEN={};
  front.querySelectorAll('path').forEach(p=>{
    const cl=p.getAttribute('class'), L=Math.ceil(p.getTotalLength())+2;
    LEN[cl]=L; p.style.strokeDasharray=L; p.style.strokeDashoffset=L;
  });

  /* estrusione 3D: cloni del marchio spinti in profondita' */
  const N = RM ? 1 : (innerWidth<720 ? 8 : 17);
  const mix=(a,b,t)=>`rgb(${a.map((v,i)=>Math.round(v+(b[i]-v)*t)).join(',')})`;
  const BACK=[8,18,44], WHITE=[255,255,255], BLUE=[30,107,255], BBACK=[5,14,46];

  for(let i=N-1;i>=1;i--){
    const t=Math.pow(i/(N-1),.72);
    const lay=document.createElement('div');
    lay.className='lay deep';
    lay.style.setProperty('--z',(-i*1.15)+'px');
    lay.style.setProperty('--d',(1.42+(N-i)*.014)+'s');
    const svg=front.cloneNode(true);
    svg.removeAttribute('id');
    svg.querySelectorAll('path').forEach(p=>{
      const cl=p.getAttribute('class');
      p.style.strokeDasharray=LEN[cl]; p.style.strokeDashoffset=LEN[cl];
      p.style.stroke = cl==='p-slash' ? mix(BLUE,BBACK,t) : mix(WHITE,BACK,t);
    });
    lay.appendChild(svg);
    rig.insertBefore(lay,rig.firstChild);
  }

  /* schegge che convergono sul marchio */
  if(!RM){
    let h='';
    for(let i=0;i<14;i++){
      const a=Math.random()*Math.PI*2, d=180+Math.random()*260;
      h+=`<i style="--x:${(Math.cos(a)*d).toFixed(0)}px;--y:${(Math.sin(a)*d*.7).toFixed(0)}px;`
       + `--z:${(-180-Math.random()*420).toFixed(0)}px;--r:${(a*57.3).toFixed(0)}deg;`
       + `--w:${(40+Math.random()*90).toFixed(0)}px;--c:${Math.random()>.45?'#4d8bff':'rgba(255,255,255,.9)'};`
       + `--dur:${(.9+Math.random()*.7).toFixed(2)}s;--del:${(Math.random()*1.1).toFixed(2)}s"></i>`;
    }
    shards.innerHTML=h;
  }

  /* wordmark lettera per lettera */
  $('#preWord').innerHTML='DANOVA TECH'.split('')
    .map((c,i)=>`<i style="--i:${i}">${c===' '?'&nbsp;':c}</i>`).join('');
})();

let PRE_LOADED=false;
addEventListener('load',()=>{PRE_LOADED=true;});
requestAnimationFrame(()=>pre.classList.add('go'));

const PRE_T0=performance.now();
/* Durata dell'intro. Tenerla bassa e' decisivo per il punteggio Core Web Vitals
   di Google (LCP): la pagina non e' "vista" finche' il velo non sparisce.
   PRE_MIN = quanto dura l'animazione, PRE_MAX = attesa massima se le immagini
   sono lente. Alzarli peggiora il punteggio, abbassarli lo migliora. */
const PRE_MIN = RM ? 350 : 1100, PRE_MAX = 1900;
setTimeout(function waitPre(){
  if(!PRE_LOADED && performance.now()-PRE_T0 < PRE_MAX){ setTimeout(waitPre,80); return; }
  finishPre();
}, PRE_MIN);

function finishPre(){
  if(pre.classList.contains('out')) return;
  pre.classList.add('out');
  setTimeout(()=>{pre.classList.add('done');document.body.style.overflow='';startHero();},380);
}

/* =========================================================
   2. CURSORE + MAGNETICO
   ========================================================= */
const cur=$('.cur'), ring=$('.cur-r');
let mx=innerWidth/2,my=innerHeight/2,rx=mx,ry=my;
const DESKTOP = !('ontouchstart' in window) && innerWidth>1024;
if(DESKTOP){
  addEventListener('mousemove',e=>{mx=e.clientX;my=e.clientY;cur.style.transform=`translate(${mx}px,${my}px) translate(-50%,-50%)`;});
  (function loop(){rx=lerp(rx,mx,.16);ry=lerp(ry,my,.16);
    ring.style.transform=`translate(${rx}px,${ry}px) translate(-50%,-50%)`;requestAnimationFrame(loop);})();
  addEventListener('mouseleave',()=>ring.classList.add('hide'));
  addEventListener('mouseenter',()=>ring.classList.remove('hide'));
  const HOV='a,button,summary,[data-tilt],input,textarea,select,.tst-dots i';
  document.addEventListener('mouseover',e=>{ if(e.target.closest(HOV)) ring.classList.add('big');});
  document.addEventListener('mouseout',e=>{ if(e.target.closest(HOV)) ring.classList.remove('big');});
}
function bindMag(){
  if(!DESKTOP) return;
  $$('[data-mag]').forEach(el=>{
    if(el.dataset.mb) return; el.dataset.mb='1';
    el.addEventListener('mousemove',e=>{
      const r=el.getBoundingClientRect();
      const x=(e.clientX-(r.left+r.width/2))*.28, y=(e.clientY-(r.top+r.height/2))*.4;
      el.style.transform=`translate(${x}px,${y}px)`;
    });
    el.addEventListener('mouseleave',()=>{el.style.transform='';});
  });
}

/* =========================================================
   3. HERO — canvas rete di particelle
   ========================================================= */
const cv=$('#net'), ctx=cv.getContext('2d');
let W,H,parts=[],DPR=Math.min(devicePixelRatio||1,2);
function sizeCv(){
  W=cv.width=cv.offsetWidth*DPR; H=cv.height=cv.offsetHeight*DPR;
  const n=Math.round(clamp((cv.offsetWidth*cv.offsetHeight)/13000,45,130));
  parts=Array.from({length:n},()=>({x:Math.random()*W,y:Math.random()*H,
    vx:(Math.random()-.5)*.28*DPR,vy:(Math.random()-.5)*.28*DPR,r:(Math.random()*1.7+.5)*DPR}));
}
let pm={x:-9999,y:-9999};
addEventListener('mousemove',e=>{const r=cv.getBoundingClientRect();pm.x=(e.clientX-r.left)*DPR;pm.y=(e.clientY-r.top)*DPR;});
function drawNet(){
  ctx.clearRect(0,0,W,H);
  const LINK=140*DPR;
  for(let i=0;i<parts.length;i++){
    const a=parts[i];
    a.x+=a.vx;a.y+=a.vy;
    if(a.x<0||a.x>W)a.vx*=-1; if(a.y<0||a.y>H)a.vy*=-1;
    const dxm=a.x-pm.x,dym=a.y-pm.y,dm=Math.hypot(dxm,dym);
    if(dm<130*DPR&&dm>0){a.x+=dxm/dm*1.5;a.y+=dym/dm*1.5;}
    for(let j=i+1;j<parts.length;j++){
      const b=parts[j],dx=a.x-b.x,dy=a.y-b.y,d=Math.hypot(dx,dy);
      if(d<LINK){ctx.strokeStyle=`rgba(60,130,255,${(1-d/LINK)*.32})`;ctx.lineWidth=DPR*.6;
        ctx.beginPath();ctx.moveTo(a.x,a.y);ctx.lineTo(b.x,b.y);ctx.stroke();}
    }
    ctx.fillStyle=Math.hypot(a.x-pm.x,a.y-pm.y)<160*DPR?'rgba(180,215,255,.95)':'rgba(90,150,255,.6)';
    ctx.beginPath();ctx.arc(a.x,a.y,a.r,0,6.284);ctx.fill();
  }
  requestAnimationFrame(drawNet);
}
sizeCv(); if(!RM) drawNet();
addEventListener('resize',sizeCv);

/* =========================================================
   4. SPLIT TEXT HERO + PAROLA ROTANTE
   ========================================================= */
let rotTimer=null, ri=0, rotSpans=[];
function splitLine(el,txt){
  /* ogni parola sta dentro uno .wd: l'a capo puo' avvenire solo fra le parole,
     mai in mezzo a una parola (fondamentale su schermi stretti e in tedesco). */
  el.textContent='';
  const words=String(txt).split(' ');
  words.forEach((word,wi)=>{
    if(word){
      const w=document.createElement('span'); w.className='wd';
      word.split('').forEach(c=>{
        const s=document.createElement('span'); s.className='ch'; s.textContent=c; w.appendChild(s);
      });
      el.appendChild(w);
    }
    if(wi<words.length-1) el.appendChild(document.createTextNode(' '));
  });
}
function buildHeroText(animate){
  const h=T().hero;
  splitLine($('#hl1'),h.l1);
  splitLine($('#hl2'),h.l2);
  const rot=$('#rot');
  rot.innerHTML='<i class="spacer"></i>';
  const spacer=$('.spacer',rot);
  spacer.textContent=h.rot.reduce((a,b)=>a.length>b.length?a:b);
  h.rot.forEach((w,i)=>{const s=document.createElement('span');s.textContent=w;if(i===0)s.classList.add('on');rot.appendChild(s);});
  rotSpans=$$('span',rot); ri=0;
  if(rotTimer) clearInterval(rotTimer);
  if(!RM) rotTimer=setInterval(nextWord,2600);
  if(animate) animateHeroChars();
}
function animateHeroChars(){
  const chs=$$('[data-split] .ch');
  chs.forEach(c=>c.classList.remove('in'));
  chs.forEach((c,i)=>setTimeout(()=>c.classList.add('in'), 40+i*20));
}
function syncRot(){
  /* rimette il rotatore in uno stato pulito: una sola parola visibile */
  if(!rotSpans.length) return;
  rotSpans.forEach((s,i)=>{ clearTimeout(s._rotT); s.classList.remove('out'); s.classList.toggle('on', i===ri); });
}
function nextWord(){
  if(!rotSpans.length) return;
  if(document.hidden) return;                 /* a scheda nascosta non si avanza */
  const cu=rotSpans[ri]; ri=(ri+1)%rotSpans.length; const nx=rotSpans[ri];
  rotSpans.forEach(s=>{ if(s!==cu && s!==nx){ clearTimeout(s._rotT); s.classList.remove('on','out'); } });
  cu.classList.remove('on'); cu.classList.add('out');
  nx.classList.remove('out');
  void nx.offsetWidth;                        /* forza il reflow: la transizione parte senza rAF */
  nx.classList.add('on');
  clearTimeout(cu._rotT);
  cu._rotT=setTimeout(()=>cu.classList.remove('out'),800);
}
document.addEventListener('visibilitychange',()=>{
  if(document.hidden){ if(rotTimer){ clearInterval(rotTimer); rotTimer=null; } }
  else { syncRot(); if(!RM && !rotTimer) rotTimer=setInterval(nextWord,2600); }
});
addEventListener('pageshow',syncRot);
function startHero(){ animateHeroChars(); runBeam($('#hero')); }

/* =========================================================
   5. RAGGIO DIAGONALE PER SEZIONE
   ========================================================= */
function runBeam(sec){
  if(RM||!sec) return;
  let b=sec.querySelector(':scope > .beam');
  if(!b){b=document.createElement('div');b.className='beam';b.style.top='45%';sec.appendChild(b);}
  b.classList.remove('run'); void b.offsetWidth; b.classList.add('run');
}

/* =========================================================
   6. REVEAL AL SCROLL
   ========================================================= */
const rvIO=new IntersectionObserver(es=>{
  es.forEach(e=>{ if(e.isIntersecting){ e.target.classList.add('in'); rvIO.unobserve(e.target);} });
},{threshold:.12,rootMargin:'0px 0px -8% 0px'});
function bindReveal(){
  $$('[data-rv]').forEach(el=>{
    if(el.dataset.bound) return; el.dataset.bound='1';
    const sib=Array.from(el.parentElement.children).filter(c=>c.hasAttribute('data-rv'));
    el.style.transitionDelay=(sib.indexOf(el)*90)+'ms';
    rvIO.observe(el);
  });
}
const secIO=new IntersectionObserver(es=>{
  es.forEach(e=>{ if(e.isIntersecting){
    runBeam(e.target);
    const id=e.target.id;
    $$('nav.links a').forEach(a=>a.classList.toggle('active',a.getAttribute('href')==='#'+id));
  }});
},{threshold:.22});
$$('section[id]').forEach(s=>secIO.observe(s));

/* =========================================================
   7. TILT 3D + SPOTLIGHT
   ========================================================= */
function bindTilt(){
  $$('[data-tilt]').forEach(el=>{
    if(el.dataset.tb) return; el.dataset.tb='1';
    el.addEventListener('mousemove',e=>{
      const r=el.getBoundingClientRect();
      const px=(e.clientX-r.left)/r.width, py=(e.clientY-r.top)/r.height;
      el.style.setProperty('--mx',(px*100)+'%');
      el.style.setProperty('--my',(py*100)+'%');
      if(RM||innerWidth<900) return;
      el.style.transform=`perspective(1000px) rotateY(${(px-.5)*7}deg) rotateX(${(.5-py)*7}deg) translateY(-6px) scale(1.012)`;
    });
    el.addEventListener('mouseleave',()=>{el.style.transform='';});
  });
}

/* =========================================================
   8. SCROLL / NAV / PARALLAX
   ========================================================= */
const hdr=$('#hdr'), prog=$('#prog'), heroBg=$('#heroBg'), topBtn=$('#top');
let tick=false;
function onScroll(){
  const sy=scrollY;
  if(!tick){requestAnimationFrame(()=>{
    hdr.classList.toggle('stuck',sy>40);
    const max=document.documentElement.scrollHeight-innerHeight;
    prog.style.width=(sy/Math.max(max,1)*100)+'%';
    topBtn.classList.toggle('on',sy>innerHeight*.9);
    if(heroBg && sy<innerHeight*1.3) heroBg.style.transform=`translateY(${sy*.28}px) scale(${1+sy*.00016})`;
    tick=false;
  });tick=true;}
}
addEventListener('scroll',onScroll,{passive:true});
topBtn.addEventListener('click',()=>scrollTo({top:0,behavior:'smooth'}));

const burger=$('#burger'), mob=$('#mob');
burger.addEventListener('click',()=>{
  const on=mob.classList.toggle('on'); burger.classList.toggle('on',on);
  burger.setAttribute('aria-expanded',on?'true':'false');
  document.body.style.overflow=on?'hidden':'';
  if(on) $$('#mob .mob-links a').forEach((a,i)=>a.style.transitionDelay=(120+i*70)+'ms');
});
$$('#mob .mob-links a').forEach(a=>a.addEventListener('click',closeMob));
function closeMob(){mob.classList.remove('on');burger.classList.remove('on');burger.setAttribute('aria-expanded','false');document.body.style.overflow='';}

/* =========================================================
   9. CONTATORI
   ========================================================= */
let cntIO=new IntersectionObserver(es=>{
  es.forEach(e=>{
    if(!e.isIntersecting) return;
    runCount(e.target); cntIO.unobserve(e.target);
  });
},{threshold:.5});
function runCount(el){
  const to=parseFloat(el.dataset.to), suf=el.dataset.suffix||'', dur=1500, t0=performance.now();
  (function step(t){
    const k=clamp((t-t0)/dur,0,1), eased=1-Math.pow(1-k,3);
    el.textContent=Math.round(to*eased)+suf;
    if(k<1) requestAnimationFrame(step);
  })(t0);
}
function bindCounters(force){
  $$('.cnt').forEach(c=>{
    if(force){ const r=c.getBoundingClientRect();
      if(r.top<innerHeight && r.bottom>0){ runCount(c); return; } }
    cntIO.observe(c);
  });
}

/* =========================================================
   10. SCRAMBLE
   ========================================================= */
const CH='ABCDEFGHIJKLMNOPQRSTUVWXYZ#$%&/*<>[]{}';
function scramble(el){
  const fin=el.textContent; let f=0; const total=fin.length*3+12;
  clearInterval(el._sc);
  el._sc=setInterval(()=>{
    f++;
    el.textContent=fin.split('').map((c,i)=> i<f/3 ? c : (c===' '?' ':CH[Math.floor(Math.random()*CH.length)])).join('');
    if(f>=total){clearInterval(el._sc);el.textContent=fin;}
  },28);
}
const scIO=new IntersectionObserver(es=>{es.forEach(e=>{if(e.isIntersecting){if(!RM)scramble(e.target);scIO.unobserve(e.target);}})},{threshold:.6});
function bindScramble(){ $$('[data-scramble]').forEach(e=>scIO.observe(e)); }
function scrambleVisible(){
  if(RM) return;
  $$('[data-scramble]').forEach(e=>{ const r=e.getBoundingClientRect();
    if(r.top<innerHeight&&r.bottom>0) scramble(e); });
}

/* =========================================================
   11. MARQUEE
   ========================================================= */
function fillMq(sel,items){
  const t=$('.track',$(sel));
  const html=items.map(i=>`<span class="it">${i}</span>`).join('');
  t.innerHTML=html+html;
}
const TECH=['React','Next.js','Node.js','TypeScript','WordPress','Shopify','WooCommerce','Laravel','Python','PostgreSQL','Flutter','React Native','Figma','Meta Business','Google Analytics','Docker','AWS','Stripe'];

/* =========================================================
   12. ICONE SETTORI
   ========================================================= */
const ICON={
  food:'<path d="M7 3v8a3 3 0 0 0 6 0V3M10 11v10M17 3c-1.5 2-2 4-2 6s.5 3 2 3v9"/>',
  shop:'<path d="M3 7h18l-1.5 12.5a2 2 0 0 1-2 1.5h-11a2 2 0 0 1-2-1.5L3 7ZM8 7a4 4 0 0 1 8 0"/>',
  home:'<path d="m3 10 9-7 9 7v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2Z"/><path d="M9 21v-7h6v7"/>',
  gym:'<path d="M6 6v12M18 6v12M3 9v6M21 9v6M6 12h12"/>',
  law:'<path d="M12 3v18M5 7h14M7 7l-3 6a3 3 0 0 0 6 0ZM17 7l-3 6a3 3 0 0 0 6 0Z"/>',
  tool:'<path d="M14.7 6.3a4 4 0 0 1 5.3 5.3l-9 9-5.3-5.3 9-9Z"/><path d="m3 21 3-3"/>',
  car:'<path d="M5 17h14M4 17v-4l2-5h12l2 5v4M7 17v2M17 17v2M7 13h.01M17 13h.01"/>',
  med:'<path d="M12 3v18M3 12h18"/><rect x="3" y="3" width="18" height="18" rx="4"/>'
};
const CHECK='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4"><path d="M20 6 9 17l-5-5"/></svg>';
const ARROW='<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 12h14M13 6l6 6-6 6"/></svg>';
const IMGS={
  siti:'/assets/img/dt-03.webp', seo:'/assets/img/dt-09.webp', ads:'/assets/img/dt-08.webp',
  app:'/assets/img/dt-04.webp', gest:'/assets/img/dt-10.webp', soft:'/assets/img/dt-01.webp',
  p1:'/assets/img/dt-05.webp', p2:'/assets/img/dt-02.webp', p3:'/assets/img/dt-11.webp'
};
/* indirizzi delle pagine di servizio, per ogni lingua */
const SRV_SLUG={
  it:['siti-web-ecommerce','seo','meta-ads','app-su-misura','gestionali-crm','software-automazioni'],
  en:['websites-ecommerce','seo','meta-ads','custom-apps','erp-crm','software-automation'],
  de:['websites-ecommerce','seo','meta-ads','individuelle-apps','warenwirtschaft-crm','software-automatisierung'],
  fr:['sites-web-ecommerce','seo','meta-ads','applications-sur-mesure','erp-crm','logiciels-automatisation'],
  es:['webs-ecommerce','seo','meta-ads','apps-a-medida','erp-crm','software-automatizacion']};
const SRV_DIR={it:'servizi',en:'services',de:'leistungen',fr:'services',es:'servicios'};
function srvUrl(i){ return '/'+(LANG==='it'?'':LANG+'/')+SRV_DIR[LANG]+'/'+SRV_SLUG[LANG][i]+'/'; }
const SRV_IMG=[IMGS.siti,IMGS.seo,IMGS.ads,IMGS.app,IMGS.gest,IMGS.soft];
const PREF_BY_LANG={it:'+39',en:'+44',de:'+49',fr:'+33',es:'+34'};
const PF_META=[
  {c:'web', img:IMGS.p1,   k:['+184%','1.2s']},
  {c:'gest',img:IMGS.p2,   k:['-11h','4']},
  {c:'app', img:IMGS.p3,   k:['8.400','+37%']},
  {c:'ads', img:IMGS.ads,  k:['€4,10','x5,8']},
  {c:'web', img:IMGS.siti, k:['+220%','100']},
  {c:'ads', img:IMGS.seo,  k:['#1','+310%']}
];
const PF_KEYS=['all','web','app','gest','ads'];

/* =========================================================
   13. RENDER COMPLETO DEI CONTENUTI
   ========================================================= */
function render(){
  const t=T();

  /* --- testi semplici via data-i18n --- */
  /* si riscrive solo cio' che cambia: riscrivere testi identici (es. il sottotitolo
     dell'hero) fa ripartire il conteggio LCP di Google e rallenta la pagina */
  const setT=(el,v)=>{ if(el && typeof v==='string' && el.textContent!==v) el.textContent=v; };
  const setH=(el,v)=>{ if(el && typeof v==='string' && el.innerHTML.trim()!==v.trim()) el.innerHTML=v; };
  $$('[data-i18n]').forEach(el=>setT(el,dig(t,el.dataset.i18n)));
  $$('[data-i18n-html]').forEach(el=>setH(el,dig(t,el.dataset.i18nHtml)));
  setT($('#hcta1'),t.hero.cta1);
  setT($('#hcta2'),t.hero.cta2);
  setT($('#scrollLbl'),t.hero.scroll);
  setT($('.nav-r .btn-p .lbl'),t.nav.cta);
  setH($('#heroSub'),t.hero.sub);

  /* --- meta / lang --- */
  document.documentElement.lang=t.htmlLang;
  document.title=t.meta.title;
  const md=document.querySelector('meta[name="description"]'); if(md) md.content=t.meta.desc;

  /* --- hero stats --- */
  const gg = LANG==='it' ? ' gg' : LANG==='de' ? ' Tage' : ' days';
  const sufs=[NUMS_HERO_SUF[0],NUMS_HERO_SUF[1],gg,'/7'];
  $('#heroStats').innerHTML=t.hero.stats.map((s,i)=>
    `<div><b class="cnt" data-to="${NUMS_HERO[i]}" data-suffix="${sufs[i]}">0</b><small>${s}</small></div>`).join('');

  /* --- marquee --- */
  fillMq('#mq1',t.mq); fillMq('#mq2',TECH);

  /* --- prefisso telefonico coerente con la lingua (se l'utente non l'ha toccato) --- */
  const _pf=$('#pref');
  if(_pf && !_pf.dataset.touched){ const _v=PREF_BY_LANG[LANG]; if(_v && [..._pf.options].some(o=>o.value===_v)) _pf.value=_v; }

  /* --- servizi --- */
  const SRV_URL=t.servizi.items.map((_,i)=>srvUrl(i));
  $('#srvGrid').innerHTML=t.servizi.items.map((s,i)=>`
    <article class="card srv" data-tilt data-rv="blur"><i class="edge"></i>
      <div class="pic"><span class="num">0${i+1}</span><div class="scan"></div>
        <img src="${SRV_IMG[i]}" alt="Danova Tech — ${s.t}" width="1000" height="737"
             loading="lazy" decoding="async"></div>
      <div class="body">
        <h3>${s.t}</h3><p>${s.p}</p>
        <ul>${s.l.map(x=>`<li>${CHECK}${x}</li>`).join('')}</ul>
        <a href="${SRV_URL[i]}" class="more"><span>${s.m}</span>${ARROW}</a>
      </div>
    </article>`).join('');

  /* --- settori --- */
  $('#sectGrid').innerHTML=t.settori.items.map(([ic,ti,d])=>`
    <div class="sect" data-rv="up" data-tilt>
      <div class="ic"><svg width="21" height="21" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">${ICON[ic]}</svg></div>
      <h4>${ti}</h4><p>${d}</p>
    </div>`).join('');

  /* --- filtri + portfolio --- */
  $('#pfFilters').innerHTML=t.lavori.filters.map((f,i)=>
    `<button class="${i===0?'on':''}" data-f="${PF_KEYS[i]}">${f}</button>`).join('');
  $('#pfGrid').innerHTML=t.lavori.items.map((pj,i)=>{
    const m=PF_META[i];
    return `<article class="card pf" data-c="${m.c}" data-rv="up" data-tilt><i class="edge"></i>
      <div class="pic"><img src="${m.img}" alt="${ALT_PRJ[LANG]||ALT_PRJ.en} — ${pj.t}" width="1000" height="700" loading="lazy" decoding="async">
        <div class="ov"><span class="go">${t.lavori.go}
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M7 17 17 7M9 7h8v8"/></svg></span></div>
      </div>
      <div class="body">
        <span class="tag">${pj.tag}</span><h3>${pj.t}</h3><p>${pj.d}</p>
        <div class="kpi">${pj.k.map((lbl,j)=>`<div><b>${m.k[j]}</b><small>${lbl}</small></div>`).join('')}</div>
      </div>
    </article>`;
  }).join('');
  bindFilters();

  /* --- processo --- */
  const proc=$('#proc');
  proc.innerHTML='<div class="line"><i></i></div>'+t.processo.items.map((s,i)=>`
    <div class="step"><div class="no">0${i+1}</div><div class="txt">
      <h3>${s.t}</h3><p>${s.p}</p>
      <div class="meta">${s.m.map(x=>`<span>${x}</span>`).join('')}</div>
    </div></div>`).join('');

  /* --- numeri --- */
  $('#numsBox').innerHTML=t.numeri.map((lbl,i)=>
    `<div><b class="cnt" data-to="${NUMS_BIG[i]}" data-suffix="${t.numeriSuffix[i]}">0</b><small>${lbl}</small></div>`).join('');

  /* --- testimonial --- */
  const TST=t.dicono.items;
  $('#tst').innerHTML=TST.map(([q,av,n,r],i)=>`
    <div class="q ${i===0?'on':''}">
      <blockquote>“${q}”</blockquote>
      <div class="who"><div class="av">${av}</div><div><b>${n}</b><small>${r}</small></div></div>
    </div>`).join('');
  $('#tstDots').innerHTML=TST.map((_,i)=>`<i class="${i===0?'on':''}" data-i="${i}"></i>`).join('');
  bindTst(TST.length);

  /* --- FAQ --- */
  $('#faqBox').innerHTML=t.faq.items.map(([q,a])=>`
    <details data-rv="up"><summary>${q}<span class="pm"></span></summary>
      <div class="ans"><p>${a}</p></div></details>`).join('');
  bindFaq();

  /* --- CTA list + form select --- */
  $('#ctaList').innerHTML=t.cta.list.map(x=>
    `<div><svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4"><path d="M20 6 9 17l-5-5"/></svg>${x}</div>`).join('');
  const sel=$('#tipo'), prev=sel.selectedIndex;
  sel.innerHTML='<option value="" disabled selected hidden></option>'+t.cta.f.opts.map(o=>`<option>${o}</option>`).join('');
  if(prev>0) sel.selectedIndex=prev;

  /* --- footer --- */
  $('#fc1').innerHTML=t.footer.c1.map((x,i)=>`<li><a href="${srvUrl(i)}">${x}</a></li>`).join('');
  const ABOUT_URL={it:'/chi-siamo/',en:'/en/about/',de:'/de/ueber-uns/',fr:'/fr/a-propos/',es:'/es/sobre-nosotros/'};
  $$('[data-about]').forEach(a=>a.href=ABOUT_URL[LANG]);
  /* pagina Prezzi: un indirizzo per lingua */
  const PRICING_URL={it:'/prezzi/',en:'/en/pricing/',de:'/de/preise/',fr:'/fr/tarifs/',es:'/es/precios/'};
  const PRICING_LBL={it:'Prezzi',en:'Pricing',de:'Preise',fr:'Tarifs',es:'Precios'};
  $$('[data-pricing]').forEach(a=>a.href=PRICING_URL[LANG]);
  const anch=['#settori','#lavori','#processo',ABOUT_URL[LANG],'#faq','#contatti'];
  const c2=t.footer.c2.map((x,i)=>`<li><a href="${anch[i]}">${x}</a></li>`);
  c2.push(`<li><a href="${PRICING_URL[LANG]}">${PRICING_LBL[LANG]}</a></li>`);
  if(LANG==='it') c2.push('<li><a href="/guide/">Guide</a></li>');
  $('#fc2').innerHTML=c2.join('');

  /* --- blocco "Dove operiamo": pagine solo in italiano, quindi visibile solo in IT --- */
  const IT=(LANG==='it'), ZN=$('#zone'), FZ=$('#fcZone'), FT=$('#fTop'), AP=$('#approf');
  if(ZN) ZN.style.display=IT?'':'none';
  if(AP) AP.style.display=IT?'':'none';
  if(FZ) FZ.style.display=IT?'':'none';
  if(FT) FT.classList.toggle('z5',IT);

  /* --- link legali nel footer --- */
  const LGL_URL={
    it:[['/privacy/','Privacy Policy'],['/cookie-policy/','Cookie Policy'],['/termini/','Termini'],['/contatti/','Contatti']],
    en:[['/en/privacy/','Privacy Policy'],['/en/cookie-policy/','Cookie Policy'],['/en/terms/','Terms'],['/en/contact/','Contact']],
    de:[['/de/datenschutz/','Datenschutz'],['/de/cookie-richtlinie/','Cookie-Richtlinie'],['/de/agb/','AGB'],['/de/kontakt/','Kontakt']],
    fr:[['/fr/confidentialite/','Confidentialit\u00e9'],['/fr/cookies/','Cookies'],['/fr/conditions/','Conditions'],['/fr/contact/','Contact']],
    es:[['/es/privacidad/','Privacidad'],['/es/cookies/','Cookies'],['/es/condiciones/','Condiciones'],['/es/contacto/','Contacto']]
  };
  const FL=$('#fLegal');
  if(FL) FL.innerHTML=(LGL_URL[LANG]||LGL_URL.it)
    .map(([u,x])=>`<a href="${u}">${x}</a>`).join('<i>\u00b7</i>');
  if(LGL_CUR) paintLegal();

  /* --- rebind --- */
  bindReveal(); bindTilt(); bindMag(); bindScramble(); bindAnchors();
}

/* =========================================================
   14. FILTRI PORTFOLIO
   ========================================================= */
function bindFilters(){
  $$('#pfFilters button').forEach(b=>b.addEventListener('click',()=>{
    $$('#pfFilters button').forEach(x=>x.classList.remove('on')); b.classList.add('on');
    const f=b.dataset.f;
    $$('.pf').forEach((c,i)=>{
      const show=f==='all'||c.dataset.c===f;
      if(show){c.classList.remove('hidden');c.style.transitionDelay=(i*45)+'ms';}
      else c.classList.add('hidden');
    });
  }));
}

/* =========================================================
   15. PROCESSO — linea che si disegna
   ========================================================= */
function procScroll(){
  const proc=$('#proc'); if(!proc) return;
  const line=$('#proc .line i'); if(!line) return;
  const r=proc.getBoundingClientRect();
  line.style.transform=`scaleY(${clamp((innerHeight*.75-r.top)/(r.height*.85),0,1)})`;
  $$('#proc .step').forEach(s=>s.classList.toggle('lit', s.getBoundingClientRect().top<innerHeight*.7));
}
addEventListener('scroll',procScroll,{passive:true});

/* =========================================================
   16. TESTIMONIAL
   ========================================================= */
let ti=0,tAuto=null;
function bindTst(n){
  ti=0; clearInterval(tAuto);
  $$('#tstDots i').forEach(d=>d.addEventListener('click',()=>{goT(+d.dataset.i);restartT(n);}));
  if(!RM) restartT(n);
}
function goT(n){
  const qs=$$('#tst .q'), ds=$$('#tstDots i');
  if(!qs.length) return;
  qs[ti].classList.remove('on'); ds[ti].classList.remove('on');
  ti=n; qs[ti].classList.add('on'); ds[ti].classList.add('on');
}
function restartT(n){clearInterval(tAuto);tAuto=setInterval(()=>goT((ti+1)%n),5200);}

/* =========================================================
   17. FAQ
   ========================================================= */
function bindFaq(){
  $$('#faqBox details').forEach(d=>{
    const ans=$('.ans',d), sum=$('summary',d);
    sum.addEventListener('click',e=>{
      e.preventDefault();
      const open=d.hasAttribute('open');
      $$('#faqBox details[open]').forEach(o=>{ if(o!==d){$('.ans',o).style.height='0px';setTimeout(()=>o.removeAttribute('open'),300);} });
      if(open){ ans.style.height=ans.scrollHeight+'px'; requestAnimationFrame(()=>ans.style.height='0px');
        setTimeout(()=>d.removeAttribute('open'),480);
      }else{
        d.setAttribute('open',''); ans.style.height='0px';
        requestAnimationFrame(()=>ans.style.height=ans.scrollHeight+'px');
        setTimeout(()=>{ if(d.hasAttribute('open')) ans.style.height='auto'; },520);
      }
    });
  });
}

/* =========================================================
   18. FORM
   ========================================================= */
/* --- validazione telefono --- */
const TEL_LEN={'+39':[9,11],'+41':[9,9],'+49':[9,12],'+43':[9,13],'+33':[9,9],'+34':[9,9],
  '+44':[9,10],'+31':[9,9],'+32':[8,9],'+351':[9,9],'+353':[7,9],'+1':[10,10],'+7':[10,10],
  '+30':[10,10],'+48':[9,9],'+420':[9,9],'+45':[8,8],'+46':[7,10],'+47':[8,8],'+358':[6,10]};
function telParts(){
  const pref=($('#pref')||{}).value||'+39';
  let d=(($('#tel')||{}).value||'').replace(/\D/g,'');
  if(pref!=='+39') d=d.replace(/^0+/,'');          // tolgo lo zero interurbano (in IT fa parte del numero)
  return {pref,d};
}
function telOk(){
  const {pref,d}=telParts();
  if(!d) return false;
  if(/^(\d)\1+$/.test(d)) return false;             // cifre tutte uguali
  const r=TEL_LEN[pref]||[6,14];
  if(d.length<r[0]||d.length>r[1]) return false;
  const tot=pref.replace(/\D/g,'').length+d.length;
  return tot>=8&&tot<=15;
}
function mailOk(){
  const v=(($('#email')||{}).value||'').trim();
  return !v || /^[^\s@]+@[^\s@]+\.[a-z]{2,}$/i.test(v);
}
(function(){
  const t=$('#tel'), e=$('#email'), p=$('#pref');
  if(t){
    t.addEventListener('input',()=>{                // solo caratteri plausibili
      const c=t.value.replace(/[^\d\s().\/-]/g,'');
      if(c!==t.value) t.value=c;
      t.classList.remove('bad'); $('#telErr').classList.remove('on');
    });
    t.addEventListener('blur',()=>{ if(t.value.trim()&&!telOk()){ t.classList.add('bad'); $('#telErr').classList.add('on'); } });
  }
  if(p) p.addEventListener('change',()=>{ p.dataset.touched='1'; t.classList.remove('bad'); $('#telErr').classList.remove('on'); });
  if(e){
    e.addEventListener('input',()=>{ e.classList.remove('bad'); $('#emailErr').classList.remove('on'); });
    e.addEventListener('blur',()=>{ if(!mailOk()){ e.classList.add('bad'); $('#emailErr').classList.add('on'); } });
  }
})();

$('#form').addEventListener('submit',e=>{
  e.preventDefault();
  const g=id=>((($('#'+id)||{}).value)||'').trim();
  const shake=el=>{
    if(!el) return;
    el.classList.add('bad');
    el.animate([{transform:'translateX(0)'},{transform:'translateX(-7px)'},{transform:'translateX(7px)'},{transform:'translateX(0)'}],{duration:300});
  };
  let first=null;
  ['nome','azienda','tipo'].forEach(id=>{ if(!g(id)){ shake($('#'+id)); first=first||$('#'+id); } });
  if(!telOk()){ shake($('#tel')); $('#telErr').classList.add('on'); first=first||$('#tel'); }
  else { $('#tel').classList.remove('bad'); $('#telErr').classList.remove('on'); }
  if(!mailOk()){ shake($('#email')); $('#emailErr').classList.add('on'); first=first||$('#email'); }
  else { $('#email').classList.remove('bad'); $('#emailErr').classList.remove('on'); }
  if(first){ if(first.focus) first.focus(); return; }

  const f=T().cta.f, tp=telParts();
  const lines=[
    f.subj,
    '',
    f.nome+': '+g('nome'),
    f.tel+': '+tp.pref+' '+tp.d,
    f.azienda+': '+g('azienda'),
    f.tipo+': '+g('tipo')
  ];
  if(g('email')) lines.push('Email: '+g('email'));
  const url='https://wa.me/'+WA+'?text='+encodeURIComponent(lines.join('\n'));
  const openWa=()=>{
    // 14/10/2026: senza 'noopener' (che faceva restituire null a window.open e apriva WhatsApp due volte, anche nella pagina corrente)
    let w=null; try{ w=window.open(url,'_blank'); }catch(_){}
    if(w){ try{ w.opener=null; }catch(_){} } else location.href=url;
  };
  /* 15/10/2026: la richiesta arriva direttamente via email (contatto.js); WhatsApp resta il ripiego */
  if(window.DTLead){
    const btn=$('#form button[type=submit]'); if(btn) btn.disabled=true;
    try{ if(window.gtag) gtag('event','generate_lead',{method:'form',form:'home'}); }catch(_){}
    window.DTLead.send(f.subj+' - '+g('azienda'),[[f.nome,g('nome')],[f.azienda,g('azienda')],[f.tipo,g('tipo')],[f.tel,tp.pref+' '+tp.d],['Email',g('email')]],g('email'))
      .then(ok=>{ if(btn) btn.disabled=false; if(ok){ $('#ok').classList.add('on'); $('#form').reset(); } else openWa(); });
    return;
  }
  $('#ok').classList.add('on');
  openWa();
});

/* =========================================================
   19. SELETTORE LINGUA + TRANSIZIONE
   ========================================================= */
const langBox=$('#lang'), langBtn=$('#langBtn'), langMenu=$('#langMenu'), langCode=$('#langCode');
const fx=$('#langfx');
langBtn.addEventListener('click',e=>{
  e.stopPropagation();
  const on=langBox.classList.toggle('on');
  langBtn.setAttribute('aria-expanded',on);
});
document.addEventListener('click',e=>{ if(!e.target.closest('#lang')) langBox.classList.remove('on'); });
addEventListener('keydown',e=>{ if(e.key==='Escape'){langBox.classList.remove('on');closeMob();} });
$$('#langMenu button, #mobLang button').forEach(b=>b.addEventListener('click',()=>{
  setLang(b.dataset.lang);
  langBox.classList.remove('on');
  if(mob.classList.contains('on')) closeMob();
}));

function markSelected(){
  $$('#langMenu button, #mobLang button').forEach(b=>b.classList.toggle('sel',b.dataset.lang===LANG));
  langCode.textContent=T().code;
}
/* I dizionari delle altre lingue si scaricano solo quando servono. */
const LANG_LOADING={};
function loadLang(l,cb){
  if(window.I18N[l]) return cb();
  if(LANG_LOADING[l]) return LANG_LOADING[l].push(cb);
  LANG_LOADING[l]=[cb];
  const s=document.createElement('script');
  s.src='/assets/js/i18n-'+l+'.js?v=20261018';
  s.onload=()=>{ const q=LANG_LOADING[l]; LANG_LOADING[l]=null; q.forEach(f=>f()); };
  s.onerror=()=>{ LANG_LOADING[l]=null; };
  document.head.appendChild(s);
}
function setLang(l,instant){
  if(l===LANG && !instant) return;
  if(!window.I18N[l]){ loadLang(l,()=>setLang(l,instant)); return; }
  LANG=l;
  syncLangUrl();
  if(instant||RM){ render(); markSelected(); bindCounters(true); return; }

  /* effetto: slash a tutto schermo + sigla lingua */
  $('#lfxCode').textContent=T().code;
  $('#lfxName').textContent=T().name;
  fx.classList.remove('on'); void fx.offsetWidth; fx.classList.add('on');
  document.body.classList.add('swapping');
  langCode.classList.remove('swap'); void langCode.offsetWidth; langCode.classList.add('swap');

  setTimeout(()=>{                       /* a metà sweep sostituisco i contenuti */
    render(); markSelected();
    buildHeroText(false);
  },430);
  setTimeout(()=>{                       /* contenuti riappaiono e ri-animano */
    document.body.classList.remove('swapping');
    animateHeroChars(); scrambleVisible(); bindCounters(true);
    $$('section[id]').forEach(s=>{ const r=s.getBoundingClientRect();
      if(r.top<innerHeight&&r.bottom>0) runBeam(s); });
    procScroll();
  },700);
  setTimeout(()=>fx.classList.remove('on'),1250);
}

/* =========================================================
   20. VARIE + INIT
   ========================================================= */
function bindAnchors(){
  $$('a[href^="#"]').forEach(a=>{
    if(a.dataset.ab) return; a.dataset.ab='1';
    a.addEventListener('click',e=>{
      const t=document.querySelector(a.getAttribute('href')); if(!t) return;
      e.preventDefault();
      scrollTo({top:t.getBoundingClientRect().top+scrollY-56,behavior:'smooth'});
    });
  });
}
document.addEventListener('mousemove',e=>{
  const c=e.target.closest('.card,.sect'); if(!c) return;
  const r=c.getBoundingClientRect();
  c.style.setProperty('--mx',((e.clientX-r.left)/r.width*100)+'%');
  c.style.setProperty('--my',((e.clientY-r.top)/r.height*100)+'%');
});

/* =========================================================
   19b. LEGALI — Privacy Policy / Cookie Policy / Termini
   ========================================================= */
const LGL_KEYS=['privacy','cookie','terms'];
let LGL_CUR=null;
const lgl=$('#lgl');

function paintLegal(){
  if(!LGL_CUR) return;
  const L=T().legal, d=L.docs[LGL_CUR];
  $('#lglEye').textContent=L.eyebrow;
  $('#lglTitle').textContent=d.t;
  $('#lglTabs').innerHTML=LGL_KEYS.map((k,i)=>
    `<button type="button" data-lg="${k}" class="${k===LGL_CUR?'on':''}">${L.nav[i]}</button>`).join('');
  $$('#lglTabs button').forEach(b=>b.addEventListener('click',()=>{
    LGL_CUR=b.dataset.lg; paintLegal(); $('#lglBody').scrollTop=0;
  }));
  $('#lglBody').innerHTML=d.s.map((sec,i)=>
    `<h4><b>${String(i+1).padStart(2,'0')}</b>${sec[0]}</h4>${sec[1]}`).join('');
  $('#lglUpd').textContent=L.updated;
  $('#lglDone').textContent=L.close;
}
function openLegal(k){
  LGL_CUR=k; paintLegal();
  lgl.classList.add('on'); lgl.setAttribute('aria-hidden','false');
  document.body.style.overflow='hidden';
  $('#lglBody').scrollTop=0;
  setTimeout(()=>$('#lglX').focus({preventScroll:true}),120);
}
function closeLegal(){
  lgl.classList.remove('on'); lgl.setAttribute('aria-hidden','true');
  document.body.style.overflow='';
}
$('#lglX').addEventListener('click',closeLegal);
$('#lglDone').addEventListener('click',closeLegal);
$('#lglBd').addEventListener('click',closeLegal);
addEventListener('keydown',e=>{ if(e.key==='Escape' && lgl.classList.contains('on')) closeLegal(); });

/* Lingua di partenza. Metti 'auto' al posto di 'it' per seguire la lingua del browser. */
const START_LANG=(window.DT&&window.DT.lang)||'it';
if(window.I18N[START_LANG]) LANG=START_LANG;
else LANG=Object.keys(window.I18N)[0]||'it';

render();
buildHeroText(false);
markSelected();
bindCounters(false);
$('#yy').textContent=new Date().getFullYear();
onScroll(); procScroll();

/* Quando il browser e' libero, scarica in sottofondo gli altri dizionari:
   il cambio lingua resta istantaneo senza pesare sul primo caricamento. */
const OTHERS=['it','en','de','fr','es'].filter(l=>l!==LANG);
const idle=window.requestIdleCallback||(f=>setTimeout(f,2500));
addEventListener('load',()=>idle(()=>OTHERS.forEach((l,i)=>setTimeout(()=>loadLang(l,()=>{}),i*300))));
})();

/* Allestimenti fieristici: il pulsante della sezione preseleziona la voce nel modulo contatti */
document.addEventListener('click',e=>{
  const a=e.target.closest&&e.target.closest('[data-pick-tipo]'); if(!a) return;
  const s=document.getElementById('tipo'); if(!s||s.options.length<3) return;
  s.selectedIndex=s.options.length-2; s.dispatchEvent(new Event('change',{bubbles:true}));
});
