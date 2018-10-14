import collections
import csv
import copy
from itertools import combinations
from functools import reduce
from os import system

def Pplanes(zp,w):
    """
    Input:  zp is a list of l lists, each of which contains the indexes
            of the zeros of a sequence (among the first w elements)
            w is (q^m-1)/(q-1)
    Output: Returns a list PP, where each element is  a tuple of sets;
            each set is the zero indexes of a row that starts with zeros
            in the corresponding array. In other words, each tuple
            contains all the distinct projective planes corresponding
            to the array.
    See Algorithm 4 in Section 4.2
    """
    PP=[]
    for s in zp:
        # s contains the zero positions of the sequence of the
        # corresponding representative. Every set is the index of
        # the zeros in some row of the array that starts with a zero.
        shifts= tuple( set([ (i-d)%w for i in s if i!=d]) for d in s)
        PP.append(shifts)
    return(PP)

def ComputeCand(e, PV, F, w,m):
    """
    See Algorithm 4 in Section 4.2 for pseudocode and detailed
    explanation
    """
    if not PV:
        return([])
    l=len(e)
    if l<m-1:
        return(PV)
    else:
        C=[ (j-e[-1])%w for j in e[:-1] ]
        for p in [list(T) for T in combinations(C,m-2)]:
            p.sort()
            Fij=reduce(lambda l,i: l[i], p, F)
            R=set([(r+e[-1])%w for r in Fij ])
            PV=[j for j in PV if j not in R]
            if not PV: return([])
    return(PV)


def is_necklace(L):
    """
    Input:  L is a binary word, represented as a collections.deque(list)
            object of 0s and 1s
    Output: True if L is a necklace, as per Definition 4.8
    """
    x=collections.deque(L)
    i=0
    while i<len(L):
        x.rotate(-1)
        if x<L:
            return(False)
        i+=1
    return(True)

def columns2bin(e,w):
    """
    Input:  a list of columns e
    Output: The binary representation of this set of columns, as per
            Definition 4.11
    """
    b=[1]
    j=1
    for i in range(1, e[-1]+1):
        if i==e[j]:
            b.append(1)
            j+=1
        else:
            b.append(0)
    return((w-e[-1]-1)*[0]+b)

def CombineUElements(S,indexes):
    """
    This is just an auxiliary function, used in UncovLookup.
    Input:  S is a list of the form S=[L1, ..., Ln], where Li is a list
            that contains sets of integers.
            'indexes' is a list of integers
    Output: Let Ui be the union of all the sets of in Li.
            Then the output is the intersection of U1, .., Un with the
            elements in 'indexes' removed
    """
    x = set.intersection( *[ set.union(*z) for z in S ] )
    x.difference_update(indexes)
    return(tuple(x))

def UncovLookup(PP,w,m):
    """
    Input:  The output of Pplanes(zp,w), i.e. a list of the projective
            planes that we work with, expressed as tuples of integers
            corresponding to the zeros in the corresponding row of the
            LFSR array
    Output: F is an m-dimensional array where F[i1][i2]...[im] is a
            list of integers, call it B, with the property that, for
            every b in B, the set of columns {0, i1, ..., im, b} is
            uncovered.

            This is essentially an implementation of what we define as
            U_P(I) in pg. 72, where I={i1, ..., im} in the above example
    """
    l=len(PP)
    F=[[] for i in range(l)]
    for i in range(m-2):
        F=[copy.deepcopy(F) for j in range(w)]
    # F is now a w x l array where each element is an empty list

    for j in range(l):
        # PP[j]: the tuple containing the projective planes of the j-th
        # representative, as sets of zero indexes
        for plane in PP[j]:
            for p in [list(T) for T in combinations(plane,m-2)]:
                # in the case m=4, p is a pair
                p.sort()
                reduce(lambda l, i: l[i], p+[j], F).append(plane)

    for indexes in [list(T) for T in combinations(range(1,w),m-2)]:
            reduce(lambda l, i: l[i], indexes, F)[:] = CombineUElements(reduce(lambda l, i: l[i], indexes, F),indexes)

    return(tuple(F))

MAX=0 #Global variable for the next function.
def FindCA(e,PV,F,w,m):
    """
    This is discussed in detail in Section 4.3. Also, see Algorithm 5
    for the pseudocode.
    """
    global MAX
    le=len(e)
    if le > MAX:
        MAX = le
        #print the new best columns and how many they are
        system('clear')
        print "So far, the best columns are %s and MAX is %d" % (e,MAX)
    PV=ComputeCand(e,PV,F,w,m)
    lp=len(PV)
    if le+lp > MAX:
        for i in range(le+lp-MAX):
            newe=e+[PV[i]]
            test=collections.deque(columns2bin(newe, w))
            if is_necklace(test):
                FindCA(newe,PV[i+1:],F,w,m)
            else:
                break
