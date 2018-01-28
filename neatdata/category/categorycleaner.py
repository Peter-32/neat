from neatdata.category.categorydropcolumns import *
from neatdata.category.categorymetadata import *
from neatdata.category.categoryvalueassigner import *

class CategoryCleaner:

    def __init__(self):
        self.trainX, self.categoryColumns = None, None
        self.categoryMetadata = None

    def cleanAndLearn(self, trainX, categoryColumns, columnsDropped):
        self.trainX, self.categoryColumns = trainX, categoryColumns
        self.categoryMetadata = CategoryMetadata()
        self.categoryMetadata.train(trainX, self.categoryColumns)
        self.categoryDropColumns = CategoryDropColumns()
        self.trainX = self.categoryDropColumns.execute(self.trainX, self.categoryColumns, columnsDropped)     
        return self.clean(self.trainX)

    def clean(self, x):
        x = CategoryValueAssigner().execute(x, self.categoryColumns, self.categoryMetadata)
        return x
