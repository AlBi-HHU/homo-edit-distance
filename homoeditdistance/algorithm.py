#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Homo-Edit Distance
Maren Brand, Gunnar W. Klau, Philipp Spohr, Nguyen Khoa Tran, Max Jakub Ried
"""

import numpy as np


def homoEditDistance(s, t, backtracking=0):
    """
    Main dynamic programming algorithm to compute the homo-edit distance between two strings s and t.
    :param s: string one
    :param t: string two
    :param backtracking: 0 -> no backtracking, 1 -> basic backtracking, 2 -> full backtracking
    :return:
    """
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
        #     print(k, zbt[k])

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
                    if s[i - 1] == t[j - 1]:
                        c = d[i - 1][j - 1]
                        C.append((i - 1, j - 1))

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
        'hed': d[m][n],
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


def resolveDeletion(s, btz, i, j):
    """
    Performs backtracking on the auxiliary dynamic programming method to resolve string deletions
    :param s:
    :param btz:
    :param i:
    :param j:
    :return:
    """
    if i == j - 1:
        return [(i, j)]
    elif i > j - 1:
        return []
    btd = btz[(s, i, j)]
    for k in btd:
        # TODO: Show multiple variants for deletions
        if s[i] == s[j - 1]:
            return [['merge'] + resolveDeletion(s, btz, i, k) + resolveDeletion(s, btz, k, j)]
        else:
            return [['split'] + resolveDeletion(s, btz, i, k) + resolveDeletion(s, btz, k, j)]


def processDeletions(path, deletionInstructions):
    """
    Applies a list of deletions on a string and outputs human-readable representations of the deletion events
    :param path:
    :param deletionInstructions:
    """
    inst = deletionInstructions[0]

    path += processDeletionsRecursive(inst)


def processDeletionsRecursive(deletionInstructions):
    if isinstance(deletionInstructions, tuple):
        return [deletionInstructions]

    deletionType = deletionInstructions[0]
    left = deletionInstructions[1]
    right = deletionInstructions[2]
    if deletionType == 'split':
        return processDeletionsRecursive(left) + processDeletionsRecursive(right)
    elif deletionType == 'merge':
        lresult = processDeletionsRecursive(left)
        rresult = processDeletionsRecursive(right)
        return lresult[1:] + rresult[:-1] + [(lresult[0][0], rresult[-1][1])]
    # else:
    #     print('invalid deletion type: {}'.format(deletionType))
    #     sys.exit(-1)


def resolveDeletions(path, s, t, btz):
    """
    Replaces all deletion events with a step by step backtracking
    :param path:
    :param s:
    :param t:
    :param btz:
    :return:
    """
    # print(path)
    newPath = ['s: {} t: {}\n'.format(s, t)]
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
                newPath.append('Deleting substring {} -> {} ({}) from s\n'.format(i, j, s[i:j]))
                processDeletions(newPath, deletionInstructions)
            else:
                newPath.append('Deleting substring {} -> {} ({}) from t\n'.format(i, j, t[i:j]))
                processDeletions(newPath, deletionInstructions)
        else:
            pass

    return newPath


def assemblePaths(bt, s, t, btz):
    """
    Returns all possible backtracking paths that resulted in the calculated optimal homo-edit distance
    :param bt:
    :param s:
    :param t:
    :param btz:
    :return:
    """
    txt = {}
    transforms = []
    m = len(s)
    n = len(t)
    nmMax = max(m, n) + 1
    for idx, gen in enumerate(assemblePathsRecursive(bt, s, t, transforms, m, n)):
        txtPath = ''
        path = resolveDeletions(gen, s, t, btz)
        txtPath += ('Possible optimal sequence of operations:\n'.format(idx))
        sPrint = s
        tPrint = t
        st = ''
        for step in path:
            if isinstance(step, tuple):
                if st == 's':
                    sDel = sPrint[step[0]:step[1]].replace('-', '')
                    sPrint = sPrint[:step[0]] + '-'*(step[1] - step[0]) + sPrint[step[1]:]
                    txtPath += ('Deleting: ' + sDel + ' '*(nmMax - len(sDel)) + 'Result: ' + sPrint + '\n')
                if st == 't':
                    tDel = tPrint[step[0]:step[1]].replace('-', '')
                    tPrint = tPrint[:step[0]] + '-'*(step[1] - step[0]) + tPrint[step[1]:]
                    txtPath += ('Deleting: ' + tDel + ' '*(nmMax - len(tDel)) + 'Result: ' + tPrint + '\n')
            else:
                txtPath += step
                if step.startswith('Deleting substring'):
                    st = step[-2]
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
            for gen in assemblePathsRecursive(bt, s, t, transforms + ['del t {} {}'.format(C[1], j)], i, C[1]):
                yield gen

        # vertical
        elif C[1] == j:
            for gen in assemblePathsRecursive(bt, s, t, transforms + ['del s {} {}'.format(C[0], i)], C[0], j):
                yield gen

        # diagonal
        else:
            for gen in assemblePathsRecursive(bt, s, t, transforms + ['match'], C[0], C[1]):
                yield gen


def distancesToEmptyString(s, backtracking=0):
    """
    Auxiliary dynamic programming algorithm to compute the homo-edit distance
    between every substring of a string s and the empty string.
    :param s: The string to analyze
    :param backtracking: optional backtracking mode, see help for function homoEditDistance.
    :return:
    """
    n = len(s)
    H = {}

    BT = {} if backtracking == 2 else None

    for l in range(0, n):
        for i in range(0, n - l):
            j = i + l + 1
            if i == j - 1:
                H[(s, i, j)] = 1
            else:
                # C = list([])
                C = {}
                for k in range(i + 1, j):
                    C[k] = (H[(s, i, k)] + H[(s, k, j)] - int(s[i] == s[j - 1]))
                H[(s, i, j)] = int(min(C.values()))

                if backtracking == 2:
                    minKeys = [k for k in C if C[k] == H[(s, i, j)]]
                    BT[(s, i, j)] = minKeys

    ret = {
        'H': H,
    }

    # print('H:\n', H)

    if backtracking == 2:
        ret['BTMatrix'] = BT
    # print(ret)
    return ret
