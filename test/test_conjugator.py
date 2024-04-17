# tests complete verb conjugations : from conjutils to vutils
import pytest
import conjugator_utils as conjutils

# read from files
irregular_verbs = conjutils.get_irregular_verbs()
concrete_verbs = conjutils.get_concrete_verbs()
prefixes = conjutils.get_prefixes()

# tests unamibguous irregular verb conjugations
def test_irregular_conjugation_no_disambiguate():
    assert True == True

# test ambiguous irregular verb conjugations
def test_irregular_conjugation_yes_disambiguate():
    assert True == True

# tests stát conjugation(s)
def test_stat_conjugation():
    assert True == True

# tests concrete verb conjugations
def test_concrete_conjugation():
    assert True == True

# tests regular verb conjugations, 1 from each class.
def test_regular_conjugation():
    assert True == True


# TODO:
# # tests perfective conjugations
# def test_perfective_conjugation():
#     assert True == True