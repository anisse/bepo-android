#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Produit une carte de touches android à partir d'un fichier xkb
#
# Copyright (C) 2008 Gaëtan Lehmann <gaetan.lehmann@jouy.inra.fr>
# Copyright (C) 2014 Anisse Astier <anisse@astier.eu>
#
# Utilisable uniquement au sein du configGenerator bépo;
# premier argument: le fichier xkb source
# second argument: le fichier de sortie kcm
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#

import defaults, sys
defaults.xkbFile = sys.argv[1]

import xkb, dead_keys, codecs
from terminators import terminators


keyTemplate = """key %(QWERTYNAME)s {
    label:              '%(UPPERNAME)s'
    base:               '%(LOWERNAME)s'
    shift, capslock:    '%(UPPERNAME)s'
    shift+capslock:     '%(LOWER2NAME)s'
    ralt:               '%(ALTGRNAME)s'
    shift+ralt:         '%(SHALTGRNAME)s'
}
"""

xkbToQwerty = {
        'TLDE': 'GRAVE',
        'AE01': '1',
        'AE02': '2',
        'AE03': '3',
        'AE04': '4',
        'AE05': '5',
        'AE06': '6',
        'AE07': '7',
        'AE08': '8',
        'AE09': '9',
        'AE10': '0',
        'AE11': 'MINUS',
        'AE12': 'EQUALS',

        'AD01': 'Q',
        'AD02': 'W',
        'AD03': 'E',
        'AD04': 'R',
        'AD05': 'T',
        'AD06': 'Y',
        'AD07': 'U',
        'AD08': 'I',
        'AD09': 'O',
        'AD10': 'P',
        'AD11': 'LEFT_BRACKET',
        'AD12': 'RIGHT_BRACKET',

        'AC01': 'A',
        'AC02': 'S',
        'AC03': 'D',
        'AC04': 'F',
        'AC05': 'G',
        'AC06': 'H',
        'AC07': 'J',
        'AC08': 'K',
        'AC09': 'L',
        'AC10': 'SEMICOLON',
        'AC11': 'APOSTROPHE',

        'BKSL': 'BACKSLASH',
        'LSGT': 'PLUS',

        'AB01': 'Z',
        'AB02': 'X',
        'AB03': 'C',
        'AB04': 'V',
        'AB05': 'B',
        'AB06': 'N',
        'AB07': 'M',
        'AB08': 'COMMA',
        'AB09': 'PERIOD',
        'AB10': 'SLASH',

        'SPCE': 'SPACE',
    }

# Arbitrary names that are in the keyTemplate
modifiersMap =  {
        'shift': 'UPPER',
        'option': 'ALTGR',
        '': 'LOWER',
        'shift_capslock': 'LOWER2',
        'shift_option': 'SHALTGR',
    }

ascii_set = set([
'^', '~', '<', '=', '>', '|', '_', '-', ',', ';', '!', '?', '/', '.', '"', '(',
')', '[', ']', '{', '}', '@', '$', '*', '&', '#', '%', '+', '0', '1', '2', '3',
'4', '5', '6', '7', '8', '9', 'a', 'A', 'b', 'B', 'c', 'C', 'd', 'D', 'e', 'E',
'f', 'F', 'g', 'G', 'h', 'H', 'i', 'I', 'j', 'J', 'k', 'K', 'l', 'L', 'm', 'M',
'n', 'N', 'o', 'O', 'p', 'P', 'q', 'Q', 'r', 'R', 's', 'S', 't', 'T', 'u', 'U',
'v', 'V', 'w', 'W', 'x', 'X', 'y', 'Y', 'z', 'Z'
])

androidkeys = {}
for k in xkbToQwerty.itervalues():
    androidkeys[k] = {}

for k, v in xkb.tmplValues.iteritems():
    v = terminators.get( v, v )
    if v == "":
        v = " "
    key = k.split('_', 1)
    if len(key) == 0:
        continue
    xkbName = key[0]
    if len(key) > 1:
        modifiers = key[1]
    else:
        modifiers = ""

    #print("Key: %s, modifier: %s, value: %s"%(xkbName,modifiers,v))
    for km, vm in modifiersMap.iteritems():
        if modifiers == km:
            #print("%s %s: %s"%(xkbToQwerty[xkbName], modifiersMap[modifiers], v))


            if v in ascii_set:
                androidkeys[xkbToQwerty[xkbName]][vm + 'NAME'] = v
            else:
                # Unicode all the things
                value = hex(ord(v))[2:].upper()
                value = "0000"[0:4-len(value)] + value

                #Prepare the map for what we'll print later
                androidkeys[xkbToQwerty[xkbName]][vm + 'NAME'] = '\u' + value

# special case for android dead keys
androidkeys[xkbToQwerty['AD05']]['ALTGRNAME'] = '\\u0300' #dead_grave
androidkeys[xkbToQwerty['AD02']]['ALTGRNAME'] = '\\u0301' #dead_acute
androidkeys[xkbToQwerty['AD06']]['LOWERNAME'] = '\\u0302' #dead_circumflex
androidkeys[xkbToQwerty['AC10']]['ALTGRNAME'] = '\\u0303' #dead_tilde
androidkeys[xkbToQwerty['AC03']]['ALTGRNAME'] = '\\u0308' #dead_diaeresis

out = codecs.open(sys.argv[2], "w", "utf8")
out.write(u"""# File generated automatically
# It's under MIT license - don't hesitate to contact me
# Copyright (c) 2014 Anisse Astier <anisse@astier.eu> and PushVision

type OVERLAY

# 102ND key we want to use, not as a BACKSLASH
map key 86 PLUS

""")
for k, v in iter(sorted(androidkeys.iteritems())):
    v['QWERTYNAME'] = k
    out.write( keyTemplate % v)
