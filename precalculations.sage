#!/usr/bin/env sage
"""
See README.md for details
Run 'sage precalculations.sage -h' for a list of options
"""

# Command line arguments; run "sage precalculations.sage -h" to see
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-i", \
                    "--info",\
                    help="print information on data that has already\
                    been calculated, and exit",\
                    action="store_true")
parser.add_argument("-d", \
                    "--dump",\
                    help="dump precalculated information; meant to be\
                    redirected to a csv file, see README.md",\
                    action="store_true")
args=parser.parse_args()


# Input/output:
import pickle
import os.path
import sys

# Counting time:
import timeit
from datetime import timedelta

load('precalculations_definitions.sage')

# Checking for previously saved data; otherwise initializing dictionaries
if os.path.isfile("data/sequences.dat") and os.path.isfile("data/polynomInfo.dat"):
    sequences=pickle.load(open("data/sequences.dat",'rb'))
    polynomInfo=pickle.load(open("data/polynomInfo.dat",'rb'))
    dataexist=True
else:
    sequences={}
    polynomInfo={}
    dataexist=False

# If -i or --info flag was used, print information
if args.info:
    if dataexist:
        print "\nm\tq\t# of representatives\tPrimitive polynomial used over Fq"
        print 80*"-"
        for m in sequences.keys():
            for q in sequences[m].keys():
                numrepr=len(sequences[m][q])
                pi=polynomInfo[m][q]
                print "%d\t%d\t%d\t\t\t%s" % (m,q,numrepr,pi)
        print
    else:
        print "There are no existing precalculated data; nothing to show"
    exit()

# If -d or --dump flag was used, dump calculations in csv format
if args.dump:
    if dataexist:
        for m in sorted(sequences):
            for q in sorted(sequences[m]):
                for r in sorted(sequences[m][q]):
                    zerosstring = ' '.join(str(i) for i in sequences[m][q][r])
                    print "%d,%d,%d,%s" % (m,q,r,zerosstring)
    else:
        print "There are no existing precalculated data; nothing to output"
    exit()


# Double-check we have prime powers in 'primepowers'
for i in primepowers:
    if not i.is_prime_power():
        raise ValueError("%d is not a prime power; remove from primepowers" % i)

for m in degrees:
    if not (m in sequences) or not (m in polynomInfo):
        sequences[m]={}
        polynomInfo[m]={}
    for q in primepowers:
        if (q in sequences[m]) and (q in polynomInfo[m]):
            print "Data for m=%d and q=%d has already been calculated; skipping" % (m,q)
        else:
            start = timeit.default_timer() # Counting running clock time, out of curiocity

            sequences[m][q]={}
            counter=1 # for progress, later
            print
            print "Starting calculations for m=%d and q=%d" % (m,q)
            repr=Representatives(m,q)
            print "\tI computed %d representatives for this case" % len(repr)

            F.<a>=GF(q)
            K.<x>=F[]
            f=PrimPol_q(m,q)[0] # Polynomial in K.<x>; see definitions.sage
            Fm.<alpha>=f.root_field()

            # Calcuate the lists of the zero indexes, of a chunk of size (q^m-1)/(q-1) 
            # for all the distinct sequences corresponding to the representatives, and save them.
            for i in repr:
                sequences[m][q][i]=ZerosOfSequence(m,q,i)
                # Print progress:
                sys.stdout.write("\tCalculated the zero indexes of %d of the %d distinct sequences \r" % (counter,len(repr)))
                sys.stdout.flush()
                counter+=1

            # Save some information for later use
            infotext= str(f)                # The primitive over Fq to construct Fq^m
            if not is_prime(q):             # Then it is a prime power
                p=q.prime_factors()[0]      # q=p^n, some n
                infotext+=". F%d is constructed as F_%d(a), where a is the root of %s." % (q,p,str(F.modulus()))
            polynomInfo[m][q]=infotext

            # Print the time required
            stop = timeit.default_timer()
            print "\t - Time required to calculate the sequences: "+str(timedelta(seconds=stop-start))[:-7]

            sys.stdout.write("\tSaving data..." )
            sys.stdout.flush()
            f=open("data/sequences.dat",'wb')
            pickle.dump(sequences,f)
            f.close()

            f=open("data/polynomInfo.dat",'wb')
            pickle.dump(polynomInfo,f)
            f.close()
            sys.stdout.write(" Done\n" )
