import unittest
import pandas as pd
import numpy as np
from neatdata.columnmetadata.columndatatypegetter import *

class TestColumnDataTypeGetter(unittest.TestCase):

    def testColumnDataTypeGetter_Execute(self):
        # Assemble
        now = pd.datetime.now()
        trainX = pd.DataFrame({'col1': [1,1,1,1,1,1,1],
                               'col2': ['a','a','a','b','a','b','b'],
                               'col3': ['a','a','a','b','a','b','b'],
                               'col4': ['a','a','a','b','a','b','b'],
                               'col5': ['a','a','a','b','a','b','b'],
                               'col6': [now,now,now,now,now,now,now],
                               'col7': [1,None,None,None,None,None,None],
                               'col8': ['a',None,None,None,None,None,None],
                               'col9': [now,None,None,None,None,None,None],
                               'col10': [np.nan,None,None,None,None,None,None],
                               'col11': [np.inf,None,None,None,None,None,None],
                               'col12': [-np.inf,1,None,None,None,None,None]})
        indexColumns = ['col3','col4']
        skipColumns = ['col5']
        # Act
        numberColumns, categoryColumns, datetimeColumns = ColumnDataTypeGetter().execute(trainX, indexColumns, skipColumns)
        # Assert
        self.assertTrue('col1' in numberColumns)
        self.assertTrue('col2' in categoryColumns)
        self.assertTrue('col3' not in numberColumns)
        self.assertTrue('col3' not in categoryColumns)
        self.assertTrue('col3' not in datetimeColumns)
        self.assertTrue('col4' not in numberColumns)
        self.assertTrue('col4' not in categoryColumns)
        self.assertTrue('col4' not in datetimeColumns)
        self.assertTrue('col5' not in numberColumns)
        self.assertTrue('col5' not in categoryColumns)
        self.assertTrue('col5' not in datetimeColumns)
        self.assertTrue('col6' in datetimeColumns)
        self.assertTrue('col7' in numberColumns)
        self.assertTrue('col8' in categoryColumns)
        self.assertTrue('col9' in datetimeColumns)
        self.assertTrue('col10' in numberColumns)
        self.assertTrue('col11' in numberColumns)
        self.assertTrue('col12' in numberColumns)
