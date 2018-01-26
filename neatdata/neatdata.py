import pandas as pd
import numpy as np
from sklearn import preprocessing
from sklearn.utils import resample
from math import ceil

class NeatData:

    def __init__(self):
        self.indexer = None

    def cleanTrainingDataset(self, trainX, trainY, indexColumns=[], skipColumns=[]):
        trainX, trainY = self._initialTrainingDatasetClean(trainX, trainY)
        trainX, trainY = self._datatypeSpecificTrainingDatasetClean(trainX, trainY)
        trainX, trainY = self._finalTrainingDatasetClean(trainX, trainY)
        return trainX, trainY

    def _initialTrainingDatasetClean(self, trainX, trainY):
        self._validateTrainingInput(trainX, trainY)
        trainX, trainY = YCleaner().execute(trainX, trainY)
        trainX, indexColumns, skipColumns = ColumnNameCleaner().execute(trainX, indexColumns, skipColumns)
        numberColumns, categoryColumns, datetimeColumns = ColumnDataTypeGetter().execute(trainX, indexColumns, skipColumns)
        return trainX, trainY

    def _validateTrainingInput(self, trainX, trainY):
        if len(trainY) != len(trainX.index): raise Exception('Error: trainX and trainY are differing lengths.') else None

    def _datatypeSpecificTrainingDatasetClean(self, trainX, trainY):
        self.numberCleaner = NumberCleaner()
        self.datetimeCleaner = DatetimeCleaner()
        self.categoryCleaner = CategoryCleaner()
        return trainX, trainY

    def _finalTrainingDatasetClean(self, trainX, trainY):
        self.indexer = Indexer() #TODO: delete this comment.  All indexing should be last in this iteration.
        return trainX, trainY












    def cleanTestDataset(self, testX):
        self._validateCleanedTrainingDataset()
        self._cleanTestDataset(testX)

    def _validateCleanedTrainingDataset(self):
        if self.indexer = None: raise Exception('Error: cleanTrainingDataset() must be run first.')

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
