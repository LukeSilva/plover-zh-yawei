# SKPMTF*RNLYOEAUIln$DC

KEYS = (
    '#-',
'x-', 'b-', 'd-', 'z-', 'g-', 'w-', 'i-', 'u-', 'n-', 'e-', 'a-', 'o-',
'-x', '-b', '-d', '-z', '-g', '-w', '-i', '-u', '-n', '-e', '-a', '-o'
)
IMPLICIT_HYPHEN_KEYS = ()

SUFFIX_KEYS = ()

NUMBER_KEY = None

NUMBERS = {}

UNDO_STROKE_STENO = 'W-W'

ORTHOGRAPHY_RULES = []

ORTHOGRAPHY_RULES_ALIASES = {}

ORTHOGRAPHY_WORDLIST = None

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
        'no-op'     : ('Fn', 'pwr', 'res1', 'res2', '-D', '-Z'),
    },
}

DICTIONARIES_ROOT = 'asset:plover_zh_yawei:plover_zh_yawei:dictionaries'
DEFAULT_DICTIONARIES = (
	'yawei_user.json',
	'yawei_chinese.json',
)
