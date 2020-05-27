# Homo-Edit-Distance

[![DOI](https://zenodo.org/badge/260235161.svg)](https://zenodo.org/badge/latestdoi/260235161)

A homo-insertion is an insertion of a string of equal characters, which we also call a block, into another string. A homo-deletion is the inverse operation, that is, the deletion of such a block. We consider the following problem: Given two strings, what is the minimum number of homo-insertions or homo-deletions needed to convert one into the other? We refer to this number as the homo-edit distance.

## References

The algorithm is described in the following publication:

* M. Brand,  N. K. Tran, P. Spohr, S. Schrinner, G. W. Klau. The homo-edit distance problem. bioRxiv, Cold Spring Harbor Laboratory, DOI: <http://doi.org/10.5281/zenodo.3859404>

## Installation from Repository

```sh
pip3 install homoeditdistance
```

## Installation from Source

```sh
git clone https://github.com/AlBi-HHU/homo-edit-distance.git
cd homo-edit-distance
python3 setup.py install
```

## How to Run on the Command Line

The Python package comes with a command line tool `hed`, which can be used to run a demonstration of the algorithm. Its source code is located in [demonstration.py](homoeditdistance/demonstration.py). It may also help you to see how to invoke the functions. If you just cloned the repository you can start the demonstration from inside the cloned repository using

```sh
python3 -m homoeditdistance
```

### Help

```
usage: hed [-h] -s STRING1 -t STRING2 [-a] [-b]

Given two strings, find their homo-edit distance

optional arguments:
  -h, --help            show this help message and exit
  -s STRING1, --string1 STRING1
                        first string. Use quotation marks around your string
                        (e.g. "STRING")for the empty string or strings with
                        special characters
  -t STRING2, --string2 STRING2
                        second string
  -a, --all             show all optimal subsequences
  -b, --backtrace       print transformation steps
```

### Example

#### Output of `hed -s "TCAGACT" -t "TAGGCTT" -a -b`

```
The homo-edit distance between TCAGACT and TAGGCTT is 4

The following optimal subsequences were found, and obtained using the listed operations:

TAGCT
Possible optimal sequence of operations:
s: TCAGACT t: TAGGCTT
Deleting substring 1 -> 2 (C) from s
Deleting: C       Result: T-AGACT
Deleting substring 4 -> 5 (A) from s
Deleting: A       Result: T-AG-CT
Deleting substring 3 -> 4 (G) from t
Deleting: G       Result: TAG-CTT
Deleting substring 6 -> 7 (T) from t
Deleting: T       Result: TAG-CT-
```

## How to Use in Your Own Code

### Homo-Edit-Distance between Two Strings

```python
from homoeditdistance import homoEditDistance

string1 = "TCAGACT"
string2 = "TAGGCTT"
print('The homo-edit-distance of {} and {} is {}.'.format(string1, string2, homoEditDistance(string1, string2, 0)['hed']))
```

## How to Run the Unit Tests

Make sure that `unittest` Python package is installed, and run `python3 -m unittest` from inside the cloned repository.
