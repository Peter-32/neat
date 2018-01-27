import numpy as np

class YConverter:

    def __init__(self):
        self._trainYMappingsStrToNum, self._trainYMappingsNumToStr = {'NotFound': -99}, {-99: 'NotFound'}

    def setYMappings(self, y):
        i = 0
        for value in np.unique(y):
            if value != None and value.strip() != "":
                self._trainYMappingsStrToNum[value] = i
                self._trainYMappingsNumToStr[i] = value
                i = i + 1

    def convertToNumber(self, y):
        pass

    def convertToString(self, y):
        pass
