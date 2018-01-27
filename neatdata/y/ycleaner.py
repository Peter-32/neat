class YCleaner:

    def __init__(self):
        pass

    def execute(self, trainX, trainY):
        trainY = YConverter().execute(trainY)
        trainX, trainY = MissingYRowDropper().execute(trainX, trainY)
        trainX, trainY = YBalancer().execute(trainX, trainY)
        return trainX, trainY
