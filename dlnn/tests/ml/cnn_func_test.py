from keras import Input

from dlnn.tests.ml.activation_test import layer_2_activation
from dlnn.tests.ml.activation_test import layer_4_activation
from dlnn.tests.ml.activation_test import layer_7_activation
from dlnn.tests.ml.conv_test import layer_1_conv
from dlnn.tests.ml.conv_test import layer_3_conv
from dlnn.tests.ml.conv_test import layer_6_conv
from dlnn.tests.ml.pooling_test import layer_5_pool
from dlnn.tests.ml.pooling_test import layer_8_pool
from dlnn.tests.ml.repos_helper import normalized
from dlnn.tests.ml.testcase import TestCase

inputs = Input(shape=normalized.shape[1:])
step_1_conv = layer_1_conv()(inputs)
step_2_activation = layer_2_activation()(step_1_conv)
step_3_conv = layer_3_conv()(step_2_activation)
step_4_activation = layer_4_activation()(step_3_conv)
step_5_pool = layer_5_pool(2)(step_4_activation)
step_6_conv = layer_6_conv()(step_5_pool)
step_7_activation = layer_7_activation()(step_6_conv)
step_8_pool = layer_8_pool(1)(step_7_activation)


class CnnFuncTest(TestCase):
    def test_input_to_step_1(self):
        from keras import Model
        from dlnn.tests.ml.repos_helper import corr_step_1
        import numpy
        network = Model(inputs=inputs, outputs=step_1_conv)
        network.compile(optimizer='rmsprop', loss='categorical_crossentropy', metrics=['accuracy'])
        output = network.predict(normalized)
        self.assertIsNotNone(output)
        self.assertTrue(numpy.allclose(output[0], corr_step_1, rtol=1e-6))
        # print(output)
        # print(output.shape)

    def test_input_to_step_2(self):
        from keras import Model
        from dlnn.tests.ml.repos_helper import corr_step_2
        import numpy
        network = Model(inputs=inputs, outputs=step_2_activation)
        network.compile(optimizer='rmsprop', loss='categorical_crossentropy', metrics=['accuracy'])
        output = network.predict(normalized)
        self.assertIsNotNone(output)
        self.assertTrue(numpy.allclose(output[0], corr_step_2, rtol=1e-6))
        # print(output)
        # print(output.shape)

    def test_input_to_step_3(self):
        from keras import Model
        from dlnn.tests.ml.repos_helper import corr_step_3
        import numpy
        network = Model(inputs=inputs, outputs=step_3_conv)
        network.compile(optimizer='rmsprop', loss='categorical_crossentropy', metrics=['accuracy'])
        output = network.predict(normalized)
        self.assertIsNotNone(output)
        self.assertTrue(numpy.allclose(output[0], corr_step_3, rtol=1e-6))
        # print(output)
        # print(output.shape)

    def test_input_to_step_4(self):
        from keras import Model
        from dlnn.tests.ml.repos_helper import corr_step_4
        import numpy
        network = Model(inputs=inputs, outputs=step_4_activation)
        network.compile(optimizer='rmsprop', loss='categorical_crossentropy', metrics=['accuracy'])
        output = network.predict(normalized)
        self.assertIsNotNone(output)
        self.assertTrue(numpy.allclose(output[0], corr_step_4, rtol=1e-6))
        # print(output)
        # print(output.shape)

    def test_input_to_step_5(self):
        from keras import Model
        from dlnn.tests.ml.repos_helper import corr_step_5
        import numpy
        network = Model(inputs=inputs, outputs=step_5_pool)
        network.compile(optimizer='rmsprop', loss='categorical_crossentropy', metrics=['accuracy'])
        output = network.predict(normalized)
        self.assertIsNotNone(output)
        self.assertTrue(numpy.allclose(output[0], corr_step_5, rtol=1e-6))
        # print(output)
        # print(output.shape)

    def test_input_to_step_6(self):
        from keras import Model
        from dlnn.tests.ml.repos_helper import corr_step_6
        import numpy
        network = Model(inputs=inputs, outputs=step_6_conv)
        network.compile(optimizer='rmsprop', loss='categorical_crossentropy', metrics=['accuracy'])
        output = network.predict(normalized)
        self.assertIsNotNone(output)
        self.assertTrue(numpy.allclose(output[0], corr_step_6, rtol=1e-6))
        # print(output)
        # print(output.shape)

    def test_input_to_step_7(self):
        from keras import Model
        from dlnn.tests.ml.repos_helper import corr_step_7
        import numpy
        network = Model(inputs=inputs, outputs=step_7_activation)
        network.compile(optimizer='rmsprop', loss='categorical_crossentropy', metrics=['accuracy'])
        output = network.predict(normalized)
        self.assertIsNotNone(output)
        self.assertTrue(numpy.allclose(output[0], corr_step_7, rtol=1e-6))
        # print(output)
        # print(output.shape)

    def test_input_to_step_8(self):
        from keras import Model
        from dlnn.tests.ml.repos_helper import corr_step_8
        import numpy
        network = Model(inputs=inputs, outputs=step_8_pool)
        network.compile(optimizer='rmsprop', loss='categorical_crossentropy', metrics=['accuracy'])
        output = network.predict(normalized)
        self.assertIsNotNone(output)
        self.assertTrue(numpy.allclose(output[0], corr_step_8, rtol=1e-6))
        # print(output)
        # print(output.shape)

    def test_input_to_step_8_full(self):
        from keras import Model
        from dlnn.tests.ml.repos_helper import corr_step_8_full
        import numpy
        network = Model(inputs=inputs, outputs=step_8_pool)
        network.compile(optimizer='rmsprop', loss='categorical_crossentropy', metrics=['accuracy'])
        output = network.predict(normalized)
        self.assertIsNotNone(output)
        self.assertTrue(numpy.allclose(output, corr_step_8_full, rtol=1e-6))
        # print(output)
        # print(output.shape)
