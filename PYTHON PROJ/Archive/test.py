import csv
with open('data.csv', 'rb') as csvfile:
	spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
	for row in spamreader:
		print row
csvfile.close()
choice = raw_input("> ")


if(choice == "edit"):
	r = csv.reader(open('data.csv'))
	lines = [l for l in r]
	
	row = raw_input("row> ")
	col = raw_input("col> ")
	val = raw_input("val> ")
	lines[int(col)][int(row)] = val
	with open('data.csv', 'rU') as csvfile:
		spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
		for row in spamreader:
			print row
	csvfile.close()
	
	
	
	

