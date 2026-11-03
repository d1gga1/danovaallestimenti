/* Modulo "Richiedi lo stand" delle pagine fiere: prepara il messaggio su WhatsApp (o email).
   Danova Tech, ottobre 2026. 14/10/2026: multilingua (it, en, zh-Hans, zh-Hant) e apertura di WhatsApp
   in una sola scheda (prima, con 'noopener', window.open restituiva null e non c'era ripiego se il popup era bloccato). */
(function(){
  var WA='393884706887', MAIL='info@danova-tech.com';
  var L=(document.documentElement.lang||'it').toLowerCase();
  L = L.indexOf('zh-hant')===0 ? 'zht' : L.indexOf('zh')===0 ? 'zh' : L.indexOf('en')===0 ? 'en' : 'it';
  var T={
    it:{head:'Richiesta stand dal sito danova-tech.com',fiera:'Fiera',mq:'Metri quadri',spazio:'Tipo di spazio',nome:'Nome',azienda:'Azienda',tel:'Telefono',note:'Note',pagina:'Pagina',subj:'Richiesta stand: ',
        e_fiera:'Indica la fiera a cui partecipi.',e_nome:'Inserisci nome e cognome.',e_azienda:"Inserisci il nome dell'azienda.",e_tel:'Inserisci un numero di telefono.',
        e_tel2:'Il numero di telefono sembra incompleto.',e_mail:"L'email non sembra valida: correggila o lascia il campo vuoto.",
        ok:'Richiesta inviata! Ti ricontattiamo al più presto con le prime idee e un preventivo.'},
    en:{head:'Stand request from danova-tech.com',fiera:'Fair',mq:'Square metres',spazio:'Type of space',nome:'Name',azienda:'Company',tel:'Phone',note:'Notes',pagina:'Page',subj:'Stand request: ',
        e_fiera:'Please enter the fair you are exhibiting at.',e_nome:'Please enter your name.',e_azienda:'Please enter your company name.',e_tel:'Please enter a phone number.',
        e_tel2:'The phone number looks incomplete.',e_mail:'The email does not look valid: correct it or leave it empty.',
        ok:'Request sent! We will get back to you shortly with first ideas and a quote.'},
    zh:{head:'Stand request from danova-tech.com (中文页面)',fiera:'Fair / 展会',mq:'m² / 面积',spazio:'Space / 展位类型',nome:'Name / 姓名',azienda:'Company / 公司',tel:'Phone / 电话',note:'Notes / 备注',pagina:'Page',subj:'展台询价 Stand request: ',
        e_fiera:'请填写您参加的展会。',e_nome:'请填写您的姓名。',e_azienda:'请填写公司名称。',e_tel:'请填写电话号码。',
        e_tel2:'电话号码似乎不完整。',e_mail:'邮箱格式不正确：请修改或留空。',
        ok:'询价已发送！我们会尽快通过邮件或电话与您联系。'},
    zht:{head:'Stand request from danova-tech.com (繁體中文頁面)',fiera:'Fair / 展會',mq:'m² / 面積',spazio:'Space / 展位類型',nome:'Name / 姓名',azienda:'Company / 公司',tel:'Phone / 電話',note:'Notes / 備註',pagina:'Page',subj:'展臺詢價 Stand request: ',
        e_fiera:'請填寫您參加的展會。',e_nome:'請填寫您的姓名。',e_azienda:'請填寫公司名稱。',e_tel:'請填寫電話號碼。',
        e_tel2:'電話號碼似乎不完整。',e_mail:'郵箱格式不正確：請修改或留空。',
        ok:'詢價已發送！我們會盡快通過郵件或電話與您聯繫。'}
  }[L];
  function val(f,n){var e=f.elements[n];return e?String(e.value||'').trim():'';}
  function testo(f){
    var r=[T.head,'',T.fiera+': '+val(f,'fiera')];
    if(val(f,'mq')) r.push(T.mq+': '+val(f,'mq'));
    if(val(f,'spazio')) r.push(T.spazio+': '+val(f,'spazio'));
    r.push(T.nome+': '+val(f,'nome'),T.azienda+': '+val(f,'azienda'),T.tel+': '+val(f,'tel'));
    if(val(f,'email')) r.push('Email: '+val(f,'email'));
    if(val(f,'note')) r.push('',T.note+': '+val(f,'note'));
    r.push('',T.pagina+': '+location.href.split('#')[0]);
    return r.join('\n');
  }
  function aggiornaMail(f){
    var w=f.querySelector('.fr-req-wa'); if(w) w.href='https://wa.me/'+WA+'?text='+encodeURIComponent(testo(f));
    var a=f.querySelector('.fr-req-mail'); if(!a) return;
    a.href='mailto:'+MAIL+'?subject='+encodeURIComponent(T.subj+(val(f,'fiera')||''))+'&body='+encodeURIComponent(testo(f));
  }
  function errore(f,msg,el){
    var p=f.querySelector('.fr-req-err'); if(p){p.textContent=msg;p.classList.remove('ok');p.classList.add('on');}
    if(el){el.classList.add('bad');el.focus();}
  }
  function apri(url){
    var w=null; try{ w=window.open(url,'_blank'); }catch(_){}
    if(w){ try{ w.opener=null; }catch(_){} } else { location.href=url; }
  }
  document.querySelectorAll('form.fr-req').forEach(function(f){
    f.addEventListener('input',function(e){if(e.target.classList)e.target.classList.remove('bad');var p=f.querySelector('.fr-req-err');if(p)p.classList.remove('on');aggiornaMail(f);});
    f.addEventListener('change',function(){aggiornaMail(f);});
    aggiornaMail(f);
    f.addEventListener('submit',function(e){
      e.preventDefault();
      var req=[['fiera',T.e_fiera],['nome',T.e_nome],['azienda',T.e_azienda],['tel',T.e_tel]];
      for(var i=0;i<req.length;i++){ if(!val(f,req[i][0])) return errore(f,req[i][1],f.elements[req[i][0]]); }
      if(val(f,'tel').replace(/\D/g,'').length<6) return errore(f,T.e_tel2,f.elements.tel);
      var em=val(f,'email'); if(em && !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(em)) return errore(f,T.e_mail,f.elements.email);
      try{ if(window.gtag) gtag('event','generate_lead',{method:'form',form:'richiesta_stand',fiera:val(f,'fiera'),lingua:L}); }catch(_){}
      var p=f.querySelector('.fr-req-err');
      /* 15/10/2026: la richiesta arriva direttamente via email (contatto.js); se non riesce, WhatsApp come prima */
      if(window.DTLead){
        var b=f.querySelector('button[type=submit]'); if(b) b.disabled=true;
        var campi=testo(f).split('\n').filter(function(r){return r.indexOf(': ')>0;}).map(function(r){var i=r.indexOf(': ');return [r.slice(0,i),r.slice(i+2)];});
        window.DTLead.send(T.subj+(val(f,'fiera')||''),campi,val(f,'email')).then(function(ok){
          if(b) b.disabled=false;
          if(ok){ if(p){p.textContent=T.ok;p.classList.add('on','ok');} f.reset(); }
          else apri('https://wa.me/'+WA+'?text='+encodeURIComponent(testo(f)));
        });
        return;
      }
      if(p){p.textContent=T.ok;p.classList.add('on','ok');}
      apri('https://wa.me/'+WA+'?text='+encodeURIComponent(testo(f)));
    });
  });
  /* pulsanti "Richiedi lo stand" (calendario e schede): compilano il modulo e ci portano li' */
  function compila(nome){
    var f=document.querySelector('form.fr-req'); if(!f) return false;
    f.elements.fiera.value=nome; aggiornaMail(f);
    var sec=f.closest('section')||f; sec.scrollIntoView({behavior:'smooth',block:'start'});
    setTimeout(function(){ (f.elements.mq||f.elements.nome).focus({preventScroll:true}); },600);
    return true;
  }
  window.frRichiedi=compila;
  document.addEventListener('click',function(e){
    var b=e.target.closest&&e.target.closest('[data-req]'); if(!b) return;
    if(compila(b.getAttribute('data-req'))) e.preventDefault();
  });
  try{ var q=new URLSearchParams(location.search).get('fiera'); if(q){ var f=document.querySelector('form.fr-req'); if(f&&!f.elements.fiera.value){f.elements.fiera.value=q.slice(0,120);aggiornaMail(f);} } }catch(_){}
})();
