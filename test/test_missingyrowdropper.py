import unittest
from neatdata.y.missingyrowdropper import *

class TestMissingYRowDropper(unittest.TestCase):

    def testMissingYRowDropper_Execute(self):
        # Assemble
        now = pd.datetime.now()
        trainX = pd.DataFrame({'col1': [1,1,1,1,1,1,1],
                               'col2': ['a','a','a','a','a','a','a'],
                               'col3': [now,now,now,now,now,now,now]})
        trainY = ['a','b','c',None,'b', None, None]
        # Act
        cleanTrainX, cleanTrainY = MissingYRowDropper().execute(trainX, trainY)
        # Assert
        self.assertEqual(len(trainY), 4)
        self.assertEqual(len(trainX.index), 4)
