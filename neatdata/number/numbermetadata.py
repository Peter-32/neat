import numpy as np
class NumberMetadata:

    def __init__(self):
        self.medians, self.lowerBounds, self.upperBounds = None, None, None

    def train(self, trainX, numberColumns):
        trainX = self._ignoreInfinityForQuantiles(trainX)

        firstQuantiles = trainX.quantile(.25)
        thirdQuantiles = trainX.quantile(.75)

        self.medians = trainX.quantile(.50)
        self.lowerBounds = {}
        self.upperBounds = {}
        for column in numberColumns:
            self.lowerBounds[column] = self.medians[column] - 2*(self.medians[column] - firstQuantiles[column])
            self.upperBounds[column] = self.medians[column] + 2*(thirdQuantiles[column] - self.medians[column])

    def _ignoreInfinityForQuantiles(self, trainX):
        return trainX.replace([np.inf, -np.inf], np.nan)
