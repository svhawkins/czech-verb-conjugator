# tests complete verb conjugations : from conjutils to vutils
import pytest
import conjugator_utils as conjutils
import verbs as v
import re
import copy

# also used in every test
def conjugate_verb(verb_in : v.Verb) -> tuple:
    irregular_verbs = conjutils.get_irregular_verbs()
    prefixes = conjutils.get_prefixes()
    concrete_verbs = conjutils.get_concrete_verbs()
    matches = conjutils.find_verb_matches(verb_in, irregular_verbs)
    is_concrete = conjutils.is_concrete_verb(verb_in, concrete_verbs)
    (not_root, root) = conjutils.get_prefix(verb_in, prefixes)
    (verb, verb2) = (None, None)
    if matches != []:
        (verb, verb2) = conjutils.disambiguate_verb(matches, verb_in, root, is_concrete)
    if not verb:
        verb = conjutils.determine_verb_class(verb_in, root, is_concrete)
    if verb:
        verb.conjugate() 
        if verb2 is not None:
            verb2.conjugate()
    return (verb, verb2)


####### TESTS BEGIN #######

# tests unamibguous irregular verb conjugations
def test_irregular_conjugation_no_disambiguate():
    verbs = ["moct", "říct", "dít"]
    expected_conjugations = [ [] for verb in verbs]
    expected_conjugations[0] = [["můžu", "můžeš", "může", "můžeme", "můžete", "můžou"], # present
                            ["mohl/a jsem", "mohl/a jsi/jseš", "mohl/a/o", "mohli/y jsme", "mohli/y jste", "mohli/y/a"], # past
                            ["budu moct", "budeš moct", "bude moct", "budeme moct", "budete moct", "budou moct"], # future
                            ["", "moz", "", "mozme", "mozte", ""], # imperative
                            ["mohl/a bych", "mohl/a bys", "mohl/a/o by", "mohli/y bychom", "mohli/y byste", "mohli/y/a by"], # conditional
                           ]
    expected_conjugations[1] = [["řeknu", "řekneš", "řekne", "řekneme", "řeknete", "řeknou"], # present
                        ["řekl/a jsem", "řekl/a jsi/jseš", "řekl/a/o", "řekli/y jsme", "řekli/y jste", "řekli/y/a"], # past
                        ["budu říct", "budeš říct", "bude říct", "budeme říct", "budete říct", "budou říct"], # future
                        ["", "řekni", "", "řekněme", "řekněte", ""], # imperative
                        ["řekl/a bych", "řekl/a bys", "řekl/a/o by", "řekli/y bychom", "řekli/y byste", "řekli/y/a by"], # conditional
                        ]
    expected_conjugations[2] = [["ději/u", "děješ", "děje", "dějeme", "dějete", "dějí"], # present
                            ["děl/a jsem", "děl/a jsi/jseš", "děl/a/o", "děli/y jsme", "děli/y jste", "děli/y/a"], # past
                            ["budu dít", "budeš dít", "bude dít", "budeme dít", "budete dít", "budou dít"], # future
                            ["", "děj", "", "dějme", "dějte", ""], # imperative
                            ["děl/a bych", "děl/a bys", "děl/a/o by", "děli/y bychom", "děli/y byste", "děli/y/a by"], # conditional
                            ]
    
    for i in range(len(verbs)):
        (verb, verb2) = conjugate_verb(verbs[i])
        assert verb.get_table() == expected_conjugations[i]



# test ambiguous irregular verb conjugations
def test_irregular_conjugation_yes_disambiguate():
    verbs = ["skákat", "zbýt", "vzít"]
    expected_conjugations = [ [] for verb in verbs]
    expected_conjugations[0] = [["skáču", "skáčeš", "skáče", "skáčeme", "skáčete", "skáčou"], # present
                            ["skákal/a jsem", "skákal/a jsi/jseš", "skákal/a/o", "skákali/y jsme", "skákali/y jste", "skákali/y/a"], # past
                            ["budu skákat", "budeš skákat", "bude skákat", "budeme skákat", "budete skákat", "budou skákat"], # future
                            ["", "skákej", "", "skákejme", "skákejte", ""], # imperative
                            ["skákal/a bych", "skákal/a bys", "skákal/a/o by", "skákali/y bychom", "skákali/y byste", "skákali/y/a by"], # conditional
                            ]
    expected_conjugations[1] = [["zbudu", "zbudeš", "zbude", "zbudeme", "zbudete", "zbudou"], # present
                        ["zbyl/a jsem", "zbyl/a jsi/jseš", "zbyl/a/o", "zbyli/y jsme", "zbyli/y jste", "zbyli/y/a"], # past
                        ["budu zbýt", "budeš zbýt", "bude zbýt", "budeme zbýt", "budete zbýt", "budou zbýt"], # future
                        ["", "zbuď", "", "zbuďme", "zbuďte", ""], # imperative
                        ["zbyl/a bych", "zbyl/a bys", "zbyl/a/o by", "zbyli/y bychom", "zbyli/y byste", "zbyli/y/a by"], # conditional
                        ]
    expected_conjugations[2] = [["vezmu", "vezmeš", "vezme", "vezmeme", "vezmete", "vezmou"], # present
                            ["vzal/a jsem", "vzal/a jsi/jseš", "vzal/a/o", "vzali/y jsme", "vzali/y jste", "vzali/y/a"], # past
                            ["budu vzít", "budeš vzít", "bude vzít", "budeme vzít", "budete vzít", "budou vzít"], # future
                            ["", "vezmi", "", "vezměme", "vezměte", ""], # imperative
                            ["vzal/a bych", "vzal/a bys", "vzal/a/o by", "vzali/y bychom", "vzali/y byste", "vzali/y/a by"], # conditional
                            ]

    for i in range(len(verbs)):
        (verb, verb2) = conjugate_verb(verbs[i])
        assert verb.get_table() == expected_conjugations[i]

# tests regular disambiguated verbs
def test_regular_conjugation_yes_disambiguate():
    verbs = ["chlastat", "dbát", "ctít"]
    expected_conjugations = [ [] for verb in verbs]
    expected_conjugations[0] = [["chlastám", "chlastáš", "chlastá", "chlastáme", "chlastáte", "chlastají"], # present
                            ["chlastal/a jsem", "chlastal/a jsi/jseš", "chlastal/a/o", "chlastali/y jsme", "chlastali/y jste", "chlastali/y/a"], # past
                            ["budu chlastat", "budeš chlastat", "bude chlastat", "budeme chlastat", "budete chlastat", "budou chlastat"], # future
                            ["", "chlastej", "", "chlastejme", "chlastejte", ""], # imperative
                            ["chlastal/a bych", "chlastal/a bys", "chlastal/a/o by", "chlastali/y bychom", "chlastali/y byste", "chlastali/y/a by"], # conditional
                           ]
    expected_conjugations[1] = [["dbám", "dbáš", "dbá", "dbáme", "dbáte", "dbají"], # present
                        ["dbal/a jsem", "dbal/a jsi/jseš", "dbal/a/o", "dbali/y jsme", "dbali/y jste", "dbali/y/a"], # past
                        ["budu dbát", "budeš dbát", "bude dbát", "budeme dbát", "budete dbát", "budou dbát"], # future
                        ["", "dbej", "", "dbejme", "dbejte", ""], # imperative
                        ["dbal/a bych", "dbal/a bys", "dbal/a/o by", "dbali/y bychom", "dbali/y byste", "dbali/y/a by"], # conditional
                        ]
    expected_conjugations[2] = [["ctím", "ctíš", "ctí", "ctíme", "ctíte", "ctí"], # present
                            ["ctil/a jsem", "ctil/a jsi/jseš", "ctil/a/o", "ctili/y jsme", "ctili/y jste", "ctili/y/a"], # past
                            ["budu ctít", "budeš ctít", "bude ctít", "budeme ctít", "budete ctít", "budou ctít"], # future
                            ["", "cti", "", "ctěme", "ctěte", ""], # imperative
                            ["ctil/a bych", "ctil/a bys", "ctil/a/o by", "ctili/y bychom", "ctili/y byste", "ctili/y/a by"], # conditional
                            ]
    
    for i in range(len(verbs)):
        (verb, verb2) = conjugate_verb(verbs[i])
        assert verb.get_table() == expected_conjugations[i]


# tests stát conjugation(s)
def test_stat_conjugation():

    # conjugations of stát
    stat1 = [["stanu", "staneš", "stane", "staneme", "stanete", "stanou"], # present
            ["stal/a jsem", "stal/a jsi/jseš", "stal/a/o", "stali/y jsme", "stali/y jste", "stali/y/a"], # past
            ["budu stát", "budeš stát", "bude stát", "budeme stát", "budete stát", "budou stát"], # future
            ["", "staň", "", "staňme", "staňte", ""], # imperative
            ["stal/a bych", "stal/a bys", "stal/a/o by", "stali/y bychom", "stali/y byste", "stali/y/a by"], # conditional
            ]
    stat2 = [["stojím", "stojíš", "stojí", "stojíme", "stojíte", "stojí"], # present
            ["stál/a jsem", "stál/a jsi/jseš", "stál/a/o", "stáli/y jsme", "stáli/y jste", "stáli/y/a"], # past
            ["budu stát", "budeš stát", "bude stát", "budeme stát", "budete stát", "budou stát"], # future
            ["", "stůj", "", "stůjme", "stůjte", ""], # imperative
            ["stál/a bych", "stál/a bys", "stál/a/o by", "stáli/y bychom", "stáli/y byste", "stáli/y/a by"] # conditional
            ]
    (verb, verb2) = conjugate_verb("stát")
    assert verb.get_table() == stat1
    assert verb2.get_table() == stat2

    # prefixed forms
    verbs = ["přistát", "přestat", "přistat", "ustat", "vstat", "vstát", "dostat",
             "postát", "obstát", "přestát", "ustát", "vystát", "dostát", "odstát"
            ]
    expected_conjugations = [stat1, stat1, stat1, stat1, stat1, stat1, stat1,
                             stat2, stat2, stat2, stat2, stat2, stat2, stat2
                            ]
    for i in range(len(verbs)):
        # update expected conjugation based on prefix
        expected_conjugation = copy.deepcopy(expected_conjugations[i])
        prefix = verbs[i][:-4]
        root = verbs[i][-4:]
        expected_conjugation[0] = [prefix + conjugation for conjugation in expected_conjugation[0]]
        expected_conjugation[1] = [prefix + conjugation for conjugation in expected_conjugation[1]]
        expected_conjugation[3] = ["", prefix + expected_conjugation[3][1], "",
                                   prefix + expected_conjugation[3][3], prefix + expected_conjugation[3][4], ""]
        expected_conjugation[4] = [prefix + conjugation for conjugation in expected_conjugation[4]]
        expected_conjugation[2] = [re.sub("(st[aá]t)$", prefix + root, conjugation) for conjugation in expected_conjugation[2]]


        (verb, verb2) = conjugate_verb(verbs[i])
        assert verb.get_table() == expected_conjugation

# tests concrete verb conjugations (future only)
def test_concrete_conjugation():
    verbs = ["jít", "jet", "nést", "vést", "vézt", "běžet", "letět", "hnát", "růst", "kvést", "lézt"]
    expected_conjugation = [ ["půjdu", "půjdeš", "půjde", "půjdeme", "půjdete", "půjdou"],
                             ["pojedu", "pojedeš", "pojede", "pojedeme", "pojedete", "pojedou"],
                             ["ponesu", "poneseš", "ponese", "poneseme", "ponesete", "ponesou"],
                             ["povedu", "povedeš", "povede", "povedeme", "povedete", "povedou"],
                             ["povezu", "povezeš", "poveze", "povezeme", "povezete", "povezou"],
                             ["poběžím", "poběžíš", "poběží", "poběžíme", "poběžíte", "poběží"],
                             ["poletím", "poletíš", "poletí", "poletíme", "poletíte", "poletí"],
                             ["poženu", "poženeš", "požene", "poženeme", "poženete", "poženou"],
                             ["porostu", "porosteš", "poroste", "porosteme", "porostete", "porostou"],
                             ["pokvetu", "pokveteš", "pokvete", "pokveteme", "pokvetete", "pokvetou"],
                             ["polezu", "polezeš", "poleze", "polezeme", "polezete", "polezou"]
                           ]
    for i in range(len(verbs)):
        (verb, verb2) = conjugate_verb(verbs[i])
        for person in range(len(v.Person)):
            assert verb.get_conjugation_at(v.Tense.FUTURE, person) == expected_conjugation[i][person]


# TODO:
# # tests perfective conjugations (future only)
# def test_perfective_conjugation():
#     assert True == True


# tests regular verb conjugations, one from each class.
def test_regular_conjugation():
    verbs = ["být", # Byt class
             "dělat", # class 1
             "sledovat", # class2_ovat
             "nechápat", # class4_apat
             "brát", # class4_cluster
             "kát",  # class2_at
             "otevřít", # class4_rit
             "snít", # class3_cluster
             "mýt", # class 2
             "zapomenout", # class4_nout
             "neplout", # class2_out
             "pocházet", # class 3
             "krást"] # class4_st
    
    expected_conjugations = [ [] for verb in verbs]
    expected_conjugations[0] = [["jsem", "jseš/jsi", "je", "jsme", "jste", "jsou"], # present
                            ["byl/a jsem", "byl/a jsi/jseš", "byl/a/o", "byli/y jsme", "byli/y jste", "byli/y/a"], # past
                            ["budu", "budeš", "bude", "budeme", "budete", "budou"], # future
                            ["", "buď", "", "buďme", "buďte", ""], # imperative
                            ["byl/a bych", "byl/a bys", "byl/a/o by", "byli/y bychom", "byli/y byste", "byli/y/a by"], # conditional
                           ]
    expected_conjugations[1] = [["dělám", "děláš", "dělá", "děláme", "děláte", "dělají"], # present
                        ["dělal/a jsem", "dělal/a jsi/jseš", "dělal/a/o", "dělali/y jsme", "dělali/y jste", "dělali/y/a"], # past
                        ["budu dělat", "budeš dělat", "bude dělat", "budeme dělat", "budete dělat", "budou dělat"], # future
                        ["", "dělej", "", "dělejme", "dělejte", ""], # imperative
                        ["dělal/a bych", "dělal/a bys", "dělal/a/o by", "dělali/y bychom", "dělali/y byste", "dělali/y/a by"], # conditional
                        ]
    expected_conjugations[2] = [["sleduji/u", "sleduješ", "sleduje", "sledujeme", "sledujete", "sledují"], # present
                            ["sledoval/a jsem", "sledoval/a jsi/jseš", "sledoval/a/o", "sledovali/y jsme", "sledovali/y jste", "sledovali/y/a"], # past
                            ["budu sledovat", "budeš sledovat", "bude sledovat", "budeme sledovat", "budete sledovat", "budou sledovat"], # future
                            ["", "sleduj", "", "sledujme", "sledujte", ""], # imperative
                            ["sledoval/a bych", "sledoval/a bys", "sledoval/a/o by", "sledovali/y bychom", "sledovali/y byste", "sledovali/y/a by"], # conditional
                           ]
    expected_conjugations[3] = [["nechápu", "nechápeš", "nechápe", "nechápeme", "nechápete", "nechápou"], # present
                        ["nechápal/a jsem", "nechápal/a jsi/jseš", "nechápal/a/o", "nechápali/y jsme", "nechápali/y jste", "nechápali/y/a"], # past
                        ["nebudu chápat", "nebudeš chápat", "nebude chápat", "nebudeme chápat", "nebudete chápat", "nebudou chápat"], # future
                        ["", "nechápej", "", "nechápejme", "nechápejte", ""], # imperative
                        ["nechápal/a bych", "nechápal/a bys", "nechápal/a/o by", "nechápali/y bychom", "nechápali/y byste", "nechápali/y/a by"], # conditional
                        ]
    expected_conjugations[4] = [["beru", "bereš", "bere", "bereme", "berete", "berou"], # present
                        ["bral/a jsem", "bral/a jsi/jseš", "bral/a/o", "brali/y jsme", "brali/y jste", "brali/y/a"], # past
                        ["budu brát", "budeš brát", "bude brát", "budeme brát", "budete brát", "budou brát"], # future
                        ["", "ber", "", "berme", "berte", ""], # imperative
                        ["bral/a bych", "bral/a bys", "bral/a/o by", "brali/y bychom", "brali/y byste", "brali/y/a by"], # conditional
                        ]
    expected_conjugations[5] = [["kaji/u", "kaješ", "kaje", "kajeme", "kajete", "kají"], # present
                        ["kál/a jsem", "kál/a jsi/jseš", "kál/a/o", "káli/y jsme", "káli/y jste", "káli/y/a"], # past
                        ["budu kát", "budeš kát", "bude kát", "budeme kát", "budete kát", "budou kát"], # future
                        ["", "kaj", "", "kajme", "kajte", ""], # imperative
                        ["kál/a bych", "kál/a bys", "kál/a/o by", "káli/y bychom", "káli/y byste", "káli/y/a by"], # conditional
                        ]
    expected_conjugations[6] = [["otevřu", "otevřeš", "otevře", "otevřeme", "otevřete", "otevřou"], # present
                        ["otevřel/a jsem", "otevřel/a jsi/jseš", "otevřel/a/o", "otevřeli/y jsme", "otevřeli/y jste", "otevřeli/y/a"], # past
                        ["budu otevřít", "budeš otevřít", "bude otevřít", "budeme otevřít", "budete otevřít", "budou otevřít"], # future
                        ["", "otevři", "", "otevřeme", "otevřete", ""], # imperative
                        ["otevřel/a bych", "otevřel/a bys", "otevřel/a/o by", "otevřeli/y bychom", "otevřeli/y byste", "otevřeli/y/a by"], # conditional
                        ]
    expected_conjugations[7] = [["sním", "sníš", "sní", "sníme", "sníte", "sní"], # present
                        ["snil/a jsem", "snil/a jsi/jseš", "snil/a/o", "snili/y jsme", "snili/y jste", "snili/y/a"], # past
                        ["budu snít", "budeš snít", "bude snít", "budeme snít", "budete snít", "budou snít"], # future
                        ["", "sni", "", "sněme", "sněte", ""], # imperative
                        ["snil/a bych", "snil/a bys", "snil/a/o by", "snili/y bychom", "snili/y byste", "snili/y/a by"], # conditional
                        ]
    expected_conjugations[8] = [["myji/u", "myješ", "myje", "myjeme", "myjete", "myjí"], # present
                        ["myl/a jsem", "myl/a jsi/jseš", "myl/a/o", "myli/y jsme", "myli/y jste", "myli/y/a"], # past
                        ["budu mýt", "budeš mýt", "bude mýt", "budeme mýt", "budete mýt", "budou mýt"], # future
                        ["", "myj", "", "myjme", "myjte", ""], # imperative
                        ["myl/a bych", "myl/a bys", "myl/a/o by", "myli/y bychom", "myli/y byste", "myli/y/a by"], # conditional
                        ]
    expected_conjugations[9] = [["zapomenu", "zapomeneš", "zapomene", "zapomeneme", "zapomenete", "zapomenou"], # present
                        ["zapomněl/a jsem", "zapomněl/a jsi/jseš", "zapomněl/a/o", "zapomněli/y jsme", "zapomněli/y jste", "zapomněli/y/a"], # past
                        ["budu zapomenout", "budeš zapomenout", "bude zapomenout", "budeme zapomenout", "budete zapomenout", "budou zapomenout"], # future
                        ["", "zapomeň", "", "zapomeňme", "zapomeňte", ""], # imperative
                        ["zapomněl/a bych", "zapomněl/a bys", "zapomněl/a/o by", "zapomněli/y bychom", "zapomněli/y byste", "zapomněli/y/a by"], # conditional
                        ]
    expected_conjugations[10] = [["nepluji/u", "nepluješ", "nepluje", "neplujeme", "neplujete", "neplují"], # present
                        ["neplul/a jsem", "neplul/a jsi/jseš", "neplul/a/o", "nepluli/y jsme", "nepluli/y jste", "nepluli/y/a"], # past
                        ["nebudu plout", "nebudeš plout", "nebude plout", "nebudeme plout", "nebudete plout", "nebudou plout"], # future
                        ["", "nepluj", "", "neplujme", "neplujte", ""], # imperative
                        ["neplul/a bych", "neplul/a bys", "neplul/a/o by", "nepluli/y bychom", "nepluli/y byste", "nepluli/y/a by"], # conditional
                        ]
    expected_conjugations[11] = [["pocházím", "pocházíš", "pochází", "pocházíme", "pocházíte", "pochází"], # present
                    ["pocházel/a jsem", "pocházel/a jsi/jseš", "pocházel/a/o", "pocházeli/y jsme", "pocházeli/y jste", "pocházeli/y/a"], # past
                    ["budu pocházet", "budeš pocházet", "bude pocházet", "budeme pocházet", "budete pocházet", "budou pocházet"], # future
                    ["", "pocházej", "", "pocházejme", "pocházejte", ""], # imperative
                    ["pocházel/a bych", "pocházel/a bys", "pocházel/a/o by", "pocházeli/y bychom", "pocházeli/y byste", "pocházeli/y/a by"], # conditional
                    ]
    expected_conjugations[12] = [["kradu", "kradeš", "krade", "krademe", "kradete", "kradou"], # present
                    ["kradl/a jsem", "kradl/a jsi/jseš", "kradl/a/o", "kradli/y jsme", "kradli/y jste", "kradli/y/a"], # past
                    ["budu krást", "budeš krást", "bude krást", "budeme krást", "budete krást", "budou krást"], # future
                    ["", "kraď", "", "kraďme", "kraďte", ""], # imperative
                    ["kradl/a bych", "kradl/a bys", "kradl/a/o by", "kradli/y bychom", "kradli/y byste", "kradli/y/a by"], # conditional
                    ]
    for i in range(len(verbs)):
        (verb, verb2) = conjugate_verb(verbs[i])
        assert verb.get_table() == expected_conjugations[i]