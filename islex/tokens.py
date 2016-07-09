# -*- coding: utf-8 -*-

from collections import namedtuple
import re


class Ortho(namedtuple('Ortho', ['ortho', 'pos'])):
    """Munges the orthographic & POS section"""
    def to_string(self):
        return self.ortho + "(" + self.pos + ")"
    patt = re.compile(r'^([^\(]+?)\((.*)\)\s*$')

    @classmethod
    def from_string(cls, s):
        match = cls.patt.match(s)
        if match:
            ortho, pos = match.groups()
            # might want to do more with the pos parsing, maybe ortho too.
            return cls(ortho=ortho, pos=pos)
        else:
            raise ValueError("Word %s doesn't seem to have ortho pattern" % s)


class Consonant(namedtuple('Consonant', ['phone'])):
    """Contains consonant features."""

    def to_string(self):
        return self.phone
    # TODO: support (e.g.) is_voiced(), etc.


class Vowel(namedtuple('Vowel', ['phone', 'stress'])):
    @classmethod
    def is_vowel(cls, s):
        if '=' in s:  # Syllabic l:  l= etc
            return True  # Syllable nucleus
        if '@' in s or '&' in s or '^' in s:
            return True
        # TODO: Needs more attention to handle other vowels (in
        # unstressed syllables).
        return

    def to_string(self):
        stress = None
        if self.stress == 'primary':
            stress = "'"
        elif self.stress == 'secondary':
            stress = ','
        elif self.stress == '0':
            stress = ''
        else:
            raise ValueError("vowel doesn't have right stress")
        return self.phone + stress
    # TODO: support (e.g.) is_front, is_back, etc.


class Phone(object):
    @classmethod
    def from_string(cls, s):
        if s.endswith("'"):
            return Vowel(s[:-1], stress='primary')
        elif s.endswith(","):
            return Vowel(s[:-1], stress='secondary')
        elif Vowel.is_vowel(s):
            return Vowel(s, stress='0')
        else:
            return Consonant(s)


class Syll(namedtuple('Syll', ['phones'])):
    """Model of syllable"""
    @classmethod
    def from_string(cls, s):
        return cls(phones=[Phone.from_string(p.strip()) for p in s.split()])

    def to_string(self):
        return " ".join([p.to_string() for p in self.phones])
    # TODO: support (e.g.) onset, nucleus, coda, rhyme methods.


class Phon(namedtuple('Phon', ['sylls'])):
    """Phonetic representation of entire word."""
    @classmethod
    def from_string(cls, s):
        return cls(sylls=[Syll.from_string(sy) for sy in s.split('.')])

    def to_string(self):
        return ' . '.join([s.to_string() for s in self.sylls])


class Word(namedtuple('Word', ['ortho', 'phons'])):
    @classmethod
    def from_line(cls, l):
        l = l.rstrip()
        _prons = str.split(l, '#')
        ortho = _prons.pop(0)
        while not _prons[-1]:
            _prons.pop(-1)
        return cls(ortho=Ortho.from_string(ortho),
                   phons=[Phon.from_string(p) for p in _prons])

    def to_string(self):
        return " # ".join([self.ortho.to_string()]
                          + [p.to_string() for p in self.phons])

    def to_phones(self, by_syllables=False):
        out = []
        for phon in self.phons:
            for syll in phon.sylls:
                syll_phones = []
                for phone in syll.phones:
                    syll_phones.append(phone.phone)
                if by_syllables:
                    out.append(syll_phones)
                else:
                    out.extend(syll_phones)
        return tuple(out)
