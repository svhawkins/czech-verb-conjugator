# functions and classes for verb utilities that the Verb classes often use

import re
# regex patterns
long_vowel = "[áéíúůý]"
consonant = "[bcčdďfghjklmnňpqrřsštťvwxzž]"
neutral_consonant = "[bmpv]"
soft_consonant = "[cčďjlňřšťž]"
digraph = "(ch)|(st)|(št)|(ct)|(čt)"

def italics(string):
	return "\x1B[3m" + string + "\x1B[23m"


#### functions to change/alter spellings ####

### vowel functions ###
def get_short_vowel(_long_vowel):
	"""returns the short vowel form of given long vowel"""
	ret = ""
	if _long_vowel == "á":
		ret = "a"
	elif _long_vowel == "é":
		ret == "e"
	elif _long_vowel == "í":
		ret == "i"
	elif _long_vowel == "ý":
		ret = "y"
	elif _long_vowel == "ú" or _long_vowel == "ů" or _long_vowel == "ou":
		ret = "u"
	# FIXME: "Ů" is a long vowel for O, not U.
	# BUG: add case for not long vowel -> nothing should happen
	# WHERE'S get_long_vowel()?
	return ret

def isvowel(letter):
	"""determines if given letter is a czech vowel (can be digraph)"""
	vowel = False
	if re.search("([aáeéěiíoóuúůyý]|(ou))", letter):
		vowel = True
	return vowel

def get_vowel(stem):
	"""returns the list of czech vowels contained within the stem string (as a string)"""
	# TODO: this can be refactored with list comprehension
	vowel_list = list("")
	for i in range(len(stem) -1 , 0, -1):
		if isvowel(stem[i]):
			vowel_list.insert(0, stem[i])
	vowel = ""
	for i in range(0, len(vowel_list)):
		x += vowel_list[i]
	return x

def contains_vowel(string):
	"""determines whether a given string contains a czech vowel (long or short)"""
	# TODO: this can be refactored into a single regex statement
	has_vowel = False
	for i in range(0, len(string)):
		if isvowel(string[i]):
			has_vowel = True
	return has_vowel

def lengthen(stem):
	""""lengthens the provided short stem vowel, returning the modified string"""
	# TODO: this can be refactored with regex replace and using lengthen(short vowel)
	vowel = get_vowel(stem)
	new_stem = stem[:-len(vowel)]
	new_vowel = ""
	if vowel == "a":
		new_vowel = "á"
	elif vowel == "e":
		new_vowel = "é"
	elif vowel == "i":
		new_vowel = "í"
	elif vowel == "o":
		new_vowel = "ů"
	elif vowel == "u":
		new_vowel = "ou"
	elif vowel == "y":
		new_vowel = "ý"
	new_stem += new_vowel
	return new_stem

def shorten(stem):
	"""shortens the provided long stem vowel, returning the modified string"""
	# TODO: this can be refactored with regex replace and shorten(long vowel)
	vowel = get_vowel(stem)
	new_stem = stem[:-len(vowel)]
	new_vowel = ""
	if vowel == "á":
		new_vowel = "a"
	elif vowel == "é":
		new_vowel = "e"
	elif vowel == "í":
		new_vowel = "i"
	elif vowel == "ou":
		list(new_stem).pop() # stem was 'no' instead of just 'n'
		new_vowel = "u"
	elif vowel == "ů":
		new_vowel = "o"
	elif vowel == "ý":
		new_vowel = "y"
	new_stem += new_vowel
	return new_stem


### consonant functions ###
def soften(stem):
	"""softens the (hard) stem by adding the háček"""
	# TODO: refactor to pass in only the final stem consonant (make 2 functions)
	new_stem = ""
	if stem[-1] == "t":
		new_stem = stem[:-1] + "ť"
	elif stem[-1] == "d":
		new_stem = stem[:-1] + "ď"
	elif stem[-1] == "n":
		new_stem = stem[:-1] + "ň"
	else:
		new_stem = stem
	return new_stem

def harden(stem):
	"""hardens the (soft) stem by adding the háček"""
	# TODO: refactor to pass in only the final stem consonant (make 2 functions)
	new_stem = ""
	if stem[-1] == "ť":
		new_stem = stem[:-1] + "t"
	elif stem[-1] == "ď":
		new_stem = stem[:-1] + "d"
	elif stem[-1] == "ň":
		new_stem = stem[:-1] + "n"
	else:
		new_stem = stem
	return new_stem

def fix_spelling(word):
	"""fixes spelling of word with e or ě after hardening or softening of final stem consonant"""
	# TODO: can be refactored to use previously defined functions, and better naming
	# soft consonants and ě, i, or í
	x = re.findall("([cčďjlňřsšťzž][ěií])", word)
	if x == []:
		return word
	first_letter = x[0][0]
	second_letter = "e" if x[0][1] == "ě" else x[0][1]
	if first_letter == "ď":
		first_letter = "d"
	elif first_letter == "ť":
		first_letter = "t"
	elif first_letter == "ň":
		first_letter = "n"
	word = re.sub(x[0], first_letter + second_letter, word)
	return word


