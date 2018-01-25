class TargetCleaner:

    def __init__(self, trainX, trainY):
        missingTargetRowDropper = MissingTargetRowDropper(trainX, trainY)
        targetBalancer = TargetBalancer(trainX, trainY)
