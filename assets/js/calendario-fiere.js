/* Calendario fiere: filtri, mappa interattiva (Leaflet caricato solo quando serve), richiesta stand. Danova Tech, ottobre 2026 */
(function(){
  var $=function(s,c){return (c||document).querySelector(s)}, $$=function(s,c){return Array.prototype.slice.call((c||document).querySelectorAll(s))};
  var dataEl=$('#cal-data'); if(!dataEl) return;
  var V=JSON.parse(dataEl.textContent).v;
  var items=$$('.cal-ev'), oggi=new Date().toISOString().slice(0,10);
  // le fiere gia' concluse spariscono anche se la pagina non e' stata rigenerata
  items.forEach(function(li){ if(li.dataset.end<oggi){ li.classList.add('past'); li.hidden=true; } });
  items=items.filter(function(li){return !li.classList.contains('past')});
  var q=$('#cal-q'), fp=$('#cal-paese'), fs=$('#cal-sett'), fm=$('#cal-mese'), cnt=$('#cal-count'), empty=$('#cal-empty');
  var norm=function(s){return (s||'').toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g,'')};
  items.forEach(function(li){ li._t=norm(li.textContent); });
  var map=null, layer=null, markers={};
  function visibili(){ return items.filter(function(li){return !li.hidden}); }
  function filtra(){
    var t=norm(q.value.trim()), p=fp.value, s=fs.value, m=fm.value;
    items.forEach(function(li){
      li.hidden=!((!p||li.dataset.paese===p)&&(!s||li.dataset.sett===s)&&(!m||li.dataset.mese===m)&&(!t||li._t.indexOf(t)>-1));
    });
    $$('.cal-mese').forEach(function(g){ g.hidden=!$$('.cal-ev',g).some(function(li){return !li.hidden}); });
    var n=visibili().length;
    cnt.textContent=n===1?'1 fiera trovata':n+' fiere trovate';
    empty.style.display=n?'none':'block';
    disegna();
  }
  [q,fp,fs,fm].forEach(function(el){ el.addEventListener(el===q?'input':'change',filtra); });
  function esc(s){return String(s).replace(/[&<>"]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]})}
  function popup(vk,lis){
    var v=V[vk], h='<b>'+esc(v.n)+'</b><br><span style="color:#8b97b0">'+esc(v.c)+', '+esc(v.p)+'</span><ul style="list-style:none;padding:0;margin:10px 0 0;display:grid;gap:10px;max-height:240px;overflow:auto">';
    lis.forEach(function(li){
      var a=li.querySelector('h4 a'), nome=li.querySelector('h4').childNodes[0].textContent, d=li.querySelector('.d').textContent.replace(/(\d{4})$/,' $1');
      var req=li.querySelector('[data-req]').getAttribute('data-req');
      h+='<li><b>'+(a?'<a href="'+a.getAttribute('href')+'" style="color:#fff">'+esc(nome)+'</a>':esc(nome))+'</b><br><span style="color:#bcd3ff;font-size:12.5px">'+esc(d)+'</span><br>'+
         '<button type="button" class="cal-btn" data-req="'+esc(req)+'">Richiedi lo stand</button> <a class="cal-btn g" href="#f-'+li.dataset.id+'" data-goto="'+li.dataset.id+'">Dettagli</a></li>';
    });
    return h+'</ul>';
  }
  function disegna(){
    if(!map) return;
    layer.clearLayers(); markers={};
    var per={}; visibili().forEach(function(li){ (per[li.dataset.v]=per[li.dataset.v]||[]).push(li); });
    var pts=[];
    Object.keys(per).forEach(function(vk){
      var v=V[vk]; if(!v) return;
      var icon=L.divIcon({className:'',html:'<div class="cal-pin">'+per[vk].length+'</div>',iconSize:[30,30],iconAnchor:[15,15]});
      var mk=L.marker([v.lat,v.lon],{icon:icon,title:v.n+' – '+v.c,keyboard:true}).bindPopup(popup(vk,per[vk]),{maxWidth:300});
      mk.addTo(layer); markers[vk]=mk; pts.push([v.lat,v.lon]);
    });
    if(pts.length===1) map.setView(pts[0],9); else if(pts.length) map.fitBounds(pts,{padding:[40,40],maxZoom:8});
  }
  function caricaMappa(){
    var css=document.createElement('link'); css.rel='stylesheet'; css.href='https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.css'; document.head.appendChild(css);
    var s=document.createElement('script'); s.src='https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.js'; s.async=true;
    s.onload=function(){
      var box=$('#cal-map'); box.innerHTML='';
      // mappa senza servizi esterni: confini dei paesi (Natural Earth, pubblico dominio) ospitati dal sito
      map=L.map(box,{scrollWheelZoom:false,zoomSnap:0.5,minZoom:3,maxZoom:9,maxBounds:[[24,-40],[76,60]],maxBoundsViscosity:0.8,attributionControl:true}).setView([47,9],4);
      map.attributionControl.setPrefix(false).addAttribution('Confini: <a href="https://www.naturalearthdata.com/" target="_blank" rel="noopener">Natural Earth</a>');
      fetch('/assets/data/europa.geojson').then(function(r){return r.json()}).then(function(g){
        L.geoJSON(g,{interactive:false,style:function(f){
          var it=f.properties.n==='Italy';
          return {color:it?'rgba(122,169,255,.75)':'rgba(122,169,255,.32)',weight:it?1.2:0.8,fillColor:it?'#13224a':'#0d1630',fillOpacity:1};
        }}).addTo(map).bringToBack();
      }).catch(function(){});
      layer=L.layerGroup().addTo(map);
      map.on('click',function(){ map.scrollWheelZoom.enable(); });
      disegna();
    };
    s.onerror=function(){ $('#cal-map .ph').textContent='La mappa non si è caricata: trovi tutte le fiere nell’elenco qui sotto.'; };
    document.head.appendChild(s);
  }
  // la mappa si carica appena il riquadro si avvicina allo schermo, e comunque poco dopo l'apertura della pagina
  var box=$('#cal-map'), avviata=false;
  function avvia(){ if(avviata) return; avviata=true; caricaMappa(); }
  if('IntersectionObserver' in window){
    var io=new IntersectionObserver(function(en){ if(en.some(function(x){return x.isIntersecting})){ io.disconnect(); avvia(); } },{rootMargin:'400px'});
    io.observe(box);
  }
  if(document.readyState==='complete') setTimeout(avvia,800); else window.addEventListener('load',function(){ setTimeout(avvia,800); });
  // "Dettagli" dal popup: porta alla riga in elenco e la evidenzia
  document.addEventListener('click',function(e){
    var g=e.target.closest&&e.target.closest('[data-goto]'); if(!g) return;
    e.preventDefault(); var li=document.getElementById('f-'+g.getAttribute('data-goto')); if(!li) return;
    li.scrollIntoView({behavior:'smooth',block:'center'}); li.classList.add('on'); setTimeout(function(){li.classList.remove('on')},2500);
  });
  // passando sopra una riga dell'elenco si apre il punto sulla mappa
  items.forEach(function(li){
    li.addEventListener('mouseenter',function(){ var mk=markers[li.dataset.v]; if(mk&&map&&window.matchMedia('(hover:hover)').matches) mk.openPopup(); });
  });
  // link diretto: /calendario-fiere/?paese=DE&settore=food&mese=2027-03&q=vino
  try{ var u=new URLSearchParams(location.search);
    if(u.get('paese')) fp.value=u.get('paese'); if(u.get('settore')) fs.value=u.get('settore'); if(u.get('mese')) fm.value=u.get('mese'); if(u.get('q')) q.value=u.get('q');
  }catch(_){}
  filtra();
})();
