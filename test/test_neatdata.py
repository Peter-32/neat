import unittest
from neatdata.neatdata import *

class TestNeatData(unittest.TestCase):

    # @classmethod
    # def setUpClass(cls):
    #     cls._connection = createExpensiveConnectionObject()
    #
    # @classmethod
    # def tearDownClass(cls):
    #     cls._connection.destroy()

    def testCleanTrainingDataset_InvalidLengths(self):
        # Assemble
        neatdata = NeatData()
        now = pd.datetime.now()
        trainX = pd.DataFrame({'col1': [1,1,1,1,1,1,1],
                               'col2': ['a','a','a','a','a','a','a'],
                               'col3': [now,now,now,now,now,now,now]})
        trainY = ['a','b','c','a','b','c']
        # Act
        # Assert
        self.assertRaises(SomeCoolException, neatdata.cleanTrainingDataset, trainX, trainY)

    def testCleanTrainingDataset_ColumnsStayTheSame(self):
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
            self.assertEqual(row['col2'], 'a')
            self.assertEqual(row['col3'], 0)

    def testCleanTrainingDataset_ColumnDefaultValues(self):
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
        for i, row in cleanTrainX.iterrows():
            self.assertEqual(row['col2'], 'a')
            self.assertEqual(row['col3'], 0)
            if j < 5:
                self.assertEqual(row['col1'], 2)
            elif j == 5:
                self.assertEqual(row['col1'], 1)
            elif j == 6:
                self.assertEqual(row['col1'], 3)
            j = j + 1

    def testCleanTrainingDataset_DropEmptyColumn(self):
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

# df = pd.DataFrame({'col2': [None,None,None,9,5,10,11,12,13,14,None,None,None,9,5,10,11,12,13,14,11,12,13,14,None,None,None,9,5,10,11,12,13,14,None,None,None,9,5,10,11,12,13,14,11,12,13,14]
#                   , 'col3': ['test1','test1','test1','test3',None,None,'test1','test1','test2','test2','test1','test1','test1','test1',None,None,'test1','test1','test2','test2', 'test1','test1','test2','test2','test1','test1','test1','test1',None,None,'test1','test1','test2','test2','test1','test1','test1','test1',None,None,'test1','test1','test2','test2', 'test1','test1','test2','test2']
#                   , 'col4': [None, 5, 3 ,6 ,8, 9, 14, 87, 999 ,9999,None, 5, 3 ,6 ,8, 9, 14, 87, 999 ,9999, 14, 87, 999 ,9999,None, 5, 3 ,6 ,8, 9, 14, 87, 999 ,9999,None, 5, 3 ,6 ,8, 9, 14, 87, 999 ,9999, 14, 87, 999 ,9999]
#                   , 'col5': ['a','a',None,None,'adsf','bas',None,None,None,None,None,None,None,None,'adsf','bas',None,None,None,None,None,None,None,None,'a','a',None,None,'adsf','bas',None,None,None,None,None,None,None,None,'adsf','bas',None,None,None,None,None,None,None,None]})
#
# targetY = ['a','b','c','a','a','g','b','a','i','t','a','b','c','a','a','g','b','a','i','t','b','a','i','t','a','b','c','a','a','g','b','a','i','t','a','b','c','a','a','g','b','a','i','t','b','a','i','t']
# indexColumns = ['col4']
#
# neat = Neat(df, targetY, indexColumns)
#
# print(neat.df)
# #df = neat.df
#
# neat.cleanNewData(df)
#
# neat.df
