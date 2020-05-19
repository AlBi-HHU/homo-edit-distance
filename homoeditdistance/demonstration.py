#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Usage demonstration for the homoeditdistance package."""

import sys
import argparse
from homoeditdistance import homoEditDistance, backtrack, assemblePaths


def get_parser():
    """
    Returns the argument parser used to parse the command line used for invoking the demo application.
    Used internally, exists solely for readability.
    :return: The ArgumentParser.
    """
    parser = argparse.ArgumentParser(description='Given two strings, find their homo-edit distance',
                                     fromfile_prefix_chars='@')

    parser.add_argument('-s', '--string1', required=True,
                        help='first string. Use quotation marks around your string (e.g. "STRING")'
                             'for the empty string or strings with special characters')
    parser.add_argument('-t', '--string2', required=True,
                        help='second string')
    parser.add_argument('-a', '--all', action='store_true', default=False, required=False,
                        help='show all optimal subsequences')
    parser.add_argument('-b', '--backtrace', action='store_true', default=False, required=False,
                        help='print transformation steps')
    return parser


def run(args):
    """
    The main function of the
    :param args: The arguments provided by the user and pre-parsed by our argument parser.
    """
    s, t = args.string1, args.string2

    requiredBacktrackLevel = 0
    if args.backtrace:
        requiredBacktrackLevel = 2
    elif args.all:
        requiredBacktrackLevel = 1

    result = homoEditDistance(s, t, requiredBacktrackLevel)
    print('The homo-edit distance between {} and {} is {}\n'.format(
            s if s != '' else 'the empty string',
            t if t != '' else 'the empty string',
            result['hed']
        )
    )

    if args.all and args.backtrace:
        print('The following optimal subsequences were found, and obtained using the listed operations:')
        subs = backtrack(result['bt'], s, t)
        txt = dict(assemblePaths(result['bt'], s, t, result['zbt']))
        for sup in set(subs):
            print()
            if sup == '':
                print('empty string')
            else:
                print(sup)
            print(txt[sup].strip())

    elif args.all:
        print('The following optimal subsequences were found:')
        subs = backtrack(result['bt'], s, t)
        for sup in set(subs):
            print(sup, end=' ')

    elif args.backtrace:
        print('Detailed Backtracking for one possible subsequence:')
        txt = dict(assemblePaths(result['bt'], s, t, result['zbt']))
        key = next(iter(txt))
        print(key)
        print(txt[key])


def main():
    """Run the demo."""
    run(get_parser().parse_args(sys.argv[1:]))
