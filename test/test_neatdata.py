import unittest
import pandas as pd
import numpy as np
from neatdata.neatdata import *

class TestNeatData(unittest.TestCase):

    # @classmethod
    # def setUpClass(cls):
    #     cls._connection = createExpensiveConnectionObject()
    #
    # @classmethod
    # def tearDownClass(cls):
    #     cls._connection.destroy()

    def testNeatData_TestCleanTrainingDataset_InvalidLengths(self):
        # Assemble
        neatdata = NeatData()
        now = pd.datetime.now()
        trainX = pd.DataFrame({'col1': [1,1,1,1,1,1,1],
                               'col2': ['a','a','a','a','a','a','a'],
                               'col3': [now,now,now,now,now,now,now]})
        trainY = ['a','b','c','a','b','c']
        # Act
        # Assert
        self.assertRaises(Exception, neatdata.cleanTrainingDataset, trainX, trainY)

    def testNeatData_TestCleanTrainingDataset_ColumnsStayTheSame(self):
        # Assemble
        neatdata = NeatData()
        now = pd.datetime.now()
        trainX = pd.DataFrame({'col1': [1,1,1,1,1,1,1],
                               'col2': ['a','a','a','a','a','a','a'],
                               'col3': [now,now,now,now,now,now,now]})
        trainY = ['a','b','c','a','b','c','a']
        # Act
        cleanTrainX, cleanTrainY = neatdata.cleanTrainingDataset(trainX, trainY)
        # Assert
        for i, row in cleanTrainX.iterrows():
            self.assertEqual(row['col1'], 1)
            self.assertEqual(row['col2__a'], 1)
            self.assertEqual(row['col3'], 0)

    def testNeatData_TestCleanTrainingDataset_ColumnDefaultValues(self):
        # Assemble
        neatdata = NeatData()
        now = pd.datetime.now()
        trainX = pd.DataFrame({'col1': [1,2,3,None,None,-np.inf,np.inf],
                               'col2': ['a','a','a',None,None,None,None],
                               'col3': [now,now,now,None,None,None,None]})
        trainY = ['a','b','c','a','b','c','a']
        # Act
        cleanTrainX, cleanTrainY = neatdata.cleanTrainingDataset(trainX, trainY)
        # Assert
        j = 0
        print(cleanTrainX)
        for i, row in cleanTrainX.iterrows():
            self.assertEqual(row['col2__a'], 1)
            self.assertEqual(row['col3'], 0)
            if j == 0:
                self.assertEqual(row['col1'], 1)
            elif j == 1:
                self.assertEqual(row['col1'], 2)
            elif j == 2:
                self.assertEqual(row['col1'], 3)
            elif j == 3 or j == 4:
                self.assertEqual(row['col1'], 2)
            elif j == 5:
                self.assertEqual(row['col1'], 1)
            elif j == 6:
                self.assertEqual(row['col1'], 3)
            j = j + 1

    def testNeatData_TestCleanTrainingDataset_DropEmptyColumn(self):
        # Assemble
        neatdata = NeatData()
        now = pd.datetime.now()
        trainX = pd.DataFrame({'col1': [1,1,1,1,1,1,1],
                               'col2': [None,None,None,None,None,None,None],
                               'col3': [now,now,now,now,now,now,now]})
        trainY = ['a','b','c','a','b','c','a']
        # Act
        cleanTrainX, cleanTrainY = neatdata.cleanTrainingDataset(trainX, trainY)
        # Assert
        columns = cleanTrainX.columns.values.tolist()
        self.assertEqual('col1' in columns, True)
        self.assertEqual('col2' in columns, False)
        self.assertEqual('col3' in columns, True)





    if __name__ == "__main__":
        unittest.main()
