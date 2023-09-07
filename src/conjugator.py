import src.verb_utils as vutils
import src.conjugator_utils as conjutils
import verbs as v
############## MAIN PROGRAM ####################

# TODO: make this a loop to continue conjugating verbs
irregular_verbs = conjutils.get_irregular_verbs()
word = input("please enter a verb infinitive: ")
verb_match = conjutils.linear_search(word, irregular_verbs)
not_root = conjutils.get_prefixes(word)
root = word[len(not_root):]
verb = None
if verb_match != []:
	verb = conjutils.check_match(verb_match, word, root)
if not verb:
	verb = conjutils.determine_verb(word, root)
if verb:
	verb.conjugate()
