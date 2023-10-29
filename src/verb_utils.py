# functions and classes for verb utilities that the Verb classes often use

import re

# regex patterns
short_vowel = "[aeiouy]"
long_vowel = "(ou)|[áéíóúůý]"
soft_vowel = "[ěií]"
hard_consonant_non_syllabic = "dghknst"
hard_consonant = "[" + hard_consonant_non_syllabic + "r]"
neutral_consonant = "[bmpvfqwx]"
soft_consonant_non_syllabic = "cčďjňřšťzž"
soft_consonant = "[" + soft_consonant_non_syllabic + "l]"
syllabic_consonant = "[rl]" # not including m/n since those are RARE
digraph = "(ch)|(st)|(št)|(ct)|(čt)"
consonant = hard_consonant + "|" + neutral_consonant + "|" + soft_consonant
consonant_non_syllabic = digraph + "|" + neutral_consonant + "|[" + soft_consonant_non_syllabic + "]|[" + hard_consonant_non_syllabic + "]"
consonant_or_digraph = digraph + "|" + consonant
vowel = long_vowel + "|" + short_vowel + "|" + soft_vowel
phoneme = "(" + consonant_or_digraph + "|" + vowel + ")"
cluster = r"(" + consonant_non_syllabic + "){3,5}"


# dictionaries for letter mappings
hard_to_soft = {"k":"c", "d":"ď", "g":"z", "h":"z", "n":"ň", "r":"ř", "ch":"š", "t":"ť"}
soft_to_hard = {"c":"k", "ď":"d","z":"h", "ň":"n", "ř":"r", "š":"ch", "ť":"t"}
long_to_short = {"á":"a", "é":"e", "í":"i", "ů":"o", "ou":"u", "ý":"y", "ú" : "u"}
short_to_long = {"a":"á", "e":"é", "i":"í", "o":"ů", "u":"ou", "y":"ý"}

# helper functions
def italics(string):
	return "\x1B[3m" + string + "\x1B[23m"

def get_val_from_dict(d, key):
	'''function that retrieves value at <key> from <map> via get(). defaults to <key> as value.'''
	return d.get(key, key)

# functions to change specific letters/digraphs
def get_short_vowel(long_vowel):
	'''retrieves the corresponding short vowel of <long_vowel>'''
	# FIXME: there is ambiguity from key 'u' since it can lead to either long ou or ú. for now it is ou->u only.
	# ú is only present at the beginning of words
	return get_val_from_dict(long_to_short, long_vowel)

def get_long_vowel(short_vowel):
	'''retrieves the corresponding long vowel of <short vowel>'''
	return get_val_from_dict(short_to_long, short_vowel)

def get_hard_consonant(soft_consonant):
	'''retrieves the corresponding hard consonant of <soft_consonant>'''
	# FIXME: there is ambiguity from key 'z' since it can lead to either hard g or h. for now it is z->h only.
	# g is mostly in foreign words/loanwords anyway
	return get_val_from_dict(soft_to_hard, soft_consonant)

def get_soft_consonant(hard_consonant):
	'''retrieves the corresponding soft consonant of <hard_consonant>'''
	return get_val_from_dict(hard_to_soft, hard_consonant)

def isvowel(letter):
	'''determines if <letter> is a vowel'''
	return re.search(vowel, letter) != None

def isconsonant(letter):
	'''determines if <letter> is a consonant'''
	return re.search(consonant, letter) != None

def issyllabic(letter):
	'''dteermines if <letter> is a syllabic consonant'''
	return re.search(syllabic_consonant, letter) != None

def get_vowel(stem):
	'''returns the contained vowels in string <stem> as a list->string'''
	return str(''.join([letter for letter in stem if isvowel(letter)]))

def get_consonant(stem):
	'''returns the contained consonants in string <stem> as a list->string'''
	return str(''.join([letter for letter in stem if isconsonant(letter)]))

def contains_vowel(string):
	'''determines whether <string> contains czech vowels'''
	#return re.search("(" + vowel + ")", string) != None
	return get_vowel(string) != ""

# regex-conversion mappings
regex_conversion = {"soft" : (soft_consonant, get_hard_consonant), "hard" : ("(ch)|" + hard_consonant, get_soft_consonant),
					"short" : (short_vowel, get_long_vowel), "long" : (long_vowel, get_short_vowel) }
def get_pattern_function(pattern_type):
	''' Returns corresponding regex pattern and conversion function as a tuple'''
	ret = get_val_from_dict(regex_conversion, pattern_type)
	return ret if ret != pattern_type else ("^$", None)

# BUG: converts 2nd-to last and so forth if others don't prior match pattern.
def convert_last_match(word, pattern_type):
	'''replaces last occurring match of <pattern_type> in <word> with converted value based from <pattern_type>'''
	ret = word
	(pattern, conversion) = get_pattern_function(pattern_type)

	# separate into phonemes
	phonemes  = [match[0] for match in re.findall(phoneme, word)]

	# find last occurrence of the pattern within phonemes to substitute
	phonemes.reverse()
	match = re.search(pattern, "".join(phonemes))
	if match is not None:
		match = match[0]
		if match in phonemes:
			idx = phonemes.index(match) 
			phonemes[idx] = conversion(match)
			phonemes.reverse()
			ret = "".join(phonemes)
	return ret
						  
def lengthen(stem):
	'''lengthens short vowel in <stem>'''
	return convert_last_match(stem, "short")

def shorten(stem):
	'''shortens long vowel in <stem>'''
	return convert_last_match(stem, "long")

def soften(stem):
	'''softens the final hard consonant in <stem>'''
	return convert_last_match(stem, "hard")

def harden(stem):
	'''hardens the final soft consonant in <stem>'''
	return convert_last_match(stem, "soft")

def fix_spelling(word):
	'''fixes spelling of soft consonants ď, ť, and ň  aside soft vowels i, í, and ě in <word>'''
	if (soft_matches := re.findall("(" + soft_consonant + soft_vowel + ")", word)):
		for match in soft_matches:
			# make e->ě if not preceded by ď, ť, or ň
			consonant = match[0]
			vowel = "e" if match[1]== "ě" else match[1]
			
			if re.search("[ďťň]", match[0]):
				consonant = harden(match[0])
				vowel = match[1]
			# replace consonant and vowel
			word = re.sub(match, consonant + vowel, word)
	return word

# helper class
class Syllables:
	def __init__(self, word):
		# separate into phonemes
		phonemes  = [match[0] for match in re.findall(phoneme, word)]

		# construct the syllables from the given word
		self.syllable_list = [] # tuples of (syllable, has_syllabic)
		self._construct_syllable_list(phonemes)
		
	def _construct_syllable_list(self, phonemes):
		syllable_string = ""
		has_vowel = False
		has_syllabic = False
		for phoneme in phonemes:
			if isvowel(phoneme):
				if has_vowel:
					# syllable is complete
					self.syllable_list.append((syllable_string, has_syllabic))
					has_vowel = False
					has_syllabic = False
					syllable_string = ""
				syllable_string += phoneme
				has_vowel = True
				has_syllabic = False
			elif issyllabic(phoneme):
				has_syllabic = not has_vowel
				syllable_string += phoneme
			elif isconsonant(phoneme):
				if has_vowel or has_syllabic:
					# syllable is complete
					self.syllable_list.append((syllable_string, has_syllabic))
					has_vowel = False
					has_syllabic = False
					syllable_string = ""
				syllable_string += phoneme

		# there may be trailing phonemes
		if len(syllable_string) > 0:
			# put trailing consonants onto current syllable
			if not has_vowel and not has_syllabic and len(self.syllable_list) > 0:
				new_syllable = (self.syllable_list[-1][0] + syllable_string, self.syllable_list[-1][1])
				self.syllable_list[-1] = new_syllable
			# otherwise make as new syllable
			else:
				has_syllabic = False
				self.syllable_list.append((syllable_string, has_syllabic))

	# utilities	
	def _get_syllable_at(self, idx):
		valid_cond = (idx < 0 and abs(idx) <= len(self.syllable_list)) or (idx < len(self.syllable_list))
		return self.syllable_list[idx] if valid_cond else ("", False)

	def inspect_syllable(self, idx):
		'''returns syllable string at indicated <idx>'''
		return self._get_syllable_at(idx)[0]
	
	def is_syllabic(self, idx):
		'''returns is_syllabic state at indicated <idx>'''
		return self._get_syllable_at(idx)[1]

	def contains_cluster(self, idx):
		'''determines if syllable at <idx> contains a consonant cluster'''
		return re.search(cluster, self.inspect_syllable(idx))
	
	def contains_vowel(self, idx):
		'''determines if syllable at <idx> contains any vowels'''
		return contains_vowel(self.inspect_syllable(idx))