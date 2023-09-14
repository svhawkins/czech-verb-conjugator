# module containing the verb classes required to conjugate a czech verb
# the base class is Verb
# further subdivided into 4 classes: class1, class2, class3, and class4 and být (entirely irregular)
# there are other "irregular" verbs, but only their stems change and conjugate according to one of the 4 classes absolutely
# each of the classes have subclasses for the verbs that are regular based on ending where the stems are inferred from the infinitive and ending.
# class1 has 1 subclass, class2 with 2, class3 with 1, and class4 with 4.
# all classes and subclasses require 2 strings to construct: the given infinitive and its corresponding ending. if not given, it defaults to the empty string.


# TODO/FIXME: the conjugations actually have to be tested. store the forms as private members that are generated.
from prettytable import PrettyTable
import re
import verb_utils as vutils

# base class, contains code to construct the conjugation tables and non-present tenses and non-indicative moods
class Verb:
	_conjugation_headers = ["PERSON (OSOBA)", "SINGULAR (ČÍSLO JEDNOTNÉ)", "PLURAL (ČÍSLO MNOŽNÉ)"]
	_participle_note = ["NOTE: past participles must agree with both gender and number of the subject(s):"]
	_conditional_note = ["NOTE: conjugations of " + vutils.italics("by") +
					     " also apply to " + vutils.italics("aby") + " and " +
						 vutils.italics("kdyby")]
	_present_header = ["PRESENT TENSE (PŘÍTOMNÝ ČAS)"]
	_past_header = ["PAST TENSE (MINULÝ ČAS)"]
	_imperative_header = ["IMPERATIVE MOOD (ROZKAZOVÁCÍ ZPŮSOB)"]
	_conditional_header = ["CONDITIONAL MOOD (PODMIŇOVÁCÍ ZPŮSOB)"]
	def __init__(self, infinitive = "", ending = ""):
		self._infinitive = infinitive
		self._ending = ending
		self._stem = ""
		self._present_stem = ""
		self._past_stem = ""
		#self._passive_stem = ""
		self._imperative_stem = ""

	def kind(self):
		print("Verb")

	def stems(self):
		print("infinitive: ", self._infinitive)
		print("stem: ", self._stem)
		print("present stem: ", self._present_stem)
		#print("past stem: ", self._past_stem)
		#print("passive stem: ", self._passive_stem)
		print("imperative stem: ", self._imperative_stem)

	def set_stem(self, stem):
		self._stem = stem

	def set_present_stem(self, present_stem):
		self._present_stem = present_stem

	def set_past_stem(self, past_stem):
		self._past_stem = past_stem

	def set_imperative_stem(self, imperative_stem):
		self._imperative_stem = imperative_stem

	def present_stem(self):
		return self._present_stem

	def conjugate(self):
		self._conjugate_past()
		self._conjugate_imperative()
		self._conjugate_conditional()

	def _conjugate_participle(self):
		participle = PrettyTable(["GENDER (ROD)", "SINGULAR (ČÍSLO JEDNOTNÉ)", "PLURAL (ČÍSLO MNOŽNÉ)"])
		participle.add_row(["MASCULINE ANIMATE (ROD MUŽSKÝ ŽIVOTNÝ)", self._past_stem , self._past_stem + "i"])
		participle.add_row(["MASCULINE INANIMATE (ROD MUŽSKÝ NEŽIVOTNÝ)", self._past_stem, self._past_stem + "y"])
		participle.add_row(["FEMININE (ROD ŽENSKÝ)", self._past_stem + "a", self._past_stem + "y"])
		participle.add_row(["NEUTER (ROD STŘEDNÍ)", self._past_stem + "o", self._past_stem + "a"])
		return participle

	def _conjugate_past(self):
		participle = self._conjugate_participle()
		past_tense = PrettyTable(self._past_header)
		past_conjugation = PrettyTable(self._conjugation_headers)
		past_conjugation.add_row(["1.", self._past_stem + " jsem", self._past_stem + "i jsme"])
		past_conjugation.add_row(["2.", self._past_stem + " jsi/jseš", self._past_stem + "i jste"])
		past_conjugation.add_row(["3.", self._past_stem, self._past_stem + "i"])
		past_tense.add_row([past_conjugation])
		past_tense.add_row(self._participle_note)
		past_tense.add_row([participle])
		return past_tense

	def _conjugate_conditional(self):
		participle = self._conjugate_participle()
		conditional_mood = PrettyTable(self._conditional_header)
		conditional_conjugation = PrettyTable(self._conjugation_headers)
		conditional_conjugation.add_row(["1.", self._past_stem + " bych", self._past_stem +"i bychom/bysme"])
		conditional_conjugation.add_row(["2.", self._past_stem + " bys", self._past_stem + " byste"])
		conditional_conjugation.add_row(["3.", self._past_stem + " by", self._past_stem + " by"])
		conditional_mood.add_row(self._conditional_note)
		conditional_mood.add_row([conditional_conjugation])
		conditional_mood.add_row(self._participle_note)
		conditional_mood.add_row([participle])
		return conditional_mood

	def _conjugate_imperative(self):
		imperative_stem = self._imperative_stem if not vutils.isvowel(self._imperative_stem[-1]) else vutils.fix_spelling(self._imperative_stem[:-1] + "ě")
		imperative_mood = PrettyTable(self._imperative_header)
		imperative_conjugation = PrettyTable(self._conjugation_headers)
		imperative_conjugation.add_row(["1.", "-", imperative_stem + "me"])
		imperative_conjugation.add_row(["2.", self._imperative_stem, imperative_stem + "te"])
		imperative_conjugation.add_row(["3.", "-", "-"])
		imperative_mood.add_row([imperative_conjugation])
		return imperative_mood

# completely irregular, so has own class for itself
# only this verb has a future tense applied to it
class Byt(Verb):
	def __init__(self, infinitive, ending = ""):
		self._prefix = infinitive[:-len("být")]
		self._infinitive = infinitive
		self._ending = ""
		self._stem =  ""
		self._present_stem = ""
		self._past_stem = self._prefix + "byl"
		self._future_stem = self._prefix + "bud"
		self._imperative_stem = self._prefix + "buď"

	def kind(self):
		print("Irregular verb: ", self._infinitive)

	def _conjugate_present(self):
		sg3rd = "je" if not self._prefix else "není"
		present_tense = PrettyTable(self._present_header)
		present_conjugation =  PrettyTable(self._conjugation_headers)
		present_conjugation.add_row(["1.", self._prefix + "jsem", self._prefix + "jsme"])
		present_conjugation.add_row(["2.", self._prefix + "jsi/" + self._prefix + "jseš", self._prefix + "jste"])
		present_conjugation.add_row(["3.", sg3rd, self._prefix + "jsou"])
		present_tense.add_row([present_conjugation])
		return present_tense

	def _conjugate_future(self):
		future_tense = PrettyTable(["FUTURE TENSE (BUDOUCÍ ČAS)"])
		future_conjugation = PrettyTable(self._conjugation_headers)
		future_conjugation.add_row(["1.", self._future_stem + "u", self._future_stem + "eme"])
		future_conjugation.add_row(["2.", self._future_stem + "eš", self._future_stem + "ete"])
		future_conjugation.add_row(["3.", self._future_stem + "e", self._future_stem + "ou"])
		future_tense.add_row([future_conjugation])
		return future_tense

	def conjugate(self):
		print(self._conjugate_present())
		print(self._conjugate_future())
		print(Verb._conjugate_imperative(self))
		print(Verb._conjugate_past(self))
		print(Verb._conjugate_conditional(self))

### REGULAR VERBS BEGIN HERE ###
class Class1(Verb):
	def __init__(self, infinitive = "", ending = ""):
		Verb.__init__(self, infinitive, ending)

	def kind(self):
		print("Class I verb, conjugates according to -at/-át paradigm")

	def _conjugate_present(self):
		present_tense = PrettyTable(self._present_header)
		present_conjugation = PrettyTable(self._conjugation_headers)
		present_conjugation.add_row(["1.",  self._present_stem + "ám", self._present_stem + "áme"])
		present_conjugation.add_row(["2.", self._present_stem + "áš", self._present_stem + "áte"])
		present_conjugation.add_row(["3.", self._present_stem + "á", self._present_stem + "ají"])
		present_tense.add_row([present_conjugation])
		return present_tense

	def conjugate(self):
		print(self._conjugate_present())
		print(Verb._conjugate_imperative(self))
		print(Verb._conjugate_past(self))
		print(Verb._conjugate_conditional(self))

class Class1_at(Class1):
	def __init__(self, infinitive, ending):
		self._infinitive = infinitive
		self._ending = ending
		self._stem = infinitive[:-len(ending)]
		self._present_stem = self._stem
		self._past_stem = self._stem + "al"
		#self._passive_stem = self._stem + "án"
		self._imperative_stem = self._stem + "ej"

	def kind(self):
		print("Class I verb subclass, specific to regular -at/-át verbs")

class Class2(Verb):
	def __init__(self, infinitive = "", ending = ""):
		Verb.__init__(self, infinitive, ending)

	def kind(self):
		print("Class II verb, conjugates according to -ít/-ýt/-ovat paradigm")

	def _conjugate_present(self):
		plural_third = self._present_stem[:-1] + "tějí" if re.search("chtít$", self._infinitive) else self._present_stem + "í"
		singular_first = self._present_stem + "i"

		# TODO: add function in vutils for contains_stem
		if not re.search("chtít$", self._infinitive):
			singular_first += "/" + self._present_stem + "u"
		present_tense = PrettyTable(self._present_header)
		present_conjugation = PrettyTable(self._conjugation_headers)
		present_conjugation.add_row(["1.", singular_first, self._present_stem + "eme"])
		present_conjugation.add_row(["2.", self._present_stem + "eš", self._present_stem + "ete"])
		present_conjugation.add_row(["3.", self._present_stem + "e", plural_third])
		present_tense.add_row([present_conjugation])
		return present_tense

	def conjugate(self):
		print(self._conjugate_present())
		print(Verb._conjugate_imperative(self))
		print(Verb._conjugate_past(self))
		print(Verb._conjugate_conditional(self))

class Class2_ityt(Class2):
	def __init__(self, infinitive, ending):
		_thematic_vowel = "i" if ending.startswith("í") else "y"
		self._infinitive = infinitive
		self._ending = ending
		self._stem = infinitive[:-len(ending)]
		self._present_stem = self._stem + _thematic_vowel + "j"
		self._past_stem = self._stem + _thematic_vowel + "l"
		#self._passive_stem = self._stem + _thematic_vowel + "t"
		self._imperative_stem = self._present_stem

	def kind(self):
		print("Class II verb subclass, specific to -ít/-ýt verbs")

class Class2_ovat(Class2):
	def __init__(self, infinitive, ending):
		self._infinitive = infinitive
		self._ending = ending
		self._stem = infinitive[:-len(ending)]
		self._present_stem = self._stem + "uj"
		self._past_stem = self._stem + "oval"
		#self._passive_stem = self._stem + "ován"
		self._imperative_stem = self._present_stem

	def kind(self):
		print("Class II verb subclass, specific to -ovat verbs")

class Class3(Verb):
	def __init__(self, infinitive = "", ending = ""):
		Verb.__init__(self, infinitive, ending)

	def kind(self):
		print("Class III verb, conjugates according to -it/et/-ět paradigm")

	def _conjugate_present(self):
		# TODO: move the regex to vutils, contains_stem()
		plural_third_ending = "ědí" if re.search("jíst$|sníst$|vědět$", self._infinitive) else "í"
		plural_third = self._present_stem + plural_third_ending
		present_tense = PrettyTable(self._present_header)
		present_conjugation = PrettyTable(self._conjugation_headers)
		present_conjugation.add_row(["1.", self._present_stem + "ím", self._present_stem + "íme"])
		present_conjugation.add_row(["2.", self._present_stem + "íš", self._present_stem + "íte"])
		present_conjugation.add_row(["3.", self._present_stem + "í", plural_third])
		present_tense.add_row([present_conjugation])
		return present_tense

	def conjugate(self):
		print(self._conjugate_present())
		print(Verb._conjugate_imperative(self))
		print(Verb._conjugate_past(self))
		print(Verb._conjugate_conditional(self))

class Class3_itet(Class3):
	def __init__(self, infinitive, ending):
		_thematic_vowel = ending[0]
		self._infinitive = infinitive
		self._ending = ending
		self._stem = vutils.soften(infinitive[:-len(ending)])
		self._present_stem = vutils.harden(self._stem)
		self._past_stem = self._present_stem + _thematic_vowel + "l"

		consonants = "(" + vutils.consonant + "{1}|" + vutils.digraph + "){1}" # polygraphs/multigraphs though single phonemes

		# long vowels and non-clusters have j added to imperative with thematic vowel
		# TODO: move the regex to vutils, you can define the regex strings here, contains_stem()
		if re.search(vutils.long_vowel + consonants + "[eě]t$", self._infinitive) or re.search("ou" + consonants + "[eě]t$", self._infinitive):
			self._imperative_stem = self._present_stem + _thematic_vowel + "j"
		# ditto with (some) neutral consonants
		elif re.search("[bmvs]ět$", self._infinitive) or re.search("víjet$", self._infinitive):
			self._imperative_stem  = self._present_stem + _thematic_vowel + "j"
		# long vowels, non clusters and SHORT thematic vowel has the root vowel shortened
		elif x := re.findall(vutils.long_vowel + vutils.consonant + "{1}it$", self._infinitive) or re.findall("ou" + vutils.consonant + "{1}it$", self._infinitive):
			# 1. check if the verb matches the above pattern
			# 2. isolate the contained long vowel
			# 3. replace long vowel with its shortened in the original stem
			y = re.findall(vutils.long_vowel, x[0]) or re.findall("ou", x[0])
			self._imperative_stem = re.sub(y[0], vutils.get_short_vowel(y[0]), self._stem)

		# fixing imperative stem if digraph
		elif x := re.findall(vutils.digraph + "$", self._infinitive[:-2]):
			self._imperative_stem = self._present_stem
		else:
			self._imperative_stem = self._stem

		# non-cluster stems are softened, otherwise add i
		if x := re.findall("[^aeiouyrlě]{2}", self._imperative_stem[-2:]):
			if y := re.findall(vutils.digraph, x[0]) and not re.search("[ei]", self._imperative_stem[-3]):
				self._imperative_stem = vutils.soften(self._imperative_stem)
			else:
				self._imperative_stem = vutils.harden(self._imperative_stem) + "i"


		#self._passive_stem = self._stem[:-1] if _thematic_vowel == "i" else (self._stem + _thematic_vowel + "n")
		#if _thematic_vowel == "i":
		#	match self._stem[-1]:
		#		case "ť":
		#			self._passive_stem += "cen"
		#		case "ď":
		#			self._passive_stem += "děn"
		#		case "ň":
		#			self._passive_stem += "něn"
		#		case _:
		#			self._passive_stem += self._present_stem[-1] + "en"

	def kind(self):
		print("Class III subclass, specific to regular -it/-et/-ět verbs")

class Class4(Verb):
	def __init__(self, infinitive = "", ending = ""):
		Verb.__init__(self, infinitive, ending)

	def kind(self):
		print("Class IV verb, conjugates according to -nout/-st/-ct/-zt paradigm")

	def _conjugate_present(self):
		present_tense = PrettyTable(self._present_header)
		present_conjugation = PrettyTable(self._conjugation_headers)
		present_conjugation.add_row(["1.", self._present_stem + "u", self._present_stem + "eme"])
		present_conjugation.add_row(["2.", self._present_stem + "eš", self._present_stem + "ete"])
		present_conjugation.add_row(["3.", self._present_stem + "e", self._present_stem + "ou"])
		present_tense.add_row([present_conjugation])
		return present_tense

	def conjugate(self):
		print(self._conjugate_present())
		print(Verb._conjugate_imperative(self))
		print(Verb._conjugate_past(self))
		print(Verb._conjugate_conditional(self))

class Class4_nout(Class4):
	def __init__(self, infinitive, ending):
		self._infinitive = infinitive
		self._ending = ending
		self._stem = infinitive[:-len(ending)]
		self._present_stem = self._stem + "n"
		self._imperative_stem = self._stem + "ň" if vutils.isvowel(self._stem[-1]) else self._stem + "ni"
		self._past_stem = self._stem
		if vutils.isvowel(self._past_stem[0]) or  not vutils.contains_vowel(self._past_stem[:-len(self._ending)]):
			self._past_stem += "nul"
		else:
			self._past_stem += "l"
		#self._passive_stem = self._stem + "nut"

		#self._past_stem_variant = self._stem[:-1] + "něl"
		#self._passive_stem_variant = self._stem[:-1] + "něn"

	def kind(self):
		print("Class IV verb subclass, specific for -nout verbs")

	def stems(self):
		Verb.stems(self)
		#print("past stem variant: ", self._past_stem_variant)
		#print("passive stem variant: ", self._passive_stem_variant)

class Class4_st(Class4):
	def __init__(self, infinitive, ending):
		self._infinitive = infinitive
		self._ending = ending
		self._stem = vutils.shorten(infinitive[:-len(ending)])
		self._present_stem = self._stem + "d"
		self._past_stem = self._present_stem + "l"
		#self._passive_stem = self._present_stem + "en"
		self._imperative_stem = vutils.soften(self._present_stem)

	def kind(self):
		print("Class IV verb subclass, specific for -st verbs")

class Class4_zt(Class4):
	def __init__(self, infinitive, ending):
		self._infinitive = infinitive
		self._ending = ending
		self._stem = vutils.shorten(infinitive[:len(ending)])
		self._present_stem = self._stem + "z"
		self._past_stem = self._present_stem + "l"
		#self._passive_stem = self._present_stem + "en"
		self._imperative_stem = self._present_stem

	def kind(self):
		print("Class IV verb subclass, specific to -zt verbs")

class Class4_ct(Class4):
	def __init__(self, infinitive, ending):
		self._infinitive = infinitive
		self._ending = ending
		self._stem = vutils.shorten(infinitive[:-len(ending)])
		self._present_stem = self._stem + "č"
		self._past_stem = self._stem + "kl"
		#self._passive_stem = self._present_stem + "en"
		self._imperative_stem = self._present_stem

	def kind(self):
		print("Class IV verb subclass, specific to -ct verbs")
