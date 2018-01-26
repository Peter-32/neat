import pandas as pd
import numpy as np
from sklearn import preprocessing
from sklearn.utils import resample
from math import ceil

class NeatData:

    def __init__(self):
        self.categoryCleaner = None

    def cleanTrainingDataset(self, trainX, trainY, indexColumns=[], skipColumns=[]):
        self.InputValidator()
        trainX, trainY = YCleaner(trainX, trainY)
        self.columnNameCleaner = ColumnNameCleaner()
        self.columnDataTyper = ColumnDataTyper()
        self.yConverter = YConverter()
        self.numberCleaner = NumberCleaner()
        self.datetimeCleaner = DatetimeCleaner()
        self.categoryCleaner = CategoryCleaner()
        self.indexer = Indexer() #TODO: delete this comment.  All indexing should be last in this iteration.
        return trainX, trainY

    def cleanTestDataset(self, testX):
        self._validateCleanedTrainingDataset()
        self._cleanTestDataset(testX)

    def _validateCleanedTrainingDataset(self):
        self.categoryCleaner = None:
            raise Exception('Error: trainX and trainY are differing lengths')
        return

    def _cleanTestDataset(testX):
        pass

    def getYAsNumber(self, testY):
        return TargetConverter().convertToNumber(testY)

    def getYAsString(self, testY):
        return TargetConverter().convertToString(testY)

        #return cleanTestX, cleanTestY








# self.trainX = trainX
# self.trainY = trainY
# self.indexColumns = indexColumns
# self.skipColumns = skipColumns
