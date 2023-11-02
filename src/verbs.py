# module containing the verb classes to conjugate a czech verb
# the base class is Verb responsible for majority of the conjugations
# the derived classes do the present tense as well as set the necessary stems for the conjugations
# 5 derived classes: class1, class2, class3, class4, and být (entirely irregular)
# each of these derived classes have subclasses for differing (though nonetheless the same endings):
# class1 has 1 subclass, class2 with 2, class3 with 1, and class4 with 4

# all verbs 2 strings during init: infinitive and ending
# optional flags can also be passed in: is_perfective (bool) , is_motion (tuple)
# these flags modify endings in some conjugations

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
		self.class_num = 0
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
		# set up ranges for given tense and person
		tense_range = range(tense_idx, tense_idx + 1) if tense_idx != len(Tense) else range(len(Tense))
		person_range = range(person_idx, person_idx + 1) if person_idx != len(Person) else range(len(Person))

		for tense in tense_range:
			for person in person_range:
				self._conjugation_table[tense][person] = self._get_conjugation(tense, person)

	def get_conjugation_at(self, tense_idx, person_idx):
		'''Returns a conjugation at the specified indices'''
		valid_cond = (tense_idx >= 0 and tense_idx < len(Tense)) and (person_idx >= 0 and person_idx < len(Person))
		return self._conjugation_table[tense_idx][person_idx] if valid_cond else ""
	
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
		self.class_num = 1

		# update endings
		self._tense_to_ending[Tense.PRESENT] = self._present_endings

	def kind(self):
		print("Class I verb, conjugates according to -at/-át paradigm")

class Class1_at(Class1):
	def __init__(self, infinitive = "", ending = "", is_perfective = False, is_motion = (False, "")):
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

class Class2(Verb):
	# class specific endings
	_present_endings = ["i/u", "eš", "e", "eme", "ete", "í"]
	_tense_to_ending = [ _present_endings, Verb._participle_endings, Verb._empty, Verb._imperative_endings, Verb._participle_endings]
	_tense_to_auxiliary = [ Verb._empty, Verb._past_auxiliary, Verb._future_auxiliary, Verb._empty, Verb._conditional_auxiliary]
	def __init__(self, infinitive = "", ending = "", is_perfective = False, is_motion = (False, "")):
		super().__init__(infinitive, ending, is_perfective, is_motion)
		self.class_num = 2

		# update endings
		self._tense_to_ending[Tense.PRESENT] = self._present_endings

	def kind(self):
		print("Class II verb, conjugates according to -ít/-ýt/-ovat paradigm")

	def _apply_chtit_correction(self, tense_idx, person_idx):
		if ((tense_idx == Tense.PRESENT or tense_idx == len(Tense))):
			if (person_idx == Person.FIRST_SG or person_idx == len(Person)):
				entry = self._conjugation_table[Tense.PRESENT][Person.FIRST_SG]
				entry = entry[:-8] + "chci"
				self._conjugation_table[Tense.PRESENT][Person.FIRST_SG] = entry
			if (person_idx == Person.THIRD_PL or person_idx == len(Person)):
				entry = self._conjugation_table[Tense.PRESENT][Person.THIRD_PL]
				entry = entry[:-6] + "chtějí"
				self._conjugation_table[Tense.PRESENT][Person.THIRD_PL] = entry
		return
		
	def conjugate(self, tense_idx = len(Tense), person_idx = len(Person)):
		# if verb is chtít, ALWAYS overwrite/correct it
		Verb.conjugate(self, tense_idx, person_idx)
		if re.search("chtít$", self.infinitive):
			self._apply_chtit_correction(tense_idx, person_idx)


class Class2_ityt(Class2):
	def __init__(self, infinitive = "", ending = "", is_perfective = False, is_motion = (False, "")):
		super().__init__(infinitive, ending, is_perfective, is_motion)
		_thematic_vowel = "i" if ending.startswith("í") else "y"
		self.infinitive = infinitive
		self.ending = ending
		self.stem = infinitive[:-len(ending)]
		self.present_stem = self.stem + _thematic_vowel + "j"
		self.past_stem = self.stem + _thematic_vowel + "l"
		self.imperative_stem = self.present_stem
		#self.passive_stem = self.stem + _thematic_vowel + "t"

		# update stems
		future_stem = self.infinitive[2:] if self.infinitive[:2] == "ne" else self.infinitive
		self._stems = [self.present_stem, self.past_stem, future_stem, self.imperative_stem, self.past_stem ]

	def kind(self):
		print("Class II verb subclass, specific to -ít/-ýt verbs")

class Class2_ovat(Class2):
	def __init__(self, infinitive = "", ending = "", is_perfective = False, is_motion = (False, "")):
		super().__init__(infinitive, ending, is_perfective, is_motion)
		self.infinitive = infinitive
		self.ending = ending
		self.stem = infinitive[:-len(ending)]
		self.present_stem = self.stem + "uj"
		self.past_stem = self.stem + "oval"
		self.imperative_stem = self.present_stem
		#self.passive_stem = self.stem + "ován"

		# update stems
		future_stem = self.infinitive[2:] if self.infinitive[:2] == "ne" else self.infinitive
		self._stems = [self.present_stem, self.past_stem, future_stem, self.imperative_stem, self.past_stem ]

	def kind(self):
		print("Class II verb subclass, specific to -ovat verbs")

class Class3(Verb):
	# class specific endings
	_present_endings = ["ím", "íš", "í", "íme", "íte", "í"]
	_tense_to_ending = [ _present_endings, Verb._participle_endings, Verb._empty, Verb._imperative_endings, Verb._participle_endings]
	_tense_to_auxiliary = [ Verb._empty, Verb._past_auxiliary, Verb._future_auxiliary, Verb._empty, Verb._conditional_auxiliary]
	def __init__(self, infinitive = "", ending = "", is_perfective = False, is_motion = (False, "")):
		super().__init__(infinitive, ending, is_perfective, is_motion)
		self.class_num = 3

		# update endings
		self._tense_to_ending[Tense.PRESENT] = self._present_endings

	def kind(self):
		print("Class III verb, conjugates according to -it/et/-ět paradigm")

class Class3_itet(Class3):
	def __init__(self, infinitive = "", ending = "", is_perfective = False, is_motion = (False, "")):
		super().__init__(infinitive, ending, is_perfective, is_motion)
		self._thematic_vowel = ending[0] # the thematic vowel is important here!
		not_ending = infinitive[:-len(ending)]
		self.infinitive = infinitive
		self.ending = ending
		self.present_stem = not_ending
		self.past_stem = not_ending + self._thematic_vowel + "l"
		self.stem = not_ending[:-1]+ vutils.get_soft_consonant(not_ending[-1])
		self.imperative_stem = self.stem

		# update the imperative stem, there are many edge cases!
		self._update_imperative_stem()

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

		# update stems
		future_stem = self.infinitive[2:] if self.infinitive[:2] == "ne" else self.infinitive
		self._stems = [self.present_stem, self.past_stem, future_stem, self.imperative_stem, self.past_stem ]

	def _update_imperative_stem(self):
		'''Updates the imperative stem according to edge cases'''

		# syllables
		syllables = vutils.Syllables(self.present_stem)

		# the actually exceptional-but-still-regular cases are here:
		if re.search("slzet$", self.infinitive):
			self.imperative_stem = self.stem + "ej"
		elif re.search("(pustit|půjčit)$", self.infinitive):
			self.imperative_stem = self.stem
		elif re.search("(chvět|ouštět)$", self.infinitive):
			self.imperative_stem = self.present_stem + "ěj"
		
		# the actual special cases

		# 1. neutral consonant with -ět: this gets -ěj
		elif re.search( vutils.neutral_consonant + "ět$", self.infinitive)\
			and not syllables.is_syllabic(-1) and syllables.contains_vowel(-1):
			self.imperative_stem = self.present_stem + "ěj"

		# 2. ends in 2+ non-syllabic consonants, regardless of ending:
		# aka a CONSONANT CLUSTER! Add an -i.
		elif (re.search("(" + vutils.consonant_or_digraph + "){2}[ieě]t$", self.infinitive)\
			and not vutils.Syllables(self.present_stem).is_syllabic(-1)) or\
			(syllables.is_syllabic(-1) and syllables.contains_cluster(-1)):
			self.imperative_stem = self.present_stem + "i"	

		# 2. long vowel followed by a consonant/digraph ending with -et/-ět
		# this gives it the -ěj or -ej ending
		elif re.search("((" + vutils.long_vowel + ")(" + vutils.consonant_or_digraph + "){1}[eě]t$)", self.infinitive):
			self.imperative_stem = self.present_stem if self._thematic_vowel == "ě" else self.stem 
			self.imperative_stem += self._thematic_vowel + "j"
	
		# 3. long vowel followed by a SINGLE consonant with -it:
		# this shortens the (final) long vowel present in the stem
		elif re.search("(" + vutils.long_vowel + "(" + vutils.consonant + "){1}" + "it$)", self.infinitive):
			self.imperative_stem = vutils.shorten(self.stem)

		# the actually exceptional-but-still-regular cases are here:
		if re.search("slzet$", self.infinitive):
			self.imperative_stem = self.stem + "ej"
		elif re.search("pustit$", self.infinitive):
			self.imperative_stem = self.stem
		elif re.search("chvěj$", self.infinitive):
			self.imperative_stem = self.stem + "ěj"

		

	def kind(self):
		print("Class III subclass, specific to regular -it/-et/-ět verbs")

class Class4(Verb):
	# class specific endings
	_present_endings = ["u", "eš", "e", "eme", "ete", "ou"]
	_tense_to_ending = [ _present_endings, Verb._participle_endings, Verb._empty, Verb._imperative_endings, Verb._participle_endings]
	_tense_to_auxiliary = [ Verb._empty, Verb._past_auxiliary, Verb._future_auxiliary, Verb._empty, Verb._conditional_auxiliary]
	def __init__(self, infinitive = "", ending = "", is_perfective = False, is_motion = (False, "")):
		super().__init__(infinitive, ending, is_perfective, is_motion)
		self.class_num = 4

	def kind(self):
		print("Class IV verb, conjugates according to -nout/-st/-ct/-zt paradigm")

class Class4_nout(Class4):
	def __init__(self, infinitive = "", ending = "", is_perfective = False, is_motion = (False, "")):
		super().__init__(infinitive, ending, is_perfective, is_motion)
		self.infinitive = infinitive
		self.ending = ending
		self.stem = infinitive[:-len(ending)]
		self.present_stem = self.stem + "n"
		self.imperative_stem = self.stem + "ň" 
		if not vutils.isvowel(self.stem[-1]):
			self.imperative_stem = self.stem + "ni"
		self.past_stem = self.stem + "nul"
		if not (vutils.isvowel(self.past_stem[0]) or not vutils.contains_vowel(self.past_stem[:-len(self.ending)])):
			self.past_stem = self.stem + "l" # ie "tiskl"
			
		# update stems
		future_stem = self.infinitive[2:] if self.infinitive[:2] == "ne" else self.infinitive
		self._stems = [self.present_stem, self.past_stem, future_stem, self.imperative_stem, self.past_stem ]

		#self._passive_stem = self._stem + "nut"

	def kind(self):
		print("Class IV verb subclass, specific for -nout verbs")

	def conjugate(self, tense_idx = len(Tense), person_idx = len(Person)):
		Verb.conjugate(self, tense_idx, person_idx)

		# apply imperative corrections if stem is -ni
		if self.imperative_stem[-2:] == "ni":
			self._conjugation_table[Tense.IMPERATIVE][Person.FIRST_PL] = self.imperative_stem[:-1] + "ěme"
			self._conjugation_table[Tense.IMPERATIVE][Person.SECOND_PL] = self.imperative_stem[:-1] + "ěte"


class Class4_st(Class4):
	def __init__(self, infinitive = "", ending = "", is_perfective = False, is_motion = (False, "")):
		super().__init__(infinitive, ending, is_perfective, is_motion)
		self.infinitive = infinitive
		self.ending = ending
		self.stem = vutils.shorten(infinitive[:-len(ending)])
		self.present_stem = self.stem + "d"
		self.past_stem = self.present_stem + "l"
		#self.passive_stem = self.present_stem + "en"
		self.imperative_stem = self.stem + vutils.get_soft_consonant(self.present_stem[-1])

		# update stems
		future_stem = self.infinitive[2:] if self.infinitive[:2] == "ne" else self.infinitive
		self._stems = [self.present_stem, self.past_stem, future_stem, self.imperative_stem, self.past_stem ]

	def kind(self):
		print("Class IV verb subclass, specific for -st verbs")

class Class4_zt(Class4):
	def __init__(self, infinitive = "", ending = "", is_perfective = False, is_motion = (False, "")):
		super().__init__(infinitive, ending, is_perfective, is_motion)
		self._infinitive = infinitive
		self.ending = ending
		self.stem = vutils.shorten(infinitive[:len(ending)])
		self.present_stem = self.stem + "z"
		self.past_stem = self.present_stem + "l"
		#self.passive_stem = self._present_stem + "en"
		self.imperative_stem = self.present_stem

		# update stems
		future_stem = self.infinitive[2:] if self.infinitive[:2] == "ne" else self.infinitive
		self._stems = [self.present_stem, self.past_stem, future_stem, self.imperative_stem, self.past_stem ]

	def kind(self):
		print("Class IV verb subclass, specific to -zt verbs")

class Class4_ct(Class4):
	def __init__(self, infinitive = "", ending = "", is_perfective = False, is_motion = (False, "")):
		super().__init__(infinitive, ending, is_perfective, is_motion)
		self.infinitive = infinitive
		self.ending = ending
		self.stem = vutils.shorten(infinitive[:-len(ending)])
		self.present_stem = self.stem + "č"
		self.past_stem = self.stem + "kl"
		#self.passive_stem = self.present_stem + "en"
		self.imperative_stem = self.present_stem

		# update stems
		future_stem = self.infinitive[2:] if self.infinitive[:2] == "ne" else self.infinitive
		self._stems = [self.present_stem, self.past_stem, future_stem, self.imperative_stem, self.past_stem ]

	def kind(self):
		print("Class IV verb subclass, specific to -ct verbs")
