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
        ur:{call:'کال کریں',wa:'WhatsApp',write:'لکھیں',sending:'بھیجا جا رہا ہے…',ok:'درخواست بھیج دی گئی! ہم جلد ای میل پر جواب دیں گے۔',fail:'ویب سائٹ سے نہیں بھیجا جا سکا: آپ کی ای میل ایپ تیار پیغام کے ساتھ کھل گئی ہے، بس بھیجیں دبائیں۔',e_nome:'اپنا نام لکھیں۔',e_mail:'درست ای میل ایڈریس لکھیں۔',e_msg:'دو سطروں میں بتائیں کہ آپ کو کیا چاہیے۔',subj:'ویب سائٹ سے درخواست'},
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
  /* 24/11/2026: testi del modulo in tutte le altre lingue del sito (prima ricadevano sull'inglese) */
  var DTX_EXTRA={"pt": {"t": {"call": "Ligar", "wa": "WhatsApp", "write": "Escreva para nós", "sending": "Enviando…", "ok": "Pedido enviado! Responderemos por e-mail o mais rápido possível.", "fail": "Não foi possível enviar pelo site: seu programa de e-mail foi aberto com a mensagem pronta, é só clicar em enviar.", "e_nome": "Informe seu nome.", "e_mail": "Informe um e-mail válido.", "e_msg": "Conte em poucas linhas do que você precisa.", "subj": "Website enquiry (pt)"}, "u": {"q": "Quando você gostaria de começar?", "o": ["Já, em até 2 semanas", "Dentro de um mês", "Em 1 a 3 meses", "Só estou pesquisando"], "hot": "Perfeito, seu pedido vai para o topo da lista."}, "et": "Informe um número de telefone válido."}, "nl": {"t": {"call": "Bellen", "wa": "WhatsApp", "write": "Mail ons", "sending": "Bezig met verzenden…", "ok": "Aanvraag verzonden! Wij antwoorden zo snel mogelijk per e-mail.", "fail": "Verzenden via de website is niet gelukt: uw e-mailprogramma is geopend met het bericht klaar, druk op verzenden.", "e_nome": "Vul uw naam in.", "e_mail": "Vul een geldig e-mailadres in.", "e_msg": "Vertel ons in een paar regels wat u nodig hebt.", "subj": "Website enquiry (nl)"}, "u": {"q": "Wanneer wilt u starten?", "o": ["Direct, binnen 2 weken", "Binnen een maand", "Over 1 tot 3 maanden", "Ik oriënteer me alleen"], "hot": "Perfect, uw aanvraag komt bovenaan de lijst."}, "et": "Vul een geldig telefoonnummer in."}, "pl": {"t": {"call": "Zadzwoń", "wa": "WhatsApp", "write": "Napisz do nas", "sending": "Wysyłanie…", "ok": "Zapytanie wysłane! Odpowiemy e-mailem najszybciej, jak to możliwe.", "fail": "Nie udało się wysłać ze strony: otworzył się Twój program pocztowy z gotową wiadomością, kliknij „Wyślij”.", "e_nome": "Wpisz swoje imię i nazwisko.", "e_mail": "Wpisz poprawny adres e-mail.", "e_msg": "Napisz w kilku słowach, czego potrzebujesz.", "subj": "Website enquiry (pl)"}, "u": {"q": "Kiedy chcesz zacząć?", "o": ["Od razu, w ciągu 2 tygodni", "W ciągu miesiąca", "Za 1–3 miesiące", "Na razie tylko się rozglądam"], "hot": "Świetnie, Twoje zapytanie trafia na początek listy."}, "et": "Wpisz poprawny numer telefonu."}, "ar": {"t": {"call": "اتصل بنا", "wa": "WhatsApp", "write": "راسلنا", "sending": "جارٍ الإرسال…", "ok": "تم إرسال الطلب! سنرد عليك عبر البريد الإلكتروني في أقرب وقت.", "fail": "تعذّر الإرسال من الموقع: فُتح برنامج البريد لديك والرسالة جاهزة، اضغط إرسال فقط.", "e_nome": "يرجى كتابة اسمك.", "e_mail": "يرجى إدخال بريد إلكتروني صحيح.", "e_msg": "أخبرنا في سطرين بما تحتاجه.", "subj": "Website enquiry (ar)"}, "u": {"q": "متى تودّ البدء؟", "o": ["فوراً، خلال أسبوعين", "خلال شهر", "خلال 1 إلى 3 أشهر", "أستكشف الخيارات فقط"], "hot": "ممتاز، سنضع طلبك في أعلى القائمة."}, "et": "يرجى إدخال رقم هاتف صحيح."}, "tr": {"t": {"call": "Arayın", "wa": "WhatsApp", "write": "Bize yazın", "sending": "Gönderiliyor…", "ok": "Talebiniz gönderildi! En kısa sürede e-postayla yanıt vereceğiz.", "fail": "Siteden gönderilemedi: e-posta programınız mesaj hazır şekilde açıldı, sadece Gönder’e basın.", "e_nome": "Lütfen adınızı yazın.", "e_mail": "Lütfen geçerli bir e-posta adresi girin.", "e_msg": "Neye ihtiyacınız olduğunu birkaç satırda anlatın.", "subj": "Website enquiry (tr)"}, "u": {"q": "Ne zaman başlamak istersiniz?", "o": ["Hemen, 2 hafta içinde", "Bir ay içinde", "1–3 ay içinde", "Sadece araştırıyorum"], "hot": "Harika, talebinizi listenin en üstüne alıyoruz."}, "et": "Lütfen geçerli bir telefon numarası girin."}, "ja": {"t": {"call": "電話する", "wa": "WhatsApp", "write": "メールする", "sending": "送信中…", "ok": "送信しました！できるだけ早くメールでご返信します。", "fail": "サイトから送信できませんでした。メッセージを入れた状態でメールソフトを開きましたので、送信を押してください。", "e_nome": "お名前を入力してください。", "e_mail": "有効なメールアドレスを入力してください。", "e_msg": "ご要望を簡単にお書きください。", "subj": "Website enquiry (ja)"}, "u": {"q": "いつ頃の開始をご希望ですか？", "o": ["すぐに（2週間以内）", "1か月以内", "1〜3か月後", "情報収集中"], "hot": "ありがとうございます。優先して対応いたします。"}, "et": "有効な電話番号を入力してください。"}, "ko": {"t": {"call": "전화하기", "wa": "WhatsApp", "write": "이메일 보내기", "sending": "전송 중…", "ok": "요청이 전송되었습니다! 최대한 빨리 이메일로 답변드리겠습니다.", "fail": "사이트에서 전송하지 못했습니다. 메시지가 준비된 이메일 앱이 열렸으니 보내기를 눌러 주세요.", "e_nome": "이름을 입력해 주세요.", "e_mail": "올바른 이메일 주소를 입력해 주세요.", "e_msg": "필요하신 내용을 간단히 적어 주세요.", "subj": "Website enquiry (ko)"}, "u": {"q": "언제 시작하고 싶으신가요?", "o": ["바로, 2주 이내", "한 달 이내", "1~3개월 후", "정보만 알아보는 중"], "hot": "좋습니다. 요청을 우선 처리하겠습니다."}, "et": "올바른 전화번호를 입력해 주세요."}, "ru": {"t": {"call": "Позвонить", "wa": "WhatsApp", "write": "Написать нам", "sending": "Отправка…", "ok": "Запрос отправлен! Мы ответим по электронной почте как можно скорее.", "fail": "Не удалось отправить с сайта: открылась ваша почтовая программа с готовым письмом, просто нажмите «Отправить».", "e_nome": "Укажите ваше имя.", "e_mail": "Укажите действительный адрес электронной почты.", "e_msg": "Опишите в двух словах, что вам нужно.", "subj": "Website enquiry (ru)"}, "u": {"q": "Когда вы хотели бы начать?", "o": ["Сразу, в течение 2 недель", "В течение месяца", "Через 1–3 месяца", "Пока просто изучаю"], "hot": "Отлично, ставим ваш запрос в начало списка."}, "et": "Укажите действительный номер телефона."}, "uk": {"t": {"call": "Зателефонувати", "wa": "WhatsApp", "write": "Написати нам", "sending": "Надсилання…", "ok": "Запит надіслано! Ми відповімо електронною поштою якнайшвидше.", "fail": "Не вдалося надіслати з сайту: відкрилася ваша поштова програма з готовим листом, просто натисніть «Надіслати».", "e_nome": "Вкажіть ваше ім’я.", "e_mail": "Вкажіть дійсну адресу електронної пошти.", "e_msg": "Опишіть коротко, що вам потрібно.", "subj": "Website enquiry (uk)"}, "u": {"q": "Коли ви хотіли б почати?", "o": ["Одразу, протягом 2 тижнів", "Протягом місяця", "Через 1–3 місяці", "Поки що лише цікавлюся"], "hot": "Чудово, ставимо ваш запит на початок списку."}, "et": "Вкажіть дійсний номер телефону."}, "bg": {"t": {"call": "Обадете се", "wa": "WhatsApp", "write": "Пишете ни", "sending": "Изпращане…", "ok": "Запитването е изпратено! Ще ви отговорим по имейл възможно най-скоро.", "fail": "Не успяхме да изпратим от сайта: отвори се имейл програмата ви с готовото съобщение, просто натиснете „Изпрати“.", "e_nome": "Въведете името си.", "e_mail": "Въведете валиден имейл адрес.", "e_msg": "Опишете накратко от какво имате нужда.", "subj": "Website enquiry (bg)"}, "u": {"q": "Кога бихте искали да започнете?", "o": ["Веднага, до 2 седмици", "До един месец", "След 1 до 3 месеца", "Само проучвам"], "hot": "Чудесно, поставяме запитването ви най-отгоре в списъка."}, "et": "Въведете валиден телефонен номер."}, "cs": {"t": {"call": "Zavolejte", "wa": "WhatsApp", "write": "Napište nám", "sending": "Odesílá se…", "ok": "Poptávka odeslána! Odpovíme e-mailem co nejdříve.", "fail": "Odeslání z webu se nezdařilo: otevřel se váš e-mailový program s připravenou zprávou, stačí stisknout Odeslat.", "e_nome": "Zadejte své jméno.", "e_mail": "Zadejte platnou e-mailovou adresu.", "e_msg": "Napište nám v pár řádcích, co potřebujete.", "subj": "Website enquiry (cs)"}, "u": {"q": "Kdy byste chtěli začít?", "o": ["Hned, do 2 týdnů", "Do měsíce", "Za 1 až 3 měsíce", "Zatím se jen informuji"], "hot": "Skvělé, vaši poptávku dáváme na začátek seznamu."}, "et": "Zadejte platné telefonní číslo."}, "el": {"t": {"call": "Καλέστε", "wa": "WhatsApp", "write": "Γράψτε μας", "sending": "Αποστολή…", "ok": "Το αίτημα στάλθηκε! Θα σας απαντήσουμε με email το συντομότερο.", "fail": "Δεν ήταν δυνατή η αποστολή από τον ιστότοπο: άνοιξε το πρόγραμμα email σας με έτοιμο το μήνυμα, πατήστε αποστολή.", "e_nome": "Γράψτε το όνομά σας.", "e_mail": "Εισαγάγετε μια έγκυρη διεύθυνση email.", "e_msg": "Πείτε μας σε δύο γραμμές τι χρειάζεστε.", "subj": "Website enquiry (el)"}, "u": {"q": "Πότε θα θέλατε να ξεκινήσετε;", "o": ["Αμέσως, μέσα σε 2 εβδομάδες", "Μέσα σε έναν μήνα", "Σε 1 έως 3 μήνες", "Απλώς ενημερώνομαι"], "hot": "Τέλεια, βάζουμε το αίτημά σας πρώτο στη λίστα."}, "et": "Εισαγάγετε έναν έγκυρο αριθμό τηλεφώνου."}, "fa": {"t": {"call": "تماس بگیرید", "wa": "WhatsApp", "write": "برای ما بنویسید", "sending": "در حال ارسال…", "ok": "درخواست ارسال شد! در اسرع وقت از طریق ایمیل پاسخ می‌دهیم.", "fail": "ارسال از سایت ممکن نشد: برنامهٔ ایمیل شما با پیام آماده باز شد، فقط دکمهٔ ارسال را بزنید.", "e_nome": "لطفاً نام خود را بنویسید.", "e_mail": "لطفاً یک ایمیل معتبر وارد کنید.", "e_msg": "در دو خط بگویید به چه چیزی نیاز دارید.", "subj": "Website enquiry (fa)"}, "u": {"q": "چه زمانی می‌خواهید شروع کنید؟", "o": ["فوراً، ظرف ۲ هفته", "ظرف یک ماه", "۱ تا ۳ ماه دیگر", "فقط در حال بررسی هستم"], "hot": "عالی، درخواست شما را در صدر فهرست قرار می‌دهیم."}, "et": "لطفاً یک شماره تلفن معتبر وارد کنید."}, "he": {"t": {"call": "התקשרו", "wa": "WhatsApp", "write": "כתבו לנו", "sending": "שולח…", "ok": "הבקשה נשלחה! נחזור אליכם במייל בהקדם.", "fail": "לא הצלחנו לשלוח מהאתר: תוכנת הדוא״ל שלכם נפתחה עם ההודעה מוכנה, פשוט לחצו על שליחה.", "e_nome": "נא לכתוב את שמכם.", "e_mail": "נא להזין כתובת דוא״ל תקינה.", "e_msg": "ספרו לנו בשתי שורות מה אתם צריכים.", "subj": "Website enquiry (he)"}, "u": {"q": "מתי תרצו להתחיל?", "o": ["מיד, תוך שבועיים", "תוך חודש", "בעוד 1 עד 3 חודשים", "רק בודקים אפשרויות"], "hot": "מצוין, הבקשה שלכם עוברת לראש הרשימה."}, "et": "נא להזין מספר טלפון תקין."}, "hu": {"t": {"call": "Hívjon", "wa": "WhatsApp", "write": "Írjon nekünk", "sending": "Küldés…", "ok": "Ajánlatkérés elküldve! A lehető leghamarabb válaszolunk e-mailben.", "fail": "Nem sikerült elküldeni az oldalról: megnyílt a levelezőprogramja a kész üzenettel, csak nyomja meg a Küldés gombot.", "e_nome": "Adja meg a nevét.", "e_mail": "Adjon meg érvényes e-mail-címet.", "e_msg": "Írja le pár sorban, mire van szüksége.", "subj": "Website enquiry (hu)"}, "u": {"q": "Mikor szeretne kezdeni?", "o": ["Azonnal, 2 héten belül", "Egy hónapon belül", "1–3 hónap múlva", "Csak tájékozódom"], "hot": "Remek, kérését a lista elejére tesszük."}, "et": "Adjon meg érvényes telefonszámot."}, "id": {"t": {"call": "Telepon", "wa": "WhatsApp", "write": "Kirim email", "sending": "Mengirim…", "ok": "Permintaan terkirim! Kami akan membalas lewat email secepatnya.", "fail": "Gagal mengirim dari situs: aplikasi email Anda sudah terbuka dengan pesan siap kirim, tinggal tekan kirim.", "e_nome": "Silakan tulis nama Anda.", "e_mail": "Masukkan alamat email yang valid.", "e_msg": "Ceritakan singkat apa yang Anda butuhkan.", "subj": "Website enquiry (id)"}, "u": {"q": "Kapan Anda ingin mulai?", "o": ["Segera, dalam 2 minggu", "Dalam sebulan", "Dalam 1–3 bulan", "Baru mencari informasi"], "hot": "Bagus, permintaan Anda kami taruh di urutan teratas."}, "et": "Masukkan nomor telepon yang valid."}, "ms": {"t": {"call": "Hubungi", "wa": "WhatsApp", "write": "E-mel kami", "sending": "Menghantar…", "ok": "Permintaan dihantar! Kami akan membalas melalui e-mel secepat mungkin.", "fail": "Tidak dapat menghantar dari laman: aplikasi e-mel anda telah dibuka dengan mesej sedia, tekan hantar sahaja.", "e_nome": "Sila tulis nama anda.", "e_mail": "Sila masukkan alamat e-mel yang sah.", "e_msg": "Terangkan ringkas apa yang anda perlukan.", "subj": "Website enquiry (ms)"}, "u": {"q": "Bilakah anda mahu bermula?", "o": ["Segera, dalam 2 minggu", "Dalam sebulan", "Dalam 1 hingga 3 bulan", "Sekadar meninjau"], "hot": "Bagus, permintaan anda diletakkan di atas senarai."}, "et": "Sila masukkan nombor telefon yang sah."}, "sv": {"t": {"call": "Ring", "wa": "WhatsApp", "write": "Mejla oss", "sending": "Skickar…", "ok": "Förfrågan skickad! Vi svarar via e-post så snart som möjligt.", "fail": "Det gick inte att skicka från webbplatsen: ditt e-postprogram har öppnats med meddelandet klart, tryck bara på skicka.", "e_nome": "Skriv ditt namn.", "e_mail": "Ange en giltig e-postadress.", "e_msg": "Berätta kort vad du behöver.", "subj": "Website enquiry (sv)"}, "u": {"q": "När vill du komma igång?", "o": ["Direkt, inom 2 veckor", "Inom en månad", "Om 1–3 månader", "Jag undersöker bara"], "hot": "Perfekt, vi lägger din förfrågan först i kön."}, "et": "Ange ett giltigt telefonnummer."}, "vi": {"t": {"call": "Gọi", "wa": "WhatsApp", "write": "Gửi email", "sending": "Đang gửi…", "ok": "Đã gửi yêu cầu! Chúng tôi sẽ trả lời qua email sớm nhất.", "fail": "Không gửi được từ trang web: ứng dụng email của bạn đã mở với tin nhắn soạn sẵn, chỉ cần bấm gửi.", "e_nome": "Vui lòng nhập tên.", "e_mail": "Vui lòng nhập email hợp lệ.", "e_msg": "Cho chúng tôi biết ngắn gọn bạn cần gì.", "subj": "Website enquiry (vi)"}, "u": {"q": "Bạn muốn bắt đầu khi nào?", "o": ["Ngay, trong 2 tuần", "Trong vòng một tháng", "Trong 1–3 tháng", "Chỉ đang tìm hiểu"], "hot": "Tuyệt, yêu cầu của bạn sẽ được ưu tiên đầu danh sách."}, "et": "Vui lòng nhập số điện thoại hợp lệ."}, "th": {"t": {"call": "โทร", "wa": "WhatsApp", "write": "ส่งอีเมล", "sending": "กำลังส่ง…", "ok": "ส่งคำขอแล้ว! เราจะตอบกลับทางอีเมลโดยเร็วที่สุด", "fail": "ส่งจากเว็บไซต์ไม่สำเร็จ: โปรแกรมอีเมลของคุณเปิดพร้อมข้อความแล้ว เพียงกดส่ง", "e_nome": "กรุณากรอกชื่อ", "e_mail": "กรุณากรอกอีเมลที่ถูกต้อง", "e_msg": "บอกเราสั้น ๆ ว่าคุณต้องการอะไร", "subj": "Website enquiry (th)"}, "u": {"q": "คุณต้องการเริ่มเมื่อไร?", "o": ["ทันที ภายใน 2 สัปดาห์", "ภายในหนึ่งเดือน", "อีก 1–3 เดือน", "แค่หาข้อมูล"], "hot": "ยอดเยี่ยม เราจะจัดคำขอของคุณไว้ลำดับแรก"}, "et": "กรุณากรอกหมายเลขโทรศัพท์ที่ถูกต้อง"}, "ta": {"t": {"call": "அழைக்கவும்", "wa": "WhatsApp", "write": "மின்னஞ்சல் அனுப்பவும்", "sending": "அனுப்பப்படுகிறது…", "ok": "கோரிக்கை அனுப்பப்பட்டது! விரைவில் மின்னஞ்சலில் பதிலளிப்போம்.", "fail": "தளத்திலிருந்து அனுப்ப முடியவில்லை: உங்கள் மின்னஞ்சல் செயலி தயாரான செய்தியுடன் திறந்துள்ளது, அனுப்பு என்பதை அழுத்தவும்.", "e_nome": "உங்கள் பெயரை உள்ளிடவும்.", "e_mail": "சரியான மின்னஞ்சல் முகவரியை உள்ளிடவும்.", "e_msg": "உங்களுக்கு என்ன தேவை என்று சுருக்கமாக எழுதுங்கள்.", "subj": "Website enquiry (ta)"}, "u": {"q": "எப்போது தொடங்க விரும்புகிறீர்கள்?", "o": ["உடனே, 2 வாரங்களுக்குள்", "ஒரு மாதத்திற்குள்", "1 முதல் 3 மாதங்களில்", "தகவல் மட்டும் தேடுகிறேன்"], "hot": "அருமை, உங்கள் கோரிக்கையைப் பட்டியலில் முதலில் வைக்கிறோம்."}, "et": "சரியான தொலைபேசி எண்ணை உள்ளிடவும்."}, "bn": {"t": {"call": "কল করুন", "wa": "WhatsApp", "write": "ইমেল করুন", "sending": "পাঠানো হচ্ছে…", "ok": "অনুরোধ পাঠানো হয়েছে! আমরা যত দ্রুত সম্ভব ইমেলে উত্তর দেব।", "fail": "সাইট থেকে পাঠানো যায়নি: আপনার ইমেল অ্যাপ প্রস্তুত বার্তাসহ খুলেছে, শুধু পাঠান চাপুন।", "e_nome": "আপনার নাম লিখুন।", "e_mail": "একটি সঠিক ইমেল ঠিকানা দিন।", "e_msg": "সংক্ষেপে লিখুন আপনার কী প্রয়োজন।", "subj": "Website enquiry (bn)"}, "u": {"q": "আপনি কবে শুরু করতে চান?", "o": ["এখনই, ২ সপ্তাহের মধ্যে", "এক মাসের মধ্যে", "১ থেকে ৩ মাসের মধ্যে", "শুধু খোঁজ নিচ্ছি"], "hot": "চমৎকার, আপনার অনুরোধ তালিকার শীর্ষে রাখছি।"}, "et": "একটি সঠিক ফোন নম্বর দিন।"}, "gu": {"t": {"call": "કૉલ કરો", "wa": "WhatsApp", "write": "ઇમેઇલ કરો", "sending": "મોકલાઈ રહ્યું છે…", "ok": "વિનંતી મોકલાઈ ગઈ! અમે શક્ય તેટલી ઝડપથી ઇમેઇલથી જવાબ આપીશું.", "fail": "સાઇટ પરથી મોકલી શકાયું નહીં: તમારી ઇમેઇલ એપ તૈયાર સંદેશ સાથે ખૂલી છે, ફક્ત મોકલો દબાવો.", "e_nome": "કૃપા કરીને તમારું નામ લખો.", "e_mail": "કૃપા કરીને માન્ય ઇમેઇલ સરનામું લખો.", "e_msg": "તમને શું જોઈએ છે તે ટૂંકમાં લખો.", "subj": "Website enquiry (gu)"}, "u": {"q": "તમે ક્યારે શરૂ કરવા માંગો છો?", "o": ["તરત, 2 અઠવાડિયામાં", "એક મહિનામાં", "1 થી 3 મહિનામાં", "હમણાં ફક્ત માહિતી લઉં છું"], "hot": "સરસ, તમારી વિનંતી યાદીમાં સૌથી ઉપર મૂકીએ છીએ."}, "et": "કૃપા કરીને માન્ય ફોન નંબર લખો."}, "pa": {"t": {"call": "ਕਾਲ ਕਰੋ", "wa": "WhatsApp", "write": "ਈਮੇਲ ਕਰੋ", "sending": "ਭੇਜਿਆ ਜਾ ਰਿਹਾ ਹੈ…", "ok": "ਬੇਨਤੀ ਭੇਜ ਦਿੱਤੀ ਗਈ! ਅਸੀਂ ਜਲਦੀ ਤੋਂ ਜਲਦੀ ਈਮੇਲ ਰਾਹੀਂ ਜਵਾਬ ਦੇਵਾਂਗੇ।", "fail": "ਸਾਈਟ ਤੋਂ ਭੇਜਿਆ ਨਹੀਂ ਜਾ ਸਕਿਆ: ਤੁਹਾਡੀ ਈਮੇਲ ਐਪ ਤਿਆਰ ਸੁਨੇਹੇ ਨਾਲ ਖੁੱਲ੍ਹ ਗਈ ਹੈ, ਬੱਸ ਭੇਜੋ ਦਬਾਓ।", "e_nome": "ਕਿਰਪਾ ਕਰਕੇ ਆਪਣਾ ਨਾਮ ਲਿਖੋ।", "e_mail": "ਕਿਰਪਾ ਕਰਕੇ ਸਹੀ ਈਮੇਲ ਪਤਾ ਲਿਖੋ।", "e_msg": "ਥੋੜ੍ਹੇ ਸ਼ਬਦਾਂ ਵਿੱਚ ਦੱਸੋ ਕਿ ਤੁਹਾਨੂੰ ਕੀ ਚਾਹੀਦਾ ਹੈ।", "subj": "Website enquiry (pa)"}, "u": {"q": "ਤੁਸੀਂ ਕਦੋਂ ਸ਼ੁਰੂ ਕਰਨਾ ਚਾਹੋਗੇ?", "o": ["ਤੁਰੰਤ, 2 ਹਫ਼ਤਿਆਂ ਵਿੱਚ", "ਇੱਕ ਮਹੀਨੇ ਵਿੱਚ", "1 ਤੋਂ 3 ਮਹੀਨਿਆਂ ਵਿੱਚ", "ਸਿਰਫ਼ ਜਾਣਕਾਰੀ ਲੈ ਰਹੇ ਹਾਂ"], "hot": "ਬਹੁਤ ਵਧੀਆ, ਤੁਹਾਡੀ ਬੇਨਤੀ ਸੂਚੀ ਵਿੱਚ ਸਭ ਤੋਂ ਉੱਪਰ ਰੱਖ ਰਹੇ ਹਾਂ।"}, "et": "ਕਿਰਪਾ ਕਰਕੇ ਸਹੀ ਫ਼ੋਨ ਨੰਬਰ ਲਿਖੋ।"}, "zh": {"t": {"call": "致电", "wa": "WhatsApp", "write": "发邮件", "sending": "正在发送…", "ok": "询价已发送！我们会尽快通过邮件回复您。", "fail": "无法通过网站发送：您的邮件程序已打开并附上消息，请直接点击发送。", "e_nome": "请填写您的姓名。", "e_mail": "请填写有效的邮箱地址。", "e_msg": "请简要说明您的需求。", "subj": "Website enquiry (zh)"}, "u": {"q": "您希望什么时候开始？", "o": ["马上，2周内", "一个月内", "1至3个月内", "先了解一下"], "hot": "好的，我们会优先处理您的询价。"}, "et": "请填写有效的电话号码。"}, "zt": {"t": {"call": "致電", "wa": "WhatsApp", "write": "寄電子郵件", "sending": "正在傳送…", "ok": "詢價已送出！我們會盡快透過電子郵件回覆您。", "fail": "無法透過網站傳送：您的郵件程式已開啟並附上訊息，請直接按傳送。", "e_nome": "請填寫您的姓名。", "e_mail": "請填寫有效的電子郵件地址。", "e_msg": "請簡要說明您的需求。", "subj": "Website enquiry (zt)"}, "u": {"q": "您希望什麼時候開始？", "o": ["馬上，2週內", "一個月內", "1至3個月內", "先了解一下"], "hot": "好的，我們會優先處理您的詢價。"}, "et": "請填寫有效的電話號碼。"}};
  function dtLk(){ var h=(document.documentElement.lang||'it').toLowerCase(); if(h.indexOf('zh-hant')===0||h.indexOf('zh-tw')===0||h.indexOf('zh-hk')===0) return 'zt'; return h.slice(0,2); }
  for(var _k in DTX_EXTRA){ if(!TX[_k]) TX[_k]=DTX_EXTRA[_k].t; }
  L=dtLk();
  var T=TX[L]||TX.en;

  /* 18/10/2026: "Quando vorresti partire?" (pillole) in tutti i moduli. Nell'email il valore arriva sempre in italiano. */
  var URG_IT=['Subito (entro 2 settimane)','Entro un mese','Fra 1 e 3 mesi','Sto solo valutando'];
  var UTX={
    it:{q:'Quando vorresti partire?',o:['Subito, entro 2 settimane','Entro un mese','Fra 1 e 3 mesi','Sto solo valutando'],hot:'Perfetto, mettiamo la tua richiesta in cima alla lista.'},
    ro:{q:'Când ați vrea să începeți?',o:['Imediat, în 2 săptămâni','În decurs de o lună','În 1–3 luni','Doar mă informez'],hot:'Perfect, cererea dvs. ajunge prima pe listă.'},
        sq:{q:'Kur do të donit të fillonit?',o:['Menjëherë, brenda 2 javësh','Brenda një muaji','Për 1 deri në 3 muaj','Thjesht po informohem'],hot:'Shkëlqyeshëm, kërkesa juaj del e para në listë.'},
        hr:{q:'Kada biste željeli početi?',o:['Odmah, u roku od 2 tjedna','U roku od mjesec dana','Za 1 do 3 mjeseca','Samo se informiram'],hot:'Odlično, vaš upit stavljamo na vrh popisa.'},
        hi:{q:'आप कब शुरू करना चाहेंगे?',o:['तुरंत, 2 हफ़्ते में','एक महीने के अंदर','1 से 3 महीने में','बस जानकारी ले रहा/रही हूँ'],hot:'बढ़िया, आपका अनुरोध सूची में सबसे ऊपर जाएगा।'},
        ur:{q:'آپ کب شروع کرنا چاہیں گے؟',o:['فوراً، 2 ہفتوں میں','ایک مہینے کے اندر','1 سے 3 ماہ میں','صرف معلومات لے رہا/رہی ہوں'],hot:'بہت خوب، آپ کی درخواست فہرست میں سب سے اوپر جائے گی۔'},
        en:{q:'When would you like to start?',o:['Right away, within 2 weeks','Within a month','In 1 to 3 months','Just exploring'],hot:'Great, we will put your request at the top of the list.'},
    de:{q:'Wann möchten Sie starten?',o:['Sofort, in 2 Wochen','Innerhalb eines Monats','In 1 bis 3 Monaten','Ich informiere mich nur'],hot:'Perfekt, Ihre Anfrage kommt ganz nach oben auf die Liste.'},
    fr:{q:'Quand souhaitez-vous démarrer ?',o:['Tout de suite, sous 2 semaines','Dans le mois','Dans 1 à 3 mois','Je me renseigne'],hot:'Parfait, nous mettons votre demande en haut de la liste.'},
    es:{q:'¿Cuándo te gustaría empezar?',o:['Ya, en 2 semanas','En un mes','En 1 a 3 meses','Solo estoy valorando'],hot:'Perfecto, ponemos tu solicitud la primera de la lista.'}
  };
  for(var _u in DTX_EXTRA){ if(!UTX[_u]) UTX[_u]=DTX_EXTRA[_u].u; }
  var lastForm=null;
  document.addEventListener('submit',function(e){ lastForm=e.target; },true);
  function urg(subject, fields){
    var el=lastForm && lastForm.elements && lastForm.elements['urgenza'], u=el?el.value:'';
    if(!u) return [subject, fields];
    var hot=(u===URG_IT[0]);
    return [(hot?'🔥 [SUBITO] ':'['+u+'] ')+subject, [['Quando vuole partire',u]].concat(fields)];
  }

  (function(){ var st=document.createElement('style'); st.id='dt-contatto-css'; st.textContent='.dt-lead{display:grid;gap:12px;max-width:620px;margin:8px auto 0;text-align:left}.dt-lead-2{display:grid;grid-template-columns:1fr 1fr;gap:12px}.dt-lead .btn{justify-content:center;width:100%}.dt-lead .btn[disabled]{opacity:.6}.dt-hp{position:absolute!important;left:-9999px!important;width:1px;height:1px;opacity:0}.dt-lead-msg{display:none;margin:0;font-size:14px}.dt-lead-msg.on{display:block}.dt-lead-msg.err{color:#ff8b98}.dt-lead-msg.ok{color:#8fe3b0}.dt-lead p.form-note,.dt-lead p.dt-lead-msg{max-width:none;margin:4px 0 0;text-align:center}.dt-lead .form-note a[href^=tel]{white-space:nowrap}#dt-scrivi,#richiesta{scroll-margin-top:120px}.dt-lead .form-note a{color:#ffe49f}.dt-bar{display:none}@media (max-width:760px){.dt-lead-2{grid-template-columns:1fr}.dt-bar{display:grid;grid-template-columns:1fr 1fr 1fr;position:fixed;left:10px;right:10px;bottom:calc(10px + env(safe-area-inset-bottom));z-index:8000;background:rgba(7,11,20,.92);-webkit-backdrop-filter:blur(12px);backdrop-filter:blur(12px);border:1px solid rgba(255,217,122,.28);border-radius:16px;overflow:hidden;box-shadow:0 10px 30px rgba(0,0,0,.45);transition:transform .35s,opacity .35s}.dt-bar.hide{transform:translateY(140%);opacity:0;pointer-events:none}.dt-bar a{display:flex;flex-direction:column;align-items:center;gap:3px;padding:9px 4px 8px;color:#e9edf7;font-size:12px;font-weight:600;text-decoration:none}.dt-bar a+a{border-left:1px solid rgba(255,255,255,.08)}.dt-bar svg{width:20px;height:20px}.dt-bar-call{background:#FFC93C;color:#0b0b0b!important}.dt-bar-wa svg{color:#3ddc84}body.has-dt-bar footer{padding-bottom:84px}body.has-dt-bar #top{bottom:96px}}'; document.head.appendChild(st); })();

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
        chk.splice(2,0,['tel',ET[dtLk()]||(DTX_EXTRA[dtLk()]&&DTX_EXTRA[dtLk()].et)||ET.en,function(v){return v.replace(/\D/g,'').length>=6;}]); }
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
      '.dt-urg-p button:hover{border-color:var(--line-strong,rgba(255,255,255,.25))}.dt-urg-p button[aria-pressed=true]{background:var(--blue,#FFC93C);border-color:var(--blue,#FFC93C);color:#0b0b0b}'+
      '.dt-urg-h{font-size:13px;color:#ff7a45;margin-top:8px;min-height:0}.dt-urg-h:empty{display:none}';
    document.head.appendChild(st);
    function lang(){ return UTX[dtLk()]||UTX.en; }
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
