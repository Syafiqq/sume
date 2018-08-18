from keras import backend as K

from dlnn.tests.ml.testcase import TestCase


def layer_5_pool(window_size):
    from keras.layers import MaxPooling2D
    return MaxPooling2D(pool_size=(window_size, window_size), padding='same', data_format='channels_first')


def layer_8_pool(window_size):
    from keras.layers import MaxPooling2D
    return MaxPooling2D(pool_size=(window_size, window_size), padding='same', data_format='channels_first')


class PoolingTest(TestCase):
    def test_pooling_w2_from_corr_step_4_seg_1(self):
        from dlnn.tests.ml.repos_helper import corr_step_4_seg_1
        from dlnn.tests.ml.repos_helper import corr_step_5_seg_1
        import numpy
        i = K.variable(numpy.concatenate(([[[corr_step_4_seg_1]]])))
        act = layer_5_pool(2)
        act.build(i.shape)
        x = act.call(i)
        self.assertIsNotNone(x)
        self.assertTrue(numpy.allclose(K.eval(x)[0][0], corr_step_5_seg_1, rtol=1e-6))
        # print(K.eval(x))

    def test_pooling_w2_from_corr_step_4_seg_2(self):
        from dlnn.tests.ml.repos_helper import corr_step_4_seg_2
        from dlnn.tests.ml.repos_helper import corr_step_5_seg_2
        import numpy
        i = K.variable(numpy.concatenate(([[[corr_step_4_seg_2]]])))
        act = layer_5_pool(2)
        act.build(i.shape)
        x = act.call(i)
        self.assertIsNotNone(x)
        self.assertTrue(numpy.allclose(K.eval(x)[0][0], corr_step_5_seg_2, rtol=1e-6))
        # print(K.eval(x))

    def test_pooling_w2_from_corr_step_4_seg_3(self):
        from dlnn.tests.ml.repos_helper import corr_step_4_seg_3
        from dlnn.tests.ml.repos_helper import corr_step_5_seg_3
        import numpy
        i = K.variable(numpy.concatenate(([[[corr_step_4_seg_3]]])))
        act = layer_5_pool(2)
        act.build(i.shape)
        x = act.call(i)
        self.assertIsNotNone(x)
        self.assertTrue(numpy.allclose(K.eval(x)[0][0], corr_step_5_seg_3, rtol=1e-6))
        # print(K.eval(x))

    def test_pooling_w2_from_corr_step_4(self):
        from dlnn.tests.ml.repos_helper import corr_step_4
        from dlnn.tests.ml.repos_helper import corr_step_5
        import numpy
        i = K.variable(corr_step_4)
        act = layer_5_pool(2)
        act.build(i.shape)
        x = act.call(i)
        self.assertIsNotNone(x)
        self.assertTrue(numpy.allclose(K.eval(x), corr_step_5, rtol=1e-6))
        # print(K.eval(x))

    def test_pooling_w1_from_corr_step_7_seg_1(self):
        from dlnn.tests.ml.repos_helper import corr_step_7_seg_1
        from dlnn.tests.ml.repos_helper import corr_step_8_seg_1
        import numpy
        i = K.variable(numpy.concatenate(([[[corr_step_7_seg_1]]])))
        act = layer_8_pool(1)
        act.build(i.shape)
        x = act.call(i)
        self.assertIsNotNone(x)
        self.assertTrue(numpy.allclose(K.eval(x)[0][0], corr_step_8_seg_1, rtol=1e-6))
        # print(K.eval(x))

    def test_pooling_w1_from_corr_step_7_seg_2(self):
        from dlnn.tests.ml.repos_helper import corr_step_7_seg_2
        from dlnn.tests.ml.repos_helper import corr_step_8_seg_2
        import numpy
        i = K.variable(numpy.concatenate(([[[corr_step_7_seg_2]]])))
        act = layer_8_pool(1)
        act.build(i.shape)
        x = act.call(i)
        self.assertIsNotNone(x)
        self.assertTrue(numpy.allclose(K.eval(x)[0][0], corr_step_8_seg_2, rtol=1e-6))
        # print(K.eval(x))

    def test_pooling_w1_from_corr_step_7_seg_3(self):
        from dlnn.tests.ml.repos_helper import corr_step_7_seg_3
        from dlnn.tests.ml.repos_helper import corr_step_8_seg_3
        import numpy
        i = K.variable(numpy.concatenate(([[[corr_step_7_seg_3]]])))
        act = layer_8_pool(1)
        act.build(i.shape)
        x = act.call(i)
        self.assertIsNotNone(x)
        self.assertTrue(numpy.allclose(K.eval(x)[0][0], corr_step_8_seg_3, rtol=1e-6))
        # print(K.eval(x))

    def test_pooling_w1_from_corr_step_7(self):
        from dlnn.tests.ml.repos_helper import corr_step_7
        from dlnn.tests.ml.repos_helper import corr_step_8
        import numpy
        i = K.variable(corr_step_7)
        act = layer_8_pool(1)
        act.build(i.shape)
        x = act.call(i)
        self.assertIsNotNone(x)
        self.assertTrue(numpy.allclose(K.eval(x), corr_step_8, rtol=1e-6))
        # print(K.eval(x))
