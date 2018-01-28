class CategoryDropColumns:

    def __init__():
        self.trainX, self.categoryColumns = None, None

    def execute(self, trainX, categoryColumns):
        self.trainX, self.categoryColumns = trainX, categoryColumns
        self._dropCategoryColumnsWithAllMissingValues()

    def _dropCategoryColumnsWithAllMissingValues(self):
        columnsToRemove = []
        for column in self.categoryColumns:
            uniqueValues = self.trainX[column].unique()
            if len(uniqueValues) == 1 and uniqueValues[0] == None:
                columnsToRemove.append(column)
                self.categoryColumns.remove(column)
        return self.trainX.drop(columnsToRemove, 1)
