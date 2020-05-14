#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Analyze two strings for their homo-edit distance.

Implementation of the homo-edit-distance as described in
add paper ref once it is accepted or location on some archive
"""

__author__ = 'Maren Brand, Gunnar W. Klau, Philipp Spohr, Nguyen Khoa Tran'
__credits__ = ['Maren Brand', 'Gunnar W. Klau', 'Philipp Spohr', 'Nguyen Khoa Tran']
__license__ = 'MIT'
__copyright__ = 'Copyright (C) 2020 by AlBi-HHU (gunnar.klau@hhu.de),  all rights reserved, MIT license.'
__email__ = 'gunnar.klau@hhu.de'
# __revision__ = ''
# __date__ = ''
# __version__ = ''
# __maintainer__ = ''
# __status__ = ''

from homoeditdistance.algorithm import homoEditDistance, backtrack, assemblePaths

__all__ = ['homoEditDistance', 'backtrack', 'assemblePaths']
