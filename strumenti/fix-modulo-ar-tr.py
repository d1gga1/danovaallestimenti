#!/usr/bin/env python3
"""24/11/2026: traduce in arabo e turco il modulo contatti in fondo alle pagine ar/ e tr/
(il modello copiato era in inglese). Rilanciare dopo aver rigenerato pagine ar/ o tr/.
Uso: python3 strumenti/fix-modulo-ar-tr.py"""
import glob, os
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
WA = '<a href="https://wa.me/393884706887" target="_blank" rel="noopener">WhatsApp</a>'
TEL = '<a href="tel:+393884706887">+39 388 470 6887</a>'
NOTE_EN = f'We reply within 24 working hours. Prefer to talk? Call {TEL} or message us on {WA}.'
R = {
 'ar': [('>Name and company<', '>الاسم والشركة<'), ('>Email<', '>البريد الإلكتروني<'), ('>Phone (optional)<', '>الهاتف (اختياري)<'),
        ('>What do you need?<', '>ما الذي تحتاجه؟<'), ('>Send request<', '>إرسال الطلب<'), ('aria-label="Leave empty"', 'aria-label="اتركه فارغاً"'),
        (NOTE_EN, f'نرد خلال 24 ساعة عمل. تفضّل التحدث؟ اتصل على <span dir="ltr">{TEL}</span> أو راسلنا عبر {WA} (بالإنجليزية أو الإيطالية).')],
 'tr': [('>Name and company<', '>Ad ve firma<'), ('>Email<', '>E-posta<'), ('>Phone (optional)<', '>Telefon (isteğe bağlı)<'),
        ('>What do you need?<', '>Neye ihtiyacınız var?<'), ('>Send request<', '>Talep gönder<'), ('aria-label="Leave empty"', 'aria-label="Boş bırakın"'),
        (NOTE_EN, f'24 iş saati içinde yanıt veriyoruz. Konuşmayı mı tercih edersiniz? {TEL} numarasını arayın veya {WA} üzerinden yazın (İngilizce veya İtalyanca).')],
}
n = 0
for lg, rep in R.items():
    for p in glob.glob(f'{lg}/**/index.html', recursive=True):
        s = open(p, encoding='utf-8').read()
        i, j = s.find('<form class="dt-lead"'), s.find('</form>', s.find('<form class="dt-lead"'))
        if i < 0: continue
        f = s[i:j]; g = f
        for a, b in rep: g = g.replace(a, b)
        if g != f:
            open(p, 'w', encoding='utf-8').write(s[:i] + g + s[j:]); n += 1; print('ok', p)
print('pagine corrette:', n)
