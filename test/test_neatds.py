import unittest
from neatDS.neatDS import *

class TestNeatDS(unittest.TestCase):

    def test_initialize_without_errors(self):
        neatDS()

        self.assertEqual(False)
        #(Put the assemble, act, assert code here)
        #(To assert do:)
        #self.assertEqual(yourVariable, yourExpectedResult)

    if __name__ == "__main__":
        unittest.main()
