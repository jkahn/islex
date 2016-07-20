# -*- coding: utf-8 -*-

import codecs
from collections import defaultdict

from islex.tokens import Word

ISLE_FILE = '/opt/data/ISLEdict.txt'


def generate_words(clean=False):
    for l in codecs.open(ISLE_FILE, 'r', encoding='utf-8'):
        try:
            yield Word.from_string(l, clean=clean)
        except ValueError as v:
            print v.encode('utf-8')
            continue


def index_on_ortho(clean=False):
    """returns ortho: all Word objects with that ortho"""
    mmap = defaultdict(list)
    for w in generate_words(clean=clean):
        mmap[w.ortho].append(w)
    return mmap


def index_on_phones(clean=False):
    mmap = defaultdict(list)
    for w in generate_words(clean=clean):
        mmap[w.ipa].append(w)
    return mmap
