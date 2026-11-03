/* ============================================================
   DANOVA TECH — animazioni delle pagine interne
   Gli stessi blocchi della home (cursore, reveal, tilt, raggio,
   scramble, barra di scorrimento, FAQ), senza il preloader.
   ============================================================ */
(function(){
"use strict";
const RM = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
const $  = (s,c)=> (c||document).querySelector(s);
const $$ = (s,c)=> Array.from((c||document).querySelectorAll(s));
const lerp=(a,b,t)=>a+(b-a)*t;
document.documentElement.classList.remove('no-js');

/* ---------- 1. cursore + magnetico ---------- */
const cur=$('.cur'), ring=$('.cur-r');
/* mouse vero (anche su portatili con schermo touch); prima si guardava solo 'ontouchstart' e sui portatili touch il cursore spariva */
const DESKTOP = window.matchMedia ? matchMedia('(hover:hover) and (pointer:fine)').matches && innerWidth>1024 : !('ontouchstart' in window) && innerWidth>1024;
if(DESKTOP && cur && ring){
  let mx=innerWidth/2,my=innerHeight/2,rx=mx,ry=my;
  let on=false;
  addEventListener('mousemove',e=>{mx=e.clientX;my=e.clientY;
    if(!on){on=true;rx=mx;ry=my;document.documentElement.classList.add('cur-on');}
    cur.style.transform=`translate(${mx}px,${my}px) translate(-50%,-50%)`;});
  (function loop(){rx=lerp(rx,mx,.16);ry=lerp(ry,my,.16);
    ring.style.transform=`translate(${rx}px,${ry}px) translate(-50%,-50%)`;requestAnimationFrame(loop);})();
  addEventListener('mouseleave',()=>ring.classList.add('hide'));
  addEventListener('mouseenter',()=>ring.classList.remove('hide'));
  const HOV='a,button,summary,[data-tilt],input,textarea,select';
  document.addEventListener('mouseover',e=>{ if(e.target.closest(HOV)) ring.classList.add('big');});
  document.addEventListener('mouseout', e=>{ if(e.target.closest(HOV)) ring.classList.remove('big');});
}
if(DESKTOP){
  $$('[data-mag]').forEach(el=>{
    el.addEventListener('mousemove',e=>{
      const r=el.getBoundingClientRect();
      const x=(e.clientX-(r.left+r.width/2))*.28, y=(e.clientY-(r.top+r.height/2))*.4;
      el.style.transform=`translate(${x}px,${y}px)`;
    });
    el.addEventListener('mouseleave',()=>{el.style.transform='';});
  });
}

/* ---------- 2. raggio diagonale per sezione ---------- */
function runBeam(sec){
  if(RM||!sec) return;
  let b=sec.querySelector(':scope > .beam');
  if(!b){b=document.createElement('div');b.className='beam';b.style.top='45%';sec.appendChild(b);}
  b.classList.remove('run'); void b.offsetWidth; b.classList.add('run');
}

/* ---------- 3. comparsa al scorrimento ---------- */
const rvIO=new IntersectionObserver(es=>{
  es.forEach(e=>{ if(e.isIntersecting){ e.target.classList.add('in'); rvIO.unobserve(e.target);} });
},{threshold:.12,rootMargin:'0px 0px -8% 0px'});
$$('[data-rv]').forEach(el=>{
  const sib=Array.from(el.parentElement.children).filter(c=>c.hasAttribute('data-rv'));
  el.style.transitionDelay=(sib.indexOf(el)*90)+'ms';
  rvIO.observe(el);
});
const secIO=new IntersectionObserver(es=>{
  es.forEach(e=>{ if(e.isIntersecting) runBeam(e.target); });
},{threshold:.22});
$$('section').forEach(s=>secIO.observe(s));

/* ---------- 4. inclinazione 3D + faretto ---------- */
$$('[data-tilt]').forEach(el=>{
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

/* ---------- 5. intestazione, barra di avanzamento, torna su ---------- */
const hdr=$('#hdr'), prog=$('#prog'), topBtn=$('#top');
let tick=false;
function onScroll(){
  const sy=scrollY;
  if(!tick){requestAnimationFrame(()=>{
    if(hdr) hdr.classList.toggle('stuck',sy>40);
    if(prog){ const max=document.documentElement.scrollHeight-innerHeight;
      prog.style.width=(sy/Math.max(max,1)*100)+'%'; }
    if(topBtn) topBtn.classList.toggle('on',sy>innerHeight*.9);
    tick=false;
  });tick=true;}
}
addEventListener('scroll',onScroll,{passive:true});
if(topBtn) topBtn.addEventListener('click',()=>scrollTo({top:0,behavior:'smooth'}));

/* ---------- 6. menu mobile ---------- */
const burger=$('#burger'), mob=$('#mob');
if(burger && mob){
  burger.addEventListener('click',()=>{
    const on=mob.classList.toggle('on'); burger.classList.toggle('on',on);
    burger.setAttribute('aria-expanded',on?'true':'false');
    document.body.style.overflow=on?'hidden':'';
    if(on) $$('#mob a').forEach((a,i)=>a.style.transitionDelay=(120+i*70)+'ms');
  });
  addEventListener('keydown',e=>{ if(e.key==='Escape' && mob.classList.contains('on')){
    mob.classList.remove('on');burger.classList.remove('on');burger.setAttribute('aria-expanded','false');document.body.style.overflow='';burger.focus(); } });
  $$('#mob a').forEach(a=>a.addEventListener('click',()=>{
    mob.classList.remove('on');burger.classList.remove('on');burger.setAttribute('aria-expanded','false');document.body.style.overflow='';
  }));
}

/* ---------- 7. scramble delle etichette ---------- */
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
const scIO=new IntersectionObserver(es=>{es.forEach(e=>{
  if(e.isIntersecting){ if(!RM) scramble(e.target); scIO.unobserve(e.target);}
})},{threshold:.6});
$$('[data-scramble]').forEach(e=>scIO.observe(e));

/* ---------- 8. domande frequenti ---------- */
$$('.faq details').forEach(d=>{
  const ans=$('.ans',d), sum=$('summary',d);
  if(!ans||!sum) return;
  sum.addEventListener('click',e=>{
    e.preventDefault();
    const open=d.hasAttribute('open');
    $$('.faq details[open]').forEach(o=>{ if(o!==d){
      const a=$('.ans',o); if(a) a.style.height='0px';
      setTimeout(()=>o.removeAttribute('open'),300);} });
    if(open){
      ans.style.height=ans.scrollHeight+'px';
      requestAnimationFrame(()=>ans.style.height='0px');
      setTimeout(()=>d.removeAttribute('open'),480);
    }else{
      d.setAttribute('open',''); ans.style.height='0px';
      requestAnimationFrame(()=>ans.style.height=ans.scrollHeight+'px');
      setTimeout(()=>{ if(d.hasAttribute('open')) ans.style.height='auto'; },520);
    }
  });
});

/* ---------- 9. anno nel piede ---------- */
const yy=$('#yy'); if(yy) yy.textContent=new Date().getFullYear();
onScroll();
})();

/* ---------- 10. selettore lingua compatto ----------
   Nell'HTML le lingue restano link veri (utili a Google e alle AI); qui la riga
   di link dell'header diventa un menu a tendina, cosi' occupa sempre lo stesso
   spazio anche con 9 lingue. Senza JS resta la riga di link originale. */
(function(){
  const NOMI={it:'Italiano',en:'English',de:'Deutsch',fr:'Français',es:'Español','zh-Hans':'简体中文','zh-Hant':'繁體中文',tr:'Türkçe',ar:'العربية'};
  const SVG='<svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="1.7" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c2.5 2.6 3.8 5.6 3.8 9s-1.3 6.4-3.8 9c-2.5-2.6-3.8-5.6-3.8-9S9.5 5.6 12 3z"/></svg>';
  const CHEV='<svg viewBox="0 0 24 24" width="12" height="12" fill="none" stroke="currentColor" stroke-width="2.2" aria-hidden="true"><path d="m6 9 6 6 6-6"/></svg>';
  document.querySelectorAll('header .lang-links').forEach(function(w,n){
    const links=Array.prototype.slice.call(w.querySelectorAll('a'));
    if(links.length<2) return;
    const cur=w.querySelector('a[aria-current]')||links[0];
    const id='ll-menu-'+n;
    const btn=document.createElement('button');
    btn.type='button'; btn.className='ll-btn';
    btn.setAttribute('aria-haspopup','true'); btn.setAttribute('aria-expanded','false'); btn.setAttribute('aria-controls',id);
    btn.setAttribute('aria-label','Lingua / Language: '+(NOMI[cur.getAttribute('hreflang')]||cur.textContent.trim()));
    btn.innerHTML=SVG+'<span>'+cur.textContent.trim()+'</span>'+CHEV;
    const menu=document.createElement('span'); menu.className='ll-menu'; menu.id=id;
    links.forEach(function(a){
      const code=a.textContent.trim(), nome=NOMI[a.getAttribute('hreflang')]||code;
      a.innerHTML='<span class="ll-nome"></span><b></b>';
      a.firstChild.textContent=nome; a.lastChild.textContent=code;
      if(a.getAttribute('hreflang')==='ar') a.firstChild.setAttribute('dir','rtl');
      menu.appendChild(a);
    });
    w.textContent=''; w.appendChild(btn); w.appendChild(menu); w.classList.add('ll');
    function set(open){ w.classList.toggle('open',open); btn.setAttribute('aria-expanded',open?'true':'false'); }
    btn.addEventListener('click',function(e){ e.stopPropagation(); set(!w.classList.contains('open')); });
    document.addEventListener('click',function(e){ if(!w.contains(e.target)) set(false); });
    document.addEventListener('keydown',function(e){ if(e.key==='Escape' && w.classList.contains('open')){ set(false); btn.focus(); } });
  });
})();
