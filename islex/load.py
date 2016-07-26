# -*- coding: utf-8 -*-

from __future__ import print_function

import bz2
import itertools
import os.path

from six import text_type as unicode
from collections import defaultdict

from islex.tokens import Word, PosCategory

ISLE_FILE = '/opt/data/ISLEdict.txt'

# TODO(jkahn): fetch these from namespace packages using official packagers
CORE_FILE = os.path.join(os.path.dirname(__file__), 'data', 'core.bz2')
ENTITIES_FILE = os.path.join(os.path.dirname(__file__), 'data', 'entities.bz2')
PERIPHERY_FILE = os.path.join(os.path.dirname(__file__), 'data',
                              'periphery.bz2')


def _open_package_files(mode='r'):
    core = bz2.BZ2File(CORE_FILE, mode=mode)
    entities = bz2.BZ2File(ENTITIES_FILE, mode=mode)
    periphery = bz2.BZ2File(PERIPHERY_FILE, mode=mode)
    return core, entities, periphery


def write_package_data():
    core, entities, periphery = _open_package_files(mode='w')

    def is_unambiguous_entity(w):
        ENTITY_CATEGORIES = (PosCategory.ABBREVIATION, PosCategory.NNP,
                             PosCategory.NNPS)
        return all(pos.category in ENTITY_CATEGORIES for pos in w.pos)

    for w in stream_from_fh(open(ISLE_FILE, mode='r'), clean=True):
        if not len(w.pos) and not len(w.morphs):
            out = periphery
        elif is_unambiguous_entity(w):
            out = entities
        else:
            # Some entities with other tags will end up in core.
            out = core
        out.write(w.to_string().encode('utf-8') + "\n")


def stream_entries(core=True, entities=True, periphery=True):
    core_f, entities_f, periphery_f = _open_package_files()
    files = []
    if core:
        files.append(core_f)
    if entities:
        files.append(entities_f)
    if periphery:
        files.append(periphery_f)

    return itertools.chain.from_iterable(stream_from_fh(fh) for fh in files)


def stream_from_fh(fh, clean=False):
    for l in fh:
        l = l.decode('utf-8')
        try:
            yield Word.from_string(unicode(l), clean=clean)
        except ValueError as v:
            print(unicode(v).encode('utf-8'))
            continue


def index_on_ortho(stream):
    """returns ortho: all Word objects with that ortho"""
    mmap = defaultdict(list)
    for w in stream:
        mmap[w.ortho].append(w)
    return mmap


def index_on_phones(stream):
    mmap = defaultdict(list)
    for w in stream:
        mmap[w.ipa].append(w)
    return mmap
