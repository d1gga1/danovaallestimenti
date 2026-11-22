/* Danova — statistiche visite per l'area privata danovastand.com/private_area/ (solo uso interno).
   STESSO FILE su danovastand.com, danovacostruzioni.it e danova-tech.com: il sito si riconosce dal dominio.
   Stesso sistema di pandooragroup.it (pd-live.js), con database Supabase e funzione "ds".
   Per tutti: conteggi anonimi (pagine viste, provenienza, dispositivo, zona approssimativa; nessun indirizzo IP salvato).
   Solo per chi accetta il banner: clic, sezioni lette, moduli iniziati / inviati / lasciati a metà (mai quello che si scrive).
   Le richieste inviate dai moduli (FormSubmit) vengono copiate anche nel database: scheda "Richieste" della dashboard.
   Per escludere il proprio browser dalle statistiche: aprire una volta danovastand.com/?dslive=no
   Per riaprire la scelta dei cookie: link con href="#cookie" oppure window.dsCookie(). */
(function () {
  if (window.__dsLive) return; window.__dsLive = 1;
  try { if (window.top !== window.self) return; } catch (e) { return; }   // non contare le pagine dentro un iframe
  var BASE = window.DS_LIVE_BASE || 'https://hqodsztwzcofdsunnpxa.supabase.co/functions/v1/ds';   // impostato da strumenti/attiva-area-privata.py
  if (/TUO-PROGETTO/.test(BASE)) return;   // area privata non ancora collegata a Supabase: non si fa nulla
  var URL_ = BASE + '/s';
  var LS = null; try { LS = window.localStorage; LS.setItem('ds_t', '1'); LS.removeItem('ds_t'); } catch (e) { LS = null; }
  var get = function (k) { try { return LS ? LS.getItem(k) : null; } catch (e) { return null; } };
  var set = function (k, v) { try { if (LS) LS.setItem(k, v); } catch (e) {} };
  var del = function (k) { try { if (LS) LS.removeItem(k); } catch (e) {} };

  var q = location.search;
  if (/[?&]dslive=no\b/.test(q)) set('ds_live_off', '1');
  if (/[?&]dslive=si\b/.test(q)) del('ds_live_off');
  if (get('ds_live_off') || navigator.webdriver) return;
  var SITI = { 'danovastand.com': 'stand', 'danovacostruzioni.it': 'costruzioni', 'danova-tech.com': 'tech' };
  var NOMI = { stand: 'Danova Stand', costruzioni: 'Danova Costruzioni', tech: 'Danova Tech' };
  var DOMINIO = location.hostname.replace(/^www\./, '');
  var SITO = window.DS_SITO || SITI[DOMINIO] || '';
  if (!SITO || (!window.DS_LIVE_BASE && !SITI[DOMINIO])) return;   // niente statistiche in locale o in anteprima
  var NOME = NOMI[SITO];

  var rid = function () {
    var a = new Uint8Array(12);
    (window.crypto || window.msCrypto).getRandomValues(a);
    return Array.prototype.map.call(a, function (b) { return ('0' + b.toString(16)).slice(-2); }).join('');
  };
  var ora = function () { return Date.now(); };
  var MAX_PAUSA = 30 * 60 * 1000;   // dopo 30 minuti di inattività inizia una nuova visita

  var vid = get('ds_v'); if (!vid || !/^[a-z0-9]{12,40}$/.test(vid)) { vid = rid(); set('ds_v', vid); }
  var vn = parseInt(get('ds_vn') || '0', 10) || 0;
  window.dsVisitatore = function () { return vid; };
  /* codice breve del visitatore ("Rif."): finisce nei messaggi WhatsApp, così in dashboard sapete chi vi sta scrivendo */
  var rif = function () { return vid.slice(0, 6).toUpperCase(); };
  window.dsRif = rif;
  var LG = String(document.documentElement.lang || 'it').slice(0, 2).toLowerCase();
  var conRif = function (u) {
    try {
      u = String(u); var r = rif();
      if (u.indexOf(r) >= 0 || !/^(https?:\/\/(wa\.me|api\.whatsapp\.com|web\.whatsapp\.com)\/|whatsapp:)/i.test(u)) return u;
      var m = /([?&])text=([^&#]*)/.exec(u), tx = '';
      if (m) { try { tx = decodeURIComponent(m[2].replace(/\+/g, ' ')); } catch (e) { tx = m[2]; } }
      var ini = { it: 'Ciao ' + NOME + '! Vi scrivo dal sito ' + DOMINIO + '.', de: 'Hallo ' + NOME + '! Ich schreibe Ihnen über ' + DOMINIO + '.', fr: 'Bonjour ' + NOME + ' ! Je vous écris depuis ' + DOMINIO + '.', es: '¡Hola ' + NOME + '! Os escribo desde ' + DOMINIO + '.' }[LG] || 'Hello ' + NOME + '! I am writing from ' + DOMINIO + '.';
      var nuovo = encodeURIComponent((tx || ini) + '\n\n' + (LG === 'it' ? 'Rif. ' : 'Ref. ') + r);
      if (m) return u.slice(0, m.index) + m[1] + 'text=' + nuovo + u.slice(m.index + m[0].length);
      var h = u.indexOf('#'), coda = h >= 0 ? u.slice(h) : ''; if (h >= 0) u = u.slice(0, h);
      return u + (u.indexOf('?') >= 0 ? '&' : '?') + 'text=' + nuovo + coda;
    } catch (e) { return u; }
  };
  window.dsConRif = conRif;
  var sess = null; try { sess = JSON.parse(get('ds_s') || 'null'); } catch (e) {}
  var nuovaVisita = !sess || !sess.id || ora() - (sess.t || 0) > MAX_PAUSA;
  if (nuovaVisita) { sess = { id: rid(), t: ora() }; vn += 1; set('ds_vn', String(vn)); }
  var tocca = function () { sess.t = ora(); set('ds_s', JSON.stringify(sess)); };
  tocca();

  var percorso = function () {
    var p = location.pathname || '/';
    var m = /[?&]p=([^&#]{1,80})/.exec(location.search);   // prodotto aperto nello shop
    return m ? p + '?p=' + m[1] : p;
  };
  var invia = function (e, extra) {
    var d = { e: e, si: SITO, v: vid, s: sess.id, p: percorso(), t: (document.title || '').slice(0, 200) };
    if (extra) for (var k in extra) d[k] = extra[k];
    var body = JSON.stringify(d);
    try {
      if (navigator.sendBeacon && navigator.sendBeacon(URL_, new Blob([body], { type: 'text/plain' }))) return;
    } catch (x) {}
    try { fetch(URL_, { method: 'POST', body: body, mode: 'no-cors', keepalive: true, headers: { 'Content-Type': 'text/plain' } }); } catch (x) {}
  };

  /* pagina vista */
  var ref = document.referrer || '';
  try { if (ref && new URL(ref).hostname.replace(/^www\./, '') === location.hostname.replace(/^www\./, '')) ref = ''; } catch (e) {}
  var utm = {};
  var par = function (k) { var m = new RegExp('[?&]' + k + '=([^&#]*)').exec(location.search); return m ? decodeURIComponent(m[1].replace(/\+/g, ' ')).slice(0, 80) : ''; };
  if (par('utm_source')) utm.s = par('utm_source');
  if (par('utm_medium')) utm.m = par('utm_medium');
  if (par('utm_campaign')) utm.c = par('utm_campaign');
  if (par('utm_term')) utm.t = par('utm_term');
  if (par('gclid') || par('gbraid') || par('wbraid')) utm.g = 1;
  if (par('fbclid')) utm.f = 1;
  var dati = function () { // dispositivo e browser (nessun dato personale)
    var d = { w: screen.width || 0, l: navigator.language || '' };
    try { d.tz = Intl.DateTimeFormat().resolvedOptions().timeZone || ''; } catch (e) {}
    d.sch = (screen.width || 0) + 'x' + (screen.height || 0);
    d.fin = (innerWidth || 0) + 'x' + (innerHeight || 0);
    d.dpr = Math.round((devicePixelRatio || 1) * 100) / 100;
    d.tc = (navigator.maxTouchPoints || 0) > 0 ? 1 : 0;
    var c = navigator.connection; if (c && c.effectiveType) d.cn = c.effectiveType;
    if (navigator.deviceMemory) d.mem = navigator.deviceMemory;
    if (navigator.hardwareConcurrency) d.cpu = navigator.hardwareConcurrency;
    try { d.dk = matchMedia('(prefers-color-scheme: dark)').matches ? 1 : 0; } catch (e) {}
    d.ls = (navigator.languages || []).slice(0, 4).join(',');
    return d;
  };
  var primo = { n: nuovaVisita ? 1 : 0, k: vn, r: nuovaVisita ? ref.slice(0, 400) : '', u: nuovaVisita ? utm : {} };
  var dd = dati(); for (var x in dd) primo[x] = dd[x];
  var partito = false, parti = function () { if (partito) return; partito = true; invia('pv', primo); };
  try {
    var uad = navigator.userAgentData;
    if (uad && uad.getHighEntropyValues) {
      uad.getHighEntropyValues(['model', 'platformVersion']).then(function (h) { if (h.model) primo.mo = h.model; if (h.platformVersion) primo.ov = h.platformVersion; parti(); }, parti);
      setTimeout(parti, 400);
    } else {
      var mi = /iPhone|iPad|iPod/.exec(navigator.userAgent); if (mi) primo.mo = mi[0];
      var vi = /OS (\d+)[_.](\d+)/.exec(navigator.userAgent) || /Mac OS X (\d+)[_.](\d+)/.exec(navigator.userAgent); if (vi) primo.ov = vi[1] + '.' + vi[2];
      parti();
    }
  } catch (e) { parti(); }

  /* quanto della pagina è stato letto (scroll massimo in %) */
  var scrollMax = 0;
  var misuraScroll = function () {
    var h = Math.max(document.documentElement.scrollHeight, document.body ? document.body.scrollHeight : 0) - innerHeight;
    var p = h > 0 ? Math.round(Math.min(1, (scrollY || pageYOffset || 0) / h) * 100) : 100;
    if (p > scrollMax) scrollMax = p;
  };
  addEventListener('scroll', function () { misuraScroll(); }, { passive: true });
  setTimeout(misuraScroll, 1500);

  /* azioni: clic su WhatsApp, telefono, email (e altri eventi mandati dal sito con window.dsEvento) */
  window.dsEvento = function (tipo, dettaglio) { try { tocca(); invia('ev', { k: String(tipo), x: String(dettaglio || '').slice(0, 200) }); } catch (e) {} };
  var tipoLink = function (href) {
    if (/^(https?:)?\/\/(wa\.me|api\.whatsapp\.com|web\.whatsapp\.com|chat\.whatsapp\.com)\//i.test(href) || /^whatsapp:/i.test(href)) return 'whatsapp';
    if (/^tel:/i.test(href)) return 'telefono';
    if (/^mailto:/i.test(href)) return 'email';
    if (/\.pdf(\?|#|$)/i.test(href)) return 'download';
    if (/(^|\/)(preventivo|contatti|contact|kontakt|contacto|prezzi|preise)(\/|\.html|$|\?|#)/i.test(href) || /#(richiesta|dt-scrivi)$/.test(href)) return 'preventivo';
    try { var u = new URL(href, location.href); if (/^https?:$/.test(u.protocol) && u.hostname.replace(/^www\./, '') !== location.hostname.replace(/^www\./, '')) return 'esterno'; } catch (e) {}
    return '';
  };
  document.addEventListener('click', function (e) {
    var a = e.target && e.target.closest ? e.target.closest('a[href]') : null;
    if (!a) return;
    var href = a.getAttribute('href') || '', tipo = tipoLink(href);
    if (!tipo) return;
    if (tipo === 'whatsapp') { var hr = conRif(href); if (hr !== href) { a.setAttribute('href', hr); href = hr; } }
    var testo = (a.getAttribute('aria-label') || a.textContent || '').replace(/\s+/g, ' ').trim();
    if (!testo && a.className) testo = String(a.className);
    if (tipo === 'esterno') testo = (testo ? testo.slice(0, 60) + ' · ' : '') + href.replace(/^https?:\/\//, '').slice(0, 80);
    window.dsEvento(tipo, (testo || href).slice(0, 120) + (tipo === 'download' ? ' · ' + href.split('/').pop() : '') + (tipo === 'whatsapp' ? ' · Rif. ' + rif() : ''));
  }, true);

  /* ricerche fatte nel sito (barra di ricerca dello shop) */
  var ultimaRicerca = '', tRic = null;
  var registraRicerca = function (el) {
    var v = String(el.value || '').trim().replace(/\s+/g, ' ');
    if (v.length < 2 || v.toLowerCase() === ultimaRicerca) return;
    ultimaRicerca = v.toLowerCase(); window.dsEvento('ricerca', v.slice(0, 80));
  };
  var eRicerca = function (el) { return el && el.tagName === 'INPUT' && (el.type === 'search' || el.name === 'q' || /cerca/i.test(el.placeholder || '')); };
  document.addEventListener('input', function (e) { if (!eRicerca(e.target)) return; clearTimeout(tRic); var el = e.target; tRic = setTimeout(function () { registraRicerca(el); }, 1800); }, true);
  document.addEventListener('keydown', function (e) { if (e.key === 'Enter' && eRicerca(e.target)) { clearTimeout(tRic); registraRicerca(e.target); } }, true);

  /* chi copia il vostro numero o la vostra email */
  document.addEventListener('copy', function () {
    try {
      var s = String(getSelection() || '').trim();
      if (s && s.length < 120 && (/(\+?\d[\d\s.\-]{7,}\d)/.test(s) || /@/.test(s))) window.dsEvento('copia', s.slice(0, 80));
    } catch (e) {}
  }, true);
  if (window.open) { // WhatsApp aperto dal codice (es. "invia l'ordine su WhatsApp")
    var apri = window.open;
    window.open = function (u) {
      var arg = Array.prototype.slice.call(arguments);
      try { if (u && tipoLink(String(u)) === 'whatsapp') { arg[0] = conRif(u); window.dsEvento('whatsapp', 'apertura da pulsante · Rif. ' + rif()); } } catch (e) {}
      return apri.apply(window, arg);
    };
  }

  /* prodotti aperti nello shop (cambiano l'indirizzo senza ricaricare la pagina) */
  var ultimo = percorso();
  ['pushState', 'replaceState'].forEach(function (f) {
    var orig = history[f]; if (!orig) return;
    history[f] = function () { var r = orig.apply(this, arguments); var p = percorso(); if (p !== ultimo) { ultimo = p; scrollMax = 0; tocca(); invia('pv', { k: vn }); setTimeout(misuraScroll, 1500); } return r; };
  });

  /* "sono ancora qui": ogni 15 secondi, solo con la pagina in primo piano e se la persona non è inattiva da più di 10 minuti */
  var attivita = ora();
  ['pointerdown', 'keydown', 'scroll', 'mousemove', 'touchstart'].forEach(function (ev) {
    addEventListener(ev, function () { attivita = ora(); }, { passive: true, capture: true });
  });
  setInterval(function () {
    if (document.visibilityState !== 'visible' || ora() - attivita > 10 * 60 * 1000) return;
    misuraScroll(); tocca(); invia('hb', { sc: scrollMax });
  }, 15000);
  document.addEventListener('visibilitychange', function () {
    if (document.visibilityState === 'hidden') { misuraScroll(); invia('bye', { sc: scrollMax }); }
    else if (ora() - sess.t > MAX_PAUSA) {   // tornati dopo una lunga pausa: è una nuova visita
      sess = { id: rid(), t: ora() }; vn += 1; set('ds_vn', String(vn)); tocca(); attivita = ora();
      invia('pv', { n: 1, k: vn, r: '', u: {}, w: screen.width || 0, l: navigator.language || '' });
    } else { attivita = ora(); tocca(); invia('hb'); }
  });
  addEventListener('pagehide', function () { misuraScroll(); invia('bye', { sc: scrollMax }); });

  /* ───────── statistiche dettagliate: SOLO per chi ha accettato il banner (in fondo a questo file, chiave ds_consent) ─────────
     ogni clic, sezioni lette, scelte nei configuratori, carrello, moduli iniziati / inviati / abbandonati.
     Nei moduli NON si registra mai cosa viene scritto nei campi di testo: solo quali campi sono stati compilati. */
  var consenso = function () {
    try { var c = JSON.parse(localStorage.getItem('ds_consent') || 'null'); return !!(c && c.v === 1 && c.s === 'granted' && Date.now() - c.t < 180 * 864e5); } catch (e) { return false; }
  };
  var dett = function (tipo, x) {
    if (!consenso()) return;
    try { tocca(); invia('ev', { k: tipo, x: String(x || '').replace(/\s+/g, ' ').trim().slice(0, 200), c: 1 }); } catch (e) {}
  };
  window.dsDettaglio = dett;
  var pulito = function (s, max) { return String(s || '').replace(/\s+/g, ' ').trim().slice(0, max || 80); };
  var testoLabel = function (lb) { // testo dell'etichetta senza il contenuto dei campi che contiene
    try { var c = lb.cloneNode(true); var x = c.querySelectorAll('input,textarea,select,button,svg'); for (var i = 0; i < x.length; i++) x[i].parentNode.removeChild(x[i]); return pulito(c.textContent, 60); } catch (e) { return ''; }
  };
  var etichettaCampo = function (el) {
    var l = '';
    try { if (el.labels && el.labels[0]) l = testoLabel(el.labels[0]); } catch (e) {}
    if (!l) { var lb = el.closest && el.closest('label'); if (lb) l = testoLabel(lb); }
    return pulito(l || el.getAttribute('aria-label') || el.getAttribute('placeholder') || el.name || el.type || 'campo', 60);
  };
  var campoPrivato = function (el) { // campi in cui la persona scrive: mai il contenuto
    if (!el || !el.tagName) return false;
    if (el.tagName === 'TEXTAREA' || el.isContentEditable) return true;
    if (el.tagName !== 'INPUT') return false;
    var ty = (el.type || 'text').toLowerCase();
    if (/^(text|email|tel|password|search|url|date|datetime-local|month|week|time|file)$/.test(ty)) return true;
    if (ty === 'number') { var f = el.form || (el.closest && el.closest('form')); return !!(f && f.querySelector('input[type=email],input[type=tel],input[type=password]')); }
    return false;
  };
  var testoDi = function (el) {
    var s = el.getAttribute('aria-label') || el.getAttribute('title') || (el.tagName === 'IMG' ? el.getAttribute('alt') : '') || '';
    if (!s && el.tagName === 'INPUT') s = (el.type === 'checkbox' || el.type === 'radio') ? etichettaCampo(el) : el.value;
    if (!s) s = el.innerText || el.textContent || '';
    s = pulito(s);
    if (!s && el.querySelector) { var im = el.querySelector('img[alt]'); if (im) s = 'foto ' + pulito(im.getAttribute('alt')); }
    return s;
  };
  var zona = function (el) {
    var z = [['header', 'intestazione'], ['nav', 'menu'], ['footer', 'fondo pagina'], ['[role=dialog],[class*="modal"],[class*="-m-c"]', 'finestra'], ['[class*="cart"],[class*="carrell"]', 'carrello'], ['[class*="gallery"],[class*="galler"],[class*="thumb"]', 'galleria'], ['[class*="filt"]', 'filtri']];
    for (var i = 0; i < z.length; i++) { try { if (el.closest(z[i][0])) return z[i][1]; } catch (e) {} }
    return '';
  };

  /* ogni clic */
  var ultimoClic = '', tClic = 0, nClic = 0;
  document.addEventListener('click', function (e) {
    if (nClic > 400 || !consenso()) return;
    var el = e.target && e.target.closest ? e.target.closest('a[href],button,summary,label,[role=button],[role=tab],[role=link],[role=menuitem],input[type=checkbox],input[type=radio],input[type=submit],input[type=button],img,video,[onclick],[data-p],[data-id]') : null;
    if (!el || el.closest('[aria-label="Cookie"]')) return;
    if (el.tagName === 'A' && tipoLink(el.getAttribute('href') || '')) return;   // WhatsApp, telefono, email, PDF…: già registrati sopra
    if (el.tagName === 'LABEL') { var ci = el.querySelector('input,select,textarea') || (el.htmlFor && document.getElementById(el.htmlFor)); if (!ci || campoPrivato(ci) || ci.tagName === 'SELECT') return; el = ci; }
    if (campoPrivato(el)) return;
    var cosa = el.tagName === 'A' ? 'Link' : el.tagName === 'IMG' ? 'Foto' : el.tagName === 'VIDEO' ? 'Video' : el.tagName === 'SUMMARY' ? 'Apre' : (el.type === 'checkbox' || el.type === 'radio') ? 'Opzione' : 'Pulsante';
    var tx = testoDi(el), dove = '';
    if (el.tagName === 'A') { var h = el.getAttribute('href') || ''; if (h && h.charAt(0) !== '#' && !/^javascript:/i.test(h)) dove = ' → ' + h.replace(/^https?:\/\/[^/]+/i, function (o) { return o.replace(/^https?:\/\/(www\.)?/i, '') === DOMINIO ? '' : o; }).slice(0, 90); }
    if (el.type === 'checkbox') tx += el.checked ? ' (sì)' : ' (no)';
    var z = zona(el), d = cosa + (tx ? ' «' + tx + '»' : '') + dove + (z ? ' · ' + z : '');
    var adesso = ora(); if (d === ultimoClic && adesso - tClic < 1500) return;
    ultimoClic = d; tClic = adesso; nClic++;
    dett('clic', d);
  }, true);

  /* scelte nei configuratori e nei menu (misure, finiture, quantità…): mai i campi di testo */
  document.addEventListener('change', function (e) {
    var el = e.target; if (!el || !el.tagName || !consenso() || campoPrivato(el)) return;
    if (el.closest && el.closest('[aria-label="Cookie"]')) return;
    var nome = etichettaCampo(el), v;
    if (el.tagName === 'SELECT') v = (el.options[el.selectedIndex] || {}).text || el.value;
    else if (el.type === 'checkbox') v = el.checked ? 'sì' : 'no';
    else if (el.type === 'radio') { if (!el.checked) return; var fs = el.closest('fieldset'), lg = fs && fs.querySelector('legend'); v = nome; nome = lg ? pulito(lg.textContent, 60) : (el.name || 'scelta'); }
    else if (el.tagName === 'INPUT') v = el.value;
    else return;
    if (/^(sito_web|privacy)$/.test(el.name || '')) return;
    dett('scelta', nome + ': ' + pulito(v, 80));
  }, true);

  /* moduli: iniziati, inviati, errori, lasciati a metà */
  var moduli = [];
  var nomeModulo = function (f) {
    var s = f.getAttribute('aria-label') || f.getAttribute('name') || '';
    if (!s) { var c = f.closest('[role=dialog],section,article,.pa-m-c,main') || f.parentNode, h = c && c.querySelector('h1,h2,h3'); if (h) s = h.textContent; }
    if (!s) { var b = f.querySelector('button[type=submit],input[type=submit]'); if (b) s = b.textContent || b.value; }
    return pulito(s || 'modulo', 60);
  };
  var statoModulo = function (f) {
    for (var i = 0; i < moduli.length; i++) if (moduli[i].f === f) return moduli[i];
    var m = { f: f, nome: nomeModulo(f), campi: {}, ultimo: '', avviato: false, inviato: false, segnalato: false, pagina: percorso() };
    moduli.push(m); return m;
  };
  var campoModulo = function (el) {
    if (!el || !/^(INPUT|TEXTAREA|SELECT)$/.test(el.tagName) || /^(hidden|submit|button)$/i.test(el.type || '')) return null;
    if (eRicerca(el) || /trap/.test(el.className || '') || el.name === 'sito_web') return null;
    return el.form || (el.closest && el.closest('form'));
  };
  document.addEventListener('focusin', function (e) {
    var f = campoModulo(e.target); if (!f || !consenso()) return;
    var m = statoModulo(f); m.ultimo = etichettaCampo(e.target);
    if (!m.avviato) { m.avviato = true; m.segnalato = false; dett('modulo', 'Iniziato: ' + m.nome); }
  }, true);
  document.addEventListener('input', function (e) {
    var f = campoModulo(e.target); if (!f) return;
    var m = statoModulo(f), k = etichettaCampo(e.target), v = e.target.type === 'checkbox' ? e.target.checked : String(e.target.value || '').trim();
    if (v) m.campi[k] = 1; else delete m.campi[k];
  }, true);
  document.addEventListener('submit', function (e) {
    var f = e.target; if (!f || f.tagName !== 'FORM' || !consenso()) return;
    if (f.querySelector('input[type=search]') && !f.querySelector('input[type=email],input[type=tel]')) return;
    var m = statoModulo(f), nc = Object.keys(m.campi).length;
    m.inviato = true;
    dett('modulo', 'Inviato: ' + m.nome + ' · ' + nc + ' campi compilati');
    setTimeout(function () { // il sito ha segnalato errori? (campi evidenziati o messaggio d'errore)
      if (!document.contains(f)) return;
      var err = f.querySelectorAll('.err,[aria-invalid="true"]'), nomi = [];
      for (var i = 0; i < err.length && nomi.length < 6; i++) if (/^(INPUT|TEXTAREA|SELECT)$/.test(err[i].tagName)) nomi.push(etichettaCampo(err[i]));
      var msg = f.querySelector('.pa-msg:not(.ok),[role=alert]:not(.ok)'), mt = msg ? pulito(msg.textContent, 100) : '';
      if (nomi.length || mt) { m.inviato = false; dett('modulo', 'Errore in: ' + m.nome + (nomi.length ? ' · campi: ' + nomi.join(', ') : '') + (mt ? ' · «' + mt + '»' : '')); }
    }, 2500);
  }, true);
  var abbandoni = function (tutti) {
    if (!consenso()) return;
    moduli.forEach(function (m) {
      if (!m.avviato || m.inviato || m.segnalato) return;
      if (!tutti && document.contains(m.f)) return;   // ancora aperto: aspettiamo
      m.segnalato = true;
      var c = Object.keys(m.campi);
      dett('modulo', 'Lasciato a metà: ' + m.nome + ' · compilati ' + c.length + (c.length ? ' (' + c.slice(0, 8).join(', ') + ')' : '') + (m.ultimo ? ' · ultimo campo: ' + m.ultimo : ''));
    });
  };

  /* sezioni lette: titoli (h2) rimasti visibili almeno 2 secondi */
  var visteSez = {}, nSez = 0, io = null;
  var osservaSezioni = function () {
    if (!window.IntersectionObserver || !consenso()) return;
    io = io || new IntersectionObserver(function (ents) {
      ents.forEach(function (en) {
        var el = en.target;
        if (en.isIntersecting) el.__pdT = setTimeout(function () {
          var tx = pulito(el.textContent, 90), k = percorso() + '|' + tx;
          if (tx && !visteSez[k] && nSez < 300) { visteSez[k] = 1; nSez++; dett('sezione', tx); }
        }, 2000);
        else clearTimeout(el.__pdT);
      });
    }, { threshold: 0.6 });
    var hs = document.querySelectorAll('h2');
    for (var i = 0; i < hs.length; i++) if (!hs[i].__pdO && !hs[i].closest('[aria-label="Cookie"]')) { hs[i].__pdO = 1; io.observe(hs[i]); }
  };
  setTimeout(osservaSezioni, 1200);
  setInterval(function () { osservaSezioni(); abbandoni(false); }, 10000);
  document.addEventListener('visibilitychange', function () { if (document.visibilityState === 'hidden') abbandoni(true); });
  addEventListener('pagehide', function () { abbandoni(true); });

  /* posizione precisa (GPS / Wi-Fi del dispositivo), SOLO se il visitatore clicca
     "Usa la mia posizione" nei moduli con CAP/Città: compila i campi e la registra nelle statistiche. */
  var GL = navigator.geolocation;
  var TX = {
    it: ['Ci dite da dove ci visitate?', 'Condividete la vostra posizione: la usiamo solo internamente per capire da quali zone arrivano i clienti. Non la cediamo a nessuno.', 'Condividi posizione', 'No, grazie', 'Usa la mia posizione', 'Cerco la posizione…', 'Posizione non disponibile', 'Informativa'],
    en: ['Where are you visiting from?', 'Share your location: we only use it internally to see which areas our customers come from and plan deliveries and agents. We never pass it on.', 'Share location', 'No, thanks', 'Use my location', 'Locating…', 'Location unavailable', 'Privacy'],
    de: ['Woher besuchen Sie uns?', 'Teilen Sie Ihren Standort: Wir nutzen ihn nur intern, um zu sehen, aus welchen Regionen unsere Kunden kommen, und Lieferungen zu planen. Keine Weitergabe an Dritte.', 'Standort teilen', 'Nein, danke', 'Meinen Standort verwenden', 'Standort wird ermittelt…', 'Standort nicht verfügbar', 'Datenschutz'],
    fr: ['D\'où nous rendez-vous visite ?', 'Partagez votre position : nous l\'utilisons uniquement en interne pour savoir de quelles zones viennent nos clients et organiser les livraisons. Jamais transmise à des tiers.', 'Partager la position', 'Non merci', 'Utiliser ma position', 'Localisation…', 'Position indisponible', 'Confidentialité'],
    es: ['¿Desde dónde nos visita?', 'Comparta su ubicación: solo la usamos internamente para saber de qué zonas vienen nuestros clientes y organizar entregas. Nunca la cedemos a terceros.', 'Compartir ubicación', 'No, gracias', 'Usar mi ubicación', 'Buscando ubicación…', 'Ubicación no disponible', 'Privacidad']
  };
  var T = TX[LG] || TX.en;
  var mandaPos = function (p, modo) {
    var c = p.coords; tocca();
    invia('pos', { la: Math.round(c.latitude * 1e5) / 1e5, lo: Math.round(c.longitude * 1e5) / 1e5, ac: Math.round(c.accuracy || 0), m: modo });
    set('ds_gps_ok', String(ora())); del('ds_gps_no');
  };
  var chiediPos = function (modo, ok, ko) {
    if (!GL) { if (ko) ko(); return; }
    GL.getCurrentPosition(function (p) { mandaPos(p, modo); if (ok) ok(p); },
      function (err) { if (err && err.code === 1) set('ds_gps_no', String(ora())); if (ko) ko(err); },
      { enableHighAccuracy: true, timeout: 20000, maximumAge: 5 * 60000 });
  };
  /* pulsante "Usa la mia posizione" accanto ai campi CAP / Città dei moduli */
  var campoDi = function (f, re, ac) {
    var els = f.querySelectorAll('input'); for (var i = 0; i < els.length; i++) { var e = els[i];
      if ((ac && (e.getAttribute('autocomplete') || '').indexOf(ac) >= 0) || re.test(e.name || '') || re.test(e.id || '')) return e; }
    return null;
  };
  var riempi = function (el, v) { if (el && v && !String(el.value || '').trim()) { el.value = v; el.dispatchEvent(new Event('input', { bubbles: true })); el.dispatchEvent(new Event('change', { bubbles: true })); } };
  var aggiungiPulsanti = function () {
    if (!GL || !window.isSecureContext) return;
    var forms = document.querySelectorAll('form'); for (var i = 0; i < forms.length; i++) (function (f) {
      if (f.getAttribute('data-pd-gps')) return;
      var citta = campoDi(f, /(^|_)(citt[aà]|city|town)$/i, 'address-level2'), cap = campoDi(f, /(^|_)(cap|zip|postal)/i, 'postal-code');
      var ancora = cap; if (!ancora || !citta) return;   // solo moduli di indirizzo (CAP + Città)
      f.setAttribute('data-pd-gps', '1');
      var b = document.createElement('button'); b.type = 'button'; b.textContent = '📍 ' + T[4];
      b.style.cssText = 'display:inline-block;margin:6px 0 2px;padding:6px 10px;border:1px solid currentColor;border-radius:8px;background:transparent;color:inherit;font:inherit;font-size:13px;cursor:pointer;opacity:.85';
      b.onclick = function () {
        b.disabled = true; b.textContent = T[5];
        chiediPos('modulo', function (p) {
          var c = p.coords;
          fetch('https://nominatim.openstreetmap.org/reverse?format=jsonv2&addressdetails=1&zoom=18&lat=' + c.latitude + '&lon=' + c.longitude + '&accept-language=' + LG)
            .then(function (r) { return r.json(); }).then(function (j) {
              var a = (j && j.address) || {};
              riempi(campoDi(f, /(^|_)(cap|zip|postal)/i, 'postal-code'), a.postcode);
              riempi(campoDi(f, /(^|_)(citt[aà]|city|town)$/i, 'address-level2'), a.city || a.town || a.village || a.municipality);
              var pr = campoDi(f, /(^|_)(provincia|province|county)$/i, 'address-level1'); riempi(pr, a['ISO3166-2-lvl6'] ? a['ISO3166-2-lvl6'].split('-').pop() : (a.county || ''));
              riempi(campoDi(f, /(^|_)(via|indirizzo|street|address)$/i, 'street-address'), [a.road, a.house_number].filter(Boolean).join(' '));
              b.textContent = '📍 ✓'; b.disabled = false;
            }).catch(function () { b.textContent = '📍 ' + T[4]; b.disabled = false; });
        }, function () { b.textContent = T[6]; setTimeout(function () { b.textContent = '📍 ' + T[4]; b.disabled = false; }, 2500); });
      };
      ancora.parentNode.insertBefore(b, ancora.nextSibling);
    })(forms[i]);
  };
  var tPuls = null, programma = function () { clearTimeout(tPuls); tPuls = setTimeout(aggiungiPulsanti, 300); };
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', programma); else programma();
  try { new MutationObserver(programma).observe(document.documentElement, { childList: true, subtree: true }); } catch (e) {}

  /* ───────── richieste dei moduli: copia nel database (scheda "Richieste" della dashboard) ─────────
     I moduli del sito (assets/js/contatto.js e fiere-richiesta.js) inviano a FormSubmit con fetch():
     qui intercettiamo quella chiamata e ne mandiamo una copia alla funzione ds/richiesta.
     L'email continua ad arrivare come prima; se FormSubmit non risponde la richiesta resta comunque salvata. */
  var URL_RICHIESTA = BASE + '/richiesta';
  var copiaRichiesta = function (d) {
    try {
      var campi = [], email = '';
      for (var k in d) {
        if (!d.hasOwnProperty(k) || k.charAt(0) === '_') continue;
        if (k === 'email') { email = String(d[k] || ''); continue; }
        campi.push([k, String(d[k] == null ? '' : d[k]).slice(0, 3000)]);
      }
      if (!campi.length) return;
      set('ds_rq', '1');   // ha già scritto: niente popup dello sconto
      tocca();
      var body = JSON.stringify({ si: SITO, v: vid, s: sess.id, p: percorso(), t: (document.title || '').slice(0, 200), l: LG, oggetto: String(d._subject || '').slice(0, 200), email: email, campi: campi });
      origFetch(URL_RICHIESTA, { method: 'POST', body: body, mode: 'no-cors', keepalive: true, headers: { 'Content-Type': 'text/plain' } }).catch(function () {});
    } catch (e) {}
  };
  var origFetch = window.fetch;
  if (origFetch) {
    window.fetch = function (u, o) {
      try {
        var url = String(u && u.url ? u.url : u);
        if (/^https:\/\/formsubmit\.co\//i.test(url) && o && typeof o.body === 'string') copiaRichiesta(JSON.parse(o.body));
      } catch (e) {}
      return origFetch.apply(this, arguments);
    };
  }

  /* ───────── più richieste: popup −3% newsletter, fascia preventivo, fumetto WhatsApp (ds-conversioni.js) ───────── */
  if (SITO === 'stand') try { var cv = document.createElement('script'); cv.src = '/assets/js/ds-conversioni.js?v=1'; cv.defer = true; (document.head || document.documentElement).appendChild(cv); } catch (e) {}

  /* ───────── banner cookie (statistiche dettagliate) ─────────
     Senza consenso restano solo i conteggi anonimi. La scelta vale 6 mesi. */
  var MOSTRA_BANNER = true;
  var KEY = 'ds_consent', DURATA = 180 * 864e5;
  var leggiScelta = function () {
    try { var v = JSON.parse(localStorage.getItem(KEY) || 'null'); if (v && v.v === 1 && (v.s === 'granted' || v.s === 'denied') && Date.now() - v.t < DURATA) return v.s; } catch (e) {}
    return null;
  };
  var CK = {
    it: ['Per migliorare il sito e risponderti meglio registriamo in forma anonima le pagine visitate. Se accetti, registriamo anche come navighi (clic, sezioni lette, moduli iniziati: mai quello che scrivi). Il sito funziona in ogni caso.', 'Accetta', 'Rifiuta', 'Cookie policy', '/cookie-policy/'],
    en: ['To improve the site and help you better we record the pages you visit anonymously. If you accept, we also record how you browse (clicks, sections read, forms started: never what you type). The site works either way.', 'Accept', 'Decline', 'Cookie policy', '/en/cookie-policy/'],
    de: ['Um die Website zu verbessern, erfassen wir die besuchten Seiten anonym. Wenn Sie zustimmen, erfassen wir auch, wie Sie navigieren (Klicks, gelesene Abschnitte, begonnene Formulare: nie, was Sie eingeben). Die Website funktioniert in jedem Fall.', 'Akzeptieren', 'Ablehnen', 'Cookie-Richtlinie', '/de/cookie-richtlinie/'],
    fr: ['Pour améliorer le site, nous enregistrons de façon anonyme les pages consultées. Si vous acceptez, nous enregistrons aussi votre navigation (clics, sections lues, formulaires commencés : jamais ce que vous écrivez). Le site fonctionne dans tous les cas.', 'Accepter', 'Refuser', 'Cookies', '/fr/cookies/'],
    es: ['Para mejorar la web registramos de forma anónima las páginas visitadas. Si aceptas, registramos también cómo navegas (clics, secciones leídas, formularios empezados: nunca lo que escribes). La web funciona igualmente.', 'Aceptar', 'Rechazar', 'Cookies', '/es/cookies/']
  };
  var ck = CK[LG] || CK.en;
  var box = null;
  var chiudiBanner = function () { if (box && box.parentNode) box.parentNode.removeChild(box); box = null; };
  var decidi = function (ok) {
    var prima = leggiScelta();
    try { localStorage.setItem(KEY, JSON.stringify({ s: ok ? 'granted' : 'denied', t: Date.now(), v: 1 })); } catch (e) {}
    if (prima !== (ok ? 'granted' : 'denied')) window.dsEvento('consenso', ok ? 'ha accettato le statistiche dettagliate' : 'ha rifiutato le statistiche dettagliate');
    chiudiBanner();
    if (ok) osservaSezioni();
  };
  var apriBanner = function () {
    if (box || !document.body) return;
    box = document.createElement('div');
    box.setAttribute('role', 'dialog'); box.setAttribute('aria-live', 'polite'); box.setAttribute('aria-label', 'Cookie');
    box.style.cssText = 'position:fixed;left:16px;bottom:16px;z-index:2147483000;max-width:400px;background:rgba(7,11,20,.97);color:#e9edf7;' +
      'border:1px solid rgba(255,217,122,.28);border-radius:14px;padding:16px 18px;font:14px/1.5 Inter,system-ui,-apple-system,Segoe UI,Roboto,sans-serif;box-shadow:0 10px 30px rgba(0,0,0,.45)';
    if (window.innerWidth < 760) box.style.cssText += ';left:10px;right:10px;bottom:calc(84px + env(safe-area-inset-bottom));max-width:none';   // sopra la barra contatti mobile
    var bt = 'cursor:pointer;border-radius:999px;padding:9px 18px;font:600 14px Inter,system-ui,-apple-system,Segoe UI,Roboto,sans-serif;';
    box.innerHTML = '<p style="margin:0 0 12px">' + ck[0] + ' <a href="' + ck[4] + '" style="color:#ffe49f;text-decoration:underline">' + ck[3] + '</a></p>' +
      '<div style="display:flex;gap:8px;justify-content:flex-end;flex-wrap:wrap">' +
      '<button type="button" data-c="0" style="' + bt + 'background:transparent;color:#e9edf7;border:1px solid rgba(255,255,255,.3)">' + ck[2] + '</button>' +
      '<button type="button" data-c="1" style="' + bt + 'background:#FFC93C;color:#0b0b0b;border:1px solid #FFC93C">' + ck[1] + '</button></div>';
    box.addEventListener('click', function (e) { var b = e.target.closest('button[data-c]'); if (b) decidi(b.getAttribute('data-c') === '1'); });
    document.body.appendChild(box);
  };
  window.dsCookie = apriBanner;
  document.addEventListener('click', function (e) {
    var a = e.target && e.target.closest ? e.target.closest('a[href="#cookie"]') : null;
    if (a) { e.preventDefault(); apriBanner(); }
  }, true);
  var avvioBanner = function () { if (MOSTRA_BANNER && !leggiScelta() && !/^\/(render|private_area)(\/|$)/.test(location.pathname)) setTimeout(apriBanner, 1200); };
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', avvioBanner); else avvioBanner();
})();
