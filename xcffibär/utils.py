'''Utility functions

'''
from collist import collist


class QuitApplication(Exception):
    pass


def xStr(string):
    encoded = string.encode('utf8')
    return len(encoded), encoded


def Perimeter(*args):  # pylint: disable=invalid-name
    if len(args) == 1:
        return (args[0], args[0], args[0], args[0])
    elif len(args) == 2:
        return (args[0], args[1], args[0], args[1])
    elif len(args) == 3:
        return (args[0], args[1], args[2], args[1])
    return (args[0], args[1], args[2], args[3])


def dataAttrs(key, val):
    return key != '__dict__' and not callable(val)


def publicDataAttrs(key, val):
    return not key.startswith('__') and not key.endswith('__') and not callable(val)


def methodAttrs(_key, val):
    return callable(val)


def inspect(obj, attrFilter=publicDataAttrs):
    output = []
    for key in dir(obj):
        val = getattr(obj, key)
        if attrFilter(key, val):
            #print('  %s: %r' % (key, val))
            output.append('  \x1b[96m%s:\x1b[m %r' % (key, val))
    print(collist(output))


def topStrut(width, height):
    return (
        0, 0, height, 0,  # left, right, top, bottom,
        0, 0,             # left_start_y, left_end_y
        0, 0,             # right_start_y, right_end_y,
        0, width,         # top_start_x, top_end_x,
        0, 0              # bottom_start_x, bottom_end_x
    )


def bottomStrut(width, height):
    return (
        0, 0, 0, height,  # left, right, top, bottom,
        0, 0,             # left_start_y, left_end_y
        0, 0,             # right_start_y, right_end_y,
        0, 0,             # top_start_x, top_end_x,
        0, width          # bottom_start_x, bottom_end_x
    )


def leftStrut(width, height):
    return (
        width, 0, 0, 0,  # left, right, top, bottom,
        0, height,       # left_start_y, left_end_y
        0, 0,            # right_start_y, right_end_y,
        0, 0,            # top_start_x, top_end_x,
        0, 0             # bottom_start_x, bottom_end_x
    )


def rightStrut(width, height):
    return (
        0, width, 0, 0,  # left, right, top, bottom,
        0, 0,            # left_start_y, left_end_y
        0, height,       # right_start_y, right_end_y,
        0, 0,            # top_start_x, top_end_x,
        0, 0             # bottom_start_x, bottom_end_x
    )
