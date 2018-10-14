#!/usr/bin/env python2
"""
Run as 'python2 main.py m q r1 ... rl' where r1, .., rl are the 
representatives and l>1.
"""

from sys import argv
from csv import reader
import search_definitions as sd

# Arguments
m=int(argv[1])
q=int(argv[2])
l=len(argv)-3 # Number of
w=int((q**m-1)/(q-1))

# List of powers of a primitive element given as input:
Rs=[int(r) for r in argv[3:]]

# Create dictionary from dumped precalculations in .csv file
datafile='data/data.csv' # previously calculated data
data={}
CSVreader = reader(open(datafile))
for row in CSVreader:
    M=int(row[0])
    if not M in data: data[M]={}
    Q=int(row[1])
    if not Q in data[M]: data[M][Q]={}
    R=int(row[2])
    z=[int(i) for i in row[3].split(' ')]
    data[M][Q][R]=z

# Create the zero positions
zp = [data[m][q][r] for r in Rs]
PP=sd.Pplanes(zp,w)
F=sd.UncovLookup(PP,w,m)

#definitions.MAX=0
e=[0]
PV=range(1,w)
print "Starting search"
sd.FindCA(e,PV,F,w,m)
