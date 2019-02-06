"""
Implementation of the proposed Missouri Medicare Levl of Care (LOC) algorithm.
For use on csv files with each survey question as a labeled column in the file.

Written Jan 28, 2019 by Emma Weil at Upturn / emma@upturn.org

Usage: argv[1] is the path/filename of csv file and argv[2] is the destination
destination file will have only ID and new score 

csv file should have AT LEAST the following column title formatting:

Organization Name,ID,Current LOC Score,E3a,E3b,E3c,E3d,E3e,E3f,[...],J3b,J3c,J3d

because the titles will be used as dictionary keys. 

"""

import csv
import pprint

with open(argv[1], newline='') as csvfile:
	new_rows = {}
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
			if v > 0:
				LOC_total += v

		# add new subtotals to current row in csv with their titles 
		temp["New LOC Total Score"] = LOC_total
		row.update(temp)

		# put row to be written
		new_rows.append(row)

with open(argv[2], newline='') as csvfile:
	writer = csv.DictWriter(csvfile)
	writer.writeRows(new_rows)
	

def LOC_behavioral(client):
	e3a = int(client["E3a"])
	e3b = int(client["E3b"])
	e3c = int(client["E3c"])
	e3d = int(client["E3d"])
	e3e = int(client["E3e"])
	e3f = int(client["E3f"])
	j3g = int(client["J3g"])
	j3h = int(client["J3h"])
	j3i = int(client["J3i"])
	n7b = int(client["N7b"])

	new_loc_behavioral = None

	if ((n7b == 0 || n7b == 1) && 
		e3a == 0 && 
		e3b == 0 && 
		e3c == 0 && 
		e3d == 0 && 
		e3e == 0 && 
		e3f == 0 && 
		j3g == 0 && 
		j3h == 0 && 
		j3i == 0):
		new_loc_behavioral = 0

	if ((n7b == 2 || n7b == 3) ||
		e3a == 1 || 
		e3b == 1 || 
		e3c == 1 || 
		e3d == 1 || 
		e3e == 1 || 
		e3f == 1 || 
		j3g == 1 || 
		j3h == 1 || 
		j3i == 1):
		new_loc_behavioral = 3

	if ((n7b == 2 || n7b == 3) ||
		(e3a == 2 || e3a == 3) || 
		(e3b == 2 || e3b == 3) ||
		(e3c == 2 || e3c == 3) ||
		(e3d == 2 || e3d == 3) ||
		(e3e == 2 || e3e == 3) ||
		(e3f == 2 || e3f == 3) || 
		(j3g == 2 || j3g == 3 || j3g == 4) || 
		(j3h == 2 || j3h == 3 || j3h == 4) || 
		(j3i == 2 || j3i == 3 || j3i == 4)):
		new_loc_behavioral = 6

	if ((n7b == 2 || n7b == 3) &&
		((e3a == 3) || 
		 (e3b == 3) ||
		 (e3c == 3) ||
		 (e3d == 3) ||
		 (e3e == 3) ||
		 (e3f == 3) || 
		 (j3g == 3 || j3g == 4) || 
		 (j3h == 3 || j3h == 4) || 
		 (j3i == 3 || j3i == 4))):
		new_loc_behavioral = 9

	return new_loc_behavioral


def LOC_cognition(client):
	c1 = int(client["C1"])
	c2a = int(client["C2a"])
	c2b = int(client["C2b"])
	c2c = int(client["C2c"])
	c3c = int(client["C3c"])
	d1 = int(client["D1"])
	d2 = int(client["D2"])

	new_loc_cognition = None
	loc_cognition_trigger = "Not Present"

	if ((c1 == 0 || c1 == 1 || c1 == 2 || c1 == 3) && 
		c2a == 0 && 
		c2b == 0 && 
		c2c == 0 && 
		c3c == 0 && 
		(d1 == 0 || d1 == 1) && 
		(d2 == 0 || d2 == 1)):
		new_loc_cognition = 0

	if ((c1 == 1 || c1 == 2) && 
		(c2a == 1 || 
		 c2b == 1 || 
		 c2c == 1 || 
		 (c3c == 1 || c3c == 2) ||
		 (d1 == 2 || d1 == 3 || d1 == 4) || 
		 (d2 == 2 || d2 == 3 || d2 == 4))):
		new_loc_cognition = 3

	if (c1 == 3 && 
		(c2a == 1 || 
		 c2b == 1 || 
		 c2c == 1 || 
		 (c3c == 1 || c3c == 2) ||
		 d1 == 3 || 
		 d2 == 3)):
		new_loc_cognition = 6
	
	if (c1 >= 3 && (d1 == 4 || d2 == 4)):
		new_loc_cognition = 9

	# note deviation from proposed algorithm, as this is the only way to reach the c1=4 / c1=5 trigger
	if (c1 == 4 || c1 == 5):
		new_loc_cognition = 9
		loc_cognition_trigger = "Present"

	return [new_loc_cognition, loc_cognition_trigger]


def LOC_mobility(client):
	g2e = int(client["G2e"])
	g2f = int(client["G2f"])
	g2i = int(client["G2i"])
	g3a = int(client["G3a"])

	new_loc_mobility = None
	loc_mobility_trigger = "Not Present"

	if ((g2e == 0 || g2e == 1 || g2e == 2) && 
		(g2f == 0 || g2f == 1 || g2f == 2) && 
		(g2i == 0 || g2i == 1 || g2i == 2)):
		new_loc_mobility = 0

	if ((g2e == 3 || g2e == 4) ||
		(g2f == 3 || g2f == 4) ||
		(g2i == 3 || g2i == 4)):
		new_loc_mobility = 3

	if (g2e == 5 || g2f == 5 || g2i == 5):
		new_loc_mobility = 6

	if (g2e == 6 || g2f == 6 || g2i == 6 || g3a == 3):
		new_loc_mobility = 9
		if (g3a == 3):
			loc_mobility_trigger = "Present"

	return [new_loc_mobility, loc_mobility_trigger]


def LOC_eating(client):
	g2j = int(client["G2j"])
	k2e = int(client["K2e"])

	new_loc_eating = None
	loc_eating_trigger = "Not Present"

	if (g2j == 0 || k2e == 0):
		new_loc_eating = 0

	if ((g2j == 1 || g2j == 2 || g2j == 3) || 
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
	g2g = int(client["G2g"])
	g2h = int(client["G2h"])

	new_loc_toileting = None

	if ((g2g == 0 || g2g == 1 || g2g == 2) && 
		(g2h == 0 || g2h == 1 || g2h == 2)):
		new_loc_toileting = 0

	if ((g2g == 3 || g2g == 4) || 
		(g2h == 3 || g2h == 4)):
		new_loc_toileting = 3

	if (g2g == 5 || g2h == 5):
		new_loc_toileting = 6

	if (g2g == 6 || g2h == 6):
		new_loc_toileting = 9


def LOC_bathing(client):
	g2a = int(client["G2a"])

	new_loc_bathing = None

	if (g2a == 0 || g2a == 1 || g2a == 2 || g2a == 3):
		new_loc_bathing = 0

	if (g2a == 4 || g2a == 5 || g2a == 6):
		new_loc_bathing = 3

	return new_loc_bathing


def LOC_dressing(client):
	g2b = int(client["G2b"])
	g2c = int(client["G2c"])
	g2d = int(client["G2d"])

	new_loc_dressing = None

	if ((g2b == 0 || g2b == 1 || g2b == 2 || g2b == 3) &&
		(g2c == 0 || g2c == 1 || g2c == 2 || g2c == 3) &&
		(g2d == 0 || g2d == 1 || g2d == 2 || g2d == 3)):
		new_loc_dressing = 0

	if ((g2b == 4 || g2b == 5 || g2b == 6) ||
		(g2c == 4 || g2c == 5 || g2c == 6) ||
		(g2d == 4 || g2d == 5 || g2d == 6)):
		new_loc_dressing = 3

	return new_loc_dressing


def LOC_rehabilitation(client):
	n3ea = int(client["N3ea"])
	n3fa = int(client["N3fa"])
	n3ga = int(client["N3ga"])
	n3ia = int(client["N3ia"])

	new_loc_rehabilitation = None

	if (n3ea == 0 && n3fa == 0 && n3ga == 0 && n3ia == 0):
		new_loc_rehabilitation = 0

	if (n3ea == 1 || n3fa == 1 || n3ga == 1 && n3ia == 1):
		new_loc_rehabilitation = 3

	if ((n3ea == 2 || n3ea == 3) ||
		(n3fa == 2 || n3fa == 3) ||
		(n3ga == 2 || n3ga == 3) ||
		(n3ia == 2 || n3ia == 3)):
		new_loc_rehabilitation = 6

	if ((n3ea == 4 || n3ea == 5 || n3ea == 6 || n3ea == 7) ||
		(n3fa == 4 || n3fa == 5 || n3fa == 6 || n3fa == 7) ||
		(n3ga == 4 || n3ga == 5 || n3ga == 6 || n3ga == 7) ||
		(n3ia == 4 || n3ia == 5 || n3ia == 6 || n3ia == 7)):
		new_loc_rehabilitation = 9
	
	return new_loc_rehabilitation


def LOC_treatments(client):
	h1 = int(client["H1"]) # this value is not defined in proposed document
	h2 = int(client["H2"])
	h3 = int(client["H3"])
	l1 = int(client["L1"])
	l3 = int(client["L3"])
	l4 = int(client["L4"])
	n2g = int(client["N2g"])
	n2j = int(client["N2j"])
	n2k = int(client["N2k"])
	n2h = int(client["N2h"])
	n2q = int(client["N2q"])

	new_loc_treatments = None

	if ((l1 == 0 && n2k == 0) &&
		(l3 == 0 && n2k == 0) && 
		(l4 == 0 && n2k == 0) &&
		(n2g == 0 && n2h == 0 && n2j == 0 && n2q == 0)):
		new_loc_treatments = 0

	if (((l1 == 1 || l1 == 2) && (n2k == 1 || n2k == 2)) ||
		(l3 == 1 && (n2k == 1 || n2k == 2 )) || 
		(l4 == 1 && (n2k == 1 || n2k == 2 )) ||
		(n2k == 1 || n2k == 2)):
		new_loc_treatments = 3
	# observation: this could be simplified to just "n2k == 1 or n2k == 2"

	if (h2 == 2 || h3 == 1 || 
		(l1 == 2 && n2k == 3) ||
		(l3 == 1 && n2k == 3) ||
		(l4 == 1 && n2k == 3) ||
		(n2g == 1 || n2g == 2 || n2g == 3)):
		new_loc_treatments = 6

	if ((h1 == 1 && h2 == 3) ||
		((l1 == 3 || l1 == 4) && n2k == 4) ||
		(l3 == 1 && n2k == 4) ||
		(l4 == 1 && n2k == 4) ||
		((n2g == 1 || n2g == 2 || n2g == 3) && (n2j == 1 || n2j == 2 || n2j == 3)) ||
		(n2h == 1 || n2h == 2 || n2h == 3) ||
		n2q == 1):
		new_loc_treatments = 9
	
	return new_loc_treatments


def LOC_medications(client):
	g1d = int(client["G1d"])

	new_loc_medications = None

	if (g1d == 0 || g1d == 1 || g1d == 2 || g1d == 3):
		new_loc_medications = 0

	if (g1d == 4 || g1d == 5):
		new_loc_medications = 3

	if (g1d == 6):
		new_loc_medications = 6 

	return new_loc_medications


def LOC_mealprep(client):
	g1a = int(client["G1a"])

	new_loc_mealprep = None

	if (g1a == 0 || g1a == 1 || g1a == 2 || g1a == 3):
		new_loc_mealprep = 0

	if (g1a == 4 || g1a == 5):
		new_loc_mealprep = 3

	if (g1a == 6):
		new_loc_mealprep = 6
	
	return new_loc_mealprep


def LOC_safety(client):
	d4 = int(client["D4"])
	j1 = int(client["J1"])
	j3a = int(client["J3a"])
	j3b = int(client["J3b"])
	j3c = int(client["J3c"])
	j3d = int(client["J3d"])

	new_loc_safety = None

	if ((d4 == 0 || d4 == 1 || d4 == 2) ||
		j1 == 0 ||
		((j1 == 1 || j1 == 2 || j1 == 3) && (j3a == 0 || j3a == 1)
										&& (j3b == 0 || j3b == 1)
										&& (j3c == 0 || j3c == 1)
										&& (j3d == 0 || j3d == 1))):
		new_loc_safety = 0

	if ((d4 == 3) || 
		(j3a == 2 || j3a == 3 || j3a == 4) ||
		(j3b == 2 || j3b == 3 || j3b == 4) ||
		(j3c == 2 || j3c == 3 || j3c == 4) ||
		(j3d == 2 || j3d == 3 || j3d == 4)):
		new_loc_safety = 3

	if ((d4 == 4) ||
		((j1 == 1 || j1 == 2 || j1 == 3) && ((j3a == 1 || j3a == 2 || j3a == 3 || j3a == 4) ||
										 (j3b == 1 || j3b == 2 || j3b == 3 || j3b == 4) ||
										 (j3c == 1 || j3c == 2 || j3c == 3 || j3c == 4) ||
										 (j3d == 1 || j3d == 2 || j3d == 3 || j3d == 4)))):
		new_loc_safety = 6

	return new_loc_safety





