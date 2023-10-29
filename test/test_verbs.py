# tests verb classes in initialization and conjugation of non-present tenses and non-indicative moods

import pytest
import src.verbs as v

############# BASE CLASS VERB TESTS ################

# tests initialization of a Verb
def test_init_default():
     # test with all empty strings
     a = v.Verb()
     assert a.infinitive == ""
     assert a.ending == ""
     assert a.stem == ""
     assert a.present_stem == ""
     assert a.past_stem == ""
     assert a.imperative_stem == ""


def test_init_non_default():
    # tests initializations with non-empty strings
    a = v.Verb("foo", "bar")
    assert a.infinitive == "foo"
    assert a.ending == "bar"
    assert a.stem == ""
    assert a.present_stem == ""
    assert a.past_stem == ""
    assert a.imperative_stem == ""

    # conjugation should also be empty
    for tense in range(len(v.Tense)):
        for person in range(len(v.Person)):
            assert a.get_conjugation_at(tense, person) == ""


# test conjugations across each tense
def test_conjugate_present():
    # should still remain the empty string
    a = v.Verb()
    a.conjugate(v.Tense.PRESENT)

    expected_present= ["", "", "", "", "", ""] # present tense is class dependent
    for person in range(len(v.Person)):
        assert expected_present[person] == a.get_conjugation_at(v.Tense.PRESENT, person)

    # even with an infinitive should still be empty
    b = v.Verb("foobar", "bar")
    b.conjugate(v.Tense.PRESENT)
    for person in range(len(v.Person)):
        assert expected_present[person] == b.get_conjugation_at(v.Tense.PRESENT, person)

def test_conjugate_past():
    # should have the right auxillaries
    a = v.Verb()
    a.conjugate(v.Tense.PAST)
    expected_past = ["/a jsem", "/a jsi/jseš", "/a/o", "i/y jsme", "i/y jste", "i/y/a"] # past tense
    for person in range(len(v.Person)):
        assert expected_past[person] == a.get_conjugation_at(v.Tense.PAST, person)


    # auxiliaries should still be correct with non-empty (in this case empty)
    b = v.Verb("foobar", "bar")
    b.conjugate(v.Tense.PAST)
    for person in range(len(v.Person)):
        assert expected_past[person] == b.get_conjugation_at(v.Tense.PAST, person)

def test_conjugate_future():
     # should have the right auxillaries
    a = v.Verb()
    a.conjugate(v.Tense.FUTURE)
    expected_future = ["budu", "budeš", "bude", "budeme", "budete", "budou"] # future tense
    for person in range(len(v.Person)):
        assert expected_future[person] == a.get_conjugation_at(v.Tense.FUTURE, person)


    # there should now be an associated infinitive that is non-empty
    expected_future = ["budu foobar", "budeš foobar", "bude foobar", "budeme foobar", "budete foobar", "budou foobar"] # future tense
    b = v.Verb("foobar", "bar")
    b.conjugate(v.Tense.FUTURE)
    for person in range(len(v.Person)):
        assert expected_future[person] == b.get_conjugation_at(v.Tense.FUTURE, person)

def test_conjugate_imperative():
     # should have the right auxillaries
    a = v.Verb()
    a.conjugate(v.Tense.IMPERATIVE)
    expected_imperative = ["", "", "", "me", "te", ""] # imperative mood
    for person in range(len(v.Person)):
        assert expected_imperative[person] == a.get_conjugation_at(v.Tense.IMPERATIVE, person)


    # should all still be empty-ish
    b = v.Verb("foobar", "bar")
    b.conjugate(v.Tense.IMPERATIVE)
    for person in range(len(v.Person)):
        assert expected_imperative[person] == b.get_conjugation_at(v.Tense.IMPERATIVE, person)

def test_conjugate_conditional():
    # should have the right auxillaries
    expected_conditional = ["/a bych", "/a bys", "/a/o by", "i/y bychom", "i/y byste", "i/y/a by"]
    a = v.Verb()
    a.conjugate(v.Tense.CONDITIONAL)
    for person in range(len(v.Person)):
        assert expected_conditional[person] == a.get_conjugation_at(v.Tense.CONDITIONAL, person)


    # should all still be empty-ish
    b = v.Verb("foobar", "bar")
    b.conjugate(v.Tense.CONDITIONAL)
    for person in range(len(v.Person)):
        assert expected_conditional[person] == b.get_conjugation_at(v.Tense.CONDITIONAL, person)


# test conjugations across all persons (and i guess tests that other entries remain empty)
def test_conjugate_first_person_singular():
    # expected conjugations
    # indices (0-4): present, past, future, imperative, conditional
    person = v.Person.FIRST_SG
    expected_conjugations = ["", "/a jsem", "budu", "", "/a bych"]

    a = v.Verb()
    a.conjugate(person_idx = person)
    for tense in range(len(v.Tense)):
        assert expected_conjugations[tense] == a.get_conjugation_at(tense, person)

    b = v.Verb("foobar", "bar")
    expected_conjugations = ["", "/a jsem", "budu foobar", "", "/a bych"]
    b.conjugate(person_idx = person)
    for tense in range(len(v.Tense)):
        assert expected_conjugations[tense] == b.get_conjugation_at(tense, person)

def test_conjugate_second_person_singular():
    # expected conjugations
    # indices (0-4): present, past, future, imperative, conditional
    person = v.Person.SECOND_SG
    expected_conjugations = ["", "/a jsi/jseš", "budeš", "", "/a bys"]

    a = v.Verb()
    a.conjugate(person_idx = person)
    for tense in range(len(v.Tense)):
        assert expected_conjugations[tense] == a.get_conjugation_at(tense, person)

    b = v.Verb("foobar", "bar")
    expected_conjugations = ["", "/a jsi/jseš", "budeš foobar", "", "/a bys"]
    b.conjugate(person_idx = person)
    for tense in range(len(v.Tense)):
        assert expected_conjugations[tense] == b.get_conjugation_at(tense, person)

def test_conjugate_third_person_singular():
    # expected conjugations
    # indices (0-4): present, past, future, imperative, conditional
    person = v.Person.THIRD_SG
    expected_conjugations = ["", "/a/o", "bude", "", "/a/o by"]

    a = v.Verb()
    a.conjugate(person_idx = person)
    for tense in range(len(v.Tense)):
        assert expected_conjugations[tense] == a.get_conjugation_at(tense, person)

    b = v.Verb("foobar", "bar")
    expected_conjugations = ["", "/a/o", "bude foobar", "", "/a/o by"]
    b.conjugate(person_idx = person)
    for tense in range(len(v.Tense)):
        assert expected_conjugations[tense] == b.get_conjugation_at(tense, person)

def test_conjugate_first_person_plural():
    # expected conjugations
    # indices (0-4): present, past, future, imperative, conditional
    person = v.Person.FIRST_PL
    expected_conjugations = ["", "i/y jsme", "budeme", "me", "i/y bychom"]

    a = v.Verb()
    a.conjugate(person_idx = person)
    for tense in range(len(v.Tense)):
        assert expected_conjugations[tense] == a.get_conjugation_at(tense, person)

    b = v.Verb("foobar", "bar")
    expected_conjugations = ["", "i/y jsme", "budeme foobar", "me", "i/y bychom"]
    b.conjugate(person_idx = person)
    for tense in range(len(v.Tense)):
        assert expected_conjugations[tense] == b.get_conjugation_at(tense, person)

def test_conjugate_second_person_plural():
    # expected conjugations
    # indices (0-4): present, past, future, imperative, conditional
    person = v.Person.SECOND_PL
    expected_conjugations = ["", "i/y jste", "budete", "te", "i/y byste"]

    a = v.Verb()
    a.conjugate(person_idx = person)
    for tense in range(len(v.Tense)):
        assert expected_conjugations[tense] == a.get_conjugation_at(tense, person)

    b = v.Verb("foobar", "bar")
    expected_conjugations = ["", "i/y jste", "budete foobar", "te", "i/y byste"]
    b.conjugate(person_idx = person)
    for tense in range(len(v.Tense)):
        assert expected_conjugations[tense] == b.get_conjugation_at(tense, person)

def test_conjugate_third_person_plural():
    # expected conjugations
    # indices (0-4): present, past, future, imperative, conditional
    person = v.Person.THIRD_PL
    expected_conjugations = ["", "i/y/a", "budou", "", "i/y/a by"]

    a = v.Verb()
    a.conjugate(person_idx = person)
    for tense in range(len(v.Tense)):
        assert expected_conjugations[tense] == a.get_conjugation_at(tense, person)

    b = v.Verb("foobar", "bar")
    expected_conjugations = ["", "i/y/a", "budou foobar", "", "i/y/a by"]
    b.conjugate(person_idx = person)
    for tense in range(len(v.Tense)):
        assert expected_conjugations[tense] == b.get_conjugation_at(tense, person)

# test all conjugations at once
def test_conjugate_all():

    # expected conjugations
    # indices (0-4): present, past, future, imperative, conditional
    expected_conjugations = []
    expected_present= ["", "", "", "", "", ""] # present tense is class dependent
    expected_past = ["/a jsem", "/a jsi/jseš", "/a/o", "i/y jsme", "i/y jste", "i/y/a"] # past tense
    expected_future = ["budu", "budeš", "bude", "budeme", "budete", "budou"] # future tense
    expected_imperative = ["", "", "", "me", "te", ""] # imperative mood
    expected_conditional = ["/a bych", "/a bys", "/a/o by", "i/y bychom", "i/y byste", "i/y/a by"] # (present) conditional mood

    # indices (0-4): present, past, future, imperative, conditional
    expected_conjugations = [expected_present, expected_past, expected_future, expected_imperative, expected_conditional]

    # conjugate everything
    a = v.Verb()
    a.conjugate() 
    for tense in range(len(v.Tense)):
        for person in range(len(v.Person)):
            assert expected_conjugations[tense][person] == a.get_conjugation_at(tense, person)

    # now for a verb with an actual infinitive
    b = v.Verb("foobar", "bar")
    expected_future = ["budu foobar", "budeš foobar", "bude foobar", "budeme foobar", "budete foobar", "budou foobar"]
    expected_conjugations = [expected_present, expected_past, expected_future, expected_imperative, expected_conditional]
    b.conjugate()
    for tense in range(len(v.Tense)):
        for person in range(len(v.Person)):
            assert expected_conjugations[tense][person] == b.get_conjugation_at(tense, person)

# test clear for one tense (future)
def test_conjugate_table_clear():
    tense = v.Tense.FUTURE
    a = v.Verb()
    a.conjugate()
    for person in range(len(v.Person)):
        assert a.get_conjugation_at(tense, person) != ""

    a.clear_table()
    for person in range(len(v.Person)):
        assert a.get_conjugation_at(tense, person) == ""

############# BÝT CLASS TESTS ###############
def test_byt_stems():
    byt = v.Byt("být")
    assert byt.infinitive == "být"
    assert byt.ending == ""
    assert byt.stem == ""
    assert byt.present_stem == ""
    assert byt.past_stem == "byl"
    assert byt.imperative_stem == "buď"

    # and the negated form
    nebyt = v.Byt("nebýt")
    assert nebyt.infinitive == "nebýt"
    assert nebyt._is_negative == True
    assert nebyt._prefix == "ne"
    assert nebyt.ending == ""
    assert nebyt.stem == ""
    assert nebyt.present_stem == ""
    assert nebyt.past_stem == "nebyl"
    assert nebyt.imperative_stem == "nebuď"


def test_byt_conjugate():
    byt = v.Byt("být")
    assert byt._is_negative == False
    # expected conjugations
    # indices (0-4): present, past, future, imperative, conditional
    expected_conjugations = []
    expected_present= ["jsem", "jseš/jsi", "je", "jsme", "jste", "jsou"]
    expected_past = ["byl/a jsem", "byl/a jsi/jseš", "byl/a/o", "byli/y jsme", "byli/y jste", "byli/y/a"]
    expected_future = ["budu", "budeš", "bude", "budeme", "budete", "budou"]
    expected_imperative = ["", "buď", "", "buďme", "buďte", ""]
    expected_conditional = ["byl/a bych", "byl/a bys", "byl/a/o by", "byli/y bychom", "byli/y byste", "byli/y/a by"]

    # indices (0-4): present, past, future, imperative, conditional
    expected_conjugations = [expected_present, expected_past, expected_future, expected_imperative, expected_conditional]

    byt.conjugate()
    for tense in range(len(v.Tense)):
        for person in range(len(v.Person)):
            assert expected_conjugations[tense][person] == byt.get_conjugation_at(tense, person)

def test_nebyt_conjugate():
    nebyt = v.Byt("nebýt")
    # expected conjugations
    # indices (0-4): present, past, future, imperative, conditional
    expected_conjugations = []
    expected_present= ["nejsem", "nejseš/jsi", "není", "nejsme", "nejste", "nejsou"]
    expected_past = ["nebyl/a jsem", "nebyl/a jsi/jseš", "nebyl/a/o", "nebyli/y jsme", "nebyli/y jste", "nebyli/y/a"]
    expected_future = ["nebudu", "nebudeš", "nebude", "nebudeme", "nebudete", "nebudou"]
    expected_imperative = ["", "nebuď", "", "nebuďme", "nebuďte", ""]
    expected_conditional = ["nebyl/a bych", "nebyl/a bys", "nebyl/a/o by", "nebyli/y bychom", "nebyli/y byste", "nebyli/y/a by"]

    # indices (0-4): present, past, future, imperative, conditional
    expected_conjugations = [expected_present, expected_past, expected_future, expected_imperative, expected_conditional]

    nebyt.conjugate()
    for tense in range(len(v.Tense)):
        for person in range(len(v.Person)):
            assert expected_conjugations[tense][person] == nebyt.get_conjugation_at(tense, person)

#### TESTS FOR INIT FLAGS (uses být) ####

# perfective verbs use the present tense to form the future, as they cannot express the present
# the future conjugations are expected present conjugations
# the present conjugations are empty strings (there is no conjugation)
def test_perfective_conjugation():
    expected_future= ("jsem", "jseš/jsi", "je", "jsme", "jste", "jsou")
    expected_present = ("", "", "", "", "", "")
    byt = v.Byt("být", is_perfective = True)

    # stuff from just __init__
    assert byt._is_negative == False
    assert v.get_motion(byt._is_motion) == False
    assert byt._is_perfective == True
    assert byt._tense_to_auxiliary[v.Tense.FUTURE] == ("", "", "", "", "", "")
    assert byt._tense_to_ending[v.Tense.FUTURE] == expected_future
    assert byt._tense_to_ending[v.Tense.PRESENT] == expected_present # because být this gets overwritten

    # now conjugation should reflect this
    byt.conjugate(tense_idx = v.Tense.FUTURE)

    # future conjugations should be present conjugations
    for person in range(len(v.Person)):
        assert expected_future[person] == byt.get_conjugation_at(v.Tense.FUTURE, person)

def test_motion_conjugation():
    expected_future= ("pojsem", "pojseš/jsi", "poje", "pojsme", "pojste", "pojsou")
    expected_present = ("jsem", "jseš/jsi", "je", "jsme", "jste", "jsou")
    byt = v.Byt("být", is_motion = (True, "po"))

    # stuff from just __init__
    assert byt._is_negative == False
    assert v.get_motion(byt._is_motion) == True
    assert byt._is_perfective == False
    assert byt._present_endings == expected_present
    assert byt._tense_to_auxiliary[v.Tense.FUTURE] == v.Verb._empty
    assert byt._tense_to_ending[v.Tense.FUTURE] == expected_present

    # now conjugation should reflect this
    byt.conjugate(tense_idx = v.Tense.FUTURE)
    byt.conjugate(tense_idx = v.Tense.PRESENT)

    # future conjugations should be present conjugations
    for person in range(len(v.Person)):
        assert expected_future[person] == byt.get_conjugation_at(v.Tense.FUTURE, person)

    # present conjugations should also be present
    for person in range(len(v.Person)):
        assert expected_present[person] == byt.get_conjugation_at(v.Tense.PRESENT, person)

######## REGULAR CLASS 1 VERBS #############
# tests that the right stems are formed and correct conjugations for -at
def test_class1_at_short_a():
    a = v.Class1_at("bat", "at")

    # expected conjugations
    # indices (0-4): present, past, future, imperative, conditional
    expected_conjugations = []
    expect_present= ["bám", "báš", "bá", "báme", "báte", "bají"]
    expected_past = ["bal/a jsem", "bal/a jsi/jseš", "bal/a/o", "bali/y jsme", "bali/y jste", "bali/y/a"]
    expected_future = ["budu bat", "budeš bat", "bude bat", "budeme bat", "budete bat", "budou bat"]
    expected_imperative = ["", "bej", "", "bejme", "bejte", ""]
    expected_conditional = ["bal/a bych", "bal/a bys", "bal/a/o by", "bali/y bychom", "bali/y byste", "bali/y/a by"]

    # from __init__
    assert a.infinitive == "bat"
    assert a.ending == "at"
    assert a.stem == "b"
    assert a.present_stem == "b"
    assert a.past_stem == "bal"
    assert a.imperative_stem == "bej"
    assert a._is_negative == False
    assert a._is_perfective == False
    assert v.get_motion(a._is_motion) == False
    assert v.get_motion_prefix(a._is_motion) == ""

    # indices (0-4): present, past, future, imperative, conditional
    expected_conjugations = [expect_present, expected_past, expected_future, expected_imperative, expected_conditional]
    a.clear_table()
    a.conjugate()
    for tense in range(0, len(v.Tense)):
        for person in range(0, len(v.Person)):
            assert expected_conjugations[tense][person] == a.get_conjugation_at(tense, person)
    assert a.get_table() == expected_conjugations # just double checking!


# tests that the right stems are formed and correct conjugations for -át
def test_class1_at_long_a():
    a = v.Class1_at("bát", "at")

    # expected conjugations
    # indices (0-4): present, past, future, imperative, conditional
    expected_conjugations = []
    expect_present= ["bám", "báš", "bá", "báme", "báte", "bají"]
    expected_past = ["bal/a jsem", "bal/a jsi/jseš", "bal/a/o", "bali/y jsme", "bali/y jste", "bali/y/a"]
    expected_future = ["budu bát", "budeš bát", "bude bát", "budeme bát", "budete bát", "budou bát"]
    expected_imperative = ["", "bej", "", "bejme", "bejte", ""]
    expected_conditional = ["bal/a bych", "bal/a bys", "bal/a/o by", "bali/y bychom", "bali/y byste", "bali/y/a by"]

    # from __init__
    assert a.infinitive == "bát"
    assert a.ending == "at"
    assert a.stem == "b"
    assert a.present_stem == "b"
    assert a.past_stem == "bal"
    assert a.imperative_stem == "bej"
    assert a._is_negative == False
    assert a._is_perfective == False
    assert v.get_motion(a._is_motion) == False
    assert v.get_motion_prefix(a._is_motion) == ""

    # indices (0-4): present, past, future, imperative, conditional
    expected_conjugations = [expect_present, expected_past, expected_future, expected_imperative, expected_conditional]
    a.conjugate()
    for tense in range(0, len(v.Tense)):
        for person in range(0, len(v.Person)):
            assert expected_conjugations[tense][person] == a.get_conjugation_at(tense, person)
    assert a.get_table() == expected_conjugations # just double checking!


############# REGULAR CLASS 2 VERBS ###################

# tests conjugation of the ít/ýt subclass
def test_class2_yt():
    a = v.Class2_ityt("být", "ýt")

    # expected conjugations
    # indices (0-4): present, past, future, imperative, conditional
    expected_conjugations = []
    expect_present= ["byji/u", "byješ", "byje", "byjeme", "byjete", "byjí"]
    expected_past = ["byl/a jsem", "byl/a jsi/jseš", "byl/a/o", "byli/y jsme", "byli/y jste", "byli/y/a"]
    expected_future = ["budu být", "budeš být", "bude být", "budeme být", "budete být", "budou být"]
    expected_imperative = ["", "byj", "", "byjme", "byjte", ""]
    expected_conditional = ["byl/a bych", "byl/a bys", "byl/a/o by", "byli/y bychom", "byli/y byste", "byli/y/a by"]

    # from __init__
    assert a.infinitive == "být"
    assert a.ending == "ýt"
    assert a.stem == "b"
    assert a.present_stem == "byj"
    assert a.past_stem == "byl"
    assert a.imperative_stem == "byj"
    assert a._is_negative == False
    assert a._is_perfective == False
    assert v.get_motion(a._is_motion) == False
    assert v.get_motion_prefix(a._is_motion) == ""

    # indices (0-4): present, past, future, imperative, conditional
    expected_conjugations = [expect_present, expected_past, expected_future, expected_imperative, expected_conditional]
    a.conjugate()
    for tense in range(0, len(v.Tense)):
        for person in range(0, len(v.Person)):
            assert expected_conjugations[tense][person] == a.get_conjugation_at(tense, person)
    assert a.get_table() == expected_conjugations # just double checking!

def test_class2_it():
    a = v.Class2_ityt("bít", "ít")

    # expected conjugations
    # indices (0-4): present, past, future, imperative, conditional
    expected_conjugations = []
    expect_present= ["biji/u", "biješ", "bije", "bijeme", "bijete", "bijí"]
    expected_past = ["bil/a jsem", "bil/a jsi/jseš", "bil/a/o", "bili/y jsme", "bili/y jste", "bili/y/a"]
    expected_future = ["budu bít", "budeš bít", "bude bít", "budeme bít", "budete bít", "budou bít"]
    expected_imperative = ["", "bij", "", "bijme", "bijte", ""]
    expected_conditional = ["bil/a bych", "bil/a bys", "bil/a/o by", "bili/y bychom", "bili/y byste", "bili/y/a by"]

    # from __init__
    assert a.infinitive == "bít"
    assert a.ending == "ít"
    assert a.stem == "b"
    assert a.present_stem == "bij"
    assert a.past_stem == "bil"
    assert a.imperative_stem == "bij"
    assert a._is_negative == False
    assert a._is_perfective == False
    assert v.get_motion(a._is_motion) == False
    assert v.get_motion_prefix(a._is_motion) == ""

    # indices (0-4): present, past, future, imperative, conditional
    expected_conjugations = [expect_present, expected_past, expected_future, expected_imperative, expected_conditional]
    a.conjugate()
    for tense in range(0, len(v.Tense)):
        for person in range(0, len(v.Person)):
            assert expected_conjugations[tense][person] == a.get_conjugation_at(tense, person)
    assert a.get_table() == expected_conjugations # just double checking!

# tests that the chtít correction is applied on (un)prefixed chtít-like verbs (tests conjugations only affected by correction)
def test_class2_chtit_correction():
    a = v.Class2_ityt("chtít", "ít")
    a.conjugate(v.Tense.PRESENT, v.Person.FIRST_SG)
    a.conjugate(v.Tense.PRESENT, v.Person.THIRD_PL)
    assert a.get_conjugation_at(v.Tense.PRESENT, v.Person.FIRST_SG) == "chci"
    assert a.get_conjugation_at(v.Tense.PRESENT, v.Person.THIRD_PL) == "chtějí"

    b = v.Class2_ityt("nechtít", "ít")
    b.conjugate(v.Tense.PRESENT, v.Person.FIRST_SG)
    b.conjugate(v.Tense.PRESENT, v.Person.THIRD_PL)
    assert b.get_conjugation_at(v.Tense.PRESENT, v.Person.FIRST_SG) == "nechci"
    assert b.get_conjugation_at(v.Tense.PRESENT, v.Person.THIRD_PL) == "nechtějí"

    c = v.Class2_ityt("zachtít", "ít")
    c.conjugate(v.Tense.PRESENT, v.Person.FIRST_SG)
    c.conjugate(v.Tense.PRESENT, v.Person.THIRD_PL)
    assert c.get_conjugation_at(v.Tense.PRESENT, v.Person.FIRST_SG) == "zachci"
    assert c.get_conjugation_at(v.Tense.PRESENT, v.Person.THIRD_PL) == "zachtějí"

    d = v.Class2_ityt("nezachtít", "ít")
    d.conjugate(v.Tense.PRESENT, v.Person.FIRST_SG)
    d.conjugate(v.Tense.PRESENT, v.Person.THIRD_PL)
    assert d.get_conjugation_at(v.Tense.PRESENT, v.Person.FIRST_SG) == "nezachci"
    assert d.get_conjugation_at(v.Tense.PRESENT, v.Person.THIRD_PL) == "nezachtějí"

# tests the conjugation of the ovat subclass
def test_class2_ovat():
    a = v.Class2_ovat("bovat", "ovat")

    # expected conjugations
    # indices (0-4): present, past, future, imperative, conditional
    expected_conjugations = []
    expect_present= ["buji/u", "buješ", "buje", "bujeme", "bujete", "bují"]
    expected_past = ["boval/a jsem", "boval/a jsi/jseš", "boval/a/o", "bovali/y jsme", "bovali/y jste", "bovali/y/a"]
    expected_future = ["budu bovat", "budeš bovat", "bude bovat", "budeme bovat", "budete bovat", "budou bovat"]
    expected_imperative = ["", "buj", "", "bujme", "bujte", ""]
    expected_conditional = ["boval/a bych", "boval/a bys", "boval/a/o by", "bovali/y bychom", "bovali/y byste", "bovali/y/a by"]

    # from __init__
    assert a.infinitive == "bovat"
    assert a.ending == "ovat"
    assert a.stem == "b"
    assert a.present_stem == "buj"
    assert a.past_stem == "boval"
    assert a.imperative_stem == "buj"
    assert a._is_negative == False
    assert a._is_perfective == False
    assert v.get_motion(a._is_motion) == False
    assert v.get_motion_prefix(a._is_motion) == ""

    # indices (0-4): present, past, future, imperative, conditional
    expected_conjugations = [expect_present, expected_past, expected_future, expected_imperative, expected_conditional]
    a.conjugate()
    for tense in range(0, len(v.Tense)):
        for person in range(0, len(v.Person)):
            assert expected_conjugations[tense][person] == a.get_conjugation_at(tense, person)
    assert a.get_table() == expected_conjugations # just double checking!'



###### REGULAR CLASS 3 VERBS #####

# tests conjugation of majority verbs (one's WITHOUT an imperative stem special case)

# regular -it verbs
def test_class3_it():
    a = v.Class3_itet("skočit", "it")

    # expected conjugations
    # indices (0-4): present, past, future, imperative, conditional
    expected_conjugations = []
    expect_present= ["skočím", "skočíš", "skočí", "skočíme", "skočíte", "skočí"]
    expected_past = ["skočil/a jsem", "skočil/a jsi/jseš", "skočil/a/o", "skočili/y jsme", "skočili/y jste", "skočili/y/a"]
    expected_future = ["budu skočit", "budeš skočit", "bude skočit", "budeme skočit", "budete skočit", "budou skočit"]
    expected_imperative = ["", "skoč", "", "skočme", "skočte", ""]
    expected_conditional = ["skočil/a bych", "skočil/a bys", "skočil/a/o by", "skočili/y bychom", "skočili/y byste", "skočili/y/a by"]

    # from __init__
    assert a.infinitive == "skočit"
    assert a.ending == "it"
    assert a.stem == "skoč"
    assert a.present_stem == "skoč"
    assert a.past_stem == "skočil"
    assert a.imperative_stem == "skoč"
    assert a._is_negative == False
    assert a._is_perfective == False
    assert v.get_motion(a._is_motion) == False
    assert v.get_motion_prefix(a._is_motion) == ""

    # indices (0-4): present, past, future, imperative, conditional
    expected_conjugations = [expect_present, expected_past, expected_future, expected_imperative, expected_conditional]
    a.conjugate()
    for tense in range(0, len(v.Tense)):
        for person in range(0, len(v.Person)):
            assert expected_conjugations[tense][person] == a.get_conjugation_at(tense, person)
    assert a.get_table() == expected_conjugations # just double checking!'

# tests regular -et verbs (hard e, NOT ě!)
def test_class3_et_hard_e():
    a = v.Class3_itet("mručet", "et")

    # expected conjugations
    # indices (0-4): present, past, future, imperative, conditional
    expected_conjugations = []
    expect_present= ["mručím", "mručíš", "mručí", "mručíme", "mručíte", "mručí"]
    expected_past = ["mručel/a jsem", "mručel/a jsi/jseš", "mručel/a/o", "mručeli/y jsme", "mručeli/y jste", "mručeli/y/a"]
    expected_future = ["budu mručet", "budeš mručet", "bude mručet", "budeme mručet", "budete mručet", "budou mručet"]
    expected_imperative = ["", "mruč", "", "mručme", "mručte", ""]
    expected_conditional = ["mručel/a bych", "mručel/a bys", "mručel/a/o by", "mručeli/y bychom", "mručeli/y byste", "mručeli/y/a by"]

    # from __init__
    assert a.infinitive == "mručet"
    assert a.ending == "et"
    assert a.stem == "mruč"
    assert a.present_stem == "mruč"
    assert a.past_stem == "mručel"
    assert a.imperative_stem == "mruč"
    assert a._is_negative == False
    assert a._is_perfective == False
    assert v.get_motion(a._is_motion) == False
    assert v.get_motion_prefix(a._is_motion) == ""

    # indices (0-4): present, past, future, imperative, conditional
    expected_conjugations = [expect_present, expected_past, expected_future, expected_imperative, expected_conditional]
    a.conjugate()
    for tense in range(0, len(v.Tense)):
        for person in range(0, len(v.Person)):
            assert expected_conjugations[tense][person] == a.get_conjugation_at(tense, person)
    assert a.get_table() == expected_conjugations # just double checking!'

# test regular -ět verbs (soft e)
def test_class3_et_soft_e():
    a = v.Class3_itet("dunět", "ět")

    # expected conjugations
    # indices (0-4): present, past, future, imperative, conditional
    expected_conjugations = []
    expect_present= ["duním", "duníš", "duní", "duníme", "duníte", "duní"]
    expected_past = ["duněl/a jsem", "duněl/a jsi/jseš", "duněl/a/o", "duněli/y jsme", "duněli/y jste", "duněli/y/a"]
    expected_future = ["budu dunět", "budeš dunět", "bude dunět", "budeme dunět", "budete dunět", "budou dunět"]
    expected_imperative = ["", "duň", "", "duňme", "duňte", ""]
    expected_conditional = ["duněl/a bych", "duněl/a bys", "duněl/a/o by", "duněli/y bychom", "duněli/y byste", "duněli/y/a by"]

    # from __init__
    assert a.infinitive == "dunět"
    assert a.ending == "ět"
    assert a.stem == "duň"
    assert a.present_stem == "dun"
    assert a.past_stem == "duněl"
    assert a.imperative_stem == "duň"
    assert a._is_negative == False
    assert a._is_perfective == False
    assert v.get_motion(a._is_motion) == False
    assert v.get_motion_prefix(a._is_motion) == ""

    # indices (0-4): present, past, future, imperative, conditional
    expected_conjugations = [expect_present, expected_past, expected_future, expected_imperative, expected_conditional]
    a.conjugate()
    for tense in range(0, len(v.Tense)):
        for person in range(0, len(v.Person)):
            assert expected_conjugations[tense][person] == a.get_conjugation_at(tense, person)
    assert a.get_table() == expected_conjugations # just double checking!'


# test imperative stem special cases
def test_class3_imperative_stem_long_et():
    # verbs to test:
    # chvět, vyvíjet, vyrábět, umět, přenášet, ztrácet, dovádět, pouštět, zkoušet, prospět, tvářet, slzet
    assert v.Class3_itet("chvět", "ět").imperative_stem == "chvěj"
    assert v.Class3_itet("vyvíjet", "et").imperative_stem == "vyvíjej"
    assert v.Class3_itet("vyrábět", "ět").imperative_stem == "vyráběj"
    assert v.Class3_itet("umět", "ět").imperative_stem == "uměj"
    assert v.Class3_itet("přenášet", "et").imperative_stem == "přenášej"
    assert v.Class3_itet("ztrácet", "et").imperative_stem == "ztrácej"
    assert v.Class3_itet("dovádět", "ět").imperative_stem == "dováděj"
    assert v.Class3_itet("pouštět", "ět").imperative_stem == "pouštěj"
    assert v.Class3_itet("zkoušet", "et").imperative_stem == "zkoušej"
    assert v.Class3_itet("prospět", "ět").imperative_stem == "prospěj"
    assert v.Class3_itet("tvářet", "et").imperative_stem == "tvářej"
    assert v.Class3_itet("slzet", "et").imperative_stem == "slzej"

def test_class3_imperative_stem_long_it():
    # verbs to test
    # chýlit, pálit, blížit, bouřit, bránit, cítit, hájit, kamarádit, podřídit, půlit,
    # rdousit, sloučit, tvářit, úžit, léčit, sílit
    assert v.Class3_itet("chýlit", "it").imperative_stem == "chyl"
    assert v.Class3_itet("pálit", "it").imperative_stem == "pal"
    assert v.Class3_itet("blížit", "it").imperative_stem == "bliž"
    assert v.Class3_itet("bouřit", "it").imperative_stem == "buř"
    assert v.Class3_itet("bránit", "it").imperative_stem == "braň"
    assert v.Class3_itet("cítit", "it").imperative_stem == "ciť"
    assert v.Class3_itet("hájit", "it").imperative_stem == "haj"
    assert v.Class3_itet("kamarádit", "it").imperative_stem == "kamaraď"
    assert v.Class3_itet("podřídit", "it").imperative_stem == "podřiď"
    assert v.Class3_itet("prýštit", "it").imperative_stem == "prýšti"
    assert v.Class3_itet("půlit", "it").imperative_stem == "pol"
    assert v.Class3_itet("rdousit", "it").imperative_stem == "rdus"
    assert v.Class3_itet("sloučit", "it").imperative_stem == "sluč"
    assert v.Class3_itet("tvářit", "it").imperative_stem == "tvař"
    assert v.Class3_itet("úžit", "it").imperative_stem == "už"
    assert v.Class3_itet("léčit", "it").imperative_stem == "leč"
    assert v.Class3_itet("sílit", "it").imperative_stem == "sil"

def test_class3_imperative_stem_cluster():
    # verbs to test
    # shromáždit, vřeštět, ošetřit, brázdit, ověnčit, bruslit, kreslit, běsnit, hmoždit, čpět, 
    # patřit, zhoršit, zlepšit, rozluštit, vrstvit, rozmístit, různit, sídlit, svraštit, šustit, tříštit, ústit, prýštit

    assert v.Class3_itet("shromáždit", "it").imperative_stem == "shromáždi"
    assert v.Class3_itet("vřeštět", "ět").imperative_stem == "vřešti"
    assert v.Class3_itet("ošetřit", "it").imperative_stem == "ošetři"
    assert v.Class3_itet("brázdit", "it").imperative_stem == "brázdi"
    assert v.Class3_itet("ověnčit", "it").imperative_stem == "ověnči"
    assert v.Class3_itet("bruslit", "it").imperative_stem == "brusli"
    assert v.Class3_itet("kreslit", "it").imperative_stem == "kresli"
    assert v.Class3_itet("běsnit", "it").imperative_stem == "běsni"
    assert v.Class3_itet("hmoždit", "it").imperative_stem == "hmoždi"
    assert v.Class3_itet("čpět", "ět").imperative_stem == "čpi"
    assert v.Class3_itet("patřit", "it").imperative_stem == "patři"
    assert v.Class3_itet("zhoršit", "it").imperative_stem == "zhorši"
    assert v.Class3_itet("zlepšit", "it").imperative_stem == "zlepši"
    assert v.Class3_itet("rozluštit", "it").imperative_stem == "rozlušti"
    assert v.Class3_itet("vrstvit", "it").imperative_stem == "vrstvi"
    assert v.Class3_itet("rozmístit", "it").imperative_stem == "rozmísti"
    assert v.Class3_itet("různit", "it").imperative_stem == "různi"
    assert v.Class3_itet("sídlit", "it").imperative_stem == "sídli"
    assert v.Class3_itet("svraštit", "it").imperative_stem == "svrašti"
    assert v.Class3_itet("šustit", "it").imperative_stem == "šusti"
    assert v.Class3_itet("třístit", "it").imperative_stem == "třísti"
    assert v.Class3_itet("ústit", "it").imperative_stem == "ústi"
    assert v.Class3_itet("prýštit", "it").imperative_stem == "prýšti"

def test_class3_imperative_stem():
    # verbs to test
    # pršet, trpět, drtit, robit, chytit, zkamenět, oslnit, naplnit, ověřit, mlčet, půjčit, tvrdit, opustit
    assert v.Class3_itet("pršet", "et").imperative_stem == "prš"
    assert v.Class3_itet("trpět", "ět").imperative_stem == "trp"
    assert v.Class3_itet("drtit", "it").imperative_stem == "drť"
    assert v.Class3_itet("robit", "it").imperative_stem == "rob"
    assert v.Class3_itet("chytit", "it").imperative_stem == "chyť"
    assert v.Class3_itet("zkamenět", "ět").imperative_stem == "zkameň"
    assert v.Class3_itet("oslnit", "it").imperative_stem == "oslň"
    assert v.Class3_itet("naplnit", "it").imperative_stem == "naplň"
    assert v.Class3_itet("ověřit", "it").imperative_stem == "ověř"
    assert v.Class3_itet("mlčet", "et").imperative_stem == "mlč"
    assert v.Class3_itet("půjčit", "it").imperative_stem == "půjč"
    assert v.Class3_itet("tvrdit", "it").imperative_stem == "tvrď"
    assert v.Class3_itet("opustit", "it").imperative_stem == "opusť"

###### REGULAR CLASS 4 VERBS #####

# tests conjugation of -nout subclass
def test_class4_nout_with_vowel():
    a = v.Class4_nout("bnout", "nout")

    # expected conjugations
    # indices (0-4): present, past, future, imperative, conditional
    expected_conjugations = []
    expect_present= ["bnu", "bneš", "bne", "bneme", "bnete", "bnou"]
    expected_past = ["bnul/a jsem", "bnul/a jsi/jseš", "bnul/a/o", "bnuli/y jsme", "bnuli/y jste", "bnuli/y/a"]
    expected_future = ["budu bnout", "budeš bnout", "bude bnout", "budeme bnout", "budete bnout", "budou bnout"]
    expected_imperative = ["", "bni", "", "bněme", "bněte", ""]
    expected_conditional = ["bnul/a bych", "bnul/a bys", "bnul/a/o by", "bnuli/y bychom", "bnuli/y byste", "bnuli/y/a by"]

    # from __init__
    assert a.infinitive == "bnout"
    assert a.ending == "nout"
    assert a.stem == "b"
    assert a.present_stem == "bn"
    assert a.past_stem == "bnul"
    assert a.imperative_stem == "bni"
    assert a._is_negative == False
    assert a._is_perfective == False
    assert v.get_motion(a._is_motion) == False
    assert v.get_motion_prefix(a._is_motion) == ""

    # indices (0-4): present, past, future, imperative, conditional
    expected_conjugations = [expect_present, expected_past, expected_future, expected_imperative, expected_conditional]
    a.conjugate()
    for tense in range(0, len(v.Tense)):
        for person in range(0, len(v.Person)):
            assert expected_conjugations[tense][person] == a.get_conjugation_at(tense, person)
    assert a.get_table() == expected_conjugations # just double checking!'

def test_class4_nout_without_vowel():
    a = v.Class4_nout("benout", "nout")

    # expected conjugations
    # indices (0-4): present, past, future, imperative, conditional
    expected_conjugations = []
    expect_present= ["benu", "beneš", "bene", "beneme", "benete", "benou"]
    expected_past = ["benul/a jsem", "benul/a jsi/jseš", "benul/a/o", "benuli/y jsme", "benuli/y jste", "benuli/y/a"]
    expected_future = ["budu benout", "budeš benout", "bude benout", "budeme benout", "budete benout", "budou benout"]
    expected_imperative = ["", "beň", "", "beňme", "beňte", ""]
    expected_conditional = ["benul/a bych", "benul/a bys", "benul/a/o by", "benuli/y bychom", "benuli/y byste", "benuli/y/a by"]

    # from __init__
    assert a.infinitive == "benout"
    assert a.ending == "nout"
    assert a.stem == "be"
    assert a.present_stem == "ben"
    assert a.past_stem == "benul"
    assert a.imperative_stem == "beň"
    assert a._is_negative == False
    assert a._is_perfective == False
    assert v.get_motion(a._is_motion) == False
    assert v.get_motion_prefix(a._is_motion) == ""

    # indices (0-4): present, past, future, imperative, conditional
    expected_conjugations = [expect_present, expected_past, expected_future, expected_imperative, expected_conditional]
    a.conjugate()
    for tense in range(0, len(v.Tense)):
        for person in range(0, len(v.Person)):
            assert expected_conjugations[tense][person] == a.get_conjugation_at(tense, person)
    assert a.get_table() == expected_conjugations # just double checking!'

# tests -st subclass
def test_class4_st():
    a = v.Class4_st("bást", "st")

    # expected conjugations
    # indices (0-4): present, past, future, imperative, conditional
    expected_conjugations = []
    expect_present= ["badu", "badeš", "bade", "bademe", "badete", "badou"]
    expected_past = ["badl/a jsem", "badl/a jsi/jseš", "badl/a/o", "badli/y jsme", "badli/y jste", "badli/y/a"]
    expected_future = ["budu bást", "budeš bást", "bude bást", "budeme bást", "budete bást", "budou bást"]
    expected_imperative = ["", "baď", "", "baďme", "baďte", ""]
    expected_conditional = ["badl/a bych", "badl/a bys", "badl/a/o by", "badli/y bychom", "badli/y byste", "badli/y/a by"]

    # from __init__
    assert a.infinitive == "bást"
    assert a.ending == "st"
    assert a.stem == "ba"
    assert a.present_stem == "bad"
    assert a.past_stem == "badl"
    assert a.imperative_stem == "baď"
    assert a._is_negative == False
    assert a._is_perfective == False
    assert v.get_motion(a._is_motion) == False
    assert v.get_motion_prefix(a._is_motion) == ""

    # indices (0-4): present, past, future, imperative, conditional
    expected_conjugations = [expect_present, expected_past, expected_future, expected_imperative, expected_conditional]
    a.conjugate()
    for tense in range(0, len(v.Tense)):
        for person in range(0, len(v.Person)):
            assert expected_conjugations[tense][person] == a.get_conjugation_at(tense, person)
    assert a.get_table() == expected_conjugations # just double checking!'


# tests conjugation of -zt subclass
def test_class4_zt():
    a = v.Class4_zt("bázt", "zt")

    # expected conjugations
    # indices (0-4): present, past, future, imperative, conditional
    expected_conjugations = []
    expect_present= ["bazu", "bazeš", "baze", "bazeme", "bazete", "bazou"]
    expected_past = ["bazl/a jsem", "bazl/a jsi/jseš", "bazl/a/o", "bazli/y jsme", "bazli/y jste", "bazli/y/a"]
    expected_future = ["budu bázt", "budeš bázt", "bude bázt", "budeme bázt", "budete bázt", "budou bázt"]
    expected_imperative = ["", "baz", "", "bazme", "bazte", ""]
    expected_conditional = ["bazl/a bych", "bazl/a bys", "bazl/a/o by", "bazli/y bychom", "bazli/y byste", "bazli/y/a by"]

    # from __init__
    assert a.infinitive == "bázt"
    assert a.ending == "zt"
    assert a.stem == "ba"
    assert a.present_stem == "baz"
    assert a.past_stem == "bazl"
    assert a.imperative_stem == "baz"
    assert a._is_negative == False
    assert a._is_perfective == False
    assert v.get_motion(a._is_motion) == False
    assert v.get_motion_prefix(a._is_motion) == ""

    # indices (0-4): present, past, future, imperative, conditional
    expected_conjugations = [expect_present, expected_past, expected_future, expected_imperative, expected_conditional]
    a.conjugate()
    for tense in range(0, len(v.Tense)):
        for person in range(0, len(v.Person)):
            assert expected_conjugations[tense][person] == a.get_conjugation_at(tense, person)
    assert a.get_table() == expected_conjugations # just double checking!

# tests conjugation of -ct subclass
def test_class4_ct():
    a = v.Class4_ct("báct", "ct")

    # expected conjugations
    # indices (0-4): present, past, future, imperative, conditional
    expected_conjugations = []
    expect_present= ["baču", "bačeš", "bače", "bačeme", "bačete", "bačou"]
    expected_past = ["bakl/a jsem", "bakl/a jsi/jseš", "bakl/a/o", "bakli/y jsme", "bakli/y jste", "bakli/y/a"]
    expected_future = ["budu báct", "budeš báct", "bude báct", "budeme báct", "budete báct", "budou báct"]
    expected_imperative = ["", "bač", "", "bačme", "bačte", ""]
    expected_conditional = ["bakl/a bych", "bakl/a bys", "bakl/a/o by", "bakli/y bychom", "bakli/y byste", "bakli/y/a by"]

    # from __init__
    assert a.infinitive == "báct"
    assert a.ending == "ct"
    assert a.stem == "ba"
    assert a.present_stem == "bač"
    assert a.past_stem == "bakl"
    assert a.imperative_stem == "bač"
    assert a._is_negative == False
    assert a._is_perfective == False
    assert v.get_motion(a._is_motion) == False
    assert v.get_motion_prefix(a._is_motion) == ""

    # indices (0-4): present, past, future, imperative, conditional
    expected_conjugations = [expect_present, expected_past, expected_future, expected_imperative, expected_conditional]
    a.conjugate()
    for tense in range(0, len(v.Tense)):
        for person in range(0, len(v.Person)):
            assert expected_conjugations[tense][person] == a.get_conjugation_at(tense, person)
    assert a.get_table() == expected_conjugations # just double checking!