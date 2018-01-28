import pandas as pd
import numpy as np

class CategoryValueAssigner:

    def __init__(self):
        self.x, self.categoryColumns = None, None
        self.valuesThatDontMapTo_Other = None
        self.categoryFrequencies = None
        self.uniqueCategoryValues = None

    def execute(self, x, categoryColumns, categoryMetadata):
        self.x, self.categoryColumns = x, categoryColumns
        self.valuesThatDontMapTo_Other = categoryMetadata.valuesThatDontMapTo_Other
        self.categoryFrequencies = categoryMetadata.categoryFrequencies
        self.uniqueCategoryValues = categoryMetadata.uniqueCategoryValues
        self._fixMissingCategoryValuesAndMapValuesTo_Other()
        self._applyOneHotEncoding()
        return self.x

    def _fixMissingCategoryValuesAndMapValuesTo_Other(self):
        for i, row in self.x.iterrows():
            for column in self.categoryColumns:
                if row[column] == None:
                    self.x.at[i, column] = self._getRandomCategoryBasedOnFrequencies(column)
                elif row[column] not in self.valuesThatDontMapTo_Other[column]:
                    self.x.at[i, column] = '_Other'

    def _getRandomCategoryBasedOnFrequencies(self, column):
        chosenValue, prevValue, cumulativeProbability = None, None, 0
        randomNumber = np.random.uniform(0,1,1)[0]
        for value in self.uniqueCategoryValues[column]:
            if value in self.valuesThatDontMapTo_Other[column]:
                probabilityOfValue, prevValue = self.categoryFrequencies[column][value], value
                cumulativeProbability = cumulativeProbability + probabilityOfValue
                if cumulativeProbability > randomNumber:
                    chosenValue = value
                    break
        return prevValue if chosenValue == None else chosenValue

    def _applyOneHotEncoding(self): # don't drop_first => one hot encoding instead of dummy encoding
        for column in self.categoryColumns:
            self.x = pd.concat([self.x.drop(column, axis=1), pd.get_dummies(self.x[column], prefix=column+"_", drop_first=False)], axis=1)
