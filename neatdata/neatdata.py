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
        trainX, trainY = self.yCleaner.execute(trainX, trainY)
        trainX, self.indexColumns, self.skipColumns = ColumnNameCleaner().execute(trainX, self.indexColumns, self.skipColumns)
        self.numberColumns, self.categoryColumns, self.datetimeColumns = ColumnDataTypeGetter().execute(trainX, self.indexColumns, self.skipColumns)
        return trainX, trainY

    def _validateTrainingInput(self, trainX, trainY):
        if len(trainY) != len(trainX.index): raise Exception('Error: trainX and trainY are differing lengths.')

    def _datatypeSpecific(self, trainX, trainY):
        self.datetimeCleaner = DatetimeCleaner()
        trainX = self.datetimeCleaner.execute(trainX, deepcopy(self.datetimeColumns))
        self.numberCleaner = NumberCleaner()
        trainX = self.numberCleaner.execute(trainX, deepcopy(self.numberColumns))
        self.categoryCleaner = CategoryCleaner()
        trainX = self.categoryCleaner.execute(trainX, self.categoryColumns, self.columnsDropped) # Rare mutates to both arrays
        return trainX, trainY

    def _final(self, trainX, trainY):
        self.indexer = Indexer() #TODO: delete this comment.  All indexing should be last in this iteration.
        self.indexer.execute(trainX, trainY, deepcopy(self.indexColumns))
        self.finalColumnNames = list(trainX)
        return trainX, trainY

    def cleanTestDataset(self, testX):
        self._validateCleanedTrainingDataset()
        self._cleanTestDataset(testX)

    def _validateCleanedTrainingDataset(self):
        if self.finalColumnNames == None: raise Exception('Error: cleanTrainingDataset() must be run first.')

    def _cleanTestDataset(testX):
        testX
        # Column Metadata
        ColumnNameCleaner().execute(testX, self.indexColumns, self.skipColumns)
        # Datetimes
        self._convertDatetimeToNumber()
        # Numbers
        self._fixMissingNumValuesAndInfinity()
        self._fixHighLeveragePoints()
        # Categories
        self._fixMissingCategoryValuesAndMapValuesTo_Other()
        self._applyOneHotEncoding()
        # Index
        self._addIndex()
        # New Data
        self._newDataDropDroppedColumns()
        self._newDataAddMissingFinalColumnNames()
        self._newDataDropExtraColumnNames()

    def convertToNumberForModeling(self, testY):
        return self.yCleaner.convertToNumberForModeling(testY)

    def convertToStringOrNumberForPresentation(self, testY):
        return self.yCleaner.convertToStringOrNumberForPresentation(testY)


        #return cleanTestX, cleanTestY






# self.trainX = trainX
# self.trainY = trainY
# self.indexColumns = indexColumns
# self.skipColumns = skipColumns
