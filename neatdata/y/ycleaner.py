class YCleaner:

    def __init__(self):
        self.yConverter = None

    def cleanTrainingY(self, x, y):
        y = self._castAsString()
        self._initializeYConverter()
        trainX, trainY = self.cleanAnyY(trainX, trainY)
        trainX, trainY = YBalancer().execute(trainX, trainY)
        return trainX, trainY

    def _castAsString(self, y):
        return trainY.astype(str)

    def _initializeYConverter(self, y):
        self.yConverter = YConverter()
        self.yConverter.setYMappings(y)

    # def _isStringType(self, y):
    #     return False if y.dtype.kind in {'O', 'U', 'S'} else True

    def cleanAnyY(self, x, y):
        trainX, trainY = MissingYRowDropper().execute(trainX, trainY)
        return trainX, trainY

    def convertToNumber(self, y):
        return self.yConverter.convertToNumber(y)

    def convertToString(self, y):
        return self.yConverter.convertToString(y)
