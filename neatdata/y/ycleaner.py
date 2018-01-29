import pandas as pd
import numpy as np
from neatdata.numpyhelper.numpyhelper import *
from neatdata.y.missingyrowdropper import *
from neatdata.y.yconverter import *
from neatdata.y.ybalancer import *

class YCleaner:

    def __init__(self):
        self.yConverter = None
        self.trained = False

    def cleanTrainingY(self, trainX, trainY):
        trainY = castAsNumpy(trainY)
        trainX, trainY = MissingYRowDropper().execute(trainX, trainY)
        if isStringType(trainY):
            self._initializeYConverter(trainY)
        trainX, trainY = YBalancer().execute(trainX, trainY)
        self.trained = True
        return trainX, trainY

    def _initializeYConverter(self, trainY):
        self.yConverter = YConverter()
        self.yConverter.setYMappings(trainY)

    def convertYToNumbersForModeling(self, trainY):
        if not self.trained: raise Exception('Error: Use cleanTrainingY(x, y) before using convertToNumber(trainY).')
        return self.yConverter.convertYToNumbersForModeling(trainY)

    def convertYToStringsOrNumbersForPresentation(self, trainY):
        if not self.trained: raise Exception('Error: Use cleanTrainingY(x, y) before using convertToString(trainY).')
        return self.yConverter.convertYToStringsOrNumbersForPresentation(trainY)
