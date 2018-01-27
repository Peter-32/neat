import pandas as pd
import numpy as np
from sklearn.utils import resample
from neatdata.numpyhelper.numpyhelper import *
from math import ceil

class YBalancer:

    def __init__(self):
        self.trainYFrequencies, self.trainYUpsamplesNeeded = None, None
        self.trainX, self.trainY = None, None
        self.uniqueValues = None

    def execute(self, trainX, trainY):
        self.trainX, self.trainY = trainX, castAsNumpy(trainY)
        self.uniqueValues = np.unique(trainY)
        self.trainYUpsamplesNeeded = {}
        self._saveTrainYFrequencies()
        self._saveTrainYUpsamplesNeeded()
        self._fixTrainYImbalance()
        return self.trainX, self.trainY

    def _saveTrainYFrequencies(self):
        self.trainYFrequencies = pd.value_counts(self.trainY, sort=True, normalize=False)

    def _saveTrainYUpsamplesNeeded(self):
        maxCount = self._findTheMaxCount()
        minCountAllowed = ceil(maxCount / 2)
        for value in self.uniqueValues:
            actualFrequency = self.trainYFrequencies[value]
            idealTrainYFrequency = minCountAllowed if actualFrequency < minCountAllowed else actualFrequency
            self.trainYUpsamplesNeeded[value] = idealTrainYFrequency - actualFrequency

    def _findTheMaxCount(self):
        maxCount = None
        for value in self.uniqueValues:
            frequency = self.trainYFrequencies[value]
            if maxCount == None or frequency > maxCount:
                maxCount = frequency
        return maxCount

    def _fixTrainYImbalance(self):
        self.trainX['__trainY__'] = self.trainY
        for value in self.uniqueValues:
            samplesToGet = self.trainYUpsamplesNeeded[value]
            if samplesToGet > 0:
                upsampleRows = resample(self.trainX[self.trainX['__trainY__']==value],
                                    replace=True,
                                    n_samples=samplesToGet,
                                    random_state=123)
                self.trainX = pd.concat([self.trainX, upsampleRows])
        self.trainY = self.trainX['__trainY__'].values
        self.trainX = self.trainX.drop(['__trainY__'], 1)
