"""Verify bibliographic references against Crossref (title + first author); writes lit/crossref_verified.json."""
import json, os, re, sys, time, urllib.parse, urllib.request
from difflib import SequenceMatcher
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, '..', 'lit', 'crossref_verified.json')
REFS = [l.split('|') for l in open(os.path.join(HERE, '..', 'lit', 'candidates.txt'), encoding='utf-8').read().strip().splitlines() if l.strip()]
res = json.load(open(OUT)) if os.path.exists(OUT) else {}
for key, author, title in REFS:
    if key in res and res[key].get('ok'):
        continue
    q = urllib.parse.urlencode({'query.bibliographic': title, 'query.author': author, 'rows': 6,
                                'select': 'DOI,title,author,container-title,issued,volume,issue,page,type,publisher'})
    req = urllib.request.Request('https://api.crossref.org/works?' + q, headers={'User-Agent': 'rent-determinants-lit-check/1.0 (mailto:research@example.org)'})
    items = None
    for k in range(5):
        try:
            items = json.load(urllib.request.urlopen(req, timeout=40))['message']['items']; break
        except Exception as e:
            err = str(e); time.sleep(5 * (k + 1))
    if items is None:
        res[key] = {'ok': False, 'err': err}; continue
    best = None
    for it in items:
        t = re.sub(r'<[^>]+>', '', (it.get('title') or [''])[0]).strip()
        s = SequenceMatcher(None, t.lower(), title.lower()).ratio()
        s += 0.05 if it.get('type') in ('journal-article', 'book') else 0      # prefer the published version over SSRN/NBER copies
        if best is None or s > best[0]:
            best = (s, it)
    s, it = best
    au = [f"{a.get('family','')}, {a.get('given','')}" for a in it.get('author', [])]
    res[key] = {'ok': s > 0.85, 'sim': round(s, 3), 'title': re.sub(r'<[^>]+>', '', (it.get('title') or [''])[0]).strip(), 'authors': au,
                'journal': (it.get('container-title') or [''])[0], 'year': (it.get('issued', {}).get('date-parts') or [[None]])[0][0],
                'volume': it.get('volume'), 'issue': it.get('issue'), 'pages': it.get('page'), 'doi': it.get('DOI'), 'type': it.get('type')}
    time.sleep(2.0)
json.dump(res, open(OUT, 'w'), indent=1, ensure_ascii=False)
for k, v in res.items():
    if v.get('ok'):
        print(f"OK  {k}: {'; '.join(a.split(',')[0] for a in v['authors'][:4])} ({v['year']}) {v['title'][:80]} | {v['journal']} {v['volume']}({v['issue']}):{v['pages']} doi:{v['doi']}")
    else:
        print(f"??  {k}: sim={v.get('sim')} -> {v.get('title','')[:80]} | {v.get('journal')} {v.get('year')} {v.get('err','')}")
