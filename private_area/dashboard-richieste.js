/* DANOVA STAND — dashboard · scheda Richieste: tutte le richieste arrivate dai moduli del sito
   (contatti e "Richiedi lo stand"), con chi le ha mandate, da dove arrivava e cosa ha guardato prima. */
(function () {
  'use strict';
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  var esc = function (s) { return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]; }); };
  var EUR = new Intl.NumberFormat('it-IT', { style: 'currency', currency: 'EUR', maximumFractionDigits: 0 });
  var NF = new Intl.NumberFormat('it-IT');
  var dt = function (t, conOra) { if (!t) return '—'; var d = new Date(t * 1000); return d.toLocaleDateString('it-IT', { day: '2-digit', month: '2-digit', year: '2-digit' }) + (conOra ? ' ' + d.toLocaleTimeString('it-IT', { hour: '2-digit', minute: '2-digit' }) : ''); };
  var fa = function (t) { if (!t) return 'mai'; var s = Date.now() / 1000 - t; if (s < 3600) return Math.max(1, Math.round(s / 60)) + ' min fa'; if (s < 86400) return Math.round(s / 3600) + ' ore fa'; if (s < 86400 * 30) return Math.round(s / 86400) + ' giorni fa'; return dt(t); };
  var tel = function (t) { return String(t || '').replace(/[^\d+]/g, ''); };
  var wa = function (t) { var n = tel(t).replace(/^\+/, '').replace(/^00/, ''); if (n.length === 10 && n[0] === '3') n = '39' + n; return 'https://wa.me/' + n; };
  var STATI = { nuova: 'Nuova', contattato: 'Contattato', preventivo: 'Preventivo inviato', acquisita: 'Acquisita', persa: 'Persa' };
  var CL = { nuova: 'ricevuto', contattato: 'produzione', preventivo: 'spedito', acquisita: 'consegnato', persa: 'annullato' };
  var badge = function (s) { return '<span class="st st-' + (CL[s] || 'ricevuto') + '">' + esc(STATI[s] || s) + '</span>'; };
  var NOME = (window.DSSITO || {}).nome && window.DSSITO.id ? window.DSSITO.nome : 'Danova';
  var NOMI_S = { stand: 'Danova Stand', costruzioni: 'Danova Costruzioni', tech: 'Danova Tech' };
  var MSG = {
    it: function (n, f, b) { return 'Buongiorno' + (n ? ' ' + n : '') + ', sono di ' + b + ': abbiamo ricevuto la sua richiesta' + (f ? ' per ' + f : '') + ' dal nostro sito. Quando possiamo sentirci per parlarne e prepararle il preventivo?'; },
    en: function (n, f, b) { return 'Hello' + (n ? ' ' + n : '') + ', this is ' + b + ': we received your request' + (f ? ' for ' + f : '') + ' from our website. When can we talk about it and prepare your quote?'; },
    de: function (n, f, b) { return 'Guten Tag' + (n ? ' ' + n : '') + ', hier ist ' + b + ': Wir haben Ihre Anfrage' + (f ? ' für ' + f : '') + ' über unsere Website erhalten. Wann können wir darüber sprechen und Ihr Angebot vorbereiten?'; },
    fr: function (n, f, b) { return 'Bonjour' + (n ? ' ' + n : '') + ', ici ' + b + ' : nous avons reçu votre demande' + (f ? ' pour ' + f : '') + ' depuis notre site. Quand pouvons-nous en parler et préparer votre devis ?'; },
    es: function (n, f, b) { return 'Hola' + (n ? ' ' + n : '') + ', le escribe ' + b + ': hemos recibido su solicitud' + (f ? ' para ' + f : '') + ' desde nuestra web. ¿Cuándo podemos hablar y prepararle el presupuesto?'; }
  };
  var marchio = function (r) { return NOMI_S[r.sito] || NOME; };
  var testo = function (r) { var f = MSG[r.lingua] || (r.lingua && r.lingua !== 'it' ? MSG.en : MSG.it); return f(String(r.nome || '').split(' ')[0], r.fiera || '', marchio(r)); };

  function api(a, q, corpo) {
    var opt = { cache: 'no-store', headers: PDADM.headers() };
    if (corpo) { opt.method = 'POST'; opt.headers['Content-Type'] = 'application/json'; opt.body = JSON.stringify(corpo); }
    return fetch(PDADM.url('a=' + a + (q ? '&' + q : '')), opt).then(function (r) { if (r.status === 401) { PDADM.esci(); throw new Error('accesso'); } return r.json(); });
  }
  function qs(o) { return Object.keys(o).filter(function (k) { return o[k] !== '' && o[k] != null; }).map(function (k) { return k + '=' + encodeURIComponent(o[k]); }).join('&'); }
  function modal(html) { $('#modal-body').innerHTML = html; $('#modal').hidden = false; $('#modal .modal-box').scrollTop = 0; return $('#modal-body'); }

  var F = { stato: 'aperte', q: '' }, ultime = [];
  function init() {
    var s = $('#tab-richieste');
    s.innerHTML = '<div class="kpis k5" id="r-kpi"></div>'
      + '<div class="card filters"><div class="seg" id="r-stati"></div><div class="sel"><input type="search" id="r-q" placeholder="Cerca nome, azienda, fiera, email, telefono…"><a class="ghost" id="r-csv" href="#">Scarica CSV</a></div></div>'
      + '<div class="card bz-card"><div class="bz-head"><div><h3>💬 Chi mi sta scrivendo su WhatsApp?</h3><small class="muted">I messaggi WhatsApp partiti dai siti finiscono con un codice «Rif.» (es. Rif. 3FA9C1): scrivetelo qui per vedere chi è e cosa ha guardato.</small></div>'
      + '<div class="sel"><input type="search" id="rif-q" placeholder="Codice Rif., es. 3FA9C1" maxlength="14"><button class="ghost" id="rif-go">Trova chi è</button></div></div><div id="rif-out"></div></div>'
      + '<div class="card"><div class="table-wrap tall"><table class="tbl" id="r-tab"></table></div></div>';
    $('#r-csv').href = PDADM.link('a=csv_richieste');
    var t; $('#r-q').addEventListener('input', function (e) { clearTimeout(t); t = setTimeout(function () { F.q = e.target.value.trim(); carica(); }, 300); });
    $('#rif-go').onclick = cercaRif; $('#rif-q').addEventListener('keydown', function (e) { if (e.key === 'Enter') cercaRif(); });
    carica();
  }
  function carica() {
    return api('richieste', qs(F)).then(function (d) {
      var tb = $('#r-tab'); if (!tb) return;
      if (!d.ok) { tb.innerHTML = '<tbody><tr><td class="empty">Non disponibile: aggiornate la funzione ds su Supabase.</td></tr></tbody>'; return; }
      if (d.stati) STATI = d.stati;
      var c = d.conta || {}, p = d.periodo || {}, aperte = (c.nuova || 0) + (c.contattato || 0) + (c.preventivo || 0);
      segnaNuovi(c.nuova || 0);
      $('#r-kpi').innerHTML = [
        ['Da gestire', NF.format(c.nuova || 0), (c.nuova ? 'richieste nuove' : 'tutto in ordine'), c.nuova ? 'hot' : ''],
        ['Oggi', NF.format(+p.oggi || 0), 'richieste arrivate'],
        ['Ultimi 7 giorni', NF.format(+p.d7 || 0), NF.format(+p.d30 || 0) + ' negli ultimi 30'],
        ['In trattativa', NF.format((c.contattato || 0) + (c.preventivo || 0)), NF.format(c.preventivo || 0) + ' con preventivo inviato'],
        ['Acquisite', NF.format(c.acquisita || 0), +p.valore_acquisito ? EUR.format(+p.valore_acquisito) + ' di lavori' : 'segnatele per vedere il valore']
      ].map(function (k) { return '<div class="kpi ' + (k[3] || '') + '"><span>' + k[0] + '</span><b>' + k[1] + '</b><em>' + k[2] + '</em></div>'; }).join('');
      var tot = Object.keys(c).reduce(function (a, k) { return a + c[k]; }, 0);
      $('#r-stati').innerHTML = [['aperte', 'Da seguire', aperte]].concat(Object.keys(STATI).map(function (k) { return [k, STATI[k], c[k] || 0]; })).concat([['tutte', 'Tutte', tot]])
        .map(function (x) { return '<button data-s="' + x[0] + '"' + (F.stato === x[0] ? ' class="on"' : '') + '>' + esc(x[1]) + ' <i>' + x[2] + '</i></button>'; }).join('');
      $$('#r-stati button').forEach(function (b) { b.onclick = function () { F.stato = b.dataset.s; carica(); }; });
      ultime = d.richieste || [];
      tb.innerHTML = '<thead><tr><th>Quando</th><th>Chi</th><th>Richiesta</th><th>Da dove</th><th>Contatta</th><th>Stato</th></tr></thead><tbody>'
        + (ultime.length ? ultime.map(function (r, i) {
          var rich = [r.fiera ? '<b>' + esc(r.fiera) + '</b>' : '', (r.campi || []).map(function (x) { return esc(x[0]) + ': ' + esc(x[1]); }).join(' · '), r.messaggio ? esc(String(r.messaggio).slice(0, 140)) + (String(r.messaggio).length > 140 ? '…' : '') : ''].filter(Boolean).join('<br>');
          return '<tr data-i="' + i + '"><td>' + dt(r.creato, true) + '<br><small class="muted">' + fa(r.creato) + '</small>' + (r.urgenza ? '<br><small class="' + (/^Subito/.test(r.urgenza) ? 'hot-t' : 'muted') + '">' + (/^Subito/.test(r.urgenza) ? '🔥 ' : '⏱ ') + esc(r.urgenza) + '</small>' : '') + '</td>'
            + '<td>' + (!(window.DSSITO || {}).id && r.sito ? '<span class="st st-spedito">' + esc(NOMI_S[r.sito] || r.sito) + '</span><br>' : '') + '<b>' + esc(r.nome || '—') + '</b>' + (r.azienda ? '<br><small>' + esc(r.azienda) + '</small>' : '') + '<br><small class="muted">' + [esc(r.email), esc(r.telefono)].filter(Boolean).join('<br>') + '</small></td>'
            + '<td class="wrap">' + (rich || '<span class="muted">' + esc(r.oggetto || '') + '</span>') + '</td>'
            + '<td><small>' + esc(r.titolo || r.pagina || '') + '</small><br><small class="muted">' + [r.citta, r.paese].filter(Boolean).map(esc).join(', ') + (r.sorgente ? ' · da ' + esc(r.sorgente) : '') + (+r.visite ? ' · ' + r.visite + ' visit' + (+r.visite === 1 ? 'a' : 'e') + ', ' + r.pagine_viste + ' pagine' : '') + '</small></td>'
            + '<td><div class="acts">' + (r.telefono ? '<a class="ghost" href="tel:' + esc(tel(r.telefono)) + '">📞</a><a class="ghost" target="_blank" rel="noopener" href="' + wa(r.telefono) + '?text=' + encodeURIComponent(testo(r)) + '">💬</a>' : '')
            + (r.email ? '<a class="ghost" href="mailto:' + esc(r.email) + '?subject=' + encodeURIComponent(marchio(r) + ' — la sua richiesta' + (r.fiera ? ' per ' + r.fiera : '')) + '&body=' + encodeURIComponent(testo(r)) + '">✉️</a>' : '')
            + (r.pid && window.PDPersona ? '<button class="ghost" data-pp="' + esc(r.pid) + '" title="Cosa ha guardato sul sito">👤</button>' : '') + '</div></td>'
            + '<td>' + badge(r.stato) + (r.valore != null ? '<br><small>' + EUR.format(+r.valore) + '</small>' : '') + (r.note_admin ? '<br><small class="muted">' + esc(String(r.note_admin).slice(0, 80)) + '</small>' : '') + '</td></tr>';
        }).join('') : '<tr><td colspan="6" class="empty">' + (F.q ? 'Nessuna richiesta trovata.' : F.stato === 'aperte' ? 'Nessuna richiesta da seguire. Compariranno qui appena qualcuno invia un modulo del sito.' : 'Nessuna.') + '</td></tr>') + '</tbody>';
      $$('tbody tr[data-i]', tb).forEach(function (tr) {
        tr.onclick = function (e) { if (e.target.closest('a,button')) return; apri(ultime[+tr.dataset.i]); };
      });
      $$('[data-pp]', tb).forEach(function (x) { x.onclick = function (e) { e.stopPropagation(); window.PDPersona.apri(x.dataset.pp); }; });
    }).catch(function () {});
  }
  function apri(r) {
    var b = modal('<div class="m-head"><h2>' + esc(r.nome || r.azienda || 'Richiesta') + '</h2>' + badge(r.stato) + '</div>'
      + '<div class="muted small">Arrivata il ' + dt(r.creato, true) + (r.titolo || r.pagina ? ' dalla pagina <i>' + esc(r.titolo || r.pagina) + '</i>' : '') + (r.rif ? ' · Rif. ' + esc(r.rif) : '') + '</div>'
      + '<div class="m-grid"><div><h3>Contatto</h3><p><b>' + esc(r.nome || '—') + '</b>' + (r.azienda ? '<br>' + esc(r.azienda) : '') + '</p><div class="acts">'
      + (r.email ? '<a class="ghost" href="mailto:' + esc(r.email) + '?subject=' + encodeURIComponent(marchio(r) + ' — la sua richiesta') + '&body=' + encodeURIComponent(testo(r)) + '">' + esc(r.email) + '</a>' : '')
      + (r.telefono ? '<a class="ghost" href="tel:' + esc(tel(r.telefono)) + '">' + esc(r.telefono) + '</a><a class="ghost" target="_blank" rel="noopener" href="' + wa(r.telefono) + '?text=' + encodeURIComponent(testo(r)) + '">WhatsApp</a>' : '') + '</div>'
      + (r.pid && window.PDPersona ? '<p><button class="ghost" id="r-pp">👤 Cosa ha guardato sul sito</button></p>' : '') + '</div>'
      + '<div><h3>Provenienza</h3><div class="det">' + [['Luogo', [r.citta, r.regione, r.paese].filter(Boolean).join(', ')], ['Arrivato da', [r.sorgente, r.canale].filter(Boolean).join(' · ')], ['Lingua', String(r.lingua || '').toUpperCase()], ['Visite sul sito', r.visite ? r.visite + ' (' + r.pagine_viste + ' pagine)' : '']]
        .filter(function (x) { return x[1]; }).map(function (x) { return '<span>' + x[0] + '</span><b>' + esc(x[1]) + '</b>'; }).join('') + '</div></div></div>'
      + '<h3>Richiesta</h3><div class="det">' + [['Fiera', r.fiera], ['Quando vuole partire', r.urgenza]].concat(r.campi || []).filter(function (x) { return x[1]; }).map(function (x) { return '<span>' + esc(x[0]) + '</span><b>' + esc(x[1]) + '</b>'; }).join('') + '</div>'
      + (r.messaggio ? '<p class="quote" style="margin-top:10px">' + esc(r.messaggio) + '</p>' : '')
      + '<form class="card m-form" id="r-form"><h3>Aggiorna</h3><label>Stato <select name="stato">' + Object.keys(STATI).map(function (k) { return '<option value="' + k + '"' + (k === r.stato ? ' selected' : '') + '>' + esc(STATI[k]) + '</option>'; }).join('') + '</select></label>'
      + '<label>Valore del lavoro in € (facoltativo, per i totali)<input name="valore" type="number" min="0" step="1" value="' + (r.valore != null ? +r.valore : '') + '" style="background:var(--page);border:1px solid var(--line-2);border-radius:9px;padding:8px 10px;color:var(--ink)"></label>'
      + '<label>Note interne<textarea name="note_admin" rows="3">' + esc(r.note_admin || '') + '</textarea></label><div class="acts"><button class="btn" type="submit">Salva</button><span id="r-msg" class="muted small"></span></div></form>');
    var pp = $('#r-pp', b); if (pp) pp.onclick = function () { window.PDPersona.apri(r.pid); };
    var f = $('#r-form', b);
    f.onsubmit = function (e) {
      e.preventDefault(); var bt = $('button', f); bt.disabled = true;
      api('richiesta_salva', 'id=' + r.id, { stato: f.stato.value, note_admin: f.note_admin.value, valore: f.valore.value }).then(function (x) {
        bt.disabled = false; $('#r-msg').textContent = x.ok ? 'Salvato ✓' : 'Errore';
        if (x.ok) carica();
      });
    };
  }
  function cercaRif() {
    var v = $('#rif-q').value.replace(/^\s*(rif|ref)\.?\s*/i, '').trim(), out = $('#rif-out');
    if (!v) return;
    out.innerHTML = '<p class="muted small">Cerco…</p>';
    api('rif', 'rif=' + encodeURIComponent(v)).then(function (r) {
      if (!r.ok) { out.innerHTML = '<p class="muted small">Codice non valido: sono 6 lettere o numeri, es. 3FA9C1.</p>'; return; }
      if (!r.pid) { out.innerHTML = '<p class="muted small">Nessun visitatore con il codice Rif. ' + esc(r.rif) + '. I codici compaiono solo nei messaggi partiti dal sito dopo l\'attivazione dell\'area privata.</p>'; return; }
      var chi = r.chi || {};
      out.innerHTML = '<div class="rif-hit"><span>Rif. <b>' + esc(r.rif) + '</b> → ' + esc(chi.nome || chi.email || 'visitatore anonimo') + (chi.telefono ? ' · ' + esc(chi.telefono) : '')
        + (r.evento ? ' · ha aperto WhatsApp ' + fa(r.evento.ts) + ' dalla pagina <i>' + esc(r.evento.titolo || r.evento.percorso || '') + '</i>' : '') + '</span>'
        + (window.PDPersona ? '<button class="ghost" id="rif-pp">👤 Apri il profilo completo</button>' : '') + '</div>';
      var bt = $('#rif-pp'); if (bt) bt.onclick = function () { window.PDPersona.apri(r.pid); };
    });
  }

  /* avvio: la scheda si carica quando viene aperta; il numero delle nuove richieste si aggiorna ogni minuto */
  var fatto = false;
  function apriScheda(t) { if (t !== 'richieste') return; if (!fatto) { fatto = true; init(); } else carica(); }
  document.addEventListener('pd-tab', function (e) { apriScheda(e.detail); });
  var att = $('.tabs button.on'); if (att) apriScheda(att.dataset.tab);
  function segnaNuovi(n) {
    var b = $('.tabs [data-tab=richieste]'); if (!b) return;
    var i = $('i', b);
    if (!i) { i = document.createElement('i'); i.className = 'cnt'; b.appendChild(i); }
    i.textContent = n; i.hidden = !n;
  }
  function contatore() { api('richieste', 'stato=nuova').then(function (r) { if (r.ok) segnaNuovi((r.conta || {}).nuova || 0); }).catch(function () {}); }
  contatore(); setInterval(function () { if (!document.hidden) contatore(); }, 60000);
})();
