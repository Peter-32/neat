import pandas as pd

class DatetimeCleaner:

    def __init__(self):
        self.datetimeColumns = None
        self.x = None

    def clean(self, x, datetimeColumns):
        self.x, self.datetimeColumns = x, datetimeColumns
        self._convertDatetimeToNumber()
        return x

    def _convertDatetimeToNumber(self):
        for column in self.datetimeColumns:
            values = []
            for i, row in self.x.iterrows():
                values.append((pd.datetime.now() - row[column]).days)
            self.x[column] = values
