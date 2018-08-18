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


def array_merge(*dict_args):
    if isinstance(dict_args[0], dict):
        result = {}
        for dictionary in dict_args:
            result.update(dictionary)
        return result
    return None
