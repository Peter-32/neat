import unittest
from neatdata.neatdata import *

class TestNeatData(unittest.TestCase):

    # def test_initialize_without_errors(self):
    #     neatdata()
    #     self.assertEqual(False)

    def testCleanTrainingDataset_ColumnsStayTheSame(self):
        # Assemble
        neatdata = NeatData()
        now = pd.datetime.now()
        trainX = pd.DataFrame({'col1': [1,2,3,1,2,3,1],
                               'col2': ['a','b','c','a','b','c','a'],
                               'col3': [now,now,now,now,now,now,now]})
        trainY = ['a','b','c','a','b','c','a']


        # Act
        cleanTrainX, cleanTrainY = neatdata.cleanTrainingDataset(trainX, trainY)
        # Assert
        self.assertEqual(False)

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
