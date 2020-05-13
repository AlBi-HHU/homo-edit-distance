import unittest

from homoeditdistance import *

class TestHED(unittest.TestCase):
    def test_basic(self):
        """
        Basic test, shold always work
        """
        result = homoEditDistance("aba", "aa")
        print(result)
        self.assertEqual(result, {'hed': 1})

if __name__ == '__main__':
    unittest.main()


