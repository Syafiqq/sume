import numpy
from keras import backend as K
from keras.initializers import Initializer
from scipy import stats


class Unifinv(Initializer):

    def __init__(self, minval=-0.05, maxval=0.05):
        self.minval = minval
        self.maxval = maxval

    def __call__(self, shape, dtype=None):
        return K.variable(
            stats.uniform.ppf(numpy.random.rand(*shape), loc=self.minval, scale=self.maxval - self.minval), dtype=dtype)

    def get_config(self):
        return {
            'minval': self.minval,
            'maxval': self.maxval,
        }
