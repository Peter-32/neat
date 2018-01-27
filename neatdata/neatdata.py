import pandas as pd
import numpy as np
from sklearn import preprocessing
from sklearn.utils import resample
from math import ceil
from copy import deepcopy

class NeatData:

    def __init__(self):
        self.indexer = None # TODO: Unsure
        self.numberColumns, self.categoryColumns, self.datetimeColumns = None, None, None
        self.indexColumns, self.skipColumns = None, None

    def cleanTrainingDataset(self, trainX, trainY, indexColumns=[], skipColumns=[]):
        trainX, trainY = self._initial(trainX, trainY)
        trainX, trainY = self._datatypeSpecific(trainX, trainY)
        trainX, trainY = self._final(trainX, trainY)
        return trainX, trainY

    def _initial(self, trainX, trainY):
        self._validateTrainingInput(trainX, trainY)
        trainX, trainY = YCleaner().execute(trainX, trainY)
        trainX, indexColumns, skipColumns = ColumnNameCleaner().execute(trainX, indexColumns, skipColumns)
        self.numberColumns, self.categoryColumns, self.datetimeColumns = ColumnDataTypeGetter().execute(trainX, indexColumns, skipColumns)
        return trainX, trainY

    def _validateTrainingInput(self, trainX, trainY):
        if len(trainY) != len(trainX.index): raise Exception('Error: trainX and trainY are differing lengths.')

    def _datatypeSpecific(self, trainX, trainY):
        self.datetimeCleaner = DatetimeCleaner()
        trainX = self.datetimeCleaner.execute(trainX, deepcopy(self.datetimeColumns))
        self.numberCleaner = NumberCleaner()
        trainX = self.numberCleaner.execute(trainX, deepcopy(self.numberColumns))
        self.categoryCleaner = CategoryCleaner()
        trainX = self.categoryCleaner.execute(trainX, deepcopy(self.categoryColumns))
        return trainX, trainY

    def _final(self, trainX, trainY):
        self.indexer = Indexer() #TODO: delete this comment.  All indexing should be last in this iteration.
        return trainX, trainY




    def cleanTestDataset(self, testX):
        self._validateCleanedTrainingDataset()
        self._cleanTestDataset(testX)

    def _validateCleanedTrainingDataset(self):
        if self.indexer == None: raise Exception('Error: cleanTrainingDataset() must be run first.')

    def _cleanTestDataset(testX):
        pass

    def getYAsNumber(self, testY):
        return yConverter().convertToNumber(testY)

    def getYAsString(self, testY):
        return yConverter().convertToString(testY)

        #return cleanTestX, cleanTestY








# self.trainX = trainX
# self.trainY = trainY
# self.indexColumns = indexColumns
# self.skipColumns = skipColumns
