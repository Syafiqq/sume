def first_or_default(array, default=''):
    return array if not isinstance(array, list) else array[0] if len(array) > 0 else default


def array_except(array, excepts):
    if not isinstance(array, dict):
        return array
    if not isinstance(excepts, list):
        excepts = [excepts]
    for exp in excepts:
        del array[exp]
    return array
