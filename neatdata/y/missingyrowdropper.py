import pandas as pd
from neatdata.numpyhelper.numpyhelper import *

class MissingYRowDropper:

    def __init__(self):
        self.rowsToDrop = None

    def execute(self, trainX, trainY):
        self.rowsToDrop = []
        trainX['__trainY__'] = trainY
        self._appendToRowsToDropForNoneValue(trainX)
        self._appendToRowsToDropForNan(trainX, trainY)
        trainX = trainX.drop(trainX.index[self.rowsToDrop])
        trainY = trainX['__trainY__'].values
        trainX = trainX.drop(['__trainY__'], 1)
        return trainX, trainY

    def _appendToRowsToDropForNoneValue(self, trainX):
        for i, row in trainX.iterrows():
            self.rowsToDrop.append(i) if row['__trainY__'] == None else None

    def _appendToRowsToDropForNanAndInf(self, trainX, trainY):
        if isStringType(trainY):
            for i, row in trainX.iterrows():
                self.rowsToDrop.append(i) if np.isnan(row['__trainY__']) else None
                self.rowsToDrop.append(i) if row['__trainY__'] == np.inf else None
                self.rowsToDrop.append(i) if row['__trainY__'] == -np.inf else None
