import tensorflow as tf
from keras import backend as K
from keras.engine.topology import Layer


class MergeCategorical(Layer):

    def __init__(self, categorical_length, **kwargs):
        self.categorical_length = categorical_length
        super(MergeCategorical, self).__init__(**kwargs)

    def build(self, input_shape):
        super(MergeCategorical, self).build(input_shape)  # Be sure to call this at the end

    def call(self, x, **kwargs):
        result = K.cast(K.argmax(x), dtype=tf.int32)
        result = tf.map_fn(lambda sub: tf.bincount(sub, minlength=self.categorical_length), result)
        result = K.cast(result, dtype=tf.float32)
        return result

    def compute_output_shape(self, input_shape):
        return input_shape[0], self.categorical_length

    def get_config(self):
        config = {
            'categorical_length': self.categorical_length,
        }
        base_config = super(MergeCategorical, self).get_config()
        return dict(list(base_config.items()) + list(config.items()))
