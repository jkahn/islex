#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_load_strings
----------------------------------

Tests for `islex.tokens` module.
"""

from six import text_type as unicode
import pytest

from islex.tokens import Word, Pos, Pron, Syllable, Phone, \
    PosCategory, EntityCategory


class TestIsleWord(object):

    test_str = (u"007(+abbreviation,nnp_person) # "
                + u"d ˌʌ . b ə l . ˌoʊ . s ˌɛ̃ . v ˌɪ n #")
    syllables = (Syllable.from_string(u'd ˌʌ'),
                 Syllable.from_string(u'b ə l'),
                 Syllable.from_string(u'ˌoʊ'),
                 Syllable.from_string(u's ˌɛ'),
                 Syllable.from_string(u'v ˌɪ n'))

    phones = tuple(u"d ˌʌ b ə l ˌoʊ s ˌɛ v ˌɪ n".split())
    
    @classmethod
    def setup_class(cls):
        pass

    def test_word(self):
        word = Word.from_string(self.test_str, clean=True)
        assert unicode(word.ortho) == u"007"
        assert len(word.prons) == 1
        assert word.prons[0] == Pron(sylls=self.syllables)

    def test_empty_pos_tags(self):
        s = u"foo() # f  ˈu #"
        w = Word.from_string(s)
        assert len(w.prons) == 1
        assert len(w.pos) == 0

    def test_morph_scheme(self):
        s = u"fooed(+foo+ed,vbd) # f  ˈu d #"
        w = Word.from_string(s)
        assert len(w.prons) == 1
        assert len(w.pos) == 1
        assert w.pos[0] == Pos(category=PosCategory.VBD)
        assert len(w.morphs) == 2
        assert w.morphs == ("foo", "ed")
        
    def test_pos_tags(self):
        word = Word.from_string(self.test_str, clean=True)
        assert len(word.pos) == 2
        assert word.pos[0].category is PosCategory.ABBREVIATION
        assert word.pos[0].entity_type is None
        assert word.pos[1].category is PosCategory.NNP
        assert word.pos[1].entity_type is EntityCategory.PERSON

    def test_syllable(self):
        assert Syllable.from_string(u'v ˌɪ n') == Syllable(
            phones=(Phone(u'v'), Phone(u'ˌɪ'), Phone(u'n')))
        
    def test_ipa(self):
        word = Word.from_string(self.test_str, clean=True)
        assert word.ipa == self.phones
        
    @pytest.mark.skip("No syllable functionality yet")
    def test_stress(self):
        vin = Syllable.from_string(u'v ˌɪ n')
        assert vin.onset == [Phone(u'v'),]
        assert vin.coda == [Phone(u'ˌɪ'), Phone(u'n')]
        assert vin.is_stressed
        assert not vin.is_primary_stressed
        assert vin.nucleus == [Phone(u'ˌɪ')]

    @classmethod
    def teardown_class(cls):
        pass
