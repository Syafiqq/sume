import tensorflow as tf


def pad_center(x, num=0, val=0):
    return tf.pad(
        tensor=x,
        paddings=((num, num), (num, num)),
        mode='CONSTANT',
        name=None,
        constant_values=val
    )
