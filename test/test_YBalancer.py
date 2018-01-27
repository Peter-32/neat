import unittest
import pandas as pd
import numpy as np
from neatdata.y.ybalancer import *

class TestYBalancer(unittest.TestCase):

    def testYBalancer(self):
        # Assemble
        now = pd.datetime.now()
        trainX = pd.DataFrame({'col1': [1,1,1,1,1,1,1],
                               'col2': ['a','a','a','a','a','a','a'],
                               'col3': [now,now,now,now,now,now,now]})
        trainY_EvenMaximumFrequency = [1, 1, 1, 1, 2, 3, 4, 2]
        trainY_OddMaximumFrequency =  [1, 1, 1, 1, 1, 2, 3, 4, 2]
        # Act
        cleanTrainX, cleanTrainY = YBalancer().execute(trainX, trainY_EvenMaximumFrequency)
        trainYFrequenciesEven = pd.value_counts(cleanTrainY, sort=True, normalize=False)
        cleanTrainX, cleanTrainY = YBalancer().execute(trainX, trainY_OddMaximumFrequency)
        trainYFrequenciesOdd = pd.value_counts(cleanTrainY, sort=True, normalize=False)
        # Assert
        self.assertEqual(trainYFrequenciesEven[1], 4)
        self.assertEqual(trainYFrequenciesEven[2], 2)
        self.assertEqual(trainYFrequenciesEven[3], 2)
        self.assertEqual(trainYFrequenciesEven[4], 2)
        self.assertEqual(trainYFrequenciesOdd[1], 5)
        self.assertEqual(trainYFrequenciesOdd[2], 3)
        self.assertEqual(trainYFrequenciesOdd[3], 3)
        self.assertEqual(trainYFrequenciesOdd[4], 3)
