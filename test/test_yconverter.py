import unittest
import pandas as pd
import numpy as np
from neatdata.y.missingyrowdropper import *
from neatdata.y.yconverter import *
from neatdata.y.ycleaner import *


class TestYConverter(unittest.TestCase):

    def testYConverter_ConvertToNumberAndString(self):
        # Assemble
        trainYStr = ['a', 'a', 'a', 'a', 'b', 'c', 'd']
        trainYNum = [1, 1, 1, 1, 2, 3, 4]
        # Act
        yConverter = YConverter()
        yConverter.setYMappings(trainYStr)
        TrainYConvertedToNum = yConverter.convertToNumber(trainYStr)
        TrainYConvertedToStr = yConverter.convertToString(TrainYConvertedToNum)
        # Assert
        for i in range(len(trainYStr)):
            self.assertEqual(TrainYConvertedToStr[i], trainYStr[i])
            self.assertEqual(TrainYConvertedToNum[i], trainYNum[i])

    def testYConverter_SetMappingWithNanValuesSkipsNanMapping(self):
        # Assemble
        now = pd.datetime.now()
        x = pd.DataFrame({'col1': [1,1,1,1,1,1,1],
                               'col2': ['a','a','a','a','a','a','a'],
                               'col3': [now,now,now,now,now,now,now]})
        y = [0, 0, 0, 0, 1, 2, np.nan]
        y = YCleaner()._castAsNumpyString(y)
        x, y = MissingYRowDropper().execute(x, y)
        yConverter = YConverter()
        # Act
        yConverter.setYMappings(y)
        # Assert
        self.assertEqual(len(yConverter._trainYMappingsStrToNum), 4)
        self.assertEqual(len(yConverter._trainYMappingsNumToStr), 4)
        self.assertTrue(0 in yConverter._trainYMappingsNumToStr)
        self.assertTrue(1 in yConverter._trainYMappingsNumToStr)
        self.assertTrue(2 in yConverter._trainYMappingsNumToStr)
        self.assertTrue(-99 in yConverter._trainYMappingsNumToStr)
        self.assertTrue("0.0" in yConverter._trainYMappingsStrToNum)
        self.assertTrue("1.0" in yConverter._trainYMappingsStrToNum)
        self.assertTrue("2.0" in yConverter._trainYMappingsStrToNum)
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
        self.assertTrue(0 in yConverter._trainYMappingsNumToStr)
        self.assertTrue(1 in yConverter._trainYMappingsNumToStr)
        self.assertTrue(2 in yConverter._trainYMappingsNumToStr)
        self.assertTrue(3 in yConverter._trainYMappingsNumToStr)
        self.assertTrue(-99 in yConverter._trainYMappingsNumToStr)
        self.assertTrue("a" in yConverter._trainYMappingsStrToNum)
        self.assertTrue("b" in yConverter._trainYMappingsStrToNum)
        self.assertTrue("c" in yConverter._trainYMappingsStrToNum)
        self.assertTrue("z" in yConverter._trainYMappingsStrToNum)
        self.assertTrue("NotFound" in yConverter._trainYMappingsStrToNum)
