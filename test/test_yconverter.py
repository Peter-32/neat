import unittest
import numpy as np
from neatdata.y.yconverter import *


class TestYConverter(unittest.TestCase):

    def testYConverter_ConvertToNumberAndString(self):
        # Assemble
        trainYStr = ['a', 'a', 'a', 'a', 'b', 'c', 'd']
        trainYNum = [1, 1, 1, 1, 2, 3, 4]
        # Act
        yConverter = YConverter().setYMappings(trainYStr)
        TrainYConvertedToNum = yConverter.convertToNumber(trainYStr)
        TrainYConvertedToStr = yConverter.convertToString(TrainYConvertedToNum)
        # Assert
        for i in range(len(trainYStr)):
            self.assertEqual(TrainYConvertedToStr[i], trainYStr[i])
            self.assertEqual(TrainYConvertedToNum[i], trainYNum[i])

    def testYConverter_SetMappingWithNanValuesSkipsNanMapping(self):
        # Assemble
        y = [1, 1, 1, 1, 2, 3, np.nan]
        y = YCleaner()._castAsNumpyString(y)
        yConverter = YConverter()
        # Act
        yConverter.setYMappings(y)
        # Assert
        self.assertEqual(len(yConverter._trainYMappingsStrToNum), 4)
        self.assertEqual(len(yConverter._trainYMappingsNumToStr), 4)
        self.assertTrue(1 in yConverter._trainYMappingsNumToStr)
        self.assertTrue(2 in yConverter._trainYMappingsNumToStr)
        self.assertTrue(3 in yConverter._trainYMappingsNumToStr)
        self.assertTrue(-99 in yConverter._trainYMappingsNumToStr)
        self.assertTrue("1" in yConverter._trainYMappingsStrToNum)
        self.assertTrue("2" in yConverter._trainYMappingsStrToNum)
        self.assertTrue("3" in yConverter._trainYMappingsStrToNum)
        self.assertTrue("NotFound" in yConverter._trainYMappingsStrToNum)

    def testYConverter_SetMappingAutoIncrementsStrings(self):
        # Assemble
        y = ["a", "b", "c", "z"]
        yConverter = YConverter()
        # Act
        yConverter.setYMappings(y)
        # Assert
        self.assertEqual(len(yConverter._trainYMappingsStrToNum), 5)
        self.assertEqual(len(yConverter._trainYMappingsNumToStr), 5)
        self.assertTrue(1 in yConverter._trainYMappingsNumToStr)
        self.assertTrue(2 in yConverter._trainYMappingsNumToStr)
        self.assertTrue(3 in yConverter._trainYMappingsNumToStr)
        self.assertTrue(4 in yConverter._trainYMappingsNumToStr)
        self.assertTrue(-99 in yConverter._trainYMappingsNumToStr)
        self.assertTrue("a" in yConverter._trainYMappingsStrToNum)
        self.assertTrue("b" in yConverter._trainYMappingsStrToNum)
        self.assertTrue("c" in yConverter._trainYMappingsStrToNum)
        self.assertTrue("z" in yConverter._trainYMappingsStrToNum)
        self.assertTrue("NotFound" in yConverter._trainYMappingsStrToNum)
