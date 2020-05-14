#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""unittests to use with unittest. Run `python3 -m unittest` from repository root."""

import unittest
from homoeditdistance import *


class TestHED(unittest.TestCase):
    def test_basic(self):
        """
        Basic test, should always work
        """
        result = homoEditDistance('aba', 'aa')
        # print(result)
        self.assertEqual(result, {'hed': 1})

    def test_empty(self):
        """
        Test with empty strings
        """
        result = homoEditDistance('', '')
        self.assertEqual(result, {'hed': 0})


if __name__ == '__main__':
    unittest.main()
