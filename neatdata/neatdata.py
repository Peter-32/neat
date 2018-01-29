import pandas as pd
import numpy as np
from sklearn import preprocessing
from sklearn.utils import resample
from math import ceil
from copy import deepcopy
from neatdata.category.categorycleaner import *
from neatdata.category.categorydropcolumns import *
from neatdata.category.categorymetadata import *
from neatdata.category.categoryvalueassigner import *
from neatdata.columnmetadata.columndatatypegetter import *
from neatdata.columnmetadata.columnnamecleaner import *
from neatdata.datetime.datetimecleaner import *
from neatdata.indexer.indexer import *
from neatdata.number.numbercleaner import *
from neatdata.numpyhelper.numpyhelper import *
from neatdata.testdataset.testdataset import *
from neatdata.y.ycleaner import *


class NeatData:

    def __init__(self):
        self.indexer = None # TODO: Unsure
        self.numberColumns, self.categoryColumns, self.datetimeColumns = None, None, None
        self.indexColumns, self.skipColumns = None, None
        self.columnsDropped = []
        self.finalColumnNames = None
        self.yCleaner = None

    def cleanTrainingDataset(self, trainX, trainY, indexColumns=[], skipColumns=[]):
        self.indexColumns, self.skipColumns = indexColumns, skipColumns
        trainX, trainY = self._initial(trainX, trainY)
        trainX, trainY = self._datatypeSpecific(trainX, trainY)
        trainX, trainY = self._final(trainX, trainY)
        return trainX, trainY

    def _initial(self, trainX, trainY):
        self._validateTrainingInput(trainX, trainY)
        self.yCleaner = YCleaner()
        trainX, trainY = self.yCleaner.cleanTrainingY(trainX, trainY)
        trainX, self.indexColumns, self.skipColumns = ColumnNameCleaner().execute(trainX, self.indexColumns, self.skipColumns)
        self.numberColumns, self.categoryColumns, self.datetimeColumns = ColumnDataTypeGetter().execute(trainX, self.indexColumns, self.skipColumns)
        return trainX, trainY

    def _validateTrainingInput(self, trainX, trainY):
        if len(trainY) != len(trainX.index): raise Exception('Error: trainX and trainY are differing lengths.')

    def _datatypeSpecific(self, trainX, trainY):
        self.datetimeCleaner = DatetimeCleaner()
        trainX = self.datetimeCleaner.clean(trainX, deepcopy(self.datetimeColumns))
        self.numberCleaner = NumberCleaner()
        trainX = self.numberCleaner.cleanAndLearn(trainX, deepcopy(self.numberColumns))
        self.categoryCleaner = CategoryCleaner()
        trainX = self.categoryCleaner.cleanAndLearn(trainX, self.categoryColumns, self.columnsDropped) # Rare mutates to both arrays
        return trainX, trainY

    def _final(self, trainX, trainY):
        self.indexer = Indexer() #TODO: delete this comment.  All indexing should be last in this iteration.
        self.indexer.execute(trainX, trainY, deepcopy(self.indexColumns))
        self.finalColumnNames = list(trainX)
        return trainX, trainY

    def cleanTestDataset(self, testX):
        self._validateCleanedTrainingDataset()
        return self._cleanTestDataset(testX)

    def _validateCleanedTrainingDataset(self):
        if self.finalColumnNames == None: raise Exception('Error: cleanTrainingDataset() must be run first.')

    def _cleanTestDataset(testX):
        ColumnNameCleaner().cleanColumnNamesOnDF(testX)
        testX = self.datetimeCleaner.clean(testX, deepcopy(self.datetimeColumns))
        testX = self.numberCleaner.clean(testX)
        testX = self.categoryCleaner.clean(testX)
        testX = self.indexer.addIndex(testX)
        testX = TestDataset().execute(self, x, columnsDropped, finalColumnNames)
        return testX

    def convertYToNumbersForModeling(self, testY):
        return self.yCleaner.convertYToNumbersForModeling(testY)

    def convertYToStringsOrNumbersForPresentation(self, testY):
        return self.yCleaner.convertYToStringsOrNumbersForPresentation(testY)


### throwaway test:
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
