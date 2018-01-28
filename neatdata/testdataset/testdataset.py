class TestDataset:

    def __init__(self):


    def execute(self):








    ########## New Data ##########

    def _newDataDropDroppedColumns(self):
        self.df = self.df.drop(self.columnsDropped, axis=1)

    def _newDataAddMissingFinalColumnNames(self):
        # Assuming only category columns will be missing
        for column in self.finalColumnNames:
            if column not in list(self.df):
                self.df[column] = np.zeros((len(self.df.index),1))

    def _newDataDropExtraColumnNames(self): # This hopefully does nothing - using it anyway
        columnsToDrop = []
        for column in list(self.df):
            if column not in self.finalColumnNames:
                columnsToDrop.append(column)
        self.df = self.df.drop(columnsToDrop, axis=1)
