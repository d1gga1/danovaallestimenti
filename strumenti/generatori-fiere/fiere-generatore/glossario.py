# -*- coding: utf-8 -*-
import os,re,json,html
R=os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','..')); G='https://danova-tech.com/glossario/'
T=[("stand-preallestito","Stand preallestito","Uno stand con pareti, moquette, illuminazione, insegna e arredi base già previsti, spesso a noleggio. È la soluzione più rapida ed economica da organizzare, adatta alla prima fiera o agli spazi piccoli.",'/noleggio-stand-fieristici/'),
("stand-modulare","Stand modulare","Uno stand costruito con telai e pannelli componibili, di solito in alluminio, che si smontano e si rimontano su metrature e forme diverse. Conviene a chi fa molte fiere, perché la struttura si riutilizza e cambiano solo grafiche e arredi.",'/stand-modulari/'),
("tessuto-teso","Tessuto teso","Grafica stampata su tessuto e montata in tensione su un telaio leggero. Permette immagini molto grandi senza giunture, si trasporta piegata e si sostituisce facilmente da una fiera all'altra.",'/stand-modulari/'),
("stand-su-misura","Stand su misura","Uno stand progettato e costruito da zero, spesso in legno, su forme, materiali e finiture scelte per il marchio. Costa di più di un modulare, ma comunica di più e può integrare elementi riutilizzabili.",'/stand-fieristici-su-misura/'),
("stand-a-isola","Stand a isola","Uno spazio espositivo libero su quattro lati, visibile da tutte le direzioni. Ha più visibilità ma richiede un progetto pensato a 360 gradi; gli altri tipi di spazio sono in linea (un lato aperto), ad angolo (due) e a penisola (tre).",'/stand-fieristici-su-misura/'),
("regolamento-tecnico","Regolamento tecnico di fiera","Le regole che ogni quartiere fieristico impone agli allestimenti: altezze massime, materiali ammessi, impianti, sicurezza, scadenze per presentare il progetto e orari di montaggio. Uno stand non conforme può non essere approvato.",'/montaggio-stand-fieristici/'),
("allestimento-disallestimento","Allestimento e disallestimento","I giorni, fissati dall'organizzatore, in cui gli stand si montano prima dell'apertura (allestimento) e si smontano dopo la chiusura (disallestimento). Sono finestre strette: materiali e squadre vanno organizzati in anticipo.",'/montaggio-stand-fieristici/'),
("dichiarazione-conformita","Dichiarazione di conformità dell'impianto","Il documento con cui l'installatore certifica che l'impianto elettrico dello stand è eseguito a regola d'arte. Nelle fiere italiane viene richiesto per allacciare lo stand alla rete del padiglione.",'/servizi/allestimenti-fieristici/')]
p=os.path.join(R,'glossario/index.html'); s=open(p,encoding='utf-8').read()
if 'id="fiere"' not in s:
    body=''.join(f'<h3 id="{i}">{n}</h3><p>{d} <a href="{u}">Approfondisci</a>.</p>' for i,n,d,u in T)
    sec=f'<section id="fiere"><div class="wrap"><div class="sec-head"><h2 class="title" data-rv="up">Fiere e allestimenti</h2></div><div class="pg-testo gloss" data-rv="up">{body}</div></div></section>\n'
    k=s.index('<section><div class="wrap"><div class="sec-head"><h2 class="title">Pagine collegate</h2>')
    s=s[:k]+sec+s[k:]
    s=s.replace('<a href="#ads">Pubblicità online</a>','<a href="#ads">Pubblicità online</a><a href="#fiere">Fiere e allestimenti</a>',1)
    s=s.replace('<a href="/servizi/">Tutti i servizi</a>','<a href="/servizi/">Tutti i servizi</a><a href="/servizi/allestimenti-fieristici/">Allestimenti fieristici</a>',1)
    m=re.search(r'(<script type="application/ld\+json">)(.*?)(</script>)',s,re.S); g=json.loads(m.group(2))
    for nd in g['@graph']:
        if nd.get('@type')=='DefinedTermSet':
            for i,n,d,u in T: nd['hasDefinedTerm'].append({"@type":"DefinedTerm","@id":G+'#'+i,"name":n,"description":d,"inDefinedTermSet":{"@id":G+"#glossario"},"url":G+'#'+i})
    s=s[:m.start(2)]+'\n'+json.dumps(g,ensure_ascii=False,indent=2)+'\n'+s[m.end(2):]
    s=s.replace('Queste sono 50 definizioni','Queste sono 58 definizioni')
    open(p,'w',encoding='utf-8').write(s); print('glossario ok')
# guide index: card in testa
p=os.path.join(R,'guide/index.html'); s=open(p,encoding='utf-8').read()
if 'come-preparare-una-fiera' not in s:
    card='<a class="sect sect-zone" href="/guide/come-preparare-una-fiera/"><div class="ic"><svg width="21" height="21" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="17" rx="2"></rect><path d="M8 2v4M16 2v4M3 10h18"></path><path d="m9 15 2 2 4-4"></path></svg></div><h4>Come preparare una fiera: la checklist completa</h4><p>Cosa fare mese per mese, dalla scelta della fiera allo stand, dagli inviti ai contatti da richiamare. E gli errori che costano di più.</p><span class="go">Leggi la guida <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M13 6l6 6-6 6"></path></svg></span></a>'
    s=s.replace('<div class="sect-grid">',f'<div class="sect-grid">{card}',1)
    m=re.search(r'(<script type="application/ld\+json">)(.*?)(</script>)',s,re.S); g=json.loads(m.group(2))
    def walk(o):
        if isinstance(o,dict):
            if o.get('@type')=='ItemList' and isinstance(o.get('itemListElement'),list):
                L=o['itemListElement']; L.append({"@type":"ListItem","position":len(L)+1,"name":"Come preparare una fiera: la checklist completa","url":"https://danova-tech.com/guide/come-preparare-una-fiera/"}); return True
            return any(walk(v) for v in o.values())
        if isinstance(o,list): return any(walk(v) for v in o)
    print('itemlist guide',walk(g))
    s=s[:m.start(2)]+'\n'+json.dumps(g,ensure_ascii=False,indent=2)+'\n'+s[m.end(2):]
    open(p,'w',encoding='utf-8').write(s); print('guide ok')
# servizi index: link al cluster nel paragrafo della card
p=os.path.join(R,'servizi/index.html'); s=open(p,encoding='utf-8').read()
old='Per aziende di ogni settore, con un unico referente.</p>'
if old in s and 'stand-modulari' not in s:
    s=s.replace(old,'Per aziende di ogni settore, in Italia e all\'estero: <a href="/montaggio-stand-fieristici/">montaggio stand</a>, <a href="/stand-fieristici-su-misura/">stand su misura</a>, <a href="/stand-modulari/">stand modulari</a> e <a href="/noleggio-stand-fieristici/">noleggio</a>.</p>',1)
    open(p,'w',encoding='utf-8').write(s); print('servizi ok')
