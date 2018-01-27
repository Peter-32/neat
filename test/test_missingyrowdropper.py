import unittest
import pandas as pd
import numpy as np
from neatdata.y.missingyrowdropper import *

class TestMissingYRowDropper(unittest.TestCase):

    def testMissingYRowDropper_Execute(self):
        # Assemble
        now = pd.datetime.now()
        trainX = pd.DataFrame({'col1': [1,1,1,1,1,1,1],
                               'col2': ['a','a','a','b','a','b','b'],
                               'col3': [now,now,now,now,now,now,now]})
        trainY = ['a','b','c',np.inf,'b', -np.inf, None]
        # Act
        trainX, trainY = MissingYRowDropper().execute(trainX, trainY)
        # Assert
        self.assertEqual(len(trainY), 4)
        self.assertEqual(len(trainX.index), 4)
        self.assertEqual(trainY[0], 'a')
        self.assertEqual(trainY[1], 'b')
        self.assertEqual(trainY[2], 'c')
        self.assertEqual(trainY[3], 'b')
        for i, row in self.df.iterrows():
            self.assertEqual(row['col2'], 'a')
