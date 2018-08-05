import os
from unittest import TestCase

import numpy
import numpy.matlib
import pandas

from sume.settings import BASE_DIR


class ReadCSVTest(TestCase):
    corpus_path = os.path.join(BASE_DIR, 'dlnn/resources/databank/datatrainClassify.csv')

    def test_read_csv(self):
        dataframe = pandas.read_csv(self.corpus_path, header=None)
        self.assertIsNotNone(dataframe)
        # print(dataframe)

    def test_get_num_data(self):
        dataframe = pandas.read_csv(self.corpus_path, header=None)
        dim = dataframe.shape
        self.assertEqual(8, dim[0])
        # print(dim)

    def test_get_feature_num_data(self):
        dataframe = pandas.read_csv(self.corpus_path, header=None)
        dim = dataframe.shape
        self.assertEqual(4, dim[1] - 1)
        # print(dim)

    def test_get_feature_data(self):
        dataframe = pandas.read_csv(self.corpus_path, header=None)
        dim = dataframe.shape
        features = dataframe.drop(columns=dim[1] - 1)
        self.assertEqual(4, features.shape[1])
        # print(features)

    def test_convert_feature_to_numpy_array(self):
        dataframe = pandas.read_csv(self.corpus_path, header=None)
        dim = dataframe.shape
        r_feature = dataframe.drop(columns=dim[1] - 1)
        feature = r_feature.values
        f_shape = numpy.shape(feature)
        self.assertEqual((8, 4), f_shape)
        # print(feature)

    def test_normalize_feature(self):
        dataframe = pandas.read_csv(self.corpus_path, header=None)
        dim = dataframe.shape
        r_feature = dataframe.drop(columns=dim[1] - 1)
        feature = r_feature.values.astype(float)
        feature *= 1 / 300.0
        self.assertTrue(numpy.allclose([.8433, .4367, .8633, .3167], feature[0], rtol=1e-3))
        # print(feature)

    def test_reshaping_feature(self):
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
        self.assertTrue(numpy.allclose(nfeature, oneliner, rtol=1e-3))
        # print(oneliner)

    def test_get_label_data(self):
        dataframe = pandas.read_csv(self.corpus_path, header=None)
        dim = dataframe.shape
        features = dataframe.drop(columns=numpy.arange(dim[1] - 1))
        self.assertEqual(1, features.shape[1])
        # print(features)
