import json

out_dict = {}
files = ['base', 'corpus-base', 'conflicts']
for fname in files:
  with open('build/{}.json'.format(fname), 'r', encoding='utf-8') as f:
    obj = json.load(f)
    for key in obj:
      out_dict[key.lower()] = obj[key]

with open('out/combined_no_select_no_briefs.json', 'w', encoding='utf-8') as f:
  json.dump(out_dict, f, ensure_ascii=False, indent=0)

select = {}
with open('build/select.json', 'r', encoding='utf-8') as f:
  select = json.load(f)
  for key in select:
    out_dict[key.lower()] = select[key]


with open('out/combined_no_briefs.json', 'w', encoding='utf-8') as f:
  json.dump(out_dict, f, ensure_ascii=False, indent=0)

with open('out/select.json', 'w', encoding='utf-8') as f:
  json.dump(select, f, ensure_ascii=False, indent=0)

one_stroke_briefs = {}
with open('brief_one_stroke.json', 'r', encoding='utf-8') as f:
  one_stroke_briefs = json.load(f)
  for key in one_stroke_briefs:
    out_dict[key.lower()] = one_stroke_briefs[key]


with open('out/combined.json', 'w', encoding='utf-8') as f:
  json.dump(out_dict, f, ensure_ascii=False, indent=0)
  

with open('out/briefs.json', 'w', encoding='utf-8') as f:
  json.dump(one_stroke_briefs, f, ensure_ascii=False, indent=0)
  