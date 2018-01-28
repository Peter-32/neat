import pandas as pd
import numpy as np

class CategoryMetadata:

    def __init__(self):
        self.trainX, self.categoryColumns = None, None
        self.valuesThatDontMapTo_Other = None
        self.categoryFrequencies = None
        self.uniqueCategoryValues = None

    def train(self, trainX, categoryColumns):
        self.trainX, self.categoryColumns = trainX, categoryColumns
        self.valuesThatDontMapTo_Other, self.categoryFrequencies = {}, {}
        self.uniqueCategoryValues = {}
        self._saveUniqueCategoryValues()
        self._saveCategoryFrequenciesAndValuesThatDontMapTo_Other()

    def _saveUniqueCategoryValues(self):
        for column in self.categoryColumns:
            self.uniqueCategoryValues[column] = []
            for value in self.trainX[column].unique():
                if value == None or pd.isnull(value):
                    continue
                else:
                    self.uniqueCategoryValues[column].append(value)
            self.uniqueCategoryValues[column].append('_Other')

    def _saveCategoryFrequenciesAndValuesThatDontMapTo_Other(self):
        for column in self.categoryColumns:
            _otherFrequency = 0
            self.valuesThatDontMapTo_Other[column] = ['_Other']
            frequencyPercentage = pd.value_counts(self.trainX[column].values, sort=False, normalize=True)
            self.categoryFrequencies[column] = {}
            for value in self.uniqueCategoryValues[column]:
                if value == '_Other':
                    continue
                elif frequencyPercentage[value] < .05:
                    _otherFrequency = _otherFrequency + frequencyPercentage[value]
                else:
                    self.valuesThatDontMapTo_Other[column].append(value)
                    self.categoryFrequencies[column][value] = frequencyPercentage[value]
            self.categoryFrequencies[column]['_Other'] = _otherFrequency
