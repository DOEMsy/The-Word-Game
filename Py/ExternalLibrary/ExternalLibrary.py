GlobalVariable = dict()


def Set(key, value):
    GlobalVariable[key] = value


def Get(key):
    return GlobalVariable.get(key)
