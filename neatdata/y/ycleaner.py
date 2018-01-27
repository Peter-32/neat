import pandas as pd
import numpy as np
from neatdata.numpyhelper.numpyhelper import *

class YCleaner:

    def __init__(self):
        self.yConverter = None
        self.trained = False

    def cleanTrainingY(self, x, y):
        y = self.castAsNumpy(y)
        trainX, trainY = MissingYRowDropper().execute(trainX, trainY)
        if isStringType(y):
            self._initializeYConverter()
        trainX, trainY = YBalancer().execute(trainX, trainY)
        self.trained = True
        return trainX, trainY

    def _initializeYConverter(self, y):
        self.yConverter = YConverter()
        self.yConverter.setYMappings(y)

    def convertToNumber(self, y):
        if not self.trained: raise Exception('Error: Use cleanTrainingY(x, y) before using convertToNumber(y).')
        return self.yConverter.convertToNumber(y)

    def convertToString(self, y):
        if not self.trained: raise Exception('Error: Use cleanTrainingY(x, y) before using convertToString(y).')
        return self.yConverter.convertToString(y)
