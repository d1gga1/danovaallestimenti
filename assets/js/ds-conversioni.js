/* Danova Stand — più richieste dal sito (caricato da ds-live.js, 22/11/2026).
   1) Popup "−3% con la newsletter": sconto sull'allestimento, valido 30 giorni dal ricevimento del codice.
      L'iscrizione arriva via email a info@danova-tech.com (FormSubmit, con risposta automatica al cliente
      che contiene il codice) e finisce anche nella scheda Richieste dell'area privata (copia fatta da ds-live.js).
   2) Fascia "Preventivo gratuito" a metà delle pagine lunghe (fiere, servizi, guide, città…).
   3) Fumetto accanto al pulsante WhatsApp dopo un po' che la persona legge.
   Ogni parte si spegne mettendo false qui sotto. */
(function () {
  'use strict';
  if (window.__dsConv) return; window.__dsConv = 1;
  var ATTIVO = { popup: true, fascia: true, fumetto: true };
  var SCONTO = { perc: 3, giorni: 30, mail: 'info@danova-tech.com', wa: '393884706887' };

  var P = location.pathname;
  if (/^\/(private_area|render)(\/|$)/.test(P)) return;
  var LEGALE = /(^|\/)(privacy|privacidad|confidentialite|datenschutz|cookie-policy|cookie-richtlinie|cookies|termini|agb|terms)(\/|$)/.test(P);
  var CONTATTI = /(^|\/)(contatti|kontakt|contact|contacto)(\/|$)/.test(P);

  var LS = null, SS = null; try { LS = localStorage; SS = sessionStorage; } catch (e) {}
  var lg = function (k) { try { return LS ? LS.getItem(k) : null; } catch (e) { return null; } };
  var ls = function (k, v) { try { if (LS) LS.setItem(k, v); } catch (e) {} };
  var sg = function (k) { try { return SS ? SS.getItem(k) : null; } catch (e) { return null; } };
  var ss = function (k, v) { try { if (SS) SS.setItem(k, v); } catch (e) {} };
  var ev = function (t, x) { try { if (window.dsEvento) window.dsEvento(t, x); } catch (e) {} };
  var esc = function (s) { return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]; }); };

  var L = String(document.documentElement.lang || 'it').slice(0, 2).toLowerCase();
  var TX = {
    it: { vs: 'sul tuo allestimento, valido 30 giorni', k: 'Solo per chi si iscrive', h: '−3% sul tuo prossimo allestimento', s: 'Iscriviti alla newsletter di Danova Stand: ti mandiamo subito il codice sconto, da usare entro 30 giorni dal ricevimento.',
      li: ['Stand chiavi in mano in Italia e in Europa', 'Preventivo gratuito entro 24 ore lavorative', 'Calendario fiere e idee per lo stand'],
      nome: 'Nome e cognome', az: 'Azienda', mail: 'Email', tel: 'Telefono (facoltativo)', fiera: 'A quale fiera parteciperai? (facoltativo)', fieraPh: 'es. Vinitaly 2027',
      ok: 'Acconsento a ricevere la newsletter e le offerte di Danova Stand e a essere ricontattato per la mia richiesta. Ho letto l\'<a href="/privacy/" target="_blank" rel="noopener">informativa privacy</a>.',
      btn: 'Voglio il codice sconto', no: 'No grazie', e1: 'Scrivi il tuo nome.', e2: 'Inserisci un\'email valida.', e3: 'Spunta il consenso per ricevere il codice.', inv: 'Invio in corso…',
      fatto: 'Fatto! Ecco il tuo codice', fattoS: 'Te l\'abbiamo mandato anche via email. Comunicacelo quando confermi il preventivo: vale fino al ', copia: 'Copia', copiato: 'Copiato ✓',
      prev: 'Richiedi subito il preventivo', pill: 'con la newsletter',
      fT: 'Stai preparando una fiera?', fS: 'Raccontaci fiera, metri quadri e idee: preventivo gratuito entro 24 ore lavorative, con un solo referente dal progetto allo smontaggio.', fB: 'Richiedi un preventivo', fW: 'Scrivici su WhatsApp', fN: 'oppure iscriviti e ricevi il −3%',
      bolla: 'Hai una fiera in arrivo? Scrivici su WhatsApp: ti rispondiamo noi.',
      waTxt: 'Ciao Danova Stand! Vi scrivo dal sito danovastand.com: vorrei un preventivo per uno stand.' },
    en: { vs: 'off your stand, valid for 30 days', k: 'For subscribers only', h: '3% off your next exhibition stand', s: 'Subscribe to the Danova Stand newsletter: we send you the discount code right away, valid for 30 days from receipt.',
      li: ['Turnkey stands in Italy and across Europe', 'Free quote within 24 working hours', 'Trade fair calendar and stand ideas'],
      nome: 'Full name', az: 'Company', mail: 'Email', tel: 'Phone (optional)', fiera: 'Which trade fair are you exhibiting at? (optional)', fieraPh: 'e.g. Vinitaly 2027',
      ok: 'I agree to receive the Danova Stand newsletter and offers and to be contacted about my request. I have read the <a href="/en/privacy/" target="_blank" rel="noopener">privacy notice</a>.',
      btn: 'Send me the code', no: 'No thanks', e1: 'Please enter your name.', e2: 'Please enter a valid email.', e3: 'Please tick the consent box to receive the code.', inv: 'Sending…',
      fatto: 'Done! Here is your code', fattoS: 'We have also sent it by email. Mention it when you confirm the quote: valid until ', copia: 'Copy', copiato: 'Copied ✓',
      prev: 'Request a quote now', pill: 'with the newsletter',
      fT: 'Preparing for a trade fair?', fS: 'Tell us the fair, the size and your ideas: free quote within 24 working hours, one contact from design to dismantling.', fB: 'Request a quote', fW: 'Message us on WhatsApp', fN: 'or subscribe and get 3% off',
      bolla: 'Got a trade fair coming up? Message us on WhatsApp.',
      waTxt: 'Hello Danova Stand! I am writing from danovastand.com: I would like a quote for a stand.' },
    de: { vs: 'auf Ihren Messestand, 30 Tage gültig', k: 'Nur für Abonnenten', h: '3 % Rabatt auf Ihren nächsten Messestand', s: 'Abonnieren Sie den Newsletter von Danova Stand: Sie erhalten sofort den Rabattcode, gültig 30 Tage ab Erhalt.',
      li: ['Messestände schlüsselfertig in Italien und Europa', 'Kostenloses Angebot innerhalb von 24 Arbeitsstunden', 'Messekalender und Ideen für den Stand'],
      nome: 'Vor- und Nachname', az: 'Firma', mail: 'E-Mail', tel: 'Telefon (optional)', fiera: 'Auf welcher Messe stellen Sie aus? (optional)', fieraPh: 'z. B. Vinitaly 2027',
      ok: 'Ich möchte den Newsletter und Angebote von Danova Stand erhalten und zu meiner Anfrage kontaktiert werden. Ich habe die <a href="/de/datenschutz/" target="_blank" rel="noopener">Datenschutzerklärung</a> gelesen.',
      btn: 'Rabattcode erhalten', no: 'Nein danke', e1: 'Bitte geben Sie Ihren Namen ein.', e2: 'Bitte geben Sie eine gültige E-Mail ein.', e3: 'Bitte stimmen Sie zu, um den Code zu erhalten.', inv: 'Wird gesendet…',
      fatto: 'Fertig! Ihr Code', fattoS: 'Wir haben ihn auch per E-Mail geschickt. Nennen Sie ihn bei der Auftragsbestätigung: gültig bis ', copia: 'Kopieren', copiato: 'Kopiert ✓',
      prev: 'Jetzt Angebot anfordern', pill: 'mit dem Newsletter',
      fT: 'Sie planen eine Messe?', fS: 'Nennen Sie uns Messe, Fläche und Ideen: kostenloses Angebot innerhalb von 24 Arbeitsstunden, ein Ansprechpartner vom Entwurf bis zum Abbau.', fB: 'Angebot anfordern', fW: 'Per WhatsApp schreiben', fN: 'oder abonnieren und 3 % sparen',
      bolla: 'Steht eine Messe an? Schreiben Sie uns auf WhatsApp.',
      waTxt: 'Hallo Danova Stand! Ich schreibe über danovastand.com: Ich hätte gern ein Angebot für einen Messestand.' },
    fr: { vs: 'sur votre stand, valable 30 jours', k: 'Réservé aux abonnés', h: '−3 % sur votre prochain stand', s: 'Abonnez-vous à la newsletter de Danova Stand : nous vous envoyons tout de suite le code de réduction, valable 30 jours après réception.',
      li: ['Stands clés en main en Italie et en Europe', 'Devis gratuit sous 24 heures ouvrées', 'Calendrier des salons et idées de stand'],
      nome: 'Nom et prénom', az: 'Entreprise', mail: 'E-mail', tel: 'Téléphone (facultatif)', fiera: 'À quel salon exposez-vous ? (facultatif)', fieraPh: 'ex. Vinitaly 2027',
      ok: 'J\'accepte de recevoir la newsletter et les offres de Danova Stand et d\'être recontacté pour ma demande. J\'ai lu la <a href="/fr/confidentialite/" target="_blank" rel="noopener">politique de confidentialité</a>.',
      btn: 'Recevoir le code', no: 'Non merci', e1: 'Indiquez votre nom.', e2: 'Indiquez un e-mail valide.', e3: 'Cochez la case de consentement pour recevoir le code.', inv: 'Envoi…',
      fatto: 'C\'est fait ! Voici votre code', fattoS: 'Nous vous l\'avons aussi envoyé par e-mail. Indiquez-le en confirmant le devis : valable jusqu\'au ', copia: 'Copier', copiato: 'Copié ✓',
      prev: 'Demander un devis', pill: 'avec la newsletter',
      fT: 'Vous préparez un salon ?', fS: 'Dites-nous le salon, la surface et vos idées : devis gratuit sous 24 heures ouvrées, un seul interlocuteur du projet au démontage.', fB: 'Demander un devis', fW: 'Écrire sur WhatsApp', fN: 'ou abonnez-vous et obtenez −3 %',
      bolla: 'Un salon approche ? Écrivez-nous sur WhatsApp.',
      waTxt: 'Bonjour Danova Stand ! Je vous écris depuis danovastand.com : je voudrais un devis pour un stand.' },
    es: { vs: 'en tu stand, válido 30 días', k: 'Solo para suscriptores', h: '−3% en tu próximo stand', s: 'Suscríbete a la newsletter de Danova Stand: te enviamos ya el código de descuento, válido 30 días desde que lo recibes.',
      li: ['Stands llave en mano en Italia y Europa', 'Presupuesto gratis en 24 horas laborables', 'Calendario de ferias e ideas para tu stand'],
      nome: 'Nombre y apellidos', az: 'Empresa', mail: 'Email', tel: 'Teléfono (opcional)', fiera: '¿En qué feria vas a exponer? (opcional)', fieraPh: 'p. ej. Vinitaly 2027',
      ok: 'Acepto recibir la newsletter y las ofertas de Danova Stand y que me contacten por mi solicitud. He leído la <a href="/es/privacidad/" target="_blank" rel="noopener">política de privacidad</a>.',
      btn: 'Quiero el código', no: 'No, gracias', e1: 'Escribe tu nombre.', e2: 'Introduce un email válido.', e3: 'Marca el consentimiento para recibir el código.', inv: 'Enviando…',
      fatto: '¡Listo! Este es tu código', fattoS: 'También te lo hemos enviado por email. Indícalo al confirmar el presupuesto: válido hasta el ', copia: 'Copiar', copiato: 'Copiado ✓',
      prev: 'Pedir presupuesto ahora', pill: 'con la newsletter',
      fT: '¿Preparas una feria?', fS: 'Cuéntanos la feria, los metros y tus ideas: presupuesto gratis en 24 horas laborables, un solo interlocutor del proyecto al desmontaje.', fB: 'Pedir presupuesto', fW: 'Escríbenos por WhatsApp', fN: 'o suscríbete y consigue un −3%',
      bolla: '¿Tienes una feria pronto? Escríbenos por WhatsApp.',
      waTxt: '¡Hola Danova Stand! Os escribo desde danovastand.com: quiero un presupuesto para un stand.' }
  };
  var T = TX[L] || TX.en;

  var CHECK = '<svg viewBox="0 0 24 24"><path d="M5 12.5l4.5 4.5L19 7.5"/></svg>';
  var CSS = '.dsnl{position:fixed;inset:0;z-index:2147483100;display:none;font-family:Inter,system-ui,sans-serif}.dsnl.open{display:block}'
    + '.dsnl-scrim{position:absolute;inset:0;background:rgba(5,6,10,.7);backdrop-filter:blur(6px);-webkit-backdrop-filter:blur(6px);opacity:0;transition:opacity .35s}.dsnl.show .dsnl-scrim{opacity:1}'
    + '.dsnl-box{position:absolute;left:50%;top:50%;width:min(880px,calc(100% - 28px));max-height:calc(100% - 28px);overflow:auto;background:#0f0d07;color:#e9edf7;border:1px solid rgba(255,217,122,.28);border-radius:22px;display:grid;grid-template-columns:1fr 1.15fr;box-shadow:0 30px 90px rgba(0,0,0,.6);opacity:0;transform:translate(-50%,-46%);transition:opacity .35s,transform .35s}'
    + '.dsnl.show .dsnl-box{opacity:1;transform:translate(-50%,-50%)}'
    + '.dsnl-x{position:absolute;top:12px;right:12px;z-index:2;width:38px;height:38px;border-radius:50%;border:1px solid rgba(255,255,255,.15);background:rgba(255,255,255,.06);color:#e9edf7;font:400 24px/1 sans-serif;cursor:pointer}'
    + '.dsnl-vis{position:relative;padding:34px 28px;display:flex;flex-direction:column;justify-content:space-between;gap:24px;background:radial-gradient(120% 90% at 0% 0%,rgba(255,201,60,.28),transparent 60%),linear-gradient(160deg,#1a1508,#0b0904)}'
    + '.dsnl-vis small{display:block;font:700 12px/1 Inter,sans-serif;letter-spacing:.14em;text-transform:uppercase;color:#FFC93C}'
    + '.dsnl-vis b.big{display:block;font:700 clamp(84px,11vw,128px)/.9 Sora,system-ui,sans-serif;letter-spacing:-.05em;margin:12px 0 4px;color:#FFC93C}.dsnl-vis b.big i{font-style:normal;font-size:.5em;vertical-align:.6em}'
    + '.dsnl-vis span.sub{font:600 19px/1.25 Sora,system-ui,sans-serif}.dsnl-vis ul{list-style:none;margin:0;padding:0;display:grid;gap:9px;font:600 14px Inter,sans-serif}.dsnl-vis li{display:flex;gap:9px;align-items:center}'
    + '.dsnl svg{width:18px;height:18px;stroke:#FFC93C;fill:none;stroke-width:2.6;flex:none}'
    + '.dsnl-f{padding:30px 28px 22px;display:flex;flex-direction:column;gap:11px}'
    + '.dsnl-f h2{font:700 clamp(23px,2.8vw,30px)/1.1 Sora,system-ui,sans-serif;margin:0;padding-right:40px;color:#fff}.dsnl-sub{margin:0;color:#b9bfcc;line-height:1.5;font-size:14px}'
    + '.dsnl-g{display:grid;grid-template-columns:1fr 1fr;gap:9px}.dsnl-g label{display:grid;gap:4px;font:600 12px Inter,sans-serif;color:#b9bfcc}.dsnl-g .w{grid-column:1/-1}'
    + '.dsnl-g input{width:100%;box-sizing:border-box;border:1px solid rgba(255,255,255,.16);border-radius:11px;padding:11px 12px;font:500 15px Inter,sans-serif;color:#fff;background:rgba(255,255,255,.04)}'
    + '.dsnl-g input:focus{outline:0;border-color:#FFC93C}.dsnl .err{border-color:#ff8b98!important}'
    + '.dsnl-ok{display:flex;gap:9px;align-items:flex-start;font-size:12px;line-height:1.5;color:#b9bfcc;cursor:pointer}.dsnl-ok input{width:18px;height:18px;margin:1px 0 0;flex:none;accent-color:#FFC93C}.dsnl-ok input.err{outline:2px solid #ff8b98}.dsnl-ok a{color:#ffe49f}'
    + '.dsnl-e{margin:0;color:#ff8b98;font-size:13.5px;font-weight:600}.dsnl-e:empty{display:none}'
    + '.dsnl-b{width:100%;border:0;border-radius:999px;padding:15px 20px;background:#FFC93C;color:#0b0b0b;font:700 15.5px Inter,sans-serif;cursor:pointer;text-align:center;text-decoration:none;display:block}.dsnl-b:disabled{opacity:.6}'
    + '.dsnl-no{border:0;background:none;color:#8a8f99;font:600 13px Inter,sans-serif;cursor:pointer;padding:4px;align-self:center;text-decoration:underline}'
    + '.dsnl-code{display:flex;gap:10px;align-items:center;border:2px dashed #FFC93C;border-radius:14px;padding:12px 14px;justify-content:space-between}.dsnl-code b{font:700 22px ui-monospace,monospace;letter-spacing:.06em;color:#FFC93C}'
    + '.dsnl-code button{border:1px solid rgba(255,255,255,.3);background:transparent;color:#fff;border-radius:999px;padding:8px 14px;font:600 13px Inter,sans-serif;cursor:pointer}'
    + '.dsnl-pill{position:fixed;left:16px;bottom:16px;z-index:2147482000;display:flex;align-items:center;gap:8px;border:1px solid rgba(255,217,122,.3);border-radius:999px;padding:7px 15px 7px 7px;background:rgba(15,13,7,.95);color:#fff;font:600 13px Inter,sans-serif;cursor:pointer;box-shadow:0 10px 30px rgba(0,0,0,.4)}'
    + '.dsnl-pill b{background:#FFC93C;color:#0b0b0b;border-radius:999px;padding:6px 10px}'
    + '.ds-fascia{margin:10px auto 40px}.ds-fascia .ds-f-in{display:flex;gap:22px;align-items:center;justify-content:space-between;flex-wrap:wrap;padding:26px 28px;border:1px solid rgba(255,217,122,.28);border-radius:20px;background:radial-gradient(120% 140% at 0% 0%,rgba(255,201,60,.16),transparent 55%),rgba(255,255,255,.02)}'
    + '.ds-fascia h3{margin:0 0 6px;font:700 22px/1.2 Sora,system-ui,sans-serif;color:#fff}.ds-fascia p{margin:0;max-width:620px;color:#b9bfcc;font-size:15px;line-height:1.55}'
    + '.ds-fascia .ds-f-b{display:flex;gap:10px;flex-wrap:wrap;align-items:center}.ds-fascia .ds-f-w{display:inline-flex;align-items:center;gap:8px;padding:12px 18px;border-radius:999px;border:1px solid rgba(255,255,255,.2);color:#e9edf7;text-decoration:none;font-weight:600;font-size:14px}'
    + '.ds-fascia .ds-f-n{display:block;margin-top:8px;font-size:13px;color:#ffe49f;background:none;border:0;padding:0;cursor:pointer;text-decoration:underline;font-family:inherit}'
    + '.ds-bolla{position:fixed;z-index:2147481000;max-width:250px;padding:12px 32px 12px 14px;border-radius:14px 14px 4px 14px;background:#fff;color:#0b0b0b;font:600 13.5px/1.4 Inter,sans-serif;box-shadow:0 12px 34px rgba(0,0,0,.4);cursor:pointer;opacity:0;transform:translateY(8px);transition:opacity .35s,transform .35s}'
    + '.ds-bolla.on{opacity:1;transform:none}.ds-bolla button{position:absolute;top:4px;right:6px;border:0;background:none;font:400 18px/1 sans-serif;color:#555;cursor:pointer}'
    + '@media(max-width:760px){.dsnl-box{grid-template-columns:1fr;top:auto;bottom:0;left:0;width:100%;max-height:92%;border-radius:22px 22px 0 0;transform:translateY(30px)}.dsnl.show .dsnl-box{transform:none}'
    + '.dsnl-vis{padding:22px 20px;gap:8px}.dsnl-vis ul{display:none}.dsnl-vis b.big{font-size:64px}.dsnl-f{padding:20px 18px 18px}.dsnl-g{grid-template-columns:1fr}'
    + '.dsnl-pill{bottom:calc(84px + env(safe-area-inset-bottom));left:10px}.ds-fascia .ds-f-in{padding:20px}.ds-bolla{display:none}}';
  var st = document.createElement('style'); st.id = 'ds-conv-css'; st.textContent = CSS; (document.head || document.documentElement).appendChild(st);

  /* chi ha già lasciato i dati non va disturbato con il popup */
  var iscritto = function () { return !!lg('ds_nl'); };
  var haScritto = function () { return !!lg('ds_rq') || iscritto(); };
  var vid = function () { try { return window.dsVisitatore ? window.dsVisitatore() : ''; } catch (e) { return ''; } };
  var codice = function () { var r = (vid() || Math.random().toString(16).slice(2)).slice(0, 6).toUpperCase(); return 'DANOVA3-' + r; };
  var dataIt = function (d) { return ('0' + d.getDate()).slice(-2) + '/' + ('0' + (d.getMonth() + 1)).slice(-2) + '/' + d.getFullYear(); };
  var bersaglio = function () { return document.getElementById('richiesta') || document.getElementById('dt-scrivi') || document.querySelector('form.fr-req,form.dt-lead'); };
  var vaiAlModulo = function (da) {
    ev('preventivo', da);
    var b = bersaglio();
    if (b) { b.scrollIntoView({ behavior: 'smooth', block: 'start' }); setTimeout(function () { var i = b.querySelector && b.querySelector('input:not([type=hidden]),textarea'); if (i) try { i.focus({ preventScroll: true }); } catch (e) {} }, 700); }
    else location.href = { en: '/en/contact/', de: '/de/kontakt/', fr: '/fr/contact/', es: '/es/contacto/' }[L] || '/contatti/';
  };
  var linkWa = function () { var u = 'https://wa.me/' + SCONTO.wa + '?text=' + encodeURIComponent(T.waTxt); try { return window.dsConRif ? window.dsConRif(u) : u; } catch (e) { return u; } };

  /* ================= 1) popup newsletter −3% ================= */
  var BOX = null, PILL = null;
  function costruisci() {
    if (BOX) return BOX;
    BOX = document.createElement('div'); BOX.className = 'dsnl'; BOX.setAttribute('role', 'dialog'); BOX.setAttribute('aria-modal', 'true'); BOX.setAttribute('aria-label', T.h);
    BOX.innerHTML = '<div class="dsnl-scrim"></div><div class="dsnl-box"><button type="button" class="dsnl-x" aria-label="Chiudi">×</button>'
      + '<div class="dsnl-vis"><div><small>' + esc(T.k) + '</small><b class="big">−' + SCONTO.perc + '<i>%</i></b><span class="sub">' + esc(T.vs) + '</span></div><ul>' + T.li.map(function (x) { return '<li>' + CHECK + esc(x) + '</li>'; }).join('') + '</ul></div>'
      + '<div class="dsnl-f"><form novalidate><h2>' + esc(T.h) + '</h2><p class="dsnl-sub">' + esc(T.s) + '</p>'
      + '<div class="dsnl-g"><label class="w">' + esc(T.nome) + '<input name="nome" autocomplete="name" required></label>'
      + '<label>' + esc(T.mail) + '<input name="email" type="email" autocomplete="email" required></label>'
      + '<label>' + esc(T.az) + '<input name="azienda" autocomplete="organization"></label>'
      + '<label>' + esc(T.tel) + '<input name="tel" type="tel" autocomplete="tel"></label>'
      + '<label>' + esc(T.fiera) + '<input name="fiera" placeholder="' + esc(T.fieraPh) + '"></label></div>'
      + '<input type="text" name="_honey" tabindex="-1" autocomplete="off" style="position:absolute;left:-9999px;width:1px;height:1px;opacity:0">'
      + '<label class="dsnl-ok"><input type="checkbox" name="consenso"><span>' + T.ok + '</span></label>'
      + '<p class="dsnl-e" aria-live="polite"></p><button class="dsnl-b" type="submit">' + esc(T.btn) + '</button><button type="button" class="dsnl-no">' + esc(T.no) + '</button></form></div></div>';
    document.body.appendChild(BOX);
    BOX.querySelector('.dsnl-x').onclick = function () { chiudi(true); };
    BOX.querySelector('.dsnl-no').onclick = function () { chiudi(true); };
    BOX.querySelector('.dsnl-scrim').onclick = function () { chiudi(true); };
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && BOX.classList.contains('open')) chiudi(true); });
    BOX.querySelector('form').addEventListener('submit', invia);
    BOX.addEventListener('input', function (e) { if (e.target.classList) e.target.classList.remove('err'); BOX.querySelector('.dsnl-e').textContent = ''; });
    return BOX;
  }
  function apri(da) {
    if (iscritto()) return;
    costruisci(); BOX.classList.add('open'); requestAnimationFrame(function () { BOX.classList.add('show'); });
    ss('ds_nl_vista', '1'); if (PILL) PILL.hidden = true;
    ev('preventivo', 'popup −' + SCONTO.perc + '% aperto' + (da ? ' (' + da + ')' : ''));
    setTimeout(function () { var i = BOX.querySelector('input[name=nome]'); if (i && window.innerWidth > 760) i.focus(); }, 350);
  }
  function chiudi(rifiutato) {
    if (!BOX) return;
    BOX.classList.remove('show'); setTimeout(function () { BOX.classList.remove('open'); }, 300);
    if (rifiutato && !iscritto()) { ls('ds_nl_no', String(Date.now())); pillola(); }
  }
  function pillola() {
    if (iscritto() || LEGALE) return;
    if (!PILL) { PILL = document.createElement('button'); PILL.type = 'button'; PILL.className = 'dsnl-pill'; PILL.innerHTML = '<b>−' + SCONTO.perc + '%</b><span>' + esc(T.pill) + '</span>'; PILL.onclick = function () { apri('pulsante'); }; document.body.appendChild(PILL); }
    PILL.hidden = !!document.querySelector('[aria-label="Cookie"]');
  }
  function invia(e) {
    e.preventDefault();
    var f = e.target, g = function (n) { return String((f.elements[n] || {}).value || '').trim(); }, err = BOX.querySelector('.dsnl-e');
    if (g('_honey')) return;
    var bad = function (n, msg) { var el = f.elements[n]; if (el) { el.classList.add('err'); el.focus(); } err.textContent = msg; };
    if (g('nome').length < 2) return bad('nome', T.e1);
    if (!/^[^@\s]+@[^@\s]+\.[^@\s]{2,}$/.test(g('email'))) return bad('email', T.e2);
    if (!f.elements.consenso.checked) return bad('consenso', T.e3);
    var b = f.querySelector('.dsnl-b'); b.disabled = true; b.textContent = T.inv;
    var cod = codice(), scad = new Date(Date.now() + SCONTO.giorni * 864e5), ora = new Date();
    var nome1 = g('nome').split(/\s+/)[0];
    var corpo = {
      _subject: '📰 Iscrizione newsletter −' + SCONTO.perc + '%: ' + g('nome') + (g('azienda') ? ' (' + g('azienda') + ')' : '') + (g('fiera') ? ' · ' + g('fiera') : ''),
      _template: 'table', _captcha: 'false',
      _autoresponse: (L === 'it'
        ? 'Ciao ' + nome1 + ', grazie per esserti iscritto alla newsletter di Danova Stand!\n\nEcco il tuo codice sconto: ' + cod + '\n−' + SCONTO.perc + '% sul tuo allestimento, valido ' + SCONTO.giorni + ' giorni: fino al ' + dataIt(scad) + '.\nComunicacelo quando ci chiedi o confermi il preventivo.\n\nRaccontaci fiera, metri quadri e idee rispondendo a questa email o su WhatsApp (+39 388 470 6887): ti mandiamo il preventivo gratuito entro 24 ore lavorative.\n\nDanova Stand — danovastand.com'
        : 'Hello ' + nome1 + ', thank you for subscribing to the Danova Stand newsletter!\n\nYour discount code: ' + cod + '\n' + SCONTO.perc + '% off your exhibition stand, valid for ' + SCONTO.giorni + ' days: until ' + dataIt(scad) + '.\nMention it when you request or confirm your quote.\n\nTell us the fair, the size and your ideas by replying to this email or on WhatsApp (+39 388 470 6887): free quote within 24 working hours.\n\nDanova Stand — danovastand.com'),
      'Nome': g('nome'), email: g('email'), 'Azienda': g('azienda'), 'Telefono': g('tel'), 'Fiera': g('fiera'),
      'Tipo': 'Iscrizione newsletter (popup −' + SCONTO.perc + '%)', 'Codice sconto': cod, 'Valido fino al': dataIt(scad),
      'Consenso newsletter': 'Sì, ' + dataIt(ora) + ' ' + ('0' + ora.getHours()).slice(-2) + ':' + ('0' + ora.getMinutes()).slice(-2), 'Lingua': L.toUpperCase(),
      'Pagina': location.href.split('#')[0]
    };
    for (var k in corpo) if (corpo[k] === '') delete corpo[k];
    /* fetch: ds-live.js ne salva una copia nella scheda Richieste dell'area privata */
    var fatto = false, finito = function () {
      if (fatto) return; fatto = true;
      ls('ds_nl', JSON.stringify({ t: Date.now(), c: cod, s: scad.getTime() })); ls('ds_rq', '1');
      ev('iscrizione', 'newsletter −' + SCONTO.perc + '% · ' + cod);
      try { if (window.gtag) window.gtag('event', 'generate_lead', { method: 'newsletter_popup' }); } catch (x) {}
      grazie(cod, scad);
    };
    fetch('https://formsubmit.co/ajax/' + SCONTO.mail, { method: 'POST', headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' }, body: JSON.stringify(corpo) })
      .then(finito, finito);
    setTimeout(finito, 5000);   // il codice si mostra comunque
  }
  function grazie(cod, scad) {
    var f = BOX.querySelector('.dsnl-f');
    f.innerHTML = '<h2>' + esc(T.fatto) + '</h2><div class="dsnl-code"><b>' + esc(cod) + '</b><button type="button">' + esc(T.copia) + '</button></div>'
      + '<p class="dsnl-sub">' + esc(T.fattoS) + '<b style="color:#fff">' + dataIt(scad) + '</b>.</p>'
      + '<a class="dsnl-b" href="#">' + esc(T.prev) + ' →</a><a class="dsnl-no" href="' + esc(linkWa()) + '" target="_blank" rel="noopener">' + esc(T.fW) + '</a>';
    f.querySelector('.dsnl-code button').onclick = function () { var bt = this; try { navigator.clipboard.writeText(cod).then(function () { bt.textContent = T.copiato; }); } catch (e) {} };
    f.querySelector('a.dsnl-b').onclick = function (e) { e.preventDefault(); chiudi(false); setTimeout(function () { vaiAlModulo('dopo l\'iscrizione'); }, 320); };
    if (PILL) PILL.remove(), PILL = null;
  }
  window.dsSconto = function () { apri('link'); };
  document.addEventListener('click', function (e) { var a = e.target.closest && e.target.closest('a[href="#sconto"]'); if (a) { e.preventDefault(); apri('link'); } }, true);

  /* quando mostrarlo: una volta per visita, dopo 30 s sulla pagina, a metà lettura o quando il mouse esce verso
     la barra del browser (sta per chiudere). Mai prima che la persona abbia risposto al banner dei cookie,
     mai a chi ha già inviato una richiesta, e se l'ha chiuso aspettiamo 3 giorni. */
  function puoMostrare() {
    if (!ATTIVO.popup || LEGALE || CONTATTI || haScritto() || sg('ds_nl_vista')) return false;
    if (BOX && BOX.classList.contains('open')) return false;
    var no = parseInt(lg('ds_nl_no') || '0', 10); if (no && Date.now() - no < 3 * 864e5) return false;
    var fm = document.activeElement; if (fm && /^(INPUT|TEXTAREA|SELECT)$/.test(fm.tagName)) return false;   // sta già compilando un modulo
    return true;
  }
  var t0 = Date.now();
  function prova(da) { if (Date.now() - t0 > 8000 && puoMostrare()) apri(da); }
  if (ATTIVO.popup && !LEGALE && !iscritto()) {
    setTimeout(function () { prova('tempo'); }, 30000);
    addEventListener('scroll', function () {
      var h = document.documentElement.scrollHeight - innerHeight;
      if (h > 600 && scrollY / h > 0.55) prova('lettura');
    }, { passive: true });
    document.addEventListener('mouseout', function (e) { if (!e.relatedTarget && e.clientY <= 0) prova('uscita'); });
    setInterval(pillolaSeServe, 2000);
  }
  function pillolaSeServe() {
    if (iscritto()) return;
    var no = lg('ds_nl_no'); if (no || sg('ds_nl_vista')) { if (!BOX || !BOX.classList.contains('open')) pillola(); }
  }

  /* ================= 2) fascia "Preventivo gratuito" a metà delle pagine lunghe ================= */
  function fascia() {
    if (!ATTIVO.fascia || LEGALE || CONTATTI || document.querySelector('.ds-fascia')) return;
    var main = document.querySelector('main') || document.body;
    var sez = Array.prototype.filter.call(main.querySelectorAll('section'), function (s) { return s.querySelector('h2') && !s.querySelector('form') && !s.closest('form'); });
    if (sez.length < 4) return;
    var dopo = sez[Math.min(2, sez.length - 2)];
    var el = document.createElement('section'); el.className = 'ds-fascia';
    el.innerHTML = '<div class="wrap"><div class="ds-f-in"><div><h3>' + esc(T.fT) + '</h3><p>' + esc(T.fS) + '</p>'
      + (iscritto() ? '' : '<button type="button" class="ds-f-n">' + esc(T.fN) + '</button>') + '</div>'
      + '<div class="ds-f-b"><a href="#richiesta" class="btn btn-p ds-f-p"><span class="lbl">' + esc(T.fB) + '</span></a>'
      + '<a class="ds-f-w" href="' + esc(linkWa()) + '" target="_blank" rel="noopener">💬 ' + esc(T.fW) + '</a></div></div></div>';
    dopo.parentNode.insertBefore(el, dopo.nextSibling);
    el.querySelector('.ds-f-p').onclick = function (e) { e.preventDefault(); vaiAlModulo('fascia a metà pagina'); };
    var n = el.querySelector('.ds-f-n'); if (n) n.onclick = function () { apri('fascia'); };
  }

  /* ================= 3) fumetto accanto al pulsante WhatsApp ================= */
  function fumetto() {
    if (!ATTIVO.fumetto || LEGALE || sg('ds_bolla') || window.innerWidth < 760) return;
    var fab = document.querySelector('.wa-fab'); if (!fab) return;
    if (document.querySelector('[aria-label="Cookie"]') || (BOX && BOX.classList.contains('open'))) { setTimeout(fumetto, 8000); return; }
    var r = fab.getBoundingClientRect(); if (!r.width) return;
    ss('ds_bolla', '1');
    var b = document.createElement('div'); b.className = 'ds-bolla'; b.innerHTML = esc(T.bolla) + '<button type="button" aria-label="Chiudi">×</button>';
    b.style.right = Math.max(8, innerWidth - r.left + 10) + 'px'; b.style.bottom = Math.max(8, innerHeight - r.bottom + 6) + 'px';
    document.body.appendChild(b); requestAnimationFrame(function () { b.classList.add('on'); });
    var via = function () { b.classList.remove('on'); setTimeout(function () { b.remove(); }, 400); };
    b.querySelector('button').onclick = function (e) { e.stopPropagation(); via(); };
    b.onclick = function () { via(); fab.click(); };
    setTimeout(via, 15000);
  }

  var avvio = function () { fascia(); setTimeout(fumetto, 45000); pillolaSeServe(); };
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', avvio); else avvio();
})();
