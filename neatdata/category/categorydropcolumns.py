class CategoryDropColumns:

    def __init__(self):
        self.trainX, self.categoryColumns, self.columnsDropped = None, None, None

    def execute(self, trainX, categoryColumns, columnsDropped):
        self.trainX, self.categoryColumns, self.columnsDropped = trainX, categoryColumns, columnsDropped
        return self._dropCategoryColumnsWithAllMissingValues()

    def _dropCategoryColumnsWithAllMissingValues(self):
        columnsToRemove = []
        for column in self.categoryColumns:
            uniqueValues = self.trainX[column].unique()
            if len(uniqueValues) == 1 and uniqueValues[0] == None:
                columnsToRemove.append(column)
                self.categoryColumns.remove(column)
        self.columnsDropped.append(columnsToRemove)
        return self.trainX.drop(columnsToRemove, 1)
