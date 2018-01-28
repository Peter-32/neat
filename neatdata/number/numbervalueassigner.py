class NumberValueAssigner:

    def __init__(self):
        self.x, self.numberColumns, self.numberMetadata = None, None, None

    def execute(self, x, numberColumns, numberMetadata):
        self.x, self.numberColumns, self.numberMetadata = x, numberColumns, numberMetadata
        x = _fixMissingNumValuesAndInfinity(x)
        x = _fixHighLeveragePoints(x)

    def _fixMissingNumValuesAndInfinity(self, x):
        x = x.fillna(self.numberMetadata.medians) # optionally: replace self.medians with 0
        x.replace([np.inf, -np.inf], np.nan)
        x = x.fillna(self.numberMetadata.upperBounds)
        return x

    def _fixHighLeveragePoints(self, x):
        for i, row in x.iterrows():
            for column in self.numberColumns:
                if row[column] > self.numberMetadata.upperBounds[column]:
                    x.at[i, column] = self.numberMetadata.upperBounds[column]
                if row[column] < self.numberMetadata.lowerBounds[column]:
                    x.at[i, column] = self.numberMetadata.lowerBounds[column]
        return x
