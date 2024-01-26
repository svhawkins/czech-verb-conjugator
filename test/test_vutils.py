# tests verb utilities

import pytest
import verb_utils as vutils

# tests italics() with the empty string 
def test_italics():
    test_str=""
    assert vutils.italics(test_str) == "\x1B[3m\x1B[23m"

# tests short->long vowel mappings
# short vowels should now become long
# all other letters and digraphs must be unaffected.
def test_get_short_vowel():
    alphabet = ["a", "á", "b", "c", "č", "d", "ď", "e", "ě", "é", "f", "g", "h", "ch",
             "i", "í", "j", "k", "l", "m", "n", "ň", "o", "ó", "p", "q", "r", "ř",
             "s", "š", "t", "ť", "u", "ú", "ů", "ou", "v", "w", "x", "y", "ý", "z", "ž"]
    expected = ["a", "a", "b", "c", "č", "d", "ď", "e", "ě", "e", "f", "g", "h", "ch",
             "i", "i", "j", "k", "l", "m", "n", "ň", "o", "ó", "p", "q", "r", "ř",
             "s", "š", "t", "ť", "u", "u", "o", "u", "v", "w", "x", "y", "y", "z", "ž"]
    
    for i in range(len(alphabet)):
        assert vutils.get_short_vowel(alphabet[i]) == expected[i]

# tests long->short vowel mappings
# long vowels should now become short
# all other letters and digraphs must be unaffected.
def test_get_long_vowel():
    alphabet = ["a", "á", "b", "c", "č", "d", "ď", "e", "ě", "é", "f", "g", "h", "ch",
             "i", "í", "j", "k", "l", "m", "n", "ň", "o", "ó", "p", "q", "r", "ř",
             "s", "š", "t", "ť", "u", "ú", "ů", "ou", "v", "w", "x", "y", "ý", "z", "ž"]
    expected = ["á", "á", "b", "c", "č", "d", "ď", "é", "ě", "é", "f", "g", "h", "ch",
             "í", "í", "j", "k", "l", "m", "n", "ň", "ů", "ó", "p", "q", "r", "ř",
             "s", "š", "t", "ť", "ou", "ú", "ů", "ou", "v", "w", "x", "ý", "ý", "z", "ž"]
    
    for i in range(len(alphabet)):
        assert vutils.get_long_vowel(alphabet[i]) == expected[i]

# tests hard->soft consonant mappings
# hard consonants should now become soft
# all other letters and digraphs must be unaffected.
def test_get_soft_consonant():
    alphabet = ["a", "á", "b", "c", "č", "d", "ď", "e", "ě", "é", "f", "g", "h", "ch",
             "i", "í", "j", "k", "l", "m", "n", "ň", "o", "ó", "p", "q", "r", "ř",
             "s", "š", "t", "ť", "u", "ú", "ů", "ou", "v", "w", "x", "y", "ý", "z", "ž"]
    expected = ["a", "á", "b", "c", "č", "ď", "ď", "e", "ě", "é", "f", "z", "z", "š",
             "i", "í", "j", "c", "l", "m", "ň", "ň", "o", "ó", "p", "q", "ř", "ř",
             "s", "š", "ť", "ť", "u", "ú", "ů", "ou", "v", "w", "x", "y", "ý", "z", "ž"]
    
    for i in range(len(alphabet)):
        assert vutils.get_soft_consonant(alphabet[i]) == expected[i]

# tests soft->hard consonant mappings
# soft consonants should now become hard
# all other letters and digraphs must be unaffected.
# CAVEAT: there is no mapping from z->g, only z->h due to ambiguity.
def test_get_hard_consonant():
    alphabet = ["a", "á", "b", "c", "č", "d", "ď", "e", "ě", "é", "f", "g", "h", "ch",
             "i", "í", "j", "k", "l", "m", "n", "ň", "o", "ó", "p", "q", "r", "ř",
             "s", "š", "t", "ť", "u", "ú", "ů", "ou", "v", "w", "x", "y", "ý", "z", "ž"]
    expected = ["a", "á", "b", "k", "č", "d", "d", "e", "ě", "é", "f", "g", "h", "ch",
             "i", "í", "j", "k", "l", "m", "n", "n", "o", "ó", "p", "q", "r", "r",
             "s", "ch", "t", "t", "u", "ú", "ů", "ou", "v", "w", "x", "y", "ý", "h", "ž"]
    
    for i in range(len(alphabet)):
        assert vutils.get_hard_consonant(alphabet[i]) == expected[i]

# tests isvowel() function
# vowels and vowel digraphs (if applicable) should return true
# consonants and consonant digraphs should return false
def test_is_vowel():
    alphabet = ["a", "á", "b", "c", "č", "d", "ď", "e", "ě", "é", "f", "g", "h", "ch",
             "i", "í", "j", "k", "l", "m", "n", "ň", "o", "ó", "p", "q", "r", "ř",
             "s", "š", "t", "ť", "u", "ú", "ů", "ou", "v", "w", "x", "y", "ý", "z", "ž"]
    expected = [True, True, False, False, False, False, False, True, True, True, False, False, False, False,
                True, True, False, False, False, False, False, False, True, True, False, False, False, False,
                False, False, False, False, True, True, True, True, False, False, False, True, True, False, False]
    for i in range(len(alphabet)):
        assert vutils.isvowel(alphabet[i]) == expected[i]

# tests isconsonant() function
# vowels and vowel digraphs (if applicable) should return false
# consonants and consonant digraphs should return true
def test_is_vowel():
    alphabet = ["a", "á", "b", "c", "č", "d", "ď", "e", "ě", "é", "f", "g", "h", "ch",
             "i", "í", "j", "k", "l", "m", "n", "ň", "o", "ó", "p", "q", "r", "ř",
             "s", "š", "t", "ť", "u", "ú", "ů", "ou", "v", "w", "x", "y", "ý", "z", "ž"]
    expected = [True, True, False, False, False, False, False, True, True, True, False, False, False, False,
                True, True, False, False, False, False, False, False, True, True, False, False, False, False,
                False, False, False, False, True, True, True, True, False, False, False, True, True, False, False]
    for i in range(len(alphabet)):
        assert vutils.isconsonant(alphabet[i]) != expected[i]

# tests get_vowel() function
# vowels in stems should be returned properly
# vowel digraphs return a 2 element string
# consonant clusters return the empty string
# empty string is obviously empty
def test_get_vowel():
    # test strings will also container other symbols since using regex strings
    # but they are OBVIOUSLY not vowels

    # nothing
    letters = ""
    expected = ""
    assert vutils.get_vowel(letters) == expected

    # all consonants
    consonants = vutils.consonant
    assert vutils.get_vowel(consonants) == expected

     # all vowels
    expected = "ouáéíóúůýaeiouyěií" # repeat since using regex string as source
    vowels = vutils.vowel
    assert vutils.get_vowel(vowels) == expected

    # vowels and consonants
    letters = consonants + vowels
    assert vutils.get_vowel(letters) == expected

# tests get_consonant() function
# vowels return empty
# consonant clusters should be returned properly
# empty string is obviously empty
def test_get_consonant():
    # test strings will also container other symbols since using regex strings
    # but they are OBVIOUSLY not consonants

    # nothing
    letters = ""
    expected = ""
    assert vutils.get_consonant(letters) == expected

    # all vowels
    vowels = vutils.vowel
    assert vutils.get_consonant(vowels) == expected

     # all vowels
    expected = "chstštctčtdghknstrbmpvfqwxcčďjňřšťzžl" # repeat since using regex string as source
    consonants = vutils.consonant_or_digraph
    assert vutils.get_consonant(consonants) == expected

    # vowels and consonants
    letters = consonants + vowels
    assert vutils.get_consonant(letters) == expected


# tests contains_vowel() function
# contained strings return true
# consonant clusters return false
# empty string is false
def test_contains_vowel():
    # test strings will also container other symbols since using regex strings
    # but they are OBVIOUSLY not vowels

    # nothing
    letters = ""
    expected = False
    assert vutils.contains_vowel(letters) == expected

    # all consonants
    consonants = vutils.consonant
    assert vutils.contains_vowel(consonants) == expected

     # all vowels
    expected = True
    vowels = vutils.vowel
    assert vutils.contains_vowel(vowels) == expected

    # vowels and consonants
    letters = consonants + vowels
    assert vutils.contains_vowel(letters) == expected
    


# tests lengthen() function
# basically test of get_long_vowel() but with words instead of letters
def test_lengthen():
    # nothing
    stem = ""
    expected = ""
    assert vutils.lengthen(stem) == expected

    alphabet = ["a", "á", "b", "c", "č", "d", "ď", "e", "ě", "é", "f", "g", "h", "ch",
             "i", "í", "j", "k", "l", "m", "n", "ň", "o", "ó", "p", "q", "r", "ř",
             "s", "š", "t", "ť", "u", "ú", "ů", "ou", "v", "w", "x", "y", "ý", "z", "ž"]
    expected = ["á", "á", "b", "c", "č", "d", "ď", "é", "ě", "é", "f", "g", "h", "ch",
             "í", "í", "j", "k", "l", "m", "n", "ň", "ů", "ó", "p", "q", "r", "ř",
             "s", "š", "t", "ť", "ou", "ú", "ů", "ou", "v", "w", "x", "ý", "ý", "z", "ž"]
    
    for i in range(len(alphabet)):
        assert vutils.lengthen( "n" + alphabet[i]) == "n" + expected[i]

# tests shorten() function
# basically test of get_short_vowel() but with words instead of letters
def test_shorten():
    # nothing
    stem = ""
    expected = ""
    assert vutils.shorten(stem) == expected

    alphabet = ["a", "á", "b", "c", "č", "d", "ď", "e", "ě", "é", "f", "g", "h", "ch",
             "i", "í", "j", "k", "l", "m", "n", "ň", "o", "ó", "p", "q", "r", "ř",
             "s", "š", "t", "ť", "u", "ú", "ů", "ou", "v", "w", "x", "y", "ý", "z", "ž"]
    expected = ["a", "a", "b", "c", "č", "d", "ď", "e", "ě", "e", "f", "g", "h", "ch",
             "i", "i", "j", "k", "l", "m", "n", "ň", "o", "ó", "p", "q", "r", "ř",
             "s", "š", "t", "ť", "u", "u", "o", "u", "v", "w", "x", "y", "y", "z", "ž"]
    
    for i in range(len(alphabet)):
        assert vutils.shorten( "n" + alphabet[i]) == "n" + expected[i]

# tests soften() function
# basically test of get_soft_consonant() but with words instead of letters
def test_soften():
    # nothing
    stem = ""
    expected = ""
    assert vutils.soften(stem) == expected

    alphabet = ["a", "á", "b", "c", "č", "d", "ď", "e", "ě", "é", "f", "g", "h", "ch",
             "i", "í", "j", "k", "l", "m", "n", "ň", "o", "ó", "p", "q", "r", "ř",
             "s", "š", "t", "ť", "u", "ú", "ů", "ou", "v", "w", "x", "y", "ý", "z", "ž"]
    expected = ["a", "á", "b", "c", "č", "ď", "ď", "e", "ě", "é", "f", "z", "z", "š",
             "i", "í", "j", "c", "l", "m", "ň", "ň", "o", "ó", "p", "q", "ř", "ř",
             "s", "š", "ť", "ť", "u", "ú", "ů", "ou", "v", "w", "x", "y", "ý", "z", "ž"]
    
    for i in range(len(alphabet)):
        assert vutils.soften( "a" + alphabet[i]) == "a" + expected[i]

# tests harden() function
# basically test of get_hard_consonant() but with words instead of letters
def test_harden():
    # nothing
    stem = ""
    expected = ""
    assert vutils.harden(stem) == expected

    alphabet = ["a", "á", "b", "c", "č", "d", "ď", "e", "ě", "é", "f", "g", "h", "ch",
             "i", "í", "j", "k", "l", "m", "n", "ň", "o", "ó", "p", "q", "r", "ř",
             "s", "š", "t", "ť", "u", "ú", "ů", "ou", "v", "w", "x", "y", "ý", "z", "ž"]
    expected = ["a", "á", "b", "k", "č", "d", "d", "e", "ě", "é", "f", "g", "h", "ch",
             "i", "í", "j", "k", "l", "m", "n", "n", "o", "ó", "p", "q", "r", "r",
             "s", "ch", "t", "t", "u", "ú", "ů", "ou", "v", "w", "x", "y", "ý", "h", "ž"]
    
    for i in range(len(alphabet)):
        assert vutils.harden( "a" + alphabet[i]) == "a" + expected[i]


# tests fix_spelling()
# [ďťň][ěií] --> [dtn][ěií] (harden the consonant)
# [cčjlsšřzž][ěií]--> [cčjlsšrřzž][eií] (harden the e)
def test_fix_spelling():

    expected = [["ce", "ci", "cí"], ["če", "či", "čí"], ["dě", "di", "dí"], ["je", "ji", "jí"],
                ["ně", "ni", "ní"], ["ře", "ři", "ří"], ["še", "ši", "ší"], ["tě", "ti", "tí"], 
                ["ze", "zi", "zí"], ["že", "ži", "ží"], ["le", "li", "lí"]]  
    for i in range(len(vutils.soft_consonant[1:-1])): # no [] in string
        for j in range(len(vutils.soft_vowel[1:-1])): # no [] in string
            consonant = vutils.soft_consonant[1 + i] # skip [
            vowel = vutils.soft_vowel[1 + j] # skip [
            assert vutils.fix_spelling(consonant + vowel) == expected[i][j]


# tests syllables
def test_syllables():

    s = vutils.Syllables("pokrm")
    assert s.syllable_list == [('po', False), ('krm', True)]
    assert s.inspect_syllable(0) == 'po'
    assert s.inspect_syllable(1) == 'krm'
    assert s.is_syllabic(0) == False
    assert s.is_syllabic(1) == True

    s = vutils.Syllables("trp")
    assert s.syllable_list == [('trp', True)]
    assert s.inspect_syllable(0) == 'trp'
    assert s.is_syllabic(0) == True

    s = vutils.Syllables("shromazdit")
    assert s.syllable_list == [('shro', False), ('ma', False), ('zdit', False)]
    assert s.inspect_syllable(0) == 'shro'
    assert s.inspect_syllable(1) == 'ma'
    assert s.inspect_syllable(2) == 'zdit'
    assert s.is_syllabic(0) == False
    assert s.is_syllabic(1) == False
    assert s.is_syllabic(2) == False


