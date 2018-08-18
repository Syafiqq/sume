import numpy

from dlnn.tests.ml.testcase import TestCase


class FilterTest(TestCase):
    data = numpy.array(
        [
            [
                [[0.1, 0.2, 0.3, 0.4],
                 [0.1, 0.2, 0.3, 0.4],
                 [0.1, 0.2, 0.3, 0.4],
                 [0.1, 0.2, 0.3, 0.4]]
            ],
            [
                [[0.5, 0.6, 0.7, 0.8],
                 [0.5, 0.6, 0.7, 0.8],
                 [0.5, 0.6, 0.7, 0.8],
                 [0.5, 0.6, 0.7, 0.8]]
            ]
        ])

    def test_avg_filter(self):
        from keras import backend as K
        from dlnn.layer.Conv2D import AvgFilter
        tensor = K.variable(self.data[0][0])
        fltr = AvgFilter()
        ntensor = fltr.filter(tensor, 3)
        self.assertIsNotNone(ntensor)
        # print(K.eval(ntensor))
        # print(ntensor.shape)

    def test_max_filter(self):
        from keras import backend as K
        from dlnn.layer.Conv2D import MaxFilter
        tensor = K.variable(self.data[0][0])
        fltr = MaxFilter()
        ntensor = fltr.filter(tensor, 3)
        self.assertIsNotNone(ntensor)
        # print(K.eval(ntensor))
        # print(ntensor.shape)

    def test_stddev_filter(self):
        from keras import backend as K
        from dlnn.layer.Conv2D import StdDevFilter
        tensor = K.variable(self.data[0][0])
        fltr = StdDevFilter()
        ntensor = fltr.filter(tensor, 3)
        self.assertIsNotNone(ntensor)
        # print(K.eval(ntensor))
        # print(ntensor.shape)

    def test_repos_normalized_avg_filter_from_normalized(self):
        from keras import backend as K
        from dlnn.layer.Conv2D import AvgFilter
        from dlnn.tests.ml.repos_helper import normalized
        from dlnn.tests.ml.repos_helper import corr_step_1_seg_1
        tensor = K.variable(normalized[0][0])
        fltr = AvgFilter()
        ntensor = fltr.filter(tensor, 3)
        self.assertIsNotNone(ntensor)
        self.assertTrue(numpy.allclose(K.eval(ntensor), corr_step_1_seg_1, rtol=1e-6))
        # print(K.eval(ntensor))
        # print(ntensor.shape)

    def test_repos_max_avg_filter_from_normalized(self):
        from keras import backend as K
        from dlnn.layer.Conv2D import MaxFilter
        from dlnn.tests.ml.repos_helper import normalized
        from dlnn.tests.ml.repos_helper import corr_step_1_seg_2
        tensor = K.variable(normalized[0][0])
        fltr = MaxFilter()
        ntensor = fltr.filter(tensor, 3)
        self.assertIsNotNone(ntensor)
        self.assertTrue(numpy.allclose(K.eval(ntensor), corr_step_1_seg_2, rtol=1e-6))
        # print(K.eval(ntensor))
        # print(ntensor.shape)

    def test_repos_max_std_filter_from_normalized(self):
        from keras import backend as K
        from dlnn.layer.Conv2D import StdDevFilter
        from dlnn.tests.ml.repos_helper import normalized
        from dlnn.tests.ml.repos_helper import corr_step_1_seg_3
        tensor = K.variable(normalized[0][0])
        fltr = StdDevFilter()
        ntensor = fltr.filter(tensor, 3)
        self.assertIsNotNone(ntensor)
        self.assertTrue(numpy.allclose(K.eval(ntensor), corr_step_1_seg_3, rtol=1e-6))
        # print(K.eval(ntensor))
        # print(ntensor.shape)

    def test_repos_normalized_avg_filter_from_corr_step_2(self):
        from keras import backend as K
        from dlnn.layer.Conv2D import AvgFilter
        from dlnn.tests.ml.repos_helper import corr_step_2_seg_1
        from dlnn.tests.ml.repos_helper import corr_step_3_seg_1
        tensor = K.variable(corr_step_2_seg_1)
        fltr = AvgFilter()
        ntensor = fltr.filter(tensor, 3)
        self.assertIsNotNone(ntensor)
        self.assertTrue(numpy.allclose(K.eval(ntensor), corr_step_3_seg_1, rtol=1e-6))
        # print(K.eval(ntensor))
        # print(ntensor.shape)

    def test_repos_normalized_max_filter_from_corr_step_2(self):
        from keras import backend as K
        from dlnn.layer.Conv2D import MaxFilter
        from dlnn.tests.ml.repos_helper import corr_step_2_seg_2
        from dlnn.tests.ml.repos_helper import corr_step_3_seg_2
        tensor = K.variable(corr_step_2_seg_2)
        fltr = MaxFilter()
        ntensor = fltr.filter(tensor, 3)
        self.assertIsNotNone(ntensor)
        self.assertTrue(numpy.allclose(K.eval(ntensor), corr_step_3_seg_2, rtol=1e-6))
        # print(K.eval(ntensor))
        # print(ntensor.shape)

    def test_repos_normalized_std_filter_from_corr_step_2(self):
        from keras import backend as K
        from dlnn.layer.Conv2D import StdDevFilter
        from dlnn.tests.ml.repos_helper import corr_step_2_seg_3
        from dlnn.tests.ml.repos_helper import corr_step_3_seg_3
        tensor = K.variable(corr_step_2_seg_3)
        fltr = StdDevFilter()
        ntensor = fltr.filter(tensor, 3)
        self.assertIsNotNone(ntensor)
        self.assertTrue(numpy.allclose(K.eval(ntensor), corr_step_3_seg_3, rtol=1e-6))
        # print(K.eval(ntensor))
        # print(ntensor.shape)

    def test_repos_normalized_avg_filter_from_corr_step_5(self):
        from keras import backend as K
        from dlnn.layer.Conv2D import AvgFilter
        from dlnn.tests.ml.repos_helper import corr_step_5_seg_1
        from dlnn.tests.ml.repos_helper import corr_step_6_seg_1
        tensor = K.variable(corr_step_5_seg_1)
        fltr = AvgFilter()
        ntensor = fltr.filter(tensor, 3)
        self.assertIsNotNone(ntensor)
        self.assertTrue(numpy.allclose(K.eval(ntensor), corr_step_6_seg_1, rtol=1e-6))
        # print(K.eval(ntensor))
        # print(ntensor.shape)

    def test_repos_normalized_max_filter_from_corr_step_5(self):
        from keras import backend as K
        from dlnn.layer.Conv2D import MaxFilter
        from dlnn.tests.ml.repos_helper import corr_step_5_seg_2
        from dlnn.tests.ml.repos_helper import corr_step_6_seg_2
        tensor = K.variable(corr_step_5_seg_2)
        fltr = MaxFilter()
        ntensor = fltr.filter(tensor, 3)
        self.assertIsNotNone(ntensor)
        self.assertTrue(numpy.allclose(K.eval(ntensor), corr_step_6_seg_2, rtol=1e-6))
        # print(K.eval(ntensor))
        # print(ntensor.shape)

    def test_repos_normalized_std_filter_from_corr_step_5(self):
        from keras import backend as K
        from dlnn.layer.Conv2D import StdDevFilter
        from dlnn.tests.ml.repos_helper import corr_step_5_seg_3
        from dlnn.tests.ml.repos_helper import corr_step_6_seg_3
        tensor = K.variable(corr_step_5_seg_3)
        fltr = StdDevFilter()
        ntensor = fltr.filter(tensor, 3)
        self.assertIsNotNone(ntensor)
        self.assertTrue(numpy.allclose(K.eval(ntensor), corr_step_6_seg_3, rtol=1e-6))
        # print(K.eval(ntensor))
        # print(ntensor.shape)
