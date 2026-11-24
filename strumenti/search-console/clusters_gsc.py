import csv,re,sys
r=list(csv.DictReader(open(sys.argv[1])))
C=[
('Noleggio arredi stand (Rho/Milano)', r'arred|mobili|lounge|desk|bancon|sollevamento'),
('Rendering stand', r'render'),
('MEDICA / Düsseldorf / Colonia NL-EN-DE', r'medica|d[uü]sseldorf|keulen|standbouw|standbouwer|standenbouwer|compamed'),
('Hannover (Messe, messestand)', r'hannover'),
('Bologna in inglese', r'(builder|contractor|design|booth|manufacturer|construction|companies).*bologna|bologna.*(builder|stand$)|custom stand bologna'),
('Milano/Parma/Rimini/Firenze/Venezia/Genova in inglese', r'(builder|contractor|booth|design|construction|manufacturer).*(milan|parma|rimini|florence|venice|genoa)'),
('Lugano / Ticino', r'lugano'),
('Varese-Novara-Como (stampa stand, totem)', r'luino|tradate|malnate|varese|gallarate|busto|castelletto|arona|\boleggio|novara|como$|somma lombardo|laveno|cassano magnago|dormelletto|cant[uù]|lainate|stand fieristici pero|stand fieristici rho'),
('Palermo / Sicilia / Sardegna', r'palermo|sicilia|sardegna'),
('Toscana / Chianti', r'chianti|toscana|pistoia'),
('Stand modulari / componibili', r'modular|componibil'),
('Noleggio / affitto stand', r'noleggio stand|stand noleggio|affitto|stand mieten|stand rent|noleggio allestimenti|noleggio stand'),
('Chiavi in mano', r'chiavi in mano'),
('Idee / esempi stand', r'idee|esempi|immagini stand|innovativ'),
('Congressi / convention / corporate', r'congress|convention|corporate|portanomi'),
('Showroom', r'showroom'),
('Fiere meccanica / metalmeccanica', r'meccanica|metalmeccan|macchine industriali|fiera industria'),
('Fiere tecnologia / elettronica', r'elettronic|tecnologia|informatica|computer|electronica'),
('Calendari Parma', r'parma.*(calend|202|fiere)|(calend|fiere|fiera).*parma'),
('Calendari Bologna', r'(calend|fiere|fiera|prossim).*bologna|bologna.*(calend|fier)'),
('Calendari Rimini', r'(calend|fiere|fiera).*rimini|rimini.*calend'),
('Calendari Milano / Rho', r'(calend|fiere|fiera|eventi).*(milano|rho)|rho fiera calend|fiera milano'),
('Turismo / alberghiere', r'turism|alberghier|viaggi'),
('Ledwall noleggio', r'ledwall|videowall|led noleggio|noleggio operativo led|totem led'),
('Grafica / stampa', r'grafic|stampa'),
('Stand in cartone', r'cartone'),
('Ecologici / sostenibili', r'ecolog|ecosostenib|riciclabil|sostenibil'),
('Food / cantine / enogastronomici', r'enogastronom|gastronomic|cantine|stand cucina'),
('Vicenzaoro T-Gold', r't-gold'),
('Soppalcati / due piani', r'soppalc|due piani'),
('Fiere avicole / zootecnia / agricole', r'avicol|zootecn|agricol|agricoltura'),
('Brand Danova', r'danova'),
('Arredo urbano', r'arredo urbano'),
]
rows=[]
for name,pat in C:
    m=[x for x in r if re.search(pat,x['Query più frequenti'])]
    imp=sum(int(x['Impressioni']) for x in m); clk=sum(int(x['Clic']) for x in m)
    pos=sum(float(x['Posizione'])*int(x['Impressioni']) for x in m)/imp if imp else 0
    rows.append((imp,name,len(m),clk,round(pos,1)))
for x in sorted(rows,reverse=True): print(*x,sep=' | ')
