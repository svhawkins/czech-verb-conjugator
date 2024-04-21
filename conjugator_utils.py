""""
Conjugation Utilites

Provides functions to ease in finding a verb's
proper Verb class as well as other other class-agnostic features, which affect tense conjugations:
	1. concrete or abstract
	2. verbal aspect (TODO)
"""

import re
import verbs as v
import verb_utils as vutils
from enum import IntEnum
import os

class IrregularIdx(IntEnum):
	RGX_INFINITIVE = 0
	CONJUGATION_CLASS = 1
	PRESENT_STEM = 2
	PAST_STEM = 3
	IMPERATIVE_STEM = 4
	#PASSIVE_STEM = 5
	#TRANSGRESSIVE_STEM = 6

# dictionaries
int_to_verb_class = { 1 : v.Class1, 2 : v.Class2, 3: v.Class3, 4: v.Class4 }
consonant_to_class= {"c" : v.Class4_ct, "s" : v.Class4_st, "z" : v.Class4_zt }

def get_irregular_verbs() -> list:
	"""
	Retrieve the irregular verb constructions from the file and store them as a list of tuples.
	
	Each line becomes its own tuple, with each element within each tuple being the following:
	0 (IrregularIdx.RGX_INFINITIVE): The irregular verb's infinitive
	1 (IrregularIdx.CONJUGATION_CLASS): The irregular verb's conjugation class (determines which literal Verb class to construct).
	2 (IrregularIdx.PRESENT_STEM): The irregular verb's present stem for present tense conjugations.
	3 (IrregularIdx.PAST_STEM): The irregular verb's past participle stem for past tense and conditional mood conjugations.
	4 (IrregularIdx.IMPERATIVE_STEM): The irregular verb's imperative stem for imperative mood conjugations.

	Return:
		list[tuple[str, int, str, str, str]]
	"""
	file = open(os.environ["VERB_DATA_DIR"] + "/" + "irregular.txt", "r")
	lines = file.readlines()
	file.close()

	verbs = []
	for line in lines:
		verb = (line.rstrip("\n")).split(",") # remove the newline as well
		verb[IrregularIdx.CONJUGATION_CLASS] = int(verb[IrregularIdx.CONJUGATION_CLASS]) # from str to int
		verb = tuple(verb)
		verbs.append(verb)
	return verbs

def get_concrete_verbs() -> list:
	"""
	Retrieve the concrete* verbs from file, store as list.
	*concrete verbs being imperfective verbs with irregular future forms, taking prefix po- or its variant pů-

	Return:
		list[str]
	"""
	file = open(os.environ["VERB_DATA_DIR"] + "/" + "concrete.txt", "r")
	lines = file.readlines()
	file.close()
	verbs = [ line.rstrip("\n") for line in lines ]
	return verbs

def find_verb_matches(word : str, verbs : list) -> list:
	"""
	Return all verb-tuples that end with <word>.
	
		Construct a list of matches by comparing <word> with the infinitive in <verbs> and if they
		end identically. If so, it is added to the list.

		Parameters:
			word: str --> string to compare the irregular verbs to.
			verbs: list[tuple[str, int, str, str, str]] --> list holding the irregular verb information.
		Return:
			list[tuple[str, int, str, str, str]] --> list of irregular verb-tuples that match the word-ending regex pattern.
	"""
	matches = [verb for verb in verbs if re.findall("(" + verb[IrregularIdx.RGX_INFINITIVE] + ")" + "$", word) != []]
	return matches

def is_concrete_verb(word : str, verbs : list) -> bool:
	"""Determines if given word is concrete by checking list membership"""
	non_negative_verb = word[2:] if word[:2] == "ne" else word
	return non_negative_verb in verbs

def verb_class(word : str, match : tuple, is_concrete : bool = False, is_perfective : bool = False) -> v.Verb:
	"""Return corresponding base class Verb (Class 1-4 ONLY) from provided <class_num>"""
	return vutils.get_val_from_dict(int_to_verb_class,
								 	match[IrregularIdx.CONJUGATION_CLASS])(infinitive = word, stems = match, is_concrete = is_concrete, is_perfective = is_perfective)

def construct_verb(word : str, match : tuple, is_concrete : bool = False, is_perfective : bool = False) -> v.Verb:
	"""Construct a Verb object manually by overwriting stem values from __init__()."""
	verb = verb_class(word, match, is_concrete, is_perfective)
	return verb

# removes ambiguities in irregular matches and constructs from the correct match
def disambiguate_verb(match : list , word : str, root : str, is_concrete : bool = False, is_perfective : bool = False) -> tuple:
	"""
	Disambiguates between an irregular verb match and a regular verb, constructing the irregular verb.
	Returns tuple since stát can have 2 conjugations.
	"""
	verb = v.Verb()
	verb2 = None
	m = match[0][IrregularIdx.RGX_INFINITIVE]
	if m == "být" and word == "být" or word == "nebýt":
		verb = v.Byt(infinitive = word, is_concrete = is_concrete, is_perfective = is_perfective)
	
	# cases where the prefix removal got overzealous and they took too much off so there's now a bad root
	elif ((m == "zát" or m == "zábst") and re.findall("((zát)|(zábst))$", word)) or \
		 (m == "začít") and re.findall("(začít)$", word) or \
		 (m == "stít" and root == "tít") or \
	     (m == "sníst") and re.findall("(sníst)$", word) or \
		 (m == "spát") and re.findall("(spát)$", word) or \
		 (m == "vědět") and re.findall("(vědět)$", word) or \
		 ((m == "zet") and re.findall("(zet)$", word) and "t" == root) or \
		 ((m == "stat") and ("tat" == root or re.findall("(zůstat)$", word))) or \
		 ((m == "skákat") and ("kákat" == root or re.findall("(skákat)$", word))) or \
	     ((m == "vzít") and ("ít" == root or re.findall("(vzít)$", word))):
		 verb = construct_verb(word, match[0], is_concrete, is_perfective)

	# stát has multiple matches
	elif ((m == "stat" or re.findall("(((při)|(v))st[aá]t)$", word)) and (root == "tat" or root == "tát")):
		# construct 1st
		verb = construct_verb(word, match[0], is_concrete, is_perfective)
	elif m == "stát":
		if word == "stát" or word == "nestát":
			# construct both matches
			verb2 = construct_verb(word, match[1], is_concrete, is_perfective)
			verb = construct_verb(word, match[0], is_concrete, is_perfective)
		else:
			# construct the 2ND match
			verb = construct_verb(word, match[1], is_concrete, is_perfective)

	# regular verbs that have either irregular verb or verb of different class as a substring
	# (vice versa as well)
	# aka 'unmatch'
	elif(m == "dít" and re.findall("((bz)|[bzr](dít))$", word)) or \
		(m == "pět") and re.findall("(úpět)$", word) or \
		(m == "klít") and re.findall("(sklít)$", word):
	 	verb = None
	elif (m != root ): # non-exact matches are considered regular and are to be classified.
		verb = None
	else:
		verb = construct_verb(word, match[0], is_concrete, is_perfective)
	return (verb, verb2)

def determine_verb_class(word : str, root : str, is_concrete : bool = False, is_perfective : bool = False) -> v.Verb:
	"""Construct the proper Verb class based on the ending of <root> formed from <word>."""
	verb  = None

	# NOTE: all the matches have the [0] subscription to access item in Match object/array
	# 1. check for -at/-át ending
	if at_match := re.search("([aá]t)$", word):
		if (ovat_match := re.search("(ovat)$", word)) and not re.search("chovat$", word):
			verb = v.Class2_ovat(word, ovat_match[0], is_concrete = is_concrete, is_perfective = is_perfective)
		elif (apat_match := re.search("([aá][bpmz]at)$", word)) and not re.search("(papat|chlámat)", word):
			verb = v.Class4_apat(word, apat_match[0], is_concrete = is_concrete, is_perfective = is_perfective)
		elif (cluster_at_match := re.search("((" + vutils.consonant + ")+[pvrlhž][áa]t)$", word)) \
			and not re.search("(hr[áa]t)|([pv]l[aá]t)$", word):
			verb = v.Class4_cluster(word, cluster_at_match[0], is_concrete = is_concrete, is_perfective = is_perfective)
		elif (long_at_match := re.search("([ltkvsmrř]át)$", word)) and  \
			 (not re.findall("([tl]kát)|([p]tát)$", word)) and \
			 (vutils.Syllables(root).is_monosyllabic() == True):
			verb = v.Class2_at(word, long_at_match[0], is_concrete = is_concrete, is_perfective = is_perfective)
		else:
			verb = v.Class1_at(word, at_match[0], is_concrete = is_concrete, is_perfective = is_perfective)
	
	# 2. check for -ít/-ýt ending
	elif ityt_match := re.search("([íý]t)$", word):
		if (rit_match := re.search("(řít)$", word)) and not re.search("(zřít)$", word):
			verb = v.Class4_rit(word, rit_match[0], is_concrete = is_concrete, is_perfective = is_perfective)
		elif (cluster_match := re.search("((" + vutils.consonant + "){2,}ít)$", root)) \
			and not re.search("((blít)|(hnít))$", word):
			verb = v.Class3_cluster(word, cluster_match[0], is_concrete = is_concrete, is_perfective = is_perfective)
		elif (cluster_match := re.search("((zdít)(znít)|(snít))$", word)):
			verb = v.Class3_cluster(word, cluster_match[0], is_concrete = is_concrete, is_perfective = is_perfective)
		else:
			verb = v.Class2_ityt(word, ityt_match[0], is_concrete = is_concrete, is_perfective = is_perfective)
	
	# 3. check for -out ending
	elif out_match := re.search("(out)$", word):
		if nout_match := re.search("(nout)$", word):
			verb = v.Class4_nout(word, nout_match[0], is_concrete = is_concrete, is_perfective = is_perfective)
		else:
			verb = v.Class2_out(word, out_match[0], is_concrete = is_concrete, is_perfective = is_perfective)
	
	# 4. check for -it/-et/-ět ending
	elif itet_match := re.search("([ieě]t)$", word):
		verb = v.Class3_itet(word, itet_match[0], is_concrete = is_concrete, is_perfective = is_perfective)
	
	# 5. check for -ct/-st/-zt endings
	elif szct_match := re.search("((" + vutils.long_vowel + ")[csz]t)$", word):
		thematic_consonant = szct_match[0][-2] # get the consonant before the -t
		verb = (vutils.get_val_from_dict(consonant_to_class, thematic_consonant))(word, szct_match[0], is_concrete = is_concrete, is_perfective = is_perfective)
	
	# 6. no match has been found...
	else:
		print("No verb class pattern corresponding with given verb.")
		verb = None
	return verb

def get_prefixes() -> str:
	"""Retrieve the prefixes from the file as a single regex expression."""
	file = open(os.environ["VERB_DATA_DIR"] + "/" + "prefix.txt", "r")
	lines = file.readlines()
	file.close()

	# append each line (excluding the new line) within an OR capture
	prefixes = "^("
	for line in lines:
		prefixes += "(" + line[:-1] + ")|"
	prefixes =  prefixes[:-1] + ")" # remove last/redundant "|"
	return prefixes


def get_last_prefix(matches : tuple):
	"""Return the last non-empty element in tuple <matches>."""
	prefix_match = ""
	for match in matches:
		if match:
			prefix_match = match # the previous match is overwritten.
	return prefix_match


def get_prefix(word : str, prefixes_expr: str) -> tuple:
	"""
	Extract the prefixes from provided <word>.
	
	Continuously appends consecutive prefixes to string <prefixes> in order to obtain
	a string containing all of the contained prefixes within <word> that
	adhere to the <prefixes> regex pattern. As a result, as <prefixes> expands,
	the remaining length of <word> decreases, eventually reducing it to its
	unprefixed root.

	Parameters:
		word : str --> word to extract the prefixes from.
		prefixes_expr : str -->  regex expression containing all valid verbal prefixes.
	Return:
		tuple[str, str] --> [0]: The resulting string from appending all of the consecutively found prefixes in <word>.
							[1]: The resulting string from removing the found prefixes from <word> within <word> (the root).
	"""
	prefixes = ""
	prefix = ""
	root = ""
	while(1):
		# keep extracting last prefix matched until all have been found.
		word = word[len(prefix):]
		found_prefixes = re.findall(prefixes_expr, word)
		if found_prefixes == []:
			break
		found_prefixes = found_prefixes[0] # list is a singleton
		prefix = get_last_prefix(found_prefixes)
		prefixes += prefix
	root = word
	return (prefixes, root)