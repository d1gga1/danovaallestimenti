/* Danova Tech - contatti (15/10/2026)
   1) DTLead.send(): invia le richieste dei moduli direttamente a info@danova-tech.com (FormSubmit, senza server).
      Se l'invio non riesce si apre il programma di posta con il messaggio gia' scritto: nessuna richiesta persa.
   2) Moduli "form.dt-lead" (box contatti in fondo alle pagine).
   3) Barra contatti fissa su smartphone: Chiama / WhatsApp / Scrivici.
   4) Misura i contatti: se e' installato Google Analytics (gtag) registra chiamate, WhatsApp, email e moduli. */
(function(){
  'use strict';
  var MAIL='info@danova-tech.com', WA='393884706887', TEL='+393884706887';
  var ENDPOINT='https://formsubmit.co/ajax/'+MAIL;
  var hl=(document.documentElement.lang||'it').toLowerCase();
  var L=hl.indexOf('zh')===0?'en':hl.slice(0,2); /* le pagine cinesi gestiscono i testi nel loro modulo */
  var TX={
    it:{call:'Chiama',wa:'WhatsApp',write:'Scrivici',sending:'Invio in corso…',ok:'Richiesta inviata! Ti rispondiamo via email al più presto.',
        fail:'Non siamo riusciti a inviare dal sito: si è aperto il tuo programma di posta con il messaggio già pronto, premi invia.',
        e_nome:'Scrivi il tuo nome.',e_mail:'Inserisci un indirizzo email valido.',e_msg:'Scrivici in due righe di cosa hai bisogno.',subj:'Richiesta dal sito'},
    ro:{call:'Sunați',wa:'WhatsApp',write:'Scrieți-ne',sending:'Se trimite…',ok:'Cerere trimisă! Vă răspundem prin e-mail cât mai curând.',fail:'Nu am putut trimite de pe site: s-a deschis aplicația de e-mail cu mesajul pregătit, apăsați trimite.',e_nome:'Introduceți numele.',e_mail:'Introduceți o adresă de e-mail validă.',e_msg:'Spuneți-ne în două rânduri de ce aveți nevoie.',subj:'Cerere de pe site'},
        sq:{call:'Telefononi',wa:'WhatsApp',write:'Na shkruani',sending:'Po dërgohet…',ok:'Kërkesa u dërgua! Do t’ju përgjigjemi me email sa më shpejt.',fail:'Nuk mundëm ta dërgonim nga faqja: u hap aplikacioni i email-it me mesazhin gati, shtypni dërgo.',e_nome:'Shkruani emrin.',e_mail:'Shkruani një adresë email të vlefshme.',e_msg:'Na tregoni në dy rreshta për çfarë keni nevojë.',subj:'Kërkesë nga faqja'},
        hr:{call:'Nazovite',wa:'WhatsApp',write:'Pišite nam',sending:'Šalje se…',ok:'Upit je poslan! Odgovorit ćemo e-mailom što prije.',fail:'Nismo uspjeli poslati sa stranice: otvorila se aplikacija za e-mail s pripremljenom porukom, samo pritisnite pošalji.',e_nome:'Upišite ime.',e_mail:'Upišite ispravnu e-mail adresu.',e_msg:'Recite nam u dva retka što vam treba.',subj:'Upit sa stranice'},
        hi:{call:'कॉल करें',wa:'WhatsApp',write:'लिखें',sending:'भेजा जा रहा है…',ok:'अनुरोध भेज दिया गया! हम जल्द ही ईमेल से जवाब देंगे।',fail:'साइट से भेजा नहीं जा सका: आपका ईमेल ऐप तैयार संदेश के साथ खुल गया है, बस भेजें दबाएँ।',e_nome:'अपना नाम लिखें।',e_mail:'सही ईमेल पता लिखें।',e_msg:'दो लाइनों में बताइए कि आपको क्या चाहिए।',subj:'वेबसाइट से अनुरोध'},
        en:{call:'Call',wa:'WhatsApp',write:'Email us',sending:'Sending…',ok:'Request sent! We will reply by email as soon as possible.',
        fail:'We could not send it from the site: your email app has opened with the message ready, just press send.',
        e_nome:'Please enter your name.',e_mail:'Please enter a valid email address.',e_msg:'Tell us in a couple of lines what you need.',subj:'Website enquiry'},
    de:{call:'Anrufen',wa:'WhatsApp',write:'Schreiben',sending:'Wird gesendet…',ok:'Anfrage gesendet! Wir antworten so schnell wie möglich per E-Mail.',
        fail:'Das Senden über die Website hat nicht geklappt: Ihr E-Mail-Programm ist mit der fertigen Nachricht geöffnet, bitte absenden.',
        e_nome:'Bitte geben Sie Ihren Namen ein.',e_mail:'Bitte geben Sie eine gültige E-Mail-Adresse ein.',e_msg:'Beschreiben Sie kurz, was Sie brauchen.',subj:'Anfrage über die Website'},
    fr:{call:'Appeler',wa:'WhatsApp',write:'Écrire',sending:'Envoi en cours…',ok:'Demande envoyée ! Nous vous répondons par e-mail au plus vite.',
        fail:'L\'envoi depuis le site a échoué : votre messagerie s\'est ouverte avec le message prêt, il suffit de l\'envoyer.',
        e_nome:'Indiquez votre nom.',e_mail:'Indiquez une adresse e-mail valide.',e_msg:'Expliquez-nous en deux lignes ce dont vous avez besoin.',subj:'Demande depuis le site'},
    es:{call:'Llamar',wa:'WhatsApp',write:'Escríbenos',sending:'Enviando…',ok:'¡Solicitud enviada! Te respondemos por email lo antes posible.',
        fail:'No pudimos enviarla desde la web: se ha abierto tu programa de correo con el mensaje listo, solo pulsa enviar.',
        e_nome:'Escribe tu nombre.',e_mail:'Introduce un email válido.',e_msg:'Cuéntanos en dos líneas qué necesitas.',subj:'Solicitud desde la web'}
  };
  var T=TX[L]||TX.en;

  /* 18/10/2026: "Quando vorresti partire?" (pillole) in tutti i moduli. Nell'email il valore arriva sempre in italiano. */
  var URG_IT=['Subito (entro 2 settimane)','Entro un mese','Fra 1 e 3 mesi','Sto solo valutando'];
  var UTX={
    it:{q:'Quando vorresti partire?',o:['Subito, entro 2 settimane','Entro un mese','Fra 1 e 3 mesi','Sto solo valutando'],hot:'Perfetto, mettiamo la tua richiesta in cima alla lista.'},
    ro:{q:'Când ați vrea să începeți?',o:['Imediat, în 2 săptămâni','În decurs de o lună','În 1–3 luni','Doar mă informez'],hot:'Perfect, cererea dvs. ajunge prima pe listă.'},
        sq:{q:'Kur do të donit të fillonit?',o:['Menjëherë, brenda 2 javësh','Brenda një muaji','Për 1 deri në 3 muaj','Thjesht po informohem'],hot:'Shkëlqyeshëm, kërkesa juaj del e para në listë.'},
        hr:{q:'Kada biste željeli početi?',o:['Odmah, u roku od 2 tjedna','U roku od mjesec dana','Za 1 do 3 mjeseca','Samo se informiram'],hot:'Odlično, vaš upit stavljamo na vrh popisa.'},
        hi:{q:'आप कब शुरू करना चाहेंगे?',o:['तुरंत, 2 हफ़्ते में','एक महीने के अंदर','1 से 3 महीने में','बस जानकारी ले रहा/रही हूँ'],hot:'बढ़िया, आपका अनुरोध सूची में सबसे ऊपर जाएगा।'},
        en:{q:'When would you like to start?',o:['Right away, within 2 weeks','Within a month','In 1 to 3 months','Just exploring'],hot:'Great, we will put your request at the top of the list.'},
    de:{q:'Wann möchten Sie starten?',o:['Sofort, in 2 Wochen','Innerhalb eines Monats','In 1 bis 3 Monaten','Ich informiere mich nur'],hot:'Perfekt, Ihre Anfrage kommt ganz nach oben auf die Liste.'},
    fr:{q:'Quand souhaitez-vous démarrer ?',o:['Tout de suite, sous 2 semaines','Dans le mois','Dans 1 à 3 mois','Je me renseigne'],hot:'Parfait, nous mettons votre demande en haut de la liste.'},
    es:{q:'¿Cuándo te gustaría empezar?',o:['Ya, en 2 semanas','En un mes','En 1 a 3 meses','Solo estoy valorando'],hot:'Perfecto, ponemos tu solicitud la primera de la lista.'}
  };
  var lastForm=null;
  document.addEventListener('submit',function(e){ lastForm=e.target; },true);
  function urg(subject, fields){
    var el=lastForm && lastForm.elements && lastForm.elements['urgenza'], u=el?el.value:'';
    if(!u) return [subject, fields];
    var hot=(u===URG_IT[0]);
    return [(hot?'🔥 [SUBITO] ':'['+u+'] ')+subject, [['Quando vuole partire',u]].concat(fields)];
  }

  (function(){ var st=document.createElement('style'); st.id='dt-contatto-css'; st.textContent='.dt-lead{display:grid;gap:12px;max-width:620px;margin:8px auto 0;text-align:left}.dt-lead-2{display:grid;grid-template-columns:1fr 1fr;gap:12px}.dt-lead .btn{justify-content:center;width:100%}.dt-lead .btn[disabled]{opacity:.6}.dt-hp{position:absolute!important;left:-9999px!important;width:1px;height:1px;opacity:0}.dt-lead-msg{display:none;margin:0;font-size:14px}.dt-lead-msg.on{display:block}.dt-lead-msg.err{color:#ff8b98}.dt-lead-msg.ok{color:#8fe3b0}.dt-lead p.form-note,.dt-lead p.dt-lead-msg{max-width:none;margin:4px 0 0;text-align:center}.dt-lead .form-note a[href^=tel]{white-space:nowrap}#dt-scrivi,#richiesta{scroll-margin-top:120px}.dt-lead .form-note a{color:#9fc0ff}.dt-bar{display:none}@media (max-width:760px){.dt-lead-2{grid-template-columns:1fr}.dt-bar{display:grid;grid-template-columns:1fr 1fr 1fr;position:fixed;left:10px;right:10px;bottom:calc(10px + env(safe-area-inset-bottom));z-index:8000;background:rgba(7,11,20,.92);-webkit-backdrop-filter:blur(12px);backdrop-filter:blur(12px);border:1px solid rgba(122,169,255,.28);border-radius:16px;overflow:hidden;box-shadow:0 10px 30px rgba(0,0,0,.45);transition:transform .35s,opacity .35s}.dt-bar.hide{transform:translateY(140%);opacity:0;pointer-events:none}.dt-bar a{display:flex;flex-direction:column;align-items:center;gap:3px;padding:9px 4px 8px;color:#e9edf7;font-size:12px;font-weight:600;text-decoration:none}.dt-bar a+a{border-left:1px solid rgba(255,255,255,.08)}.dt-bar svg{width:20px;height:20px}.dt-bar-call{background:#1E6BFF;color:#fff!important}.dt-bar-wa svg{color:#3ddc84}body.has-dt-bar footer{padding-bottom:84px}body.has-dt-bar #top{bottom:96px}}'; document.head.appendChild(st); })();

  function track(name,params){
    try{ if(window.gtag) window.gtag('event',name,params||{}); }catch(_){}
    try{ if(window.fbq) window.fbq('track','Contact'); }catch(_){}
  }

  /* invio email: fields = [[etichetta, valore], ...] */
  function send(subject, fields, replyTo){
    var _u=urg(subject, fields); subject=_u[0]; fields=_u[1];
    var body={_subject:subject,_template:'table',_captcha:'false'};
    fields.forEach(function(f){ if(f[1]) body[f[0]]=f[1]; });
    var _pg=location.href.split('#')[0];   /* niente doppione se il modulo manda gia' l'indirizzo della pagina */
    if(!fields.some(function(f){ return String(f[1]||'').indexOf(_pg)===0; })) body['Pagina']=_pg;
    if(replyTo) body.email=replyTo;
    return fetch(ENDPOINT,{method:'POST',headers:{'Content-Type':'application/json','Accept':'application/json'},body:JSON.stringify(body)})
      .then(function(r){ return r.json(); })
      .then(function(j){ return j && (j.success===true || j.success==='true'); })
      .catch(function(){ return false; });
  }
  function mailto(subject, fields){
    var _u=urg(subject, fields); subject=_u[0]; fields=_u[1];
    var txt=fields.filter(function(f){return f[1];}).map(function(f){return f[0]+': '+f[1];}).join('\n')+'\n\n'+location.href.split('#')[0];
    location.href='mailto:'+MAIL+'?subject='+encodeURIComponent(subject)+'&body='+encodeURIComponent(txt);
  }
  /* invia, e se fallisce apre la posta. Ritorna una Promise<boolean> (true = arrivata via sito) */
  function deliver(subject, fields, replyTo, form){
    track('generate_lead',{method:'form',form:form||'modulo'});
    return send(subject, fields, replyTo).then(function(ok){ if(!ok) mailto(subject, fields); return ok; });
  }
  window.DTLead={send:send, deliver:deliver, mailto:mailto, T:T, MAIL:MAIL, WA:WA};

  function val(f,n){ var e=f.elements[n]; return e?String(e.value||'').trim():''; }
  var MAILRE=/^[^@\s]+@[^@\s]+\.[^@\s]{2,}$/;

  /* ---- moduli contatti in fondo alle pagine ---- */
  document.querySelectorAll('form.dt-lead').forEach(function(f){
    var out=f.querySelector('.dt-lead-msg'), btn=f.querySelector('button[type=submit]');
    function say(msg,cls){ if(!out) return; out.textContent=msg; out.className='dt-lead-msg on '+(cls||''); }
    f.addEventListener('input',function(e){ if(e.target.classList) e.target.classList.remove('bad'); });
    f.addEventListener('submit',function(e){
      e.preventDefault();
      if(val(f,'_honey')) return;
      var chk=[['nome',T.e_nome,function(v){return v.length>1;}],['email',T.e_mail,function(v){return MAILRE.test(v);}],['msg',T.e_msg,function(v){return v.length>3;}]];
      /* 24/10/2026: telefono obbligatorio dove il campo ha l'attributo required */
      var tel=f.elements['tel'];
      if(tel && tel.required){ var ET={it:'Inserisci un numero di telefono valido.',en:'Please enter a valid phone number.',de:'Bitte geben Sie eine gültige Telefonnummer ein.',ro:'Introduceți un număr de telefon valid.',sq:'Shkruani një numër telefoni të vlefshëm.',hr:'Unesite ispravan broj telefona.',hi:'सही फ़ोन नंबर लिखें।',fr:'Indiquez un numéro de téléphone valide.',es:'Introduce un número de teléfono válido.'};
        chk.splice(2,0,['tel',ET[(document.documentElement.lang||'it').slice(0,2).toLowerCase()]||ET.en,function(v){return v.replace(/\D/g,'').length>=6;}]); }
      for(var i=0;i<chk.length;i++){ var el=f.elements[chk[i][0]]; if(el && !chk[i][2](val(f,chk[i][0]))){ el.classList.add('bad'); el.focus(); say(chk[i][1],'err'); return; } }
      var fields=[['Nome',val(f,'nome')],['Email',val(f,'email')],['Telefono',val(f,'tel')],['Messaggio',val(f,'msg')]];
      var _h1=document.querySelector('h1'); var subj=T.subj+' - '+(_h1?(_h1.innerText||_h1.textContent):'');
      if(btn) btn.disabled=true; say(T.sending,'');
      deliver(subj.replace(/\s+/g,' ').slice(0,140), fields, val(f,'email'), 'contatti_pagina').then(function(ok){
        if(btn) btn.disabled=false;
        if(ok){ say(T.ok,'ok'); f.reset(); } else say(T.fail,'ok');
      });
    });
  });

  /* ---- campo urgenza (pillole) in tutti i moduli ---- */
  (function(){
    var st=document.createElement('style'); st.id='dt-urg-css';
    st.textContent='.dt-urg{margin:4px 0 12px;border:0;padding:0;min-width:0}.dt-urg legend{font-size:13.5px;font-weight:600;color:var(--text,#e9edf7);margin-bottom:10px;padding:0}'+
      '.dt-urg-p{display:flex;flex-wrap:wrap;gap:8px}.dt-urg-p button{border:1px solid var(--line,rgba(255,255,255,.12));background:rgba(255,255,255,.03);color:var(--text,#e9edf7);'+
      'border-radius:999px;padding:9px 15px;font:inherit;font-size:14px;line-height:1.3;cursor:pointer;transition:background .2s,border-color .2s}'+
      '.dt-urg-p button:hover{border-color:var(--line-strong,rgba(255,255,255,.25))}.dt-urg-p button[aria-pressed=true]{background:var(--blue,#1E6BFF);border-color:var(--blue,#1E6BFF);color:#fff}'+
      '.dt-urg-h{font-size:13px;color:#ff7a45;margin-top:8px;min-height:0}.dt-urg-h:empty{display:none}';
    document.head.appendChild(st);
    function lang(){ var h=(document.documentElement.lang||'it').slice(0,2).toLowerCase(); return UTX[h]||UTX.en; }
    function paint(box){
      var t=lang(); box.querySelector('legend').textContent=t.q;
      box.querySelectorAll('button').forEach(function(b,i){ b.textContent=t.o[i]; });
      var h=box.querySelector('.dt-urg-h'); if(h.textContent) h.textContent=t.hot;
    }
    document.querySelectorAll('form.dt-lead, form.fr-req, form#form').forEach(function(f){
      if(f.querySelector('.dt-urg')) return;
      var box=document.createElement('fieldset'); box.className='dt-urg';
      box.innerHTML='<legend></legend><div class="dt-urg-p" role="group"></div><p class="dt-urg-h" aria-live="polite"></p><input type="hidden" name="urgenza" value="">';
      var wrap=box.querySelector('.dt-urg-p'), hid=box.querySelector('input'), hint=box.querySelector('.dt-urg-h');
      URG_IT.forEach(function(v,i){
        var b=document.createElement('button'); b.type='button'; b.setAttribute('aria-pressed','false');
        b.addEventListener('click',function(){
          var on=b.getAttribute('aria-pressed')==='true';
          wrap.querySelectorAll('button').forEach(function(x){ x.setAttribute('aria-pressed','false'); });
          b.setAttribute('aria-pressed', on?'false':'true'); hid.value=on?'':v;
          hint.textContent=(!on && i===0)?lang().hot:'';
          track('urgenza_scelta',{valore:on?'':v});
        });
        wrap.appendChild(b);
      });
      paint(box);
      f.addEventListener('reset',function(){ setTimeout(function(){ hid.value=''; hint.textContent='';
        wrap.querySelectorAll('button').forEach(function(x){ x.setAttribute('aria-pressed','false'); }); },0); });
      var before=f.querySelector('.dt-lead-msg')||f.querySelector('button[type=submit]');
      before.parentNode.insertBefore(box, before);
    });
    /* homepage: se si cambia lingua, cambiano anche le pillole */
    try{ new MutationObserver(function(){ document.querySelectorAll('.dt-urg').forEach(paint); })
      .observe(document.documentElement,{attributes:true,attributeFilter:['lang']}); }catch(_){}
  })();

  /* ---- misura i click su telefono, WhatsApp ed email ---- */
  document.addEventListener('click',function(e){
    var a=e.target.closest&&e.target.closest('a[href]'); if(!a) return;
    var h=a.getAttribute('href')||'';
    if(h.indexOf('tel:')===0) track('generate_lead',{method:'telefono'});
    else if(h.indexOf('wa.me')>-1) track('generate_lead',{method:'whatsapp'});
    else if(h.indexOf('mailto:')===0) track('generate_lead',{method:'email'});
  },true);

  /* ---- barra contatti fissa su smartphone ---- */
  if(!document.querySelector('.dt-bar')){
    var target=document.querySelector('form.dt-lead, form.fr-req, #form');
    var bar=document.createElement('nav');
    bar.className='dt-bar'; bar.setAttribute('aria-label',T.write);
    var ico={
      call:'<path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1.9.4 1.8.7 2.7a2 2 0 0 1-.5 2.1L8 9.8a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.7.7a2 2 0 0 1 1.7 2z"/>',
      wa:'<path d="M21 11.5a8.4 8.4 0 0 1-12.4 7.4L3 21l2.1-5.4A8.4 8.4 0 1 1 21 11.5z"/>',
      write:'<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 6 9-6"/>'};
    function item(href,key,cls,ext){
      return '<a href="'+href+'" class="'+cls+'"'+(ext?' target="_blank" rel="noopener"':'')+'><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'+ico[key]+'</svg><span>'+T[key]+'</span></a>';
    }
    bar.innerHTML=item('tel:'+TEL,'call','dt-bar-call')+item('https://wa.me/'+WA,'wa','dt-bar-wa',true)+
      item(target?'#dt-scrivi':'mailto:'+MAIL,'write','dt-bar-write');
    document.body.appendChild(bar); document.body.classList.add('has-dt-bar');
    if(target){
      bar.querySelector('.dt-bar-write').addEventListener('click',function(e){
        e.preventDefault(); track('generate_lead_click',{method:'scrivici'});
        target.scrollIntoView({behavior:'smooth',block:'center'});
        var first=target.querySelector('input:not([type=hidden]):not(.dt-hp),textarea');
        setTimeout(function(){ if(first) first.focus({preventScroll:true}); },650);
      });
    }
    /* mentre si scrive in un modulo (tastiera aperta) la barra si toglie di mezzo */
    document.addEventListener('focusin',function(e){ if(e.target.closest && e.target.closest('form')) bar.classList.add('hide'); });
    document.addEventListener('focusout',function(){ setTimeout(function(){ var a=document.activeElement; if(!(a && a.closest && a.closest('form'))) bar.classList.remove('hide'); },150); });
    if(false){
    }
  }
})();
