import keras


def to_categorical(y, num_classes=None):
    return keras.utils.to_categorical(y, num_classes=num_classes) * 2 - 1
