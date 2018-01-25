import pandas as pd
import numpy as np
from sklearn import preprocessing
from sklearn.utils import resample
from math import ceil

class NeatData:

    def __init__(self, trainX, trainY, indexColumns=[], skipColumns=[]):
        InputValidator()
        targetCleaner = TargetCleaner(trainX, trainY)
        columnNameCleaner = ColumnNameCleaner()
        columnDataTyper = ColumnDataTyper()
        indexer = Indexer()
        targetConverter = TargetConverter()
        numberCleaner = NumberCleaner()
        numberMetadata = NumberMetadata()
        numberValueAssigner = NumberValueAssigner()
        datetimeCleaner = DatetimeCleaner()
        categoryCleaner = CategoryCleaner()
        categoryMetadata = CategoryMetadata()
        categoryValueAssigner = CategoryValueAssigner()
        newDataCleaner = NewDataCleaner()
