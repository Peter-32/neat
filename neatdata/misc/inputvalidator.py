class InputValidator:

    def __init__(self, trainX, trainY):
        self._testDifferingLengths(trainX, trainY)

    def _testDifferingLengths(self, trainX, trainY):
        if len(trainY) != len(trainX.index):
            raise Exception('Error: trainX and trainY are differing lengths')
            return
