from dlnn.tests.ml.testcase import TestCase


class CnnSeqTest(TestCase):
    def build_helper(self):
        from keras import Sequential
        from dlnn.tests.ml.conv_test import layer_1_conv
        from dlnn.tests.ml.activation_test import layer_2_activation
        from dlnn.tests.ml.conv_test import layer_3_conv
        from dlnn.tests.ml.activation_test import layer_4_activation
        from dlnn.tests.ml.pooling_test import layer_5_pool
        from dlnn.tests.ml.conv_test import layer_6_conv
        from dlnn.tests.ml.activation_test import layer_7_activation
        from dlnn.tests.ml.pooling_test import layer_8_pool

        model = Sequential()
        model.add(layer_1_conv())
        model.add(layer_2_activation())
        model.add(layer_3_conv())
        model.add(layer_4_activation())
        model.add(layer_5_pool(2))
        model.add(layer_6_conv())
        model.add(layer_7_activation())
        model.add(layer_8_pool(1))
        return model

    def test_input_to_step_1(self):
        from keras import Model
        from dlnn.tests.ml.repos_helper import normalized
        from dlnn.tests.ml.repos_helper import corr_step_1
        import numpy
        model = self.build_helper()
        network = Model(inputs=model.input,
                        outputs=model.get_layer(index=0).output)
        output = network.predict(normalized)
        self.assertIsNotNone(output)
        self.assertTrue(numpy.allclose(output[0], corr_step_1, rtol=1e-6))
        # print(output)
        # print(output.shape)

    def test_input_to_step_2(self):
        from keras import Model
        from dlnn.tests.ml.repos_helper import normalized
        from dlnn.tests.ml.repos_helper import corr_step_2
        import numpy
        model = self.build_helper()
        network = Model(inputs=model.input,
                        outputs=model.get_layer(index=1).output)
        output = network.predict(normalized)
        self.assertIsNotNone(output)
        self.assertTrue(numpy.allclose(output[0], corr_step_2, rtol=1e-6))
        # print(output)
        # print(output.shape)

    def test_input_to_step_3(self):
        from keras import Model
        from dlnn.tests.ml.repos_helper import normalized
        from dlnn.tests.ml.repos_helper import corr_step_3
        import numpy
        model = self.build_helper()
        network = Model(inputs=model.input,
                        outputs=model.get_layer(index=2).output)
        output = network.predict(normalized)
        self.assertIsNotNone(output)
        self.assertTrue(numpy.allclose(output[0], corr_step_3, rtol=1e-6))
        # print(output)
        # print(output.shape)

    def test_input_to_step_4(self):
        from keras import Model
        from dlnn.tests.ml.repos_helper import normalized
        from dlnn.tests.ml.repos_helper import corr_step_4
        import numpy
        model = self.build_helper()
        network = Model(inputs=model.input,
                        outputs=model.get_layer(index=3).output)
        output = network.predict(normalized)
        self.assertIsNotNone(output)
        self.assertTrue(numpy.allclose(output[0], corr_step_4, rtol=1e-6))
        # print(output)
        # print(output.shape)

    def test_input_to_step_5(self):
        from keras import Model
        from dlnn.tests.ml.repos_helper import normalized
        from dlnn.tests.ml.repos_helper import corr_step_5
        import numpy
        model = self.build_helper()
        network = Model(inputs=model.input,
                        outputs=model.get_layer(index=4).output)
        output = network.predict(normalized)
        self.assertIsNotNone(output)
        self.assertTrue(numpy.allclose(output[0], corr_step_5, rtol=1e-6))
        # print(output)
        # print(output.shape)

    def test_input_to_step_6(self):
        from keras import Model
        from dlnn.tests.ml.repos_helper import normalized
        from dlnn.tests.ml.repos_helper import corr_step_6
        import numpy
        model = self.build_helper()
        network = Model(inputs=model.input,
                        outputs=model.get_layer(index=5).output)
        output = network.predict(normalized)
        self.assertIsNotNone(output)
        self.assertTrue(numpy.allclose(output[0], corr_step_6, rtol=1e-6))
        # print(output)
        # print(output.shape)

    def test_input_to_step_7(self):
        from keras import Model
        from dlnn.tests.ml.repos_helper import normalized
        from dlnn.tests.ml.repos_helper import corr_step_7
        import numpy
        model = self.build_helper()
        network = Model(inputs=model.input,
                        outputs=model.get_layer(index=6).output)
        output = network.predict(normalized)
        self.assertIsNotNone(output)
        self.assertTrue(numpy.allclose(output[0], corr_step_7, rtol=1e-6))
        # print(output)
        # print(output.shape)

    def test_input_to_step_8(self):
        from keras import Model
        from dlnn.tests.ml.repos_helper import normalized
        from dlnn.tests.ml.repos_helper import corr_step_8
        import numpy
        model = self.build_helper()
        network = Model(inputs=model.input,
                        outputs=model.get_layer(index=7).output)
        output = network.predict(normalized)
        self.assertIsNotNone(output)
        self.assertTrue(numpy.allclose(output[0], corr_step_8, rtol=1e-6))
        # print(output)
        # print(output.shape)

    def test_input_to_step_8_full(self):
        from keras import Model
        from dlnn.tests.ml.repos_helper import normalized
        from dlnn.tests.ml.repos_helper import corr_step_8_full
        import numpy
        model = self.build_helper()
        network = Model(inputs=model.input,
                        outputs=model.get_layer(index=7).output)
        output = network.predict(normalized)
        self.assertIsNotNone(output)
        self.assertTrue(numpy.allclose(output, corr_step_8_full, rtol=1e-6))
        # print(output)
        # print(output.shape)
