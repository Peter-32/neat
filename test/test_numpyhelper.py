import unittest
import pandas as pd
import numpy as np
from neatdata.y.ycleaner import *
from neatdata.numpyhelper.numpyhelper import *

class TestNumpyHelper(unittest.TestCase):

    def testNumpyHelper_CastAsNumpy_IsStringType(self):
        # Assemble
        trainYStrings = ['a', 'a', 'a', 'a', 'b', 'c', 'd']
        trainYNumbers = [1, 1, 1, 1, 2, 3, 4]
        yCleaner = YCleaner()
        trainYStrings = castAsNumpy(trainYStrings)
        trainYNumbers = castAsNumpy(trainYNumbers)
        # Act
        isStringTypeTrue = isStringType(trainYStrings)
        isStringTypeFalse = isStringType(trainYNumbers)
        # Assert
        self.assertTrue(isStringTypeTrue)
        self.assertFalse(isStringTypeFalse)
