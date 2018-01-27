class DatetimeCleaner:

    def __init__(self):
        self.datetimeColumns = None
        self.x = None

    def execute(self, x, datetimeColumns):
        self.x, self.datetimeColumns = x, datetimeColumns
        self._convertDatetimeToNumber()
        return x

    def _convertDatetimeToNumber(self):
        for column in self.datetimeColumns:
            values = []
            for i, row in trainX.iterrows():
                values.append((pd.datetime.now() - row[column]).days)
            self.df[column] = values
