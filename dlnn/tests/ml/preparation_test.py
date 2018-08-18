import numpy as np
from keras import Input, Model
from keras import backend as K
from keras.layers import Lambda, Reshape

from dlnn.tests.ml.repos_helper import corpus, corpus_data, corpus_label, normalized, label_init
from dlnn.tests.ml.testcase import TestCase

inputs = Input(shape=(corpus_data.shape[-1],))
scale = Lambda(lambda x: (((x - 0.0) / (300.0 - 0.0)) * (1.0 - 0.0)) + 0.0)(inputs)
reshape = Reshape([1, 1, 4])(scale)
tile = Lambda(lambda x: K.tile(x, (1, 1, 4, 1)))(reshape)


class PreparationTest(TestCase):
    def test_separate_data_and_its_label(self):
        combined = corpus
        _corpus_data, _corpus_label = np.hsplit(combined, [combined.shape[1] - 1])
        self.assertTrue(np.allclose(_corpus_data, corpus_data, rtol=0))
        self.assertTrue(np.allclose(_corpus_label, corpus_label, rtol=0))
        # print(corpus_data, corpus_label)
        self.assertIsNotNone(combined)

    def test_get_formatted_label(self):
        label = corpus_label
        label = label.flatten() - 1
        self.assertTrue(np.allclose(label, label_init, rtol=0))

    def test_defining_input_tensor(self):
        o = Lambda(lambda x: x)(inputs)
        network = Model(inputs=inputs, outputs=o)
        result = network.predict(corpus_data)
        # print(result)
        self.assertIsNotNone(result)

    def test_scaling_value(self):
        network = Model(inputs=inputs, outputs=scale)
        result = network.predict(corpus_data)
        # print(result)
        self.assertIsNotNone(result)

    def test_reshape_data(self):
        network = Model(inputs=inputs, outputs=reshape)
        result = network.predict(corpus_data)
        # print(result)
        self.assertIsNotNone(result)

    def test_tiling_data(self):
        network = Model(inputs=inputs, outputs=tile)
        result = network.predict(corpus_data)
        self.assertTrue(np.allclose(result, normalized, rtol=1e-6))
        # print(result)
        self.assertIsNotNone(result)
