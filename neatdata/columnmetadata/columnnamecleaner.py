class ColumnNameCleaner:

    def __init__(self):
        pass

    def execute(trainX, indexColumns, skipColumns):
        trainX = self.cleanColumnNamesOnDF(trainX)
        indexColumns = self._cleanArrayOfColumnNames(indexColumns)
        skipColumns = self._cleanArrayOfColumnNames(skipColumns)

        return trainX, indexColumns, skipColumns

    def cleanColumnNamesOnDF(self, trainX):
        trainX.columns = trainX.columns.str.strip().str.lower().str.replace(' ', '_')
        return trainX

    def _cleanArrayOfColumnNames(self, columns):
        if type(columns) == str:
            columns = [columns]
        arr = []
        for column in columns:
            arr.append(self._cleanColumnName(column))
        return arr

    def _cleanColumnName(self, string):
        return string.strip().lower().replace(' ', '_')
