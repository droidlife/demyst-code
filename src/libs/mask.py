def mask_value(value):
    return value[0] + "*" * (len(value) - 2) + value[-1]
