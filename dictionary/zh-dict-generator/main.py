import csv
import json
import re
from conversion import conversion, inv_conversion, single_freq, double_freq

def read_corpus_file(fname):
    print("Reading corpus: {}".format(fname))
    word_frequency = []
    with open(fname, 'r', encoding='utf-8') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        L = 0
        InList = False
        for row in csvreader:
            # The most common word in chinese in both datasets is 的
            if row[1] == '的':
                InList = True
            if InList:
                L += 1
                word_frequency.append(row[1])
    return word_frequency



#A parser for the CC-Cedict. Convert the Chinese-English dictionary into a list of python dictionaries with "traditional","simplified", "pinyin", and "english" keys.

#Make sure that the cedict_ts.u8 file is in the same folder as this file, and that the name matches the file name on line 13.

#Before starting, open the CEDICT text file and delete the copyright information at the top. Otherwise the program will try to parse it and you will get an error message.

#Characters that are commonly used as surnames have two entries in CC-CEDICT. This program will remove the surname entry if there is another entry for the character. If you want to include the surnames, simply delete lines 59 and 60.

#This code was written by Franki Allegra in February 2020.

#open CEDICT file



with open('cedict_ts.u8', encoding="utf-8") as file:
    text = file.read()
    lines = text.split('\n')
    dict_lines = list(lines)

#define functions

    def parse_line(line):
        parsed = {}
        if line == '':
            dict_lines.remove(line)
            return 0
        line = line.rstrip('/')
        line = line.split('/')
        if len(line) <= 1:
            return 0
        english = line[1]
        char_and_pinyin = line[0].split('[')
        characters = char_and_pinyin[0]
        characters = characters.split()
        traditional = characters[0]
        simplified = characters[1]
        pinyin = char_and_pinyin[1]
        pinyin = pinyin.rstrip()
        pinyin = pinyin.rstrip("]")
        parsed['traditional'] = traditional
        parsed['simplified'] = simplified
        parsed['pinyin'] = pinyin
        parsed['english'] = english
        list_of_dicts.append(parsed)

    def remove_surnames():
        for x in range(len(list_of_dicts)-1, -1, -1):
            if "surname " in list_of_dicts[x]['english']:
                if list_of_dicts[x]['traditional'] == list_of_dicts[x+1]['traditional']:
                    list_of_dicts.pop(x)
            if "variant of" in list_of_dicts[x]['english']:
                list_of_dicts.pop(x)


    def personal_filter():
        for x in range(len(list_of_dicts)-1, -1, -1):
            if list_of_dicts[x]['pinyin'].count(' ') > 1:
                list_of_dicts.pop(x)

    def main():

        #make each line into a dictionary
        print("Parsing dictionary . . .")
        for line in dict_lines:
                parse_line(line)
        
        #remove entries for surnames from the data (optional):

        print("Removing Surnames . . .")
        remove_surnames()
        print("Removing Non two character words . . .")
        #personal_filter()

        return list_of_dicts


        #If you want to save to a database as JSON objects, create a class Word in the Models file of your Django project:

        # print("Saving to database (this may take a few minutes) . . .")
        # for one_dict in list_of_dicts:
        #     new_word = Word(traditional = one_dict["traditional"], simplified = one_dict["simplified"], english = one_dict["english"], pinyin = one_dict["pinyin"], hsk = one_dict["hsk"])
        #     new_word.save()

list_of_dicts = []
parsed_dict = main()

d = {}
sound_frequency = {}
for entry in parsed_dict:
        pinyin = entry['pinyin']
        for c in ['1', '2', '3', '4', '5']:
            pinyin = pinyin.replace(c, '')

        parts = pinyin.lower().split(' ')

        if len(parts) != len(entry['traditional']):
            #{'traditional': '兙', 'simplified': '兙', 'pinyin': 'shi2 ke4', 'english': 'decagram (old)'}
            # This shouldn't be here
            continue
        elif set(parts) - set(conversion):
            # There are parts that couldn't be converted
           # print('cannot convert: ' + str(parts))
            continue

        if len(parts) == 2:
            if entry['traditional'][0] in sound_frequency:
                sound_frequency[entry['traditional'][0]].setdefault(conversion[parts[0]], 0)
                sound_frequency[entry['traditional'][0]][conversion[parts[0]]] += 1
            else:
                sound_frequency[entry['traditional'][0]]= { conversion[parts[0]]: 1 }

            if entry['traditional'][1] in sound_frequency:
                sound_frequency[entry['traditional'][1]].setdefault(conversion[parts[1]], 0)
                sound_frequency[entry['traditional'][1]][conversion[parts[1]]] += 1
            else:
                sound_frequency[entry['traditional'][1]]= { conversion[parts[1]]: 1 }
            

        strokes = []
        while len(parts) > 1:
            left = parts.pop(0)
            right = parts.pop(0)
            strokes.append(conversion[left] + '-' + conversion[right])
        
        if len(parts) > 0:
            strokes.append('-' + conversion[parts[0]])
        
        key = '/'.join(strokes)

        if key in d:
            d[key].append(entry)
        else:
            d[key] = [entry]


def keywithmaxval(d):
     """ a) create a list of the dict's keys and values; 
         b) return the key with the max value"""  
     v=list(d.values())
     k=list(d.keys())
     return k[v.index(max(v))]

sound_frequency = { k: keywithmaxval(v) for k, v in sound_frequency.items()}

d = {k: list(filter(lambda x: len(x['traditional']) != 1 or x['traditional'] not in sound_frequency or sound_frequency[x['traditional']] == k[1:], v)) for k, v in d.items()}
CHARACTER_SET = 'traditional'

base_dict = dict(filter(lambda x: len(x[1]) == 1, d.items()))
conflict_dict = dict(filter(lambda x: len(x[1]) > 1, d.items()))

def write_dict(fname, d):
    with open(fname, 'w', encoding='utf-8') as outfile:
        outfile.write('{\n')
        NeedComma = False
        for key in d:
            if key == "W-W":
                continue

            stroke = re.sub('^-', 'X-', key)
            stroke = re.sub('/-', '/X-', stroke)
            for entry in d[key]:
                if NeedComma:
                    outfile.write(',\n')
                NeedComma = True
                outfile.write('"{}": "{}"'.format(stroke, entry[CHARACTER_SET]))
        
        outfile.write('\n}')

# Write out all non-conflicting entries
write_dict('build/base.json', base_dict)

tw_corp = read_corpus_file('corpus/tw.csv')
cn_corp = read_corpus_file('corpus/cn.csv')
tw_set = set(tw_corp[:40000])
cn_set = set(cn_corp[:5000])
corp_set = set()
corp_set |= tw_set
corp_set |= cn_set

with open('build/not-in-corpus.txt', 'w', encoding='utf-8') as f:
    for steno in conflict_dict:
        for entry in conflict_dict[steno]:
            if len(entry['traditional']) <3 and entry['traditional'] not in corp_set and entry['simplified'] not in corp_set:
                f.write("{}\n".format(entry['traditional']))


print("Default amount of conflicts = {}".format(len(dict(filter(lambda x: len(x[1]) > 1, d.items())))))
n_dict = {k: list(filter(lambda x: len(x['traditional']) > 2 or  x['simplified'] in corp_set or x['traditional'] in corp_set, v)) for k, v in conflict_dict.items()}
conflict_base = dict(filter(lambda x: len(x[1]) == 1, n_dict.items()))
conflict_dict = dict(filter(lambda x: len(x[1]) > 1, n_dict.items()))
print("Conflicts after non-corpus removal = {}".format(len(dict(filter(lambda x: len(x[1]) > 1, n_dict.items())))))
print("Resolved words = {}".format(len(conflict_base)))

write_dict('build/corpus-base.json', conflict_base)


def raw_get_freq(corp, word):
    try:
        return corp.index(word)
    except ValueError:
        return 9999999

def get_freq(entry):
    if entry['simplified'] not in cn_set and entry['traditional'] not in tw_set:
        return 9999999
    elif entry['simplified'] not in cn_set:
        return tw_corp.index(entry['traditional'])
    elif entry['traditional'] not in tw_set:
        return cn_corp.index(entry['simplified'])
    else:
        return min(cn_corp.index(entry['simplified']), tw_corp.index(entry['traditional']))

def filter_out_duplicates(entries):
    new_entries = []
    for entry in entries:
        AlreadyExists = False
        for test in new_entries:
            if entry['simplified'] == test['simplified'] and entry['traditional'] == test['traditional']:
                AlreadyExists = True

        if AlreadyExists == False:
            new_entries.append(entry)
    return new_entries
conflict_dict = {k: sorted(filter_out_duplicates(v), key=lambda x: get_freq(x)) for k, v in conflict_dict.items()}

sorted_keys = sorted(list(conflict_dict.keys()), key=lambda key: get_freq(conflict_dict[key][0]))
print("Maximum amount of words in a conflict group = {}".format(
    len(max(conflict_dict.values(), key=lambda entry: len(entry)))
))
print(max(conflict_dict.values(), key=lambda entry: len(entry)))
a = [0 for i in range(200)]
for value in conflict_dict.values():
    a[len(value)] += 1
print(a)

brief_obj = {}
brief_chars = set()
with open('brief_one_stroke.json', 'r', encoding='utf-8') as brief_file:
    brief_obj = json.load(brief_file)
    brief_chars.update(brief_obj.values())

def output_completions(f, prev_strokes, stroke, word):
    if len(word) != 1:
        return
    parts = stroke.split('-')
    for prev_possibility in single_freq:
        f.write(',\n"{}{}-{}/{}": "{}"'.format(prev_strokes, prev_possibility, parts[1], parts[0], word))

with open('build/conflicts.json', 'w', encoding='utf-8') as outfile, open('build/select.json', 'w', encoding='utf-8') as select_file:
    outfile.write('{\n')
    select_file.write('{\n"":""')
    NeedComma = False
    for key in sorted_keys:
        if key == "W-W" or key == '-W':
            continue
        I = 0
        Translations = conflict_dict[key]
        last_stroke = key.split('/')[-1]
        prev_strokes = '/'.join(key.split('/')[:-1] + [''])
        for word in Translations:
            
            if last_stroke[0] == '-':
                if word[CHARACTER_SET] in brief_chars:
                    continue
                while I < len(single_freq) and "{}{}{}".format(prev_strokes, single_freq[I], key) in brief_obj:
                    I += 1

            if (last_stroke[0] == '-' and I >= len(single_freq)) or (last_stroke[0] != '-' and I >= len(double_freq)):
                print("Cannot write {}".format(key))
                if last_stroke[1:] in inv_conversion:
                    print(" ↳ {}".format(inv_conversion[key[1:]]))
                break

            if NeedComma:
                outfile.write(',\n')

            if last_stroke[0] == '-':
                #outfile.write('"{}{}/{}": "{}",\n'.format(prev_strokes, last_stroke, single_freq[I], word[CHARACTER_SET]))
                outfile.write('"{}{}{}": "{}"'.format(prev_strokes, single_freq[I], last_stroke, word[CHARACTER_SET]))
                output_completions(select_file, prev_strokes, single_freq[I] + key, word[CHARACTER_SET])
            elif last_stroke[0] != '-' and I != 0:
                outfile.write('"{}/{}": "{}"'.format(key, double_freq[I-1], word[CHARACTER_SET]))
            elif last_stroke[0] != '-':
                outfile.write('"{}": "{}"'.format(key, word[CHARACTER_SET]))
            I += 1

            NeedComma = True
    for stroke in brief_obj:
        output_completions(select_file, '', stroke, brief_obj[stroke])
    outfile.write('\n}')
    select_file.write("\n}")



# for i in [1000, 2000, 3000, 4000, 5000, 8000, 10000, 12000, 15000, 20000, 30000, 40000, 99999]:
#     cn_freq = set(cn_corp[:i])
#     tw_freq = set(tw_corp[:i])

#     with open('build/corpus/cn-{}.txt'.format(i), 'w', encoding='utf-8') as f:
#         for char in cn_corp[:i]:
#             f.write('{}\n'.format(char))

#     with open('build/corpus/tw-{}.txt'.format(i), 'w', encoding='utf-8') as f:
#         for char in tw_corp[:i]:
#             f.write('{}\n'.format(char))

    
#     cn_dict = {k: list(filter(lambda x: x['simplified'] in cn_freq, v)) for k, v in conflict_dict.items()}
    
#     tw_dict = {k: list(filter(lambda x: x['traditional'] in tw_freq, v)) for k, v in conflict_dict.items()}
    
#     both_dict = {k: list(filter(lambda x: x['simplified'] in cn_freq or x['traditional'] in tw_freq, v)) for k, v in conflict_dict.items()}
    
#     print("Number of conflicts at {:>5} (cn/tw/both): {:>5} {:>5} {:>5}".format(
#         i,
#         len(list(filter(lambda x: len(x[1]) > 1, cn_dict.items()))),
#         len(list(filter(lambda x: len(x[1]) > 1, tw_dict.items()))),
#         len(list(filter(lambda x: len(x[1]) > 1, both_dict.items())))
#     ))

    