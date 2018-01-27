import pandas as pd

class MissingYRowDropper:

    def __init__(self):
        pass

    def execute(self, trainX, trainY):
        rowsToDrop = []
        trainX['__trainY__'] = trainY
        for i, row in trainX.iterrows():
            rowsToDrop.append(i) if row['__trainY__'] == 'nan' or row['__trainY__'] == None else None
        trainX = trainX.drop(trainX.index[rowsToDrop])
        trainY = trainX['__trainY__'].values
        trainX = trainX.drop(['__trainY__'], 1)
        return trainX, trainY
