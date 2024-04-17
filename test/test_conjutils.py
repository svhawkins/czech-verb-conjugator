# tests conjugation utilities (mainly verb class determination)

import pytest
import conjugator_utils as conjutils



#### FILE DATA TESTS ####
# tests that get_irregular_verbs functions properly by examining contents of the 1st, 10th, 30th, and 75th lines. 
def test_get_irregular_verbs():
    # infinitive, class, stem, past stem, imperative stem, passive stem?, transgressive stem?
    irregular_verbs = conjutils.get_irregular_verbs()

    indices = [13, 17, 32, 43]
    expected  = [("jít", 4, "jd", "šel", "pojď"),
                ("spát", 3, "sp", "spal", "spi"),
                ("mít", 1, "m", "měl", "měj"),
                ("vzít", 4, "vezm", "vzal", "vezmi")]
    for idx in range(len(indices)):
        for irregularIdx in range(len(conjutils.IrregularIdx)):
            assert expected[idx][irregularIdx] == irregular_verbs[indices[idx]][irregularIdx]

# tests that the regex search works for find irregular verb
def test_find_verb_matches():
    irregular_verbs = conjutils.get_irregular_verbs()

    # st[áa]t		4		stan		stal		staň
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

# tests that prefixes are retrieved correctly
def test_get_prefixes():
    expected = "^((beze?)|(d[oů])|(nade?)|(n[aá])|(ne)|"
    expected += "(ode?)|(ob?e?)|(pode?)|(přede?)|(p[oů])|(pře)|"
    expected += "(př[ií])|(pr[oů])|(roze?)|(spolu)|(sou)|(se?)|([uú])|"
    expected += "(v[yý])|(vze?)|(ve?)|(z[aá])|(zne)|(znovu)|(ze?))"
    prefixes = conjutils.get_prefixes()
    assert expected == prefixes

# tests that prefixes are able to be extracted from provided words
def test_get_prefix():
    prefixes = conjutils.get_prefixes()

    # no prefixes
    word = "ledne"
    (not_root, root) = conjutils.get_prefix(word, prefixes)
    assert not_root == ""
    assert root == "ledne"

    # all prefixes
    word = "nenenenavydopo"
    (not_root, root) = conjutils.get_prefix(word, prefixes)
    assert not_root == "nenenenavydopo"
    assert root == ""

    # some prefixes
    word = "nenenenavydopoledne"
    (not_root, root) = conjutils.get_prefix(word, prefixes)
    assert not_root == "nenenenavydopo"
    assert root == "ledne"

    # prefixes that are seperate are part of the root.
    word = "nedalekohledpo"
    (not_root, root) = conjutils.get_prefix(word, prefixes)
    assert not_root == "ne"
    assert root == "dalekohledpo"
 

 #### VERB CLASSIFICAITON TESTS ####
def test_at_class1_classification():
    infinitives = ["lat", "kat", "plat", "vat", "smat", "hrat", "hřat", "sat", "tat",
                   "kázát", "mazát", 
                   #"klamát", # FIXME: this is being confused for class2 due to m. class2 only triggered with MONOSYLLABIC
                   "lapát", 
                   #"lámát", # FIXME: this is being confused for class2 due to m. class2 only triggered with MONOSYLLABIC
                   "chápát", "tápát", "ťapát",
                   #"chlámat", # FIXME: this is being confused for class2 due to m. class2 only triggered with MONOSYLLABIC 
                   "papat"
                   ]
    for i in range(len(infinitives)):
        a = conjutils.determine_verb_class(infinitives[i], infinitives[i])
        assert a.class_num == 1
        assert a.kind() == "Class1_at"

def test_at_class2_classification():
    # lát, kát, plát, vát, smát, hrát, hřát, sát, tát correctly classified
    # dát is class 1
    infinitives = ["lát", "kát", "plát", "vát", "smát", "hrát", "hřát", "sát", "tát"]
    for i in range(len(infinitives)):
        a = conjutils.determine_verb_class(infinitives[i], infinitives[i])
        assert a.class_num == 2
        assert a.kind() == "Class2_át"

    a = conjutils.determine_verb_class("dát", "dát")
    assert a.class_num != 2
    assert a.kind() != "Class2_át"

    a = conjutils.determine_verb_class("tat", "tat")
    assert a.class_num != 2
    assert a.kind() != "Class2_át"

def test_at_class4_classification():
    # apat, azat, etc. but not chlamat or papat
    infinitives = ["kázat", "mazat", "klamat", "lapat", "lámat", "chápat", "tápat", "ťapat"]
    for infinitive in infinitives:
        a = conjutils.determine_verb_class(infinitive, infinitive)
        assert a.class_num == 4
        assert a.kind() == "Class4_ápat"

    a = conjutils.determine_verb_class("chlámat", "chlámat")
    assert a.class_num != 4
    assert a.class_num == 1
    assert a.kind() != "Class4_ápat"
    assert a.kind() == "Class1_at"

    a = conjutils.determine_verb_class("papat", "papat")
    assert a.class_num != 4
    assert a.class_num == 1
    assert a.kind() != "Class4_ápat"
    assert a.kind() == "Class1_at"

def test_at_cluster_classification():
    infinitives = ["zvát", "brát", "prát", "drát", "srát", "štvát", "slát", "ržát", "řvát", "žrát", "lhát", "rvát", "stlát", "cpát"]
    for infinitive in infinitives:
        a = conjutils.determine_verb_class(infinitive, infinitive)
        assert a.class_num == 4
        assert a.kind() == "Class4_cluster"
    

def test_ityt_classification():
    infinitives = ["zedít", "skelít", "omdelít", "bzedít", "senít",
                   "telít", "skevít", "redít", "menít", "msetít",
                   "hřebít", "dšetít", "cetít", "čenít", "bedít",
                   "zedýt", "skelýt", "omdelýt", "bzedýt", "senýt",
                   "telýt", "skevýt", "redýt", "menýt", "msetýt", 
                   "hřebýt", "dšetýt", "cetýt", "čenýt", "bedýt", 
                   "zerýt","blít"]
    
    for infinitive in infinitives:
        a = conjutils.determine_verb_class(infinitive, infinitive)
        assert a.class_num == 2
        assert a.kind() == "Class2_ityt"

def test_ovat_classification():
    # chovat is not class2, but studovat is.
    a = conjutils.determine_verb_class("chovat", "chovat")
    assert a.class_num != 2
    assert a.kind() != "Class2_ovat"

    a = conjutils.determine_verb_class("studovat", "studovat")
    assert a.class_num == 2
    assert a.kind() == "Class2_ovat"

def test_ityt_cluster_classification():
    infinitives = ["zdít", "sklít", "omdlít", 
                   "bzdít", "snít", "tlít",
                   "skvít", "rdít", "mnít", "mstít",
                   "hřbít", "dštít", "ctít", "čnít", "bdít",
                   "zřít"
                  ]
    
    for infinitive in infinitives:
        a = conjutils.determine_verb_class(infinitive, infinitive)
        assert a.class_num == 3
        assert a.kind() == "Class3_cluster"

    # test with single consonant prefixes: s,z,v
    prefixes = ["v", "s", "z"]
    infinitives = ["lít"]
    for prefix in prefixes:
        for infinitive in infinitives:
            a = conjutils.determine_verb_class(prefix + infinitive, infinitive)
            assert a.class_num == 2
            assert a.kind() == "Class2_ityt"

def test_ityt_rit_classification():
    # zřít is class3, but zeřít is class4.
    a = conjutils.determine_verb_class("zřít", "zřít")
    assert a.class_num == 3
    assert a.kind() == "Class3_cluster"

    a = conjutils.determine_verb_class("zeřít", "zeřít")
    assert a.class_num == 4
    assert a.kind() == "Class4_řít"

def test_out_classification():
    # nout verbs are class4, out verbs are class2
    infinitives = ["zout", "plout", "dout", "slout", "kout", "obout"]
    for infinitive in infinitives:
        a = conjutils.determine_verb_class(infinitive, infinitive)
        assert a.class_num == 2
        assert a.kind() == "Class2_out"

    infinitives = ["zapomenout", "zhasnout", "buchnout"]
    for infinitive in infinitives:
        a = conjutils.determine_verb_class(infinitive, infinitive)
        assert a.class_num == 4
        assert a.kind() == "Class4_nout"

def test_itet_classification():

    infinitives = ["mručet", "skočit", "dunět", "chvět", "vyvíjet",
                   "vyrábět", "umět", "přenášet", "ztrácet", "dovádět",
                   "pouštět", "zkoušet", "prospět", "tvářet", "slzet",
                   "chýlit", "pálit", "blížit", "bouřit", "bránit",
                   "cítit", "hájit", "kamarádit", "podřídit", "půlit",
                    "rdousit", "sloučit", "tvářit", "úžit", "léčit",
                    "sílit", "shromáždit", "vřeštět", "ošetřit",
                    "brázdit", "ověnčit", "bruslit", "kreslit",
                    "běsnit", "hmoždit", "čpět", "patřit", "zhoršit",
                    "zlepšit", "rozluštit", "vrstvit", "rozmístit",
                    "různit", "sídlit", "svraštit", "šustit",
                    "tříštit", "ústit", "prýštit"
                  ]
    
    for infinitive in infinitives:
        a = conjutils.determine_verb_class(infinitive, infinitive)
        assert a.class_num == 3
        assert a.kind() == "Class3_itet"

def test_sczt_classifcation():
    # all require long vowels

    # st
    infinitives = ["bást", "bést", "bíst", "boust", "búst", "bůst", "býst"]
    for infinitive in infinitives:
        a = conjutils.determine_verb_class(infinitive, infinitive)
        assert a.class_num == 4
        assert a.kind() == "Class4_st"

    # zt
    infinitives = ["bázt", "bézt", "bízt", "bouzt", "búzt", "bůzt", "býzt"]
    for infinitive in infinitives:
        a = conjutils.determine_verb_class(infinitive, infinitive)
        assert a.class_num == 4
        assert a.kind() == "Class4_zt"

    # ct
    infinitives = ["báct", "béct", "bíct", "bouct", "búct", "bůct", "býct"]
    for infinitive in infinitives:
        a = conjutils.determine_verb_class(infinitive, infinitive)
        assert a.class_num == 4
        assert a.kind() == "Class4_ct"


def test_invalid_classification():
    # verify that the resulting verb is still None

    # no verbs end in ét, ůt, short vowels with st/ct/zt
    # hard consonants with soft vowels following and vice versa also bad
    bad_infinitives = [
        "bét", "bůt",
        "bact", "bect", "bict", "běct", "buct", "boct", "byct",
        "bazt", "bezt", "bizt", "bězt", "buzt", "bozt", "byzt",
        "bast", "best", "bist", "běst", "bust", "bost", "byst",
    ]
    for bad_infinitive in bad_infinitives:
        assert conjutils.determine_verb_class(bad_infinitive, bad_infinitive) == None

def test_disambiguate_verb():
    # tests that it (un)classifies verbs correctly
    infinitives = ["kovat", "abdikovat", "děkovat",
                    "dít", "bzdít", "bdít","rdít" , "zdít",
                    "být", "nebýt", "dobýt", "zbýt",
                    "stít", "mstít", "obelstít",
                    "ctít", "dštít", "chtít", "křtít", "tít",
                    "klít","mlít", "plít", "tklít", "sklít",
                    "sehnat", "hnát", "žehnat",
                    "bujet", "jet", "dojet", "pájet", "krájet",
                    "dostat", "chlastat", "zůstat", "stat", "trestat",
                    "dbát", "bát",
                    "čpět", "dospět", "lpět", "pět", "trpět", "úpět", "potápět",
                    "klát", "sklát",
                    "pnout", "čapnout", "zapnout", "drapnout",
                    "spát", "zát", "zábst", "zet", "odcházet"]
    
    classes = [-1, None, None,
               -1, None, None, None, None,
               -1, -1, -1, -1,
               -1, None, None,
               None, None, -1, None, -1,
               -1, -1, -1, None, None,
               -1, -1, None,
               None, -1, -1, None, None,
               -1, None, -1, -1, None,
               None, -1,
               None, -1, None, -1, None, None, None,
               -1, -1,
               -1, None, -1, None,
               -1, -1, -1, -1, None]

    irregular_verbs = conjutils.get_irregular_verbs()
    prefixes = conjutils.get_prefixes()
    for i in range(0, len(classes)):
        infinitive = infinitives[i]
        matches = conjutils.find_verb_matches(infinitive, irregular_verbs)
        (not_root, root) = conjutils.get_prefix(infinitive, prefixes)
        if (classes[i] == None):
            assert conjutils.disambiguate_verb(matches, infinitive, root)[0] == None
        else:
            assert conjutils.disambiguate_verb(matches, infinitive, root)[0] != None
