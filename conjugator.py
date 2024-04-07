import conjugator_utils as conjutils

# TODO: actually make this a 'main' function
############## MAIN PROGRAM ####################

irregular_verbs = conjutils.get_irregular_verbs()
prefixes = conjutils.get_prefixes()

# TODO: check that a verb is a verb of motion

while(1):
	word = input("enter a verb infinitive (or 'q' to quit): ")
	if word == "q":
		break

	matches = conjutils.find_verb_matches(word, irregular_verbs)
	(not_root, root) = conjutils.get_prefix(word, prefixes)

	verb = None
	if matches != []:
		verb = conjutils.disambiguate_verb(matches, word, root)
	if not verb:
		verb = conjutils.determine_verb_class(word, root)
	if verb:
		verb.conjugate()
		# TODO: display the conjugation (prettily)
		print(verb.get_table())
