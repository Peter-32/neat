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
        self.yCleaner = YCleaner(trainX, trainY)
        self.columnNameCleaner = ColumnNameCleaner()
        self.columnDataTyper = ColumnDataTyper()
        self.indexer = Indexer()
        self.yConverter = YConverter()
        self.numberCleaner = NumberCleaner()
        self.datetimeCleaner = DatetimeCleaner()
        self.categoryCleaner = CategoryCleaner()
        return trainX, trainY

    def cleanTestDataset(self, testX):
        self._validateCleanedTrainingDataset()
        self._cleanTestDataset(testX)

    def _validateCleanedTrainingDataset(self):
        self.categoryCleaner = None:
            raise Exception('Error: trainX and trainY are differing lengths')
        return

    def _cleanTestDataset(testX):



    def getYAsNumber(self, testY):
        TargetConverter().convertToString()
        pass

    def getYAsStringUsingMapping(self, testY):
        pass

        #return cleanTestX, cleanTestY








# self.trainX = trainX
# self.trainY = trainY
# self.indexColumns = indexColumns
# self.skipColumns = skipColumns
