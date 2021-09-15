# SKPMTF*RNLYOEAUIln$DC

KEYS = (

'X-', 'B-', 'D-', 'Z-', 'G-', 'W-', 'I-', 'U-', 'N-', 'E-', 'A-', 'O-',
'-X', '-B', '-D', '-Z', '-G', '-W', '-I', '-U', '-N', '-E', '-A', '-O'
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
        'A-'        : 'S1-',
        'O-'        : 'S2-',
        'N-'        : 'T-',
        'E-'        : 'K-',
        'I-'        : 'P-',
        'U-'        : 'W-',
        'G-'        : 'H-',
        'W-'        : 'R-',
        'D-'        : '*1',
        'Z-'        : '*2',
        'B-'        : 'A-',
        'X-'        : 'O-',
        '-X'        : '-E',
        '-B'        : '-U',
        '-D'        : '*3',
        '-Z'        : '*4',
        '-G'        : '-F',
        '-W'        : '-R',
        '-I'        : '-P',
        '-U'        : '-B',
        '-N'        : '-L',
        '-E'        : '-G',
        '-A'        : '-T',
        '-O'        : '-S',
        'no-op'     : ('Fn', 'pwr', 'res1', 'res2', '#1', '#2', '#3', '#4', '#5', '#6', '#7', '#8', '#9', '#A', '#B', '#C', '-D', '-Z'),
    },
}

DICTIONARIES_ROOT = 'asset:plover_zh_yawei:plover_zh_yawei:dictionaries'
DEFAULT_DICTIONARIES = (
	'yawei_user.json',
	'yawei_chinese.json',
)
