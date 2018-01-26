class ColumnDataTypeGetter:
    def __init__(self):
        pass

    def execute(self, trainX, indexColumns, skipColumns):
        columns = self.trainX.columns.values.tolist()
        numberColumns = []
        categoryColumns = []
        datetimeColumns = []
        for column in columns:
            datatype = trainX[column].dtype
            if column in indexColumns or column in skipColumns:
                continue
            elif datatype == 'int64' or datatype == 'float64':
                numberColumns.append(column)
            elif datatype == 'object':
                categoryColumns.append(column)
            else:
                datetimeColumns.append(column)
                numberColumns.append(column)
        return numberColumns, categoryColumns, datetimeColumns
