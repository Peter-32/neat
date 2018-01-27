import unittest
from neatdata.y.yconverter import *

class TestYConverter(unittest.TestCase):

    def testYConverter_SetYMappings(self):
        # Assemble
        now = pd.datetime.now()
        trainX = pd.DataFrame({'col1': [1,1,1,1,1,1,1],
                               'col2': ['a','a','a','a','a','a','a'],
                               'col3': [now,now,now,now,now,now,now]})
        trainY = [1, 1, 1, 1, 2, 3, 4, 2]
        # Act
        cleanTrainX, cleanTrainY = YConverter().setYMappings(trainY)
        # Assert
        self.assertEqual(4, 4)
