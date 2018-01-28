class Indexer:

    def __init__(self):
        self.x, self.trainY, self.indexColumns = None, None, None

    def execute(self, x, trainY, indexColumns):
        self.x, self.trainY, self.indexColumns = x, trainY, indexColumns
        self._dropDuplicatesAndMissingRowsIfIndexIsSpecified()
        self._addIndex()
        return x


    def _dropDuplicatesAndMissingRowsIfIndexIsSpecified(self):
        rowsToDrop = []
        if self.indexColumns != []:
            self.x['__trainY__'] = self.trainY
            self.x = self.x.drop_duplicates(subset=self.indexColumns)

            for i, row in self.x.iterrows():
                for column in self.indexColumns:
                    if ((self.x[column].dtype == 'int64' or self.x[column].dtype == 'float64') and (np.isnan(row[column]) or np.isinf(row[column]))) or row[column] == None:
                        rowsToDrop.append(i)
            self.x = self.x.drop(self.x.index[rowsToDrop])
            self.trainY = self.x['__trainY__'].values
            self.x = self.x.drop(['__trainY__'], 1)

    def _addIndex(self):
        indexColumns = []
        self.x['_id'] = np.arange(1,len(self.x.index)+1)
        if self.indexColumns != []:
            indexColumns = list(self.indexColumns)
        indexColumns.append('_id')
        self.x = self.x.set_index(indexColumns)
