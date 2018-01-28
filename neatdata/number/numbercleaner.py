from neatdata.number.numbermetadata import *
from neatdata.number.numbervalueassigner import *

class NumberCleaner:

    def __init__(self):
        self.trainX, self.numberColumns = None, None
        self.numberMetadata = None

    def cleanAndLearn(self, trainX, numberColumns):
        self.trainX, self.numberColumns = trainX, numberColumns
        self.numberMetadata = NumberMetadata()
        self.numberMetadata.train(trainX, self.numberColumns)
        return self.clean(trainX)

    def clean(self, x):
        x = NumberValueAssigner().execute(x, self.numberColumns, self.numberMetadata)
        return x
