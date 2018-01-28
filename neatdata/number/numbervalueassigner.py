class NumberValueAssigner:

    def __init__(self):
        self.x, self.numberColumns, self.numberMetadata = None, None, None

    def execute(self, x, numberColumns, numberMetadata):
        self.x, self.numberColumns, self.numberMetadata = x, numberColumns, numberMetadata
        self.x = _fixMissingNumValuesAndInfinity()
        self.x = _fixHighLeveragePoints()

    def _fixMissingNumValuesAndInfinity(self):
        self.x = self.x.fillna(self.numberMetadata.medians) # optionally: replace self.medians with 0
        self.x.replace([np.inf, -np.inf], np.nan)
        self.x = self.x.fillna(self.numberMetadata.upperBounds)

    def _fixHighLeveragePoints(self):
        for i, row in self.x.iterrows():
            for column in self.numberColumns:
                if row[column] > self.numberMetadata.upperBounds[column]:
                    self.x.at[i, column] = self.numberMetadata.upperBounds[column]
                if row[column] < self.numberMetadata.lowerBounds[column]:
                    self.x.at[i, column] = self.numberMetadata.lowerBounds[column]
