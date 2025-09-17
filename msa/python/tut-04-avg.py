#!/usr/bin/python

num = [ 6, 12, -7, 29, 14, 38, 11, 7 ]

sum = 0
for n in num:
	sum = sum + n
print float( sum ) / len( num )

i = 0
sum = 0
while i < len( num ):
	sum = sum + num[ i ]
	i = i + 1
print sum / len( num )
