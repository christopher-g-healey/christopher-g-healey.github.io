#!/usr/bin/python

import csv
import numpy


#  Initialize name, height lists

nm = [ ]
ht = [ ]

#  Open CSV file for input

with open( "ht.csv", "rb" ) as fp:
	inp = csv.reader( fp )
	header = inp.next()

#  Read name, height on each row

	for row in inp:
		nm.append( row[ 0 ] )
		ht.append( int( row[ 1 ] ) )

#  Create numpy height array to calculate avg, stdev

ht_arr = numpy.array( ht )
avg = numpy.mean( ht_arr )
std = numpy.std( ht_arr )

#  Open CSV file for output

with open( "ht_w_class.csv", "wb" ) as fp:
	out = csv.writer( fp )
	out.writerow( header + [ 'Class' ] )

#  Write name,height,class for each row

	for row in range( len( nm ) ):

	#  Calculate proper class for given height

		if abs( ht[ row ] - avg  ) <= std:
			cl = 1
		elif abs( ht[ row ] - avg ) <= 2.0 * std:
			cl = 2
		elif ( ht[ row ] - avg ) < -2.0 * std:
			cl = 3
		else:
			cl = 4

	#  Write row

		out.writerow( [ nm[ row ], ht[ row ], cl ] )
