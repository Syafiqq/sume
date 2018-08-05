import os

import numpy
from keras import Input, Model
from keras import backend as K
from keras.activations import sigmoid
from keras.engine.saving import load_model
from keras.initializers import RandomUniform, Zeros
from keras.layers import Reshape, Activation, MaxPooling2D, Flatten, Dense, Concatenate
from keras.losses import categorical_crossentropy
from keras.metrics import categorical_accuracy, mape
from keras.optimizers import RMSprop

from dlnn.layer.Conv2D import AvgFilter
from dlnn.layer.Conv2D import Conv2D
from dlnn.layer.Conv2D import MaxFilter
from dlnn.layer.Conv2D import StdDevFilter
from dlnn.layer.MergeCategorical import MergeCategorical
from dlnn.layer.Scaling import Scaling
from dlnn.layer.Tiling import Tiling
from dlnn.util import MoorePenrose, to_categorical
from dlnn.util.Initializers import Unifinv
from sume.settings import BASE_DIR

DLNN_DEFAULT_CONFIG = {
    'scale_min1': 0.0,
    'scale_max1': 300.0,
    'scale_min2': 0.0,
    'scale_max2': 1.0,
    'conv_1_window': 3,
    'conv_2_window': 3,
    'conv_3_window': 3,
    'pool_1_size': 2,
    'pool_2_size': 1,
    'elm_1_dense_1_units': 5,
    'elm_2_dense_1_units': 7,
    'elm_3_dense_1_units': 4,
    'elm_1_dense_1_kernel_min': -0.5,
    'elm_1_dense_1_kernel_max': +0.5,
    'elm_2_dense_1_kernel_min': -0.5,
    'elm_2_dense_1_kernel_max': +0.5,
    'elm_3_dense_1_kernel_min': -0.5,
    'elm_3_dense_1_kernel_max': +0.5,
    'elm_1_dense_1_bias_min': 0.0,
    'elm_1_dense_1_bias_max': 1.0,
    'elm_2_dense_1_bias_min': 0.0,
    'elm_2_dense_1_bias_max': 1.0,
    'elm_3_dense_1_bias_min': 0.0,
    'elm_3_dense_1_bias_max': 1.0,
}


class Dlnn(object):
    def __init__(self,
                 network_name='network',
                 scale_min1=0.0,
                 scale_max1=0.0,
                 scale_min2=0.0,
                 scale_max2=0.0,
                 conv_1_window=0,
                 conv_2_window=0,
                 conv_3_window=0,
                 pool_1_size=0,
                 pool_2_size=0,
                 elm_1_dense_1_units=0,
                 elm_2_dense_1_units=0,
                 elm_3_dense_1_units=0,
                 elm_1_dense_1_kernel_min=0.0,
                 elm_1_dense_1_kernel_max=0.0,
                 elm_2_dense_1_kernel_min=0.0,
                 elm_2_dense_1_kernel_max=0.0,
                 elm_3_dense_1_kernel_min=0.0,
                 elm_3_dense_1_kernel_max=0.0,
                 elm_1_dense_1_bias_min=0.0,
                 elm_1_dense_1_bias_max=0.0,
                 elm_2_dense_1_bias_min=0.0,
                 elm_2_dense_1_bias_max=0.0,
                 elm_3_dense_1_bias_min=0.0,
                 elm_3_dense_1_bias_max=0.0, ):
        self.layer = {}
        self.network_name = network_name,
        self.network_path = os.path.join(BASE_DIR, "dlnn/resources/%s.h5" % self.network_name)
        self.input_shape = None
        self.category_num = None

        self.scale_min1 = float(scale_min1)
        self.scale_max1 = float(scale_max1)
        self.scale_min2 = float(scale_min2)
        self.scale_max2 = float(scale_max2)

        self.conv_1_window = int(conv_1_window)
        self.conv_2_window = int(conv_2_window)
        self.conv_3_window = int(conv_3_window)

        self.pool_1_size = int(pool_1_size)
        self.pool_2_size = int(pool_2_size)

        self.elm_1_dense_1_units = int(elm_1_dense_1_units)
        self.elm_2_dense_1_units = int(elm_2_dense_1_units)
        self.elm_3_dense_1_units = int(elm_3_dense_1_units)
        self.elm_1_dense_1_kernel_min = float(elm_1_dense_1_kernel_min)
        self.elm_1_dense_1_kernel_max = float(elm_1_dense_1_kernel_max)
        self.elm_2_dense_1_kernel_min = float(elm_2_dense_1_kernel_min)
        self.elm_2_dense_1_kernel_max = float(elm_2_dense_1_kernel_max)
        self.elm_3_dense_1_kernel_min = float(elm_3_dense_1_kernel_min)
        self.elm_3_dense_1_kernel_max = float(elm_3_dense_1_kernel_max)
        self.elm_1_dense_1_bias_min = float(elm_1_dense_1_bias_min)
        self.elm_1_dense_1_bias_max = float(elm_1_dense_1_bias_max)
        self.elm_2_dense_1_bias_min = float(elm_2_dense_1_bias_min)
        self.elm_2_dense_1_bias_max = float(elm_2_dense_1_bias_max)
        self.elm_3_dense_1_bias_min = float(elm_3_dense_1_bias_min)
        self.elm_3_dense_1_bias_max = float(elm_3_dense_1_bias_max)

        self.fully_connected_num = 3

    def train(self, x, y):
        assert x is not None
        assert y is not None
        if len(y.shape) > 1:
            y = y.flatten()
        self.input_shape = x.shape[-1]
        self.category_num = len(numpy.unique(y))
        self.build_model()
        self.__train(x, y)
        return self.__evaluate(x, y)

    def __train(self, x, y):
        assert self.layer is not None
        yc = to_categorical(y, self.category_num)
        elm_1_beta_net = Model(inputs=self.layer['input'], outputs=self.layer['elm_1_activation_1'])
        elm_1_activation_1_o = elm_1_beta_net.predict(x)
        elm_1_dense_1_w = elm_1_beta_net.get_layer(name='elm_1_dense_1').get_weights()
        elm_1_dense_2_w = [
            K.eval(K.dot(MoorePenrose.pinv3(elm_1_activation_1_o), yc))]
        elm_2_beta_net = Model(inputs=self.layer['input'], outputs=self.layer['elm_2_activation_1'])
        elm_2_activation_1_o = elm_2_beta_net.predict(x)
        elm_2_dense_1_w = elm_2_beta_net.get_layer(name='elm_2_dense_1').get_weights()
        elm_2_dense_2_w = [
            K.eval(K.dot(MoorePenrose.pinv3(elm_2_activation_1_o), yc))]
        elm_3_beta_net = Model(inputs=self.layer['input'], outputs=self.layer['elm_3_activation_1'])
        elm_3_activation_1_o = elm_3_beta_net.predict(x)
        elm_3_dense_1_w = elm_3_beta_net.get_layer(name='elm_3_dense_1').get_weights()
        elm_3_dense_2_w = [
            K.eval(K.dot(MoorePenrose.pinv3(elm_3_activation_1_o), yc))]
        network = Model(inputs=self.layer['input'], outputs=self.layer['fully_connected_merge'])
        network.compile(optimizer=RMSprop(lr=0.0, rho=0.0, epsilon=None, decay=0.0),
                        loss=categorical_crossentropy,
                        metrics=[categorical_accuracy, mape])
        network.get_layer(name='elm_1_dense_1').set_weights(elm_1_dense_1_w)
        network.get_layer(name='elm_1_dense_2').set_weights(elm_1_dense_2_w)
        network.get_layer(name='elm_2_dense_1').set_weights(elm_2_dense_1_w)
        network.get_layer(name='elm_2_dense_2').set_weights(elm_2_dense_2_w)
        network.get_layer(name='elm_3_dense_1').set_weights(elm_3_dense_1_w)
        network.get_layer(name='elm_3_dense_2').set_weights(elm_3_dense_2_w)
        network.fit(x, yc)
        network.save(self.network_path)

    def __evaluate(self, x, y):
        yc = to_categorical(y, self.category_num)
        network = self.get_model()
        return network.evaluate(x, yc)

    def build_model(self):
        self.layer['input'] = Input(
            shape=(self.input_shape,))

        self.layer['pre_scaling'] = Scaling(
            scale_min1=self.scale_min1,
            scale_max1=self.scale_max1,
            scale_min2=self.scale_min2,
            scale_max2=self.scale_max2,
            name='pre_scaling')(self.layer['input'])

        self.layer['pre_reshaping'] = Reshape(
            target_shape=[1, 1, self.input_shape],
            name='pre_reshaping')(self.layer['pre_scaling'])

        self.layer['pre_tiling'] = Tiling(
            units=self.input_shape,
            name='pre_tiling')(self.layer['pre_reshaping'])

        self.layer['cnn_conv_1'] = Conv2D(
            filters=[AvgFilter(), MaxFilter(), StdDevFilter()],
            window=self.conv_1_window,
            padding='same',
            use_bias=False,
            kernel_size=(self.input_shape, self.input_shape),
            data_format='channels_first',
            name='cnn_conv_1')(self.layer['pre_tiling'])

        self.layer['cnn_activation_1'] = Activation(
            activation=sigmoid,
            name='cnn_activation_1')(self.layer['cnn_conv_1'])

        self.layer['cnn_conv_2'] = Conv2D(
            filters=[AvgFilter(), MaxFilter(), StdDevFilter()],
            window=self.conv_2_window,
            padding='same',
            use_bias=False,
            kernel_size=(self.input_shape, self.input_shape),
            data_format='channels_first',
            name='cnn_conv_2')(self.layer['cnn_activation_1'])

        self.layer['cnn_activation_2'] = Activation(
            activation=sigmoid,
            name='cnn_activation_2')(self.layer['cnn_conv_2'])

        self.layer['cnn_pooling_1'] = MaxPooling2D(
            pool_size=(self.pool_1_size, self.pool_1_size),
            padding='same',
            data_format='channels_first',
            name='cnn_pooling_1')(self.layer['cnn_activation_2'])

        self.layer['cnn_conv_3'] = Conv2D(
            filters=[AvgFilter(), MaxFilter(), StdDevFilter()],
            window=self.conv_3_window,
            padding='same',
            use_bias=False,
            kernel_size=(self.input_shape, self.input_shape),
            data_format='channels_first',
            name='cnn_conv_3')(self.layer['cnn_pooling_1'])

        self.layer['cnn_activation_3'] = Activation(
            activation=sigmoid,
            name='cnn_activation_3')(self.layer['cnn_conv_3'])

        self.layer['cnn_pooling_2'] = MaxPooling2D(
            pool_size=(self.pool_2_size, self.pool_2_size),
            padding='same',
            data_format='channels_first',
            name='cnn_pooling_2')(self.layer['cnn_activation_3'])

        self.layer['bridge_flatten'] = Flatten(
            name='bridge_flatten')(self.layer['cnn_pooling_2'])

        self.layer['elm_1_dense_1'] = Dense(
            units=self.elm_1_dense_1_units,
            activation=None,
            use_bias=True,
            kernel_initializer=Unifinv(minval=self.elm_1_dense_1_kernel_min, maxval=self.elm_1_dense_1_kernel_max),
            bias_initializer=RandomUniform(minval=self.elm_1_dense_1_bias_min, maxval=self.elm_1_dense_1_bias_max),
            trainable=False,
            name='elm_1_dense_1')(self.layer['bridge_flatten'])

        self.layer['elm_1_activation_1'] = Activation(
            activation=sigmoid,
            name='elm_1_activation_1')(self.layer['elm_1_dense_1'])

        self.layer['elm_1_dense_2'] = Dense(
            units=self.category_num,
            activation=None,
            use_bias=False,
            kernel_initializer=Zeros(),
            trainable=False,
            name='elm_1_dense_2')(self.layer['elm_1_activation_1'])

        self.layer['elm_2_dense_1'] = Dense(
            units=self.elm_2_dense_1_units,
            activation=None,
            use_bias=True,
            kernel_initializer=Unifinv(minval=self.elm_2_dense_1_kernel_min, maxval=self.elm_2_dense_1_kernel_max),
            bias_initializer=RandomUniform(minval=self.elm_2_dense_1_bias_min, maxval=self.elm_2_dense_1_bias_max),
            trainable=False,
            name='elm_2_dense_1')(self.layer['bridge_flatten'])

        self.layer['elm_2_activation_1'] = Activation(
            activation=sigmoid,
            name='elm_2_activation_1')(self.layer['elm_2_dense_1'])

        self.layer['elm_2_dense_2'] = Dense(
            units=self.category_num,
            activation=None,
            use_bias=False,
            kernel_initializer=Zeros(),
            trainable=False,
            name='elm_2_dense_2')(self.layer['elm_2_activation_1'])

        self.layer['elm_3_dense_1'] = Dense(
            units=self.elm_3_dense_1_units,
            activation=None,
            use_bias=True,
            kernel_initializer=Unifinv(minval=self.elm_3_dense_1_kernel_min, maxval=self.elm_3_dense_1_kernel_max),
            bias_initializer=RandomUniform(minval=self.elm_3_dense_1_bias_min, maxval=self.elm_3_dense_1_bias_max),
            trainable=False,
            name='elm_3_dense_1')(self.layer['bridge_flatten'])

        self.layer['elm_3_activation_1'] = Activation(
            activation=sigmoid,
            name='elm_3_activation_1')(self.layer['elm_3_dense_1'])

        self.layer['elm_3_dense_2'] = Dense(
            units=self.category_num,
            activation=None,
            use_bias=False,
            kernel_initializer=Zeros(),
            trainable=False,
            name='elm_3_dense_2')(self.layer['elm_3_activation_1'])

        self.layer['fully_connected_concat'] = Concatenate(
            name='fully_connected_concat')(
            [self.layer['elm_1_dense_2'], self.layer['elm_2_dense_2'], self.layer['elm_3_dense_2']])

        self.layer['fully_connected_reshape'] = Reshape(
            target_shape=(self.fully_connected_num, self.category_num),
            name='fully_connected_reshape')(self.layer['fully_connected_concat'])

        self.layer['fully_connected_merge'] = MergeCategorical(
            categorical_length=self.category_num,
            name='fully_connected_merge')(self.layer['fully_connected_reshape'])

    def get_model(self):
        return load_model(self.network_path, custom_objects={'Scaling': Scaling,
                                                             'Tiling': Tiling,
                                                             'AvgFilter': AvgFilter,
                                                             'MaxFilter': MaxFilter,
                                                             'StdDevFilter': StdDevFilter,
                                                             'Conv2D': Conv2D,
                                                             'MergeCategorical': MergeCategorical,
                                                             'Unifinv': Unifinv})
