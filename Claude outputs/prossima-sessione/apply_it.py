# Uso (dalla radice del sito): python3 "Claude outputs/prossima-sessione/apply_it.py" [--dry]
# Applica it_fix_*.py (R = {k: dict(campo=valore)}) a strumenti/dati_fiere_nuove_3.py e _4.py, sostituendo
# solo il testo dei campi indicati (via ast), senza toccare il resto del file.
import ast, glob, os, sys, pprint
here = os.path.dirname(os.path.abspath(__file__)); dry = '--dry' in sys.argv
R = {}
for fn in sorted(glob.glob(f'{here}/it_fix_*.py')):
    g = {}; exec(open(fn, encoding='utf-8').read(), g); R.update(g['R'])
done = set()
for fn in ['strumenti/dati_fiere_nuove_3.py', 'strumenti/dati_fiere_nuove_4.py']:
    src = open(fn, encoding='utf-8').read(); tree = ast.parse(src)
    lines = src.splitlines(keepends=True); off = [0]
    for l in lines: off.append(off[-1] + len(l))
    pos = lambda ln, col: off[ln - 1] + len(lines[ln - 1].encode('utf-8')[:col].decode('utf-8'))
    params = None
    for n in tree.body:
        if isinstance(n, ast.FunctionDef) and n.name == 'fiera': params = [a.arg for a in n.args.args]
    reps = []
    for n in ast.walk(tree):
        if not isinstance(n, ast.Call) or not isinstance(n.func, ast.Name) or n.func.id not in ('fiera', 'dict'): continue
        args = {}
        if n.func.id == 'fiera':
            for i, a in enumerate(n.args): args[params[i]] = a
        for kw in n.keywords:
            if kw.arg: args[kw.arg] = kw.value
        if 'k' not in args or not isinstance(args['k'], ast.Constant): continue
        k = args['k'].value
        if k not in R: continue
        for campo, val in R[k].items():
            node = args[campo]
            reps.append((pos(node.lineno, node.col_offset), pos(node.end_lineno, node.end_col_offset), pprint.pformat(val, width=220, sort_dicts=False).replace('\n', '\n ')))
        done.add(k)
    for a, b, t in sorted(reps, reverse=True): src = src[:a] + t + src[b:]
    compile(src, fn, 'exec')
    if not dry: open(fn, 'w', encoding='utf-8').write(src)
print('applicate:', len(done), '| non trovate:', sorted(set(R) - done))
