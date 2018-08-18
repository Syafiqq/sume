from keras import backend as K
from keras.engine import Layer


class Tiling(Layer):
    def __init__(self, units, **kwargs):
        self.units = int(units)
        super(Tiling, self).__init__(**kwargs)

    def build(self, input_shape):
        super(Tiling, self).build(input_shape)  # Be sure to call this at the end

    def call(self, x, **kwargs):
        return K.tile(x, (1, 1, self.units, 1))

    def compute_output_shape(self, input_shape):
        return input_shape[0], input_shape[1], self.units, input_shape[3]

    def get_config(self):
        config = {
            'units': self.units,
        }
        base_config = super(Tiling, self).get_config()
        return dict(list(base_config.items()) + list(config.items()))
