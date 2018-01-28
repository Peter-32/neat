class TestDataset:

    def __init__(self):
        self.x, self.columnsDropped, self.finalColumnNames = None, None, None

    def execute(self, x, columnsDropped, finalColumnNames):
        self.x, self.columnsDropped, self.finalColumnNames = x, columnsDropped, finalColumnNames
        self._newDataDropDroppedColumns()
        self._newDataAddMissingFinalColumnNames()
        self._newDataDropExtraColumnNames()
        return x

    def _newDataDropDroppedColumns(self):
        self.x = self.x.drop(self.columnsDropped, axis=1)

    def _newDataAddMissingFinalColumnNames(self):
        # Assuming only category columns will be missing
        for column in self.finalColumnNames:
            if column not in list(self.x):
                self.x[column] = np.zeros((len(self.x.index),1))

    def _newDataDropExtraColumnNames(self): # This hopefully does nothing - using it anyway
        columnsToDrop = []
        for column in list(self.x):
            if column not in self.finalColumnNames:
                columnsToDrop.append(column)
        self.x = self.x.drop(columnsToDrop, axis=1)
