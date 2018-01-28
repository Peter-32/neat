class CategoryDropColumns:

    def __init__():
        self.trainX, self.categoryColumns = None, None
        self.categoryMetadata = None

    def execute():
        _dropCategoryColumnsWithAllMissingValues()

    def _dropCategoryColumnsWithAllMissingValues(self, trainX):
        columnsToRemove = []
        for column in self.categoryColumns:
            if len(self.uniqueCategoryValues[column]) == 1 and self.uniqueCategoryValues[column][0] == '_Other':
                columnsToRemove.append(column)
                self.categoryColumns.remove(column)
                self.columnsDropped.append(column)
        self.df = self.df.drop(columnsToRemove, 1)
