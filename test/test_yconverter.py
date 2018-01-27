import unittest
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
        for i in range(len(trainYStr)-1):
            self.assertEqual(TrainYConvertedToStr[i], trainYStr[i])
            self.assertEqual(TrainYConvertedToNum[i], trainYNum[i])

    def testYConverter_SetMappingWithNanValuesSkipsNanMapping(self):
        # Assemble
        trainY = [1, 1, 1, 1, 2, 3, nan]
        # Act
        yConverter = YConverter().setYMappings(trainY)
        trainY = yConverter.convertToNumber(trainYStr)
        TrainYConvertedToStr = yConverter.convertToString(TrainYConvertedToNum)
        # Assert
        for i in range(len(trainYStr)-1):
            self.assertEqual(TrainYConvertedToStr[i], trainYStr[i])
            self.assertEqual(TrainYConvertedToNum[i], trainYNum[i])
