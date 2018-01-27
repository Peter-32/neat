import numpy as np

def isStringType(y):
    y = castAsNumpy(y)
    return True if y.dtype.kind in {'O', 'U', 'S'} else False

def castAsNumpy(y):
    return np.array(y)
