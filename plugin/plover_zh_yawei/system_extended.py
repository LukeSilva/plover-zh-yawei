# SKPMTF*RNLYOEAUIln$DC
KEYS = (

    '中-', '英-', '#-',
    
    'x-', 'b-', 'd-', 'z-', 'g-', 'w-', 'i-', 'u-', 'n-', 'e-', 'a-', 'o-',

    'S-', 'T-', 'K-', 'P-', 'W-', 'H-', 'R-',
    'A-', 'O-',
    '*',
    '-E', '-U',
    '-F', '-R', '-P', '-B', '-L', '-G', '-T', '-S',

    '-x', '-b', '-d', '-z', '-g', '-w', '-i', '-u', '-n', '-e', '-a', '-o',
    '-D', '-Z'
)
IMPLICIT_HYPHEN_KEYS = ('A-', 'O-', '5-', '0-', '-E', '-U', '*')
SUFFIX_KEYS = ('-Z', '-D', '-S', '-G', 'w-', '-w')

NUMBER_KEY = '#-'

NUMBERS = {
    'S-': '1-',
    'T-': '2-',
    'P-': '3-',
    'H-': '4-',
    'A-': '5-',
    'O-': '0-',
    '-F': '-6',
    '-P': '-7',
    '-L': '-8',
    '-T': '-9',
}
# NUMBERS = [
#     ('a-', 'S-'),
#     ('o-', 'S-'),
#     ('n-', 'T-'),
#     ('e-', 'K-'),
#     ('i-', 'P-'),
#     ('u-', 'W-'),
#     ('g-', 'H-'),
#     ('w-', 'R-'),
#     ('b-', 'A-'),
#     ('x-', 'O-'),
#     ('d-', '*'),
#     ('z-', '*'),
#     ('-d', '*'),
#     ('-z', '*'),
#     ('-x', '-E'),
#     ('-b', '-U'),
#     ('-g', '-F'),
#     ('-w', '-R'),
#     ('-i', '-P'),
#     ('-u', '-B'),
#     ('-n', '-L'),
#     ('-e', '-G'),
#     ('-a', '-T'),
#     ('-o', '-S'),
# ]

UNDO_STROKE_STENO = '*'

ORTHOGRAPHY_RULES = [
    # == +ly ==
    # artistic + ly = artistically
    (r'^(.*[aeiou]c) \^ ly$', r'\1ally'),
    # humble + ly = humbly (*humblely)
    # questionable +ly = questionably
    # triple +ly = triply
    (r'^(.+[aeioubmnp])le \^ ly$', r'\1ly'),

    # == +ry ==
    # statute + ry = statutory
    (r'^(.*t)e \^ (ry|ary)$', r'\1ory'),
    # confirm +tory = confirmatory (*confirmtory)
    (r'^(.+)m \^ tor(y|ily)$', r'\1mator\2'),
    # supervise +ary = supervisory (*supervisary)
    (r'^(.+)se \^ ar(y|ies)$', r'\1sor\2'),

    # == t +cy ==
    # frequent + cy = frequency (tcy/tecy removal)
    (r'^(.*[naeiou])te? \^ cy$', r'\1cy'),

    # == +s ==
    # establish + s = establishes (sibilant pluralization)
    (r'^(.*(?:s|sh|x|z|zh)) \^ s$', r'\1es'),
    # speech + s = speeches (soft ch pluralization)
    (r'^(.*(?:oa|ea|i|ee|oo|au|ou|l|n|(?<![gin]a)r|t)ch) \^ s$', r'\1es'),
    # cherry + s = cherries (consonant + y pluralization)
    (r'^(.+[bcdfghjklmnpqrstvwxz])y \^ s$', r'\1ies'),

    # == y ==
    # die+ing = dying
    (r'^(.+)ie \^ ing$', r'\1ying'),
    # metallurgy + ist = metallurgist
    (r'^(.+[cdfghlmnpr])y \^ ist$', r'\1ist'),
    # beauty + ful = beautiful (y -> i)
    (r'^(.+[bcdfghjklmnpqrstvwxz])y \^ ([a-hj-xz].*)$', r'\1i\2'),

    # == +en ==
    # write + en = written
    (r'^(.+)te \^ en$', r'\1tten'),
    # Minessota +en = Minessotan (*Minessotaen)
    (r'^(.+[ae]) \^ e(n|ns)$', r'\1\2'),

    # == +ial ==
    # ceremony +ial = ceremonial (*ceremonyial)
    (r'^(.+)y \^ (ial|ially)$', r'\1\2'),
    # == +if ==
    # spaghetti +ification = spaghettification (*spaghettiification)
    (r'^(.+)i \^ if(y|ying|ied|ies|ication|ications)$', r'\1if\2'),

    # == +ical ==
    # fantastic +ical = fantastical (*fantasticcal)
    (r'^(.+)ic \^ (ical|ically)$', r'\1\2'),
    # epistomology +ical = epistomological
    (r'^(.+)ology \^ ic(al|ally)$', r'\1ologic\2'),
    # oratory +ical = oratorical (*oratoryical)
    (r'^(.*)ry \^ ica(l|lly|lity)$', r'\1rica\2'),

    # == +ist ==
    # radical +ist = radicalist (*radicallist)
    (r'^(.*[l]) \^ is(t|ts)$', r'\1is\2'),

    # == +ity ==
    # complementary +ity = complementarity (*complementaryity)
    (r'^(.*)ry \^ ity$', r'\1rity'),
    # disproportional +ity = disproportionality (*disproportionallity)
    (r'^(.*)l \^ ity$', r'\1lity'),

    # == +ive, +tive ==
    # perform +tive = performative (*performtive)
    (r'^(.+)rm \^ tiv(e|ity|ities)$', r'\1rmativ\2'),
    # restore +tive = restorative
    (r'^(.+)e \^ tiv(e|ity|ities)$', r'\1ativ\2'),

    # == +ize ==
    # token +ize = tokenize (*tokennize)
    # token +ise = tokenise (*tokennise)
    (r'^(.+)y \^ iz(e|es|ing|ed|er|ers|ation|ations|able|ability)$', r'\1iz\2'),
    (r'^(.+)y \^ is(e|es|ing|ed|er|ers|ation|ations|able|ability)$', r'\1is\2'),
    # conditional +ize = conditionalize (*conditionallize)
    (r'^(.+)al \^ iz(e|ed|es|ing|er|ers|ation|ations|m|ms|able|ability|abilities)$', r'\1aliz\2'),
    (r'^(.+)al \^ is(e|ed|es|ing|er|ers|ation|ations|m|ms|able|ability|abilities)$', r'\1alis\2'),
    # spectacular +ization = spectacularization (*spectacularrization)
    (r'^(.+)ar \^ iz(e|ed|es|ing|er|ers|ation|ations|m|ms)$', r'\1ariz\2'),
    (r'^(.+)ar \^ is(e|ed|es|ing|er|ers|ation|ations|m|ms)$', r'\1aris\2'),

    # category +ize/+ise = categorize/categorise (*categoryize/*categoryise)
    # custom +izable/+isable = customizable/customisable (*custommizable/*custommisable)
    # fantasy +ize = fantasize (*fantasyize)
    (r'^(.*[lmnty]) \^ iz(e|es|ing|ed|er|ers|ation|ations|m|ms|able|ability|abilities)$', r'\1iz\2'),
    (r'^(.*[lmnty]) \^ is(e|es|ing|ed|er|ers|ation|ations|m|ms|able|ability|abilities)$', r'\1is\2'),

    # == +olog ==
    # criminal + ology = criminology
    # criminal + ologist = criminalogist (*criminallologist)
    (r'^(.+)al \^ olog(y|ist|ists|ical|ically)$', r'\1olog\2'),

    # == +ish ==
    # similar +ish = similarish (*similarrish)
    (r'^(.+)(ar|er|or) \^ ish$', r'\1\2ish'),

    # free + ed = freed
    (r'^(.+e)e \^ (e.+)$', r'\1\2'),
    # narrate + ing = narrating (silent e)
    (r'^(.+[bcdfghjklmnpqrstuvwxz])e \^ ([aeiouy].*)$', r'\1\2'),

    # == misc ==
    # defer + ed = deferred (consonant doubling)   XXX monitor(stress not on last syllable)
    (r'^(.*(?:[bcdfghjklmnprstvwxyz]|qu)[aeiou])([bcdfgklmnprtvz]) \^ ([aeiouy].*)$', r'\1\2\2\3'),
]

ORTHOGRAPHY_RULES_ALIASES = {
    'able': 'ible',
    'ability': 'ibility',
}

ORTHOGRAPHY_WORDLIST = 'american_english_words.txt'


KEYMAPS = {
    'Gemini PR': {
        '#-'        : ('#1', '#2', '#3', '#4', '#5', '#6', '#7', '#8', '#9', '#A', '#B', '#C'),
        'a-'        : 'S1-',
        'o-'        : 'S2-',
        'n-'        : 'T-',
        'e-'        : 'K-',
        'i-'        : 'P-',
        'u-'        : 'W-',
        'g-'        : 'H-',
        'w-'        : 'R-',
        'd-'        : '*1',
        'z-'        : '*2',
        'b-'        : 'A-',
        'x-'        : 'O-',
        '-x'        : '-E',
        '-b'        : '-U',
        '-d'        : '*3',
        '-z'        : '*4',
        '-g'        : '-F',
        '-w'        : '-R',
        '-i'        : '-P',
        '-u'        : '-B',
        '-n'        : '-L',
        '-e'        : '-G',
        '-a'        : '-T',
        '-o'        : '-S',
        '-D'        : '-D',
        '-Z'        : '-Z',
        'no-op'     : ('pwr', 'res1', 'res2', 'Fn'),
    },
    'YaweiExtendedGeminiPR': {
        # '$-'        : 'Fn',
        '中-'        : '中-',
        '英-'        : '英-',
        '#-'        : ('#1', '#2', '#3', '#4', '#5', '#6', '#7', '#8', '#9', '#A', '#B', '#C'),
        'a-'        : 'a-',
        'o-'        : 'o-',
        'n-'        : 'n-',
        'e-'        : 'e-',
        'i-'        : 'i-',
        'u-'        : 'u-',
        'g-'        : 'g-',
        'w-'        : 'w-',
        'd-'        : 'd-',
        'z-'        : 'z-',
        'b-'        : 'b-',
        'x-'        : 'x-',
        '-x'        : '-x',
        '-b'        : '-b',
        '-d'        : '-d',
        '-z'        : '-z',
        '-g'        : '-g',
        '-w'        : '-w',
        '-i'        : '-i',
        '-u'        : '-u',
        '-n'        : '-n',
        '-e'        : '-e',
        '-a'        : '-a',
        '-o'        : '-o',
        'S-'        : ('S1-', 'S2-'),   
        'T-'        : 'T-',
        'K-'        : 'K-',
        'P-'        : 'P-',
        'W-'        : 'W-',
        'H-'        : 'H-',
        'R-'        : 'R-',
        'A-'        : 'A-',
        'O-'        : 'O-',
        '*'         : ('*1', '*2', '*3', '*4'),
        '-E'        : '-E',
        '-U'        : '-U',
        '-F'        : '-F',
        '-R'        : '-R',
        '-P'        : '-P',
        '-B'        : '-B',
        '-L'        : '-L',
        '-G'        : '-G',
        '-T'        : '-T',
        '-S'        : '-S',
        '-D'        : '-D',
        '-Z'        : '-Z',
        'no-op'     : ('pwr', 'res1', 'res2'),
    },
}

DICTIONARIES_ROOT = 'asset:plover_zh_yawei:plover_zh_yawei/dictionaries'
DEFAULT_DICTIONARIES = (
	'yawei_user.json',
	'yawei_chinese.json',
)

letter_to_num = {
    'a': 1,
    'n': 2,
    'i': 3,
    'g': 4,
    'd': 5,
    'x': 'X',
    'w': 'W'
}

right_conv = {
    'a': 0,
    'n': 9,
    'i': 8,
    'g': 7,
    'd': 6
}
def NS_STROKE_FORMATTER(stroke: str) -> str:
    """Formats single strokes, such as STROEBG"""
    out = stroke
    if stroke[0] == '#':
        if '-' in stroke:
            left, right = stroke[1:].split('-')    
            arr = [letter_to_num[x] for x in left]
            arr.reverse()
            arr.extend([right_conv[x] for x in right])
        else:
            arr = [letter_to_num[x] for x in stroke[1:]]
            arr.sort(key=lambda x: -2 if x == 'X' else -1 if x == 'W' else x)
        out = "".join([str(x) for x in arr])
    elif stroke == 'x':
        out = 'X'
    elif stroke == 'w':
        out = 'W'
    elif stroke == 'xw':
        out = 'XW'
    return out

def NS_SORTER(entry):
    """
    Scores outline-translation pairs, such as (("TRAPBS", "HRAEUT"), "translate")

    Pairs are ordered from smallest to biggest;
    it need not be an int - anything that can be compared
    works, including strings or tuples of ints.
    """
    outline, translation = entry
    print(outline, translation)
    if outline[0] == 'X':
        return (-3, 0, '')
    elif outline[0] == 'W':
        return (-2, 0, '')
    elif outline[0] == 'XW':
        return (-1, 0, '')
    elif not (set(outline[0]) - set(['1','2','3','4','5', '6', '7', '8', '9'])):
        return (0, int(outline[0]), '')
    elif outline[0][0] == 'X' and not (set(outline[0][1:]) - set(['1','2','3','4','5','6','7','8','9'])):
        return (1, int(outline[0][1:]), '')
    elif outline[0][0] == 'W' and not (set(outline[0][1:]) - set(['1','2','3','4','5','6','7','8','9'])):
        return (2, int(outline[0][1:]), '')
    elif outline[0][0:2] == 'XW' and not (set(outline[0][2:]) - set(['1','2','3','4','5','6','7','8','9'])):
        return (3, int(outline[0][2:]), '')
    return (4, len(outline), "/".join(outline))