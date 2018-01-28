

class CategoryValueAssigner:

    def __init__(self):
        pass



    def _fixMissingCategoryValuesAndMapValuesTo_Other(self):
        for i, row in self.df.iterrows():
            for column in self.categoryColumns:
                if row[column] == None:
                    self.df.at[i, column] = self._getRandomCategoryBasedOnFrequencies(column)
                elif row[column] not in self.valuesThatDontMapTo_Other[column]:
                    self.df.at[i, column] = '_Other'

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
            self.df = pd.concat([self.df.drop(column, axis=1), pd.get_dummies(self.df[column], prefix=column+"_", drop_first=False)], axis=1)
