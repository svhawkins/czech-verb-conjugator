# functions and classes for verb utilities that the Verb classes often use

import re

# regex patterns
short_vowel = "[aeiouy]"
long_vowel = "[áéíóúůý]|(ou)"
soft_vowel = "[ěií]"
hard_consonant = "[dghknrst]"
neutral_consonant = "[bmpvfqwx]"
soft_consonant = "[cčďjlňřšťzž]"
digraph = "(ch)|(st)|(št)|(ct)|(čt)"
consonant = hard_consonant + "|" + neutral_consonant + "|" + soft_consonant + "|" + digraph
vowel = short_vowel + "|" + long_vowel + "|" + soft_vowel

# dictionaries for letter mappings
hard_to_soft = {"k":"c", "d":"ď", "g":"z", "h":"z", "n":"ň", "r":"ř", "ch":"š", "t":"ť"}
soft_to_hard = {"c":"k", "ď":"d","z":"h", "ň":"n", "ř":"r", "š":"ch", "ť":"t"}
long_to_short = {"á":"a", "é":"e", "í":"i", "ů":"o", "ou":"u", "ý":"y"}
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
	return get_val_from_dict(long_to_short, long_vowel)

def get_long_vowel(short_vowel):
	'''retrieves the corresponding long vowel of <short vowel>'''
	return get_val_from_dict(short_to_long, short_vowel)

def get_hard_consonant(soft_consonant):
	'''retrieves the corresponding hard consonant of <soft_consonant>'''
	# FIXME: there is ambiguity from key 'z' since it can lead to either hard g or h. for now it is z->h only.
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

def lengthen(stem):
	'''lengthens short vowel in <stem>'''
	# FIXME: this can be improved to not only work for vowel-final strings.
	# consonants at the end of the word
	# more than one vowel...
	vowel = get_vowel(stem)
	stem_no_vowel = stem[:-len(vowel)] if len(vowel) > 0 else stem[:len(stem)]
	return stem_no_vowel + get_long_vowel(vowel)

def shorten(stem):
	'''shortens long vowel in <stem>'''
	# FIXME: this can be improved to not only work for vowel-final strings.
	# consonants at the end of the word
	# more than one vowel...
	vowel = get_vowel(stem)
	stem_no_vowel = stem[:-len(vowel)] if len(vowel) > 0 else stem[:len(stem)]
	return stem_no_vowel + get_short_vowel(vowel)

def soften(stem):
	'''softens the final hard consonant in <stem>'''
	# FIXME: this can be improved upon
	consonant = get_consonant(stem)
	stem_no_consonant = stem[:-len(consonant)] if len(consonant) > 0 else stem[:len(stem)]
	return stem_no_consonant + get_soft_consonant(consonant)

def harden(stem):
	'''hardens the final soft consonant in <stem>'''
	# FIXME: this can be improved upon
	consonant = get_consonant(stem)
	stem_no_consonant = stem[:-len(consonant)] if len(consonant) > 0 else stem[:len(stem)]
	return stem_no_consonant + get_hard_consonant(consonant)

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


