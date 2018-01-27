class NumberCleaner:

    def __init__():
        self.trainX, self.numberColumns = None, None

    def initialize(self, trainX, numberColumns):
        self.trainX, self.numberColumns = trainX, numberColumns

    def execute(self):
        trainX, trainY = NumberMetadata().execute(trainX, trainY)
        trainX, trainY = NumberValueAssigner().execute(trainX, trainY)
        return trainX, trainY
