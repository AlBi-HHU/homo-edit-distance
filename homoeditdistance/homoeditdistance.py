#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Homo-Edit Distance
Maren Brand, Gunnar W. Klau, Philipp Spohr, Nguyen Khoa Tran
"""
__author__ = """Maren Brand, Gunnar W. Klau, Philipp Spohr, Nguyen Khoa Tran"""
__date__ = ""
__credits__ = ""
__revision__ = ""
#    Copyright (C) 2020 by
#    AlBi-HHU (gunnar.klau@hhu.de)
#    All rights reserved.
#    MIT license.

import argparse
import sys
import numpy as np


# Main dynamic programming algorithm to compute the homo-edit distance between two strings s and t.

# backtracking can be controlled with int argument 0-> none, 1-> basic, 2-> full
def homoEditDistance(s, t, backtracking=0):
    m = len(s)
    n = len(t)
    d = np.zeros(shape=(m + 1, n + 1), dtype=object)
    bt = np.zeros(shape=(m + 1, n + 1), dtype=object) if backtracking > 0 else None

    # Calculate auxiliary DP
    auxResultS = distancesToEmptyString(s, backtracking)
    H = auxResultS['H']
    auxResultT = distancesToEmptyString(t, backtracking)
    H_t = auxResultT['H']
    H.update(H_t)

    # print('H:\n', H)

    # Fetch backtracking if applicable
    zbt = {} if backtracking == 2 else None

    if backtracking == 2:
        zbt = auxResultS['BTMatrix']
        zbt.update(auxResultT['BTMatrix'])
        # for k in zbt:
        #     print(k,zbt[k])

    for i in range(0, m + 1):
        for j in range(0, n + 1):
            C = list([])
            # initialisation
            if i == 0 and j == 0:
                d[i][j] = 0
                if backtracking > 0:
                    bt[i][j] = list([])
            # main body of method
            else:
                c = float('inf')
                if i > 0 and j > 0:
                    if s[i-1] == t[j-1]:
                        c = d[i-1][j-1]
                        C.append((i-1, j-1))

                for k in range(0, i):
                    if c > d[k, j] + H[(s, k, i)]:
                        c = d[k, j] + H[(s, k, i)]
                        C = list([(k, j)])
                    elif c == d[k, j] + H[(s, k, i)]:
                        C.append((k, j))

                for l in range(0, j):
                    if c > d[i, l] + H[(t, l, j)]:
                        c = d[i, l] + H[(t, l, j)]
                        C = list([(i, l)])
                    elif c == d[i, l] + H[(t, l, j)]:
                        C.append((i, l))

                d[i][j] = c
                if backtracking > 0:
                    bt[i][j] = list(C)
    ret = {
        'hed': d[m][n]
    }

    # Add backtracking matrices to result if needed
    if backtracking > 0:
        ret['bt'] = bt
    if backtracking == 2:
        ret['zbt'] = zbt

    return ret


def backtrack(bt, s, t):
    sub = ''
    m = len(s)
    n = len(t)
    for gen in backtrackRecursive(bt, s, t, sub, m, n):
        yield gen


def backtrackRecursive(bt, s, t, sub, i, j):
    if i == 0 and j == 0:
        yield sub[::-1]
        return

    for C in bt[i][j]:
        # horizontal
        if C[0] == i:
            for gen in backtrackRecursive(bt, s, t, sub, i, C[1]):
                yield gen

        # vertical
        elif C[1] == j:
            for gen in backtrackRecursive(bt, s, t, sub, C[0], j):
                yield gen

        # diagonal
        else:
            for gen in backtrackRecursive(bt, s, t, sub + s[i - 1], C[0], C[1]):
                yield gen


# Performs backtracking on the auxiliary dynamic programming method to resolve string deletions
def resolveDeletion(s, btz, i, j):
    if i == j-1:
        return [(i, j)]
    elif i > j-1:
        return []
    btd = btz[(s, i, j)]
    for k in btd:
        # TODO: Show multiple variants for deletions
        if s[i] == s[j-1]:
            return [['merge']+resolveDeletion(s, btz, i, k)+resolveDeletion(s, btz, k, j)]
        else:
            return [['split']+resolveDeletion(s, btz, i, k)+resolveDeletion(s, btz, k, j)]


# Applies a list of deletions on a string and outputs human-readable representations of the deletion events
def processDeletions(path, string, deletionInstructions):
    inst = deletionInstructions[0]

    path += processDeletionsRecursive(inst)


def processDeletionsRecursive(deletionInstructions):
    if isinstance(deletionInstructions, tuple):
        return [deletionInstructions]

    deletionType = deletionInstructions[0]
    left = deletionInstructions[1]
    right = deletionInstructions[2]
    if deletionType == 'split':
        return processDeletionsRecursive(left)+processDeletionsRecursive(right)
    elif deletionType == 'merge':
        lresult = processDeletionsRecursive(left)
        rresult = processDeletionsRecursive(right)
        return lresult[1:]+rresult[:-1]+[(lresult[0][0], rresult[-1][1])]
    # else:
    #     print('invalid deletion type: {}'.format(deletionType))
    #     sys.exit(-1)


# Replaces all deletion events with a step by step backtracking
def resolveDeletions(path, s, t, btz):
    # print(path)
    newPath = ['s: {} t: {}'.format(s, t)]
    # the state of the strings at a given location in the path is reflected in smod and tmod
    for step in path:
        stepData = step.split(' ')
        if stepData[0] == 'del':
            string = s if stepData[1] == 's' else t
            j = int(stepData[3])
            i = int(stepData[2])
            deletionInstructions = resolveDeletion(string, btz, i, j)  # [::-1]
            # print('delIns', deletionInstructions)
            if stepData[1] == 's':
                newPath.append('Deleting substring {} -> {} ({}) from s'.format(i, j, s[i:j]))
                processDeletions(newPath, s, deletionInstructions)
            else:
                newPath.append('Deleting substring {} -> {} ({}) from t'.format(i, j, t[i:j]))
                processDeletions(newPath, t, deletionInstructions)
        else:
            pass

    return newPath


# returns all possible backtracking paths that resulted in the calculated optimal homo-edit distance
def assemblePaths(bt, s, t, btz):
    txt = dict({})
    transforms = []
    m = len(s)
    n = len(t)
    nmMax = max(m, n) + 1
    for idx, gen in enumerate(assemblePathsRecursive(bt, s, t, transforms, m, n)):
        txtPath = ''
        path = resolveDeletions(gen, s, t, btz)
        txtPath += ('Possible optimal sequence of operations: \n'.format(idx))
        sPrint = s
        tPrint = t
        st = ''
        for step in path:
            if isinstance(step, tuple):
                if st == 's':
                    sDel = sPrint[step[0]:step[1]].replace('-', '')
                    sPrint = sPrint[:step[0]] + '-'*(step[1]-step[0]) + sPrint[step[1]:]
                    txtPath += ('Deleting: ' + sDel + ' '*(nmMax-len(sDel)) + 'Result: ' + sPrint + '\n')
                if st == 't':
                    tDel = tPrint[step[0]:step[1]].replace('-', '')
                    tPrint = tPrint[:step[0]] + '-'*(step[1]-step[0]) + tPrint[step[1]:]
                    txtPath += ('Deleting: ' + tDel + ' '*(nmMax-len(tDel)) + 'Result: ' + tPrint + '\n')
            else:
                txtPath += step
                if step.startswith('Deleting substring'):
                    st = step[-1]
        txtPath += '\n'
        resStr = ''
        for char in sPrint:
            if char != '-' and char != ' ':
                resStr += char
        txt[resStr] = txtPath
    return txt


def assemblePathsRecursive(bt, s, t, transforms, i, j):
    if i == 0 and j == 0:
        yield transforms[::-1]
        return
    for C in bt[i][j]:
        # horizontal
        if C[0] == i:
            for gen in assemblePathsRecursive(bt, s, t, transforms+['del t {} {}'.format(C[1], j)], i, C[1]):
                yield gen

        # vertical
        elif C[1] == j:
            for gen in assemblePathsRecursive(bt, s, t, transforms+['del s {} {}'.format(C[0], i)], C[0], j):
                yield gen

        # diagonal
        else:
            for gen in assemblePathsRecursive(bt, s, t, transforms+['match'], C[0], C[1]):
                yield gen


# Auxiliary dynamic programming algorithm to compute the homo-edit distance
# between every substring of a string s and the empty string.
def distancesToEmptyString(s, backtracking=0):
    n = len(s)
    H = dict({})

    BT = {} if backtracking == 2 else None

    for l in range(0, n):
        for i in range(0, n - l):
            j = i + l + 1
            if i == j-1:
                H[(s, i, j)] = 1
            else:
                # C = list([])
                C = {}
                for k in range(i+1, j):
                    C[k] = (H[(s, i, k)] + H[(s, k, j)] - int(bool(s[i] == s[j-1])))
                H[(s, i, j)] = int(min(C.values()))

                if backtracking == 2:
                    minKeys = [k for k in C if C[k] == H[(s, i, j)]]
                    if s[i] == s[j-1]:
                        pass  # TODO: Analyze for validity

                        # Khoa's old code:
                        # Removes second backtracking in case there are two for a merger
                        # Problem: If two characters are merged and there is nothing inbetween,
                        # there is only one backtracking pointer that then gets deleted

                        # if minKeys[-1] == j-1:
                        #     minKeys.pop(-1)

                        # sameCharBetween = False
                        # minKeys2 = []
                        # for mK in minKeys:
                        #     if s[mK] == s[i]:
                        #         sameCharBetween = True
                        #         minKeys2.append(mK)
                        # if sameCharBetween:
                        #     minKeys = minKeys2.copy()
                    BT[(s, i, j)] = minKeys

    ret = {
        'H': H,
    }

    # print('H:\n', H)

    if backtracking == 2:
        ret['BTMatrix'] = BT
    print(ret)
    return ret


# demo:

# Parse arguments
def get_parser():
    description = 'Given two strings, find their homo-edit distance'
    parser = argparse.ArgumentParser(description=description, fromfile_prefix_chars='@')
    # input
    parser.add_argument('-s', '--string1', required=True,
                        help='first string. Use \"STRING\" for the empty string or strings with special characters')
    parser.add_argument('-t', '--string2', required=True,
                        help='second string')
    parser.add_argument('-a', '--all', action="store_true", default=False, required=False,
                        help='show all optimal subsequences')
    parser.add_argument('-b', '--backtrace', action="store_true", default=False, required=False,
                        help='print transformation steps')
    return parser


def run(args):
    s, t = args.string1, args.string2

    requiredBacktrackLevel = 0
    if args.backtrace:
        requiredBacktrackLevel = 2
    elif args.all:
        requiredBacktrackLevel = 1

    result = homoEditDistance(s, t, requiredBacktrackLevel)
    print('The homo-edit distance between {} and {} is {}\n'.format(
            s if s != "" else "the empty string", t if t != "" else "the empty string", result['hed']
        )
    )

    if args.all and args.backtrace:
        print('The following optimal subsequences were found, and obtained using the listed operations:\n')
        subs = backtrack(result['bt'], s, t)
        txt = dict(assemblePaths(result['bt'], s, t, result['zbt']))
        for sup in set(subs):
            print(sup)
            print(txt[sup])
        print('\n')  # Needed?

    elif args.all:
        print('The following optimal subsequences were found:\n')
        subs = backtrack(result['bt'], s, t)
        for sup in set(subs):
            print(sup, end=' ')
        print('\n')  # Needed?

    elif args.backtrace:
        print('Detailed Backtracking for one possible subsequence:\n')
        txt = dict(assemblePaths(result['bt'], s, t, result['zbt']))
        key = next(iter(txt))
        print(key)
        print(txt[key])


if __name__ == "__main__":
    run(get_parser().parse_args(sys.argv[1:]))
