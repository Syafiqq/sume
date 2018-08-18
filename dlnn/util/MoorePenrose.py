import tensorflow as tf


# https://stackoverflow.com/questions/42501715/alternative-of-numpy-linalg-pinv-in-tensorflow
# https://stackoverflow.com/a/51087168
def pinv1(mtx, reltol=1e-31):
    s, u, v = tf.svd(mtx)
    limit = reltol * tf.reduce_max(s)
    non_zero = tf.greater(s, limit)
    reciprocal = tf.where(non_zero, tf.reciprocal(s), tf.zeros(s.shape))
    lhs = tf.matmul(v, tf.diag(reciprocal))
    return tf.matmul(lhs, u, transpose_b=True)


# https://stackoverflow.com/questions/42501715/alternative-of-numpy-linalg-pinv-in-tensorflow
# https://stackoverflow.com/a/47155138
def pinv2(mtx, reltol=1e-31):
    s, u, v = tf.svd(mtx)
    atol = tf.reduce_max(s) * reltol
    s = tf.boolean_mask(s, s > atol)
    s_inv = tf.diag(1. / s)
    return tf.matmul(v, tf.matmul(s_inv, u, transpose_b=True))


# https://stackoverflow.com/questions/42501715/alternative-of-numpy-linalg-pinv-in-tensorflow
# https://stackoverflow.com/a/44617373
def pinv3(mtx):
    import numpy
    return tf.py_func(numpy.linalg.pinv, [mtx], tf.float32)
