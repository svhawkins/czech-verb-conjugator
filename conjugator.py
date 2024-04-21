import conjugator_utils as conjutils

############## MAIN PROGRAM ####################

irregular_verbs = conjutils.get_irregular_verbs()
concrete_verbs = conjutils.get_concrete_verbs()
prefixes = conjutils.get_prefixes()

while(1):
	word = input("enter a verb infinitive (or 'q' to quit): ")
	if word == "q":
		break

	matches = conjutils.find_verb_matches(word, irregular_verbs)
	(not_root, root) = conjutils.get_prefix(word, prefixes)
	is_concrete = conjutils.is_concrete_verb(word, concrete_verbs)

	# TODO: determine if perfective
	is_perfective = False

	verb = None
	verb2 = None
	if matches != []:
		(verb, verb2) = conjutils.disambiguate_verb(matches, word, root, is_concrete, is_perfective)
	if not verb:
		verb = conjutils.determine_verb_class(word, root, is_concrete, is_perfective)
	if verb:
		verb.conjugate()
		# TODO: display the conjugation (prettily)
		print(verb.get_table())

		if verb2 is not None:
			verb2.conjugate()
			print(verb2.get_table())
