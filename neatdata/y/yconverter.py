import numpy as np
from neatdata.numpyhelper.numpyhelper import *

class YConverter:

    def __init__(self):
        self._trainYMappingsStrToNum, self._trainYMappingsNumToStr = {'NotFound': -99}, {-99: 'NotFound'}
        self._setMappingsAsStringType = None

    def setYMappings(self, y):
        self._setMappingsAsStringType = True if isStringType(y) else False
        if not self._setMappingsAsStringType:
            return
        i = 0
        for value in np.unique(y):
            if value != None and value.strip() != "":
                self._trainYMappingsStrToNum[value] = i
                self._trainYMappingsNumToStr[i] = value
                i = i + 1

    def convertToNumber(self, y):
        if self._setMappingsAsStringType:
            pass

    def convertToString(self, y):
        if self._setMappingsAsStringType:
            pass



def getYAsNumber(self, y):
    output = None
    y = self.castAsNumpy(y)
    if self._setMappingsAsStringType:
        for i in newDataY.index:
            if newDataY[i] == None or np.isnan(newDataY[i]) or newDataY[i] not in self._trainYMappingsStrToNum.keys():
                newDataY[i] = 'NotFound'
        return np.vectorize(self._trainYMappingsStrToNum.get)(y)
    else:
        y[y == np.inf] = -99
        y[y == -np.inf] = -99
        for i in y.index:
            if np.isnan(y[i]) or y[i] not in self._trainYMappingsStrToNum.values():
                y[i] = -99
        return y



    if newDataYAsNumpy.dtype.kind in {'O', 'U', 'S'}: # a string
        for i in newDataY.index:
            if newDataY[i] == None or np.isnan(newDataY[i]) or newDataY[i] not in self.trainYMappingsStrToNum.keys():
                newDataY[i] = 'NotFound'
        newDataYAsNumpy = np.array( newDataY )
        output = np.vectorize(self.trainYMappingsStrToNum.get)(newDataYAsNumpy)

    else:
        newDataY[newDataY == np.inf] = -99
        newDataY[newDataY == -np.inf] = -99
        for i in newDataY.index:
            if np.isnan(newDataY[i]) or newDataY[i] not in self.trainYMappingsStrToNum.values():
                newDataY[i] = -99
        newDataYAsNumpy = np.array( newDataY )
        output = newDataYAsNumpy
    return output




def getYAsString(self, newDataY):
    output = None
    newDataYAsNumpy = np.array( newDataY )
    if newDataYAsNumpy.dtype.kind in {'O', 'U', 'S'}: # a string
        for i in newDataY.index:
            if newDataY[i] == None or np.isnan(newDataY[i]) or newDataY[i] not in self.trainYMappingsNumToStr.values():
                newDataY[i] = 'NotFound'
        newDataYAsNumpy = np.array( newDataY )
        output = newDataYAsNumpy

    else:
        newDataY[newDataY == np.inf] = -99
        newDataY[newDataY == -np.inf] = -99
        for i in newDataY.index:
            if np.isnan(newDataY[i]) or newDataY[i] not in self.trainYMappingsNumToStr.keys():
                newDataY[i] = -99
        newDataYAsNumpy = np.array( newDataY )
        output = np.vectorize(self.trainYMappingsNumToStr.get)(newDataYAsNumpy)
    return output
