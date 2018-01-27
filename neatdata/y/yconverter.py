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


#
# def getYAsString(self, newDataY):
#     output = None
#     newDataYAsNumpy = np.array( newDataY )
#     if newDataYAsNumpy.dtype.kind in {'O', 'U', 'S'}: # a string
#         for i in newDataY.index:
#             if newDataY[i] == None or np.isnan(newDataY[i]) or newDataY[i] not in self.trainYMappingsNumToStr.values():
#                 newDataY[i] = 'NotFound'
#         newDataYAsNumpy = np.array( newDataY )
#         output = newDataYAsNumpy
#
#     else:
#         newDataY[newDataY == np.inf] = -99
#         newDataY[newDataY == -np.inf] = -99
#         for i in newDataY.index:
#             if np.isnan(newDataY[i]) or newDataY[i] not in self.trainYMappingsNumToStr.keys():
#                 newDataY[i] = -99
#         newDataYAsNumpy = np.array( newDataY )
#         output = np.vectorize(self.trainYMappingsNumToStr.get)(newDataYAsNumpy)
#     return output
#
# def getYAsNumber(self, newDataY):
#     output = None
#     newDataYAsNumpy = np.array( newDataY )
#     if newDataYAsNumpy.dtype.kind in {'O', 'U', 'S'}: # a string
#         for i in newDataY.index:
#             if newDataY[i] == None or np.isnan(newDataY[i]) or newDataY[i] not in self.trainYMappingsStrToNum.keys():
#                 newDataY[i] = 'NotFound'
#         newDataYAsNumpy = np.array( newDataY )
#         output = np.vectorize(self.trainYMappingsStrToNum.get)(newDataYAsNumpy)
#
#     else:
#         newDataY[newDataY == np.inf] = -99
#         newDataY[newDataY == -np.inf] = -99
#         for i in newDataY.index:
#             if np.isnan(newDataY[i]) or newDataY[i] not in self.trainYMappingsStrToNum.values():
#                 newDataY[i] = -99
#         newDataYAsNumpy = np.array( newDataY )
#         output = newDataYAsNumpy
#     return output
