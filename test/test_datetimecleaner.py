import unittest
import pandas as pd
import numpy as np
from copy import deepcopy
from neatdata.neatdata import *

class TestDatetimeCleaner(unittest.TestCase):

    def testDatetimeCleaner_Execute(self):
        # Assemble
        trainX = pd.DataFrame({'col1': [pd.datetime.now()- pd.Timedelta(days=2),
                                        pd.datetime.now()- pd.Timedelta(days=3),
                                        pd.datetime.now()- pd.Timedelta(days=444),
                                        pd.datetime.now()- pd.Timedelta(days=555)]})
        datetimeColumnName = 'col1'
        datetimeColumns = [datetimeColumnName]
        datetimeCleaner = DatetimeCleaner()
        # Act
        trainX = datetimeCleaner.clean(trainX, deepcopy(datetimeColumns))
        # Assert
        j = 0
        for i, row in trainX.iterrows():
            if j == 0:
                self.assertEqual(row[datetimeColumnName], 2)
            elif j == 1:
                self.assertEqual(row[datetimeColumnName], 3)
            elif j == 2:
                self.assertEqual(row[datetimeColumnName], 444)
            elif j == 3:
                self.assertEqual(row[datetimeColumnName], 555)
            j = j + 1
