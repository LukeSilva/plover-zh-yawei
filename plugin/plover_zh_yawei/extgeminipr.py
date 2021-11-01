# Copyright (c) 2010-2011 Joshua Harlan Lifton.
# See LICENSE.txt for details.

"""Thread-based monitoring of a Gemini PR stenotype machine."""

import binascii

from plover import log
from plover.machine.base import SerialStenotypeBase


# In the Gemini PR protocol, each packet consists of exactly six bytes
# and the most significant bit (MSB) of every byte is used exclusively
# to indicate whether that byte is the first byte of the packet
# (MSB=1) or one of the remaining five bytes of the packet (MSB=0). As
# such, there are really only seven bits of steno data in each packet
# byte. This is why the STENO_KEY_CHART below is visually presented as
# six rows of seven elements instead of six rows of eight elements.
STENO_KEY_CHART = ("Fn", "#1", "#2", "#3", "#4", "#5", "#6",
                   "S1-", "S2-", "T-", "K-", "P-", "W-", "H-",
                   "R-", "A-", "O-", "*1", "*2", "res1", "res2",
                   "pwr", "*3", "*4", "-E", "-U", "-F", "-R",
                   "-P", "-B", "-L", "-G", "-T", "-S", "-D",
                   "#7", "#8", "#9", "#A", "#B", "#C", "-Z")

BYTES_PER_STROKE = 6

CHINESE_CONVERSION = {
    'S1-': 'a-',
    'S2-': 'o-',
    'T-':  'n-',
    'K-':  'e-',
    'P-':  'i-',
    'W-':  'u-',
    'H-':  'g-',
    'R-':  'w-',
    '*1':  'd-',
    '*2':  'z-',
    'A-':  'b-',
    'O-':  'x-',
    '-E':  '-x',
    '-U':  '-b',
    '*3':  '-d',
    '*4':  '-z',
    '-F':  '-g',
    '-R':  '-w',
    '-P':  '-i',
    '-B':  '-u',
    '-L':  '-n',
    '-G':  '-e',
    '-T':  '-a',
    '-S':  '-o'
}

NUMBER_KEYS = set(['#1', '#2', '#3', '#4', '#5', '#6', '#7', '#8', '#9', '#A', '#B', '#C'])

class YaweiExtGeminiPr(SerialStenotypeBase):
    """Standard stenotype interface for a Gemini PR machine.
    """

    KEYS_LAYOUT = '''
        #1 #2  #3 #4 #5 #6 #7 #8 #9 #A #B #C
           a-  n- i- g- d- -d -g -i -n -a
        Fn S1- T- P- H- *1 *3 -F -P -L -T -D
           S2- K- W- R- *2 *4 -R -B -G -S -Z
           o-  e- u- w- z- -z -w -u -e -o
                  A- O-       -E -U
                  b- x-       -x -b
        pwr
        res1
        res2
        中- 英-
    '''

    def run(self):
        """Overrides base class run method. Do not call directly."""
        ChineseMode = False # Start in English mode because of default spacing
        LastMode = False
        HasFnKey = False # Not all amateur machines have a usable fn key, detect on first use

        def send_mode_key(Mode):
            nonlocal LastMode
            steno_keys = ['中-'] if Mode else ['英-']
            steno_keys = self.keymap.keys_to_actions(steno_keys)
            if steno_keys:
                self._notify(steno_keys)
            LastMode = Mode
            #print('sending mode', Mode)

        self._ready()
        print("Running yawei geminipr")
        for packet in self._iter_packets(BYTES_PER_STROKE):
            if not (packet[0] & 0x80) or sum(b & 0x80 for b in packet[1:]):
                log.error('discarding invalid packet: %s',
                binascii.hexlify(packet))
                continue
            steno_keys = []
            for i, b in enumerate(packet):
                for j in range(1, 8):
                    if (b & (0x80 >> j)):
                        steno_keys.append(STENO_KEY_CHART[i * 7 + j - 1])

            #print('Received stroke, mode = {} last_mode = {}'.format(ChineseMode, LastMode))
            # print('raw ', steno_keys)
            if 'Fn' in steno_keys:
                HasFnKey = True # Disable the number bar switching

            if steno_keys == ['Fn']:
                ChineseMode = not ChineseMode
                send_mode_key(ChineseMode)
            elif not HasFnKey and len(steno_keys) == 1 and steno_keys[0] in NUMBER_KEYS:
                ChineseMode = not ChineseMode
                send_mode_key(ChineseMode)
            elif steno_keys == ['res1']:
                ChineseMode = True
                send_mode_key(ChineseMode)
            elif steno_keys == ['res2']:
                ChineseMode = False
                send_mode_key(ChineseMode)
            else: 
                IsThisStrokeChinese = ChineseMode
                if 'Fn' in steno_keys:
                    IsThisStrokeChinese = not IsThisStrokeChinese
                    steno_keys.remove('Fn')
                # elif not HasFnKey and len(NUMBER_KEYS & set(steno_keys)) == 1:
                #     IsThisStrokeChinese = not IsThisStrokeChinese
                #     steno_keys = [x for x in steno_keys if x not in NUMBER_KEYS]
            
                if IsThisStrokeChinese:
                    for i in range(len(steno_keys)):
                        if steno_keys[i] in CHINESE_CONVERSION:
                            steno_keys[i] = CHINESE_CONVERSION[steno_keys[i]]

                if IsThisStrokeChinese != LastMode:
                    send_mode_key(IsThisStrokeChinese)
                    
                # print('post', steno_keys)
                steno_keys = self.keymap.keys_to_actions(steno_keys)
                if steno_keys:
                    self._notify(steno_keys)
