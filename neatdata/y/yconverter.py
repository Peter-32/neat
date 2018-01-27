import numpy as np

class YConverter:

    def __init__(self):
        self._trainYMappingsStrToNum, self._trainYMappingsNumToStr = None, None

    def setYMappings(self, y):
        i = 0
        for value in np.unique(y):
            if value != None and value.strip() != "":
                self.trainYMappingsStrToNum[value] = i
                self.trainYMappingsNumToStr[i] = value
                i = i + 1
        self._trainYMappingsNumToStr = None
        self._trainYMappingsStrToNum = None
        return

    def convertToNumber(self, y):
        pass

    def convertToString(self, y):
        pass
