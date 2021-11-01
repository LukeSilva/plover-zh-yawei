import json
import sys
import os


english_default = ["other_dictionaries/main.json", "other_dictionaries/q-and-a.json", "other_dictionaries/common.json", "stenodict/movement.json", "stenodict/modifier.json", "stenodict/single_stroke_commands_v1.json", "luke.json", "misc.json"]
targets = {
  "chinese": {
    "display_name": "Chinese",
    "folder": "zh-dict",
    "files": {
      "default": "main.json",
      "brief": "brief.json",
    },
    "build": {
      "default": ["../zh-dict-generator/out/combined.json", "main.json", "brief.json"]
    }
  }
}

try: 
    os.makedirs('backup')
except OSError:
    if not os.path.isdir('backup'):
        raise

def read_json(folder, fname, language = ''):
  try:
    tmp_file = open(os.path.join(folder, fname),'r', encoding="utf-8")
    tmp_json = json.load(tmp_file)
    tmp_file.close()

    tmp_bak_file = open(os.path.join('backup', language + '_' + fname +'.bak'), 'w', encoding="utf-8")
    json.dump(tmp_json, tmp_bak_file, indent=0, sort_keys=True,  ensure_ascii=False)
    tmp_bak_file.close()
    
    return tmp_json
  except FileNotFoundError as e:
    return {}

def read_jsons(t, name):
  json_files = {}
  for key in t["files"]:
    json_files[key] = read_json(t["folder"], t["files"][key], name)

  return json_files


def write_jsons(t, name, json_files):
  for key in t["files"]:
    f = open(os.path.join(t["folder"], t["files"][key]),'w', encoding="utf-8")
    json.dump(json_files[key], f, indent=0, ensure_ascii=False, sort_keys=True)
    f.close()


# def read_tmp(t, name):
#   tmp_file = open(os.path.join(t["folder"], name + '.json'),'r', encoding="utf-8")
#   tmp_json = json.load(tmp_file)
#   tmp_file.close()

#   tmp_bak_file = open(os.path.join('backup', name +'.json.bak'), 'w', encoding="utf-8")
#   json.dump(tmp_json, tmp_bak_file, indent=0, sort_keys=True)
#   tmp_bak_file.close()

#   return tmp_json


def build_target(folder, b, name):
  out_json = {}
  for fname in b:
    f = open(os.path.join(folder, fname), 'r', encoding="utf-8")
    f_json = json.load(f)
    f.close()

    for k in f_json:
      out_json[k] = f_json[k]

  f = open(name + '.json', 'w', encoding="utf-8")
  json.dump(out_json, f, indent=0, ensure_ascii=False, sort_keys=True)
  f.close()


def process_target(t, name, build_name = None):

  if build_name is None:
    try:
      with open(os.path.join(name, 'default_build'), 'r', encoding="utf-8") as f:
        build_name = f.readlines()[0].strip()
        if not build_name in t['build']:
          build_name = 'default'
    except IOError:
      build_name = 'default'


  display_name = t.get('display_name', name)
  print('Processing ' + display_name)

  json_files = read_jsons(t, name)
  tmp_json = read_json(t["folder"], name + '_tmp.json')

  key_list = list(tmp_json.keys())
    
  for i in range(len(key_list)): #because we need to change tmp_json
    key = key_list[i]

    cmd = input(display_name + '=> "' + key + '": "' + tmp_json[key] + '" (' + str(i) + '/' + str(len(key_list)) + ')')
    if cmd == '':
        cmd = 'default'

    if cmd == 'quit':
        break
    elif cmd == 'd' or cmd == 'del' or cmd == 'delete':
        del tmp_json[key]
    elif cmd in json_files:
        json_files[cmd][key] = tmp_json[key]
        del tmp_json[key]
    else:
        print('Unknown response, ignoring...')

  write_jsons(t, name, json_files)

  tmp_file = open(os.path.join(t["folder"], name) + '_tmp.json', 'w', encoding="utf-8")
  json.dump(tmp_json, tmp_file, indent=0, ensure_ascii=False, sort_keys=True)
  tmp_file.close()

  b = t["build"][build_name]

  if sys.platform.startswith('darwin'):
    b = t["build"].get(build_name + "_mac", b)

  print('Building ' + display_name + ':' + build_name)
  build_target(t["folder"], b, name)


def split_tmp():
  new_entries = read_json('','tmp.json')
  en = read_json('en-dict', 'english_tmp.json')
  zw = read_json('zh-dict', 'chinese_tmp.json')

  for key in new_entries:
    if key.upper() == key:
      en[key] = new_entries[key]
    else:
      zw[key] = new_entries[key]

  f = open(os.path.join('en-dict', 'english_tmp.json'), 'w', encoding='utf-8')
  json.dump(en, f, indent=0, sort_keys=True, ensure_ascii=False)
  f.close()
  f = open(os.path.join('zh-dict', 'chinese_tmp.json'), 'w', encoding='utf-8')
  json.dump(zw, f, indent=0, sort_keys=True, ensure_ascii=False)
  f.close()

  f = open('tmp.json', 'w')
  f.write('{}')
  f.close()

if __name__ == "__main__":
  split_tmp()
  for target in targets:
    process_target(targets[target], target)
