

class NumpyHelper:

    def __init__(self):
        pass

    def isStringType(self, y):
        return True if y.dtype.kind in {'O', 'U', 'S'} else False

    def castAsNumpy(self, y):
        return np.array(y)
