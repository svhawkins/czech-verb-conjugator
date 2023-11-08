""""
Verbs

Module containing all of the verb classes and subclasses needed
to conjugate a Czech verb. 

Consists of 5 main classes, all of which are derived from the Verb base class.
The Verb class does most of the work in the conjugations.
The derived classes alter the present endings and stems.
A Verb is constructed from an infinitive, ending, perfective indicator, and an 'is_motion' indicator
and that indicator's accompanying prefix (these indicators vary how a verb is conjugated in the present
and fututre tense, regardless of class).

The 5 main classes are as follows:

0. Byt : for the irregular verb Být
1. Class1 : for Class1 Verbs
2. Class2 : for Class2 Verbs
3. Class3 : for Class3 Verbs
4. Class4 : for Class4 Verbs

Classes 1-4 also each have their own subclasses to house
ending-specific stem constructions and conjugations.
Class1 subclasses (1):
	- Class1_at
Class2 subclasses (4):
	- Class2_ityt
	- Class2_ovat
	- Class2_out
	- Class2_at
Class3 subclasses (2):
	- Class3_itet
	- Class3_cluster
Class4 subclasses (7):
	- Class4_nout
	- Class4_st
	- Class4_zt
	- Class4_ct
	- Class4_rit
	- Class4_apat
	- Class4_cluster
"""

import src.verb_utils as vutils
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
	"""
	Base class to store a verb's conjugation.

	This base class houses the majority of a verb's necessary conjugation(s),
	holding the endings needed for moods and tenses other than the present indicative.

	Class members:
		_empty : tuple --> empty/default endings
		_participle_endings : tuple --> participle endings for conditional mood and past tense
		_present_endings : tuple --> default present tense endings
		_imperative_endings : tuple ---> imperative endings for imperative mood

		_past_auxiliary : tuple --> auxiliary verb used in the past tense
		_future_auxiliary : tuple --> auxiliary verb used in the future tense for imperfective verbs
		_conditional_auxiliary : tuple --> auxiliary verb used in the conditional/subjunctive moods

		_tense_to_ending : list --> list that maps tense IntEnum to endings tuple
		_tense_to_auxiliary : list --> list that maps tense IntEnum to auxiliary tuple

	Attributes:
		class_num : int --> Integer indicator of verb class (0, 1, 2, 3, or 4)
		infinitive : str --> a verb's infinitive
		ending : str --> a verb's ending
		stem : str --> a verb's stem (infinitive sans the ending)
		present_stem : str --> a verb's present tense stem
		past_stem : str --> a verb's past tense stem
		imperative_stem : str --> a verb's imperative mood stem
	
	Methods:
		conjugate(self, tense_idx : int = len(Tense), person_idx : int = len(Person))
			conjugate a verb
		get_conjugation_at(self, tense_idx : int, person_idx : int) -> str
			get specified conjugation
		clear_table(self)
			clear conjugation table
		get_table(self)
			get conjugation table
	"""
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

	# tense to (auxiliary) ending mappings
	# present,past,future,imperative,conditional
	_tense_to_ending = [ _present_endings, _participle_endings, _empty, _imperative_endings, _participle_endings]
	_tense_to_auxiliary = [ _empty, _past_auxiliary, _future_auxiliary, _empty, _conditional_auxiliary]

	def __init__(self, infinitive : str = "", ending : str = "",
			  	 is_perfective : bool = False, is_motion : tuple = (False, "")):
		"""
		Construct a Verb object.

		Parameters:
			infinitive (default "") : str --> infinitive of the verb
			ending (default "") : str --> the verb's ending
			is_perfective (default False) : bool --> indicator if a verb is perfective
			is_motion (default (False, "") : tuple(bool, str)) --> indicator if verb is motion verb and accompanying prefix
		"""
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

	def _get_conjugation(self, tense : int, person : int) -> str:
		"""Return a fully constructed conjugation for given tense and person indices."""
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
	
	def conjugate(self, tense_idx : int = len(Tense), person_idx : int = len(Person)):
		"""
		Conjugate a verb according provided tense and person indices.

		Parameters:
			tense : int --> any one of the integer constants defined in IntEnum Tense
			person : int --> any one of the integer constants defined in IntEnum Person
		"""

		# set up ranges for given tense and person
		tense_range = range(tense_idx, tense_idx + 1) if tense_idx != len(Tense) else range(len(Tense))
		person_range = range(person_idx, person_idx + 1) if person_idx != len(Person) else range(len(Person))

		for tense in tense_range:
			for person in person_range:
				self._conjugation_table[tense][person] = self._get_conjugation(tense, person)

	def get_conjugation_at(self, tense_idx : int, person_idx : int) -> str:
		"""Return a conjugation at the specified indices."""
		valid_cond = (tense_idx >= 0 and tense_idx < len(Tense)) and (person_idx >= 0 and person_idx < len(Person))
		return self._conjugation_table[tense_idx][person_idx] if valid_cond else ""
	
	def clear_table(self):
		"""Clear the conjugation table."""
		for tense in range(len(Tense)):
			for person in range(len(Person)):
				self._conjugation_table[tense][person] = ""

	def get_table(self) -> list:
		"""Retrieve the conjugation table as a 2-dimensional string list."""
		return self._conjugation_table
	
	def kind(self) -> str:
		"""Return type of class as string"""
		return "Verb"

class Byt(Verb):
	""""
	Class to store the stems, endings, and conjugations of the (wholly) irregular verb být.

	Extends the Verb base class and overwrites the present endings.
	Has the same methods and attributes as Verb.
	"""

	_present_endings = ("jsem", "jseš/jsi", "je", "jsme", "jste", "jsou")
	_endings = (_present_endings, Verb._participle_endings, Verb._imperative_endings )
	def __init__(self, infinitive : str = "", ending : str = "",
			  	 is_perfective : bool = False, is_motion : tuple = (False, "")):
		""""Constructs Byt object by extending the Verb construction by overwriting the default stems."""

		super().__init__(infinitive, ending, is_perfective, is_motion )
		self._prefix = infinitive[:-len("být")]
		self.infinitive = infinitive
		self.past_stem = self._prefix + "byl"
		self.imperative_stem = self._prefix + "buď"
		
		# update stems, future is empty since would be redundant to have bud- + být. Auxiliary is just future být!
		self._stems = [ self.present_stem, self.past_stem, "", self.imperative_stem, self.past_stem ]
		
		# update the endings for it to be to this class
		self._tense_to_auxiliary[Tense.PRESENT] = self._present_endings
	
	def conjugate(self, tense_idx = len(Tense), person_idx = len(Person)):
		"""Extends Verb's conjugate method by updating some present-tense endings."""
		super().conjugate(tense_idx, person_idx)

		# update the present tense with the present endings since there is no present stem
		negation_prefix = "ne" if self._is_negative == True else ""
		for person in range(len(Person)):
			ending = "ní" if self._is_negative and person == Person.THIRD_SG else self._present_endings[person]
			self._conjugation_table[Tense.PRESENT][person] = negation_prefix + ending

	def kind(self) -> str:
		"""Return type of class as string"""
		return "Být"

class Class1(Verb):
	"""Extension of Verb base class to accommodate Class 1 verbs and their endings."""
	# verb class specific endings:
	_present_endings = [ "ám", "áš", "á", "áme" ,"áte", "ají" ]

	# sanity check, was making past, present, and future tack on present být conjugations otherwise
	_tense_to_ending = [ _present_endings, Verb._participle_endings, Verb._empty, Verb._imperative_endings, Verb._participle_endings]
	_tense_to_auxiliary = [ Verb._empty, Verb._past_auxiliary, Verb._future_auxiliary, Verb._empty, Verb._conditional_auxiliary]
	def __init__(self, infinitive : str = "", ending : str = "",
			  	 is_perfective : bool = False, is_motion : tuple = (False, "")):
		"""Extends Verb's __init__ by overwriting the class_num and present tense endings."""
		super().__init__(infinitive, ending, is_perfective, is_motion)
		self.class_num = 1

		# update endings
		self._tense_to_ending[Tense.PRESENT] = self._present_endings

	def kind(self) -> str:
		"""Return type of class as string"""
		return "Class1"

class Class1_at(Class1):
	"""Extension of Class1 verbs to accomodate Class1 verbs with -at/-át endings."""
	def __init__(self, infinitive : str = "", ending : str = "",
			  	 is_perfective : bool = False, is_motion : tuple = (False, "")):
		"""Extends Class1's __init__ by overwriting the stems."""
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

	def kind(self) -> str:
		"""Return type of class as string"""
		return "Class1_at"

class Class2(Verb):
	"""Extension of Verb base class to accommodate Class 2 verbs and their endings."""
	# class specific endings
	_present_endings = ["i/u", "eš", "e", "eme", "ete", "í"]
	_tense_to_ending = [ _present_endings, Verb._participle_endings, Verb._empty, Verb._imperative_endings, Verb._participle_endings]
	_tense_to_auxiliary = [ Verb._empty, Verb._past_auxiliary, Verb._future_auxiliary, Verb._empty, Verb._conditional_auxiliary]
	def __init__(self, infinitive : str = "", ending : str = "",
			  	 is_perfective : bool = False, is_motion : tuple = (False, "")):
		"""Extends Verb's __init__ by overwriting the class_num and present tense endings."""
		super().__init__(infinitive, ending, is_perfective, is_motion)
		self.class_num = 2

		# update endings
		self._tense_to_ending[Tense.PRESENT] = self._present_endings

	def _apply_chtit_correction(self, tense_idx : int, person_idx :int):
		"""Overwrites chtít conjugations in the present tense for the 3rd person plural and 1st person singular."""
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
		
	def conjugate(self, tense_idx : int = len(Tense), person_idx : int = len(Person)):
		"""Extension of Verb's conjugate but modifies a few conjugations afterwards."""
		# if verb is chtít, ALWAYS overwrite/correct it
		super().conjugate(tense_idx, person_idx)
		if re.search("chtít$", self.infinitive):
			self._apply_chtit_correction(tense_idx, person_idx)

	def kind(self) -> str:
		"""Return type of class as string"""
		return "Class2"


class Class2_ityt(Class2):
	"""Extension of Class2 verbs to accomodate Class2 verbs with -ít/-ýt endings."""
	def __init__(self, infinitive : str = "", ending : str = "",
			  	 is_perfective : bool = False, is_motion : tuple = (False, "")):
		"""Extends Class2's __init__ by overwriting the stems."""
		super().__init__(infinitive, ending, is_perfective, is_motion)
		_thematic_vowel = "i" if ending.startswith("í") else "y"
		if re.search("(sít)$", self.infinitive):
			_thematic_vowel = "e"
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

	def kind(self) -> str:
		"""Return type of class as string"""
		return "Class2_ityt"

class Class2_ovat(Class2):
	"""Extension of Class2 verbs to accomodate Class2 verbs with -ovat endings."""
	def __init__(self, infinitive : str = "", ending : str = "",
			  	 is_perfective : bool = False, is_motion : tuple = (False, "")):
		"""Extends Class2's __init__ by overwriting the stems."""
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

	def kind(self) -> str:
		"""Return type of class as string"""
		return "Class2_ovat"

class Class3(Verb):
	"""Extension of Verb base class to accommodate Class 3 verbs and their endings."""
	# class specific endings
	_present_endings = ["ím", "íš", "í", "íme", "íte", "í"]
	_tense_to_ending = [ _present_endings, Verb._participle_endings, Verb._empty, Verb._imperative_endings, Verb._participle_endings]
	_tense_to_auxiliary = [ Verb._empty, Verb._past_auxiliary, Verb._future_auxiliary, Verb._empty, Verb._conditional_auxiliary]
	def __init__(self, infinitive : str = "", ending : str = "",
			  	 is_perfective : bool = False, is_motion : tuple = (False, "")):
		"""Extends Verb's __init__ by overwriting the class_num and present tense endings."""
		super().__init__(infinitive, ending, is_perfective, is_motion)
		self.class_num = 3

		# update endings
		self._tense_to_ending[Tense.PRESENT] = self._present_endings

	def kind(self) -> str:
		"""Return type of class as string"""
		return "Class3"

class Class3_itet(Class3):
	"""Extension of Class3 verbs to accomodate Class3 verbs with -it/-et/-ět endings."""
	def __init__(self, infinitive : str = "", ending : str = "",
			  	 is_perfective : bool = False, is_motion : tuple = (False, "")):
		"""Extends Class3's __init__ by overwriting the stems."""
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
		"""Updates the imperative stem according to edge cases."""

		# syllables
		syllables = vutils.Syllables(self.present_stem)

		# the actually exceptional-but-still-regular cases are here:
		if re.search("slzet$", self.infinitive):
			self.imperative_stem = self.stem + "ej"
		elif re.search("(pustit|půjčit)$", self.infinitive):
			self.imperative_stem = self.stem
		elif re.search("(chvět|ouštět)$", self.infinitive):
			self.imperative_stem = self.present_stem + "ěj"
		elif re.search("(skřípět)$", self.infinitive):
			self.imperative_stem = vutils.shorten(self.stem)
		elif re.search("(lpět)$", self.infinitive):
			self.imperative_stem = self.stem + "i"
		
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

	def kind(self) -> str:
		"""Return type of class as string"""
		return "Class3_itet"

class Class4(Verb):
	"""Extension of Verb base class to accommodate Class 4 verbs and their endings."""
	# class specific endings
	_present_endings = ["u", "eš", "e", "eme", "ete", "ou"]
	_tense_to_ending = [ _present_endings, Verb._participle_endings, Verb._empty, Verb._imperative_endings, Verb._participle_endings]
	_tense_to_auxiliary = [ Verb._empty, Verb._past_auxiliary, Verb._future_auxiliary, Verb._empty, Verb._conditional_auxiliary]
	def __init__(self, infinitive : str = "", ending : str = "",
			  	 is_perfective : bool = False, is_motion : tuple = (False, "")):
		"""Extends Verb's __init__ by overwriting the class_num and present tense endings."""
		super().__init__(infinitive, ending, is_perfective, is_motion)
		self.class_num = 4

	def kind(self) -> str:
		"""Return type of class as string"""
		return "Class4"

class Class4_nout(Class4):
	"""Extension of Class4 verbs to accomodate Class4 verbs with -nout endings."""
	def __init__(self, infinitive : str = "", ending : str = "",
			  	 is_perfective : bool = False, is_motion : tuple = (False, "")):
		"""Extends Class4's __init__ by overwriting the stems."""
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

	def conjugate(self, tense_idx : int = len(Tense), person_idx : int = len(Person)):
		"""Extends Verb's conjugate but updates with vowel changes to the imperative plural endings."""
		super().conjugate(tense_idx, person_idx)

		# apply imperative corrections if stem is -ni
		if self.imperative_stem[-2:] == "ni":
			self._conjugation_table[Tense.IMPERATIVE][Person.FIRST_PL] = self.imperative_stem[:-1] + "ěme"
			self._conjugation_table[Tense.IMPERATIVE][Person.SECOND_PL] = self.imperative_stem[:-1] + "ěte"

	def kind(self) -> str:
		"""Return type of class as string"""
		return "Class4_nout"


class Class4_st(Class4):
	"""Extension of Class4 verbs to accomodate Class4 verbs with -st endings."""
	def __init__(self, infinitive : str = "", ending : str = "",
			  	 is_perfective : bool = False, is_motion : tuple = (False, "")):
		"""Extends Class4's __init__ by overwriting the stems."""
		super().__init__(infinitive, ending, is_perfective, is_motion)
		self.infinitive = infinitive
		self.ending = ending
		# í -> ě/e, NOT í -> i
		self.stem = vutils.shorten(infinitive[:-len(ending)])
		if self.stem[-1] == "i":
			self.stem = self.stem[:-1] + "e"

		self.present_stem = self.stem + "d"
		self.past_stem = self.present_stem + "l"
		#self.passive_stem = self.present_stem + "en"
		self.imperative_stem = self.stem + vutils.get_soft_consonant(self.present_stem[-1])

		# update stems
		future_stem = self.infinitive[2:] if self.infinitive[:2] == "ne" else self.infinitive
		self._stems = [self.present_stem, self.past_stem, future_stem, self.imperative_stem, self.past_stem ]

	def kind(self) -> str:
		"""Return type of class as string"""
		return "Class4_st"

class Class4_zt(Class4):
	"""Extension of Class4 verbs to accomodate Class4 verbs with -zt endings."""
	def __init__(self, infinitive : str = "", ending : str = "",
			  	 is_perfective : bool = False, is_motion : tuple = (False, "")):
		"""Extends Class4's __init__ by overwriting the stems."""
		super().__init__(infinitive, ending, is_perfective, is_motion)
		self._infinitive = infinitive
		self.ending = ending
		# í -> ě/e, NOT í -> i
		self.stem = vutils.shorten(infinitive[:-len(ending)])
		if self.stem[-1] == "i":
			self.stem = self.stem[:-1] + "e"
		
		self.present_stem = self.stem + "z"
		self.past_stem = self.present_stem + "l"
		#self.passive_stem = self._present_stem + "en"
		self.imperative_stem = self.present_stem

		# update stems
		future_stem = self.infinitive[2:] if self.infinitive[:2] == "ne" else self.infinitive
		self._stems = [self.present_stem, self.past_stem, future_stem, self.imperative_stem, self.past_stem ]

	def kind(self) -> str:
		"""Return type of class as string"""
		return "Class4_zt"

class Class4_ct(Class4):
	"""Extension of Class4 verbs to accomodate Class4 verbs with -ct endings."""
	def __init__(self, infinitive : str = "", ending : str = "",
			  	 is_perfective : bool = False, is_motion : tuple = (False, "")):
		"""Extends Class4's __init__ by overwriting the stems."""
		super().__init__(infinitive, ending, is_perfective, is_motion)
		self.infinitive = infinitive
		self.ending = ending
		# í -> ě/e, NOT í -> i
		self.stem = vutils.shorten(infinitive[:-len(ending)])
		if self.stem[-1] == "i":
			self.stem = self.stem[:-1] + "e"

		
		self.present_stem = self.stem + "č"
		self.past_stem = self.stem + "kl"
		if self.stem[-1] == "u": # ou -> u
			self.past_stem = vutils.lengthen(self.past_stem)
		#self.passive_stem = self.present_stem + "en"
		self.imperative_stem = self.present_stem

		# update stems
		future_stem = self.infinitive[2:] if self.infinitive[:2] == "ne" else self.infinitive
		self._stems = [self.present_stem, self.past_stem, future_stem, self.imperative_stem, self.past_stem ]

	def kind(self) -> str:
		"""Return type of class as string"""
		return "Class4_ct"


#### semi-irregular classes ####
# verb classes that are technically regular, but at first glance their classes are 'misleading'
class Class4_rit(Class4):
	"""Extension of Class4 verbs to accomodate Class4 verbs with -řít endings."""
	def __init__(self, infinitive : str = "", ending : str = "",
			  	 is_perfective : bool = False, is_motion : tuple = (False, "")):
		"""Extends Class4's __init__ by overwriting the stems."""
		super().__init__(infinitive, ending, is_perfective, is_motion)
		self.class_num = 4
		self.infinitive = infinitive
		self.ending = ending
		self.stem = self.infinitive[:-len(ending)]
		self.present_stem = self.stem + "ř"
		self.past_stem = self.stem + "řel"
		self.imperative_stem = self.stem  + "ři"

		# update stems
		future_stem = self.infinitive[2:] if self.infinitive[:2] == "ne" else self.infinitive
		self._stems = [self.present_stem, self.past_stem, future_stem, self.imperative_stem, self.past_stem ]

	def conjugate(self, tense_idx : int = len(Tense), person_idx : int = len(Person)):
		"""Extends Verb's conjugate but updates with vowel changes to the imperative plural endings."""
		super().conjugate(tense_idx, person_idx)

		# apply imperative corrections, always ending in -i
		self._conjugation_table[Tense.IMPERATIVE][Person.FIRST_PL] = self.imperative_stem[:-1] + "eme"
		self._conjugation_table[Tense.IMPERATIVE][Person.SECOND_PL] = self.imperative_stem[:-1] + "ete"

	def kind(self) -> str:
		"""Return type of class as string"""
		return "Class4_řít"

class Class2_out(Class2):
	"""Extension of Class2 verbs to accomodate Class2 verbs with -out endings."""
	def __init__(self, infinitive : str = "", ending : str = "",
			  	 is_perfective : bool = False, is_motion : tuple = (False, "")):
		"""Extends Class2's __init__ by overwriting the stems."""
		super().__init__(infinitive, ending, is_perfective, is_motion)
		self.class_num = 2
		self.infinitive = infinitive
		self.ending = ending
		self.stem = self.infinitive[:-len(ending)]
		self.present_stem = self.stem + "uj"
		self.past_stem = self.stem + "ul"
		self.imperative_stem = self.present_stem

		# update stems
		future_stem = self.infinitive[2:] if self.infinitive[:2] == "ne" else self.infinitive
		self._stems = [self.present_stem, self.past_stem, future_stem, self.imperative_stem, self.past_stem ]

	def kind(self) -> str:
		"""Return type of class as string"""
		return "Class2_out"

class Class2_at(Class2):
	"""Extension of Class2 verbs to accomodate Class2 verbs with -át endings."""
	def __init__(self, infinitive : str = "", ending : str = "",
			  	 is_perfective : bool = False, is_motion : tuple = (False, "")):
		"""Extends Class2's __init__ by overwriting the stems."""
		super().__init__(infinitive, ending, is_perfective, is_motion)
		self.class_num = 2
		self.infinitive = infinitive
		self.ending = ending
		self.stem = self.infinitive[:-len(ending)]

		# soft stem endings take ej, rest take aj
		self.present_stem = self.stem + "aj"
		if re.search("[smvř]$", self.stem):
			self.present_stem = self.stem + "ej"
			if re.search("[vm]$", self.stem):
				self.present_stem = self.stem + "ěj"
		self.past_stem = self.stem + "ál"
		self.imperative_stem = self.present_stem

		# update stems
		future_stem = self.infinitive[2:] if self.infinitive[:2] == "ne" else self.infinitive
		self._stems = [self.present_stem, self.past_stem, future_stem, self.imperative_stem, self.past_stem ]

	def kind(self) -> str:
		"""Return type of class as string"""
		return "Class2_át"
	
class Class3_cluster(Class3):
	"""Extension of Class3 verbs to accomodate Class3 verbs with cluster stems."""
	def __init__(self, infinitive : str = "", ending : str = "",
			  	 is_perfective : bool = False, is_motion : tuple = (False, "")):
		"""Extends Class3's __init__ by overwriting the stems."""
		super().__init__(infinitive, ending, is_perfective, is_motion)
		self.class_num = 3
		self.infinitive = infinitive
		self.ending = ending
		self.stem = self.infinitive[:-len(ending)]
		self.present_stem = self.stem

		# the thematic vowel in the past stem varies with what the final stem consonant is
		self.past_stem = self.stem + "il"
		if re.search("[dlvř]$", self.stem):
			self.past_stem = self.stem + "el"
			if re.search("[vd]$", self.stem):
				self.past_stem = self.stem + "ěl"

		# case-by-case basis
		if re.search("^((zdít)|(sklít)|(mnít))", self.infinitive): # FIXME: use the root + ending other than whole infinitive
			self.past_stem = self.stem + "il" # the root/non-prefix infinitive is corrected during disambiguation.
		elif re.search("(znít)$", self.infinitive):
			self.past_stem = self.stem + "ěl"
		
		self.imperative_stem = self.stem  + "i"

		# update stems
		future_stem = self.infinitive[2:] if self.infinitive[:2] == "ne" else self.infinitive
		self._stems = [self.present_stem, self.past_stem, future_stem, self.imperative_stem, self.past_stem ]

	def conjugate(self, tense_idx : int = len(Tense), person_idx : int = len(Person)):
		"""Extends Verb's conjugate but updates with vowel changes to the imperative plural endings."""
		super().conjugate(tense_idx, person_idx)

		# apply imperative corrections, stem always ending in i.
		imperative_plural_vowel = "ě" if re.search("[dtvn]$", self.stem) else "e"
		self._conjugation_table[Tense.IMPERATIVE][Person.FIRST_PL] = self.imperative_stem[:-1] \
																	+ imperative_plural_vowel + "me"
		self._conjugation_table[Tense.IMPERATIVE][Person.SECOND_PL] = self.imperative_stem[:-1] \
																	+ imperative_plural_vowel + "te"

	def kind(self) -> str:
		"""Return type of class as string"""
		return "Class3_cluster"
	
class Class4_apat(Class4):
	"""Extension of Class4 verbs to accomodate Class4 verbs with -ápat, ámat, ázat endings."""
	def __init__(self, infinitive : str = "", ending : str = "",
			  	 is_perfective : bool = False, is_motion : tuple = (False, "")):
		"""Extends Class4's __init__ by overwriting the stems."""
		super().__init__(infinitive, ending, is_perfective, is_motion)
		self.class_num = 4
		self.infinitive = infinitive
		self.ending = ending
		self.stem = self.infinitive[:-2] # remove the -at
		self.present_stem = self.stem
		self.past_stem = self.stem + "al"
		self.imperative_stem = self.present_stem + "ej"

		# z is softened (palatalized? this is the same change as a palatalization...)
		if re.search("(zat)$", ending):
			self.present_stem = self.present_stem[:-1] + "ž" # z -> ž
			self.imperative_stem = vutils.shorten(self.present_stem)

		# update stems
		future_stem = self.infinitive[2:] if self.infinitive[:2] == "ne" else self.infinitive
		self._stems = [self.present_stem, self.past_stem, future_stem, self.imperative_stem, self.past_stem ]

	def kind(self) -> str:
		"""Return type of class as string"""
		return "Class4_ápat"


class Class4_cluster(Class4):
	"""Extension of Class4 verbs to accomodate Class4 verbs with -át endings and clusters in the root."""
	def __init__(self, infinitive : str = "", ending : str = "",
			  	 is_perfective : bool = False, is_motion : tuple = (False, "")):
		"""Extends Class4's __init__ by overwriting the stems."""
		super().__init__(infinitive, ending, is_perfective, is_motion)
		self.class_num = 4
		self.infinitive = infinitive
		self.ending = ending
		self.stem = self.infinitive[:-2] # remove the -at
		self.present_stem = self.stem

		# stem may have fill vowel added or soften consonants.
		if self.stem[-1] == "h":
			self.present_stem = self.stem[:-1] + "ž"
		elif self.stem[-2:] == "sl":
			self.present_stem = self.stem[:-2] + "šl"
		elif re.search("(" + vutils.syllabic_consonant + ")$", self.stem):
			self.present_stem = self.stem[:-1] + "e" + self.stem[-1]

		self.past_stem = self.stem + "al"
		self.imperative_stem = self.present_stem

		# append i if cluster
		if re.search("(" + vutils.consonant + "){2,}", self.present_stem):
			self.imperative_stem = self.imperative_stem + "i"

		# update stems
		future_stem = self.infinitive[2:] if self.infinitive[:2] == "ne" else self.infinitive
		self._stems = [self.present_stem, self.past_stem, future_stem, self.imperative_stem, self.past_stem ]

	def conjugate(self, tense_idx : int = len(Tense), person_idx : int = len(Person)):
		"""Extends Verb's conjugate but updates with vowel changes to the imperative plural endings."""
		super().conjugate(tense_idx, person_idx)

		# apply imperative corrections if stem is -i
		if self.imperative_stem[-1] == "i":
			imperative_plural_vowel = "ě" if re.search("[dtvnpb]$", self.stem) else "e"
			self._conjugation_table[Tense.IMPERATIVE][Person.FIRST_PL] = self.imperative_stem[:-1] \
																		+ imperative_plural_vowel + "me"
			self._conjugation_table[Tense.IMPERATIVE][Person.SECOND_PL] = self.imperative_stem[:-1] \
																		+ imperative_plural_vowel + "te"

	def kind(self) -> str:
		"""Return type of class as string"""
		return "Class4_cluster"
