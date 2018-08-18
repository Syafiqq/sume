from keras import backend as K

from dlnn.tests.ml.testcase import TestCase


def layer_2_activation():
    from keras.layers import Activation
    return Activation('sigmoid')


def layer_4_activation():
    from keras.layers import Activation
    return Activation('sigmoid')


def layer_7_activation():
    from keras.layers import Activation
    return Activation('sigmoid')


def layer_11_a_activation():
    from keras.layers import Activation
    return Activation('sigmoid')


def layer_11_b_activation():
    from keras.layers import Activation
    return Activation('sigmoid')


def layer_11_c_activation():
    from keras.layers import Activation
    return Activation('sigmoid')


class ActivationTest(TestCase):
    def test_sigmoid_activation(self):
        from keras.layers import Activation
        i = K.variable([0.2])
        act = Activation('sigmoid')
        act.build(i.shape)
        x = act.call(i)
        self.assertIsNotNone(x)
        # print(K.eval(x))

    def test_sigmoid_activation_from_corr_step_1_seg_1(self):
        from dlnn.tests.ml.repos_helper import corr_step_1_seg_1
        from dlnn.tests.ml.repos_helper import corr_step_2_seg_1
        import numpy
        i = K.variable(corr_step_1_seg_1)
        act = layer_2_activation()
        act.build(i.shape)
        x = act.call(i)
        self.assertIsNotNone(x)
        self.assertTrue(numpy.allclose(K.eval(x), corr_step_2_seg_1, rtol=1e-6))
        # print(K.eval(x))

    def test_sigmoid_activation_from_corr_step_1_seg_2(self):
        from dlnn.tests.ml.repos_helper import corr_step_1_seg_2
        from dlnn.tests.ml.repos_helper import corr_step_2_seg_2
        import numpy
        i = K.variable(corr_step_1_seg_2)
        act = layer_2_activation()
        act.build(i.shape)
        x = act.call(i)
        self.assertIsNotNone(x)
        self.assertTrue(numpy.allclose(K.eval(x), corr_step_2_seg_2, rtol=1e-6))
        # print(K.eval(x))

    def test_sigmoid_activation_from_corr_step_1_seg_3(self):
        from dlnn.tests.ml.repos_helper import corr_step_1_seg_3
        from dlnn.tests.ml.repos_helper import corr_step_2_seg_3
        import numpy
        i = K.variable(corr_step_1_seg_3)
        act = layer_2_activation()
        act.build(i.shape)
        x = act.call(i)
        self.assertIsNotNone(x)
        self.assertTrue(numpy.allclose(K.eval(x), corr_step_2_seg_3, rtol=1e-6))
        # print(K.eval(x))

    def test_sigmoid_activation_from_corr_step_1(self):
        from dlnn.tests.ml.repos_helper import corr_step_1
        from dlnn.tests.ml.repos_helper import corr_step_2
        import numpy
        i = K.variable(corr_step_1)
        act = layer_2_activation()
        act.build(i.shape)
        x = act.call(i)
        self.assertIsNotNone(x)
        self.assertTrue(numpy.allclose(K.eval(x), corr_step_2, rtol=1e-6))
        # print(K.eval(x))

    def test_sigmoid_activation_from_corr_step_3_seg_1(self):
        from dlnn.tests.ml.repos_helper import corr_step_3_seg_1
        from dlnn.tests.ml.repos_helper import corr_step_4_seg_1
        import numpy
        i = K.variable(corr_step_3_seg_1)
        act = layer_4_activation()
        act.build(i.shape)
        x = act.call(i)
        self.assertIsNotNone(x)
        self.assertTrue(numpy.allclose(K.eval(x), corr_step_4_seg_1, rtol=1e-6))
        # print(K.eval(x))

    def test_sigmoid_activation_from_corr_step_3_seg_2(self):
        from dlnn.tests.ml.repos_helper import corr_step_3_seg_2
        from dlnn.tests.ml.repos_helper import corr_step_4_seg_2
        import numpy
        i = K.variable(corr_step_3_seg_2)
        act = layer_4_activation()
        act.build(i.shape)
        x = act.call(i)
        self.assertIsNotNone(x)
        self.assertTrue(numpy.allclose(K.eval(x), corr_step_4_seg_2, rtol=1e-6))
        # print(K.eval(x))

    def test_sigmoid_activation_from_corr_step_3_seg_3(self):
        from dlnn.tests.ml.repos_helper import corr_step_3_seg_3
        from dlnn.tests.ml.repos_helper import corr_step_4_seg_3
        import numpy
        i = K.variable(corr_step_3_seg_3)
        act = layer_4_activation()
        act.build(i.shape)
        x = act.call(i)
        self.assertIsNotNone(x)
        self.assertTrue(numpy.allclose(K.eval(x), corr_step_4_seg_3, rtol=1e-6))
        # print(K.eval(x))

    def test_sigmoid_activation_from_corr_step_3(self):
        from dlnn.tests.ml.repos_helper import corr_step_3
        from dlnn.tests.ml.repos_helper import corr_step_4
        import numpy
        i = K.variable(corr_step_3)
        act = layer_4_activation()
        act.build(i.shape)
        x = act.call(i)
        self.assertIsNotNone(x)
        self.assertTrue(numpy.allclose(K.eval(x), corr_step_4, rtol=1e-6))
        # print(K.eval(x))

    def test_sigmoid_activation_from_corr_step_6_seg_1(self):
        from dlnn.tests.ml.repos_helper import corr_step_6_seg_1
        from dlnn.tests.ml.repos_helper import corr_step_7_seg_1
        import numpy
        i = K.variable(corr_step_6_seg_1)
        act = layer_7_activation()
        act.build(i.shape)
        x = act.call(i)
        self.assertIsNotNone(x)
        self.assertTrue(numpy.allclose(K.eval(x), corr_step_7_seg_1, rtol=1e-6))
        # print(K.eval(x))

    def test_sigmoid_activation_from_corr_step_6_seg_2(self):
        from dlnn.tests.ml.repos_helper import corr_step_6_seg_2
        from dlnn.tests.ml.repos_helper import corr_step_7_seg_2
        import numpy
        i = K.variable(corr_step_6_seg_2)
        act = layer_7_activation()
        act.build(i.shape)
        x = act.call(i)
        self.assertIsNotNone(x)
        self.assertTrue(numpy.allclose(K.eval(x), corr_step_7_seg_2, rtol=1e-6))
        # print(K.eval(x))

    def test_sigmoid_activation_from_corr_step_6_seg_3(self):
        from dlnn.tests.ml.repos_helper import corr_step_6_seg_3
        from dlnn.tests.ml.repos_helper import corr_step_7_seg_3
        import numpy
        i = K.variable(corr_step_6_seg_3)
        act = layer_7_activation()
        act.build(i.shape)
        x = act.call(i)
        self.assertIsNotNone(x)
        self.assertTrue(numpy.allclose(K.eval(x), corr_step_7_seg_3, rtol=1e-6))
        # print(K.eval(x))

    def test_sigmoid_activation_from_corr_step_6(self):
        from dlnn.tests.ml.repos_helper import corr_step_6
        from dlnn.tests.ml.repos_helper import corr_step_7
        import numpy
        i = K.variable(corr_step_6)
        act = layer_7_activation()
        act.build(i.shape)
        x = act.call(i)
        self.assertIsNotNone(x)
        self.assertTrue(numpy.allclose(K.eval(x), corr_step_7, rtol=1e-6))
        # print(K.eval(x))

    def test_sigmoid_activation_from_corr_step_10_a(self):
        from dlnn.tests.ml.repos_helper import corr_step_10_a
        from dlnn.tests.ml.repos_helper import corr_step_11_a
        import numpy
        i = K.variable(corr_step_10_a)
        act = layer_11_a_activation()
        act.build(i.shape)
        x = act.call(i)
        self.assertIsNotNone(x)
        self.assertTrue(numpy.allclose(K.eval(x), corr_step_11_a, rtol=1e-6))
        # print(K.eval(x))

    def test_sigmoid_activation_from_corr_step_10_b(self):
        from dlnn.tests.ml.repos_helper import corr_step_10_b
        from dlnn.tests.ml.repos_helper import corr_step_11_b
        import numpy
        i = K.variable(corr_step_10_b)
        act = layer_11_b_activation()
        act.build(i.shape)
        x = act.call(i)
        self.assertIsNotNone(x)
        self.assertTrue(numpy.allclose(K.eval(x), corr_step_11_b, rtol=1e-6))
        # print(K.eval(x))

    def test_sigmoid_activation_from_corr_step_10_c(self):
        from dlnn.tests.ml.repos_helper import corr_step_10_c
        from dlnn.tests.ml.repos_helper import corr_step_11_c
        import numpy
        i = K.variable(corr_step_10_c)
        act = layer_11_b_activation()
        act.build(i.shape)
        x = act.call(i)
        self.assertIsNotNone(x)
        self.assertTrue(numpy.allclose(K.eval(x), corr_step_11_c, rtol=1e-6))
        # print(K.eval(x))
