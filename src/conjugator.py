# TODO: imports being effing annoying.
import src.conjugator_utils as conjutils

# TODO: actually make this a 'main' function
############## MAIN PROGRAM ####################

irregular_verbs = conjutils.get_irregular_verbs()
prefixes = conjutils.get_prefixes()

# TODO: check that a verb is a verb of motion

# TODO: add breaking condition!
while(1):
	word = input("please enter a verb infinitive: ")
	if word == "q":
		break

	matches = conjutils.find_verb_matches(word, irregular_verbs)
	(not_root, root) = conjutils.get_prefix(word)

	verb = None
	if matches != []:
		verb = conjutils.disambiguate_verb(matches, word, root)
	if not verb:
		verb = conjutils.determine_verb_class(word, root)
	if verb:
		verb.conjugate()
		# TODO: display the conjugation
