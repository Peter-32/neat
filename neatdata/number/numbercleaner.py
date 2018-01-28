class NumberCleaner:

    def __init__():
        self.trainX, self.numberColumns = None, None
        self.numberMetadata = None

    def train(self, trainX, numberColumns):
        self.trainX, self.numberColumns = trainX, numberColumns
        self.numberMetadata = NumberMetadata()
        self.numberMetadata.train(trainX, self.numberColumns)
        return clean(trainX)

    def clean(self, x):
        x = NumberValueAssigner().execute(x, self.numberColumns, self.numberMetadata)
        return x
