import keras
import numpy
from keras import backend as K
from keras.layers import Flatten, Dense
from scipy import stats

from dlnn.tests.ml.activation_test import layer_11_a_activation, layer_11_b_activation, layer_11_c_activation
from dlnn.tests.ml.cnn_func_test import inputs, step_8_pool
from dlnn.tests.ml.elm_process_helper import step_10_a_kernel_init, step_10_a_bias_init, \
    step_10_b_kernel_init, step_10_b_bias_init, step_10_c_kernel_init, step_10_c_bias_init
from dlnn.tests.ml.repos_helper import normalized, categorical_label_init
from dlnn.tests.ml.testcase import TestCase


def layer_9_flatten():
    return Flatten()


def layer_10_a_dense():
    return Dense(5, activation=None, use_bias=True, kernel_initializer=step_10_a_kernel_init,
                 bias_initializer=step_10_a_bias_init, trainable=False)


def layer_10_b_dense():
    return Dense(7, activation=None, use_bias=True, kernel_initializer=step_10_b_kernel_init,
                 bias_initializer=step_10_b_bias_init, trainable=False)


def layer_10_c_dense():
    return Dense(4, activation=None, use_bias=True, kernel_initializer=step_10_c_kernel_init,
                 bias_initializer=step_10_c_bias_init, trainable=False)


def layer_12_a_dense():
    return Dense(3, activation=None, use_bias=False, kernel_initializer=keras.initializers.Zeros(), trainable=False)


def layer_12_b_dense():
    return Dense(3, activation=None, use_bias=False, kernel_initializer=keras.initializers.Zeros(), trainable=False)


def layer_12_c_dense():
    return Dense(3, activation=None, use_bias=False, kernel_initializer=keras.initializers.Zeros(), trainable=False)


def layer_13_concatenate():
    return keras.layers.Concatenate()


def layer_14_reshape():
    return keras.layers.Reshape((3, 3))


def layer_15_merge_categorical():
    from dlnn.layer.MergeCategorical import MergeCategorical
    return MergeCategorical(3)


def unifinv_init(shape, dtype=None):
    return K.variable(stats.uniform.ppf(numpy.random.rand(*shape), loc=-.5, scale=(.5 - -.5)),
                      dtype=dtype)


step_9_flatten = layer_9_flatten()(step_8_pool)
step_10_a_dense = layer_10_a_dense()(step_9_flatten)
step_11_a_activation = layer_11_a_activation()(step_10_a_dense)
step_12_a_dense = layer_12_a_dense()(step_11_a_activation)
step_10_b_dense = layer_10_b_dense()(step_9_flatten)
step_11_b_activation = layer_11_b_activation()(step_10_b_dense)
step_12_b_dense = layer_12_b_dense()(step_11_b_activation)
step_10_c_dense = layer_10_c_dense()(step_9_flatten)
step_11_c_activation = layer_11_c_activation()(step_10_c_dense)
step_12_c_dense = layer_12_c_dense()(step_11_c_activation)
step_13_concatenate = layer_13_concatenate()([step_12_a_dense, step_12_b_dense, step_12_c_dense])
step_14_reshape = layer_14_reshape()(step_13_concatenate)
step_15_output = layer_15_merge_categorical()(step_14_reshape)


class ElmFuncTest(TestCase):
    def test_input_to_step_9(self):
        from keras import Model
        from dlnn.tests.ml.repos_helper import corr_step_9
        import numpy
        network = Model(inputs=inputs, outputs=step_9_flatten)
        network.compile(optimizer='rmsprop', loss='categorical_crossentropy', metrics=['accuracy'])
        output = network.predict(normalized)
        self.assertIsNotNone(output)
        self.assertTrue(numpy.allclose(output, corr_step_9, rtol=1e-6))
        # print(output)
        # print(output.shape)

    def test_input_to_step_10_a(self):
        from keras import Model
        from dlnn.tests.ml.repos_helper import corr_step_10_a
        import numpy
        network = Model(inputs=inputs, outputs=step_10_a_dense)
        network.compile(optimizer='rmsprop', loss='categorical_crossentropy', metrics=['accuracy'])
        output = network.predict(normalized)
        self.assertIsNotNone(output)
        self.assertTrue(numpy.allclose(output, corr_step_10_a, rtol=1e-6))
        # print(output)
        # print(output.shape)

    def test_input_to_step_11_a(self):
        from keras import Model
        from dlnn.tests.ml.repos_helper import corr_step_11_a
        import numpy
        network = Model(inputs=inputs, outputs=step_11_a_activation)
        network.compile(optimizer='rmsprop', loss='categorical_crossentropy', metrics=['accuracy'])
        output = network.predict(normalized)
        self.assertIsNotNone(output)
        self.assertTrue(numpy.allclose(output, corr_step_11_a, rtol=1e-6))
        # print(output)
        # print(output.shape)

    def test_input_to_beta_a(self):
        from keras import Model
        from dlnn.util import MoorePenrose
        network = Model(inputs=inputs, outputs=step_11_a_activation)
        network.compile(optimizer='rmsprop', loss='categorical_crossentropy', metrics=['accuracy'])
        output = network.predict(normalized)
        beta = K.dot(MoorePenrose.pinv3(output), K.variable(categorical_label_init))
        self.assertIsNotNone(beta)
        # print(K.eval(beta))
        # print(beta.shape)

    def test_check_weights_layer(self):
        from keras import Model
        from dlnn.tests.ml.cnn_func_test import inputs
        network = Model(inputs=inputs, outputs=step_11_a_activation)
        network.compile(optimizer='rmsprop', loss='categorical_crossentropy', metrics=['accuracy'])
        for i in range(12):
            layer = network.get_layer(index=i).get_weights()
            self.assertIsNotNone(layer)
            # print("step_%d" % (i + 1), layer)
        network.predict(normalized)
        for i in range(12):
            layer = network.get_layer(index=i).get_weights()
            self.assertIsNotNone(layer)
            # print("step_%d" % (i + 1), layer)

    def test_training_model_aka_to_step_12_a(self):
        from keras import Model
        from dlnn.tests.ml.cnn_func_test import inputs
        from dlnn.util import MoorePenrose
        #
        # Feed Beta
        #
        feed = Model(inputs=inputs, outputs=step_11_a_activation)
        output = feed.predict(normalized)
        w_10_a = feed.get_layer(index=10).get_weights()
        w_12_a = [K.eval(K.dot(MoorePenrose.pinv3(output), K.variable(categorical_label_init)))]
        for i in range(12):
            layer = feed.get_layer(index=i).get_weights()
            self.assertIsNotNone(layer)
            # print("step_%d" % (i + 1), layer)

        #
        # Training Model
        #
        network = Model(inputs=inputs, outputs=step_12_a_dense)
        network.compile(optimizer=keras.optimizers.RMSprop(lr=0.0, rho=0.0, epsilon=None, decay=0.0),
                        loss=keras.losses.categorical_crossentropy,
                        metrics=[keras.metrics.categorical_accuracy, keras.metrics.mape])
        network.get_layer(index=10).set_weights(w_10_a)
        network.get_layer(index=12).set_weights(w_12_a)
        network.fit(normalized, categorical_label_init, batch_size=normalized.shape[0])
        self.assertTrue(numpy.allclose(w_10_a[0], network.get_layer(index=10).get_weights()[0], rtol=0))
        self.assertTrue(numpy.allclose(w_12_a[0], network.get_layer(index=12).get_weights()[0], rtol=0))
        result = network.predict(normalized, batch_size=normalized.shape[0])
        self.assertIsNotNone(result)
        # print(result.argmax(axis=-1))

    def test_input_to_step_10_b(self):
        from keras import Model
        from dlnn.tests.ml.repos_helper import corr_step_10_b
        import numpy
        network = Model(inputs=inputs, outputs=step_10_b_dense)
        network.compile(optimizer='rmsprop', loss='categorical_crossentropy', metrics=['accuracy'])
        output = network.predict(normalized)
        self.assertIsNotNone(output)
        self.assertTrue(numpy.allclose(output, corr_step_10_b, rtol=1e-6))
        # print(output)
        # print(output.shape)

    def test_input_to_step_11_b(self):
        from keras import Model
        from dlnn.tests.ml.repos_helper import corr_step_11_b
        import numpy
        network = Model(inputs=inputs, outputs=step_11_b_activation)
        network.compile(optimizer='rmsprop', loss='categorical_crossentropy', metrics=['accuracy'])
        output = network.predict(normalized)
        self.assertIsNotNone(output)
        self.assertTrue(numpy.allclose(output, corr_step_11_b, rtol=1e-6))
        # print(output)
        # print(output.shape)

    def test_input_to_beta_b(self):
        from keras import Model
        from dlnn.util import MoorePenrose
        network = Model(inputs=inputs, outputs=step_11_b_activation)
        network.compile(optimizer='rmsprop', loss='categorical_crossentropy', metrics=['accuracy'])
        output = network.predict(normalized)
        beta = K.dot(MoorePenrose.pinv3(output), K.variable(categorical_label_init))
        self.assertIsNotNone(beta)
        # print(K.eval(beta))
        # print(beta.shape)

    def test_training_model_bka_to_step_12_b(self):
        from keras import Model
        from dlnn.tests.ml.cnn_func_test import inputs
        from dlnn.util import MoorePenrose
        #
        # Feed Beta
        #
        feed = Model(inputs=inputs, outputs=step_11_b_activation)
        output = feed.predict(normalized)
        w_10_b = feed.get_layer(index=10).get_weights()
        w_12_b = [K.eval(K.dot(MoorePenrose.pinv3(output), K.variable(categorical_label_init)))]
        for i in range(12):
            layer = feed.get_layer(index=i).get_weights()
            self.assertIsNotNone(layer)
            # print("step_%d" % (i + 1), layer)

        #
        # Training Model
        #
        network = Model(inputs=inputs, outputs=step_12_b_dense)
        network.compile(optimizer=keras.optimizers.RMSprop(lr=0.0, rho=0.0, epsilon=None, decay=0.0),
                        loss=keras.losses.categorical_crossentropy,
                        metrics=[keras.metrics.categorical_accuracy, keras.metrics.mape])
        network.get_layer(index=10).set_weights(w_10_b)
        network.get_layer(index=12).set_weights(w_12_b)
        network.fit(normalized, categorical_label_init, batch_size=normalized.shape[0])
        self.assertTrue(numpy.allclose(w_10_b[0], network.get_layer(index=10).get_weights()[0], rtol=0))
        self.assertTrue(numpy.allclose(w_12_b[0], network.get_layer(index=12).get_weights()[0], rtol=0))
        result = network.predict(normalized, batch_size=normalized.shape[0])
        self.assertIsNotNone(result)
        # print(result.argmax(axis=-1))

    def test_input_to_step_10_c(self):
        from keras import Model
        from dlnn.tests.ml.repos_helper import corr_step_10_c
        import numpy
        network = Model(inputs=inputs, outputs=step_10_c_dense)
        network.compile(optimizer='rmsprop', loss='categorical_crossentropy', metrics=['accuracy'])
        output = network.predict(normalized)
        self.assertIsNotNone(output)
        self.assertTrue(numpy.allclose(output, corr_step_10_c, rtol=1e-6))
        # print(output)
        # print(output.shape)

    def test_input_to_step_11_c(self):
        from keras import Model
        from dlnn.tests.ml.repos_helper import corr_step_11_c
        import numpy
        network = Model(inputs=inputs, outputs=step_11_c_activation)
        network.compile(optimizer='rmsprop', loss='categorical_crossentropy', metrics=['accuracy'])
        output = network.predict(normalized)
        self.assertIsNotNone(output)
        self.assertTrue(numpy.allclose(output, corr_step_11_c, rtol=1e-6))
        # print(output)
        # print(output.shape)

    def test_input_to_beta_c(self):
        from keras import Model
        from dlnn.util import MoorePenrose
        network = Model(inputs=inputs, outputs=step_11_c_activation)
        network.compile(optimizer='rmsprop', loss='categorical_crossentropy', metrics=['accuracy'])
        output = network.predict(normalized)
        beta = K.dot(MoorePenrose.pinv3(output), K.variable(categorical_label_init))
        self.assertIsNotNone(beta)
        # print(K.eval(beta))
        # print(beta.shape)

    def test_training_model_bka_to_step_12_c(self):
        from keras import Model
        from dlnn.tests.ml.cnn_func_test import inputs
        from dlnn.util import MoorePenrose
        #
        # Feed Beta
        #
        feed = Model(inputs=inputs, outputs=step_11_c_activation)
        output = feed.predict(normalized)
        w_10_b = feed.get_layer(index=10).get_weights()
        w_12_b = [K.eval(K.dot(MoorePenrose.pinv3(output), K.variable(categorical_label_init)))]
        for i in range(12):
            layer = feed.get_layer(index=i).get_weights()
            self.assertIsNotNone(layer)
            # print("step_%d" % (i + 1), layer)

        #
        # Training Model
        #
        network = Model(inputs=inputs, outputs=step_12_c_dense)
        network.compile(optimizer=keras.optimizers.RMSprop(lr=0.0, rho=0.0, epsilon=None, decay=0.0),
                        loss=keras.losses.categorical_crossentropy,
                        metrics=[keras.metrics.categorical_accuracy, keras.metrics.mape])
        network.get_layer(index=10).set_weights(w_10_b)
        network.get_layer(index=12).set_weights(w_12_b)
        network.fit(normalized, categorical_label_init, batch_size=normalized.shape[0])
        self.assertTrue(numpy.allclose(w_10_b[0], network.get_layer(index=10).get_weights()[0], rtol=0))
        self.assertTrue(numpy.allclose(w_12_b[0], network.get_layer(index=12).get_weights()[0], rtol=0))
        result = network.predict(normalized, batch_size=normalized.shape[0])
        self.assertIsNotNone(result)
        # print(result.argmax(axis=1))

    def test_manual_merge_categorical_value(self):
        from keras import Model
        from dlnn.tests.ml.cnn_func_test import inputs
        from dlnn.util import MoorePenrose
        import tensorflow as tf
        #
        # Feed Beta
        #
        feed = Model(inputs=inputs, outputs=step_11_a_activation)
        output = feed.predict(normalized)
        w_10_a = feed.get_layer(index=10).get_weights()
        w_12_a = [K.eval(K.dot(MoorePenrose.pinv3(output), K.variable(categorical_label_init)))]
        feed = Model(inputs=inputs, outputs=step_11_b_activation)
        output = feed.predict(normalized)
        w_10_b = feed.get_layer(index=10).get_weights()
        w_12_b = [K.eval(K.dot(MoorePenrose.pinv3(output), K.variable(categorical_label_init)))]
        feed = Model(inputs=inputs, outputs=step_11_c_activation)
        output = feed.predict(normalized)
        w_10_c = feed.get_layer(index=10).get_weights()
        w_12_c = [K.eval(K.dot(MoorePenrose.pinv3(output), K.variable(categorical_label_init)))]

        #
        # Training Model
        #
        network = Model(inputs=inputs, outputs=step_14_reshape)
        network.compile(optimizer=keras.optimizers.RMSprop(lr=0.0, rho=0.0, epsilon=None, decay=0.0),
                        loss=keras.losses.categorical_crossentropy,
                        metrics=[keras.metrics.categorical_accuracy, keras.metrics.mape])
        network.get_layer(index=10).set_weights(w_10_a)
        network.get_layer(index=11).set_weights(w_10_b)
        network.get_layer(index=12).set_weights(w_10_c)
        network.get_layer(index=16).set_weights(w_12_a)
        network.get_layer(index=17).set_weights(w_12_b)
        network.get_layer(index=18).set_weights(w_12_c)
        result = network.predict(normalized, batch_size=normalized.shape[0])
        # print(result)
        result = K.cast(K.argmax(result), dtype=tf.int32)
        # print(K.eval(result))
        result = tf.map_fn(lambda x: tf.bincount(x, minlength=3), result)
        # print(K.eval(result))
        result = K.argmax(result)
        # print(K.eval(result))
        self.assertIsNotNone(result)

    def test_dlnn_final(self):
        from keras import Model
        from dlnn.tests.ml.cnn_func_test import inputs
        from dlnn.util import MoorePenrose
        #
        # Feed Beta
        #
        feed = Model(inputs=inputs, outputs=step_11_a_activation)
        output = feed.predict(normalized)
        w_10_a = feed.get_layer(index=10).get_weights()
        w_12_a = [K.eval(K.dot(MoorePenrose.pinv3(output), K.variable(categorical_label_init)))]
        feed = Model(inputs=inputs, outputs=step_11_b_activation)
        output = feed.predict(normalized)
        w_10_b = feed.get_layer(index=10).get_weights()
        w_12_b = [K.eval(K.dot(MoorePenrose.pinv3(output), K.variable(categorical_label_init)))]
        feed = Model(inputs=inputs, outputs=step_11_c_activation)
        output = feed.predict(normalized)
        w_10_c = feed.get_layer(index=10).get_weights()
        w_12_c = [K.eval(K.dot(MoorePenrose.pinv3(output), K.variable(categorical_label_init)))]

        #
        # Training Model
        #
        network = Model(inputs=inputs, outputs=step_15_output)
        network.compile(optimizer=keras.optimizers.RMSprop(lr=0.0, rho=0.0, epsilon=None, decay=0.0),
                        loss=keras.losses.categorical_crossentropy,
                        metrics=[keras.metrics.categorical_accuracy, keras.metrics.mape])
        for i in range(20):
            layer = network.get_layer(index=i).get_weights()
            self.assertIsNotNone(layer)
            # print("step_%d" % (i + 1), layer)
        network.get_layer(index=10).set_weights(w_10_a)
        network.get_layer(index=11).set_weights(w_10_b)
        network.get_layer(index=12).set_weights(w_10_c)
        network.get_layer(index=16).set_weights(w_12_a)
        network.get_layer(index=17).set_weights(w_12_b)
        network.get_layer(index=18).set_weights(w_12_c)
        network.fit(normalized, categorical_label_init, batch_size=normalized.shape[0])
        self.assertTrue(numpy.allclose(w_10_a[0], network.get_layer(index=10).get_weights()[0], rtol=0))
        self.assertTrue(numpy.allclose(w_10_b[0], network.get_layer(index=11).get_weights()[0], rtol=0))
        self.assertTrue(numpy.allclose(w_10_c[0], network.get_layer(index=12).get_weights()[0], rtol=0))
        self.assertTrue(numpy.allclose(w_12_a[0], network.get_layer(index=16).get_weights()[0], rtol=0))
        self.assertTrue(numpy.allclose(w_12_b[0], network.get_layer(index=17).get_weights()[0], rtol=0))
        self.assertTrue(numpy.allclose(w_12_c[0], network.get_layer(index=18).get_weights()[0], rtol=0))
        result = network.predict(normalized, batch_size=normalized.shape[0])
        # print(result.argmax(axis=1))
        self.assertIsNotNone(result)
