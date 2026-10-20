# -*- coding: utf-8 -*-
"""从「掉落概率基准.csv」生成 drop-sources.js（配装器掉落索引）
用法: python3 gen_drop_sources.py [csv路径] [输出路径]
"""
import csv, json, os, sys

SRC = sys.argv[1] if len(sys.argv) > 1 else '/vol2/1000/存储/虾/Minecraft_Dungeons_II_装备档案/data/csv/掉落概率基准.csv'
OUT = sys.argv[2] if len(sys.argv) > 2 else os.path.join(os.path.dirname(os.path.abspath(__file__)), 'drop-sources.js')

rows = list(csv.DictReader(open(SRC, encoding='utf-8-sig')))
idx = {}
for r in rows:
    iid = (r.get('物品ID') or '').strip()
    if not iid:
        continue
    d = idx.setdefault(iid, {'a': [], 's': {}})
    area = (r.get('区域池') or '').strip()
    if area and area not in d['a']:
        d['a'].append(area)
    key = ((r.get('来源') or '').strip(), (r.get('领取或出现条件') or '').strip())
    try:
        prob = float(r.get('至少一件概率') or 0)
    except ValueError:
        prob = 0.0
    if key not in d['s'] or prob > d['s'][key]:
        d['s'][key] = prob

out = {}
for iid, d in idx.items():
    items = sorted(d['s'].items(), key=lambda kv: -kv[1])[:6]
    out[iid] = {'a': d['a'][:4], 's': [[s, c, round(p, 4)] for (s, c), p in items]}

open(OUT, 'w', encoding='utf-8').write('window.DROP_SRC=' + json.dumps(out, ensure_ascii=False, separators=(',', ':')) + ';' + chr(10))
print('物品:', len(out), '大小: %.1f KB' % (os.path.getsize(OUT) / 1024))