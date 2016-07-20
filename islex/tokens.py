# -*- coding: utf-8 -*-

import attr
from attr.validators import optional, instance_of
import re
from six import text_type as unicode
import enum
import itertools


@enum.unique
class PosCategory(enum.Enum):
    """Enumeration of possible POS tags."""
    UNUSED_POSTAG = 0

    # Adverbs, and comparative/superlative forms.
    RB = 1
    RBR = 2
    RBS = 3

    # (Common) nouns.
    NN = 4
    NNS = 5

    # Adjectives in various forms (incl comparative & superlative).
    JJ = 6
    JJR = 7
    JJS = 8

    # Verbs in various conjugations.
    VB = 9
    VBD = 10
    VBG = 11
    VBP = 12
    VBN = 13
    VBZ = 14

    # Proper nouns.
    NNP = 15
    NNPS = 16

    # Discourse markers.
    LS = 20
    FW = 21
    UH = 22

    # Various closed-class items.
    DT = 50  # Determiners.
    EX = 51  # Existential there.
    CD = 52  # Count determiner?
    MD = 53
    IN = 54
    TO = 55
    OF = 56
    PRP = 57
    CC = 58
    PDT = 59
    WRB = 60
    WDT = 61
    WP = 62
    RP = 63

    # Symbol?
    ABBREVIATION = 80
    SYM = 81
    PUNC = 82


@enum.unique
class EntityCategory(enum.Enum):
    UNSPECIFIED_ENTITY = 0
    PRODUCT = 1
    CITY = 2
    SURNAME = 3
    EVENT = 4
    COUNTRY = 5
    CONTINENT = 6
    PERSON = 7
    ORGANIZATION = 8
    COMPANY = 9
    PLACE = 10
    STATE = 11
    MONTH = 12
    BOYNAME = 13
    GIRLNAME = 14


_scored_patt = re.compile(r'_\d\.\d+$')


def _clean_tag(t):
    """Fix up some garbage errors."""
    # TODO: when score present, include info.
    t = _scored_patt.sub(string=t, repl='')
    if t == '_country_' or t.startswith('_country:'):
        t = 'nnp_country'
    elif t == 'vpb':
        t = 'vb'  # "carjack" is listed with vpb tag.
    elif t == 'nnd':
        t = 'nns'  # "abbes" is listed with nnd tag.
    elif t == 'nns_root:':
        t = 'nns'  # 'micros' is listed as nns_root.
    elif t == 'root:zygote':
        t = 'nn'  # 'root:zygote' for zygote. :-/
    elif t.startswith('root:'):
        t = 'uh'  # Don't know why, but these are all UH tokens.
    elif t in ('abbr_united_states_marine_corps', 'abbr_orange_juice'):
        t = "abbreviation"
    elif t == '+abbreviation':
        t = 'abbreviation'
    elif t.startswith('fw_misspelling:'):
        t = 'fw'
    return t


@attr.s
class Pos(object):
    category = attr.ib(validator=instance_of(PosCategory))
    entity_type = attr.ib(default=None,
                          validator=optional(instance_of(EntityCategory)))

    @classmethod
    def from_string(cls, t):
        # Extract some systematic structure from the data.
        postag = t
        entity = None
        if t.startswith('nnp_'):
            postag = PosCategory.NNP
            entity = EntityCategory[t[4:].upper()]
        elif t.startswith('nnps_'):
            postag = PosCategory.NNPS
            entity = EntityCategory[t[5:].upper()]
        else:
            postag = PosCategory[t.upper()]
            entity = None
        return cls(category=postag, entity_type=entity)


@attr.s
class Phone(object):
    value = attr.ib(instance_of(unicode))


@attr.s
class Syllable(object):
    phones = attr.ib(instance_of(tuple))  # of strings? of Phones?

    @classmethod
    def from_string(cls, s):
        return cls(phones=tuple(Phone(value=p) for p in s.split()))

    @property
    def ipa(self):
        return tuple(ph.value for ph in self.phones)


@attr.s
class Pron(object):
    sylls = attr.ib(validator=instance_of(tuple))

    @classmethod
    def from_string(cls, s, clean=False):
        s = s.strip()
        raw_sylls = s.split(u' . ')
        if clean:
            raw_sylls = [p.replace(u"ɛ̃", u"ɛ") for p in raw_sylls]
        # TODO: break into phones?
        return cls(sylls=tuple(Syllable.from_string(p) for p in raw_sylls))

    @property
    def ipa(self):
        return tuple(itertools.chain.from_iterable(syll.ipa
                                                   for syll in self.sylls))


@attr.s
class Word(object):
    ortho = attr.ib()
    pos = attr.ib(validator=instance_of(tuple))  # of Pos
    morphs = attr.ib(validator=instance_of(tuple))  # of strings
    # TODO: validate that each element is instance of...
    prons = attr.ib(validator=instance_of(tuple))  # of Prons

    ortho_patt = re.compile(r'^([^\(]+?)\((.*)\)\s*$')

    @classmethod
    def from_string(cls, s, clean=False):
        s = s.strip()
        raw_prons = s.split(u'#')
        while not raw_prons[-1]:
            raw_prons.pop(-1)
        if len(raw_prons) < 2:
            raise ValueError("string doesn't have enough segments: %s" % s)
        raw_ortho = raw_prons.pop(0)
        m = cls.ortho_patt.match(raw_ortho)
        if not m:
            raise ValueError("ortho doesn't match expected" % raw_ortho)
        ortho, raw_pos = m.groups()
        all_morphs = []
        all_pos = []
        for t in raw_pos.split(','):
            if clean:
                t = _clean_tag(t)
            if not t:
                continue
            if t.startswith('+'):
                assert not all_morphs
                all_morphs = t[1:].split('+')
            else:
                try:
                    all_pos.append(Pos.from_string(t))
                except KeyError as k:
                    raise ValueError("pos tag %s not found" % k)

        all_prons = [Pron.from_string(raw_pron, clean=clean)
                     for raw_pron in raw_prons]

        return cls(ortho=ortho, morphs=tuple(all_morphs), pos=tuple(all_pos),
                   prons=tuple(all_prons))

    @property
    def ipa(self):
        return tuple(itertools.chain.from_iterable(
            pron.ipa for pron in self.prons))
