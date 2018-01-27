import pandas as pd
import numpy as np
from neatdata.numpyhelper.numpyhelper import *

class YCleaner:

    def __init__(self):
        self.yConverter = None
        self.trained = False

    def cleanTrainingY(self, trainX, trainY):
        trainY = castAsNumpy(trainY)
        trainX, trainY = MissingYRowDropper().execute(trainX, trainY)
        if isStringType(trainY):
            self._initializeYConverter()
        trainYMappingsStrToNum
        trainX, trainY = YBalancer().execute(trainX, trainY)
        self.trained = True
        return trainX, trainY

    def _initializeYConverter(self, trainY):
        self.yConverter = YConverter()
        self.yConverter.setYMappings(trainY)

    def convertToNumber(self, trainY):
        if not self.trained: raise Exception('Error: Use cleanTrainingY(x, y) before using convertToNumber(trainY).')
        return self.yConverter.convertToNumber(trainY)

    def convertToString(self, trainY):
        if not self.trained: raise Exception('Error: Use cleanTrainingY(x, y) before using convertToString(trainY).')
        return self.yConverter.convertToString(trainY)
