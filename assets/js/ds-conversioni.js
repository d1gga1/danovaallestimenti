/* Danova Stand, Danova Costruzioni, Danova Tech — più richieste dal sito (caricato da ds-live.js, 22/11/2026).
   Stesso file sui tre siti: testi, email e servizi cambiano da soli in base al dominio (vedi SITO qui sotto).
   Su Costruzioni e Tech c'è solo il popup −3% (fascia e fumetto parlano di fiere: solo su Stand).
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

  var SITI = { 'danovastand.com': 'stand', 'danovacostruzioni.it': 'costruzioni', 'danova-tech.com': 'tech' };
  var SITO = window.DS_SITO || SITI[location.hostname.replace(/^www\./, '')] || 'stand';
  var CFG = {
    stand: { brand: 'Danova Stand', dom: 'danovastand.com', mail: 'info@danova-tech.com' },
    costruzioni: { brand: 'Danova Costruzioni', dom: 'danovacostruzioni.it', mail: 'info@danovacostruzioni.it' },
    tech: { brand: 'Danova Tech', dom: 'danova-tech.com', mail: 'info@danova-tech.com' }
  }[SITO];
  SCONTO.mail = CFG.mail;
  if (SITO !== 'stand') { ATTIVO.fascia = false; ATTIVO.fumetto = false; }

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

  var LANG = String(document.documentElement.lang || 'it').toLowerCase();
  var L = /^zh-(hant|tw|hk|mo)/.test(LANG) ? 'zht' : LANG.slice(0, 2);   // zh-Hant = cinese tradizionale
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
      waTxt: '¡Hola Danova Stand! Os escribo desde danovastand.com: quiero un presupuesto para un stand.' },
    hi: { vs: 'आपके स्टॉल पर, 30 दिन तक मान्य', k: 'सिर्फ़ सब्सक्राइबर्स के लिए', h: 'अगले एग्ज़िबिशन स्टॉल पर 3% छूट', s: 'Danova Stand न्यूज़लेटर सब्सक्राइब करें: हम तुरंत डिस्काउंट कोड भेजते हैं, जो मिलने के 30 दिन तक मान्य है।',
      li: ['इटली और पूरे यूरोप में टर्नकी स्टॉल', '24 कार्य-घंटों में मुफ़्त कोटेशन', 'ट्रेड फ़ेयर कैलेंडर और स्टॉल के आइडिया'],
      nome: 'पूरा नाम', az: 'कंपनी', mail: 'ईमेल', tel: 'फ़ोन (वैकल्पिक)', fiera: 'आप किस ट्रेड फ़ेयर में भाग ले रहे हैं? (वैकल्पिक)', fieraPh: 'जैसे Heimtextil 2027',
      ok: 'मैं Danova Stand का न्यूज़लेटर और ऑफ़र पाने और अपने अनुरोध के बारे में संपर्क किए जाने के लिए सहमत हूँ। मैंने <a href="/en/privacy/" target="_blank" rel="noopener">प्राइवेसी नोटिस</a> पढ़ लिया है।',
      btn: 'मुझे कोड भेजें', no: 'नहीं, धन्यवाद', e1: 'अपना नाम लिखें।', e2: 'सही ईमेल लिखें।', e3: 'कोड पाने के लिए सहमति पर टिक करें।', inv: 'भेजा जा रहा है…',
      fatto: 'हो गया! यह रहा आपका कोड', fattoS: 'हमने इसे ईमेल से भी भेजा है। कोटेशन कन्फ़र्म करते समय बताइए: मान्य है ', copia: 'कॉपी', copiato: 'कॉपी हो गया ✓',
      prev: 'अभी कोटेशन माँगें', pill: 'न्यूज़लेटर के साथ',
      fT: 'ट्रेड फ़ेयर की तैयारी कर रहे हैं?', fS: 'हमें फ़ेयर, जगह और अपने आइडिया बताइए: 24 कार्य-घंटों में मुफ़्त कोटेशन, डिज़ाइन से डिसमैंटलिंग तक एक ही संपर्क।', fB: 'कोटेशन माँगें', fW: 'WhatsApp पर लिखें', fN: 'या सब्सक्राइब करें और 3% छूट पाएँ',
      bolla: 'कोई ट्रेड फ़ेयर आने वाला है? हमें WhatsApp पर लिखें।',
      waTxt: 'नमस्ते Danova Stand! मैं danovastand.com से लिख रहा/रही हूँ: मुझे स्टॉल का कोटेशन चाहिए।' },
    ur: { vs: 'آپ کے اسٹال پر، 30 دن کے لیے', k: 'صرف سبسکرائبرز کے لیے', h: 'اگلے نمائشی اسٹال پر 3% رعایت', s: 'Danova Stand نیوز لیٹر سبسکرائب کریں: ہم فوراً ڈسکاؤنٹ کوڈ بھیجتے ہیں، جو ملنے کے بعد 30 دن تک قابلِ استعمال ہے۔',
      li: ['اٹلی اور پورے یورپ میں ٹرن کی اسٹال', '24 کاروباری گھنٹوں میں مفت کوٹیشن', 'نمائشوں کا کیلنڈر اور اسٹال کے آئیڈیاز'],
      nome: 'پورا نام', az: 'کمپنی', mail: 'ای میل', tel: 'فون (اختیاری)', fiera: 'آپ کس نمائش میں شرکت کر رہے ہیں؟ (اختیاری)', fieraPh: 'مثلاً Heimtextil 2027',
      ok: 'میں Danova Stand کا نیوز لیٹر اور آفرز وصول کرنے اور اپنی درخواست کے بارے میں رابطے پر متفق ہوں۔ میں نے <a href="/en/privacy/" target="_blank" rel="noopener">پرائیویسی نوٹس</a> پڑھ لیا ہے۔',
      btn: 'مجھے کوڈ بھیجیں', no: 'نہیں، شکریہ', e1: 'اپنا نام لکھیں۔', e2: 'درست ای میل لکھیں۔', e3: 'کوڈ کے لیے رضامندی پر نشان لگائیں۔', inv: 'بھیجا جا رہا ہے…',
      fatto: 'ہو گیا! یہ رہا آپ کا کوڈ', fattoS: 'ہم نے یہ ای میل پر بھی بھیج دیا ہے۔ کوٹیشن کنفرم کرتے وقت بتائیں: قابلِ استعمال ہے ', copia: 'کاپی', copiato: 'کاپی ہو گیا ✓',
      prev: 'ابھی کوٹیشن مانگیں', pill: 'نیوز لیٹر کے ساتھ',
      fT: 'نمائش کی تیاری کر رہے ہیں؟', fS: 'ہمیں نمائش، رقبہ اور اپنے آئیڈیاز بتائیں: 24 کاروباری گھنٹوں میں مفت کوٹیشن، ڈیزائن سے اختتام تک ایک ہی رابطہ۔', fB: 'کوٹیشن مانگیں', fW: 'واٹس ایپ پر لکھیں', fN: 'یا سبسکرائب کریں اور 3% رعایت پائیں',
      bolla: 'کوئی نمائش آنے والی ہے؟ ہمیں واٹس ایپ پر لکھیں۔',
      waTxt: 'السلام علیکم Danova Stand! میں danovastand.com سے لکھ رہا/رہی ہوں: مجھے اسٹال کی کوٹیشن چاہیے۔' }
  };
  var TXS = {
    costruzioni: {
      it: { vs: 'sui tuoi lavori, valido 30 giorni', h: '−3% sui tuoi prossimi lavori', s: 'Iscriviti alla newsletter di Danova Costruzioni: ti mandiamo subito il codice sconto, da usare entro 30 giorni dal ricevimento.',
        li: ['Ristrutturazioni chiavi in mano in Veneto e Friuli', 'Sopralluogo gratuito e prezzo bloccato', 'Un solo referente dal progetto alla consegna'],
        fiera: 'Che lavoro devi fare? (facoltativo)', fieraPh: 'es. ristrutturazione bagno', fieraK: 'Lavoro',
        ok: 'Acconsento a ricevere la newsletter e le offerte di Danova Costruzioni e a essere ricontattato per la mia richiesta. Ho letto l\'<a href="/privacy/" target="_blank" rel="noopener">informativa privacy</a>.',
        prev: 'Richiedi subito il sopralluogo gratuito', arCosa: 'sui tuoi lavori', arRacc: 'Raccontaci che lavoro devi fare, dove e quando',
        waTxt: 'Ciao Danova Costruzioni! Vi scrivo dal sito danovacostruzioni.it: vorrei un preventivo per dei lavori.' },
      en: { vs: 'off your building works, valid for 30 days', h: '3% off your next building works', s: 'Subscribe to the Danova Costruzioni newsletter: we send you the discount code right away, valid for 30 days from receipt.',
        li: ['Turnkey renovations in Veneto and Friuli', 'Free site visit and fixed price', 'One contact from design to handover'],
        fiera: 'What work do you need? (optional)', fieraPh: 'e.g. bathroom renovation', fieraK: 'Lavoro',
        ok: 'I agree to receive the Danova Costruzioni newsletter and offers and to be contacted about my request. I have read the <a href="/en/privacy/" target="_blank" rel="noopener">privacy policy</a>.',
        prev: 'Book your free site visit', arCosa: 'off your building works', arRacc: 'Tell us what work you need, where and when',
        waTxt: 'Hello Danova Costruzioni! I am writing from danovacostruzioni.it: I would like a quote for some building works.' }
    },
    tech: {
      it: { vs: 'sul tuo progetto, valido 30 giorni', h: '−3% sul tuo prossimo progetto', s: 'Iscriviti alla newsletter di Danova Tech: ti mandiamo subito il codice sconto, da usare entro 30 giorni dal ricevimento.',
        li: ['Siti web, app e software su misura', 'Preventivo fisso entro 24 ore', 'Bozza gratuita prima di pagare'],
        fiera: 'Di cosa hai bisogno? (facoltativo)', fieraPh: 'es. sito web, app, SEO', fieraK: 'Progetto',
        ok: 'Acconsento a ricevere la newsletter e le offerte di Danova Tech e a essere ricontattato per la mia richiesta. Ho letto l\'<a href="/privacy/" target="_blank" rel="noopener">informativa privacy</a>.',
        prev: 'Richiedi subito il preventivo', arCosa: 'sul tuo progetto', arRacc: 'Raccontaci di cosa hai bisogno (sito, app, gestionale, marketing)',
        waTxt: 'Ciao Danova Tech! Vi scrivo dal sito danova-tech.com: vorrei un preventivo.' },
      en: { vs: 'off your project, valid for 30 days', h: '3% off your next project', s: 'Subscribe to the Danova Tech newsletter: we send you the discount code right away, valid for 30 days from receipt.',
        li: ['Websites, apps and custom software', 'Fixed quote within 24 hours', 'Free draft before you pay'],
        fiera: 'What do you need? (optional)', fieraPh: 'e.g. website, app, SEO', fieraK: 'Progetto',
        ok: 'I agree to receive the Danova Tech newsletter and offers and to be contacted about my request. I have read the <a href="/en/privacy/" target="_blank" rel="noopener">privacy policy</a>.',
        prev: 'Request your quote now', arCosa: 'off your project', arRacc: 'Tell us what you need (website, app, software, marketing)',
        waTxt: 'Hello Danova Tech! I am writing from danova-tech.com: I would like a quote.' }
    }
  };
  /* altre lingue: testi comuni (UI), testi per sito (XS), email automatica (AR), privacy per lingua (PRIV) */
  var UI = {"ro": {"k": "Doar pentru abonați", "nome": "Nume și prenume", "az": "Companie", "mail": "Email", "tel": "Telefon (opțional)", "btn": "Vreau codul de reducere", "no": "Nu, mulțumesc", "e1": "Scrieți numele.", "e2": "Introduceți un email valid.", "e3": "Bifați acordul pentru a primi codul.", "inv": "Se trimite…", "fatto": "Gata! Iată codul dvs.", "fattoS": "L-am trimis și pe email. Comunicați-ni-l când confirmați oferta: este valabil până la ", "copia": "Copiază", "copiato": "Copiat ✓", "pill": "cu newsletterul"}, "sq": {"k": "Vetëm për abonentët", "nome": "Emri dhe mbiemri", "az": "Kompania", "mail": "Email", "tel": "Telefoni (opsional)", "btn": "Dua kodin e zbritjes", "no": "Jo, faleminderit", "e1": "Shkruani emrin tuaj.", "e2": "Vendosni një email të vlefshëm.", "e3": "Shënoni pëlqimin për të marrë kodin.", "inv": "Duke dërguar…", "fatto": "U krye! Ja kodi juaj", "fattoS": "Jua dërguam edhe me email. Na e tregoni kur konfirmoni ofertën: është i vlefshëm deri më ", "copia": "Kopjo", "copiato": "U kopjua ✓", "pill": "me buletinin"}, "ar": {"k": "للمشتركين فقط", "nome": "الاسم الكامل", "az": "الشركة", "mail": "البريد الإلكتروني", "tel": "الهاتف (اختياري)", "btn": "أريد رمز الخصم", "no": "لا، شكراً", "e1": "يرجى كتابة اسمك.", "e2": "يرجى إدخال بريد إلكتروني صحيح.", "e3": "يرجى تحديد خانة الموافقة لاستلام الرمز.", "inv": "جارٍ الإرسال…", "fatto": "تم! هذا هو رمزك", "fattoS": "أرسلناه إليك أيضاً عبر البريد الإلكتروني. أخبرنا به عند تأكيد عرض السعر: صالح حتى ", "copia": "نسخ", "copiato": "تم النسخ ✓", "pill": "مع النشرة الإخبارية"}, "tr": {"k": "Yalnızca aboneler için", "nome": "Ad soyad", "az": "Şirket", "mail": "E-posta", "tel": "Telefon (isteğe bağlı)", "btn": "İndirim kodunu istiyorum", "no": "Hayır, teşekkürler", "e1": "Lütfen adınızı yazın.", "e2": "Lütfen geçerli bir e-posta girin.", "e3": "Kodu almak için onay kutusunu işaretleyin.", "inv": "Gönderiliyor…", "fatto": "Tamam! İşte kodunuz", "fattoS": "Kodu e-postayla da gönderdik. Teklifi onaylarken bize bildirin. Son geçerlilik tarihi: ", "copia": "Kopyala", "copiato": "Kopyalandı ✓", "pill": "bültenle"}, "nl": {"k": "Alleen voor abonnees", "nome": "Voor- en achternaam", "az": "Bedrijf", "mail": "E-mail", "tel": "Telefoon (optioneel)", "btn": "Stuur mij de kortingscode", "no": "Nee, bedankt", "e1": "Vul uw naam in.", "e2": "Vul een geldig e-mailadres in.", "e3": "Vink de toestemming aan om de code te ontvangen.", "inv": "Bezig met verzenden…", "fatto": "Klaar! Hier is uw code", "fattoS": "We hebben hem ook per e-mail gestuurd. Vermeld hem wanneer u de offerte bevestigt: geldig tot ", "copia": "Kopiëren", "copiato": "Gekopieerd ✓", "pill": "met de nieuwsbrief"}, "zh": {"k": "仅限订阅用户", "nome": "姓名", "az": "公司", "mail": "电子邮箱", "tel": "电话（选填）", "btn": "获取优惠码", "no": "不用了，谢谢", "e1": "请填写您的姓名。", "e2": "请输入有效的电子邮箱。", "e3": "请勾选同意框以获取优惠码。", "inv": "正在发送…", "fatto": "完成！这是您的优惠码", "fattoS": "我们也已通过电子邮件发送给您。确认报价时请告诉我们。有效期至 ", "copia": "复制", "copiato": "已复制 ✓", "pill": "订阅即享"}, "zht": {"k": "僅限訂閱用戶", "nome": "姓名", "az": "公司", "mail": "電子郵件", "tel": "電話（選填）", "btn": "取得優惠碼", "no": "不用了，謝謝", "e1": "請填寫您的姓名。", "e2": "請輸入有效的電子郵件。", "e3": "請勾選同意框以取得優惠碼。", "inv": "傳送中…", "fatto": "完成！這是您的優惠碼", "fattoS": "我們也已透過電子郵件寄給您。確認報價時請告訴我們。有效期至 ", "copia": "複製", "copiato": "已複製 ✓", "pill": "訂閱即享"}};
  var XS = { stand: {"de": {"arCosa": "auf Ihren Messestand", "arRacc": "Nennen Sie uns Messe, Fläche und Ihre Ideen"}, "fr": {"arCosa": "sur votre stand", "arRacc": "Indiquez-nous le salon, la surface et vos idées"}, "es": {"arCosa": "en tu stand", "arRacc": "Cuéntanos la feria, los metros y tus ideas"}, "hi": {"arCosa": "आपके प्रदर्शनी स्टॉल पर", "arRacc": "हमें प्रदर्शनी, जगह और अपने आइडिया बताएं"}, "ur": {"arCosa": "آپ کے نمائشی اسٹال پر", "arRacc": "ہمیں نمائش، رقبہ اور اپنے آئیڈیاز بتائیں"}, "ar": {"vs": "على جناحك، صالح 30 يوماً", "h": "خصم 3% على جناحك القادم في المعرض", "s": "اشترك في النشرة الإخبارية لـ Danova Stand: نرسل لك رمز الخصم فوراً، صالح لمدة 30 يوماً من استلامه.", "li": ["أجنحة معارض جاهزة في إيطاليا وأوروبا", "عرض سعر مجاني خلال 24 ساعة عمل", "تقويم المعارض وأفكار للجناح"], "fiera": "في أي معرض ستشارك؟ (اختياري)", "fieraPh": "مثال: Vinitaly 2027", "prev": "اطلب عرض السعر الآن", "fT": "هل تستعد لمعرض؟", "fS": "أخبرنا بالمعرض والمساحة وأفكارك: عرض سعر مجاني خلال 24 ساعة عمل، مع مسؤول واحد من التصميم حتى الفك.", "fB": "اطلب عرض سعر", "fW": "راسلنا على واتساب", "fN": "أو اشترك واحصل على خصم 3%", "bolla": "لديك معرض قريب؟ راسلنا على واتساب وسنرد عليك.", "waTxt": "مرحباً Danova Stand! أكتب إليكم من موقع danovastand.com: أريد عرض سعر لجناح معرض.", "arCosa": "على جناحك في المعرض", "arRacc": "أخبرنا بالمعرض والمساحة وأفكارك", "ok": "أوافق على تلقي النشرة الإخبارية وعروض {b} وعلى التواصل معي بخصوص طلبي. لقد قرأت <a href=\"{priv}\" target=\"_blank\" rel=\"noopener\">سياسة الخصوصية</a>."}, "tr": {"vs": "standınızda, 30 gün geçerli", "h": "Bir sonraki fuar standınızda %3 indirim", "s": "Danova Stand bültenine abone olun: indirim kodunu hemen gönderiyoruz, alındığı tarihten itibaren 30 gün geçerli.", "li": ["İtalya ve Avrupa'da anahtar teslim standlar", "24 iş saati içinde ücretsiz teklif", "Fuar takvimi ve stand fikirleri"], "fiera": "Hangi fuara katılacaksınız? (isteğe bağlı)", "fieraPh": "örn. Vinitaly 2027", "prev": "Hemen teklif isteyin", "fT": "Bir fuara mı hazırlanıyorsunuz?", "fS": "Fuarı, metrekareyi ve fikirlerinizi anlatın: 24 iş saati içinde ücretsiz teklif, projeden sökümüne kadar tek muhatap.", "fB": "Teklif isteyin", "fW": "WhatsApp'tan yazın", "fN": "ya da abone olun, %3 indirim kazanın", "bolla": "Yaklaşan bir fuarınız mı var? WhatsApp'tan yazın, size dönelim.", "waTxt": "Merhaba Danova Stand! danovastand.com sitesinden yazıyorum: bir stand için teklif almak istiyorum.", "arCosa": "fuar standınızda", "arRacc": "Fuarı, metrekareyi ve fikirlerinizi anlatın", "ok": "{b} bültenini ve tekliflerini almayı ve talebimle ilgili benimle iletişime geçilmesini kabul ediyorum. <a href=\"{priv}\" target=\"_blank\" rel=\"noopener\">Gizlilik politikasını</a> okudum."}, "nl": {"vs": "op uw stand, 30 dagen geldig", "h": "3% korting op uw volgende beursstand", "s": "Schrijf u in voor de nieuwsbrief van Danova Stand: we sturen u meteen de kortingscode, 30 dagen geldig na ontvangst.", "li": ["Turnkey beursstands in Italië en heel Europa", "Gratis offerte binnen 24 werkuren", "Beurskalender en ideeën voor uw stand"], "fiera": "Op welke beurs staat u? (optioneel)", "fieraPh": "bijv. Vinitaly 2027", "prev": "Vraag nu een offerte aan", "fT": "Bereidt u een beurs voor?", "fS": "Vertel ons de beurs, de afmetingen en uw ideeën: gratis offerte binnen 24 werkuren, één aanspreekpunt van ontwerp tot afbouw.", "fB": "Offerte aanvragen", "fW": "Stuur ons een WhatsApp", "fN": "of schrijf u in en krijg 3% korting", "bolla": "Staat er een beurs op de planning? Stuur ons een WhatsApp, wij reageren snel.", "waTxt": "Hallo Danova Stand! Ik schrijf via danovastand.com: ik wil graag een offerte voor een beursstand.", "arCosa": "op uw beursstand", "arRacc": "Vertel ons de beurs, de afmetingen en uw ideeën", "ok": "Ik ga akkoord met het ontvangen van de nieuwsbrief en aanbiedingen van {b} en om gecontacteerd te worden over mijn aanvraag. Ik heb het <a href=\"{priv}\" target=\"_blank\" rel=\"noopener\">privacybeleid</a> gelezen."}, "zh": {"vs": "用于您的展台，30天内有效", "h": "下一个展台立减3%", "s": "订阅 Danova Stand 新闻通讯：我们会立即发送优惠码，自收到之日起30天内有效。", "li": ["意大利及欧洲交钥匙展台搭建", "24个工作小时内免费报价", "展会日历与展台创意"], "fiera": "您将参加哪个展会？（选填）", "fieraPh": "例如 Vinitaly 2027", "prev": "立即获取报价", "fT": "正在准备参展？", "fS": "告诉我们展会、面积和您的想法：24个工作小时内免费报价，从设计到拆除只需一位对接人。", "fB": "获取报价", "fW": "WhatsApp 联系我们", "fN": "或订阅即享3%优惠", "bolla": "即将参展？通过 WhatsApp 联系我们，我们会尽快回复。", "waTxt": "您好 Danova Stand！我通过 danovastand.com 联系你们：我想获取展台报价。", "arCosa": "用于您的展台", "arRacc": "告诉我们展会、面积和您的想法", "ok": "我同意接收 {b} 的新闻通讯和优惠信息，并同意就我的需求与我联系。我已阅读<a href=\"{priv}\" target=\"_blank\" rel=\"noopener\">隐私政策</a>。"}, "zht": {"vs": "用於您的展位，30天內有效", "h": "下一個展位立減3%", "s": "訂閱 Danova Stand 電子報：我們會立即寄送優惠碼，自收到之日起30天內有效。", "li": ["義大利及歐洲統包展位搭建", "24個工作小時內免費報價", "展覽日曆與展位創意"], "fiera": "您將參加哪個展覽？（選填）", "fieraPh": "例如 Vinitaly 2027", "prev": "立即取得報價", "fT": "正在準備參展？", "fS": "告訴我們展覽、面積和您的想法：24個工作小時內免費報價，從設計到拆除只需一位窗口。", "fB": "取得報價", "fW": "WhatsApp 聯絡我們", "fN": "或訂閱即享3%優惠", "bolla": "即將參展？透過 WhatsApp 聯絡我們，我們會盡快回覆。", "waTxt": "您好 Danova Stand！我透過 danovastand.com 聯絡你們：我想取得展位報價。", "arCosa": "用於您的展位", "arRacc": "告訴我們展覽、面積和您的想法", "ok": "我同意接收 {b} 的電子報和優惠資訊，並同意就我的需求與我聯絡。我已閱讀<a href=\"{priv}\" target=\"_blank\" rel=\"noopener\">隱私政策</a>。"}}, costruzioni: {"de": {"vs": "auf Ihre Bauarbeiten, 30 Tage gültig", "h": "3 % Rabatt auf Ihre nächsten Bauarbeiten", "s": "Abonnieren Sie den Newsletter von Danova Costruzioni: Wir senden Ihnen sofort den Rabattcode, gültig 30 Tage ab Erhalt.", "li": ["Schlüsselfertige Renovierungen in Venetien und Friaul", "Kostenlose Besichtigung und Festpreis", "Ein Ansprechpartner von der Planung bis zur Übergabe"], "fiera": "Welche Arbeiten planen Sie? (optional)", "fieraPh": "z. B. Badsanierung", "prev": "Kostenlose Besichtigung anfragen", "arCosa": "auf Ihre Bauarbeiten", "arRacc": "Erzählen Sie uns, welche Arbeiten Sie planen, wo und wann", "waTxt": "Hallo Danova Costruzioni! Ich schreibe über danovacostruzioni.it: Ich hätte gern ein Angebot für Bauarbeiten.", "ok": "Ich möchte den Newsletter und Angebote von {b} erhalten und zu meiner Anfrage kontaktiert werden. Ich habe die <a href=\"{priv}\" target=\"_blank\" rel=\"noopener\">Datenschutzerklärung</a> gelesen.", "fieraK": "Lavoro"}, "ro": {"vs": "la lucrările dvs., valabil 30 de zile", "h": "−3% la următoarele lucrări", "s": "Abonați-vă la newsletterul Danova Costruzioni: vă trimitem imediat codul de reducere, valabil 30 de zile de la primire.", "li": ["Renovări la cheie în Veneto și Friuli", "Vizită gratuită pe șantier și preț blocat", "Un singur responsabil de la proiect la predare"], "fiera": "Ce lucrare doriți? (opțional)", "fieraPh": "ex. renovare baie", "prev": "Solicitați vizita gratuită", "arCosa": "la lucrările dvs.", "arRacc": "Spuneți-ne ce lucrare doriți, unde și când", "waTxt": "Bună ziua, Danova Costruzioni! Vă scriu de pe danovacostruzioni.it: aș dori o ofertă pentru niște lucrări.", "ok": "Sunt de acord să primesc newsletterul și ofertele {b} și să fiu contactat pentru cererea mea. Am citit <a href=\"{priv}\" target=\"_blank\" rel=\"noopener\">politica de confidențialitate</a>.", "fieraK": "Lavoro"}, "sq": {"vs": "për punimet tuaja, i vlefshëm 30 ditë", "h": "−3% në punimet tuaja të ardhshme", "s": "Abonohuni në buletinin e Danova Costruzioni: ju dërgojmë menjëherë kodin e zbritjes, i vlefshëm 30 ditë nga marrja.", "li": ["Rinovime çelës në dorë në Veneto dhe Friuli", "Inspektim falas dhe çmim i bllokuar", "Një person kontakti nga projekti deri në dorëzim"], "fiera": "Çfarë punimi ju duhet? (opsional)", "fieraPh": "p.sh. rinovim banjoje", "prev": "Kërkoni inspektimin falas", "arCosa": "për punimet tuaja", "arRacc": "Na tregoni çfarë punimi ju duhet, ku dhe kur", "waTxt": "Përshëndetje Danova Costruzioni! Ju shkruaj nga danovacostruzioni.it: dëshiroj një ofertë për disa punime.", "ok": "Pranoj të marr buletinin dhe ofertat e {b} dhe të kontaktohem për kërkesën time. Kam lexuar <a href=\"{priv}\" target=\"_blank\" rel=\"noopener\">politikën e privatësisë</a>.", "fieraK": "Lavoro"}, "hi": {"vs": "आपके निर्माण कार्य पर, 30 दिन तक मान्य", "h": "अगले निर्माण कार्य पर 3% छूट", "s": "Danova Costruzioni का न्यूज़लेटर सब्सक्राइब करें: हम तुरंत डिस्काउंट कोड भेजते हैं, मिलने के 30 दिन तक मान्य।", "li": ["वेनेतो और फ्रियुली में टर्नकी रेनोवेशन", "मुफ़्त साइट विज़िट और तय कीमत", "प्रोजेक्ट से हैंडओवर तक एक ही संपर्क"], "fiera": "आपको कौन-सा काम करवाना है? (वैकल्पिक)", "fieraPh": "जैसे बाथरूम रेनोवेशन", "prev": "मुफ़्त साइट विज़िट बुक करें", "arCosa": "आपके निर्माण कार्य पर", "arRacc": "हमें बताएं कि कौन-सा काम, कहां और कब करवाना है", "waTxt": "नमस्ते Danova Costruzioni! मैं danovacostruzioni.it से लिख रहा/रही हूं: मुझे कुछ निर्माण कार्य के लिए कोटेशन चाहिए।", "ok": "मैं {b} का न्यूज़लेटर और ऑफ़र पाने और अपने अनुरोध के लिए संपर्क किए जाने के लिए सहमत हूं। मैंने <a href=\"{priv}\" target=\"_blank\" rel=\"noopener\">गोपनीयता नीति</a> पढ़ ली है।", "fieraK": "Lavoro"}}, tech: {"de": {"vs": "auf Ihr Projekt, 30 Tage gültig", "h": "3 % Rabatt auf Ihr nächstes Projekt", "s": "Abonnieren Sie den Newsletter von Danova Tech: Wir senden Ihnen sofort den Rabattcode, gültig 30 Tage ab Erhalt.", "li": ["Websites, Apps und Software nach Maß", "Festpreisangebot innerhalb von 24 Stunden", "Kostenloser Entwurf, bevor Sie zahlen"], "fiera": "Was brauchen Sie? (optional)", "fieraPh": "z. B. Website, App, SEO", "prev": "Jetzt Angebot anfordern", "arCosa": "auf Ihr Projekt", "arRacc": "Erzählen Sie uns, was Sie brauchen (Website, App, Software, Marketing)", "waTxt": "Hallo Danova Tech! Ich schreibe über danova-tech.com: Ich hätte gern ein Angebot.", "ok": "Ich möchte den Newsletter und Angebote von {b} erhalten und zu meiner Anfrage kontaktiert werden. Ich habe die <a href=\"{priv}\" target=\"_blank\" rel=\"noopener\">Datenschutzerklärung</a> gelesen.", "fieraK": "Progetto"}, "es": {"vs": "en tu proyecto, válido 30 días", "h": "−3% en tu próximo proyecto", "s": "Suscríbete a la newsletter de Danova Tech: te enviamos ya el código de descuento, válido 30 días desde que lo recibes.", "li": ["Webs, apps y software a medida", "Presupuesto cerrado en 24 horas", "Borrador gratis antes de pagar"], "fiera": "¿Qué necesitas? (opcional)", "fieraPh": "p. ej. web, app, SEO", "prev": "Pide tu presupuesto ahora", "arCosa": "en tu proyecto", "arRacc": "Cuéntanos qué necesitas (web, app, software, marketing)", "waTxt": "¡Hola Danova Tech! Os escribo desde danova-tech.com: quiero un presupuesto.", "ok": "Acepto recibir la newsletter y las ofertas de {b} y que me contacten por mi solicitud. He leído la <a href=\"{priv}\" target=\"_blank\" rel=\"noopener\">política de privacidad</a>.", "fieraK": "Progetto"}, "fr": {"vs": "sur votre projet, valable 30 jours", "h": "−3 % sur votre prochain projet", "s": "Abonnez-vous à la newsletter de Danova Tech : nous vous envoyons tout de suite le code de réduction, valable 30 jours après réception.", "li": ["Sites web, applications et logiciels sur mesure", "Devis à prix fixe sous 24 heures", "Maquette gratuite avant de payer"], "fiera": "De quoi avez-vous besoin ? (facultatif)", "fieraPh": "ex. site web, appli, SEO", "prev": "Demandez votre devis maintenant", "arCosa": "sur votre projet", "arRacc": "Dites-nous ce dont vous avez besoin (site, appli, logiciel, marketing)", "waTxt": "Bonjour Danova Tech ! Je vous écris depuis danova-tech.com : je voudrais un devis.", "ok": "J'accepte de recevoir la newsletter et les offres de {b} et d'être recontacté(e) pour ma demande. J'ai lu la <a href=\"{priv}\" target=\"_blank\" rel=\"noopener\">politique de confidentialité</a>.", "fieraK": "Progetto"}, "ar": {"vs": "على مشروعك، صالح 30 يوماً", "h": "خصم 3% على مشروعك القادم", "s": "اشترك في النشرة الإخبارية لـ Danova Tech: نرسل لك رمز الخصم فوراً، صالح لمدة 30 يوماً من استلامه.", "li": ["مواقع وتطبيقات وبرمجيات حسب الطلب", "عرض سعر ثابت خلال 24 ساعة", "نموذج أولي مجاني قبل الدفع"], "fiera": "ما الذي تحتاجه؟ (اختياري)", "fieraPh": "مثال: موقع، تطبيق، SEO", "prev": "اطلب عرض السعر الآن", "arCosa": "على مشروعك", "arRacc": "أخبرنا بما تحتاجه (موقع، تطبيق، برنامج، تسويق)", "waTxt": "مرحباً Danova Tech! أكتب إليكم من موقع danova-tech.com: أريد عرض سعر.", "ok": "أوافق على تلقي النشرة الإخبارية وعروض {b} وعلى التواصل معي بخصوص طلبي. لقد قرأت <a href=\"{priv}\" target=\"_blank\" rel=\"noopener\">سياسة الخصوصية</a>.", "fieraK": "Progetto"}, "tr": {"vs": "projenizde, 30 gün geçerli", "h": "Bir sonraki projenizde %3 indirim", "s": "Danova Tech bültenine abone olun: indirim kodunu hemen gönderiyoruz, alındığı tarihten itibaren 30 gün geçerli.", "li": ["Web siteleri, uygulamalar ve özel yazılımlar", "24 saat içinde sabit fiyat teklifi", "Ödemeden önce ücretsiz taslak"], "fiera": "Neye ihtiyacınız var? (isteğe bağlı)", "fieraPh": "örn. web sitesi, uygulama, SEO", "prev": "Hemen teklif isteyin", "arCosa": "projenizde", "arRacc": "Neye ihtiyacınız olduğunu anlatın (web sitesi, uygulama, yazılım, pazarlama)", "waTxt": "Merhaba Danova Tech! danova-tech.com sitesinden yazıyorum: teklif almak istiyorum.", "ok": "{b} bültenini ve tekliflerini almayı ve talebimle ilgili benimle iletişime geçilmesini kabul ediyorum. <a href=\"{priv}\" target=\"_blank\" rel=\"noopener\">Gizlilik politikasını</a> okudum.", "fieraK": "Progetto"}, "zh": {"vs": "用于您的项目，30天内有效", "h": "下一个项目立减3%", "s": "订阅 Danova Tech 新闻通讯：我们会立即发送优惠码，自收到之日起30天内有效。", "li": ["网站、应用和定制软件", "24小时内固定报价", "付款前免费出草稿"], "fiera": "您需要什么？（选填）", "fieraPh": "例如 网站、应用、SEO", "prev": "立即获取报价", "arCosa": "用于您的项目", "arRacc": "告诉我们您的需求（网站、应用、软件、营销）", "waTxt": "您好 Danova Tech！我通过 danova-tech.com 联系你们：我想获取报价。", "ok": "我同意接收 {b} 的新闻通讯和优惠信息，并同意就我的需求与我联系。我已阅读<a href=\"{priv}\" target=\"_blank\" rel=\"noopener\">隐私政策</a>。", "fieraK": "Progetto"}} };
  var AR = {"it": "Ciao {n}, grazie per esserti iscritto alla newsletter di {b}!\n\nEcco il tuo codice sconto: {c}\n−{p}% {cosa}, valido {g} giorni: fino al {d}.\nComunicacelo quando ci chiedi o confermi il preventivo.\n\n{racc} rispondendo a questa email o su WhatsApp (+39 388 470 6887): ti mandiamo il preventivo gratuito entro 24 ore lavorative.\n\n{b} — {dom}", "en": "Hello {n}, thank you for subscribing to the {b} newsletter!\n\nYour discount code: {c}\n{p}% {cosa}, valid for {g} days: until {d}.\nMention it when you request or confirm your quote.\n\n{racc} by replying to this email or on WhatsApp (+39 388 470 6887): free quote within 24 working hours.\n\n{b} — {dom}", "de": "Hallo {n}, danke für Ihre Anmeldung zum Newsletter von {b}!\n\nIhr Rabattcode: {c}\n{p} % Rabatt {cosa}, gültig {g} Tage: bis {d}.\nNennen Sie ihn uns, wenn Sie das Angebot anfragen oder bestätigen.\n\n{racc}: Antworten Sie einfach auf diese E-Mail oder schreiben Sie uns auf WhatsApp (+39 388 470 6887). Kostenloses Angebot innerhalb von 24 Arbeitsstunden.\n\n{b} — {dom}", "fr": "Bonjour {n}, merci de vous être abonné(e) à la newsletter de {b} !\n\nVotre code de réduction : {c}\n−{p} % {cosa}, valable {g} jours : jusqu'au {d}.\nIndiquez-le-nous lorsque vous demandez ou confirmez votre devis.\n\n{racc} en répondant à cet e-mail ou sur WhatsApp (+39 388 470 6887) : devis gratuit sous 24 heures ouvrées.\n\n{b} — {dom}", "es": "Hola {n}, ¡gracias por suscribirte a la newsletter de {b}!\n\nTu código de descuento: {c}\n−{p}% {cosa}, válido {g} días: hasta el {d}.\nDínoslo cuando pidas o confirmes el presupuesto.\n\n{racc} respondiendo a este email o por WhatsApp (+39 388 470 6887): presupuesto gratis en 24 horas laborables.\n\n{b} — {dom}", "ro": "Bună, {n}! Vă mulțumim că v-ați abonat la newsletterul {b}!\n\nCodul dvs. de reducere: {c}\n−{p}% {cosa}, valabil {g} zile: până la {d}.\nComunicați-ni-l când cereți sau confirmați oferta.\n\n{racc}, răspunzând la acest email sau pe WhatsApp (+39 388 470 6887): ofertă gratuită în 24 de ore lucrătoare.\n\n{b} — {dom}", "sq": "Përshëndetje {n}, faleminderit që u abonuat në buletinin e {b}!\n\nKodi juaj i zbritjes: {c}\n−{p}% {cosa}, i vlefshëm {g} ditë: deri më {d}.\nNa e tregoni kur kërkoni ose konfirmoni ofertën.\n\n{racc} duke iu përgjigjur këtij emaili ose në WhatsApp (+39 388 470 6887): ofertë falas brenda 24 orëve të punës.\n\n{b} — {dom}", "hi": "नमस्ते {n}, {b} का न्यूज़लेटर सब्सक्राइब करने के लिए धन्यवाद!\n\nआपका डिस्काउंट कोड: {c}\n{cosa} {p}% छूट, {g} दिन तक मान्य: {d} तक।\nकोटेशन मांगते या कन्फ़र्म करते समय हमें यह कोड बताएं।\n\n{racc} — इस ईमेल का जवाब दें या WhatsApp (+39 388 470 6887) पर लिखें: 24 कार्य घंटों में मुफ़्त कोटेशन।\n\n{b} — {dom}", "ur": "السلام علیکم {n}، {b} کا نیوز لیٹر سبسکرائب کرنے کا شکریہ!\n\nآپ کا ڈسکاؤنٹ کوڈ: {c}\n{cosa} {p}% رعایت، {g} دن کے لیے: {d} تک۔\nکوٹیشن مانگتے یا کنفرم کرتے وقت ہمیں یہ کوڈ بتائیں۔\n\n{racc} — اس ای میل کا جواب دیں یا WhatsApp (+39 388 470 6887) پر لکھیں: 24 کاروباری گھنٹوں میں مفت کوٹیشن۔\n\n{b} — {dom}", "ar": "مرحباً {n}، شكراً لاشتراكك في النشرة الإخبارية لـ {b}!\n\nرمز الخصم الخاص بك: {c}\nخصم {p}% {cosa}، صالح {g} يوماً: حتى {d}.\nأخبرنا به عند طلب عرض السعر أو تأكيده.\n\n{racc} بالرد على هذا البريد أو عبر واتساب (+39 388 470 6887): عرض سعر مجاني خلال 24 ساعة عمل.\n\n{b} — {dom}", "tr": "Merhaba {n}, {b} bültenine abone olduğunuz için teşekkürler!\n\nİndirim kodunuz: {c}\n{cosa} %{p} indirim, {g} gün geçerli. Son tarih: {d}.\nTeklif isterken veya onaylarken bize bildirin.\n\n{racc}: bu e-postayı yanıtlayın veya WhatsApp'tan yazın (+39 388 470 6887). 24 iş saati içinde ücretsiz teklif.\n\n{b} — {dom}", "nl": "Hallo {n}, bedankt voor uw inschrijving op de nieuwsbrief van {b}!\n\nUw kortingscode: {c}\n{p}% korting {cosa}, {g} dagen geldig: tot {d}.\nVermeld hem wanneer u een offerte aanvraagt of bevestigt.\n\n{racc} door op deze e-mail te antwoorden of via WhatsApp (+39 388 470 6887): gratis offerte binnen 24 werkuren.\n\n{b} — {dom}", "zh": "{n}您好，感谢您订阅 {b} 新闻通讯！\n\n您的优惠码：{c}\n{cosa}立减{p}%，{g}天内有效：截至 {d}。\n申请或确认报价时请告诉我们此优惠码。\n\n{racc}：直接回复此邮件或通过 WhatsApp（+39 388 470 6887）联系我们，24个工作小时内免费报价。\n\n{b} — {dom}", "zht": "{n}您好，感謝您訂閱 {b} 電子報！\n\n您的優惠碼：{c}\n{cosa}立減{p}%，{g}天內有效：截至 {d}。\n申請或確認報價時請告訴我們此優惠碼。\n\n{racc}：直接回覆此郵件或透過 WhatsApp（+39 388 470 6887）聯絡我們，24個工作小時內免費報價。\n\n{b} — {dom}"};
  var PRIV = {"stand": {"it": "/privacy/", "en": "/en/privacy/", "de": "/de/datenschutz/", "fr": "/fr/confidentialite/", "es": "/es/privacidad/"}, "costruzioni": {"it": "/privacy/", "en": "/en/privacy/", "de": "/de/datenschutz/", "hi": "/hi/privacy/", "ro": "/ro/confidentialitate/", "sq": "/sq/privatesia/"}, "tech": {"it": "/privacy/", "en": "/en/privacy/", "de": "/de/datenschutz/", "fr": "/fr/confidentialite/", "es": "/es/privacidad/", "hi": "/hi/privacy/", "ro": "/ro/confidentialitate/", "sq": "/sq/privatesia/"}};
  var unisci = function () { var o = {}, i, k; for (i = 0; i < arguments.length; i++) for (k in arguments[i] || {}) o[k] = arguments[i][k]; return o; };
  var LT = L;   // lingua dei testi: se per questa lingua manca qualcosa si usa l'inglese, mai un miscuglio
  if (SITO === 'stand') { if (!TX[LT] && !(UI[LT] && XS.stand[LT] && XS.stand[LT].vs)) LT = 'en'; }
  else if (!(LT === 'it' || LT === 'en' || (XS[SITO][LT] && (TX[LT] || UI[LT])))) LT = 'en';
  var T = unisci(TX.en, UI[LT], TX[LT], SITO === 'stand' ? null : TXS[SITO][LT === 'it' ? 'it' : 'en'], XS[SITO][LT]);
  var priv = (PRIV[SITO] || {})[LT] || '/en/privacy/';
  T.ok = String(T.ok).replace('{priv}', priv).replace('{b}', CFG.brand);
  T.fieraK = T.fieraK || 'Fiera';
  T.arCosa = T.arCosa || (LT === 'it' ? 'sul tuo allestimento' : 'off your exhibition stand');
  T.arRacc = T.arRacc || (LT === 'it' ? 'Raccontaci fiera, metri quadri e idee' : 'Tell us the fair, the size and your ideas');

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
  var bersaglio = function () { return document.getElementById('richiesta') || document.getElementById('dt-scrivi') || document.querySelector('form.fr-req,form.dt-lead,main form#form'); };
  var vaiAlModulo = function (da) {
    ev('preventivo', da);
    var b = bersaglio();
    if (b) { b.scrollIntoView({ behavior: 'smooth', block: 'start' }); setTimeout(function () { var i = b.querySelector && b.querySelector('input:not([type=hidden]),textarea'); if (i) try { i.focus({ preventScroll: true }); } catch (e) {} }, 700); }
    else if (SITO === 'costruzioni') location.href = '/#dt-scrivi';
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
    if (iscritto()) return;
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
      _subject: '📰 ' + CFG.brand + ' · iscrizione newsletter −' + SCONTO.perc + '%: ' + g('nome') + (g('azienda') ? ' (' + g('azienda') + ')' : '') + (g('fiera') ? ' · ' + g('fiera') : ''),
      _template: 'table', _captcha: 'false',
      _autoresponse: (AR[LT] || AR.en).replace(/\{(\w+)\}/g, function (m, k) {
        return { n: nome1, b: CFG.brand, c: cod, p: SCONTO.perc, cosa: T.arCosa, g: SCONTO.giorni, d: dataIt(scad), racc: T.arRacc, dom: CFG.dom }[k];
      }),
      'Nome': g('nome'), email: g('email'), 'Azienda': g('azienda'), 'Telefono': g('tel'), 'Sito': CFG.brand,
      'Tipo': 'Iscrizione newsletter (popup −' + SCONTO.perc + '%)', 'Codice sconto': cod, 'Valido fino al': dataIt(scad),
      'Consenso newsletter': 'Sì, ' + dataIt(ora) + ' ' + ('0' + ora.getHours()).slice(-2) + ':' + ('0' + ora.getMinutes()).slice(-2), 'Lingua': L.toUpperCase(),
      'Pagina': location.href.split('#')[0]
    };
    corpo[T.fieraK] = g('fiera');
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

  /* quando mostrarlo: su qualsiasi pagina, 5-7 secondi dopo l'ingresso. Una volta per visita; ricompare a ogni
     nuova visita finché la persona non lascia i dati (iscrizione al −3% o qualsiasi richiesta inviata dal sito).
     Se lo chiude, nella stessa visita resta solo la pillola "−3%" in basso a sinistra. */
  function puoMostrare() {
    if (!ATTIVO.popup || haScritto() || sg('ds_nl_vista')) return false;
    if (BOX && BOX.classList.contains('open')) return false;
    return true;
  }
  function prova(da) {
    if (!puoMostrare()) return;
    var fm = document.activeElement;   // sta scrivendo in un modulo: riproviamo tra poco
    if (fm && /^(INPUT|TEXTAREA|SELECT)$/.test(fm.tagName) && !(BOX && BOX.contains(fm))) { setTimeout(function () { prova(da); }, 4000); return; }
    apri(da);
  }
  var attesa = 5000 + Math.floor(Math.random() * 2000);
  if (ATTIVO.popup && !iscritto()) {
    setTimeout(function () { prova('dopo ' + Math.round(attesa / 1000) + ' s'); }, attesa);
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
