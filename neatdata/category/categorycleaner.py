class CategoryCleaner:

    def __init__():
        self.trainX, self.categoryColumns = None, None
        self.categoryMetadata = None

    def train(self, trainX, categoryColumns):
        self.trainX, self.categoryColumns = trainX, categoryColumns
        self.categoryMetadata = CategoryMetadata()
        self.categoryMetadata.train(trainX, self.categoryColumns)
        self.categoryDropColumns = CategoryDropColumns()
        trainX = self.categoryDropColumns.execute(trainX, self.categoryColumns)
        return clean(trainX)

    def clean(self, x):
        x = categoryValueAssigner().execute(x, self.categoryColumns, self.categoryMetadata)
        return x
