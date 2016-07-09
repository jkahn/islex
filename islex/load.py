# -*- coding: utf-8 -*-

from collections import defaultdict

from islex.tokens import Word

ISLE_FILE = '/opt/data/islev2.txt'


def generate_words():
    for l in open(ISLE_FILE, 'r'):
        yield Word.from_line(l)


def index_on_ortho():
    """returns ortho: all Word objects with that ortho"""
    mmap = defaultdict(list)
    for w in generate_words():
        mmap[w.ortho.ortho].append(w)
    return mmap


def index_on_phones():
    mmap = defaultdict(list)
    for w in generate_words():
        mmap[w.to_phones()].append(w)
    return mmap
