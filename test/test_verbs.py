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
    for tense in range(v.Tense.NUM_TENSE):
        for person in range(v.Person.NUM_PERSON):
            assert a.get_conjugation_at(tense, person) == ""


# test conjugations across each tense
def test_conjugate_present():
    # should still remain the empty string
    a = v.Verb()
    a.conjugate(v.Tense.PRESENT)

    # including spaces since it's not normally a verb is conjugated with empty strings
    expected_present= [" ", " ", " ", " ", " ", " "] # present tense is class dependent
    for person in range(v.Person.NUM_PERSON):
        assert expected_present[person] == a.get_conjugation_at(v.Tense.PRESENT, person)

    # even with an infinitive should still be empty
    b = v.Verb("foobar", "bar")
    b.conjugate(v.Tense.PRESENT)
    for person in range(v.Person.NUM_PERSON):
        assert expected_present[person] == b.get_conjugation_at(v.Tense.PRESENT, person)

def test_conjugate_past():
    # should have the right auxillaries
    a = v.Verb()
    a.conjugate(v.Tense.PAST)
    expected_past = ["/a jsem", "/a jsi/jseš", "/a/o ", "i/y jsme", "i/y jste", "i/y/a "] # past tense
    for person in range(v.Person.NUM_PERSON):
        assert expected_past[person] == a.get_conjugation_at(v.Tense.PAST, person)


    # auxiliaries should still be correct with non-empty (in this case empty)
    b = v.Verb("foobar", "bar")
    b.conjugate(v.Tense.PAST)
    for person in range(v.Person.NUM_PERSON):
        assert expected_past[person] == b.get_conjugation_at(v.Tense.PAST, person)

def test_conjugate_future():
     # should have the right auxillaries
    a = v.Verb()
    a.conjugate(v.Tense.FUTURE)
    expected_future = ["budu ", "budeš ", "bude ", "budeme ", "budete ", "budou "] # future tense
    for person in range(v.Person.NUM_PERSON):
        assert expected_future[person] == a.get_conjugation_at(v.Tense.FUTURE, person)


    # there should now be an associated infinitive that is non-empty
    expected_future = ["budu foobar", "budeš foobar", "bude foobar", "budeme foobar", "budete foobar", "budou foobar"] # future tense
    b = v.Verb("foobar", "bar")
    b.conjugate(v.Tense.FUTURE)
    for person in range(v.Person.NUM_PERSON):
        assert expected_future[person] == b.get_conjugation_at(v.Tense.FUTURE, person)

def test_conjugate_imperative():
     # should have the right auxillaries
    a = v.Verb()
    a.conjugate(v.Tense.IMPERATIVE)
    expected_imperative = ["", " ", "", "me ", "te ", ""] # imperative mood
    for person in range(v.Person.NUM_PERSON):
        assert expected_imperative[person] == a.get_conjugation_at(v.Tense.IMPERATIVE, person)


    # should all still be empty-ish
    b = v.Verb("foobar", "bar")
    b.conjugate(v.Tense.IMPERATIVE)
    for person in range(v.Person.NUM_PERSON):
        assert expected_imperative[person] == b.get_conjugation_at(v.Tense.IMPERATIVE, person)

def test_conjugate_conditional():
    # should have the right auxillaries
    expected_conditional = ["/a bych", "/a bys", "/a/o by", "i/y bychom", "i/y byste", "i/y/a by"]
    a = v.Verb()
    a.conjugate(v.Tense.CONDITIONAL)
    for person in range(v.Person.NUM_PERSON):
        assert expected_conditional[person] == a.get_conjugation_at(v.Tense.CONDITIONAL, person)


    # should all still be empty-ish
    b = v.Verb("foobar", "bar")
    b.conjugate(v.Tense.CONDITIONAL)
    for person in range(v.Person.NUM_PERSON):
        assert expected_conditional[person] == b.get_conjugation_at(v.Tense.CONDITIONAL, person)


# test conjugations across all persons (and i guess tests that other entries remain empty)
def test_conjugate_first_person_singular():
    # expected conjugations
    # indices (0-4): present, past, future, imperative, conditional
    person = v.Person.FIRST_SG
    expected_conjugations = [" ", "/a jsem", "budu ", "", "/a bych"]

    a = v.Verb()
    a.conjugate(person_idx = person)
    for tense in range(v.Tense.NUM_TENSE):
        assert expected_conjugations[tense] == a.get_conjugation_at(tense, person)

    b = v.Verb("foobar", "bar")
    expected_conjugations = [" ", "/a jsem", "budu foobar", "", "/a bych"]
    b.conjugate(person_idx = person)
    for tense in range(v.Tense.NUM_TENSE):
        assert expected_conjugations[tense] == b.get_conjugation_at(tense, person)

def test_conjugate_second_person_singular():
    # expected conjugations
    # indices (0-4): present, past, future, imperative, conditional
    person = v.Person.SECOND_SG
    expected_conjugations = [" ", "/a jsi/jseš", "budeš ", " ", "/a bys"]

    a = v.Verb()
    a.conjugate(person_idx = person)
    for tense in range(v.Tense.NUM_TENSE):
        assert expected_conjugations[tense] == a.get_conjugation_at(tense, person)

    b = v.Verb("foobar", "bar")
    expected_conjugations = [" ", "/a jsi/jseš", "budeš foobar", " ", "/a bys"]
    b.conjugate(person_idx = person)
    for tense in range(v.Tense.NUM_TENSE):
        assert expected_conjugations[tense] == b.get_conjugation_at(tense, person)

def test_conjugate_third_person_singular():
    # expected conjugations
    # indices (0-4): present, past, future, imperative, conditional
    person = v.Person.THIRD_SG
    expected_conjugations = [" ", "/a/o ", "bude ", "", "/a/o by"]

    a = v.Verb()
    a.conjugate(person_idx = person)
    for tense in range(v.Tense.NUM_TENSE):
        assert expected_conjugations[tense] == a.get_conjugation_at(tense, person)

    b = v.Verb("foobar", "bar")
    expected_conjugations = [" ", "/a/o ", "bude foobar", "", "/a/o by"]
    b.conjugate(person_idx = person)
    for tense in range(v.Tense.NUM_TENSE):
        assert expected_conjugations[tense] == b.get_conjugation_at(tense, person)

def test_conjugate_first_person_plural():
    # expected conjugations
    # indices (0-4): present, past, future, imperative, conditional
    person = v.Person.FIRST_PL
    expected_conjugations = [" ", "i/y jsme", "budeme ", "me ", "i/y bychom"]

    a = v.Verb()
    a.conjugate(person_idx = person)
    for tense in range(v.Tense.NUM_TENSE):
        assert expected_conjugations[tense] == a.get_conjugation_at(tense, person)

    b = v.Verb("foobar", "bar")
    expected_conjugations = [" ", "i/y jsme", "budeme foobar", "me ", "i/y bychom"]
    b.conjugate(person_idx = person)
    for tense in range(v.Tense.NUM_TENSE):
        assert expected_conjugations[tense] == b.get_conjugation_at(tense, person)

def test_conjugate_second_person_plural():
    # expected conjugations
    # indices (0-4): present, past, future, imperative, conditional
    person = v.Person.SECOND_PL
    expected_conjugations = [" ", "i/y jste", "budete ", "te ", "i/y byste"]

    a = v.Verb()
    a.conjugate(person_idx = person)
    for tense in range(v.Tense.NUM_TENSE):
        assert expected_conjugations[tense] == a.get_conjugation_at(tense, person)

    b = v.Verb("foobar", "bar")
    expected_conjugations = [" ", "i/y jste", "budete foobar", "te ", "i/y byste"]
    b.conjugate(person_idx = person)
    for tense in range(v.Tense.NUM_TENSE):
        assert expected_conjugations[tense] == b.get_conjugation_at(tense, person)

def test_conjugate_third_person_plural():
    # expected conjugations
    # indices (0-4): present, past, future, imperative, conditional
    person = v.Person.THIRD_PL
    expected_conjugations = [" ", "i/y/a ", "budou ", "", "i/y/a by"]

    a = v.Verb()
    a.conjugate(person_idx = person)
    for tense in range(v.Tense.NUM_TENSE):
        assert expected_conjugations[tense] == a.get_conjugation_at(tense, person)

    b = v.Verb("foobar", "bar")
    expected_conjugations = [" ", "i/y/a ", "budou foobar", "", "i/y/a by"]
    b.conjugate(person_idx = person)
    for tense in range(v.Tense.NUM_TENSE):
        assert expected_conjugations[tense] == b.get_conjugation_at(tense, person)

# test all conjugations at once
def test_conjugate_all():

    # expected conjugations
    # indices (0-4): present, past, future, imperative, conditional
    expected_conjugations = []
    expected_present= [" ", " ", " ", " ", " ", " "] # present tense is class dependent
    expected_past = ["/a jsem", "/a jsi/jseš", "/a/o ", "i/y jsme", "i/y jste", "i/y/a "] # past tense
    expected_future = ["budu ", "budeš ", "bude ", "budeme ", "budete ", "budou "] # future tense
    expected_imperative = ["", " ", "", "me ", "te ", ""] # imperative mood
    expected_conditional = ["/a bych", "/a bys", "/a/o by", "i/y bychom", "i/y byste", "i/y/a by"] # (present) conditional mood

    # indices (0-4): present, past, future, imperative, conditional
    expected_conjugations = [expected_present, expected_past, expected_future, expected_imperative, expected_conditional]

    # conjugate everything
    a = v.Verb()
    a.conjugate() 
    for tense in range(v.Tense.NUM_TENSE):
        for person in range(v.Person.NUM_PERSON):
            assert expected_conjugations[tense][person] == a.get_conjugation_at(tense, person)

    # now for a verb with an actual infinitive
    b = v.Verb("foobar", "bar")
    expected_future = ["budu foobar", "budeš foobar", "bude foobar", "budeme foobar", "budete foobar", "budou foobar"]
    expected_conjugations = [expected_present, expected_past, expected_future, expected_imperative, expected_conditional]
    b.conjugate()
    for tense in range(v.Tense.NUM_TENSE):
        for person in range(v.Person.NUM_PERSON):
            assert expected_conjugations[tense][person] == b.get_conjugation_at(tense, person)

# test clear for one tense (future)
def test_conjugate_table_clear():
    tense = v.Tense.FUTURE
    a = v.Verb()
    a.conjugate()
    for person in range(v.Person.NUM_PERSON):
        assert a.get_conjugation_at(tense, person) != ""

    a.clear_table()
    for person in range(v.Person.NUM_PERSON):
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
    expected_past = ["byl/a jsem", "byl/a jsi/jseš", "byl/a/o ", "byli/y jsme", "byli/y jste", "byli/y/a "]
    expected_future = ["budu ", "budeš ", "bude ", "budeme ", "budete ", "budou "]
    expected_imperative = ["", "buď ", "", "buďme ", "buďte ", ""]
    expected_conditional = ["byl/a bych", "byl/a bys", "byl/a/o by", "byli/y bychom", "byli/y byste", "byli/y/a by"]

    # indices (0-4): present, past, future, imperative, conditional
    expected_conjugations = [expected_present, expected_past, expected_future, expected_imperative, expected_conditional]

    byt.conjugate()
    for tense in range(v.Tense.NUM_TENSE):
        for person in range(v.Person.NUM_PERSON):
            assert expected_conjugations[tense][person] == byt.get_conjugation_at(tense, person)

def test_nebyt_conjugate():
    nebyt = v.Byt("nebýt")
    # expected conjugations
    # indices (0-4): present, past, future, imperative, conditional
    expected_conjugations = []
    expected_present= ["nejsem", "nejseš/jsi", "není", "nejsme", "nejste", "nejsou"]
    expected_past = ["nebyl/a jsem", "nebyl/a jsi/jseš", "nebyl/a/o ", "nebyli/y jsme", "nebyli/y jste", "nebyli/y/a "]
    expected_future = ["nebudu ", "nebudeš ", "nebude ", "nebudeme ", "nebudete ", "nebudou "]
    expected_imperative = ["", "nebuď ", "", "nebuďme ", "nebuďte ", ""]
    expected_conditional = ["nebyl/a bych", "nebyl/a bys", "nebyl/a/o by", "nebyli/y bychom", "nebyli/y byste", "nebyli/y/a by"]

    # indices (0-4): present, past, future, imperative, conditional
    expected_conjugations = [expected_present, expected_past, expected_future, expected_imperative, expected_conditional]

    nebyt.conjugate()
    for tense in range(v.Tense.NUM_TENSE):
        for person in range(v.Person.NUM_PERSON):
            assert expected_conjugations[tense][person] == nebyt.get_conjugation_at(tense, person)



