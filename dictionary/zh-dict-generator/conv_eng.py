import json
import re
class ConversionError(Exception):
  pass

left_conv = [
  ('X', 'O'),
  ('B', 'A'),
  ('G', 'H'),
  ('W', 'R'),
  ('I', 'P'),
  ('U', 'W'),
  ('N', 'T'),
  ('E', 'K'),
  ('A', 'S'),
]

right_conv = [
  ('X', 'E'),
  ('B', 'U'),
  ('Z', '*'),
  ('G', 'F'),
  ('W', 'R'),
  ('I', 'P'),
  ('U', 'B'),
  ('N', 'L'),
  ('E', 'G'),
  ('A', 'T'),
  ('O', 'S'),
  ('d', 'D'),
  ('z', 'Z')
]

def convert_stroke(stroke):
  if re.findall(r'[#0-9]', stroke):
    #print("not converting " + stroke)
    raise ConversionError("Not Supported")
  left = ''
  right = ''
  if '-' in stroke:
    left, right = stroke.split('-')
  elif '*' in stroke:
    left, right = stroke.split('*')
    right = '*' + right
  elif 'O' in stroke:
    left, right = stroke.split('O')
    left += 'O'
  elif 'E' in stroke:
    left, right = stroke.split('E')
    right = 'E' + right
  elif 'A' in stroke:
    left, right = stroke.split('A')
    left += 'A'
  elif 'U' in stroke:
    left, right = stroke.split('U')
    right = 'U' + right
  else:
    left = stroke

  left_out = ''
  right_out = ''

  for yawei, eng in left_conv:
    if eng in left:
      left_out += yawei

  for yawei, eng in right_conv:
    if eng in right:
      right_out += yawei

  return '$' + "".join(left_out) + '-' + "".join(right_out)

yawei_dict = {}
with open('luke_steno_dictionary/english.json', 'r', encoding='utf-8') as f:
  eng_dict = json.load(f)
  for key in eng_dict:
    strokes = key.split('/')
    try:
      strokes = list(map(convert_stroke, strokes))
    except ConversionError:
      continue

    strokes = ["/".join(strokes)]
    # if '*' in strokes[0]:
    #   I = 0
    #   while I < len(strokes):
    #     stroke = strokes[I]
    #     if '*' in stroke:
    #       first_star = stroke.index('*')
    #       assert stroke[first_star + 1] == '-'
    #       strokes[I] = stroke[:first_star] + 'D' + stroke[first_star+1:]
    #       strokes.append(stroke[:first_star] + 'Z' + stroke[first_star+1:])
    #       strokes.append(stroke[:first_star] + '-D' + stroke[first_star+2:])
    #       strokes.append(stroke[:first_star] + '-Z' + stroke[first_star+2:])
    #     else: I += 1
    for stroke in strokes:
      yawei_dict[stroke] = eng_dict[key]

with open('conv_eng.json', 'w', encoding='utf-8') as f:
  json.dump(yawei_dict, f, ensure_ascii=False, indent=0, sort_keys=True)