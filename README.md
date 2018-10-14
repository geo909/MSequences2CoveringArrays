# PhD thesis companion code

This is the companion code of [my PhD thesis](http://people.math.carleton.ca/~gtzanaki/project/phd-thesis).
This program relies on several areas of discrete mathematics and a rather involved type of backtracking, to output covering arrays using a compact notation.
A more convoluted cythonized version produced dramatic improvements over previously known covering arrays.
In the context of combinatorial testing, that meant up to 38% less tests required for some cases of parameters; for more information on combinatorial testing for software and its connection to covering arrays, you can check [this overview](https://csrc.nist.gov/projects/automated-combinatorial-testing-for-software) by the US National Institute of Standards and Technology.

Understanding what this program does and how it works requires a certain familiarity with [my thesis](http://people.math.carleton.ca/~gtzanaki/project/phd-thesis), especially Chapter 4.
*The rest of this README assumes notations and definitions from that chapter and some understanding of the basic concepts that are discussed thereof.*

## Usage

This program requires a precalculation of necessary data prior to running the search.

1. First, choose the degrees and the prime powers to run experiments for and define them in the the file `precalculations_definitions.sage` as in the following example:

	```Python
	# file precalculations_definitions.sage
	primepowers=[2,3,4,5,7,8,9,11,13,16,17]
	degrees=[4,5,6,7]
	```
2. Run `sage precalculations.sage`. This will store (using python's pickle) the necessary data in the files `data/polynomInfo.dat` and `data/sequences.dat`; next time precalculations are performed, any previously stored data in these files will not be re-computed.

3. Run  `sage precalculations.sage -d > output.csv`. This will dump the stored data into the text file `output.csv`. As the extension suggests, this is a comma-separated file, so you can look at the data yourself by opening it with a spreadsheet program.

4. Now you can run a search by `python2 search.py m q r1 ... rl` where

	* m is the degree of the finite field extension
	* q is the prime power of the finite field
	* r<sub>1</sub>, ..., r<sub>l</sub> are the representatives that we run the search for

	The representatives that you can choose from can be found in the third column of `output.csv`.

    The program will print on the screen the best set of columns and update this information whenever it finds something better. This set of columns is nothing less than the covering array in compact form; to see how we obtain the actual matrix, check Section 4.4.

## Some details on the precalculations


The program `precalculations.sage` will construct the python multidimensional dictionaries `sequences` and `polynomInfo` and pickle them in the files `sequences.dat` and `polynomInfo.dat`. These contain the following information:

<table>
<tbody>
<tr>
    <td>
    <tt>polynomInfo[m][q]</tt>
    <td>
    human-readable information regarding the construction of Fq<sup>m</sup>
<tr>
    <td>
    <tt>sequences[m].keys()</tt>
    <td>
    list of q that have been calculated
<tr>
    <td width="220">
    <tt>sequences[m][q].keys()</tt>
    <td>
    list of representatives corresponding to q and m
<tr>
    <td>
    <tt> sequences[m][q][r]</tt>
    <td>
    list of the indexes of the zeros among the first (q^m-1)/(q-1) elements of the LFSR sequence with representative r
</table>

Note: Theses dictionaries contain *sage* types, and can only be read by sage (and not python) scripts.


#### Optional arguments:
<table>
<tr>
<td width="140">
-i, --information
<td>
Print on the screen the following information and exit:
    <ul>
        <li> which q and m were calculated
        <li> how many representatives were calculated for every (q,m)
        <li> which primitive polynomials is used for every (q,m)
    </ul>
<tr>
<td>
-d, --dump
<td>
Dump the calculated information in a csv format as follows, then exit:

<table>
<tr>
    <th> column1 <th> column2 <th> column3 <th> column4
<tr>
    <td> m,      <td>q,       <td>r1,      <td> space-separated zero indexes
<tr>
    <td> m,      <td>q,       <td>r2,      <td> space-separated zero indexes
<tr>
    <td>  .      <td> .       <td>  .      <td> .
<tr>
    <td>  .      <td> .       <td>  .      <td> .
<tr>
    <td>  .      <td> .       <td>  .      <td> .
</table>

where r1, r2, .. are the representatives for the m, q.

Intended usage: `sage precalculations -d > output.csv`
</table>

