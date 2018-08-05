from keras.engine import Layer


class Scaling(Layer):
    def __init__(self, scale_min1, scale_max1, scale_min2, scale_max2, **kwargs):
        self.scale_min1 = float(scale_min1)
        self.scale_max1 = float(scale_max1)
        self.scale_min2 = float(scale_min2)
        self.scale_max2 = float(scale_max2)
        super(Scaling, self).__init__(**kwargs)

    def build(self, input_shape):
        super(Scaling, self).build(input_shape)  # Be sure to call this at the end

    def call(self, x, **kwargs):
        return (((x - self.scale_min1) / (self.scale_max1 - self.scale_min1)) *
                (self.scale_max2 - self.scale_min2)) + self.scale_min2

    def compute_output_shape(self, input_shape):
        return input_shape

    def get_config(self):
        config = {
            'scale_min1': self.scale_min1,
            'scale_max1': self.scale_max1,
            'scale_min2': self.scale_min2,
            'scale_max2': self.scale_max2,
        }
        base_config = super(Scaling, self).get_config()
        return dict(list(base_config.items()) + list(config.items()))
