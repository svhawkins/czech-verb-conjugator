import re
import verbs as v

# regex patterns
long_vowel = "[áéíýů]"
consonant = "[bcčdďfghjklmnňpqrřsštťvwxzž]"

# indexing constants
RGX_INFINITIVE = 0
CONJUGATION_CLASS = 1
PRESENT_STEM = 2
PAST_STEM = 3
IMPERATIVE_STEM = 4

# gets irregular verbs from .txt files by constructing 2 lists: a list for only the verbs ad a list (of lists) for that verb's content
def get_irregular_verbs():
	file = open("irregular.txt", "r")
	lines = file.readlines()
	file.close()

	verbs = []
	words = []
	for line in lines:
		words = line.split()
		words[CONJUGATION_CLASS] = int(words[CONJUGATION_CLASS])
		verbs.append(words)
	return verbs

def linear_search(word, verbs):
	matches = []
	for verb in verbs:
		x = re.findall("(" + verb[RGX_INFINITIVE] + ")" + "$", word)
		if x != []:
			matches.append(verb)
	return matches

# constructs the proper base clas verb from corresponding integer
def verb_class(word, class_num):
	if class_num == 1:
		verb = v.Class1(word)
	elif class_num == 2:
		verb = v.Class2(word)
	elif class_num == 3:
		verb = v.Class3(word)
	elif class_num == 4:
		verb = v.Class4(word)
	return verb

# constructs the matching irregular verb by manual setting
def construct_verb(word, match):
	remainder = word[:-len(match[RGX_INFINITIVE])]
	verb = v.Verb()
	verb = verb_class(word, match[CONJUGATION_CLASS])
	verb.set_present_stem(remainder + match[PRESENT_STEM])
	verb.set_past_stem(remainder + match[PAST_STEM])
	verb.set_imperative_stem(remainder + match[IMPERATIVE_STEM])
	return verb

# removes ambiguities in irregular matches and constructs from the correct match
def check_match(match, word, root):
	verb = v.Verb()
	m = match[0][RGX_INFINITIVE]
	if m == "být" and word == "být" or word == "nebýt":
		verb = v.Byt(word)
	elif m == "dít" and word == "dít":
		# set the stems and use the appropriate constructor
		verb = construct_verb(word, match[0])
	elif m == "stat" or word == "vstát":
		# construct 1st
		verb = construct_verb(word, match[0])
	elif m == "stát":
		if word == "stát":
			# construct both matches
			verb2 = construct_verb(word, match[1])
			verb2.conjugate()
			verb = construct_verb(word, match[0])
		else:
			# construct the 2ND match
			verb = construct_verb(word, match[1])

	# regular verbs that have irregular verb as a substring
	elif (m == "bát" and re.findall("dbát$", word)) or (m == "tát" and re.findall("ptát$", word)):
		verb = None
	elif (m == "kat" and (root != "kat" or re.findall("sekat$", word)) or (m == "kát" and root != "kát")):
		verb = None
	elif (m == "tít" and re.findall("(sklít|dštít|křtít)$", word)) or (m == "stít" and re.findall("mstít$", word)):
		verb = None
	elif m == "pět" and re.findall("(čpět)$", word):
		verb = None
	else:
		verb = construct_verb(word, match[0])
	return verb


# determines verb class and sets the right forms for slightly irregular cases
def determine_verb(word, root):
	verb  = v.Verb()
	x = []

	# chovat is class1 otherwise class 2
	if (x := re.findall("ovat$", root)) and not re.search("chovat$", word):
		verb = v.Class2_ovat(word, x[0])
	elif x := re.findall("ít|ýt$", word):
		# řít endings, přít added manually since without t looks like pří prefix and not part of 'root'
		if y := re.findall("řít$", word):
			# class4 general constructor. manually set stems. ...řu, ...řel, ...ři, ending ít
			verb = v.Class4(word, x[0])
			stem = word[:-len(x[0])]
			verb.set_stem(stem)
			verb.set_present_stem(stem)
			verb.set_past_stem(stem + "el")
			verb.set_imperative_stem(stem + "i")
		# cluster rule
		elif re.search(consonant + "{2,}ít$", root):
			# class3 general constructor. manually set stems. past thematic vowel is e if stem ends in l, if ends in v/d/n/b: ě, +i to stem in imperative, present stem is stem
			verb = v.Class3(word, x[0])
			stem = word[:-2]
			verb.set_stem(stem)
			verb.set_present_stem(stem)
			past = "el" if stem[-1] == "l" else ("ěl" if stem[-1] == "v" or stem[-1] == "d" or stem[-1] == "n" else "il")
			verb.set_past_stem(stem + past)
			verb.set_imperative_stem(stem + "i")
		else:
			verb = v.Class2_ityt(word, x[0])
	elif x := re.findall("at|át$", root):
		if re.search("ápat$", root):
			# class4 general constructor. manusally set stems. present stem is sans at, past: t->l, imperative: at->ej
			verb = v.Class4(word, x[0])
			stem = word[:-len(x[0])]
			verb.set_stem(stem)
			verb.set_present_stem(stem)
			verb.set_past_stem(stem + "al")
			verb.set_imperative_stem(stem + "ej")
		else:
			verb = v.Class1_at(word, x[0])
	elif x := re.findall("it|ět|et$", root):
		verb = v.Class3_itet(word, x[0])
	elif x := re.findall("nout$", root):
		verb = v.Class4_nout(word, x[0])
	elif bool(x := re.findall(long_vowel + "ct$", root)) or bool(x := re.findall("ouct$", root)):
		verb = v.Class4_ct(word, x[0][-2:])
	elif x := re.findall(long_vowel + "st$", root):
		verb = v.Class4_st(word, x[0][-2:])
	elif x := re.findall(long_vowel + "zt$", root):
		verb = v.Class4_zt(word, x[0][-2:])
	elif x := re.findall("out$", root):
		# -out ending. class2 general. manually set stems: present uj, past ul, imperative uj
		verb = v.Class2(word, x[0])
		stem = word[:-len(x[0])]
		verb.set_stem(stem)
		verb.set_present_stem(stem + "uj")
		verb.set_past_stem(stem + "ul")
		verb.set_imperative_stem(stem + "uj")
	else:
		print("none of the above")
		verb = None
	return verb

# returns .txt as a single regex string to represent the prefixes a verb may begin with
def prefix_regex():
	file = open("prefix.txt", "r")
	lines = file.readlines()
	file.close()

	prefixes = "^("
	for line in lines:
		prefixes += "(" + line[:-1] + ")|"
	prefixes =  prefixes[:-1] + ")"
	return prefixes


# returns the non-empty element in a regex match list
def get_prefix(matches):
	ret = ""
	for match in matches:
		if match:
			ret = match
	return ret

# returns the prefixes within the verb
def get_prefixes(verb):
	prefixes = prefix_regex()
	word = verb
	not_root = ""
	prefix = ""
	while(1):
		word = word[len(prefix):]
		x = re.findall(prefixes, word)
		if not x:
			break
		prefix = get_prefix(x[0])
		not_root += prefix
	return not_root


############## MAIN PROGRAM ####################
irregular_verbs = get_irregular_verbs()
word = input("please enter a verb infinitive: ")
verb_match = linear_search(word, irregular_verbs)
not_root = get_prefixes(word)
root = word[len(not_root):]
verb = None
if verb_match != []:
	verb = check_match(verb_match, word, root)
if not verb:
	verb = determine_verb(word, root)
if verb:
	verb.conjugate()
