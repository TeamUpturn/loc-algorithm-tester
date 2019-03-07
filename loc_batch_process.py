"""
Implementation of the proposed Missouri Medicare Levl of Care (LOC) algorithm.
For use on csv files with each survey question as a labeled column in the file.

Written Jan 28, 2019 by Emma Weil at Upturn / emma@upturn.org

Usage: argv[1] is the path/filename of csv file and argv[2] is the destination
destination file will have all new columns + old columns 

"""

import csv
import pprint
import sys
import re
	

def LOC_behavioral(client):

	e3a = int(client["E3a (page 3)"])
	e3b = int(client["E3b (page 3)"])
	e3c = int(client["E3c (page 3)"])
	e3d = int(client["E3d (page 3)"])
	e3e = int(client["E3e (page 3)"])
	e3f = int(client["E3f (page 3)"])
	j3g = int(client["J3g (page 7)"])
	j3h = int(client["J3h (page 7)"])
	j3i = int(client["J3i (page 7)"])
	n7b = int(client["N7b (page 11)"])

	new_loc_behavioral = None

	if ((n7b == 0 or n7b == 1) and
		e3a == 0 and 
		e3b == 0 and 
		e3c == 0 and 
		e3d == 0 and 
		e3e == 0 and 
		e3f == 0 and 
		j3g == 0 and 
		j3h == 0 and 
		j3i == 0):
		new_loc_behavioral = 0

	if ((n7b == 2 or n7b == 3) or
		e3a == 1 or 
		e3b == 1 or 
		e3c == 1 or 
		e3d == 1 or 
		e3e == 1 or 
		e3f == 1 or 
		j3g == 1 or 
		j3h == 1 or 
		j3i == 1):
		new_loc_behavioral = 3

	if ((n7b == 2 or n7b == 3) or
		(e3a == 2 or e3a == 3) or 
		(e3b == 2 or e3b == 3) or
		(e3c == 2 or e3c == 3) or
		(e3d == 2 or e3d == 3) or
		(e3e == 2 or e3e == 3) or
		(e3f == 2 or e3f == 3) or 
		(j3g == 2 or j3g == 3 or j3g == 4) or 
		(j3h == 2 or j3h == 3 or j3h == 4) or 
		(j3i == 2 or j3i == 3 or j3i == 4)):
		new_loc_behavioral = 6

	if ((n7b == 2 or n7b == 3) and
		((e3a == 3) or 
		 (e3b == 3) or
		 (e3c == 3) or
		 (e3d == 3) or
		 (e3e == 3) or
		 (e3f == 3) or 
		 (j3g == 3 or j3g == 4) or 
		 (j3h == 3 or j3h == 4) or 
		 (j3i == 3 or j3i == 4))):
		new_loc_behavioral = 9

	return new_loc_behavioral


def LOC_cognition(client):

	c1 = int(client["C1 (page 2)"])
	c2a = int(client["C2a (page 2)"])
	c2b = int(client["C2b (page 2)"])
	c2c = int(client["C2c (page 2)"])
	c3c = int(client["C3c (page 2)"])
	d1 = int(client["D1 (page 2)"])
	d2 = int(client["D2 (page 3)"])

	new_loc_cognition = None
	loc_cognition_trigger = "Not Present"

	if ((c1 == 0 or c1 == 1 or c1 == 2 or c1 == 3) and 
		c2a == 0 and 
		c2b == 0 and 
		c2c == 0 and 
		c3c == 0 and 
		(d1 == 0 or d1 == 1) and 
		(d2 == 0 or d2 == 1)):
		new_loc_cognition = 0

	if ((c1 == 1 or c1 == 2) and 
		(c2a == 1 or 
		 c2b == 1 or 
		 c2c == 1 or 
		 (c3c == 1 or c3c == 2) or
		 (d1 == 2 or d1 == 3 or d1 == 4) or 
		 (d2 == 2 or d2 == 3 or d2 == 4))):
		new_loc_cognition = 3

	if (c1 == 3 and 
		(c2a == 1 or 
		 c2b == 1 or 
		 c2c == 1 or 
		 (c3c == 1 or c3c == 2) or
		 d1 == 3 or 
		 d2 == 3)):
		new_loc_cognition = 6
	
	if (c1 >= 3 and (d1 == 4 or d2 == 4)):
		new_loc_cognition = 9

	# note deviation from proposed algorithm, as this is the only way to reach the c1=4 / c1=5 trigger
	if (c1 == 4 or c1 == 5):
		new_loc_cognition = 9
		loc_cognition_trigger = "Present"

	return [new_loc_cognition, loc_cognition_trigger]


def LOC_mobility(client):

	g2e = int(client["G2e (page 5)"])
	g2f = int(client["G2f (page 5)"])
	g2i = int(client["G2i (page 5)"])
	g3a = int(client["G3a (page 5)"])

	new_loc_mobility = None
	loc_mobility_trigger = "Not Present"

	if ((g2e == 0 or g2e == 1 or g2e == 2) and 
		(g2f == 0 or g2f == 1 or g2f == 2) and 
		(g2i == 0 or g2i == 1 or g2i == 2)):
		new_loc_mobility = 0

	if ((g2e == 3 or g2e == 4) or
		(g2f == 3 or g2f == 4) or
		(g2i == 3 or g2i == 4)):
		new_loc_mobility = 3

	if (g2e == 5 or g2f == 5 or g2i == 5):
		new_loc_mobility = 6

	if (g2e == 6 or g2f == 6 or g2i == 6 or g3a == 3):
		new_loc_mobility = 9
		if (g3a == 3):
			loc_mobility_trigger = "Present"

	return [new_loc_mobility, loc_mobility_trigger]


def LOC_eating(client):

	g2j = int(client["G2j (page 5)"])
	k2e = int(client["K2e (page 8)"])

	new_loc_eating = None
	loc_eating_trigger = "Not Present"

	if (g2j == 0 or k2e == 0):
		new_loc_eating = 0

	if ((g2j == 1 or g2j == 2 or g2j == 3) or 
		(k2e == 1)):
		new_loc_eating = 3

	if (g2j == 4):
		new_loc_eating = 6

	if (g2j == 5):
		new_loc_eating = 9

	if (g2j == 6):
		new_loc_eating = 9
		loc_eating_trigger = "Present"

	return [new_loc_eating, loc_eating_trigger]


def LOC_toileting(client):

	g2g = int(client["G2g (page 5)"])
	g2h = int(client["G2h (page 5)"])

	new_loc_toileting = None

	if ((g2g == 0 or g2g == 1 or g2g == 2) and 
		(g2h == 0 or g2h == 1 or g2h == 2)):
		new_loc_toileting = 0

	if ((g2g == 3 or g2g == 4) or 
		(g2h == 3 or g2h == 4)):
		new_loc_toileting = 3

	if (g2g == 5 or g2h == 5):
		new_loc_toileting = 6

	if (g2g == 6 or g2h == 6):
		new_loc_toileting = 9

	return new_loc_toileting


def LOC_bathing(client):

	g2a = int(client["G2a (page 5)"])

	new_loc_bathing = None

	if (g2a == 0 or g2a == 1 or g2a == 2 or g2a == 3):
		new_loc_bathing = 0

	if (g2a == 4 or g2a == 5 or g2a == 6):
		new_loc_bathing = 3

	return new_loc_bathing


def LOC_dressing(client):

	g2b = int(client["G2b (page 5)"])
	g2c = int(client["G2c (page 5)"])
	g2d = int(client["G2d (page 5)"])

	new_loc_dressing = None

	if ((g2b == 0 or g2b == 1 or g2b == 2 or g2b == 3) and
		(g2c == 0 or g2c == 1 or g2c == 2 or g2c == 3) and
		(g2d == 0 or g2d == 1 or g2d == 2 or g2d == 3)):
		new_loc_dressing = 0

	if ((g2b == 4 or g2b == 5 or g2b == 6) or
		(g2c == 4 or g2c == 5 or g2c == 6) or
		(g2d == 4 or g2d == 5 or g2d == 6)):
		new_loc_dressing = 3

	return new_loc_dressing


def LOC_rehabilitation(client):

	n3ea = int(client["N3ea (page 10)"])
	n3fa = int(client["N3fa (page 10)"])
	n3ga = int(client["N3ga (page 10)"])
	n3ia = int(client["N3ia (page 10)"])

	new_loc_rehabilitation = None

	if (n3ea == 0 and n3fa == 0 and n3ga == 0 and n3ia == 0):
		new_loc_rehabilitation = 0

	if (n3ea == 1 or n3fa == 1 or n3ga == 1 and n3ia == 1):
		new_loc_rehabilitation = 3

	if ((n3ea == 2 or n3ea == 3) or
		(n3fa == 2 or n3fa == 3) or
		(n3ga == 2 or n3ga == 3) or
		(n3ia == 2 or n3ia == 3)):
		new_loc_rehabilitation = 6

	if ((n3ea == 4 or n3ea == 5 or n3ea == 6 or n3ea == 7) or
		(n3fa == 4 or n3fa == 5 or n3fa == 6 or n3fa == 7) or
		(n3ga == 4 or n3ga == 5 or n3ga == 6 or n3ga == 7) or
		(n3ia == 4 or n3ia == 5 or n3ia == 6 or n3ia == 7)):
		new_loc_rehabilitation = 9
	
	return new_loc_rehabilitation


def LOC_treatments(client):

	h1 = int(client["H1 (page 6)"]) # this value is not defined in proposed document
	h2 = int(client["H2 (page 6)"])
	h3 = int(client["H3 (page 6)"])
	l1 = int(client["L1 (page 9)"])
	l3 = int(client["L3 (page 9)"])
	l4 = int(client["L4 (page 9)"])
	n2g = int(client["N2g (page 10)"])
	n2j = int(client["N2j (page 10)"])
	n2k = int(client["N2k (page 10)"])
	n2h = int(client["N2h (page 10)"])
	n2q = int(client["N2q (page 10)"])

	new_loc_treatments = None

	if ((l1 == 0 and n2k == 0) and
		(l3 == 0 and n2k == 0) and 
		(l4 == 0 and n2k == 0) and
		(n2g == 0 and n2h == 0 and n2j == 0 and n2q == 0)):
		new_loc_treatments = 0

	if (((l1 == 1 or l1 == 2) and (n2k == 1 or n2k == 2)) or
		(l3 == 1 and (n2k == 1 or n2k == 2 )) or 
		(l4 == 1 and (n2k == 1 or n2k == 2 )) or
		(n2k == 1 or n2k == 2)):
		new_loc_treatments = 3
	# observation: this could be simplified to just "n2k == 1 or n2k == 2"

	if (h2 == 2 or h3 == 1 or 
		(l1 == 2 and n2k == 3) or
		(l3 == 1 and n2k == 3) or
		(l4 == 1 and n2k == 3) or
		(n2g == 1 or n2g == 2 or n2g == 3)):
		new_loc_treatments = 6

	if ((h1 == 1 and h2 == 3) or
		((l1 == 3 or l1 == 4) and n2k == 4) or
		(l3 == 1 and n2k == 4) or
		(l4 == 1 and n2k == 4) or
		((n2g == 1 or n2g == 2 or n2g == 3) and (n2j == 1 or n2j == 2 or n2j == 3)) or
		(n2h == 1 or n2h == 2 or n2h == 3) or
		n2q == 1):
		new_loc_treatments = 9
	
	return new_loc_treatments


def LOC_medications(client):

	g1d = int(client["G1d (page 4)"])

	new_loc_medications = None

	if (g1d == 0 or g1d == 1 or g1d == 2 or g1d == 3):
		new_loc_medications = 0

	if (g1d == 4 or g1d == 5):
		new_loc_medications = 3

	if (g1d == 6):
		new_loc_medications = 6 

	return new_loc_medications


def LOC_mealprep(client):

	g1a = int(client["G1a (page 4)"])

	new_loc_mealprep = None

	if (g1a == 0 or g1a == 1 or g1a == 2 or g1a == 3):
		new_loc_mealprep = 0

	if (g1a == 4 or g1a == 5):
		new_loc_mealprep = 3

	if (g1a == 6):
		new_loc_mealprep = 6
	
	return new_loc_mealprep


def LOC_safety(client):

	d4 = int(client["D4 (page 3)"])
	j1 = int(client["J1 (page 7)"])
	j3a = int(client["J3a (page 7)"])
	j3b = int(client["J3b (page 7)"])
	j3c = int(client["J3c (page 7)"])
	j3d = int(client["J3d (page 7)"])

	new_loc_safety = None

	if ((d4 == 0 or d4 == 1 or d4 == 2) or
		j1 == 0 or
		((j1 == 1 or j1 == 2 or j1 == 3) and (j3a == 0 or j3a == 1)
										and (j3b == 0 or j3b == 1)
										and (j3c == 0 or j3c == 1)
										and (j3d == 0 or j3d == 1))):
		new_loc_safety = 0

	if ((d4 == 3) or 
		(j3a == 2 or j3a == 3 or j3a == 4) or
		(j3b == 2 or j3b == 3 or j3b == 4) or
		(j3c == 2 or j3c == 3 or j3c == 4) or
		(j3d == 2 or j3d == 3 or j3d == 4)):
		new_loc_safety = 3

	if ((d4 == 4) or
		((j1 == 1 or j1 == 2 or j1 == 3) and ((j3a == 1 or j3a == 2 or j3a == 3 or j3a == 4) or
										 (j3b == 1 or j3b == 2 or j3b == 3 or j3b == 4) or
										 (j3c == 1 or j3c == 2 or j3c == 3 or j3c == 4) or
										 (j3d == 1 or j3d == 2 or j3d == 3 or j3d == 4)))):
		new_loc_safety = 6

	return new_loc_safety


### MAIN ###

## for dictwriter
new_rows = []
headers = []

## for record-keeping
# keys are categories of interest, values are number of times each category appears
cat_of_interest = {}  

with open(sys.argv[1], 'r') as csvfile:
	# read first line of file to get headers in order
	header_reader = csv.reader(csvfile)
	headers = next(header_reader)

with open(sys.argv[1], 'r') as csvfile:
	reader = csv.DictReader(csvfile)
	for row in reader:
		LOC_total = 0
		temp = {}
		temp["LOC Behavioral"] = LOC_behavioral(row)
		temp["LOC Cognition"] = LOC_cognition(row)[0]
		temp["LOC Cognition Trigger"] = LOC_cognition(row)[1]
		temp["LOC Mobility"] = LOC_mobility(row)[0]
		temp["LOC Mobility Trigger"] = LOC_mobility(row)[1]		
		temp["LOC Eating"] = LOC_eating(row)[0]
		temp["LOC Eating Trigger"] = LOC_eating(row)[1]	
		temp["LOC Toileting"] = LOC_toileting(row)
		temp["LOC Bathing"] = LOC_bathing(row)
		temp["LOC Dressing"] = LOC_dressing(row)
		temp["LOC Rehabilitation"] = LOC_rehabilitation(row)
		temp["LOC Treatments"] = LOC_treatments(row)
		temp["LOC Medications"] = LOC_medications(row)
		temp["LOC Meal Prep"] = LOC_mealprep(row)
		temp["LOC Safety"] = LOC_safety(row)

		for k, v in temp.items():
			if v == "Not Present" or v == "Present":
				pass
			elif v == None:
				temp[k] = "No matching output"
			else:
				LOC_total += v

		# add new subtotals to current row in csv with their titles 
		temp["New LOC Total Score"] = LOC_total
		row.update(temp)

		# put row to be written, to the list of dictionaries
		new_rows.append(row)

		# update categories of interest counter dictionary
		# pprint.pprint(row["Categories of Interest"].split(", "))
		categories = re.split(",|;|AND", row["Categories of Interest"].upper())
		for cat in categories:
			if cat.strip() not in cat_of_interest:
				cat_of_interest[cat.strip()] = 0
			cat_of_interest[cat.strip()] += 1

with open(sys.argv[2], 'w') as csvfile:
	new_headers = [ 
					"New LOC Total Score",
					"LOC Behavioral", 
					"LOC Cognition", 
					"LOC Cognition Trigger", 
					"LOC Mobility", 
					"LOC Mobility Trigger",
					"LOC Eating",
					"LOC Eating Trigger",
					"LOC Toileting",
					"LOC Bathing",
					"LOC Dressing",
					"LOC Rehabilitation",
					"LOC Treatments",
					"LOC Medications",
					"LOC Meal Prep",
					"LOC Safety"
					]
	# add new column headers after the current LOC score to make comparison easy
	temp = headers[6:]
	headers = headers[:6]
	headers.extend(new_headers)
	headers.extend(temp)
	# create writer object w/ those headers
	writer = csv.DictWriter(csvfile, fieldnames = headers)
	# write the dictionary objects 
	writer.writeheader()
	writer.writerows(new_rows)

	# count total now ineligible, AKA old score was >= 24 and new score is < 18
	newly_ineligible = 0
	for e, row in enumerate(new_rows):
		if (int(row["Current LOC Score"]) >= 24) and (int(row["New LOC Total Score"]) < 18):
			newly_ineligible += 1

	print("Newly ineligible: " + str(newly_ineligible) + " out of " + str(len(new_rows)) + ", or " + str(newly_ineligible * 100.0 / len(new_rows)) + "%")
	pprint.pprint(cat_of_interest)

with open("categories_of_interest.csv", 'w') as csvfile:
	writer = csv.writer(csvfile)
	writer.writerows(map(list, cat_of_interest.items()))

