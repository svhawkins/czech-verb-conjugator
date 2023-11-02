# tests conjugation utilities (mainly verb class determination)

import pytest
import src.conjugator_utils as conjutils


# placeholder test
def test_success():
    assert 493 == 493


# tests that get_irregular_verbs functions properly by examining contents of the 1st, 10th, 30th, and 75th lines. 
def test_get_irregular_verbs():
    # infinitive, class, stem, past stem, imperative stem, passive stem?, transgressive stem?
    irregular_verbs = conjutils.get_irregular_verbs()

    # items
    #  0: zvát		4		zv		zval		zvi
    # 10: brát		4		ber		bral		ber
    # 30: spát		3		sp		spal		spi
    # 75: ržát		4		rž		ržal		rži

    indices = [0, 9, 29, 74]
    expected  = [("zvát", 4, "zv", "zval", "zvi"),
                ("brát", 4, "ber", "bral", "ber"),
                ("spát", 3, "sp", "spal", "spi"),
                ("ržát", 4, "rž", "ržal", "rži")]
    for idx in range(len(indices)):
        for irregularIdx in range(len(conjutils.IrregularIdx)):
            assert expected[idx][irregularIdx] == irregular_verbs[indices[idx]][irregularIdx]

# tests that the verb class mapping works
def test_verb_class():

    for class_int in range(1, 5):
        assert class_int == conjutils.verb_class("", class_int).class_num

# tests that the regex search works for find irregular verb
def test_find_verb_matches():
    irregular_verbs = conjutils.get_irregular_verbs()

    # stát		4		stan		stal		staň
    # stát		3		stoj		stál		stůj
    expected = [("stát", 4, "stan", "stal", "staň"), ("stát", 3 , "stoj", "stál", "stůj")]
    matches = []
    matches = conjutils.find_verb_matches("stát", irregular_verbs)
    for verb_idx in range(len(expected)):
        for irregular_idx in range(len(conjutils.IrregularIdx)):
            assert expected[verb_idx][irregular_idx] == matches[verb_idx][irregular_idx]

    # vědět		3		v		věděl		věz
    expected = [("vědět", 3, "v", "věděl", "věz")]
    matches = []
    matches = conjutils.find_verb_matches("vědět", irregular_verbs)
    for verb_idx in range(len(expected)):
        for irregular_idx in range(len(conjutils.IrregularIdx)):
            assert expected[verb_idx][irregular_idx] == matches[verb_idx][irregular_idx]

# tests construct verb
def test_construct_verb():
    # vědět		3		v		věděl		věz
    irregular_verbs = conjutils.get_irregular_verbs()
    matches = conjutils.find_verb_matches("vědět", irregular_verbs)
    verb = conjutils.construct_verb("vědět", matches[0])
    assert verb.class_num == 3
    assert verb.present_stem == "v"
    assert verb.past_stem == "věděl"
    assert verb.imperative_stem == "věz"