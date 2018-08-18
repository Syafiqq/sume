import os

import numpy
import numpy.matlib
from keras import backend as K

from dlnn.tests.ml.testcase import TestCase
from sume.settings import BASE_DIR


def layer_1_conv():
    from dlnn.layer.Conv2D import Conv2D
    from dlnn.layer.Conv2D import AvgFilter
    from dlnn.layer.Conv2D import MaxFilter
    from dlnn.layer.Conv2D import StdDevFilter
    return Conv2D(
        name='step_1',
        filters=[AvgFilter(), MaxFilter(), StdDevFilter()],
        window=3,
        padding='same',
        use_bias=False,
        kernel_size=(4, 4),
        data_format='channels_first',
        input_shape=(1, 4, 4))


def layer_3_conv():
    from dlnn.layer.Conv2D import Conv2D
    from dlnn.layer.Conv2D import AvgFilter
    from dlnn.layer.Conv2D import MaxFilter
    from dlnn.layer.Conv2D import StdDevFilter
    return Conv2D(
        name='step_3',
        filters=[AvgFilter(), MaxFilter(), StdDevFilter()],
        window=3,
        padding='same',
        use_bias=False,
        kernel_size=(4, 4),
        data_format='channels_first',
        input_shape=(3, 4, 4))


def layer_6_conv():
    from dlnn.layer.Conv2D import Conv2D
    from dlnn.layer.Conv2D import AvgFilter
    from dlnn.layer.Conv2D import MaxFilter
    from dlnn.layer.Conv2D import StdDevFilter
    return Conv2D(
        name='step_6',
        filters=[AvgFilter(), MaxFilter(), StdDevFilter()],
        window=3,
        padding='same',
        use_bias=False,
        kernel_size=(2, 2),
        data_format='channels_first',
        input_shape=(3, 2, 2))


class ConvTest(TestCase):
    corpus_path = os.path.join(BASE_DIR, 'dlnn/resources/databank/datatrainClassify.csv')

    def corpus(self):
        import pandas
        dataframe = pandas.read_csv(self.corpus_path, header=None)
        dim = dataframe.shape
        r_feature = dataframe.drop(columns=dim[1] - 1)
        feature = r_feature.values.astype(float)
        feature_dim = numpy.shape(feature)
        feature *= 1 / 300.0
        nfeature = numpy.delete(numpy.empty([1, feature_dim[1], feature_dim[1]]), 0, 0)
        for _k, _v in enumerate(feature):
            nfeature = numpy.concatenate((nfeature, [numpy.matlib.repmat(_v, feature_dim[1], 1)]))
        oneliner = numpy.tile(numpy.reshape(feature, (feature_dim[0], 1, feature_dim[1])), (1, feature_dim[1], 1))
        self.assertTrue(numpy.allclose(nfeature, oneliner, rtol=1e-6))
        return oneliner

    def test_step_1(self):
        from dlnn.tests.ml.repos_helper import normalized
        from dlnn.tests.ml.repos_helper import corr_step_1
        i = K.variable(normalized)
        conv = layer_1_conv()
        conv.build(i.shape)
        result = conv.call(i)
        self.assertIsNotNone(result)
        self.assertTrue(numpy.allclose(K.eval(result)[0], corr_step_1, rtol=1e-6))
        # print(K.eval(result))

    def test_step_3(self):
        from dlnn.tests.ml.repos_helper import corr_step_2
        from dlnn.tests.ml.repos_helper import corr_step_3
        i = K.variable(corr_step_2)
        conv = layer_3_conv()
        conv.build(i.shape)
        result = conv.call(i)
        self.assertIsNotNone(result)
        self.assertTrue(numpy.allclose(K.eval(result), corr_step_3, rtol=1e-6))
        # print(K.eval(result))

    def test_step_6(self):
        from dlnn.tests.ml.repos_helper import corr_step_5
        from dlnn.tests.ml.repos_helper import corr_step_6
        i = K.variable(corr_step_5)
        conv = layer_6_conv()
        conv.build(i.shape)
        result = conv.call(i)
        self.assertIsNotNone(result)
        self.assertTrue(numpy.allclose(K.eval(result), corr_step_6, rtol=1e-6))
        # print(K.eval(result))
