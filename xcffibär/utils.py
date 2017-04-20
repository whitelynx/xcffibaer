from collist import collist


class QuitApplication(Exception):
    pass


def xStr(string):
    b = string.encode('utf8')
    return len(b), b


def Perimeter(*args):
    if len(args) == 1:
        return (args[0], args[0], args[0], args[0])
    elif len(args) == 2:
        return (args[0], args[1], args[0], args[1])
    elif len(args) == 3:
        return (args[0], args[1], args[2], args[1])
    else:
        return (args[0], args[1], args[2], args[3])


def dataAttrs(key, val):
    return key != '__dict__' and not callable(val)


def methodAttrs(key, val):
    return callable(val)


def inspect(obj, filter=dataAttrs):
    output = []
    for key in dir(obj):
        val = getattr(obj, key)
        if filter(key, val):
            #print('  %s: %r' % (key, val))
            output.append('  \x1b[96m%s:\x1b[m %r' % (key, val))
    print(collist(output))
