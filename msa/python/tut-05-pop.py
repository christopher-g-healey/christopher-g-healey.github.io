#!/usr/bin/python

import csv				# Import CSV module

inp = open( 'pop.csv', 'rb' )		# Open pop.csv input file
reader = csv.reader( inp )		# Attach CSV reader to pop.csv

header = reader.next()			# Strip header from CSV file

max_pop = 0				# Initialize max pop...
max_city_nm = "Unknown"			# ...max city name
max_st_nm = "Unknown"			# ...max city state

for row in reader:			# For all CSV rows
	pop = int( row[ 11 ] )		# Convert string pop to integer
	if row[ 6 ] != row[ 7 ]:	# If this isn't a state pop line
		if pop > max_pop:	# Check for larger population
			max_city_nm = row[ 6 ]
			max_st_nm = row[ 7 ]
			max_pop = pop

inp.close()				# Close input file

#  Print the maximum city's name, its state name, and its population

print max_city_nm, 'in state', max_st_nm, 'has population', max_pop
