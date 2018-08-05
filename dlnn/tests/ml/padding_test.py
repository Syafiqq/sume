import numpy
from keras import backend as K

from dlnn.tests.ml.testcase import TestCase


class PaddingTest(TestCase):
    data = numpy.array([[
        [[0.1, 0.2, 0.3, 0.4],
         [0.1, 0.2, 0.3, 0.4],
         [0.1, 0.2, 0.3, 0.4],
         [0.1, 0.2, 0.3, 0.4]]
    ], [
        [[0.5, 0.6, 0.7, 0.8],
         [0.5, 0.6, 0.7, 0.8],
         [0.5, 0.6, 0.7, 0.8],
         [0.5, 0.6, 0.7, 0.8]]
    ]])

    def test_it_generate_Tensor(self):
        self.assertIsNotNone(self.data)
        tensor = K.variable(self.data)
        self.assertIsNotNone(tensor)
        # print(K.eval(tensor))

    def test_padding(self):
        import tensorflow as tf
        tensor = K.variable(self.data)
        ntensor = tf.pad(
            tensor=tensor,
            paddings=((1, 1), (1, 1), (1, 1), (1, 1))
        )
        self.assertIsNotNone(ntensor)
        # print(K.eval(ntensor))
        # print(ntensor.shape)

    def test_pad_util(self):
        from dlnn.util import Pad as PadUtil
        tensor = K.variable(self.data[0][0])
        ntensor = PadUtil.pad_center(tensor, 1)
        self.assertIsNotNone(ntensor)
        # print(K.eval(ntensor))
        # print(ntensor.shape)

    def test_repos_normalized_padding(self):
        from dlnn.util import Pad as PadUtil
        from dlnn.tests.ml.repos_helper import normalized
        import tensorflow as tf
        tensor = K.variable(normalized[0][0])
        ntensor = PadUtil.pad_center(tensor, 1)
        correction = tf.pad(
            tensor=normalized[0][0],
            paddings=((1, 1), (1, 1)),
        )
        self.assertTrue(numpy.allclose(K.eval(ntensor), K.eval(correction), rtol=1e-6))
        # print(K.eval(ntensor))
        # print(ntensor.shape)
