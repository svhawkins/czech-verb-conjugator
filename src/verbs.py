# module containing the verb classes to conjugate a czech verb
# the base class is Verb responsible for majority of the conjugations
# the derived classes do the present tense as well as set the necessary stems for the conjugations
# 5 derived classes: class1, class2, class3, class4, and (entirely irregular)
# each of these derived classes have subclasses for differing (though nonetheless the same endings):
# class1 has 1 subclass, class2 with 2, class3 with 1, and class4 with 4

# all verbs 2 strings during init: infinitive and ending
# optional flags can also be passed in: is_perfective (bool) , is_motion (tuple)


# TODO:
# 1. remove the pretty table elements entirely
		# requires refactoring all the verb classes

import src.verb_utils as vutils
#import verb_utils as vutils
import re
from enum import IntEnum

# enum classes for better (readable) array access that's not a dictionary.
class Tense(IntEnum): # includes MOOD AND VOICE AND OTHER PARTICIPLES AS WELL
	PRESENT = 0
	PAST = 1
	FUTURE = 2
	IMPERATIVE = 3
	CONDITIONAL = 4
	#PASSIVE = 5
	#PAST_CONDTIONAL = 6
	#NOUN = 7
	#TRANSGRESSIVE = 8
	#PAST_TRANSGRESSIVE = 9

class Person(IntEnum): # includes also NUMBER
	FIRST_SG = 0
	SECOND_SG = 1
	THIRD_SG = 2
	FIRST_PL = 3
	SECOND_PL = 4
	THIRD_PL = 5

# lambdas
is_none_value = lambda tense, person: (tense == Tense.IMPERATIVE and
										(person == Person.FIRST_SG or
			   							 person == Person.THIRD_SG or
										 person == Person.THIRD_PL ))
get_motion = lambda motion_tuple: (motion_tuple[0])
get_motion_prefix = lambda motion_tuple: (motion_tuple[1])


class Verb:
	# static/protected class members --> constant for ALL verbs pretty much unless aspect stuff appears

	# past participle endings: 1st singular, 2nd singular, 3rd singular, 1st plural, 2nd plural, 3rd plural
	_empty = ("", "", "", "", "", "")
	_participle_endings = ("/a", "/a", "/a/o", "i/y", "i/y", "i/y/a")
	_present_endings = ("", "", "", "", "", "")  # is made in derived classes
	_imperative_endings = ( None, "", None, "me", "te",  None ) # singular 2nd person only (just stem), plural 1st 2nd only

	# auxiliary verb endings
	_past_auxiliary = ("jsem", "jsi/jseš", "", "jsme", "jste", "")
	_future_auxiliary = ("budu", "budeš", "bude", "budeme", "budete", "budou")
	_conditional_auxiliary = ("bych", "bys", "by", "bychom", "byste", "by")
	_auxiliaries = ( _past_auxiliary, _future_auxiliary, _conditional_auxiliary )

	# tense to (auxiliary) ending mappings
	# present,past,future,imperative,conditional
	_tense_to_ending = [ _present_endings, _participle_endings, _empty, _imperative_endings, _participle_endings]
	_tense_to_auxiliary = [ _empty, _past_auxiliary, _future_auxiliary, _empty, _conditional_auxiliary]

	def __init__(self, infinitive = "", ending = "", is_perfective = False, is_motion = (False, "")):
		# stems (public)
		self.infinitive = infinitive
		self.ending = ending
		self.stem = ""
		self.present_stem = ""
		self.past_stem = ""
		self.imperative_stem = ""
		#self.passive_stem = ""
		#self.present_transgressive_stem = ""
		#self.past_transgressive_stem = ""

		# stems. make sure the 'future stem' does NOT contain the negation prefix ne-
		self._is_negative = False
		future_stem = self.infinitive
		if self.infinitive[:2] == "ne":
			future_stem = self.infinitive[2:]
			self._is_negative = True
		self._stems = [ self.present_stem, self.past_stem, future_stem, self.imperative_stem, self.past_stem ]

		self._is_perfective = is_perfective
		if is_perfective: # overrides default future conjugation
			# future tense will use present endings, and thus have an 'empty' auxiliary
			self._tense_to_ending[Tense.FUTURE] = self._present_endings
			self._tense_to_auxiliary[Tense.FUTURE] = self._empty
			self._tense_to_ending[Tense.PRESENT] = self._empty
		
		# usually verbs of motion take a future prefix instead an auxiliary
		# these are always imperfective, so the perfective future override need not apply.
		self._is_motion = is_motion
		if get_motion(self._is_motion):
			self._tense_to_auxiliary[Tense.FUTURE] = self._empty
			self._tense_to_ending[Tense.FUTURE] = self._present_endings

		# conjugation table
		self._conjugation_table = [["" for person in range(len(Person))] for tense in range(len(Tense))]

	def kind(self):
		'''displays verb conjugation class information'''
		print("Verb")

	def stems(self):
		'''Displays stem information'''
		print("infinitive: ", self.infinitive)
		print("stem: ", self.stem)
		print("present stem: ", self.present_stem)
		print("past stem: ", self.past_stem)
		print("imperative stem: ", self.imperative_stem)
		#print("passive stem :", self.passive_stem)
		#print("trangressive stem :" self.transgressive_stem)
		#print("past trasngressive stem: " self.past_transgressive_stem)
	
	def describe(self):
		'''Displays both kind and stem data'''
		self.kind(self)
		self.stems(self)

	def _get_conjugation(self, tense, person):
		'''returns a fully constructed conjugation for given tense and person indices'''
		auxiliary = (self._tense_to_auxiliary[tense])[person]
		ending = (self._tense_to_ending[tense])[person]
		conjugation = ""
		space = " " if auxiliary != "" else "" # so no space AFTER
		if not is_none_value(tense, person):
			# future tense: future auxiliary + infinitive if there is no override
			conjugation = self._stems[tense] + ending + space + auxiliary
			if tense == Tense.FUTURE and not self._is_perfective:
				space = "" if self._stems[tense] == "" else space # so no space AFTER
				conjugation = auxiliary + space + self._stems[tense] + ending
				if get_motion(self._is_motion):
					conjugation = get_motion_prefix(self._is_motion) + self._stems[tense] + ending
				if self._is_negative:
					conjugation = "ne" + conjugation
		return conjugation

	def conjugate(self, tense_idx = len(Tense), person_idx = len(Person)):
		'''Conjugates a verb according provided tense and person
		tense refers to any one of the integer constants defined in Tense
		person refers to any one of the integer constants defined in Person
		'''

		# TODO: don't do anything if out of enum range

		# set up ranges for given tense and person
		tense_range = range(tense_idx, tense_idx + 1) if tense_idx != len(Tense) else range(len(Tense))
		person_range = range(person_idx, person_idx + 1) if person_idx != len(Person) else range(len(Person))

		for tense in tense_range:
			for person in person_range:
				self._conjugation_table[tense][person] = self._get_conjugation(tense, person)

	def get_conjugation_at(self, tense_idx, person_idx):
		'''Returns A conjugation at specified indices'''

		# TODO: don't do anything if out of enum range (empty string??)
		return self._conjugation_table[tense_idx][person_idx]
	
	def clear_table(self):
		'''Clears the conjugation table'''
		for tense in range(len(Tense)):
			for person in range(len(Person)):
				self._conjugation_table[tense][person] = ""

	def get_table(self):
		'''Retrieves the conjugation table'''
		return self._conjugation_table

# completely irregular, so has own class for itself
# this covers ONLY the verb být and its negated form nebýt
class Byt(Verb):
	_present_endings = ("jsem", "jseš/jsi", "je", "jsme", "jste", "jsou")
	_endings = (_present_endings, Verb._participle_endings, Verb._imperative_endings )
	def __init__(self, infinitive, ending = "", is_perfective = False, is_motion = (False, "")):
		super().__init__(infinitive, ending, is_perfective, is_motion )
		self._prefix = infinitive[:-len("být")]
		self.infinitive = infinitive
		self.past_stem = self._prefix + "byl"
		self.imperative_stem = self._prefix + "buď"
		
		# update stems, future is empty since would be redundant to have bud- + být. Auxiliary is just future být!
		self._stems = [ self.present_stem, self.past_stem, "", self.imperative_stem, self.past_stem ]
		
		# update the endings for it to be to this class
		self._tense_to_auxiliary[Tense.PRESENT] = self._present_endings

	def kind(self):
		print("Irregular verb: ", self.infinitive)
	
	def conjugate(self, tense_idx = len(Tense), person_idx = len(Person)):
		super().conjugate(tense_idx, person_idx)

		# update the present tense with the present endings since there is no present stem
		negation_prefix = "ne" if self._is_negative == True else ""
		for person in range(len(Person)):
			ending = "ní" if self._is_negative and person == Person.THIRD_SG else self._present_endings[person]
			self._conjugation_table[Tense.PRESENT][person] = negation_prefix + ending

class Class1(Verb):
	# verb class specific endings:
	_present_endings = [ "ám", "áš", "á", "áme" ,"áte", "ají" ]

	# sanity check, was making past, present, and future tack on present být conjugations otherwise
	_tense_to_ending = [ _present_endings, Verb._participle_endings, Verb._empty, Verb._imperative_endings, Verb._participle_endings]
	_tense_to_auxiliary = [ Verb._empty, Verb._past_auxiliary, Verb._future_auxiliary, Verb._empty, Verb._conditional_auxiliary]
	def __init__(self, infinitive = "", ending = "", is_perfective = False, is_motion = (False, "")):
		super().__init__(infinitive, ending, is_perfective, is_motion)

		# update endings
		self._tense_to_ending[Tense.PRESENT] = self._present_endings

	def kind(self):
		print("Class I verb, conjugates according to -at/-át paradigm")

class Class1_at(Class1):
	def __init__(self, infinitive, ending, is_perfective = False, is_motion = (False, "")):
		super().__init__(infinitive, ending, is_perfective, is_motion)
		self.infinitive = infinitive
		self.ending = ending
		self.stem = infinitive[:-len(ending)]
		self.present_stem = self.stem
		self.past_stem = self.stem + "al"
		self.imperative_stem = self.stem + "ej"
		#self.passive_stem = self._stem + "án"

		# update stems
		future_stem = self.infinitive[2:] if self.infinitive[:2] == "ne" else self.infinitive
		self._stems = [self.present_stem, self.past_stem, future_stem, self.imperative_stem, self.past_stem ]

	def kind(self):
		print("Class I verb subclass, specific to regular -at/-át verbs")

# class Class2(Verb):
# 	# class specific endings
# 	_present_endings = ["i/u", "eš", "e", "eme", "ete", "í"]
# 	def __init__(self, infinitive = "", ending = ""):
# 		Verb.__init__(self, infinitive, ending)

# 	def kind(self):
# 		print("Class II verb, conjugates according to -ít/-ýt/-ovat paradigm")

# 	def _apply_chtit_correction(self, tense_idx, person_idx):
# 		if ((tense_idx == Tense.PRESENT or tense_idx == len(Tense))):
# 			if (person_idx == Person.FIRST_SG or person_idx == len(Person)):
# 				self._conjugation_table[Tense.PRESENT][Person.FIRST_SG] = "chci"
# 			if (person_idx == Person.THIRD_PL or person_idx == len(Person)):
# 				self._conjugation_table[Tense.PRESENT][Person.THIRD_PL] = "chtějí"
# 		return
		
# 	def conjugate(self, tense_idx, person_idx):
# 		# if verb is chtít, ALWAYS overwrite/correct it
# 		Verb.conjugate(self, tense_idx, person_idx)
# 		if re.search("chtít$", self.infinitive):
# 			self._apply_chtit_correction(self, tense_idx, person_idx)


# class Class2_ityt(Class2):
# 	def __init__(self, infinitive, ending):
# 		_thematic_vowel = "i" if ending.startswith("í") else "y"
# 		self.infinitive = infinitive
# 		self.ending = ending
# 		self.stem = infinitive[:-len(ending)]
# 		self.present_stem = self.stem + _thematic_vowel + "j"
# 		self.past_stem = self.stem + _thematic_vowel + "l"
# 		self.imperative_stem = self.present_stem
# 		#self.passive_stem = self.stem + _thematic_vowel + "t"

# 	def kind(self):
# 		print("Class II verb subclass, specific to -ít/-ýt verbs")

# class Class2_ovat(Class2):
# 	def __init__(self, infinitive, ending):
# 		self.infinitive = infinitive
# 		self.ending = ending
# 		self.stem = infinitive[:-len(ending)]
# 		self.present_stem = self.stem + "uj"
# 		self.past_stem = self.stem + "oval"
# 		self.imperative_stem = self.present_stem
# 		#self.passive_stem = self.stem + "ován"

# 	def kind(self):
# 		print("Class II verb subclass, specific to -ovat verbs")

# class Class3(Verb):
# 	def __init__(self, infinitive = "", ending = ""):
# 		Verb.__init__(self, infinitive, ending)

# 	def kind(self):
# 		print("Class III verb, conjugates according to -it/et/-ět paradigm")

# 	def _conjugate_present(self):
# 		# TODO: move the regex to vutils, contains_stem()
# 		plural_third_ending = "ědí" if re.search("jíst$|sníst$|vědět$", self._infinitive) else "í"
# 		plural_third = self._present_stem + plural_third_ending
# 		present_tense = PrettyTable(self._present_header)
# 		present_conjugation = PrettyTable(self._conjugation_headers)
# 		present_conjugation.add_row(["1.", self._present_stem + "ím", self._present_stem + "íme"])
# 		present_conjugation.add_row(["2.", self._present_stem + "íš", self._present_stem + "íte"])
# 		present_conjugation.add_row(["3.", self._present_stem + "í", plural_third])
# 		present_tense.add_row([present_conjugation])
# 		return present_tense

# 	def conjugate(self):
# 		print(self._conjugate_present())
# 		print(Verb._conjugate_imperative(self))
# 		print(Verb._conjugate_past(self))
# 		print(Verb._conjugate_conditional(self))

# class Class3_itet(Class3):
# 	def __init__(self, infinitive, ending):
# 		_thematic_vowel = ending[0]
# 		self._infinitive = infinitive
# 		self._ending = ending
# 		self._stem = vutils.soften(infinitive[:-len(ending)])
# 		self._present_stem = vutils.harden(self._stem)
# 		self._past_stem = self._present_stem + _thematic_vowel + "l"

# 		consonants = "(" + vutils.consonant + "{1}|" + vutils.digraph + "){1}" # polygraphs/multigraphs though single phonemes

# 		# long vowels and non-clusters have j added to imperative with thematic vowel
# 		# TODO: move the regex to vutils, you can define the regex strings here, contains_stem()
# 		if re.search(vutils.long_vowel + consonants + "[eě]t$", self._infinitive) or re.search("ou" + consonants + "[eě]t$", self._infinitive):
# 			self._imperative_stem = self._present_stem + _thematic_vowel + "j"
# 		# ditto with (some) neutral consonants
# 		elif re.search("[bmvs]ět$", self._infinitive) or re.search("víjet$", self._infinitive):
# 			self._imperative_stem  = self._present_stem + _thematic_vowel + "j"
# 		# long vowels, non clusters and SHORT thematic vowel has the root vowel shortened
# 		elif x := re.findall(vutils.long_vowel + vutils.consonant + "{1}it$", self._infinitive) or re.findall("ou" + vutils.consonant + "{1}it$", self._infinitive):
# 			# 1. check if the verb matches the above pattern
# 			# 2. isolate the contained long vowel
# 			# 3. replace long vowel with its shortened in the original stem
# 			y = re.findall(vutils.long_vowel, x[0]) or re.findall("ou", x[0])
# 			self._imperative_stem = re.sub(y[0], vutils.get_short_vowel(y[0]), self._stem)

# 		# fixing imperative stem if digraph
# 		elif x := re.findall(vutils.digraph + "$", self._infinitive[:-2]):
# 			self._imperative_stem = self._present_stem
# 		else:
# 			self._imperative_stem = self._stem

# 		# non-cluster stems are softened, otherwise add i
# 		if x := re.findall("[^aeiouyrlě]{2}", self._imperative_stem[-2:]):
# 			if y := re.findall(vutils.digraph, x[0]) and not re.search("[ei]", self._imperative_stem[-3]):
# 				self._imperative_stem = vutils.soften(self._imperative_stem)
# 			else:
# 				self._imperative_stem = vutils.harden(self._imperative_stem) + "i"


# 		#self._passive_stem = self._stem[:-1] if _thematic_vowel == "i" else (self._stem + _thematic_vowel + "n")
# 		#if _thematic_vowel == "i":
# 		#	match self._stem[-1]:
# 		#		case "ť":
# 		#			self._passive_stem += "cen"
# 		#		case "ď":
# 		#			self._passive_stem += "děn"
# 		#		case "ň":
# 		#			self._passive_stem += "něn"
# 		#		case _:
# 		#			self._passive_stem += self._present_stem[-1] + "en"

# 	def kind(self):
# 		print("Class III subclass, specific to regular -it/-et/-ět verbs")

# class Class4(Verb):
# 	def __init__(self, infinitive = "", ending = ""):
# 		Verb.__init__(self, infinitive, ending)

# 	def kind(self):
# 		print("Class IV verb, conjugates according to -nout/-st/-ct/-zt paradigm")

# 	def _conjugate_present(self):
# 		present_tense = PrettyTable(self._present_header)
# 		present_conjugation = PrettyTable(self._conjugation_headers)
# 		present_conjugation.add_row(["1.", self._present_stem + "u", self._present_stem + "eme"])
# 		present_conjugation.add_row(["2.", self._present_stem + "eš", self._present_stem + "ete"])
# 		present_conjugation.add_row(["3.", self._present_stem + "e", self._present_stem + "ou"])
# 		present_tense.add_row([present_conjugation])
# 		return present_tense

# 	def conjugate(self):
# 		print(self._conjugate_present())
# 		print(Verb._conjugate_imperative(self))
# 		print(Verb._conjugate_past(self))
# 		print(Verb._conjugate_conditional(self))

# class Class4_nout(Class4):
# 	def __init__(self, infinitive, ending):
# 		self._infinitive = infinitive
# 		self._ending = ending
# 		self._stem = infinitive[:-len(ending)]
# 		self._present_stem = self._stem + "n"
# 		self._imperative_stem = self._stem + "ň" if vutils.isvowel(self._stem[-1]) else self._stem + "ni"
# 		self._past_stem = self._stem
# 		if vutils.isvowel(self._past_stem[0]) or  not vutils.contains_vowel(self._past_stem[:-len(self._ending)]):
# 			self._past_stem += "nul"
# 		else:
# 			self._past_stem += "l"
# 		#self._passive_stem = self._stem + "nut"

# 		#self._past_stem_variant = self._stem[:-1] + "něl"
# 		#self._passive_stem_variant = self._stem[:-1] + "něn"

# 	def kind(self):
# 		print("Class IV verb subclass, specific for -nout verbs")

# 	def stems(self):
# 		Verb.stems(self)
# 		#print("past stem variant: ", self._past_stem_variant)
# 		#print("passive stem variant: ", self._passive_stem_variant)

# class Class4_st(Class4):
# 	def __init__(self, infinitive, ending):
# 		self._infinitive = infinitive
# 		self._ending = ending
# 		self._stem = vutils.shorten(infinitive[:-len(ending)])
# 		self._present_stem = self._stem + "d"
# 		self._past_stem = self._present_stem + "l"
# 		#self._passive_stem = self._present_stem + "en"
# 		self._imperative_stem = vutils.soften(self._present_stem)

# 	def kind(self):
# 		print("Class IV verb subclass, specific for -st verbs")

# class Class4_zt(Class4):
# 	def __init__(self, infinitive, ending):
# 		self._infinitive = infinitive
# 		self._ending = ending
# 		self._stem = vutils.shorten(infinitive[:len(ending)])
# 		self._present_stem = self._stem + "z"
# 		self._past_stem = self._present_stem + "l"
# 		#self._passive_stem = self._present_stem + "en"
# 		self._imperative_stem = self._present_stem

# 	def kind(self):
# 		print("Class IV verb subclass, specific to -zt verbs")

# class Class4_ct(Class4):
# 	def __init__(self, infinitive, ending):
# 		self._infinitive = infinitive
# 		self._ending = ending
# 		self._stem = vutils.shorten(infinitive[:-len(ending)])
# 		self._present_stem = self._stem + "č"
# 		self._past_stem = self._stem + "kl"
# 		#self._passive_stem = self._present_stem + "en"
# 		self._imperative_stem = self._present_stem

# 	def kind(self):
# 		print("Class IV verb subclass, specific to -ct verbs")
