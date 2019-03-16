Dimensions query plan:

	query whole publications database for author name as it appears on faculty file
	
	if response length is 0:
		author DNE
	
	otherwise loop through all returned authors and find match by first_name and last_name:

		if the current author has a field 'research_orgs':

			if found return id and UR affiliation

			if loop hasn't hit limit of 20 at its end:
				author has ID but NOT UR AFFILIATED 

		otherwise the current author has NO AFFILIATIONS at all
	
	if loop hit limit of 20 and the affiliation is still UNDETERMINED:
		author has TOO MANY
	
	if author hasn't been found at the end or there was a JSON decoding error:
		author is UNDETERMINED