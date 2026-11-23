/* DANOVA — dashboard · scheda "Clienti & lavori": anagrafica dei clienti (anche potenziali) e dei lavori,
   con le date di produzione, montaggio, fiera e smontaggio. Calendario del mese, agenda dei prossimi giorni,
   avviso quando due montaggi/smontaggi cadono lo stesso giorno, calendario da aggiungere al telefono (.ics). */
(function () {
  'use strict';
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  var esc = function (s) { return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]; }); };
  var EUR = new Intl.NumberFormat('it-IT', { style: 'currency', currency: 'EUR', maximumFractionDigits: 0 });
  var NF = new Intl.NumberFormat('it-IT');
  var tel = function (t) { return String(t || '').replace(/[^\d+]/g, ''); };
  var wa = function (t) { var n = tel(t).replace(/^\+/, '').replace(/^00/, ''); if (n.length === 10 && n[0] === '3') n = '39' + n; return 'https://wa.me/' + n; };

  /* ---------- date come testo AAAA-MM-GG (niente fusi orari) ---------- */
  var pad = function (n) { return (n < 10 ? '0' : '') + n; };
  var ds = function (d) { return d.getFullYear() + '-' + pad(d.getMonth() + 1) + '-' + pad(d.getDate()); };
  var dd = function (s) { var p = String(s).split('-'); return new Date(+p[0], +p[1] - 1, +p[2]); };
  var piu = function (s, n) { var d = dd(s); d.setDate(d.getDate() + n); return ds(d); };
  var diff = function (a, b) { return Math.round((dd(b) - dd(a)) / 86400000); };
  var OGGI = ds(new Date());
  var GS = ['dom', 'lun', 'mar', 'mer', 'gio', 'ven', 'sab'];
  var MS = ['gen', 'feb', 'mar', 'apr', 'mag', 'giu', 'lug', 'ago', 'set', 'ott', 'nov', 'dic'];
  var fd = function (s, conGiorno) { if (!s) return ''; var d = dd(s); return (conGiorno ? GS[d.getDay()] + ' ' : '') + d.getDate() + ' ' + MS[d.getMonth()] + (d.getFullYear() !== new Date().getFullYear() ? ' ' + d.getFullYear() : ''); };
  var fr = function (da, a) {
    if (!da) return '';
    if (!a || a === da) return fd(da, true);
    var x = dd(da), y = dd(a);
    if (x.getMonth() === y.getMonth() && x.getFullYear() === y.getFullYear()) return GS[x.getDay()] + ' ' + x.getDate() + ' → ' + GS[y.getDay()] + ' ' + fd(a);
    return fd(da, true) + ' → ' + fd(a, true);
  };
  var quando = function (da) {
    var n = diff(OGGI, da);
    if (n > 1) return 'tra ' + n + ' giorni';
    if (n === 1) return 'domani';
    return '';
  };

  /* ---------- fasi di un lavoro ---------- */
  var FASI = [
    { k: 'prod', nome: 'Produzione', ic: '🏭', da: 'prod_da', a: 'prod_a', flag: 'produzione' },
    { k: 'mont', nome: 'Montaggio', ic: '🔧', da: 'mont_da', a: 'mont_a', flag: 'montaggio' },
    { k: 'fiera', nome: 'Fiera / evento', ic: '🎪', da: 'evento_da', a: 'evento_a', flag: null },
    { k: 'smont', nome: 'Smontaggio', ic: '📦', da: 'smont_da', a: 'smont_a', flag: 'smontaggio' }
  ];
  var attiva = function (l, f) { return !f.flag || +l[f.flag] === 1; };
  function fasiDi(l) {
    return FASI.filter(function (f) { return attiva(l, f) && l[f.da]; }).map(function (f) { return { f: f, da: l[f.da], a: l[f.a] || l[f.da], l: l }; });
  }
  var chip = function (f, testo) { return '<span class="fase ' + f.k + '"><i></i>' + esc(testo != null ? testo : f.nome) + '</span>'; };
  var ATTIVI = { preventivo: 1, confermato: 1, produzione: 1, montato: 1 };
  var STATI_C0 = { potenziale: 'Potenziale', trattativa: 'In trattativa', attivo: 'Cliente', ex: 'Non più attivo', perso: 'Perso' };
  var STATI_L0 = { preventivo: 'Da confermare', confermato: 'Confermato', produzione: 'In produzione', montato: 'Montato / in fiera', concluso: 'Concluso', annullato: 'Annullato' };

  /* ---------- dati ---------- */
  var D = { clienti: [], lavori: [], stati_c: STATI_C0, stati_l: STATI_L0, ics: '' }, C = {};
  var V = { mese: OGGI.slice(0, 8) + '01', fc: 'tutti', fl: 'attivi', q: '' };
  var badgeC = function (s) { return '<span class="st st-' + esc(s) + '">' + esc(D.stati_c[s] || s) + '</span>'; };
  var badgeL = function (s) { return '<span class="st st-' + esc(s) + '">' + esc(D.stati_l[s] || s) + '</span>'; };
  var nomeLav = function (l) { return l.fiera || l.titolo || 'Lavoro'; };
  var cliDi = function (l) { return C[l.cliente] || {}; };

  function api(a, q, corpo) {
    var opt = { cache: 'no-store', headers: PDADM.headers() };
    if (corpo) { opt.method = 'POST'; opt.headers['Content-Type'] = 'application/json'; opt.body = JSON.stringify(corpo); }
    return fetch(PDADM.url('a=' + a + (q ? '&' + q : '')), opt).then(function (r) { if (r.status === 401) { PDADM.esci(); throw new Error('accesso'); } return r.json(); });
  }
  function modal(html) { $('#modal-body').innerHTML = html; $('#modal').hidden = false; $('#modal .modal-box').scrollTop = 0; return $('#modal-body'); }
  function chiudi() { $('#modal').hidden = true; }

  function init() {
    $('#tab-clienti').innerHTML = '<div class="kpis k5" id="c-kpi"></div>'
      + '<div class="card filters cl-bar"><button class="btn" id="c-nuovo">＋ Nuovo cliente</button><button class="btn" id="l-nuovo">＋ Nuovo lavoro</button>'
      + '<div class="sel"><input type="search" id="c-q" placeholder="Cerca cliente, fiera, città, telefono…"><button class="ghost" id="c-ics">📅 Calendario sul telefono</button><a class="ghost" id="c-csv" href="#">Scarica CSV</a></div></div>'
      + '<div class="card"><div class="cal-head"><button class="ghost" id="cal-p">‹</button><h3 id="cal-t"></h3><button class="ghost" id="cal-n">›</button><button class="ghost" id="cal-o">Oggi</button>'
      + '<div class="fasi-leg">' + FASI.map(function (f) { return chip(f, f.ic + ' ' + f.nome); }).join('') + '</div></div><div class="cal" id="cal"></div></div>'
      + '<div class="cl-cols"><div class="card"><h3>Prossimi 60 giorni</h3><div class="agenda" id="agenda"></div></div>'
      + '<div class="card"><div class="chart-head"><h3>Clienti</h3><div class="seg small" id="c-seg"></div></div><div class="cl-grid" id="c-grid"></div></div></div>'
      + '<div class="card" style="margin-top:14px"><div class="chart-head"><h3>Lavori</h3><div class="seg small" id="l-seg"></div></div><div class="table-wrap tall"><table class="tbl" id="l-tab"></table></div></div>';
    $('#c-nuovo').onclick = function () { apriCliente(null); };
    $('#l-nuovo').onclick = function () { apriLavoro(null); };
    $('#c-ics').onclick = apriIcs;
    $('#c-csv').href = PDADM.link('a=csv_lavori');
    $('#cal-p').onclick = function () { V.mese = meseAgg(-1); calendario(); };
    $('#cal-n').onclick = function () { V.mese = meseAgg(1); calendario(); };
    $('#cal-o').onclick = function () { V.mese = OGGI.slice(0, 8) + '01'; calendario(); };
    var t; $('#c-q').addEventListener('input', function (e) { clearTimeout(t); t = setTimeout(function () { V.q = e.target.value.trim().toLowerCase(); clienti(); lavori(); }, 200); });
    calendario();
    carica();
  }
  function meseAgg(n) { var d = dd(V.mese); d.setDate(1); d.setMonth(d.getMonth() + n); return ds(d); }

  function carica() {
    return api('clienti').then(function (d) {
      if (!d.ok) { if ($('#c-kpi')) $('#c-kpi').innerHTML = '<div class="kpi hot"><span>Sezione non ancora attiva</span><b>—</b><em>Aggiornate la funzione «ds» su Supabase (strumenti/supabase/GUIDA-SUPABASE.md)</em></div>'; return; }
      D = d; C = {}; d.clienti.forEach(function (c) { c.lavori = []; C[c.id] = c; });
      d.lavori.forEach(function (l) { if (C[l.cliente]) C[l.cliente].lavori.push(l); });
      if ($('#c-kpi')) tutto();
    }).catch(function () {});
  }
  function tutto() { kpi(); calendario(); agenda(); clienti(); lavori(); }

  function kpi() {
    var cc = D.clienti, ll = D.lavori.filter(function (l) { return l.stato !== 'annullato'; });
    var cnt = function (f) { return cc.filter(f).length; };
    var fra7 = piu(OGGI, 7), sett = [];
    ll.forEach(function (l) { if (l.stato === 'concluso') return; fasiDi(l).forEach(function (x) { if ((x.f.k === 'mont' || x.f.k === 'smont') && x.da <= fra7 && x.a >= OGGI) sett.push(x); }); });
    var val = ll.filter(function (l) { return l.stato !== 'preventivo' && l.valore != null; }).reduce(function (a, l) { return a + (+l.valore || 0); }, 0);
    var dacf = ll.filter(function (l) { return l.stato === 'preventivo'; }).length;
    $('#c-kpi').innerHTML = [
      ['Clienti', NF.format(cnt(function (c) { return c.stato === 'attivo'; })), NF.format(cc.length) + ' in rubrica'],
      ['Potenziali', NF.format(cnt(function (c) { return c.stato === 'potenziale' || c.stato === 'trattativa'; })), NF.format(cnt(function (c) { return c.stato === 'trattativa'; })) + ' in trattativa'],
      ['Lavori aperti', NF.format(ll.filter(function (l) { return ATTIVI[l.stato]; }).length), dacf ? dacf + ' da confermare' : 'nessuno da confermare'],
      ['Montaggi e smontaggi', NF.format(sett.length), 'nei prossimi 7 giorni', sett.length ? 'hot' : ''],
      ['Valore lavori', val ? EUR.format(val) : '—', 'confermati e conclusi']
    ].map(function (k) { return '<div class="kpi ' + (k[3] || '') + '"><span>' + k[0] + '</span><b>' + k[1] + '</b><em>' + k[2] + '</em></div>'; }).join('');
  }

  /* ---------- calendario del mese ---------- */
  function calendario() {
    var m = dd(V.mese), primo = V.mese;
    $('#cal-t').textContent = m.toLocaleDateString('it-IT', { month: 'long', year: 'numeric' });
    var inizio = piu(primo, -((m.getDay() + 6) % 7));
    var ultimo = piu(ds(new Date(m.getFullYear(), m.getMonth() + 1, 1)), -1);
    var giorni = Math.ceil((diff(inizio, ultimo) + 1) / 7) * 7;
    var fine = piu(inizio, giorni - 1), ev = [];
    D.lavori.forEach(function (l) { if (l.stato === 'annullato') return; fasiDi(l).forEach(function (x) { if (x.da <= fine && x.a >= inizio) ev.push(x); }); });
    ev.sort(function (a, b) { return FASI.indexOf(a.f) - FASI.indexOf(b.f) || (a.da < b.da ? -1 : 1); });
    var h = ['lun', 'mar', 'mer', 'gio', 'ven', 'sab', 'dom'].map(function (g) { return '<div class="dn">' + g + '</div>'; }).join('');
    for (var i = 0; i < giorni; i++) {
      var g = piu(inizio, i), d = dd(g), qui = ev.filter(function (x) { return x.da <= g && x.a >= g; });
      var squadre = qui.filter(function (x) { return x.f.k === 'mont' || x.f.k === 'smont'; }).length;
      h += '<div class="g' + (g.slice(0, 7) !== primo.slice(0, 7) ? ' fuori' : '') + (g === OGGI ? ' oggi' : '') + (d.getDay() === 0 || d.getDay() === 6 ? ' we' : '') + '">'
        + '<div class="n"><span>' + d.getDate() + '</span>' + (squadre > 1 ? '<span class="warn" title="Più montaggi/smontaggi nello stesso giorno">⚠ ' + squadre + ' squadre</span>' : '') + '</div>'
        + qui.slice(0, 4).map(function (x) { var c = cliDi(x.l); return '<div class="ev ' + x.f.k + '" data-l="' + x.l.id + '" title="' + esc(x.f.nome + ' · ' + (c.nome || '') + ' · ' + nomeLav(x.l) + ' · ' + fr(x.da, x.a)) + '">' + x.f.ic + ' ' + esc(c.nome || nomeLav(x.l)) + '</div>'; }).join('')
        + (qui.length > 4 ? '<div class="piu" data-g="' + g + '">+' + (qui.length - 4) + ' altri</div>' : '') + '</div>';
    }
    $('#cal').innerHTML = h;
    $$('#cal [data-l]').forEach(function (e) { e.onclick = function () { apriLavoro(+e.dataset.l); }; });
    $$('#cal [data-g]').forEach(function (e) { e.onclick = function () { apriGiorno(e.dataset.g); }; });
  }
  function apriGiorno(g) {
    var qui = [];
    D.lavori.forEach(function (l) { if (l.stato !== 'annullato') fasiDi(l).forEach(function (x) { if (x.da <= g && x.a >= g) qui.push(x); }); });
    var b = modal('<h2>' + esc(fd(g, true)) + '</h2><div class="lav-mini" style="margin-top:12px">' + qui.map(function (x) {
      return '<div data-l="' + x.l.id + '">' + chip(x.f, x.f.ic + ' ' + x.f.nome) + ' <b>' + esc(cliDi(x.l).nome || '') + '</b> · ' + esc(nomeLav(x.l)) + '<br><small class="muted">' + esc(fr(x.da, x.a)) + (x.l.luogo ? ' · ' + esc(x.l.luogo) : '') + '</small></div>';
    }).join('') + '</div>');
    $$('[data-l]', b).forEach(function (e) { e.onclick = function () { apriLavoro(+e.dataset.l); }; });
  }

  /* ---------- agenda: le prossime fasi, giorno per giorno ---------- */
  function agenda() {
    var fino = piu(OGGI, 60), ev = [];
    D.lavori.forEach(function (l) { if (l.stato === 'annullato' || l.stato === 'concluso') return; fasiDi(l).forEach(function (x) { if (x.a >= OGGI && x.da <= fino) ev.push(x); }); });
    ev.sort(function (a, b) { var x = a.da < OGGI ? OGGI : a.da, y = b.da < OGGI ? OGGI : b.da; return x < y ? -1 : x > y ? 1 : FASI.indexOf(a.f) - FASI.indexOf(b.f); });
    if (!ev.length) { $('#agenda').innerHTML = '<p class="empty">Nessuna data nei prossimi 60 giorni.<br>Aggiungete un lavoro con le date di montaggio e smontaggio.</p>'; return; }
    var h = '', ult = '';
    ev.forEach(function (x) {
      var g = x.da < OGGI ? OGGI : x.da, c = cliDi(x.l);
      if (g !== ult) { ult = g; h += '<div class="ag-g' + (g === OGGI ? ' oggi' : '') + '"><span>' + esc(g === OGGI ? 'Oggi · ' + fd(g, true) : fd(g, true)) + '</span><span>' + esc(quando(g)) + '</span></div>'; }
      h += '<div class="ag-r" data-l="' + x.l.id + '">' + chip(x.f, x.f.ic + ' ' + x.f.nome) + '<b>' + esc(c.nome || '—') + ' · ' + esc(nomeLav(x.l)) + '</b><span class="q">' + (x.da < OGGI ? 'in corso' : '') + '</span>'
        + '<small>' + esc(fr(x.da, x.a)) + (x.l.luogo ? ' · ' + esc(x.l.luogo) : '') + (x.l.stand ? ' · stand ' + esc(x.l.stand) : '') + (x.l.stato === 'preventivo' ? ' · da confermare' : '') + '</small></div>';
    });
    $('#agenda').innerHTML = h;
    $$('#agenda [data-l]').forEach(function (e) { e.onclick = function () { apriLavoro(+e.dataset.l); }; });
  }

  /* ---------- clienti ---------- */
  var cerca = function (testi) { return !V.q || testi.filter(Boolean).join(' ').toLowerCase().indexOf(V.q) >= 0; };
  function prossima(c) {
    var p = null;
    c.lavori.forEach(function (l) { if (l.stato === 'annullato' || l.stato === 'concluso') return; fasiDi(l).forEach(function (x) { if (x.a >= OGGI && (!p || x.da < p.da)) p = x; }); });
    return p;
  }
  function clienti() {
    var segs = [['tutti', 'Tutti'], ['potenziale', 'Potenziali'], ['trattativa', 'In trattativa'], ['attivo', 'Clienti'], ['ex', 'Altri']];
    var dentro = function (c, k) { return k === 'tutti' || c.stato === k || (k === 'ex' && c.stato === 'perso'); };
    $('#c-seg').innerHTML = segs.map(function (s) { return '<button data-s="' + s[0] + '"' + (V.fc === s[0] ? ' class="on"' : '') + '>' + s[1] + ' <i>' + D.clienti.filter(function (c) { return dentro(c, s[0]); }).length + '</i></button>'; }).join('');
    $$('#c-seg button').forEach(function (b) { b.onclick = function () { V.fc = b.dataset.s; clienti(); }; });
    var cc = D.clienti.filter(function (c) {
      return dentro(c, V.fc) && cerca([c.nome, c.referente, c.email, c.telefono, c.citta, c.settore, c.note].concat(c.lavori.map(function (l) { return [l.fiera, l.titolo, l.luogo].join(' '); })));
    });
    $('#c-grid').innerHTML = cc.length ? cc.map(function (c) {
      var p = prossima(c), aperti = c.lavori.filter(function (l) { return ATTIVI[l.stato]; }).length;
      return '<div class="cl-c" data-c="' + c.id + '"><div class="t"><b>' + esc(c.nome) + '</b>' + badgeC(c.stato) + '</div>'
        + '<small>' + [c.referente, c.citta, c.settore].filter(Boolean).map(esc).join(' · ') + '</small>'
        + '<div class="nx">' + (c.lavori.length ? NF.format(c.lavori.length) + ' lavor' + (c.lavori.length === 1 ? 'o' : 'i') + (aperti ? ' (' + aperti + ' apert' + (aperti === 1 ? 'o' : 'i') + ')' : '') : '<span class="muted">nessun lavoro</span>') + '</div>'
        + (p ? '<div class="nx">' + chip(p.f, p.f.ic + ' ' + fd(p.da < OGGI ? OGGI : p.da)) + '<span>' + esc(nomeLav(p.l)) + '</span></div>' : '')
        + '<div class="acts" style="margin-top:2px">' + (c.telefono ? '<a class="ghost" href="tel:' + esc(tel(c.telefono)) + '">📞</a><a class="ghost" target="_blank" rel="noopener" href="' + wa(c.telefono) + '">💬</a>' : '') + (c.email ? '<a class="ghost" href="mailto:' + esc(c.email) + '">✉️</a>' : '') + '</div></div>';
    }).join('') : '<p class="empty">' + (D.clienti.length ? 'Nessun cliente trovato.' : 'Ancora nessun cliente. Iniziate con «＋ Nuovo cliente»: potete salvare anche i potenziali.') + '</p>';
    $$('#c-grid [data-c]').forEach(function (e) { e.onclick = function (ev) { if (ev.target.closest('a')) return; apriCliente(+e.dataset.c); }; });
  }

  /* ---------- lavori ---------- */
  function fineLav(l) { var f = fasiDi(l).map(function (x) { return x.a; }).sort(); return f[f.length - 1] || ''; }
  function lavori() {
    var segs = [['attivi', 'Da fare e in corso'], ['preventivo', 'Da confermare'], ['concluso', 'Conclusi'], ['tutti', 'Tutti']];
    var ok = function (l, k) { return k === 'tutti' || (k === 'attivi' ? !!ATTIVI[l.stato] : l.stato === k); };
    $('#l-seg').innerHTML = segs.map(function (s) { return '<button data-s="' + s[0] + '"' + (V.fl === s[0] ? ' class="on"' : '') + '>' + s[1] + ' <i>' + D.lavori.filter(function (l) { return ok(l, s[0]); }).length + '</i></button>'; }).join('');
    $$('#l-seg button').forEach(function (b) { b.onclick = function () { V.fl = b.dataset.s; lavori(); }; });
    var ll = D.lavori.filter(function (l) { var c = cliDi(l); return ok(l, V.fl) && cerca([c.nome, c.referente, c.telefono, l.fiera, l.titolo, l.luogo, l.stand, l.note]); });
    if (V.fl === 'concluso' || V.fl === 'tutti') ll = ll.slice().reverse();
    $('#l-tab').innerHTML = '<thead><tr><th>Cliente</th><th>Fiera / lavoro</th><th>Luogo</th><th>Date</th><th>Stato</th><th class="num">Valore</th></tr></thead><tbody>'
      + (ll.length ? ll.map(function (l) {
        var c = cliDi(l), fz = fasiDi(l), fin = fineLav(l);
        return '<tr data-l="' + l.id + '"' + (fin && fin < OGGI ? ' class="passato"' : '') + '><td><b>' + esc(c.nome || '—') + '</b>' + (c.referente ? '<br><small class="muted">' + esc(c.referente) + '</small>' : '') + '</td>'
          + '<td class="wrap"><b>' + esc(nomeLav(l)) + '</b>' + (l.fiera && l.titolo ? '<br><small>' + esc(l.titolo) + '</small>' : '') + (l.mq ? '<br><small class="muted">' + NF.format(+l.mq) + ' mq</small>' : '') + '</td>'
          + '<td class="wrap">' + esc(l.luogo || '') + (l.stand ? '<br><small class="muted">stand ' + esc(l.stand) + '</small>' : '') + '</td>'
          + '<td><div class="fasi-td">' + (fz.length ? fz.map(function (x) { return chip(x.f, x.f.ic + ' ' + fr(x.da, x.a)); }).join('') : '<span class="muted small">date da definire</span>') + '</div></td>'
          + '<td>' + badgeL(l.stato) + '</td><td class="num">' + (l.valore != null ? EUR.format(+l.valore) : '') + '</td></tr>';
      }).join('') : '<tr><td colspan="6" class="empty">' + (D.lavori.length ? 'Nessun lavoro in questa vista.' : 'Ancora nessun lavoro. Usate «＋ Nuovo lavoro».') + '</td></tr>') + '</tbody>';
    $$('#l-tab tbody tr[data-l]').forEach(function (tr) { tr.onclick = function () { apriLavoro(+tr.dataset.l); }; });
  }

  /* ---------- finestra cliente ---------- */
  function campo(nome, et, v, tipo, extra) { return '<label>' + et + '<input name="' + nome + '" type="' + (tipo || 'text') + '" value="' + esc(v == null ? '' : v) + '"' + (extra || '') + '></label>'; }
  function formCliente(c) {
    return '<form class="card m-form" id="c-form"><h3>' + (c.id ? 'Modifica cliente' : 'Nuovo cliente') + '</h3>'
      + '<div class="f2">' + campo('nome', 'Azienda o nome *', c.nome, 'text', ' required') + '<label>Stato<select name="stato">' + Object.keys(D.stati_c).map(function (k) { return '<option value="' + k + '"' + (k === (c.stato || 'potenziale') ? ' selected' : '') + '>' + esc(D.stati_c[k]) + '</option>'; }).join('') + '</select></label></div>'
      + '<div class="f2">' + campo('referente', 'Referente', c.referente) + campo('telefono', 'Telefono', c.telefono, 'tel') + '</div>'
      + '<div class="f2">' + campo('email', 'Email', c.email, 'email') + campo('citta', 'Città', c.citta) + '</div>'
      + '<div class="f3">' + campo('settore', 'Settore', c.settore) + campo('piva', 'P. IVA', c.piva) + campo('fonte', 'Come ci ha conosciuto', c.fonte) + '</div>'
      + '<label>Note<textarea name="note" rows="3">' + esc(c.note || '') + '</textarea></label>'
      + '<div class="acts"><button class="btn" type="submit">Salva</button>' + (c.id ? '<button class="btn danger" type="button" id="c-del">Elimina cliente</button>' : '') + '<span id="c-msg" class="muted small"></span></div></form>';
  }
  function dati(f) {
    var o = {};
    $$('input,select,textarea', f).forEach(function (e) { if (!e.name) return; o[e.name] = e.type === 'checkbox' ? e.checked : e.value; });
    return o;
  }
  function apriCliente(id, pre) {
    var c = id ? C[id] : (pre || {});
    if (id && !c) return;
    var h = '';
    if (c.id) {
      var ll = c.lavori.slice().sort(function (a, b) { return (fineLav(b) || '') < (fineLav(a) || '') ? -1 : 1; });
      h += '<div class="m-head"><h2>' + esc(c.nome) + '</h2>' + badgeC(c.stato) + '</div>'
        + '<div class="muted small">' + [c.referente, c.citta, c.settore].filter(Boolean).map(esc).join(' · ') + '</div>'
        + '<div class="acts">' + (c.telefono ? '<a class="ghost" href="tel:' + esc(tel(c.telefono)) + '">📞 ' + esc(c.telefono) + '</a><a class="ghost" target="_blank" rel="noopener" href="' + wa(c.telefono) + '">💬 WhatsApp</a>' : '') + (c.email ? '<a class="ghost" href="mailto:' + esc(c.email) + '">✉️ ' + esc(c.email) + '</a>' : '') + '</div>'
        + (c.note ? '<p class="quote" style="margin-top:12px">' + esc(c.note) + '</p>' : '')
        + '<h3>Lavori <button class="ghost" id="c-addl" style="float:right;font-size:12px;padding:3px 10px">＋ Aggiungi lavoro</button></h3>'
        + '<div class="lav-mini">' + (ll.length ? ll.map(function (l) {
          return '<div data-l="' + l.id + '"><b>' + esc(nomeLav(l)) + '</b> ' + badgeL(l.stato) + (l.valore != null ? ' <small class="muted">' + EUR.format(+l.valore) + '</small>' : '')
            + (l.luogo ? '<br><small class="muted">' + esc(l.luogo) + (l.stand ? ' · stand ' + esc(l.stand) : '') + '</small>' : '')
            + '<div class="fasi-leg">' + fasiDi(l).map(function (x) { return chip(x.f, x.f.ic + ' ' + fr(x.da, x.a)); }).join('') + '</div></div>';
        }).join('') : '<p class="muted small">Nessun lavoro ancora.</p>') + '</div>';
    }
    var b = modal(h + formCliente(c));
    if (c.id) {
      $('#c-addl', b).onclick = function () { apriLavoro(null, c.id); };
      $$('.lav-mini [data-l]', b).forEach(function (e) { e.onclick = function () { apriLavoro(+e.dataset.l); }; });
    }
    var f = $('#c-form', b);
    f.onsubmit = function (e) {
      e.preventDefault(); var bt = $('button[type=submit]', f); bt.disabled = true;
      var o = dati(f); if (!c.id && pre && pre.richiesta) o.richiesta = pre.richiesta;
      api('cliente_salva', c.id ? 'id=' + c.id : '', o).then(function (x) {
        bt.disabled = false;
        if (!x.ok) { $('#c-msg').textContent = x.errore || 'Errore'; return; }
        carica().then(function () { apriCliente(x.id); var m = $('#c-msg'); if (m) m.textContent = 'Salvato ✓'; });
      }).catch(function () { bt.disabled = false; $('#c-msg').textContent = 'Server non raggiungibile'; });
    };
    var del = $('#c-del', b);
    if (del) del.onclick = function () {
      if (!confirm('Eliminare ' + c.nome + (c.lavori.length ? ' e i suoi ' + c.lavori.length + ' lavori' : '') + '? Non si può annullare.')) return;
      api('cliente_elimina', 'id=' + c.id, {}).then(function () { chiudi(); carica(); });
    };
  }

  /* ---------- finestra lavoro ---------- */
  function apriLavoro(id, clienteId) {
    var l = id ? D.lavori.filter(function (x) { return +x.id === +id; })[0] : { cliente: clienteId || '', montaggio: 1, smontaggio: 1, produzione: 0, stato: 'preventivo' };
    if (!l) return;
    var c = cliDi(l);
    var opz = D.clienti.map(function (x) { return '<option value="' + x.id + '"' + (+x.id === +l.cliente ? ' selected' : '') + '>' + esc(x.nome) + '</option>'; }).join('');
    var box = function (f) {
      var on = attiva(l, f);
      return '<div class="fase-box ' + f.k + (on ? '' : ' off') + '">' + (f.flag ? '<label class="chk"><input type="checkbox" name="' + f.flag + '"' + (on ? ' checked' : '') + '> ' + f.ic + ' ' + f.nome + (f.k === 'prod' ? ' <small class="muted" style="font-weight:400">(lo produciamo noi)</small>' : '') + '</label>' : '<label class="chk" style="cursor:default">' + f.ic + ' ' + f.nome + '</label>')
        + '<div class="f2">' + campo(f.da, 'Dal', l[f.da], 'date') + campo(f.a, 'Al', l[f.a], 'date') + '</div></div>';
    };
    var b = modal((l.id ? '<div class="m-head"><h2>' + esc(nomeLav(l)) + '</h2>' + badgeL(l.stato) + '</div><div class="acts"><button class="ghost" id="l-cli">👤 ' + esc(c.nome || 'Cliente') + '</button>' + (c.telefono ? '<a class="ghost" href="tel:' + esc(tel(c.telefono)) + '">📞</a><a class="ghost" target="_blank" rel="noopener" href="' + wa(c.telefono) + '">💬</a>' : '') + '</div>' : '<h2>Nuovo lavoro</h2>')
      + '<form class="card m-form" id="l-form"><div class="f2"><label>Cliente *<select name="cliente" id="l-sel"><option value="">— scegliete —</option>' + opz + '<option value="__nuovo">＋ Nuovo cliente…</option></select></label>'
      + '<label>Stato<select name="stato">' + Object.keys(D.stati_l).map(function (k) { return '<option value="' + k + '"' + (k === l.stato ? ' selected' : '') + '>' + esc(D.stati_l[k]) + '</option>'; }).join('') + '</select></label></div>'
      + '<div id="l-nc" hidden>' + campo('nuovo_cliente', 'Nome del nuovo cliente', '') + '</div>'
      + '<div class="f2">' + campo('fiera', 'Fiera / evento', l.fiera, 'text', ' list="l-fiere" placeholder="es. MEDICA 2026"') + campo('titolo', 'Descrizione del lavoro', l.titolo, 'text', ' placeholder="es. stand a isola 6×8 con soppalco"') + '</div>'
      + '<datalist id="l-fiere">' + uniche('fiera').map(function (x) { return '<option value="' + esc(x) + '">'; }).join('') + '</datalist>'
      + '<div class="f3">' + campo('luogo', 'Luogo / quartiere fieristico', l.luogo, 'text', ' list="l-luoghi"') + campo('stand', 'Padiglione e stand', l.stand, 'text', ' placeholder="es. Pad. 6 – B21"') + campo('mq', 'Metri quadri', l.mq, 'number', ' min="0" step="0.5"') + '</div>'
      + '<datalist id="l-luoghi">' + uniche('luogo').map(function (x) { return '<option value="' + esc(x) + '">'; }).join('') + '</datalist>'
      + '<h3>Date <small class="muted" style="font-weight:400">— mettete le date della fiera: montaggio e smontaggio si propongono da soli, poi correggeteli</small></h3>'
      + '<div class="fasi-grid">' + [FASI[0], FASI[2], FASI[1], FASI[3]].map(box).join('') + '</div>'
      + '<div class="f2">' + campo('valore', 'Valore del lavoro in €', l.valore, 'number', ' min="0" step="1"') + '<span></span></div>'
      + '<label>Note (materiali, squadra, orari di accesso, contatti in fiera…)<textarea name="note" rows="3">' + esc(l.note || '') + '</textarea></label>'
      + '<div class="acts"><button class="btn" type="submit">Salva</button>' + (l.id ? '<button class="btn danger" type="button" id="l-del">Elimina lavoro</button>' : '') + '<span id="l-msg" class="muted small"></span></div></form>');
    var f = $('#l-form', b);
    var lc = $('#l-cli', b); if (lc) lc.onclick = function () { apriCliente(+l.cliente); };
    $('#l-sel', b).onchange = function () { $('#l-nc', b).hidden = this.value !== '__nuovo'; if (this.value === '__nuovo') f.nuovo_cliente.focus(); };
    $$('.fase-box input[type=checkbox]', f).forEach(function (cb) { cb.onchange = function () { cb.closest('.fase-box').classList.toggle('off', !cb.checked); proponi(); }; });
    // date della fiera → proposta: montaggio i 2 giorni prima, smontaggio l'ultimo giorno e il successivo, produzione i 10 giorni prima del montaggio
    var ed = f.evento_da, ea = f.evento_a;
    function proponi() {
      if (ed.value && (!ea.value || ea.value < ed.value)) ea.value = ed.value;
      if (ed.value && !f.mont_da.value) { f.mont_da.value = piu(ed.value, -2); f.mont_a.value = piu(ed.value, -1); }
      if (ea.value && !f.smont_da.value) { f.smont_da.value = ea.value; f.smont_a.value = piu(ea.value, 1); }
      if (f.mont_da.value && f.produzione.checked && !f.prod_da.value) { f.prod_da.value = piu(f.mont_da.value, -10); f.prod_a.value = piu(f.mont_da.value, -1); }
    }
    ed.addEventListener('change', proponi); ea.addEventListener('change', proponi);
    FASI.forEach(function (x) { f[x.da].addEventListener('change', function () { if (f[x.da].value && (!f[x.a].value || f[x.a].value < f[x.da].value)) f[x.a].value = f[x.da].value; }); });
    f.onsubmit = function (e) {
      e.preventDefault(); var bt = $('button[type=submit]', f), msg = $('#l-msg', b); bt.disabled = true;
      var o = dati(f), prima = Promise.resolve(o.cliente);
      if (o.cliente === '__nuovo') {
        if (!o.nuovo_cliente.trim()) { bt.disabled = false; msg.textContent = 'Scrivete il nome del nuovo cliente.'; return; }
        prima = api('cliente_salva', '', { nome: o.nuovo_cliente, stato: o.stato === 'preventivo' ? 'trattativa' : 'attivo' }).then(function (x) { if (!x.ok) throw new Error(x.errore); return x.id; });
      } else if (!o.cliente) { bt.disabled = false; msg.textContent = 'Scegliete il cliente.'; return; }
      prima.then(function (cid) { o.cliente = cid; delete o.nuovo_cliente; return api('lavoro_salva', l.id ? 'id=' + l.id : '', o); })
        .then(function (x) {
          bt.disabled = false;
          if (!x.ok) { msg.textContent = x.errore || 'Errore'; return; }
          carica().then(function () { apriLavoro(x.id); var m = $('#l-msg'); if (m) m.textContent = 'Salvato ✓'; });
        }).catch(function (er) { bt.disabled = false; msg.textContent = er && er.message && er.message !== 'Failed to fetch' ? er.message : 'Server non raggiungibile'; });
    };
    var del = $('#l-del', b);
    if (del) del.onclick = function () { if (!confirm('Eliminare il lavoro «' + nomeLav(l) + '»?')) return; api('lavoro_elimina', 'id=' + l.id, {}).then(function () { chiudi(); carica(); }); };
  }
  function uniche(k) { var s = {}; D.lavori.forEach(function (l) { if (l[k]) s[l[k]] = 1; }); return Object.keys(s).sort(); }

  /* ---------- calendario sul telefono ---------- */
  function apriIcs() {
    if (!D.ics) { modal('<h2>📅 Calendario sul telefono</h2><p class="muted">Disponibile dopo aver aggiornato la funzione «ds» su Supabase.</p>'); return; }
    var url = new URL(PDADM.url('a=x')).origin + D.ics, web = url.replace(/^https:/, 'webcal:');
    var b = modal('<h2>📅 Montaggi e smontaggi nel calendario del telefono</h2>'
      + '<p class="muted small" style="margin-top:6px">Il calendario si aggiorna da solo: ogni lavoro che salvate qui compare sul telefono (produzione, montaggio, fiera, smontaggio). Non condividete il link: chi lo ha vede le date e i nomi dei clienti.</p>'
      + '<div class="ics-box" style="margin-top:12px"><a class="btn" href="' + esc(web) + '" style="text-align:center;text-decoration:none">Iscriviti (iPhone / Mac)</a>'
      + '<input readonly value="' + esc(url) + '" id="ics-u"><div class="acts"><button class="ghost" id="ics-c">Copia il link</button><a class="ghost" target="_blank" rel="noopener" href="https://calendar.google.com/calendar/u/0/r/settings/addbyurl">Google Calendar → Da URL</a></div>'
      + '<p class="small muted">Google Calendar: aprite il link qui sopra dal computer, incollate l\'indirizzo e confermate. Google aggiorna i calendari esterni ogni qualche ora.</p></div>');
    $('#ics-c', b).onclick = function () { var i = $('#ics-u', b); i.select(); try { navigator.clipboard.writeText(i.value); } catch (e) { document.execCommand('copy'); } this.textContent = 'Copiato ✓'; };
  }

  /* da Richieste: "Salva tra i clienti" */
  window.DSClienti = {
    daRichiesta: function (r) {
      apriCliente(null, { nome: r.azienda || r.nome || '', referente: r.azienda ? r.nome : '', email: r.email, telefono: r.telefono, citta: r.citta, fonte: 'Richiesta dal sito' + (r.sorgente ? ' (' + r.sorgente + ')' : ''), stato: 'trattativa', richiesta: r.id,
        note: [r.fiera ? 'Fiera: ' + r.fiera : '', r.urgenza ? 'Quando: ' + r.urgenza : '', r.messaggio || ''].filter(Boolean).join('\n') });
    }
  };

  var fatto = false;
  function apriScheda(t) { if (t !== 'clienti') return; OGGI = ds(new Date()); if (!fatto) { fatto = true; init(); } else carica(); }
  document.addEventListener('pd-tab', function (e) { apriScheda(e.detail); });
  var att = $('.tabs button.on'); if (att) apriScheda(att.dataset.tab);
})();
