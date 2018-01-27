import unittest
import pandas as pd
import numpy as np
from neatdata.y.ycleaner import *

class TestYCleaner(unittest.TestCase):

    def testYCleanerCastAsString(self):
        # Assemble
        trainYStrings = ['a', 'a', 'a', 'a', 'b', 'c', 'd']
        trainYNumbers = [1, 1, 1, 1, 2, 3, 4]
        trainYNumbersStringForm = ["1", "1", "1", "1", "2", "3", "4"]
        yCleaner = YCleaner()
        # Act
        trainYStringsCastedAsString = yCleaner._castAsNumpyString(trainYStrings)
        trainYNumbersCastedAsString = yCleaner._castAsNumpyString(trainYNumbers)
        # Assert
        for i in range(len(trainY)):
            self.assertEqual(trainYStringsCastedAsString[i], trainYStrings[i])
            self.assertEqual(trainYNumbersCastedAsString[i], trainYNumbersStringForm[i])
