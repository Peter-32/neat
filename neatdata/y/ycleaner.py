import pandas as pd
import numpy as np

class YCleaner:

    def __init__(self):
        self.yConverter = None

    def cleanTrainingY(self, x, y):
        y = self._castAsNumpyString()
        trainX, trainY = MissingYRowDropper().execute(trainX, trainY)
        self._initializeYConverter()
        trainX, trainY = YBalancer().execute(trainX, trainY)
        return trainX, trainY

    def _castAsNumpyString(self, y):
        y = np.array(y)
        return y.astype(str)

    def _initializeYConverter(self, y):
        self.yConverter = YConverter()
        self.yConverter.setYMappings(y)

    def convertToNumber(self, y):
        return self.yConverter.convertToNumber(y)

    def convertToString(self, y):
        return self.yConverter.convertToString(y)
