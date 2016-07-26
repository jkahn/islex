# -*- coding: utf-8 -*-

from __future__ import print_function

import os.path

from six import text_type as unicode

from islex.tokens import Word, PosCategory

ISLE_FILE = '/opt/data/ISLEdict.txt'

# TODO(jkahn): this is obviously only going to work for me.
CHECKOUT_ROOT = '/home/jeremy/src'


def _open_data_package_target(stem):
    islex_path = 'islex-%s' % stem
    package_dir = os.path.join(CHECKOUT_ROOT, islex_path, islex_path)
    if not os.path.exists(package_dir):
        os.makedirs(package_dir)
    f = os.path.join(package_dir, 'entries.txt')
    return open(f, mode='w')


def write_package_data():
    core = _open_data_package_target('core')
    entities = _open_data_package_target('entities')
    periphery = _open_data_package_target('periphery')

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


def stream_from_fh(fh, clean=False):
    for l in fh:
        l = l.decode('utf-8')
        try:
            yield Word.from_string(unicode(l), clean=clean)
        except ValueError as v:
            print(unicode(v).encode('utf-8'))
            continue
