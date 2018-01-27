import pandas as pd
from neatdata.numpyhelper.numpyhelper import isStringType

class MissingYRowDropper:

    def __init__(self):
        self.rowsToDrop = None

    def execute(self, trainX, trainY):
        self.rowsToDrop = []
        trainX['__trainY__'] = trainY
        self._appendToRowsToDropForNoneValue()
        self._appendToRowsToDropForNan()
        trainX = trainX.drop(trainX.index[rowsToDrop])
        trainY = trainX['__trainY__'].values
        trainX = trainX.drop(['__trainY__'], 1)
        return trainX, trainY

    def _appendToRowsToDropForNoneValue(self, trainX):
        for i, row in trainX.iterrows():
            self.rowsToDrop.append(i) if row['__trainY__'] == None else None

    def _appendToRowsToDropForNan(self, trainX, trainY):
        if isStringType(trainY):
            for i, row in trainX.iterrows():
                self.rowsToDrop.append(i) if np.isnan(newDataY[i]) else None
