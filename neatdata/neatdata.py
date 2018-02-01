import pandas as pd
import numpy as np
from sklearn import preprocessing
from sklearn.utils import resample
from math import ceil
from copy import deepcopy

class NeatData:

    def __init__(self):
        self.indexer = None # TODO: Unsure
        self.numberColumns, self.categoryColumns, self.datetimeColumns = None, None, None
        self.indexColumns, self.iWillManuallyCleanColumns = None, None
        self.columnsDropped = []
        self.finalColumnNames = None
        self.yCleaner = None

    def cleanTrainingDataset(self, trainX, trainY, indexColumns=[], iWillManuallyCleanColumns=[]):
        self.indexColumns, self.iWillManuallyCleanColumns = indexColumns, iWillManuallyCleanColumns
        trainX, trainY = self._initial(trainX, trainY)
        trainX, trainY = self._datatypeSpecific(trainX, trainY)
        trainX, trainY = self._final(trainX, trainY)
        return trainX, trainY

    def _initial(self, trainX, trainY):
        self._validateTrainingInput(trainX, trainY)
        self.yCleaner = YCleaner()
        trainX, trainY = self.yCleaner.cleanTrainingY(trainX, trainY)
        trainX, self.indexColumns, self.iWillManuallyCleanColumns = ColumnNameCleaner().execute(trainX, self.indexColumns, self.iWillManuallyCleanColumns)
        self.numberColumns, self.categoryColumns, self.datetimeColumns = ColumnDataTypeGetter().execute(trainX, self.indexColumns, self.iWillManuallyCleanColumns)
        return trainX, trainY

    def _validateTrainingInput(self, trainX, trainY):
        if len(trainY) != len(trainX.index): raise Exception('Error: trainX and trainY are differing lengths.')

    def _datatypeSpecific(self, trainX, trainY):
        self.datetimeCleaner = DatetimeCleaner()
        trainX = self.datetimeCleaner.clean(trainX, deepcopy(self.datetimeColumns))
        self.numberCleaner = NumberCleaner()
        trainX = self.numberCleaner.cleanAndLearn(trainX, deepcopy(self.numberColumns))
        self.categoryCleaner = CategoryCleaner()
        trainX = self.categoryCleaner.cleanAndLearn(trainX, self.categoryColumns, self.columnsDropped) # Rare mutates to both arrays
        return trainX, trainY

    def _final(self, trainX, trainY):
        self.indexer = Indexer() #TODO: delete this comment.  All indexing should be last in this iteration.
        self.indexer.execute(trainX, trainY, deepcopy(self.indexColumns))
        self.finalColumnNames = list(trainX)
        return trainX, trainY

    def cleanTestDataset(self, testX):
        self._validateCleanedTrainingDataset()
        return self._cleanTestDataset(testX)

    def _validateCleanedTrainingDataset(self):
        if self.finalColumnNames == None: raise Exception('Error: cleanTrainingDataset() must be run first.')

    def _cleanTestDataset(self, testX):
        ColumnNameCleaner().cleanColumnNamesOnDF(testX)
        testX = self.datetimeCleaner.clean(testX, deepcopy(self.datetimeColumns))
        testX = self.numberCleaner.clean(testX)
        testX = self.categoryCleaner.clean(testX)
        testX = self.indexer.addIndex(testX)
        testX = TestDataset().execute(testX, self.columnsDropped, self.finalColumnNames)
        return testX

    def convertYToNumbersForModeling(self, testY):
        return self.yCleaner.convertYToNumbersForModeling(testY)

    def convertYToStringsOrNumbersForPresentation(self, testY):
        return self.yCleaner.convertYToStringsOrNumbersForPresentation(testY)

class YCleaner:

    def __init__(self):
        self.yConverter = None
        self.trained = False

    def cleanTrainingY(self, trainX, trainY):
        trainY = castAsNumpy(trainY)
        trainX, trainY = MissingYRowDropper().execute(trainX, trainY)
        self._initializeYConverter(trainY)
        trainX, trainY = YBalancer().execute(trainX, trainY)
        self.trained = True
        trainY = self.convertYToNumbersForModeling(trainY)
        return trainX, trainY

    def _initializeYConverter(self, trainY):
        self.yConverter = YConverter()
        self.yConverter.setYMappings(trainY)

    def convertYToNumbersForModeling(self, trainY):
        if not self.trained: raise Exception('Error: Use cleanTrainingY(x, y) before using convertToNumber(trainY).')
        return self.yConverter.convertYToNumbersForModeling(trainY)

    def convertYToStringsOrNumbersForPresentation(self, trainY):
        if not self.trained: raise Exception('Error: Use cleanTrainingY(x, y) before using convertToString(trainY).')
        return self.yConverter.convertYToStringsOrNumbersForPresentation(trainY)

class MissingYRowDropper:

    def __init__(self):
        self.rowsToDrop = None

    def execute(self, trainX, trainY):
        self.rowsToDrop = []
        trainX['__trainY__'] = trainY
        self._appendToRowsToDropForNoneValue(trainX)
        self._appendToRowsToDropForNumbers(trainX, trainY)
        self._appendToRowsToDropForStrings(trainX, trainY)
        trainX = trainX.drop(trainX.index[self.rowsToDrop])
        trainY = trainX['__trainY__'].values
        trainX = trainX.drop(['__trainY__'], 1)
        return trainX, trainY

    def _appendToRowsToDropForNoneValue(self, trainX):
        for i, row in trainX.iterrows():
            self.rowsToDrop.append(i) if row['__trainY__'] == None else None

    def _appendToRowsToDropForNumbers(self, trainX, trainY):
        if not isStringType(trainY):
            for i, row in trainX.iterrows():
                self.rowsToDrop.append(i) if np.isnan(row['__trainY__']) else None
                self.rowsToDrop.append(i) if row['__trainY__'] == np.inf else None
                self.rowsToDrop.append(i) if row['__trainY__'] == -np.inf else None

    def _appendToRowsToDropForStrings(self, trainX, trainY):
        if isStringType(trainY):
            for i, row in trainX.iterrows():
                if row['__trainY__'] != None:
                    self.rowsToDrop.append(i) if row['__trainY__'].strip() == "" else None

class YBalancer:

    def __init__(self):
        self.trainYFrequencies, self.trainYUpsamplesNeeded = None, None
        self.trainX, self.trainY = None, None
        self.uniqueValues = None

    def execute(self, trainX, trainY):
        self.trainX, self.trainY = trainX, castAsNumpy(trainY)
        self.uniqueValues = np.unique(trainY)
        self.trainYUpsamplesNeeded = {}
        self._saveTrainYFrequencies()
        self._saveTrainYUpsamplesNeeded()
        self._fixTrainYImbalance()
        return self.trainX, self.trainY

    def _saveTrainYFrequencies(self):
        self.trainYFrequencies = pd.value_counts(self.trainY, sort=True, normalize=False)

    def _saveTrainYUpsamplesNeeded(self):
        maxCount = self._findTheMaxCount()
        minCountAllowed = ceil(maxCount / 2)
        for value in self.uniqueValues:
            actualFrequency = self.trainYFrequencies[value]
            idealTrainYFrequency = minCountAllowed if actualFrequency < minCountAllowed else actualFrequency
            self.trainYUpsamplesNeeded[value] = idealTrainYFrequency - actualFrequency

    def _findTheMaxCount(self):
        maxCount = None
        for value in self.uniqueValues:
            frequency = self.trainYFrequencies[value]
            if maxCount == None or frequency > maxCount:
                maxCount = frequency
        return maxCount

    def _fixTrainYImbalance(self):
        self.trainX['__trainY__'] = self.trainY
        for value in self.uniqueValues:
            samplesToGet = self.trainYUpsamplesNeeded[value]
            if samplesToGet > 0:
                upsampleRows = resample(self.trainX[self.trainX['__trainY__']==value],
                                    replace=True,
                                    n_samples=samplesToGet,
                                    random_state=123)
                self.trainX = pd.concat([self.trainX, upsampleRows])
        self.trainY = self.trainX['__trainY__'].values
        self.trainX = self.trainX.drop(['__trainY__'], 1)

class YConverter:

    def __init__(self):
        self._trainYMappingsStrToNum, self._trainYMappingsNumToStr = None, None
        self._trainYListOfValidInputs = None
        self._stringWasPassedToMapping = None
        self._setYMappingsWasRun = False

    def setYMappings(self, y):
        self._trainYMappingsStrToNum, self._trainYMappingsNumToStr = {'NotFound': -99}, {-99: 'NotFound'}
        self._trainYListOfValidInputs = [-99]
        self._setYMappingsWasRun = True
        self._stringWasPassedToMapping = True if isStringType(y) else False
        if not self._stringWasPassedToMapping:
            y[y == np.inf] = -99
            y[y == -np.inf] = -99
            for value in np.unique(y):
                if value != None and not np.isnan(value):
                    self._trainYListOfValidInputs.append(value)
            return
        i = 0
        for value in np.unique(y):
            if value != None and value.strip() != "":
                self._trainYMappingsStrToNum[value] = i
                self._trainYMappingsNumToStr[i] = value
                i = i + 1

    def convertYToNumbersForModeling(self, y):
        y = castAsNumpy(y)
        yIsStringType = isStringType(y)
        self._raiseExceptionsForConvertYToNumbersForModeling(yIsStringType)
        if yIsStringType and self._stringWasPassedToMapping:
            return self._convertStringToNumber(y)
        elif not yIsStringType and self._stringWasPassedToMapping:
            return self._convertNumberToNumberWithMapping(y)
        elif not yIsStringType and not self._stringWasPassedToMapping:
            return self._convertNumberToNumberWithList(y)
        else:
            raise Exception('Error: Impossible event.')

    def _raiseExceptionsForConvertYToNumbersForModeling(self, yIsStringType):
        if not self._setYMappingsWasRun: raise Exception('Error: run setYMappings before convertToNumber')
        if not self._stringWasPassedToMapping and yIsStringType: raise Exception('Error: Y was not string during setYMappings, therefore Y must be a number.')

    def _convertStringToNumber(self, y):
        y = self._prepareStringForMapping(y)
        return np.vectorize(self._trainYMappingsStrToNum.get)(y)

    def _prepareStringForMapping(self, y):
        for i in range(len(y)):
            if y[i] == None or y[i] not in self._trainYMappingsStrToNum.keys():
                y[i] = 'NotFound'
        return y

    def _convertNumberToNumberWithMapping(self, y):
        return self._prepareNumberForMapping(y)

    def _prepareNumberForMapping(self, y):
        y[y == np.inf] = -99
        y[y == -np.inf] = -99
        for i in range(len(y)):
            if np.isnan(y[i]) or y[i] not in self._trainYMappingsStrToNum.values():
                y[i] = -99
        return y

    def _convertNumberToNumberWithList(self, y):
        y[y == np.inf] = -99
        y[y == -np.inf] = -99
        for i in range(len(y)):
            if np.isnan(y[i]) or y[i] not in self._trainYListOfValidInputs:
                y[i] = -99
        return y

    def convertYToStringsOrNumbersForPresentation(self, y):
        y = castAsNumpy(y)
        yIsStringType = isStringType(y)
        self._raiseExceptionsForConvertYToStringsOrNumbersForPresentation(yIsStringType)
        if yIsStringType and self._stringWasPassedToMapping:
            return self._convertStringToString(y)
        elif not yIsStringType and self._stringWasPassedToMapping:
            return self._convertNumberToString(y)
        elif not yIsStringType and not self._stringWasPassedToMapping:
            return y
        else:
            raise Exception('Error: Impossible event.')

    def _raiseExceptionsForConvertYToStringsOrNumbersForPresentation(self, yIsStringType):
        if not self._setYMappingsWasRun: raise Exception('Error: run setYMappings before convertToString')
        if not self._stringWasPassedToMapping and yIsStringType: raise Exception('Error: Y was not string during setYMappings, so converting from string to number is not possible..')

    def _convertStringToString(self, y):
        return self._prepareStringForMapping(y)

    def _convertNumberToString(self, y):
        y = self._prepareNumberForMapping(y)
        return np.vectorize(self._trainYMappingsNumToStr.get)(y)

class ColumnNameCleaner:

    def __init__(self):
        pass

    def execute(self, trainX, indexColumns, iWillManuallyCleanColumns):
        trainX = self.cleanColumnNamesOnDF(trainX)
        indexColumns = self._cleanArrayOfColumnNames(indexColumns)
        iWillManuallyCleanColumns = self._cleanArrayOfColumnNames(iWillManuallyCleanColumns)

        return trainX, indexColumns, iWillManuallyCleanColumns

    def cleanColumnNamesOnDF(self, trainX):
        trainX.columns = trainX.columns.str.strip().str.lower().str.replace(' ', '_')
        return trainX

    def _cleanArrayOfColumnNames(self, columns):
        if type(columns) == str:
            columns = [columns]
        arr = []
        for column in columns:
            arr.append(self._cleanColumnName(column))
        return arr

    def _cleanColumnName(self, string):
        return string.strip().lower().replace(' ', '_')

class ColumnDataTypeGetter:

    def __init__(self):
        pass

    def execute(self, trainX, indexColumns, iWillManuallyCleanColumns):
        numberColumns, categoryColumns, datetimeColumns, columns = [], [], [], trainX.columns.values.tolist()
        for column in columns:
            datatype = trainX[column].dtype
            if column in indexColumns or column in iWillManuallyCleanColumns: pass
            elif datatype == 'int64' or datatype == 'float64':
                numberColumns.append(column)
            elif datatype == 'object':
                categoryColumns.append(column)
            else:
                datetimeColumns.append(column)
                numberColumns.append(column) # Assuming dates always become numbers early when cleaning
        return numberColumns, categoryColumns, datetimeColumns

class DatetimeCleaner:

    def __init__(self):
        self.datetimeColumns = None
        self.x = None

    def clean(self, x, datetimeColumns):
        self.x, self.datetimeColumns = x, datetimeColumns
        self._convertDatetimeToNumber()
        return x

    def _convertDatetimeToNumber(self):
        for column in self.datetimeColumns:
            values = []
            for i, row in self.x.iterrows():
                values.append((pd.datetime.now() - row[column]).days)
            self.x[column] = values

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

class NumberMetadata:

    def __init__(self):
        self.medians, self.lowerBounds, self.upperBounds = None, None, None

    def train(self, trainX, numberColumns):
        trainX = self._ignoreInfinityForQuantiles(trainX)

        firstQuantiles = trainX.quantile(.25)
        thirdQuantiles = trainX.quantile(.75)

        self.medians = trainX.quantile(.50)
        self.lowerBounds = {}
        self.upperBounds = {}
        for column in numberColumns:
            self.lowerBounds[column] = self.medians[column] - 2*(self.medians[column] - firstQuantiles[column])
            self.upperBounds[column] = self.medians[column] + 2*(thirdQuantiles[column] - self.medians[column])

    def _ignoreInfinityForQuantiles(self, trainX):
        return trainX.replace([np.inf, -np.inf], np.nan)

class NumberValueAssigner:

    def __init__(self):
        self.x, self.numberColumns, self.numberMetadata = None, None, None

    def execute(self, x, numberColumns, numberMetadata):
        self.x, self.numberColumns, self.numberMetadata = x, numberColumns, numberMetadata
        self._fixMissingNumValuesAndInfinity()
        self._fixHighLeveragePoints()
        return self.x

    def _fixMissingNumValuesAndInfinity(self):
        self.x = self.x.fillna(self.numberMetadata.medians) # optionally: replace self.medians with 0
        self.x = self.x.replace([-np.inf], np.nan)
        self.x = self.x.fillna(self.numberMetadata.lowerBounds)
        self.x = self.x.replace([np.inf], np.nan)
        self.x = self.x.fillna(self.numberMetadata.upperBounds)

    def _fixHighLeveragePoints(self):
        for i, row in self.x.iterrows():
            for column in self.numberColumns:
                if row[column] > self.numberMetadata.upperBounds[column]:
                    self.x.at[i, column] = self.numberMetadata.upperBounds[column]
                if row[column] < self.numberMetadata.lowerBounds[column]:
                    self.x.at[i, column] = self.numberMetadata.lowerBounds[column]

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

class CategoryMetadata:

    def __init__(self):
        self.trainX, self.categoryColumns = None, None
        self.valuesThatDontMapTo_Other = None
        self.categoryFrequencies = None
        self.uniqueCategoryValues = None

    def train(self, trainX, categoryColumns):
        self.trainX, self.categoryColumns = trainX, categoryColumns
        self.valuesThatDontMapTo_Other, self.categoryFrequencies = {}, {}
        self.uniqueCategoryValues = {}
        self._saveUniqueCategoryValues()
        self._saveCategoryFrequenciesAndValuesThatDontMapTo_Other()

    def _saveUniqueCategoryValues(self):
        for column in self.categoryColumns:
            self.uniqueCategoryValues[column] = []
            for value in self.trainX[column].unique():
                if value == None or pd.isnull(value):
                    continue
                else:
                    self.uniqueCategoryValues[column].append(value)
            self.uniqueCategoryValues[column].append('_Other')

    def _saveCategoryFrequenciesAndValuesThatDontMapTo_Other(self):
        for column in self.categoryColumns:
            _otherFrequency = 0
            self.valuesThatDontMapTo_Other[column] = ['_Other']
            frequencyPercentage = pd.value_counts(self.trainX[column].values, sort=False, normalize=True)
            self.categoryFrequencies[column] = {}
            for value in self.uniqueCategoryValues[column]:
                if value == '_Other':
                    continue
                elif frequencyPercentage[value] < .05:
                    _otherFrequency = _otherFrequency + frequencyPercentage[value]
                else:
                    self.valuesThatDontMapTo_Other[column].append(value)
                    self.categoryFrequencies[column][value] = frequencyPercentage[value]
            self.categoryFrequencies[column]['_Other'] = _otherFrequency

class CategoryDropColumns:

    def __init__(self):
        self.trainX, self.categoryColumns, self.columnsDropped = None, None, None

    def execute(self, trainX, categoryColumns, columnsDropped):
        self.trainX, self.categoryColumns, self.columnsDropped = trainX, categoryColumns, columnsDropped
        return self._dropCategoryColumnsWithAllMissingValues()

    def _dropCategoryColumnsWithAllMissingValues(self):
        columnsToRemove = []
        for column in self.categoryColumns:
            uniqueValues = self.trainX[column].unique()
            if len(uniqueValues) == 1 and uniqueValues[0] == None:
                columnsToRemove.append(column)
                self.columnsDropped.append(column)
                self.categoryColumns.remove(column)
        return self.trainX.drop(columnsToRemove, 1)

class CategoryValueAssigner:

    def __init__(self):
        self.x, self.categoryColumns = None, None
        self.valuesThatDontMapTo_Other = None
        self.categoryFrequencies = None
        self.uniqueCategoryValues = None

    def execute(self, x, categoryColumns, categoryMetadata):
        self.x, self.categoryColumns = x, categoryColumns
        self.valuesThatDontMapTo_Other = categoryMetadata.valuesThatDontMapTo_Other
        self.categoryFrequencies = categoryMetadata.categoryFrequencies
        self.uniqueCategoryValues = categoryMetadata.uniqueCategoryValues
        self._fixMissingCategoryValuesAndMapValuesTo_Other()
        self._applyOneHotEncoding()
        return self.x

    def _fixMissingCategoryValuesAndMapValuesTo_Other(self):
        for i, row in self.x.iterrows():
            for column in self.categoryColumns:
                if row[column] == None:
                    self.x.at[i, column] = self._getRandomCategoryBasedOnFrequencies(column)
                elif row[column] not in self.valuesThatDontMapTo_Other[column]:
                    self.x.at[i, column] = '_Other'

    def _getRandomCategoryBasedOnFrequencies(self, column):
        chosenValue, prevValue, cumulativeProbability = None, None, 0
        randomNumber = np.random.uniform(0,1,1)[0]
        for value in self.uniqueCategoryValues[column]:
            if value in self.valuesThatDontMapTo_Other[column]:
                probabilityOfValue, prevValue = self.categoryFrequencies[column][value], value
                cumulativeProbability = cumulativeProbability + probabilityOfValue
                if cumulativeProbability > randomNumber:
                    chosenValue = value
                    break
        return prevValue if chosenValue == None else chosenValue

    def _applyOneHotEncoding(self): # don't drop_first => one hot encoding instead of dummy encoding
        for column in self.categoryColumns:
            self.x = pd.concat([self.x.drop(column, axis=1), pd.get_dummies(self.x[column], prefix=column+"_", drop_first=False)], axis=1)

class Indexer:

    def __init__(self):
        self.x, self.trainY, self.indexColumns = None, None, None

    def execute(self, x, trainY, indexColumns):
        self.x, self.trainY, self.indexColumns = x, trainY, indexColumns
        self._dropDuplicatesAndMissingRowsIfIndexIsSpecified()
        x = self.addIndex(self.x)
        return x

    def _dropDuplicatesAndMissingRowsIfIndexIsSpecified(self):
        rowsToDrop = []
        if self.indexColumns != []:
            self.x['__trainY__'] = self.trainY
            self.x = self.x.drop_duplicates(subset=self.indexColumns)

            for i, row in self.x.iterrows():
                for column in self.indexColumns:
                    if ((self.x[column].dtype == 'int64' or self.x[column].dtype == 'float64') and (np.isnan(row[column]) or np.isinf(row[column]))) or row[column] == None:
                        rowsToDrop.append(i)
            self.x = self.x.drop(self.x.index[rowsToDrop])
            self.trainY = self.x['__trainY__'].values
            self.x = self.x.drop(['__trainY__'], 1)

    def addIndex(self, x):
        indexColumns = []
        x['_id'] = np.arange(1,len(x.index)+1)
        if self.indexColumns != []:
            indexColumns = list(self.indexColumns)
        indexColumns.append('_id')
        x = x.set_index(indexColumns)
        return x

class TestDataset:

    def __init__(self):
        self.x, self.columnsDropped, self.finalColumnNames = None, None, None

    def execute(self, x, columnsDropped, finalColumnNames):
        self.x, self.columnsDropped, self.finalColumnNames = x, columnsDropped, finalColumnNames
        self._newDataDropDroppedColumns()
        self._newDataAddMissingFinalColumnNames()
        self._newDataDropExtraColumnNames()
        return self.x

    def _newDataDropDroppedColumns(self):
        self.x = self.x.drop(self.columnsDropped, axis=1)

    def _newDataAddMissingFinalColumnNames(self):
        # Assuming only category columns will be missing
        for column in self.finalColumnNames:
            if column not in list(self.x):
                self.x[column] = np.zeros((len(self.x.index),1))

    def _newDataDropExtraColumnNames(self): # This hopefully does nothing - using it anyway
        columnsToDrop = []
        for column in list(self.x):
            if column not in self.finalColumnNames:
                columnsToDrop.append(column)
        self.x = self.x.drop(columnsToDrop, axis=1)

def isStringType(y):
    y = castAsNumpy(y)
    return True if y.dtype.kind in {'O', 'U', 'S'} else False

def castAsNumpy(y):
    return np.array(y)
